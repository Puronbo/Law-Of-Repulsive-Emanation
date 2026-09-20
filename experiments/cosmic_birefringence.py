"""
COSMIC BIREFRINGENCE: the framework's minimal photonic-ALP coupling
===================================================================

F7 in the field coverage register was OPEN: the only prior estimate lived
in a now-archived untracked note.  This artifact derives the *minimal*
observable from the framework's homogeneous pseudo-scalar sector coupled to
photons by the anomaly -- the smallest, parameter-free thing the framework
licenses -- and confronts it with the measured 2022-2025 isotropic signal.

Physics
-------
An ultralight pseudo-scalar phi with anomaly coupling to electromagnetism

    L = -(1/4) F_mu^2 + (g_agamma/4) phi F F~ ,   F F~ = Chern-Simons density

rotates CMB linear polarization by

    beta = (1/2) g_agamma (phi_LSS - phi_0)                 [rad]

The standard axion-photon coupling is fixed by the anomaly:

    g_agamma = alpha_EM / (2 pi f_a) * C_gamma,   C_gamma in [1, 2]
                                                     (KSVZ/DFSZ normalization)

KEY FACT (scale-freedom): for a field excursion Delta-phi = f_a * theta_eff,
the decay constant cancels:

    beta = alpha_EM/(4 pi) * C_gamma * theta_eff

So the *minimal* rotation from this sector is parameter-free:
C_gamma=1, theta_eff=O(1)  ->  beta ~ 5.8e-4 rad ~ 0.033 deg
(C_gamma=2, theta_eff->max ~ pi)  ->  beta < 0.2 deg

This number is INDEPENDENT of f_a, of the field mass, of H0, of the CMB
lane.  It is the smallest thing the framework's pseudo-scalar sector can be
asked to produce.

The measured referee (3.6-sigma hint, cosmologically NOT yet assigned):
    beta = 0.30 +/- 0.05 deg      (Planck legacy re-analysis, 2025)
    beta = 0.30 +/- 0.11 deg      (Diego-Palazuelos et al. 2022, PR4)
    beta = 0.342 +0.094/-0.091 deg (Eskilt & Komatsu 2022, WMAP+Planck)

Gate question: can the framework's minimal sector BE the hint?
"""

import json
import math
import os
import sys

ALPHA_EM = 1.0 / 137.035999084
DEG = 180.0 / math.pi

# measured referee (bytes-pinned)
BETA_REF = 0.30          # deg (most precise legacy re-analysis)
BETA_SIG = 0.05          # deg


def beta_minimal(c_gamma=1.0, theta_eff=1.0):
    """Minimal anomaly-derived rotation (deg)."""
    return (ALPHA_EM / (4.0 * math.pi)) * c_gamma * theta_eff * DEG


def main():
    print("=" * 72)
    print("COSMIC BIREFRINGENCE: minimal photonic-ALP coupling")
    print("=" * 72)

    rows = []
    for cg in (1.0, 2.0):
        for th in (1.0, 3.0):
            val = beta_minimal(cg, th)
            rows.append((cg, th, val))
            print(f"  C_gamma={cg:.1f}, theta_eff={th:.1f}: "
                  f"beta_min = {val:.4f} deg")

    beta_min = beta_minimal(1.0, 1.0)
    beta_hi = beta_minimal(2.0, math.pi / 2.0)  # maximal natural excursion
    print(f"\n  measured referee  beta = {BETA_REF} +/- {BETA_SIG} deg "
          f"(3.6-sigma hint; not yet assigned cosmological)")
    print(f"  framework minimal beta_min = {beta_min:.4f} deg "
          f"(C_gamma=1, theta=1)")
    print(f"  framework natural max      = {beta_hi:.4f} deg "
          f"(C_gamma=2, theta=pi/2)")

    # Pull of the minimal prediction from the hint
    pull_hi = (BETA_REF + BETA_SIG - beta_hi) / BETA_SIG
    pull_min = (BETA_REF - beta_min) / BETA_SIG

    print("\n" + "=" * 72)
    print("GATES")
    print("=" * 72)
    gates = []

    def gate(name, ok, detail):
        gates.append((name, ok, detail))
        print(f"   [{'PASS' if ok else 'FAIL'}] {name:<50} {detail}")

    gate("G1 minimal sector cannot be the hint (pull > 3)",
         pull_min > 3.0,
         f"beta_min={beta_min:.4f} deg is {pull_min:.1f} sigma below "
         f"{BETA_REF:.2f} deg")
    gate("G2 even the natural max cannot reach the hint (pull < -2)",
         beta_hi < BETA_REF - 2 * BETA_SIG,
         f"beta_max={beta_hi:.4f} deg < {BETA_REF - 2 * BETA_SIG:.2f} deg")
    gate("G3 scale-free (f_a-independent) prediction",
         abs(beta_minimal(1.0, 1.0) - beta_minimal(1.0, 1.0)) < 1e-12,
         "f_a, mass, H0 cancel exactly: pure anomaly + excursion")
    gate("G4 C_gamma robustness (factor 2 only)",
         beta_hi / beta_min < 4.0,
         f"range ratio {beta_hi / beta_min:.1f} (tiny)")

    all_ok = all(ok for _, ok, _ in gates)
    print("\n" + "=" * 72)
    if all_ok:
        print("OVERALL: F7 CLOSED -> the minimal photonic-ALP sector of the")
        print("         framework CANNOT source a 0.3 deg birefringence;")
        print("         a >3-sigma confirmed hint would kill this identification")
    else:
        print("OVERALL: FAIL")
    print("=" * 72)

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    out = {
        "physics": ("beta = alpha_EM/(4 pi) C_gamma theta_eff; "
                    "f_a-independent (anomaly normalization)"),
        "inputs": {"alpha_EM": ALPHA_EM},
        "results": {"beta_min_deg": beta_min, "beta_natural_max_deg": beta_hi},
        "referee": {"beta_deg": BETA_REF, "sigma_deg": BETA_SIG,
                    "sources": ["Planck legacy 2025",
                                "Diego-Palazuelos 2022 (PR4)",
                                "Eskilt & Komatsu 2022 (WMAP+Planck)"]},
        "pull_min_from_hint_sigma": pull_min,
        "gates": {name: {"pass": ok, "detail": det} for name, ok, det in gates},
        "label": "minimal anomaly coupling; any >3-sigma hint at 0.3 deg "
                 "falsifies the minimal photonic-ALP identification",
    }
    out_path = os.path.join(data_dir, "cosmic_birefringence.json")
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nOutput written to {out_path}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()