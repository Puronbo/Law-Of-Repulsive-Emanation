"""Compare C0 geodesic: Poincare vs Cusp metric (stable start)."""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "Universals"))
from hamiltonian_flow import run_hamiltonian_flow, repulsion_loss, hamiltonian_time_reverse
CONTEXT = ["Tech", "Silicon"]
x0 = np.array([0.05, 0.05])
p0 = np.array([0.01, 0.02])
C0 = repulsion_loss(np.zeros(2), CONTEXT)

print("=" * 65)
print("  C0 geodesic: Poincare vs Cusp metric (stable start)")
print("=" * 65)

for metric_name in ["poincare", "cusp"]:
    traj = run_hamiltonian_flow(x0, CONTEXT, steps=2000, dt=0.005,
                                 p0=p0, friction=0.0, metric=metric_name)
    qs = np.array([s.q for s in traj.states])
    r = np.array([float(np.linalg.norm(q)) for q in qs])
    Vs = np.array([repulsion_loss(q, CONTEXT) for q in qs])
    drift = abs(traj.energies[-1]-traj.energies[0])/max(abs(traj.energies[0]),1e-12)
    rev = hamiltonian_time_reverse(traj, CONTEXT, dt=0.005, friction=0.0, metric=metric_name)
    ts_err = float(np.linalg.norm(rev.states[-1].q - x0))
    turns = []
    for i in range(1, len(qs)-1):
        v1 = qs[i]-qs[i-1]; v2 = qs[i+1]-qs[i]
        dot = float(np.dot(v1,v2)); norm = float(np.linalg.norm(v1))*float(np.linalg.norm(v2))
        if norm > 1e-12:
            turns.append(math.degrees(math.acos(np.clip(dot/norm,-1,1))))
    escaped = r[-1] > 0.99 if metric_name == "poincare" else r[-1] > 100
    c0_max = float(abs(Vs - C0).max())
    c0_holds = c0_max < 0.5
    print(f"\n  {metric_name.upper()} metric:")
    print(f"    r range: [{r.min():.4f}, {r.max():.4f}]")
    print(f"    V range: [{Vs.min():.4f}, {Vs.max():.4f}]")
    print(f"    C0 law:  {'HOLDS' if c0_holds else 'BROKEN'} (max|V-C0|={c0_max:.4f})")
    print(f"    Energy drift: {drift:.2e}")
    print(f"    T-symmetry:   {'OK' if ts_err < 0.01 else 'FAIL'} (err={ts_err:.2e})")
    print(f"    Mean turn:    {float(np.mean(turns)):.2f} deg")
    print(f"    Escaped?      {'YES' if escaped else 'NO'}")
