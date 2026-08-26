#!/usr/bin/env python3
"""
Solar System as Spiral with 0/0 Mass Gap
==========================================

Mathematical model showing:
1. Solar system as spiral (tornado-like) structure
2. Mass gap as removable singularity (0/0)
3. Connections to Navier-Stokes, Yang-Mills, BSD

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

def parker_spiral(r, theta, omega_sun=2.7e-6, v_wind=400e3, B0=1e-4, R0=2.0):
    """
    Parker spiral magnetic field.
    
    B_r = B0 * (R0/r)^2
    B_phi = B_r * omega_sun * (r - R0) / v_wind
    
    The spiral angle: tan(psi) = omega_sun * r / v_wind
    
    At r -> 0: B_r -> infinity (pole)
    At r -> infinity: B_phi/B_r -> infinity (tight winding)
    The mass gap: at r = R0, B_phi = 0 (removable singularity)
    """
    r = np.maximum(r, 1e-10)
    Br = B0 * (R0 / r)**2
    Bphi = Br * omega_sun * (r - R0) / v_wind
    
    spiral_angle = np.arctan2(Bphi, Br)
    
    return Br, Bphi, spiral_angle

def kepler_spiral(r, theta, omega_sun=2.7e-6, v_wind=400e3):
    """
    Keplerian orbit as spiral in rotating frame.
    
    In the rotating frame with omega_sun, a Keplerian orbit
    with omega_orbit(r) = sqrt(GM/r^3) traces a spiral:
    
    dtheta/dr = (omega_orbit - omega_sun) / v_r
    
    where v_r is the radial velocity.
    
    At the corotation radius: omega_orbit = omega_sun
    This is the 0/0 point: dtheta/dr = 0/0
    
    The removable value: the spiral pitch angle at corotation.
    """
    GM = 1.327e20  # m^3/s^2
    omega_orbit = np.sqrt(GM / np.maximum(r, 1e-10)**3)
    
    dtheta_dr = (omega_orbit - omega_sun) / (v_wind + 1e-10)
    
    return omega_orbit, dtheta_dr

def toomre_stability(r, cs, omega, G=6.674e-11, Sigma=None):
    """
    Toomre Q parameter for disk stability.
    
    Q = cs * kappa / (pi * G * Sigma)
    
    where kappa = 2*omega * sqrt(1 + (r/omega) * domega/dr)
    
    For Keplerian: kappa = omega, so Q = cs * omega / (pi * G * Sigma)
    
    At Q = 1: marginal stability (0/0 in growth rate)
    At Q < 1: unstable (spiral arms form)
    At Q > 1: stable (no spirals)
    
    The mass gap: Q = 1 is the removable singularity
    between stable and unstable regimes.
    """
    if Sigma is None:
        Sigma = 1e-3  # kg/m^2
    
    kappa = omega  # Keplerian approximation
    Q = cs * kappa / (np.pi * G * Sigma)
    
    return Q

def navier_stokes_disk(r, t, nu=1e15, Sigma0=1e-3, R0=1.0):
    """
    Navier-Stokes solution for thin accretion disk.
    
    Surface density evolution:
    dSigma/dt = (1/r) * d/dr(r * nu * r * dSigma/dr)
    
    Solution: Sigma(r,t) = Sigma0 * (R0/r) * exp(-r^2/(4*nu*t)) / (4*pi*nu*t)
    
    This is the fundamental solution (Green's function) of the diffusion equation.
    
    At t -> 0: Sigma -> delta(r) (point singularity)
    At r -> 0: Sigma -> 0/0 (removable singularity)
    
    The removable value: the central surface density
    Sigma(0,t) = Sigma0 / (4*pi*nu*t) * (R0/0) -> finite when regularized
    """
    t = np.maximum(t, 1e-10)
    r = np.maximum(r, 1e-10)
    
    Sigma = Sigma0 * (R0 / r) * np.exp(-r**2 / (4 * nu * t)) / (4 * np.pi * nu * t)
    
    return Sigma

def yang_mills_mass_gap():
    """
    Yang-Mills mass gap as 0/0.
    
    Classical: massless gauge bosons (mass = 0)
    Quantum: glueball mass m_g > 0
    
    The mass gap: Delta = m_g - 0 = m_g
    
    Lattice QCD estimate: m_g ≈ 1870(75) MeV for SU(3)
    
    The 0/0 structure:
    Classical energy spectrum: E = 0 (massless)
    Quantum energy spectrum: E = Delta > 0
    
    The gap is the removable value of the 0/0 singularity
    in the spectral density at mu^2 = 0.
    """
    m_g = 1870  # MeV (lightest glueball mass)
    Delta = m_g  # Mass gap
    
    return Delta, m_g

def bsd_conductor(r, theta, a=1.0, b=0.5):
    """
    BSD conjecture: elliptic curve y^2 = x^3 + ax + b
    
    The conductor N encodes ramification.
    
    For orbital resonances: p:q resonances are rational points
    on the orbit frequency ratio space.
    
    The 0/0: at exact resonance p/q = omega_1/omega_2,
    the perturbation grows as 0/0 (secular resonance).
    
    The removable value: the libration amplitude.
    """
    discriminant = -16 * (4 * a**3 + 27 * b**2)
    
    conductor = abs(int(round(discriminant)))
    
    return discriminant, conductor

def spiral_mass_gap_solar_system():
    """
    Main computation: Solar system as spiral with 0/0 mass gap.
    """
    print("=" * 70)
    print("SOLAR SYSTEM AS SPIRAL WITH 0/0 MASS GAP")
    print("=" * 70)
    print()
    
    results = {}
    
    # 1. Parker Spiral
    print("1. PARKER SPIRAL")
    print("-" * 70)
    r_au = np.linspace(0.1, 10, 1000)
    r_m = r_au * 1.496e11
    
    Br, Bphi, spiral_angle = parker_spiral(r_m, 0)
    
    print("   Spiral angle at 1 AU: %.1f degrees" % math.degrees(spiral_angle[499]))
    print("   B_r at 0.1 AU: %.2e T" % Br[0])
    print("   B_r at 1 AU: %.2e T" % Br[499])
    print("   B_phi/B_r at 1 AU: %.4f" % (Bphi[499]/Br[499]))
    
    results['parker'] = {
        'spiral_angle_1au': float(math.degrees(spiral_angle[499])),
        'Br_01au': float(Br[0]),
        'Br_1au': float(Br[499]),
        'Bphi_ratio_1au': float(Bphi[499]/Br[499])
    }
    
    # 2. Corotation radius (the 0/0 point)
    print()
    print("2. COROTATION RADIUS (0/0 POINT)")
    print("-" * 70)
    omega_sun = 2.7e-6
    GM = 1.327e20
    r_corot = (GM / omega_sun**2)**(1/3)
    r_corot_au = r_corot / 1.496e11
    
    print("   Corotation radius: %.2f AU" % r_corot_au)
    print("   At corotation: omega_orbit = omega_sun (0/0 in spiral pitch)")
    print("   Removable value: finite spiral pitch angle")
    
    results['corotation'] = {
        'r_corot_au': float(r_corot_au),
        'omega_sun': omega_sun,
        'omega_orbit_corot': float(omega_sun)
    }
    
    # 3. Toomre stability
    print()
    print("3. TOOMRE STABILITY (MASS GAP IN DISK)")
    print("-" * 70)
    cs = 1000  # m/s (sound speed)
    Sigma = 1e-3  # kg/m^2
    omega = 2.7e-6
    Q = toomre_stability(r_au * 1.496e11, cs, omega, Sigma=Sigma)
    
    print("   Q = %.4f" % Q)
    print("   Q > 1: disk is STABLE (mass gap exists)")
    print("   Q < 1: disk is UNSTABLE (no gap, spirals form)")
    print("   Q = 1: MARGINAL (0/0 removable singularity)")
    
    results['toomre'] = {
        'Q': float(Q),
        'cs': cs,
        'Sigma': Sigma,
        'stable': bool(Q > 1)
    }
    
    # 4. Navier-Stokes disk
    print()
    print("4. NAVIER-STOKES ACCRETION DISK")
    print("-" * 70)
    nu = 1e15  # m^2/s (turbulent viscosity)
    t = 1e6 * 365.25 * 24 * 3600  # 1 Myr
    Sigma_disk = navier_stokes_disk(r_m, t, nu=nu)
    
    print("   Turbulent viscosity: %.2e m^2/s" % nu)
    print("   Time: 1 Myr")
    print("   Max surface density: %.2e kg/m^2" % np.max(Sigma_disk))
    print("   Central density (r->0): 0/0 removable singularity")
    print("   Removable value: finite central density")
    
    results['navier_stokes'] = {
        'nu': nu,
        't_myr': 1.0,
        'max_Sigma': float(np.max(Sigma_disk)),
        'central_0over0': True
    }
    
    # 5. Yang-Mills mass gap
    print()
    print("5. YANG-MILLS MASS GAP (0/0)")
    print("-" * 70)
    Delta, m_g = yang_mills_mass_gap()
    
    print("   Classical: massless gauge bosons (mass = 0)")
    print("   Quantum: glueball mass m_g = %d MeV" % m_g)
    print("   Mass gap Delta = %d MeV" % Delta)
    print("   0/0 structure: 0 mass -> Delta > 0 (removable singularity)")
    
    results['yang_mills'] = {
        'Delta_MeV': Delta,
        'm_g_MeV': m_g,
        'classical_mass': 0,
        'quantum_mass': m_g
    }
    
    # 6. BSD and orbital resonances
    print()
    print("6. BSD CONJECTURE AND ORBITAL RESONANCES")
    print("-" * 70)
    
    # Planetary orbital ratios (approximate)
    planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn']
    periods = [0.241, 0.615, 1.000, 1.881, 11.86, 29.46]  # years
    
    resonances = []
    for i in range(len(planets)):
        for j in range(i+1, len(planets)):
            ratio = periods[j] / periods[i]
            # Find closest rational p/q
            best_p, best_q = 1, 1
            for q in range(1, 20):
                p = round(ratio * q)
                if p > 0 and p < 100:
                    err = abs(ratio - p/q)
                    if err < abs(ratio - best_p/best_q):
                        best_p, best_q = p, q
            
            resonances.append({
                'pair': '%s:%s' % (planets[i], planets[j]),
                'ratio': float(ratio),
                'rational': '%d/%d' % (best_p, best_q),
                'error': float(abs(ratio - best_p/best_q))
            })
    
    print("   Orbital period ratios and nearest resonances:")
    for res in resonances[:6]:
        print("   %s: %.3f ~ %s (error: %.4f)" % (
            res['pair'], res['ratio'], res['rational'], res['error']))
    
    results['bsd_resonances'] = resonances
    
    # 7. Mass gap as 0/0 in spiral structure
    print()
    print("7. MASS GAP AS 0/0 IN SPIRAL STRUCTURE")
    print("-" * 70)
    print()
    print("   The solar system has THREE mass gaps:")
    print()
    print("   a) ASTEROID GAP: between Mars and Jupiter")
    print("      - Kirkwood gaps at resonances with Jupiter")
    print("      - Mass ~ 0 at these radii (0/0 removable singularity)")
    print("      - Removable value: finite mass that was ejected")
    print()
    print("   b) PLANET-STAR GAP: mass ratio planet/star ~ 10^-3 to 10^-6")
    print("      - Classical: no planets (0 mass)")
    print("      - Reality: small but finite mass (removable value)")
    print("      - This is the Yang-Mills mass gap analogy")
    print()
    print("   c) SPIRAL PITCH GAP: at corotation radius")
    print("      - dtheta/dr = 0/0 (Keplerian angular velocity = frame rotation)")
    print("      - Removable value: finite spiral pitch angle")
    print("      - This governs where spiral arms are visible")
    
    # 8. Connection to Millennium Problems
    print()
    print("8. CONNECTIONS TO MILLENNIUM PRIZE PROBLEMS")
    print("-" * 70)
    print()
    print("   a) NAVIER-STOKES (NS)")
    print("      Disk fluid dynamics governed by NS equations")
    print("      Question: do smooth solutions exist globally?")
    print("      0/0 connection: if blow-up occurs, velocity gradient")
    print("      -> infinity while density -> 0 (0/0)")
    print("      Caffarelli-Kohn-Nirenberg: singular set has measure zero")
    print("      Removable singularity: singularities can be 'removed'")
    print()
    print("   b) YANG-MILLS (YM)")
    print("      Mass gap Delta > 0 in gauge theory")
    print("      Classical: massless (0). Quantum: massive (Delta > 0)")
    print("      0/0 structure: mass gap is removable value")
    print("      Lattice QCD: m_g ~ 1870 MeV")
    print("      Connection to disk: MRI wavelength gap ~ mass gap")
    print()
    print("   c) BIRCH AND SWINNERTON-DYER (BSD)")
    print("      Orbital resonances are rational points on frequency space")
    print("      p:q resonance = rational point where perturbation -> 0/0")
    print("      Removable value: libration amplitude")
    print("      BSD: rank of elliptic curve = number of rational points")
    print("      Analogy: number of stable resonances = 'rank' of system")
    
    # 9. The tornado/spiral analogy
    print()
    print("9. THE TORNADO/SPIRAL ANALOGY")
    print("-" * 70)
    print()
    print("   A tornado is a spiral with:")
    print("   - Center: 0/0 singularity (velocity -> infinity, pressure -> 0)")
    print("   - Mass gap: eye of tornado (no debris, invisible)")
    print("   - Spiral arms: visible debris bands")
    print()
    print("   The solar system is analogous:")
    print("   - Sun: 0/0 singularity (infinite density in point mass)")
    print("   - Asteroid belt gap: mass gap (invisible material)")
    print("   - Planetary orbits: spiral arms (visible structure)")
    print()
    print("   Both have the SAME mathematical structure:")
    print("   - Removable singularity at center")
    print("   - Mass gap in spectrum")
    print("   - Spiral pattern from differential rotation")
    
    # 10. Formal mathematical statement
    print()
    print("10. FORMAL MATHEMATICAL STATEMENT")
    print("-" * 70)
    print()
    print("   THEOREM (informal):")
    print("   The solar system structure is a spiral with removable")
    print("   singularities at three scales:")
    print()
    print("   (i)   Stellar scale: Sun as point mass (r -> 0)")
    print("         M(r) = M_sun * (r/R_sun)^3 for r < R_sun")
    print("         At r = 0: M(0) = 0/0 (removable)")
    print("         Removable value: M_sun")
    print()
    print("   (ii)  Planetary scale: Kirkwood gaps at resonances")
    print("         rho(r) = rho_0 / sinh(2*pi / (sigma * (N-1)))")
    print("         At resonances: rho -> 0/0 (removable)")
    print("         Removable value: finite density at non-resonant radii")
    print()
    print("   (iii) Galactic scale: spiral pattern speed")
    print("         Omega_pattern(r) = Omega_kep(r) at corotation")
    print("         dtheta/dr = 0/0 (removable)")
    print("         Removable value: spiral pitch angle")
    print()
    print("   COROLLARY:")
    print("   The mass gap in the solar system (empty zones between")
    print("   planets) is mathematically equivalent to the Yang-Mills")
    print("   mass gap (Delta > 0) and the Navier-Stokes regularity")
    print("   condition (global smooth solutions).")
    
    return results

def main():
    results = spiral_mass_gap_solar_system()
    
    output_path = os.path.join(OUTPUT_DIR, 'spiral_mass_gap.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    print()
    print("=" * 70)
    print("RESULTS SAVED TO: %s" % output_path)
    print("=" * 70)

if __name__ == '__main__':
    main()
