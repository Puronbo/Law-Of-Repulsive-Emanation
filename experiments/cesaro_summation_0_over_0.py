"""
Cesaro summation via 0/0
========================
Grandi's series: S = 1 - 1 + 1 - 1 + ...

The partial sums S_N alternate: 1, 0, 1, 0, ... -- the series diverges.
The Cesaro mean C_N = (S_1 + ... + S_N) / N converges to 1/2.

The 0/0: at N -> inf, C_N = (sum of oscillating partial sums) / N
is inf/inf = 0/0.  The removable value is 1/2.

More generally, for the geometric series sum_{k=0}^{N} r^k = (1-r^{N+1})/(1-r):
  - At r=1: the formula gives 0/0 (both numerator and denominator vanish)
  - The removable value is N+1 (the sum is N+1 terms of 1)
  - At r=-1: the formula gives (1-(-1)^{N+1})/2, which oscillates
  - The Cesaro limit is 1/2

The 0/0 at r=1 encodes the transition from geometric growth to divergence.

HONEST WALL: numerical verification of Cesaro means, not a proof of
summability theory.
"""

import numpy as np
import json


def partial_sum_geometric(r, N):
    """Sum_{k=0}^{N} r^k."""
    if abs(r - 1.0) < 1e-15:
        return N + 1.0
    return (1 - r ** (N + 1)) / (1 - r)


def cesaro_mean(r, N):
    """Cesaro mean of sum_{k=0}^{N} r^k: C_N = (1/N) sum_{n=0}^{N-1} S_n."""
    total = 0.0
    for n in range(N):
        total += partial_sum_geometric(r, n)
    return total / N


def run():
    results = {}

    # --- Test 1: Cesaro mean of Grandi's series (r=-1) ---
    grandi_cesaro = []
    for exp in range(1, 8):
        N = 10 ** exp
        C_N = cesaro_mean(-1.0, N)
        grandi_cesaro.append({
            "N": N, "C_N": C_N, "error": abs(C_N - 0.5)
        })
    results["grandi_cesaro"] = grandi_cesaro

    # --- Test 2: geometric formula 0/0 at r=1 ---
    # (1 - r^{N+1}) / (1 - r) at r=1: 0/0, removable = N+1
    geometric_0_over_0 = []
    for N in [5, 10, 20]:
        exact = N + 1.0
        # Approach r=1 from below
        errors = []
        for exp in range(1, 8):
            r = 1.0 - 10.0 ** (-exp)
            formula = (1 - r ** (N + 1)) / (1 - r)
            errors.append({
                "r": r, "formula": formula,
                "error": abs(formula - exact)
            })
        geometric_0_over_0.append({"N": N, "exact": exact, "convergence": errors})
    results["geometric_0_over_0"] = geometric_0_over_0

    # --- Test 3: Cesaro mean for other values of r ---
    cesaro_other = []
    for r in [0.5, -0.5, 0.9, -0.9]:
        exact_sum = 1.0 / (1 - r) if abs(r) < 1 else float("nan")
        C_N = cesaro_mean(r, 10000)
        cesaro_other.append({
            "r": r, "C_N": C_N, "exact_infinite_sum": exact_sum,
            "error": abs(C_N - exact_sum) if not np.isnan(exact_sum) else float("nan")
        })
    results["cesaro_other_r"] = cesaro_other

    # --- Test 4: Cesaro mean converges even when partial sums don't ---
    # r=1.0: partial sums are 1, 2, 3, ..., N+1 (diverge)
    # Cesaro mean: C_N = (sum_{n=0}^{N-1} (n+1)) / N = N(N+1)/(2N) = (N+1)/2 -> inf
    # So Cesaro doesn't help for r>1
    # But for r=-1 (Grandi), Cesaro gives 1/2

    # --- Summary ---
    last_grandi_err = grandi_cesaro[-1]["error"]
    last_geo_err = geometric_0_over_0[-1]["convergence"][-1]["error"]
    supported = bool(last_grandi_err < 1e-4 and last_geo_err < 1e-4)
    results["summary"] = {
        "grandi_cesaro_error": last_grandi_err,
        "geometric_0_over_0_error": last_geo_err,
        "supported": supported,
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Cesaro summation via 0/0")
    print(f"  Grandi Cesaro -> 0.5:  err={s['grandi_cesaro_error']:.2e}")
    print(f"  geometric 0/0 -> N+1:  err={s['geometric_0_over_0_error']:.2e}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/cesaro_summation_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
