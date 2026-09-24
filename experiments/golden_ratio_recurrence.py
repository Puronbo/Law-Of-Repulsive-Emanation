"""
GOLDEN RATIO RECURRENCE: F_{n+1}/F_n AT n = oo  (0/0 at infinity, Index)
=======================================================================
Atlas entry 100.  The Fibonacci recurrence F_{n+2} = F_{n+1} + F_n
produces two diverging sequences; their ratio is the classic 0/0 at
infinity that collapses onto the golden ratio:

    R_n = F_{n+1} / F_n  ->  phi = (1 + sqrt 5)/2 = 1.6180339887...

The index law is Binet's closed form: F_n = (phi^n - psi^n)/sqrt 5 with
psi = (1 - sqrt 5)/2; the ratio phi carries exactly the index-1 exponent
of the dominant root -- the same eigenvalue-content the register reads
elsewhere as an Index mechanism.  The approach is geometric:
|R_n - phi| ~ |psi|^n / phi^n, contracting by |psi|/phi = 0.381966 per
step.

Verified with EXACT big-integer Fibonacci numbers and 50-digit Decimal
ratios (float underflow would wash out the tail, so the difference
|R_n - phi| is computed in Decimal): |R(500) - phi| < 1e-12, monotone
geometric contraction, and the per-step contraction log10(|R300-phi|/
|R150-phi|)/150 equals log10(|psi|/phi) to within 0.01.

Honest wall: Binet's closed form is elementary algebra; the integers
are exact.
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
getcontext().prec = 200
SQ5 = Decimal(5).sqrt()
PHI = (Decimal(1) + SQ5) / Decimal(2)
# |psi|/phi = (sqrt(5)-1)/(sqrt(5)+1) = (3 - sqrt(5))/2
PSI_PHI_RATIO = (Decimal(3) - SQ5) / Decimal(2)


def fib_pair(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a, b


def main():
    print("=" * 70)
    print("GOLDEN RATIO RECURRENCE: F_{n+1}/F_n -> phi  (0/0, Index)")
    print("=" * 70)
    pts = []
    for n in (50, 100, 150, 200, 250, 300, 400, 500):
        a, b = fib_pair(n)   # F_n, F_{n+1}
        R = Decimal(b) / Decimal(a)
        pts.append({"n": n, "F_n": a,
                    "diff": abs(R - PHI)})
    diffs = [p["diff"] for p in pts]
    g1 = all(diffs[i] < diffs[i - 1] for i in range(1, len(diffs)))
    g2 = diffs[-1] < Decimal(10) ** -12
    ## contraction per step: log10(|R300-phi|/|R150-phi|) / 150
    ln10 = Decimal(10).ln()
    measured_pers = (diffs[5].ln() - diffs[2].ln()) / (Decimal(150) * ln10)
    predicted_pers = PSI_PHI_RATIO.ln() / ln10
    g3 = abs(measured_pers - predicted_pers) < Decimal("0.01")
    gates = {
        "G1 |R_n - phi| monotonically shrinking over 50..500": bool(g1),
        "G2 |R(500) - phi| < 1e-12": bool(g2),
        "G3 per-step contraction log10(r300/r150)/150 matches "
        "log10(|psi|/phi) within 0.01": bool(g3),
    }
    overall = all(gates.values())
    for p in pts:
        print("  n=%-4d  F_n=%-25d  R-phi=%.3e"
              % (p["n"], p["F_n"], float(p["diff"])))
    print("  measured per-step contraction = %.6f ; predicted = %.6f"
          % (float(measured_pers), float(predicted_pers)))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "F_{n+1}/F_n at n -> oo (0/0 at infinity)",
        "mechanism": "Index",
        "removable_value": "phi = (1 + sqrt 5)/2 (Binet closed form)",
        "instances": [{"n": p["n"], "diff": float(p["diff"])}
                      for p in pts],
        "contraction_per_step": float(measured_pers),
        "predicted_per_step": float(predicted_pers),
        "gates": gates, "overall": overall,
        "wall": "exact big-integer Fibonacci; Binet elementary",
    }, open(os.path.join(DATA, "golden_ratio_recurrence.json"), "w"),
        indent=2)
    print("Wrote data/golden_ratio_recurrence.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()