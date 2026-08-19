"""
C0 Curvature Analysis
=====================
Tests whether the 0/0 structure forces F''(1/2) > 0.
Computes level sets around zeros to check for elliptical geometry.
"""

import numpy as np
from mpmath import mp, zeta, gamma, pi, fabs, mpc, power
import json

mp.dps = 30


def xi(s):
    return mp.mpf('0.5') * s * (s - 1) * power(pi, -s/2) * gamma(s/2) * zeta(s)


def level_set_around_zero(gamma_n, n_pts=50, radius=0.3):
    """
    Compute |xi(sigma+it)|^2 on a circle around the zero rho_n.
    If the level sets are elliptical (curving up), F''(1/2) > 0.
    """
    t_range = np.linspace(gamma_n - radius, gamma_n + radius, n_pts)
    sigma_range = np.linspace(0.5 - radius, 0.5 + radius, n_pts)

    results = []
    for t in t_range:
        for sigma in sigma_range:
            try:
                val = xi(mpc(sigma, t))
                mag2 = float(fabs(val))**2
                results.append({
                    'sigma': float(sigma),
                    't': float(t),
                    'magnitude_sq': mag2,
                    'distance_to_line': abs(sigma - 0.5),
                    'distance_to_zero': ((sigma - 0.5)**2 + (t - gamma_n)**2)**0.5
                })
            except:
                pass
    return results


def curvature_along_sigma(gamma_n, n_pts=100):
    """
    Compute |xi(sigma+it)|^2 along sigma at fixed t=gamma_n (the zero).
    This IS the valley profile. If it curves up, F''(1/2) > 0.
    """
    sigmas = np.linspace(0.0, 1.0, n_pts)
    results = []
    for sigma in sigmas:
        try:
            val = xi(mpc(sigma, gamma_n))
            mag2 = float(fabs(val))**2
            results.append({'sigma': float(sigma), 'magnitude_sq': mag2})
        except:
            pass
    return results


def curvature_along_t(sigma, t_range=(5, 100), n_pts=200):
    """
    Compute |xi(sigma+it)|^2 along t at fixed sigma.
    Shows the oscillatory behavior.
    """
    tvals = np.linspace(t_range[0], t_range[1], n_pts)
    results = []
    for t in tvals:
        try:
            val = xi(mpc(sigma, t))
            mag2 = float(fabs(val))**2
            results.append({'t': float(t), 'magnitude_sq': mag2})
        except:
            pass
    return results


def mirroring_test(gamma_n):
    """
    Test the mirror symmetry: |xi(0.5-d+it)|^2 vs |xi(0.5+d+it)|^2.
    If equal, the function is symmetric. The curvature is determined
    by the Taylor expansion: F(sigma) = F(0.5) + (1/2)F''(0.5)(sigma-0.5)^2 + ...
    Since F(0.5) = 0 at a zero, and F >= 0 everywhere, F''(0.5) >= 0.
    If the zero is simple, F''(0.5) > 0.
    """
    results = []
    for d in [0.01, 0.05, 0.1, 0.15, 0.2]:
        try:
            left = float(fabs(xi(mpc(0.5 - d, gamma_n))))**2
            right = float(fabs(xi(mpc(0.5 + d, gamma_n))))**2
            center = float(fabs(xi(mpc(0.5, gamma_n))))**2
            diff = abs(left - right)
            # Curvature estimate: F'' ~ 2*(F(0.5+d) - F(0.5)) / d^2
            fpp = 2 * (right - center) / d**2
            results.append({
                'd': d,
                'left': left,
                'right': right,
                'center': center,
                'mirror_diff': diff,
                'curvature_estimate': fpp
            })
        except:
            pass
    return results


def run():
    print("=== C0 Curvature Analysis ===")
    print()

    known_zeros = [14.134725, 21.022040, 25.010858]

    # 1. Valley profile at each zero
    print("1. Valley profile at zeros (|xi|^2 along sigma at t=gamma_n):")
    for gamma in known_zeros:
        profile = curvature_along_sigma(gamma, n_pts=50)
        vals = [r['magnitude_sq'] for r in profile]
        min_val = min(vals)
        # The minimum should be at sigma=0.5 (the zero)
        # and values should increase away from it
        center_idx = len(vals) // 2
        center_val = vals[center_idx]
        left_val = vals[center_idx - 5] if center_idx >= 5 else vals[0]
        right_val = vals[center_idx + 5] if center_idx + 5 < len(vals) else vals[-1]
        increases = left_val > center_val and right_val > center_val
        print(f"  gamma={gamma:.2f}: center={center_val:.4e}, "
              f"left={left_val:.4e}, right={right_val:.4e}, "
              f"curves_up={increases}")
    print()

    # 2. Mirror symmetry test
    print("2. Mirror symmetry |xi(0.5-d)|^2 = |xi(0.5+d)|^2:")
    for gamma in known_zeros:
        mirrors = mirroring_test(gamma)
        max_diff = max(r['mirror_diff'] for r in mirrors)
        print(f"  gamma={gamma:.2f}: max mirror diff = {max_diff:.4e}")
    print()

    # 3. The C0 argument
    print("3. The C0 Argument:")
    print("   At each zero rho_n:")
    print("   - xi(rho_n) = 0 (the 0/0)")
    print("   - |xi|^2 >= 0 everywhere")
    print("   - |xi|^2 = 0 only at zeros")
    print("   - By symmetry: F(sigma) = F(1-sigma)")
    print("   - Therefore F'(1/2) = 0")
    print("   - Since F >= 0 and F(1/2) = 0 at a zero:")
    print("     F''(1/2) >= 0 (local minimum)")
    print("   - If zero is simple (xi'(rho) != 0):")
    print("     F''(1/2) = 2|xi'(rho)|^2 > 0")
    print()

    # 4. Check if zeros are simple
    print("4. Simplicity of zeros:")
    for gamma in known_zeros:
        try:
            h = 1e-12
            xp = float(fabs(xi(mpc(0.5, gamma + h)) - xi(mpc(0.5, gamma - h)))) / (2*h)
            print(f"  gamma={gamma:.2f}: |xi''(rho)| ~ {xp:.4e} (nonzero = simple)")
        except:
            pass
    print()

    # 5. The curvature shape
    print("5. Curvature shape (F''(1/2) at different distances from zero):")
    for gamma in known_zeros:
        mirrors = mirroring_test(gamma)
        for r in mirrors:
            print(f"  gamma={gamma:.2f}, d={r['d']:.2f}: "
                  f"F''~{r['curvature_estimate']:+.6e}")
    print()

    data = {
        'known_zeros': known_zeros,
        'mirrors': {str(g): mirroring_test(g) for g in known_zeros}
    }
    with open('data/c0_curvature_data.json', 'w') as f:
        json.dump(data, f, indent=2, default=str)
    print("Saved to data/c0_curvature_data.json")


if __name__ == '__main__':
    run()
