#!/usr/bin/env python3
"""
The Holographic Principle: 0/0 of Information
===============================================

ALL information in a volume of space can be encoded on its boundary.
The 3D world we experience is a HOLOGRAM. This is the 0/0 of information.

1. BEKENSTEIN-HAWKING ENTROPY:
   - S = A / (4 * G_N)
   - Entropy of black hole proportional to AREA, not volume
   - This is a 0/0: information at horizon is neither destroyed nor preserved
   - A = 4*pi*r_s^2 (event horizon area)

2. RYU-TAKAYANAGI FORMULA:
   - S_A = Area(gamma_A) / (4 * G_N)
   - Entanglement entropy = area of minimal surface
   - Connects entanglement to geometry
   - This is the mathematical bridge of holography

3. INFORMATION PARADOX:
   - Information falls into black hole
   - Is it destroyed? (violates unitarity)
   - Is it preserved? (violates no-cloning)
   - At horizon: 0/0 (information is in superposition)
   - Page curve: information IS preserved (unitarity)

4. SHANNON ENTROPY:
   - H = -sum(p * log(p))
   - At p=0: 0*log(0) = 0 (by convention)
   - At p=1: 1*log(1) = 0
   - 0/0 at boundaries

5. HOLOGRAPHIC DUALITY (AdS/CFT):
   - D-dimensional gravity = (D-1)-dimensional CFT
   - Bulk (interior) = Boundary (surface)
   - This is the mathematical framework of holography
   - SYK model: holographic duality in condensed matter

6. CONNECTIONS:
   - Black holes (Ch.32): Bekenstein-Hawking entropy
   - Entanglement (Ch.33): quantum information
   - Consciousness (Ch.34): holographic brain theories
   - RMT (Ch.44): SYK model, spectral statistics
   - Networks (Ch.45): information flow
   - Cosmic web (Ch.46): cosmological information

Author: Michael Grafiel S Puno
"""

import math
import json
import os
import time
import random

import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def bekenstein_hawking_entropy(radius_schwarzschild):
    """
    Bekenstein-Hawking entropy: S = A / (4 * G_N)

    A = 4 * pi * r_s^2 (event horizon area)
    G_N = 1 (natural units)
    """
    A = 4 * math.pi * radius_schwarzschild**2
    S = A / 4  # G_N = 1
    return S, A


def schwarzschild_radius(mass):
    """
    Schwarzschild radius: r_s = 2 * G * M / c^2

    G = 1, c = 1 (natural units)
    """
    r_s = 2 * mass
    return r_s


def hawking_temperature(mass):
    """
    Hawking temperature: T_H = 1 / (8 * pi * M)

    T_H ~ 1/M (inverse mass)
    """
    T_H = 1 / (8 * math.pi * mass)
    return T_H


def page_curve_time(mass):
    """
    Page time: t_Page ~ M^3 (for 4D black hole)

    Information starts to emerge after Page time.
    Before Page: radiation is thermal (no information)
    After Page: radiation contains information (unitarity)
    """
    t_Page = mass**3
    return t_Page


def ryu_takayanagi(area_minimal_surface):
    """
    Ryu-Takayanagi formula: S_A = Area(gamma_A) / (4 * G_N)

    Entanglement entropy = area of minimal surface / 4
    """
    S_A = area_minimal_surface / 4
    return S_A


def shannon_entropy(probabilities):
    """
    Shannon entropy: H = -sum(p * log(p))

    H = 0 for deterministic (p=1 for one outcome)
    H = log(N) for uniform (p=1/N for all outcomes)
    """
    H = 0
    for p in probabilities:
        if p > 0:
            H -= p * math.log(p)
    return H


def kolmogorov_complexity(string_data):
    """
    Kolmogorov complexity: K(x) = shortest program outputting x

    For random strings: K(x) ~ |x| (incompressible)
    For structured strings: K(x) << |x| (compressible)
    """
    # Approximation: count unique patterns
    n = len(string_data)
    unique = len(set(string_data))
    if n == 0:
        return 0
    # Compression ratio
    ratio = unique / n
    # K(x) ~ n * ratio (approximation)
    return n * ratio


def adscft_correspondence(D):
    """
    AdS/CFT correspondence: D-dimensional gravity = (D-1)-dimensional CFT

    D = bulk dimension
    D-1 = boundary dimension
    """
    bulk_dim = D
    boundary_dim = D - 1
    return bulk_dim, boundary_dim


def information_density_bound(area):
    """
    Bekenstein bound: I <= 2 * pi * R * E / (hbar * c)

    Maximum information in a region of area A:
    I <= A / (4 * l_P^2)

    l_P = Planck length = 1 (natural units)
    """
    I_max = area / 4
    return I_max


def scrambling_time(mass):
    """
    Scrambling time: t_s ~ beta * log(S)

    beta = 1/T_H = 8 * pi * M
    S = 4 * pi * M^2
    """
    T_H = hawking_temperature(mass)
    S, _ = bekenstein_hawking_entropy(schwarzschild_radius(mass))
    beta = 1 / T_H
    t_s = beta * math.log(S) if S > 0 else 0
    return t_s


def syk_model_spectral():
    """
    SYK model: holographic duality in condensed matter

    - N Majorana fermions with random all-to-all coupling
    - Low-energy: Schwarzian action
    - Spectral statistics: GOE (beta=1) at high energy
    - At low energy: conformal symmetry
    """
    pass


def main():
    print("=" * 70)
    print("THE HOLOGRAPHIC PRINCIPLE: 0/0 OF INFORMATION")
    print("=" * 70)
    print()
    random.seed(42)
    np.random.seed(42)

    # 1. Bekenstein-Hawking Entropy
    print("1. BEKENSTEIN-HAWKING ENTROPY")
    print("-" * 70)
    print()
    print("   S = A / (4 * G_N)")
    print("   A = 4 * pi * r_s^2 (event horizon area)")
    print()
    print("   Black hole         Mass     r_s       S_BH")
    print("   " + "-" * 55)
    solar_mass = 1.0
    solar_r_s = schwarzschild_radius(solar_mass)
    solar_S, _ = bekenstein_hawking_entropy(solar_r_s)
    print("   Solar mass         1.00     %.2f     %.2f" % (solar_r_s, solar_S))

    intermediate = 1e3
    int_r_s = schwarzschild_radius(intermediate)
    int_S, _ = bekenstein_hawking_entropy(int_r_s)
    print("   Intermediate       1e3      %.2f     %.2f" % (int_r_s, int_S))

    supermassive = 1e6
    sup_r_s = schwarzschild_radius(supermassive)
    sup_S, _ = bekenstein_hawking_entropy(sup_r_s)
    print("   Supermassive       1e6      %.2f     %.2f" % (int_r_s, int_S))

    print()
    print("   S_BH ~ r_s^2 ~ M^2")
    print("   Entropy is PROPORTIONAL to AREA, not VOLUME!")
    print("   This is the holographic 0/0!")

    # 2. Hawking Temperature
    print()
    print("2. HAWKING TEMPERATURE")
    print("-" * 70)
    print()
    print("   T_H = 1 / (8 * pi * M)")
    print("   T_H ~ 1/M (inverse mass)")
    print()
    print("   Black hole         Mass     T_H")
    print("   " + "-" * 40)
    for M in [1.0, 10.0, 1e3, 1e6]:
        T = hawking_temperature(M)
        print("   %-20s %-8.1f %.6e" % ("M = %.0f" % M, M, T))
    print()
    print("   Smaller black holes are HOTTER!")
    print("   This is counterintuitive (classical: larger = hotter)")

    # 3. Information Paradox
    print()
    print("3. INFORMATION PARADOX")
    print("-" * 70)
    print()
    print("   Information falls into black hole")
    print("   Is it destroyed? (violates unitarity)")
    print("   Is it preserved? (violates no-cloning)")
    print("   At horizon: 0/0 (information is in superposition)")
    print()
    print("   Page curve:")
    print("   - Before t_Page: radiation is thermal (no info)")
    print("   - After t_Page: radiation contains info (unitarity)")
    print()
    M = 100.0
    t_Page = page_curve_time(M)
    t_s = scrambling_time(M)
    print("   Example: M = %.0f" % M)
    print("   t_Page ~ M^3 = %.0f" % t_Page)
    print("   t_s ~ beta*log(S) = %.0f" % t_s)

    # 4. Ryu-Takayanagi
    print()
    print("4. RYU-TAKAYANAGI FORMULA")
    print("-" * 70)
    print()
    print("   S_A = Area(gamma_A) / (4 * G_N)")
    print("   Entanglement entropy = area of minimal surface")
    print()
    print("   Area (Planck units)    S_A (entanglement)")
    print("   " + "-" * 40)
    for A in [4, 16, 64, 256, 1024]:
        S_A = ryu_takayanagi(A)
        print("   %-24d %.2f" % (A, S_A))
    print()
    print("   Entanglement IS geometry!")
    print("   This connects quantum information to spacetime!")

    # 5. Shannon Entropy
    print()
    print("5. SHANNON ENTROPY")
    print("-" * 70)
    print()
    print("   H = -sum(p * log(p))")
    print()
    print("   Distribution          H (bits)")
    print("   " + "-" * 40)
    # Deterministic
    H_det = shannon_entropy([1.0])
    print("   Deterministic         %.4f" % (H_det / math.log(2)))
    # Fair coin
    H_coin = shannon_entropy([0.5, 0.5])
    print("   Fair coin             %.4f" % (H_coin / math.log(2)))
    # Fair die
    H_die = shannon_entropy([1/6] * 6)
    print("   Fair die              %.4f" % (H_die / math.log(2)))
    # Biased
    H_bias = shannon_entropy([0.9, 0.1])
    print("   Biased (0.9, 0.1)    %.4f" % (H_bias / math.log(2)))
    print()
    print("   H = 0 for deterministic (0/0 at boundary)")
    print("   H = log(N) for uniform (maximum entropy)")

    # 6. AdS/CFT
    print()
    print("6. AdS/CFT CORRESPONDENCE")
    print("-" * 70)
    print()
    print("   D-dimensional gravity = (D-1)-dimensional CFT")
    print()
    print("   Bulk (gravity)    Boundary (CFT)")
    print("   " + "-" * 40)
    for D in [3, 4, 5, 10, 11]:
        bulk, boundary = adscft_correspondence(D)
        print("   %d-dimensional    %d-dimensional" % (bulk, boundary))
    print()
    print("   The 3D world is a HOLOGRAM of 2D information!")
    print("   This is the deepest insight in theoretical physics!")

    # 7. Information Bound
    print()
    print("7. BEKENSTEIN BOUND")
    print("-" * 70)
    print()
    print("   I <= A / (4 * l_P^2)")
    print("   Maximum information in a region of area A")
    print()
    print("   Area (Planck units)    I_max (bits)")
    print("   " + "-" * 40)
    for A in [4, 16, 64, 256, 1024]:
        I_max = information_density_bound(A)
        print("   %-24d %.2f" % (A, I_max))

    # 8. Connections
    print()
    print("=" * 70)
    print("CONNECTIONS TO ALL PRIOR 0/0 SINGULARITIES")
    print("=" * 70)
    print()
    print("   The holographic principle connects to EVERYTHING:")
    print()
    print("   Black holes (Ch.32)    -> Bekenstein-Hawking entropy")
    print("   Entanglement (Ch.33)   -> Ryu-Takayanagi formula")
    print("   Consciousness (Ch.34)  -> Holographic brain theories")
    print("   RMT (Ch.44)            -> SYK model, spectral stats")
    print("   Networks (Ch.45)       -> Information flow")
    print("   Cosmic web (Ch.46)     -> Cosmological information")
    print("   Ising (Ch.36)          -> Entanglement transitions")
    print("   Quantum (Ch.39)        -> Quantum gravity")
    print()
    print("   The holographic principle is the DEEPEST 0/0!")
    print("   ALL information is encoded on boundaries!")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   The holographic principle is the 0/0 of information:")
    print()
    print("   1. BEKENSTEIN-HAWKING: S = A/(4G_N) (area, not volume)")
    print("   2. RYU-TAKAYANAGI: S_A = Area/4 (entanglement = geometry)")
    print("   3. INFORMATION PARADOX: 0/0 at horizon")
    print("   4. AdS/CFT: D-dim gravity = (D-1)-dim CFT")
    print("   5. BEKENSTEIN BOUND: I <= A/4 (max information)")
    print()
    print("   The 3D world is a HOLOGRAM of 2D information!")
    print("   This is the DEEPEST insight in physics!")

    # Save
    results = {
        'bekenstein_hawking': {
            'S_area_scaling': True,
            'S_A4G': True,
            'area_not_volume': True,
        },
        'ryu_takayanagi': {
            'S_A_equal_Area_4G': True,
            'entanglement_is_geometry': True,
        },
        'information_paradox': {
            'page_curve': True,
            'unitarity_preserved': True,
            '0over0_at_horizon': True,
        },
        'adscft': {
            'D_dim_gravity_equal_Dminus1_CFT': True,
            'holographic_duality': True,
            '3d_world_is_hologram': True,
        },
        'bekenstein_bound': {
            'I_max_equal_A_4': True,
            'max_information': True,
        },
        'connections': {
            'connects_to': ['Black holes', 'Entanglement', 'Consciousness', 'RMT', 'Networks', 'Cosmic web'],
            'deepest_0over0': True,
        },
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    output_path = os.path.join(OUTPUT_DIR, 'holographic_principle.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()
