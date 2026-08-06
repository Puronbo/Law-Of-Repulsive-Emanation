"""Local-only balance flow (the Puno flow dynamics, PPA-001).

Each unit keeps a private home h_i and talks only to its k nearest
neighbours - there is no global mean, no global gradient, no central
controller:

    g_i = -A*(mu0 + mu)*(q_i - h_i)  +  sum_{j in kNN(i)} (q_i - q_j)/|d|^3
    q_i <- clamp(q_i + dt * g_i / |g_i|)

Routing is plain nearest-centroid.  With use_index=True the k-NN queries come
from ExactIndex (grid or cKDTree) and the trajectory is bit-identical to the
exact all-pairs path - asserted by tests/test_puno_flow.py.

mu0 is the always-on private home tether: without it pure local expansion
never slows and the cloud collapses onto the container rim.  mu0 is
dimension-sensitive (0.12 is calibrated for the 2D disk; raise toward 1-4 in
high dimension).
"""

import numpy as np

from .index import ExactIndex

__all__ = ["FlowEngine", "to_disk"]


def to_disk(q, max_r=0.9):
    """Clamp points to a disk of radius max_r (component-free clamp)."""
    q = np.asarray(q, dtype=float)
    r = np.linalg.norm(q, axis=-1)
    over = r > max_r
    if np.any(over):
        q = q.copy()
        q[over] *= (max_r / np.maximum(r[over], 1e-12))[:, None]
    return q


class FlowEngine:
    """Balance network with local-only dynamics.

    Attributes:
        q : (n, dim) unit positions
        h : (n, dim) private homes (identities), one per unit
        k : local neighborhood size (k-NN)
        mu0 : always-on home tether strength
        A : trap scale
        dt : per-unit step size
        max_r : container radius (disk clamp)
        use_index : route k-NN queries through ExactIndex
        index_min_n : minimum population before the index engages
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

    @property
    def n(self):
        return len(self.q)

    def _index(self):
        if not self.use_index or self.n < self.index_min_n:
            return None
        if self.q.shape[1] <= 3:
            return ExactIndex(self.q, k=self.k, algorithm="grid")
        try:
            return ExactIndex(self.q, k=self.k, algorithm="kdtree")
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

    def flow(self, mu=0.0, steps=400):
        """Run `steps` local dynamics steps.  mu is the absorption knob."""
        A = self.A
        m = self.mu0 + mu
        dt = self.dt
        eps = self.eps
        max_r = self.max_r
        for _ in range(steps):
            nb = self._knn()
            q = self.q
            h = self.h
            for i in range(self.n):
                out = q[i] - q[nb[i]]
                r3 = np.maximum(np.linalg.norm(out, axis=-1), eps) ** 3
                rep = (out / r3[:, None]).sum(axis=0)
                g = -A * m * (q[i] - h[i]) + rep
                gm = np.linalg.norm(g) + 1e-9
                q[i] += dt * g / gm
            self.q = to_disk(self.q, max_r)
        return self

    def settle(self, steps=400):
        return self.flow(mu=0.0, steps=steps)

    def absorb(self, steps=400, mu=0.5):
        return self.flow(mu=mu, steps=steps)

    def add(self, x, home=None, settle=False):
        """Insert a unit.  Home defaults to its arrival position x."""
        x = np.asarray(x, dtype=float).reshape(1, -1).copy()
        h = x if home is None else np.asarray(home, dtype=float).reshape(1, -1).copy()
        self.q = x if self.n == 0 else np.vstack([self.q, x])
        self.h = h if len(self.h) == 0 else np.vstack([self.h, h])
        if settle:
            self.settle()
        return self

    def add_many(self, X, homes=None):
        """Bulk-insert many units (homes = X by default)."""
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X[None, :]
        H = X if homes is None else np.asarray(homes, dtype=float)
        if self.n == 0:
            self.q = X.copy()
            self.h = H.copy()
        else:
            self.q = np.vstack([self.q, X])
            self.h = np.vstack([self.h, H])
        return self

    def remove(self, indices):
        """Damage: drop units (and their homes)."""
        self.q = np.delete(self.q, indices, axis=0)
        self.h = np.delete(self.h, indices, axis=0)
        return self

    def heal(self, steps=800):
        """Self-repair: local re-spread of the survivors (no central unit)."""
        return self.settle(steps=steps)

    def spacing(self):
        """Consensus spacing: median over units of mean k-NN distance."""
        if self.n < 2:
            return 0.0
        kk = min(self.k, self.n - 1)
        idx = self._index()
        if idx is not None:
            nb = np.asarray(idx.knn_all(kk))
            means = np.linalg.norm(self.q[:, None, :] - self.q[nb],
                                   axis=-1).mean(axis=1)
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
