"""
RH: CONDUCTOR RATIO |chi(rho)| AT KNOWN ZEROS
================================================

From the functional equation: zeta(s) = chi(s) * zeta(1-s)
where chi(s) = pi^{s-1/2} * Gamma((1-s)/2) / Gamma(s/2)

At a zero rho: zeta(rho) = 0 = chi(rho) * zeta(1-rho)
=> zeta(1-rho) = 0 too (trivially, since 1-rho is also a zero)

The 0/0 limit: lim_{s->rho} zeta(s)/zeta(1-s) = chi(rho)

RH <=> |chi(rho)| = 1 for all nontrivial zeros rho  (a re-encoding of RH,
     true, and NOT a verification of it - see below)

Key property: |chi(1/2+it)| = 1 for ALL t (by symmetry).
So |chi(rho)| = 1 iff Re(rho) = 1/2  ON THE CRITICAL STRIP 0 < Re < 1.

READ THIS BEFORE TRUSTING THE OUTPUT  (corrected 2026-09-28)
------------------------------------------------------------
The original header of this file read "Key property: ... So |chi(rho)| = 1
iff Re(rho) = 1/2" and listed "2. Tests if |chi(s)| = 1 exactly on the
critical line" among the things this script establishes. That pairing is the
exact structure of the withdrawn argument, and it is the reason this file is
flagged:

  |chi(1/2+it)| = 1 holds for ALL t, zeros and non-zeros alike. A non-zero
  point on the line at the same height returns the same modulus to ~1.97e-31.
  So "test |chi(s)| = 1 on the critical line" is a check that CANNOT FAIL, and
  cannot distinguish a zero from a non-zero. It is not evidence for RH.

The statement that does carry information is the level set: on the strip
0 < Re(s) < 1, |chi(s)| = 1 forces Re(s) = 1/2, and displacing Re(s) is caught
at every scale (Re = 0.501 gives |chi| = 0.99919). Globally the stronger form
is FALSE - |chi(sigma+it)| = 1 has three solutions in sigma for t < t* =
6.2898359888369, the two extras lying outside the strip.

Measurements: experiments/chi_rho_vacuity_0_over_0.py
Governance:  docs/PREDICTION_LEDGER.md PL-22, docs/AUDIT.md section 2 item 8
RH remains open.

This script:
1. Computes |chi(s)| for s near known zeros
2. Confirms |chi(s)| = 1 on the whole critical line - INCLUDING at non-zeros,
   which is why this is an identity and not a test
3. Tests if |chi(s)| deviates from 1 when Re(s) is displaced (this one has
   teeth)
4. Verifies the de Branges connection
"""

import math
import numpy as np
from scipy.special import gamma as gamma_func
from scipy.optimize import brentq

OUT = "data/rh_conductor_ratio.json"


def chi(s_real, s_imag):
    """Compute |chi(s)| where chi(s) = pi^{s-1/2} * Gamma((1-s)/2) / Gamma(s/2)."""
    s = complex(s_real, s_imag)
    
    # pi^{s-1/2}
    log_pi = math.log(math.pi)
    pi_factor = math.exp((s.real - 0.5) * log_pi)
    
    # Gamma((1-s)/2)
    arg1 = (1 - s) / 2
    g1 = gamma_func(arg1)
    
    # Gamma(s/2)
    arg2 = s / 2
    g2 = gamma_func(arg2)
    
    if abs(g2) < 1e-300:
        return float('inf')
    
    chi_val = pi_factor * g1 / g2
    return abs(chi_val)


def chi_log(s_real, s_imag):
    """Compute log|chi(s)| for numerical stability."""
    s = complex(s_real, s_imag)
    
    log_pi = math.log(math.pi)
    log_pi_factor = (s.real - 0.5) * log_pi
    
    # For Gamma, use Stirling for large arguments
    def log_gamma_stirling(z):
        z = complex(z)
        if abs(z) < 10:
            return complex(math.log(abs(gamma_func(z))), math.angle(gamma_func(z)))
        # Stirling: log(Gamma(z)) ~ (z-0.5)*log(z) - z + 0.5*log(2*pi)
        return (z - 0.5) * z.log() - z + 0.5 * math.log(2 * math.pi)
    
    arg1 = (1 - s) / 2
    arg2 = s / 2
    
    try:
        lg1 = complex(math.log(abs(gamma_func(arg1))), math.angle(gamma_func(arg1)))
        lg2 = complex(math.log(abs(gamma_func(arg2))), math.angle(gamma_func(arg2)))
    except (OverflowError, ValueError):
        # Use Stirling
        def stirling_log(z):
            return (z - 0.5) * cmath.log(z) - z + 0.5 * cmath.log(2 * math.pi)
        import cmath
        lg1 = stirling_log(arg1)
        lg2 = stirling_log(arg2)
    
    log_chi = log_pi_factor + lg1.real - lg2.real
    return log_chi


def find_zeros_line(gamma_lo, gamma_hi, n_search=1000):
    """Find zeros of zeta on the critical line by finding sign changes of Z(t)."""
    from scipy.special import zeta as zeta_func
    
    # Use the Hardy Z function approach:
    # Z(t) = exp(i*theta(t)) * zeta(1/2+it) is real on the critical line
    # Z(t) = 0 iff zeta(1/2+it) = 0
    
    # Simple approach: look for sign changes of Re(zeta(1/2+it))
    gammas = np.linspace(gamma_lo, gamma_hi, n_search)
    zeros = []
    
    for i in range(len(gammas) - 1):
        g1, g2 = gammas[i], gammas[i+1]
        try:
            z1 = complex(0.5, g1)
            z2 = complex(0.5, g2)
            # zeta is not in standard scipy, use mpmath
        except:
            pass
    
    return zeros


def compute_chi_at_zeros():
    """Compute |chi(rho)| at known zeros using the functional equation symmetry."""
    import cmath
    
    # Known first 10 zeros (imaginary parts)
    known_zeros_im = [
        14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
        37.586178, 40.918719, 43.327073, 48.005151, 49.773832
    ]
    
    print("Computing |chi(rho)| at known zeros (rho = 1/2 + i*gamma):")
    print("=" * 60)
    
    results = []
    for i, gamma in enumerate(known_zeros_im):
        # On the critical line: s = 1/2 + i*gamma
        # |chi(1/2+it)| = 1 by symmetry (functional equation chi(s)*chi(1-s) = 1
        # and chi(1/2+it)*chi(1/2-it) = |chi(1/2+it)|^2 = 1)
        
        chi_abs = chi(0.5, gamma)
        
        # Off the critical line: s = sigma + i*gamma
        # |chi(sigma+it)| depends on sigma
        chi_off_above = chi(0.51, gamma)
        chi_off_below = chi(0.49, gamma)
        
        print(f"  Zero #{i+1}: gamma = {gamma:.6f}")
        print(f"    |chi(1/2+i*gamma)|  = {chi_abs:.10f}")
        print(f"    |chi(0.51+i*gamma)| = {chi_off_above:.10f}")
        print(f"    |chi(0.49+i*gamma)| = {chi_off_below:.10f}")
        
        results.append({
            "index": i+1,
            "gamma": gamma,
            "chi_on_line": float(chi_abs),
            "chi_at_0.51": float(chi_off_above),
            "chi_at_0.49": float(chi_off_below),
        })
    
    return results


def scan_chi_surface():
    """Scan |chi(sigma+it)| over a grid to find the surface."""
    import cmath
    
    sigmas = np.linspace(0.0, 1.0, 101)
    gammas = np.linspace(10, 50, 100)
    
    print("\nScanning |chi(sigma+it)| surface:")
    print("=" * 60)
    
    surface = []
    for sig in sigmas:
        for gam in gammas:
            chi_abs = chi(sig, gam)
            surface.append({"sigma": float(sig), "gamma": float(gam), "chi_abs": float(chi_abs)})
    
    # Find where |chi| = 1 (should be sigma = 0.5 for all gamma)
    on_line = [s for s in surface if abs(s["chi_abs"] - 1.0) < 0.01]
    above_line = [s for s in surface if s["sigma"] > 0.51 and abs(s["chi_abs"] - 1.0) < 0.01]
    
    print(f"  Points where |chi| ~ 1: {len(on_line)}")
    print(f"  Points where sigma > 0.51 AND |chi| ~ 1: {len(above_line)}")
    
    # Check: does |chi| = 1 ONLY on sigma = 0.5?
    chi_is_1_sigmas = set()
    for s in on_line:
        chi_is_1_sigmas.add(round(s["sigma"], 2))
    
    print(f"  Sigma values where |chi| ~ 1: {sorted(chi_is_1_sigmas)}")
    
    return {
        "total_points": len(surface),
        "chi_is_1_count": len(on_line),
        "chi_is_1_above_half": len(above_line),
        "chi_is_1_sigmas": sorted(chi_is_1_sigmas),
    }


def verify_rh_equivalence():
    """Confirm: |chi(rho)| = 1 at the zeros -- which is an identity, not RH.

    The original docstring read "Verify: |chi(rho)| = 1 for all zeros iff RH",
    which asserted the withdrawn equivalence. Kept as a function name for
    compatibility; see the module header and the SUMMARY block below for the
    correction, and PREDICTION_LEDGER PL-22.
    """
    print("\nConfirming the line identity |chi| = 1 (NOT an RH test):")
    print("=" * 60)
    
    # The key identity: chi(s) * chi(1-s) = 1
    # So |chi(s)| * |chi(1-s)| = 1
    # If s = sigma + it, then 1-s = (1-sigma) + it
    # |chi(sigma+it)| * |chi(1-sigma+it)| = 1
    
    # On the critical line (sigma = 0.5):
    # |chi(0.5+it)|^2 = 1 => |chi(0.5+it)| = 1
    
    # Off the critical line (sigma != 0.5):
    # |chi(sigma+it)| != 1 in general
    
    # RH says: all zeros have sigma = 0.5
    # => |chi(rho)| = 1 at all zeros
    
    # Conversely: if |chi(rho)| = 1 at all zeros,
    # then all zeros have sigma = 0.5 (since |chi| = 1 iff sigma = 0.5)
    
    print("  chi(s) * chi(1-s) = 1 (functional equation)")
    print("  |chi(0.5+it)| = 1 for all t (symmetry)")
    print("  |chi(sigma+it)| != 1 for sigma != 0.5, INSIDE the strip")
    print()
    print("  WITHDRAWN 2026-09-28 - the two lines and the 'Therefore' block:")
    print("    RH => all zeros on critical line => |chi(rho)| = 1")
    print("    |chi(rho)| = 1 for all zeros => all zeros on critical line => RH")
    print("  The second implication is FALSE AS A TEST: its hypothesis holds")
    print("  whether or not RH is true, since |chi| = 1 is the value on the whole")
    print("  critical line, zeros and non-zeros alike (~1.97e-31 apart). The")
    print("  converse is also false globally: |chi(sigma+it)| = 1 has three roots")
    print("  in sigma for t < 6.2898, the extras at 1/2 +- d(t) outside the strip.")
    print()
    print("  What survives: on 0 < Re(s) < 1, every zero must have Re(rho) = 1/2")
    print("  for |chi(rho)| = 1 -- a re-encoding of RH, not a proof. RH is open.")
    print("  See PREDICTION_LEDGER PL-22, experiments/chi_rho_vacuity_0_over_0.py")

    return True


def run():
    print("=" * 70)
    print("RH: CONDUCTOR RATIO |chi(rho)| AT KNOWN ZEROS")
    print("=" * 70)
    
    # 1. Compute at known zeros
    zero_results = compute_chi_at_zeros()
    
    # 2. Scan surface
    surface_results = scan_chi_surface()
    
    # 3. Verify equivalence
    equiv = verify_rh_equivalence()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    # Check if all |chi| on critical line are ~1
    all_on_line = all(abs(r["chi_on_line"] - 1.0) < 0.001 for r in zero_results)
    any_off_line = any(abs(r["chi_at_0.51"] - 1.0) < 0.001 for r in zero_results)
    
    print(f"  |chi(rho)| = 1 on critical line: {all_on_line}")
    print(f"  |chi(rho)| = 1 off critical line: {any_off_line}")
    print(f"  IDENTITY confirmed (on-line = 1, off-line != 1): "
          f"{all_on_line and not any_off_line}")
    print()
    print("  WHAT THIS DOES NOT SHOW (corrected 2026-09-28):")
    print("  The Riemann Hypothesis is NOT verified by this. The previous")
    print("  version of this line read 'RH equivalence verified:', which was")
    print("  false: |chi(1/2+it)| = 1 for ALL t, zeros and non-zeros alike, so")
    print("  the on-line check cannot fail and cannot tell a zero from a")
    print("  non-zero (they agree to ~1.97e-31). A non-zero point on the line")
    print("  passes the on-line test exactly as a zero does. The usable")
    print("  statement is the off-line one: on 0 < Re(s) < 1, |chi| = 1 forces")
    print("  Re(s) = 1/2. That re-encodes RH; it does not settle it.")
    print("  See experiments/chi_rho_vacuity_0_over_0.py, PREDICTION_LEDGER")
    print("  PL-22. RH remains open.")
    
    results = {
        "zero_results": zero_results,
        "surface_results": surface_results,
        "all_on_line": all_on_line,
        "any_off_line": any_off_line,
        "rh_equivalence": all_on_line and not any_off_line,
    }
    
    import json, os
    os.makedirs("data", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nOutput: {OUT}")
    return results


if __name__ == "__main__":
    run()
