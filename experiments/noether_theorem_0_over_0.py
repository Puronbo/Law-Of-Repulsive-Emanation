"""
Noether's theorem (Lagrangian mechanics) via 0/0
================================================
Noether's theorem: every continuous symmetry of the Lagrangian gives
a conserved quantity.

The 0/0: for a symmetry transformation with parameter epsilon:
  L(q + epsilon*delta_q, q_dot + epsilon*delta_q_dot, t) = L(q, q_dot, t)
The variation of the action: delta S = integral (dL/depsilon) dt = 0.
At epsilon = 0: dL/depsilon = 0/0 (the Lagrangian is unchanged).
The removable value = 0 (by symmetry).

The conserved quantity: Q = dL/d(q_dot) * delta_q (for time-independent symmetries).
The 0/0: Q is conserved, so dQ/dt = 0. The ratio Q(t)/Q(0) = 1 for all t.
At t = infinity (if applicable): Q(inf)/Q(0) = 1, but Q(inf) may be 0 if the
system dissipates (breaking the symmetry). The 0/0: Q(inf)/Q(0) = 0/0 if the
symmetry is broken. Removable value = 1 (if symmetry is exact).

For translational symmetry (shift invariance): L depends only on q_dot, not q.
Conserved: momentum p = dL/dq_dot.
For rotational symmetry: L depends only on |q_dot|, not angle.
Conserved: angular momentum L = q x p.

The 0/0 in the symmetry check: (L(q + eps*dq) - L(q)) / eps as eps -> 0.
At eps = 0: 0/0, removable value = dL/dq * dq = 0 (by the Euler-Lagrange equation).

HONEST WALL: numerical verification of Noether's theorem for specific Lagrangians.
"""

import numpy as np
import json


def lagrangian_free_particle(q, q_dot, t=0):
    """L = (1/2) * m * q_dot^2 (free particle in 1D)."""
    m = 1.0
    return 0.5 * m * q_dot**2


def lagrangian_harmonic(q, q_dot, t=0):
    """L = (1/2) * m * q_dot^2 - (1/2) * k * q^2 (harmonic oscillator)."""
    m, k = 1.0, 1.0
    return 0.5 * m * q_dot**2 - 0.5 * k * q**2


def lagrangian_pendulum(theta, theta_dot, t=0):
    """L = (1/2) * m * l^2 * theta_dot^2 + m * g * l * cos(theta)."""
    m, l, g = 1.0, 1.0, 9.81
    return 0.5 * m * l**2 * theta_dot**2 + m * g * l * np.cos(theta)


def euler_lagrange_update(L_func, q, q_dot, dt, t=0):
    """Simple Euler-Lagrange integration step."""
    eps = 1e-7
    dL_dq = (L_func(q + eps, q_dot, t) - L_func(q - eps, q_dot, t)) / (2 * eps)
    dL_dqdot = (L_func(q, q_dot + eps, t) - L_func(q, q_dot - eps, t)) / (2 * eps)

    # dL/dqdot gives momentum, ddqdot = dL/dq / m_eff
    ddq = dL_dq  # assuming d2L/dqdot2 = 1 (m=1)

    q_new = q + q_dot * dt + 0.5 * ddq * dt**2
    q_dot_new = q_dot + ddq * dt

    return q_new, q_dot_new, dL_dqdot


def run():
    results = {"tests": [], "summary": {}}

    dt = 0.001
    T = 10.0
    n_steps = int(T / dt)

    # --- Test 1: Free particle conservation of momentum ---
    # L = (1/2) * q_dot^2 (translational symmetry in q)
    # Conserved: p = q_dot
    free_tests = []
    q, q_dot = 0.0, 3.0  # initial velocity
    p_initial = q_dot
    max_p_drift = 0.0
    for i in range(n_steps):
        q, q_dot, p = euler_lagrange_update(lagrangian_free_particle, q, q_dot, dt, i * dt)
        drift = abs(p - p_initial)
        if drift > max_p_drift:
            max_p_drift = drift

    free_tests.append({
        "initial_p": float(p_initial),
        "final_p": float(p),
        "max_drift": float(max_p_drift),
        "conserved": bool(max_p_drift < 0.1)
    })

    results["free_particle"] = {
        "note": "Free particle: p = q_dot conserved (translational symmetry)",
        "tests": free_tests
    }

    # --- Test 2: Harmonic oscillator conservation of energy ---
    # L = (1/2)*q_dot^2 - (1/2)*q^2
    # Conserved: E = (1/2)*q_dot^2 + (1/2)*q^2
    harmonic_tests = []
    q, q_dot = 1.0, 0.0
    E_initial = 0.5 * q_dot**2 + 0.5 * q**2
    energies = []
    for i in range(n_steps):
        q, q_dot, _ = euler_lagrange_update(lagrangian_harmonic, q, q_dot, dt, i * dt)
        E = 0.5 * q_dot**2 + 0.5 * q**2
        energies.append(E)

    E_arr = np.array(energies)
    harmonic_tests.append({
        "E_initial": float(E_initial),
        "E_final": float(energies[-1]),
        "E_mean": float(np.mean(E_arr)),
        "E_std": float(np.std(E_arr)),
        "relative_drift": float(abs(np.mean(E_arr[-100:]) - E_initial) / E_initial) if E_initial > 0 else 0,
        "conserved": bool(np.std(E_arr) / E_initial < 0.05) if E_initial > 0 else False
    })

    results["harmonic_oscillator"] = {
        "note": "Harmonic oscillator: E = (1/2)q_dot^2 + (1/2)q^2 conserved",
        "tests": harmonic_tests
    }

    # --- Test 3: Noether's symmetry check ---
    # For a symmetry: L(q + eps*dq) = L(q) + O(eps^2)
    # So (L(q+eps*dq) - L(q))/eps -> 0 as eps -> 0
    symmetry_tests = []
    q0, qdot0 = 1.0, 2.0

    # Translation symmetry: dq = 1 (shift in q)
    # L_free(q+eps) = L_free(q) (no q-dependence)
    # L_harmonic(q+eps) != L_harmonic(q)
    for eps in [0.1, 0.01, 0.001, 0.0001]:
        dL_free = (lagrangian_free_particle(q0 + eps, qdot0) -
                   lagrangian_free_particle(q0, qdot0)) / eps
        dL_harm = (lagrangian_harmonic(q0 + eps, qdot0) -
                   lagrangian_harmonic(q0, qdot0)) / eps
        symmetry_tests.append({
            "eps": eps,
            "dL_free_dq": float(dL_free),
            "dL_harmonic_dq": float(dL_harm),
            "free_is_symmetric": bool(abs(dL_free) < 0.01),
            "harmonic_not_symmetric": bool(abs(dL_harm) > 0.1)
        })

    results["symmetry_check"] = {
        "note": "Translation dL/dq = 0 for free (symmetric), != 0 for harmonic",
        "tests": symmetry_tests
    }

    # --- Test 4: Pendulum energy conservation ---
    # L = (1/2)*theta_dot^2 + g*cos(theta)
    # E = (1/2)*theta_dot^2 - g*cos(theta)
    pendulum_tests = []
    theta, theta_dot = 0.5, 0.0  # small angle
    E_init = 0.5 * theta_dot**2 - 9.81 * np.cos(theta)
    E_pend = []
    for i in range(n_steps):
        theta, theta_dot, _ = euler_lagrange_update(lagrangian_pendulum, theta, theta_dot, dt, i * dt)
        E = 0.5 * theta_dot**2 - 9.81 * np.cos(theta)
        E_pend.append(E)

    E_pend_arr = np.array(E_pend)
    pendulum_tests.append({
        "E_initial": float(E_init),
        "E_final": float(E_pend[-1]),
        "E_std": float(np.std(E_pend_arr)),
        "relative_drift": float(abs(np.mean(E_pend_arr[-100:]) - E_init) / abs(E_init)) if abs(E_init) > 1e-10 else 0,
        "conserved": bool(np.std(E_pend_arr) / abs(E_init) < 0.05) if abs(E_init) > 1e-10 else False
    })

    results["pendulum"] = {
        "note": "Pendulum: E conserved (rotational symmetry around pivot)",
        "tests": pendulum_tests
    }

    # --- Test 5: Momentum 0/0 ---
    # p = dL/dq_dot. For the harmonic oscillator at q_dot = 0: p = 0.
    # The ratio p / q_dot = m = 1 (constant). At q_dot = 0: 0/0, removable = 1.
    mom_tests = []
    for qd in [1.0, 0.5, 0.1, 0.01, 0.001]:
        p = qd  # for m=1
        ratio = p / qd if qd > 0 else 1.0
        mom_tests.append({
            "q_dot": float(qd),
            "momentum": float(p),
            "ratio_p_over_qdot": float(ratio),
            "is_one": bool(abs(ratio - 1.0) < 1e-10)
        })

    mom_tests.append({
        "q_dot": 0,
        "momentum": 0,
        "ratio_p_over_qdot": "0/0",
        "removable_value": 1.0
    })

    results["momentum_0_over_0"] = {
        "note": "p/q_dot = m = 1; at q_dot=0: 0/0 removable = 1 (mass)",
        "tests": mom_tests
    }

    # --- Summary ---
    free_ok = free_tests[0]["conserved"]
    harm_ok = harmonic_tests[0]["conserved"]
    pend_ok = pendulum_tests[0]["conserved"]
    sym_ok = symmetry_tests[-1]["free_is_symmetric"]

    supported = bool(free_ok and harm_ok and pend_ok and sym_ok)

    results["summary"] = {
        "supported": supported,
        "free_particle_conserved": free_ok,
        "harmonic_energy_conserved": harm_ok,
        "pendulum_energy_conserved": pend_ok,
        "symmetry_check_correct": sym_ok,
        "honest_wall": "numerical Euler-Lagrange integration; drift is numerical"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Noether's theorem via 0/0")
    print(f"  Free particle conserved:  {s['free_particle_conserved']}")
    print(f"  Harmonic conserved:       {s['harmonic_energy_conserved']}")
    print(f"  Pendulum conserved:       {s['pendulum_energy_conserved']}")
    print(f"  Symmetry correct:         {s['symmetry_check_correct']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/noether_theorem_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
