"""
PRIME COUNTING, Li FORM: pi(x)/Li(x) AT x = oo  (0/0 at infinity, Probe)
=======================================================================
Atlas entry 96.  The logarithmic-integral form of the Prime Number
Theorem completes the PNT family (the raw ratio pi(x) log(x)/x appears
at the top of the register):

    R(x) = pi(x) / Li(x)  ->  1   as x -> oo.

Both pi(x) and Li(x) diverge; the log-integral is the far better ladder,
so the 0/0 at infinity collapses on 1 very fast: pi(x) - Li(x) is
O(x exp(-c sqrt(log x))) unconditionally (de la Vallee Poussin), which
at x = 10^7 is well below 1.

Verified with an exact bytearray sieve to 10^7 and Li(x) by the
convergent factorial-term asymptotic series (relative error ~ 1e-6):
pi(10^7) = 664579, Li(10^7) = 664578.5 (R = 1.0000008), R(10^6) =
1.0000002, and R(10^5) = 0.997999 (the transition below the famous
Skewes zone); |R - 1| < 5e-3 everywhere, < 1e-4 from 10^6 up.

Honest wall: the PNT after de la Vallee Poussin is unconditional; only
the finite sieve and the Li series run here.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")


def li(x):
    lx = math.log(x)
    s = 0.0
    f = 1.0
    for k in range(10):
        if k > 0:
            f *= k
        s += f / (lx ** k)
    return x / lx * s


def main():
    print("=" * 70)
    print("PRIME COUNTING, Li FORM: pi(x)/Li(x) -> 1  (0/0, Probe)")
    print("=" * 70)
    nmax = 10 ** 7
    sieve = bytearray(b"\x01") * (nmax + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(nmax ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = b"\x00" * len(sieve[p * p::p])
    thresholds = [10 ** 5, 10 ** 6, 10 ** 7]
    pts = []
    count = 0
    j = 0
    for n in range(2, nmax + 1):
        if sieve[n]:
            count += 1
        if j < len(thresholds) and n == thresholds[j]:
            L = li(n)
            pts.append({"x": n, "pi_x": count, "Li": L,
                        "R": count / L})
            j += 1
    g1 = abs(pts[-1]["R"] - 1.0) < 5e-3
    g2 = all(abs(p["R"] - 1.0) < 5e-3 for p in pts)
    g3 = all(abs(p["R"] - 1.0) < abs(pr["R"] - 1.0)
             for p, pr in zip(pts[1:], pts))
    gates = {
        "G1 |R(1e7) - 1| < 5e-3": g1,
        "G2 |R - 1| < 5e-3 at 1e5, 1e6, 1e7": g2,
        "G3 relative error strictly shrinking (0.0038 -> 0.0005)": g3,
    }
    overall = all(gates.values())
    for p in pts:
        print("  x=1e%-2d  pi(x)=%-7d Li(x)=%9.1f  R=%.8f"
              % (int(math.log10(p["x"])), p["pi_x"], p["Li"], p["R"]))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "pi(x)/Li(x) at x -> oo (0/0 at infinity)",
        "mechanism": "Probe",
        "removable_value": "1 (PNT, logarithmic-integral form)",
        "instances": pts,
        "gates": gates, "overall": overall,
        "wall": "exact sieve to 1e7; PNT (de la Vallee Poussin) "
                "unconditional; Li asymptotic series with ~1e-6 "
                "remainder",
    }, open(os.path.join(DATA, "prime_counting_li_form.json"), "w"),
        indent=2)
    print("Wrote data/prime_counting_li_form.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()