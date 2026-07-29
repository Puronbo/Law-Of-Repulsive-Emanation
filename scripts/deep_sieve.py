"""
Deep congruence sieve: find candidates for 2^n - 3 (k=3) beyond n=5630.
Filters with trial division by primes up to 10000, then Miller-Rabin on survivors.
"""
import sys, time, random

sys.set_int_max_str_digits(100000)

# Primes from 200 to ~10000 for deep trial division
def primes_upto(N):
    sieve = [True] * (N + 1)
    sieve[0:2] = [False, False]
    for p in range(2, int(N**0.5) + 1):
        if sieve[p]:
            sieve[p*p:N+1:p] = [False] * ((N - p*p)//p + 1)
    return [i for i, is_p in enumerate(sieve) if is_p]

SMALL = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,
         67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,
         139,149,151,157,163,167,173,179,181,191,193,197,199]

DEEP = primes_upto(10000)
DEEP = [p for p in DEEP if p >= 200]  # only new primes

def trial_sieve(n, k, primes):
    for p in primes:
        if pow(2, n, p) == k % p:
            return p
    return None

N_START = 5631
N_END = 20000
K = 3

print(f"Deep sieve: 2^n - {K}, n={N_START}..{N_END}")
print(f"Stage 1: trial division by {len(SMALL)} small primes", flush=True)

# Stage 1: quick trial division by small primes
candidates = []
for n in range(N_START, N_END + 1, 2):
    f = trial_sieve(n, K, SMALL)
    if f is None:
        candidates.append(n)

print(f"  Survivors after stage 1: {len(candidates)}", flush=True)

print(f"Stage 2: trial division by {len(DEEP)} primes (200..10000)", flush=True)

# Stage 2: deeper trial division
survivors = []
t0 = time.time()
for i, n in enumerate(candidates):
    f = trial_sieve(n, K, DEEP)
    if f is None:
        survivors.append(n)
    if (i + 1) % 500 == 0:
        t = time.time() - t0
        print(f"  checked {i+1}/{len(candidates)}, found {len(survivors)} survivors, {t:.0f}s", flush=True)

t = time.time() - t0
print(f"Stage 2 complete: {len(survivors)} survivors in {t:.0f}s")
print(f"Survivor n values: {survivors}")

if survivors:
    print(f"\nStage 3: Miller-Rabin (k=5) on survivors", flush=True)
    for n in survivors:
        v = (1 << n) - K
        d = n * 30103 // 100000
        t0 = time.time()
        # 1 round MR
        r, s = 0, v - 1
        while s % 2 == 0:
            r += 1
            s //= 2
        a = 2
        x = pow(a, s, v)
        if x == 1 or x == v - 1:
            t = time.time() - t0
            print(f"  n={n} ({d} digits): survived 1 round MRI, {t:.1f}s", flush=True)
        else:
            composite = False
            for _ in range(r - 1):
                x = pow(x, 2, v)
                if x == v - 1:
                    break
            else:
                t = time.time() - t0
                print(f"  n={n} ({d} digits): composite after 1 round, {t:.1f}s", flush=True)
                continue
            t = time.time() - t0
            print(f"  n={n} ({d} digits): survived 1 round MRI, {t:.1f}s", flush=True)
