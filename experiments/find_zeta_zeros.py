"""Compute all zeta zeros up to height T_MAX with incremental saves."""
import mpmath, json, time, math, os, sys
import numpy as np

T_MAX = 22000
SAVE_EVERY = 200
FP = 'data/zeta_zeros_extended.json'
PROGRESS = 'data/zeta_zeros_progress.json'

# Load existing
existing = np.load('data/mertens_explicit_height_zeros.npz')
eg = sorted(existing['g_all'].tolist())
Ne = len(eg)
print(f'Existing: {Ne} zeros to t={max(eg):.1f}')

# Resume or start fresh
if os.path.exists(PROGRESS):
    with open(PROGRESS) as f:
        nz = json.load(f)
    n = nz[-1]['n'] + 1
    print(f'Resuming from n={n}, {len(nz)} already computed')
else:
    nz = []
    n = Ne + 1

t0 = time.time()
last_save = time.time()

while True:
    z = mpmath.zetazero(n)
    t = float(mpmath.im(z))
    if t > T_MAX:
        break
    nz.append({'n': n, 'beta': float(mpmath.re(z)), 'gamma': t})
    n += 1

    if len(nz) % SAVE_EVERY == 0:
        with open(PROGRESS, 'w') as f:
            json.dump(nz, f)
        elapsed = time.time() - t0
        rate = len(nz) / elapsed if elapsed > 0 else 0
        print(f'  n={n}, t={t:.1f}, total={len(nz)}, {elapsed:.0f}s, {rate:.1f}z/s', flush=True)

# Final save
with open(PROGRESS, 'w') as f:
    json.dump(nz, f)

# Combine
g = sorted(eg + [z['gamma'] for z in nz])
N = len(g)
betas = [0.5]*Ne + [z['beta'] for z in nz]
mx = max(abs(b-0.5) for b in betas)

# NNSD
sp = [(g[i+1]-g[i])*math.log(g[i]/(2*math.pi))/(2*math.pi) for i in range(N-1)]
mu = sum(sp)/len(sp)
vr = sum((s-mu)**2 for s in sp)/len(sp)
lag1 = sum((sp[i]-mu)*(sp[i+1]-mu) for i in range(len(sp)-1))/((len(sp)-1)*vr)

print(f'\nTotal: {N} zeros, t_max={g[-1]:.1f}')
print(f'Max |Re(rho)-1/2|: {mx:.15e}')
print(f'NNSD: mean={mu:.6f}, std={math.sqrt(vr):.6f}, lag1={lag1:.6f}')
print(f'  GUE:  mean=1.000, std=0.523, lag1=-0.323')
print(f'  Poisson: mean=1.000, std=1.000, lag1~0')

L_vals = [1.0, 2.0, 5.0, 10.0, 20.0]
nv = {}
for L in L_vals:
    counts = []
    i = 0
    while i < len(sp):
        total = 0.0
        j = i
        while j < len(sp) and total < L:
            total += sp[j]
            j += 1
        counts.append(j - i)
        i = j
    v = round(float(np.var(counts)), 4)
    nv[str(L)] = v
    print(f'  Sigma^2(L={L:.1f}): {v:.4f}  (Poisson={L:.1f})')

data = {
    'T_max': T_MAX, 'N': N, 't_max': g[-1], 're_rho_max': mx,
    'nnsd': {'mean': mu, 'std': math.sqrt(vr), 'lag1': lag1},
    'number_variance': nv, 'new_zeros': nz
}
with open(FP, 'w') as f:
    json.dump(data, f, indent=2)
print(f'Saved {FP} ({os.path.getsize(FP)//1024} KB)')
