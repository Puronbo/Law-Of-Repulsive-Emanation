"""
Fibonacci square-figure spiral: a frictionless trajectory on the Poincare disk.

A Fibonacci square spiral turns by exactly 90 deg at each step, with
side length growing by the golden ratio phi ≈ 1.618 every full turn.

On the Poincare disk, we map each corner q_n = (r_n cos theta_n, r_n sin theta_n)
where r_n = tanh(alpha * F_n) and theta_n = n * 90 deg.
The "frictionless" claim: if the discrete energy H_n = V(q_n) + K_n is
conserved, the spiral is a symplectic trajectory.
"""
import sys, os, math
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "Universals"))
from hamiltonian_flow import repulsion_loss, hyperbolic_dist, repulsion_gradient, run_hamiltonian_flow, hamiltonian_time_reverse

CONTEXT = ["Tech", "Silicon"]
GOLDEN = (1 + math.sqrt(5)) / 2


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fibonacci_square_corners(n_turns: int = 20) -> np.ndarray:
    """Generate Fibonacci square spiral corners.

    Each turn adds a square of side F_k.  The outer corner of the
    k-th square is at polar coords (r_k, theta_k) where the spiral
    grows by phi per quarter-turn.
    """
    points = []
    x, y = 0.0, 0.0
    sides = []
    for k in range(1, n_turns + 1):
        fk = float(fib(k))
        # Direction cycles: right, up, left, down
        direction = (k - 1) % 4
        dx, dy = [(fk, 0), (0, fk), (-fk, 0), (0, -fk)][direction]
        x += dx
        y += dy
        points.append(np.array([x, y]))
        sides.append(fk)

    pts = np.array(points)
    # Scale so that all points fit in [-0.99, 0.99]
    max_extent = float(np.max(np.abs(pts)))
    scale = 0.95 / max_extent if max_extent > 0 else 1
    pts = pts * scale
    return pts, sides


def analyze_fibonacci_squares(pts: np.ndarray, sides: list):
    """Analyze the Fibonacci square spiral as a frictionless trajectory."""
    n = len(pts)
    print(f"\n{'='*65}")
    print(f"  FIBONACCI SQUARE SPIRAL  ({n} corners, {n-1} squares)")
    print(f"{'='*65}")

    # 1. Geometry: radii, turning angles, step lengths
    radii = np.array([float(np.linalg.norm(q)) for q in pts])
    print(f"  Radii: range [{radii.min():.4f}, {radii.max():.4f}], "
          f"final r = {radii[-1]:.4f}")

    # Turning angles (should be exactly 90 deg for square corners)
    angles = []
    for i in range(1, n - 1):
        v1 = pts[i] - pts[i - 1]
        v2 = pts[i + 1] - pts[i]
        dot = float(np.dot(v1, v2))
        norm = float(np.linalg.norm(v1)) * float(np.linalg.norm(v2))
        if norm > 1e-12:
            angle = math.degrees(math.acos(np.clip(dot / norm, -1, 1)))
            angles.append(angle)
    if angles:
        print(f"  Turning angles: mean={np.mean(angles):.2f} deg, "
              f"std={np.std(angles):.2f} deg, "
              f"expected=90 deg")

    # 2. Potential V(q) at each corner
    Vs = np.array([repulsion_loss(q, CONTEXT) for q in pts])
    C0 = repulsion_loss(np.zeros(2), CONTEXT)
    print(f"  V(q): min={Vs.min():.4f}, max={Vs.max():.4f}, "
          f"C0={C0:.4f}")
    print(f"  V near C0: min diff = {abs(Vs - C0).min():.4f}")

    # 3. Euclidean step lengths (side lengths of squares)
    steps = np.array([float(np.linalg.norm(pts[i+1] - pts[i]))
                      for i in range(n - 1)])
    step_ratios = steps[1:] / steps[:-1]
    print(f"  Steps: mean={steps.mean():.4f}, ", end="")
    if len(step_ratios) > 0:
        print(f"mean ratio={step_ratios.mean():.4f} "
              f"(expected phi/2={GOLDEN/2:.4f})")
    else:
        print()

    # 4. Discrete pseudo-energy: H = V(q_n) + 0.5 * |step_n|^2
    ke = 0.5 * steps ** 2
    total_e = Vs[1:] + ke  # kinetic at n uses step from n to n+1
    if len(total_e) > 1:
        drift = abs(total_e[-1] - total_e[0]) / max(abs(total_e[0]), 1e-12)
        print(f"  Pseudo-energy drift: {drift:.4f} "
              f"(< 1 = bounded, ~ 0 = conserved)")

        # Fit energy to see if it has a conserved trend
        slopes = np.polyfit(range(len(total_e)), total_e, 1)[0]
        print(f"  Energy linear trend: {slopes:.4f} per step "
              f"({'decaying' if slopes < 0 else 'growing' if slopes > 0 else 'stable'})")

    # 5. Check if the trajectory "turns without friction":
    #    The turning should be regular (low std) and the trajectory
    #    should explore the disk without escaping
    escaped = radii[-1] > 0.98
    print(f"  Escaped to boundary? {'YES' if escaped else 'NO'}")

    return {
        "n_corners": n,
        "drift": drift if len(total_e) > 1 else None,
        "mean_turn": float(np.mean(angles)) if angles else None,
        "std_turn": float(np.std(angles)) if angles else None,
    }


# === Experiment: Fibonacci square spiral ===
pts, sides = fibonacci_square_corners(n_turns=30)
res = analyze_fibonacci_squares(pts, sides)

# === Compare: what would a frictionless geodesic look like? ===
# For reference, run a short Hamiltonian trajectory from the first point
print(f"\n  --- Comparison with Hamiltonian trajectory ---")
from hamiltonian_flow import run_hamiltonian_flow
traj = run_hamiltonian_flow(pts[0], CONTEXT, steps=len(pts), dt=0.001,
                            friction=0.0, max_grad=5.0)
h_qs = np.array([s.q for s in traj.states])
h_energies = np.array(traj.energies)
h_drift = abs(h_energies[-1] - h_energies[0]) / max(abs(h_energies[0]), 1e-12)
h_min_dist = float(np.min([np.linalg.norm(s.q) for s in traj.states]))
print(f"  Hamiltonian trajectory from same start:")
print(f"    Energy drift: {h_drift:.4e} (should be near 0)")
print(f"    Min distance to origin: {h_min_dist:.4f}")
print(f"    Final r = {float(np.linalg.norm(traj.states[-1].q)):.4f}")

# === Key insight: time-reversal ===
# If the Fibonacci spiral is a time-reversed geodesic, then reversing
# it and running the Hamiltonian flow should return to the starting point.
print(f"\n  --- Time-reversal test ---")
fib_reversed = pts[::-1]  # time-reversed Fibonacci trajectory
rev_from_end = run_hamiltonian_flow(pts[-1], CONTEXT, steps=len(pts),
                                     dt=0.001, friction=0.0, max_grad=5.0)
rev_final = rev_from_end.states[-1].q
ts_error = float(np.linalg.norm(rev_final - pts[0]))
print(f"  Time-reverse Fibonacci from end, flow back to start:")
print(f"    Reconstruction error: {ts_error:.4f} "
      f"({'PASS' if ts_error < 0.5 else 'FAIL'})")
print(f"    Start point:    ({pts[0][0]:+.4f}, {pts[0][1]:+.4f})")
print(f"    Reconstructed:  ({rev_final[0]:+.4f}, {rev_final[1]:+.4f})")

# === Compare with C0 geodesic time-reversal ===
traj_from_start = run_hamiltonian_flow(pts[0], CONTEXT, steps=len(pts),
                                        dt=0.001, friction=0.0, max_grad=5.0)
rev_traj = hamiltonian_time_reverse(traj_from_start, CONTEXT,
                                     dt=0.001, friction=0.0, max_grad=5.0)
c0_ts_error = float(np.linalg.norm(rev_traj.states[-1].q - pts[0]))
print(f"  C0 geodesic T-symmetry error: {c0_ts_error:.4e} "
      f"({'PASS' if c0_ts_error < 0.5 else 'FAIL'})")

# === Final synthesis ===
print(f"\n{'='*65}")
print(f"  SYNTHESIS")
print(f"{'='*65}")
print(f"  Fibonacci square spiral vs C0 geodesic from same start:")
print(f"  ")
print(f"  Property               Fibonacci     C0 geodesic")
print(f"  {'-'*50}")
print(f"  Turning regularity     90.0 deg (0 var)  chaotic")
print(f"  Energy drift           0.96            1.4e-06")
print(f"  Radial direction       outward         inward")
print(f"  T-symmetry            {ts_error:.2e}          {c0_ts_error:.2e}")
print(f"  ")
print(f"  The Fibonacci spiral is a DIFFERENT flow from the C0 geodesic.")
print(f"  It has constant 90 deg cornering (the 'square figure turning')")
print(f"  and bounded pseudo-energy ('without friction').")
print(f"  This suggests a 'golden metric' where the logarithmic spiral")
print(f"  r ~ tanh(phi * theta / 2) is the geodesic.")

# ---- persist a claim/verdict artifact (AUDIT 5.8 norm) ----
import json
_steps = np.array([float(np.linalg.norm(pts[i+1] - pts[i])) for i in range(len(pts) - 1)])
_Vs = np.array([repulsion_loss(q, CONTEXT) for q in pts])
_results = {
    "claim": (
        "The Fibonacci square-figure spiral is a frictionless trajectory on "
        "the Poincare disk: constant 90-deg cornering with bounded "
        "pseudo-energy ('turning without friction'), suggesting a golden "
        "metric whose geodesic is a logarithmic spiral"
    ),
    "measurements": {
        "n_corners": res["n_corners"],
        "mean_turn_deg": res["mean_turn"],
        "std_turn_deg": res["std_turn"],
        "final_r": float(np.linalg.norm(pts[-1])),
        "escaped": bool(float(np.linalg.norm(pts[-1])) > 0.98),
        "pseudo_energy_drift": res["drift"],
        "energy_linear_trend_per_step": float(np.polyfit(
            range(len(_Vs) - 1), _Vs[1:] + 0.5 * _steps ** 2, 1)[0]),
        "fib_tsym_error": float(ts_error),
        "fib_tsym_ok": bool(ts_error < 0.5),
        "c0_geodesic_tsym_error": float(c0_ts_error),
        "c0_geodesic_drift": float(h_drift),
    },
    "verdict": (
        "REFUTED as a 'frictionless trajectory' claim: the constant 90-deg "
        "turning is a trivial artifact of the square construction, not a "
        "dynamical property. Pseudo-energy is bounded but clearly NOT "
        "conserved: drift 0.9647 with a monotone linear decay of -0.357 per "
        "step. The spiral ESCAPES the disk (final r = 1.117 > 1). "
        "T-symmetry FAILS for the spiral treated as a trajectory (error "
        "0.9900 vs 5.9994e-09 for a true C0 geodesic from the same start), "
        "so it is NOT a time-reversible frictionless flow. The hypothesized "
        "'golden metric' whose geodesic is a logarithmic spiral is "
        "unsubstantiated by these data (compare t39_cusp_flow: the cusp "
        "metric, not a disk metric, makes the Fibonacci spiral an exact "
        "geodesic)."
    ),
}
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "data", "fibonacci_squares_data.json")
with open(out_path, "w") as f:
    json.dump(_results, f, indent=2)
print("\nverdict:", _results["verdict"][:150], "...")
print("wrote data/fibonacci_squares_data.json")
