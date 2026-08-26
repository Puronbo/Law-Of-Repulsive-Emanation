"""
Example 1: Detecting Removable Singularities
=============================================

Shows how to use the detector to find and classify singularities.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sigma.chassis.detector import lhopital, analyze_function, KNOWN_SINGULARITIES
import math


def main():
    print("EXAMPLE 1: Detecting Removable Singularities")
    print("=" * 60)
    print()
    
    # 1. Compute L'Hopital limits
    print("1. L'HOPITAL LIMITS")
    print("-" * 60)
    
    tests = [
        ("sin(x)/x", math.sin, lambda x: x, 0),
        ("(e^x-1)/x", lambda x: math.exp(x)-1, lambda x: x, 0),
        ("log(1+x)/x", lambda x: math.log(1+x), lambda x: x, 0),
        ("(1-cos(x))/x^2", lambda x: 1-math.cos(x), lambda x: x*x, 0),
        ("tan(x)/x", math.tan, lambda x: x, 0),
    ]
    
    for name, f, g, a in tests:
        result = lhopital(f, g, a)
        print("  %-20s = %.10f  [%s]" % (
            name, result['result'], 
            "PASS" if result['verified'] else "FAIL"))
    
    print()
    
    # 2. Analyze a function
    print("2. FUNCTION ANALYSIS")
    print("-" * 60)
    
    analysis = analyze_function(
        lambda x: math.sin(x)/x if abs(x) > 1e-15 else 1.0,
        'sin(x)/x'
    )
    print("  Function: %s" % analysis['name'])
    print("  Zeros found: %d" % analysis['zeros_found'])
    print("  Singularities:")
    for s in analysis['singularities']:
        print("    x = %.6f  [%s]  value = %.6f" % (
            s['point'], s['type'], s['removable_value']))
    
    print()
    
    # 3. Pre-defined singularities
    print("3. PRE-DEFINED SINGULARITIES")
    print("-" * 60)
    
    for name, data in KNOWN_SINGULARITIES.items():
        print("  %-20s = %.6f  at x = %.1f  [%s]" % (
            data['name'], data['value'], data['point'], data['source']))
    
    print()
    print("Done!")


if __name__ == "__main__":
    main()
