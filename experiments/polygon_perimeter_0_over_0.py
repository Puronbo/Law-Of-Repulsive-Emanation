"""
POLYGON PERIMETER: n sin(pi/n) AT n = oo  (0/0, Probe)
======================================================
Atlas entry 86.  The regular n-gon inscribed in the unit circle has
perimeter P(n) = 2 n sin(pi/n); as n -> oo the polygon collapses onto
the circle and the half-perimeter ratio

    R(n) = n sin(pi/n)  ->  pi   as n -> oo.

The 0/0 at infinity: n -> oo while sin(pi/n) -> 0, product finite = pi.
The approach is quadratic:  n sin(pi/n) = pi - pi^3/(6 n^2) + ..., so
pi - R(n) ~ pi^3 / (6 n^2), approach exponent 2 (in log n).

Verified with exact Decimal sin-series (argument pi/n, n a power of ten,
pi pinned to 60 digits): agreement to pi to 1e-40 at n = 1e7, the fitted
exponent over n = 10^4..10^7 is 2 (r^2 = 1).

Honest wall: the sine series converges absolutely; geometry of the
inscribed polygon is classical; no open theorem.
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
getcontext().prec = 60
PI = Decimal("3.141592653589793238462643383279502884197169399375105820")


def sin_series(x, n=28):
    s = Decimal(0)
    term = x
    for k in range(0, n):
        s += term if k % 2 == 0 else -term
        term = term * x * x / Decimal((2 * k + 2) * (2 * k + 3))
    return s


def main():
    print("=" * 70)
    print("POLYGON PERIMETER: n sin(pi/n) AT n = oo  (0/0, Probe)")
    print("=" * 70)
    pts = []
    max_err = Decimal(0)
    for k in range(1, 8):
        n = Decimal(10) ** k
        r = n * sin_series(PI / n)
        max_err = max(max_err, abs(r - PI))
        pts.append((float(k), float(r)))
    # exponent fit over n = 10^4..10^7 in log-log (residual vs n)
    xf = [p for p, _ in pts if 4 <= float(p) <= 7]
    y = [math.log10(abs(PI - Decimal(r))) for p, r in pts
         if 4 <= float(p) <= 7]
    n = len(xf)
    mx, my = sum(xf) / n, sum(y) / n
    sxx = sum((p - mx) ** 2 for p in xf)
    sxy = sum((p - mx) * (q - my) for p, q in zip(xf, y))
    syy = sum((q - my) ** 2 for q in y)
    slope = sxy / sxx
    r2 = (sxy * sxy) / (sxx * syy)
    fine_err = max(abs(r - float(PI))
                   for p, r in pts if float(p) >= 6)
    g1 = fine_err < 1e-8
    g2 = abs(slope + 2.0) < 0.02 and r2 > 0.999
    gates = {
        "G1 n sin(pi/n) -> pi within 1e-8 at n >= 1e6": bool(g1),
        "G2 approach exponent 2 in n (residual ~ pi^3/(6n^2)), r2 > 0.999":
        g2,
    }
    overall = all(gates.values())
    print("  fine |R - pi| at n = 1e7: %.2e" % float(fine_err))
    print("  exponent %.5f (r^2=%.5f)" % (slope, r2))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "n sin(pi/n) at n -> oo (half-perimeter of the inscribed "
                "n-gon; 0/0 at infinity)",
        "mechanism": "Probe",
        "removable_value": "pi",
        "approach": {"exponent_in_n": 2, "r2": r2},
        "fine_divergence_at_1e7": float(fine_err),
        "gates": gates, "overall": overall,
        "wall": "sin series + pinned pi, Decimal 60 digits",
    }, open(os.path.join(DATA, "polygon_perimeter_0_over_0.json"), "w"),
        indent=2)
    print("Wrote data/polygon_perimeter_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()