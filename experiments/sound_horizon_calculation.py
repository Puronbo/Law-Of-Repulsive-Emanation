"""
SOUND HORIZON CALCULATION: close the INPUT anchor row (F11)
============================================================

The sigma8 pipeline consumes the BAO sound horizon r_drag as an
internally calibrated anchor (Planck 147.09 +/- 0.26 Mpc) but never
recomputes it.  This experiment closes that INPUT row with the standard
cosmology integral (first-principles sound speed, Hubble evolution),
the same physics family the Eisenstein-Hu transfer uses:

    r_s(zc) = (c/H0) * int_zc^inf  c_s(z)/c * dz / E(z)
    c_s(z)/c = 1 / sqrt(3 (1 + R(z))) ,  R(z) = 3 rho_b/(4 rho_g)   (1+z)^-1
    E(z)^2   = Om_m (1+z)^3 + Om_r (1+z)^4 + Om_L

Inputs are pinned Planck 2018 (TT,TE,EE+lowE+lensing) values; the
cutoffs z* (recombination, 1090) and z_d (drag, 1060) are empirical
anchors on the SAME footing as T_CMB.  The derived numbers are the
pipeline's own cross-check of its distance anchor.

Verify:
    r_s(1090) ~ 144-145 Mpc   (recombination sound horizon)
    r_s(1060) ~ 147 Mpc       (drag sound horizon)   [Planck 147.09 +/- 0.26]
"""

import json
import math
import os
import sys

# Planck 2018 cosmology (TT,TE,EE+lowE+lensing)
H0 = 67.36
h = H0 / 100.0
OM_M = 0.3153
OM_B_H2 = 0.02237
OM_G_H2 = 2.469e-5        # photon density fraction * h^2
N_EFF = 3.044
OM_R_H2 = OM_G_H2 * (1.0 + 0.2271 * N_EFF)   # radiation incl. neutrinos

C_KMPS = 299792.458        # km/s
C_OVER_H0 = C_KMPS / (100.0 * h)   # Mpc

Z_RECOMB = 1090.0          # last-scattering anchor
Z_DRAG = 1060.0            # baryon-drag anchor
R_DRAG_REF, R_DRAG_ERR = 147.09, 0.26   # Planck
R_STAR_REF = 144.5         # literature recombination sound horizon (~144-145)


def E2(z):
    om_b = OM_B_H2 / (h * h)
    om_r = OM_R_H2 / (h * h)
    om_l = 1.0 - OM_M - om_r
    return OM_M * (1 + z) ** 3 + om_r * (1 + z) ** 4 + om_l


def R(z):
    # 3 rho_b/(4 rho_g) = (3/4) (Om_b/Om_g) / (1+z)
    return (3.0 / 4.0) * (OM_B_H2 / OM_G_H2) / (1.0 + z)


def sound_horizon(z_cut, z_max=2.0e6, n=80000):
    """r_s in Mpc: trapezoid integral of c_s/c / E from z_cut to z_max
    (the wave traveled from deep in the radiation era DOWN to z_cut)."""
    lo = max(z_cut, 1e-4)
    dz = (z_max - lo) / n
    s = 0.0
    for i in range(n):
        za = lo + i * dz
        zb = za + dz
        fa = 1.0 / math.sqrt(3.0 * (1.0 + R(za))) / math.sqrt(E2(za))
        fb = 1.0 / math.sqrt(3.0 * (1.0 + R(zb))) / math.sqrt(E2(zb))
        s += 0.5 * (fa + fb) * dz
    return C_OVER_H0 * s


def main():
    print("=" * 72)
    print("SOUND HORIZON / BAO ANCHOR: sigma8 pipeline self-check")
    print("=" * 72)
    print(f"Planck: H0={H0}, Om_m={OM_M}, Om_b h^2={OM_B_H2}, "
          f"Om_r h^2={OM_R_H2:.4e}")
    print(f"cutoffs: z* = {Z_RECOMB} (recomb), z_d = {Z_DRAG} (drag)")

    r_star = sound_horizon(Z_RECOMB)
    r_drag = sound_horizon(Z_DRAG)
    print(f"\nr_s(recombination, z={Z_RECOMB}) = {r_star:.2f} Mpc   "
          f"(literature ~ {R_STAR_REF})")
    print(f"r_drag(z={Z_DRAG})                 = {r_drag:.2f} Mpc   "
          f"(Planck {R_DRAG_REF} +/- {R_DRAG_ERR})")

    # sample table
    print("\ncutoff-table (z_cut : r_s Mpc)  [horizon shrinks as cut raises]:")
    for zc in (500, 1000, 1060, 1090, 1200):
        print(f"   z_cut={zc:<5} r_s = {sound_horizon(zc):.2f} Mpc")

    # gates ------------------------------------------------------------
    print("\n" + "=" * 72)
    print("GATES")
    print("=" * 72)
    gates = []
    def gate(name, ok, detail):
        gates.append((name, ok, detail))
        print(f"   [{'PASS' if ok else 'FAIL'}] {name:<40} {detail}")

    gate("G1 r_drag within 2% of Planck", abs(r_drag - R_DRAG_REF) / R_DRAG_REF < 0.02,
         f"r_drag={r_drag:.2f} vs {R_DRAG_REF} ({(r_drag-R_DRAG_REF):+.2f} Mpc)")
    gate("G2 r_star within 5% of literature", abs(r_star - R_STAR_REF) / R_STAR_REF < 0.05,
         f"r_star={r_star:.2f} vs ~{R_STAR_REF}")
    gate("G3 monotone in z", r_drag > r_star > sound_horizon(1200.0),
         "sound horizon shrinks as the cutoff (z_cut) rises")

    all_ok = all(ok for _, ok, _ in gates)
    print("\n" + "=" * 72)
    print(f"OVERALL: {'ANCHOR RECOMPUTED, PIPELINE CONSISTENT' if all_ok else 'DRIFT'}")
    print("=" * 72)

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    out = {
        "inputs": {"H0": H0, "Om_m": OM_M, "Om_b_h2": OM_B_H2,
                   "Om_r_h2": OM_R_H2, "N_eff": N_EFF},
        "anchors": {"z_recomb": Z_RECOMB, "z_drag": Z_DRAG,
                    "r_drag_planck": R_DRAG_REF},
        "results": {
            "r_star_Mpc": r_star, "r_drag_Mpc": r_drag,
            "pull_vs_planck_sigma": (r_drag - R_DRAG_REF) / R_DRAG_ERR
        },
        "gates": {name: {"pass": ok, "detail": det} for name, ok, det in gates},
        "label": "standard-cosmology recomputation; anchors are empirical"
    }
    out_path = os.path.join(data_dir, "sound_horizon_calculation.json")
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nOutput written to {out_path}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()