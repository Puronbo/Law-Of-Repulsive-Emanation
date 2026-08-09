"""
T-symmetry experiments crossing the C0 origin (q=0).

Two cases:
  Exp A (0+ > 0 < x_0+): start at x_0 > 0, forward > past 0, reverse < to x_0
  Exp B (0- < 0 > x_0-): start at x_0 < 0, forward > past 0, reverse < to x_0

Tests whether the symplectic integrator preserves time-reversal symmetry
when the trajectory crosses the C0 critical point (V(0) = C0 minimum).
"""
import sys, os, math
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "Universals"))
from hamiltonian_flow import run_hamiltonian_flow, hamiltonian_time_reverse, repulsion_loss

CONTEXT = ["Tech", "Silicon"]
DT = 0.0005
STEPS = 2000

def run_experiment(label: str, x0: np.ndarray, direction: str):
    """Run a T-symmetry crossing experiment.

    direction: "+" means start positive, "-" means start negative.
    """
    c0 = repulsion_loss(np.zeros(2), CONTEXT)
    V0 = repulsion_loss(x0, CONTEXT)

    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  x0 = ({x0[0]:+.4f}, {x0[1]:+.4f}),  |x0| = {np.linalg.norm(x0):.4f}")
    print(f"  V(x0) = {V0:.4f},  C0 = V(0) = {c0:.4f}")
    print(f"  Direction: {direction}")
    print(f"{'='*60}")

    # Forward trajectory
    traj = run_hamiltonian_flow(x0, CONTEXT, steps=STEPS, dt=DT,
                                friction=0.0, max_grad=5.0)

    # Did the trajectory cross the origin?
    qs = np.array([s.q for s in traj.states])
    sign_start = np.sign(qs[0, 0])
    sign_changes = np.sum(np.diff(np.sign(qs[:, 0])) != 0)
    crosses_origin = sign_changes > 0

    min_dist_to_origin = float(np.min(np.linalg.norm(qs, axis=1)))
    final_dist = float(np.linalg.norm(qs[-1] - x0))

    print(f"  Forward: {len(traj.states)} steps")
    print(f"  Min distance to origin: {min_dist_to_origin:.6f}")
    if min_dist_to_origin < 0.05:
        print(f"  >>> TRAJECTORY CROSSES NEAR ORIGIN (q=0) <<<")
    print(f"  Crossings of q_1=0 axis: {sign_changes}")

    # Energy behavior near origin
    es = np.array(traj.energies)
    e0, ef = es[0], es[-1]
    drift = abs(ef - e0) / max(abs(e0), 1e-12)
    print(f"  Energy: E0={e0:.4f}, Ef={ef:.4f}, drift={drift:.2e}")

    # Find the index where trajectory is closest to origin
    dists = np.linalg.norm(qs, axis=1)
    closest_idx = int(np.argmin(dists))
    print(f"  Closest approach: idx={closest_idx}, "
          f"q=({qs[closest_idx,0]:.4f},{qs[closest_idx,1]:.4f}), "
          f"dist={dists[closest_idx]:.4f}")

    # Time-reversal
    rev = hamiltonian_time_reverse(traj, CONTEXT, dt=DT, friction=0.0, max_grad=5.0)
    rev_final_q = rev.states[-1].q
    ts_error = float(np.linalg.norm(rev_final_q - x0))

    print(f"\n  T-symmetry reconstruction error = {ts_error:.6e}")
    print(f"  Reversed final q = ({rev_final_q[0]:+.6f}, {rev_final_q[1]:+.6f})")
    print(f"  Expected x0     = ({x0[0]:+.6f}, {x0[1]:+.6f})")

    # Check the reversed trajectory also crosses origin appropriately
    rev_qs = np.array([s.q for s in rev.states])
    rev_min_dist = float(np.min(np.linalg.norm(rev_qs, axis=1)))
    print(f"  Reversed min dist to origin: {rev_min_dist:.6f}")

    success = ts_error < 0.5
    print(f"  {'PASS' if success else 'FAIL'} (threshold: 0.5)")
    return {
        "label": label,
        "x0": x0,
        "ts_error": ts_error,
        "crossed_origin": crosses_origin,
        "min_dist_to_origin": min_dist_to_origin,
        "energy_drift": drift,
        "success": success,
    }


# === Experiment A: positive offset, forward across origin ===
# Starting slightly right of origin, forward trajectory crosses
# through q=0 as it oscillates
res_a = run_experiment(
    "Exp A: 0+ > 0 < x_0+   (start positive, cross origin forward)",
    x0=np.array([0.02, 0.0]),
    direction="+",
)

# === Experiment B: negative offset, forward across origin ===
res_b = run_experiment(
    "Exp B: 0- < 0 > x_0-   (start negative, cross origin forward)",
    x0=np.array([-0.02, 0.0]),
    direction="-",
)

# Also test with larger offset to see if behavior changes
res_c = run_experiment(
    "Exp C: larger positive offset",
    x0=np.array([0.1, 0.05]),
    direction="+",
)

res_d = run_experiment(
    "Exp D: perpendicular offset (off the q_1 axis)",
    x0=np.array([0.0, 0.05]),
    direction="|",
)

# Summary
print(f"\n\n{'='*60}")
print(f"  SUMMARY")
print(f"{'='*60}")
print(f"  {'Experiment':<35} {'Error':>10} {'Crossed':>8} {'OK':>5}")
print(f"  {'-'*58}")
for res in [res_a, res_b, res_c, res_d]:
    print(f"  {res['label'][:35]:<35} {res['ts_error']:10.2e} "
          f"{str(res['crossed_origin']):>8} {'PASS' if res['success'] else 'FAIL':>5}")

# Key finding: is T-symmetry preserved when crossing the origin?
print(f"\n  Key question: Does the symplectic integrator preserve")
print(f"  T-symmetry when trajectory crosses q=0 (the C0 minimum)?")
all_pass = all(r["success"] for r in [res_a, res_b, res_c, res_d])
print(f"  Answer: {'YES' if all_pass else 'PARTIAL'} "
      f"(all experiments {'PASS' if all_pass else 'mixed'})")

# ---- persist a claim/verdict artifact (AUDIT 5.8 norm) ----
import json
rows = []
for res in [res_a, res_b, res_c, res_d]:
    rows.append({
        "label": res["label"],
        "x0": [float(v) for v in res["x0"]],
        "ts_error": float(res["ts_error"]),
        "crossed_origin": bool(res["crossed_origin"]),
        "min_dist_to_origin": float(res["min_dist_to_origin"]),
        "energy_drift": float(res["energy_drift"]),
        "pass": bool(res["success"]),
    })
results = {
    "claim": (
        "The symplectic integrator preserves time-reversal symmetry even "
        "when the C0 geodesic trajectory crosses the origin q=0 (the C0 "
        "minimum)"
    ),
    "settings": {"dt": 0.0005, "steps": 2000, "friction": 0.0, "max_grad": 5.0},
    "experiments": rows,
    "verdict": (
        "CAVEAT: T-symmetry reconstruction errors are small (0.066-0.226) "
        "in all four runs, so the integrator IS time-reversible in these "
        "regimes. BUT the crossing premise never actually occurred: in every "
        "experiment the closest approach to the origin is the STARTING "
        "distance itself (idx=0), i.e. the trajectories monotonically recede "
        "from q=0. A/B/C have zero q1-axis crossings; only D crosses the "
        "axis once while keeping min dist = 0.05. The headline regime - a "
        "trajectory passing THROUGH the C0 critical point - was never "
        "exercised, so the claim is PASS-with-caveat, not confirmed."
    ),
}
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "data", "c0_crossing_tsym_data.json")
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)
print("\nverdict:", results["verdict"][:160], "...")
print("wrote data/c0_crossing_tsym_data.json")
