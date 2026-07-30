"""
Segmented Sieve Benchmark — T31 PNT Window Verification

Verifies Li(x) prediction against actual prime counts in
2e6-wide windows from 1e6 to 1e15, using O(sqrt(x)) memory.
"""
import math, time, numpy as np

WINDOW = 2_000_000

def segmented_primes_in_window(start, n_primes_seeds):
    """Count primes in [start, start+WINDOW) using segmented sieve."""
    limit = start + WINDOW - 1
    sqrt_limit = int(limit ** 0.5) + 1
    # Use precomputed small primes up to sqrt(limit)
    small_primes = []
    sieve = bytearray(b'\x01') * (sqrt_limit + 1)
    sieve[0:2] = b'\x00\x00'
    for i in range(2, sqrt_limit + 1):
        if sieve[i]:
            small_primes.append(i)
            step = i
            start_i = i * i
            sieve[start_i: sqrt_limit + 1: step] = b'\x00' * (((sqrt_limit - start_i) // step) + 1)
    # Segmented sieve for the window
    seg = bytearray(b'\x01') * WINDOW
    if start == 1:
        seg[0] = 0
    for p in small_primes:
        first = max(p * p, ((start + p - 1) // p) * p)
        for j in range(first, limit + 1, p):
            seg[j - start] = 0
    return sum(seg), len(small_primes)

def li(x):
    """Logarithmic integral Li(x) — approximation of pi(x)."""
    if x < 2:
        return 0.0
    from scipy.special import expn
    # Use series expansion for Li(x) = Ei(log x)
    # Ei(x) = gamma + ln|x| + sum_{k=1}^\infty x^k / (k * k!)
    # For large x, use scipy's expn or approximate
    from mpmath import li as mp_li
    return float(mp_li(x))

# Scales to test
scales = [1e6, 1e9, 1e12, 1e15]

print(f"Segmented Sieve Benchmark (window={WINDOW:,})")
print(f"{'Scale':>12} {'Actual':>10} {'Li(x)':>12} {'Error':>10} {'AvgGap':>10} {'log x':>10} {'Time':>8}")
print("-" * 72)

for sx in scales:
    x = int(sx)
    t0 = time.time()
    actual_pi, n_small = segmented_primes_in_window(x, 200_000)
    elapsed = time.time() - t0
    predicted = li(x + WINDOW) - li(x)
    error_pct = abs(actual_pi - predicted) / actual_pi * 100
    avg_gap = WINDOW / actual_pi if actual_pi > 0 else 0
    log_x = math.log(x)
    max_gap = 0
    # compute gaps for max
    prev = x
    # re-scan for max gap (simplified: use the seg array)
    # This is slow for large scales, skip for now
    print(f"{sx:>12.0e} {actual_pi:>10,} {predicted:>12.1f} {error_pct:>9.3f}% {avg_gap:>10.2f} {log_x:>10.2f} {elapsed:>7.2f}s")
