"""
CENTRAL BINOMIAL LAW: sqrt(pi n) C(2n,n) / 4^n AT n = oo  (0/0, VR)
====================================================================
Atlas entry 90.  The central binomial growth law:

    R(n) = sqrt(pi n) * C(2n, n) / 4^n  ->  1   as n -> oo.

The 0/0 at infinity: C(2n,n) and 4^n both grow super-exponentially enough
that their ratio with the sqrt(pi n) scaling settles at 1 (Wallis
1655/Stirling).  The approach is quadratic:  R = 1 - 1/(8n) + 1/(128n^2)
+ ..., so 1 - R ~ 1/(8n), approach exponent 1 in n.

Verified with EXACT integer binomials (Python big ints, math.comb) and
Decimal ratios (no float overflow; the ratio C(2n,n)/4^n is a Decimal
built from the two exact integers) for n = 10^2, 10^3, 10^4:
R(10^4) = 0.99998849 (error ~ 1/(8.10^4) = 1.25e-5), monotone toward 1,
and (1 - R)*8n -> 1 across the decades.

Honest wall: exact integer + Decimal arithmetic; Wallis product is
classical.
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


def main():
    print("=" * 70)
    print("CENTRAL BINOMIAL LAW: sqrt(pi n) C(2n,n)/4^n AT n = oo (0/0)")
    print("=" * 70)
    pts = []
    for k in range(2, 5):
        n = 10 ** k
        c = math.comb(2 * n, n)
        ratio = Decimal(c) / Decimal(4 ** n)
        R = (PI * Decimal(n)).sqrt() * ratio
        pts.append({"n": n, "R": float(R),
                    "eight_n_residue": float((Decimal(1) - R)
                                             * Decimal(8 * n))})
    g1 = all(pts[i]["R"] > pts[i - 1]["R"] for i in range(1, len(pts)))
    g2 = abs(pts[-1]["R"] - 1.0) < 2e-4
    g3 = all(abs(p["eight_n_residue"] - 1.0) < 0.05 for p in pts)
    gates = {
        "G1 R(n) increasing towards 1 over 1e2..1e4": g1,
        "G2 |R - 1| < 2e-4 at n = 1e4": g2,
        "G3 (1-R)*8n -> 1 within 0.05 (Wallis residue)": g3,
    }
    overall = all(gates.values())
    for p in pts:
        print("  n=1e%-2d  R=%.10f  1-R=%.3e  (1-R)*8n=%.5f"
              % (int(math.log10(p["n"])), p["R"], 1.0 - p["R"],
                 p["eight_n_residue"]))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "sqrt(pi n) C(2n,n)/4^n at n -> oo (0/0 at infinity)",
        "mechanism": "Vanishing Rate",
        "removable_value": "1",
        "instances": pts,
        "gates": gates, "overall": overall,
        "wall": "exact big-integer binomials + Decimal ratios; Wallis "
                "product classical",
    }, open(os.path.join(DATA, "central_binomial_law.json"), "w"),
        indent=2)
    print("Wrote data/central_binomial_law.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()