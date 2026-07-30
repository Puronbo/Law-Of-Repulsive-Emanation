"""
spectrum_extended.py
====================
Extend the chaos spectrum with σ(n) (sum of divisors) and φ(n) (Euler totient).
Compute D and C(f) = D_f / D_d for all functions.
"""

import math, json, numpy as np

N = 100

def factorise(n):
    if n == 1: return {}
    d, pf, p = n, {}, 2
    while p * p <= d:
        while d % p == 0:
            pf[p] = pf.get(p, 0) + 1
            d //= p
        p += 1 if p == 2 else 2
    if d > 1: pf[d] = pf.get(d, 0) + 1
    return pf

# ---- arithmetic functions ----
def omega(n): return len(factorise(n))
def big_omega(n): return sum(factorise(n).values())
def d(n):
    cnt = 1
    for a in factorise(n).values(): cnt *= (a + 1)
    return cnt
def sigma(n):
    pf = factorise(n)
    s = 1
    for p, a in pf.items():
        s *= (p**(a+1) - 1) // (p - 1)
    return s
def phi(n):
    pf = factorise(n)
    r = n
    for p in pf:
        r -= r // p
    return r

# ---- compute D for each ----
def gap_D(vals):
    gaps = [abs(vals[i+1] - vals[i]) for i in range(len(vals)-1)]
    mg = float(np.mean(gaps))
    vg = float(np.var(gaps))
    return vg / mg if mg > 0 else 0

funcs = {
    "ω(n)":       lambda n: omega(n),
    "Ω(n)":       lambda n: big_omega(n),
    "d(n)":       lambda n: d(n),
    "σ(n)":       lambda n: sigma(n),
    "φ(n)":       lambda n: phi(n),
}

results = []
for name, fn in funcs.items():
    vals = [fn(n) for n in range(1, N+1)]
    D = gap_D(vals)
    results.append((name, float(np.mean(vals)), float(np.var(vals)), D, len(set(vals))))

# Mersenne
with open("data/googol_census_all_k.json") as f:
    census = json.load(f)
mDs = []
for k_str, ns in census["families"].items():
    if len(ns) < 5: continue
    gk = [ns[i+1] - ns[i] for i in range(len(ns)-1)]
    mg = float(np.mean(gk)); vg = float(np.var(gk))
    if mg > 0: mDs.append(vg / mg)
D_M = float(np.mean(mDs)) if mDs else 0

# Prime gaps
primes = [n for n in range(1, N+1) if d(n) == 2]
pgaps = [primes[i+1] - primes[i] for i in range(len(primes)-1)]
D_p = float(np.var(pgaps)) / max(float(np.mean(pgaps)), 0.01) if pgaps else 0

# Baselines
D_d = gap_D([d(n) for n in range(1, N+1)])

print("=" * 75)
print("  EXTENDED CHAOS SPECTRUM  (n = 1..{})".format(N))
print("=" * 75)
print(f"{'Function':<20} {'Mean':>10} {'Var':>10} {'D':>8} {'C(f)=D/D_d':>12} {'Distinct':>8}")
print("-" * 75)
for name, mn, vr, Dval, nd in results:
    C = Dval / D_d if D_d > 0 else 0
    print(f"{name:<20} {mn:10.3f} {vr:10.3f} {Dval:8.4f} {C:12.4f} {nd:8d}")

print(f"{'Prime gaps':<20} {'-':>10} {'-':>10} {D_p:8.4f} {D_p/D_d:12.4f} {'-':>8}")
print(f"{'Mersenne S_k':<20} {'-':>10} {'-':>10} {D_M:8.2f} {D_M/D_d:12.2f} {'-':>8}")

print(f"\n  Baseline: D_d = {D_d:.4f} (divisor function)")
print(f"  Chaos index C(f) = D_f / D_d  (C=1 is deterministic baseline)")
print(f"  C > 10 indicates geodesic-flow-driven chaos")
