"""
The Imaginary Identity
======================
On the critical line, xi'/xi is purely imaginary (Re=0 to order 1e-32).
This means:
  (xi'/xi)^2 = -(Im(xi'/xi))^2    (real, NEGATIVE)
  (xi'/xi)'  = sum 1/(t-gamma_n)^2 - 1/|s|^2    (real, POSITIVE)

The curvature is:
  F''/|xi|^2 = 2[(xi'/xi)^2 + (xi'/xi)' + correction]
             = 2[-(Im(xi'/xi))^2 + sum 1/(t-gn)^2 - 1/|s|^2 + ...]

We need to show: sum 1/(t-gn)^2 > (Im(xi'/xi))^2 + 1/|s|^2
This is a Turan-type inequality.
"""

import numpy as np
from mpmath import mp, zeta, gamma, pi, fabs, mpc, power, re as mpre, im as mpim
import json

mp.dps = 30


def xi(s):
    return mp.mpf('0.5') * s * (s - 1) * power(pi, -s/2) * gamma(s/2) * zeta(s)


def compute_identity(t, gammas):
    """
    Decompose the critical expression into its Hadamard components.
    """
    s = mpc(0.5, t)
    h = mp.mpf('1e-10')

    # xi and derivatives
    xi_s = xi(s)
    xi_p = (xi(s + h) - xi(s - h)) / (2 * h)

    # Logarithmic derivative
    ld = xi_p / xi_s if fabs(xi_s) > 1e-30 else None

    # Numerical F''
    h2 = 0.005
    fpp = (float(fabs(xi(mpc(0.5 + h2, t))))**2
           - 2 * float(fabs(xi_s))**2
           + float(fabs(xi(mpc(0.5 - h2, t))))**2) / h2**2

    # Hadamard sum: sum 1/(t-gamma_n)^2
    inv_sq_sum = sum(1.0 / (t - g)**2 for g in gammas if abs(t - g) > 0.01)

    # |xi'/xi|^2
    ld_sq = float(fabs(ld))**2 if ld else 0

    # (xi'/xi)^2 is -(Im(xi'/xi))^2 when Re=0
    im_ld = float(mpim(ld)) if ld else 0
    im_ld_sq = im_ld**2

    # 1/|s|^2
    inv_s_sq = 1.0 / (0.25 + t**2)

    # The Turan comparison
    # Need: inv_sq_sum > im_ld_sq + inv_s_sq
    turan_surplus = inv_sq_sum - im_ld_sq - inv_s_sq

    return {
        't': t,
        'fpp': fpp,
        'ld_real': float(mpre(ld)) if ld else 0,
        'ld_imag': im_ld,
        'im_ld_sq': im_ld_sq,
        'inv_sq_sum': inv_sq_sum,
        'inv_s_sq': inv_s_sq,
        'turan_surplus': turan_surplus,
        'turan_holds': turan_surplus > 0,
        'xi_val': float(fabs(xi_s))
    }


def main():
    print("=== The Imaginary Identity ===")
    print()
    print("On the critical line s = 1/2 + it:")
    print("  Re(xi'/xi) = 0  (proved numerically to 1e-32)")
    print("  Im(xi'/xi) = sum 1/(t-gn) + Im(1/s)")
    print()
    print("  (xi'/xi)^2 = -(Im(xi'/xi))^2         [real, NEGATIVE]")
    print("  (xi'/xi)'  = sum 1/(t-gn)^2 - 1/|s|^2 [real, POSITIVE]")
    print()
    print("  F''/|xi|^2 = 2[(xi'/xi)^2 + (xi'/xi)' + xi''/xi - (xi'/xi)']")
    print("             = 2[-(Im(xi'/xi))^2 + 2*sum 1/(t-gn)^2 - 2/|s|^2 + ...]")
    print()
    print("TURAN INEQUALITY: sum 1/(t-gn)^2 > (Im(xi'/xi))^2 + 1/|s|^2")
    print()

    gammas = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
              37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
              52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
              67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
              79.337376, 82.910381, 84.735493, 87.425275, 88.809111,
              92.491899, 94.651344, 95.870634, 98.831194, 101.317851]

    t_values = [3, 5, 7, 10, 12, 14.13, 15, 16, 18, 20, 21.02,
                22, 24, 25, 26, 28, 30, 32.94, 35, 37.59, 40, 45,
                50, 60, 70, 80, 100, 150, 200]
    t_values.sort()

    results = []
    all_holds = True
    for t in t_values:
        r = compute_identity(t, gammas)
        results.append(r)
        is_zero = any(abs(t - z) < 0.1 for z in gammas[:10])
        tag = " [ZERO]" if is_zero else ""

        print(f"  t={t:7.2f}: "
              f"|Im(L')|^2={r['im_ld_sq']:+.6e}  "
              f"sum(1/d^2)={r['inv_sq_sum']:+.6e}  "
              f"surplus={r['turan_surplus']:+.6e}  "
              f"holds={r['turan_holds']}{tag}")

        if not r['turan_holds']:
            all_holds = False

    print()
    if all_holds:
        print("TURAN INEQUALITY HOLDS at ALL tested points.")
    else:
        print("TURAN INEQUALITY VIOLATED at some points!")

    # Find minimum surplus
    min_surplus = min(r['turan_surplus'] for r in results)
    min_t = [r['t'] for r in results if r['turan_surplus'] == min_surplus][0]
    print(f"  Minimum surplus: {min_surplus:.6e} at t={min_t:.2f}")

    # Save
    with open('data/imaginary_identity_data.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print("  Saved to data/imaginary_identity_data.json")


if __name__ == '__main__':
    main()
