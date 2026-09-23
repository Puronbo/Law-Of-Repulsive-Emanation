"""NUMBER THEORY (ANTI-CLASS): MERTENS FUNCTION M(n)/n^(1/2), SECOND
MEMBER OF THE CLASS THE CORPUS FOUNDED AS EMPTY.

Atlas entry 67.  Companion to entry 64 (Polya/Liouville): the two OEIS
random walks at the sqrt scale -- F(n) = sum lambda(k) and
M(n) = sum mu(k) -- are the canonical anti-class members.  The 0/0 form
M(n)/n^(1/2) has no limit: the Mertens conjecture |M(n)| < sqrt(n) is
FALSE.

Odlyzko & te Riele (1985, proved):  limsup M(n)/sqrt(n) > 1.06  and
liminf M(n)/sqrt(n) < -1.009.  Unlike Polya (first + at 906,150,257),
no explicit counterexample to the Mertens conjecture is known: the
conjecture has been verified to 10^23 (Helfgott & Thompson 2021) and
still stands numerically everywhere it has been checked -- the farthest
0/0 whose removable value waits beyond every verified range.

The verification here is the mirror of entry 64:
  - exact mu(n) for n <= 1e8 (Mobius sieve),
  - the sum-over-divisors identity sum_{d|n} mu(d) = [n==1] (a theorem
    gate, independent of any literature table),
  - M(10^k) at k = 4..8 against literature (A084237),
  - the fluctuation exponent beta of the running max of |M(n)| across
    decades: calibration target 1/2 (fluctuations sit on the sqrt(n)
    denominator, the signature of the anti-class),
  - the honest wall: |M(n)| < sqrt(n) holds on [2, 1e8] -- it is
    designed to fail, and Odlyzko-te Riele prove it fails.

All |M| census, near-miss ratios and fluctuation bins are accumulated in
a single streaming walk over the prefix sum (no M-array, no rmax-array):
the running max is monotone, so each decade's bin value is the running
max the moment the walk exits that decade.

Mechanism: ANTI-CLASS (the removable value does not exist).
"""

import json
import math
import os
import sys
from array import array

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")

KNOWN_M_POW10 = {4: -23, 5: -48, 6: 212, 7: 1037, 8: 1928}  # A084237


def mobius_summatory_sieve(N):
    """exact mu(0..N), byte-array backed (signed char)."""
    mu = array("b", [1]) * (N + 1)
    mu[0] = 0
    sc = bytearray([1]) * (N + 1)
    sc[0] = sc[1] = 0
    for i in range(2, int(N ** 0.5) + 1):
        if sc[i]:
            sc[i * i::i] = bytearray(len(sc[i * i::i]))
    primes = [i for i in range(2, N + 1) if sc[i]]
    for p in primes:
        p2 = p * p
        if p2 > N:
            break
        mu[p2::p2] = array("b", [0]) * (len(mu[p2::p2]))
    for p in primes:
        for j in range(p, N + 1, p):
            mu[j] = -mu[j]
    return mu


def mobius_inversion_check(mu, upto):
    """sum_{d|n} mu(d) == 1 iff n == 1, else 0, for n <= upto."""
    for n in range(1, upto + 1):
        sm = 0
        d = 1
        while d * d <= n:
            if n % d == 0:
                sm += mu[d]
                e = n // d
                if e != d:
                    sm += mu[e]
            d += 1
        want = 1 if n == 1 else 0
        if sm != want:
            return False
    return True


def fluctuation_beta(bins):
    """log-log slope of running-max-bin series (decade max of |M(n)|)."""
    xs = [math.log(10 ** (d + 0.5)) for d in sorted(bins) if d >= 2]
    ys = [math.log(bins[d]) for d in sorted(bins) if d >= 2]
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx if sxx else 0.0
    syy = sum((y - my) ** 2 for y in ys)
    r2 = (sxy * sxy) / (sxx * syy) if sxx and syy else 0.0
    return slope, r2, n


def main():
    print("=" * 70)
    print("MERTENS FUNCTION M(n)/sqrt(n): THE ANTI-CLASS, SECOND MEMBER")
    print("=" * 70)

    N = 100_000_000
    mu = mobius_summatory_sieve(N)
    print(f"  mu(n) computed for n <= {N:,}")

    # Gate 1: theorem gate, the sum-over-divisors identity (independent of
    # any literature table).
    g1 = mobius_inversion_check(mu, 300)
    print(f"  sum_{{d|n}} mu(d) = [n==1] for n <= 300: "
          f"{'OK' if g1 else 'FAIL'}")

    # Single streaming walk: prefix sum, spot values M(10^k), record
    # census, running max per decade (monotone -> decade bin = running max
    # at decade exit), and the near-miss ratio probes on windows.
    pow10 = {10 ** k for k in range(0, 9)}
    spot = {}
    bins = {}
    cp = 0
    prevd = -1
    s = 0
    rec_max = 0
    nrec = 0
    last_rec_n = 0
    max_r2 = max_r3 = max_r5 = 0.0
    at2 = at1e3 = at1e5 = 0
    top = []
    for n in range(1, N + 1):
        s += mu[n]
        if n in pow10:
            spot[n] = s
        a = s if s > 0 else -s
        if a > rec_max:
            rec_max = a
            nrec += 1
            last_rec_n = n
        if a > cp:
            cp = a
        d = int(math.floor(math.log10(n)) + 1e-9)
        if d != prevd:
            if prevd >= 2:
                bins[prevd] = cp
            prevd = d
        r = a / math.sqrt(n) if n >= 2 else 0.0
        if n >= 2:
            if r > max_r2:
                max_r2, at2 = r, n
            if len(top) < 5 or r > top[0][0]:
                top.append((r, n))
                top.sort(key=lambda z: z[0])
                top = top[-5:]
        if n >= 1000 and r > max_r3:
            max_r3, at1e3 = r, n
        if n >= 100000 and r > max_r5:
            max_r5, at1e5 = r, n
    bins[prevd] = cp  # top (partial) decade closed at the walk's end

    g2 = all(spot[10 ** k] == v for k, v in KNOWN_M_POW10.items())
    print(f"  M(10^k) for k=4..8: "
          f"{[spot[10**k] for k in range(4, 9)]}  "
          f"(A084237: -23, -48, 212, 1037, 1928)  "
          f"{'OK' if g2 else 'MISMATCH'}")

    g3 = max_r2 < 1.0  # |M(n)| < sqrt(n) throughout the verified range

    print("  nearest misses (max |M|/sqrt n):  n>=2: "
          f"{max_r2:.4f}@{at2:,}  n>=10^3: {max_r3:.4f}@{at1e3:,}  "
          f"n>=10^5: {max_r5:.4f}@{at1e5:,}")
    print("  top near-miss holders: " +
          ", ".join(f"n={n:,} ratio={r:.4f}" for r, n in reversed(top)))
    print(f"  Mertens bound |M(n)| < sqrt(n) on [2,{N:,}]: "
          f"{'HELD' if g3 else 'BROKEN'} (max ratio {max_r2:.4f} at "
          f"n={at2:,}); the conjecture is designed to fail -- "
          f"Odlyzko-te Riele prove limsup ratio > 1.06, liminf < -1.009")

    # Gate 4: fluctuation exponent.  Calibration target 1/2 (anti-class).
    beta, r2b, nd = fluctuation_beta(bins)
    g4 = 0.38 < beta < 0.62
    print(f"  fluctuation exponent beta = {beta:.3f} (r2={r2b:.2f}, "
          f"{nd} decades 10^2..10^8); target 0.5 = fluctuations sit ON "
          f"the sqrt(n) denominator")
    print(f"  record census: {nrec} new |M| maxima, last at "
          f"n={last_rec_n:,} > N/2 = {N // 2:,}")

    g5 = True  # Odlyzko-te Riele, cited: the limit of M(n)/sqrt(n) does not exist
    print("  anti-class cited: M(n)/sqrt(n) has NO limit (Odlyzko & te "
          "Riele 1985); like Polya (#64), no removable value exists")

    print("\n  M(10^k): " + ", ".join(
        f"M(10^{k})={spot[10 ** k]:>6,}" for k in range(0, 9)))

    gates = {"G1 Mobius inversion identity sum_{d|n} mu(d) = [n==1]": g1,
             "G2 M(10^k) matches A084237 (k=4..8)": g2,
             "G3 Mertens bound holds on [2,1e8] (honest wall, designed to fail)": g3,
             "G4 fluctuation exponent ~ 1/2 (anti-class, calibrated at Polya)": g4,
             "G5 no removable value (Odlyzko-te Riele, cited)": g5}
    overall = all(gates.values())
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'} (second anti-class "
          f"member; the removable value does not exist, and every verified "
          f"range keeps the conjecture alive)")
    os.makedirs(DATA, exist_ok=True)
    json.dump(
        {"form": "M(n)/n^(1/2), M(n) = sum_{k<=n} mu(k)",
         "mechanism": "ANTI-CLASS",
         "point": "n -> infinity (records)",
         "removable_value": None,
         "conjecture": "|M(n)| < sqrt(n) is FALSE (Odlyzko-te Riele 1985: "
                       "limsup ratio > 1.06, liminf < -1.009; no explicit "
                       "counterexample known; verified numerically to 10^23)",
         "M_at_powers_of_10": {str(k): spot[10 ** k] for k in range(0, 9)},
         "fluctuation_beta": beta, "beta_r2": r2b, "beta_ndecades": nd,
         "max_abs_ratio_in_range": max_r2, "argmax_ratio": at2,
         "near_miss_n_ge_1e3": {"ratio": max_r3, "at": at1e3},
         "near_miss_n_ge_1e5": {"ratio": max_r5, "at": at1e5},
         "top_near_miss_holders": [{"n": n, "ratio": r}
                                   for r, n in reversed(top)],
         "n_records": nrec, "last_record_n": last_rec_n,
         "gates": gates, "overall": overall,
         "wall": "exact mu to 1e8; first confirmed Mertens-counterexample "
                 "region not reachable (conjecture verified to 10^23 "
                 "externally)"},
        open(os.path.join(DATA, "mobius_mertens_0_over_0.json"), "w"),
        indent=2)
    print("Wrote data/mobius_mertens_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()