#!/usr/bin/env python3
"""
Turbulence & the Kolmogorov Spectrum: 0/0 at the Dissipation Scale
====================================================================

Turbulence is the last great unsolved problem of classical physics.
The Kolmogorov 1941 (K41) theory reveals a 0/0 removable singularity
at the dissipation scale:

1. KOLMOGOROV ENERGY SPECTRUM (1941):
   - Inertial range: E(k) = C_K * epsilon^{2/3} * k^{-5/3}
   - The -5/3 exponent is UNIVERSAL across all turbulent flows
   - At dissipation scale eta: spectrum = 0/0 (inertial meets viscous)

2. RICHARDSON CASCADE (1922):
   - "Big whorls have little whorls which feed on their velocity"
   - Energy cascades from large scales to small scales
   - Self-similar 0/0 at each scale (fractal structure)
   - The cascade is a removable singularity in scale space

3. DISSIPATION SCALE:
   - eta = (nu^3 / epsilon)^{1/4}
   - Below eta: viscous dissipation dominates
   - Above eta: inertial cascade dominates
   - At eta: 0/0 removable singularity

4. REYNOLDS NUMBER:
   - Re = U*L/nu
   - Below Re_c: laminar flow
   - Above Re_c: turbulent flow
   - At Re_c: 0/0 (transition to turbulence)

5. INTERMITTENCY (Kolmogorov 1962, She-Leveque 1994):
   - K41 assumes Gaussian statistics (no intermittency)
   - Real turbulence has intermittency: rare intense events
   - She-Leveque model: log-Poisson cascade
   - Corrections to -5/3: E(k) ~ k^{-5/3 + mu/3}
   - mu = 2/9 (She-Leveque 1994)

The key insight: turbulence has a 0/0 at the dissipation scale,
with a UNIVERSAL exponent -5/3 that is DIFFERENT from all Ising
universality classes.

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


def kolmogorov_spectrum(k, C_K=1.5, epsilon=1.0):
    """
    Kolmogorov 1941 energy spectrum.

    E(k) = C_K * epsilon^{2/3} * k^{-5/3}

    The -5/3 exponent is UNIVERSAL.
    """
    return C_K * epsilon**(2.0/3.0) * k**(-5.0/3.0)


def dissipation_scale(nu, epsilon):
    """
    Kolmogorov dissipation scale.

    eta = (nu^3 / epsilon)^{1/4}

    Below eta: viscous dissipation dominates
    Above eta: inertial cascade dominates
    At eta: 0/0 removable singularity
    """
    return (nu**3 / epsilon)**0.25


def taylor_microscale(U, L, Re):
    """
    Taylor microscale: lambda = sqrt(15 * nu * U^2 / epsilon)

    For isotropic turbulence: epsilon = U^3 / L
    lambda = L * sqrt(15 / Re)
    """
    return L * math.sqrt(15.0 / Re)


def integral_scale(L, Re):
    """
    Integral (energy-containing) scale.
    ~ L (the largest eddy size)
    """
    return L


def reynolds_number(U, L, nu):
    """Reynolds number: Re = U*L/nu"""
    return U * L / nu


def energy_flux(k, E_k):
    """
    Energy flux through wavenumber k.

    Pi(k) = integral from k to infinity of 2*E(p)/p dp

    In the inertial range: Pi(k) = epsilon (constant)
    At dissipation scale: Pi(k) -> 0 (0/0 removable singularity)
    """
    # Simplified: Pi(k) ~ k * E(k) ~ epsilon in inertial range
    return k * E_k


def richardson_cascade(n_scales, L_max, eta):
    """
    Richardson cascade: energy transfer across scales.

    Each scale: L_i = L_max * (eta/L_max)^{i/n_scales}
    Energy transfer rate: epsilon_i = epsilon (constant in inertial range)
    """
    scales = []
    for i in range(n_scales):
        ratio = i / n_scales
        L_i = L_max * (eta / L_max)**ratio
        scales.append(L_i)
    return scales


def intermittency_correction(k, C_K=1.5, epsilon=1.0, mu=2.0/9.0):
    """
    She-Leveque (1994) intermittency correction.

    E(k) = C_K * epsilon^{2/3} * k^{-5/3 + mu/3}

    mu = 2/9 (She-Leveque 1994)
    Without intermittency: mu = 0 (K41)
    """
    return C_K * epsilon**(2.0/3.0) * k**(-5.0/3.0 + mu/3.0)


def velocity_increment_pdf(r, epsilon, nu, n_samples=10000):
    """
    Velocity increment distribution.

    K41: Gaussian (no intermittency)
    Real: stretched exponential (intermittency)
    """
    # K41 prediction: Gaussian with sigma ~ (epsilon * r)^{1/3}
    sigma = (epsilon * r)**(1.0/3.0)
    return sigma


def structure_function_p(p, r, epsilon=1.0):
    """
    p-th order structure function.

    K41: S_p(r) = C_p * (epsilon * r)^{p/3}
    Intermittency: S_p(r) = C_p * (epsilon * r)^{zeta_p}
    zeta_p = p/3 - mu*p*(p-3)/18 (She-Leveque)
    """
    mu = 2.0 / 9.0
    zeta_p = p / 3.0 - mu * p * (p - 3) / 18.0
    return r**zeta_p


def kolmogorov_62_correction(r, r_0=1.0):
    """
    Kolmogorov (1962) refined similarity hypothesis.

    S_3(r) = C_3 * epsilon_r * r
    where epsilon_r is the local averaged dissipation.
    """
    # Log-normal model: epsilon_r ~ exp(mu*xi - mu^2*sigma^2/2)
    mu_k62 = 1.0 / 3.0
    return r**(1.0 + mu_k62)


def reynolds_transition(Re_values):
    """
    Laminar-turbulent transition.

    Re < Re_c: laminar (order parameter = 0)
    Re > Re_c: turbulent (order parameter > 0)
    At Re_c: 0/0 removable singularity
    """
    results = []
    for Re in Re_values:
        if Re < 2000:
            state = "LAMINAR"
            intensity = 0.0
        elif Re < 4000:
            state = "TRANSITIONAL"
            intensity = (Re - 2000) / 2000
        else:
            state = "TURBULENT"
            intensity = 1.0
        results.append((state, intensity))
    return results


def main():
    print("=" * 70)
    print("TURBULENCE & THE KOLMOGOROV SPECTRUM: 0/0 AT DISSIPATION SCALE")
    print("=" * 70)
    print()

    # 1. Kolmogorov Energy Spectrum
    print("1. KOLMOGOROV ENERGY SPECTRUM (K41, 1941)")
    print("-" * 70)
    print()
    print("   E(k) = C_K * epsilon^{2/3} * k^{-5/3}")
    print("   C_K = 1.5 (Kolmogorov constant)")
    print("   epsilon = energy dissipation rate")
    print()
    print("   The -5/3 exponent is UNIVERSAL across all turbulent flows!")
    print()
    print("   k (1/m)    E(k)          State")
    print("   " + "-" * 55)
    for k_exp in [-2, -1, 0, 1, 2, 3, 4]:
        k = 10.0**k_exp
        E = kolmogorov_spectrum(k)
        if k < 0.1:
            state = "ENERGY-CONTAINING"
        elif k < 100:
            state = "INERTIAL RANGE"
        else:
            state = "DISSIPATION"
        print("   10^%-2d     %.6e    %s" % (k_exp, E, state))

    print()
    print("   In inertial range: E(k) ~ k^{-5/3} (UNIVERSAL)")
    print("   At dissipation scale: spectrum = 0/0 (removable singularity)")

    # 2. Dissipation Scale
    print()
    print("2. DISSIPATION SCALE")
    print("-" * 70)
    print()
    print("   eta = (nu^3 / epsilon)^{1/4}")
    print("   Below eta: viscous dissipation dominates")
    print("   Above eta: inertial cascade dominates")
    print()
    print("   Flow            U(m/s)  L(m)    nu(m^2/s)   Re        eta(m)")
    print("   " + "-" * 70)
    flows = [
        ("Coffee cup", 0.01, 0.1, 1e-6),
        ("River", 1.0, 10.0, 1e-6),
        ("Atmosphere", 10.0, 1000.0, 1.5e-5),
        ("Jet engine", 300.0, 1.0, 1.5e-5),
        ("Supersonic", 1000.0, 0.1, 1.5e-5),
    ]
    for name, U, L, nu in flows:
        Re = reynolds_number(U, L, nu)
        epsilon = U**3 / L
        eta = dissipation_scale(nu, epsilon)
        print("   %-15s %.1f  %.1f   %.1e   %.1e   %.1e" % (
            name, U, L, nu, Re, eta))

    # 3. Richardson Cascade
    print()
    print("3. RICHARDSON CASCADE (1922)")
    print("-" * 70)
    print()
    print('   "Big whorls have little whorls')
    print('    Which feed on their velocity,')
    print('    And little whorls have lesser whorls')
    print('    And so on to viscosity."')
    print()
    print("   Energy cascades from large to small scales.")
    print("   Self-similar 0/0 at each scale (fractal structure).")
    print()
    L_max = 10.0
    eta = 0.001
    scales = richardson_cascade(8, L_max, eta)
    print("   Scale    L(m)        Energy flux")
    print("   " + "-" * 45)
    for i, L_i in enumerate(scales):
        print("   %d        %.4f     epsilon (constant)" % (i, L_i))

    # 4. Reynolds Number Transition
    print()
    print("4. REYNOLDS NUMBER TRANSITION")
    print("-" * 70)
    print()
    print("   Re = U*L/nu")
    print("   Re < 2000: laminar")
    print("   Re > 4000: turbulent")
    print("   Re ~ 2000-4000: transitional (0/0)")
    print()
    Re_values = [100, 500, 1000, 2000, 3000, 4000, 5000, 10000, 100000]
    print("   Re       State          Intensity")
    print("   " + "-" * 45)
    for Re in Re_values:
        state, intensity = reynolds_transition([Re])[0]
        print("   %-8d %-14s %.2f" % (Re, state, intensity))

    # 5. Intermittency
    print()
    print("5. INTERMITTENCY & SHE-LEVEQUE (1994)")
    print("-" * 70)
    print()
    print("   K41 assumes Gaussian statistics (no intermittency).")
    print("   Real turbulence has rare intense events (intermittency).")
    print()
    print("   She-Leveque: zeta_p = p/3 - mu*p*(p-3)/18")
    print("   mu = 2/9 (intermittency parameter)")
    print()
    print("   p/zeta_p(K41)  zeta_p(SL)   Difference")
    print("   " + "-" * 50)
    mu = 2.0 / 9.0
    for p in [1, 2, 3, 4, 5, 6, 7, 8]:
        zeta_k41 = p / 3.0
        zeta_sl = p / 3.0 - mu * p * (p - 3) / 18.0
        diff = zeta_sl - zeta_k41
        print("   %d/%.4f        %.4f      %+.4f" % (p, zeta_k41, zeta_sl, diff))

    # 6. Structure Functions
    print()
    print("6. STRUCTURE FUNCTIONS")
    print("-" * 70)
    print()
    print("   S_p(r) = <|u(x+r) - u(x)|^p>")
    print("   K41: S_p ~ r^{p/3}")
    print("   Intermittency: S_p ~ r^{zeta_p}")
    print()
    print("   r (m)     S_2(r)       S_3(r)       S_4(r)")
    print("   " + "-" * 55)
    for r_exp in [-3, -2, -1, 0, 1]:
        r = 10.0**r_exp
        S2 = structure_function_p(2, r)
        S3 = structure_function_p(3, r)
        S4 = structure_function_p(4, r)
        print("   10^%-2d     %.6e    %.6e    %.6e" % (r_exp, S2, S3, S4))

    # 7. Connections
    print()
    print("=" * 70)
    print("CONNECTIONS TO OTHER 0/0 SINGULARITIES")
    print("=" * 70)
    print()
    print("   TURBULENCE vs ISING: TWO GREAT UNIVERSALITIES")
    print()
    print("   System               Exponent     Source")
    print("   " + "-" * 60)
    print("   K41 energy spectrum  -5/3 = -1.667  Kolmogorov 1941")
    print("   Ising 2D             1/8 = 0.125   Onsager 1944")
    print("   Ising 3D             0.326         Monte Carlo")
    print("   Ising MF             1/2 = 0.500   Bragg-Williams")
    print("   ER percolation 2D    1/3 = 0.333   Erdos-Renyi")
    print()
    print("   K41 -5/3 is a COMPLETELY DIFFERENT universality class!")
    print("   It is NOT an Ising class.")
    print()
    print("   The -5/3 exponent appears in:")
    print("   - Atmospheric turbulence")
    print("   - Ocean currents")
    print("   - Stellar interiors")
    print("   - Galaxy formation")
    print("   - Quantum chromodynamics (gluon cascade)")
    print()
    print("   ALL turbulent flows share the SAME -5/3 spectrum!")
    print("   This is the UNIVERSAL 0/0 of turbulence.")

    # 8. Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("   Turbulence has a 0/0 removable singularity:")
    print()
    print("   1. KOLMOGOROV SPECTRUM:")
    print("      E(k) = C_K * epsilon^{2/3} * k^{-5/3}")
    print("      -5/3 is UNIVERSAL (differs from Ising)")
    print()
    print("   2. DISSIPATION SCALE:")
    print("      eta = (nu^3/epsilon)^{1/4}")
    print("      0/0 at eta (inertial meets viscous)")
    print()
    print("   3. RICHARDSON CASCADE:")
    print("      Self-similar 0/0 at each scale")
    print("      Fractal structure, energy conservation")
    print()
    print("   4. REYNOLDS TRANSITION:")
    print("      Re_c ~ 2000-4000 (0/0 removable)")
    print()
    print("   5. INTERMITTENCY:")
    print("      She-Leveque: mu = 2/9")
    print("      Corrections to K41 (log-Poisson cascade)")
    print()
    print("   K41 -5/3 is a DIFFERENT universality class from Ising!")
    print("   The 0/0 framework has MULTIPLE fundamental exponents.")

    # Save
    results = {
        'kolmogorov': {
            'formula': 'E(k) = C_K * epsilon^{2/3} * k^{-5/3}',
            'C_K': 1.5,
            'exponent': -5.0/3.0,
            'universality': 'All turbulent flows',
        },
        'dissipation_scale': {
            'formula': 'eta = (nu^3/epsilon)^{1/4}',
        },
        'richardson_cascade': {
            'self_similar': True,
            'fractal': True,
            'energy_conservation': True,
        },
        'reynolds_transition': {
            'Re_c': [2000, 4000],
            '0_0_structure': True,
        },
        'intermittency': {
            'she_leveque': {
                'mu': 2.0/9.0,
                'formula': 'zeta_p = p/3 - mu*p*(p-3)/18',
            },
            'kolmogorov_62': {
                'log_normal': True,
            },
        },
        'connections': {
            'different_from_ising': True,
            'exponent': '-5/3',
            'appears_in': ['Atmosphere', 'Ocean', 'Stars', 'Galaxies', 'QCD'],
        },
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    output_path = os.path.join(OUTPUT_DIR, 'kolmogorov_turbulence.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print()
    print("   Results saved to: %s" % output_path)


if __name__ == '__main__':
    main()
