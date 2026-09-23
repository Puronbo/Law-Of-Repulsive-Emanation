"""
GALOIS THEORY: DISCRIMINANT AT A REPEATED ROOT  (0/0, Vanishing Rate)
====================================================================
Missing-experiment sweep, atlas 6.1 row 1 (Galois theory).

A real polynomial with a root of multiplicity m >= 2 has discriminant
Disc(f) = 0.  Under a generic perturbation f_t = f_0 + t q, the block
of m repeated roots splits with gaps ~ t^{1/m}, so

    Disc(f_t) =  C . t^{m-1} + O(t^{m}),     C =/= 0.

At t = 0 both the discriminant and its separability scale vanish, so
the ratio  Disc(f_t)/t^{m-1}  is a genuine 0/0 whose removable value
C is set by the non-degenerate roots (after removing the split block).
The vanishing RATE (exponent m-1) is the multiplicity fingerprint:
the mechanism is Vanishing Rate.

Float Sylvester resultants suffer catastrophic cancellation exactly
at the degeneracy, so the discriminant is computed EXACTLY: disc(t_k)
for 12 rational nodes via exact fraction Gaussian elimination, then
exact rational interpolation in t (Laplace/Lagrange) restores the
whole polynomial; the valuation (m-1) and the leading coefficient C
are read off exactly.  A verification node t = 1/8 cross-checks the
interpolant against a direct exact computation.

Closed-form estimates for the two explicit families:
    (x-1)^2 (x-2)(x-3) + t x^3:   split gap^2 ~ 2|t|, cross terms
        (1-2)^2 (1-3)^2 (2-3)^2 = 4  (two copies over the split pair)
        -> |C| = 2 * 4 * 4 = 32.
    (x-1)^3 (x-2) + t x^4:         three split pairs (disc(y^3-1) =
        27 in magnitude), cross factors -> 1  ->  |C| = 27 (blocks).

Honest wall: exact arithmetic on the two explicit families; the
aliasing-free interpolation assumes the discriminant is polynomial in
t (true in finite degree); no general theorem claimed.
"""
import json
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")


def sylvester_det(P, Q):
    """Exact resultant of two polynomial coefficient lists (Fractions)."""
    n, m = len(P) - 1, len(Q) - 1
    size = n + m
    M = [[Fraction(0) for _ in range(size)] for __ in range(size)]
    for k in range(m):
        for i in range(n + 1):
            M[k][i + k] = P[i]
    for k in range(n):
        for j in range(m + 1):
            M[m + k][j + k] = Q[j]
    det = Fraction(1)
    for col in range(size):
        piv = None
        for r in range(col, size):
            if M[r][col] != 0:
                piv = r
                break
        if piv is None:
            return Fraction(0)
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
            det = -det
        pv = M[col][col]
        det *= pv
        for r in range(col + 1, size):
            fac = M[r][col] / pv
            if fac != 0:
                for c in range(col, size):
                    M[r][c] -= fac * M[col][c]
    return det


def polyder_frac(cs):
    n = len(cs) - 1
    return [Fraction(n - i) * c for i, c in enumerate(cs) if i < n]


def disc_at(node, base, q):
    """(Signed) discriminant of base + node*q, lc = 1."""
    f = [base[i] + node * q[i] for i in range(len(base))]
    return sylvester_det(f, polyder_frac(f))


def interpolate(nodes, vals):
    """Lagrange interpolant as a list of Fraction coeffs (ascending)."""
    deg = len(nodes) - 1
    base = [Fraction(1)]                      # polynomial 1
    for j in range(deg + 1):
        base = polymul(base, [-Fraction(nodes[j]), Fraction(1)])
    out = [Fraction(0) for _ in range(len(base))]
    for k in range(deg + 1):
        # Lagrange basis L_k
        den = Fraction(1)
        for j in range(deg + 1):
            if j != k:
                den *= (nodes[k] - nodes[j])
        num = [Fraction(1)]
        for j in range(deg + 1):
            if j != k:
                num = polymul(num, [-Fraction(nodes[j]), Fraction(1)])
        coef = vals[k] / den
        for i, c in enumerate(num):
            out[i] += coef * c
    while out and out[-1] == 0:
        out.pop()
    return out


def polysub(a, b):
    out = a[:]
    while len(out) < len(b):
        out.append(Fraction(0))
    for i in range(len(b)):
        out[len(out) - 1 - i] = b[len(b) - 1 - i]
    return out


def polymul(a, b):
    r = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            r[i + j] += ai * bj
    return r


def polyval_frac(cs, t):
    v = Fraction(0)
    for c in reversed(cs):
        v = v * t + c
    return v


def valuation(cs):
    for i, c in enumerate(cs):
        if c != 0:
            return i, c
    return None, Fraction(0)


def analyze(base, q, target, label):
    nodes = [Fraction(2 * k + 1, 4) for k in range(12)]
    vals = [disc_at(t, base, q) for t in nodes]
    poly = interpolate(nodes, vals)
    e, C = valuation(poly)
    # verification: interpolant must reproduce the direct disc at 1/8
    check = polyval_frac(poly, Fraction(1, 8)) == disc_at(Fraction(1, 8),
                                                         base, q)
    return e, C, check, 1.0 if target == 0 else abs(C) / target


def main():
    print("=" * 70)
    print("GALOIS THEORY: DISCRIMINANT AT A REPEATED ROOT (0/0, VR)")
    print("=" * 70)
    ok = True

    # (x-1)^2 (x-2)(x-3)  ->  m = 2,  expectation: Disc ~ C t, |C| = 32
    base2 = [Fraction(1), Fraction(-7), Fraction(17), Fraction(-17),
             Fraction(6)]
    q3 = [Fraction(0), Fraction(0), Fraction(0), Fraction(1), Fraction(0)]
    e2, C2, chk2, m2 = analyze(base2, q3, 32.0, "double root")
    print(f"\nDouble root  (x-1)^2 (x-2)(x-3) + t x^3")
    print(f"  exact Disc(t) valuation e = {e2}   (expect 1 = m-1)")
    print(f"  exact leading coefficient C = {C2}   "
          f"(|C|={abs(C2)}; closed form 32)")
    print(f"  interpolation verified at t=1/8: {chk2}")
    g1 = (e2 == 1) and chk2
    g_c2 = 0.7 < m2 < 1.4

    # (x-1)^3 (x-2)  ->  m = 3,  expectation: Disc ~ C t^2, |C| = 27
    base3 = [Fraction(1), Fraction(-5), Fraction(9), Fraction(-7),
             Fraction(2)]
    q4 = [Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    e3, C3, chk3, m3 = analyze(base3, q4, 27.0, "triple root")
    print(f"\nTriple root  (x-1)^3 (x-2) + t x^4")
    print(f"  exact Disc(t) valuation e = {e3}   (expect 2 = m-1)")
    print(f"  exact leading coefficient C = {C3}   "
          f"(|C|={abs(C3)}; closed form 27)")
    print(f"  interpolation verified at t=1/8: {chk3}")
    g2 = (e3 == 2) and chk3
    g_c3 = 0.7 < m3 < 1.4

    # removable values (magnitudes)
    C2m, C3m = abs(C2), abs(C3)
    g4 = C2m > 0 and C3m > 0

    print("\n" + "-" * 70)
    print("INTERPRETATION")
    print("-" * 70)
    print("Disc(f_t)/t^{m-1} at t = 0 is a genuine 0/0: discriminant and")
    print("separability scale vanish together; the removable (leading)")
    print("value C is set by the NON-degenerate cross-root content, the")
    print("vanishing rate m-1 by the block multiplicity (Vanishing Rate).")
    print("Exact rational arithmetic (interpolation over fractions).")
    print("Honest wall: two explicit families; exact finite-degree calc.")

    gates = {"G1 double-root rate m-1 = 1 (valuation)": g1,
             "G2 triple-root rate m-1 = 2 (valuation)": g2,
             "G3 leading C matches closed form (double)": g_c2,
             "G4 leading C matches closed form (triple)": g_c3}
    overall = all(gates.values())
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'}")

    os.makedirs(DATA, exist_ok=True)
    json.dump(
        {"form": "Disc(f_t)/t^{m-1} at t=0 (0/0)", "mechanism":
         "Vanishing Rate",
         "double_root": {"valuation": e2, "leading_C": str(C2),
                         "verified": chk2},
         "triple_root": {"valuation": e3, "leading_C": str(C3),
                         "verified": chk3},
         "gates": gates, "overall": overall,
         "wall": "exact rational interpolation on two families"},
        open(os.path.join(DATA, "galois_discriminant_0_over_0.json"), "w"),
        indent=2)
    print("Wrote data/galois_discriminant_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()