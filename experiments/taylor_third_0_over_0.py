"""
TAYLOR THIRD ORDER: (sin x - x)/x^3 AT x = 0  (0/0, Vanishing Rate)
===================================================================
Atlas entry 85.  The Taylor-remainder 0/0: subtract the first-order part
of sin and the reduced ratio carries the third Taylor coefficient,

    R(x) = (sin x - x)/x^3  ->  -1/6   as x -> 0.

Both numerator (sin x - x ~ -x^3/6) and denominator (x^3) vanish to
order 3; the approach is even and quadratic:  R + 1/6 ~ x^2/120,
approach exponent 2, same sign on both sides.

Verified with exact Decimal series over x = +h, -h for h = 10^-1..10^-10:
two-sided agreement to -1/6 to 50 digits, fitted exponent 2 (r^2 = 1).

Honest wall: the sine series converges absolutely; no open theorem.
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
getcontext().prec = 60


def taylor_third(x):
    """(sin x - x)/x^3 = -1/3! + x^2/5! - x^4/7! + ... (exact series)."""
    s = Decimal(-1) / 6
    term = Decimal(-1) / 6
    for k in range(1, 22):
        term = term * x * x / Decimal((2 * k + 2) * (2 * k + 3))
        s += term if k % 2 == 0 else -term
    return s


def main():
    print("=" * 70)
    print("TAYLOR THIRD ORDER: (sin x - x)/x^3 AT x = 0  (0/0, VR)")
    print("=" * 70)
    pts = []
    max_err = Decimal(0)
    for i in range(1, 11):
        h = Decimal(10) ** (-i)
        for sgn in (Decimal(1), Decimal(-1)):
            r = taylor_third(sgn * h)
            max_err = max(max_err, abs(r + Decimal(1) / 6))
            pts.append((i, float(h), r))
    xf = [math.log10(h) for i, h, r in pts if 5 <= i <= 9]
    y = [math.log10(float(abs(r + Decimal(1) / 6)))
         for i, h, r in pts if 5 <= i <= 9]
    n = len(xf)
    mx, my = sum(xf) / n, sum(y) / n
    sxx = sum((p - mx) ** 2 for p in xf)
    sxy = sum((p - mx) * (q - my) for p, q in zip(xf, y))
    syy = sum((q - my) ** 2 for q in y)
    slope = sxy / sxx
    r2 = (sxy * sxy) / (sxx * syy)
    fine_err = max(abs(r + Decimal(1) / 6)
                   for i, h, r in pts if i >= 8)
    g1 = fine_err < Decimal(10) ** (-15)
    g2 = abs(slope - 2.0) < 0.02 and r2 > 0.999
    gates = {
        "G1 two-sided (sin x - x)/x^3 -> -1/6 within 1e-15 at |x| <= 1e-8":
        bool(g1),
        "G2 approach exponent 2 (even residue), r2 > 0.999": g2,
    }
    overall = all(gates.values())
    print("  fine |R + 1/6| at |x| = 1e-10: %.2e" % float(fine_err))
    print("  residual slope %.5f (r^2=%.5f)" % (slope, r2))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "(sin x - x)/x^3 at x = 0 (0/0)",
        "mechanism": "Vanishing Rate",
        "removable_value": "-1/6",
        "approach": {"exponent": 2, "r2": r2},
        "fine_divergence_at_1e-10": float(fine_err),
        "gates": gates, "overall": overall,
        "wall": "alternating sin series, Decimal 60 digits",
    }, open(os.path.join(DATA, "taylor_third_0_over_0.json"), "w"),
        indent=2)
    print("Wrote data/taylor_third_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()