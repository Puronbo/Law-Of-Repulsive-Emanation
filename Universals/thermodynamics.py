"""
thermodynamics.py
=================
Quantum thermodynamics of the Hamiltonian flow on the Poincare disk.

Connects four threads:
  1. Partition function Z(beta) = Tr(exp(-beta H)) from spectral eigenvalues
  2. Weyl law: Z(beta) ~ A / (4*pi*beta) as beta -> 0
  3. Selberg trace formula: Z(beta) = Weyl + sum over prime geodesics
  4. Classical limit: Z_cl(beta) = sum exp(-beta E_n), C0 = ground state
"""

import numpy as np, json, math, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from hamiltonian_flow import run_hamiltonian_flow, repulsion_loss

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# 1. Partition functions
# ---------------------------------------------------------------------------

def partition_function(energies: list[float], beta: float) -> float:
    """Z(beta) = sum_n exp(-beta * E_n)."""
    e = np.array(energies)
    return float(np.sum(np.exp(-beta * (e - np.min(e)))))


def partition_function_curve(energies: list[float],
                              betas: np.ndarray) -> np.ndarray:
    """Z(beta) evaluated at an array of inverse temperatures."""
    e = np.array(energies)
    e0 = float(np.min(e))
    shifted = e - e0
    vals = np.array([float(np.sum(np.exp(-b * shifted))) for b in betas])
    return vals


# ---------------------------------------------------------------------------
# 2. Thermodynamic quantities
# ---------------------------------------------------------------------------

def thermodynamics(energies: list[float],
                   betas: np.ndarray) -> dict:
    """Compute thermodynamic quantities from the spectrum.

    Args:
        energies: list of energy levels (eigenvalues or trajectory energies)
        betas: inverse temperature array

    Returns:
        Z: partition function at each beta
        F: free energy F = -log(Z) / beta
        S: entropy S = beta^2 * dF/dbeta
        U: internal energy U = -d(log Z) / dbeta
        C: heat capacity C = dU / dT = -beta^2 * dU/dbeta
        C0: ground state energy = min(energies)
    """
    e = np.array(energies)
    e0 = float(np.min(e))
    shifted = e - e0

    Z = np.array([float(np.sum(np.exp(-b * shifted))) for b in betas])
    logZ = np.log(np.maximum(Z, 1e-300))

    # Internal energy: U = -d(log Z)/dbeta
    U = np.array([float(np.sum(shifted * np.exp(-b * shifted))) / max(Z_i, 1e-300)
                   for b, Z_i in zip(betas, Z)]) + e0

    # Free energy: F = -log(Z) / beta
    F = -logZ / np.maximum(betas, 1e-300)

    # Entropy: S = beta * (U - F)
    S = betas * (U - F)

    # Heat capacity: C = dU/dT = -beta^2 * dU/dbeta
    dU = np.gradient(U, betas)
    C = -betas**2 * dU

    return {
        "betas": betas.tolist(),
        "Z": Z.tolist(),
        "free_energy": F.tolist(),
        "entropy": S.tolist(),
        "internal_energy": U.tolist(),
        "heat_capacity": C.tolist(),
        "ground_state_energy": e0,
        "n_states": len(energies),
    }


# ---------------------------------------------------------------------------
# 3. Weyl law: asymptotic density of states
# ---------------------------------------------------------------------------

def weyl_law(beta: float, area: float, dimension: int = 2) -> float:
    """Weyl asymptotic: Z(beta) ~ A / (4*pi*beta)^{d/2} as beta -> 0."""
    return area / ((4.0 * math.pi * beta) ** (dimension / 2.0))


def verify_weyl_law(eigenvalues: list[float],
                     disk_area: float,
                     betas: np.ndarray) -> dict:
    """Compare numerical partition function to Weyl law."""
    Z_num = partition_function_curve(eigenvalues, betas)
    Z_weyl = np.array([weyl_law(b, disk_area) for b in betas])

    ratio = Z_num / np.maximum(Z_weyl, 1e-300)
    deviation = np.abs(ratio - 1.0)
    mean_dev = float(np.mean(deviation[betas < 0.5]))

    return {
        "betas": betas.tolist(),
        "Z_numerical": Z_num.tolist(),
        "Z_Weyl": Z_weyl.tolist(),
        "ratio_Z_Zweyl": ratio.tolist(),
        "mean_deviation_low_beta": mean_dev,
        "weyl_area": disk_area,
        "dimension": 2,
    }


# ---------------------------------------------------------------------------
# 4. Prime geodesic contribution to the partition function (Selberg trace)
# ---------------------------------------------------------------------------

def geodesic_contribution(beta: float, lengths: list[float],
                           weight: float = 1.0) -> float:
    """Contribution of a set of geodesics to the partition function.

    From the Selberg trace formula, each primitive geodesic of length L
    contributes:
        Z_geo(beta, L) ~ L / sqrt(4*pi*beta) * exp(-L^2/(4*beta))

    This is the leading term of the heat kernel expansion on a hyperbolic
    surface, where the sum over geodesics gives the correction to the
    Weyl law due to the non-trivial topology.
    """
    total = 0.0
    for L in lengths:
        if L > 1e-6:
            total += weight * L / math.sqrt(4.0 * math.pi * beta) * math.exp(-L**2 / (4.0 * beta))
    return total


def selberg_trace_compare(eigenvalues: list[float],
                           geodesic_lengths: list[float],
                           disk_area: float,
                           betas: np.ndarray) -> dict:
    """Compare Z(beta) to Weyl + geodesic corrections."""
    Z_num = partition_function_curve(eigenvalues, betas)
    Z_weyl = np.array([weyl_law(b, disk_area) for b in betas])

    geo_contrib = np.array([geodesic_contribution(b, geodesic_lengths)
                             for b in betas])
    Z_selberg = Z_weyl + geo_contrib

    return {
        "betas": betas.tolist(),
        "Z_numerical": Z_num.tolist(),
        "Z_Weyl": Z_weyl.tolist(),
        "Z_geodesic_correction": geo_contrib.tolist(),
        "Z_Selberg_approx": Z_selberg.tolist(),
        "n_geodesics": len(geodesic_lengths),
    }


# ---------------------------------------------------------------------------
# 5. Main analysis
# ---------------------------------------------------------------------------

def run_thermo_analysis(context: list[str] | None = None) -> dict:
    """Full thermodynamic analysis of the quantum + classical trajectory."""
    if context is None:
        context = ["Tech", "Silicon"]

    q0 = np.array([0.0, 0.0])
    c0 = repulsion_loss(q0, context)

    # ---- Classical trajectory thermodynamics ----
    print("  Computing classical trajectory thermodynamics...")
    traj_con = run_hamiltonian_flow(q0, context, steps=500, dt=0.0005,
                                    friction=0.0, max_grad=5.0)
    traj_diss = run_hamiltonian_flow(q0, context, steps=500, dt=0.002,
                                     friction=0.3, max_grad=5.0)

    betas_cl = np.logspace(-1, 1.5, 30)  # 0.1 to 30
    thermo_con = thermodynamics(traj_con.energies, betas_cl)
    thermo_diss = thermodynamics(traj_diss.energies, betas_cl)

    # ---- Quantum spectrum thermodynamics ----
    print("  Computing quantum thermodynamics from spectral data...")
    spectral_path = os.path.join(BASE_DIR, "spectral_data.json")
    if os.path.exists(spectral_path):
        with open(spectral_path) as f:
            spec = json.load(f)
        eigenvalues = spec.get("eigenvalues", [])
    else:
        eigenvalues = []

    if len(eigenvalues) >= 3:
        betas_q = np.logspace(-1, 2, 40)  # 0.1 to 100
        thermo_q = thermodynamics(eigenvalues, betas_q)

        # Disk area for Weyl law: A = pi * r_max^2 in hyperbolic metric
        r_max = spec.get("grid_params", {}).get("r_max", 0.85)
        # Area of Poincare disk of radius R: A = 4*pi*sinh^2(R/2)
        disk_area = 4.0 * math.pi * (math.sinh(r_max / 2.0)**2)

        # Weyl law verification
        weyl = verify_weyl_law(eigenvalues, disk_area, betas_q[:20])

        # Prime geodesic contribution (Selberg trace)
        prime_path = os.path.join(BASE_DIR, "prime_data.json")
        geo_lengths = []
        if os.path.exists(prime_path):
            with open(prime_path) as f:
                pd = json.load(f)
            # Extract geodesic distances from conservative trajectory
            pgeo = pd.get("conservative", {}).get("prime_geodesics", [])
            geo_lengths = [g["distance"] for g in pgeo[:50] if g["distance"] > 1e-6]

        selberg = selberg_trace_compare(eigenvalues, geo_lengths, disk_area, betas_q[:20])
    else:
        thermo_q = {"ground_state_energy": 0, "n_states": 0}
        weyl = {"mean_deviation_low_beta": float('nan')}
        selberg = {"n_geodesics": 0}
        disk_area = 0.0

    # ---- Results ----
    result = {
        "C0": c0,
        "classical_conservative": {
            "ground_state_energy": thermo_con["ground_state_energy"],
            "low_temp_free_energy": thermo_con["free_energy"][-1],
            "high_temp_entropy": thermo_con["entropy"][0],
        },
        "classical_dissipative": {
            "ground_state_energy": thermo_diss["ground_state_energy"],
            "low_temp_free_energy": thermo_diss["free_energy"][-1],
        },
        "quantum_spectrum": {
            "ground_state_energy": thermo_q["ground_state_energy"],
            "n_states": thermo_q["n_states"],
            "free_energy_curve": thermo_q["free_energy"][:10],
            "entropy_curve": thermo_q["entropy"][:10],
            "heat_capacity_curve": thermo_q["heat_capacity"][:10],
        },
        "weyl_law": {
            "disk_area": disk_area,
            "mean_deviation_low_beta": weyl["mean_deviation_low_beta"],
            "ratio_Z_Zweyl": weyl["ratio_Z_Zweyl"][:5] if "ratio_Z_Zweyl" in weyl else [],
        },
        "selberg_trace": {
            "n_geodesics": selberg["n_geodesics"],
            "geodesic_correction_strength": (max(selberg["Z_geodesic_correction"])
                                              if "Z_geodesic_correction" in selberg
                                              and selberg["Z_geodesic_correction"] else 0),
        },
        "context": context,
    }

    path = os.path.join(BASE_DIR, "thermo_data.json")
    with open(path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"  Saved to {path}")

    print(f"\n  === RESULTS ===")
    print(f"  C0 = {c0:.6f}")
    print(f"  Classical (con): E0 = {thermo_con['ground_state_energy']:.6f}")
    print(f"  Classical (diss): E0 = {thermo_diss['ground_state_energy']:.6f}")
    print(f"  Quantum ground: E0 = {thermo_q['ground_state_energy']:.4f}")
    print(f"  Weyl A_disk = {disk_area:.4f}")
    print(f"  Prime geodesics in trace: {selberg['n_geodesics']}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("  QUANTUM THERMODYNAMICS")
    print("  Partition function, Weyl law, Selberg trace formula")
    print("=" * 60)

    run_thermo_analysis()
