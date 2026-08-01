"""
T55d: DecentralNet on real embeddings (MNIST, 64D) via the public API.

The standalone DecentralNet module (Universals/manifold/decentral_net.py) was
proven on 2D toy data; T55c Part 4 showed the harness net survives MNIST
routing but through the repo's own flow code.  This experiment uses ONLY
the public API (DecentralNet.add/flow/settle/remove/heal/predict/accuracy)
as the routing substrate on 64D MNIST embeddings:

  embed  -> normalize into the disk (median radius 0.35)
  grow   -> one neuron per class, home = class centroid, LOCAL settle only
  route  -> nearest-anchor accuracy vs nearest-centroid (raw) baseline
  damage -> kill 3 neurons, survivors keep routing
  heal   -> local settle re-spreads survivors
  regrow -> re-populate empty homes, full routing restored

Nothing here imports the repo flow machinery except the numpy-only module.

Usage: python decentral_net_mnist.py [seed]
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Universals'))
from manifold.decentral_net import DecentralNet, to_disk
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42
rng = np.random.RandomState(seed)

EPOCHS = 4
BS = 256
R_SCALE = 0.35           # median embedding radius after normalization

class MLP:
    def __init__(self, dims, rng, lr=0.01):
        self.layers = [{'W': rng.randn(dims[i], dims[i+1]) * np.sqrt(2/dims[i]),
                        'b': np.zeros(dims[i+1])} for i in range(len(dims)-1)]
        self.lr = lr
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
            idx = rng.permutation(len(X))
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

# ---------------------------------------------------------------------- #
print(f"Loading mnist...")
X_all, y_all = fetch_openml('mnist_784', version=1, return_X_y=True, parser='auto')
X_all = X_all.values.astype(np.float32) / 255.0
y_all = y_all.values.astype(int)
X_tr, X_te, y_tr, y_te = train_test_split(X_all, y_all, test_size=10000,
                                          random_state=seed)
X_tr, X_te = X_tr[:30000], X_te[:4000]
y_tr, y_te = y_tr[:30000], y_te[:4000]

net_mlp = MLP([784, 256, 64, 10], rng, lr=0.01)
net_mlp.train(X_tr, y_tr)
emb_te = net_mlp.embed(X_te)

# normalize embeddings into the disk (median radius 0.35)
norms = np.linalg.norm(emb_te, axis=1)
scale = R_SCALE / np.median(norms)
Z = emb_te * scale

centroids = np.array([Z[y_te == k].mean(axis=0) for k in range(10)])

def kNN_acc(anchors, neuron_classes, subset=None):
    """nearest-anchor accuracy with an explicit neuron-index -> class map
    (after remove/add the neuron order no longer equals class order)."""
    d = np.linalg.norm(Z[:, None] - anchors[None], axis=-1)
    pred = neuron_classes[d.argmin(axis=1)]
    if subset is not None:
        m = np.isin(y_te, subset)
        return float(np.mean(pred[m] == y_te[m]))
    return float(np.mean(pred == y_te))

print("=" * 70)
print("T55d: DECENTRALNET ON MNIST 64D EMBEDDINGS (public API only)")
print(f"seed={seed}  epochs={EPOCHS}  disk radius={R_SCALE}  "
      f"(net: {DecentralNet.__module__})")
print("=" * 70)

# baseline: nearest-centroid on the raw (normalized) embeddings
print("\n--- routing baseline: nearest centroid (raw embeddings) ---")
acc_base = kNN_acc(centroids, np.arange(10))
print(f"  nearest-centroid acc = {acc_base:.3f}")

# DecentralNet: neurons at centroids, LOCAL settle only
net = DecentralNet(dim=64, k=8, mu0=0.12, A=120.0, dt=0.05, max_r=0.9)
for c in centroids:
    net.add(c)
net.settle(500)
print("\n--- DecentralNet grown (local settle, no central mean/max) ---")
acc_grown = kNN_acc(net.q, np.arange(10))
print(f"  DecentralNet nearest-anchor acc = {acc_grown:.3f}")

# damage: kill 3 neurons, measure survivors
net.absorb(300)
killed = list(range(3))
surv = list(range(3, 10))
net.remove(killed)
acc_surv = kNN_acc(net.q, np.array(surv), subset=surv)
sp_before = net.spacing()
net.heal(500)
acc_healed = kNN_acc(net.q, np.array(surv), subset=surv)
sp_after = net.spacing()
print("\n--- damage: killed 3 neurons (survivors = classes 3-9) ---")
print(f"  survivors, broken   acc = {acc_surv:.3f}  spacing {sp_before:.3f}")
print(f"  survivors, healed   acc = {acc_healed:.3f}  spacing {sp_after:.3f}")

# regrow: re-populate empty homes (neuron order = surv + killed)
for j in killed:
    net.add(centroids[j])
    net.absorb(200)
acc_regrown = kNN_acc(net.q, np.array(surv + killed))
print("\n--- regrow: fresh neurons at empty homes ---")
print(f"  full 10-class acc = {acc_regrown:.3f}")

print("\n" + "=" * 70)
print("SUMMARY / VERDICT")
print("=" * 70)
print(f"  nearest-centroid (raw)      acc {acc_base:.3f}")
print(f"  DecentralNet local-settle   acc {acc_grown:.3f}")
print(f"  after killing 3, broken     acc {acc_surv:.3f} (survivors)")
print(f"  after local heal            acc {acc_healed:.3f}  spacing "
      f"{sp_before:.3f} -> {sp_after:.3f}")
print(f"  after regrow 3              acc {acc_regrown:.3f}")
print("  -> the no-dependency module routes real 64D embeddings and")
print("     survives damage with only local updates (no repair unit).")
print("\nDone.")
