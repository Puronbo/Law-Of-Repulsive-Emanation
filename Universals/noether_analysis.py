"""
noether_analysis.py
===================
Verify Noether's theorem: C0 = H(q0, 0) is the conserved charge under
time-translation symmetry of the Hamiltonian.

For a time-independent H, the Poisson bracket {H, H} = 0, so dH/dt = 0.
Therefore C0 = H(0) = H(t) for all t along a frictionless trajectory.
"""

import numpy as np, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from hamiltonian_flow import run_hamiltonian_flow, repulsion_loss, HamiltonianState

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def verify_noether(
    q0: np.ndarray,
    context: list[str],
    steps: int = 500,
    dt: float = 0.0005,
    alpha: float = 2.5,
    max_grad: float | None = 5.0
) -> dict:
    """
    Run a frictionless Hamiltonian trajectory and verify Noether charge conservation.

    Noether's theorem: continuous symmetry -> conserved charge.
    Time-translation invariance (dH/dt = 0) -> Q = H is conserved.
    """
    traj = run_hamiltonian_flow(q0, context, steps=steps, dt=dt, friction=0.0, alpha=alpha, max_grad=max_grad)

    c0 = repulsion_loss(q0, context)
    q_series = []
    q_values = []
    noether_series = []

    for i, s in enumerate(traj.states):
        q = s.noether_charge(context)
        q_values.append(round(q, 10))
        noether_series.append({
            "step": i,
            "t": round(traj.times[i], 4) if i < len(traj.times) else round(i * dt, 4),
            "charge": round(q, 10),
            "q_pos": [round(float(s.q[0]), 6), round(float(s.q[1]), 6)],
        })
        q_series.append(round(q, 10))

    max_drift = max(abs(q - c0) for q in q_series) if q_series else 0.0
    rel_drift = max_drift / max(abs(c0), 1e-12)
    conserved = rel_drift < 0.01

    # Compute Poisson bracket {H, H} at each step (should be 0)
    poisson_checks = []
    for i in range(min(len(traj.states) - 1, 50)):
        dH = traj.energies[i + 1] - traj.energies[i]
        dt_i = traj.times[i + 1] - traj.times[i] if i + 1 < len(traj.times) else dt
        poisson_checks.append({
            "step": i,
            "dH_dt": round(dH / max(dt_i, 1e-12), 8),
        })

    return {
        "q0": [float(q0[0]), float(q0[1])],
        "context": context,
        "c0": round(c0, 10),
        "steps": len(traj.states),
        "noether_charge_series": noether_series,
        "noether_charge_values": q_series,
        "max_drift": round(max_drift, 10),
        "relative_drift": round(rel_drift, 8),
        "conserved": conserved,
        "poisson_checks": poisson_checks,
        "energy_drift": round(traj.energy_drift, 8),
        "law": "dQ/dt = 0  |  Q = H(q, p) = C0  |  Noether charge under time translation",
        "verification": "PASS" if conserved else "FAIL",
    }


def run():
    """Run Noether analysis for multiple initial conditions and export."""
    print("\n[NOETHER ANALYSIS] Verifying Noether charge conservation")
    contexts = [
        (['Tech', 'Silicon'], 'Tech+Si'),
        (['Bio', 'Mammal'], 'Bio+Mam'),
        (['Origin'], 'Origin'),
    ]
    results = {}
    all_conserved = True

    for ctx, name in contexts:
        q0 = np.array([0.1, 0.05]) if name == 'Origin' else np.array([0.0, 0.0])
        r = verify_noether(q0, ctx, steps=1000, dt=0.0005)
        results[name] = r
        ok = "OK" if r["conserved"] else "FAIL"
        all_conserved = all_conserved and r["conserved"]
        n_checks = len(r["noether_charge_series"])
        print(f"  {name}: C0={r['c0']:.6f}, drift={r['max_drift']:.2e}, conserved={ok} ({n_checks} steps)")

    # Also test at multiple positions
    positions = [
        (np.array([0.0, 0.0]), 'Origin'),
        (np.array([0.3, 0.0]), 'Right'),
        (np.array([-0.2, 0.4]), 'NE'),
    ]
    ctx = ['Tech', 'Silicon']
    for q0, name in positions:
        r = verify_noether(q0, ctx, steps=1000, dt=0.0005)
        results[f"pos_{name}"] = r
        ok = "OK" if r["conserved"] else "FAIL"
        all_conserved = all_conserved and r["conserved"]
        print(f"  pos={name}: C0={r['c0']:.6f}, drift={r['max_drift']:.2e}, conserved={ok}")

    export = {
        "results": results,
        "summary": {
            "all_trajectories_conserved": all_conserved,
            "total_trajectories": len(results),
            "theorem": "Noether: Time-translation symmetry -> conserved charge Q = H = C0",
        }
    }

    with open(os.path.join(BASE_DIR, "noether_data.json"), "w") as f:
        json.dump(export, f, indent=2)
    print(f"  [EXPORTED] noether_data.json ({len(results)} trajectories)")
    print(f"  All conserved: {all_conserved}")
    print(f"  [NOETHER ANALYSIS COMPLETE]\n")


if __name__ == "__main__":
    run()
