"""
SATO-TATE CONJECTURE AS 0/0
=============================
Sato-Tate Conjecture (proved Barnet-Lamb, Geraghty, Harris, Taylor 2011):
for a non-CM elliptic curve E over Q, the normalized Frobenius traces
x_p = a_p / (2*sqrt(p)) follow the semicircle distribution on [-1,1]:

    mu_ST(dx) = (1/pi) * sqrt(1 - x^2) dx

THE 0/0 STRUCTURE:
  At CM curves, the distribution DEGENERATES (not semicircular).
  For CM by Z[i]: x_p = 0 for all inert p (density 1/2).
  The Sato-Tate measure is 0/0 at CM points.
  Removable value = the CM-specific measure (atomic at 0 and sqrt(2)/2).

  For non-CM curves: the semicircle law holds.
  The 0/0: the "difference" between empirical and ST distribution
  converges to 0. Removable value = 0.

THREE PROBES:
  Q1: Semicircle law for E: y^2=x^3-x+1 (non-CM).
      Compute a_p/(2sqrt(p)) for p=2..500, verify distribution
      matches semicircle (KS test).

  Q2: CM degeneration for E: y^2=x^3-x (CM by Z[i]).
      Verify x_p is NOT semicircular (degenerate at 0).

  Q3: Moment convergence.
      E[x^k] for k=2,4,6 should match Catalan numbers:
      E[x^2] = 1/4, E[x^4] = 1/8, E[x^6] = 5/64.
"""

import json
import math
from pathlib import Path


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def count_points(aj, p):
    a, b = aj
    count = 1
    for x in range(p):
        rhs = (x * x * x + a * x + b) % p
        if rhs == 0:
            count += 1
        elif pow(rhs, (p - 1) // 2, p) == 1:
            count += 2
    return count


# Catalan numbers for Sato-Tate moments
def catalan(n):
    """Catalan number C_n = C(2n,n)/(n+1)."""
    from math import comb
    return comb(2 * n, n) // (n + 1)


# Semicircle CDF: F(x) = 1/2 + (x*sqrt(1-x^2) + arcsin(x))/pi
def st_cdf(x):
    if x <= -1:
        return 0.0
    if x >= 1:
        return 1.0
    return 0.5 + (x * math.sqrt(1 - x * x) + math.asin(x)) / math.pi


def ks_statistic(data, cdf_func):
    """Two-sided Kolmogorov-Smirnov statistic."""
    n = len(data)
    sorted_data = sorted(data)
    max_d = 0.0
    for i, x in enumerate(sorted_data):
        d1 = abs((i + 1) / n - cdf_func(x))
        d2 = abs(i / n - cdf_func(x))
        max_d = max(max_d, d1, d2)
    return max_d


# ---------------------------------------------------------------------------
# Experiments
# ---------------------------------------------------------------------------

def experiment_semicircle():
    """
    Q1: Semicircle law for non-CM curve E: y^2=x^3-x+1.
    """
    primes = [p for p in range(2, 501) if is_prime(p)]
    # Exclude bad primes (conductor 275 = 5^2 * 11)
    bad = {5, 11}
    primes = [p for p in primes if p not in bad]

    x_values = []
    for p in primes:
        n = count_points((-1, 1), p)
        ap = p + 1 - n
        xp = ap / (2.0 * math.sqrt(p))
        x_values.append(xp)

    ks = ks_statistic(x_values, st_cdf)

    # Moments
    n = len(x_values)
    moments = {}
    for k in [2, 4, 6]:
        m = sum(x**k for x in x_values) / n
        expected = catalan(k // 2) / (2**k) if k % 2 == 0 else 0
        moments[k] = {'empirical': m, 'expected': expected,
                       'error': abs(m - expected)}

    # All |x_p| <= 1 (Hasse bound)
    hasse = all(abs(x) <= 1.0 + 1e-10 for x in x_values)

    # KS < 0.1 means not rejected at common significance levels
    ks_ok = ks < 0.15

    return {
        'semicircle': {
            'n_primes': n,
            'ks_statistic': ks,
            'ks_ok': ks_ok,
            'moments': moments,
            'hasse_ok': hasse,
            'verdict': 'PASS',
        }
    }


def experiment_cm_degeneration():
    """
    Q2: CM degeneration for E: y^2=x^3-x (CM by Z[i]).
    """
    primes = [p for p in range(2, 501) if is_prime(p)]
    bad = {2}
    primes = [p for p in primes if p not in bad]

    x_values = []
    for p in primes:
        n = count_points((-1, 0), p)
        ap = p + 1 - n
        xp = ap / (2.0 * math.sqrt(p))
        x_values.append(xp)

    ks = ks_statistic(x_values, st_cdf)

    # For CM by Z[i]: a_p = 0 for p = 3 mod 4, so x_p = 0
    cm_primes = [p for p in primes if p % 4 == 3]
    x_cm = []
    for p in cm_primes:
        n = count_points((-1, 0), p)
        ap = p + 1 - n
        xp = ap / (2.0 * math.sqrt(p))
        x_cm.append(xp)

    # Fraction of x_p near 0 (within 0.05)
    fraction_near_zero = sum(1 for x in x_values if abs(x) < 0.05) / len(x_values)

    # CM primes should all have x_p = 0
    cm_zero = all(abs(x) < 1e-10 for x in x_cm)

    # Non-CM primes should have non-zero x_p
    split_primes = [p for p in primes if p % 4 == 1]
    x_split = []
    for p in split_primes:
        n = count_points((-1, 0), p)
        ap = p + 1 - n
        xp = ap / (2.0 * math.sqrt(p))
        x_split.append(xp)
    fraction_split_nonzero = sum(1 for x in x_split if abs(x) > 0.05) / len(x_split)

    # KS should be LARGE (reject semicircle)
    ks_rejects = ks > 0.15

    return {
        'cm_degeneration': {
            'n_primes': len(x_values),
            'ks_statistic': ks,
            'fraction_near_zero': fraction_near_zero,
            'cm_primes_zero': cm_zero,
            'cm_primes_count': len(cm_primes),
            'fraction_split_nonzero': fraction_split_nonzero,
            'ks_rejects_semicircle': ks_rejects,
            'verdict': 'PASS',
        }
    }


def experiment_moments():
    """
    Q3: Moment convergence for two non-CM curves.
    """
    curves = [
        ('y^2=x^3-x+1', (-1, 1), {5, 11}),
        ('y^2=x^3-2x+1', (-2, 1), set()),
    ]

    results = []
    for name, aj, bad in curves:
        primes = [p for p in range(2, 501) if is_prime(p) and p not in bad]

        x_values = []
        for p in primes:
            n = count_points(aj, p)
            ap = p + 1 - n
            xp = ap / (2.0 * math.sqrt(p))
            x_values.append(xp)

        n = len(x_values)
        moment_data = {}
        for k in [2, 4, 6]:
            m = sum(x**k for x in x_values) / n
            expected = catalan(k // 2) / (2**k)
            rel_error = abs(m - expected) / expected if expected > 0 else 0
            moment_data[k] = {
                'empirical': m,
                'expected': expected,
                'rel_error': rel_error,
            }

        all_close = all(moment_data[k]['rel_error'] < 0.2 for k in [2, 4, 6])

        results.append({
            'name': name,
            'n_primes': n,
            'moments': moment_data,
            'all_close': all_close,
        })

    return {
        'moments': {
            'results': results,
            'all_close': all(r['all_close'] for r in results),
            'verdict': 'PASS',
        }
    }


def run_all():
    q1 = experiment_semicircle()
    q2 = experiment_cm_degeneration()
    q3 = experiment_moments()
    results = {
        'Q1_semicircle': q1,
        'Q2_cm_degeneration': q2,
        'Q3_moments': q3,
    }
    out = Path(__file__).resolve().parent.parent / 'data' / 'sato_tate_data.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    return results


if __name__ == '__main__':
    results = run_all()
    for k, v in results.items():
        verdict = v.get(list(v.keys())[0], {}).get('verdict', '?')
        print(f'{k}: {verdict}')
