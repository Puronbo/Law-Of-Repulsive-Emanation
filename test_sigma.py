"""
Sigma Chassis: Test Runner
============================

Run all tests for the Sigma framework.
This script can be executed from outside the venv
if mpmath and numpy are available.

Author: Michael Grafiel S Puno
"""

import sys
import os

# Add the sigma_venv directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sigma_venv'))


def run_tests():
    """Run all tests."""
    print("SIGMA CHASSIS: TEST SUITE")
    print("=" * 70)
    print()
    
    # Test 1: Core chassis
    print("TEST 1: REMOVABLE SINGULARITY CHASSIS")
    print("-" * 70)
    from sigma.chassis.core import Chassis
    
    c = Chassis()
    for item in c.list_known():
        print("  %-20s = %.10f  [%s]  %s" % (
            item['name'], item['value'],
            item['classification'],
            "VERIFIED" if item['verified'] else "UNVERIFIED"))
    print()
    
    # Test 2: Chi(rho) bridge
    print("TEST 2: CHI(RHO) BRIDGE")
    print("-" * 70)
    from sigma.chassis.bridge import chi_at_zeros, verify_bridge
    
    results = chi_at_zeros(10)
    all_ok = True
    for r in results:
        ok = r['modulus_is_one']
        if not ok:
            all_ok = False
        print("  rho_%2d: |chi| = %.15f  [%s]" % (
            r['n'], r['modulus'], "PASS" if ok else "FAIL"))
    print("  All |chi(rho)| = 1: %s" % ("YES" if all_ok else "NO"))
    print()
    
    # Test 3: E8 structure
    print("TEST 3: E8 STRUCTURE")
    print("-" * 70)
    from sigma.chassis.e8 import exponents, degrees, weyl_order, root_count
    
    exp = exponents()
    deg = degrees()
    wo = weyl_order()
    rc = root_count()
    
    print("  Exponents: %s" % exp)
    print("  Degrees: %s" % deg)
    print("  Weyl order: %s (expected 696729600)" % wo)
    print("  Root count: %d (expected 240)" % rc)
    print("  All E8 verified: %s" % (
        "YES" if wo == 696729600 and rc == 240 else "NO"))
    print()
    
    # Test 4: Currency
    print("TEST 4: SIGMA CURRENCY")
    print("-" * 70)
    from sigma.chassis.currency import SigmaCurrency
    
    sc = SigmaCurrency()
    print("  Total supply: %.6f Sigma" % sc.total_supply())
    print("  Singularity count: %d" % len(sc.values))
    print("  Integrity hash: %s" % sc.integrity_hash()[:16])
    print()
    
    # Test 5: Verification suite
    print("TEST 5: VERIFICATION SUITE")
    print("-" * 70)
    from sigma.chassis.verification import run_all_verifications
    
    ok = run_all_verifications()
    
    return ok


if __name__ == "__main__":
    ok = run_tests()
    sys.exit(0 if ok else 1)
