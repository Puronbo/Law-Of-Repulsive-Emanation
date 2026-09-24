"""
DIRICHLET DIVISOR SUMMATORY: D(x)/(x log x) AT x = oo  (0/0, Vanishing)
=======================================================================
Atlas entry 91.  Let tau(k) be the divisor count and

    D(x) = sum_{k <= x} tau(k)

the divisor summatory function.  D(x) -> oo and x log x -> oo; the ratio

    R(x) = D(x) / (x log x)  ->  1   as x -> oo.

The 0/0 at infinity is settled by Dirichlet's hyperbola method (1849):

    D(x) = x log x + (2 gamma - 1) x + O(sqrt x),

so R(x) = 1 + (2 gamma - 1)/log x + O(1/(sqrt x log x)); since
2 gamma - 1 = 0.15443 > 0 the approach is from above at rate 1/log x.

Verified with the EXACT divisor sieve (tau computed by adding 1 over the
multiple lattice) up to x = 10^6: R(10^6) = 1.011184 (predicted
1 + 0.1544/13.8155 = 1.011177, agreement 7e-6 -- the O(sqrt x) term at
1e6 is ~ order 1e-3/1e-6 relative? no: O(sqrt x)/ (x log x) = 1/(sqrt x
log x) = 1e-3/13.8 ~ 7e-5), monotone decrease over the last three
decades, and the residue D(x) - x log x - (2 gamma - 1)x has magnitude
well below sqrt(x)*log(x) at 10^6.

Honest wall: the two-term main term is Dirichlet's hyperbola method
(exam questions since 1849); the O(sqrt x) remainder is unconditional.
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
getcontext().prec = 40
GAMMA = Decimal("0.57721566490153286060651209008240243104215933593992")
C = 2 * GAMMA - 1


def main():
    print("=" * 70)
    print("DIRICHLET DIVISOR SUMMATORY: D(x)/(x log x) -> 1  (0/0)")
    print("=" * 70)
    n = 10 ** 6
    tau = [0] * (n + 1)
    for d in range(1, n + 1):
        for m in range(d, n + 1, d):
            tau[m] += 1
    thresholds = [10 ** 4, 10 ** 5, 10 ** 6]
    s = 0
    pts = []
    j = 0
    for k in range(1, n + 1):
        s += tau[k]
        if j < len(thresholds) and k == thresholds[j]:
            x = Decimal(k)
            lx = x.ln()
            R = Decimal(s) / (x * lx)
            resid = Decimal(s) - x * lx - C * x
            pts.append({"x": k, "D": s, "R": float(R),
                        "residue": float(resid)})
            j += 1
    g1 = (pts[0]["R"] > pts[1]["R"] > pts[2]["R"])
    g2 = 1.005 < pts[-1]["R"] < 1.020
    g3 = abs(pts[-1]["residue"]) < math.sqrt(n) * math.log(n) * 1.2
    gates = {
        "G1 R(x) monotonically decreasing (to 1) over 1e4..1e6": g1,
        "G2 R(1e6) in (1.005, 1.020) -- matches 1 + (2g-1)/log x": g2,
        "G3 |D - x log x - (2g-1)x| < 1.2 sqrt(x) log x": g3,
    }
    overall = all(gates.values())
    for p in pts:
        print("  x=1e%-2d  D=%-9d  R=%.8f   residue=%.0f"
              % (int(math.log10(p["x"])), p["D"], p["R"], p["residue"]))
    print("  expected R(1e6) = 1 + %.6f/13.8155 = %.8f"
          % (float(C), 1 + float(C) / math.log(1e6)))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "D(x)/(x log x) at x -> oo (0/0 at infinity)",
        "mechanism": "Vanishing Rate",
        "removable_value": "1 (Dirichlet divisor summatory, hyperbola "
                           "method; correction (2g-1)/log x)",
        "instances": pts,
        "expected_R_at_1e6":
            round(1 + float(C) / math.log(1e6), 8),
        "gates": gates, "overall": overall,
        "wall": "exact divisor sieve to 1e6; Dirichlet hyperbola method "
                "(1849) unconditional",
    }, open(os.path.join(DATA, "dirichlet_divisor_summatory_0_over_0.json"),
            "w"), indent=2)
    print("Wrote data/dirichlet_divisor_summatory_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()