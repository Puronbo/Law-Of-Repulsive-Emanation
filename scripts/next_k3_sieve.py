"""
Sieve for the next 2^n - 3 prime beyond n = 5630 using T6/T7 congruence sieve.
"""
import math, time, sys

N_START = 5631
N_END = 30000
K = 3

SMALL_PRIMES = [
    2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,
    67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,
    139,149,151,157,163,167,173,179,181,191,193,197,199
]

def trial_sieve(n, k):
    v = (1 << n) - k
    for p in SMALL_PRIMES:
        if v % p == 0:
            return p
    return None

print(f"Sieving 2^n - {K} for n = {N_START}..{N_END}")
print(f"Trial dividing by {len(SMALL_PRIMES)} primes < 200")
print(f"n, factor, elapsed")
print("-" * 50)

candidates = []
checked = 0
t0 = time.time()

for n in range(N_START, N_END + 1, 2):
    checked += 1
    f = trial_sieve(n, K)
    if f is None:
        candidates.append(n)
        t = time.time() - t0
        print(f"candidate n={n}, no factor < 200, elapsed={t:.0f}s")
        sys.stdout.flush()

t = time.time() - t0
print(f"\nDone: {checked} n checked in {t:.0f}s")
print(f"Survivors (no factor < 200): {len(candidates)}")
print(f"n values: {candidates}")
