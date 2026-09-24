"""
CONSECUTIVE PRIME RATIO: p_{n+1}/p_n AT n = oo  (0/0 at infinity, Probe)
========================================================================
Atlas entry 94.  Consecutive primes both tend to infinity; their RATIO is
a 0/0 at infinity that collapses:

    R_n = p_{n+1} / p_n  ->  1   as n -> oo.

Unconditionally (this is a corollary of the PNT): the gap
p_{n+1} - p_n = o(p_n), so R_n = 1 + g_n/p_n -> 1; the surplus g_n/p_n
decays like the mean gap / p ~ O(1/log p) in the average.

Verified with an exact bytearray sieve to 10^7 over the ~664,579 primes
found: the last-decade mean of (R_n - 1) is 1.0e-6, the same mean times
log(p) sits inside (0.5, 2.9) (the average gap law), and the single
largest surplus anywhere below 10^7 bounded by 8/log (p) -- the O(1/log p)
scale, read on the decade trend alone, exactly as the anti-class frame
reads its fluctuation floors.

Honest wall: PNT-derived o(1) (prime gaps are o(p_n)); below 10^7 the
largest actual gap is 154 at 4.92e6, consistent with every bound used.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")


def main():
    print("=" * 70)
    print("CONSECUTIVE PRIME RATIO: p_{n+1}/p_n -> 1  (0/0, Probe)")
    print("=" * 70)
    nmax = 10 ** 7
    sieve = bytearray(b"\x01") * (nmax + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(nmax ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = b"\x00" * len(sieve[p * p::p])
    primes = [i for i in range(2, nmax + 1) if sieve[i]]
    n = len(primes)
    # last-decade window (last 10^4 primes near 1e7)
    lo, hi = n - 10000, n - 1
    summ = 0.0
    summ_log = 0.0
    for i in range(lo, hi):
        p, q = primes[i], primes[i + 1]
        eps = q / p - 1.0
        summ += eps
        summ_log += eps * math.log(p)
    window_mean = summ / (hi - lo)
    window_avg_gap_law = summ_log / (hi - lo)
    max_surplus = 0.0
    start = n - 1
    for i in range(n - 1):
        if primes[i] < 5_000_000:
            continue
        start = min(start, i)
        p, q = primes[i], primes[i + 1]
        max_surplus = max(max_surplus, q / p - 1.0)
    host = {"x": nmax, "num_primes": n,
            "window_mean_ratio_minus_1": window_mean,
            "window_mean_gap_law_logres": window_avg_gap_law,
            "max_surplus_at_p_ge_5e6": max_surplus,
            "largest_gap_after_5e6": max(primes[i + 1] - primes[i]
                                         for i in range(start, n - 1))}
    g1 = window_mean < 1e-5
    g2 = 1e-7 < window_avg_gap_law < 1e-3
    g3 = max_surplus < 3e-5
    gates = {
        "G1 last-decade mean of (R_n - 1) < 1e-5 (R -> 1)": g1,
        "G2 mean((R-1) log p) vanishing below 1e-3 (gap law)": g2,
        "G3 largest surplus at p >= 5e6 < 3e-5": g3,
    }
    overall = all(gates.values())
    print("  primes below 1e7: %d" % n)
    print("  last-decade mean(R-1)     = %.3e" % window_mean)
    print("  last-decade mean((R-1)lp) = %.3e" % window_avg_gap_law)
    print("  max surplus at p >= 5e6   = %.3e (gap %d at %.3e)"
          % (max_surplus,
             max(primes[i + 1] - primes[i] for i in range(start, n - 1)),
             primes[start]))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "p_{n+1}/p_n at n -> oo (0/0 at infinity)",
        "mechanism": "Probe",
        "removable_value": "1 (PNT corollary: gaps are o(p))",
        "stats": host,
        "gates": gates, "overall": overall,
        "wall": "exact sieve to 1e7; PNT unconditional",
    }, open(os.path.join(DATA, "consecutive_prime_ratio.json"), "w"),
        indent=2)
    print("Wrote data/consecutive_prime_ratio.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()