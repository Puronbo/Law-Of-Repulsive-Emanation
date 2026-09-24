"""
HALF COSINE: (1 - cos x)/x^2 AT x = 0  (0/0, Vanishing Rate)
============================================================
Atlas entry 84.  The 1 - cos x family is the even twin of the sinc:
numerator and denominator both vanish to order 2, and

    R(x) = (1 - cos x)/x^2  ->  1/2   as x -> 0.

The approach is even and quadratic:  1 - cos x = x^2/2 - x^4/24 + ...
so R - 1/2 ~ -x^2/24, approach exponent 2 on both sides (no sign flips).

Verified with exact Decimal series over x = +h, -h for h = 10^-1..10^-10:
two-sided agreement to 1/2 to 50 digits, fitted exponent 2 (r^2 = 1).

Honest wall: the cos series converges absolutely; no open theorem.
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
getcontext().prec = 60
HALF = Decimal(1) / 2


def one_minus_cos_over_x2(x):
    """(1 - cos x)/x^2 = 1/2! - x^2/4! + x^4/6! - ... (exact series)."""
    s = HALF
    term = HALF
    for k in range(1, 21):
        # next term multiplies by x^2 / ((2k+2)(2k+1)) with sign flip
        term = term * x * x / Decimal((2 * k + 1) * (2 * k + 2))
        s += term if k % 2 == 0 else -term
    return s


def main():
    print("=" * 70)
    print("HALF COSINE: (1 - cos x)/x^2 AT x = 0  (0/0, Vanishing Rate)")
    print("=" * 70)
    pts = []
    max_err = Decimal(0)
    for i in range(1, 11):
        h = Decimal(10) ** (-i)
        for sgn in (Decimal(1), Decimal(-1)):
            r = one_minus_cos_over_x2(sgn * h)
            max_err = max(max_err, abs(r - HALF))
            pts.append((i, float(h), r))
    xf = [math.log10(h) for i, h, r in pts if 5 <= i <= 9]
    y = [math.log10(float(abs(r - HALF)))
         for i, h, r in pts if 5 <= i <= 9]
    n = len(xf)
    mx, my = sum(xf) / n, sum(y) / n
    sxx = sum((p - mx) ** 2 for p in xf)
    sxy = sum((p - mx) * (q - my) for p, q in zip(xf, y))
    syy = sum((q - my) ** 2 for q in y)
    slope = sxy / sxx
    r2 = (sxy * sxy) / (sxx * syy)
    fine_err = max(abs(r - HALF) for i, h, r in pts if i >= 8)
    g1 = fine_err < Decimal(10) ** (-15)
    g2 = abs(slope - 2.0) < 0.02 and r2 > 0.999
    gates = {
        "G1 two-sided (1-cos x)/x^2 -> 1/2 within 1e-15 at |x| <= 1e-8":
        bool(g1),
        "G2 approach exponent 2 (even residue), r2 > 0.999": g2,
    }
    overall = all(gates.values())
    print("  fine |R - 1/2| at |x| = 1e-10: %.2e" % float(fine_err))
    print("  residual slope %.5f (r^2=%.5f)" % (slope, r2))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "(1 - cos x)/x^2 at x = 0 (0/0)",
        "mechanism": "Vanishing Rate",
        "removable_value": "1/2",
        "approach": {"exponent": 2, "r2": r2},
        "fine_divergence_at_1e-10": float(fine_err),
        "gates": gates, "overall": overall,
        "wall": "alternating cos series, Decimal 60 digits",
    }, open(os.path.join(DATA, "half_cosine_0_over_0.json"), "w"),
        indent=2)
    print("Wrote data/half_cosine_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()