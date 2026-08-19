"""
Compute F''(1/2) for |xi(sigma+it)|^2 at 16 t-values.
Tests the valley structure at AND between zeros.
"""

import numpy as np
from mpmath import mp, zeta, gamma, pi, fabs, mpc, power
import json

mp.dps = 30


def xi(s):
    return mp.mpf('0.5') * s * (s - 1) * power(pi, -s/2) * gamma(s/2) * zeta(s)


def compute_f_double_prime(t, h=0.01):
    """Compute F''(1/2) = d^2/dsigma^2 |xi(sigma+it)|^2 at sigma=1/2."""
    f_plus = float(fabs(xi(mpc(0.5 + h, t))))**2
    f_center = float(fabs(xi(mpc(0.5, t))))**2
    f_minus = float(fabs(xi(mpc(0.5 - h, t))))**2
    fpp = (f_plus - 2 * f_center + f_minus) / h**2
    return fpp, f_center


def main():
    print("=== F''(1/2) for |xi(sigma+it)|^2 ===")
    print()

    known_zeros = [14.134725, 21.022040, 25.010858, 30.424876,
                   32.935062, 37.586178, 40.918719, 43.327073,
                   48.005151, 49.773832]

    t_values = [5, 8, 10, 12,
                14.13, 15, 18,
                21.02, 22, 25,
                25.01, 28, 30,
                32.94, 35, 37.59,
                40, 45, 50, 60, 70, 80, 100]

    results = []
    for t in t_values:
        fpp, f_val = compute_f_double_prime(t, h=0.005)
        is_near_zero = any(abs(t - z) < 0.5 for z in known_zeros)
        label = "ZERO" if is_near_zero else ""
        results.append({
            't': t,
            'f_double_prime': fpp,
            'f_value': f_val,
            'is_near_zero': is_near_zero,
            'label': label
        })
        print(f"  t={t:7.2f}: F''(1/2)={fpp:+.6e}, F(1/2)={f_val:.4e} {label}")

    print()

    positive = [r for r in results if r['f_double_prime'] > 0]
    negative = [r for r in results if r['f_double_prime'] <= 0]
    print(f"F''(1/2) > 0: {len(positive)}/{len(results)} points")
    if negative:
        print(f"F''(1/2) <= 0 at: {[r['t'] for r in negative]}")

    at_zeros = [r for r in results if r['is_near_zero']]
    between = [r for r in results if not r['is_near_zero']]
    print()
    print("At zeros:")
    for r in at_zeros:
        print(f"  t={r['t']:7.2f}: F''(1/2)={r['f_double_prime']:+.6e}")
    print("Between zeros:")
    for r in between:
        print(f"  t={r['t']:7.2f}: F''(1/2)={r['f_double_prime']:+.6e}")

    with open('data/valley_curvature_data.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("Saved to data/valley_curvature_data.json")


if __name__ == '__main__':
    main()
