"""
EULER-MASCHERONI CONSTANT: H_n - log n AT n = oo  (0/0, Conservation)
=====================================================================
Atlas entry 88.  Two diverging quantities H_n = sum 1/k and log n chase
each other; their DIFFERENCE is a genuine 0/0 (oo - oo) that does not
oscillate but settles:

    R(n) = H_n - log n  ->  gamma = 0.5772156649...

gamma is the conserved constant of the harmonic ladder: all of the
integer residue that the integral log n fails to capture.  The approach
is rate 1/2:  H_n - log n = gamma + 1/(2n) - 1/(12 n^2) + ..., so
|R(n) - gamma| ~ 1/(2n), approach exponent 1.

Verified exactly with 50-digit Decimal summations:
H(10^5) - log(10^5) = 0.57722066  (gamma + 5e-6),
and the residue (H - log - gamma) * n -> 1/2 across the decades
(gamma pinned to 40 digits).

Honest wall: the Euler-Maclaurin expansion of H_n is classical
(Euler 1734; the constant's transcendence status is not needed here,
only its existence -- which this very limit demonstrates).
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
getcontext().prec = 50
GAMMA = Decimal("0.57721566490153286060651209008240243104215933593992")


def main():
    print("=" * 70)
    print("EULER-MASCHERONI: H_n - log n AT n = oo  (0/0, Conservation)")
    print("=" * 70)
    pts = []
    h = Decimal(0)
    log10 = Decimal(0)
    for k in range(1, 6):
        target = 10 ** k
        while log10 < target:
            log10 += 1
            h += Decimal(1) / log10
        r = h - log10.ln()
        residue = (r - GAMMA) * log10
        pts.append({"n": target, "H_minus_log": float(r),
                    "residue_times_n": float(residue)})
    max_tail = max(abs(p["residue_times_n"] - 0.5) for p in pts[2:])
    g1 = all(abs(pts[i]["H_minus_log"] - float(GAMMA))
             < abs(pts[i - 1]["H_minus_log"] - float(GAMMA))
             for i in range(1, len(pts)))
    g2 = abs(pts[-1]["H_minus_log"] - float(GAMMA)) < 1e-4
    g3 = max_tail < 0.02
    gates = {
        "G1 H_n - log n monotonically converging to gamma": g1,
        "G2 |(H-log) - gamma| < 1e-4 at n = 1e5": g2,
        "G3 residue (= (H-log-gamma)*n) -> 1/2 within 0.02": g3,
    }
    overall = all(gates.values())
    for p in pts:
        print("  n=1e%-2d  H_n-log n = %.12f   diff=%.3e  n*diff=%.6f"
              % (int(math.log10(p["n"])), p["H_minus_log"],
                 p["H_minus_log"] - float(GAMMA), p["residue_times_n"]))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "H_n - log n at n -> oo (oo - oo)",
        "mechanism": "Conservation",
        "removable_value": "gamma = 0.5772156649...",
        "instances": pts,
        "gates": gates, "overall": overall,
        "wall": "exact Decimal summation; Euler-Maclaurin expansion "
                "classical",
    }, open(os.path.join(DATA, "euler_mascheroni_constant.json"), "w"),
        indent=2)
    print("Wrote data/euler_mascheroni_constant.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()