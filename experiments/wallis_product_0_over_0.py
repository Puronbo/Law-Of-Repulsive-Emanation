"""
Wallis product via 0/0
======================
The Wallis product for pi/2:

  pi/2 = prod_{n=1}^{inf} (2n)^2 / ((2n-1)(2n+1))

Each factor (2n)^2/((2n-1)(2n+1)) = 4n^2/(4n^2-1) -> 1 as n -> inf.

The 0/0: the product of infinitely many factors approaching 1 is 1^inf,
an indeterminate form.  The removable value is pi/2.

Equivalently, the ratio of the partial product P_N to any candidate
limit L gives P_N/L -> 1, but P_N itself converges to pi/2 from below.
The "0/0" is that each factor minus 1 is O(1/n^2), and the sum of
O(1/n^2) converges, so the product converges to a finite non-1 value.

HONEST WALL: numerical verification of the product convergence, not a
proof of Wallis' formula.
"""

import numpy as np
import json


def wallis_partial(N):
    """Compute the N-th partial product of the Wallis product."""
    prod = 1.0
    for n in range(1, N + 1):
        prod *= (2 * n) ** 2 / ((2 * n - 1) * (2 * n + 1))
    return prod


def wallis_partial_log(N):
    """Compute log of the N-th partial product (more numerically stable)."""
    log_sum = 0.0
    for n in range(1, N + 1):
        log_sum += 2 * np.log(2 * n) - np.log(2 * n - 1) - np.log(2 * n + 1)
    return log_sum


def run():
    results = {}

    # --- Test 1: convergence of partial products to pi/2 ---
    convergences = []
    for exp in range(1, 8):
        N = 10 ** exp
        P_N = wallis_partial(min(N, 100000)) if N > 100000 else wallis_partial(N)
        if N > 100000:
            P_N = np.exp(wallis_partial_log(N))
        convergences.append({
            "N": N, "P_N": P_N, "pi_over_2": np.pi / 2,
            "error": abs(P_N - np.pi / 2)
        })
    results["convergence"] = convergences

    # --- Test 2: each factor approaches 1 ---
    factor_checks = []
    for n in [1, 10, 100, 1000, 10000]:
        factor = (2 * n) ** 2 / ((2 * n - 1) * (2 * n + 1))
        factor_checks.append({
            "n": n, "factor": factor,
            "error_from_1": abs(factor - 1)
        })
    results["factor_limit"] = factor_checks

    # --- Test 3: ratio of consecutive partial products -> 1 ---
    ratio_checks = []
    for exp in range(1, 7):
        N = 10 ** exp
        P_N = np.exp(wallis_partial_log(N))
        P_2N = np.exp(wallis_partial_log(2 * N))
        ratio = P_2N / P_N
        ratio_checks.append({
            "N": N, "ratio": ratio, "error_from_1": abs(ratio - 1)
        })
    results["ratio_limit"] = ratio_checks

    # --- Test 4: error decreases as O(1/N) ---
    error_decay = []
    for exp in range(1, 7):
        N = 10 ** exp
        P_N = np.exp(wallis_partial_log(N))
        err = abs(P_N - np.pi / 2)
        error_decay.append({"N": N, "error": err})
    results["error_decay"] = error_decay

    # --- Summary ---
    last_conv_err = convergences[-1]["error"]
    last_factor_err = factor_checks[-1]["error_from_1"]
    supported = bool(last_conv_err < 1e-4 and last_factor_err < 1e-4)
    results["summary"] = {
        "convergence_error": last_conv_err,
        "factor_limit_error": last_factor_err,
        "pi_over_2": float(np.pi / 2),
        "supported": supported,
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Wallis product via 0/0")
    print(f"  convergence to pi/2: err={s['convergence_error']:.2e}")
    print(f"  factor -> 1:         err={s['factor_limit_error']:.2e}")
    print(f"  pi/2 = {s['pi_over_2']:.10f}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/wallis_product_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
