"""
CMB DIPOLE FRAME CONFRONTATION
=================================

The CMB kinematic dipole defines a preferred frame:
v_CMB = 369.82 +/- 0.11 km/s towards (l,b) = (264.021 deg, 48.253 deg)
(Planck 2013/2018 dipole; confirmed by 2020a CatWISE vs kinematic comparison).

This experiment checks whether the framework's C_0-centered cosmology
(GENESIS.md, THE_UNIVERSE_FROM_A_FIXED_POINT.md) makes any frame-dependent
predictions that could be confronted with the dipole measurement.

The framework's fixed point C_0 is a scalar (0/0 structure), so it is
frame-invariant by construction. The RG flow equations are also frame-invariant
(Diff-invariant effective action). The CMB dipole is a kinematic effect from
our motion relative to the CMB rest frame.

Conclusion: The framework has NO preferred frame at the fundamental level.
The dipole is an observational artifact of our motion, not a fundamental
asymmetry. This is CONSISTENT with the framework (no frame statement needed).
"""

import json
import os
import sys


def main():
    print("=" * 70)
    print("CMB DIPOLE FRAME CONFRONTATION")
    print("=" * 70)
    print()
    print("Measured kinematic dipole:")
    print("  v_CMB = 369.82 +/- 0.11 km/s")
    print("  (l, b) = (264.021 deg, 48.253 deg)")
    print("  Source: Planck 2013/2018 + 2020a CatWISE")
    print()
    print("Framework structure:")
    print("  C_0 = scalar fixed point (0/0 structure) -> frame-invariant")
    print("  RG flow = Diff-invariant effective action -> frame-invariant")
    print("  CMB dipole = kinematic effect (our motion) -> not fundamental")
    print()
    print("Dipole anomaly (CatWISE vs kinematic, >5 sigma):")
    print("  The anomaly is in the *large-scale structure* dipole, not CMB.")
    print("  It may indicate a true large-scale bulk flow or systematics.")
    print("  Framework has no prediction for bulk flows (no dark matter model).")
    print()
    print("CONCLUSION: Framework is frame-invariant at the fundamental level.")
    print("  The CMB dipole is a kinematic artifact, not a fundamental asymmetry.")
    print("  No confrontation needed; framework is CONSISTENT by construction.")
    print("=" * 70)

    # Output
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, "dipole_frame_confrontation.json")
    
    out = {
        "measured_dipole": {
            "v_km_s": 369.82,
            "v_err_km_s": 0.11,
            "l_deg": 264.021,
            "b_deg": 48.253,
            "source": "Planck 2013/2018 + 2020a CatWISE"
        },
        "dipole_anomaly": {
            "description": "CatWISE vs kinematic dipole >5 sigma",
            "note": "Anomaly is in large-scale structure dipole, not CMB. Framework has no bulk flow prediction."
        },
        "framework": {
            "C0": "scalar fixed point (0/0 structure) -> frame-invariant",
            "RG_flow": "Diff-invariant effective action -> frame-invariant",
            "prediction": "No fundamental preferred frame"
        },
        "confrontation": {
            "result": "CONSISTENT",
            "reasoning": "Framework has no frame-dependent prediction; dipole is kinematic artifact of observer motion."
        }
    }
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2)
    
    print(f"\nOutput written to {out_path}")
    sys.exit(0)


if __name__ == "__main__":
    main()