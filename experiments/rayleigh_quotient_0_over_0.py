"""
Rayleigh quotient via 0/0
=========================
The Rayleigh quotient for a symmetric matrix A and vector x is:

  R(x) = (x^T A x) / (x^T x)

At x = 0: R(0) = 0/0 (both numerator and denominator vanish).

The removable value depends on the direction of approach:
  - Along eigenvector v_i: R(t*v_i) -> lambda_i (the i-th eigenvalue)
  - The minimum removable value is lambda_min (the smallest eigenvalue)
  - The maximum removable value is lambda_max

This encodes the entire spectrum of A in a single 0/0. The min-max
principle (Courant-Fischer) says: lambda_k = min_{dim(S)=k} max_{x in S} R(x).

HONEST WALL: computation on specific finite-dimensional matrices, not a
proof of the spectral theorem.
"""

import numpy as np
import json


def rayleigh(A, x):
    """Compute R(x) = (x^T A x) / (x^T x). Returns nan at x=0."""
    x = np.asarray(x, dtype=float)
    norm2 = x @ x
    if norm2 < 1e-30:
        return float("nan")
    return float(x @ A @ x / norm2)


def run():
    results = {}

    # --- Test 1: 2x2 matrix, approach 0 along eigenvectors ---
    A2 = np.array([[5.0, 1.0], [1.0, 3.0]])
    evals2, evecs2 = np.linalg.eigh(A2)
    conv_2d = []
    for i in range(2):
        lam = evals2[i]
        v = evecs2[:, i]
        trials = []
        for exp in range(1, 10):
            t = 10.0 ** (-exp)
            R = rayleigh(A2, t * v)
            trials.append({"t": t, "R": R, "error": abs(R - lam)})
        conv_2d.append({"eigenvalue": lam, "direction": v.tolist(), "trials": trials})
    results["2x2_convergence"] = conv_2d

    # --- Test 2: 3x3 matrix, approach 0 along eigenvectors ---
    A3 = np.array([[2.0, 1.0, 0.0], [1.0, 3.0, 1.0], [0.0, 1.0, 2.0]])
    evals3, evecs3 = np.linalg.eigh(A3)
    conv_3d = []
    for i in range(3):
        lam = evals3[i]
        v = evecs3[:, i]
        trials = []
        for exp in range(1, 10):
            t = 10.0 ** (-exp)
            R = rayleigh(A3, t * v)
            trials.append({"t": t, "R": R, "error": abs(R - lam)})
        conv_3d.append({"eigenvalue": lam, "trials": trials})
    results["3x3_convergence"] = conv_3d

    # --- Test 3: approach 0 along random direction ---
    np.random.seed(42)
    v_rand = np.random.randn(3)
    v_rand /= np.linalg.norm(v_rand)
    R_limit = float(v_rand @ A3 @ v_rand)
    rand_trials = []
    for exp in range(1, 10):
        t = 10.0 ** (-exp)
        R = rayleigh(A3, t * v_rand)
        rand_trials.append({"t": t, "R": R, "limit": R_limit, "error": abs(R - R_limit)})
    results["random_direction"] = {"direction": v_rand.tolist(), "limit": R_limit, "trials": rand_trials}

    # --- Test 4: verify min/max eigenvalue bounds ---
    all_R = []
    for _ in range(1000):
        x = np.random.randn(3)
        all_R.append(rayleigh(A3, x))
    all_R = np.array(all_R)
    bounds = {
        "min_R": float(np.min(all_R)),
        "max_R": float(np.max(all_R)),
        "lambda_min": float(evals3[0]),
        "lambda_max": float(evals3[2]),
        "bounds_hold": bool(np.min(all_R) >= evals3[0] - 1e-10 and np.max(all_R) <= evals3[2] + 1e-10),
    }
    results["eigenvalue_bounds"] = bounds

    # --- Summary ---
    err_2d = max(t["error"] for c in conv_2d for t in c["trials"])
    err_3d = max(t["error"] for c in conv_3d for t in c["trials"])
    err_rand = max(t["error"] for t in rand_trials)
    supported = bool(err_2d < 1e-3 and err_3d < 1e-3 and err_rand < 1e-6 and bounds["bounds_hold"])
    results["summary"] = {
        "max_error_2d": err_2d,
        "max_error_3d": err_3d,
        "max_error_random": err_rand,
        "bounds_hold": bounds["bounds_hold"],
        "supported": supported,
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Rayleigh quotient via 0/0")
    print(f"  2x2 convergence error: {s['max_error_2d']:.2e}")
    print(f"  3x3 convergence error: {s['max_error_3d']:.2e}")
    print(f"  random direction error: {s['max_error_random']:.2e}")
    print(f"  eigenvalue bounds hold: {s['bounds_hold']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/rayleigh_quotient_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
