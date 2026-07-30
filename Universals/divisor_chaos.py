"""
divisor_chaos.py
================
Analyze the divisor function d(n) for n = 1..100 under the
consistent-chaos lens of T19-T22.

d(n) = number of positive divisors of n.
If n = prod p_i^{a_i}, then d(n) = prod (a_i + 1).
"""

import math, json, sys
import numpy as np
from collections import Counter

N_MAX = 100

# -------------------------------------------------------------------
# 1. Compute d(n) and prime factorisation for n = 1..N_MAX
# -------------------------------------------------------------------
def factorise(n):
    if n == 1:
        return {}
    d, pf = n, {}
    p = 2
    while p * p <= d:
        while d % p == 0:
            pf[p] = pf.get(p, 0) + 1
            d //= p
        p += 1 if p == 2 else 2  # skip evens after 2
    if d > 1:
        pf[d] = pf.get(d, 0) + 1
    return pf

def divisor_count(n):
    pf = factorise(n)
    d = 1
    for a in pf.values():
        d *= (a + 1)
    return d

d_vals = [divisor_count(n) for n in range(1, N_MAX + 1)]

# -------------------------------------------------------------------
# 2. Display table
# -------------------------------------------------------------------
print(f"{'n':>3} | {'d(n)':>4} | {'Factorization':>30}")
print("-" * 42)
for n in range(1, N_MAX + 1):
    pf = factorise(n)
    fac_str = " * ".join(f"{p}^{a}" if a > 1 else f"{p}" for p, a in sorted(pf.items()))
    if not fac_str:
        fac_str = "1"
    print(f"{n:3d} | {d_vals[n-1]:4d} | {fac_str:>30}")

# -------------------------------------------------------------------
# 3. Statistics
# -------------------------------------------------------------------
print("\n" + "=" * 60)
print("  DIVISOR FUNCTION STATISTICS  (n = 1..100)")
print("=" * 60)
print(f"  Min d(n)  = {min(d_vals):3d}  (n={d_vals.index(min(d_vals))+1})")
print(f"  Max d(n)  = {max(d_vals):3d}  (n={d_vals.index(max(d_vals))+1})")
print(f"  Mean      = {np.mean(d_vals):.4f}")
print(f"  Variance  = {np.var(d_vals):.4f}")
print(f"  Std dev   = {np.std(d_vals):.4f}")

# Gaps: differences between consecutive d(n)
gaps = [abs(d_vals[i+1] - d_vals[i]) for i in range(len(d_vals)-1)]
print(f"\n  Gap mean  = {np.mean(gaps):.4f}")
print(f"  Gap var   = {np.var(gaps):.4f}")
print(f"  Gap D     = {np.var(gaps)/max(np.mean(gaps),0.01):.4f}  (dispersion index)")
print(f"  Gap CV    = {np.std(gaps)/max(np.mean(gaps),0.01):.4f}  (coeff of variation)")

# -------------------------------------------------------------------
# 4. Distribution of d(n) values
# -------------------------------------------------------------------
print("\n--- Distribution of d(n) values ---")
d_counts = Counter(d_vals)
for d_val in sorted(d_counts):
    ns = [i+1 for i, v in enumerate(d_vals) if v == d_val]
    print(f"  d(n) = {d_val:2d}: {d_counts[d_val]:2d} times  (n = {ns})")

# -------------------------------------------------------------------
# 5. Primes (d(n)=2) and their gaps
# -------------------------------------------------------------------
prime_ns = [n for n in range(1, N_MAX+1) if d_vals[n-1] == 2]
prime_gaps = [prime_ns[i+1] - prime_ns[i] for i in range(len(prime_ns)-1)]
print(f"\n--- Primes (d(n)=2) ---")
print(f"  Count: {len(prime_ns)} primes under {N_MAX+1}")
print(f"  Mean gap: {np.mean(prime_gaps):.2f}" if prime_gaps else "  N/A")
print(f"  Gap D: {np.var(prime_gaps)/max(np.mean(prime_gaps),0.01):.4f}" if prime_gaps else "")

# -------------------------------------------------------------------
# 6. "Chaos" metrics (consistent-chaos lens)
# -------------------------------------------------------------------
print("\n" + "=" * 60)
print("  CHAOS ANALYSIS  (T19-T22 lens)")
print("=" * 60)

# 6a. Autocorrelation: how dependent is d(n) on d(n-1)?
d_arr = np.array(d_vals, dtype=float)
auto = np.correlate(d_arr - d_arr.mean(), d_arr - d_arr.mean(), mode='full')
auto = auto / auto[len(auto)//2]
print(f"\n  Lag-1 autocorrelation: {auto[len(auto)//2 + 1]:.4f}")
print(f"  Lag-2 autocorrelation: {auto[len(auto)//2 + 2]:.4f}")
print(f"  Lag-3 autocorrelation: {auto[len(auto)//2 + 3]:.4f}")

# 6b. Spectral density (Fourier transform)
fft_vals = np.abs(np.fft.fft(d_arr - d_arr.mean()))**2
freqs = np.fft.fftfreq(len(d_arr))
# Look at low-frequency power concentration
low_freq_mask = (0 < np.abs(freqs)) & (np.abs(freqs) < 0.1)
low_power = fft_vals[low_freq_mask].sum()
total_power = fft_vals[1:].sum()
print(f"  Low-frequency power fraction: {low_power/total_power:.4f}  (0=white, 1=red)")

# 6c. Run test: number of times d(n) goes up/down
direction_changes = sum(1 for i in range(1, N_MAX-1)
                        if (d_vals[i] - d_vals[i-1]) * (d_vals[i+1] - d_vals[i]) < 0)
print(f"  Direction changes: {direction_changes}/{N_MAX-2}  (expected ~66 for random)")

# 6d. Kolmogorov complexity proxy: how many distinct d(n) values?
distinct_d = len(d_counts)
print(f"  Distinct d(n) values: {distinct_d}  (out of {N_MAX} n)   [~entropy]")

# 6e. Entropy of d(n) distribution
probs = np.array(list(d_counts.values())) / N_MAX
entropy = -sum(p * math.log2(p) for p in probs)
print(f"  Shannon entropy of d(n): {entropy:.4f} bits  (max={math.log2(distinct_d):.4f})")

# -------------------------------------------------------------------
# 7. Connection to the Mersenne-gap framework
# -------------------------------------------------------------------
print("\n" + "=" * 60)
print("  CONNECTION TO MERSENNE-GAP FRAMEWORK")
print("=" * 60)
print("""
  The divisor function d(n) and the Mersenne-gap prime count π_k(N)
  share a common structural property: both are governed by the
  multiplicative structure of integers.

  For d(n): d(n) = Π (a_i + 1)   where n = Π p_i^{a_i}.

  For π_k(N): the sieve density ε_k = Π (1 - e_p(k)/ord_p(2))
  determines the asymptotic count.

  Both are products over primes of local factors — the divisor
  function is the *simplest* such multiplicative function, while
  the Mersenne sieve density is a *chaos-weighted* variant.

  In the consistent-chaos framework (T19):
  - d(n) is the "deterministic" extreme: perfectly predictable
    from the prime factorization.
  - π_k(N) is the "chaotic" extreme: the primality test adds
    a random filter on top of the sieve.

  The gap dispersion D for d(n):""")

# Compare gap D for d(n) vs Mersenne families
print(f"  D(d(n) gaps) = {np.var(gaps)/max(np.mean(gaps),0.01):.4f}")
print(f"  D(Mersenne k=3 gaps) = 21.12  (from T21 analysis)")
print(f"""
  The gap dispersion for d(n) is LOWER than for the Mersenne
  families, because d(n) has only multiplicative noise (from
  exponent fluctuations), while the Mersenne process adds
  the chaotic primality-test layer on top.
""")
