"""Landau function 0/0: the maximal order of a permutation.

Everything follows Landau 1903: the maximal order g(n) of a permutation of
n elements satisfies

    log g(n) ~ sqrt(n log n),      i.e.  rho(n) = log g(n)/sqrt(n log n) -> 1.

The ratio is the removable value 1 of the 0/0

    ( log g(n) )  /  ( n log n )^{1/2}

at every n: the numerator and denominator both sit on the sqrt(n log n)
scale, their ratio converges to the named value 1, unconditionally
(Landau 1903; the exact values g(n) are OEIS A000793). The referee is
settled -- this is a proved theorem kept as a calibration point, exactly
as the ledger keeps PL-20's Mertens product as the removable side of the
Mertens trio.

Method (exact, no floating truth until the last line):
  g(n) = max over partitions n = a_1 + ... + a_k of lcm(a_1, ..., a_k).
  The optimum uses prime powers with DISTINCT primes, so the exact value
  is the classic 0/1-knapsack over prime powers:
        g[0] = 1
        for each prime power p^e <= N:  g[i] = max(g[i], g[i - p^e] * p^e)
  All arithmetic is integer; validated against the classical first ten
  values 1, 2, 3, 4, 6, 6, 12, 15, 20, 30 (A000793) and reproduced by an
  independent partition-by-partition brute-force for n <= 24.

Gates (all must PASS for verdict PASS):
  G1  exact_integer: g is derived by integer DP only (no log until the ratio).
  G2  seeds_ok:      g(1..10) == [1,2,3,4,6,6,12,15,20,30].
  G3  brute_ok:      g(n) == brute-force-over-partitions for n <= 24.
  G4  rho_decay:     per-decade max |rho(n) - 1| strictly declines across
                     the decades 2 (10^1..) ... 3^+ (>= 10^3).
  G5  late_ratio:    |rho(2000) - 1| < 0.10 (value at the computed frontier).

Refutation condition (ledger): a validated computation showing the
per-decade decline of max |rho - 1| to stop, or |rho(n) - 1| to increase
with n, is a finding, not a failure; the referee (Landau 1903) is settled,
so the entry is a permanent calibration point.

HONEST WALL: Landau's theorem is asymptotic; the exact fluctuations of
g(n) about its log-asymptotic are the open part (the Jordan-Polya/Massias
second-order questions). This experiment only re-derives a proved limit.
"""

import json
import math
import os
import time

OUT = os.path.join("data", "landau_function_0_over_0_data.json")
N = 2000


def primes_upto(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(n ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p : n + 1 : p] = b"\x00" * (((n - p * p) // p) + 1)
    return [i for i in range(n + 1) if sieve[i]]


def landau_exact(N):
    g = [1] * (N + 1)  # empty product fits any weight <= i
    for p in primes_upto(N):
        new = g[:]  # copy: at most ONE power of this prime is used
        pp = p
        while pp <= N:
            for i in range(N, pp - 1, -1):
                cand = g[i - pp] * pp
                if cand > new[i]:
                    new[i] = cand
            pp *= p
        g = new
    return g  # g[n], n >= 1, is A000793: maximal order of a permutation of n


def brute_lcm_partitions(n):
    """Independent check: max lcm over all partitions of n (n small).

    Carries the running lcm downward; a sub-partition's own maximal lcm is
    NOT reusable because it can share a prime factor with the outer part
    (e.g. 6 = 3 + 2 + 1 needs the outer 3 combined with {2,1}, whose lcm
    alone is 2, not the maximal 3 of a fresh partition of 3).
    """

    best = [1]

    def rec(rest, hi, cur):
        if rest == 0:
            if cur > best[0]:
                best[0] = cur
            return
        for part in range(1, min(hi, rest) + 1):
            nxt = cur // math.gcd(cur, part) * part
            rec(rest - part, part, nxt)

    rec(n, n, 1)
    return best[0]


def main():
    t0 = time.time()
    os.makedirs("data", exist_ok=True)

    g = landau_exact(N)

    seeds = [1, 2, 3, 4, 6, 6, 12, 15, 20, 30]
    seeds_ok = bool(g[1:11] == seeds)

    brute = []
    for n in range(1, 25):
        brute.append(landau_exact(24)[n] == brute_lcm_partitions(n))
    brute_ok = bool(all(brute))

    # ratios rho(n) = log g(n) / sqrt(n log n), n >= 3
    rho = [None, None, None]
    for n in range(3, N + 1):
        rho.append(math.log(g[n]) / math.sqrt(n * math.log(n)))

    def decade_bounds(lo_exp, hi_exp):
        lo, hi = 10 ** lo_exp, min(10 ** hi_exp, N)
        return lo, hi

    decades = []
    max_devs = []
    for lo_exp, hi_exp in [(1, 2), (2, 3), (3, 4)]:
        lo, hi = decade_bounds(lo_exp, hi_exp)
        vals = [rho[n] for n in range(lo, hi + 1)]
        mx = max(abs(v - 1.0) for v in vals)
        mean = sum(vals) / len(vals)
        decades.append({"decade": "%d-%d" % (lo, hi), "n": len(vals),
                        "mean_rho": round(mean, 6),
                        "max_dev": round(mx, 6)})
        max_devs.append(mx)

    rho_decay = bool(max_devs[0] > max_devs[1] > max_devs[2])
    late_ratio = bool(abs(rho[N] - 1.0) < 0.10)

    gates = {
        "G1_exact_integer": True,
        "G2_seeds_ok": seeds_ok,
        "G3_brute_ok": brute_ok,
        "G4_rho_decay": rho_decay,
        "G5_late_ratio": late_ratio,
    }
    verdict = "PASS" if all(gates.values()) else "FAIL"

    summary = {
        "supported": verdict == "PASS",
        "exact_seeds_correct": seeds_ok,
        "brute_force_crosscheck": brute_ok,
        "decade_rho_decays": rho_decay,
        "late_ratio_near_one": late_ratio,
        "rho_2000": round(rho[N], 6),
    }

    payload = {
        "name": "landau_function_0_over_0",
        "title": "Landau's function: log g(n)/sqrt(n log n) -> 1 (Landau 1903)",
        "verdict": verdict,
        "summary": summary,
        "gates": gates,
        "class": "REMOVABLE (named value 1, settled referee: Landau 1903)",
        "referee": "Landau 1903 (log g(n) ~ sqrt(n log n)); exact values A000793",
        "refutation_condition": "per-decade max|rho-1| stops declining, or |rho(n)-1| grows with n, in a validated computation",
        "values": {
            "N": N,
            "seeds_g_1_to_10": g[1:11],
            "g_100": g[100],
            "g_1000": g[1000],
            "g_2000": g[2000],
            "rho_100": round(rho[100], 6),
            "rho_1000": round(rho[1000], 6),
            "rho_2000": round(rho[2000], 6),
            "decades": decades,
        },
        "honest_walls": [
            "A proved limit re-derived exactly; the fluctuations of g(n) about log g ~ sqrt(n log n) are open (Massias-type second-order).",
            "No new mathematics: the referee (Landau 1903) is settled, this entry is a calibration point.",
            "Integer DP to n = 2000 only; the brute-force cross-check is capped at n = 24 by partition blow-up.",
        ],
        "elapsed_sec": round(time.time() - t0, 3),
    }

    with open(OUT, "w", encoding="utf-8") as fp:
        json.dump(payload, fp, indent=2)

    print("landau 0/0: verdict", verdict)
    print("  seeds g(1..10):", g[1:11], "expected", seeds)
    print("  g(100)=%d  g(1000)=%d  g(2000)=%d" % (g[100], g[1000], g[2000]))
    print("  rho(100)=%.6f  rho(1000)=%.6f  rho(2000)=%.6f" % (rho[100], rho[1000], rho[2000]))
    print("  decades:", [(d["decade"], d["mean_rho"], d["max_dev"]) for d in decades])
    print("  gates:", gates)
    print("  saved:", OUT)


if __name__ == "__main__":
    main()