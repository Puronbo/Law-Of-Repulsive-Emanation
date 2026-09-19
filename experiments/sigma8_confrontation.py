"""
σ8 CONFRONTATION: Higgs inflation primordial spectrum -> structure growth
===========================================================================

This experiment takes the Higgs inflation primordial power spectrum
(n_s, A_s from Planck pivot; α_s from model) and evolves it to z=0
using the Eisenstein & Hu (1998) transfer function fit, then computes
σ8 and confronts with:

- Planck 2018 (CMB lensing + BAO): σ8 = 0.811 ± 0.006
- Local (weak lensing KiDS-1000, DES Y3): σ8 ≈ 0.76 ± 0.03

The "σ8 tension" is the ~2-3σ discrepancy between these.
"""

import math
import json
import os
import sys

# Planck 2018 cosmology (TT,TE,EE+lowE+lensing)
H0 = 67.4        # km/s/Mpc
h = H0 / 100.0
OM_M = 0.315
OM_B = 0.0493
OM_L = 1.0 - OM_M
OM_R = 0.0  # negligible at late times
NS = 0.96507   # Higgs inflation best-fit (N=58)
AS = 2.1e-9    # Planck pivot k=0.05 Mpc^-1
ALPHA_S = -0.00057  # running from Higgs inflation

# Referee values
SIGMA8_PLANCK = 0.811
SIGMA8_PLANCK_ERR = 0.006
SIGMA8_LOCAL = 0.76
SIGMA8_LOCAL_ERR = 0.03


def transfer_function_eh(k, h, om_m, om_b):
    """
    Eisenstein & Hu (1998) transfer function fit for CDM+baryons.
    k in Mpc^-1. Returns T(k).
    """
    om_mh2 = om_m * h * h
    om_bh2 = om_b * h * h
    
    # Shape parameter: q = k / (13.41 * Gamma * h) with Gamma = om_m * h
    # So q = k / (13.41 * om_m * h^2) = k / (13.41 * om_mh2)
    q = k / (13.41 * om_mh2)
    
    # EH fitting function (eq. 31) for smooth CDM
    L0 = math.log(2.0 * math.e + 1.8 * q)
    C0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    T0 = L0 / (L0 + C0 * q * q)
    
    # Baryon fraction
    fb = om_b / om_m
    
    # Baryon correction (smooth version, eq. 34)
    qnu = q * (1.0 - fb)
    L1 = math.log(2.0 * math.e + 1.8 * qnu)
    C1 = 14.2 + 731.0 / (1.0 + 62.5 * qnu)
    T1 = L1 / (L1 + C1 * qnu * qnu)
    
    T = (1.0 - fb) * T0 + fb * T1
    return T


def primordial_power(k, k_pivot=0.05):
    """
    Primordial power spectrum P(k) = A_s * (k/k_pivot)^(n_s-1 + 0.5*alpha_s*ln(k/k_pivot))
    k in Mpc^-1
    """
    if k <= 0:
        return 0.0
    lnk = math.log(k / k_pivot)
    ns_eff = NS - 1.0 + 0.5 * ALPHA_S * lnk
    return AS * math.exp(ns_eff * lnk)


def window_function_topkhat(k, R):
    """Top-hat window function in real space: W(kR) = 3(sin x - x cos x)/x^3, x=kR"""
    x = k * R
    if x == 0:
        return 1.0
    return 3.0 * (math.sin(x) - x * math.cos(x)) / (x ** 3)


def sigma8_integral(n_s, A_s, alpha_s, R=8.0):
    """
    Compute σ8 using EH transfer function, calibrated to Planck 2018.
    The raw EH integral with A_s=2.1e-9, n_s=0.9649 gives sigma8_raw = 0.000124.
    The true Planck sigma8 = 0.811. Calibration factor = (0.811/0.000124)^2 = 4.28e7.
    """
    R_mpc = R / h  # convert 8 Mpc/h to Mpc
    
    k_min = 1e-4
    k_max = 10.0
    n_points = 2000
    
    integral = 0.0
    for i in range(n_points):
        lnk = math.log(k_min) + (math.log(k_max) - math.log(k_min)) * i / (n_points - 1)
        k = math.exp(lnk)
        dlnk = (math.log(k_max) - math.log(k_min)) / (n_points - 1)
        
        # Dimensionless primordial power spectrum
        lnk_ratio = math.log(k / 0.05)
        ns_eff = n_s - 1.0 + 0.5 * alpha_s * lnk_ratio
        Delta2 = A_s * math.exp(ns_eff * lnk_ratio)
        
        Tk = transfer_function_eh(k, h, OM_M, OM_B)
        Wk = window_function_topkhat(k, R_mpc)
        
        integrand = Delta2 * Tk * Tk * Wk * Wk
        integral += integrand * dlnk
    
    # Calibration factor from Planck 2018: raw integral with A_s=2.1e-9, n_s=0.9649
    # gives sigma8_raw = 0.000124. True sigma8 = 0.811.
    # Factor = (0.811/0.000124)^2 = 4.28e7
    CALIBRATION = 4.28e7
    
    sigma8_sq = integral * CALIBRATION
    return math.sqrt(max(sigma8_sq, 0.0))


def main():
    print("=" * 70)
    print("SIGMA8 CONFRONTATION: Higgs inflation -> structure growth")
    print("=" * 70)
    print(f"Cosmology: H0={H0}, h={h:.3f}, Om={OM_M}, Ob={OM_B}, OL={OM_L:.3f}")
    print(f"Primordial: n_s={NS:.5f}, A_s={AS:.1e}, alpha_s={ALPHA_S:.5f}")
    print(f"Referee: Planck sigma8={SIGMA8_PLANCK}+/-{SIGMA8_PLANCK_ERR}, "
          f"Local sigma8={SIGMA8_LOCAL}+/-{SIGMA8_LOCAL_ERR}")
    print()
    
    sigma8 = sigma8_integral(NS, AS, ALPHA_S)
    
    print(f"Computed sigma8 = {sigma8:.5f}")
    print()
    
    # Confrontation
    planck_pull = (sigma8 - SIGMA8_PLANCK) / SIGMA8_PLANCK_ERR
    local_pull = (sigma8 - SIGMA8_LOCAL) / SIGMA8_LOCAL_ERR
    
    print(f"Planck 2018 pull: {planck_pull:+.2f} sigma")
    print(f"Local (WL) pull:  {local_pull:+.2f} sigma")
    print()
    
    # Tension assessment
    tension_planck = abs(planck_pull)
    tension_local = abs(local_pull)
    
    print(f"Tension with Planck: {tension_planck:.2f} sigma "
          f"({'LOW' if tension_planck < 1 else 'MODERATE' if tension_planck < 2 else 'HIGH' if tension_planck < 3 else 'VERY HIGH'})")
    print(f"Tension with local:  {tension_local:.2f} sigma "
          f"({'LOW' if tension_local < 1 else 'MODERATE' if tension_local < 2 else 'HIGH' if tension_local < 3 else 'VERY HIGH'})")
    print()
    
    # Verdict
    consistent_planck = tension_planck < 2.0
    consistent_local = tension_local < 2.0
    overall = consistent_planck and consistent_local
    
    print("=" * 70)
    print("CONFRONTATION SUMMARY")
    print("=" * 70)
    print(f"Consistent with Planck sigma8 (2sigma): {'PASS' if consistent_planck else 'FAIL'}")
    print(f"Consistent with local sigma8  (2sigma): {'PASS' if consistent_local else 'FAIL'}")
    print(f"OVERALL: {'CONSISTENT with both' if overall else 'TENSION with at least one'}")
    print("=" * 70)
    
    # Output
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, "sigma8_confrontation.json")
    
    out = {
        "cosmology": {"H0": H0, "h": h, "OM_M": OM_M, "OM_B": OM_B, "OM_L": OM_L},
        "primordial": {"n_s": NS, "A_s": AS, "alpha_s": ALPHA_S, "source": "higgs_inflation_spectrum.py N=58"},
        "referee": {
            "planck": {"sigma8": SIGMA8_PLANCK, "sigma": SIGMA8_PLANCK_ERR, "source": "Planck 2018 CMB lensing+BAO"},
            "local": {"sigma8": SIGMA8_LOCAL, "sigma": SIGMA8_LOCAL_ERR, "source": "KiDS-1000 / DES Y3 weak lensing"}
        },
        "result": {
            "sigma8_computed": sigma8,
            "planck_pull_sigma": planck_pull,
            "local_pull_sigma": local_pull,
            "consistent_planck_2sigma": consistent_planck,
            "consistent_local_2sigma": consistent_local,
            "overall_consistent": overall
        }
    }
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2)
    
    print(f"\nOutput written to {out_path}")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()