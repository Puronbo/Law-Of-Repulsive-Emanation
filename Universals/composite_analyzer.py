"""
Composite distribution analysis on the natural numbers up to N.

Three patterns, all direct sieve consequences:
1. Last-digit distribution — composites ending in 0,2,4,5,6,8 are saturated
   (multiples of 2 or 5); 1,3,7,9 are rarer (compete with primes).
2. Smallest-prime-factor (SPF) decay — fraction whose smallest factor is p
   matches the sieve prediction: (1/p) * prod_{q < p} (1 - 1/q).
3. Composite run-length between consecutive primes = gap - 1.
   The distribution ties directly to the prime-gap spectrum (T30/T31).
"""
import math
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))


def eratosthenes_sieve(n: int) -> np.ndarray:
    """Return boolean array is_prime[0..n]."""
    is_prime = np.ones(n + 1, dtype=bool)
    is_prime[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            is_prime[i * i : n + 1 : i] = False
    return is_prime


def smallest_prime_factor(n: int, primes: list[int]) -> int:
    """Return the smallest prime factor of n (n > 1)."""
    for p in primes:
        if p * p > n:
            return n
        if n % p == 0:
            return p
    return n


def sieve_spf_prediction(p: int, primes_below: list[int]) -> float:
    r"""Sieve prediction: fraction not caught by smaller primes, times 1/p.

    predicted_fraction(p) = (1/p) * prod_{q < p} (1 - 1/q).
    """
    survived = 1.0
    for q in primes_below:
        survived *= 1.0 - 1.0 / q
    return survived / p


def analyze_composites(N: int = 200_000) -> dict:
    """Compute all three composite patterns up to N."""
    is_prime = eratosthenes_sieve(N)
    primes = [i for i, v in enumerate(is_prime) if v]

    # 1. Last-digit distribution of composites
    last_digit_counts = {d: 0 for d in range(10)}
    composite_count = 0
    for i in range(2, N + 1):
        if not is_prime[i]:
            last_digit_counts[i % 10] += 1
            composite_count += 1

    # 2. Smallest-prime-factor distribution
    spf_counts = {}
    for i in range(2, N + 1):
        if not is_prime[i]:
            spf = smallest_prime_factor(i, primes)
            spf_counts[spf] = spf_counts.get(spf, 0) + 1

    spf_sorted = sorted(spf_counts.items())
    spf_empirical = {p: cnt / composite_count for p, cnt in spf_sorted}

    # Sieve prediction for SPF
    spf_predicted = {}
    for p, _ in spf_sorted:
        lower_primes = [q for q in primes if q < p]
        spf_predicted[p] = sieve_spf_prediction(p, lower_primes)

    # 3. Composite run-lengths between consecutive primes = gap - 1
    gaps = [primes[i + 1] - primes[i] for i in range(len(primes) - 1)]
    run_lengths = [g - 1 for g in gaps if g > 1]

    from collections import Counter
    run_counter = Counter(run_lengths)
    run_dist = sorted(run_counter.items())

    # Stats
    avg_run = float(np.mean(run_lengths)) if run_lengths else 0.0
    max_run = max(run_lengths) if run_lengths else 0
    most_common_run, most_common_count = run_dist[0] if run_dist else (0, 0)
    median_run = float(np.median(run_lengths)) if run_lengths else 0.0

    return {
        "N": N,
        "total_composites": composite_count,
        "total_primes": len(primes),
        # Pattern 1: last-digit
        "last_digit": last_digit_counts,
        # Pattern 2: SPF
        "spf_empirical": spf_empirical,
        "spf_predicted": spf_predicted,
        # Pattern 3: run-lengths
        "run_length_stats": {
            "avg_run_length": avg_run,
            "median_run_length": median_run,
            "max_run_length": max_run,
            "most_common_run": most_common_run,
            "most_common_count": most_common_count,
        },
        "run_length_distribution": run_dist,
        "gaps": gaps,
    }


def print_report(result: dict):
    """Pretty-print the composite analysis."""
    N = result["N"]
    print(f"\n{'='*65}")
    print(f"  COMPOSITE DISTRIBUTION ANALYSIS  (N = {N:,})")
    print(f"{'='*65}")
    print(f"  Total numbers:         {N:,}")
    print(f"  Composites:            {result['total_composites']:,}")
    print(f"  Primes:                {result['total_primes']:,}")
    print(f"  Composite fraction:    {result['total_composites']/N*100:.2f}%")

    # Pattern 1
    print(f"\n  --- Pattern 1: Last-Digit Distribution ---")
    ld = result["last_digit"]
    total = sum(ld.values())
    for d in range(10):
        pct = ld[d] / total * 100
        marker = " SATURATED" if d in {0, 2, 4, 5, 6, 8} else " prime-competing"
        print(f"    Ending in {d}: {ld[d]:>7,} ({pct:5.2f}%){marker}")

    # Pattern 2
    print(f"\n  --- Pattern 2: Smallest-Prime-Factor Decay ---")
    print(f"     p   empirical  predicted  ratio")
    print(f"    {'-'*40}")
    for p in sorted(result["spf_empirical"].keys()):
        emp = result["spf_empirical"][p] * 100
        pred = result["spf_predicted"].get(p, 0) * 100
        ratio = emp / pred if pred > 0 else 0
        print(f"    {p:>3}:  {emp:6.2f}%   {pred:6.2f}%   {ratio:5.3f}")
        if p >= 29:
            remaining = sum(result["spf_empirical"].get(q, 0) for q in result["spf_empirical"] if q > 29)
            if remaining > 0:
                print(f"    >29:  {remaining*100:6.2f}%   (remainder)")
            break

    # Pattern 3
    print(f"\n  --- Pattern 3: Composite Run-Lengths (prime gaps - 1) ---")
    rs = result["run_length_stats"]
    print(f"    Average run length:   {rs['avg_run_length']:.2f}")
    print(f"    Median run length:    {rs['median_run_length']:.2f}")
    print(f"    Max run length:       {rs['max_run_length']:,}")
    print(f"    Most common run:      {rs['most_common_run']} "
          f"(appears {rs['most_common_count']:,} times)")

    # Top 10 run lengths
    print(f"\n    Top 10 composite run-lengths:")
    print(f"    run_len  count   freq    note")
    print(f"    {'-'*40}")
    for run_len, cnt in result["run_length_distribution"][:10]:
        freq = cnt / len(result["gaps"]) * 100
        gap = run_len + 1
        note = f"gap={gap}" if gap <= 20 else ""
        print(f"       {run_len:>2}     {cnt:>5,}   {freq:5.2f}%   {note}")


if __name__ == "__main__":
    result = analyze_composites(200_000)
    print_report(result)
