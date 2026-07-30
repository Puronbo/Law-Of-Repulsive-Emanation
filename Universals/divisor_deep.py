"""
divisor_deep.py
===============
Four layers of pattern within the divisor-function pattern:

  Layer 1 — Highly composite numbers (record-setters)
  Layer 2 — Dirichlet sieve decomposition (Euler product analog)
  Layer 3 — d(n) as a 1D cellular automaton
  Layer 4 — Adjacent-factor correlation (the "divisor gap kernel")
"""

import numpy as np
from collections import defaultdict

N = 100

# -------------------------------------------------------------------
# Helpers
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

def d(n):
    pf = factorise(n)
    cnt = 1
    for a in pf.values(): cnt *= (a + 1)
    return cnt

vals = [d(n) for n in range(1, N+1)]
gaps = [abs(vals[i+1] - vals[i]) for i in range(N-1)]

print("=" * 70)
print("  LAYER 1 — HIGHLY COMPOSITE NUMBERS  (record-setters)")
print("=" * 70)
print("\n  n where d(n) > d(m) for all m < n:")
record = -1
for n in range(1, N+1):
    if vals[n-1] > record:
        pf = factorise(n)
        fac = " * ".join(f"{p}^{a}" if a > 1 else f"{p}" for p, a in sorted(pf.items()))
        print(f"    n={n:3d}  d(n)={vals[n-1]:2d}  {fac}")
        record = vals[n-1]

print(f"\n  Gap between consecutive records:")
rec_ns = [n for n in range(1, N+1)
          if vals[n-1] > max(vals[:n-1], default=-1)]
rec_gaps = [rec_ns[i+1] - rec_ns[i] for i in range(len(rec_ns)-1)]
print(f"    Mean gap: {np.mean(rec_gaps):.2f}" if rec_gaps else "")
print(f"    Gap D:    {np.var(rec_gaps)/max(np.mean(rec_gaps),0.01):.4f}")

# -------------------------------------------------------------------
# Layer 2: Dirichlet sieve — decompose d(n) by prime contributions
# -------------------------------------------------------------------
print("\n" + "=" * 70)
print("  LAYER 2 — DIRICHLET SIEVE  (Euler product decomposition)")
print("=" * 70)
print("""
  d(n) = Π_{p|n} (a_p + 1)   where a_p = v_p(n).

  This is an Euler product over primes, exactly like the
  congruence sieve density ε_k = Π (1 - e_p(k)/ord_p(2)).

  The difference: the divisor sieve AMPLIFIES (a_p + 1 >= 2 for
  any divisor), while the congruence sieve ATTENUATES (each factor
  <= 1).  Both are multiplicative over primes.
""")

# Contribution of each prime to the total divisor sum
# d(n) for n up to 100, accumulated by prime
prime_contribution = defaultdict(float)
total_d_sum = sum(vals)
for n in range(1, N+1):
    pf = factorise(n)
    for p in pf:
        prime_contribution[p] += vals[n-1]  # not exact but gives weight

print("  Top primes by total divisor weight (sum d(n) over n divisible by p):")
for p in sorted(prime_contribution, key=prime_contribution.get, reverse=True)[:10]:
    weight = prime_contribution[p]
    print(f"    p={p:2d}: weight = {weight:5.1f}  ({(weight/total_d_sum)*100:.1f}% of total d-sum)")

# -------------------------------------------------------------------
# Layer 3: d(n) as a 1D cellular automaton
# -------------------------------------------------------------------
print("\n" + "=" * 70)
print("  LAYER 3 — d(n) AS A 1D CELLULAR AUTOMATON")
print("=" * 70)
print("""
  The sequence d(n) evolves by a deterministic rule:
    d(n+1) = Π (a_p(n+1) + 1)
  where a_p(n+1) = a_p(n) + 1 if p | (n+1) and p ∤ n,
  and a_p(n+1) = 0 if p ∤ (n+1).

  This is a cellular automaton on the exponent lattice: each prime
  p is a "cell" with exponent a_p, and the update rule is:
    a_p(n+1) = a_p(n) + 1   if n+1 ≡ 0 mod p
    a_p(n+1) = 0            otherwise
  This is a shift-register CA on the infinite prime lattice.
""")

# Show the transition table for n -> n+1
print("  Transition analysis (n -> n+1):")
transitions = {}
for n in range(1, N):
    key = (vals[n-1], vals[n])
    transitions[key] = transitions.get(key, 0) + 1
print(f"    {len(transitions)} distinct (d(n), d(n+1)) transitions out of {N-1} steps")

# Most common transitions
print("    Top 10 transitions:")
for (a, b), cnt in sorted(transitions.items(), key=lambda x: -x[1])[:10]:
    print(f"      d({a}) -> d({b}): {cnt} times")

# Check: what fraction of d(n) values are local maxima/minima?
local_max = sum(1 for i in range(1, N-1) if vals[i] > vals[i-1] and vals[i] > vals[i+1])
local_min = sum(1 for i in range(1, N-1) if vals[i] < vals[i-1] and vals[i] < vals[i+1])
print(f"\n    Local maxima: {local_max}/{N-2}")
print(f"    Local minima: {local_min}/{N-2}")

# -------------------------------------------------------------------
# Layer 4: The divisor gap kernel — factor-level analysis
# -------------------------------------------------------------------
print("\n" + "=" * 70)
print("  LAYER 4 — DIVISOR GAP KERNEL  (factor-level driver)")
print("=" * 70)
print("""
  The gap |d(n+1) - d(n)| is determined by which primes divide
  n and n+1.  Let S(n) = {p : p | n}.  Then:

    d(n+1) / d(n) = Π_{p|n+1} (a_p(n+1)+1) / Π_{p|n} (a_p(n)+1)

  Key observation: n and n+1 are always coprime!  So the prime
  sets S(n) and S(n+1) are disjoint.  This means:
    d(n+1) and d(n) are INDEPENDENT in the prime-factor sense.
""")

# Verify: n and n+1 are always coprime
coprime_count = sum(1 for n in range(1, N) if np.gcd(n, n+1) == 1)
print(f"    n and n+1 coprime: {coprime_count}/{N-1} (expected {N-1})")

# The gap is hence:
#   |d(n+1) - d(n)| = |Π_{p|n+1} (a_p+1) - Π_{p|n} (a_p+1)|
# This is the difference of two products over distinct prime sets.

# Analyze: distribution of d(n) vs d(n+1) ratio
ratios = [vals[i+1] / vals[i] if vals[i] > 0 else 0 for i in range(N-1)]
print(f"\n    Mean ratio d(n+1)/d(n): {np.mean(ratios):.4f}")
print(f"    Ratio std: {np.std(ratios):.4f}")
print(f"    Ratio range: [{min(ratios):.4f}, {max(ratios):.4f}]")

# What drives large gaps?
print("\n  Top 5 largest gaps |d(n+1) - d(n)|:")
gap_indices = sorted(range(N-1), key=lambda i: gaps[i], reverse=True)[:5]
for idx in gap_indices:
    n = idx + 1
    pf_n = factorise(n)
    pf_n1 = factorise(n+1)
    fac_n = " * ".join(f"{p}^{a}" if a > 1 else f"{p}" for p, a in sorted(pf_n.items()))
    fac_n1 = " * ".join(f"{p}^{a}" if a > 1 else f"{p}" for p, a in sorted(pf_n1.items()))
    change = "+" if vals[n] > vals[n-1] else ""
    print(f"    d({n})={vals[n-1]} -> d({n+1})={vals[n]}  ({change}{vals[n]-vals[n-1]})")
    print(f"      n   = {n} = {fac_n}")
    print(f"      n+1 = {n+1} = {fac_n1}")

# -------------------------------------------------------------------
# Connection back to the framework
# -------------------------------------------------------------------
print("\n" + "=" * 70)
print("  CONNECTION TO FRAMEWORK (T19-T23)")
print("=" * 70)
print("""
  The divisor function reveals the *opposite* of the Mersenne sieve:

    Mersenne:  ε_k = Π (1 - e_p(k)/ord_p(2))    ← SUPPRESSION sieve
    Divisor:   d(n) = Π (a_p + 1)                ← AMPLIFICATION sieve

  Both are Euler products, but:
  - Mersenne sieve SELECTS a sparse subset (primes survive)
  - Divisor sieve COUNTS all divisors (every integer contributes)

  The "consistent chaos" (T19) is visible in both:
  - Mersenne: chaos from the primality-test filter (D ~ 24)
  - Divisor:  deterministic multiplicative baseline (D ~ 2.3)

  The ratio D(Mersenne) / D(divisor) ≈ 10 measures the extra
  chaotic entropy added by the geodesic-flow-based primality
  mechanism on top of the multiplicative exponent dynamics.

  Conjecture: For ANY multiplicative arithmetic function f(n)
  with Euler product f(n) = Π f_p(a_p), the gap dispersion
  D_f satisfies:
      D_f >= D_d ≈ 2.3
  with equality iff f(n) = d(n) (the divisor function) up to scaling.
""")
print(f"  Empirical check — D(d(n)) = {np.var(gaps)/max(np.mean(gaps),0.01):.4f}")
