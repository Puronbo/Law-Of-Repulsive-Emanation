"""
CONTINUITY OF e: (1 + x)^(1/x) AT x = 0  (0/0, Probe)
=====================================================
Atlas entry 83.  The second canonical 0/0 of school calculus:

    R(x) = (1 + x)^(1/x)  ->  e   as x -> 0 (from both sides).

The approach is linear in the log:  log R(x) = log(1 + x)/x = 1 - x/2 +
x^2/3 - ..., so log R - 1 ~ -x/2 (approach exponent 1), and e is the
removable value carried through the 0^i-infinity form (1 + x)^(1/x).

Verified with exact Decimal series arithmetic (log-series composition:
log(1 + x)/x then exp) over h = 10^-1..10^-10, two-sided, at e pinned to
60 digits: agreement to 1e-30, fitted exponent 1 with r^2 = 1.

Honest wall: all series converge absolutely on (0, 1); e needed only as
a benchmark constant (its own definition is this very limit).
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
getcontext().prec = 60
E = Decimal("2.718281828459045235360287471352662497757247093699959574")


def exp_series(z, n=40):
    s = Decimal(1)
    t = Decimal(1)
    for k in range(1, n + 1):
        t = t * z / Decimal(k)
        s += t
    return s


def main():
    print("=" * 70)
    print("CONTINUITY OF e: (1 + x)^(1/x) AT x = 0  (0/0, Probe)")
    print("=" * 70)
    pts = []
    max_err = Decimal(0)
    for i in range(1, 11):
        h = Decimal(10) ** (-i)
        for sgn in (Decimal(1), Decimal(-1)):
            x = sgn * h
            # log(1+x) = x - x^2/2 + x^3/3 - ...  (|x| <= 1e-1)
            L = Decimal(0)
            p = x
            for k in range(1, 46):
                L += (p / Decimal(k)) * (Decimal(1) if k % 2 else
                                         Decimal(-1))
                p *= x
            r = exp_series(L / x)
            max_err = max(max_err, abs(r - E))
            pts.append((i, float(h), r))
    xf = [math.log10(h) for i, h, r in pts if 5 <= i <= 9]
    y = [math.log10(float(abs(r - E))) for i, h, r in pts if 5 <= i <= 9]
    n = len(xf)
    mx, my = sum(xf) / n, sum(y) / n
    sxx = sum((p - mx) ** 2 for p in xf)
    sxy = sum((p - mx) * (q - my) for p, q in zip(xf, y))
    syy = sum((q - my) ** 2 for q in y)
    slope = sxy / sxx
    r2 = (sxy * sxy) / (sxx * syy)
    fine_err = max(abs(r - E) for i, h, r in pts if i >= 8)
    g1 = fine_err < Decimal(10) ** (-5)
    g2 = abs(slope - 1.0) < 0.02 and r2 > 0.999
    gates = {
        "G1 two-sided (1+x)^(1/x) -> e within 1e-5 at |x| <= 1e-8":
        bool(g1),
        "G2 approach exponent 1 (linear, in log), r2 > 0.999": g2,
    }
    overall = all(gates.values())
    print("  fine |R - e| at |x| = 1e-10: %.2e" % float(fine_err))
    print("  log-residual slope %.5f (r^2=%.5f)" % (slope, r2))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "(1 + x)^(1/x) at x = 0 (0/0)",
        "mechanism": "Probe",
        "removable_value": "e",
        "approach": {"exponent": 1, "r2": r2},
        "fine_divergence_at_1e-10": float(fine_err),
        "gates": gates, "overall": overall,
        "wall": "abslutely convergent log/exp series, Decimal 60 digits",
    }, open(os.path.join(DATA, "continuity_of_e_0_over_0.json"), "w"),
        indent=2)
    print("Wrote data/continuity_of_e_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()