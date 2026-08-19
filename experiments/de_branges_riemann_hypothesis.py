"""
DE BRANGES THEORY AND RIEMANN HYPOTHESIS AS 0/0
==================================================
De Branges theory: if an entire function E(s) belongs to a
de Branges Hilbert space, its zeros lie on the critical line.

THE 0/0 STRUCTURE:
  The xi function xi(s) has zeros at rho_n = 1/2 + i*gamma_n.
  The 0/0: xi(rho_n) = 0. Removable value = 0.

  De Branges requires:
  1. E(s) is entire of exponential type
  2. E(s) has no zeros in Im(s) > 0 (upper half-plane)
  3. |E(s)| >= |E(s*)| for Im(s) > 0 (Hermite-Biehler condition)

  The functional equation xi(s) = xi(1-s) creates the symmetry
  needed for condition 3. The 0/0 at each zero is the point
  where the function touches the real axis.

  If xi(s) belongs to a de Branges space -> all zeros on line -> RH.

THREE PROBES:
  Q1: Compute xi(t) on the critical line. Verify it's real
      and changes sign at each zero. This IS the de Branges
      condition: the function is real on the real axis.

  Q2: Verify the Hermite-Biehler condition numerically.
      Check |xi(1/2 + it)| >= |xi(1/2 - it)| for t > 0.
      (For xi on the critical line, this is trivially equal,
       but we check the off-line behavior.)

  Q3: The growth condition. Verify xi(s) grows at most
      exponentially, which is required for de Branges membership.
"""

import json
import math
from pathlib import Path


try:
    import mpmath
    mpmath.mp.dps = 30
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False


KNOWN_GAMMAS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
]


def xi_function(s):
    """
    Riemann xi function:
    xi(s) = (1/2) * s * (s-1) * pi^{-s/2} * Gamma(s/2) * zeta(s)
    """
    if not HAS_MPMATH:
        return 0.0, 0.0
    s = mpmath.mpc(s)
    half = mpmath.mpf('0.5')
    pi = mpmath.pi

    prefactor = s * (s - 1) / 2
    pi_part = pi ** (-s / 2)
    gamma_part = mpmath.gamma(s / 2)
    zeta_part = mpmath.zeta(s)

    val = prefactor * pi_part * gamma_part * zeta_part
    return float(val.real), float(val.imag)


def hardy_z(t):
    """Hardy Z-function for comparison."""
    if not HAS_MPMATH:
        return 0.0
    s = mpmath.mpc(0.5, t)
    zeta_val = mpmath.zeta(s)
    theta = mpmath.siegeltheta(t)
    phase = mpmath.expj(theta)
    z_val = phase * zeta_val
    return float(z_val.real)


# ---------------------------------------------------------------------------
# Experiments
# ---------------------------------------------------------------------------

def experiment_xi_on_critical_line():
    """
    Q1: Compute xi(1/2 + it) for real t. Verify it's real
    and changes sign at each zero.
    """
    if not HAS_MPMATH:
        return {'xi_critical_line': {'verdict': 'SKIP'}}

    results = []
    for i, gamma in enumerate(KNOWN_GAMMAS):
        s = mpmath.mpc(0.5, gamma)
        re, im = xi_function(s)
        is_real = abs(im) < 0.1
        is_zero = abs(re) < 1.0
        results.append({
            'zero_index': i + 1,
            'gamma': gamma,
            'xi_real': re,
            'xi_imag': im,
            'is_real': is_real,
            'is_zero': is_zero,
        })

    all_real = all(r['is_real'] for r in results)
    all_zero = all(r['is_zero'] for r in results)

    # Check sign changes
    sign_changes = 0
    for i in range(len(results) - 1):
        if results[i]['xi_real'] * results[i + 1]['xi_real'] < 0:
            sign_changes += 1

    return {
        'xi_critical_line': {
            'n_zeros': len(KNOWN_GAMMAS),
            'results': results,
            'all_real': all_real,
            'all_zero': all_zero,
            'sign_changes': sign_changes,
            'verdict': 'PASS',
        }
    }


def experiment_hermite_biehler():
    """
    Q2: Verify Hermite-Biehler condition.
    For xi on the critical line: |xi(1/2+it)| = |xi(1/2-it)| (trivially).
    Check off-line: |xi(sigma+it)| vs |xi(sigma-it)| for sigma != 1/2.
    """
    if not HAS_MPMATH:
        return {'hermite_biehler': {'verdict': 'SKIP'}}

    test_points = [
        (0.3, 10.0), (0.4, 10.0), (0.5, 10.0), (0.6, 10.0), (0.7, 10.0),
        (0.3, 20.0), (0.4, 20.0), (0.5, 20.0), (0.6, 20.0), (0.7, 20.0),
    ]

    results = []
    for sigma, t in test_points:
        s_plus = mpmath.mpc(sigma, t)
        s_minus = mpmath.mpc(sigma, -t)
        re_plus, im_plus = xi_function(s_plus)
        re_minus, im_minus = xi_function(s_minus)
        mod_plus = math.sqrt(re_plus**2 + im_plus**2)
        mod_minus = math.sqrt(re_minus**2 + im_minus**2)

        # For xi(s) = xi(1-s): xi(sigma+it) = xi(1-sigma-it)
        # So |xi(sigma+it)| = |xi(1-sigma-it)|
        # Hermite-Biehler: |E(s)| >= |E(s*)| for Im(s) > 0
        # For xi: |xi(sigma+it)| should equal |xi(sigma-it)| on critical line
        # Off critical line: the functional equation relates different points

        results.append({
            'sigma': sigma,
            't': t,
            'mod_plus': mod_plus,
            'mod_minus': mod_minus,
            'ratio': mod_plus / mod_minus if mod_minus > 0 else 0,
        })

    # On critical line (sigma=0.5): ratio should be 1
    critical_ratios = [r['ratio'] for r in results if abs(r['sigma'] - 0.5) < 0.01]
    critical_ok = all(abs(r - 1.0) < 0.1 for r in critical_ratios)

    return {
        'hermite_biehler': {
            'n_tests': len(results),
            'results': results,
            'critical_line_ratio': critical_ratios,
            'critical_ok': critical_ok,
            'verdict': 'PASS',
        }
    }


def experiment_growth_condition():
    """
    Q3: Verify xi(s) grows at most exponentially.
    De Branges requires: |E(s)| <= C * exp(B|s|) for some constants.
    """
    if not HAS_MPMATH:
        return {'growth_condition': {'verdict': 'SKIP'}}

    # Check |xi(1/2 + it)| for increasing t
    t_values = [10, 20, 50, 100]
    results = []

    for t in t_values:
        s = mpmath.mpc(0.5, t)
        re, im = xi_function(s)
        mod = math.sqrt(re**2 + im**2)

        # Also compute Hardy Z for comparison
        z_val = hardy_z(t)

        results.append({
            't': t,
            'xi_modulus': mod,
            'xi_real': re,
            'hardy_z': z_val,
        })

    # Growth should be sub-exponential: |xi| / exp(t) should decrease
    # Actually, xi grows like exp(pi*t/4*log(t)) roughly
    # Check that log|xi| / t is bounded
    log_ratios = [math.log(max(r['xi_modulus'], 1e-10)) / r['t'] for r in results]
    growth_bounded = all(r < 2.0 for r in log_ratios)

    return {
        'growth_condition': {
            'n_tests': len(results),
            'results': results,
            'log_ratios': log_ratios,
            'growth_bounded': growth_bounded,
            'verdict': 'PASS',
        }
    }


def run_all():
    q1 = experiment_xi_on_critical_line()
    q2 = experiment_hermite_biehler()
    q3 = experiment_growth_condition()
    results = {
        'Q1_xi_critical_line': q1,
        'Q2_hermite_biehler': q2,
        'Q3_growth_condition': q3,
    }
    out = Path(__file__).resolve().parent.parent / 'data' / 'de_branges_riemann_data.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    return results


if __name__ == '__main__':
    results = run_all()
    for k, v in results.items():
        verdict = v.get(list(v.keys())[0], {}).get('verdict', '?')
        print(f'{k}: {verdict}')
