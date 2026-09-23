"""
COMBINATORICS: GENERATING FUNCTION SINGULARITY AT THE RADIUS  (0/0, VR)
=======================================================================
Missing-experiment sweep, atlas 6.1 row 5 (Combinatorics).

For a combinatorial class with generating function singular at z = rho,
the coefficients decay as  a_n ~ A . rho^{-n} . n^{-alpha}  with the
universal amplitude A fixed by the singular type.  The 0/0 form: the
coefficient a_n AND the transfer prediction rho^{-n}.n^{-alpha} both
vanish in the appropriate limit; the amplitude A is the removable
value of  a_n . rho^{n} . n^{alpha}  at infinity (Vanishing Rate:
rate alpha and value A both coded by the singular type).

Two exact cases (the square-root-like singularities at rho = 1/4):
    Catalan C_n = binom(2n,n)/(n+1):       C_n ~ 4^n / (sqrt(pi) n^{3/2})
    central binomial b_n = binom(2n,n):    b_n ~ 4^n / sqrt(pi n)

So the amplitude A = 1/sqrt(pi) in both, alpha = 3/2 vs 1/2.

Numbers evaluated in log space (lgamma) to avoid under/overflow at
n = 20000.  Honest wall: large-but-finite n; these exact-asymptotic
identities are classical.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
SQPI = 1.0 / math.sqrt(math.pi)      #  0.56419


def log_comb(ln2n, lnn):
    return math.lgamma(2 * ln2n + 1) - 2.0 * math.lgamma(lnn + 1)


def catalan_transform(n):
    """C_n * (1/4)^n * n^{3/2}."""
    lg = log_comb(n, n) - n * math.log(4.0)
    return math.exp(lg) * (n ** 1.5) / (n + 1.0)


def binom_transform(n):
    """b_n * (1/4)^n * n^{1/2}."""
    lg = log_comb(n, n) - n * math.log(4.0)
    return math.exp(lg) * (n ** 0.5)


def main():
    print("=" * 70)
    print("COMBINATORICS: GENERATING FUNCTION SINGULARITY (0/0, VR)")
    print("=" * 70)

    print("\nCatalan numbers  C_n ~ 4^n / (sqrt(pi) n^{3/2})")
    c_rows = []
    for n in [1000, 5000, 20000]:
        v = catalan_transform(n)
        c_rows.append((n, v))
        print(f"  n={n:>6d}  C_n*rho^n*n^{'3/2':>4} = {v:.5f} "
              f"(1/sqrt(pi)={SQPI:.5f})")
    amp_c = c_rows[-1][1]
    g_cat_amp = abs(amp_c - SQPI) / SQPI < 0.002
    sl_c = (math.log(c_rows[-1][1]) - math.log(c_rows[-2][1])) / \
           (math.log(c_rows[-1][0]) - math.log(c_rows[-2][0]))
    alpha_c = 3.0 / 2.0 + sl_c        # slope of the residual drift
    g_cat_exp = abs(sl_c) < 0.005
    print(f"  residual drift (log-log slope towards 3/2) = {sl_c:+.4f}")

    print("\nCentral binomial  b_n ~ 4^n / sqrt(pi n)")
    b_rows = []
    for n in [1000, 5000, 20000]:
        v = binom_transform(n)
        b_rows.append((n, v))
        print(f"  n={n:>6d}  b_n*rho^n*sqrt(n)  = {v:.5f} "
              f"(1/sqrt(pi)={SQPI:.5f})")
    amp_b = b_rows[-1][1]
    g_bin_amp = abs(amp_b - SQPI) / SQPI < 0.002
    sl_b = (math.log(b_rows[-1][1]) - math.log(b_rows[-2][1])) / \
           (math.log(b_rows[-1][0]) - math.log(b_rows[-2][0]))
    g_bin_exp = abs(sl_b) < 0.005
    print(f"  residual drift (flat -> exponent 1/2) = {sl_b:+.4f}")

    print("\nRadius: 1/rho = limsup a_n^{1/n}")
    n = 20000
    lg = log_comb(n, n) - n * math.log(4.0)
    rn_c = 4.0 * math.exp(lg / n) * (n + 1.0) ** (-1.0 / n)
    print(f"  C_n^{{1/n}} at n={n} = {rn_c:.5f} (expect 4.0000)")
    g_radius = abs(rn_c - 4.0) < 0.02

    print("\n" + "-" * 70)
    print("INTERPRETATION")
    print("-" * 70)
    print("At the radius of convergence (rho), coefficient and transfer")
    print("prediction vanish together; the amplitude A = 1/sqrt(pi) is")
    print("the removable value of the 0/0  a_n.rho^n.n^alpha  (Vanishing")
    print("Rate). alpha = 3/2 (Catalan) vs 1/2 (plain sqrt). Honest")
    print("wall: exact sequences at large finite n; classical asympt.")

    gates = {
        "G1 Catalan amplitude 1/sqrt(pi) at n=20000": g_cat_amp,
        "G2 Catalan exponent 3/2 (drift -> 0)": g_cat_exp,
        "G3 central-binomial amplitude 1/sqrt(pi)": g_bin_amp,
        "G4 central-binomial exponent 1/2 (drift -> 0)": g_bin_exp,
        "G5 radius 1/rho = 4": g_radius,
    }
    overall = all(gates.values())
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"\nOVERALL: {'PASS' if overall else 'FAIL'}")

    os.makedirs(DATA, exist_ok=True)
    json.dump(
        {"form": "a_n * rho^n * n^alpha -> A (0/0 at the radius)",
         "mechanism": "Vanishing Rate",
         "removable_value": SQPI,
         "catalan_rows": c_rows, "central_binom_rows": b_rows,
         "alpha_catalan": 3.0 / 2.0 + sl_c,
         "alpha_binom": 1.0 / 2.0 + sl_b,
         "radius": rn_c,
         "gates": gates, "overall": overall,
         "wall": "exact sequences, finite n; classical asymptotics"},
        open(os.path.join(DATA, "generating_function_singularity_0_over_0.json"),
             "w"), indent=2)
    print("Wrote data/generating_function_singularity_0_over_0.json")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()