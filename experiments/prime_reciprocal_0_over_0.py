"""NUMBER THEORY (REMOVABLE, NAMED CONSTANT): THE PRIME-RECIPROCAL
(MEISSEL-MERTENS) CONSTANT B1.

Atlas entry 68.  The infinitary 0/0 form
    E(x) = sum_{p <= x} 1/p  -  log(log x)      (x -> infinity)
is "infinity minus infinity"; its limit exists and is the named constant

    B1 = 0.2614972128476427837554268386086958590515666482611992061920642...
    (OEIS A077761).

Mertens' second theorem (1874; conjectured by Meissel 1866) is the
existence statement -- the removable value is real, transcendental in
character, and known to hundreds of digits.  This is the *opposite pole*
of the anti-class entries 64 and 67: the fluctuation size of the
deviation |E(x) - B1| decays to zero (exponent < 0), whereas the
Polya/Mertens walks have fluctuation exponent ~ +1/2.

The verification here:
  - exact prime harmonic sum to x = 2e7 (Euler-Mertens is the limit of
    strict prime reciprocals; no prime powers),
  - decay signature: running max of |E(x) - B1| sampled at primes
    (between primes the sum is constant and log(log x) climbs, so
    extrema occur exactly at primes),
  - decay exponent beta (< 0) vs the anti-class beta ~ +1/2 -- the
    fluctuation-scale criterion of the aclass_detector, applied in the
    removable direction,
  - cross-tool consistency: pi(2e7) = 1,270,607 (matches the PNT probe
    in aclass_detector).

Mechanism: Probe (value exists; -- the constant is the answer to the
form's question).
"""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")

B1 = 0.2614972128476427837554268386086958590515666482611992061920642139


def primes_upto(N):
    sc = bytearray([1]) * (N + 1)
    sc[0] = sc[1] = 0
    for i in range(2, int(N ** 0.5) + 1):
        if sc[i]:
            sc[i * i::i] = bytearray(len(sc[i * i::i]))
    return [i for i in range(2, N + 1) if sc[i]]


def decay_slope(decades):
    xs = [math.log(10 ** (d["d"] + 0.5)) for d in decades
          if d["d"] >= 4]
    ys = [math.log(d["max_abs"]) for d in decades if d["d"] >= 4]
    n = len(xs)
    if n < 3:
        return 0.0, 1.0, n
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
    print("PRIME-RECIPROCAL CONSTANT B1: A 0/0 WHOSE VALUE HAS A NAME")
    print("=" * 70)

    N = 20_000_000
    primes = primes_upto(N)
    print(f"  primes <= {N:,}: {len(primes):,}")

    # single pass: accumulate sum 1/p; at each prime capture E(p) and the
    # running max of |E(p) - B1| per decade
    hi = int(round(math.log10(N)))
    decades = {}
    sum_rec = 0.0
    for p in primes:
        sum_rec += 1.0 / p
        dev = abs(sum_rec - math.log(math.log(p)) - B1)
        d = int(math.floor(math.log10(p)) + 1e-9)
        if dev > decades.get(d, 0.0):
            decades[d] = dev
    E = sum_rec - math.log(math.log(N))
    err = abs(E - B1)
    print(f"  E(2e7) = sum 1/p - log log x = {E:.9f}   "
          f"|E - B1| = {err:.2e}   (B1 = {B1:.18f})")

    rows = [{"d": d, "lo": 10 ** d, "hi": min(10 ** (d + 1) - 1, N),
             "max_abs": decades[d]} for d in sorted(decades)]
    for r in rows:
        print(f"  decade {r['lo']:>9,}-{r['hi']:>9,}: "
              f"max |E(x)-B1| = {r['max_abs']:.3e}")

    slope, r2s, nd = decay_slope(rows)
    print(f"  decay exponent of max|E-B1| vs x: beta = {slope:.2f} "
          f"(r2={r2s:.2f}, {nd} decades 10^4..10^7); "
          f"anti-class walks calibrate at +1/2 -- here the fluctuation "
          f"SHRINKS")

    g1 = err < 0.05
    g2 = rows[-1]["max_abs"] < rows[0]["max_abs"]
    g3 = slope < -0.3
    g4 = len(primes) == 1_270_607  # cross-tool: PNT probe in aclass_detector
    print("\n  pi(2e7) =", len(primes), "(aclass_detector P2: 1,270,607)")

    gates = {"G1 |E(2e7) - B1| < 0.05 (converges to the named constant)": g1,
             "G2 max|E-B1| decays decade-over-decade (final < first)": g2,
             "G3 decay exponent beta < -0.3 (vs anti-class beta ~ +1/2)": g3,
             "G4 pi(2e7) = 1,270,607 (cross-tool with aclass_detector P2)": g4}
    overall = all(gates.values())
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'} (the removable value "
          f"exists, has a name, and the fluctuations decay -- the exact "
          f"mirror of entries 64 and 67)")
    os.makedirs(DATA, exist_ok=True)
    json.dump(
        {"form": "sum_{p<=x} 1/p - log(log x)  (x -> infinity)",
         "mechanism": "Probe (named constant)",
         "point": "x -> infinity",
         "removable_value": B1,
         "constant": "B1 (OEIS A077761); Mertens' second theorem (1874)",
         "E_N": E, "abs_error_at_N": err,
         "decade_max_abs": rows, "decay_beta": slope, "decay_r2": r2s,
         "pi_N": len(primes),
         "gates": gates, "overall": overall,
         "wall": "exact prime harmonic to 2e7; B1 value external "
                 "(40+ digits cited, A077761)"},
        open(os.path.join(DATA, "prime_reciprocal_0_over_0.json"), "w"),
        indent=2)
    print("Wrote data/prime_reciprocal_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()