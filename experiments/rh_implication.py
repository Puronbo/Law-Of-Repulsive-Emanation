"""
What does F''(1/2) > 0 prove?
=============================
Identity: F''(1/2) = 2*L'*|xi|^2 > 0

L' = sum 1/(t-gn)^2 > 0  (proved from Hadamard product)

This proves the critical line is a valley everywhere.
But does it prove RH? Let's check.
"""

import numpy as np
from mpmath import mp, zeta, gamma, pi, fabs, mpc, power
import json

mp.dps = 30


def xi(s):
    return mp.mpf('0.5') * s * (s - 1) * power(pi, -s/2) * gamma(s/2) * zeta(s)


def g(sigma, t):
    """g(sigma) = |xi(sigma+it)|^2 as a function of sigma at fixed t."""
    return float(fabs(xi(mpc(sigma, t))))**2


def find_w_shape(t):
    """
    For fixed t, compute g(sigma) for sigma in [0, 1].
    Look for W-shape: zeros at sigma_0, 1-sigma_0, local min at 1/2.
    """
    sigmas = np.linspace(0.01, 0.99, 200)
    vals = [g(s, t) for s in sigmas]

    # Find where g is near zero
    min_val = min(vals)
    min_idx = vals.index(min_val)

    # Find the value at sigma=1/2
    center_val = g(0.5, t)

    # Find local maxima between sigma=0 and sigma=0.5
    # and between 0.5 and 1
    max_left = max(vals[:min_idx+1]) if min_idx > 0 else 0
    max_right = max(vals[min_idx:]) if min_idx < len(vals)-1 else 0

    return {
        't': t,
        'center_val': center_val,
        'min_val': min_val,
        'min_sigma': sigmas[min_idx],
        'max_left': max_left,
        'max_right': max_right,
        'w_shape': min_val < center_val and center_val > 0
    }


def main():
    print("=== Does F''(1/2) > 0 prove RH? ===")
    print()
    print("The identity F''(1/2) = 2*L'*|xi|^2 proves:")
    print("  - The critical line is a valley (local minimum of |xi|^2)")
    print("  - L' = sum 1/(t-gn)^2 > 0 (from Hadamard product)")
    print("  - F'' > 0 at every point on the line")
    print()
    print("BUT: could off-line zeros exist?")
    print("  - Off-line zeros at (sigma_0, t_0) and (1-sigma_0, t_0)")
    print("  - g(sigma) = |xi(sigma+it_0)|^2 would be 0 at sigma_0, 1-sigma_0")
    print("  - g(1/2) > 0 (positive local minimum)")
    print("  - This creates a W-shape: 0, up, down, up, 0")
    print("  - F''(1/2) > 0 is CONSISTENT with this W-shape")
    print()
    print("So F''(1/2) > 0 does NOT prove RH by itself.")
    print("It proves the line is a valley but not that off-line zeros are impossible.")
    print()

    # Verify W-shape is geometrically possible
    print("Numerical check: can we see the W-shape?")
    print("(If g has zeros at sigma_0 and 1-sigma_0 with g(1/2) > 0, it's a W)")
    print()

    # At a zero on the critical line, g(1/2) = 0 (no W-shape)
    # Between zeros, g(1/2) > 0 and no off-line zeros (no W-shape visible)
    # Off-line zeros would show g(sigma_0) = 0 with sigma_0 != 1/2

    gammas = [14.134725, 21.022040, 25.010858]

    for gamma in gammas:
        # At the zero, check g(sigma) for sigma near 0.5
        sigmas_test = [0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7]
        print(f"  t = {gamma:.2f} (on-line zero):")
        for sigma in sigmas_test:
            val = g(sigma, gamma)
            print(f"    sigma={sigma:.2f}: |xi|^2 = {val:.4e}")
        print()

    # Between zeros
    t_between = [16, 23, 35]
    for t in t_between:
        sigmas_test = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        vals = [g(s, t) for s in sigmas_test]
        print(f"  t = {t:.2f} (between zeros):")
        for s, v in zip(sigmas_test, vals):
            print(f"    sigma={s:.1f}: |xi|^2 = {v:.4e}")
        print(f"    Min: {min(vals):.4e} at sigma={sigmas_test[vals.index(min(vals))]:.1f}")
        print(f"    g(0.5) = {g(0.5, t):.4e}")
        print()

    print("CONCLUSION:")
    print("  The identity F'' = 2L'|xi|^2 is a theorem.")
    print("  It proves the critical line is a valley everywhere.")
    print("  But it does NOT prove RH (off-line zeros could exist as W-shapes).")
    print("  To prove RH, need to show no W-shapes exist.")
    print("  This requires controlling xi(sigma+it) for sigma != 1/2.")


if __name__ == '__main__':
    main()
