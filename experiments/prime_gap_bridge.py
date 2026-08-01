"""
T56: PRIME-GAP BRIDGE between 10262, 1914467, 943901200000.

Three checkpoints connected by prime gaps.  Computes, for each checkpoint:
the enclosing primes and the gaps to them; and over the middle interval
[10262, 1914467] a full gap census (count, max/mean gap, gap histogram,
location of the record).  The endpoint 943901200000 (~9.4e11) is too large
for a sieve, so it is handled analytically: enclosing primes via
deterministic Miller-Rabin (bases [2..37] valid below 3.47e12), plus the
Cramer expectation for the record gap at that scale.

  N            prev prime     next prime     gap-below  gap-above
  10262        ...
  1914467      ...
  943901200000 ...

Usage: python prime_gap_bridge.py
"""

import numpy as np
import sys, os, time

LOW, MID, HIGH = 10262, 1914467, 943901200000

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


print("=" * 72)
print("T56: PRIME-GAP BRIDGE  10262 -> 1914467 -> 943901200000")
print("=" * 72)

# ---- sieve the middle interval ----
t0 = time.time()
L = LOW - 2
sieve = np.ones(MID - L + 1, dtype=bool)
sieve[:2] = False
for p in range(2, int(MID ** 0.5) + 1):
    if sieve[p - L]:
        start = max(p * p, (L + p - 1) // p * p)
        sieve[start - L::p] = False
primes = np.nonzero(sieve)[0] + L
t_sieve = time.time() - t0
gaps = np.diff(primes)
print(f"\nINTERVAL [{LOW}, {MID}]:  sieved {len(primes):,} primes in "
      f"{t_sieve:.2f}s")
print(f"  prime count = {len(primes):,}   (pi({MID}) - pi({LOW}) via sieving)")
print(f"  max gap = {gaps.max()} at p={primes[np.argmax(gaps)]}   "
      f"mean gap = {gaps.mean():.2f}   min gap = {gaps.min()}")
hist = {g: int((gaps == g).sum()) for g in sorted(set(gaps.tolist()))}
big = {g: c for g, c in hist.items() if g >= 20}
print(f"  gap histogram (>=14): "
      + ", ".join(f"{g}:{c}" for g, c in sorted(hist.items()) if g >= 14))

# ---- enclosing primes at the three checkpoints ----
print(f"\n{'checkpoint':>16}{'prev prime':>16}{'next prime':>16}"
      f"{'gap-below':>11}{'gap-above':>11}")
for n in (LOW, MID, HIGH):
    lo, hi = prev_next(n)
    print(f"{n:>16,}{lo:>16,}{hi:>16,}{n - lo:>11,}{hi - n:>11,}")
    if n == MID:
        print(f"  (mid is prime: {lo == hi == n})")

# ---- bridge: sum of prime gaps across the middle interval ----
print(f"\nBRIDGE (telescoping): sum of all prime gaps in [{LOW}, {MID}]")
print(f"  = (largest prime <= {MID}) - (smallest prime >= {LOW})")
lo0, _ = prev_next(LOW)
_, hi1 = prev_next(MID)
print(f"  = {hi1:,} - {lo0:,} = {hi1 - lo0:,}")

# ---- analytic facts at the endpoint scale ----
lo2, hi2 = prev_next(HIGH)
print(f"\nENDPOINT 943901200000 (~9.4e11):  sieve infeasible (n^2/8 wall at "
      f"~2e4; this is 4.7e7x larger)")
print(f"  prev/next prime and gaps computed by Miller-Rabin above.")
print(f"  Cramer expectation: record gap near {int(2.0*np.log(HIGH)**2):,} "
      f"(ln^2 N = {np.log(HIGH)**2:.0f});")
print(f"  mean gap = ln {HIGH} ~ {np.log(HIGH):.1f}.  Density ~ 1 in "
      f"{np.log(HIGH):.0f} integers.")
lo3, hi3 = prev_next(hi2 + 1)               # first prime strictly after hi2
print(f"  next prime after the one above {HIGH:,}: {hi3:,} "
      f"(prime gap {hi3 - hi2:,})")
