"""
googol_census.py — Complete enumeration of all 2^n - 3 primes < 10^100

A googol = 10^100.  2^n - 3 < 10^100  ⟹  n ≤ 332.
Tests every n = 3..332 (odd) + even n known to work (2,4,6).
Outputs the full listing with C7 bridge values.
"""
import math, sys, time, json, random

sys.set_int_max_str_digits(10000)

SMALL_PRIMES = [
    2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,
    67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,
    139,149,151,157,163,167,173,179,181,191,193,197,199
]

def is_prime_mr(n, k=12):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    # trial division first (skip p == n since n divides itself)
    for p in SMALL_PRIMES:
        if p >= n: break
        if n % p == 0:
            return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, min(n - 2, 1000000))
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Upper bound: n_max = floor(100 / log10(2))
N_MAX = int(100 / math.log10(2))
print(f"Searching 2^n - 3 for n = 2..{N_MAX} (max digits: ~{int(N_MAX * math.log10(2))})")
print("=" * 60)

primes = []
t0 = time.time()
for n in range(2, N_MAX + 1):
    v = (1 << n) - 3
    if is_prime_mr(v, k=8):
        primes.append(n)
        nd = len(str(v))
        ell = n * math.log(2) - math.log(3)
        lam = 0.25 + ell**2
        t = time.time() - t0
        print(f"PRIME n={n:3d}  digits={nd:3d}  ell={ell:8.4f}  lam={lam:12.4f}  [{t:5.1f}s]")
    if n % 50 == 0:
        t = time.time() - t0
        print(f"  ... scanned n={n}, elapsed {t:.0f}s", flush=True)

t = time.time() - t0
print(f"\nDone in {t:.0f}s. Found {len(primes)} primes: {primes}")

# Compute C7 bridge for each
listing = []
for n in primes:
    v = (1 << n) - 3
    ell = n * math.log(2) - math.log(3)
    lam = 0.25 + ell**2
    listing.append({
        "n": n,
        "digits": len(str(v)),
        "prime": str(v),
        "geodesic_length": round(ell, 10),
        "selberg_eigenvalue": round(lam, 10),
        "selberg_r": round(ell, 10),
    })

output = {
    "title": "All 2^n - 3 Mersenne-gap primes less than a googol (10^100)",
    "googol": 10**100,
    "n_max": N_MAX,
    "count": len(primes),
    "primes": listing,
    "framework": "Puno Calculus — C7 Prime Geodesic Bridge (Selberg ↔ Mersenne)",
    "theorems": ["T6 (Parity sieve)", "T7 (Congruence sieve)", "C7 (Prime geodesic bridge)"],
}

with open("data/googol_census.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nSaved to data/googol_census.json")
