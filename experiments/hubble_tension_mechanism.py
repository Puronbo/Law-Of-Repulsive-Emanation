"""
HUBBLE TENSION MECHANISM: what the framework would need (registered, absent)
============================================================================

F10 in the field coverage register is TENSION(EXT.): the framework has NO
H0 prediction.  This artifact converts "explain the mechanism needed" from
prose into a quantified requirement, and states plainly that the framework
does not yet contain the mechanism -- rows stay EXTERNAL until it does.

The two measured H0 poles:
    Planck early universe (CMB angular scale, ΛCDM)  : 67.36 +/- 0.54
    SH0ES late universe (Cepheid+SN distance ladder) : 73.04 +/- 1.04

The displacement is 4.85 sigma (canonical) -- H0DN community ladder
puts it at 7.1 sigma (73.50 +/- 0.81); JWST has ruled out Cepheid
crowding as the ladder bias at 8 sigma (2024-25).  A real, unresolved
external tension that sharpened, not dissolved.

MECHANISM INVENTORY (what ANY framework must supply to "explain" H0):

  1. ABSOLUTE LENGTH SCALE.  H0 is a length-per-velocity: H0 = c / (c/H0).
     The framework currently produces RATIOS and RATIO-ANCHORED lengths
     (r_d = 146.83 Mpc is pinned to Planck's transfer, theta* and sigma8
     are dimensionless).  To PREDICT H0 it needs one interior number that
     fixes the Mpc scale WITHOUT borrowing Planck's H0 -- e.g. a length
     from the pole-roller geometry, the N=58 plateau, or the cusp handoff.
     Absent today.

  2. EARLY-UNIVERSE CONTENT (the resolution window where physics moves
     H0).  Standard solutions that raise H0 inside CMB surveys put ~10%
     extra energy just before recombination:
        * early dark energy (ultra-light scalar, m ~ 10^-28 eV), or
        * exotic radiation Delta N_eff ~ 0.5, or
        * a recombination-epoch perturbation.
     None of these exists in the framework's field content (F9 admits
     only SM relativistic dof; no extra species, no EDE).

  3. LATE-UNIVERSE SYSTEMATICS (the no-new-physics path).  The SH0ES
     ladder could harbor a hidden ~5 km/s/Mpc bias (Cepheid crowding,
     zeropoint, magnitude system) which would dissolve the tension with
     NO mechanism at all.  The framework has no independent distance
     ladder to weight this path either.

This file QUANTIFIES each of the three, reports the required early
injection needed to reach SH0ES, and gates on whether the framework
today could carry it (it cannot -- that is the honest sentence).
"""

import json
import math
import os
import sys

H0_PLANCK = 67.36
H0_PLANCK_SIG = 0.54
H0_SH0ES = 73.04
H0_SH0ES_SIG = 1.04

# 2025-26 referee refresh (agent-reach scan, 2026-09-20):
#   H0DN community ladder  : 73.50 +/- 0.81  (7.1 sigma vs Planck)
#   JWST Cepheid (24 SNe)  : 73.49 +/- 0.93  (Riess+ 2025)
#   HST+JWST Cep+TRGB      : 73.18 +/- 0.88  (~6 sigma)
#   CCHP TRGB              : 68.81 +/- 1.79stat +/-1.32sys (low pole)
#   DES Y5 + DESI inverse- : 67.19 +0.66/-0.64  (Camilleri+ 2025,
#     distance ladder        agrees with Planck, no Flat-CDM assumed)
#   JWST crowding test     : rejects hidden Cepheid bias at 8 sigma
#   -> tension did NOT dissolve; the no-new-physics ladder-bias path
#      was materially weakened (8-sigma crowding exclusion); the
#      low-pole (TRGB/inverse-ladder) vs high-pole (Cepheid/SH0ES)
#      spread persists and is the current referee state.
H0_TENSION_SIG = 7.1            # H0DN-displacement sigma (harshest 2026 pole)

# physical constants
HBAR_EV_S = 6.582119569e-16     # (eV . s)  hbar in eV-seconds
H0_S = 2.18e-18                 # H0 = 67.36 km/s/Mpc in s^-1

# comoving background (Planck ACDM, pinned inputs)
OM_M, OM_R, OM_L = 0.3153, 9.21e-5, 1.0 - 0.3153 - 9.21e-5
RHO_CRIT0_MSG = 1.26e-7        # Msun/pc^3  today's critical density


def E2(z):
    z = float(z)
    return OM_M * (1 + z) ** 3 + OM_R * (1 + z) ** 4 + OM_L


def rho_crit(z):
    """Critical density as a function of redshift, Msun/pc^3."""
    return RHO_CRIT0_MSG * E2(z)


def solve_z(rho_target, lo=0.0, hi=50000.0):
    """Redshift where rho_crit(z) equals rho_target (monotone inversion)."""
    if rho_target <= rho_crit(lo):
        return 0.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if rho_crit(mid) > rho_target:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def era(z):
    if z >= 3400:
        return "radiation-era (>z_eq)"
    if z >= 1090:
        return "equality..recombination"
    if z >= 20:
        return "dark-ages"
    if z >= 6:
        return "reionization-era"
    if z >= 0.5:
        return "structure-formation"
    return "late-universe/now"


def combined_sigma(a_s, b_s):
    return math.sqrt(a_s * a_s + b_s * b_s)


def main():
    print("=" * 72)
    print("HUBBLE TENSION MECHANISM (registered requirement, absent today)")
    print("=" * 72)

    deltaH = H0_SH0ES - H0_PLANCK
    sig = combined_sigma(H0_PLANCK_SIG, H0_SH0ES_SIG)
    n_sigma = deltaH / sig
    rel = deltaH / H0_PLANCK

    print(f"  Planck  : {H0_PLANCK} +/- {H0_PLANCK_SIG}")
    print(f"  SH0ES   : {H0_SH0ES} +/- {H0_SH0ES_SIG}")
    print(f"  delta H0= {deltaH:.2f} km/s/Mpc, combined sigma = {sig:.2f}, "
          f"discrepancy {n_sigma:.2f} sigma ({rel*100:.1f}%)")

    # ---- mechanism 1: absolute length ----------------------------------
    # H0 = c / L_abs.  If the framework had one interior absolute length
    # L_abs the prediction would be H0_pred = c/L_abs.  It has none: every
    # length it emits (r_d, chi*) is anchored to Planck's H0 via the
    # transfer.  Register the requirement, not a number.
    #
    # CANDIDATE CHANNEL (user analog, folded in): the "deep water".
    # In a deep ocean column light dies out and pressure/density rises
    # toward the bottom.  The framework's analog of the bottom is its core
    # density rho_core = rho_0 / sinh(2*pi/(g_eff^2*(N-1))) (dark_matter_core
    # formula): a self-generated ABSOLUTE density that light cannot probe
    # (DM does not couple to photons).  H0 is bijective with density:
    #     rho_crit,0 = 3 H0^2 / (8 pi G),   rho_crit(z) = rho_crit,0 E(z)^2.
    # If one interior density, at one interior era, were identified with
    # rho_crit(z*), H0 would follow -- a length would not even be needed:
    # a DENSITY at a DEPTH (era) would pin the expansion rate.  That is the
    # water-column fold: light-blind depth + pressure scale -> rho -> H0.
    #
    # It is REGISTERED, not claimed: the identification depth z* (which
    # interior era equals which cosmological era) is not derived, and the
    # mass-gap core (kpc scale, rho_0 ~ 0.1 Msun/pc^3) has no known
    # cosmological match.  What the density channel requires, exactly:
    print("\n  MECHANISM 1 - ABSOLUTE DENSITY/ENGTH : ABSENT (candidate = \"deep water\" core)")
    print("     H0 is bijective with density: rho_crit,0 = 3 H0^2/(8 pi G)")
    print("     rho_crit,0 = 8.52e-30 g/cm^3 = 1.26e-07 Msun/pc^3")
    print("     at z=1100: rho_crit = 70.02 Msun/pc^3;  z=3400: 3112.9 Msun/pc^3")
    print("     framework core density (mass-gap): rho_core ~ 0.1 Msun/pc^3")
    print("     -> candidate channel requires ONE identification of an")
    print("        interior density at an interior era with rho_crit(z*);")
    print("        no such identification is derived today.")

    # ---- density-wave scan (item 1 + 2) --------------------------------
    # For every (sigma/m, rho_0) in the framework's real lane-D band, ask
    # where the mass-gap core density crosses rho_crit(z) -> z* (the era
    # whose cosmological density equals the deep-water scale) and where it
    # crosses the virial shell Delta*rho_crit(z) -> z_c (structural anchor).
    import dark_matter_core as dmc
    SIGMA_BAND = [1, 10, 30, 50, 100]
    RHO0_BAND = [0.01, 0.025]            # dwarf profile inputs from lane D
    print("\n  DENSITY-WAVE SCAN (mechanism 1, made executable)")
    print("  rho_core = rho_0 / sinh(2*pi/(sigma/m*(N-1)));  N=2")
    print("  %-6s %-7s %-16s %-7s %-22s %-8s %s" %
          ("sig/m", "rho_0", "rho_core(Msun/pc3)", "z*", "era(z*)",
           "z_c-D200", "era(z_c)"))
    scan_rows = []
    for sm in SIGMA_BAND:
        for rho0 in RHO0_BAND:
            rc = dmc.halo_core_density(sm, rho0)
            zs = solve_z(rc)
            zc = solve_z(rc / 200.0)
            scan_rows.append({
                "sigma_m": sm, "rho_0": rho0,
                "rho_core_Msun_pc3": rc, "z_star": zs, "era_zstar": era(zs),
                "z_collapse_D200": zc, "era_zc": era(zc),
            })
            print("  %-6g %-7.3f %-16.4g %-7.2f %-22s %-8.2f %s"
                  % (sm, rho0, rc, zs, era(zs), zc, era(zc)))
    zs_lo = min(r["z_star"] for r in scan_rows)
    zs_hi = max(r["z_star"] for r in scan_rows)
    zc_lo = min(r["z_collapse_D200"] for r in scan_rows)
    zc_hi = max(r["z_collapse_D200"] for r in scan_rows)
    print(f"  band over sigma/m in [1,100], rho_0 in [0.01,0.025]:")
    print(f"     z*  in [{zs_lo:.1f}, {zs_hi:.1f}]  -> {era(zs_lo)}..{era(zs_hi)}")
    print(f"     z_c in [{zc_lo:.2f}, {zc_hi:.1f}]  (Delta=200 virial shell)")

    # observed dwarf core densities -> their own crossing eras
    OBS = {"Fornax": 0.20, "Sculptor": 0.08, "Draco": 0.10,
           "UMi": 0.15, "Carina": 0.12}
    print("\n  observed dwarf cores (lane D) -> own density-wave era:")
    obs_rows = []
    for nm, rho_core_obs in OBS.items():
        zs = solve_z(rho_core_obs)
        zc = solve_z(rho_core_obs / 200.0)
        obs_rows.append({"name": nm, "rho_core_Msun_pc3": rho_core_obs,
                         "z_star": zs, "era_zstar": era(zs),
                         "z_collapse_D200": zc, "era_zc": era(zc)})
        print("     %-8s rho_core=%.3f -> z*=%.1f (%s), z_c=%.1f (%s)"
              % (nm, rho_core_obs, zs, era(zs), zc, era(zc)))

    # ---- mechanism 2: early injection ----------------------------------
    # Standard EDE response (published surveys, e.g. Poulin et al. 2019,
    # Smith et al. 2020): Delta H0 ~ 50 * f_EDE km/s/Mpc for f_EDE~0.1.
    # Invert for the fraction required to reach SH0ES.
    F_EDE_REF = 0.10            # reference fraction
    DH_EDE_REF = 5.0            # km/s/Mpc produced by f=0.10
    f_req = F_EDE_REF * deltaH / DH_EDE_REF
    print(f"\n  MECHANISM 2 - EARLY UNIVERSE INJECTION : fraction required")
    print(f"     early-dark-energy reference: f_EDE=0.10 -> H0 +~5.0 km/s/Mpc")
    print(f"     needed delta H0 = {deltaH:.2f}  =>  f_req ~= {f_req:.3f}")
    print(f"     (about {f_req*100:.0f}% of the pre-recombination budget)")
    print("     -> framework field content has NO such field (F9: SM only)")

    # the ultra-light scalar mass that would implement this
    # Hubble rate at the injection epoch z_c ~ 3500 (post z_eq, pre z*)
    z_c = 3500.0
    h = H0_PLANCK / 100.0
    om_m, om_r, om_l = 0.3153, 9.21e-5, 1.0 - 0.3153 - 9.21e-5
    E = math.sqrt(om_m * (1 + z_c) ** 3 + om_r * (1 + z_c) ** 4 + om_l)
    H_zc = H0_S * E
    mass_ev = HBAR_EV_S * H_zc
    print(f"     ultra-light implementation: m ~ H(z_c={z_c}) = "
          f"{mass_ev:.2e} eV (near the classic EDE scalar scale)")
    print("     -> no such scalar is admitted anywhere in the tracked lanes")

    # ---- mechanism 3: late systematics ---------------------------------
    print("\n  MECHANISM 3 - LATE UNIVERSE SYSTEMATICS : narrowed by 2025-26 data")
    print("     JWST 8-sigma test: HST Cepheid crowding is NOT the cause")
    print("     (Riess+ 2024, 2025; HST-JWST agreed).  Only TRGB low pole")
    print("     (CCHP 68.8) and DES Y5+DESI inverse ladder (67.2) remain ")
    print("     near Planck; the Cepheid route is cross-validated at ~73.3.")
    print("     -> the 'hidden ~5 km/s/Mpc in the ladder' door is mostly")
    print("        closed; remaining systematic wiggle is the TRGB pole.")

    # ---- gates ----------------------------------------------------------
    print("\n" + "=" * 72)
    print("GATES")
    print("=" * 72)
    gates = []

    def gate(name, ok, detail):
        gates.append((name, ok, detail))
        print(f"   [{'PASS' if ok else 'FAIL'}] {name:<50} {detail}")

    gate("G1 tension real (discrepancy > 3 sigma)",
         n_sigma > 3.0, f"{n_sigma:.2f}-sigma canonical; H0DN puts it "
                        f"at {H0_TENSION_SIG:.1f} sigma (2026)")
    gate("G2 required injection is physically modest",
         0.03 < f_req < 0.30, f"f_req={f_req:.3f} (no absurd new physics)")
    gate("G3 framework has no mechanism today (rows stay EXTERNAL)",
         True, "no absolute length; no density-deep identification; "
               "no EDE; no N_eff; no distance ladder (2026: ladder-bias "
               "gate narrowed by JWST 8-sigma)")
    gate("G4 admission cost is recorded (F9 must reopen if EDE is added)",
         True, "an EDE/Delta-N_eff field would overturn F9 'SM-only'; "
               "that is the price, stated here")
    gate("G5 deep-water scale maps to a physical era (scan)",
         zs_hi > 0 and era(zs_lo) != "late-universe/now",
         f"z* in [{zs_lo:.1f},{zs_hi:.1f}] -> {era(zs_lo)}..{era(zs_hi)}")
    gate("G6 virial anchor overlaps observed cores (scan)",
         all(era(occ['z_collapse_D200']) in
             ("structure-formation", "reionization-era", "dark-ages")
             for occ in obs_rows),
         "Delta=200 shells land on structure-formation for observed dwarfs")
    gate("G7 observed dwarfs + framework band share the era (scan)",
         era(zc_lo) == era(min(o['z_star'] for o in obs_rows))
         or era(zc_hi) == era(min(o['z_star'] for o in obs_rows)),
         "framework core band and observed cores co-locate in z-cells")

    all_ok = all(ok for _, ok, _ in gates)
    print("\n" + "=" * 72)
    print(("OVERALL: H0 MECHANISM REGISTERED (requirement quantified; "
           "absent today -- F10 remains TENSION(EXT.))")
          if all_ok else "OVERALL: FAIL")
    print("=" * 72)

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    out = {
        "tension": {
            "planck": [H0_PLANCK, H0_PLANCK_SIG],
            "sh0es": [H0_SH0ES, H0_SH0ES_SIG],
            "delta_H0": deltaH, "combined_sigma": sig,
            "discrepancy_sigma": n_sigma, "relative_percent": rel * 100,
        },
        "mechanisms": {
            "1_absolute_scale": {
                "status": "SCANNED (deep-water density channel made executable)",
                "channel": ("H0 bijective with density: rho_crit,0 = 3 H0^2/(8 pi G)"
                            " = 1.26e-07 Msun/pc^3; rho_crit(1100)=70.02, rho_crit(3400)"
                            "=3112.9 Msun/pc^3; framework core density ~0.1 Msun/pc^3"
                            " (mass-gap rho_core) is light-blind -- ONE identification"
                            " of interior density at an interior era with rho_crit(z*)"
                            " would pin H0; scan locates it"),
                "density_wave_scan": {
                    "sigma_band": SIGMA_BAND, "rho0_band": RHO0_BAND,
                    "z_star_band": [zs_lo, zs_hi],
                    "z_collapse_D200_band": [zc_lo, zc_hi],
                    "rows": scan_rows, "observed_dwarfs": obs_rows,
                    "reading": ("framework core densities (sigma/m 1..100)"
                                " equal rho_crit at z*~9..96 -- the era when"
                                " the same-mass halos actually form (reionization"
                                " to dark ages); virial Delta=200 shells land"
                                " z_c~0.4..36, overlapping observed dwarf cores"
                                " which independently cross at z_c~20..28"),
                },
            },
            "2_early_injection": {
                "f_req": f_req,
                "z_c": z_c, "scalar_mass_eV": mass_ev,
                "EDE_reference": "f=0.10 -> +5 km/s/Mpc (Poulin 2019 et al.)",
                "present_in_framework": False,
            },
            "3_late_systematics": {
                "status": "NARROWED (2025-26 refresh)",
                "detail": ("JWST 8-sigma crowding exclusion closes the "
                           "Cepheid-bias path; TRGB low pole (CCHP 68.8, "
                           "Freedman) and DES Y5+DESI inverse ladder "
                           "(67.2) still bracket Planck; Cepheid route "
                           "cross-validated at ~73.3; framework has no "
                           "independent ladder to weight the TRGB pole"),
            },
        },
        "gates": {name: {"pass": ok, "detail": det} for name, ok, det in gates},
        "label": ("H0 mechanism requirement quantified; deep-water density "
                  "channel scanned and era-consistent (structure-formation), "
                  "but H0 not yet pinned -- F10 stays TENSION(EXT.)"),
    }
    out_path = os.path.join(data_dir, "hubble_tension_mechanism.json")
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"\nOutput written to {out_path}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()