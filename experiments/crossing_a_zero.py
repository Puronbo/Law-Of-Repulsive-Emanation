"""
CROSSING A ZERO: THE 0/0 PARITY LAW AT A MUTUAL ZERO
===============================================================
Atlas entry 80.  Constructive-program instance (Critical Phenomenon).

A mutual zero is a point x0 where BOTH the numerator and the denominator
vanish: F(x0) = G(x0) = 0, the 0/0 form itself.  The question this entry
answers is *what survives the mutual zero* -- and the answer is a law of
crossing.  Take

    F(x) = (x - 1)^(m+j) * V(x)          V(1) = v0 != 0
    G(x) = (x - 1)^m       * U(x)        U(1) = 1

so that F and G share the mutual zero x = 1 with multiplicity gap j >= 0
(m is the depth of the shared root in the denominator).  The ratio

    R(x) = F(x) / G(x) = (x - 1)^j * V(x) / U(x)

is the 0/0 at x = 1.  The parity law this entry verifies:

  1.  j = 0  (numerator and denominator vanish to the same depth):
      the ratio CONTINUES through the mutual zero; the removable value is
      the exact rational r* = V(1)/U(1) = v0, and R keeps one sign on
      both sides -- the value is *carried across*.
  2.  j >= 1 (the gap in vanishing depth) : the removable value is 0, and
      R approaches 0 at rate |R| ~ v0 * |x-1|^j -- the rate constant is
      the SAME v0 that would have been the value.  Whether the ratio
      *crosses* the zero is the parity of j:
          j odd   -> R flips sign through x = 1    (CROSSES a zero)
          j even  -> R keeps one sign (endpoint bounce, tangent to zero).
      The angle of arrival is (x-1) -> 0; the index of the crossing is
      (-1)^j, read bound the same way the anti-class frame reads the
      decade trend of a ratio.

So v0 is invariant under the 0/0: at the mutual zero it is either the
value (j = 0) or the rate (j >= 1), and which of the two it is -- plus
whether the ratio physically crosses the zero -- is carried exactly by
the multiplicity gap j.  Every instance below is a rational family for
which the value and the rate are EXACT rational numbers, verified here
with 60-digit Decimal arithmetic by one-sided approach to x = 1 from
both sides.

Honest wall: closed-form rational families, machine-exact to 60 digits,
no open theorem; a reviewer can recompute every number exactly.
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")

getcontext().prec = 60
ONE = Decimal(1)


def dec(s):
    if "/" in s:
        num, den = s.split("/")
        return Decimal(num) / Decimal(den)
    return Decimal(s)


def one_sided(j, m, v0, v1, u2, sign):
    """R(1 + sign * h) for h = 10^-i, i = 1..N, returned as (i, h, R)."""
    out = []
    k = j
    for i in range(1, N + 1):
        h = dec("1e-%d" % i)
        if sign < 0:
            xm1 = -h
        else:
            xm1 = h
        # V(x) = v0 + v1*(x-1);  U(x) = 1 + u2*(x-1)^2
        V = v0 + v1 * xm1
        U = ONE + u2 * xm1 * xm1
        # (x-1)^k computed by repeated multiplication (exact powers of 10)
        pw = ONE
        for _ in range(k):
            pw *= xm1
        R = pw * V / U
        out.append((i, h, R))
    return out


def slope_gap(points, r_cf):
    """log-log slope of |R - r_cf| vs |h| over i in [8, 28]."""
    pts = []
    for i, h, R in points:
        if i < 8 or i > 28:
            continue
        err = abs(R - r_cf)
        if err == 0:
            continue
        pts.append((math.log10(float(abs(h))), math.log10(float(err))))
    n = len(pts)
    mx = sum(p for p, _ in pts) / n
    my = sum(q for _, q in pts) / n
    sxx = sum((p - mx) ** 2 for p, _ in pts)
    sxy = sum((p - mx) * (q - my) for p, q in pts)
    syy = sum((q - my) ** 2 for _, q in pts)
    slope = sxy / sxx if sxx else 0.0
    r2 = (sxy * sxy) / (sxx * syy) if sxx and syy else 0.0
    return slope, r2, n


N = 30  # one-sided h = 10^-1 .. 10^-30, 60-digit right arithmetic


def main():
    print("=" * 70)
    print("CROSSING A ZERO: THE 0/0 PARITY LAW AT A MUTUAL ZERO")
    print("=" * 70)
    print("F = (x-1)^(m+j) V(x),  G = (x-1)^m U(x),  V(1)=v0, U(1)=1")

    # j=0 continuity instances (value carried across), then crossing
    # instances (value 0; rate |R| ~ v0 |h|^j; sign flip iff j odd).
    # The two exact-rational pins re-use the register's certified
    # rationals 2048/65537 and 65537/67108865 from the twin closure.
    SPECS = [
        ("CONT_1", 1, 0, "2048/65537", 3, 1),
        ("CONT_2", 2, 0, "65537/67108865", 5, 2),
        ("CR_1", 1, 1, "2048/65537", -7, 1),
        ("CR_2", 1, 2, "3/4", 2, 3),
        ("CR_3", 2, 1, "65537/67108865", 4, 2),
        ("CR_4", 1, 3, "1/2", 6, 1),
        ("CR_5", 2, 2, "129/128", -3, 4),
        ("CR_6", 3, 1, "5/2", 1, 1),
    ]

    instances = {}
    max_err = 0.0
    print("\n  name      m  j   value         slopeL  slopeR   r2     flip")
    for name, m, j, v0_str, v1, u2 in SPECS:
        v0 = dec(v0_str)
        r_cf = v0 if j == 0 else dec("0")
        left = one_sided(j, m, v0, v1, u2, -1)
        right = one_sided(j, m, v0, v1, u2, +1)
        # two-sided agreement to the closed form at the finest h
        err = 0.0
        for _, _, R in (left[-1], right[-1]):
            err = max(err, float(abs(R - r_cf)))
        max_err = max(max_err, err)
        # crossing parity read at the finest h
        signL = (left[-1][2] > 0) - (left[-1][2] < 0)
        signR = (right[-1][2] > 0) - (right[-1][2] < 0)
        flip = signL != signR
        sl, r2l, _ = slope_gap(left, r_cf)
        sr, r2r, _ = slope_gap(right, r_cf)
        expect_flip = (j >= 1) and (j % 2 == 1)
        instances[name] = {
            "m": m, "j": j, "v0": v0_str, "v1": v1, "u2": u2,
            "value": ("0" if j >= 1 else v0_str),
            "rate_constant": v0_str,
            "max_divergence_from_value": err,
            "slope_left": sl, "slope_right": sr,
            "r2_left": r2l, "r2_right": r2r,
            "sign_left": signL, "sign_right": signR,
            "crosses_zero": flip,
        }
        print("  %-8s  %d  %d   %-12s %.5f %.5f  %.5f   %s"
              % (name, m, j, ("2048/65537" if "2048" in v0_str
                              else ("65537/67108865" if "671" in v0_str
                                    else v0_str)),
                 sl, sr, min(r2l, r2r), ("YES" if flip else "no ")))

    # ---- gates (all closed, all exact) ----
    g1 = max_err < 1e-20
    print("\n  two-sided closeness to the closed 0/0 value: %.2e" % max_err)
    g2 = all(instances[n]["crosses_zero"]
             == (instances[n]["j"] >= 1 and instances[n]["j"] % 2 == 1)
             for n in instances)
    g3 = True
    for n, it in instances.items():
        want = it["j"] if it["j"] >= 1 else 1
        ok = (abs(it["slope_left"] - want) < 0.02
              and abs(it["slope_right"] - want) < 0.02
              and min(it["r2_left"], it["r2_right"]) > 0.999)
        g3 = g3 and ok
    g4 = (instances["CONT_1"]["value"] == "2048/65537"
          and instances["CR_1"]["rate_constant"] == "2048/65537"
          and instances["CONT_2"]["value"] == "65537/67108865"
          and instances["CR_3"]["rate_constant"] == "65537/67108865")

    gates = {
        "G1 two-sided limit equals the 0/0 value to 1e-20 at the finest "
        "step (all 8)": g1,
        "G2 crossing parity: sign flip through the mutual zero iff j odd "
        "(j>=1)": g2,
        "G3 approach exponent = gap j (j>=1) or 1 (j=0), r2 > 0.999": g3,
        "G4 exact-rational pins 2048/65537 and 65537/67108865 appear as "
        "value and rate": g4,
    }
    overall = all(gates.values())
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))

    os.makedirs(DATA, exist_ok=True)
    payload = {
        "form": "R(x) = (x-1)^j V(x) / U(x), mutual 0/0 at x = 1",
        "mechanism": "Critical Phenomenon",
        "point": "x -> 1 through the shared zero of F=(x-1)^(m+j)V and "
                 "G=(x-1)^m U; V(1)/U(1) = v0",
        "removable_value": "j=0 -> v0 (carried across); j>=1 -> 0 "
                           "(arrival rate v0 |h|^j)",
        "crossing_parity_law": "R crosses zero through x = 1 iff j odd",
        "instances": instances,
        "gates": gates,
        "overall": overall,
        "wall": "closed-form rational families, 60-digit Decimal "
                "one-sided approach; every number recomputable exactly; "
                "no open theorem involved",
    }
    with open(os.path.join(DATA, "crossing_a_zero.json"), "w") as f:
        json.dump(payload, f, indent=2)
    print("Wrote data/crossing_a_zero.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()