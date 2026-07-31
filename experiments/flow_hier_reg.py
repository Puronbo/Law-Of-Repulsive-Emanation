"""
T48b: Flow-regularized continual learning with hierarchical anchors.

Combines flow_regularized (C0 potential on 64D class centroids during MLP
training) with flow_hier_incremental (coarse groups + fine classes) into a
two-stage continual benchmark:

  Stage 1: train an MLP on classes {0..4}  (4 epochs), flow reg ON or OFF.
  Stage 2: fine-tune on ALL {0..9}          (4 epochs), flow reg ON or OFF.

The 2x2 design (flow on/off per stage) answers:
  - does flow-regularized training STABILIZE old-class anchors as new
    classes accumulate?  (old-class centroid displacement, forgetting)
  - does flow reg preserve accuracy while improving hierarchical routing?

Routing uses the concept-level physics: class centroids are the anchors;
a coarse C0 flow separates the 2 group centroids {0-4} vs {5-9}, fine
anchors are the class centroids (hierarchical PolysphereRouter).

Usage: python flow_hier_reg.py [seed] [dataset mnist|fashion]
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Universals'))
from manifold.c0_flow import c0_flow, c0_gradient
from manifold.polysphere import PolysphereRouter
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42
rng = np.random.RandomState(seed)

FLOW_LAMBDA = 5e-3
ATTRACT = 1.0
EPOCHS_S1, EPOCHS_S2 = 4, 4
BS = 256
OLD = list(range(5))            # stage-1 classes
GROUP_OF = np.array([0]*5 + [1]*5)   # group 0 = {0..4}, group 1 = {5..9}

class MLP:
    def __init__(self, dims, lr=0.01):
        self.layers = [{'W':rng.randn(dims[i],dims[i+1])*np.sqrt(2/dims[i]),'b':np.zeros(dims[i+1])}
                        for i in range(len(dims)-1)]
        self.lr = lr
    def forward(self, X):
        self.acts=[X]; self.zs=[]
        for i,l in enumerate(self.layers):
            z=self.acts[-1]@l['W']+l['b']; self.zs.append(z)
            a=z if i==len(self.layers)-1 else np.maximum(0,z); self.acts.append(a)
        return self.acts[-1]
    def embed(self, X):
        h=X
        for i,l in enumerate(self.layers[:-1]): h=np.maximum(0,h@l['W']+l['b'])
        return h
    def train_step(self, X, y1h, flow_grad=None, flow_lambda=0.0):
        l=self.forward(X)
        e=np.exp(l-l.max(axis=1,keepdims=True)); p=e/e.sum(axis=1,keepdims=True)
        loss=-np.mean(np.sum(y1h*np.log(p.clip(1e-12)),axis=1))
        d=(p-y1h)/X.shape[0]
        n_layers=len(self.layers)
        for i in reversed(range(n_layers)):
            dW=self.acts[i].T@d; db=d.sum(axis=0)
            self.layers[i]['W']-=self.lr*dW; self.layers[i]['b']-=self.lr*db
            if i>0:
                d=d@self.layers[i]['W'].T; d[self.zs[i-1]<=0]=0
                if i==n_layers-1 and flow_grad is not None and flow_lambda>0:
                    d=d+flow_lambda*flow_grad
        return float(loss)

def flow_regularizer_grad(z, y, attract=1.0):
    """Gradient of the C0 potential on class CENTROIDS, backpropagated to
    batch points (same concept-level physics as flow_regularized)."""
    n_classes = y.max() + 1
    centers = np.zeros((n_classes, z.shape[1])); counts = np.zeros(n_classes)
    for k in range(n_classes):
        m = y == k
        centers[k] = z[m].mean(axis=0) if m.sum() else 0.0
        counts[k] = m.sum()
    active = counts > 0
    g_cent = c0_gradient(centers[active], np.where(active)[0], attract=attract)
    g_cent = g_cent / np.sum(active)
    g = np.zeros_like(z)
    for k in range(n_classes):
        if not active[k]: continue
        g[y == k] = g_cent[np.where(active)[0] == k][0] / counts[k]
    return g

def train(net, X, y, flow_lambda, epochs, bs=BS):
    Y = np.eye(10)[y]
    for ep in range(epochs):
        idx=rng.permutation(len(X))
        for i in range(0,len(X),bs):
            b=idx[i:i+bs]
            fg = None
            if flow_lambda > 0:
                zb = net.embed(X[b])
                fg = flow_regularizer_grad(zb, y[b], ATTRACT)
            net.train_step(X[b], Y[b], flow_grad=fg, flow_lambda=flow_lambda)

def test_acc(net, X, y):
    return np.mean(np.argmax(net.forward(X),axis=1)==y)

def centroids(emb, y):
    return np.array([emb[y==k].mean(axis=0) for k in np.unique(y)])

def routing_acc(emb, labels, net, n_classes, subset=None, n_trials=200):
    """PolysphereRouter flat routing on MLP-logit truths (like flow_regularized)."""
    last = net.layers[-1]
    truths = [lambda X, j=j: X@last['W'][:,j]+last['b'][j] for j in range(n_classes)]
    router = PolysphereRouter(n_faces=n_classes, truths=truths, seed=42)
    n_half = 20
    correct = 0
    cands = list(range(n_classes)) if subset is None else subset
    for _ in range(n_trials):
        j_true = int(rng.choice(cands))
        j_fake = int(rng.choice([c for c in cands if c != j_true]))
        mt = labels == j_true; mf = labels == j_fake
        if mt.sum() < n_half or mf.sum() < n_half: continue
        bt = rng.choice(np.where(mt)[0], n_half)
        bf = rng.choice(np.where(mf)[0], n_half)
        Xb = np.vstack([emb[bt], emb[bf]])
        yb = np.array([1.0]*n_half + [0.0]*n_half)
        pred, _ = router.route_batch(Xb, yb, signed=True)
        if pred == j_true: correct += 1
    return correct / n_trials

def hier_routing_acc(emb, labels, group_of, n_trials=200, subset=None):
    """Coarse (group centroid distance) then fine (class centroid distance)
    routing on the flow-separated anchors."""
    n_grp = group_of.max() + 1
    n_cls = len(group_of)
    # coarse anchors: C0-separate group centroids (mean over classes in group)
    grp_c = np.array([emb[np.isin(labels, np.where(group_of == k)[0])].mean(axis=0)
                      for k in range(n_grp)])
    coarse = c0_flow(grp_c.copy(), n_steps=300, dt=0.02, friction=0.04, max_r=0.85)
    truths_c = [lambda X, j=j, c=coarse[j]: -np.linalg.norm(X - c, axis=1)
                for j in range(n_grp)]
    router_c = PolysphereRouter(n_faces=n_grp, truths=truths_c, seed=42)
    # fine anchors: class centroids
    fine = np.array([emb[labels == k].mean(axis=0) for k in range(n_cls)])
    routers_f = []
    for gi in range(n_grp):
        idx = np.where(group_of == gi)[0]
        truths_f = [lambda X, ci=ci, c=fine[idx[ci]]: -np.linalg.norm(X - c, axis=1)
                    for ci in range(len(idx))]
        routers_f.append(PolysphereRouter(n_faces=len(idx), truths=truths_f, seed=42))
    n_half = 20
    fine_ok, total = 0, 0
    cands = list(range(n_cls)) if subset is None else subset
    for _ in range(n_trials):
        j_true = int(rng.choice(cands))
        gi = group_of[j_true]
        j_fake = int(rng.choice(np.where(group_of != gi)[0]))
        mt = labels == j_true; mf = labels == j_fake
        if mt.sum() < n_half or mf.sum() < n_half: continue
        bt = rng.choice(np.where(mt)[0], n_half)
        bf = rng.choice(np.where(mf)[0], n_half)
        Xb = np.vstack([emb[bt], emb[bf]])
        yb = np.array([1.0]*n_half + [0.0]*n_half)
        pred_c, _ = router_c.route_batch(Xb, yb, signed=True)
        total += 1
        if pred_c != gi: continue
        sub_idx = np.where(group_of == gi)[0]
        local_true = list(sub_idx).index(j_true)
        siblings = [c for c in range(len(sub_idx)) if c != local_true]
        if not siblings: continue
        j_inner = sub_idx[rng.choice(siblings)]
        mt2 = labels == j_true; mf2 = labels == j_inner
        if mt2.sum() < n_half or mf2.sum() < n_half: continue
        bt2 = rng.choice(np.where(mt2)[0], n_half)
        bf2 = rng.choice(np.where(mf2)[0], n_half)
        Xb2 = np.vstack([emb[bt2], emb[bf2]])
        yb2 = np.array([1.0]*n_half + [0.0]*n_half)
        pred_f, _ = routers_f[gi].route_batch(Xb2, yb2, signed=True)
        if pred_f == local_true: fine_ok += 1
    return fine_ok / max(total, 1)

# ===================================================================
dataset = sys.argv[2] if len(sys.argv) > 2 else 'mnist'
print(f"Loading {dataset}...")
if dataset == 'mnist':
    X_all, y_all = fetch_openml('mnist_784', version=1, return_X_y=True, parser='auto')
    X_all = X_all.values.astype(np.float32) / 255.0
    y_all = y_all.values.astype(int)
else:
    X_all, y_all = fetch_openml('Fashion-MNIST', version=1, return_X_y=True, parser='auto')
    X_all = X_all.values.astype(np.float32) / 255.0
    y_all = y_all.values.astype(int)
X_tr, X_te, y_tr, y_te = train_test_split(X_all, y_all, test_size=10000, random_state=seed)

m1 = np.isin(y_tr, OLD); m2 = np.isin(y_te, OLD)
X1, y1 = X_tr[m1], y_tr[m1]
X_old_te, y_old_te = X_te[m2], y_te[m2]

print("=" * 62)
print("T48b: FLOW-REGULARIZED CONTINUAL LEARNING (hierarchical anchors)")
print(f"seed={seed}  dataset={dataset}  lambda={FLOW_LAMBDA}")
print("=" * 62)

for flow in [0.0, FLOW_LAMBDA]:
    tag = "flow-REG" if flow > 0 else "baseline "
    print(f"\n--- Stage 1 ({tag}): classes 0-4 ---")
    net = MLP([784, 256, 64, 10], lr=0.01)
    train(net, X1, y1, flow, EPOCHS_S1)
    emb1 = net.embed(X_old_te)
    a1 = test_acc(net, X_old_te, y_old_te)
    r1 = routing_acc(emb1, y_old_te, net, 5, subset=OLD, n_trials=150)
    cen1 = centroids(emb1, y_old_te)
    print(f"  test_acc={a1:.3f}  routing(old)={r1:.3f}")

    print(f"--- Stage 2 (same reg): fine-tune on classes 0-9 ---")
    train(net, X_tr, y_tr, flow, EPOCHS_S2)
    emb2 = net.embed(X_te)
    a2 = test_acc(net, X_te, y_te)
    a_old = test_acc(net, X_old_te, y_old_te)
    r_all = routing_acc(emb2, y_te, net, 10, n_trials=200)
    r_old = routing_acc(emb2, y_te, net, 10, subset=OLD, n_trials=150)
    h_all = hier_routing_acc(emb2, y_te, GROUP_OF, n_trials=200)
    h_old = hier_routing_acc(emb2, y_te, GROUP_OF, n_trials=150, subset=OLD)
    cen2 = centroids(emb2, y_te)
    disp = np.mean(np.linalg.norm(cen2[:5] - cen1, axis=1))   # old-class drift
    disp_rel = disp / np.mean(np.linalg.norm(cen1, axis=1))   # scale-free drift
    print(f"  test_acc all={a2:.3f}  old={a_old:.3f}  (forget={a_old-a1:+.3f})")
    print(f"  routing  all={r_all:.3f}  old={r_old:.3f}")
    print(f"  hier     all={h_all:.3f}  old={h_old:.3f}")
    print(f"  old-class centroid drift = {disp:.4f}  (rel {disp_rel:.3f})")

print("\n" + "="*62)
print("SUMMARY")
print("="*62)
print("  Compare the two runs above: does flow reg reduce old-class drift,")
print("  preserve accuracy, and improve hierarchical routing at stage 2?")
print("  (Flow reg shapes the centroid lattice; the stage-2 fine-tune tests")
print("  whether that lattice survives class accumulation.)")
print("\nDone.")
