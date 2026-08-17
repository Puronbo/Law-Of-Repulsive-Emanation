"""
Poisson summation via 0/0
=========================
The Poisson summation formula equates a sum over integers to a sum over
dual integers:

  sum_{n} f(n) = sum_{k} f_hat(k)

For f(x) = e^{-pi s x^2}, this gives the theta functional equation:

  theta(s) = s^{-1/2} theta(1/s)

equivalently, the completed zeta function satisfies xi(s) = xi(1-s), where:

  xi(s) = 0.5 * s * (s-1) * pi^{-s/2} * Gamma(s/2) * Zeta(s)

The 0/0: at s=0, xi(s) involves:
  - s*(s-1) = 0 (vanishes)
  - Gamma(s/2) has a pole (diverges)
  - Zeta(0) = -0.5 (finite)
  -> Product: 0 * inf * (-0.5) = 0/0

The removable value is 1/2. Similarly at s=1.

HONEST WALL: numerical verification of the removable singularity, not a
proof of the functional equation or Poisson summation.
"""

import numpy as np
from scipy.special import gamma as gamma_func
from mpmath import zeta as zeta_func, mpf
import json


def completed_zeta(s):
    """Compute xi(s) = 0.5 * s * (s-1) * pi^{-s/2} * Gamma(s/2) * Zeta(s).

    At s=0 and s=1 the formula is 0/0; the removable value is 0.5.
    """
    if abs(s) < 1e-12:
        return 0.5
    if abs(s - 1) < 1e-12:
        return 0.5
    z = float(zeta_func(mpf(s)))
    g = float(gamma_func(s / 2.0))
    return 0.5 * s * (s - 1) * np.pi ** (-s / 2.0) * g * z


def theta_function(s, N=500):
    """Theta(s) = sum_{n=-N}^{N} e^{-pi s n^2}."""
    ns = np.arange(-N, N + 1)
    return float(np.sum(np.exp(-np.pi * s * ns ** 2)))


def run():
    results = {}

    # --- Test 1: xi(s) convergence near s=0 ---
    convergences_0 = []
    for exp in range(1, 8):
        s = 10.0 ** (-exp)
        xi_s = completed_zeta(s)
        convergences_0.append({"s": s, "xi": xi_s, "error": abs(xi_s - 0.5)})
    results["xi_near_0"] = convergences_0

    # --- Test 2: xi(s) convergence near s=1 ---
    convergences_1 = []
    for exp in range(1, 8):
        s = 1.0 - 10.0 ** (-exp)
        xi_s = completed_zeta(s)
        convergences_1.append({"s": s, "xi": xi_s, "error": abs(xi_s - 0.5)})
    results["xi_near_1"] = convergences_1

    # --- Test 3: functional equation xi(s) = xi(1-s) ---
    fe_checks = []
    for s in [0.15, 0.25, 0.35, 0.45, 0.55]:
        xi_s = completed_zeta(s)
        xi_1ms = completed_zeta(1 - s)
        fe_checks.append({
            "s": s, "xi_s": xi_s, "xi_1ms": xi_1ms,
            "diff": abs(xi_s - xi_1ms)
        })
    results["functional_equation"] = fe_checks

    # --- Test 4: theta functional equation theta(s) = s^{-1/2} theta(1/s) ---
    theta_checks = []
    for s in [0.5, 1.0, 2.0, 3.0, 5.0]:
        ts = theta_function(s)
        t1s = theta_function(1.0 / s)
        ratio = ts / t1s if t1s != 0 else float("inf")
        expected = s ** (-0.5)
        theta_checks.append({
            "s": s, "theta_s": ts, "theta_1_over_s": t1s,
            "ratio": ratio, "expected": expected,
            "diff": abs(ratio - expected)
        })
    results["theta_equation"] = theta_checks

    # --- Summary ---
    rem_0 = abs(completed_zeta(1e-6) - 0.5)
    rem_1 = abs(completed_zeta(1.0 - 1e-6) - 0.5)
    fe_err = max(c["diff"] for c in fe_checks)
    theta_err = max(c["diff"] for c in theta_checks)
    supported = (rem_0 < 1e-3 and rem_1 < 1e-3 and fe_err < 1e-6 and theta_err < 1e-6)
    results["summary"] = {
        "removable_value_near_0_error": rem_0,
        "removable_value_near_1_error": rem_1,
        "functional_equation_max_error": fe_err,
        "theta_equation_max_error": theta_err,
        "supported": supported,
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Poisson summation via 0/0")
    print(f"  xi(s) -> 0.5 near s=0: err={s['removable_value_near_0_error']:.2e}")
    print(f"  xi(s) -> 0.5 near s=1: err={s['removable_value_near_1_error']:.2e}")
    print(f"  functional eq max err: {s['functional_equation_max_error']:.2e}")
    print(f"  theta eq max err:      {s['theta_equation_max_error']:.2e}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/poisson_summation_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
