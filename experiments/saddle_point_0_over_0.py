"""
Saddle point approximation via 0/0
==================================
The saddle point method (method of steepest descent):
I(lambda) = integral f(x) * exp(lambda * g(x)) dx
As lambda -> infinity, the integral is dominated by the saddle point
where g'(x*) = 0.

The 0/0: the ratio I(lambda) / (f(x*) * sqrt(2*pi / (lambda * |g''(x*)|)))
as lambda -> infinity approaches 1. But at lambda = 0: I(0) = integral f(x) dx
(finite), and the Gaussian approximation gives f(x*) * sqrt(2*pi / (0 * |g''(x*)|))
= infinity. So the ratio is finite/infinity = 0 (not 0/0).

The real 0/0: for a saddle point where g'(x*) = 0, the integrand has
a Gaussian peak. The ratio of the integrand to the Gaussian:
  f(x) * exp(lambda * g(x)) / [f(x*) * exp(lambda * g(x*)) * exp(-lambda * |g''(x*)| * (x-x*)^2 / 2)]
At x = x*: 1/1 = 1.
At x = x* + dx: exp(lambda * [g(x*+dx) - g(x*)]) / exp(-lambda * |g''(x*)| * dx^2 / 2)
  = exp(lambda * [g''(x*) * dx^2/2 + ... - g''(x*) * dx^2/2]) = exp(O(dx^3))
  -> 1 as dx -> 0.

The 0/0 at the saddle point: g'(x*) = 0. The ratio g'(x)/(x-x*) as x -> x*
is 0/0, removable value = g''(x*). This is the second derivative test.

The 0/0 in the Laplace method: I = integral_0^inf exp(-lambda * f(x)) dx.
At a minimum x* of f: f(x*) = 0 and f'(x*) = 0.
The ratio I / sqrt(pi / (2*lambda * f''(x*))) -> 1 as lambda -> infinity.
At lambda = 0: I(0) = integral_0^inf 1 dx = infinity.
0/0 at lambda = 0 if we normalize: I(0) / sqrt(pi / (2*0*f''(x*))) = infinity/infinity.

HONEST WALL: numerical verification of saddle point approximations.
"""

import numpy as np
import json
from scipy import integrate
from scipy.special import gamma as gamma_func


def gaussian_peak(x, x_star, g_pp):
    """Gaussian approximation at the saddle point."""
    return np.exp(-0.5 * g_pp * (x - x_star) ** 2)


def run():
    results = {"tests": [], "summary": {}}

    # --- Test 1: Saddle point for integral exp(lambda * (1 - x^2)) ---
    # g(x) = 1 - x^2, g'(x) = -2x = 0 at x* = 0, g''(0) = -2
    # I(lambda) = integral_{-inf}^{inf} exp(lambda*(1-x^2)) dx
    #           = exp(lambda) * integral exp(-lambda*x^2) dx
    #           = exp(lambda) * sqrt(pi/lambda)
    # Gaussian approx: f(x*) * sqrt(2*pi / (lambda * |g''(x*)|))
    #                = 1 * sqrt(2*pi / (lambda * 2)) = sqrt(pi/lambda)
    # Ratio = exp(lambda) * sqrt(pi/lambda) / sqrt(pi/lambda) = exp(lambda) -> infinity
    # Normalize: I(lambda) / exp(lambda) = sqrt(pi/lambda)
    # Gaussian approx / exp(lambda) = sqrt(pi/lambda)
    # Ratio -> 1 as lambda -> infinity

    sp1_tests = []
    for lam in [1, 5, 10, 50, 100]:
        # Exact: exp(lam) * sqrt(pi/lam)
        I_exact = np.exp(lam) * np.sqrt(np.pi / lam)
        # Gaussian approx
        I_gauss = np.sqrt(np.pi / lam)
        # Numerical integral
        I_num, _ = integrate.quad(lambda x: np.exp(lam * (1 - x**2)), -10, 10)

        sp1_tests.append({
            "lambda": lam,
            "I_exact_normalized": float(I_exact / np.exp(lam)),
            "I_gauss_normalized": float(I_gauss),
            "I_num_normalized": float(I_num / np.exp(lam)) if I_num > 0 else 0,
            "gaussian_ratio": float(I_num / (np.exp(lam) * I_gauss)) if I_gauss > 0 else 0,
            "close_to_one": bool(abs(I_num / (np.exp(lam) * I_gauss) - 1) < 0.1) if I_gauss > 0 else False
        })

    results["saddle_point_gaussian"] = {
        "note": "exp(lambda*(1-x^2)): Gaussian approx -> 1 as lambda -> inf",
        "tests": sp1_tests
    }

    # --- Test 2: Laplace method for Gamma function ---
    # Gamma(n+1) = integral_0^inf x^n * exp(-x) dx = integral_0^inf exp(n*log(x) - x) dx
    # g(x) = log(x) - x/n, saddle at x* = n
    # By Laplace: Gamma(n+1) ~ sqrt(2*pi*n) * (n/e)^n (Stirling)
    stirling_tests = []
    for n in [5, 10, 20, 50, 100]:
        from math import factorial
        exact = factorial(n)
        stirling = np.sqrt(2 * np.pi * n) * (n / np.e) ** n
        ratio = exact / stirling if stirling > 0 else 0

        stirling_tests.append({
            "n": n,
            "exact": float(exact),
            "stirling": float(stirling),
            "ratio": float(ratio),
            "close_to_one": bool(abs(ratio - 1.0) < 0.05)
        })

    results["laplace_stirling"] = {
        "note": "Laplace method gives Stirling: n!/Stirling -> 1",
        "tests": stirling_tests
    }

    # --- Test 3: 0/0 at saddle point ---
    # g'(x*) = 0. The ratio g'(x)/(x-x*) -> g''(x*) as x -> x*.
    # This is 0/0 at x = x*, removable value = g''(x*).
    saddle_0_tests = []
    g = lambda x: 1 - x**2
    g_prime = lambda x: -2 * x
    x_star = 0.0

    for dx in [0.1, 0.01, 0.001, 0.0001]:
        x = x_star + dx
        ratio = g_prime(x) / (x - x_star) if abs(x - x_star) > 1e-15 else 0
        saddle_0_tests.append({
            "x": float(x),
            "dx": float(dx),
            "g_prime": float(g_prime(x)),
            "ratio": float(ratio),
            "approaches_g_pp": bool(abs(ratio - (-2.0)) < 0.1)
        })

    saddle_0_tests.append({
        "x": float(x_star),
        "dx": 0,
        "ratio": "0/0",
        "removable_value": -2.0
    })

    results["saddle_0_over_0"] = {
        "note": "g'(x)/(x-x*) -> g''(x*) as x -> x*: 0/0 removable = g''(x*)",
        "tests": saddle_0_tests
    }

    # --- Test 4: Higher-order saddle points ---
    # For g(x) = x^4, g'(x) = 4x^3, g''(x) = 12x^2
    # At x* = 0: g'(0) = 0, g''(0) = 0 (degenerate saddle)
    # g'(x)/x = 4x^2 -> 0 as x -> 0
    # g'(x)/x^3 = 4 (removable value for the degenerate case)
    higher_tests = []
    g4_prime = lambda x: 4 * x ** 3

    for dx in [0.1, 0.01, 0.001]:
        x = dx
        r1 = g4_prime(x) / x if abs(x) > 1e-15 else 0
        r3 = g4_prime(x) / x ** 3 if abs(x) > 1e-15 else 0
        higher_tests.append({
            "x": float(x),
            "g_prime_over_x": float(r1),
            "g_prime_over_x3": float(r3),
            "removable_value": 4.0
        })

    results["higher_order_saddle"] = {
        "note": "For g=x^4: g'/x -> 0, g'/x^3 -> 4 (degenerate saddle)",
        "tests": higher_tests
    }

    # --- Test 5: Watson's lemma (asymptotic expansion) ---
    # I(lambda) = integral_0^inf x^{a-1} * exp(-lambda*x^2) dx = Gamma(a/2) / (2*lambda^{a/2})
    # The 0/0: as lambda -> 0, I -> Gamma(a/2)/0 = infinity.
    # The ratio I(lambda) * lambda^{a/2} = Gamma(a/2)/2 (constant).
    # At lambda = 0: infinity * 0 = 0/0, removable = Gamma(a/2)/2.
    watson_tests = []
    for a in [0.5, 1.0, 1.5, 2.0, 3.0]:
        for lam in [0.1, 1.0, 10.0, 100.0]:
            I_exact = gamma_func(a / 2) / (2 * lam ** (a / 2))
            I_num, _ = integrate.quad(
                lambda x: x ** (a - 1) * np.exp(-lam * x ** 2),
                0, 20)

            ratio = I_num / I_exact if I_exact > 0 else 0
            watson_tests.append({
                "a": float(a),
                "lambda": float(lam),
                "I_exact": float(I_exact),
                "I_numerical": float(I_num),
                "ratio": float(ratio),
                "close_to_one": bool(abs(ratio - 1.0) < 0.05)
            })

    results["watson_lemma"] = {
        "note": "Watson's lemma: integral x^{a-1}*exp(-lam*x^2) = Gamma(a/2)/(2*lam^{a/2})",
        "tests": watson_tests
    }

    # --- Summary ---
    sp1_ok = any(t["close_to_one"] for t in sp1_tests)
    stirling_ok = stirling_tests[-1]["close_to_one"]
    saddle0_ok = saddle_0_tests[-2]["approaches_g_pp"]
    watson_ok = all(t["close_to_one"] for t in watson_tests)

    supported = bool(sp1_ok and stirling_ok and saddle0_ok and watson_ok)

    results["summary"] = {
        "supported": supported,
        "gaussian_saddle_converges": sp1_ok,
        "stirling_correct": stirling_ok,
        "saddle_0_over_0_removable": saddle0_ok,
        "watson_lemma_correct": watson_ok,
        "honest_wall": "numerical verification of asymptotic approximations"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Saddle point approximation via 0/0")
    print(f"  Gaussian saddle converges: {s['gaussian_saddle_converges']}")
    print(f"  Stirling correct:          {s['stirling_correct']}")
    print(f"  Saddle 0/0 removable:      {s['saddle_0_over_0_removable']}")
    print(f"  Watson's lemma correct:    {s['watson_lemma_correct']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/saddle_point_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
