"""
C0 geodesic in the cusp metric: does the chaos spectrum persist?

The C0 potential V(q) (repulsion from non-context nodes) drives geodesic
flow in the Poincare metric (T8).  Here we run the SAME potential but
on the cusp metric g = dq^2/|q|^2.

Key questions:
 - Does the trajectory still explore the disk in a bounded way?
 - Does the C0 law (V = C0) still hold?
 - Does a chaos spectrum emerge?
 - Is T-symmetry preserved?
"""
import sys, os, math
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "Universals"))
from hamiltonian_flow import run_hamiltonian_flow, hamiltonian_time_reverse
from hamiltonian_flow import repulsion_loss

CONTEXT = ["Tech", "Silicon"]
GOLDEN = (1 + math.sqrt(5)) / 2

print("=" * 65)
print("  C0 GEODESIC IN THE CUSP METRIC")
print("=" * 65)

# === Run C0 geodesic in cusp metric ===
x0 = np.array([-0.4, 0.3])  # "Tech" position
traj = run_hamiltonian_flow(x0, CONTEXT, steps=5000, dt=0.005,
                             friction=0.0, metric="cusp")

qs = np.array([s.q for s in traj.states])
r = np.array([float(np.linalg.norm(q)) for q in qs])
Vs = np.array([repulsion_loss(q, CONTEXT) for q in qs])
C0 = repulsion_loss(np.zeros(2), CONTEXT)

print(f"\n  Initial q: ({qs[0,0]:.4f}, {qs[0,1]:.4f}), r={r[0]:.4f}")
print(f"  C0 = V(0) = {C0:.4f}")
print(f"  Steps: {len(qs)}")

# === 1. Trajectory characteristics ===
print(f"\n  --- 1. Trajectory bounds ---")
print(f"  r range: [{r.min():.4f}, {r.max():.4f}]")
print(f"  Final r: {r[-1]:.4f}")

# === 2. C0 law check ===
print(f"\n  --- 2. C0 law: V(q) = C0? ---")
print(f"  V range: [{Vs.min():.4f}, {Vs.max():.4f}]")
print(f"  C0 = {C0:.4f}")
print(f"  V near C0: max |V - C0| = {abs(Vs - C0).max():.4f}")
print(f"  {'C0 law HOLDS' if abs(Vs - C0).max() < 0.1 else 'C0 law BROKEN in cusp metric'}")

# === 3. Energy conservation in cusp metric ===
# H_cusp = 0.5 * r^2 * |p|^2 + V(q)
cusp_H = np.array(traj.energies)
drift = abs(cusp_H[-1] - cusp_H[0]) / max(abs(cusp_H[0]), 1e-12)
slope = np.polyfit(range(len(cusp_H)), cusp_H, 1)[0]
print(f"\n  --- 3. Energy conservation ---")
print(f"  H_cusp range: [{cusp_H.min():.4f}, {cusp_H.max():.4f}]")
print(f"  Drift: {drift:.4f} (0 = perfect)")
print(f"  Linear trend: {slope:.4f}/step")
print(f"  {'Conserved' if drift < 0.01 else 'NOT conserved in cusp metric'}")

# === 4. T-symmetry ===
print(f"\n  --- 4. T-symmetry ---")
rev = hamiltonian_time_reverse(traj, CONTEXT, dt=0.005, friction=0.0, metric="cusp")
rev_final = rev.states[-1].q
ts_error = float(np.linalg.norm(rev_final - x0))
print(f"  Reconstruction error: {ts_error:.4e}")
print(f"  {'T-symmetric' if ts_error < 0.01 else 'T-symmetry BROKEN'}")

# === 5. Turning angles ===
turns = []
for i in range(1, len(qs)-1):
    v1 = qs[i] - qs[i-1]
    v2 = qs[i+1] - qs[i]
    dot = float(np.dot(v1, v2))
    norm = float(np.linalg.norm(v1)) * float(np.linalg.norm(v2))
    if norm > 1e-12:
        turns.append(math.degrees(math.acos(np.clip(dot/norm, -1, 1))))
print(f"\n  --- 5. Turning behavior ---")
print(f"  Mean turn: {np.mean(turns):.2f} deg, std: {np.std(turns):.2f} deg")

# === 6. Compare with Poincare metric flow ===
print(f"\n  --- 6. Comparison with Poincare metric flow ---")
traj_p = run_hamiltonian_flow(x0, CONTEXT, steps=5000, dt=0.005,
                               friction=0.0, metric="poincare")
qs_p = np.array([s.q for s in traj_p.states])
r_p = np.array([float(np.linalg.norm(q)) for q in qs_p])
Vs_p = np.array([repulsion_loss(q, CONTEXT) for q in qs_p])
drift_p = abs(traj_p.energies[-1]-traj_p.energies[0])/max(abs(traj_p.energies[0]),1e-12)
rev_p = hamiltonian_time_reverse(traj_p, CONTEXT, dt=0.005, friction=0.0, metric="poincare")
ts_p = float(np.linalg.norm(rev_p.states[-1].q - x0))

print(f"  Metric      r_range              V_range              Drift     T-sym")
print(f"  {'-'*75}")
print(f"  Poincare    [{r_p.min():.3f}, {r_p.max():.3f}]       [{Vs_p.min():.3f}, {Vs_p.max():.3f}]      {drift_p:.2e}  {'OK' if ts_p < 0.01 else 'FAIL':>4}")
print(f"  Cusp        [{r.min():.3f}, {r.max():.3f}]       [{Vs.min():.3f}, {Vs.max():.3f}]      {drift:.2e}  {'OK' if ts_error < 0.01 else 'FAIL':>4}")
