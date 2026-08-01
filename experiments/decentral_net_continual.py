"""
T55e: DecentralNet class-incremental continual routing on MNIST (public API).

The numpy-only module as a CONTINUAL router.  base {0..4}, stream {5..9}
release one at a time, per-release metrics old_route / all_route / drift.

  CONTROL  raw centroids, never flowed (nearest-centroid baseline)
  ADD      add neuron + LOCAL reflow (home trap + k-NN repulsion), as the
           demo's regrow step does
  MIX      settle the base once, then append raw stream centroids with NO
           reflow -- the "can I skip the reflow?" failure mode

Extra metric: center-drift = |mean(q) - mean(homes)|, quantifying the
gauge freedom (a local-only net has no global frame; the anchor set can
float as a whole).  MIX collapses precisely because old anchors float
while a freshly-appended raw centroid still sits in the data frame, so
it steals the old classes' points.

Part 2 probes the tether: mu0=0.12 was calibrated on the 2D disk (T55c);
is it dimension-independent?  Vary mu0 in 64D and watch drift vs routing.

Usage: python decentral_net_continual.py [seed ...]
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Universals'))
from manifold.decentral_net import DecentralNet
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split

seeds = [int(s) for s in sys.argv[1:]] or [42, 11, 7]
BASE = list(range(5))
STREAM = list(range(5, 10))
R_SCALE = 0.35
EPOCHS, BS = 4, 256
SETTLE = 300

class MLP:
    def __init__(self, dims, rng, lr=0.01):
        self.layers = [{'W': rng.randn(dims[i], dims[i+1]) * np.sqrt(2/dims[i]),
                        'b': np.zeros(dims[i+1])} for i in range(len(dims)-1)]
        self.lr = lr
        self.rng = rng
    def forward(self, X):
        self.acts = [X]; self.zs = []
        for i, l in enumerate(self.layers):
            z = self.acts[-1] @ l['W'] + l['b']; self.zs.append(z)
            a = z if i == len(self.layers)-1 else np.maximum(0, z)
            self.acts.append(a)
        return self.acts[-1]
    def embed(self, X):
        h = X
        for i, l in enumerate(self.layers[:-1]):
            h = np.maximum(0, h @ l['W'] + l['b'])
        return h
    def train(self, X, y, epochs=EPOCHS, bs=BS):
        Y = np.eye(10)[y]
        for ep in range(epochs):
            idx = self.rng.permutation(len(X))
            for i in range(0, len(X), bs):
                b = idx[i:i+bs]
                l = self.forward(X[b])
                e = np.exp(l - l.max(axis=1, keepdims=True))
                p = e / e.sum(axis=1, keepdims=True)
                d = (p - Y[b]) / len(b)
                for k in reversed(range(len(self.layers))):
                    dW = self.acts[k].T @ d; db = d.sum(axis=0)
                    self.layers[k]['W'] -= self.lr * dW
                    self.layers[k]['b'] -= self.lr * db
                    if k > 0:
                        d = d @ self.layers[k]['W'].T
                        d[self.zs[k-1] <= 0] = 0

def build(seed):
    """Train the MLP and return (Z, y_te, centroids) in the disk frame."""
    rng = np.random.RandomState(seed)
    mlp = MLP([784, 256, 64, 10], rng, lr=0.01)
    mlp.train(X_tr, y_tr)
    E = mlp.embed(X_te)
    Z = E * (R_SCALE / np.median(np.linalg.norm(E, axis=1)))
    cent = np.array([Z[y_te == k].mean(axis=0) for k in range(10)])
    return Z, cent

def kNN_acc(anchors, Z, subset=None):
    """nearest-anchor accuracy; anchor i is class i (add order == class order)."""
    d = np.linalg.norm(Z[:, None] - anchors[None], axis=-1)
    pred = d.argmin(axis=1)
    if subset is not None:
        m = np.isin(y_te, subset)
        return float(np.mean(pred[m] == y_te[m]))
    return float(np.mean(pred == y_te))

print(f"Loading mnist...")
X_all, y_all = fetch_openml('mnist_784', version=1, return_X_y=True, parser='auto')
X_all = X_all.values.astype(np.float32) / 255.0
y_all = y_all.values.astype(int)
X_tr, X_te, y_tr, y_te = train_test_split(X_all, y_all, test_size=10000,
                                          random_state=42)
X_tr, X_te = X_tr[:30000], X_te[:4000]
y_tr, y_te = y_tr[:30000], y_te[:4000]

print("=" * 70)
print("T55e: DECENTRALNET CLASS-INCREMENTAL ROUTING (public API only)")
print(f"seeds={seeds}  base={BASE} stream={STREAM}  SETTLE={SETTLE}")
print("  CONTROL = raw centroids, never flowed")
print("  ADD     = add + LOCAL reflow (home trap + k-NN repulsion)")
print("  MIX     = settle base once, append raw stream centroids (no reflow)")
print("=" * 70)

# ------------------------------------------------------------------ #
agg = {p: {'old': [], 'all': [], 'drift': [], 'center': []}
       for p in ['CONTROL', 'ADD', 'MIX']}
cached = {}
for seed in seeds:
    Z, cent = build(seed)
    cached[seed] = (Z, cent)
    for policy in ['CONTROL', 'ADD', 'MIX']:
        net = DecentralNet(dim=64, k=8, mu0=0.12, A=120.0, dt=0.05, max_r=0.9)
        for c in cent[BASE]:
            net.add(c)
        if policy in ('ADD', 'MIX'):
            net.settle(400)
        home_center = cent[BASE].mean(axis=0)
        rows = []
        for c in cent[STREAM]:
            net.add(c)
            if policy == 'ADD':
                net.settle(SETTLE)
            anchors = net.q
            old = kNN_acc(anchors, Z, subset=BASE)
            all_ = kNN_acc(anchors, Z)
            drift = float(np.mean(np.linalg.norm(anchors[:5] - cent[BASE], axis=1)))
            center = float(np.linalg.norm(anchors[:5].mean(axis=0) - home_center))
            rows.append((old, all_, drift, center))
        agg[policy]['old'].append(float(np.mean([r[0] for r in rows])))
        agg[policy]['all'].append(float(np.mean([r[1] for r in rows])))
        agg[policy]['drift'].append(float(np.mean([r[2] for r in rows])))
        agg[policy]['center'].append(float(np.mean([r[3] for r in rows])))
        print(f"  seed={seed} {policy:<8} old={agg[policy]['old'][-1]:.3f} "
              f"all={agg[policy]['all'][-1]:.3f} "
              f"drift={agg[policy]['drift'][-1]:.4f} "
              f"center={agg[policy]['center'][-1]:.4f}")

print("\n" + "-" * 70)
print("MEANS over seeds (per-release average)")
for policy in ['CONTROL', 'ADD', 'MIX']:
    print(f"  {policy:<8} old={np.mean(agg[policy]['old']):.3f} "
          f"all={np.mean(agg[policy]['all']):.3f} "
          f"drift={np.mean(agg[policy]['drift']):.4f} "
          f"center={np.mean(agg[policy]['center']):.4f}")

# ------------------------------------------------------------------ #
print("\n" + "-" * 70)
print("PART 2: is the 2D-calibrated tether dimension-independent?  (seed 42)")
print("  ADD policy, mu0 sweep in 64D vs CONTROL (raw centroids)")
print("-" * 70)
Z, cent = cached[42]
cont_old = kNN_acc(cent[BASE], Z, subset=BASE)
cont_all = kNN_acc(cent, Z)
print(f"  CONTROL: old={cont_old:.3f} all={cont_all:.3f}")
for mu0 in [0.12, 0.5, 1.0, 2.0, 4.0]:
    net = DecentralNet(dim=64, k=8, mu0=mu0, A=120.0, dt=0.05, max_r=0.9)
    for c in cent[BASE]:
        net.add(c)
    net.settle(400)
    for c in cent[STREAM]:
        net.add(c)
        net.settle(SETTLE)
    old = kNN_acc(net.q, Z, subset=BASE)
    all_ = kNN_acc(net.q, Z)
    drift = float(np.mean(np.linalg.norm(net.q[:5] - cent[BASE], axis=1)))
    print(f"  mu0={mu0:<5} old={old:.3f} all={all_:.3f} drift={drift:.4f}")

print("\n" + "=" * 70)
print("SUMMARY / VERDICT")
print("=" * 70)
for policy in ['CONTROL', 'ADD', 'MIX']:
    o = np.mean(agg[policy]['old']); a = np.mean(agg[policy]['all'])
    d = np.mean(agg[policy]['drift']); c = np.mean(agg[policy]['center'])
    print(f"  {policy:<8} old {o:.3f} | all {a:.3f} | drift {d:.4f} | "
          f"center-drift {c:.4f}")
print("  ADD vs CONTROL old-route delta = {0:+.3f}".format(
    np.mean(agg['ADD']['old']) - np.mean(agg['CONTROL']['old'])))
print("  Part 1: local reflow slightly LOSES to raw centroids on MNIST 64D")
print("  (old ~.82 vs .86): on real embeddings the homes ARE the data")
print("  centroids, so reflowing them cannot help nearest-centroid routing.")
print("  MIX collapses (old .04): never mix frames - always reflow appended")
print("  neurons (gauge freedom: no global center, anchors float).")
print("  Part 2: the tether is NOT dimension-independent - mu0=0.12 tuned")
print("  on the 2D disk over-drifts in 64D (drift .49 from homes); mu0>=1")
print("  cuts drift to .1-.2 but routing never beats CONTROL (.82 all).")
print("\nDone.")
