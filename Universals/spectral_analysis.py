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
    n_primes: int = 50,
    random_seed: int = 42,
) -> dict:
    """Quantify the Bekenstein saturation shift between prime and random states.

    Runs multiple trajectories, computes the saturation ratio for prime-indexed
    states vs random subsets of the same size, and tests for a systematic shift.

    Returns:
        prime_ratios: list of saturation ratios for prime-indexed states
        random_ratios: list of saturation ratios for random subsets
        mean_shift: mean(prime) - mean(random)
        t_stat: Welch t-statistic for the difference
        p_value: significance of the shift
    """
    from hamiltonian_flow import run_hamiltonian_flow, repulsion_loss, measure_bekenstein_bound
    from prime_analysis import primes_up_to

    context = ["Tech", "Silicon"]
    q0 = np.array([0.0, 0.0])
    all_primes = [p for p in primes_up_to(steps) if p < steps]

    prime_ratios = []
    random_ratios = []
    rng = np.random.default_rng(random_seed)

    for _ in range(n_trajectories):
        q0_perturbed = q0 + rng.uniform(-0.05, 0.05, 2)
        q0_perturbed = np.clip(q0_perturbed, -0.5, 0.5)
        traj = run_hamiltonian_flow(q0_perturbed, context, steps=steps,
                                    dt=dt, friction=friction, max_grad=5.0)

        primes_in_traj = [p for p in all_primes if p < len(traj.states)]
        if len(primes_in_traj) < 3:
            continue

        prime_states = [traj.states[p] for p in primes_in_traj]
        bek_p = measure_bekenstein_bound(prime_states, context)
        prime_ratios.append(bek_p["saturation_ratio"])

        # Random subsets of same size
        for _ in range(5):
            rand_idx = rng.choice(len(traj.states), size=len(primes_in_traj), replace=False)
            rand_states = [traj.states[i] for i in rand_idx]
            bek_r = measure_bekenstein_bound(rand_states, context)
            random_ratios.append(bek_r["saturation_ratio"])

    if len(prime_ratios) < 2 or len(random_ratios) < 2:
        return {"error": "insufficient trajectories"}

    from scipy.stats import ttest_ind
    t_stat, p_val = ttest_ind(prime_ratios, random_ratios, equal_var=False)

    mean_shift = float(np.mean(prime_ratios) - np.mean(random_ratios))
    percent_shift = 100.0 * mean_shift / max(np.mean(random_ratios), 1e-12)

    result = {
        "prime_ratios": prime_ratios,
        "random_ratios": random_ratios,
        "mean_prime_ratio": float(np.mean(prime_ratios)),
        "mean_random_ratio": float(np.mean(random_ratios)),
        "mean_shift": mean_shift,
        "percent_shift": percent_shift,
        "t_statistic": float(t_stat),
        "p_value": float(p_val),
        "n_prime_trajectories": len(prime_ratios),
        "n_random_subsets": len(random_ratios),
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

    # Bekenstein shift
    print("\n" + "=" * 60)
    print("  BEKENSTEIN SHIFT ANALYSIS")
    print("=" * 60)
    bek = bekenstein_shift_analysis(n_trajectories=60)
    if "error" not in bek:
        print(f"  Prime mean saturation: {bek['mean_prime_ratio']:.4f}")
        print(f"  Random mean saturation: {bek['mean_random_ratio']:.4f}")
        print(f"  Shift: {bek['mean_shift']:.4f} ({bek['percent_shift']:.1f}%)")
        print(f"  t = {bek['t_statistic']:.3f}, p = {bek['p_value']:.4f}")

    print("\n  Done.")
