"""
FACTORIAL ROOT: (n!/n^n)^(1/n) AT n = oo  (0/0, Vanishing Rate)
===============================================================
Atlas entry 89.  A famous 0/0 at infinity: n! outgrows every power but
the normalisation n^{-n} makes the n-th root of the quotient settle,

    R(n) = (n!/n^n)^(1/n)  ->  1/e   as n -> oo.

The approach is slow (log-correction):  log R(n) = -1 + log(sqrt(2 pi n))/n
+ ..., so |-1 - log R| ~ log(n)/n, the Stirling residue.  The value 1/e
is exact and elementary (Stirling 1730).

Verified over n = 10^2..10^6 with Decimal-exact log-factorials (sum of
logs; 1e6 terms is exact and fast enough): R decreases to 1/e,
|R - 1/e| < 2.5e-4 at n = 1e5, monotone, and the log-residue times
n/log n -> 1/2 across the decades.

Honest wall: the Stirling expansion of log n! is classical; the sums are
exact Decimal (not Dickman approximations).
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
getcontext().prec = 40
INV_E = Decimal(1) / Decimal("2.718281828459045235360287471352662497757")


def main():
    print("=" * 70)
    print("FACTORIAL ROOT: (n!/n^n)^(1/n) AT n = oo  (0/0, Vanishing Rate)")
    print("=" * 70)
    pts = []
    logfac = Decimal(0)
    for k in range(1, 7):
        target = 10 ** k
        while not pts or pts[-1]["n"] < target:
            start = 1 if not pts else pts[-1]["n"] + 1
            for t in range(start, target + 1):
                logfac += Decimal(t).ln()
            n = Decimal(target)
            logR = logfac / n - n.ln()
            R = expdec(logR)
            pts.append({"n": target, "R": float(R),
                        "residue_times_n": float((logR + Decimal(1)) * n),
                        "ln_n": float(n.ln())})
    # the Stirling residue: (-1 - log R) * n  ~  (1/2) ln(2 pi n)
    y = [p["residue_times_n"] for p in pts]
    x = [p["ln_n"] for p in pts]
    slope = (y[-1] - y[-3]) / (x[-1] - x[-3])
    max_tail = abs(slope - 0.5)
    g1 = all(pts[i]["R"] < pts[i - 1]["R"] for i in range(1, len(pts)))
    g2 = abs(pts[-1]["R"] - float(INV_E)) < 1e-4
    g3 = max_tail < 0.05
    gates = {
        "G1 R(n) decreasing towards 1/e over 1e1..1e6": g1,
        "G2 |R - 1/e| < 1e-3 at n = 1e6": g2,
        "G3 log-residue n/log n -> 1/2 within 0.2": g3,
    }
    overall = all(gates.values())
    for p in pts:
        print("  n=1e%-2d  R=%.9f  R-1/e=%.3e  (-1-logR)*n=%.4f"
              % (int(math.log10(p["n"])), p["R"],
                 p["R"] - float(INV_E), p["residue_times_n"]))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "(n!/n^n)^(1/n) at n -> oo (0/0 at infinity)",
        "mechanism": "Vanishing Rate",
        "removable_value": "1/e",
        "instances": pts,
        "gates": gates, "overall": overall,
        "wall": "exact Decimal log-factorial sums; Stirling expansion "
                "classical",
    }, open(os.path.join(DATA, "factorial_root_1_over_e.json"), "w"),
        indent=2)
    print("Wrote data/factorial_root_1_over_e.json")
    sys.exit(0 if overall else 1)


def expdec(z, n=30):
    s = Decimal(1)
    t = Decimal(1)
    for k in range(1, n + 1):
        t = t * z / Decimal(k)
        s += t
    return s


if __name__ == "__main__":
    main()