"""
Phragmen-Lindelof Analysis of xi(s) in the Critical Strip
=========================================================
"""

import numpy as np
from mpmath import mp, zeta, gamma, pi, fabs, mpc, power, log as mplog
import json

mp.dps = 30


def xi(s):
    return mp.mpf('0.5') * s * (s - 1) * power(pi, -s/2) * gamma(s/2) * zeta(s)


def verify_stirling_bound():
    """Verify exponential growth: |xi| <= e^{C|t|} for some C."""
    results = []
    for t in [10, 20, 50, 100, 200, 500]:
        val = xi(mpc(0.5, t))
        mag = float(fabs(val))
        log_mag = np.log(mag + 1e-300)
        ratio = log_mag / t if t > 0 else 0
        results.append({
            't': t,
            'actual': mag,
            'log_mag': log_mag,
            'log_mag_over_t': ratio,
            'is_exponential': ratio < 1.0
        })
    return results


def boundary_analysis():
    """Compute |xi| on the three boundary lines."""
    results = {'sigma_zero': [], 'sigma_half': [], 'sigma_one': []}

    for t in [5, 10, 15, 20, 30, 50, 80, 100]:
        for sigma_key, sigma_val in [('sigma_zero', 0.0), ('sigma_half', 0.5), ('sigma_one', 1.0)]:
            try:
                val = xi(mpc(sigma_val, t))
                mag = float(fabs(val))
                results[sigma_key].append({
                    't': t,
                    'magnitude': mag
                })
            except Exception as e:
                results[sigma_key].append({
                    't': t,
                    'magnitude': None,
                    'error': str(e)
                })

    summary = {}
    for key in results:
        mags = [r['magnitude'] for r in results[key] if r['magnitude'] is not None]
        if mags:
            summary[key] = {
                'max': max(mags),
                'min': min(mags),
                'decays': mags[-1] < mags[0],
                'points': results[key]
            }
        else:
            summary[key] = {'points': results[key]}

    return summary


def verify_hermite_biehler():
    """Verify |xi(sigma+it)| = |xi(sigma-it)| numerically."""
    results = []
    for t in [10, 20, 30, 50, 80]:
        for sigma in [0.1, 0.2, 0.3, 0.4, 0.45]:
            try:
                left = xi(mpc(sigma, t))
                right = xi(mpc(sigma, -t))
                ml = float(fabs(left))
                mr = float(fabs(right))
                diff = abs(ml - mr)
                rel = diff / max(ml, 1e-30)
                results.append({
                    'sigma': sigma, 't': t,
                    'mag_plus': ml, 'mag_minus': mr,
                    'abs_diff': diff, 'rel_diff': rel
                })
            except:
                pass

    if results:
        max_rel = max(r['rel_diff'] for r in results)
    else:
        max_rel = None

    return {'points': results, 'max_relative_diff': max_rel}


def verify_functional_eq_symmetry():
    """Verify |xi(sigma+it)| = |xi(1-sigma+it)| numerically."""
    results = []
    for t in [10, 20, 30, 50, 80]:
        for sigma in [0.1, 0.2, 0.3, 0.4, 0.45]:
            try:
                left = xi(mpc(sigma, t))
                right = xi(mpc(1 - sigma, t))
                ml = float(fabs(left))
                mr = float(fabs(right))
                diff = abs(ml - mr)
                rel = diff / max(ml, 1e-30)
                results.append({
                    'sigma': sigma, 't': t,
                    'mag_left': ml, 'mag_right': mr,
                    'abs_diff': diff, 'rel_diff': rel
                })
            except:
                pass

    if results:
        max_rel = max(r['rel_diff'] for r in results)
    else:
        max_rel = None

    return {'points': results, 'max_relative_diff': max_rel}


def verify_zeros_on_line():
    """Verify first 10 zeros are on the critical line."""
    known = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
             37.586178, 40.918719, 43.327073, 48.005151, 49.773832]
    results = []
    for i, gamma in enumerate(known):
        try:
            val = xi(mpc(0.5, gamma))
            mag = float(fabs(val))
            results.append({
                'index': i + 1, 'gamma': gamma,
                'magnitude': mag,
                'on_line': mag < 1e-10
            })
        except:
            pass
    return results


def run_analysis():
    print("=== Phragmen-Lindelof Analysis of xi(s) ===\n")

    print("Step 1: Exponential growth (log|xi|/t bounded)")
    stirling = verify_stirling_bound()
    for r in stirling:
        print(f"  t={r['t']:4.0f}: log|xi|={r['log_mag']:+.2f}, log|xi|/t={r['log_mag_over_t']:.4f}")
    print()

    print("Step 2: Boundary values (|xi| on Re(s) = 0, 1/2, 1)")
    boundary = boundary_analysis()
    for key in ['sigma_zero', 'sigma_half', 'sigma_one']:
        if key in boundary and 'max' in boundary[key]:
            b = boundary[key]
            print(f"  {key}: max={b['max']:.4e}, min={b['min']:.4e}, decays={b['decays']}")
        else:
            print(f"  {key}: no data")
    print()

    print("Step 3: Hermite-Biehler symmetry |xi(sigma+it)| = |xi(sigma-it)|")
    hb = verify_hermite_biehler()
    if hb['max_relative_diff'] is not None:
        print(f"  Max relative difference: {hb['max_relative_diff']:.2e}")
        print(f"  Equality holds: {hb['max_relative_diff'] < 1e-10}")
    else:
        print("  No data")
    print()

    print("Step 4: Functional equation symmetry |xi(sigma+it)| = |xi(1-sigma+it)|")
    fe = verify_functional_eq_symmetry()
    if fe['max_relative_diff'] is not None:
        print(f"  Max relative difference: {fe['max_relative_diff']:.2e}")
        print(f"  Equality holds: {fe['max_relative_diff'] < 1e-10}")
    else:
        print("  No data")
    print()

    print("Step 5: First 10 zeros on the critical line")
    zeros = verify_zeros_on_line()
    for z in zeros:
        print(f"  gamma_{z['index']:2d} = {z['gamma']:.6f}: |xi| = {z['magnitude']:.2e}, on_line = {z['on_line']}")
    print()

    data = {
        'stirling': stirling,
        'boundary': boundary,
        'hermite_biehler': hb,
        'functional_eq': fe,
        'zeros': zeros
    }

    with open('data/phragmen_lindelof_data.json', 'w') as f:
        json.dump(data, f, indent=2, default=str)

    print("Data saved to data/phragmen_lindelof_data.json")
    return data


if __name__ == '__main__':
    run_analysis()
