"""
The Critical Computation
========================
F''(1/2) = 2|xi|^2 * [(xi'/xi)^2 + xi''/xi]
We need (xi'/xi)^2 + xi''/xi > 0 everywhere.
This computes that quantity directly.
"""

import numpy as np
from mpmath import mp, zeta, gamma, pi, fabs, mpc, power, re as mpre, im as mpim
import json

mp.dps = 30


def xi(s):
    return mp.mpf('0.5') * s * (s - 1) * power(pi, -s/2) * gamma(s/2) * zeta(s)


def compute_critical_quantity(t):
    """
    Compute the two terms in F''(1/2):
    Term A = 2 * |xi'(s)|^2           (always >= 0)
    Term B = 2 * |xi(s)|^2 * Re[xi''(s)/xi(s)]  (can be negative)
    F''(1/2) = A + B
    """
    s = mpc(0.5, t)
    h = mp.mpf('1e-10')

    xi_s = xi(s)

    # First derivative: xi'(s) = dxi/dsigma
    xi_p = (xi(s + h) - xi(s - h)) / (2 * h)

    # Second derivative: xi''(s) = d2xi/dsigma2
    xi_pp = (xi(s + h) - 2 * xi_s + xi(s - h)) / (h * h)

    # F''(1/2) directly
    h2 = 0.005
    fpp = (float(fabs(xi(mpc(0.5 + h2, t))))**2
           - 2 * float(fabs(xi_s))**2
           + float(fabs(xi(mpc(0.5 - h2, t))))**2) / h2**2

    # Component A: 2|xi'|^2
    term_a = 2 * float(fabs(xi_p))**2

    # Component B: 2|xi|^2 * Re(xi''/xi)
    if fabs(xi_s) > 1e-30:
        ratio = xi_pp / xi_s
        term_b = 2 * float(fabs(xi_s))**2 * float(mpre(ratio))
    else:
        ratio = None
        term_b = 0

    # Also compute (xi'/xi)^2 + xi''/xi which has the same sign as F''/|xi|^2
    if fabs(xi_s) > 1e-30:
        ld = xi_p / xi_s
        critical_expr = ld**2 + ratio
        ce_real = float(mpre(critical_expr))
    else:
        ce_real = float('inf')

    # Log derivative components
    ld_real = float(mpre(xi_p / xi_s)) if fabs(xi_s) > 1e-30 else 0
    ld_imag = float(mpim(xi_p / xi_s)) if fabs(xi_s) > 1e-30 else 0

    return {
        't': t,
        'fpp': fpp,
        'term_a': term_a,
        'term_b': term_b,
        'critical_expr_real': ce_real,
        'ld_real': ld_real,
        'ld_imag': ld_imag,
        'xi_val': float(fabs(xi_s)),
        'sign_A': '+' if term_a >= 0 else '-',
        'sign_B': '+' if term_b >= 0 else '-'
    }


def main():
    print("=== The Critical Computation ===")
    print()
    print("F''(1/2) = Term_A + Term_B")
    print("  Term_A = 2|xi'|^2             (ALWAYS >= 0)")
    print("  Term_B = 2|xi|^2 * Re(xi''/xi) (can be negative)")
    print()
    print("For F''(1/2) > 0 we need: Term_A > -Term_B when Term_B < 0.")
    print()

    known_zeros = [14.134725, 21.022040, 25.010858, 30.424876,
                   32.935062, 37.586178, 40.918719, 43.327073,
                   48.005151, 49.773832]

    # Test between zeros at many points
    t_values = [5, 8, 10, 12, 15, 18, 22, 25, 28, 35, 40, 45, 50, 60, 80, 100]

    # Also test AT zeros
    for g in known_zeros[:5]:
        t_values.append(g)
    t_values.sort()

    results = []
    all_positive = True
    for t in t_values:
        r = compute_critical_quantity(t)
        results.append(r)
        is_zero = any(abs(t - z) < 0.1 for z in known_zeros)
        tag = " [ZERO]" if is_zero else ""

        b_sign = "+" if r['term_b'] >= 0 else "-"
        print(f"  t={t:7.2f}: F''={r['fpp']:+.4e}  "
              f"A={r['term_a']:+.4e}  B={r['term_b']:+.4e}  "
              f"A+B={r['fpp']:+.4e}  B_sign={b_sign}{tag}")

        if r['fpp'] <= 0:
            all_positive = False

    print()
    if all_positive:
        print("F''(1/2) > 0 at ALL tested points.")
    else:
        print("WARNING: F''(1/2) <= 0 at some points!")

    # Now the key question: does Term_A always dominate Term_B?
    print()
    print("Does Term_A always dominate when Term_B is negative?")
    dominated = all(r['term_a'] + r['term_b'] > 0 for r in results)
    print(f"  Yes: {dominated}")
    print()

    # The ratio
    print("Ratio |Term_A / Term_B| when Term_B < 0:")
    for r in results:
        if r['term_b'] < -1e-50:
            ratio = r['term_a'] / abs(r['term_b'])
            print(f"  t={r['t']:7.2f}: ratio={ratio:.4f}")

    with open('data/critical_computation_data.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("Saved to data/critical_computation_data.json")


if __name__ == '__main__':
    main()
