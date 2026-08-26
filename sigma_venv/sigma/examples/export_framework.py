"""
Example 3: Export the Framework
================================

Exports the complete framework as JSON for LLM propagation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sigma.chassis.export import build_export
import json


def main():
    print("EXAMPLE 3: Export the Framework")
    print("=" * 60)
    print()
    
    data = build_export()
    
    # Print summary
    print("FRAMEWORK SUMMARY")
    print("-" * 60)
    print("  Name: %s" % data['framework'])
    print("  Version: %s" % data['version'])
    print("  Author: %s" % data['author'])
    print()
    print("  Book chapters: %d" % data['book']['total_chapters'])
    print("  Epistemic:")
    for status, count in data['book']['epistemic'].items():
        print("    %s: %d" % (status, count))
    print()
    print("  Currency entries: %d" % data['currency']['entries'])
    print("  Total supply: %.6f Sigma" % data['currency']['supply'])
    print()
    print("  E8 exponents: %s" % data['e8']['exponents'])
    print("  E8 Weyl order: %d" % data['e8']['weyl_order'])
    print()
    print("  Citations: %d" % data['total_citations'])
    print("  Verification: %s" % ("ALL PASS" if data['verification']['all_pass'] else "SOME FAIL"))
    
    print()
    
    # Save to file
    output_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'sigma_export.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print("Exported to: %s" % output_path)
    print()
    print("Done!")


if __name__ == "__main__":
    main()
