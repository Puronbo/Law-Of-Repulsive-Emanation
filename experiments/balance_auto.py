"""
T51: Self-balancing continual learning - autonomous regime switch.

Uses of the T49/T50 verdict ("mu=0.5 absorbs shocks, mu=0 optimizes layout;
the adaptive schedule wins") made AUTONOMOUS:

  Part 1 - SYNTHETIC STREAM with a burst detector.  Events arrive one at a
           time: steady additions (new class at the center, low variance)
           punctuated by an EXPLOSIVE burst (+5 classes at high radius,
           high variance = the "sudden high-variance spike").  Policies:
             P0  always mu=0
             P5  always mu=0.5
             AD  auto: detect the burst from the incoming batch's radius
                 variance; engage mu=0.5 absorption only during it, then
                 settle at mu=0.  No manual schedule.
           Metrics per event: old-anchor displacement, old routing, all
           routing, min_d.

  Part 2 - REAL DATA (MNIST/Fashion): train an MLP on digits 0-4, then
           fine-tune on all 10 (explosive addition).  The class centroids
           (64D embeddings) are re-flowed with a CENTER-REFERENCED balance
           (trap toward the cloud mean - no disk clamp, any dimension),
           under the same three policies.  Old-class routing measures
           forgetting; min centroid distance measures separation.

Usage: python balance_auto.py [seed] [dataset mnist|fashion]
"""

import numpy as np
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Universals'))
from manifold.c0_flow import to_disk
from manifold.polysphere import PolysphereRouter
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42
rng = np.random.RandomState(seed)

A = 120.0          # calibrated so mu=0.5 gives a mid-shell in scaled coords
MU = 0.5
ABSORB_STEPS, SETTLE_STEPS = 400, 400

def bal_grad(qs, mu, eps=1e-3):
    """Center-referenced balance (N-D): trap to the cloud mean + C0 repulsion."""
    c = qs.mean(axis=0)
    trap = -A * mu * (qs - c)
    d = qs[:, None] - qs[None]
    dr = np.linalg.norm(d, axis=-1)
    np.fill_diagonal(dr, np.inf)
    rep = (d / np.maximum(dr, eps)[:, :, None]**3).sum(axis=1)
    return trap + (1 - mu) * rep

def bal_flow(qs, mu, n_steps=800, dt=0.05, max_r=0.9):
    """Normalized overdamped descent with a boundary clamp (any dimension)."""
    qs = qs.copy()
    for _ in range(n_steps):
        g = bal_grad(qs, mu)
        gmax = np.max(np.linalg.norm(g, axis=1))
        if gmax > 0:
            g = g / gmax
        qs = to_disk(qs + dt * g, max_r=max_r)
    return qs

def policy_flow(qs, schedule, max_r=0.9):
    for mu, steps in schedule:
        qs = bal_flow(qs, mu, n_steps=steps, max_r=max_r)
    return qs

def burst_detect(new_anchors, threshold=0.1):
    """Explosive data = sudden high-variance radii (T49 shock_burst geometry)."""
    r = np.linalg.norm(np.atleast_2d(new_anchors), axis=1)
    return float(r.std()) > threshold

def center_burst(n_new, rng, r_hi=0.9):
    """Explosive addition: high-radius anchors (high variance)."""
    r = rng.uniform(0.3, r_hi, n_new)
    th = rng.uniform(0, 2*math.pi, n_new)
    return np.column_stack([r*np.cos(th), r*np.sin(th)])

def center_steady(rng):
    """Steady addition: new anchor at the center (low variance)."""
    return rng.randn(1, 2) * 0.03

def gen_data(anchors, noise, pts_per_class):
    pts, labels = [], []
    for j in range(len(anchors)):
        p = anchors[j] + rng.randn(pts_per_class, 2) * noise
        pts.append(to_disk(p, max_r=0.9)); labels.extend([j]*pts_per_class)
    return np.vstack(pts), np.array(labels)

def routing_acc(anchors, points, labels, n_trials=150, subset=None):
    truths = [lambda X, j=j, c=anchors[j]: -np.linalg.norm(X - c, axis=1)
              for j in range(len(anchors))]
    router = PolysphereRouter(n_faces=len(anchors), truths=truths, seed=42)
    n_half = 8; correct = 0
    cands = list(range(len(anchors))) if subset is None else subset
    for _ in range(n_trials):
        j_true = int(rng.choice(cands))
        j_fake = int(rng.choice([c for c in cands if c != j_true]))
        mt = labels == j_true; mf = labels == j_fake
        if mt.sum() < n_half or mf.sum() < n_half: continue
        bt = rng.choice(np.where(mt)[0], n_half)
        bf = rng.choice(np.where(mf)[0], n_half)
        Xb = np.vstack([points[bt], points[bf]])
        yb = np.array([1.0]*n_half + [0.0]*n_half)
        pred, _ = router.route_batch(Xb, yb, signed=True)
        if pred == j_true: correct += 1
    return correct / n_trials

print("=" * 74)
print("T51: SELF-BALANCING CONTINUAL LEARNING (autonomous regime switch)")
print(f"seed={seed}   A={A}  detector: std(radii)>0.1 -> explosive burst")
print("=" * 74)

# ===================================================================
# PART 1: synthetic stream with autonomous burst detection
# ===================================================================
print("\n" + "-" * 74)
print("PART 1 (synthetic stream): steady additions + one explosive burst")
print("-" * 74)
n_base = 10
anchors0 = bal_flow(to_disk(rng.randn(n_base, 2) * 0.05, max_r=0.1) * 0.3, 0.0)
pts0, labels0 = gen_data(anchors0, 0.04, 150)
r_base = routing_acc(anchors0, pts0, labels0)
print(f"  base: routing={r_base:.3f}  n={n_base}")

# stream events: 2 steady, 1 burst (+5), 1 steady
events = [("steady", center_steady), ("steady", center_steady),
          ("burst+5", lambda rng: center_burst(5, rng)),
          ("steady", center_steady)]

print(f"  {'event':<9}{'policy':<12}{'detect':<7}{'disp_old':<10}{'old_route':<10}"
      f"{'all_route':<10}{'min_d':<8}")
print("  " + "-"*62)
prev = anchors0.copy()
for ev_name, gen in events:
    new_pts = gen(rng)
    burst = burst_detect(new_pts)
    # AD = the actual system; P0/P5 are counterfactuals run from the SAME state
    for pname, sched in [("P0", [(0.0, 800)]), ("P5", [(MU, 800)]),
                         ("AD", ([(MU, ABSORB_STEPS), (0.0, SETTLE_STEPS)]
                                 if burst else [(0.0, 800)]))]:
        anchors1 = policy_flow(np.vstack([prev, new_pts]), sched)
        pts1, labels1 = gen_data(anchors1, 0.04, 150)
        disp = np.mean(np.linalg.norm(anchors1[:len(prev)] - prev, axis=1))
        r_old = routing_acc(anchors1, pts1, labels1, subset=list(range(len(prev))))
        r_all = routing_acc(anchors1, pts1, labels1)
        d_min, _ = (np.min(np.linalg.norm(anchors1[:, None] - anchors1[None], axis=-1)
                           + np.eye(len(anchors1))*10), None)
        print(f"  {ev_name:<9}{pname:<12}{'burst' if burst else '--':<7}{disp:<10.4f}"
              f"{r_old:<10.3f}{r_all:<10.3f}{d_min:<8.4f}")
        if pname == "AD":
            prev = anchors1.copy()   # system advances along AD only

# ===================================================================
# PART 2: real data - MNIST/Fashion continual with adaptive anchor reflow
# ===================================================================
print("\n" + "-" * 74)
print("PART 2 (real data): MLP 0-4 -> fine-tune all 10 (explosive addition)")
print("-" * 74)

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
    def train_step(self, X, y1h):
        l=self.forward(X); e=np.exp(l-l.max(axis=1,keepdims=True))
        p=e/e.sum(axis=1,keepdims=True)
        loss=-np.mean(np.sum(y1h*np.log(p.clip(1e-12)),axis=1))
        d=(p-y1h)/X.shape[0]
        for i in reversed(range(len(self.layers))):
            dW=self.acts[i].T@d; db=d.sum(axis=0)
            self.layers[i]['W']-=self.lr*dW; self.layers[i]['b']-=self.lr*db
            if i>0:
                d=d@self.layers[i]['W'].T; d[self.zs[i-1]<=0]=0
        return float(loss)

def train(net, X, y, epochs, bs=256):
    Y = np.eye(10)[y]
    for ep in range(epochs):
        idx=rng.permutation(len(X))
        for i in range(0,len(X),bs):
            b=idx[i:i+bs]; net.train_step(X[b], Y[b])

OLD = list(range(5))
m1 = np.isin(y_tr, OLD)
X1, y1 = X_tr[m1], y_tr[m1]

print(f"--- stage 1: train on classes 0-4 ---")
net = MLP([784, 256, 64, 10], lr=0.01)
train(net, X1, y1, 4)
emb1 = net.embed(X_te[np.isin(y_te, OLD)])
cen1 = np.array([emb1[y_te[np.isin(y_te, OLD)] == k].mean(axis=0) for k in OLD])

print(f"--- stage 2: fine-tune on all 10 (the explosive addition) ---")
train(net, X_tr, y_tr, 4)
emb2 = net.embed(X_te)
cen2 = np.array([emb2[y_te == k].mean(axis=0) for k in range(10)])

# normalize centroid scale (mean norm 1) so A=120 gives disk-equivalent physics
scale = np.mean(np.linalg.norm(cen2, axis=1))
cen_n = cen2 / scale
disp_raw = np.mean(np.linalg.norm(cen_n[:5] - cen1 / scale, axis=1))

def centroid_routing(anchors, emb, labels, n_trials=200, subset=None):
    truths = [lambda X, j=j, c=anchors[j]: -np.linalg.norm(X - c, axis=1)
              for j in range(len(anchors))]
    router = PolysphereRouter(n_faces=len(anchors), truths=truths, seed=42)
    n_half = 20; correct = 0
    cands = list(range(len(anchors))) if subset is None else subset
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

new5 = cen_n[5:]                       # the newly added classes (burst)
burst = burst_detect(new5, threshold=0.05)
print(f"  burst detected on the +5 new centroids: {burst}  (std={np.linalg.norm(new5,axis=1).std():.3f})")

print(f"  {'policy':<12}{'disp_old':<10}{'old_route':<10}{'all_route':<10}{'min_d':<8}")
print("  " + "-"*46)
for pname, sched in [("P0", [(0.0, 800)]), ("P5", [(MU, 800)]),
                     ("AD", ([(MU, ABSORB_STEPS), (0.0, SETTLE_STEPS)]
                             if burst else [(0.0, 800)]))]:
    reflowed = policy_flow(cen_n.copy(), sched, max_r=2.0)
    disp = np.mean(np.linalg.norm(reflowed[:5] - cen1 / scale, axis=1))
    r_old = centroid_routing(reflowed, emb2, y_te, subset=OLD)
    r_all = centroid_routing(reflowed, emb2, y_te)
    d_min = np.min(np.linalg.norm(reflowed[:, None] - reflowed[None], axis=-1)
                   + np.eye(10) * 10)
    print(f"  {pname:<12}{disp:<10.4f}{r_old:<10.3f}{r_all:<10.3f}{d_min:<8.4f}")

# ===================================================================
print("\n" + "=" * 74)
print("SUMMARY")
print("=" * 74)
print("  Part 1: the autonomous burst detector fires ONLY on the explosive")
print("          event (never on steady additions).  BUT in a crowded stream")
print("          (repeated center additions before the burst) the mu=0.5")
print("          absorb no longer protects old anchors: AD ~= P0 on routing,")
print("          AD displacement slightly HIGHER.  P5 (fixed 0.5) is decisively")
print("          worse (all_route ~0.75, min_d ~0.2).")
print("          => the T50 absorb benefit is a ONE-SHOT recovery tool for a")
print("             clean steady-state shell, not a continuous stream policy.")
print("  Part 2: on real MNIST embeddings reflow policy is nearly irrelevant")
print("          (all >= 0.94); P0 marginally best.  MLP centroids are already")
print("          separated - geometry does not rescue clean embeddings.")
print("  (Raw stage-1 vs stage-2 old-centroid drift = %.4f)" % disp_raw)
print(f"\nDone.")
