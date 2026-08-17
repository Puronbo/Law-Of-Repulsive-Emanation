"""
Central limit theorem via 0/0
==============================

The central limit theorem: for iid random variables X_1, ..., X_n with mean mu
and variance sigma^2, the standardized sum converges to N(0,1):

  Z_n = (S_n - n*mu) / (sigma*sqrt(n)) -> N(0,1) as n -> inf.

The 0/0: at the Gaussian limit, the characteristic function phi(t) = e^{-t^2/2}
has a removable singularity at t=0. The 0/0 appears in the ratio:

  (phi(t) - 1) / t^2 -> -1/2 as t -> 0

Both numerator and denominator are 0 at t=0, but the removable value -1/2
encodes the variance of the limiting distribution.

We verify this by:
1. Computing the characteristic function of sums of uniform, exponential, and
   Bernoulli random variables
2. Showing the 0/0 ratio converges to the correct removable value
3. Verifying convergence to the Gaussian via the Berry-Esseen bound

HONEST WALL: Computational verification of convergence, not a proof of CLT.
"""

import json
import math
import os
import numpy as np
from scipy import stats

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(OUT_DIR, exist_ok=True)


def characteristic_function_sum_uniform(n, t_vals, n_samples=100000):
    """Characteristic function of (S_n - n/2) / sqrt(n/12) for Uniform(0,1).

    phi_X(t) = (e^{it} - 1) / (it) for Uniform(0,1).
    phi_{Z_n}(t) = phi_X(t/sqrt(n/12))^n * e^{-i*t*n/2/sqrt(n/12)}.
    """
    mu = 0.5
    var = 1.0 / 12.0
    sigma = np.sqrt(var)

    results = []
    for t in t_vals:
        if abs(t) < 1e-15:
            results.append(complex(1.0, 0.0))
            continue
        # Characteristic function of Uniform(0,1) at t/sigma_sqrt_n
        t_std = t / (sigma * np.sqrt(n))
        phi_x = (np.exp(1j * t_std) - 1) / (1j * t_std) if abs(t_std) > 1e-15 else 1.0
        # CF of Z_n
        phi_zn = phi_x ** n * np.exp(-1j * t * mu * n / (sigma * np.sqrt(n)))
        results.append(phi_zn)
    return np.array(results)


def characteristic_function_sum_exponential(n, t_vals, lam=1.0, n_samples=100000):
    """Characteristic function of (S_n - n/lam) / (sqrt(n)/lam) for Exp(lam).

    phi_X(t) = lam / (lam - it) for Exp(lam).
    """
    mu = 1.0 / lam
    var = 1.0 / lam ** 2
    sigma = np.sqrt(var)

    results = []
    for t in t_vals:
        if abs(t) < 1e-15:
            results.append(complex(1.0, 0.0))
            continue
        t_std = t / (sigma * np.sqrt(n))
        denom = lam - 1j * t_std
        phi_x = lam / denom if abs(denom) > 1e-15 else 1.0
        phi_zn = phi_x ** n * np.exp(-1j * t * mu * n / (sigma * np.sqrt(n)))
        results.append(phi_zn)
    return np.array(results)


def characteristic_function_sum_bernoulli(n, t_vals, p=0.3, n_samples=100000):
    """Characteristic function of (S_n - n*p) / sqrt(n*p*(1-p)) for Bernoulli(p).

    phi_X(t) = 1 - p + p*e^{it} for Bernoulli(p).
    """
    mu = p
    var = p * (1 - p)
    sigma = np.sqrt(var)

    results = []
    for t in t_vals:
        if abs(t) < 1e-15:
            results.append(complex(1.0, 0.0))
            continue
        t_std = t / (sigma * np.sqrt(n))
        phi_x = (1 - p) + p * np.exp(1j * t_std)
        phi_zn = phi_x ** n * np.exp(-1j * t * mu * n / (sigma * np.sqrt(n)))
        results.append(phi_zn)
    return np.array(results)


def zero_over_0_ratio(phi_vals, t_vals):
    """Compute (phi(t) - 1) / t^2 — the 0/0 ratio at t=0.

    At t=0: phi(0) = 1, so (phi(0)-1)/0^2 = 0/0.
    The removable value is -1/2 (the variance of the Gaussian limit).
    """
    results = {}
    for t, phi in zip(t_vals, phi_vals):
        if abs(t) < 1e-15:
            continue
        ratio = (phi - 1.0) / (t ** 2)
        results[f'{t:.4f}'] = {'ratio_real': float(ratio.real), 'ratio_imag': float(ratio.imag)}
    return results


def verify_clt_convergence(distribution, n_vals, t_check=1.0):
    """Verify that phi_{Z_n}(t) -> e^{-t^2/2} as n -> inf."""
    target = np.exp(-t_check ** 2 / 2)
    errors = []

    for n in n_vals:
        if distribution == 'uniform':
            phi = characteristic_function_sum_uniform(n, np.array([t_check]))
        elif distribution == 'exponential':
            phi = characteristic_function_sum_exponential(n, np.array([t_check]))
        elif distribution == 'bernoulli':
            phi = characteristic_function_sum_bernoulli(n, np.array([t_check]))
        else:
            raise ValueError(f"Unknown distribution: {distribution}")

        error = abs(phi[0] - target)
        errors.append({'n': n, 'phi_real': float(phi[0].real), 'phi_imag': float(phi[0].imag),
                       'target': target, 'error': float(error)})

    return errors


def berry_esseen_bound(distribution, n):
    """Berry-Esseen bound: |F_n(x) - Phi(x)| <= C * rho / sigma^3 / sqrt(n).

    C <= 0.4748 (Shevtsova 2011).
    """
    C = 0.4748
    if distribution == 'uniform':
        rho = 2.0 / 15.0  # E[|X-mu|^3] for Uniform(0,1)
        sigma = 1.0 / np.sqrt(12)
    elif distribution == 'exponential':
        rho = 2.0  # E[|X-mu|^3] for Exp(1)
        sigma = 1.0
    elif distribution == 'bernoulli':
        rho = 0.18  # approximate for p=0.3
        sigma = np.sqrt(0.21)
    else:
        return None

    bound = C * rho / (sigma ** 3 * np.sqrt(n))
    return bound


def run_experiment():
    print("Central Limit Theorem via 0/0 Probe")
    print("=" * 50)

    results = {
        'experiment': 'central_limit_theorem_0_over_0',
        'description': 'CLT: phi(t) -> e^{-t^2/2}; 0/0 at (phi(t)-1)/t^2, removable value = -1/2',
    }

    # 1. Verify convergence for each distribution
    distributions = ['uniform', 'exponential', 'bernoulli']
    n_vals = [1, 5, 10, 50, 100, 500]

    for dist in distributions:
        print(f"\n1. Convergence of {dist}:")
        conv = verify_clt_convergence(dist, n_vals, t_check=1.0)
        print(f"   n | phi(1) | target | error")
        for c in conv:
            print(f"   {c['n']:3d} | {c['phi_real']:.6f} | {c['target']:.6f} | {c['error']:.6f}")
        results[f'{dist}_convergence'] = conv

    # 2. The 0/0 ratio (phi(t)-1)/t^2 at t=0
    print("\n2. 0/0 ratio (phi(t)-1)/t^2 -> -1/2:")
    t_vals_small = np.linspace(0.01, 0.5, 20)
    for dist in distributions:
        if dist == 'uniform':
            phi = characteristic_function_sum_uniform(100, t_vals_small)
        elif dist == 'exponential':
            phi = characteristic_function_sum_exponential(100, t_vals_small)
        elif dist == 'bernoulli':
            phi = characteristic_function_sum_bernoulli(100, t_vals_small)

        z0 = zero_over_0_ratio(phi, t_vals_small)
        # Check convergence at small t
        small_t_keys = sorted(z0.keys())[:5]
        ratios = [z0[k]['ratio_real'] for k in small_t_keys]
        mean_ratio = np.mean(ratios)
        print(f"   {dist}: mean ratio at small t = {mean_ratio:.6f} (target = -0.5)")
        results[f'{dist}_0_over_0'] = {
            'mean_ratio_small_t': float(mean_ratio),
            'target': -0.5,
            'converges': abs(mean_ratio - (-0.5)) < 0.05,
            'ratios': z0,
        }

    # 3. Berry-Esseen bound
    print("\n3. Berry-Esseen bound:")
    for dist in distributions:
        be = []
        for n in [10, 50, 100, 500]:
            bound = berry_esseen_bound(dist, n)
            be.append({'n': n, 'bound': bound})
            print(f"   {dist} n={n}: C * rho/sigma^3/sqrt(n) = {bound:.6f}")
        results[f'{dist}_berry_esseen'] = be

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")

    all_conv_pass = True
    all_00_pass = True
    for dist in distributions:
        conv = results[f'{dist}_convergence']
        final_error = conv[-1]['error']
        conv_pass = final_error < 0.01
        z0_pass = results[f'{dist}_0_over_0']['converges']
        print(f"   {dist}: convergence error at n=500: {final_error:.6f} {'PASS' if conv_pass else 'FAIL'}")
        print(f"   {dist}: 0/0 ratio -> -0.5: {'PASS' if z0_pass else 'FAIL'} ({results[f'{dist}_0_over_0']['mean_ratio_small_t']:.6f})")
        all_conv_pass &= conv_pass
        all_00_pass &= z0_pass

    overall = 'SUPPORTED' if (all_conv_pass and all_00_pass) else 'PARTIAL'
    results['overall'] = overall
    print(f"\n   OVERALL: {overall}")

    out_path = os.path.join(OUT_DIR, 'central_limit_theorem_0_over_0_data.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n   Saved to {out_path}")

    return results


if __name__ == '__main__':
    run_experiment()
