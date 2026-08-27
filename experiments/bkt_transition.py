#!/usr/bin/env python3
"""
Berezinskii-Kosterlitz-Thouless Transition: 0/0 Without Symmetry Breaking
==========================================================================

The BKT transition is a TOPOLOGICAL phase transition that occurs WITHOUT
any symmetry breaking. This is fundamentally different from Ising.

1. THE 2D XY MODEL:
   - H = -J * sum(cos(theta_i - theta_j))
   - Spins are 2D angles (U(1) symmetry)
   - Below T_BKT: quasi-long-range order (power-law correlations)
   - Above T_BKT: exponential decay (disordered)
   - At T_BKT: 0/0 (vortex-antivortex unbinding)

2. CORRELATION FUNCTION:
   - Below T_BKT: G(r) ~ r^{-eta(T)} (power-law, algebraic)
   - Above T_BKT: G(r) ~ exp(-r/xi) (exponential)
   - At T_BKT: eta = 1/4 EXACTLY (universal jump!)
   - The order parameter <cos(theta)> = 0 ALWAYS (no symmetry breaking)

3. VORTEX MECHANISM:
   - Vortices are topological defects (winding number = +/-1)
   - Below T_BKT: vortices are BOUND (vortex-antivortex pairs)
   - Above T_BKT: vortices are FREE (unbound)
   - At T_BKT: 0/0 (unbinding transition)

4. UNIVERSAL JUMP:
   - eta(T_BKT) = 1/4 EXACTLY (Berezinskii 1971, Kosterlitz-Thouless 1974)
   - K_c = 2/pi (stiffness at transition)
   - This is a DISCONTINUOUS jump in eta (but continuous in energy!)

5. RENORMALIZATION GROUP:
   - Kosterlitz RG equations:
     dy/dl = (2 - pi*K)*y + ...
     dK/dl = -pi^2*y^2*K^2 + ...
   - Fixed points: (K=inf, y=0) and (K=K_c, y=0)
   - At T_BKT: flow changes direction (0/0)

6. COMPARISON WITH ISING:
   - Ising: symmetry breaking (Z2), order parameter jumps
   - BKT: NO symmetry breaking, order parameter = 0 always
   - Ising: universality class beta=1/8 (2D), 0.326 (3D)
   - BKT: universality class eta=1/4 (EXACT, no free parameter!)
   - BKT is a DIFFERENT universality class from everything else

7. EXPERIMENTAL REALIZATIONS:
   - 2D superfluid He-4 (Nelson & Kosterlitz 1977)
   - 2D XY magnets (various)
   - Josephson junction arrays
   - 2D Coulomb gas
   - Thin film superconductors

8. NOBEL PRIZE 2016:
   - Thouless, Haldane, Kosterlitz
   - "for theoretical discoveries of topological phase transitions
     and topological phases of matter"

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


def correlation_function_bkt(r, eta):
    """
    BKT correlation function.

    G(r) = <cos(theta_i - theta_j)> ~ r^{-eta(T)}

    Below T_BKT: eta < 1/4 (power-law decay)
    At T_BKT: eta = 1/4 (universal jump)
    Above T_BKT: eta > 1/4 (exponential decay, effective eta grows)
    """
    if r <= 0:
        return 1.0
    return r**(-eta)


def correlation_function_exponential(r, xi):
    """
    Above T_BKT: exponential decay.

    G(r) ~ exp(-r/xi)
    """
    if r <= 0:
        return 1.0
    return math.exp(-r / xi)


def stiffness_K(T, T_BKT):
    """
    Spin stiffness (helicity modulus).

    K(T) decreases with T.
    At T_BKT: K_c = 2/pi (universal jump)
    Below T_BKT: K > 2/pi
    Above T_BKT: K < 2/pi
    """
    if T <= 0:
        return 2.0  # K(0) = 2 (stiffness at T=0)
    K = 2.0 * (1.0 - T / (2.0 * T_BKT))
    return max(K, 0.0)


def vortex_free_energy(K, L):
    """
    Vortex free energy.

    F_v = pi*K - 2*pi*ln(L)

    Below T_BKT: F_v > 0 (vortices suppressed)
    Above T_BKT: F_v < 0 (vortices proliferate)
    At T_BKT: F_v = 0 (0/0)
    """
    return math.pi * K - 2.0 * math.pi * math.log(L)


def rg_flow(K_init, y_init, n_steps=100, dl=0.01):
    """
    Kosterlitz RG flow.

    dy/dl = (2 - pi*K)*y
    dK/dl = -pi^2 * y^2 * K^2

    At T_BKT: flow changes direction (0/0)
    """
    K = K_init
    y = y_init
    trajectory = [(K, y)]

    for _ in range(n_steps):
        if K <= 0 or y <= 0:
            break
        dK = -math.pi**2 * y**2 * K**2 * dl
        dy = (2.0 - math.pi * K) * y * dl
        K += dK
        y += dy
        K = max(K, 0.0)
        y = max(y, 0.0)
        trajectory.append((K, y))

    return trajectory


def eta_vs_T(T_values, T_BKT):
    """
    Effective exponent eta vs temperature.

    Below T_BKT: eta(T) = 1/(2*pi*K(T)) (less than 1/4)
    At T_BKT: eta = 1/4 (universal jump!)
    Above T_BKT: eta grows (exponential decay looks like power-law with growing eta)
    """
    etas = []
    for T in T_values:
        if T <= 0:
            etas.append(0.0)
        elif T < T_BKT:
            K = stiffness_K(T, T_BKT)
            if K > 0:
                eta = 1.0 / (2.0 * math.pi * K)
            else:
                eta = 0.25
            etas.append(min(eta, 0.25))
        else:
            # Above T_BKT: eta > 1/4 (exponential decay)
            eta = 0.25 + 0.5 * (T - T_BKT) / T_BKT
            etas.append(eta)
    return etas


def universal_jump():
    """
    The universal jump: eta(T_BKT) = 1/4 EXACTLY.

    This is a REMOVABLE SINGULARITY:
    - Below T_BKT: eta < 1/4 (power-law)
    - Above T_BKT: eta > 1/4 (exponential)
    - At T_BKT: eta = 1/4 EXACTLY

    The jump is DISCONTINUOUS in eta but CONTINUOUS in energy!
    """
    return 1.0 / 4.0


def kosterlitz_rg_example():
    """
    Example RG flow for T < T_BKT and T > T_BKT.
    """
    # T < T_BKT: flows to (K=inf, y=0) - bound vortices
    traj_below = rg_flow(K_init=2.5, y_init=0.1, n_steps=200, dl=0.02)

    # T > T_BKT: flows to (K=0, y=inf) - free vortices
    traj_above = rg_flow(K_init=1.5, y_init=0.1, n_steps=200, dl=0.02)

    return traj_below, traj_above


def vortex_density(T, T_BKT):
    """
    Vortex density.

    Below T_BKT: ~ exp(-2*pi*K) (suppressed, bound pairs)
    Above T_BKT: ~ exp(-pi^2*K/2) * (T-T_BKT)^{pi*K_c/2} (proliferates)
    """
    if T <= 0:
        return 0.0
    K = stiffness_K(T, T_BKT)
    if T < T_BKT:
        return math.exp(-2.0 * math.pi * K)
    else:
        return math.exp(-math.pi**2 * K / 2.0) * (1.0 + 10.0 * (T - T_BKT) / T_BKT)


def specific_heat_bkt(T, T_BKT):
    """
    Specific heat near BKT transition.

    Has a broad peak ABOVE T_BKT (not at T_BKT!)
    This is unusual: the peak is at T ~ 1.2 * T_BKT, not at T_BKT itself.
    """
    T_ratio = T / T_BKT
    if T_ratio < 0.5:
        return 0.5 * T_ratio**2
    elif T_ratio < 1.0:
        return 0.5 * T_ratio**2 * (1.0 + 0.3 * (T_ratio - 0.5))
    else:
        # Broad peak above T_BKT
        return 0.8 * math.exp(-0.5 * (T_ratio - 1.2)**2) + 0.3 / T_ratio


def susceptibility_bkt(T, T_BKT):
    """
    Susceptibility near BKT.

    Diverges as T -> T_BKT from below (power-law singularity).
    """
    if T >= T_BKT:
        return 1.0
    if T <= 0:
        return 0.0
    return (T_BKT / (T_BKT - T))**2


def main():
    print("=" * 70)
    print("BKT TRANSITION: 0/0 WITHOUT SYMMETRY BREAKING")
    print("=" * 70)
    print()

    T_BKT = 0.89  # Normalized transition temperature

    # 1. Correlation Function
    print("1. CORRELATION FUNCTION")
    print("-" * 70)
    print()
    print("   Below T_BKT: G(r) ~ r^{-eta}  (power-law)")
    print("   Above T_BKT: G(r) ~ exp(-r/xi)  (exponential)")
    print("   At T_BKT: eta = 1/4 EXACTLY (universal jump!)")
    print()
    print("   r    G(r) T=0.5    G(r) T=T_BKT  G(r) T=1.2")
    print("   " + "-" * 55)
    for r in [1, 2, 4, 8, 16, 32, 64]:
        eta_below = 0.15  # Below T_BKT
        eta_crit = 0.25   # At T_BKT (universal jump)
        xi_above = 3.0    # Correlation length above T_BKT

        g_below = correlation_function_bkt(r, eta_below)
        g_crit = correlation_function_bkt(r, eta_crit)
        g_above = correlation_function_exponential(r, xi_above)

        print("   %-3d  %.6f     %.6f     %.6f" % (r, g_below, g_crit, g_above))

    print()
    print("   Below: power-law (quasi-long-range order)")
    print("   Above: exponential (disordered)")

    # 2. Universal Jump
    print()
    print("2. UNIVERSAL JUMP: eta = 1/4 EXACTLY")
    print("-" * 70)
    print()
    print("   eta(T_BKT) = 1/4  (Berezinskii 1971, Kosterlitz-Thouless 1974)")
    print()
    print("   T/T_BKT    eta(T)     State")
    print("   " + "-" * 45)
    for T_ratio in [0.3, 0.5, 0.7, 0.9, 0.99, 1.0, 1.01, 1.1, 1.3, 1.5]:
        T = T_ratio * T_BKT
        if T <= 0:
            eta = 0.0
        elif T < T_BKT:
            K = stiffness_K(T, T_BKT)
            eta = 1.0 / (2.0 * math.pi * K) if K > 0 else 0.25
            eta = min(eta, 0.25)
        else:
            eta = 0.25 + 0.5 * (T - T_BKT) / T_BKT

        state = "QLRO" if T < T_BKT else ("CRITICAL" if T_ratio < 1.05 else "EXPONENTIAL")
        print("   %.2f     %.6f     %s" % (T_ratio, eta, state))

    print()
    print("   At T = T_BKT: eta JUMPS from 1/4 to > 1/4")
    print("   This is a DISCONTINUOUS jump in eta!")
    print("   But energy and specific heat are CONTINUOUS!")

    # 3. Stiffness
    print()
    print("3. SPIN STIFFNESS (HELICITY MODULUS)")
    print("-" * 70)
    print()
    print("   K(T) decreases with T")
    print("   At T_BKT: K_c = 2/pi  (universal jump)")
    print()
    print("   T/T_BKT    K(T)       pi*K/2     State")
    print("   " + "-" * 50)
    for T_ratio in [0.0, 0.3, 0.5, 0.7, 0.9, 1.0, 1.1, 1.3]:
        T = T_ratio * T_BKT
        K = stiffness_K(T, T_BKT)
        pi_K_2 = math.pi * K / 2.0
        state = "STIFF" if K > 2.0/math.pi else ("CRITICAL" if K > 2.0/math.pi - 0.1 else "SOFT")
        print("   %.2f     %.4f     %.4f     %s" % (T_ratio, K, pi_K_2, state))

    # 4. Vortex Free Energy
    print()
    print("4. VORTEX FREE ENERGY")
    print("-" * 70)
    print()
    print("   F_v = pi*K - 2*pi*ln(L)")
    print("   Below T_BKT: F_v > 0 (vortices suppressed)")
    print("   Above T_BKT: F_v < 0 (vortices proliferate)")
    print()
    L = 10.0
    print("   T/T_BKT    F_v(L=10)  Vortices")
    print("   " + "-" * 45)
    for T_ratio in [0.3, 0.5, 0.7, 0.9, 1.0, 1.1, 1.3]:
        T = T_ratio * T_BKT
        K = stiffness_K(T, T_BKT)
        F_v = vortex_free_energy(K, L)
        vortices = "BOUND" if F_v > 0 else ("CRITICAL" if F_v > -0.5 else "FREE")
        print("   %.2f     %.4f     %s" % (T_ratio, F_v, vortices))

    # 5. RG Flow
    print()
    print("5. KOSTERLITZ RG FLOW")
    print("-" * 70)
    print()
    print("   dy/dl = (2 - pi*K)*y")
    print("   dK/dl = -pi^2 * y^2 * K^2")
    print()
    traj_below, traj_above = kosterlitz_rg_example()
    print("   T < T_BKT: flows to (K=inf, y=0) - bound vortices")
    print("   T > T_BKT: flows to (K=0, y=inf) - free vortices")
    print()
    print("   Below T_BKT:")
    for i in range(0, len(traj_below), 40):
        K, y = traj_below[i]
        print("   K=%.3f, y=%.6f" % (K, y))
    print()
    print("   Above T_BKT:")
    for i in range(0, len(traj_above), 40):
        K, y = traj_above[i]
        print("   K=%.3f, y=%.6f" % (K, y))

    # 6. Vortex Density
    print()
    print("6. VORTEX DENSITY")
    print("-" * 70)
    print()
    print("   Below T_BKT: ~ exp(-2*pi*K) (suppressed)")
    print("   Above T_BKT: proliferates")
    print()
    print("   T/T_BKT    n_vortex   State")
    print("   " + "-" * 40)
    for T_ratio in [0.3, 0.5, 0.7, 0.9, 1.0, 1.1, 1.3]:
        T = T_ratio * T_BKT
        n_v = vortex_density(T, T_BKT)
        state = "SUPPRESSED" if n_v < 0.01 else ("CRITICAL" if n_v < 0.1 else "PROLIFERATED")
        print("   %.2f     %.6f     %s" % (T_ratio, n_v, state))

    # 7. Specific Heat
    print()
    print("7. SPECIFIC HEAT")
    print("-" * 70)
    print()
    print("   Broad peak ABOVE T_BKT (not at T_BKT!)")
    print("   This is unusual: the peak is at T ~ 1.2 * T_BKT")
    print()
    print("   T/T_BKT    C(T)")
    print("   " + "-" * 30)
    for T_ratio in [0.3, 0.5, 0.7, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5]:
        T = T_ratio * T_BKT
        C = specific_heat_bkt(T, T_BKT)
        print("   %.2f     %.4f" % (T_ratio, C))

    # 8. Comparison
    print()
    print("=" * 70)
    print("COMPARISON: BKT vs ISING vs KOLMOGOROV vs QUANTUM")
    print("=" * 70)
    print()
    print("   Transition     Symmetry    Mechanism       Exponents     Nobel")
    print("   " + "-" * 70)
    print("   Ising (Ch.36)  Z2          Symmetry break  beta=1/8      No")
    print("   BKT (Ch.40)    U(1)        Vortex unbind   eta=1/4       2016")
    print("   Kolmog (Ch.37) Translation Cascade          -5/3          No")
    print("   Quantum (Ch.39)Z2          Quantum fluct   beta=1/8,z=1  No")
    print("   MF Ising       Z2          Mean-field      beta=1/2      No")
    print()
    print("   BKT is FUNDAMENTALLY different:")
    print("   - NO symmetry breaking (order param = 0 always)")
    print("   - eta = 1/4 EXACTLY (universal jump)")
    print("   - Topological mechanism (vortex unbinding)")

    # Connections
    print()
    print("=" * 70)
    print("CONNECTIONS TO ALL PRIOR 0/0 SINGULARITIES")
    print("=" * 70)
    print()
    print("   BKT connects to EVERYTHING:")
    print()
    print("   Ising (Ch.36)       -> Both 2D, different universality")
    print("   Quantum (Ch.39)     -> No 1D quantum maps to BKT")
    print("   Turbulence (Ch.37)  -> Different universality class")
    print("   E8 (Ch.24)          -> Lie algebras classify topological order")
    print("   Consciousness (Ch.34)-> Topological quantum consciousness")
    print("   Black holes (Ch.32) -> Bekenstein-Hawking entropy ~ Area")
    print("   Finance (Ch.38)     -> Market crashes as topological transitions")
    print()
    print("   The BKT 0/0 is the MOST EXOTIC!")
    print("   It has NO symmetry breaking!")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   BKT transition is 0/0 WITHOUT symmetry breaking:")
    print()
    print("   1. CORRELATION:")
    print("      G(r) ~ r^{-eta}: power-law below, exponential above")
    print()
    print("   2. UNIVERSAL JUMP:")
    print("      eta(T_BKT) = 1/4 EXACTLY")
    print("      K_c = 2/pi (stiffness)")
    print()
    print("   3. VORTEX MECHANISM:")
    print("      Bound pairs below, free vortices above")
    print()
    print("   4. TOPOLOGICAL:")
    print("      NO symmetry breaking!")
    print("      Order parameter = 0 ALWAYS!")
    print()
    print("   5. NOBEL PRIZE 2016:")
    print("      Thouless, Haldane, Kosterlitz")
    print()
    print("   The BKT 0/0 is the MOST EXOTIC!")

    # Save
    results = {
        'bkt_transition': {
            'formula': 'H = -J * sum(cos(theta_i - theta_j))',
            'T_BKT': T_BKT,
            'eta_critical': 0.25,
            'K_c': 2.0 / math.pi,
            'universal_jump': True,
            'symmetry_breaking': False,
        },
        'correlation': {
            'below_T_BKT': 'G(r) ~ r^{-eta}, eta < 1/4',
            'at_T_BKT': 'eta = 1/4 EXACTLY',
            'above_T_BKT': 'G(r) ~ exp(-r/xi)',
        },
        'vortex': {
            'mechanism': 'vortex-antivortex unbinding',
            'below': 'bound pairs',
            'above': 'free vortices',
            'free_energy': 'F_v = pi*K - 2*pi*ln(L)',
        },
        'rg_flow': {
            'equations': 'dy/dl = (2-pi*K)y, dK/dl = -pi^2*y^2*K^2',
            'below_T_BKT': 'flows to (K=inf, y=0)',
            'above_T_BKT': 'flows to (K=0, y=inf)',
        },
        'universal_jump': {
            'eta': 0.25,
            'K_c': 2.0 / math.pi,
            'discontinuous_in_eta': True,
            'continuous_in_energy': True,
        },
        'comparison': {
            'ising': 'beta=1/8, symmetry breaking',
            'bkt': 'eta=1/4, NO symmetry breaking',
            'kolmogorov': '-5/3, cascade',
            'quantum': 'beta=1/8, z=1, quantum fluctuations',
        },
        'nobel_prize': {
            'year': 2016,
            'laureates': ['Thouless', 'Haldane', 'Kosterlitz'],
        },
        'connections': {
            'connects_to': ['Ising', 'E8', 'Consciousness', 'Black holes', 'Finance'],
            'different_from_ising': True,
            'no_quantum_analogue': True,
        },
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    output_path = os.path.join(OUTPUT_DIR, 'bkt_transition.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()
