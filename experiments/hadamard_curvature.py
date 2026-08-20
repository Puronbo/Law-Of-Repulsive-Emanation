"""
Attempting to prove F''(1/2) > 0 everywhere via Hadamard product.
===============================================================
The Hadamard product gives: xi(s) = xi(0) * prod(1 - s/rho_n)
The logarithmic derivative is: xi'/xi = sum 1/(s-rho_n) + regular
On the critical line, 1/(s-rho_n) is purely imaginary.
This constrains the curvature.
"""

import numpy as np
from mpmath import mp, zeta, gamma, pi, fabs, mpc, power, re as mpre, im as mpim
import json

mp.dps = 30


def xi(s):
    return mp.mpf('0.5') * s * (s - 1) * power(pi, -s/2) * gamma(s/2) * zeta(s)


def log_deriv_xi(s):
    """Compute (xi'/xi)(s) via numerical differentiation."""
    h = mp.mpf('1e-15')
    xi_s = xi(s)
    if fabs(xi_s) < 1e-30:
        return None
    xi_prime = (xi(s + h) - xi(s - h)) / (2 * h)
    return xi_prime / xi_s


def hadamard_contribution(s, gammas, n_include=100):
    """
    Compute the Hadamard sum: sum_{n=1}^{N} [1/(s-rho_n) + 1/rho_n]
    This approximates (xi'/xi)(s) - 1/s.
    """
    total = mp.mpc(0, 0)
    for gamma in gammas[:n_include]:
        rho = mpc(0.5, gamma)
        term = mp.mpf('1') / (s - rho) + mp.mpf('1') / rho
        total += term
    return total


def compute_fpp_components(t, gammas):
    """
    Decompose F''(1/2) into components using the Hadamard product.

    F''(1/2) = 2 * Re[(xi'/xi)^2 - xi''/xi] * |xi|^2

    We compute each piece:
    1. (xi'/xi)^2 at s = 1/2 + it
    2. xi''/xi at s = 1/2 + it
    3. The difference
    4. F''(1/2) = 2 * Re[...] * |xi(s)|^2
    """
    s = mpc(0.5, t)

    # Full logarithmic derivative
    lderiv = log_deriv_xi(s)
    if lderiv is None:
        return None

    # Hadamard sum (partial product)
    hadamard_sum = hadamard_contribution(s, gammas, n_include=min(100, len(gammas)))

    # 1/s term
    poly_term = mp.mpf('1') / s

    # Total from Hadamard
    total_hadamard = poly_term + hadamard_sum

    # Components of the Hadamard sum
    # On the critical line, 1/(s-rho_n) = 1/(i(t-gamma_n)) = -i/(t-gamma_n)
    # This is purely imaginary

    real_parts = []
    imag_parts = []
    for gamma in gammas[:100]:
        diff = t - gamma
        if abs(diff) > 1e-10:
            # 1/(s-rho_n) = -i/(t-gamma_n) (purely imaginary)
            imag_part = mp.mpf('-1') / diff
            real_parts.append(0.0)
            imag_parts.append(float(imag_part))
        else:
            # Near a zero: the term is large
            real_parts.append(None)
            imag_parts.append(None)

    # F''(1/2) via direct computation
    h = 0.005
    f_plus = float(fabs(xi(mpc(0.5 + h, t))))**2
    f_center = float(fabs(xi(mpc(0.5, t))))**2
    f_minus = float(fabs(xi(mpc(0.5 - h, t))))**2
    fpp_direct = (f_plus - 2 * f_center + f_minus) / h**2

    # |xi(s)|^2
    xi_val = float(fabs(xi(s)))**2

    return {
        't': t,
        'fpp_direct': fpp_direct,
        'f_value': xi_val,
        'log_deriv_real': float(mpre(lderiv)),
        'log_deriv_imag': float(mpim(lderiv)),
        'hadamard_real': float(mpre(total_hadamard)),
        'hadamard_imag': float(mpim(total_hadamard)),
        'n_imaginary_terms': sum(1 for x in imag_parts if x is not None),
        'sum_imaginary': sum(x for x in imag_parts if x is not None)
    }


def run():
    print("=== Hadamard Product Analysis of F''(1/2) ===")
    print()

    # Known zeros (first 100)
    gammas = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
              37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
              52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
              67.079811, 69.546402, 72.067158, 75.704691, 77.144840]

    t_values = [5, 10, 14.13, 15, 18, 21.02, 22, 25, 30, 40, 50, 100]

    print("Key identity on the critical line:")
    print("  For s = 1/2 + it, rho_n = 1/2 + i*gamma_n:")
    print("  1/(s-rho_n) = 1/(i(t-gamma_n)) = -i/(t-gamma_n)")
    print("  This is PURELY IMAGINARY.")
    print()
    print("  Therefore: the Hadamard sum is purely imaginary")
    print("  (away from zeros). The real part comes from 1/s only.")
    print()
    print("  This means: (xi'/xi) is nearly imaginary on the line.")
    print("  Re(xi'/xi)^2 ~ -(Im(xi'/xi))^2 < 0.")
    print("  But F''(1/2) = 2*Re[(xi'/xi)^2 - xi''/xi]*|xi|^2 > 0.")
    print("  So Re(xi''/xi) must be sufficiently negative to compensate.")
    print()

    results = []
    for t in t_values:
        r = compute_fpp_components(t, gammas)
        if r is not None:
            results.append(r)
            is_zero = "ZERO" if any(abs(t - z) < 0.5 for z in gammas[:5]) else ""
            print(f"  t={t:6.2f}: F''={r['fpp_direct']:+.4e}, "
                  f"Re(xi'/xi)={r['log_deriv_real']:+.4e}, "
                  f"Im(xi'/xi)={r['log_deriv_imag']:+.4e}, "
                  f"sum_im={r['sum_imaginary']:+.4f} {is_zero}")

    print()
    print("Conclusion:")
    print("  The Hadamard sum is purely imaginary on the critical line.")
    print("  This constrains the curvature but does not prove F''>0 alone.")
    print("  The proof requires controlling xi''/xi as well.")

    with open('data/hadamard_curvature_data.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print("  Saved to data/hadamard_curvature_data.json")


if __name__ == '__main__':
    run()
