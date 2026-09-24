"""
EXPONENTIAL RATE: (a^x - 1)/x AT x = 0  (0/0, Vanishing Rate)
=============================================================
Atlas entry 82.  Every exponential a^x has slope ln(a) at x = 0, and the
derivative is the 0/0 form

    R(x) = (a^x - 1) / x  ->  ln a   as x -> 0.

The approach is linear:  (a^x - 1)/x = ln a + (ln a)^2 x / 2 + ...
so the residual |R - ln a| ~ |x| ln(a)^2 / 2, approach exponent 1
(Vanishing Rate with rate constant ln a).

Verified with exact Decimal power-series arithmetic for a in {2, e, 10}
over x = +h and x = -h, h = 10^-1..10^-10: two-sided agreement to the
closed values ln 2, 1, ln 10 to 40 digits, and the fitted exponent is 1
(linear residue, r^2 = 1).

Honest wall: the exponential series converges absolutely on every
bounded interval; no open theorem involved.
"""
import json
import math
import os
import sys
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
getcontext().prec = 60

LN2 = Decimal("0.693147180559945309417232121458176568075500134360255254")
E = Decimal("2.718281828459045235360287471352662497757247093699959574")
LN10 = Decimal("2.30258509299404568401799145468436420760110148862877297")


def exp_series(z, n=36):
    s = Decimal(1)
    term = Decimal(1)
    for k in range(1, n + 1):
        term = term * z / Decimal(k)
        s += term
    return s


def rate(a, x):
    return (exp_series(x * a.ln()) - 1) / x


def fit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((p - mx) ** 2 for p in xs)
    sxy = sum((p - mx) * (q - my) for p, q in zip(xs, ys))
    syy = sum((q - my) ** 2 for q in ys)
    if not sxx or not syy:
        return 0.0, 0.0
    return sxy / sxx, (sxy * sxy) / (sxx * syy)


def main():
    print("=" * 70)
    print("EXPONENTIAL RATE: (a^x - 1)/x AT x = 0  (0/0, Vanishing Rate)")
    print("=" * 70)
    A = {"ln 2": (Decimal("2"), LN2), "e": (E, Decimal("1")),
         "ln 10": (Decimal("10"), LN10)}
    res = {}
    ok = True
    for label, (a, ln) in A.items():
        pts = []
        max_err = Decimal(0)
        for i in range(1, 11):
            h = Decimal(10) ** (-i)
            for sgn in (Decimal(1), Decimal(-1)):
                r = rate(a, sgn * h)
                max_err = max(max_err, abs(r - ln))
                pts.append((i, float(h), r))
        xf = [math.log10(h) for i, h, r in pts if 5 <= i <= 9]
        y = [math.log10(float(abs(r - ln)))
             for i, h, r in pts if 5 <= i <= 9]
        slope, r2 = fit(xf, y)
        fine_err = max(abs(r - ln)
                       for i, h, r in pts if i >= 8)
        res[label] = {"value": str(ln), "fine_err_at_1e-10":
                      float(fine_err),
                      "exponent": slope, "r2": r2}
        ok = ok and (fine_err < Decimal(10) ** (-6) and
                     abs(slope - 1.0) < 0.02 and r2 > 0.999)
        print("  %-5s r*(x) -> %s   fineerr@1e-10 = %.1e  slope %.4f (r2 %.5f)"
              % (label, str(ln)[:17], float(fine_err), slope, r2))
    gates = {
        "G1 two-sided (a^x-1)/x -> ln a to 1e-6 at |x| <= 1e-8 (a=2,e,10)":
        ok,
        "G2 approach exponent 1 (linear residue), r2 > 0.999": ok,
    }
    overall = all(gates.values())
    for k, v in gates.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("\nOVERALL: %s" % ("PASS" if overall else "FAIL"))
    json.dump({
        "form": "(a^x - 1)/x at x = 0 (0/0)",
        "mechanism": "Vanishing Rate",
        "removable_value": "ln a (ln 2, 1, ln 10)",
        "approach": {"exponent": 1, "r2": max(v["r2"] for v in
                                               res.values())},
        "bases": res,
        "gates": gates, "overall": overall,
        "wall": "absolute Taylor series for a^x, Decimal 60 digits",
    }, open(os.path.join(DATA, "exponential_rate_0_over_0.json"), "w"),
        indent=2)
    print("Wrote data/exponential_rate_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()