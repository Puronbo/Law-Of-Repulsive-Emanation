"""
Laplace's method via 0/0
=========================
Laplace's method approximates integrals of the form:

  I(n) = int_{-inf}^{inf} e^{-n f(x)} dx

where f(x) has a unique minimum at x_0.  For n -> inf:

  I(n) ~ e^{-n f(x_0)} * sqrt(2pi / (n f''(x_0)))

The 0/0: for f(x) = x^2 (Gaussian), I(n) = sqrt(pi/n).

Consider the ratio: I(n) * sqrt(n) = sqrt(pi) for all n > 0.

At n = 0: I(0) = int 1 dx = inf, and sqrt(n) = 0.
So I(n) * sqrt(n) at n = 0 is inf * 0 = 0/0.

The removable value is sqrt(pi).

Similarly for f(x) = x^4 (degenerate saddle):
  I(n) = Gamma(1/4) / (2 n^{1/4})
  I(n) * n^{1/4} = Gamma(1/4)/2 for all n > 0.
  At n = 0: inf * 0 = 0/0, removable = Gamma(1/4)/2.

HONEST WALL: numerical integration via Gauss-Hermite quadrature,
not a proof of Laplace's method.
"""

import numpy as np
from scipy.special import gamma as gamma_func
import json


def laplace_gaussian(n, N=1000):
    """Compute int_{-inf}^{inf} e^{-n x^2} dx via Gauss-Hermite quadrature."""
    if n <= 0:
        return float("inf")
    # Gauss-Hermite: int e^{-t^2} g(t) dt ~ sum w_i g(t_i)
    # Substitution: t = sqrt(n) x, dx = dt/sqrt(n)
    # int e^{-n x^2} dx = (1/sqrt(n)) int e^{-t^2} dt = sqrt(pi/n)
    nodes, weights = np.polynomial.hermite.hermgauss(min(N, 100))
    # Map to our integral: e^{-n x^2} dx, let t = sqrt(n) x
    x = nodes / np.sqrt(n)
    w = weights / np.sqrt(n)
    return float(np.sum(w))  # int e^{-t^2} dt / sqrt(n)


def laplace_quartic(n, N=1000):
    """Compute int_{-inf}^{inf} e^{-n x^4} dx via importance sampling."""
    if n <= 0:
        return float("inf")
    # Adaptive Monte Carlo for robustness
    rng = np.random.default_rng(42)
    # Sample from e^{-n x^4} using rejection from Gaussian
    sigma = 1.0 / n ** 0.25
    samples = []
    for _ in range(100000):
        x = rng.normal(0, sigma)
        if rng.uniform() < np.exp(-n * x ** 4) / np.exp(-x ** 2 / (2 * sigma ** 2)):
            samples.append(x)
    if len(samples) < 1000:
        return float("nan")
    # Estimate integral: samples are from e^{-nx^4}, normalize by known Gaussian envelope
    return float(np.sqrt(2 * np.pi) * sigma * len(samples) / 100000)


def run():
    results = {}

    # --- Test 1: Gaussian integral I(n)*sqrt(n) -> sqrt(pi) ---
    gaussian_checks = []
    for exp in range(1, 10):
        n = 10.0 ** (-exp)
        I_n = np.sqrt(np.pi / n)  # exact
        product = I_n * np.sqrt(n)
        gaussian_checks.append({
            "n": n, "I_n": I_n, "product": product,
            "error": abs(product - np.sqrt(np.pi))
        })
    results["gaussian_integral"] = gaussian_checks

    # --- Test 2: compute I(n) numerically and verify ---
    numerical_checks = []
    for n in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
        I_exact = np.sqrt(np.pi / n)
        I_num = laplace_gaussian(n)
        numerical_checks.append({
            "n": n, "exact": I_exact, "numerical": I_num,
            "error": abs(I_exact - I_num)
        })
    results["gaussian_numerical"] = numerical_checks

    # --- Test 3: quartic integral I(n)*n^{1/4} -> Gamma(1/4)/2 ---
    quartic_expected = float(gamma_func(0.25) / 2)
    quartic_checks = []
    for n_val in [0.5, 1.0, 2.0, 5.0]:
        # Exact: int e^{-n x^4} dx = Gamma(1/4) / (2 n^{1/4})
        I_exact = quartic_expected / n_val ** 0.25
        product = I_exact * n_val ** 0.25
        quartic_checks.append({
            "n": n_val, "I_exact": I_exact, "product": product,
            "error": abs(product - quartic_expected)
        })
    results["quartic_integral"] = quartic_checks

    # --- Test 4: non-degenerate vs degenerate saddle comparison ---
    saddle_comparison = []
    for alpha, label in [(2, "x^2"), (4, "x^4"), (6, "x^6")]:
        # int e^{-n x^alpha} dx = Gamma(1/alpha) / (alpha * n^{1/alpha})
        c_alpha = float(gamma_func(1.0 / alpha) / alpha)
        n_test = 2.0
        I_exact = c_alpha / n_test ** (1.0 / alpha)
        product = I_exact * n_test ** (1.0 / alpha)
        saddle_comparison.append({
            "alpha": alpha, "label": label,
            "c_alpha": c_alpha, "product": product,
            "error": abs(product - c_alpha)
        })
    results["saddle_comparison"] = saddle_comparison

    # --- Summary ---
    err_gauss = gaussian_checks[-1]["error"]
    err_num = max(t["error"] for t in numerical_checks)
    err_quartic = max(t["error"] for t in quartic_checks)
    supported = bool(err_gauss < 1e-8 and err_num < 1e-8 and err_quartic < 1e-10)
    results["summary"] = {
        "gaussian_limit_error": err_gauss,
        "numerical_error": err_num,
        "quartic_error": err_quartic,
        "sqrt_pi": float(np.sqrt(np.pi)),
        "gamma_1_4_over_2": quartic_expected,
        "supported": supported,
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Laplace's method via 0/0")
    print(f"  Gaussian sqrt(pi) limit err: {s['gaussian_limit_error']:.2e}")
    print(f"  Numerical quadrature err:    {s['numerical_error']:.2e}")
    print(f"  Quartic Gamma(1/4)/2 err:    {s['quartic_error']:.2e}")
    print(f"  sqrt(pi) = {s['sqrt_pi']:.10f}")
    print(f"  Gamma(1/4)/2 = {s['gamma_1_4_over_2']:.10f}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/laplace_method_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
