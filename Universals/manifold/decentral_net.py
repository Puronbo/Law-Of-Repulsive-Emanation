"""
DecentralNet - a numpy-only, fully independent toy neural network whose units
("neurons") update from LOCAL information alone.

Each neuron keeps a private HOME h_i (its identity: where it arrived / its
class centroid) and talks only to its k nearest neighbours.  There is NO
global mean, NO global gradient, NO central controller:

    g_i = -A*(mu0 + mu)*(q_i - h_i)  +  sum_{j in kNN(i)} (q_i - q_j)/|d|^3
    q_i <- clamp(q_i + dt * g_i / |g_i|)

Routing is plain nearest-centroid: label(x) = argmin_i |x - q_i|.

No imports beyond numpy.  Run directly for a self-contained demonstration
(`python decentral_net.py`) or import it from anywhere:

    from manifold.decentral_net import DecentralNet
    net = DecentralNet(dim=2, k=8, mu0=0.12)
    net.add(np.array([0.1, 0.2]))    # new neuron, home = arrival position
    net.settle(400)                  # local relaxation (mu = 0)
    net.absorb(400)                  # tighten toward homes (mu = 0.5)
    net.heal(800)                    # re-spread survivors after neuron loss
    net.predict(X); net.accuracy(X, y)

Why mu0 exists: a private always-on home tether is required, otherwise pure
local expansion never slows (per-neuron steps) and the cloud collapses onto
the container rim.  See experiments/decentral_net.py (T55c) for the full
multi-seed benchmark and verdict.
"""

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

    def __init__(self, dim=2, k=8, mu0=0.12, A=120.0, dt=0.05, max_r=0.9, eps=1e-3):
        self.q = np.zeros((0, dim))
        self.h = np.zeros((0, dim))
        self.k = k
        self.mu0 = mu0
        self.A = A
        self.dt = dt
        self.max_r = max_r
        self.eps = eps

    # ------------------------------------------------------------------ #
    @property
    def n(self):
        return len(self.q)

    def _knn(self):
        n = self.n
        if n <= 1:
            return [np.zeros(0, dtype=int)] * n
        D = np.linalg.norm(self.q[:, None] - self.q[None], axis=-1)
        np.fill_diagonal(D, np.inf)
        kk = min(self.k, n - 1)
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
        D = np.linalg.norm(self.q[:, None] - self.q[None], axis=-1)
        np.fill_diagonal(D, np.inf)
        kk = min(self.k, self.n - 1)
        return float(np.median(np.sort(D, axis=1)[:, :kk].mean(axis=1)))

    def predict(self, X):
        """Nearest-centroid labels."""
        X = np.asarray(X, dtype=float)
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
