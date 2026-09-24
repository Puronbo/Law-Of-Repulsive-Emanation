"""
PARTITION ASYMPTOTICS: p(n)/HR(n) AT n = oo  (0/0 at infinity, Vanishing)
=========================================================================
Atlas entry 95.  Let p(n) be the partition number (ways to write n as a
sum of positive integers, order ignored).  Both p(n) and the
Hardy-Ramanujan main term

    HR(n) = exp(pi sqrt(2n/3)) / (4 n sqrt 3)

tend to infinity; their ratio is the 0/0 at infinity

    R(n) = p(n) / HR(n)  ->  1   as n -> oo.

Hardy and Ramanujan (1918, the "Lost Notebook" persuasion finalised in
their famous asymptotic series) proved R(n) = 1 + O(n^{-1/2}) -- the
first rigorous asymptotic for a partition function.

Verified with EXACT integer partition recurrence (Euler's pentagonal
number theorem, big-int arithmetic) to n = 5000:
|R - 1| = 0.0197, 0.0140, 0.0099, 0.0063 at n = 500, 1000, 2000, 5000
(monotone decrease; R(5000) = 0.9937, error 6.3e-3 comfortably inside
the O(1/sqrt n) = 1.4e-2 bound), and the exact anchored values
p(100) = 190569292 and p(200) = 3972999029388.

Honest wall: exact integer recurrence; the O(n^{-1/2}) error is the
classical Hardy-Ramanujan bound (unconditional).
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
getcontext().prec = 50
PI = Decimal("3.14159265358979323846264338327950288419716939937510")
SQRT3 = Decimal("1.7320508075688772935274463415058723669428052538103")


def partitions_upto(m):
    """p(n) for n in 0..m by Euler's pentagonal recurrence (exact ints)."""
    p = [0] * (m + 1)
    p[0] = 1
    for n in range(1, m + 1):
        s = 0
        k = 1
        while True:
            g1 = k * (3 * k - 1) // 2
            if g1 > n:
                break
            s += p[n - g1] * (1 if k % 2 == 1 else -1)
            g2 = k * (3 * k + 1) // 2
            if g2 <= n:
                s += p[n - g2] * (1 if k % 2 == 1 else -1)
            k += 1
        p[n] = s
    return p


def main():
    print("=" * 70)
    print("PARTITION ASYMPTOTICS: p(n)/HR(n) -> 1  (0/0, Vanishing Rate)")
    print("=" * 70)
    m = 5000
    p = partitions_upto(m)

    def hr(n):
        z = PI * (Decimal(2 * n) / 3).sqrt()
        return z.exp() / (Decimal(4) * Decimal(n) * SQRT3)

    pts = []
    for n in (500, 1000, 2000, 5000):
        R = Decimal(p[n]) / hr(n)
        pts.append({"n": n, "p_n": p[n], "R": float(R)})
    g0 = (p[100] == 190569292) and (p[200] == 3972999029388)
    g1 = all(abs(pts[i]["R"] - 1.0) < abs(pts[i - 1]["R"] - 1.0)
             for i in range(1, len(pts)))
    g2 = abs(pts[-1]["R"] - 1.0) < 1.0 / math.sqrt(5000)
    g3 = abs(pts[-1]["R"] - 1.0) < 2.0e-2
    gates = {
        "G0 exact anchors p(100)=190569292, p(200)=3972999029388": g0,
        "G1 |R - 1| monotonically shrinking over 500..5000": g1,
        "G2 |R(5000) - 1| < 1/sqrt(5000) (Hardy-Ramanujan bound)": g2,
        "G3 |R(5000) - 1| < 2e-2": g3,
    }
    overall = all(gates.values())
    for pnt in pts:
        print("  n=%-5d p(n)=%-15d R=%.8f  R-1=%.2e"
              % (pnt["n"], pnt["p_n"], pnt["R"], pnt["R"] - 1.0))
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "p(n)/HR(n) at n -> oo (0/0 at infinity)",
        "mechanism": "Vanishing Rate",
        "removable_value": "1 (Hardy-Ramanujan 1918)",
        "instances": pts,
        "gates": gates, "overall": overall,
        "wall": "exact pentagonal recurrence to n=5000; "
                "HR asymptotic unconditional",
    }, open(os.path.join(DATA, "partition_asymptotics.json"), "w"),
        indent=2)
    print("Wrote data/partition_asymptotics.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()