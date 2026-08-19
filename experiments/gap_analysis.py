"""
Gap Analysis: derivatives at zeros and lean ratios
===================================================
Focused on the two most critical gap measurements.
"""

import numpy as np
from mpmath import mp, zeta, gamma, pi, fabs, mpc, power
import json

mp.dps = 30


def xi(s):
    return mp.mpf('0.5') * s * (s - 1) * power(pi, -s/2) * gamma(s/2) * zeta(s)


def xi_prime(s):
    h = mp.mpf('1e-15')
    return (xi(s + h) - xi(s - h)) / (2 * h)


def xi_prime_at_zeros():
    known = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
             37.586178, 40.918719, 43.327073, 48.005151, 49.773832]

    results = []
    for i, gamma in enumerate(known):
        rho = mpc(0.5, gamma)
        xi_val = xi(rho)
        xp = xi_prime(rho)
        mag_val = float(fabs(xi_val))
        mag_prime = float(fabs(xp))
        phase = float(mp.arg(xp))
        results.append({
            'index': i + 1,
            'gamma': gamma,
            'xi_magnitude': mag_val,
            'xi_prime_magnitude': mag_prime,
            'xi_prime_phase_rad': phase,
            'xi_prime_phase_deg': float(phase * 180 / pi),
            'is_simple': mag_prime > 1e-10
        })
    return results


def lean_ratios():
    """Compute |xi(sigma+it)|/|xi(1-sigma+it)| at zero ordinates."""
    zero_ts = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062]
    sigmas = [0.0, 0.1, 0.2, 0.3, 0.4, 0.45, 0.5]

    results = []
    for t in zero_ts:
        for sigma in sigmas:
            try:
                left = xi(mpc(sigma, t))
                right = xi(mpc(1 - sigma, t))
                ml = float(fabs(left))
                mr = float(fabs(right))
                ratio = ml / max(mr, 1e-30)
                results.append({
                    'sigma': sigma, 't': t,
                    'left': ml, 'right': mr,
                    'ratio': ratio,
                    'is_one': abs(ratio - 1.0) < 1e-10
                })
            except:
                pass
    return results


def gradient_at_line():
    """
    Compute d/dsigma |xi(sigma+it)|^2 at sigma=1/2.
    If = 0, the function has no gradient off the line (no lean).
    """
    zero_ts = [14.134725, 21.022040, 25.010858]
    results = []
    for t in zero_ts:
        h = 0.01
        vals = []
        for ds in [-h, 0, h]:
            sigma = 0.5 + ds
            try:
                val = xi(mpc(sigma, t))
                vals.append(float(fabs(val)))
            except:
                vals.append(None)
        if all(v is not None for v in vals):
            grad = (vals[2] - vals[0]) / (2 * h)
            laplacian = (vals[2] - 2*vals[1] + vals[0]) / (h**2)
            results.append({
                't': t,
                'val_at_line': vals[1],
                'gradient': grad,
                'laplacian': laplacian,
                'flat': abs(grad) < 1e-10
            })
    return results


def run():
    print("=== Gap Analysis ===\n")

    print("1. xi'(rho) at first 10 zeros:")
    derivs = xi_prime_at_zeros()
    for d in derivs:
        print(f"   #{d['index']:2d} gamma={d['gamma']:.6f}: "
              f"|xi'|={d['xi_prime_magnitude']:.6e}, "
              f"phase={d['xi_prime_phase_deg']:+.1f} deg, "
              f"simple={d['is_simple']}")

    all_simple = all(d['is_simple'] for d in derivs)
    mean_phase = np.mean([d['xi_prime_phase_deg'] for d in derivs])
    std_phase = np.std([d['xi_prime_phase_deg'] for d in derivs])
    print(f"   All simple: {all_simple}")
    print(f"   Mean phase: {mean_phase:+.1f} deg, std: {std_phase:.1f} deg")
    print()

    print("2. Lean ratios |xi(sigma+it)|/|xi(1-sigma+it)|:")
    ratios = lean_ratios()
    for r in ratios:
        print(f"   sigma={r['sigma']:.2f} t={r['t']:.2f}: "
              f"ratio={r['ratio']:.10f}, is_one={r['is_one']}")
    print()

    print("3. Gradient at line d/dsigma |xi|^2:")
    grads = gradient_at_line()
    for g in grads:
        print(f"   t={g['t']:.2f}: grad={g['gradient']:.4e}, "
              f"laplacian={g['laplacian']:.4e}, flat={g['flat']}")
    print()

    data = {
        'derivatives': derivs,
        'lean_ratios': ratios,
        'gradient_at_line': grads
    }
    with open('data/gap_analysis_data.json', 'w') as f:
        json.dump(data, f, indent=2, default=str)
    print("Saved to data/gap_analysis_data.json")


if __name__ == '__main__':
    run()
