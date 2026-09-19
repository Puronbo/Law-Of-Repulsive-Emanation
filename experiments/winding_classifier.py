"""
WINDING FINGERPRINT REGULATOR CLASSIFIER
=========================================

Uses the R_trans(A,B) phase diagram to classify regulators by their
lower-ridge winding transition radius. This is a decision tool:
"Which regulators give W=-1 at a given experimental loop size?"

Input: (A,B) coefficients in the (A,B) family D = (1-2λ)^2 - (A-Bλ)G
Output: Regulator class based on R_trans
"""

import json
import os
import sys


def classify_regulator(A, B, R_experimental=0.05):
    """
    Classify a regulator by its winding at a given loop radius.
    
    Classes:
    - EARLY: R_trans <= 0.01 (W=-1 at all reasonable loop sizes)
    - STANDARD: 0.01 < R_trans <= 0.05 (W=-1 at R=0.05)
    - LATE: 0.05 < R_trans <= 0.1 (W=-1 only at large loops)
    - NONE: R_trans > 0.1 or none (W=0 at typical loops)
    """
    # Load phase diagram
    data_path = os.path.join(os.path.dirname(__file__), "data", "winding_phase_diagram.json")
    with open(data_path) as fh:
        data = json.load(fh)
    
    # Find closest (A,B) grid point
    phase_data = data["phase_data"]
    best_match = None
    best_dist = float('inf')
    
    for row in phase_data:
        a, b = row["a"], row["b"]
        # Convert to same units as input
        A_grid = a / (72.0 * 3.141592653589793)
        B_grid = b / (72.0 * 3.141592653589793)
        dist = abs(A_grid - A) + abs(B_grid - B)
        if dist < best_dist:
            best_dist = dist
            best_match = row
    
    if best_match is None:
        return "UNKNOWN"
    
    # Get transition radius from data
    trans_str = data["transition_map"].get(f"({best_match['a']},{best_match['b']})")
    if trans_str is None:
        R_trans = None
    else:
        R_trans = float(trans_str)
    
    # Determine winding at R_experimental
    w_at_R = best_match["w_by_R"].get(str(R_experimental), 0)
    
    # Classify
    if R_trans is None:
        cls = "NONE"
    elif R_trans <= 0.01:
        cls = "EARLY"
    elif R_trans <= 0.05:
        cls = "STANDARD"
    elif R_trans <= 0.1:
        cls = "LATE"
    else:
        cls = "NONE"
    
    return {
        "class": cls,
        "R_trans": R_trans,
        "W_at_R": w_at_R,
        "nearest_grid": (best_match["a"], best_match["b"]),
        "distance": best_dist
    }


def main():
    print("=" * 70)
    print("WINDING FINGERPRINT REGULATOR CLASSIFIER")
    print("=" * 70)
    print("Classes: EARLY (R_trans<=0.01), STANDARD (0.01<R_trans<=0.05),")
    print("         LATE (0.05<R_trans<=0.1), NONE (R_trans>0.1/none)")
    print()
    
    # Test some known regulators
    test_regulators = [
        ("Litim (29,9)", 29/(72*3.141592653589793), 9/(72*3.141592653589793)),
        ("Exponential (est.)", 20/(72*3.141592653589793), 5/(72*3.141592653589793)),
        ("Sharp (est.)", 40/(72*3.141592653589793), 15/(72*3.141592653589793)),
        ("Optimized (32,15)", 32/(72*3.141592653589793), 15/(72*3.141592653589793)),
    ]
    
    for name, A, B in test_regulators:
        result = classify_regulator(A, B, 0.05)
        print(f"{name:20s}: class={result['class']:8s}, "
              f"R_trans={str(result['R_trans']):>6s}, "
              f"W@0.05={result['W_at_R']:+d}, "
              f"grid=({result['nearest_grid'][0]},{result['nearest_grid'][1]})")
    
    print()
    print("=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    print("EARLY:    Lower-ridge W=-1 at all practical loop sizes")
    print("          (Litim is EARLY: R_trans=0.005)")
    print("STANDARD: W=-1 at R=0.05, transition at small loops")
    print("LATE:     W=-1 only at large loops (R>0.05)")
    print("NONE:     W=0 at all practical loop sizes")
    print()
    print("Use this to choose regulators for which the -1 fingerprint")
    print("is robust at your experimental loop resolution.")
    print("=" * 70)

    # Output
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, "winding_classifier.json")
    
    out = {
        "classes": ["EARLY", "STANDARD", "LATE", "NONE"],
        "thresholds": {"EARLY": 0.01, "STANDARD": 0.05, "LATE": 0.1},
        "test_results": {}
    }
    for name, A, B in test_regulators:
        result = classify_regulator(A, B, 0.05)
        out["test_results"][name] = result
    
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2)
    
    print(f"\nOutput written to {out_path}")
    sys.exit(0)


if __name__ == "__main__":
    main()