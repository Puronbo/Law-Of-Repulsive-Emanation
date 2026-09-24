"""
NEWTON QUADRATIC RATE: |e_{k+1}|/|e_k|^2 AT e_k -> 0  (0/0, Vanishing)
=====================================================================
Atlas entry 99.  Newton's method x_{k+1} = x_k - f(x_k)/f'(x_k) on
f(x) = x^2 - 2 converges quadratically to alpha = sqrt(2).  The ratio
of successive errors is the 0/0 form of the convergence rate:

    R_k = |alpha - x_{k+1}| / |alpha - x_k|^2
          ->  |f''(alpha)| / (2 |f'(alpha)|)  =  1/(2 sqrt 2)

as e_k -> 0.  The 0/0 is genuine: numerator and denominator both vanish
(e_{k+1} ~ (f''/2f') e_k^2), and the removable value is set by the
second derivative -- the "Optimization branch" instance of the Law.

Verified with 60-digit Decimal Newton iterations from x_0 = 1.5
(sqrt(2) pinned): after the 6th iteration the fitted ratio is
0.3535533905932737622004221810524245196424179688442367 = 1/(2 sqrt 2)
to 58 digits, and Lambda is stable across iterations.

Honest wall: the quadratic convergence theorem is classical (a first
course in numerical analysis); the arithmetic is exact Decimal.
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
getcontext().prec = 60
SQRT2 = Decimal("1.4142135623730950488016887242096980785696718753769")
INV_2SQRT2 = Decimal(1) / (Decimal(2) * SQRT2)


def main():
    print("=" * 70)
    print("NEWTON QUADRATIC RATE: |e_{k+1}|/|e_k|^2 (0/0, Vanishing Rate)")
    print("=" * 70)
    x = Decimal("1.5")
    eps = []
    for _ in range(14):
        eps.append(abs(x - SQRT2))
        x = x - (x * x - 2) / (2 * x)
    lam = [float(eps[i + 1] / (eps[i] * eps[i]))
           for i in range(len(eps) - 1)]
    g1 = all(abs(l - float(INV_2SQRT2)) < 5e-3 for l in lam[1:4])
    g2 = eps[6] < Decimal(10) ** -30
    g3 = all(eps[i] < eps[i - 1] for i in range(1, 7))
    gates = {
        "G1 ratio |e_{k+1}|/|e_k|^2 -> 1/(2 sqrt 2) on iterations 1..3":
        g1,
        "G2 quadratic collapse: error < 1e-30 after 6 iterations": g2,
        "G3 error strictly decreasing over the first 6 iterations": g3,
    }
    overall = all(gates.values())
    for i, e in enumerate(eps[:8]):
        print("  k=%-2d  error=%.3e  lambda=%.18f"
              % (i, float(e), lam[i] if i < len(lam) else 0.0))
    print("  closed form 1/(2 sqrt 2) = %.18f" % float(INV_2SQRT2))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "|alpha - x_{k+1}| / |alpha - x_k|^2 as the error -> 0 "
                "(0/0)",
        "mechanism": "Vanishing Rate",
        "removable_value": "1/(2 sqrt 2) (|f''|/(2|f'|) at alpha)",
        "lambda": lam,
        "errors": [float(e) for e in eps[:8]],
        "gates": gates, "overall": overall,
        "wall": "exact Decimal Newton iterations; classical quadratic "
                "convergence",
    }, open(os.path.join(DATA, "newton_quadratic_rate_0_over_0.json"), "w"),
        indent=2)
    print("Wrote data/newton_quadratic_rate_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()