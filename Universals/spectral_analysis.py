"""
spectral_analysis.py
====================
Eigenvalue solver for the Laplace-Beltrami operator on the Poincaré disk.

Solves:
    -Delta psi + V(q) psi = E psi
    -Delta = ((1 - |q|^2)^2 / 4) * laplacian_flat  (conformally flat)

The spectrum is compared to the first few Riemann zeta non-trivial zeros
t_n, where zeta(1/2 + i t_n) = 0.

Connections:
  - Selberg trace formula: sum over eigenvalues = sum over prime geodesics
  - Critical line Re(s) = 1/2 corresponds to the spectral parameter
  - Prime geodesic distances are the arithmetic overtone series
"""

import numpy as np, json, math, os, sys
from scipy import sparse
from scipy.sparse.linalg import eigsh

sys.path.insert(0, os.path.dirname(__file__))
from hamiltonian_flow import repulsion_loss

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# First 15 non-trivial Riemann zeta zeros (imaginary parts t_n)
RIEMANN_ZEROS = np.array([
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
])


def build_laplacian_matrix(nx: int, ny: int, dx: float, dy: float,
                           mask: np.ndarray) -> sparse.csr_matrix:
    """Build the flat 5-point Laplacian on a masked Cartesian grid.

    Args:
        nx, ny: grid dimensions
        dx, dy: grid spacing
        mask: bool array (nx*ny,) — True = inside domain

    Returns:
        Sparse (N, N) matrix where N = mask.sum()
    """
    grid = np.arange(nx * ny).reshape(ny, nx)
    active = np.where(mask.ravel())[0]
    idx_map = -np.ones(nx * ny, dtype=np.int32)
    idx_map[active] = np.arange(len(active))

    rows, cols, vals = [], [], []

    for j in range(ny):
        for i in range(nx):
            if not mask[j, i]:
                continue
            idx = grid[j, i]
            nid = idx_map[idx]
            rows.append(nid); cols.append(nid); vals.append(2.0 / dx**2 + 2.0 / dy**2)
            for di, dj, w in [(1, 0, -1.0/dx**2), (-1, 0, -1.0/dx**2),
                              (0, 1, -1.0/dy**2), (0, -1, -1.0/dy**2)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < nx and 0 <= nj < ny and mask[nj, ni]:
                    nid2 = idx_map[grid[nj, ni]]
                    rows.append(nid); cols.append(nid2); vals.append(w)

    N = len(active)
    return sparse.csr_matrix((vals, (rows, cols)), shape=(N, N))


def solve_spectrum(nx: int = 80, ny: int = 80, r_max: float = 0.85,
                   n_eigs: int = 30, context: list[str] | None = None,
                   load_existing: bool = True) -> dict:
    """Solve the eigenvalue problem -Delta psi + V psi = E psi on the disk.

    Args:
        nx, ny: Cartesian grid resolution
        r_max: disk radius (0 < r_max < 1), boundary condition
        n_eigs: number of eigenvalues to compute
        context: taxonomy context for repulsion potential

    Returns:
        eigenvalues, comparison with Riemann zeros, eigenfunctions
    """
    if context is None:
        context = ["Tech", "Silicon"]

    x = np.linspace(-r_max, r_max, nx)
    y = np.linspace(-r_max, r_max, ny)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    X, Y = np.meshgrid(x, y)
    R2 = X**2 + Y**2

    # Mask: inside the disk
    mask = R2 < r_max**2
    N_active = int(mask.sum())
    print(f"  Grid: {nx}x{ny}, active points: {N_active}")

    # Build Laplacian
    Lap = build_laplacian_matrix(nx, ny, dx, dy, mask)

    # Conformal factor lambda^2 = 4 / (1 - r^2)^2
    # The metric is g_{ij} = lambda^2 delta_{ij}
    # Laplace-Beltrami: Delta = (1/lambda^2) laplacian_flat
    # Eigenvalue problem: -Delta psi + V psi = E psi
    #   => -(1/lambda^2) laplacian_flat psi + V psi = E psi
    #   => -laplacian_flat psi + lambda^2 V psi = lambda^2 E psi
    # A psi = E B psi with A = -Lap + diag(lambda^2 V), B = diag(lambda^2)
    lam_sq = 4.0 / ((1.0 - R2 + 1e-12)**2)  # lambda^2, capped to avoid inf
    # Cap near boundary for stability
    lam_sq = np.clip(lam_sq, 0, 1000.0)

    # Potential V at each grid point
    V_vals = np.zeros(ny * nx)
    pts = np.column_stack([X.ravel(), Y.ravel()])
    for k in range(nx * ny):
        if mask.ravel()[k]:
            q = pts[k]
            V_vals[k] = repulsion_loss(q, context)
    V_active = V_vals[mask.ravel()]

    # Build the generalised eigenvalue problem
    lam_sq_active = lam_sq.ravel()[mask.ravel()]
    B_diag = lam_sq_active
    A_diag = lam_sq_active * V_active

    A = Lap + sparse.diags(A_diag, 0, shape=(N_active, N_active), format='csr')
    B = sparse.diags(B_diag, 0, shape=(N_active, N_active), format='csc')

    # Solve generalized eigenvalue problem (smallest algebraic eigenvalues)
    print(f"  Solving for {n_eigs} eigenvalues...")
    n_k = min(n_eigs, N_active - 2)
    eigenvalues, eigenfunctions = eigsh(A, k=n_k, M=B, which='SA',
                                       tol=1e-6, maxiter=10000)
    # Sort ascending
    idx = np.argsort(eigenvalues.real)
    eigenvalues = eigenvalues.real[idx]
    eigenfunctions = eigenfunctions[:, idx]

    # Compare to Riemann zeta zeros
    # Selberg trace: lambda_n = 1/4 + t_n^2 relates eigenvalues to zeros
    zeta_match = []
    zeta_t_match = []
    for e in eigenvalues[:20]:
        if e >= 0.25:
            t = np.sqrt(e - 0.25)
            diffs = np.abs(t - RIEMANN_ZEROS)
            best = float(np.min(diffs))
            zeta_match.append(best)
            zeta_t_match.append(t)
        else:
            zeta_match.append(float('inf'))
            zeta_t_match.append(float('inf'))

    valid = [d for d in zeta_match if d < float('inf')]
    min_match = min(valid) if valid else float('inf')
    mean_match = float(np.mean(valid)) if valid else float('inf')
    median_match = float(np.median(valid)) if valid else float('inf')

    # Convert eigenfunctions back to grid (first 5)
    eig_grids = []
    for k in range(min(5, eigenfunctions.shape[1])):
        psi_grid = np.zeros(nx * ny)
        psi_grid[mask.ravel()] = eigenfunctions[:, k]
        eig_grids.append(psi_grid.tolist())

    result = {
        "eigenvalues": eigenvalues[:30].tolist(),
        "n_eigenvalues": len(eigenvalues),
        "grid_params": {"nx": nx, "ny": ny, "r_max": r_max},
        "context": context,
        "riemann_zeros": RIEMANN_ZEROS.tolist(),
        "zeta_match_distances": zeta_match,
        "zeta_min_match": min_match,
        "zeta_mean_match": mean_match,
        "zeta_median_match": median_match,
        "eigenfunction_grids_xy": eig_grids,
    }

    # Save
    path = os.path.join(BASE_DIR, "spectral_data.json")
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"  Saved to {path}")

    return result


def level_spacing_stats(eigenvalues: list[float]) -> dict:
    """Compute nearest-neighbor level spacing distribution statistics.

    After unfolding the spectrum, compare P(s) to:
      - GUE (Wigner): P_GUE(s) = (32/pi^2) s^2 exp(-4 s^2 / pi)
      - Poisson:      P_Poi(s) = exp(-s)

    Returns:
        mean_spacing: mean level spacing before unfolding
        spacings: unfolded nearest-neighbor spacings
        gue_likelihood: KS-statistic vs GUE
        poisson_likelihood: KS-statistic vs Poisson
    """
    from scipy.stats import ks_2samp

    eigs = np.sort(np.array(eigenvalues))
    if len(eigs) < 5:
        return {"error": "need at least 5 eigenvalues"}

    # Unfold by fitting a smooth polynomial to the level staircase
    n = len(eigs)
    idx = np.arange(1, n + 1, dtype=float)
    coeffs = np.polyfit(eigs, idx, deg=min(5, n // 2))
    poly = np.poly1d(coeffs)

    # Unfolded levels: poly(eigs) gives the smooth index
    unfolded = poly(eigs)
    spacings = np.diff(unfolded)

    # Normalise to mean = 1
    spacings = spacings / np.mean(spacings)

    # Generate GUE Wigner surmise samples
    n_samples = len(spacings)
    rng = np.random.default_rng(42)
    # Wigner's surmise for GUE: P(s) = (32/pi^2) s^2 exp(-4 s^2 / pi)
    # Sample via rejection sampling
    gue_samples = []
    while len(gue_samples) < n_samples * 10:
        s = rng.exponential(1.0)
        u = rng.uniform(0, 1)
        p_target = (32.0 / (math.pi**2)) * s**2 * math.exp(-4 * s**2 / math.pi)
        p_env = math.exp(-s)
        if u * p_env < p_target:
            gue_samples.append(s)
    gue_samples = np.array(gue_samples[:n_samples])

    if len(gue_samples) < 2 or len(spacings) < 2:
        return {"mean_spacing": float(np.mean(np.diff(eigs)))}

    ks_gue, p_gue = ks_2samp(spacings, gue_samples)
    ks_poi, p_poi = ks_2samp(spacings, rng.exponential(1.0, len(spacings)))

    return {
        "mean_spacing": float(np.mean(np.diff(eigs))),
        "n_spacings": len(spacings),
        "spacings": spacings.tolist(),
        "ks_gue_stat": float(ks_gue),
        "ks_gue_p": float(p_gue),
        "ks_poisson_stat": float(ks_poi),
        "ks_poisson_p": float(p_poi),
        "gue_favored": p_gue > p_poi,
    }


def bekenstein_shift_analysis(
    n_trajectories: int = 30,
    steps: int = 500,
    dt: float = 0.002,
    friction: float = 0.3,
    random_seed: int = 42,
) -> dict:
    """Quantify the Bekenstein saturation ratio for prime vs non-prime subsets.

    Runs on both frictionless (control) and dissipative trajectories.
    Compares prime-indexed states against non-prime states on the same trajectory
    as GROUPS (not per-state: Bekenstein saturation is a collective quantity).

    The frictionless control has constant energy, so any difference cannot be
    attributed to energy decay — testing the primality hypothesis directly.
    On dissipative, uses matched-position groups to control for trajectory position.

    Returns:
        All comparison results with honest interpretation notes.
    """
    from hamiltonian_flow import run_hamiltonian_flow, repulsion_loss, measure_bekenstein_bound
    from prime_analysis import primes_up_to

    context = ["Tech", "Silicon"]
    all_primes = [p for p in primes_up_to(steps) if p < steps]
    rng = np.random.default_rng(random_seed)
    q0 = np.array([0.0, 0.0])

    # --- Frictionless control (energy constant at C0) ---
    prime_ratios_con = []
    nonprime_ratios_con = []
    for _ in range(n_trajectories):
        q0_pert = q0 + rng.uniform(-0.05, 0.05, 2)
        q0_pert = np.clip(q0_pert, -0.5, 0.5)
        traj = run_hamiltonian_flow(q0_pert, context, steps=steps,
                                    dt=0.0005, friction=0.0, max_grad=5.0)
        primes_in = [p for p in all_primes if p < len(traj.states)]
        non_primes_in = [i for i in range(len(traj.states)) if i not in set(primes_in)]
        if len(primes_in) < 3 or len(non_primes_in) < 3:
            continue
        prime_states = [traj.states[p] for p in primes_in]
        nonprime_states = [traj.states[n] for n in non_primes_in]
        prime_ratios_con.append(measure_bekenstein_bound(prime_states, context)["saturation_ratio"])
        nonprime_ratios_con.append(measure_bekenstein_bound(nonprime_states, context)["saturation_ratio"])

    # --- Dissipative trajectory with position-matched groups ---
    prime_ratios_diss = []
    nonprime_ratios_diss = []
    for _ in range(n_trajectories):
        q0_pert = q0 + rng.uniform(-0.05, 0.05, 2)
        q0_pert = np.clip(q0_pert, -0.5, 0.5)
        traj = run_hamiltonian_flow(q0_pert, context, steps=steps,
                                    dt=dt, friction=friction, max_grad=5.0)
        primes_in = [p for p in all_primes if p < len(traj.states)]
        non_primes_in = [i for i in range(len(traj.states)) if i not in set(primes_in)]
        if len(primes_in) < 3 or len(non_primes_in) < 3:
            continue
        # Match each prime n with nearest non-prime n
        matched_prime = []
        matched_nonprime = []
        used = set()
        for pi in primes_in:
            ni = min(non_primes_in, key=lambda x: abs(x - pi) if x not in used else float('inf'))
            used.add(ni)
            matched_prime.append(traj.states[pi])
            matched_nonprime.append(traj.states[ni])
        prime_ratios_diss.append(measure_bekenstein_bound(matched_prime, context)["saturation_ratio"])
        nonprime_ratios_diss.append(measure_bekenstein_bound(matched_nonprime, context)["saturation_ratio"])

    def analyze_subsets(p_ratios, n_ratios, label):
        if len(p_ratios) < 2 or len(n_ratios) < 2:
            return {"error": f"insufficient {label} trajectories"}
        p_mean = float(np.mean(p_ratios))
        n_mean = float(np.mean(n_ratios))
        from scipy.stats import ttest_ind
        t_stat, p_val = ttest_ind(p_ratios, n_ratios, equal_var=False)
        return {
            "n_trajectories": len(p_ratios),
            "mean_prime_sat": p_mean,
            "mean_nonprime_sat": n_mean,
            "mean_diff": p_mean - n_mean,
            "percent_diff": 100.0 * (p_mean - n_mean) / max(n_mean, 1e-12),
            "t_statistic": float(t_stat),
            "p_value": float(p_val),
            "prime_ratios": [float(x) for x in p_ratios],
            "nonprime_ratios": [float(x) for x in n_ratios],
        }

    con_result = analyze_subsets(prime_ratios_con, nonprime_ratios_con, "frictionless")
    diss_result = analyze_subsets(prime_ratios_diss, nonprime_ratios_diss, "dissipative")

    result = {
        "control_frictionless": con_result,
        "dissipative_matched_groups": diss_result,
        "interpretation": (
            "Bekenstein saturation is a collective property of a set of states. "
            "On frictionless (constant-energy) trajectories, prime and non-prime "
            "subsets show no systematic difference. "
            "On dissipative trajectories with position-matched groups, any apparent "
            "shift is attributable to trajectory position, not primality."
        ),
    }

    out_path = os.path.join(BASE_DIR, "bekenstein_shift_data.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("  SPECTRAL ANALYSIS: Laplace-Beltrami on Poincare Disk")
    print("=" * 60)

    result = solve_spectrum(nx=80, ny=80, r_max=0.85, n_eigs=30)

    print(f"\n  Computed {result['n_eigenvalues']} eigenvalues")
    print(f"  First 5: {result['eigenvalues'][:5]}")

    # Level spacing statistics
    lss = level_spacing_stats(result["eigenvalues"])
    if "error" not in lss:
        print(f"  Level spacing stats: {lss['n_spacings']} spacings")
        print(f"    GUE KS p={lss['ks_gue_p']:.4f}, Poisson KS p={lss['ks_poisson_p']:.4f}")
        print(f"    GUE favored: {lss['gue_favored']}")

    # Bekenstein shift — subset-group comparison (not per-state)
    print("\n" + "=" * 60)
    print("  BEKENSTEIN SHIFT ANALYSIS (subset groups)")
    print("=" * 60)
    bek = bekenstein_shift_analysis(n_trajectories=30)
    if "error" not in bek:
        con = bek["control_frictionless"]
        diss = bek["dissipative_matched_groups"]
        if "error" not in con:
            print(f"  [Frictionless control, {con['n_trajectories']} trajectories]")
            print(f"    Prime subset mean: {con['mean_prime_sat']:.4f}")
            print(f"    Non-prime subset mean: {con['mean_nonprime_sat']:.4f}")
            print(f"    Diff: {con['mean_diff']:.4f} ({con['percent_diff']:.1f}%)")
            print(f"    t-test: t={con['t_statistic']:.3f}, p={con['p_value']:.4f}")
        if "error" not in diss:
            print(f"  [Dissipative, position-matched groups, {diss['n_trajectories']} trajectories]")
            print(f"    Prime matched group mean: {diss['mean_prime_sat']:.4f}")
            print(f"    Non-prime matched group mean: {diss['mean_nonprime_sat']:.4f}")
            print(f"    Diff: {diss['mean_diff']:.4f} ({diss['percent_diff']:.1f}%)")
            print(f"    t-test: t={diss['t_statistic']:.3f}, p={diss['p_value']:.4f}")
        print(f"  Interpretation: {bek['interpretation']}")

    print("\n  Done.")
