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
from .ledger import ChainStore, pack_indices, pack_state

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
        self.chains = ChainStore()

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

    def flow(self, mu=0.0, steps=400, record=False):
        """Run `steps` local dynamics steps.  mu is the absorption knob.
        With record=True every unit also appends a state block (position +
        home + the neighbourhood it used) to its own hash-chained ledger."""
        A = self.A
        m = self.mu0 + mu
        dt = self.dt
        eps = self.eps
        max_r = self.max_r
        chains = self.chains
        for _ in range(steps):
            nb = self._knn()
            q = self.q
            h = self.h
            for i in range(self.n):
                out = q[i] - q[nb[i]]                    # outward vectors
                r3 = np.maximum(np.linalg.norm(out, axis=-1), eps) ** 3
                rep = (out / r3[:, None]).sum(axis=0)
                g = -A * m * (q[i] - h[i]) + rep
                gm = np.linalg.norm(g) + 1e-9
                q[i] += dt * g / gm
            self.q = to_disk(self.q, max_r)
            if record:
                for i in range(self.n):
                    chains.record(i, pack_state(self.q[i])
                                     + pack_state(self.h[i])
                                     + pack_indices(nb[i]))
        return self

    def settle(self, steps=400, record=False):
        return self.flow(mu=0.0, steps=steps, record=record)

    def absorb(self, steps=400, mu=0.5, record=False):
        return self.flow(mu=mu, steps=steps, record=record)

    def add(self, x, home=None, settle=False):
        """Insert a unit.  Home defaults to its arrival position x.  Every
        unit's ledger is born with a genesis block over its home."""
        x = np.asarray(x, dtype=float).reshape(1, -1).copy()
        h = x if home is None else np.asarray(home, dtype=float).reshape(1, -1).copy()
        self.q = x if self.n == 0 else np.vstack([self.q, x])
        self.h = h if len(self.h) == 0 else np.vstack([self.h, h])
        self.chains.genesis(self.n - 1, pack_state(self.h[self.n - 1]))
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
        for i in range(self.n - len(X), self.n):
            self.chains.genesis(i, pack_state(self.h[i]))
        return self

    def flow_over(self, edges, mu=0.0, steps=400, record=False):
        """The same local dynamics over a FIXED edge topology instead of
        k-NN: each unit talks only to its graph neighbours.  Neighbourhoods
        are read once and held fixed while the cloud relaxes, so scale-free
        wiring (puno_flow.topology) gives the same formula hubs-and-spokes
        power-law neighbourhoods.  Undirected; self-loops ignored."""
        A = self.A
        m = self.mu0 + mu
        dt = self.dt
        eps = self.eps
        max_r = self.max_r
        chains = self.chains
        n = self.n
        neigh = [[] for _ in range(n)]
        for u, v in np.asarray(edges, dtype=int):
            if u != v and 0 <= u < n and 0 <= v < n:
                neigh[u].append(int(v))
                neigh[v].append(int(u))
        nb = [np.unique(np.asarray(x, dtype=int)) for x in neigh]
        for _ in range(steps):
            q = self.q
            h = self.h
            for i in range(n):
                ni = nb[i]
                if len(ni) == 0:
                    g = -A * m * (q[i] - h[i])
                else:
                    out = q[i] - q[ni]
                    r3 = np.maximum(np.linalg.norm(out, axis=-1), eps) ** 3
                    rep = (out / r3[:, None]).sum(axis=0)
                    g = -A * m * (q[i] - h[i]) + rep
                gm = np.linalg.norm(g) + 1e-9
                q[i] += dt * g / gm
            self.q = to_disk(self.q, max_r)
            if record:
                for i in range(n):
                    chains.record(i, pack_state(self.q[i])
                                     + pack_state(self.h[i])
                                     + pack_indices(nb[i]))
        return self

    def create(self, x, home=None, parent=None, settle=False):
        """Creation: spawn a new unit.  Its genesis block (written by add)
        records its home; parent (int) optionally adds a provenance block
        naming the unit that created it.  Returns the new unit's index."""
        idx = self.n
        self.add(x, home=home, settle=settle)
        if parent is not None:
            self.chains.record(idx, pack_indices([int(parent)]))
        return idx

    def spawn(self, count, spread=0.02, rng=None):
        """Creation at scale: spawn `count` new units around existing units'
        homes (GNG-style local growth).  Returns the new units' indices."""
        rng = np.random.RandomState(7) if rng is None else rng
        if self.n == 0:
            raise ValueError("spawn needs at least one existing unit")
        base = self.h if len(self.h) else self.q
        dim = self.q.shape[1]
        created = []
        for _ in range(count):
            j = int(rng.randint(0, len(base)))
            x = base[j] + rng.randn(dim) * spread
            created.append(self.create(x, parent=j))
        return created

    def search(self, X, k=None):
        """Search engine over the unit population: for each query point, the
        k nearest units ranked by ascending distance.  Returns (indices,
        distances) - for a single query, 1-D arrays."""
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X[None, :]
        k = min(self.k if k is None else int(k), self.n)
        D = np.linalg.norm(X[:, None, :] - self.q[None, :, :], axis=-1)
        order = np.argsort(D, axis=1)[:, :k]
        dist = np.take_along_axis(D, order, axis=1)
        if X.shape[0] == 1:
            return order[0], dist[0]
        return order, dist

    def search_by_identity(self, home, k=None):
        """Search the units' homes (their private identities): the k nearest
        units to a query identity.  Returns (indices, distances)."""
        home = np.asarray(home, dtype=float)
        k = min(self.k if k is None else int(k), self.n)
        D = np.linalg.norm(self.h - home, axis=-1)
        order = np.argsort(D)[:k]
        return order, D[order]

    def consensus(self):
        """Local agreement: mean reciprocity of the k-NN graph - the fraction
        of a unit's neighbours that also list it among theirs.  1.0 means every
        link is mutual.  In the toy network, agreement is verified locally,
        not mined."""
        n = self.n
        if n < 2:
            return 1.0
        kk = min(self.k, n - 1)
        idx = self._index()
        if idx is not None:
            nb = np.asarray(idx.knn_all(kk))
        else:
            D = np.linalg.norm(self.q[:, None] - self.q[None], axis=-1)
            np.fill_diagonal(D, np.inf)
            nb = np.argsort(D, axis=1)[:, :kk]
        mutual = 0
        total = 0
        for i in range(n):
            for j in nb[i]:
                total += 1
                if i in nb[j]:
                    mutual += 1
        return mutual / total if total else 1.0

    def verify_ledger(self):
        """Audit every unit's chain: (ok, first_bad_unit, first_bad_seq)."""
        return self.chains.verify_all()

    def chain_head(self, i):
        """The current head hash of unit i's ledger."""
        return self.chains.head(i)

    def ledger_audit(self):
        """Summary of the local ledgers: chain count, total blocks, heads."""
        return self.chains.audit()

    def status(self):
        """Compact snapshot: population, geometry, agreement, ledger."""
        return {
            "n": self.n,
            "dim": self.q.shape[1] if self.q.size else None,
            "k": self.k,
            "spacing": self.spacing() if self.n > 1 else 0.0,
            "consensus": self.consensus(),
            "ledger_chains": len(self.chains.chains),
            "ledger_blocks": sum(c.length for c in self.chains.chains.values()),
        }

    def remove(self, indices):
        """Damage: drop units (and their homes)."""
        self.q = np.delete(self.q, indices, axis=0)
        self.h = np.delete(self.h, indices, axis=0)
        return self

    def heal(self, steps=800, record=False):
        """Self-repair: local re-spread of the survivors (no central unit)."""
        return self.settle(steps=steps, record=record)

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
