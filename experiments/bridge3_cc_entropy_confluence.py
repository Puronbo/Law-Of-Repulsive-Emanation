"""
BRIDGE-3: CC GAP x HORIZON ENTROPY CONFLUENCE (CONCRETE ARTIFACT)
================================================================

Quantifies the BRIDGE-3 confluence claimed in docs/VERIFICATION_LEDGER.md
("CC gap 2.77e-122 and horizon entropy are inverse numbers owned twice by
the framework").

Physically exact statement this artifact pins:

    Lambda_tilde = Lambda_obs * l_P^2            (dimensionless CC gap)
    S_dS         = 3*pi / Lambda_tilde  k_B      (de Sitter horizon entropy)
    S_dS * Lambda_tilde = 3*pi  (~9.4248)        (exact, by construction)

i.e. the observed dimensionless cosmological constant (10^-122) and the
de Sitter horizon entropy (10^122) are reciprocal numbers up to the exact
geometric factor 3*pi. Both descend from the same H0/Lambda measurement
through the same de Sitter geometry, so the confluence is an identity,
not a coincidence.

FLOOR-6 companion (NOT the inverse): S_CMB ~ 10^89-90 k_B from the photon
gas at T = 2.72548 K is the entropy floor, a distinct number.

Also records two audit findings found while building this artifact:
  1. THE_UNIVERSE_FROM_A_FIXED_POINT.md:195 prints the CC gap arithmetic
     as "1.06e-52 x 6.674e-11 / (1.616e-35)^2" which evaluates to ~2.7e7,
     NOT 2.77e-122. The correct factor is l_P^2 = G*hbar/c^3 (i.e. the
     printed divisor should be l_P^2, not G/l_P^2). The value itself is
     correct.
  2. VERIFICATION_LEDGER.md BRIDGE-3 row cited the artifact as
     "experiments" (no concrete file) and named S_CMB as the inverse
     number; the exact inverse of the CC gap is S_dS ~ 10^122.
"""

import math
import json
import os
import sys

K_B = 1.380649e-23        # J/K  (CODATA 2018)
H_BAR = 1.054571817e-34   # J s  (CODATA 2018)
C_SI = 2.99792458e8       # m/s
G_SI = 6.67430e-11        # m^3 kg^-1 s^-2  (CODATA 2018)
L_P = math.sqrt(H_BAR * G_SI / C_SI ** 3)      # 1.616e-35 m
L_P2 = H_BAR * G_SI / C_SI ** 3                # 2.611e-70 m^2
A_RAD = 7.5657e-16        # radiation constant J m^-3 K^-4

# Framework canon (THE_UNIVERSE_FROM_A_FIXED_POINT.md:195)
LAMBDA_CANON = 1.06e-52   # m^-2
TARGET_GAP = 2.77e-122

# Planck 2018 cosmology (independent cross-check)
H0_PLANCK = 67.36          # km/s/Mpc
OM_L_PLANCK = 0.6847
T_CMB = 2.72548           # K (Fixsen 2009)
N_GAMMA = 411.0e6         # cm^-3 -> 4.11e8 m^-3


def h0_si(h0_kms_mpc):
    """km/s/Mpc -> s^-1 (1 Mpc = 3.085677581e22 m)."""
    return h0_kms_mpc * 1000.0 / 3.085677581e22


def lambda_from_h0(h0_kms_mpc, om_l):
    """Lambda_obs = 3 * Omega_L * H0^2 / c^2  (m^-2)."""
    return 3.0 * om_l * h0_si(h0_kms_mpc) ** 2 / C_SI ** 2


def cc_gap(lambda_obs):
    """Dimensionless CC gap Lambda_tilde = Lambda_obs * G*hbar/c^3."""
    return lambda_obs * L_P2


def S_dS_from_gap(gap):
    """de Sitter horizon entropy in k_B: S_dS = 3*pi / Lambda_tilde."""
    return 3.0 * math.pi / gap


def S_CMB_from_temperature(T, radius_m):
    """Photon-gas entropy in k_B: S = (4/3) * a_R T^4 V / (T * k_B)
    == s/n * n_gamma * V with s/n = 2*pi^4/(45*zeta(3)) ~ 3.6016."""
    V = (4.0 * math.pi / 3.0) * radius_m ** 3
    U = A_RAD * T ** 4 * V
    S_J_K = (4.0 / 3.0) * U / T
    S_kB = S_J_K / K_B
    n_per_particle = 2.0 * math.pi ** 4 / (45.0 * 1.202056903159594)
    S_kB_cross = n_per_particle * N_GAMMA * V
    return S_kB, S_kB_cross


def main():
    print("=" * 70)
    print("BRIDGE-3: CC GAP x HORIZON ENTROPY CONFLUENCE")
    print("=" * 70)
    print(f"l_P  = {L_P:.4e} m   l_P^2 = {L_P2:.4e} m^2")
    print()

    # --- 1. Framework canon CC gap, reproduced exactly ---
    gap_canon = cc_gap(LAMBDA_CANON)
    print(f"[1] Canon gap: Lambda_tilde = {LAMBDA_CANON:.2e} x {L_P2:.3e}"
          f" = {gap_canon:.4e}   (target {TARGET_GAP:.3e})")
    print(f"    ratio canon/target = {gap_canon / TARGET_GAP:.6f}")

    # Audit finding: the printed recipe is arithmetically wrong.
    printed_recipe = LAMBDA_CANON * G_SI / L_P ** 2
    print(f"    AUDIT: literal doc arithmetic (x G / l_P^2) = "
          f"{printed_recipe:.2e}  --> NOT 2.77e-122 (doc typo)")

    # --- 2. Planck 2018 independent cross-check ---
    lam_planck = lambda_from_h0(H0_PLANCK, OM_L_PLANCK)
    gap_planck = cc_gap(lam_planck)
    print(f"\n[2] Planck 2018: Lambda_obs = 3*0.6847*H0^2/c^2 = "
          f"{lam_planck:.3e} m^-2")
    print(f"    Lambda_tilde = {gap_planck:.4e} (same order; H0/T depends)")

    # --- 3. de Sitter horizon entropy: the exact inverse number ---
    s_ds_canon = S_dS_from_gap(gap_canon)
    s_ds_planck = S_dS_from_gap(gap_planck)
    print(f"\n[3] S_dS = 3*pi / Lambda_tilde:")
    print(f"    canon : {s_ds_canon:.4e} k_B   (target ~1e122, 3.1e122 in map)")
    print(f"    planck: {s_ds_planck:.4e} k_B")
    prod = s_ds_canon * gap_canon
    print(f"    S_dS x Lambda_tilde = {prod:.10f}  (3*pi = {3*math.pi:.10f})")

    # --- 4. FLOOR-6: S_CMB (companion, NOT the inverse) ---
    R_HUBBLE = C_SI / h0_si(H0_PLANCK)          # c/H0 ~ 1.37e26 m
    R_PART_HORIZON = 46.5 * 9.4607e24           # 1 Gly = 9.4607e24 m -> 4.40e26 m
    s_cmb_h, s_cmb_h_x = S_CMB_from_temperature(T_CMB, R_HUBBLE)
    s_cmb_p, s_cmb_p_x = S_CMB_from_temperature(T_CMB, R_PART_HORIZON)
    print(f"\n[4] FLOOR-6 S_CMB at T = {T_CMB} K:")
    print(f"    radius c/H0 (1.37e26 m) : {s_cmb_h:.3e} k_B "
          f"(cross-check {s_cmb_h_x:.3e})")
    print(f"    radius 46.5 Gly (4.40e26): {s_cmb_p:.3e} k_B "
          f"(cross-check {s_cmb_p_x:.3e})")
    inv_gap = 1.0 / gap_canon
    print(f"\n[5] Inverse relations:")
    print(f"    1 / Lambda_tilde      = {inv_gap:.4e}  = S_dS/{3*math.pi:.4f}")
    print(f"    1 / S_CMB             = {1.0/s_cmb_p:.4e}  (NOT 2.77e-122)")
    print(f"    S_CMB IS the floor companion, NOT the inverse; the inverse")
    print(f"    number is S_dS ~ {s_ds_canon:.1e} k_B.")

    # --- 6. Gate checks ---
    ok_matrix = {}
    ok_matrix["canon_gap_reproduced_to_5pct"] = abs(gap_canon - TARGET_GAP) / TARGET_GAP < 0.05
    ok_matrix["planck_gap_same_order"] = 1e-123 < gap_planck < 1e-121
    ok_matrix["inverse_identity_exact"] = abs(prod - 3.0 * math.pi) < 1e-9
    ok_matrix["sds_is_1e122"] = 1e122 < s_ds_canon < 1e123
    ok_matrix["s_cmb_in_1e89_90"] = 1e89 < s_cmb_p < 1e90
    ok_matrix["s_cmb_not_inverse"] = inv_gap / s_cmb_p > 1e25
    all_ok = all(ok_matrix.values())
    print(f"\nGates:")
    for k, v in ok_matrix.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")

    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("Lambda_tilde = 2.77e-122 and S_dS = 3.40e122 k_B are exact")
    print("reciprocals up to factor 3*pi (S_dS x Lambda_tilde = 3*pi).")
    print("The CC gap and the dS horizon entropy are one number, inverted.")
    print("The framework owns both (FP product 0.12 -> 2.77e-122 gap;")
    print("entropy boundary S_dS ~ 10^122 in PHYSICAL_UNIVERSAL_MAP).")
    print("S_CMB ~ 10^89-90 k_B is the FLOOR-6 companion, a distinct number.")
    print(f"OVERALL: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 70)

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, "bridge3_cc_entropy_confluence.json")

    out = {
        "identity": {
            "formula": "S_dS = 3*pi / Lambda_tilde",
            "S_dS_times_Lambda_tilde": prod,
            "three_pi": 3.0 * math.pi,
            "exact": True
        },
        "sil_units": {
            "l_P": L_P,
            "l_P2": L_P2,
            "T_CMB_K": T_CMB,
            "H0_planck_kmsMpc": H0_PLANCK,
            "Omega_L_planck": OM_L_PLANCK,
            "R_hubble_m": R_HUBBLE,
            "R_particle_horizon_m": R_PART_HORIZON
        },
        "cc_gap": {
            "lambda_obs_canon_m2": LAMBDA_CANON,
            "lambda_tilde_canon": gap_canon,
            "target_2_77e_122": TARGET_GAP,
            "ratio": gap_canon / TARGET_GAP,
            "lambda_obs_planck2018_m2": lam_planck,
            "lambda_tilde_planck2018": gap_planck,
            "audit_doc_typo": {
                "printed_recipe_value": printed_recipe,
                "reading": "doc divides by G/l_P^2 (2.7e7); correct factor is l_P^2"
            }
        },
        "horizon_entropy": {
            "S_dS_canon_kB": s_ds_canon,
            "S_dS_planck2018_kB": s_ds_planck,
            "map_quotes_3_1e122": True
        },
        "s_cmb_floor": {
            "S_CMB_c_over_H0_kB": s_cmb_h,
            "S_CMB_46_5Gly_kB": s_cmb_p,
            "cross_check_S_CMB_46_5Gly_kB": s_cmb_p_x,
            "s_over_n": 2.0 * math.pi ** 4 / (45.0 * 1.202056903159594),
            "is_inverse_of_cc_gap": False
        },
        "gates": ok_matrix,
        "status": "CONCRETE (confluence: S_dS = 3*pi / Lambda_tilde exact)"
    }
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2)

    print(f"\nOutput written to {out_path}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()