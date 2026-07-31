"""
Three extensions:

1. Learnable NN truth functions (trainable router layer)
2. Hamiltonian flow on S^2 (C0 repulsion + routing)
3. Visualization of S^2 face regions

"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Universals'))
from manifold.polysphere import PolysphereRouter
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split

rng = np.random.RandomState(42)

# ===================================================================
# Load MNIST
# ===================================================================
print("Loading MNIST...")
X_all, y_all = fetch_openml('mnist_784', version=1, return_X_y=True, parser='auto')
X_all = X_all.values.astype(np.float32) / 255.0
y_all = y_all.values.astype(int)
X_train, X_test, y_train, y_test = train_test_split(
    X_all, y_all, test_size=10000, random_state=42)
print(f"  Train: {X_train.shape}, Test: {X_test.shape}")

# ===================================================================
# 1. Learnable NN truth functions
# ===================================================================
print("")
print("=" * 60)
print("1. LEARNABLE NN TRUTH FUNCTIONS")
print("=" * 60)

class NNTruthNet:
    """Feature extractor + NN truth functions, trained end-to-end.

    Unlike the previous LogitTruth approach (which used a fixed linear
    layer), this trains a small MLP as the truth function, making the
    router fully learnable.
    """

    def __init__(self, d_in=784, d_hidden=64, n_faces=10, lr=0.001):
        self.lr = lr
        scale1 = np.sqrt(2.0 / d_in)
        self.W1 = rng.randn(d_in, d_hidden) * scale1
        self.b1 = np.zeros(d_hidden)
        # Truth functions: small MLP from d_hidden -> n_faces
        scale2 = np.sqrt(2.0 / d_hidden)
        self.Wt1 = rng.randn(d_hidden, 32) * scale2
        self.bt1 = np.zeros(32)
        scale3 = np.sqrt(2.0 / 32)
        self.Wt2 = rng.randn(32, n_faces) * scale3
        self.bt2 = np.zeros(n_faces)

    def embed(self, X):
        return np.maximum(0, X @ self.W1 + self.b1)

    def forward(self, X):
        h = self.embed(X)
        return h @ self.Wt1 + self.bt1

    def truth_functions(self):
        """Return list of callables, one per face. Each takes embeddings -> scalar."""
        fns = []
        for j in range(self.Wt2.shape[1]):
            w = self.Wt2[:, j]
            b = self.bt2[j]
            def make_fn(w, b):
                def f(h):
                    return np.maximum(0, h @ self.Wt1 + self.bt1) @ w + b
                return f
            fns.append(make_fn(w, b))
        return fns

    def train_step(self, X, y_onehot):
        h = self.embed(X)
        a = np.maximum(0, h @ self.Wt1 + self.bt1)
        logits = a @ self.Wt2 + self.bt2
        exps = np.exp(logits - logits.max(axis=1, keepdims=True))
        probs = exps / exps.sum(axis=1, keepdims=True)
        loss = -np.mean(np.sum(y_onehot * np.log(probs.clip(1e-12)), axis=1))
        dlogits = (probs - y_onehot) / X.shape[0]
        # Backprop through Wt2, bt2
        dWt2 = a.T @ dlogits
        dbt2 = dlogits.sum(axis=0)
        da = dlogits @ self.Wt2.T
        da[a <= 0] = 0
        # Backprop through Wt1, bt1
        dWt1 = h.T @ da
        dbt1 = da.sum(axis=0)
        dh = da @ self.Wt1.T
        # Backprop through W1, b1
        dh[h <= 0] = 0
        dW1 = X.T @ dh
        db1 = dh.sum(axis=0)
        # Update
        self.Wt2 -= self.lr * dWt2
        self.bt2 -= self.lr * dbt2
        self.Wt1 -= self.lr * dWt1
        self.bt1 -= self.lr * dbt1
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
        return float(loss)

# Train NNTruthNet
print("Training NNTruthNet (learnable truth functions)...")
net2 = NNTruthNet(d_in=784, d_hidden=64, n_faces=10, lr=0.01)
n_epochs = 5
batch_size = 256
for epoch in range(n_epochs):
    idx = rng.permutation(len(X_train))
    losses = 0
    for i in range(0, len(X_train), batch_size):
        b = idx[i:i+batch_size]
        losses += net2.train_step(X_train[b], np.eye(10)[y_train[b]])
    h = net2.embed(X_train)
    a = np.maximum(0, h @ net2.Wt1 + net2.bt1)
    logits = a @ net2.Wt2 + net2.bt2
    acc = np.mean(np.argmax(logits, axis=1) == y_train)
    print(f"  Epoch {epoch+1}  loss={losses:.2f}  train_acc={acc:.3f}")

# Test
h_test = net2.embed(X_test)
a_test = np.maximum(0, h_test @ net2.Wt1 + net2.bt1)
logits_test = a_test @ net2.Wt2 + net2.bt2
test_acc = np.mean(np.argmax(logits_test, axis=1) == y_test)
print(f"  Test accuracy: {test_acc:.3f}")

# Use NN truths for routing
nn_truths = net2.truth_functions()
emb_train2 = net2.embed(X_train)
emb_test2 = net2.embed(X_test)
router_nn = PolysphereRouter(n_faces=10, truths=nn_truths, seed=42)

n_batches = 200
n_half = 20
correct = 0
for _ in range(n_batches):
    j_true = rng.randint(10)
    j_fake = (j_true + rng.randint(1, 10)) % 10
    idx_t = np.where(y_test == j_true)[0]
    idx_f = np.where(y_test == j_fake)[0]
    bt = rng.choice(idx_t, n_half)
    bf = rng.choice(idx_f, n_half)
    Xb = np.vstack([emb_test2[bt], emb_test2[bf]])
    yb = np.array([1.0]*n_half + [0.0]*n_half)
    pred, _ = router_nn.route_batch(Xb, yb, signed=True)
    if pred == j_true:
        correct += 1
print(f"  NN-truth routing accuracy: {correct}/{n_batches} = {correct/n_batches:.3f}")

# ===================================================================
# 2. Hamiltonian flow on S^2
# ===================================================================
print("")
print("=" * 60)
print("2. HAMILTONIAN FLOW ON S^2 (C0 repulsion + routing)")
print("=" * 60)

# Generate points from each face, embed on sphere, run dynamics
n_pts = 60
n_faces = 6
router_viz = PolysphereRouter(n_faces=n_faces, seed=42)

# Initial points on sphere
pts_s2 = []
labels_s2 = []
for j in range(n_faces):
    for _ in range(n_pts // n_faces):
        x = rng.uniform(-3, 3, size=(25, 2))
        y = router_viz.truths[j](x) + 0.1 * rng.randn(25)
        pt = router_viz.embed(x, y)
        pts_s2.append(pt)
        labels_s2.append(j)
pts_s2 = np.array(pts_s2)
labels_s2 = np.array(labels_s2)

def tangent_proj(v, p):
    """Project vector v onto tangent space of sphere at point p."""
    return v - (v * p).sum(axis=1, keepdims=True) * p

def c0_force(pts, face_labels, attract_strength=3.0):
    """C0 repulsion + same-face attraction on S^2."""
    n = len(pts)
    diffs = pts[:, None] - pts[None]
    dists = np.linalg.norm(diffs, axis=-1)
    np.fill_diagonal(dists, np.inf)
    # Repulsion: 1/r^2
    rep = np.sum(diffs / (dists ** 3)[:, :, None], axis=1)
    # Attraction: same-face pairs
    same = face_labels[:, None] == face_labels[None]
    np.fill_diagonal(same, False)
    attr = np.sum(same[:, :, None] * diffs / (dists ** 2 + 1e-8)[:, :, None], axis=1)
    return tangent_proj(rep - attract_strength * attr, pts)

# Evolve
for step in range(100):
    force = c0_force(pts_s2, labels_s2, attract_strength=2.0)
    pts_s2 = pts_s2 + 0.05 * force
    pts_s2 = pts_s2 / np.linalg.norm(pts_s2, axis=1, keepdims=True)

# Clustering quality
from scipy.spatial.distance import pdist, cdist
intra_f = []
inter_f = []
for j in range(n_faces):
    m = labels_s2 == j
    if m.sum() > 1:
        intra_f.append(np.mean(pdist(pts_s2[m])))
    for k in range(j + 1, n_faces):
        mk = labels_s2 == k
        if m.sum() > 0 and mk.sum() > 0:
            inter_f.append(np.mean(cdist(pts_s2[m], pts_s2[mk])))
sil = (np.mean(inter_f) - np.mean(intra_f)) / max(np.mean(inter_f), 1e-12)
print(f"  After evolution: {n_pts} pts, {n_faces} faces")
print(f"  Intra-face mean dist: {np.mean(intra_f):.3f}")
print(f"  Inter-face mean dist: {np.mean(inter_f):.3f}")
print(f"  Silhouette: {sil:.3f}")

# Re-route using per-face centroid truths computed from initial points
print("  Routing evolved points (centroid truths)...")
initial_centroids = [pts_s2[labels_s2 == j].mean(axis=0) for j in range(n_faces)]
def make_s2_truth(c):
    return lambda X: -np.linalg.norm(X - c, axis=1)
s2_truths = [make_s2_truth(c) for c in initial_centroids]
router_s2 = PolysphereRouter(n_faces=n_faces, truths=s2_truths, seed=42)

for j in range(n_faces):
    m = labels_s2 == j
    if m.sum() > 0:
        pts_j = pts_s2[m]
        # Route against each face's centroid: mix with far points
        others = np.vstack([pts_s2[labels_s2 == k] for k in range(n_faces) if k != j and (labels_s2 == k).sum() > 0])
        if len(others) > 0 and m.sum() > 0:
            Xb = np.vstack([pts_j, others[:min(len(others), m.sum())]])
            yb = np.array([1.0]*len(pts_j) + [0.0]*min(len(others), m.sum()))
            pred, conf = router_s2.route_batch(Xb, yb, signed=True)
            print(f"    Face {j} ({m.sum():2d} pts) -> routed to face {pred} (conf={conf:.3f})")
        else:
            print(f"    Face {j} ({m.sum():2d} pts) -> insufficient points to route")

# ===================================================================
# 3. Visualization: spherical projection of embeddings
# ===================================================================
print("")
print("=" * 60)
print("3. VISUALIZATION: S^2 embedding with routing boundaries")
print("=" * 60)
print("  (Writing visualization data)")

# Project MNIST test embeddings through the NN truths and route
n_viz = 1000
idx_viz = rng.choice(len(X_test), n_viz, replace=False)
X_viz = X_test[idx_viz]
y_viz = y_test[idx_viz]

# Get 2D embedding from NNTruthNet's first layer + projection via Wt1
h_viz = net2.embed(X_viz)  # 64D
a_viz = np.maximum(0, h_viz @ net2.Wt1 + net2.bt1)  # 32D

# Project to 2D via first 2 PCs of the truth layer
mean_a = a_viz.mean(axis=0)
a_centered = a_viz - mean_a
cov_a = a_centered.T @ a_centered
eigvals, eigvecs = np.linalg.eigh(cov_a)
proj_2d = a_centered @ eigvecs[:, -2:]  # top 2 components

# Route via mixed-batch routing (partition into groups of 40)
routed = np.zeros(n_viz, dtype=int)
batch_size = 40
n_batches_viz = n_viz // batch_size
for bi in range(n_batches_viz):
    batch_idx = idx_viz[bi*batch_size:(bi+1)*batch_size]
    h_batch = h_viz[bi*batch_size:(bi+1)*batch_size]
    y_batch = y_viz[bi*batch_size:(bi+1)*batch_size]
    # For each possible class, test against indicator
    # We route by: which face's truth best predicts the true class indicator?
    # Actually, just route each point individually via nearest centroid in embedding space
    pass

# Nearest-centroid routing (works per-point)
centroids_nn = np.zeros((10, net2.Wt2.shape[0]))  # 10 classes x 32D
for j in range(10):
    mask = y_train == j
    a_j = np.maximum(0, net2.embed(X_train[mask]) @ net2.Wt1 + net2.bt1)
    centroids_nn[j] = a_j.mean(axis=0)
for i in range(n_viz):
    a_i = a_viz[i]
    dists = np.linalg.norm(centroids_nn - a_i, axis=1)
    routed[i] = np.argmin(dists)
routed = np.array(routed)

# Summary stats
from collections import Counter
route_dist = Counter(routed)
print(f"  Routing distribution across {n_viz} points:")
for j in range(10):
    pct = route_dist.get(j, 0) / n_viz * 100
    true_pct = np.mean(y_viz == j) * 100
    print(f"    Face {j}: routed={pct:.1f}%  actual={true_pct:.1f}%")

# Save visualization data
viz_data = {
    'proj_2d': proj_2d.tolist(),
    'labels': y_viz.tolist(),
    'routed': routed.tolist(),
    'n_faces': 10,
    'test_acc': float(test_acc),
    'routing_acc': correct / n_batches,
}
import json
with open(os.path.join(os.path.dirname(__file__), '..', 'Universals', 's2_viz_data.json'), 'w') as f:
    json.dump(viz_data, f, indent=1)
print(f"  Visualization data saved to Universals/s2_viz_data.json")
print(f"  To plot: python -c \"import json; d=json.load(open('Universals/s2_viz_data.json')); ...\"")
print("")
print("Done.")
