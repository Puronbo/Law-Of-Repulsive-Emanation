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


def brute_knn(X, k):
    """All-pairs reference: (sorted) k-NN indices per point, self excluded."""
    n = len(X)
    D = np.linalg.norm(X[:, None] - X[None], axis=-1)
    np.fill_diagonal(D, np.inf)
    kk = min(k, n - 1)
    order = np.argsort(D, axis=1)[:, :kk]
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
        self.cell = cell
        self.origin = lo - 0.5 * cell
        self.ni = np.maximum(np.ceil((span + cell) / cell).astype(int), 1)
        ci = np.floor((self.pts - self.origin) / cell).astype(int)
        self.idx = np.clip(ci, 0, self.ni - 1)
        self.cells = {}
        for i in range(self.n):
            self.cells.setdefault(tuple(self.idx[i]), []).append(i)
        self.ring_offsets = []
        for r in range(int(self.ni.max())):
            offs = [off for off in itertools.product(
                range(-r, r + 1), repeat=self.dim)
                if max(abs(o) for o in off) == r]
            self.ring_offsets.append(offs)

    def _scan(self, x, ci, k=1, drop=-1):
        dim = self.dim
        cells = self.cells
        cand = []
        for r, offs in enumerate(self.ring_offsets):
            for off in offs:
                cc = tuple(ci[d] + off[d] for d in range(dim))
                for j in cells.get(cc, ()):
                    if j != drop:
                        cand.append(j)
            if len(cand) < k:
                continue
            c = np.asarray(cand, dtype=int)
            d = np.linalg.norm(self.pts[c] - x, axis=-1)
            if np.partition(d, k - 1)[k - 1] <= r * self.cell:
                return c[np.argsort(d)]
        c = np.asarray(cand, dtype=int)
        d = np.linalg.norm(self.pts[c] - x, axis=-1)
        return c[np.argsort(d)]

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
        _, nb = self.tree.query(self.pts, k=k + 1, workers=-1)
        nb = np.asarray(nb)
        if nb.ndim == 1:
            nb = nb[:, None]
        return [nb[i, 1:].astype(int) for i in range(nb.shape[0])]

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
        _, nb = self._index.tree.query(self.pts[i], k=k + 1, workers=-1)
        nb = np.asarray(nb)
        if nb.ndim == 1:
            nb = nb[:, None]
        return nb[0, 1:].astype(int)

    def knn_all(self, k=None):
        k = self.k if k is None else k
        return self._index.knn_all(k)

    def nearest(self, X):
        return self._index.nearest(np.asarray(X, dtype=float))
