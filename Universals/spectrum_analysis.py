"""
spectrum_analysis.py
====================
Compute the full multiplicative chaos spectrum across five arithmetic functions:

  1. ω(n)  — distinct prime divisors (Erdos-Kac regime)
  2. Ω(n)  — total prime divisors with multiplicity
  3. d(n)  — divisor count (baseline, from T23)
  4. P(n)  — prime indicator (d(n)=2)
  5. π_k(N) — Mersenne family counts (from T21)

For each, compute gap dispersion D = Var(gaps) / Mean(gaps).
"""

import math, json, numpy as np
from collections import Counter

N = 100

# -------------------------------------------------------------------
# 1. ω(n): number of distinct prime factors
# -------------------------------------------------------------------
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

def omega(n):
    return len(factorise(n))

def big_omega(n):
    pf = factorise(n)
    return sum(pf.values())

omega_vals = [omega(n) for n in range(1, N+1)]
big_omega_vals = [big_omega(n) for n in range(1, N+1)]

# -------------------------------------------------------------------
# 2. Gap statistics
# -------------------------------------------------------------------
def gap_stats(vals, label):
    gaps = [abs(vals[i+1] - vals[i]) for i in range(len(vals)-1)]
    mg = float(np.mean(gaps))
    vg = float(np.var(gaps))
    D = vg / mg if mg > 0 else float('inf')
    cv = float(np.std(gaps)) / mg if mg > 0 else 0
    n_distinct = len(set(vals))
    # Autocorrelation
    arr = np.array(vals, dtype=float)
    auto = np.correlate(arr - arr.mean(), arr - arr.mean(), mode='full')
    auto = auto / auto[len(auto)//2]
    lag1 = auto[len(auto)//2 + 1] if len(auto)//2 + 1 < len(auto) else 0
    return {
        "label": label,
        "mean": float(np.mean(vals)),
        "var": float(np.var(vals)),
        "D": D,
        "CV": cv,
        "n_distinct": n_distinct,
        "min": min(vals),
        "max": max(vals),
        "lag1_auto": lag1,
    }

# Compute for ω, Ω, d, primes
def d(n):
    cnt = 1
    for a in factorise(n).values():
        cnt *= (a + 1)
    return cnt

d_vals = [d(n) for n in range(1, N+1)]
prime_vals = [1 if d(n) == 2 else 0 for n in range(1, N+1)]  # indicator

stats = [
    gap_stats(omega_vals, "ω(n) distinct primes"),
    gap_stats(big_omega_vals, "Ω(n) total primes"),
    gap_stats(d_vals, "d(n) divisor count"),
    gap_stats(prime_vals, "P(n) prime indicator"),
]

# Add Mersenne data
with open("data/googol_census_all_k.json") as f:
    census = json.load(f)
families = census["families"]
mersenne_Ds = []
for k_str, ns in families.items():
    if len(ns) < 5:
        continue
    gaps_k = [ns[i+1] - ns[i] for i in range(len(ns)-1)]
    mg = float(np.mean(gaps_k))
    vg = float(np.var(gaps_k))
    if mg > 0:
        mersenne_Ds.append(vg / mg)

stats.append({
    "label": "Mersenne S_k (mean)",
    "mean": np.mean(mersenne_Ds),
    "var": np.var(mersenne_Ds),
    "D": np.mean(mersenne_Ds),
    "CV": np.std(mersenne_Ds) / max(np.mean(mersenne_Ds), 0.01),
    "n_distinct": len(mersenne_Ds),
    "min": min(mersenne_Ds),
    "max": max(mersenne_Ds),
})

# -------------------------------------------------------------------
# 3. Print spectrum table
# -------------------------------------------------------------------
print("=" * 75)
print("  MULTIPLICATIVE CHAOS SPECTRUM  (n = 1..{})".format(N))
print("=" * 75)
print(f"{'Function':<25} {'Mean':>7} {'Var':>8} {'D':>8} {'CV':>7} {'Distinct':>8} {'Lag-1':>7}")
print("-" * 75)
for s in stats:
    print(f"{s['label']:<25} {s['mean']:7.3f} {s['var']:8.3f} {s['D']:8.4f} {s['CV']:7.4f} {s['n_distinct']:8d} {s.get('lag1_auto',0):7.4f}")

# The prime indicator D is not comparable (0/1 variable), so recompute
# using prime GAPS (actual gaps between primes)
prime_ns = [n for n in range(1, N+1) if d(n) == 2]
prime_gaps = [prime_ns[i+1] - prime_ns[i] for i in range(len(prime_ns)-1)]
if prime_gaps:
    D_primes = float(np.var(prime_gaps)) / max(float(np.mean(prime_gaps)), 0.01)
    print(f"\n  Prime gap D (actual prime positions): {D_primes:.4f}")

print(f"\n  Divisor baseline (T23):          D = {next(s['D'] for s in stats if 'divisor' in s['label']):.4f}")
print(f"  Mersenne families (T21):         D in [{min(mersenne_Ds):.2f}, {max(mersenne_Ds):.2f}], mean = {np.mean(mersenne_Ds):.2f}")

# -------------------------------------------------------------------
# 4. Distribution of ω(n) and Ω(n)
# -------------------------------------------------------------------
print(f"\n--- ω(n) distribution ---")
wc = Counter(omega_vals)
for k in sorted(wc):
    print(f"  ω(n) = {k}: {wc[k]:3d} times")

print(f"\n--- Ω(n) distribution ---")
wc = Counter(big_omega_vals)
for k in sorted(wc):
    print(f"  Ω(n) = {k}: {wc[k]:3d} times")

# -------------------------------------------------------------------
# 5. The omega sequence as a "random walk"
# -------------------------------------------------------------------
# ω(n+1) - ω(n) can be -1, 0, or +1 only (since n and n+1 share no primes)
# Let's verify this and compute the transition matrix
print(f"\n--- ω(n) transition matrix ---")
trans = Counter()
for i in range(N-1):
    trans[(omega_vals[i], omega_vals[i+1])] += 1
print(f"  Distinct transitions: {len(trans)}")
for (a,b), c in sorted(trans.items()):
    print(f"    ω({a}) -> ω({b}): {c:3d} times")

# ω jumps are always from 0 to 1 or 1 to 0 etc — verify
omega_diffs = [omega_vals[i+1] - omega_vals[i] for i in range(N-1)]
print(f"  ω diffs = {set(omega_diffs)} (should be subset of {{-1,0,1}})")
assert all(d in {-1, 0, 1} for d in omega_diffs), "ω jump > |1| detected!"
