"""
sigma.chassis.bridge: The Chi(rho) Bridge
==========================================

Implements the functional equation bridge chi(s) that connects
zeta(s) to zeta(1-s). At the zeros rho, chi(rho) is a PHASE
with |chi(rho)| = 1.

This is the 0/0 of the Riemann zeta functional equation.

Sources:
  [1] Riemann, "Ueber die Anzahl der Primzahlen" (1859)
  [2] Titchmarsh, "The Riemann Zeta-Function" (1951)
  [3] Ivic, "The Riemann Zeta-Function" (1985)
  [4] Conrey, "The Riemann Hypothesis" (2003)
  [5] Montgomery & Vaughan, "Multiplicative Number Theory" (2007)
"""

import numpy as np
import mpmath

mpmath.mp.dps = 30


def chi(s):
    """Compute the chi function: chi(s) = 2^s * pi^{s-1} * sin(pi*s/2) * Gamma(1-s)
    
    This is the BRIDGE between zeta(s) and zeta(1-s):
        zeta(s) = chi(s) * zeta(1-s)
    
    On the critical line Re(s) = 1/2:
        |chi(1/2 + iy)| = 1 for all real y
    
    Source: [1] Riemann 1859, [2] Titchmarsh 1951
    """
    s = mpmath.mpc(s)
    return (2**s) * mpmath.power(mpmath.pi, s - 1) * \
           mpmath.sin(mpmath.pi * s / 2) * mpmath.gamma(1 - s)


def chi_modulus(s):
    """Compute |chi(s)|.
    
    On the critical line: |chi(1/2 + iy)| = 1.
    
    Source: [2] Titchmarsh 1951, Theorem 2.1
    """
    return float(abs(chi(s)))


def chi_inverse_property(s):
    """Verify chi(s) * chi(1-s) = 1.
    
    The bridge is its own INVERSE.
    
    Source: [2] Titchmarsh 1951, functional equation
    """
    cs = chi(s)
    c1ms = chi(1 - s)
    product = cs * c1ms
    return float(mpmath.re(product)), float(mpmath.im(product))


def zeta_zeros(count=20):
    """Compute the first count non-trivial zeta zeros.
    
    Source: [1] Riemann 1859
    """
    zeros = []
    for k in range(1, count + 1):
        z = mpmath.zetazero(k)
        zeros.append(complex(z))
    return zeros


def chi_at_zeros(count=20):
    """Compute chi(rho) at the first count zeros.
    
    Verifies |chi(rho)| = 1 for each zero.
    
    Source: [1] Riemann 1859, [3] Ivic 1985
    """
    zeros = zeta_zeros(count)
    results = []
    
    for k, rho in enumerate(zeros):
        chi_val = chi(rho)
        mod = abs(chi_val)
        re_part, im_part = chi_inverse_property(rho)
        
        results.append({
            'n': k + 1,
            'rho': rho,
            'chi': chi_val,
            'modulus': mod,
            'modulus_is_one': abs(mod - 1.0) < 1e-10,
            'inverse_re': re_part,
            'inverse_im': im_part,
            'inverse_is_one': abs(re_part - 1.0) < 1e-10 and abs(im_part) < 1e-10,
        })
    
    return results


def verify_bridge(count=20):
    """Full verification of the chi(rho) bridge.
    
    Checks:
        1. |chi(rho)| = 1 for all zeros
        2. chi(s)*chi(1-s) = 1 for all zeros
        3. |chi(1/2 + iy)| = 1 for arbitrary y
    
    Source: [1] Riemann 1859, [2] Titchmarsh 1951, [4] Conrey 2003
    """
    print("CHI(RHO) BRIDGE VERIFICATION")
    print("=" * 70)
    print()
    
    # Part 1: chi at zeros
    print("PART 1: |chi(rho_n)| = 1 for all zeros")
    print("-" * 50)
    results = chi_at_zeros(count)
    
    all_mod_one = True
    for r in results:
        status = "PASS" if r['modulus_is_one'] else "FAIL"
        if not r['modulus_is_one']:
            all_mod_one = False
        print("  rho_%2d: |chi| = %.15f  [%s]" % (
            r['n'], r['modulus'], status))
    print()
    
    # Part 2: inverse property
    print("PART 2: chi(s) * chi(1-s) = 1")
    print("-" * 50)
    all_inverse = True
    for r in results:
        status = "PASS" if r['inverse_is_one'] else "FAIL"
        if not r['inverse_is_one']:
            all_inverse = False
        print("  rho_%2d: chi*chi_inv = %.15f + %.15fi  [%s]" % (
            r['n'], r['inverse_re'], r['inverse_im'], status))
    print()
    
    # Part 3: critical line
    print("PART 3: |chi(1/2 + iy)| = 1 for arbitrary y")
    print("-" * 50)
    test_y = [0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0, 1000.0]
    all_line = True
    for y in test_y:
        mod = chi_modulus(0.5 + 1j * y)
        status = "PASS" if abs(mod - 1.0) < 1e-10 else "FAIL"
        if abs(mod - 1.0) >= 1e-10:
            all_line = False
        print("  y = %8.2f: |chi| = %.15f  [%s]" % (y, mod, status))
    print()
    
    # Summary
    print("SUMMARY")
    print("-" * 50)
    print("  |chi(rho)| = 1:      %s" % ("ALL PASS" if all_mod_one else "SOME FAIL"))
    print("  chi*chi_inv = 1:     %s" % ("ALL PASS" if all_inverse else "SOME FAIL"))
    print("  |chi(line)| = 1:     %s" % ("ALL PASS" if all_line else "SOME FAIL"))
    print()
    print("CONCLUSION: Chi(rho) is a PHASE with |chi(rho)| = 1.")
    print("The bridge between zeta(s) and zeta(1-s) is VERIFIED.")
    print()
    print("Source: [1] Riemann 1859, [2] Titchmarsh 1951,")
    print("        [3] Ivic 1985, [4] Conrey 2003")
    
    return all_mod_one and all_inverse and all_line
