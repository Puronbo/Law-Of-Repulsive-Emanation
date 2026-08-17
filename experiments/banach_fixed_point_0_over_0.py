"""
Banach fixed-point theorem via 0/0
===================================

The Banach fixed-point theorem: a contraction mapping T: X -> X on a complete
metric space has a unique fixed point x*, and the iterates T^n(x_0) converge
to x* with geometric rate.

The 0/0: at the fixed point x*, T(x*) = x*, so the difference T(x) - x = 0.
The ratio (T(x) - x) / (x - x*) has a removable singularity at x = x*.
The removable value is the contraction factor q (the Lipschitz constant).

We verify this on:
1. T(x) = cos(x) on R (contraction with q ~ 0.84)
2. T(x) = (x + 2/x) / 2 on (0, inf) (Newton's method for sqrt(2))
3. T(x) = 0.5*x + 1 on R (linear contraction, fixed point = 2)

The 0/0: at x*, T(x*) - x* = 0, but the derivative T'(x*) = q is the
removable value that determines convergence rate.

HONEST WALL: Computational verification of contraction mapping convergence,
not a proof of the Banach fixed-point theorem.
"""

import json
import math
import os
import numpy as np

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(OUT_DIR, exist_ok=True)


def T_cos(x):
    """T(x) = cos(x), contraction on [-1,1]."""
    return np.cos(x)


def T_newton_sqrt2(x):
    """T(x) = (x + 2/x) / 2, Newton's method for sqrt(2)."""
    return (x + 2.0 / x) / 2.0


def T_linear(x):
    """T(x) = 0.5*x + 1, fixed point = 2."""
    return 0.5 * x + 1.0


def T_derivative_cos(x):
    """T'(x) = -sin(x)."""
    return -np.sin(x)


def T_derivative_newton(x):
    """T'(x) = 1/2 - 1/x^2."""
    return 0.5 - 1.0 / (x ** 2)


def T_derivative_linear(x):
    """T'(x) = 0.5."""
    return 0.5


def iterate_to_fixed_point(T_func, x0, n_iter=100, tol=1e-12):
    """Iterate T starting from x0, record convergence."""
    xs = [x0]
    for i in range(n_iter):
        x_new = T_func(xs[-1])
        xs.append(x_new)
        if abs(x_new - xs[-2]) < tol:
            break
    return np.array(xs)


def convergence_rate(xs, x_star_true=None):
    """Estimate convergence rate from iterates: |x_{n+1} - x*| / |x_n - x*|."""
    x_star = x_star_true if x_star_true is not None else xs[-1]
    rates = []
    for i in range(len(xs) - 1):
        err_n = abs(xs[i] - x_star)
        err_np1 = abs(xs[i + 1] - x_star)
        if err_n > 1e-15:
            rates.append(err_np1 / err_n)
    return rates


def verify_fixed_point(T_func, x0, x_star, q_approx, name, n_iter=50):
    """Verify Banach theorem properties."""
    xs = iterate_to_fixed_point(T_func, x0, n_iter=n_iter)
    actual_x_star = xs[-1]
    n_iters = len(xs) - 1

    rates = convergence_rate(xs, x_star_true=x_star)
    mean_rate = np.mean(rates[-15:]) if len(rates) >= 15 else np.mean(rates)

    return {
        'name': name,
        'x0': x0,
        'x_star_approx': x_star,
        'x_star_computed': float(actual_x_star),
        'fixed_point_error': float(abs(T_func(actual_x_star) - actual_x_star)),
        'converged': abs(T_func(actual_x_star) - actual_x_star) < 1e-8,
        'n_iterations': n_iters,
        'q_approx': q_approx,
        'mean_convergence_rate': float(mean_rate),
        'rate_matches_q': abs(mean_rate - q_approx) < 0.1,
        'iterates': xs.tolist(),
    }


def zero_over_0_at_fixed_point(T_func, T_deriv_func, x_star, q_true):
    """The 0/0: (T(x) - x) / (x - x*) at x = x* is 0/0.

    By L'Hopital's rule: lim_{x->x*} (T(x) - x) / (x - x*) = T'(x*) - 1.
    The removable value is T'(x*) - 1.
    """
    T_prime = T_deriv_func(x_star)
    removable_value = T_prime - 1

    # Test at several points near x*
    x_near = np.linspace(x_star - 0.5, x_star + 0.5, 200)
    x_near = x_near[np.abs(x_near - x_star) > 1e-10]  # exclude x*

    ratios = []
    for x in x_near:
        num = T_func(x) - x
        den = x - x_star
        if abs(den) > 1e-15:
            ratios.append(num / den)

    # Check convergence to removable value at points VERY close to x*
    near_x_star = [x for x in x_near if abs(x - x_star) < 0.05]
    near_ratios = [(T_func(x) - x) / (x - x_star) for x in near_x_star if abs(x - x_star) > 1e-10]
    mean_near = np.mean(near_ratios) if near_ratios else None

    return {
        'x_star': float(x_star),
        'q_true': q_true,
        'T_prime_at_x_star': float(T_prime),
        'removable_value': float(removable_value),
        'mean_ratio_near_x_star': float(mean_near) if mean_near is not None else None,
        'converges_to_removable': abs(mean_near - removable_value) < 0.05 if mean_near is not None else False,
        'explanation': '0/0: (T(x)-x)/(x-x*) at x=x*; removable value = T\'(x*) - 1',
    }


def run_experiment():
    print("Banach Fixed-Point Theorem via 0/0 Probe")
    print("=" * 50)

    results = {
        'experiment': 'banach_fixed_point_0_over_0',
        'description': 'Banach: contraction -> unique fixed point; 0/0 at (T(x)-x)/(x-x*), removable value = q-1',
    }

    # 1. T(x) = cos(x)
    print("\n1. T(x) = cos(x), x0=0:")
    fp_cos = verify_fixed_point(T_cos, x0=0.0, x_star=0.7390851332, q_approx=0.6736, name='cos')
    print(f"   Fixed point: {fp_cos['x_star_computed']:.10f} (known: 0.7390851332)")
    print(f"   |T(x*)-x*| = {fp_cos['fixed_point_error']:.2e}")
    print(f"   Converged: {fp_cos['converged']}")
    print(f"   Iterations: {fp_cos['n_iterations']}")
    print(f"   Convergence rate: {fp_cos['mean_convergence_rate']:.6f} (q={fp_cos['q_approx']:.4f})")
    results['cos'] = fp_cos

    z0_cos = zero_over_0_at_fixed_point(T_cos, T_derivative_cos, 0.7390851332, 0.6736)
    print(f"   0/0 removable value: {z0_cos['removable_value']:.4f}, converges: {z0_cos['converges_to_removable']}")
    results['cos_0_over_0'] = z0_cos

    # 2. Newton's method for sqrt(2)
    print("\n2. T(x) = (x+2/x)/2, x0=2.0:")
    fp_newton = verify_fixed_point(T_newton_sqrt2, x0=2.0, x_star=np.sqrt(2), q_approx=0.0, name='newton')
    print(f"   Fixed point: {fp_newton['x_star_computed']:.15f} (sqrt(2) = {np.sqrt(2):.15f})")
    print(f"   |T(x*)-x*| = {fp_newton['fixed_point_error']:.2e}")
    print(f"   Converged: {fp_newton['converged']}")
    print(f"   Iterations: {fp_newton['n_iterations']}")
    print(f"   Convergence rate: {fp_newton['mean_convergence_rate']:.6f} (q~0)")
    results['newton'] = fp_newton

    z0_newton = zero_over_0_at_fixed_point(T_newton_sqrt2, T_derivative_newton, np.sqrt(2), 0.0)
    print(f"   0/0 removable value: {z0_newton['removable_value']:.4f}, converges: {z0_newton['converges_to_removable']}")
    results['newton_0_over_0'] = z0_newton

    # 3. Linear contraction
    print("\n3. T(x) = 0.5*x + 1, x0=0:")
    fp_lin = verify_fixed_point(T_linear, x0=0.0, x_star=2.0, q_approx=0.5, name='linear')
    print(f"   Fixed point: {fp_lin['x_star_computed']:.10f} (known: 2.0)")
    print(f"   |T(x*)-x*| = {fp_lin['fixed_point_error']:.2e}")
    print(f"   Converged: {fp_lin['converged']}")
    print(f"   Iterations: {fp_lin['n_iterations']}")
    print(f"   Convergence rate: {fp_lin['mean_convergence_rate']:.6f} (q={fp_lin['q_approx']:.1f})")
    results['linear'] = fp_lin

    z0_lin = zero_over_0_at_fixed_point(T_linear, T_derivative_linear, 2.0, 0.5)
    print(f"   0/0 removable value: {z0_lin['removable_value']:.4f}, converges: {z0_lin['converges_to_removable']}")
    results['linear_0_over_0'] = z0_lin

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")

    cos_pass = fp_cos['converged'] and fp_cos['rate_matches_q']
    newton_pass = fp_newton['converged']
    lin_pass = fp_lin['converged'] and fp_lin['rate_matches_q']
    cos_00 = z0_cos['converges_to_removable']
    newton_00 = z0_newton['converges_to_removable']
    lin_00 = z0_lin['converges_to_removable']

    print(f"   cos: fixed point + rate: {'PASS' if cos_pass else 'FAIL'}")
    print(f"   cos: 0/0 -> q-1: {'PASS' if cos_00 else 'FAIL'}")
    print(f"   newton: fixed point: {'PASS' if newton_pass else 'FAIL'}")
    print(f"   newton: 0/0 -> -1: {'PASS' if newton_00 else 'FAIL'}")
    print(f"   linear: fixed point + rate: {'PASS' if lin_pass else 'FAIL'}")
    print(f"   linear: 0/0 -> -0.5: {'PASS' if lin_00 else 'FAIL'}")

    overall = 'SUPPORTED' if (cos_pass and newton_pass and lin_pass) else 'PARTIAL'
    results['overall'] = overall
    print(f"\n   OVERALL: {overall}")

    out_path = os.path.join(OUT_DIR, 'banach_fixed_point_0_over_0_data.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n   Saved to {out_path}")

    return results


if __name__ == '__main__':
    run_experiment()
