"""
Random Matrix Theory as 0/0
============================
Montgomery-Odlyzko Law: L-function zeros follow GUE statistics.
Level repulsion: R_2(0) = 0 (eigenvalues repel).

Theory:
  R_2(x) = 1 - (sin(pi*x)/(pi*x))^2  (GUE pair correlation)
  Wigner GOE: P(s) = (pi/2) * s * exp(-pi*s^2/4)
  Wigner GUE: P(s) = (32/pi^2) * s^2 * exp(-4*s^2/pi)
  Level repulsion: R_2(0) = 0 for all beta >= 1
"""

import numpy as np
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def gue_matrix(N):
    A = (np.random.randn(N, N) + 1j * np.random.randn(N, N)) / np.sqrt(2)
    return (A + A.conj().T) / 2


def goe_matrix(N):
    A = np.random.randn(N, N)
    return (A + A.T) / 2


def wigner_surmise_GOE(s):
    return (np.pi / 2.0) * s * np.exp(-np.pi * s**2 / 4.0)


def wigner_surmise_GUE(s):
    return (32.0 / np.pi**2) * s**2 * np.exp(-4.0 * s**2 / np.pi)


def wigner_cdf_GOE(s):
    return 1.0 - np.exp(-np.pi * np.asarray(s, dtype=float)**2 / 4.0)


def wigner_cdf_GUE(s):
    from scipy.special import erf
    s = np.asarray(s, dtype=float)
    return erf(2.0 * s / np.sqrt(np.pi)) - (4.0 * s / np.pi) * np.exp(-4.0 * s**2 / np.pi)


def montgomery_odlyzko(x):
    x = np.asarray(x, dtype=float)
    result = np.ones_like(x)
    nonzero = np.abs(x) > 1e-10
    pix = np.pi * x[nonzero]
    result[nonzero] = 1.0 - (np.sin(pix) / pix) ** 2
    return result


def eigenvalue_spacings(eigenvalues):
    sorted_eigs = np.sort(np.real(eigenvalues))
    spacings = np.diff(sorted_eigs)
    mean_spacing = np.mean(spacings)
    if mean_spacing < 1e-15:
        return np.array([])
    return spacings / mean_spacing


def ks_test_vs_wigner(spacings, cdf_func):
    sorted_sp = np.sort(spacings)
    N = len(sorted_sp)
    empirical_cdf = np.arange(1, N + 1) / N
    theoretical_cdf = cdf_func(sorted_sp)
    return np.max(np.abs(empirical_cdf - theoretical_cdf))


def pair_correlation_single(eigenvalues, n_bins=80, x_max=4.0):
    """Compute R_2(x) from a single matrix's eigenvalues."""
    sorted_eigs = np.sort(np.real(eigenvalues))
    N = len(sorted_eigs)
    if N < 10:
        return np.array([]), np.array([])
    mean_spacing = (sorted_eigs[-1] - sorted_eigs[0]) / (N - 1)
    if mean_spacing < 1e-15:
        return np.array([]), np.array([])
    diffs = sorted_eigs[:, None] - sorted_eigs[None, :]
    diffs = np.abs(diffs[np.triu_indices(N, k=1)])
    diffs = diffs / mean_spacing
    diffs = diffs[diffs < x_max]
    hist, bin_edges = np.histogram(diffs, bins=n_bins, range=(0, x_max))
    x_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
    dx = bin_edges[1] - bin_edges[0]
    expected_per_bin = N * dx
    r2 = hist.astype(float) / expected_per_bin
    return x_centers, r2


def experiment_level_repulsion():
    print("  Q1: Level repulsion (eigenvalues repel)")
    N_trials = 200
    matrix_size = 200
    all_spacings = []
    for _ in range(N_trials):
        H = gue_matrix(matrix_size)
        eigs = np.linalg.eigvalsh(H)
        sp = eigenvalue_spacings(eigs)
        all_spacings.extend(sp)
    all_spacings = np.array(all_spacings)
    tiny = np.sum(all_spacings < 0.01) / len(all_spacings)
    repulsion = tiny < 0.001
    print(f"    Fraction of spacings < 0.01: {tiny:.6f}")
    print(f"    Level repulsion (R_2(0) -> 0): {repulsion}")
    return {
        "tiny_fraction": float(tiny),
        "level_repulsion": bool(repulsion),
        "n_spacings": len(all_spacings)
    }


def experiment_wigner_gue():
    print("  Q2: GUE eigenvalue spacings match Wigner surmise")
    N_trials = 500
    matrix_size = 200
    all_spacings = []
    for _ in range(N_trials):
        H = gue_matrix(matrix_size)
        eigs = np.linalg.eigvalsh(H)
        sp = eigenvalue_spacings(eigs)
        all_spacings.extend(sp)
    all_spacings = np.array(all_spacings)
    ks = ks_test_vs_wigner(all_spacings, wigner_cdf_GUE)
    var_theory = 4.0 / np.pi - 1.0
    good_fit = ks < 0.06
    print(f"    Mean spacing: {np.mean(all_spacings):.4f} (should be ~1.0)")
    print(f"    Var spacing: {np.var(all_spacings):.4f} (theory {var_theory:.4f})")
    print(f"    KS statistic: {ks:.4f}")
    print(f"    Good fit: {good_fit}")
    return {
        "mean_spacing": float(np.mean(all_spacings)),
        "var_spacing": float(np.var(all_spacings)),
        "ks_statistic": float(ks),
        "good_fit": bool(good_fit),
        "n_spacings": len(all_spacings)
    }


def experiment_wigner_goe():
    print("  Q3: GOE eigenvalue spacings match Wigner surmise")
    N_trials = 500
    matrix_size = 200
    all_spacings = []
    for _ in range(N_trials):
        H = goe_matrix(matrix_size)
        eigs = np.linalg.eigvalsh(H)
        sp = eigenvalue_spacings(eigs)
        all_spacings.extend(sp)
    all_spacings = np.array(all_spacings)
    ks = ks_test_vs_wigner(all_spacings, wigner_cdf_GOE)
    var_theory = 2.0 - np.pi / 2.0
    good_fit = ks < 0.06
    print(f"    Mean spacing: {np.mean(all_spacings):.4f} (should be ~1.0)")
    print(f"    Var spacing: {np.var(all_spacings):.4f} (theory {var_theory:.4f})")
    print(f"    KS statistic: {ks:.4f}")
    print(f"    Good fit: {good_fit}")
    return {
        "mean_spacing": float(np.mean(all_spacings)),
        "var_spacing": float(np.var(all_spacings)),
        "ks_statistic": float(ks),
        "good_fit": bool(good_fit),
        "n_spacings": len(all_spacings)
    }


def experiment_pair_correlation():
    print("  Q4: Pair correlation matches Montgomery-Odlyzko")
    n_matrices = 200
    matrix_size = 500
    n_bins = 80
    x_max = 4.0
    r2_accumulated = None
    valid_matrices = 0
    for _ in range(n_matrices):
        H = gue_matrix(matrix_size)
        eigs = np.linalg.eigvalsh(H)
        x_data, r2 = pair_correlation_single(eigs, n_bins=n_bins, x_max=x_max)
        if len(r2) == n_bins:
            if r2_accumulated is None:
                r2_accumulated = r2.copy()
            else:
                r2_accumulated += r2
            valid_matrices += 1
    if valid_matrices == 0 or r2_accumulated is None:
        return {"mse": float('nan'), "r2_near_zero": float('nan'), "good_fit": False}
    r2_empirical = r2_accumulated / valid_matrices
    r2_theoretical = montgomery_odlyzko(x_data)
    mse = np.mean((r2_empirical - r2_theoretical) ** 2)
    r2_at_zero_emp = np.mean(r2_empirical[:3])
    zero_close = abs(r2_at_zero_emp) < 0.3
    good = mse < 0.1 and zero_close
    print(f"    MSE (empirical vs theoretical): {mse:.4f}")
    print(f"    R_2 near x=0: {r2_at_zero_emp:.4f} (should be ~0)")
    print(f"    Good fit: {good}")
    return {
        "mse": float(mse),
        "r2_near_zero": float(r2_at_zero_emp),
        "good_fit": bool(good),
        "n_matrices": valid_matrices
    }


def experiment_symmetry_classes():
    print("  Q5: GOE/GUE symmetry classification")
    N_trials = 200
    matrix_size = 200
    gue_spacings = []
    goe_spacings = []
    for _ in range(N_trials):
        H = gue_matrix(matrix_size)
        eigs = np.linalg.eigvalsh(H)
        gue_spacings.extend(eigenvalue_spacings(eigs))
        H = goe_matrix(matrix_size)
        eigs = np.linalg.eigvalsh(H)
        goe_spacings.extend(eigenvalue_spacings(eigs))
    gue_spacings = np.array(gue_spacings)
    goe_spacings = np.array(goe_spacings)
    goe_repulsion = np.sum(goe_spacings < 0.01) / len(goe_spacings)
    gue_repulsion = np.sum(gue_spacings < 0.01) / len(gue_spacings)
    both_repel = goe_repulsion < 0.001 and gue_repulsion < 0.001
    print(f"    GOE P(s<0.01)={goe_repulsion:.6f}")
    print(f"    GUE P(s<0.01)={gue_repulsion:.6f}")
    print(f"    Both show level repulsion: {both_repel}")
    return {
        "goe_level_repulsion": float(goe_repulsion),
        "gue_level_repulsion": float(gue_repulsion),
        "both_repel": bool(both_repel)
    }


def run_all():
    results = {}
    results["Q1_level_repulsion"] = {"level_repulsion": experiment_level_repulsion()}
    results["Q2_wigner_gue"] = {"wigner_gue": experiment_wigner_gue()}
    results["Q3_wigner_goe"] = {"wigner_goe": experiment_wigner_goe()}
    results["Q4_pair_correlation"] = {"pair_correlation": experiment_pair_correlation()}
    results["Q5_symmetry_classes"] = {"symmetry_classes": experiment_symmetry_classes()}
    print("\n" + "=" * 60)
    print("  ALL RANDOM MATRIX THEORY PROBES COMPLETE")
    print("=" * 60)
    return results


if __name__ == "__main__":
    np.random.seed(42)
    print("=" * 60)
    print("  RANDOM MATRIX THEORY AS 0/0")
    print("=" * 60)
    results = run_all()
    DATA_DIR.mkdir(exist_ok=True)
    with open(DATA_DIR / "random_matrix_theory_data.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
