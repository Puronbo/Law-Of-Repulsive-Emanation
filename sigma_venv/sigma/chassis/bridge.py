"""
sigma.chassis.bridge: The Chi(rho) Bridge
==========================================

Implements the functional equation bridge chi(s) that connects
zeta(s) to zeta(1-s). At the zeros rho, chi(rho) is a PHASE
with |chi(rho)| = 1.

This is the 0/0 of the Riemann zeta functional equation.

WHAT THIS DOES AND DOES NOT SHOW  (corrected 2026-09-28)
------------------------------------------------------
The identities below are true and the code checks them correctly. What
they do NOT show is the Riemann Hypothesis, and the earlier version of
this docstring implied that they did.

|chi| = 1 is a property of the critical LINE, not of the zeros. Since
|chi(1/2 + iy)| = 1 for every real y, a point on the line that is NOT a
zero passes every check in this module exactly as a zero does - they
agree to ~1.97e-31. So verify_bridge() cannot fail on the question it
appears to ask, and by the repository's own ledger rule ("a claim with
no refutation condition is not a claim") it was never evidence for RH.

The half of chi that DOES have teeth is the level set: on the critical
strip 0 < Re(s) < 1, |chi| = 1 forces Re(s) = 1/2, and displacing
Re(s) is caught at every scale (Re = 0.501 gives |chi| = 0.99919). That
is a sharp, usable statement about the strip - and it is a re-encoding
of RH, not a proof of it. RH remains open.

Measurements: experiments/chi_rho_vacuity_0_over_0.py
Governance:    docs/PREDICTION_LEDGER.md PL-22, docs/AUDIT.md section 2 item 8

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
    """Compute the completed factor: chi(s) = 2^s * pi^{s-1} * sin(pi*s/2) * Gamma(1-s)

    This is the BRIDGE between zeta(s) and zeta(1-s):
        zeta(s) = chi(s) * zeta(1-s)

    On the critical line Re(s) = 1/2:
        |chi(1/2 + iy)| = 1 for all real y

    ROBUSTNESS (2026-09-28): the formula above is a 0 * infinity product at
    every even positive integer and raises "gamma function pole" at s = 2, 4,
    6, ... where chi is perfectly finite (|chi(2)| = 2 pi^2). Where a pole is
    possible, use chi_ratio(s) below, which is the same function written as
    pi^(s-1/2) * Gamma((1-s)/2) / Gamma(s/2) and has no removable singularities.

    Source: [1] Riemann 1859, [2] Titchmarsh 1951
    """
    s = mpmath.mpc(s)
    return (2**s) * mpmath.power(mpmath.pi, s - 1) * \
           mpmath.sin(mpmath.pi * s / 2) * mpmath.gamma(1 - s)


def chi_ratio(s):
    """The same chi, pole-free: pi^(s-1/2) * Gamma((1-s)/2) / Gamma(s/2).

    Identical to chi(s) as a function, but regular at s = 2, 4, 6, ... where
    chi() raises. Gate 7 of experiments/chi_rho_vacuity_0_over_0.py checks the
    two forms agree wherever both are defined.
    """
    s = mpmath.mpc(s)
    return (mpmath.power(mpmath.pi, s - mpmath.mpf(0.5)) * mpmath.gamma((1 - s) / 2)
            / mpmath.gamma(s / 2))


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

    Confirms |chi(rho)| = 1 for each zero. This is a true identity, but note
    (2026-09-28) that it is NOT evidence for RH: the same value is produced at
    a non-zero point of the critical line at the same height (they agree to
    ~1.97e-31), so this check has no discriminating power. Use
    chi_line_displaced() to exercise the half of chi that can fail.

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


def chi_line_displaced(t=14.1347251417, deltas=(0.1, 0.01, 0.001, 1e-6)):
    """Exercise the half of chi that CAN fail: displace Re(s) off 1/2.

    |chi(1/2 + iy)| = 1 identically, so it cannot fail. But on the critical
    strip 0 < Re(s) < 1 the level set is exactly {1/2}, so displacing the real
    part is caught at every scale tested. This is the check that carries
    information, and it is the one the earlier version of this module omitted.

    Source: [2] Titchmarsh 1951, Theorem 2.1; measured in
            experiments/chi_rho_vacuity_0_over_0.py
    """
    out = []
    for d in deltas:
        s = 0.5 + d + 1j * t
        mod = chi_modulus(s)
        out.append({
            'delta': d,
            'modulus': mod,
            'deviation': abs(mod - 1.0),
            'caught': abs(mod - 1.0) > 1e-10,
        })
    return out


def chi_line_impostor(k=1):
    """A point on the critical line that is NOT a zero, at zero k's height.

    The falsification control: the identity at this point is indistinguishable
    from the identity at the zero itself, which is exactly why checking
    |chi(rho)| = 1 at located zeros certifies nothing. Agreement measured at
    ~1.97e-31 over 10 zeros.

    Source: measured in experiments/chi_rho_vacuity_0_over_0.py gate 2
    """
    rho = mpmath.zetazero(k)
    impostor = mpmath.mpc(0.5, mpmath.im(rho) + 0.5)
    at_zero = abs(chi(rho))
    at_impostor = chi_modulus(impostor)
    return {
        'k': k,
        'gamma': float(mpmath.im(rho)),
        'abs_zeta_at_impostor': float(abs(mpmath.zeta(impostor))),
        'modulus_at_zero': float(at_zero),
        'modulus_at_impostor': at_impostor,
        'difference': abs(float(at_zero) - at_impostor),
        'impostor_passes_same_test': abs(at_impostor - 1.0) < 1e-10,
    }


def verify_bridge(count=20):
    """Check the chi(rho) bridge - and state honestly what it decides.

    Checks (all true identities, all confirmed here):
        1. |chi(rho)| = 1 at the first `count` zeros
        2. chi(s)*chi(1-s) = 1 at those zeros
        3. |chi(1/2 + iy)| = 1 for arbitrary y, zero or not

    Falsification controls (added 2026-09-28), because checks 1-3 cannot fail:
        4. a NON-zero point on the line passes check 1 identically
        5. displacing Re(s) off 1/2 IS caught, at every scale

    CONCLUSION: the identities are VERIFIED; the Riemann Hypothesis is NOT.
    Check 4 is the reason - the instrument has no teeth where the corpus used
    to read it as a verification. Check 5 shows the level-set statement does
    have teeth, and is the sharp, usable form.

    Source: [1] Riemann 1859, [2] Titchmarsh 1951, [4] Conrey 2003
    """
    print("CHI(RHO) BRIDGE - IDENTITY CHECK + FALSIFICATION CONTROLS")
    print("=" * 70)
    print()

    # Part 1: chi at zeros
    print("PART 1: |chi(rho_n)| = 1 at the first %d zeros" % count)
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

    # Part 4: falsification control - a NON-zero on the line passes Part 1
    print("PART 4: FALSIFICATION CONTROL - a non-zero on the line")
    print("-" * 50)
    imp = chi_line_impostor(1)
    print("  planted point 1/2 + i(gamma_1 + 0.5), |zeta| there = %.6g"
          % imp['abs_zeta_at_impostor'])
    print("  |chi| at the zero        = %.15f" % imp['modulus_at_zero'])
    print("  |chi| at the NON-zero    = %.15f" % imp['modulus_at_impostor'])
    print("  difference               = %.3g" % imp['difference'])
    print("  non-zero passes Part 1?  %s   <-- THIS IS WHY PART 1 PROVES NOTHING"
          % ("YES" if imp['impostor_passes_same_test'] else "no"))
    print()

    # Part 5: the half with teeth
    print("PART 5: the level set does have teeth (Re(s) displaced)")
    print("-" * 50)
    disp = chi_line_displaced()
    all_caught = all(d['caught'] for d in disp)
    for d in disp:
        print("  Re(s) = 1/2 + %-8g : |chi| = %.15f  [%s]" % (
            d['delta'], d['modulus'], "CAUGHT" if d['caught'] else "MISSED"))
    print()

    # Summary
    print("SUMMARY")
    print("-" * 50)
    print("  |chi(rho)| = 1:      %s" % ("ALL PASS" if all_mod_one else "SOME FAIL"))
    print("  chi*chi_inv = 1:     %s" % ("ALL PASS" if all_inverse else "SOME FAIL"))
    print("  |chi(line)| = 1:     %s" % ("ALL PASS" if all_line else "SOME FAIL"))
    print("  non-zero passes:     %s  (falsification control - expected YES)"
          % ("YES" if imp['impostor_passes_same_test'] else "no"))
    print("  Re(s) displaced:     %s" % ("ALL CAUGHT" if all_caught else "SOME MISSED"))
    print()
    print("CONCLUSION")
    print("-" * 50)
    print("  VERIFIED: chi(rho) is a PHASE with |chi(rho)| = 1, and")
    print("            zeta(s) = chi(s) zeta(1-s) is the bridge.")
    print("  NOT VERIFIED, and withdrawn 2026-09-28: the Riemann Hypothesis.")
    print("            Part 1 cannot fail - Part 4 shows a point that is not a")
    print("            zero passes it identically - so it is not evidence for RH.")
    print("  The usable statement is Part 5: on 0 < Re(s) < 1, |chi| = 1 forces")
    print("            Re(s) = 1/2. That re-encodes RH; it does not settle it.")
    print("  RH remains open.")
    print()
    print("Sources: [1] Riemann 1859, [2] Titchmarsh 1951,")
    print("         [3] Ivic 1985, [4] Conrey 2003")
    print("Checks:  experiments/chi_rho_vacuity_0_over_0.py,")
    print("         docs/PREDICTION_LEDGER.md PL-22")

    return all_mod_one and all_inverse and all_line and all_caught
