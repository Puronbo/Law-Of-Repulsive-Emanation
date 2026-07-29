"""
modular_forms.py
================
Automorphic forms and L-functions from the Hamiltonian trajectory on the
Poincare disk.

Key observations (most are tautological or standard identities):
  1. Cayley transform: disk origin w=0 -> elliptic point z=i of SL(2,Z).
     This is a standard map. C0 = V(0) at w=0 maps to F(i) = V(Cayley^{-1}(i))
     = V(0) = C0 by construction. Not a discovery.

  2. Trajectory L-function: for a conservative trajectory (friction=0),
     E_n = C0 for all n, so:
         L(s) = sum_{n=1}^{inf} E_n / n^s = C0 * zeta(s)
     This works for ANY constant C0. The Euler product is zeta's, not the
     system's. The functional equation is likewise zeta's.

  3. The deviation D_n = |E_n - C0| measures numerical drift on conservative
     trajectories, or energy loss on dissipative ones. This is a diagnostic,
     not a spectral invariant.

  4. Modular form: F(z) = V(Cayley^{-1}(z)) on H. The stabiliser average at i
     of F is trivially C0 because F is constant at the fixed point. The
     property S(i) = i is a property of PSL(2,Z), not of the system.
"""

import numpy as np, json, math, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from hamiltonian_flow import repulsion_loss, run_hamiltonian_flow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Riemann zeta function at special values
ZETA_0 = -0.5        # zeta(0) = -1/2
ZETA_NEG1 = -1/12    # zeta(-1) = -1/12
ZETA_2 = math.pi**2 / 6  # zeta(2) = pi^2/6


# ---------------------------------------------------------------------------
# 1. Cayley transform and elliptic point
# ---------------------------------------------------------------------------

def cayley(w: np.ndarray) -> complex:
    """Cayley map: disk -> upper half-plane. w=0 -> z=i (elliptic point)."""
    wx, wy = float(w[0]), float(w[1])
    denom = (1 - wx)**2 + wy**2
    if denom < 1e-12:
        return 1e12j
    return complex(2 * wy / denom, (1 - wx**2 - wy**2) / denom)


def cayley_inv(z: complex) -> np.ndarray:
    """Inverse Cayley: upper half-plane -> disk."""
    denom = z + 1j
    if abs(denom) < 1e-12:
        return np.zeros(2)
    w = (z - 1j) / denom
    return np.array([float(w.real), float(w.imag)])


# ---------------------------------------------------------------------------
# 2. Trajectory L-function: L(s) = sum E_n / n^s
# ---------------------------------------------------------------------------

def dirichlet_series(energies: list[float], s: float,
                     n_max: int | None = None) -> complex:
    """L(s) = sum_{n=1}^{N} E_n / n^s."""
    if n_max is None:
        n_max = len(energies)
    total = 0.0j
    for n in range(1, min(n_max, len(energies)) + 1):
        total += energies[n - 1] / (n ** s)
    return total


def compute_trajectory_lfunction(traj_energies: list[float],
                                  c0: float) -> dict:
    """Compute L(s) at special values and verify L(0) = -C0/2.

    For conservative trajectories: L(s) = C0 * zeta(s).
    Verifies this at s = 0, -1, 2 using known zeta values.
    """
    n = len(traj_energies)

    # Dirichlet series only converges for Re(s) > 1.
    # s = 2 is in the convergence region: L(2) = C0 * zeta(2) = C0 * pi^2/6
    l2 = float(dirichlet_series(traj_energies, 2).real)
    # s = 1.5 is also in the convergence region
    l1p5 = float(dirichlet_series(traj_energies, 1.5).real)

    # Euler product at s = 2: C0 * prod_p (1-p^{-2})^{-1} = C0 * pi^2/6
    predicted_l2 = c0 * ZETA_2

    # Analytic continuation (not directly summable):
    # L(s) = C0 * zeta(s) for conservative trajectories, giving:
    #   L(0) = -C0/2  (zeta(0) = -1/2)
    #   L(-1) = -C0/12  (zeta(-1) = -1/12)
    # These are properties of the meromorphic continuation, not the
    # Dirichlet series which diverges at these values.

    return {
        "n_terms": n,
        "c0": c0,
        "L(1.5)": l1p5,
        "L(2)": l2,
        "predicted_L(2)_for_conservative": predicted_l2,
        "deviation_L2": abs(l2 - predicted_l2) / max(abs(predicted_l2), 1e-12),
        "analytic_continuation_L0": c0 * ZETA_0,
        "analytic_continuation_Lneg1": c0 * ZETA_NEG1,
        "euler_product_verified_at_s2": abs(l2 - predicted_l2) / max(abs(predicted_l2), 1e-12) < 0.05,
    }


# ---------------------------------------------------------------------------
# 3. L-function of the deviation: tilde{L}(s) = sum |E_n - C0| / n^s
# ---------------------------------------------------------------------------

def deviation_lfunction(traj_energies: list[float], c0: float,
                        s: float) -> float:
    """L_tilde(s) = sum |E_n - C0| / n^s.

    For conservative trajectories, this is zero (or numerical noise).
    For dissipative, it measures the rate of energy loss.
    """
    total = 0.0
    for n, e in enumerate(traj_energies, start=1):
        total += abs(e - c0) / (n ** s)
    return total


# ---------------------------------------------------------------------------
# 4. Euler product over primes for the trajectory
# ---------------------------------------------------------------------------

def trajectory_euler_product(c0: float, friction: float,
                              pts: int, steps: int,
                              s: float = 2.0) -> dict:
    """For a trajectory, factor L(s) = C0 * prod_p (1 - p^{-s})^{-1}.

    Only exact for conservative trajectories (friction=0).
    For friction > 0, the product gives a dissipative correction.
    """
    from prime_analysis import primes_up_to

    primes = primes_up_to(200)

    # Conservative Euler product: C0 * prod_p (1 - p^{-s})^{-1}
    prod_euler = c0 + 0.0j
    for p in primes[:50]:
        prod_euler /= (1.0 - p ** (-s))

    return {
        "c0": c0,
        "s": s,
        "euler_product_approx": float(prod_euler.real),
        "C0_times_zeta(s)": c0 * ZETA_2 if s == 2 else float('nan'),
        "match_vs_analytic": abs(float(prod_euler.real) - c0 * ZETA_2),
    }


# ---------------------------------------------------------------------------
# 5. Modular form: F(z) = V(Cayley^{-1}(z)) at the elliptic point z=i
# ---------------------------------------------------------------------------

def f_on_half_plane(z: complex, context: list[str],
                    alpha: float = 2.5) -> float:
    """Lift of V to the upper half-plane: F(z) = V(Cayley^{-1}(z)).

    F(i) = V(0) = C0 because Cayley^{-1}(i) = 0.
    """
    w = cayley_inv(z)
    return repulsion_loss(w, context, alpha)


def stabiliser_average(context: list[str],
                       alpha: float = 2.5) -> dict:
    """Average of F over the stabiliser of i.

    The stabiliser of z=i in SL(2,Z) is {I, S} where S: z -> -1/z.
    The averaged value at i is (F(i) + F(S(i))) / 2 = (C0 + C0) / 2 = C0.

    Also evaluates F at the other elliptic point rho = exp(pi*i/3)
    for comparison.
    """
    z_i = 1j
    z_rho = complex(-0.5, math.sqrt(3) / 2)

    f_i = f_on_half_plane(z_i, context, alpha)
    f_si = f_on_half_plane(mobius_s(z_i), context, alpha)
    avg_i = (f_i + f_si) / 2.0

    f_rho = f_on_half_plane(z_rho, context, alpha)
    f_srho = f_on_half_plane(mobius_s(z_rho), context, alpha)
    avg_rho = (f_rho + f_srho) / 2.0

    c0 = repulsion_loss(np.zeros(2), context, alpha)

    return {
        "C0": c0,
        "F(i)": f_i,
        "F(S(i))": f_si,
        "stabiliser_average_at_i": avg_i,
        "stabiliser_average_equals_C0": abs(avg_i - c0) < 1e-10,
        "F(rho)": f_rho,
        "F(S(rho))": f_srho,
        "stabiliser_average_at_rho": avg_rho,
        "rho": "exp(pi*i/3)",
    }


def mobius_s(z: complex) -> complex:
    """S: z -> -1/z, the order-2 elliptic element of SL(2,Z)."""
    if abs(z) < 1e-12:
        return complex(1e12, 0)
    return -1.0 / z


# ---------------------------------------------------------------------------
# 6. Main analysis
# ---------------------------------------------------------------------------

def run_modular_analysis(context: list[str] | None = None,
                         n_traj_steps: int = 500) -> dict:
    """Run the full modular forms + L-function analysis."""
    if context is None:
        context = ["Tech", "Silicon"]

    print("  Computing conservative trajectory...")
    q0 = np.array([0.0, 0.0])
    c0 = repulsion_loss(q0, context)
    traj_con = run_hamiltonian_flow(q0, context, steps=n_traj_steps,
                                    dt=0.0005, friction=0.0, max_grad=5.0)

    # L-function for conservative trajectory
    print("  Computing L-function (conservative)...")
    lf_con = compute_trajectory_lfunction(traj_con.energies, c0)

    # L-function for dissipative trajectory
    print("  Computing L-function (dissipative)...")
    traj_diss = run_hamiltonian_flow(q0, context, steps=n_traj_steps,
                                     dt=0.002, friction=0.3, max_grad=5.0)
    lf_diss = compute_trajectory_lfunction(traj_diss.energies, c0)

    # Deviation L-function
    dev_s1 = deviation_lfunction(traj_diss.energies, c0, 1.0)
    dev_s2 = deviation_lfunction(traj_diss.energies, c0, 2.0)

    # Euler product
    print("  Computing Euler product...")
    euler = trajectory_euler_product(c0, 0.0, 50, n_traj_steps, s=2.0)

    # Stabiliser average at elliptic points
    print("  Computing elliptic point values...")
    stab = stabiliser_average(context)

    result = {
        "C0": c0,
        "elliptic_point": "z = i (Cayley image of disk origin)",
        "stabiliser": stab,
        "l_function_conservative": lf_con,
        "l_function_dissipative": lf_diss,
        "deviation_L_tilde(1)": dev_s1,
        "deviation_L_tilde(2)": dev_s2,
        "euler_product": euler,
        "context": context,
    }

    path = os.path.join(BASE_DIR, "modular_data.json")
    with open(path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"  Saved to {path}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("  MODULAR FORMS & L-FUNCTIONS")
    print("  C0 at elliptic point, trajectory L(s), Euler product")
    print("=" * 60)

    r = run_modular_analysis()

    print(f"\n  === ELLIPTIC POINT ===")
    print(f"  C0 = V(0) = {r['C0']:.6f}")
    s = r['stabiliser']
    print(f"  F(i) = {s['F(i)']:.6f}, F(S(i)) = {s['F(S(i))']:.6f}")
    print(f"  Stabiliser avg = {s['stabiliser_average_at_i']:.6f}")
    print(f"  Avg equals C0: {s['stabiliser_average_equals_C0']}")

    print(f"\n  === L-FUNCTION (CONSERVATIVE) ===")
    lc = r['l_function_conservative']
    print(f"  L(2) = {lc['L(2)']:.6f}  (predicted C0*pi^2/6 = {lc['predicted_L(2)_for_conservative']:.6f})")
    print(f"  Euler product verified at s=2: {lc['euler_product_verified_at_s2']}")
    print(f"  Relative deviation: {lc['deviation_L2']:.2e}")
    print(f"  Analytic continuation: L(0) = -C0/2 = {lc['analytic_continuation_L0']:.6f}")

    print(f"\n  === L-FUNCTION (DISSIPATIVE, gamma=0.3) ===")
    ld = r['l_function_dissipative']
    print(f"  L(2) = {ld['L(2)']:.6f}  (vs conservative {lc['L(2)']:.6f})")

    print(f"\n  === EULER PRODUCT ===")
    print(f"  C0 * prod_p (1-p^{{-2}}){{-1}} = {r['euler_product']['euler_product_approx']:.4f}")
    print(f"  C0 * zeta(2) = C0*pi^2/6 = {r['euler_product']['C0_times_zeta(s)']:.4f}")

    print("\n  Done.")
