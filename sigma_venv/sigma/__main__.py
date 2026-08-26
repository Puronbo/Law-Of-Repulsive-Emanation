"""
Sigma: The Removable Singularity Chassis
==========================================

A self-contained computational space for identifying, classifying,
and computing removable singularities (0/0) across all fields.

Usage:
    python -m sigma run
    python -m sigma verify
    python -m sigma bridge
    python -m sigma e8
    python -m sigma currency
    python -m sigma book

Author: Michael Grafiel S Puno
Repository: https://github.com/Puronbo/Law-Of-Repulsive-Emanation
"""

import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m sigma <command>")
        print()
        print("Commands:")
        print("  run        Run all modules")
        print("  verify     Run verification suite")
        print("  bridge     Verify chi(rho) bridge")
        print("  e8         Verify E8 structure")
        print("  currency   Show Sigma currency")
        print("  chassis    Show removable singularities")
        print("  book       Show book integration")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "run":
        from .chassis.core import Chassis
        from .chassis.bridge import verify_bridge
        from .chassis.e8 import verify_e8
        from .chassis.currency import SigmaCurrency
        from .chassis.book import BookIntegration
        from .chassis.verification import run_all_verifications
        
        c = Chassis()
        c.summary()
        print()
        
        verify_bridge(20)
        print()
        
        verify_e8()
        print()
        
        sc = SigmaCurrency()
        sc.print_summary()
        print()
        
        b = BookIntegration()
        b.summary()
        print()
        
        run_all_verifications()
    
    elif command == "verify":
        from .chassis.verification import run_all_verifications
        run_all_verifications()
    
    elif command == "bridge":
        from .chassis.bridge import verify_bridge
        verify_bridge(20)
    
    elif command == "e8":
        from .chassis.e8 import verify_e8
        verify_e8()
    
    elif command == "currency":
        from .chassis.currency import SigmaCurrency
        sc = SigmaCurrency()
        sc.print_summary()
        print()
        print(sc.export_json())
    
    elif command == "chassis":
        from .chassis.core import Chassis
        c = Chassis()
        c.summary()
    
    elif command == "book":
        from .chassis.book import BookIntegration
        b = BookIntegration()
        b.summary()
    
    else:
        print("Unknown command: %s" % command)
        sys.exit(1)


if __name__ == "__main__":
    main()
