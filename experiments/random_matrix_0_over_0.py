import numpy as np
import json
from math import pi, sqrt, log, e

def circular_law():
    """Eigenvalues of iid matrix -> uniform on unit disk"""
    np.random.seed(42)
    ns = [100, 200, 500]
    results = []
    for n in ns:
        A = (np.random.randn(n, n) + 1j * np.random.randn(n, n)) / sqrt(2 * n)
        eigenvalues = np.linalg.eigvals(A)
        radii = np.abs(eigenvalues)
        frac_inside = float(np.mean(radii <= 1.0))
        mean_r = float(np.mean(radii))
        target_mean_r = 2.0 / 3.0
        results.append({
            "n": n, "frac_inside": frac_inside,
            "mean_radius": mean_r, "mean_r_error": abs(mean_r - target_mean_r),
        })
    max_err = max(r["mean_r_error"] for r in results)
    return {
        "name": "circular_law",
        "description": "Circular law: eigenvalues uniform on disk; mean radius -> 2/3",
        "removable_value": 2.0 / 3.0,
        "limit_value": results[-1]["mean_radius"],
        "max_error": max_err,
        "passed": bool(max_err < 0.05),
        "details": results,
    }

def tracy_widom_fluctuation():
    """Largest eigenvalue of GUE follows Tracy-Widom (proper normalization)"""
    np.random.seed(42)
    n = 300
    n_trials = 200
    largest_eigs = []
    for _ in range(n_trials):
        # Construct GUE properly: H_ii ~ N(0,1/n), H_ij (i<j) ~ CN(0, 1/n)
        # Generate upper triangle only, then hermitianize
        A = (np.random.randn(n, n) + 1j * np.random.randn(n, n)) / sqrt(2 * n)
        H = np.triu(A, 1) + np.triu(A, 1).conj().T
        np.fill_diagonal(H, np.random.randn(n) / sqrt(n))
        eigs = np.linalg.eigvalsh(H)
        # Semicircle radius = 2, Tracy-Widom: n^{2/3}(lambda_max - 2) -> TW_1
        scaled = (eigs[-1] - 2.0) * n ** (2.0 / 3.0)
        largest_eigs.append(float(scaled))

    tw_mean = np.mean(largest_eigs)
    # Tracy-Widom mean ~ -1.7711
    target_mean = -1.7711
    err = abs(tw_mean - target_mean)
    return {
        "name": "tracy_widom_fluctuation",
        "description": "Largest eigenvalue of GUE follows Tracy-Widom; n^{2/3}(lmax-2) -> TW_1",
        "removable_value": target_mean,
        "limit_value": float(tw_mean),
        "max_error": err,
        "passed": bool(err < 0.5),
        "n_trials": n_trials,
    }

def wigner_semicircle_0_over_0():
    """GUE eigenvalue density -> semicircle"""
    np.random.seed(42)
    n = 500
    n_trials = 20
    all_eigs = []
    for _ in range(n_trials):
        A = (np.random.randn(n, n) + 1j * np.random.randn(n, n)) / sqrt(2 * n)
        H = np.triu(A, 1) + np.triu(A, 1).conj().T
        np.fill_diagonal(H, np.random.randn(n) / sqrt(n))
        all_eigs.extend(np.linalg.eigvalsh(H))
    all_eigs = np.array(all_eigs)
    bins = np.linspace(-2.1, 2.1, 200)
    hist, edges = np.histogram(all_eigs, bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2.0
    semicircle = np.sqrt(np.maximum(4.0 - centers ** 2, 0)) / (2 * pi)
    mask = np.abs(centers) < 1.5
    err = float(np.mean(np.abs(hist[mask] - semicircle[mask])))
    return {
        "name": "wigner_semicircle_0_over_0",
        "description": "GUE density -> semicircle (0/0 at edge, removable=0)",
        "removable_value": 0.0,
        "bulk_error": err,
        "passed": bool(err < 0.1),
    }

def marchenko_pastur():
    """Singular values of rectangular random matrix follow MP law"""
    np.random.seed(42)
    m, n = 200, 100
    gamma = n / m
    n_trials = 20
    all_sv2 = []
    for _ in range(n_trials):
        A = np.random.randn(m, n) / sqrt(n)
        sv = np.linalg.svd(A, compute_uv=False)
        all_sv2.extend(sv ** 2)
    all_sv2 = np.array(all_sv2)
    a = (1 - sqrt(gamma)) ** 2
    b = (1 + sqrt(gamma)) ** 2
    bins = np.linspace(a - 0.1, b + 0.1, 200)
    hist, edges = np.histogram(all_sv2, bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2.0
    mp_density = np.sqrt(np.maximum((b - centers) * (centers - a), 0)) / (2 * pi * gamma * np.maximum(centers, 1e-10))
    mask = (centers > a + 0.05) & (centers < b - 0.05)
    err = float(np.mean(np.abs(hist[mask] - mp_density[mask]))) if np.any(mask) else 1.0
    return {
        "name": "marchenko_pastur",
        "description": "Marchenko-Pastur: MP density for rectangular random matrix",
        "bulk_error": err,
        "passed": bool(err < 0.3),
    }

def sample_covariance_mean():
    """Mean eigenvalue of Wishart W_p(n,I)/n = 1"""
    np.random.seed(42)
    p, n = 50, 200
    n_trials = 50
    means = []
    for _ in range(n_trials):
        X = np.random.randn(p, n)
        S = X @ X.T / n
        eigs = np.linalg.eigvalsh(S)
        means.append(float(np.mean(eigs)))
    mean_eig = np.mean(means)
    target = 1.0
    err = abs(mean_eig - target)
    return {
        "name": "sample_covariance_mean",
        "description": "Mean eigenvalue of sample covariance = 1 (0/0 removable=1)",
        "removable_value": target,
        "limit_value": float(mean_eig),
        "max_error": err,
        "passed": bool(err < 0.1),
    }

if __name__ == "__main__":
    results = {}
    tests = [
        circular_law,
        tracy_widom_fluctuation,
        wigner_semicircle_0_over_0,
        marchenko_pastur,
        sample_covariance_mean,
    ]
    all_pass = True
    for test in tests:
        r = test()
        results[r["name"]] = r
        status = "PASS" if r["passed"] else "FAIL"
        if not r["passed"]:
            all_pass = False
        print(f"  {status}: {r['description']}")
    outfile = "data/random_matrix_0_over_0_data.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  All pass: {all_pass}")
    print(f"  Wrote {outfile}")
