"""
SIGMA SUMMATORY: (sum_{k<=x} sigma(k)) / x^2 AT x = oo  (0/0, VR)
=================================================================
Atlas entry 92.  Let sigma(k) be the sum of divisors of k and

    S(x) = sum_{k <= x} sigma(k).

Both S(x) and x^2 -> oo, and Dirichlet (1849) proved the ratio settles
on a transcendental closed form:

    R(x) = S(x) / x^2  ->  pi^2 / 12  =  0.8224670334...

The approach is fast:  S(x) = pi^2/12 x^2 + O(x log x), so
|R - pi^2/12| = O(log x / x), vanishing like rate ~ x^{-1} times a log.

Verified with the EXACT sigma sieve (add d over the multiples of d) up
to x = 10^6: R(10^6) = 0.822467794 (error 7.6e-7, matching the
O(log x/x) = 1.4e-5 bound), monotone decrease over 1e4..1e6, and the
residue |S - (pi^2/12) x^2| < 4 x log x.

Honest wall: exact sieve arithmetic; the pi^2/12 coefficient is
Dirichlet 1849 (the same hyperbola method as entry 91, applied to sigma).
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
getcontext().prec = 50
PI2_12 = Decimal(3.141592653589793238462643383279502884) ** 2 / 12


def main():
    print("=" * 70)
    print("SIGMA SUMMATORY: S(x)/x^2 -> pi^2/12  (0/0, Vanishing Rate)")
    print("=" * 70)
    n = 10 ** 6
    sigma = [0] * (n + 1)
    for d in range(1, n + 1):
        for m in range(d, n + 1, d):
            sigma[m] += d
    thresholds = [10 ** 4, 10 ** 5, 10 ** 6]
    s = 0
    pts = []
    j = 0
    for k in range(1, n + 1):
        s += sigma[k]
        if j < len(thresholds) and k == thresholds[j]:
            x = Decimal(k)
            R = Decimal(s) / (x * x)
            resid = abs(Decimal(s) - PI2_12 * x * x)
            pts.append({"x": k, "S": s, "R": float(R),
                        "abs_residue": float(resid)})
            j += 1
    expected = float(PI2_12)
    g1 = (pts[0]["R"] > pts[1]["R"] > pts[2]["R"])
    g2 = abs(pts[-1]["R"] - expected) < 5e-4
    g3 = pts[-1]["abs_residue"] < 4.0 * n * math.log(n)
    gates = {
        "G1 R(x) monotonically decreasing (to pi^2/12) over 1e4..1e6": g1,
        "G2 |R(1e6) - pi^2/12| < 5e-4": g2,
        "G3 |S - (pi^2/12)x^2| < 4 x log x (Dirichlet O(x log x))": g3,
    }
    overall = all(gates.values())
    for p in pts:
        print("  x=1e%-2d  S=%-12d  R=%.10f  |residue|=%.0f"
              % (int(math.log10(p["x"])), p["S"], p["R"],
                 p["abs_residue"]))
    print("  pi^2/12 = %.10f ;  R(1e6) - pi^2/12 = %.3e"
          % (expected, pts[-1]["R"] - expected))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "S(x)/x^2 at x -> oo (0/0 at infinity)",
        "mechanism": "Vanishing Rate",
        "removable_value": "pi^2/12 (Dirichlet 1849)",
        "instances": pts,
        "gates": gates, "overall": overall,
        "wall": "exact sigma sieve to 1e6; Dirichlet's hyperbola method "
                "unconditional",
    }, open(os.path.join(DATA, "sigma_summatory_pi2_12.json"), "w"),
        indent=2)
    print("Wrote data/sigma_summatory_pi2_12.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()