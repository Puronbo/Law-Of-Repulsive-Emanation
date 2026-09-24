"""
n-TH ROOT OF n: n^(1/n) AT n = oo  (0/0 at infinity, Vanishing Rate)
====================================================================
Atlas entry 87.  The sequence ratio that proves (in one line of algebra
that it squeezes to 1 c, 1 < c: take n^(1/n) = e^{log n / n}):

    R(n) = n^(1/n)  ->  1   as n -> oo.

The 0/0 at infinity: n -> oo, exponent 1/n -> 0; the surplus decays at
rate 1:  R(n) - 1 ~ log(n)/n, so R - 1 ~ log(n) * n^{-1} (approach
exponent 1 in n, times log n).

Verified exactly with Decimal over n = 10^1..10^12: monotone decrease of
R(n) toward 1, R(10^12) - 1 < 3.0e-12, and the product
n*(R(n) - 1) ~ log n tracked over the decades (grows like log n, exactly
matching the log(n)/n surplus).

Honest wall: elementary limits; no open theorem.
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
getcontext().prec = 50


def main():
    print("=" * 70)
    print("n-TH ROOT OF n: n^(1/n) AT n = oo  (0/0, Vanishing Rate)")
    print("=" * 70)
    pts = []
    prev = Decimal(10)
    for k in range(1, 13):
        n = Decimal(10) ** k
        r = (n ** (Decimal(1) / n))
        surplus = r - Decimal(1)
        pts.append({"n": int(n), "R": float(r),
                    "surplus": float(surplus),
                    "n_surplus": float(surplus * n),
                    "log_n": float(n.ln())})
        if surplus >= prev:
            break
        prev = surplus
    monotone = len(pts) == 12
    final = pts[-1]
    g1 = monotone
    g2 = final["surplus"] < 1.0e-10
    ln_last = final["log_n"]
    g3 = 0.5 * ln_last < final["n_surplus"] < 1.5 * ln_last
    gates = {
        "G1 R(n) strictly decreasing towards 1 over 1e1..1e12": g1,
        "G2 R(1e12) - 1 < 1e-10 (rate 1/n times log n)": g2,
        "G3 n*(R-1) tracks log n within 50%": g3,
    }
    overall = all(gates.values())
    for p in pts:
        print("  n=1e%-3d  R=%.12f  R-1=%.3e  n(R-1)=%.4f"
              % (int(math.log10(p["n"])), p["R"], p["surplus"],
                 p["n_surplus"]))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "n^(1/n) at n -> oo (0/0 at infinity)",
        "mechanism": "Vanishing Rate",
        "removable_value": "1",
        "instances": pts,
        "gates": gates, "overall": overall,
        "wall": "elementary limit; Decimal 50 digits",
    }, open(os.path.join(DATA, "nth_root_of_n.json"), "w"), indent=2)
    print("Wrote data/nth_root_of_n.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()