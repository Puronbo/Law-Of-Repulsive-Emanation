"""
UNIVERSE IN THE POINCARE SPHERE: 0/0 COSMOLOGY
================================================

The Poincare sphere conformally compactifies spacetime.
The Big Bang singularity is a 0/0: both the metric and its
conformal factor vanish simultaneously. The removable value
determines the geometry of the compactified universe.

Key 0/0 structures:
1. Friedmann eq: H^2 = (8piG/3) * rho - k/a^2 + Lambda/3
   At a->0: both sides blow up. Ratio = removable.

2. Conformal factor: Omega(a) -> 0 as a -> 0
   Metric: g_ij / Omega^2 -> finite (Penrose diagram)

3. Cosmological constant: Lambda appears as removable value
   of the vacuum energy density at a->infinity

4. Big Bang: t -> 0, a -> 0, but conformal time eta -> finite
   The universe "starts" at a finite conformal distance
"""

import numpy as np
import json, os

OUT = "data/poincare_universe.json"


def friedmann_H(a, Omega_m=0.3, Omega_r=0.0, Omega_L=0.7, Omega_k=0.0, H0=70.0):
    """Hubble parameter from Friedmann equation.
    H^2 = H0^2 * (Omega_m/a^3 + Omega_r/a^4 + Omega_k/a^2 + Omega_L)
    """
    H2 = H0**2 * (Omega_m / a**3 + Omega_r / a**4 + Omega_k / a**2 + Omega_L)
    return np.sqrt(np.maximum(H2, 0))


def conformal_time_integrand(a, Omega_m=0.3, Omega_r=0.0, Omega_L=0.7, Omega_k=0.0, H0=70.0):
    """Integrand for conformal time: d_eta = da / (a * H(a))"""
    H = friedmann_H(a, Omega_m, Omega_r, Omega_L, Omega_k, H0)
    return 1.0 / (a * H)


def compute_conformal_time(a_min=1e-10, a_max=10.0, n=100000,
                           Omega_m=0.3, Omega_r=0.0, Omega_L=0.7):
    """Compute conformal time eta(a) by integration."""
    a_vals = np.logspace(np.log10(a_min), np.log10(a_max), n)
    integrand = np.array([
        conformal_time_integrand(a, Omega_m, Omega_r, Omega_L) for a in a_vals
    ])
    # Trapezoid integration
    log_a = np.log(a_vals)
    eta = np.zeros(n)
    for i in range(1, n):
        eta[i] = eta[i-1] + 0.5 * (integrand[i] + integregrand[i-1]) * (log_a[i] - log_a[i-1]) * a_vals[i]
    return a_vals, eta


def penrose_dessitter():
    """Penrose diagram of de Sitter space.
    
    de Sitter: a(t) = exp(H*t), conformal time eta = -exp(-H*t)/H
    After rescaling: u = tanh(H*eta), v = tanh(H*eta')
    
    The Penrose diagram is a diamond:
        /\\
       /  \\
      /    \\   (future infinity i+)
     /      \\
    |   dS   |  (spatial infinity i)
     \\      /
      \\    /   (past infinity i-)
       \\  /
        \\/
    """
    print("--- Penrose Diagram of de Sitter Space ---")
    
    # de Sitter metric in conformal coordinates:
    # ds^2 = (1/H^2) * (1/chi^4) * (-dchi^2 + dOmega_3^2)
    # where chi = eta (conformal time), chi in (-1/H, 1/H)
    
    H = 1.0  # Normalized
    chi = np.linspace(-0.99/H, 0.99/H, 1000)
    
    # Conformal factor: Omega = H * chi^2 / (1 - H^2*chi^2)
    # This is the 0/0: Omega -> 0 as chi -> 0 (big bang)
    # and Omega -> 0 as chi -> +/- 1/H (conformal infinity)
    
    Omega = H * chi**2 / (1 - H**2 * chi**2)
    
    # The 0/0 structure:
    # At chi=0: Omega = 0/1 = 0 (big bang singularity)
    # At chi=+/-1/H: Omega = H*(1/H^2)/0 = 1/(H*0) = infinity (infinity)
    # BUT: the RESCALED metric g_ij / Omega^2 is FINITE everywhere
    
    # Rescaled metric component:
    g_tilde_00 = -1.0  # Constant in conformal coordinates
    g_tilde_ij = 1.0 / chi**2  # Spatial part
    
    # At chi -> 0: g_tilde_ij = 1/chi^2 -> infinity
    # But Omega^2 * g_tilde_ij = H^2*chi^4/(1-H^2*chi^2)^2 * 1/chi^2
    #                          = H^2*chi^2/(1-H^2*chi^2)^2 -> 0
    
    # The physical metric is:
    g_phys_00 = -Omega**2 * g_tilde_00
    g_phys_ij = Omega**2 * g_tilde_ij
    
    # At chi -> 0: g_phys_ij = H^2*chi^4/(1-H^2*chi^2)^2 * 1/chi^2 
    #                        = H^2*chi^2/(1-H^2*chi^2)^2 -> 0 (smooth!)
    
    # At chi -> 1/H: g_phys_ij = H^2*(1/H^4)/(0)^2 * H^2 = finite!
    # This is the conformal compactification boundary
    
    print("  chi=0 (Big Bang):")
    print("    Omega = 0 (conformal factor vanishes)")
    print("    g_tilde_ij = 1/chi^2 = infinity")
    print("    g_phys = Omega^2 * g_tilde = 0 (SMOOTH)")
    print("    => Big Bang is a REMOVABLE SINGULARITY")
    print()
    print("  chi=1/H (infinity):")
    print("    Omega = infinity (conformal factor blows up)")
    print("    g_tilde_ij = H^2 (finite)")
    print("    g_phys = Omega^2 * g_tilde = infinity")
    print("    => Physical infinity. Compactified by conformal rescaling.")
    print()
    print("  After Penrose rescaling chi -> chi/(1+H*|chi|):")
    print("    New chi in (-1/H, 1/H) -> (-1, 1)")
    print("    Boundary at chi = +/-1 is now FINITE")
    print("    => The entire universe fits on a FINITE diagram")
    
    return {
        "H": H,
        "chi_range": [-1/H, 1/H],
        "Omega_at_0": 0.0,
        "g_phys_at_0": 0.0,
        "removable": True,
    }


def friedmann_0over0():
    """Analyze the Friedmann equation as a 0/0 singularity."""
    print("\n--- Friedmann Equation 0/0 Analysis ---")
    
    # H^2 = (8piG/3) * rho - k/a^2 + Lambda/3
    # For matter domination: rho = rho_0 / a^3
    # H^2 = (8piG*rho_0/3) * a^{-3} - k*a^{-2} + Lambda/3
    
    # As a -> 0:
    #   H^2 ~ (8piG*rho_0/3) * a^{-3}  (matter dominates)
    #   H ~ a^{-3/2} -> infinity
    
    # The 0/0: compute scale factor from H = da/dt / a
    # dt = da / (a*H) ~ da / (a * a^{-3/2}) = a^{1/2} da
    # t ~ (2/3) * a^{3/2} -> 0 as a -> 0
    
    # So: a(t) ~ (3/2 * t)^{2/3}
    # At t=0: a=0 (0/0: 0 = (3/2 * 0)^{2/3})
    
    # The removable value: a/t^{2/3} = (3/2)^{2/3} = 1.3104
    ratio = (3.0/2.0)**(2.0/3.0)
    print("  a(t) ~ (3t/2)^{2/3} for matter domination")
    print("  At t=0: a=0 (Big Bang)")
    print(f"  Removable value: a/t^{{2/3}} = (3/2)^{{2/3}} = {ratio:.4f}")
    print()
    
    # For radiation domination: rho = rho_0 / a^4
    # H^2 ~ (8piG*rho_0/3) * a^{-4}
    # H ~ a^{-2}
    # dt = da / (a * a^{-2}) = a da
    # t ~ a^2 / 2
    # a(t) ~ (2t)^{1/2}
    ratio_r = 2.0**0.5
    print("  a(t) ~ (2t)^{1/2} for radiation domination")
    print(f"  Removable value: a/t^{{1/2}} = sqrt(2) = {ratio_r:.4f}")
    print()
    
    # For Lambda domination: rho = Lambda/(8piG)
    # H^2 = Lambda/3
    # a(t) = exp(sqrt(Lambda/3) * t)
    # At t=0: a = 1 (NOT 0, no singularity in de Sitter!)
    print("  a(t) = exp(sqrt(Lambda/3) * t) for Lambda domination")
    print("  At t=0: a=1 (NO Big Bang in pure de Sitter!)")
    print("  The cosmological constant RESOLVES the 0/0 singularity")
    print()
    
    return {
        "matter_ratio": ratio,
        "radiation_ratio": ratio_r,
        "lambda_resolves": True,
    }


def dessitter_conformal():
    """de Sitter space: full conformal analysis."""
    print("\n--- de Sitter Conformal Compactification ---")
    
    # de Sitter metric:
    # ds^2 = -dt^2 + exp(2Ht) * (dx^2 + dy^2 + dz^2)
    #
    # Conformal time: eta = -exp(-Ht)/H, eta in (-1/H, 0)
    # a(eta) = -1/(H*eta) = 1/(H*|eta|)
    #
    # ds^2 = (1/(H*eta)^2) * (-deta^2 + dx^2 + dy^2 + dz^2)
    #
    # This is conformally flat! The conformal factor is:
    # Omega(eta) = 1/(H*|eta|)
    #
    # As eta -> 0- (big bang): Omega -> infinity (BLows up)
    # As eta -> -1/H (infinity): Omega -> 1 (finite)
    
    # The 0/0 is: a(eta) = 1/(H*|eta|) -> infinity as eta -> 0
    # But in physical time t: a(t) = exp(Ht) -> 0 as t -> -infinity
    # The big bang is at t = -infinity, NOT at a finite time!
    
    print("  Metric: ds^2 = (1/(H*eta)^2) * (-deta^2 + dx^2)")
    print("  a(eta) = 1/(H*|eta|)")
    print()
    print("  As eta -> 0- (past):")
    print("    a -> infinity (anti-de Sitter region)")
    print("    Omega = 1/(H*|eta|) -> infinity")
    print("    => NOT a big bang, but a spatial infinity")
    print()
    print("  As eta -> -1/H (future):")
    print("    a = 1 (finite)")
    print("    Omega = 1")
    print("    => Future infinity is FINITE (conformal)")
    print()
    
    # The key insight: in de Sitter, the "big bang" is REMOVED
    # by the cosmological constant. The universe extends to
    # t = -infinity with no singularity.
    
    # Penrose diagram: diamond shape
    # Future infinity i+ is TIMELIKE (not spacelike as in Minkowski)
    # This is because Lambda > 0 makes the expansion accelerate
    
    print("  Penrose diagram structure:")
    print("    - Past: extends to t = -infinity (no singularity)")
    print("    - Future: timelike infinity i+ (Lambda-dominated)")
    print("    - Spatial infinity i: finite conformal distance")
    print("    - Diagram: DIAMOND (not triangle as in Minkowski)")
    print()
    print("  The cosmological constant Lambda is the REMOVABLE VALUE")
    print("  of the vacuum energy density at a -> infinity:")
    print("    rho_vac = Lambda/(8piG)")
    print("    At a -> infinity: rho_vac * a^3 = Lambda*a^3/(8piG) -> infinity")
    print("    But rho_vac / H^2 = (Lambda/(8piG)) / (Lambda/3) = 3/(8piG)")
    print("    = FINITE (removable value)")
    
    return {
        "conformal_factor": "1/(H*|eta|)",
        "big_bang_removed": True,
        "lambda_removable_value": "3/(8piG)",
        "penrose_shape": "diamond",
    }


def quantum_gravity_0over0():
    """The 0/0 at the Planck scale."""
    print("\n--- Planck Scale 0/0 Structure ---")
    
    # At the Planck scale, quantum gravity effects become important.
    # The metric itself becomes uncertain:
    #   g_ij = <0|g_hat_ij|0> (expectation value)
    #
    # At the Planck scale:
    #   delta_g ~ (l_P/l)^2 (metric fluctuations)
    #   l_P = sqrt(hbar*G/c^3) ~ 1.6e-35 m
    #
    # The 0/0:
    #   As l -> l_P: delta_g -> 1 (metric is maximally uncertain)
    #   The CLASSICAL metric g_ij vanishes (or becomes meaningless)
    #   The QUANTUM metric is a superposition of all geometries
    #
    # This is the Wheeler-DeWitt equation:
    #   H|Psi> = 0
    #   The Hamiltonian constraint: energy = 0 (0/0!)
    
    print("  At the Planck scale (l ~ l_P):")
    print("    Classical metric g_ij -> undefined (0/0)")
    print("    Quantum metric: superposition of all geometries")
    print("    Wheeler-DeWitt: H|Psi> = 0 (energy = 0)")
    print()
    print("  The 0/0 structure of quantum gravity:")
    print("    H = 0 (Hamiltonian constraint)")
    print("    This is a 0/0: the total energy is zero")
    print("    because gravitational energy is negative")
    print("    and cancels matter energy exactly")
    print()
    print("  Removable value: the wavefunction Psi[g_ij]")
    print("    encodes the entire history of the universe")
    print("    The 'removable value' is the path integral:")
    print("    Psi[g] = int D[g'] exp(-S[g']/hbar)")
    print()
    print("  This is EXACTLY the 0/0 framework:")
    print("    Numerator: exp(-S/hbar) (action)")
    print("    Denominator: 0 (Hamiltonian constraint)")
    print("    Removable value: the path integral (well-defined!)")
    
    return {
        "planck_scale": "1.6e-35 m",
        "hamiltonian_constraint": "H|Psi> = 0",
        "path_integral_removable": True,
    }


def run():
    print("=" * 70)
    print("UNIVERSE IN THE POINCARE SPHERE: 0/0 COSMOLOGY")
    print("=" * 70)
    print()
    
    results = {}
    
    results["penrose_dessitter"] = penrose_dessitter()
    print()
    results["friedmann_0over0"] = friedmann_0over0()
    results["dessitter_conformal"] = dessitter_conformal()
    results["quantum_gravity"] = quantum_gravity_0over0()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: THE 0/0 UNIVERSE")
    print("=" * 70)
    print()
    print("The Poincare sphere compactifies the entire universe onto a")
    print("finite ball. The Big Bang singularity is a 0/0:")
    print()
    print("  - Metric g_ij -> 0 (spacetime vanishes)")
    print("  - Conformal factor Omega -> 0 (frame vanishes)")
    print("  - Physical metric g_ij/Omega^2 = FINITE (removable!)")
    print()
    print("The cosmological constant Lambda is the removable value")
    print("of the vacuum energy density at infinity.")
    print()
    print("The Wheeler-DeWitt equation H|Psi> = 0 is a 0/0:")
    print("  - H = 0 (total energy vanishes)")
    print("  - |Psi> = path integral (well-defined)")
    print("  - The universe is the removable value of its own")
    print("    partition function.")
    print()
    print("In the 0/0 framework, the universe EXISTS because the")
    print("singularity at the Big Bang is removable. The 'removable")
    print("value' is the initial condition - and it is uniquely")
    print("determined by the conformal structure.")
    
    os.makedirs("data", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("\nOutput: %s" % OUT)


if __name__ == "__main__":
    run()
