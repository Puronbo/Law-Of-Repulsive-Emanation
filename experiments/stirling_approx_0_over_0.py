"""
Stirling's approximation via 0/0
================================
Stirling's formula: n! ~ sqrt(2*pi*n) * (n/e)^n as n -> infinity.

The 0/0: the ratio n! / (sqrt(2*pi*n) * (n/e)^n) -> 1 as n -> infinity.
At n = 0: 0! / sqrt(0) = 1/0 = infinity (not 0/0).
But the log ratio: log(n!) / log(sqrt(2*pi*n) * (n/e)^n) -> 1 as n -> infinity.
At n = 1: log(1)/log(sqrt(2*pi)/e) = 0/log(0.922) = 0 (not 0/0).

The real 0/0: consider the correction terms.
Stirling with correction: n! = sqrt(2*pi*n) * (n/e)^n * (1 + 1/(12n) + ...)
The ratio (n! / (sqrt(2*pi*n) * (n/e)^n) - 1) * n -> 1/12 as n -> infinity.
At n = infinity: (1-1)*inf = 0*inf = 0/0. Removable value = 1/12.

For the Gamma function: Gamma(z) ~ sqrt(2*pi/z) * (z/e)^z for large |z|.
The 0/0: Gamma(z) * sqrt(z) / (sqrt(2*pi) * (z/e)^z) -> 1 as z -> infinity.
At z = 0: Gamma(0) = infinity, sqrt(0) = 0, (0/e)^0 = 1.
The ratio is infinity * 0 / sqrt(2*pi) = 0/0. Removable value = 1
(since Gamma(z) ~ 1/z near z=0, so Gamma(z)*sqrt(z) ~ sqrt(z)/z = 1/sqrt(z) -> infinity).
Actually this is more subtle.

The Wallis product connection:
pi/2 = prod_{n=1}^{inf} (2n)^2 / ((2n-1)*(2n+1))
= lim_{n->inf} (2^n * n!)^2 / ((2n)! * sqrt(n))

The 0/0: (2n)! / ((2^n * n!)^2 * sqrt(pi*n)) -> 1 as n -> infinity.
At n = 0: 1 / (1 * 1 * 0) = infinity (not 0/0).

The clean 0/0: log(n!) - n*log(n) + n = (1/2)*log(2*pi*n) + O(1/n).
The ratio [log(n!) - n*log(n) + n - (1/2)*log(2*pi*n)] * n -> 1/12.
At n = infinity: 0*inf = 0/0, removable = 1/12.

HONEST WALL: numerical verification of Stirling's approximation.
"""

import numpy as np
import json
from math import factorial, log, sqrt, pi, e
from scipy.special import gammaln


def stirling_approx(n):
    """sqrt(2*pi*n) * (n/e)^n in log space for large n."""
    if n <= 0:
        return 0
    log_val = 0.5 * log(2 * pi * n) + n * log(n / e)
    if log_val > 700:
        return float('inf')
    return np.exp(log_val)


def stirling_log(n):
    """log(sqrt(2*pi*n)) + n*log(n/e)"""
    if n <= 0:
        return 0
    return 0.5 * log(2 * pi * n) + n * log(n / e)


def run():
    results = {"tests": [], "summary": {}}

    # --- Test 1: Basic Stirling ratio ---
    ratio_tests = []
    for n in [1, 2, 5, 10, 20, 50, 100, 200, 500]:
        log_exact = gammaln(n + 1)
        log_approx = stirling_log(n)
        log_ratio = log_exact - log_approx
        ratio = np.exp(log_ratio)

        ratio_tests.append({
            "n": n,
            "log_ratio": float(log_ratio),
            "ratio": float(ratio),
            "deviation_from_one": float(abs(ratio - 1.0))
        })

    results["basic_ratio"] = {
        "note": "n! / Stirling -> 1 as n -> infinity",
        "tests": ratio_tests
    }

    # --- Test 2: Log ratio (better for large n) ---
    log_tests = []
    for n in [1, 2, 5, 10, 20, 50, 100, 200, 500]:
        log_exact = gammaln(n + 1)
        log_approx = stirling_log(n)
        log_diff = log_exact - log_approx

        log_tests.append({
            "n": n,
            "log_n!": float(log_exact),
            "log_stirling": float(log_approx),
            "log_difference": float(log_diff),
            "relative_error": float(log_diff / log_exact) if log_exact > 0 else 0
        })

    results["log_ratio"] = {
        "note": "log(n!) - log(Stirling) -> 0; relative error -> 0",
        "tests": log_tests
    }

    # --- Test 3: Correction term 1/(12n) ---
    # n! / Stirling = 1 + 1/(12n) + 1/(288*n^2) + ...
    correction_tests = []
    for n in [5, 10, 20, 50, 100, 200]:
        log_exact = gammaln(n + 1)
        log_approx = stirling_log(n)
        ratio = np.exp(log_exact - log_approx)
        correction = ratio - 1.0
        expected_correction = 1.0 / (12 * n)

        correction_tests.append({
            "n": n,
            "ratio": float(ratio),
            "correction": float(correction),
            "expected_1_12n": float(expected_correction),
            "ratio_correction": float(correction / expected_correction) if abs(expected_correction) > 1e-15 else 0,
            "approaches_one": bool(abs(correction / expected_correction - 1.0) < 0.1) if abs(expected_correction) > 1e-15 else False
        })

    results["correction_term"] = {
        "note": "n!/Stirling - 1 ~ 1/(12n): correction ratio -> 1",
        "tests": correction_tests
    }

    # --- Test 4: 0/0 in correction ---
    # [n!/Stirling - 1] * n -> 1/12 as n -> infinity
    # At n = infinity: 0 * inf = 0/0, removable = 1/12
    correction_0_tests = []
    for n in [10, 50, 100, 200, 500]:
        log_exact = gammaln(n + 1)
        log_approx = stirling_log(n)
        ratio = np.exp(log_exact - log_approx)
        product = (ratio - 1.0) * n

        correction_0_tests.append({
            "n": n,
            "ratio_minus_1": float(ratio - 1.0),
            "times_n": float(product),
            "approaches_1_12": bool(abs(product - 1.0 / 12) < 0.05)
        })

    correction_0_tests.append({
        "n": "infinity",
        "ratio_minus_1": 0,
        "times_n": "0*inf = 0/0",
        "removable_value": 1.0 / 12
    })

    results["correction_0_over_0"] = {
        "note": "[n!/Stirling - 1] * n -> 1/12: 0*inf = 0/0 removable = 1/12",
        "tests": correction_0_tests
    }

    # --- Test 5: Gamma function Stirling ---
    # Gamma(n+1) = n!
    gamma_tests = []
    for n in [5, 10, 20, 50]:
        from scipy.special import gamma
        gamma_val = gamma(n + 1)
        stirling_val = stirling_approx(n)
        ratio = gamma_val / stirling_val if stirling_val > 0 else 0

        gamma_tests.append({
            "n": n,
            "Gamma(n+1)": float(gamma_val),
            "stirling": float(stirling_val),
            "ratio": float(ratio),
            "close_to_one": bool(abs(ratio - 1.0) < 0.01)
        })

    results["gamma_stirling"] = {
        "note": "Gamma(n+1) / Stirling -> 1",
        "tests": gamma_tests
    }

    # --- Test 6: Wallis product connection ---
    # Wallis: pi/2 = prod_{k=1}^{inf} (2k)^2 / ((2k-1)*(2k+1))
    wallis_tests = []
    for n in [5, 10, 50, 100, 500]:
        product = 1.0
        for k in range(1, n + 1):
            product *= (2 * k) ** 2 / ((2 * k - 1) * (2 * k + 1))
        ratio = product / (np.pi / 2)

        wallis_tests.append({
            "n": n,
            "product": float(product),
            "pi_over_2": float(np.pi / 2),
            "ratio": float(ratio),
            "approaches_one": bool(abs(ratio - 1.0) < 0.05)
        })

        wallis_tests.append({
            "n": n,
            "product": float(product),
            "pi_over_2": float(np.pi / 2),
            "ratio": float(ratio),
            "approaches_one": bool(abs(ratio - 1.0) < 0.05)
        })

    results["wallis_connection"] = {
        "note": "Wallis: (2n)! / (4^n * (n!)^2 * sqrt(pi*n)) -> 1",
        "tests": wallis_tests
    }

    # --- Summary ---
    ratio_ok = ratio_tests[-1]["deviation_from_one"] < 0.01
    log_ok = log_tests[-1]["relative_error"] < 0.01
    correction_ok = any(t["approaches_one"] for t in correction_tests)
    correction_0_ok = correction_0_tests[-2]["approaches_1_12"]
    gamma_ok = gamma_tests[-1]["close_to_one"]
    wallis_ok = wallis_tests[-1]["approaches_one"]

    supported = bool(ratio_ok and log_ok and correction_ok and correction_0_ok and gamma_ok and wallis_ok)

    results["summary"] = {
        "supported": supported,
        "ratio_converges": ratio_ok,
        "log_converges": log_ok,
        "correction_correct": correction_ok,
        "correction_0_over_0": correction_0_ok,
        "gamma_stirling_correct": gamma_ok,
        "wallis_correct": wallis_ok,
        "honest_wall": "numerical verification of Stirling's approximation"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Stirling's approximation via 0/0")
    print(f"  Ratio converges:         {s['ratio_converges']}")
    print(f"  Log converges:           {s['log_converges']}")
    print(f"  Correction correct:      {s['correction_correct']}")
    print(f"  Correction 0/0:          {s['correction_0_over_0']}")
    print(f"  Gamma correct:           {s['gamma_stirling_correct']}")
    print(f"  Wallis correct:          {s['wallis_correct']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/stirling_approx_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
