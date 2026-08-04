"""
DecentralNet - a numpy-only, fully independent toy neural network whose units
("neurons") update from LOCAL information alone.

Each neuron keeps a private HOME h_i (its identity: where it arrived / its
class centroid) and talks only to its k nearest neighbours.  There is NO
global mean, NO global gradient, NO central controller:

    g_i = -A*(mu0 + mu)*(q_i - h_i)  +  sum_{j in kNN(i)} (q_i - q_j)/|d|^3
    q_i <- clamp(q_i + dt * g_i / |g_i|)

Routing is plain nearest-centroid: label(x) = argmin_i |x - q_i|.

No imports beyond numpy (the fast index path, use_index=True, lazily uses
scipy.cKDTree for dim >= 4; the dim <= 3 grid path is numpy-only).  Run
directly for a self-contained demonstration (`python decentral_net.py`) or
import it from anywhere:

    from manifold.decentral_net import DecentralNet
    net = DecentralNet(dim=2, k=8, mu0=0.12)
    net.add(np.array([0.1, 0.2]))    # new neuron, home = arrival position
    net.settle(400)                  # local relaxation (mu = 0)
    net.absorb(400)                  # tighten toward homes (mu = 0.5)
    net.heal(800)                    # re-spread survivors after neuron loss
    net.predict(X); net.accuracy(X, y)

Spatial index (T67): the exact path builds an n x n distance matrix per
flow step - O(n^2) memory and time, which caps the population at ~10^4.
With use_index=True the same k-NN sets come from a spatial index instead:
a uniform grid (dim <= 3, O(1)-expected per-neuron queries, exact) or
scipy.cKDTree (any dim, O(log n) per query, exact).  Results are identical
to the exact path (both return true k-NN), so indexed flow is not an
approximation - it is the same dynamics with a sub-quadratic neighbour
search, which is what unlocks flowing internet-scale populations (T67).
Off by default: every existing experiment keeps the exact path unchanged.

Why mu0 exists: a private always-on home tether is required, otherwise pure
local expansion never slows (per-neuron steps) and the cloud collapses onto
the container rim.  See experiments/decentral_net.py (T55c) for the full
multi-seed benchmark and verdict.

Caveats (T55e, experiments/decentral_net_continual.py):
  1. NEVER mix frames: after removing/add-ing neurons, always reflow the net
     (settle/absorb) before routing.  A fresh point appended to a floated
     anchor set sits in the data frame and steals the old classes' points
     (routing collapses ~0.86 -> ~0.04).  The demo's regrow loop reflows.
  2. The dynamics have gauge freedom (no global center): the anchor set can
     float as a whole.  When homes ARE the data centroids, reflow slightly
     LOSES to plain nearest-centroid routing - the flow buys a consistent
     frame, not accuracy.
  3. mu0/A are dimension-sensitive: mu0=0.12 is calibrated for the 2D disk;
     in 64D it over-drifts anchors ~0.5 from their homes.  Raise mu0 with
     the dimension (mu0 ~ 1-4 in 64D) to reduce drift.
"""

import itertools

import numpy as np

__all__ = ["DecentralNet", "to_disk"]


def to_disk(q, max_r=0.9):
    """Clamp points to a disk of radius max_r (component-free clamp)."""
    q = np.asarray(q, dtype=float)
    r = np.linalg.norm(q, axis=-1)
    over = r > max_r
    if np.any(over):
        q = q.copy()
        q[over] *= (max_r / np.maximum(r[over], 1e-12))[:, None]
    return q


class _GridIndex:
    """Uniform-grid k-NN for dim <= 3: O(1)-expected per-neuron queries (T67).

    The domain is bucketed into cells whose size tracks the current point
    density (a few points per cell), so a query finds its k neighbours by
    scanning a small expanding ring of cells.  The ring grows until k
    candidates are found, which makes the result EXACT for any set - it is
    only the *expected* work per query that is constant, not the answer.
    """

    def __init__(self, pts, k=8, cell=None):
        self.pts = np.asarray(pts, dtype=float)
        self.dim = self.pts.shape[1]
        self.n = self.pts.shape[0]
        lo = self.pts.min(axis=0)
        hi = self.pts.max(axis=0)
        span = np.maximum(hi - lo, 1e-12)
        if cell is None:
            vol = span.prod()
            cell = max((vol * max(k, 1) / max(self.n, 1)) ** (1.0 / self.dim), 1e-9)
        self.cell = cell
        self.origin = lo - 0.5 * cell
        self.ni = np.maximum(np.ceil((span + cell) / cell).astype(int), 1)
        ci = np.floor((self.pts - self.origin) / cell).astype(int)
        self.idx = np.clip(ci, 0, self.ni - 1)
        self.cells = {}
        for i in range(self.n):
            self.cells.setdefault(tuple(self.idx[i]), []).append(i)

    def _scan(self, x, ci, k=1, drop=-1):
        """All points in cells within the smallest Chebyshev ring r such that
        the k-th nearest candidate is provably closer than every point in an
        unscanned cell (min distance to a ring-(r+1) cell is >= r*cell)."""
        cand, seen = [], set()
        for r in range(0, int(self.ni.max())):
            for off in itertools.product(range(-r, r + 1), repeat=self.dim):
                cc = tuple(ci[d] + off[d] for d in range(self.dim))
                if cc in seen:
                    continue
                seen.add(cc)
                for j in self.cells.get(cc, ()):
                    if j != drop:
                        cand.append(j)
            if len(cand) < k:
                continue
            c = np.asarray(cand, dtype=int)
            d = np.linalg.norm(self.pts[c] - x, axis=-1)
            order = np.argsort(d)
            if d[order[k - 1]] <= r * self.cell:
                return c[order]
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


class _KDTreeIndex:
    """Exact k-NN for dim >= 4 via scipy.cKDTree: O(log n) per query (T67)."""

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


class DecentralNet:
    """Balance network with local-only dynamics.

    Attributes:
        q : (n, dim) neuron positions (the "weights")
        h : (n, dim) private homes (identities), one per neuron
        k : local neighborhood size (k-NN)
        mu0 : always-on home tether strength
        A  : trap scale
        dt : per-neuron step size
        max_r : container radius (disk clamp)
    """

    def __init__(self, dim=2, k=8, mu0=0.12, A=120.0, dt=0.05, max_r=0.9,
                 eps=1e-3, use_index=False, index_min_n=512):
        self.q = np.zeros((0, dim))
        self.h = np.zeros((0, dim))
        self.k = k
        self.mu0 = mu0
        self.A = A
        self.dt = dt
        self.max_r = max_r
        self.eps = eps
        self.use_index = use_index
        self.index_min_n = index_min_n

    # ------------------------------------------------------------------ #
    @property
    def n(self):
        return len(self.q)

    def _index(self):
        """Spatial index over the CURRENT q (T67): O(1)-expected grid for
        dim <= 3, exact cKDTree for higher dims.  Returns None when the
        index is disabled or the population is too small for it to pay."""
        if not self.use_index or self.n < self.index_min_n:
            return None
        if self.q.shape[1] <= 3:
            return _GridIndex(self.q, k=self.k)
        try:
            return _KDTreeIndex(self.q)
        except ImportError:
            return None

    def _knn(self):
        n = self.n
        if n <= 1:
            return [np.zeros(0, dtype=int)] * n
        kk = min(self.k, n - 1)
        idx = self._index()
        if idx is not None:
            return idx.knn_all(kk)
        D = np.linalg.norm(self.q[:, None] - self.q[None], axis=-1)
        np.fill_diagonal(D, np.inf)
        return list(np.argsort(D, axis=1)[:, :kk])

    # ------------------------------------------------------------------ #
    def flow(self, mu=0.0, steps=400):
        """Run `steps` local dynamics steps.  mu is the absorption knob."""
        for _ in range(steps):
            nb = self._knn()
            for i in range(self.n):
                out = self.q[i] - self.q[nb[i]]              # outward vectors
                r3 = np.maximum(np.linalg.norm(out, axis=-1), self.eps) ** 3
                rep = (out / r3[:, None]).sum(axis=0) if len(nb[i]) else 0.0
                g = -self.A * (self.mu0 + mu) * (self.q[i] - self.h[i]) + rep
                gm = np.linalg.norm(g) + 1e-9
                self.q[i] += self.dt * g / gm
            self.q = to_disk(self.q, self.max_r)
        return self

    def settle(self, steps=400):
        return self.flow(mu=0.0, steps=steps)

    def absorb(self, steps=400, mu=0.5):
        return self.flow(mu=mu, steps=steps)

    # ------------------------------------------------------------------ #
    def add(self, x, home=None, settle=False):
        """Insert a neuron.  Home defaults to its arrival position x."""
        x = np.asarray(x, dtype=float).reshape(1, -1)
        h = x if home is None else np.asarray(home, dtype=float).reshape(1, -1)
        self.q = x if self.n == 0 else np.vstack([self.q, x])
        self.h = h if len(self.h) == 0 else np.vstack([self.h, h])
        if settle:
            self.settle()
        return self

    def add_many(self, X, homes=None):
        """Bulk-insert many neurons at once (vectorized; homes = X by
        default).  For loading large populations without a per-neuron loop."""
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X[None, :]
        H = X if homes is None else np.asarray(homes, dtype=float)
        if self.n == 0:
            self.q, self.h = X, H
        else:
            self.q = np.vstack([self.q, X])
            self.h = np.vstack([self.h, H])
        return self

    def remove(self, indices):
        """Damage: drop neurons (and their homes)."""
        self.q = np.delete(self.q, indices, axis=0)
        self.h = np.delete(self.h, indices, axis=0)
        return self

    def heal(self, steps=800):
        """Self-repair: local re-spread of the survivors (no central unit)."""
        return self.settle(steps=steps)

    # ------------------------------------------------------------------ #
    def spacing(self):
        """Consensus spacing: median over neurons of mean k-NN distance."""
        if self.n < 2:
            return 0.0
        kk = min(self.k, self.n - 1)
        idx = self._index()
        if idx is not None:
            nb = idx.knn_all(kk)
            means = np.array([np.linalg.norm(self.q[i] - self.q[nb[i]],
                                             axis=-1).mean() for i in range(self.n)])
            return float(np.median(means))
        D = np.linalg.norm(self.q[:, None] - self.q[None], axis=-1)
        np.fill_diagonal(D, np.inf)
        return float(np.median(np.sort(D, axis=1)[:, :kk].mean(axis=1)))

    def predict(self, X):
        """Nearest-centroid labels."""
        X = np.asarray(X, dtype=float)
        idx = self._index()
        if idx is not None:
            return idx.nearest(X)
        D = np.linalg.norm(X[:, None, :] - self.q[None, :, :], axis=-1)
        return np.argmin(D, axis=1)

    def accuracy(self, X, y):
        return float(np.mean(self.predict(X) == np.asarray(y)))


# ---------------------------------------------------------------------- #
def _demo(seed=7, n_classes=12, noise=0.05):
    rng = np.random.RandomState(seed)
    net = DecentralNet(dim=2, k=8, mu0=0.12)

    # class identities: homes on a circle (each neuron's private reference)
    th = np.linspace(0, 2 * np.pi, n_classes, endpoint=False)
    homes = np.column_stack([0.35 * np.cos(th), 0.35 * np.sin(th)])
    for h in homes:
        net.add(h)          # neuron arrives at its home, identity = home
    net.settle(800)

    def probe(subset=None):
        # self-consistent test set: one cloud around each CURRENT neuron
        X = np.vstack([net.q[j] + rng.randn(200, 2) * noise for j in range(net.n)])
        y = np.repeat(np.arange(net.n), 200)
        if subset is not None:
            m = np.isin(y, subset); X, y = X[m], y[m]
        return net.accuracy(X, y)

    acc_grown = probe()
    net.absorb(400)                                     # tighten to homes
    acc_tight = probe()

    # damage: kill the first 4 neurons, then measure the SURVIVORS
    net.remove(list(range(4)))
    acc_surv = probe()
    spread_before = net.spacing()
    net.heal(800)                                       # local re-spread
    acc_healed = probe()
    spread_after = net.spacing()

    # regrow: re-populate the empty homes (GNG-style insertion)
    for j in range(4):
        net.add(homes[j]); net.absorb(300)
    acc_regrown = probe()

    print("=" * 62)
    print("DecentralNet standalone demo (numpy only, no repo imports)")
    print("=" * 62)
    print(f"  {n_classes} classes on a circle, 200 pts/class, noise={noise}")
    print(f"  grown shell (local settle)   accuracy {acc_grown:.3f}")
    print(f"  after absorb (tight to home) accuracy {acc_tight:.3f}")
    print(f"  after killing 4 neurons      accuracy {acc_surv:.3f} (survivors)")
    print(f"  after local heal             accuracy {acc_healed:.3f}"
          f"  spacing {spread_before:.3f} -> {spread_after:.3f}")
    print(f"  after regrow 4 (fresh homes) accuracy {acc_regrown:.3f}")
    print("  (self-healing: no central repair unit - local settle + regrowth)")
    print(f"\nDone.")


if __name__ == "__main__":
    _demo()
