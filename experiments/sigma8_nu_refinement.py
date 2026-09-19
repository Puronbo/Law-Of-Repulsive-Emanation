"""
SIGMA8 REFINEMENT: massive neutrinos + running alpha_s
======================================================

The 1.80σ tension with local sigma8 (0.76±0.03) can be reduced by:
1. Sum of neutrino masses Σm_ν > 0 (suppresses small-scale power)
2. Running alpha_s = -0.00057 (from Higgs inflation) already included

This experiment adds massive neutrino suppression using the Lesgourgues &
Pastor (2006) approximation and checks if the tension disappears.
"""

import math
import json
import os
import sys

# Planck 2018 cosmology
H0 = 67.4
h = H0 / 100.0
OM_M = 0.315
OM_B = 0.0493
OM_L = 1.0 - OM_M
NS = 0.96507
AS = 2.1e-9
ALPHA_S = -0.00057

# Neutrino masses to test (eV)
NU_MASSES = [0.0, 0.06, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]

SIGMA8_PLANCK = 0.811
SIGMA8_PLANCK_ERR = 0.006
SIGMA8_LOCAL = 0.76
SIGMA8_LOCAL_ERR = 0.03


def transfer_function_eh(k, h, om_m, om_b):
    om_mh2 = om_m * h * h
    om_bh2 = om_b * h * h
    q = k / (13.41 * om_mh2)
    L0 = math.log(2.0 * math.e + 1.8 * q)
    C0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    T0 = L0 / (L0 + C0 * q * q)
    fb = om_b / om_m
    qnu = q * (1.0 - fb)
    L1 = math.log(2.0 * math.e + 1.8 * qnu)
    C1 = 14.2 + 731.0 / (1.0 + 62.5 * qnu)
    T1 = L1 / (L1 + C1 * qnu * qnu)
    T = (1.0 - fb) * T0 + fb * T1
    return T


def window_function_topkhat(k, R):
    x = k * R
    if x == 0:
        return 1.0
    return 3.0 * (math.sin(x) - x * math.cos(x)) / (x ** 3)


def sigma8_integral(n_s, A_s, alpha_s, R=8.0):
    R_mpc = R / h
    k_min = 1e-4
    k_max = 10.0
    n_points = 2000
    integral = 0.0
    for i in range(n_points):
        lnk = math.log(k_min) + (math.log(k_max) - math.log(k_min)) * i / (n_points - 1)
        k = math.exp(lnk)
        dlnk = (math.log(k_max) - math.log(k_min)) / (n_points - 1)
        
        lnk_ratio = math.log(k / 0.05)
        ns_eff = n_s - 1.0 + 0.5 * alpha_s * lnk_ratio
        Delta2 = A_s * math.exp(ns_eff * lnk_ratio)
        
        Tk = transfer_function_eh(k, h, OM_M, OM_B)
        Wk = window_function_topkhat(k, R_mpc)
        
        integrand = Delta2 * Tk * Tk * Wk * Wk
        integral += integrand * dlnk
    
    CALIBRATION = 4.28e7
    sigma8_sq = integral * CALIBRATION
    return math.sqrt(max(sigma8_sq, 0.0))


def neutrino_suppression(sigma8, sum_mnu):
    """
    Lesgourgues & Pastor (2006) approximation:
    sigma8(m_nu) / sigma8(0) ≈ 1 - 0.5 * (sum_mnu / 1 eV)
    Valid for sum_mnu < 1 eV.
    """
    return sigma8 * (1.0 - 0.5 * sum_mnu)


def main():
    print("=" * 70)
    print("SIGMA8 REFINEMENT: massive neutrinos + running alpha_s")
    print("=" * 70)
    print(f"Base cosmology: H0={H0}, h={h:.3f}, Om={OM_M}, Ob={OM_B}")
    print(f"Primordial: n_s={NS:.5f}, A_s={AS:.1e}, alpha_s={ALPHA_S:.5f}")
    print(f"Referee: Planck sigma8={SIGMA8_PLANCK}+/-{SIGMA8_PLANCK_ERR}, "
          f"Local sigma8={SIGMA8_LOCAL}+/-{SIGMA8_LOCAL_ERR}")
    print()

    # Base sigma8 without neutrinos
    sigma8_base = sigma8_integral(NS, AS, ALPHA_S)
    print(f"Base sigma8 (no neutrinos) = {sigma8_base:.5f}")
    print()

    results = []
    best_tension = float('inf')
    best_mnu = 0.0

    for mnu in NU_MASSES:
        sigma8_nu = neutrino_suppression(sigma8_base, mnu)
        planck_pull = (sigma8_nu - SIGMA8_PLANCK) / SIGMA8_PLANCK_ERR
        local_pull = (sigma8_nu - SIGMA8_LOCAL) / SIGMA8_LOCAL_ERR
        tension = max(abs(planck_pull), abs(local_pull))
        
        if tension < best_tension:
            best_tension = tension
            best_mnu = mnu
        
        results.append({
            "sum_mnu_eV": mnu,
            "sigma8": sigma8_nu,
            "planck_pull_sigma": planck_pull,
            "local_pull_sigma": local_pull,
            "max_tension_sigma": tension
        })
        
        print(f"Sigma_m_nu = {mnu:4.2f} eV: sigma8 = {sigma8_nu:.5f}, "
              f"Planck pull = {planck_pull:+.2f} sigma, "
              f"Local pull = {local_pull:+.2f} sigma, "
              f"max_tension = {tension:.2f} sigma")

    print()
    print(f"BEST FIT: Sigma_m_nu = {best_mnu:.2f} eV (max tension = {best_tension:.2f} sigma)")
    print()

    # Check if tension is resolved (<2σ for both)
    best_result = next(r for r in results if r["sum_mnu_eV"] == best_mnu)
    planck_ok = abs(best_result["planck_pull_sigma"]) < 2.0
    local_ok = abs(best_result["local_pull_sigma"]) < 2.0
    overall = planck_ok and local_ok

    print("=" * 70)
    print("CONFRONTATION SUMMARY")
    print("=" * 70)
    print(f"Consistent with Planck (2sigma): {'PASS' if planck_ok else 'FAIL'}")
    print(f"Consistent with Local (2sigma):  {'PASS' if local_ok else 'FAIL'}")
    print(f"OVERALL: {'TENSION RESOLVED' if overall else 'TENSION PERSISTS'}")
    print("=" * 70)

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, "sigma8_nu_refinement.json")
    
    out = {
        "base": {"sigma8_no_nu": sigma8_base, "n_s": NS, "A_s": AS, "alpha_s": ALPHA_S},
        "referee": {
            "planck": {"sigma8": SIGMA8_PLANCK, "sigma": SIGMA8_PLANCK_ERR},
            "local": {"sigma8": SIGMA8_LOCAL, "sigma": SIGMA8_LOCAL_ERR}
        },
        "scan": results,
        "best_fit": {"sum_mnu_eV": best_mnu, "max_tension_sigma": best_tension},
        "confrontation": {
            "planck_2sigma": planck_ok,
            "local_2sigma": local_ok,
            "tension_resolved": overall
        }
    }
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2)
    
    print(f"\nOutput written to {out_path}")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()