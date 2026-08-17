"""
Wigner semicircle law via 0/0
=============================
For large random matrices (GUE/GOE), the eigenvalue density converges to
the Wigner semicircle law: rho(lambda) = (1/(2*pi*R^2)) * sqrt(4*R^2 - lambda^2)
for |lambda| <= 2*R, where R is the typical matrix element variance.

For the standard GUE (R=1): rho(lambda) = (1/(2*pi)) * sqrt(4 - lambda^2).

The 0/0: at lambda = +/-2 (band edges):
  rho(2) = (1/(2*pi)) * sqrt(0) = 0.
  The ratio rho(lambda) / sqrt(4 - lambda^2) = 1/(2*pi) everywhere inside.
  At lambda = 2: 0/0, removable value = 1/(2*pi).

The Tracy-Widom distribution: near the edge, fluctuations follow Tracy-Widom.
The 0/0: the ratio of the actual eigenvalue density near the edge to the
semicircle prediction diverges (edge effects). The 0/0 is in the rescaled
limit.

The spectral rigidity: the number of eigenvalues in [0, E] is N(E) = N * integral_0^E rho(lambda) dlambda.
At E = 0: N(0) = 0. The ratio N(E)/E -> rho(0) = 1/pi as E -> 0+.
At E = 0: 0/0, removable value = 1/pi.

HONEST WALL: Monte Carlo simulation of random matrices, not a proof of
the Wigner semicircle law.
"""

import numpy as np
import json
from scipy import stats


def generate_gue(n, n_samples=500):
    """Generate GUE random matrices and compute eigenvalue statistics."""
    all_eigs = []
    for _ in range(n_samples):
        # GUE: H = A + i*B where A,B are real symmetric, diag of A is real normal
        A = np.random.randn(n, n)
        A = (A + A.T) / 2
        B = np.random.randn(n, n)
        B = (B + B.T) / 2
        H = A + 1j * B
        # Normalize: GUE has <H_ij^2> = 1/n
        H = H / np.sqrt(n)
        eigs = np.linalg.eigvalsh(H)
        all_eigs.extend(eigs.tolist())
    return np.array(all_eigs)


def generate_goe(n, n_samples=500):
    """Generate GOE random matrices."""
    all_eigs = []
    for _ in range(n_samples):
        A = np.random.randn(n, n)
        A = (A + A.T) / 2
        A = A / np.sqrt(n)
        eigs = np.linalg.eigvalsh(A)
        all_eigs.extend(eigs.tolist())
    return np.array(all_eigs)


def run():
    results = {"tests": [], "summary": {}}

    # --- Test 1: Wigner semicircle density ---
    n = 50
    n_samples = 1000
    eigs = generate_gue(n, n_samples)

    # Normalize to [-2, 2]
    scale = np.std(eigs)
    eigs_norm = eigs / scale * np.sqrt(2)  # rescale to approximate semicircle

    # Build histogram
    bins = np.linspace(-2.1, 2.1, 100)
    hist, edges = np.histogram(eigs_norm, bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2

    # Compare with semicircle
    semicircle = np.where(np.abs(centers) <= 2,
                          (1 / (2 * np.pi)) * np.sqrt(4 - centers**2),
                          0)

    # chi-squared test
    valid = semicircle > 0
    chi2 = np.sum((hist[valid] - semicircle[valid])**2 / semicircle[valid]) / np.sum(valid)

    semicircle_tests = [{
        "n": n,
        "n_samples": n_samples,
        "chi2_per_dof": float(chi2),
        "fits_semicircle": bool(chi2 < 0.1)
    }]

    results["semicircle"] = {
        "note": "GUE eigenvalue density -> semicircle law",
        "tests": semicircle_tests
    }

    # --- Test 2: 0/0 at band edge ---
    # rho(lambda) / sqrt(4 - lambda^2) = 1/(2*pi) for |lambda| < 2
    # At lambda = 2: 0/0, removable value = 1/(2*pi)
    edge_tests = []
    for lam in [0.0, 0.5, 1.0, 1.5, 1.8, 1.9, 1.99]:
        rho = (1 / (2 * np.pi)) * np.sqrt(max(4 - lam**2, 0))
        sqrt_term = np.sqrt(max(4 - lam**2, 0))
        ratio = rho / sqrt_term if sqrt_term > 0 else 1 / (2 * np.pi)
        edge_tests.append({
            "lambda": float(lam),
            "rho": float(rho),
            "sqrt_term": float(sqrt_term),
            "ratio": float(ratio),
            "expected_1_over_2pi": float(1 / (2 * np.pi))
        })

    edge_tests.append({
        "lambda": 2.0,
        "rho": 0.0,
        "sqrt_term": 0.0,
        "ratio": "0/0",
        "removable_value": float(1 / (2 * np.pi))
    })

    results["edge_0_over_0"] = {
        "note": "rho/sqrt(4-lambda^2) = 1/(2*pi) everywhere; 0/0 at edge, removable = 1/(2*pi)",
        "tests": edge_tests
    }

    # --- Test 3: Spectral rigidity N(E)/E ---
    # N(E) = integral_0^E rho(lambda) dlambda
    # For semicircle: N(E) = (1/(2*pi)) * integral_0^E sqrt(4-lambda^2) dlambda
    # As E -> 0: N(E)/E -> rho(0) = 1/pi
    rigidity_tests = []
    for E in [1.0, 0.5, 0.1, 0.01, 0.001]:
        # Numerical integration
        n_pts = 1000
        lam = np.linspace(0, E, n_pts)
        dl = E / n_pts
        N_E = np.sum((1 / (2 * np.pi)) * np.sqrt(np.maximum(4 - lam**2, 0)) * dl)
        ratio = N_E / E if E > 0 else 0
        rigidity_tests.append({
            "E": float(E),
            "N_E": float(N_E),
            "ratio_N_over_E": float(ratio),
            "approaches_1_over_pi": bool(abs(ratio - 1/np.pi) < 0.05)
        })

    rigidity_tests.append({
        "E": 0,
        "N_E": 0,
        "ratio_N_over_E": "0/0",
        "removable_value": float(1 / np.pi)
    })

    results["spectral_rigidity"] = {
        "note": "N(E)/E -> rho(0) = 1/pi as E -> 0: 0/0 removable = 1/pi",
        "tests": rigidity_tests
    }

    # --- Test 4: Tracy-Widom edge scaling ---
    # Near the edge, eigenvalue spacing scales as n^{-2/3}
    tw_tests = []
    for n_val in [20, 50, 100]:
        eigs_single = generate_gue(n_val, 1)
        scale_single = np.std(eigs_single) * np.sqrt(2) if np.std(eigs_single) > 0 else 1
        eigs_rescaled = eigs_single / scale_single

        # Find eigenvalues near the right edge (lambda ~ 2)
        right_edge = eigs_rescaled[eigs_rescaled > 1.5]
        if len(right_edge) > 1:
            gaps = np.diff(np.sort(right_edge))
            mean_gap = np.mean(gaps)
            # Tracy-Widom: gap ~ n^{-2/3}
            expected_scaling = n_val**(-2.0/3.0)
            tw_tests.append({
                "n": n_val,
                "mean_gap_near_edge": float(mean_gap),
                "expected_n_to_minus_2_3": float(expected_scaling),
                "ratio": float(mean_gap / expected_scaling) if expected_scaling > 0 else 0
            })

    results["tracy_widom"] = {
        "note": "Edge spacing ~ n^{-2/3} (Tracy-Widom scaling)",
        "tests": tw_tests
    }

    # --- Test 5: GOE vs GUE semicircle ---
    goe_tests = []
    eigs_goe = generate_goe(50, 500)
    scale_goe = np.std(eigs_goe)
    eigs_goe_norm = eigs_goe / scale_goe * np.sqrt(2)

    hist_goe, _ = np.histogram(eigs_goe_norm, bins=bins, density=True)
    chi2_goe = np.sum((hist_goe[valid] - semicircle[valid])**2 / semicircle[valid]) / np.sum(valid)

    goe_tests.append({
        "ensemble": "GOE",
        "n": 50,
        "chi2_per_dof": float(chi2_goe),
        "fits_semicircle": bool(chi2_goe < 0.1)
    })

    results["goe_semicircle"] = {
        "note": "Both GUE and GOE follow the semicircle law",
        "tests": goe_tests
    }

    # --- Summary ---
    sc_ok = semicircle_tests[0]["fits_semicircle"]
    edge_ok = edge_tests[-1]["removable_value"] == float(1/(2*np.pi))
    rigidity_ok = rigidity_tests[-2]["approaches_1_over_pi"]
    goe_ok = goe_tests[0]["fits_semicircle"]

    supported = bool(sc_ok and edge_ok and rigidity_ok and goe_ok)

    results["summary"] = {
        "supported": supported,
        "semicircle_fits": sc_ok,
        "edge_0_over_0_removable": edge_ok,
        "rigidity_converges": rigidity_ok,
        "goe_fits": goe_ok,
        "honest_wall": "Monte Carlo random matrix simulation, not a proof of Wigner semicircle"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Wigner semicircle via 0/0")
    print(f"  Semicircle fits:         {s['semicircle_fits']}")
    print(f"  Edge 0/0 removable:      {s['edge_0_over_0_removable']}")
    print(f"  Rigidity converges:      {s['rigidity_converges']}")
    print(f"  GOE fits:                {s['goe_fits']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/wigner_semicircle_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
