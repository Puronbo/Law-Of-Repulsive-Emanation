#!/usr/bin/env python3
"""
The Big Bang: 0/0 of Origin
==============================

THE UNIVERSE ITSELF emerged from a singularity. The Big Bang IS the
LARGEST 0/0 in existence: nothing -> singularity -> everything.

1. THE SINGULARITY:
   - At T = 0: density = infinity, temperature = infinity
   - This is a 0/0: undefined (singularity)
   - Quantum gravity may resolve this 0/0
   - No "before" Big Bang (time begins at T = 0)

2. INFLATION:
   - T = 10^-32 seconds: exponential expansion
   - Universe expanded by factor of 10^26 in 10^-32 seconds
   - Solves horizon and flatness problems
   - This is the 0/0: exponential growth from tiny seed

3. HORIZON PROBLEM:
   - CMB is uniform in ALL directions
   - But regions too far apart to communicate!
   - Inflation solves this: regions WERE in contact before inflation
   - This is the 0/0: uniformity from chaos

4. FLATNESS PROBLEM:
   - Omega = 1.000 (exactly!)
   - Why is universe so flat?
   - Inflation drives Omega -> 1
   - This is the 0/0: fine-tuning explained

5. MATTER-ANTIMATTER ASYMMETRY:
   - More matter than antimatter (by factor of 10^-9)
   - CP violation in weak interactions
   - This is the 0/0: why does anything exist?

6. CONNECTIONS:
   - Cosmic web (Ch.46): structure formation from Big Bang
   - Arrow of time (Ch.48): Past Hypothesis, low entropy
   - Holographic principle (Ch.47): cosmological information
   - Measurement problem (Ch.49): the observer
   - Black holes (Ch.32): singularities
   - SOC (Ch.41): self-organization from initial conditions

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


def friedmann_equation(Omega_m, Omega_L, a, H0=70.0):
    """
    Friedmann equation: H(a) = H0 * sqrt(Omega_m * a^{-3} + Omega_L)
    """
    rho_m = Omega_m * a**(-3)
    rho_L = Omega_L
    H = H0 * math.sqrt(rho_m + rho_L)
    return H


def scale_factor_matter(Omega_m, t, t0=13.8e9):
    """
    Scale factor for matter-dominated universe: a(t) ~ t^{2/3}
    """
    a = (t / t0)**(2/3)
    return a


def temperature_history(t_seconds):
    """
    Temperature of the universe as function of time.

    T(t) ~ 1/sqrt(t) (approximately)
    """
    # Planck temperature at T = 0
    T_planck = 1.416e32  # K

    if t_seconds <= 0:
        return T_planck

    # Approximate temperature
    T = 1e10 / math.sqrt(t_seconds)  # K (approximate)
    return min(T, T_planck)


def density_history(t_seconds):
    """
    Density of the universe as function of time.

    rho(t) ~ 1/t^2 (approximately)
    """
    rho_planck = 5.16e96  # kg/m^3

    if t_seconds <= 0:
        return rho_planck

    rho = 1e20 / t_seconds**2  # kg/m^3 (approximate)
    return min(rho, rho_planck)


def inflation_factor(e_folds):
    """
    Inflation factor: factor = exp(N)

    N = number of e-folds (typically 50-60)
    """
    factor = math.exp(e_folds)
    return factor


def horizon_problem_solution():
    """
    Horizon problem: why is CMB uniform?

    Before inflation: regions WERE in contact
    After inflation: regions separated but same temperature
    """
    # Size of observable universe before inflation
    size_before = 1e-26  # meters (Planck scale)

    # Size after inflation
    size_after = size_before * inflation_factor(60)

    # Current size
    size_now = 8.8e26  # meters (observable universe)

    return size_before, size_after, size_now


def flatness_problem_solution(Omega_initial, e_folds):
    """
    Flatness problem: why is Omega = 1?

    Inflation drives Omega -> 1 exponentially.
    """
    # During inflation, Omega approaches 1
    # Omega(t) = 1 / (1 + (1/Omega_0 - 1) * exp(-2*N))
    Omega = 1.0 / (1.0 + (1.0/Omega_initial - 1.0) * math.exp(-2 * e_folds))
    return Omega


def matter_antimatter_asymmetry():
    """
    Matter-antimatter asymmetry: why more matter?

    CP violation in weak interactions.
    Asymmetry parameter: eta = (n_b - n_bar) / n_gamma ~ 6e-10
    """
    eta = 6e-10  # Observed asymmetry
    return eta


def timeline_events():
    """
    Key events in Big Bang history.
    """
    events = [
        (0, "T = 0", "Singularity (0/0)"),
        (1e-43, "Planck time", "Quantum gravity dominates"),
        (1e-36, "GUT epoch", "Strong force separates"),
        (1e-32, "Inflation", "Exponential expansion"),
        (1e-12, "Electroweak", "W, Z bosons appear"),
        (1e-6, "Quark epoch", "Quarks form protons"),
        (1, "Nucleosynthesis", "First nuclei form"),
        (3.8e5, "Recombination", "CMB released"),
        (1e9, "First stars", "Stars form"),
        (1.38e10, "Now", "Current universe"),
    ]
    return events


def planck_units():
    """
    Planck units: fundamental scales of quantum gravity.
    """
    l_P = 1.616e-35  # meters (Planck length)
    t_P = 5.391e-44  # seconds (Planck time)
    T_P = 1.416e32   # K (Planck temperature)
    rho_P = 5.16e96  # kg/m^3 (Planck density)
    E_P = 1.956e9    # J (Planck energy)

    return l_P, t_P, T_P, rho_P, E_P


def quantum_gravity_resolution():
    """
    Quantum gravity may resolve the Big Bang singularity.

    - Loop quantum cosmology: bounce instead of singularity
    - String theory: pre-Big Bang scenarios
    - Causal set theory: discrete spacetime
    """
    resolutions = [
        "Loop quantum cosmology: Big Bounce",
        "String theory: pre-Big Bang",
        "Causal set theory: discrete spacetime",
        "Asymptotic safety: renormalizable gravity",
    ]
    return resolutions


def main():
    print("=" * 70)
    print("THE BIG BANG: 0/0 OF ORIGIN")
    print("=" * 70)
    print()
    random.seed(42)
    np.random.seed(42)

    # 1. The Singularity
    print("1. THE SINGULARITY: THE COSMIC 0/0")
    print("-" * 70)
    print()
    print("   At T = 0: density = infinity, temperature = infinity")
    print("   This is a 0/0: undefined (singularity)")
    print("   No 'before' Big Bang (time begins at T = 0)")
    print()
    l_P, t_P, T_P, rho_P, E_P = planck_units()
    print("   Planck scales (quantum gravity):")
    print("   Planck length:     %.2e meters" % l_P)
    print("   Planck time:       %.2e seconds" % t_P)
    print("   Planck temperature: %.2e K" % T_P)
    print("   Planck density:    %.2e kg/m^3" % rho_P)
    print("   Planck energy:     %.2e J" % E_P)
    print()
    print("   Below Planck scales: quantum gravity dominates")
    print("   The singularity may be resolved by quantum gravity!")

    # 2. Timeline
    print()
    print("2. TIMELINE OF THE UNIVERSE")
    print("-" * 70)
    print()
    events = timeline_events()
    print("   Time              Event")
    print("   " + "-" * 50)
    for time_s, name, desc in events:
        if time_s == 0:
            print("   %-18s %-20s %s" % ("T = 0", name, desc))
        elif time_s < 1e-3:
            print("   %-18s %-20s %s" % ("%.0e s" % time_s, name, desc))
        elif time_s < 1e6:
            print("   %-18s %-20s %s" % ("%.0e s" % time_s, name, desc))
        else:
            print("   %-18s %-20s %s" % ("%.1e s" % time_s, name, desc))

    # 3. Inflation
    print()
    print("3. INFLATION: EXPONENTIAL EXPANSION")
    print("-" * 70)
    print()
    print("   T = 10^-32 seconds: exponential expansion")
    print("   Universe expanded by factor of 10^26 in 10^-32 seconds!")
    print()
    print("   e-folds    Factor")
    print("   " + "-" * 30)
    for N in [10, 20, 30, 40, 50, 60]:
        factor = inflation_factor(N)
        print("   %-10d %.2e" % (N, factor))
    print()
    print("   60 e-folds = factor of 10^26!")
    print("   This is the 0/0: exponential growth from tiny seed!")

    # 4. Horizon Problem
    print()
    print("4. HORIZON PROBLEM")
    print("-" * 70)
    print()
    print("   CMB is uniform in ALL directions")
    print("   But regions too far apart to communicate!")
    print()
    size_before, size_after, size_now = horizon_problem_solution()
    print("   Size before inflation: %.2e meters" % size_before)
    print("   Size after inflation:  %.2e meters" % size_after)
    print("   Current size:          %.2e meters" % size_now)
    print()
    print("   Inflation solved this: regions WERE in contact!")
    print("   This is the 0/0: uniformity from chaos!")

    # 5. Flatness Problem
    print()
    print("5. FLATNESS PROBLEM: OMEGA = 1.000")
    print("-" * 70)
    print()
    print("   Omega = 1.000 (exactly!)")
    print("   Inflation drives Omega -> 1 exponentially")
    print()
    print("   Omega_initial    e-folds    Omega_final")
    print("   " + "-" * 45)
    for Omega_i in [0.5, 0.9, 0.99, 0.999]:
        Omega_f = flatness_problem_solution(Omega_i, 60)
        print("   %-17.3f %-11d %.10f" % (Omega_i, 60, Omega_f))
    print()
    print("   Inflation makes Omega -> 1!")
    print("   This explains why universe is flat!")

    # 6. Matter-Antimatter
    print()
    print("6. MATTER-ANTIMATTER ASYMMETRY")
    print("-" * 70)
    print()
    eta = matter_antimatter_asymmetry()
    print("   Asymmetry parameter: eta = %.1e" % eta)
    print()
    print("   For every 10^9 antimatter particles:")
    print("   there were 10^9 + 6 matter particles!")
    print()
    print("   This tiny asymmetry created ALL matter in universe!")
    print("   This is the 0/0: why does anything exist?")

    # 7. Temperature History
    print()
    print("7. TEMPERATURE HISTORY")
    print("-" * 70)
    print()
    print("   T(t) ~ 1/sqrt(t)")
    print()
    print("   Time          Temperature")
    print("   " + "-" * 35)
    for t in [1e-43, 1e-32, 1e-12, 1e-6, 1, 3.8e5, 1.38e10]:
        T = temperature_history(t)
        if t < 1e-3:
            print("   %-13s %.2e K" % ("%.0e s" % t, T))
        elif t < 1e6:
            print("   %-13s %.2e K" % ("%.0e s" % t, T))
        else:
            print("   %-13s %.2e K" % ("%.1e s" % t, T))

    # 8. Quantum Gravity Resolution
    print()
    print("8. QUANTUM GRAVITY RESOLUTION")
    print("-" * 70)
    print()
    print("   The singularity may be resolved by quantum gravity:")
    print()
    resolutions = quantum_gravity_resolution()
    for i, res in enumerate(resolutions, 1):
        print("   %d. %s" % (i, res))
    print()
    print("   These theories replace the 0/0 singularity")
    print("   with a smooth transition (Big Bounce, etc.)")

    # 9. Connections
    print()
    print("=" * 70)
    print("CONNECTIONS TO ALL PRIOR 0/0 SINGULARITIES")
    print("=" * 70)
    print()
    print("   The Big Bang connects to EVERYTHING:")
    print()
    print("   Cosmic web (Ch.46)     -> Structure formation")
    print("   Arrow of time (Ch.48)  -> Past Hypothesis")
    print("   Holographic (Ch.47)    -> Cosmological info")
    print("   Measurement (Ch.49)    -> The observer")
    print("   Black holes (Ch.32)    -> Singularities")
    print("   SOC (Ch.41)            -> Self-organization")
    print("   Networks (Ch.45)       -> Cosmic web network")
    print("   Dark matter (Ch.20)    -> Structure formation")
    print()
    print("   The Big Bang is the ORIGIN of ALL 0/0 singularities!")
    print("   EVERYTHING emerged from this singularity!")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   The Big Bang is the 0/0 of origin:")
    print()
    print("   1. SINGULARITY: density = infinity (0/0 at T = 0)")
    print("   2. INFLATION: 10^26 expansion in 10^-32 seconds")
    print("   3. HORIZON PROBLEM: uniformity from chaos")
    print("   4. FLATNESS PROBLEM: Omega = 1.000 (inflation solves)")
    print("   5. MATTER-ANTIMATTER: tiny asymmetry creates everything")
    print()
    print("   The universe emerged from a singularity (0/0)!")
    print("   Quantum gravity may resolve this 0/0!")

    # Save
    results = {
        'singularity': {
            'density_infinity': True,
            'temperature_infinity': True,
            '0over0': True,
            'quantum_gravity_resolves': True,
        },
        'inflation': {
            'factor_10_26': True,
            'time_10_neg_32': True,
            'solves_horizon': True,
            'solves_flatness': True,
        },
        'horizon_problem': {
            'cmb_uniform': True,
            'regions_separated': True,
            'inflation_solves': True,
        },
        'flatness_problem': {
            'Omega_equal_1': True,
            'inflation_drives_1': True,
        },
        'matter_antimatter': {
            'asymmetry_6e_neg_10': True,
            'CP_violation': True,
        },
        'timeline': {
            'planck_time': 5.391e-44,
            'inflation_time': 1e-32,
            'nucleosynthesis': 1,
            'recombination': 3.8e5,
            'now': 1.38e10,
        },
        'connections': {
            'connects_to': ['Cosmic web', 'Arrow of time', 'Holographic', 'Measurement', 'Black holes', 'SOC', 'Networks', 'Dark matter'],
            'origin_of_all_0over0': True,
        },
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    output_path = os.path.join(OUTPUT_DIR, 'big_bang_origin.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()
