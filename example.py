"""
Law of Repulsive Emanation (L.O.R.E.) — Quickstart Example.

Shows the core claim: the integration constant C0 = V(q0) = H(q0, 0)
is uniquely determined by the initial condition, not arbitrary.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Universals'))

import numpy as np
from hamiltonian_flow import repulsion_loss, HamiltonianState, run_hamiltonian_flow

# 1. The Law: C0 = V(q0) = H(q0, 0)
q0 = np.array([0.2, -0.15])
context = ['Tech', 'Silicon', 'Art']

C0 = repulsion_loss(q0, context)
H0 = HamiltonianState(q=q0, p=np.zeros(2)).total_energy(context)

assert abs(C0 - H0) < 1e-12, "C0 law violated!"
print(f"q0 = ({q0[0]:.3f}, {q0[1]:.3f})")
print(f"C0 = V(q0)   = {C0:.10f}")
print(f"H(q0, 0)     = {H0:.10f}")
print(f"Match: {abs(C0 - H0) < 1e-12}")
print()

# 2. Run Hamiltonian flow — C0 is conserved
traj = run_hamiltonian_flow(q0, p0=np.zeros(2), context=context, steps=200, dt=0.02, friction=0.01)
print(f"Ran {len(traj.states)} Hamiltonian steps")
print(f"Initial energy:   {traj.energies[0]:.10f}")
print(f"Final energy:     {traj.energies[-1]:.10f}")
print(f"Energy drift:     {traj.energy_drift:.2e}")
print(f"C0 law conserved: {abs(traj.energies[0] - C0) < 1e-12}")

# 3. Multiple initial positions — law holds universally
print()
print("C0 law verification across positions:")
for dx, dy in [(0.0, 0.0), (0.3, 0.1), (-0.2, 0.4), (0.5, -0.3), (-0.6, -0.2)]:
    q_test = np.array([dx, dy])
    c0 = repulsion_loss(q_test, context)
    h0 = HamiltonianState(q=q_test, p=np.zeros(2)).total_energy(context)
    ok = "OK" if abs(c0 - h0) < 1e-12 else "FAIL"
    print(f"  ({dx:+.2f}, {dy:+.2f})  C0={c0:.6f}  H0={h0:.6f}  [{ok}]")
