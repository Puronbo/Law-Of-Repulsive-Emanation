#!/usr/bin/env python3
"""
Quantum Phase Transitions: 0/0 at Absolute Zero
=================================================

Quantum phase transitions occur at ZERO temperature, driven by quantum
fluctuations rather than thermal fluctuations. This is fundamentally
different from all classical (thermal) phase transitions.

1. TRANSVERSE FIELD ISING MODEL (exact in 1D):
   - H = -J * sum(sigma_z^i * sigma_z^{i+1}) - g * sum(sigma_x^i)
   - g = 0: fully ordered (all spins aligned in z)
   - g = infinity: fully disordered (all spins aligned in x)
   - g = g_c = J: QUANTUM PHASE TRANSITION (0/0)
   - Order parameter: <sigma_z> = 0/0 at g_c

2. ENTANGLEMENT ENTROPY:
   - At criticality: S ~ c/3 * log(L) (logarithmic divergence)
   - Away from criticality: S ~ constant (area law)
   - At g_c: S diverges (0/0 removable singularity)
   - c = 1/2 (central charge, Ising universality)

3. CORRELATION LENGTH:
   - xi ~ |g - g_c|^{-nu} with nu = 1 (1D exact)
   - At g_c: xi = infinity (0/0)
   - This is the QUANTUM version of the classical divergence

4. DYNAMICAL EXPONENT:
   - z = 1 (Lorentz invariant at criticality)
   - Connects space and time: xi ~ tau^{1/z}
   - Different from classical (z = 0, no dynamics)

5. QUANTUM CRITICALITY:
   - At T = 0: quantum fluctuations dominate
   - At T > 0: thermal fluctuations dominate
   - At T = 0, g = g_c: QUANTUM CRITICAL POINT (0/0)
   - Quantum critical fan: T ~ |g - g_c|^{nu*z}

6. COMPARISON WITH CLASSICAL:
   - Classical Ising (Ch.36): T_c > 0, thermal fluctuations
   - Quantum Ising: T = 0, quantum fluctuations
   - Same universality class in 1D! (beta = 1/8, nu = 1)
   - But DYNAMICAL properties are different (z = 1 vs z = 0)

Author: Michael Grafiel S Puno
"""

import math
import json
import os
import sys
import time

import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def transverse_ising_energy(g, J=1.0, N=1000):
    """
    Transverse field Ising model ground state energy (1D, exact).

    E(g) = -J * sum_k sqrt(1 + g^2 - 2*g*cos(k))
    where k ranges over the Brillouin zone.

    At g = g_c = J: energy has a cusp (0/0 removable singularity)
    """
    k_values = np.linspace(-np.pi, np.pi, N, endpoint=False)
    epsilon_k = np.sqrt(1.0 + g**2 - 2.0 * g * np.cos(k_values))
    return -J * np.sum(epsilon_k) / N


def transverse_ising_order(g, J=1.0):
    """
    Order parameter <sigma_z> for transverse field Ising.

    <sigma_z> = (1 - g^2/J^2)^{1/8} for g < J
    <sigma_z> = 0 for g >= J

    At g = g_c = J: <sigma_z> = 0/0 removable singularity
    Critical exponent: beta = 1/8 (same as 2D classical Ising!)
    """
    if g >= J:
        return 0.0
    return (1.0 - (g / J)**2)**(1.0 / 8.0)


def transverse_ising_gap(g, J=1.0):
    """
    Energy gap Delta(g) = E_1(g) - E_0(g).

    Delta(g) = 2*J*|1 - g/J| for g != J
    Delta(g) = 0 at g = g_c = J (0/0 removable singularity)

    At criticality: gap closes (0/0)
    """
    return 2.0 * J * abs(1.0 - g / J)


def correlation_length_quantum(g, J=1.0, nu=1.0):
    """
    Quantum correlation length.

    xi ~ |g - g_c|^{-nu} with nu = 1 (1D exact)
    At g = g_c: xi = infinity (0/0)
    """
    if abs(g - J) < 1e-10:
        return float('inf')
    return abs(g - J)**(-nu)


def entanglement_entropy_block(L_sub, xi, c=0.5):
    """
    Entanglement entropy of a block of size L_sub.

    At criticality (xi = infinity):
        S ~ c/3 * log(L_sub) + const

    Away from criticality:
        S ~ c/6 * log(xi) + const (area law)

    At g = g_c: S diverges logarithmically (0/0)
    """
    if xi > 1e8:
        # At criticality: logarithmic divergence
        return c / 3.0 * math.log(L_sub) + 0.5
    else:
        # Away from criticality: area law
        return c / 6.0 * math.log(xi) + 0.5


def quantum_critical_fan(g, T, J=1.0, nu=1.0, z=1.0):
    """
    Quantum critical fan.

    T ~ |g - g_c|^{nu*z} at the boundary
    Inside the fan: quantum critical behavior
    Outside: classical behavior
    """
    delta_g = abs(g - J)
    T_boundary = delta_g**(nu * z)
    return T < T_boundary


def dynamical_correlation(g, t, J=1.0):
    """
    Dynamical correlation function.

    At criticality: C(t) ~ t^{-alpha} (power law)
    Away: C(t) ~ exp(-t/tau) (exponential decay)
    """
    if abs(g - J) < 0.1:
        # Near criticality: slow decay
        return (1.0 + t)**(-0.5)
    else:
        # Away: fast decay
        tau = 1.0 / (2.0 * J * abs(1.0 - g / J))
        return math.exp(-t / tau)


def quantum_classical_correspondence():
    """
    Quantum-classical correspondence in the Ising model.

    1D quantum Ising at T=0 <-> 2D classical Ising at T=T_c
    Same critical exponents: beta = 1/8, nu = 1
    But different DYNAMICAL properties (z = 1 vs z = 0)
    """
    return {
        'quantum_1D': {'beta': 1.0/8.0, 'nu': 1.0, 'z': 1.0},
        'classical_2D': {'beta': 1.0/8.0, 'nu': 1.0, 'z': 0.0},
        'classical_MF': {'beta': 0.5, 'nu': 0.5, 'z': 0.0},
    }


def topological_entanglement_entropy(g, J=1.0):
    """
    Topological entanglement entropy.

    In topological phases: S = alpha*L - gamma
    where gamma is the topological entanglement entropy.

    At g = g_c: gamma = 0/0 (topological phase transition)
    """
    if g < J:
        # Ordered phase: gamma = log(2) (Z2 topological order)
        return math.log(2.0)
    else:
        # Disordered phase: gamma = 0
        return 0.0


def berry_phase(g, J=1.0, N=100):
    """
    Berry phase around the quantum critical point.

    At g < g_c: Berry phase = pi (non-trivial topology)
    At g > g_c: Berry phase = 0 (trivial topology)
    At g = g_c: 0/0 (topological phase transition)
    """
    if g < J:
        return math.pi
    else:
        return 0.0


def main():
    print("=" * 70)
    print("QUANTUM PHASE TRANSITIONS: 0/0 AT ABSOLUTE ZERO")
    print("=" * 70)
    print()

    # 1. Transverse Field Ising Model
    print("1. TRANSVERSE FIELD ISING MODEL (1D, EXACT)")
    print("-" * 70)
    print()
    print("   H = -J * sum(sigma_z^i * sigma_z^{i+1}) - g * sum(sigma_x^i)")
    print("   g_c = J = 1 (quantum critical point)")
    print()
    print("   g/g_c    <sigma_z>    Gap        xi         State")
    print("   " + "-" * 60)
    for g_ratio in [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.99, 1.0, 1.01, 1.1, 1.2, 1.5, 2.0]:
        g = g_ratio
        order = transverse_ising_order(g)
        gap = transverse_ising_gap(g)
        xi = correlation_length_quantum(g)
        state = "ORDERED" if g < 0.9 else ("CRITICAL" if g < 1.1 else "DISORDERED")
        print("   %.2f    %.6f    %.4f    %s    %s" % (
            g_ratio, order, gap, "%.2f" % min(xi, 999.0) if xi < 1e6 else "inf", state))

    print()
    print("   At g = g_c: <sigma_z> = 0/0 REMOVABLE SINGULARITY")
    print("   beta = 1/8 (SAME as 2D classical Ising!)")

    # 2. Energy Gap
    print()
    print("2. ENERGY GAP CLOSING")
    print("-" * 70)
    print()
    print("   Delta(g) = 2*J*|1 - g/J|")
    print("   At g = g_c: Delta = 0 (gap closes, 0/0)")
    print()
    print("   g/Delta(g)    State")
    print("   " + "-" * 40)
    for g_ratio in [0.0, 0.5, 0.8, 0.9, 0.95, 0.99, 1.0, 1.01, 1.05, 1.1, 1.2, 2.0]:
        g = g_ratio
        gap = transverse_ising_gap(g)
        state = "GAPPED" if gap > 0.1 else ("CLOSING" if gap > 0 else "GAPLESS")
        print("   %.2f/%.4f    %s" % (g_ratio, gap, state))

    # 3. Entanglement Entropy
    print()
    print("3. ENTANGLEMENT ENTROPY")
    print("-" * 70)
    print()
    print("   At criticality: S ~ c/3 * log(L)  (c = 1/2)")
    print("   Away: S ~ constant (area law)")
    print()
    print("   L_sub    S(g=0.5)   S(g=1.0)   S(g=2.0)")
    print("   " + "-" * 50)
    for L in [2, 4, 8, 16, 32, 64, 128]:
        S_ord = entanglement_entropy_block(L, 10.0)   # g=0.5, xi small
        S_crit = entanglement_entropy_block(L, 1e10)   # g=1.0, xi=infinity
        S_dis = entanglement_entropy_block(L, 10.0)    # g=2.0, xi small
        print("   %-6d  %.4f     %.4f     %.4f" % (L, S_ord, S_crit, S_dis))

    print()
    print("   At g = g_c: S diverges LOGARITHMICALLY (0/0)")

    # 4. Quantum vs Classical
    print()
    print("4. QUANTUM vs CLASSICAL UNIVERSALITY")
    print("-" * 70)
    print()
    print("   System                  beta    nu     z      Fluctuations")
    print("   " + "-" * 65)
    print("   Quantum Ising 1D        1/8     1.0    1.0    Quantum (T=0)")
    print("   Classical Ising 2D      1/8     1.0    0.0    Thermal (T>0)")
    print("   Classical Ising 3D      0.326   0.63   0.0    Thermal (T>0)")
    print("   Mean-field Ising        1/2     1/2    0.0    Thermal (T>0)")
    print()
    print("   SAME beta, nu in 1D quantum and 2D classical!")
    print("   DIFFERENT z (dynamical exponent)")
    print("   Quantum: z = 1 (Lorentz invariant)")
    print("   Classical: z = 0 (no dynamics)")

    # 5. Quantum Critical Fan
    print()
    print("5. QUANTUM CRITICAL FAN")
    print("-" * 70)
    print()
    print("   At T = 0: quantum fluctuations dominate")
    print("   At T > 0: thermal fluctuations dominate")
    print("   The quantum critical fan: T ~ |g - g_c|^{nu*z}")
    print()
    print("   g/T      In fan?     Behavior")
    print("   " + "-" * 50)
    for g_ratio in [0.5, 0.8, 0.9, 1.0, 1.1, 1.2, 1.5]:
        g = g_ratio
        for T in [0.01, 0.1, 0.5]:
            in_fan = quantum_critical_fan(g, T)
            behavior = "QUANTUM CRITICAL" if in_fan else ("ORDERED" if g < 1 else "DISORDERED")
            print("   %.2f/%.2f  %s      %s" % (g, T, "YES" if in_fan else "NO", behavior))

    # 6. Dynamical Correlations
    print()
    print("6. DYNAMICAL CORRELATIONS")
    print("-" * 70)
    print()
    print("   At criticality: C(t) ~ t^{-alpha} (power law)")
    print("   Away: C(t) ~ exp(-t/tau) (exponential)")
    print()
    print("   t/C(t) at g=0.5  g=1.0    g=2.0")
    print("   " + "-" * 50)
    for t in [0, 1, 2, 5, 10, 20]:
        c_ord = dynamical_correlation(0.5, t)
        c_crit = dynamical_correlation(1.0, t)
        c_dis = dynamical_correlation(2.0, t)
        print("   %-3d  %.4f     %.4f   %.4f" % (t, c_ord, c_crit, c_dis))

    # 7. Topological
    print()
    print("7. TOPOLOGICAL ENTANGLEMENT ENTROPY")
    print("-" * 70)
    print()
    print("   gamma = log(2) in ordered phase (Z2 topological order)")
    print("   gamma = 0 in disordered phase")
    print("   At g = g_c: gamma = 0/0 (topological phase transition)")
    print()
    print("   g/g_c    gamma       Berry     Topology")
    print("   " + "-" * 50)
    for g_ratio in [0.5, 0.8, 0.9, 1.0, 1.1, 1.5, 2.0]:
        g = g_ratio
        gamma = topological_entanglement_entropy(g)
        berry = berry_phase(g)
        topo = "NON-TRIVIAL" if g < 1.0 else ("CRITICAL" if g < 1.1 else "TRIVIAL")
        print("   %.2f    %.4f     %.2f     %s" % (g, gamma, berry, topo))

    # 8. Connections
    print()
    print("=" * 70)
    print("CONNECTIONS TO ALL PRIOR 0/0 SINGULARITIES")
    print("=" * 70)
    print()
    print("   QUANTUM PHASE TRANSITIONS connect to EVERYTHING:")
    print()
    print("   Ising (Ch.36)         -> Same beta = 1/8 in 1D/2D")
    print("   Entanglement (Ch.33)  -> S diverges at g_c")
    print("   Consciousness (Ch.34) -> Quantum consciousness theories")
    print("   Black holes (Ch.32)   -> AdS/CFT quantum criticality")
    print("   Prebiotic (Ch.35)     -> Quantum effects in origin of life")
    print("   Turbulence (Ch.37)    -> Quantum turbulence (superfluid He)")
    print("   Finance (Ch.38)       -> Quantum finance models")
    print()
    print("   The quantum 0/0 is the MOST FUNDAMENTAL!")
    print("   It occurs at T = 0 (absolute zero, no thermal noise)")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   Quantum phase transitions are 0/0 at absolute zero:")
    print()
    print("   1. TRANSVERSE FIELD ISING:")
    print("      <sigma_z> = 0/0 at g_c = J")
    print("      beta = 1/8, nu = 1, z = 1")
    print()
    print("   2. ENERGY GAP:")
    print("      Delta = 0 at g_c (gap closes)")
    print()
    print("   3. ENTANGLEMENT ENTROPY:")
    print("      S ~ c/3 * log(L) at criticality")
    print("      c = 1/2 (central charge)")
    print()
    print("   4. QUANTUM vs CLASSICAL:")
    print("      SAME beta, nu in 1D quantum = 2D classical")
    print("      DIFFERENT z (z=1 quantum, z=0 classical)")
    print()
    print("   5. TOPOLOGICAL:")
    print("      gamma = log(2) (Z2 topological order)")
    print("      Berry phase = pi (non-trivial)")
    print()
    print("   The quantum 0/0 is the MOST FUNDAMENTAL!")
    print("   It occurs at T=0 (no thermal fluctuations)")

    # Save
    results = {
        'transverse_ising': {
            'formula': 'H = -J*sum(sigma_z^i*sigma_z^{i+1}) - g*sum(sigma_x^i)',
            'g_c': 1.0,
            'beta': 1.0/8.0,
            'nu': 1.0,
            'z': 1.0,
            'central_charge': 0.5,
        },
        'order_parameter': {
            'formula': '<sigma_z> = (1 - g^2/J^2)^{1/8} for g < J',
            'beta': 1.0/8.0,
        },
        'energy_gap': {
            'formula': 'Delta = 2*J*|1 - g/J|',
            'closes_at_g_c': True,
        },
        'entanglement': {
            'critical': 'S ~ c/3 * log(L), c = 1/2',
            'area_law': 'S ~ constant away from criticality',
        },
        'quantum_classical': {
            'quantum_1D': {'beta': 1.0/8.0, 'nu': 1.0, 'z': 1.0},
            'classical_2D': {'beta': 1.0/8.0, 'nu': 1.0, 'z': 0.0},
            'same_exponents': True,
            'different_dynamics': True,
        },
        'topological': {
            'gamma': 'log(2) (Z2 topological order)',
            'berry_phase': 'pi (non-trivial topology)',
        },
        'connections': {
            'is_same_as_classical_2D': True,
            'connects_to': ['Ising', 'Entanglement', 'Consciousness', 'Black holes'],
        },
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    output_path = os.path.join(OUTPUT_DIR, 'quantum_phase_transition.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()
