"""
SUM OF TWO SQUARES LAW: N(x)/(pi x) AT x = oo  (0/0, Vanishing Rate)
====================================================================
Atlas entry 98.  Let N(x) count the integer lattice points inside the
circle of radius sqrt(x):

    N(x) = #{(a, b) in Z^2 : a^2 + b^2 <= x}.

Both N(x) and x diverge; Gauss (1834) and Dirichlet (1849) proved the
circle law -- every integer quadratic form 'area ratio' collapse:

    R(x) = N(x) / (pi x)  ->  1   as x -> oo.

The approach is slow but principled: N(x) = pi x + O(x^{1/2 + eps}),
so |R - 1| grows at most like x^{-1/2 + eps}.  (The error REFINEMENT of
the same ratio is the anti-class lattice-wall of the register: the
remainder N(x) - pi x oscillates with no limit, proven by Hardy 1916.)

Verified with an exact isqrt circle sweep (O(sqrt x) reflections) up to
x = 10^6: N(10^6) = 3141549 (R = 0.999986, |N - pi x| = 44), in agreement
with the O(x^{0.52}) bound (1e6^0.52 ~ 1330), the ratio collapsing from
1.009 at x = 100 to 0.999986.  (The remainder N(x) - pi x keeps its
small-oscillation envelope across the whole sweep -- the anti-class
lattice wall is exactly why pointwise monotonicity is NOT claimed.)

Honest wall: the O(x^{1/2+eps}) remainder is classical (Gauss/Dirichlet
circle problem); the exact isqrt sweep is machine-exact.
"""
import json
import math
import os
import sys
from math import isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
PI = 3.14159265358979323846264338327950288419716939937510


def lattice_circle(x):
    n = 0
    for a in range(0, isqrt(x) + 1):
        rem = x - a * a
        bmax = isqrt(rem)
        mult = 1 if a == 0 else 2
        n += mult * (2 * bmax + 1)
    return n


def main():
    print("=" * 70)
    print("SUM OF TWO SQUARES LAW: N(x)/(pi x) -> 1  (0/0, Vanishing)")
    print("=" * 70)
    pts = []
    for x in (10 ** 2, 10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
        n = lattice_circle(x)
        pts.append({"x": x, "N": n, "R": n / (PI * x),
                    "abs_error": abs(n - PI * x)})
    g1 = abs(pts[0]["R"] - 1.0) > abs(pts[-1]["R"] - 1.0)
    g2 = abs(pts[-1]["R"] - 1.0) < 5e-4
    g3 = pts[-1]["abs_error"] < 10.0 ** (0.52 * 6) * 1.5
    gates = {
        "G1 |R - 1| shrinks from 1e2 (1.009) to 1e6 (0.999986)": g1,
        "G2 |R(1e6) - 1| < 5e-4": g2,
        "G3 |N - pi x| below the Gauss/Dirichlet O(x^{1/2+eps}) scale": g3,
    }
    overall = all(gates.values())
    for p in pts:
        print("  x=1e%-2d N=%-9d R=%.8f  |N-pi x|=%.0f"
              % (int(math.log10(p["x"])), p["N"], p["R"], p["abs_error"]))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "N(x)/(pi x) at x -> oo (0/0 at infinity; Gauss circle "
                "law)",
        "mechanism": "Vanishing Rate",
        "removable_value": "1 (coefficient pi; Gauss 1834, Dirichlet "
                           "1849)",
        "instances": pts,
        "gates": gates, "overall": overall,
        "wall": "exact isqrt circle sweep to 1e6; Gauss/Dirichlet "
                "remainder O(x^{1/2+eps}) unconditional; the raw "
                "remainder oscillation is the anti-class lattice wall",
    }, open(os.path.join(DATA, "sum_of_two_squares_law.json"), "w"),
        indent=2)
    print("Wrote data/sum_of_two_squares_law.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()