"""
hamiltonian_flow.py

True Hamiltonian mechanics on the Poincare disk.

Extends the Puno Calculus engine with conjugate momenta, enabling
symplectic integration and conservation-law diagnostics. The Poincare
disk is treated as a Riemannian manifold with the hyperbolic metric,
and the Hamiltonian is constructed from the repulsion loss potential
plus kinetic energy in the momentum coordinates.

Physics correspondences:
  - q_i (position) = knowledge probe coordinates on the disk
  - p_i (momentum) = conjugate momenta encoding trajectory inertia
  - H(q, p) = total energy = kinetic + potential (repulsion loss)
  - dH/dt = 0 along trajectories (energy conservation)
  - T-symmetry: (q, p, t) -> (q, -p, -t)
  - Poincare recurrence: return to (q_0, p_0) after tau ~ exp(S)
"""

from __future__ import annotations

import math
import numpy as np
from dataclasses import dataclass, field


def hyperbolic_dist(u: np.ndarray, v: np.ndarray) -> float:
    """Exact geodesic distance in the Poincare disk."""
    sq_norm_u = float(np.sum(u**2))
    sq_norm_v = float(np.sum(v**2))
    sq_dist = float(np.sum((u - v)**2))
    denom = max((1.0 - sq_norm_u) * (1.0 - sq_norm_v), 1e-12)
    return float(np.arccosh(1.0 + 2.0 * sq_dist / denom))


def riemannian_metric(x: np.ndarray) -> float:
    """Inverse conformal factor: 1/lambda^2 = (1 - ||x||^2)^2 / 4.

    This is the inverse metric component g^{ij} = (1/lambda^2) delta^{ij}.
    Used in Hamilton's equations: dq/dt = g^{ij} p_j = (1/lambda^2) p_i,
    and kinetic energy: K = (1/2) g^{ij} p_i p_j.

    Note: The conformal factor lambda^2 = 4/(1-||x||^2)^2 is returned by
    manifold.poincare.riemannian_scale(). The inverse is used here because
    the Hamiltonian formulation requires the inverse metric.
    """
    return ((1.0 - float(np.sum(x**2)))**2) / 4.0


def project_to_disk(x: np.ndarray, max_norm: float = 0.99) -> np.ndarray:
    r = float(np.linalg.norm(x))
    if r >= max_norm:
        x = (x / r) * max_norm
    return x


# Known taxonomy positions
POSITIONS = {
    "Origin": np.array([0.0, 0.0]),
    "System": np.array([-0.15, 0.10]),
    "Matter": np.array([0.18, -0.05]),
    "Idea":   np.array([-0.05, -0.18]),
    "Tech":   np.array([-0.40, 0.30]),
    "Bio":    np.array([0.45, -0.20]),
    "Art":    np.array([-0.10, -0.45]),
    "Mammal": np.array([0.70, -0.35]),
    "Silicon":np.array([-0.65, 0.50]),
    "Music":  np.array([-0.20, -0.75]),
}


def repulsion_loss(xq: np.ndarray, context: list[str], alpha: float = 2.5) -> float:
    """Potential energy: sum of squared repulsion from non-affinity nodes."""
    loss = 0.0
    for node_id, pos in POSITIONS.items():
        if node_id in context:
            continue
        d = hyperbolic_dist(xq, pos)
        if d < alpha:
            loss += (alpha - d)**2
    return loss


def repulsion_gradient(xq: np.ndarray, context: list[str], alpha: float = 2.5) -> np.ndarray:
    """Numerical gradient of repulsion loss w.r.t. position."""
    grad = np.zeros(2)
    eps = 1e-5
    for node_id, pos in POSITIONS.items():
        if node_id in context:
            continue
        d = hyperbolic_dist(xq, pos)
        if d < alpha:
            for i in range(2):
                xq_p = xq.copy()
                xq_p[i] += eps
                d_p = hyperbolic_dist(xq_p, pos)
                grad[i] += (max(0, alpha - d_p)**2 - max(0, alpha - d)**2) / eps
    return grad


@dataclass
class HamiltonianState:
    """Phase-space point (q, p) on the Poincare disk."""
    q: np.ndarray  # position on disk
    p: np.ndarray  # conjugate momentum

    @property
    def kinetic_energy(self) -> float:
        """K = (1/2) g^{ij} p_i p_j where g^{ij} = (1/lambda^2) delta^{ij}.

        riemannian_metric() returns 1/lambda^2 = (1-||x||^2)^2/4,
        which IS the inverse metric component g^{ij}/delta^{ij}.
        """
        lam_sq = riemannian_metric(self.q)
        if lam_sq < 1e-12:
            lam_sq = 1e-12
        return 0.5 * lam_sq * float(np.sum(self.p**2))

    def potential_energy(self, context: list[str]) -> float:
        """V(q) = repulsion loss."""
        return repulsion_loss(self.q, context)

    def total_energy(self, context: list[str]) -> float:
        return self.kinetic_energy + self.potential_energy(context)


@dataclass
class HamiltonianTrajectory:
    """Full phase-space trajectory with conservation diagnostics."""
    states: list[HamiltonianState] = field(default_factory=list)
    energies: list[float] = field(default_factory=list)
    times: list[float] = field(default_factory=list)

    @property
    def energy_drift(self) -> float:
        """Max fractional energy drift (should be near zero for symplectic integration)."""
        if len(self.energies) < 2:
            return 0.0
        e0 = self.energies[0]
        if abs(e0) < 1e-12:
            return max(self.energies) - min(self.energies)
        return max(abs(e - e0) / abs(e0) for e in self.energies)

    @property
    def position_trace(self) -> list[list[float]]:
        return [s.q.tolist() for s in self.states]

    @property
    def momentum_trace(self) -> list[list[float]]:
        return [s.p.tolist() for s in self.states]


def leapfrog_step(state: HamiltonianState, context: list[str],
                  dt: float, alpha: float = 2.5,
                  friction: float = 0.5,
                  max_grad: float | None = None) -> HamiltonianState:
    """
    Symplectic leapfrog (Verlet) integration of Hamilton's equations on the
    Poincare disk, with optional dissipative friction.

    Hamilton's equations:
        dq/dt =  (1/lambda^2) * p
        dp/dt = -grad V(q) - gamma * p

    When friction=0, the system is conservative (T-symmetric).
    When friction>0, energy dissipates and T-symmetry is broken.

    Gradient clamping (max_grad) is only applied when friction > 0,
    to preserve the conservative structure for T-symmetry tests.
    """
    lam_sq = riemannian_metric(state.q)
    if lam_sq < 1e-4:
        lam_sq = 1e-4

    # Force computation
    grad_v = repulsion_gradient(state.q, context, alpha)
    if max_grad is not None and friction > 0:
        grad_norm = float(np.linalg.norm(grad_v))
        if grad_norm > max_grad:
            grad_v = grad_v * (max_grad / grad_norm)

    # Half-step momentum kick (force + friction)
    p_half = state.p - 0.5 * dt * (grad_v + friction * state.p)

    # Full-step position drift
    # dq/dt = g^{ij} p_j = (1/lambda^2) p_i
    # riemannian_metric returns 1/lambda^2, so velocity = lam_sq * p
    velocity = p_half * lam_sq
    q_new = state.q + dt * velocity
    q_new = project_to_disk(q_new)

    # Force at new position
    grad_v_new = repulsion_gradient(q_new, context, alpha)
    if max_grad is not None and friction > 0:
        grad_norm_new = float(np.linalg.norm(grad_v_new))
        if grad_norm_new > max_grad:
            grad_v_new = grad_v_new * (max_grad / grad_norm_new)

    # Half-step momentum kick with friction damping
    p_new = p_half - 0.5 * dt * (grad_v_new + friction * p_half)
    if friction > 0:
        p_new = p_new / (1.0 + 0.5 * dt * friction)

    return HamiltonianState(q=q_new, p=p_new)


def run_hamiltonian_flow(
    x0: np.ndarray,
    context: list[str],
    steps: int = 500,
    dt: float = 0.005,
    alpha: float = 2.5,
    friction: float = 0.5,
    max_grad: float | None = None,
    p0: np.ndarray | None = None,
) -> HamiltonianTrajectory:
    """
    Evolve a probe under Hamilton's equations on the Poincare disk
    with optional dissipative friction.

    When friction=0, the system is conservative and T-symmetric.
    When friction>0, energy dissipates toward the attractor.
    """
    if p0 is None:
        p0 = np.zeros(2)

    state = HamiltonianState(q=x0.copy(), p=p0.copy())
    traj = HamiltonianTrajectory()
    traj.states.append(HamiltonianState(q=state.q.copy(), p=state.p.copy()))
    traj.energies.append(state.total_energy(context))
    traj.times.append(0.0)

    for i in range(steps):
        state = leapfrog_step(state, context, dt, alpha, friction=friction, max_grad=max_grad)
        traj.states.append(HamiltonianState(q=state.q.copy(), p=state.p.copy()))
        traj.energies.append(state.total_energy(context))
        traj.times.append((i + 1) * dt)

    return traj


def hamiltonian_time_reverse(traj: HamiltonianTrajectory, context: list[str],
                             dt: float = 0.005,
                             friction: float = 0.5,
                             max_grad: float | None = None) -> HamiltonianTrajectory:
    """
    Time-reverse a Hamiltonian trajectory.

    T-symmetry: (q, p, t) -> (q, -p, -t)

    For conservative systems (friction=0), the reversed trajectory
    exactly retraces the forward path. For dissipative systems,
    friction breaks T-symmetry.
    """
    if not traj.states:
        return HamiltonianTrajectory()

    final_state = traj.states[-1]
    reversed_state = HamiltonianState(
        q=final_state.q.copy(),
        p=-final_state.p.copy(),  # Negate momentum: T-symmetry
    )

    reversed_traj = HamiltonianTrajectory()
    reversed_traj.states.append(HamiltonianState(q=reversed_state.q.copy(), p=reversed_state.p.copy()))
    reversed_traj.energies.append(reversed_state.total_energy(context))
    reversed_traj.times.append(0.0)

    steps = len(traj.states) - 1
    for i in range(steps):
        reversed_state = leapfrog_step(reversed_state, context, dt, friction=friction, max_grad=max_grad)
        reversed_traj.states.append(HamiltonianState(q=reversed_state.q.copy(), p=reversed_state.p.copy()))
        reversed_traj.energies.append(reversed_state.total_energy(context))
        reversed_traj.times.append((i + 1) * dt)

    return reversed_traj


def measure_holographic_entropy(states: list[HamiltonianState], n_bins: int = 20) -> dict:
    """
    Measure the holographic entropy of a set of phase-space states.

    The Bekenstein bound: S <= 2*pi*k*R*E / (hbar*c).

    On the Poincare disk, the "boundary" is the unit circle (r=1).
    The holographic entropy is the Shannon entropy of the radial
    distribution of states, discretized into radial bins. States
    near the boundary (r -> 1) contribute maximal entropy; states
    near the origin (C_0) contribute minimal entropy.

    Returns:
        entropy: Shannon entropy of the radial distribution
        mean_radius: mean distance from C_0
        max_radius: maximum distance from C_0
        boundary_fraction: fraction of states with r > 0.85
        bekenstein_ratio: S / S_max (how close to saturation)
    """
    if not states:
        return {
            "entropy": 0.0, "mean_radius": 0.0, "max_radius": 0.0,
            "boundary_fraction": 0.0, "bekenstein_ratio": 0.0,
        }

    radii = np.array([float(np.linalg.norm(s.q)) for s in states])

    # Shannon entropy of radial distribution
    bins = np.linspace(0, 1, n_bins + 1)
    counts, _ = np.histogram(radii, bins=bins, density=True)
    counts = counts[counts > 0]
    probs = counts / counts.sum()
    entropy = float(-np.sum(probs * np.log2(probs + 1e-12)))

    # Maximum possible entropy (uniform distribution)
    max_entropy = math.log2(n_bins)

    # Boundary fraction
    boundary_frac = float(np.mean(radii > 0.85))

    return {
        "entropy": entropy,
        "max_entropy": max_entropy,
        "bekenstein_ratio": entropy / max_entropy if max_entropy > 0 else 0.0,
        "mean_radius": float(np.mean(radii)),
        "max_radius": float(np.max(radii)),
        "boundary_fraction": boundary_frac,
    }


def detect_kawasaki_constraint(states: list[HamiltonianState], epsilon: float = 0.1) -> dict:
    """
    Probe for Kawasaki-like angle constraints at ReLU decision region vertices.

    At a point where multiple hyperbolic geodesics meet (analogous to
    ReLU hyperplane intersections), the alternating angle sum condition
    (Kawasaki: sum of alternating angles = 180 degrees) is tested.

    This is a numerical probe, not a proof. It checks whether the angles
    between geodesics from a meeting point to nearby taxonomy nodes
    satisfy the alternating sum constraint.

    Returns:
        n_vertices_tested: number of meeting points examined
        mean_alternating_sum: mean of the alternating angle sums
        std_alternating_sum: standard deviation
        kawasaki_satisfied: fraction within epsilon of 180 degrees (pi radians)
    """
    if len(states) < 4:
        return {
            "n_vertices_tested": 0, "mean_alternating_sum": 0.0,
            "std_alternating_sum": 0.0, "kawasaki_satisfied": 0.0,
        }

    # Use taxonomy nodes as the "meeting points"
    node_positions = list(POSITIONS.values())
    sums = []

    for vertex in node_positions:
        # Compute angles from this vertex to all other nodes
        angles = []
        for other in node_positions:
            if np.allclose(vertex, other):
                continue
            diff = other - vertex
            angle = math.atan2(diff[1], diff[0])
            angles.append(angle)

        if len(angles) < 3:
            continue

        angles.sort()

        # Compute alternating sum of adjacent angles
        # Kawasaki: theta_1 - theta_2 + theta_3 - theta_4 + ... = 0
        # Equivalently: sum of odd-indexed gaps = sum of even-indexed gaps = pi
        gaps = []
        for i in range(len(angles)):
            next_i = (i + 1) % len(angles)
            gap = angles[next_i] - angles[i]
            if gap < 0:
                gap += 2 * math.pi
            gaps.append(gap)

        if len(gaps) >= 4:
            # Alternating sum of angular gaps.
            # Kawasaki condition for a flat-foldable vertex: alt_sum = 0.
            # Proof: for n angles on a circle, gaps sum to 2pi.
            # With alternating signs, the sum telescopes: for even n, alt_sum = 0
            # identically; for odd n, alt_sum = +/-pi.
            # A genuine Kawasaki test requires the angles to be fold-line sector
            # angles (not point directions). For point-direction gaps, the
            # condition alt_sum = 0 characterizes evenly-spaced configurations.
            alt_sum = sum(g if i % 2 == 0 else -g for i, g in enumerate(gaps))
            sums.append(alt_sum)

    if not sums:
        return {
            "n_vertices_tested": 0, "mean_alternating_sum": 0.0,
            "std_alternating_sum": 0.0, "kawasaki_satisfied": 0.0,
        }

    # Kawasaki condition: alternating sum of angular gaps = 0
    target = 0.0
    deviations = [abs(s - target) for s in sums]

    return {
        "n_vertices_tested": len(sums),
        "mean_alternating_sum": float(np.mean(sums)),
        "std_alternating_sum": float(np.std(sums)),
        "mean_deviation_from_target": float(np.mean(deviations)),
        "kawasaki_satisfied": float(np.mean([d < epsilon for d in deviations])),
        "target": target,
        "epsilon": epsilon,
    }


# ---------------------------------------------------------------------------
# Wheeler-DeWitt constraint: H_hat |Psi> = 0
# ---------------------------------------------------------------------------

def wheeler_dewitt_constraint(
    state: HamiltonianState,
    context: list[str],
    epsilon: float = 0.1,
) -> dict:
    """
    Test whether a state satisfies the Wheeler-DeWitt constraint H|Psi> = 0.

    On the Poincare disk, the constraint selects "physical" states whose
    total energy (kinetic + potential) is near zero. This is the
    quantum-gravitational analogue of energy conservation: the
    Wheeler-DeWitt equation is the Hamiltonian constraint of general
    relativity, which has no external time parameter.

    Physical interpretation:
        |H(state)| < epsilon  =>  state is "physical" (on the constraint surface)
        |H(state)| >= epsilon =>  state is "unphysical" (off the constraint surface)

    The constraint surface is a lower-dimensional submanifold of the
    full phase space -- the "arena" where the universe actually evolves.

    Returns:
        total_energy: H(q, p) = K + V
        kinetic: K = (1/2) g^{ij} p_i p_j
        potential: V = repulsion_loss(q)
        constraint_violation: |H|
        satisfied: bool (|H| < epsilon)
    """
    ke = state.kinetic_energy
    pe = state.potential_energy(context)
    total = ke + pe
    violation = abs(total)

    return {
        "total_energy": total,
        "kinetic": ke,
        "potential": pe,
        "constraint_violation": violation,
        "satisfied": bool(violation < epsilon),
    }


def wheeler_dewitt_filter(
    states: list[HamiltonianState],
    context: list[str],
    epsilon: float = 0.5,
) -> dict:
    """
    Apply the Wheeler-DeWitt constraint to a trajectory.

    Returns the fraction of states that satisfy H|Psi> = 0, and
    statistics about the constraint violation distribution.
    """
    if not states:
        return {"fraction_satisfied": 0.0, "mean_violation": 0.0,
                "max_violation": 0.0, "n_states": 0}

    violations = []
    for s in states:
        result = wheeler_dewitt_constraint(s, context, epsilon)
        violations.append(result["constraint_violation"])

    violations = np.array(violations)
    return {
        "fraction_satisfied": float(np.mean(violations < epsilon)),
        "mean_violation": float(np.mean(violations)),
        "max_violation": float(np.max(violations)),
        "median_violation": float(np.median(violations)),
        "n_states": len(states),
        "epsilon": epsilon,
    }


# ---------------------------------------------------------------------------
# True Bekenstein Bound: S <= 2*pi*k*R*E / (hbar*c)
# ---------------------------------------------------------------------------

def measure_bekenstein_bound(
    states: list[HamiltonianState],
    context: list[str],
    n_bins: int = 20,
) -> dict:
    """
    Compute the true Bekenstein bound for a set of phase-space states.

    The Bekenstein bound: S <= 2*pi*k*R*E / (hbar*c)
    In natural units (k = hbar = c = 1): S <= 2*pi*R*E

    Where:
        S = Shannon entropy of the state distribution
        R = effective geodesic radius of the region (mean distance from C_0)
        E = mean total energy of the states

    This replaces the naive radial-distribution ratio with a physically
    meaningful measure of information-theoretic saturation.

    Returns:
        shannon_entropy: measured entropy (bits)
        bekenstein_limit: 2*pi*R*E (maximum allowed entropy)
        saturation_ratio: S / S_max
        mean_radius: average geodesic distance from C_0
        mean_energy: average total energy
        is_saturated: bool (ratio > 0.9)
    """
    if not states:
        return {
            "shannon_entropy": 0.0, "bekenstein_limit": 0.0,
            "saturation_ratio": 0.0, "mean_radius": 0.0,
            "mean_energy": 0.0, "is_saturated": False,
        }

    # Compute radii and energies
    radii = np.array([float(np.linalg.norm(s.q)) for s in states])
    energies = np.array([s.total_energy(context) for s in states])

    # Shannon entropy of radial distribution
    bins = np.linspace(0, 1, n_bins + 1)
    counts, _ = np.histogram(radii, bins=bins, density=True)
    counts = counts[counts > 0]
    probs = counts / counts.sum()
    shannon = float(-np.sum(probs * np.log2(probs + 1e-12)))

    # Effective region radius (mean geodesic distance from origin)
    mean_r = float(np.mean(radii))

    # Mean energy
    mean_e = float(np.mean(np.abs(energies)))

    # Bekenstein limit: S_max = 2*pi*R*E (natural units)
    bekenstein_limit = 2.0 * math.pi * mean_r * mean_e

    # Saturation ratio
    ratio = shannon / bekenstein_limit if bekenstein_limit > 1e-12 else 0.0

    return {
        "shannon_entropy": shannon,
        "bekenstein_limit": bekenstein_limit,
        "saturation_ratio": ratio,
        "mean_radius": mean_r,
        "mean_energy": mean_e,
        "is_saturated": ratio > 0.9,
    }


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("  HAMILTONIAN FLOW ON THE POINCARE DISK")
    print("  Symplectic Integration / T-Symmetry / Holographic Entropy")
    print("=" * 60)

    x0 = (np.random.rand(2) - 0.5) * 0.05
    context = ["Tech", "Silicon"]

    # Forward flow (with friction for convergence)
    print("\n--- Forward Hamiltonian Flow (with friction) ---")
    traj = run_hamiltonian_flow(x0, context, steps=3000, dt=0.003, friction=0.8)
    print(f"Initial energy:  {traj.energies[0]:.6f}")
    print(f"Final energy:    {traj.energies[-1]:.6f}")
    print(f"Initial position: {traj.states[0].q}")
    print(f"Final position:   {traj.states[-1].q}")

    # T-symmetry test: short conservative trajectory (small dt, no clamp)
    print("\n--- T-Symmetry Test (conservative, small dt) ---")
    x0_short = np.array([0.1, 0.05])
    context_short = ["Origin"]  # Origin is at (0,0), far from x0_short
    traj_short = run_hamiltonian_flow(x0_short, context_short, steps=1000, dt=0.0001, friction=0.0)
    rev_short = hamiltonian_time_reverse(traj_short, context_short, dt=0.0001, friction=0.0)
    error_short = float(np.linalg.norm(rev_short.states[-1].q - x0_short))
    print(f"Forward start:  {traj_short.states[0].q}")
    print(f"Forward end:    {traj_short.states[-1].q}")
    print(f"Reversed end:   {rev_short.states[-1].q}")
    print(f"T-symmetry reconstruction error: {error_short:.6f}")
    print(f"Energy conservation (forward): {traj_short.energy_drift:.2e}")

    # Holographic entropy
    print("\n--- Holographic Entropy (Bekenstein Bound) ---")
    entropy_stats = measure_holographic_entropy(traj.states)
    for k, v in entropy_stats.items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")

    # Kawasaki probe
    print("\n--- Kawasaki Constraint Probe ---")
    kawasaki = detect_kawasaki_constraint(traj.states)
    for k, v in kawasaki.items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")

    print("\n[DONE]")
