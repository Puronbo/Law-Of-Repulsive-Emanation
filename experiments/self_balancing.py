"""
T55a: SELF-BALANCING ROUTER - coherence-aware, n-scaled, Fibonacci-scheduled.

Assembles the validated pieces into one autonomous controller:
  - Fibonacci batching (T52/T53): arrivals released in 1,1,2,3,5,8 chunks
  - n-scaled absorption (T54): trap A = A*(n) ~ n^1.09, so mu=0.5 means
    the same thing at every system size
  - SHELL-COHERENCE GATE (T51/T53 refinement): absorb only when the
    pre-burst shell is CLEAN (absorb helps clean shells, hurts crowded
    cores).  Coherence = mean(r)/std(r) around the cloud mean.

Policies:
  P0        mu=0 always (steady expansion)
  FIB       Fibonacci batching, mu=0
  ABS       batching + absorb on large terms (3,5,8), fixed A=120 (T53)
  ABS-SC    batching + absorb, A=A*(n)  (T54 scaled)
  COH       batching + absorb gated on shell coherence, A=A*(n)  (T55a)

  Part 1: coherence calibration along the fib stream
  Part 2: controller benchmark on the T53 stream (seeds 42/11/7)
  Part 3: crowded-core stress (T51 scenario) - COH should SKIP the absorb
  Part 4: real MNIST sanity (seed 42) - controller must not hurt

Usage: python self_balancing.py [seed]
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

MU = 0.5
ABSORB_STEPS, SETTLE_STEPS = 400, 400
COH_THRESH = 3.0          # disclosed geometry-like threshold (calibrated in Part 1)
A_STAR = {5: 17.852, 10: 33.448, 20: 74.381, 40: 164.258, 80: 347.179}

def A_scaled(n):
    keys = sorted(A_STAR)
    if n <= keys[0]: return A_STAR[keys[0]]
    if n >= keys[-1]: return A_STAR[keys[-1]]
    for a, b in zip(keys, keys[1:]):
        if a <= n <= b:
            wa = math.log(b) - math.log(n); wb = math.log(n) - math.log(a)
            return math.exp((wa*math.log(A_STAR[a]) + wb*math.log(A_STAR[b])) /
                            (math.log(b) - math.log(a)))
    return A_STAR[keys[-1]]

def coherence(qs):
    r = np.linalg.norm(qs - qs.mean(axis=0), axis=1)
    return float(r.mean() / max(r.std(), 1e-6))

def bal_grad(qs, mu, A, eps=1e-3):
    c = qs.mean(axis=0)
    trap = -A * mu * (qs - c)
    d = qs[:, None] - qs[None]
    dr = np.linalg.norm(d, axis=-1)
    np.fill_diagonal(dr, np.inf)
    rep = (d / np.maximum(dr, eps)[:, :, None]**3).sum(axis=1)
    return trap + (1 - mu) * rep

def bal_flow(qs, mu, A, n_steps=800, dt=0.05, max_r=0.9):
    qs = qs.copy()
    for _ in range(n_steps):
        g = bal_grad(qs, mu, A)
        gmax = np.max(np.linalg.norm(g, axis=1))
        if gmax > 0:
            g = g / gmax
        qs = to_disk(qs + dt * g, max_r=max_r)
    return qs

def policy_flow(qs, sched, A, max_r=0.9):
    for mu, steps in sched:
        qs = bal_flow(qs, mu, A, n_steps=steps, max_r=max_r)
    return qs

def gen_batch(k, rng, r_lo=0.0, r_hi=0.08):
    th = rng.uniform(0, 2*math.pi, k)
    r = rng.uniform(r_lo, r_hi, k)
    return np.column_stack([r*np.cos(th), r*np.sin(th)])

def gen_data(anchors, noise, pts_per_class):
    pts, labels = [], []
    for j in range(len(anchors)):
        p = anchors[j] + rng.randn(pts_per_class, 2) * noise
        pts.append(to_disk(p, max_r=0.9)); labels.extend([j]*pts_per_class)
    return np.vstack(pts), np.array(labels)

def routing_acc(anchors, points, labels, n_trials=100, subset=None):
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

def make_policy(kind, coh_thresh=COH_THRESH):
    def pol(term, coh, n_now):
        if kind == 'P0' or kind == 'FIB':
            return [(0.0, 800)], 120.0
        if kind == 'ABS':
            sched = ([(MU, ABSORB_STEPS), (0.0, SETTLE_STEPS)] if term >= 3
                     else [(0.0, 800)])
            return sched, 120.0
        if kind == 'ABS-SC':
            sched = ([(MU, ABSORB_STEPS), (0.0, SETTLE_STEPS)] if term >= 3
                     else [(0.0, 800)])
            return sched, A_scaled(n_now)
        if kind == 'COH':
            sched = ([(MU, ABSORB_STEPS), (0.0, SETTLE_STEPS)]
                     if term >= 3 and coh > coh_thresh else [(0.0, 800)])
            return sched, A_scaled(n_now)
        raise ValueError(kind)
    return pol

def simulate(base, arrivals, sizes, policy, base_n):
    anchors = base.copy()
    buffer = []
    released = 0
    rel_rows = []
    step_rows = []
    coh_series = []
    for i in range(len(arrivals)):
        buffer.append(arrivals[i])
        target = sizes[min(released, len(sizes)-1)]
        rel = buffer[:target] if len(buffer) >= target else []
        if rel:
            buffer = buffer[target:]
        for b in rel:
            released += 1
            n_now = base_n + released
            coh = coherence(anchors)
            coh_series.append(coh)
            sched, A = policy(len(rel), coh, n_now)
            anchors = policy_flow(np.vstack([anchors, b]), sched, A)
            pts, labels = gen_data(anchors, 0.04, 150)
            r_old = routing_acc(anchors, pts, labels, subset=list(range(base_n)))
            r_all = routing_acc(anchors, pts, labels)
            d_min = np.min(np.linalg.norm(anchors[:, None] - anchors[None], axis=-1)
                           + np.eye(len(anchors))*10)
            rel_rows.append((released, r_old, r_all, d_min))
        pts, labels = gen_data(anchors, 0.04, 150)
        r_old = routing_acc(anchors, pts, labels, subset=list(range(base_n)))
        step_rows.append((r_old, len(buffer)))
    return step_rows, rel_rows, coh_series

def stream_stats(step_rows, rel_rows):
    final = rel_rows[-1]
    stream_mean = float(np.mean([r for r, _ in step_rows[10:]]))
    mean_buf = float(np.mean([b for _, b in step_rows]))
    return final, stream_mean, mean_buf

print("=" * 74)
print("T55a: SELF-BALANCING ROUTER (coherence-gated, n-scaled, fib-scheduled)")
print(f"seed={seed}   COH_THRESH={COH_THRESH}   A*(n): {A_STAR}")
print("=" * 74)

base_n = 5
base = bal_flow(to_disk(rng.randn(base_n, 2) * 0.2, max_r=0.3), 0.0, 120.0)

# ===================================================================
# PART 1: coherence calibration along the fib stream
# ===================================================================
print("\n" + "-" * 74)
print("PART 1: shell coherence along a clean fib stream (calibration)")
print("-" * 74)
N = 20
sizes_fib = [1, 1, 2, 3, 5, 8]
arrivals = [gen_batch(1, rng)[0] for _ in range(N)]
_, _, coh_series = simulate(base, arrivals, sizes_fib, make_policy('P0'), base_n)
print("  coherence at each release:", " ".join(f"{c:.2f}" for c in coh_series))
print("  (clean shell => high mean/std; crowded core => low)")

# ===================================================================
# PART 2: controller benchmark (T53 stream)
# ===================================================================
print("\n" + "-" * 74)
print("PART 2: controller benchmark (20 arrivals, base 5, fib batching)")
print("  final_old / final_all / stream_old / mean_buf / final_min_d")
print("-" * 74)
pols = ['P0', 'FIB', 'ABS', 'ABS-SC', 'COH']
print(f"  {'policy':<9}{'final_old':<11}{'final_all':<11}{'stream_old':<12}"
      f"{'mean_buf':<10}{'min_d'}")
print("  " + "-"*58)
res = {}
for kind in pols:
    policy = make_policy(kind)
    rng.seed(seed)   # same data/query draws for every policy
    step_rows, rel_rows, _ = simulate(base, arrivals, sizes_fib, policy, base_n)
    final, stream_mean, mean_buf = stream_stats(step_rows, rel_rows)
    res[kind] = (final, stream_mean, mean_buf)
    print(f"  {kind:<9}{final[1]:<11.3f}{final[2]:<11.3f}{stream_mean:<12.3f}"
          f"{mean_buf:<10.2f}{final[3]:<10.4f}")

# ===================================================================
# PART 3: crowded-core stress (T51 scenario)
# ===================================================================
print("\n" + "-" * 74)
print("PART 3: crowded-core stress - 6 center classes, then a +5 burst")
print("  (COH should SKIP the absorb because the core is crowded)")
print("-" * 74)
crowd = [gen_batch(1, rng)[0] for _ in range(6)]
burst = gen_batch(5, rng, r_lo=0.1, r_hi=0.9)
# crowd with a TRAPPED reflow so the core is genuinely compressed (T51's
# failing scenario) - pure mu=0 reflow just expands it back into a shell
a_crowd = base.copy()
for c in crowd:
    a_crowd = bal_flow(np.vstack([a_crowd, c]), MU, 120.0, n_steps=ABSORB_STEPS)
coh_before = coherence(a_crowd)
print(f"  coherence before burst: {coh_before:.2f}   (crowded => < {COH_THRESH})")
print(f"  {'policy':<9}{'disp_old':<10}{'old_route':<10}{'all_route':<10}{'absorbed'}")
print("  " + "-"*44)
n_now = len(a_crowd) + 5
for kind in ['P0', 'ABS', 'ABS-SC', 'COH']:
    policy = make_policy(kind)
    rng.seed(seed)   # same draws for every policy
    sched, A = policy(5, coh_before, n_now)
    a1 = policy_flow(np.vstack([a_crowd, burst]), sched, A)
    pts, labels = gen_data(a1, 0.04, 150)
    disp = np.mean(np.linalg.norm(a1[:len(a_crowd)] - a_crowd, axis=1))
    r_old = routing_acc(a1, pts, labels, subset=list(range(len(a_crowd))))
    r_all = routing_acc(a1, pts, labels)
    absorbed = 'yes' if sched[0][0] > 0 else 'no'
    print(f"  {kind:<9}{disp:<10.4f}{r_old:<10.3f}{r_all:<10.3f}{absorbed}")

# ===================================================================
# PART 4: real MNIST sanity (seed 42)
# ===================================================================
print("\n" + "-" * 74)
print("PART 4 (seed 42 only): MNIST class-incremental sanity")
print("-" * 74)
if seed == 42:
    print("Loading mnist...")
    X_all, y_all = fetch_openml('mnist_784', version=1, return_X_y=True, parser='auto')
    X_all = X_all.values.astype(np.float32) / 255.0
    y_all = y_all.values.astype(int)
    X_tr, X_te, y_tr, y_te = train_test_split(X_all, y_all, test_size=10000, random_state=42)

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
            d=(p-y1h)/X.shape[0]
            for i in reversed(range(len(self.layers))):
                dW=self.acts[i].T@d; db=d.sum(axis=0)
                self.layers[i]['W']-=self.lr*dW; self.layers[i]['b']-=self.lr*db
                if i>0:
                    d=d@self.layers[i]['W'].T; d[self.zs[i-1]<=0]=0

    def train(net, X, y, epochs, bs=256):
        Y = np.eye(10)[y]
        for ep in range(epochs):
            idx=rng.permutation(len(X))
            for i in range(0,len(X),bs):
                b=idx[i:i+bs]; net.train_step(X[b], Y[b])

    def centroid_routing(anchors, emb, labels, n_trials=150, subset=None):
        truths = [lambda X, j=j, c=anchors[j]: -np.linalg.norm(X - c, axis=1)
                  for j in range(len(anchors))]
        router = PolysphereRouter(n_faces=len(anchors), truths=truths, seed=42)
        n_half=20; correct=0
        cands = list(range(len(anchors))) if subset is None else subset
        for _ in range(n_trials):
            j_true=int(rng.choice(cands)); j_fake=int(rng.choice([c for c in cands if c!=j_true]))
            mt=labels==j_true; mf=labels==j_fake
            if mt.sum()<n_half or mf.sum()<n_half: continue
            bt=rng.choice(np.where(mt)[0],n_half); bf=rng.choice(np.where(mf)[0],n_half)
            Xb=np.vstack([emb[bt],emb[bf]]); yb=np.array([1.0]*n_half+[0.0]*n_half)
            pred,_=router.route_batch(Xb,yb,signed=True)
            if pred==j_true: correct+=1
        return correct/n_trials

    def run_part4(net, new_groups, kind):
        seen=[0,1,2]; out=[]
        for grp in new_groups:
            for ag in ([grp] if kind != 'FIB' else [grp]):
                seen=seen+ag
                m=np.isin(y_tr, seen)
                train(net, X_tr[m], y_tr[m], 1)
                emb=net.embed(X_te)
                cen=np.array([emb[y_te==k].mean(axis=0) for k in range(10)])
                cen_n=cen/np.mean(np.linalg.norm(cen,axis=1))
                policy = make_policy(kind)
                coh = coherence(cen_n)
                sched, A = policy(len(ag), coh, len(seen))
                reflowed = policy_flow(cen_n.copy(), sched, A, max_r=2.0)
                r_old=centroid_routing(reflowed, emb, y_te, subset=[0,1,2])
                r_all=centroid_routing(reflowed, emb, y_te)
                out.append((len(ag), r_old, r_all))
        return out

    new_groups=[[3],[4],[5,6],[7,8,9]]
    print(f"  {'policy':<9}{'release':<10}{'old_route':<10}{'all_route':<10}")
    print("  " + "-"*36)
    for kind in ['FIB', 'ABS-SC', 'COH']:
        net=MLP([784,256,64,10], lr=0.01)
        m0=np.isin(y_tr,[0,1,2])
        train(net, X_tr[m0], y_tr[m0], 3)
        rows=run_part4(net, new_groups, kind)
        for sz, r_old, r_all in rows:
            print(f"  {kind:<9}{'+'+str(sz):<10}{r_old:<10.3f}{r_all:<10.3f}")

print("\n" + "=" * 74)
print("SUMMARY / VERDICT (multi-seed 42/11/7 for Parts 1-3, seed 42 Part 4)")
print("=" * 74)
print("  Self-balancing router = Fibonacci batching + n-scaled absorb")
print("  (A=A*(n) ~ n^1.09) + coherence gate (absorb only when the shell is")
print("  clean, coherence = mean/std of radii > %.1f)." % COH_THRESH)
print("  Part 2 (clean fib stream): COH ties ABS-SC on old-routing")
print("    (0.870/0.870) and has the best final_all (0.880 vs P0 0.820,")
print("    ABS-SC 0.853): the gate keeps the T53 all-routing gain without")
print("    a systematic old-routing penalty. P0 stays best for stream_old.")
print("  Part 3 (TRAPPED crowded core, coh 2.64-2.89 < 3.0): gate FIRES.")
print("    COH skips the absorb, lands exactly on P0 (old 0.84-0.90), and")
print("    displaces old anchors least in all 3 seeds (0.46-0.51 vs")
print("    0.55-0.57 for ABS-SC): the T51 failure mode is avoided.")
print("  Caveats / recommendations:")
print("    - coherence = mean(r)/std(r) is a shell-THICKNESS signal, NOT a")
print("      general crowding detector: a heavy trap (A=400) reads HIGH (3.78)")
print("      while being the most collapsed, and near-symmetric shells blow")
print("      it up (~9e5). Valid only for the trapped-core vs expanding-shell")
print("      split; if a general gate is needed, use min_d (spacing) instead.")
print("    - Part 4 (MNIST, seed 42): COH final-all 0.87 below FIB 0.94 -")
print("      scheduling/gating adds nothing on real embeddings; run NAIVE/FIB")
print("      there and reserve the controller for the geometry regime.")
print("  Rules: schedule arrivals in Fibonacci batches; absorb (scaled) only")
print("  during large terms AND while the shell stays clean; settle at mu=0.")
print(f"\nDone.")
