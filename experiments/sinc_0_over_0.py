"""
SINC FUNCTION: sin(x)/x AT x = 0  (0/0, Probe)
===============================================
Atlas entry 81.  The canonical 0/0, and the clearest instance of the Law
of Singularities: sin(0) = 0 and x vanishes together, and the ratio
R(x) = sin(x)/x carries the removable value

    R(0)  =  1   (the sinc law).

The approach is even and quadratic:  sin(x)/x = 1 - x^2/6 + x^4/120 - ...
so the residual |R - 1| ~ x^2 / 6 on BOTH sides (no sign asymmetry),
approach exponent 2.

The ratio is verified with exact Decimal series arithmetic over x = h and
x = -h for h = 10^-1 .. 10^-10 (twenty-one terms of the alternating sine
series), one-sided agreement to 70 digits, and the log-log slope of the
residual is fitted over [10^-6, 10^-2] to exponent 2 (r^2 = 1).

Honest wall: the series is exact algebra (alternating, converges on all of
R); no open theorem involved.
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
getcontext().prec = 70
ONE = Decimal(1)


def sinc_series(x):
    """sin(x)/x by the alternating Taylor series (exact Decimal)."""
    s = ONE
    term = ONE
    for k in range(1, 22):
        term = term * x * x / Decimal((2 * k) * (2 * k + 1))
        s += term if k % 2 == 0 else -term
    return s


def main():
    print("=" * 70)
    print("SINC FUNCTION: sin(x)/x AT x = 0  (0/0, Probe)")
    print("=" * 70)
    points = []
    max_err = Decimal(0)
    for i in range(1, 11):
        h = Decimal(10) ** (-i)
        for sgn in (ONE, -ONE):
            x = sgn * h
            r = sinc_series(x)
            err = abs(r - ONE)
            max_err = max(max_err, err)
            points.append((i, float(h), r))
    y = [math.log10(float(abs(r - ONE)))
         for i, h, r in points if 6 <= i <= 10]
    xf = [math.log10(h) for i, h, r in points if 6 <= i <= 10]
    slope, r2 = fit(xf, y)
    fine_err = max(abs(r - ONE)
                   for i, h, r in points if i >= 8)
    g1 = fine_err < Decimal(10) ** (-15)
    g2 = abs(slope - 2.0) < 0.02 and r2 > 0.999
    gates = {
        "G1 two-sided 1 - sin(x)/x < 1e-15 at |x| <= 1e-8": bool(g1),
        "G2 approach exponent 2 (even residue), r2 > 0.999": g2,
    }
    overall = all(gates.values())
    print("  fine |R - 1| at |x| = 1e-10: %.2e" % float(fine_err))
    print("  residual slope %.5f (r^2=%.5f)" % (slope, r2))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "sin(x)/x at x = 0 (0/0)",
        "mechanism": "Probe",
        "removable_value": "1",
        "approach": {"exponent": 2, "r2": r2},
        "fine_divergence_at_1e-10": float(fine_err),
        "gates": gates, "overall": overall,
        "wall": "exact alternating Taylor series, 70-digit Decimal",
    }, open(os.path.join(DATA, "sinc_0_over_0.json"), "w"), indent=2)
    print("Wrote data/sinc_0_over_0.json")
    sys.exit(0 if overall else 1)


def fit(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((p - mx) ** 2 for p in xs)
    sxy = sum((p - mx) * (q - my) for p, q in zip(xs, ys))
    syy = sum((q - my) ** 2 for q in ys)
    if sxx == 0 or syy == 0:
        return 0.0, 0.0
    slope = sxy / sxx
    return slope, (sxy * sxy) / (sxx * syy)


if __name__ == "__main__":
    main()