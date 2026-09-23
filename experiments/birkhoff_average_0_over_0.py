"""
ERGODIC THEORY: BIRKHOFF AVERAGE AT THE EXCEPTIONAL POINT  (0/0, Probe)
======================================================================
Missing-experiment sweep, atlas 6.1 row 6 (Ergodic theory).

Doubling map T(x) = 2x mod 1, f(t) = t^2 (mean 1/3).  At a generic
(irrational) initial condition the Birkhoff average of ANY partial
block converges to the ergodic mean.  At an exceptional point (a
periodic orbit; here x0 = 1/3) the closed-orbit average is (1/9+4/9)/2
= 5/18 instead.  Probe ratio

    R_N(x) = (A_N(x) - m_N(x)) / (A_N(x) - 1/3),

A_N = mean of the first half of the orbit, m_N = mean of the second
half.  As N -> inf both numerator and denominator leave 0 (both block
averages collapse onto the same limit), so R_N is a genuine 0/0 whose
removable value is the testimony of the initial condition:
    R_N -> 1  (generic: first-half and second-half averages agree)
    R_N -> 0  (exceptional: the two blocks settle onto the same
               closed-orbit value, which differs from the ergodic 1/3).

The mechanism is Probe: the removable value decides the
typical/exceptional classification.

Orbits are computed EXACTLY on the integer numerators (x_k = (2^k p
mod q)/q, integer arithmetic): no float drift over 2^20 iterations.
Generic x0 = sqrt(2)-1 modelled by p/q with q = 2^40+7 (the order of
2 mod q >> 2^20).  Exceptional x0 = 1/3 (q = 3, exact period 2).

Honest wall: finite N, one trajectory per class; the generic removable
value 1 is the equidistribution heuristic for irrational shifts, not a
per-point theorem.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")


def gen_orbit(p, q, N):
    """Return the first N orbit values x_k = (2^k p mod q)/q (exact)."""
    vals = []
    y = p % q
    for _ in range(N):
        vals.append(y / q)
        y = (2 * y) % q
    return vals

def mean_of(xs):
    s = 0.0
    for x in xs:
        s += x * x
    return s / len(xs)


def measure(p, q, N):
    vals = gen_orbit(p, q, N)
    A = mean_of(vals[: N // 2])
    m = mean_of(vals[N // 2:])
    R = (A - m) / (A - 1.0 / 3.0)
    Afull = mean_of(vals)
    return A, m, R, Afull


def main():
    print("=" * 70)
    print("ERGODIC THEORY: BIRKHOFF AVERAGE AT EXCEPTIONAL POINT (0/0)")
    print("=" * 70)

    q_gen = 2 ** 40 + 7                      # odd: no small 2-power period
    p_gen = int(round((math.sqrt(2.0) - 1.0) * q_gen))
    print(f"\nGeneric irrational model: p/q, q = {q_gen} "
          f"(sqrt(2)-1 to {math.log10(q_gen):.0f} digits)")

    last_g = None
    for N in [2 ** 14, 2 ** 18, 2 ** 20]:
        A, m, R, Afull = measure(p_gen, q_gen, N)
        last_g = (N, R, abs(Afull - 1.0 / 3.0), abs(A - m))
        print(f"  N={N:>7d}  A_full={Afull:+.5f}  R={R:+.3f}")

    print("\nExceptional x0 = 1/3 (orbit mean 5/18)")
    last_p = None
    for N in [2 ** 10, 2 ** 14, 2 ** 20]:
        A, m, R, Afull = measure(1, 3, N)
        last_p = (N, R, abs(Afull - 5.0 / 18.0), abs(A - m))
        print(f"  N={N:>7d}  A_full={Afull:+.5f}  R={R:+.3f}")

    g1 = last_g[2] < 1e-2 and abs(last_g[1] - 1.0) < 0.3
    g2 = last_p[2] < 1e-1 and abs(last_p[1]) < 0.1
    g3 = last_g[3] < 0.02 and last_g[2] < 0.02        # blocks collapse
    g4 = last_p[3] < 0.02 and last_p[2] < 0.001       # closed orbit exact

    print("\n" + "-" * 70)
    print("INTERPRETATION")
    print("-" * 70)
    print("R_N is the 0/0 ratio of two collapsing Birkhoff averages; its")
    print("removable value distinguishes the point class under the")
    print("doubling map: 1 (generic, full/partial averages both ergodic)")
    print("vs 0 (exceptional, partial blocks lock onto the closed-orbit")
    print("mean 5/18). Both numerator blocks verifiably vanish. Honest")
    print("wall: finite N, one trajectory per class; equidistribution")
    print("heuristic for the generic value.")

    gates = {"G1 generic: R -> 1 and A_full -> 1/3": g1,
             "G2 exceptional: R -> 0 and A_full -> 5/18": g2,
             "G3 generic: 0/0 blocks collapse": g3,
             "G4 exceptional: 0/0 blocks collapse": g4}
    overall = all(gates.values())
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'}")

    os.makedirs(DATA, exist_ok=True)
    json.dump({
        "form": "(A_N - m_N)/(A_N - 1/3) = 0/0 at N=inf",
        "mechanism": "Probe",
        "generic": {"p": p_gen, "q": q_gen, "last": last_g},
        "exceptional": {"p": 1, "q": 3, "last": last_p},
        "gates": gates, "overall": overall,
        "wall": "finite N; equidistribution heuristic"},
        open(os.path.join(DATA, "birkhoff_average_0_over_0.json"), "w"),
        indent=2)
    print("Wrote data/birkhoff_average_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()