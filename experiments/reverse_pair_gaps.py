"""
T57: THE 10262 <-> 26102 REVERSE PAIR, tested through prime gaps.

User's relations to verify (10262 reversed is 26102):
  (a) 26102 - 10262 = 15840 = 80 * 198   -> "an 80 divisor multiple"
  (b) digit sum of 10262 = 11  AND  digit sum of 26102 = 11
                                                        -> "an 11 number sum"
Then further prime-gap experiments over the bridged range up to the next
checkpoint, and the 9.4e11 endpoint handled analytically.

  PART 1  factorizations, reversal, 80-multiple, 11-sums
  PART 2  prime-gap census  [10262, 26102]  and  [26102, 1914467]
          (count, record gaps, histograms, gaps divisible by 80 / by 11)
  PART 3  emirps (p and reverse(p) both prime) and digit-sum-11 primes
  PART 4  recommendation (efficient process at large scale)

Usage: python reverse_pair_gaps.py
"""

import numpy as np
import time

L, R = 10262, 26102
NEXT = 1914467
HIGH = 943901200000

_BASES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]


def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in _BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def prev_next(n):
    lo, hi = n, n
    while not is_prime(lo):
        lo -= 1
    while not is_prime(hi):
        hi += 1
    return lo, hi


def sieve_range(a, b):
    """array of primes in [a, b] (index i <-> value a + i)."""
    n = b - a + 1
    s = np.ones(n, dtype=bool)
    sb = int(b ** 0.5)
    bs = np.ones(sb + 1, dtype=bool)
    bs[:2] = False
    for p in range(2, int(sb ** 0.5) + 1):
        if bs[p]:
            bs[p * p::p] = False
    for p in np.nonzero(bs)[0]:
        start = max(p * p, ((a + p - 1) // p) * p)
        s[start - a::p] = False
    return np.nonzero(s)[0] + a


def gap_report(name, lo, hi, hist_lo=20):
    t0 = time.time()
    P = sieve_range(lo, hi)
    g = np.diff(P)
    t = time.time() - t0
    j = int(np.argmax(g))
    print(f"  [{lo:,}, {hi:,}]: {len(P):,} primes in {t:.2f}s | "
          f"max gap {g.max():,} at p={P[j]:,} | mean {g.mean():.2f} "
          f"| min {g.min()}")
    big = {int(x): int((g == x).sum()) for x in sorted(set(g.tolist()))}
    sel = {k: v for k, v in big.items() if k >= hist_lo}
    if sel:
        print(f"    gap histogram (>= {hist_lo}): "
              + ", ".join(f"{k}:{v}" for k, v in sorted(sel.items())))
    print(f"    gaps divisible by 80: {int((g % 80 == 0).sum())} "
          f"(values {sorted(set(g[g % 80 == 0].tolist()))})")
    print(f"    gaps divisible by 11: {int((g % 11 == 0).sum())}")
    return P, g


print("=" * 72)
print("T57: THE REVERSE PAIR 10262 <-> 26102 THROUGH PRIME GAPS")
print("=" * 72)

# ---------------- PART 1 ----------------
print("\nPART 1: THE RELATIONS")
ds = lambda n: sum(map(int, str(n)))
print(f"  reverse(10262) = {int(str(L)[::-1]):,}  (=26102: {str(R) == str(L)[::-1]})")
print(f"  {R:,} - {L:,} = {R - L:,} = 80 x {(R - L) // 80}   "
      f"(divisible by 80: {(R - L) % 80 == 0})")
print(f"  digit sum {L:,} = {ds(L)}   digit sum {R:,} = {ds(R)}   "
      f"(both 11: {ds(L) == ds(R) == 11})")

# ---------------- PART 2 ----------------
print("\nPART 2: PRIME-GAP CENSUS")
P1, g1 = gap_report("PAIR", L, R, hist_lo=14)
print(f"  enclosing primes of {L:,}: {prev_next(L)}  "
      f"(digit sums {ds(prev_next(L)[0])},{ds(prev_next(L)[1])})")
print(f"  enclosing primes of {R:,}: {prev_next(R)}  "
      f"(digit sums {ds(prev_next(R)[0])},{ds(prev_next(R)[1])})")
P2, g2 = gap_report("MID", R, NEXT, hist_lo=40)

# ---------------- PART 3 ----------------
print("\nPART 3: EMIRPS AND DIGIT-SUM-11 PRIMES IN [10262, 26102]")
sieve = np.ones(100000, dtype=bool)
sieve[:2] = False
for p in range(2, 317):
    if sieve[p]:
        sieve[p * p::p] = False
emirps, ds11 = [], []
for p in P1.tolist():
    r = int(str(p)[::-1])
    if r != p and r < 100000 and sieve[r]:
        emirps.append((p, r))
    if ds(p) == 11:
        ds11.append(p)
print(f"  emirps (p and reverse(p) both prime): {len(emirps)}  "
      f"first few: {emirps[:6]}")
print(f"  primes with digit sum 11: {len(ds11)}  first few: {ds11[:6]}")
print(f"  note: the pair's own digit sum 11 recurs "
      f"{100 * len(ds11) / len(P1):.1f}% of primes in the interval")

# ---------------- PART 4 ----------------
print("\n" + "=" * 72)
print("PART 4: RECOMMENDED ACTION / EFFICIENT PROCESS")
print("=" * 72)
print("  For the 9.4e11 endpoint, sieving is wrong (needs ~3.6e10 primes).")
print("  Efficient exact process at that scale:")
print("    1. Lucy_Hedgehog/Lehmer prime-count gives pi(943901200000) in")
print("       ~1e6 ops + log N primes, not a 1e12 sieve.  (~seconds)")
print("    2. Segmented sieve over (N, N + ln^2 N] finds the record gap")
print("       at Cramer scale (~1520) with O(sqrt N) memory.")
print("    3. In the net project, the analogous wall is the O(n^2) flow:")
print("       the O(1)-per-neuron spatial search is the efficient fix,")
print("       exactly as segmented sieve is the efficient fix here.")
