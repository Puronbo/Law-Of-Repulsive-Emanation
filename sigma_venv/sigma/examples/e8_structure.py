"""
Example 2: E8 Exceptional Lie Algebra
=====================================

Shows how to access and verify the E8 structure.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sigma.chassis.e8 import exponents, degrees, weyl_order, root_count, verify_e8


def main():
    print("EXAMPLE 2: E8 Exceptional Lie Algebra")
    print("=" * 60)
    print()
    
    # 1. Structure constants
    print("1. STRUCTURE CONSTANTS")
    print("-" * 60)
    
    exp = exponents()
    deg = degrees()
    
    print("  Rank: 8")
    print("  Exponents: %s" % exp)
    print("  Degrees: %s" % deg)
    print("  Weyl order: %d" % weyl_order())
    print("  Root count: %d" % root_count())
    print("  Coxeter h: 30 (self-dual)")
    
    print()
    
    # 2. Verify
    print("2. VERIFICATION")
    print("-" * 60)
    
    verify_e8()
    
    print()
    
    # 3. The prime connection
    print("3. THE PRIME CONNECTION")
    print("-" * 60)
    
    print("  E8 exponents = 1 + primes(2,3,5,7,11,13,17,19,23,29)")
    print("  [1, 7, 11, 13, 17, 19, 23, 29]")
    print()
    print("  This is not a coincidence.")
    print("  The primes encode the structure of the universe.")
    
    print()
    print("Done!")


if __name__ == "__main__":
    main()
