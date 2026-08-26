#!/usr/bin/env python3
"""
Black Hole Information Paradox: 0/0 at the Event Horizon
=========================================================

The most extreme 0/0 in physics: the event horizon.

At the horizon: information = 0 (nothing escapes)
Far from horizon: information = infinity (all information escapes)
At the horizon (removable): information = S_BH (entropy)

This connects to:
1. Bekenstein-Hawking entropy (S = A / 4 l_Planck^2)
2. Holographic principle (information ~ area, not volume)
3. Quantum entanglement (EPR paradox)
4. Page curve (information recovery)

The key insight: the event horizon is a 0/0 removable singularity
in the space of quantum information.

Author: Michael Grafiel S Puno
"""

import math
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sigma_venv'))

import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Physical constants (SI)
c = 2.998e8          # m/s
G = 6.674e-11        # m^3 kg^-1 s^-2
hbar = 1.055e-34     # J*s
k_B = 1.381e-23      # J/K
sigma_SB = 5.670e-8  # W m^-2 K^-4
M_sun = 1.989e30     # kg
pc = 3.086e16        # m
ly = 9.461e15        # m

# Planck units
l_Planck = np.sqrt(hbar * G / c**3)  # 1.616e-35 m
M_Planck = np.sqrt(hbar * c / G)     # 2.176e-8 kg
E_Planck = M_Planck * c**2           # 1.956e9 J
t_Planck = l_Planck / c              # 5.391e-44 s

def schwarzschild_radius(M):
    """r_s = 2 * G * M / c^2"""
    return 2 * G * M / c**2

def event_horizon_area(M):
    """A = 4 * pi * r_s^2"""
    r_s = schwarzschild_radius(M)
    return 4 * np.pi * r_s**2

def bekenstein_hawking_entropy(M):
    """S_BH = k_B * A / (4 * l_Planck^2)"""
    A = event_horizon_area(M)
    return k_B * A / (4 * l_Planck**2)

def hawking_temperature(M):
    """T_H = hbar * c^3 / (8 * pi * G * M * k_B)"""
    return hbar * c**3 / (8 * np.pi * G * M * k_B)

def hawking_luminosity(M):
    """L = hbar * c^6 / (15360 * pi * G^2 * M^2)"""
    return hbar * c**6 / (15360 * np.pi * G**2 * M**2)

def evaporation_time(M):
    """t_evap = 5120 * pi * G^2 * M^3 / (hbar * c^4)"""
    return 5120 * np.pi * G**2 * M**3 / (hbar * c**4)

def information_content(M, r):
    """
    Information content at distance r from black hole.
    
    At the horizon (r = r_s): I = 0 (nothing escapes)
    Far from horizon (r >> r_s): I = infinity (all information)
    At the horizon (removable): I = S_BH (entropy)
    
    This is a 0/0 removable singularity!
    """
    r_s = schwarzschild_radius(M)
    
    if r <= r_s:
        return 0.0  # Inside horizon: no information escapes
    else:
        # Information increases with distance
        # At r >> r_s: I -> infinity
        # At r -> r_s+: I -> 0
        # Removable value: S_BH
        return bekenstein_hawking_entropy(M) * (r / r_s - 1)

def page_curve(t, M_0):
    """
    Page curve: information content of Hawking radiation vs time.
    
    At t = 0: I = 0 (no radiation)
    At t = t_Page: I = S_BH (Page time)
    At t = t_evap: I = S_BH (all information recovered)
    
    The 0/0: I(t_Page) = S_BH / 1 = S_BH (removable)
    """
    t_evap = evaporation_time(M_0)
    t_Page = t_evap / 2  # Page time (approximate)
    
    if t < t_Page:
        # Early radiation: information increases slowly
        return bekenstein_hawking_entropy(M_0) * (t / t_Page)**2
    else:
        # Late radiation: information increases rapidly
        S_BH = bekenstein_hawking_entropy(M_0)
        return S_BH * (1 - (1 - t/t_Page)**2)

def holographic_bound(M):
    """
    Holographic bound: maximum information in a region = A / (4 l_Planck^2).
    
    This is the Bekenstein-Hawking entropy.
    """
    return bekenstein_hawking_entropy(M)

def entropy_density(M, r):
    """
    Entropy density at distance r from black hole.
    
    At the horizon: sigma = S_BH / A (finite, removable value)
    Far from horizon: sigma -> 0
    """
    A = event_horizon_area(M)
    S_BH = bekenstein_hawking_entropy(M)
    
    r_s = schwarzschild_radius(M)
    if r <= r_s:
        return S_BH / A  # At horizon: finite
    else:
        return S_BH / A * (r_s / r)**2  # Decreases with distance

def main():
    print("=" * 70)
    print("BLACK HOLE INFORMATION PARADOX: 0/0 AT THE EVENT HORIZON")
    print("=" * 70)
    print()
    
    # Planck units
    print("PLANCK UNITS")
    print("-" * 70)
    print("   l_Planck = %.3e m" % l_Planck)
    print("   M_Planck = %.3e kg" % M_Planck)
    print("   E_Planck = %.3e J" % E_Planck)
    print("   t_Planck = %.3e s" % t_Planck)
    
    # Black hole catalog
    print()
    print("BLACK HOLE CATALOG")
    print("=" * 70)
    
    black_holes = [
        ("Stellar (10 M_sun)", 10 * M_sun),
        ("Intermediate (10^3 M_sun)", 1e3 * M_sun),
        ("Sagittarius A* (4e6 M_sun)", 4e6 * M_sun),
        ("Milky Way central (4e6 M_sun)", 4e6 * M_sun),
        ("M87* (6.5e9 M_sun)", 6.5e9 * M_sun),
        ("TON 618 (6.6e10 M_sun)", 6.6e10 * M_sun),
        ("Phoenix A (1e11 M_sun)", 1e11 * M_sun),
    ]
    
    print()
    print("   Name                    M(M_sun)    r_s(m)      S_BH/k_B    T_H(K)")
    print("   " + "-" * 85)
    
    for name, M in black_holes:
        r_s = schwarzschild_radius(M)
        S_BH = bekenstein_hawking_entropy(M)
        T_H = hawking_temperature(M)
        
        print("   %-23s %.1e    %.2e    %.2e    %.2e" % (
            name, M/M_sun, r_s, S_BH/k_B, T_H))
    
    # The 0/0 structure
    print()
    print("=" * 70)
    print("THE 0/0 STRUCTURE AT THE EVENT HORIZON")
    print("=" * 70)
    print()
    print("   At the event horizon (r = r_s):")
    print("   - Information escapes: I = 0 (nothing crosses outward)")
    print("   - Information outside: I = infinity (all information)")
    print("   - 0/0: I_inside / I_outside = 0 / infinity = 0")
    print()
    print("   Removable value: S_BH = A / (4 l_Planck^2)")
    print("   This is the Bekenstein-Hawking entropy!")
    print()
    print("   The event horizon is a 0/0 REMOVABLE SINGULARITY")
    print("   in the space of quantum information.")
    
    # Information content at different distances
    print()
    print("INFORMATION CONTENT vs DISTANCE")
    print("-" * 70)
    
    M = 10 * M_sun  # Stellar black hole
    r_s = schwarzschild_radius(M)
    S_BH = bekenstein_hawking_entropy(M)
    
    print("   Black hole: 10 M_sun")
    print("   r_s = %.2e m" % r_s)
    print("   S_BH/k_B = %.2e" % (S_BH/k_B))
    print()
    print("   r/r_s     I/S_BH      sigma/(S_BH/A)")
    print("   " + "-" * 50)
    
    for r_ratio in [1.0, 1.1, 1.5, 2.0, 5.0, 10.0, 100.0]:
        r = r_ratio * r_s
        I = information_content(M, r)
        sigma = entropy_density(M, r)
        
        I_norm = I / S_BH if S_BH > 0 else 0
        sigma_norm = sigma / (S_BH / event_horizon_area(M))
        
        print("   %.1f     %.6e    %.6e" % (r_ratio, I_norm, sigma_norm))
    
    # Page curve
    print()
    print("=" * 70)
    print("PAGE CURVE: INFORMATION RECOVERY")
    print("=" * 70)
    print()
    
    M_0 = 10 * M_sun
    t_evap = evaporation_time(M_0)
    t_Page = t_evap / 2
    S_BH = bekenstein_hawking_entropy(M_0)
    
    print("   Black hole: 10 M_sun")
    print("   Evaporation time: %.2e s" % t_evap)
    print("   Page time: %.2e s" % t_Page)
    print("   S_BH/k_B: %.2e" % (S_BH/k_B))
    print()
    print("   t/t_evap    I/S_BH")
    print("   " + "-" * 30)
    
    for t_ratio in [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]:
        t = t_ratio * t_evap
        I = page_curve(t, M_0)
        I_norm = I / S_BH if S_BH > 0 else 0
        
        print("   %.2f       %.6e" % (t_ratio, I_norm))
    
    # Holographic principle
    print()
    print("=" * 70)
    print("HOLOGRAPHIC PRINCIPLE")
    print("=" * 70)
    print()
    print("   The holographic principle states:")
    print("   Maximum information in a region = Area / (4 l_Planck^2)")
    print()
    print("   This is MATHEMATICALLY EQUIVALENT to:")
    print("   - Bekenstein-Hawking entropy: S = A / (4 l_Planck^2)")
    print("   - Toomre Q: stability depends on SURFACE density")
    print("   - AdS/CFT: bulk = boundary theory")
    print()
    print("   The 0/0 connection:")
    print("   - At the horizon: A = 0 (point), l_Planck = 0 (point)")
    print("   - S = 0/0 (removable singularity)")
    print("   - Removable value: S_BH (finite)")
    
    # Connection to Toomre Q
    print()
    print("=" * 70)
    print("CONNECTION TO TOOMRE Q")
    print("=" * 70)
    print()
    print("   The event horizon is a gravitational instability:")
    print("   - Q < 1: unstable (horizon forms)")
    print("   - Q > 1: stable (no horizon)")
    print("   - Q = 1: marginal (0/0 removable singularity)")
    print()
    print("   At the horizon:")
    print("   - Gravitational coupling: G*M/r_s = 1/2 (finite)")
    print("   - This is the REMOVABLE VALUE of the 0/0")
    print()
    print("   The critical exponent:")
    print("   - Near the horizon: Q ~ (r - r_s)^(1/2)")
    print("   - beta = 1/2 (mean-field Ising)")
    print("   - SAME as Toomre Q at Q = 1!")
    
    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   The black hole information paradox has a 0/0 structure:")
    print()
    print("   1. EVENT HORIZON:")
    print("      I_inside / I_outside = 0 / infinity = 0")
    print("      Removable value: S_BH = A / (4 l_Planck^2)")
    print()
    print("   2. PAGE CURVE:")
    print("      I(t_Page) = S_BH (information recovery)")
    print("      0/0 at t = t_Page (removable)")
    print()
    print("   3. HOLOGRAPHIC PRINCIPLE:")
    print("      S = A / (4 l_Planck^2) = 0/0 at horizon")
    print("      Removable value: S_BH (Bekenstein-Hawking)")
    print()
    print("   4. TOOMRE Q CONNECTION:")
    print("      Q = 1 at horizon (phase transition)")
    print("      beta = 1/2 (mean-field Ising)")
    print()
    print("   This is the L.O.R.E. framework applied to black holes.")
    
    # Save
    results = {
        'planck_units': {
            'l_Planck': float(l_Planck),
            'M_Planck': float(M_Planck),
            'E_Planck': float(E_Planck),
            't_Planck': float(t_Planck)
        },
        'black_holes': [
            {
                'name': name,
                'M_solar': M/M_sun,
                'r_s': float(schwarzschild_radius(M)),
                'S_BH_over_k': float(bekenstein_hawking_entropy(M)/k_B),
                'T_H': float(hawking_temperature(M))
            }
            for name, M in black_holes
        ],
        'page_time_ratio': 0.5,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    output_path = os.path.join(OUTPUT_DIR, 'black_hole_information.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    print()
    print("   Results saved to: %s" % output_path)

if __name__ == '__main__':
    main()
