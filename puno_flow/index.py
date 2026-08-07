"""Exact nearest-neighbor search: grid for dim <= 3, scipy.cKDTree above.

The grid answers k-NN queries by scanning an expanding Chebyshev ring until
the k-th candidate is provably closer than every point in an unscanned cell
(min distance to a ring-(r+1) cell is >= r * cell).  The result is EXACT for
any point set - only the expected work per query is constant, never the
answer.  This is the T67 index that unlocks flowing populations the all-pairs
path physically cannot touch.
"""

import itertools

import numpy as np

__all__ = ["ExactIndex", "brute_knn"]

# Per-dimension grid cell cap: keeps the ring scan bounded even for
# degenerate (near-zero-volume) point sets; never affects correctness.
_MAX_NI = 512


def brute_knn(X, k):
    """All-pairs reference: (sorted) k-NN indices per point, self excluded.

    Ties are broken canonically by ascending index (stable argsort), so the
    result is deterministic even for exactly duplicated points.
    """
    n = len(X)
    D = np.linalg.norm(X[:, None] - X[None], axis=-1)
    np.fill_diagonal(D, np.inf)
    kk = min(k, n - 1)
    order = np.argsort(D, axis=1, kind="stable")[:, :kk]
    return [np.asarray(order[i], dtype=int) for i in range(n)]


class _Grid:
    def __init__(self, pts, k=8, cell=None):
        self.pts = np.asarray(pts, dtype=float)
        self.dim = self.pts.shape[1]
        self.n = self.pts.shape[0]
        lo = self.pts.min(axis=0)
        hi = self.pts.max(axis=0)
        span = np.maximum(hi - lo, 1e-12)
        if cell is None:
            vol = span.prod()
            cell = max((vol * max(k, 1) / max(self.n, 1)) ** (1.0 / self.dim),
                       1e-9)
        # Clamp the per-dimension cell count: a near-degenerate span (e.g.
        # collinear points) makes the volume formula tiny, which would blow
        # up the number of grid cells (and with it the ring scan).  The grid
        # stays exact for any cell size; the clamp only bounds the work.
        self.cell = max(float(cell), float(span.max()) / _MAX_NI)
        self.origin = lo - 0.5 * self.cell
        self.ni = np.maximum(
            np.ceil((span + self.cell) / self.cell).astype(int), 1)
        self.ni = np.minimum(self.ni, _MAX_NI + 1)
        ci = np.floor((self.pts - self.origin) / self.cell).astype(int)
        self.idx = np.clip(ci, 0, self.ni - 1)
        self._rings = []   # lazily built Chebyshev rings (cache)
        strides = np.ones(self.dim, dtype=int)
        for d in range(self.dim - 2, -1, -1):
            strides[d] = strides[d + 1] * self.ni[d + 1]
        self._strides = strides
        cid = np.ravel_multi_index(self.idx.T, self.ni)
        order = np.argsort(cid, kind="stable")
        self.order = order
        sc = cid[order]
        uniq, starts = np.unique(sc, return_index=True)
        ends = np.append(starts[1:], self.n)
        self._slices = dict(zip(uniq.tolist(),
                                zip(starts.tolist(), ends.tolist())))

    def _ring(self, r):
        """Chebyshev ring of radius r as offsets, built on demand."""
        while len(self._rings) <= r:
            rr = len(self._rings)
            self._rings.append([off for off in itertools.product(
                range(-rr, rr + 1), repeat=self.dim)
                if max(abs(o) for o in off) == rr])
        return self._rings[r]

    def _scan(self, x, ci, k=1, drop=-1):
        if k <= 0:
            return np.zeros(0, dtype=int)
        dim = self.dim
        nix = self.ni
        strides = self._strides
        slices = self._slices
        order = self.order
        pts = self.pts
        cell = self.cell
        cand = []
        tot = 0
        for r in range(int(nix.max())):
            for off in self._ring(r):
                cid = 0
                ok = True
                for d in range(dim):
                    c = ci[d] + off[d]
                    if not (0 <= c < nix[d]):
                        ok = False
                        break
                    cid += c * strides[d]
                if ok:
                    s, e = slices.get(cid, (0, 0))
                    if s < e:
                        cand.append(order[s:e])
                        tot += e - s
            if tot < k:
                continue
            c = np.concatenate(cand)
            if drop >= 0:
                c = c[c != drop]
            if len(c) < k:
                continue
            d = np.linalg.norm(pts[c] - x, axis=-1)
            if np.partition(d, k - 1)[k - 1] <= r * cell:
                # canonical order: distance, then index (deterministic ties)
                return c[np.lexsort((c, d))]
        c = np.concatenate(cand)
        if drop >= 0:
            c = c[c != drop]
        d = np.linalg.norm(pts[c] - x, axis=-1)
        return c[np.lexsort((c, d))]

    def knn(self, i, k):
        x = self.pts[i]
        c = self._scan(x, tuple(self.idx[i]), k, drop=i)
        return c[:k] if len(c) > k else c

    def knn_all(self, k):
        return [self.knn(i, k) for i in range(self.n)]

    def nearest(self, X):
        out = np.empty(len(X), dtype=int)
        for r0, x in enumerate(X):
            xc = tuple(np.clip(
                np.floor((x - self.origin) / self.cell).astype(int),
                0, self.ni - 1).tolist())
            c = self._scan(x, xc, 1)
            d = np.linalg.norm(self.pts[c] - x, axis=-1)
            out[r0] = c[np.argmin(d)]
        return out


class _KDTree:
    def __init__(self, pts):
        from scipy.spatial import cKDTree
        self.pts = np.asarray(pts, dtype=float)
        self.tree = cKDTree(self.pts)

    def knn_all(self, k):
        d, nb = self.tree.query(self.pts, k=k + 1, workers=-1)
        nb = np.asarray(nb)
        d = np.asarray(d)
        if nb.ndim == 1:
            nb = nb[:, None]
            d = d[:, None]
        out = []
        for i in range(nb.shape[0]):
            row = nb[i]
            rd = d[i]
            # drop self and any out-of-range padding (scipy pads with n)
            m = (row != i) & (row < len(self.pts))
            row, rd = row[m], rd[m]
            o = np.lexsort((row, rd))       # canonical: distance, then index
            out.append(row[o][:k].astype(int))
        return out

    def nearest(self, X):
        _, nb = self.tree.query(np.asarray(X, dtype=float), k=1)
        return np.atleast_1d(nb).astype(int)


class ExactIndex:
    """Exact k-NN index: uniform grid (dim <= 3) or scipy.cKDTree (dim >= 4).

    Both paths return true k-NN sets (identical to brute force); the index
    only changes the work, never the answer.
    """

    def __init__(self, pts, k=8, cell=None, algorithm="auto"):
        self.pts = np.asarray(pts, dtype=float)
        self.k = k
        self.dim = self.pts.shape[1]
        if algorithm == "auto":
            algorithm = "grid" if self.dim <= 3 else "kdtree"
        self.algorithm = algorithm
        if algorithm == "grid":
            if self.dim > 3:
                raise ValueError("grid index is exact only for dim <= 3 "
                                 f"(got dim={self.dim}); use algorithm='kdtree'")
            self._index = _Grid(self.pts, k=k, cell=cell)
        elif algorithm == "kdtree":
            self._index = _KDTree(self.pts)
        else:
            raise ValueError(f"unknown algorithm: {algorithm}")

    @property
    def n(self):
        return len(self.pts)

    def knn(self, i, k=None):
        k = self.k if k is None else k
        if isinstance(self._index, _Grid):
            return self._index.knn(i, k)
        d, nb = self._index.tree.query(self.pts[i], k=k + 1, workers=-1)
        nb = np.asarray(nb).ravel()
        d = np.asarray(d).ravel()
        m = (nb != i) & (nb < len(self.pts))
        nb, d = nb[m], d[m]
        o = np.lexsort((nb, d))
        return nb[o][:k].astype(int)

    def knn_all(self, k=None):
        k = self.k if k is None else k
        return self._index.knn_all(k)

    def nearest(self, X):
        return self._index.nearest(np.asarray(X, dtype=float))
