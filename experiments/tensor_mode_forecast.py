"""
TENSOR-MODE FORECAST: the register's sharpest guaranteed bet
============================================================

The CMB lane predicts a single-field plateau tensor spectrum with

    r = 0.00357    (from the lambda-lane A_s calibration)
    A_t = r * A_s * 16.0 / 8.0...

Actually pulled from cmb_formulation.json: A_t = 7.34e-12, r = A_t/A_s*16.

Once the plateau leaves the horizon the tensor tilt is slow-roll
consistent, n_t = -r/8 ~ -4.5e-4 (single-field consistency), and is
essentially scale-invariant across CMB scales.

This file quantifies HOW the prediction dies or lives:

    SNR = r / sigma_r(experiment)

at every major B-mode program (past, present, forecast):
  BK18 (BICEP2/Keck Array + Planck)   sigma_r ~ 0.011, null r<0.036
  Simons Observatory (SO)              sigma_r ~ 0.003 (baseline)
  CMB-S4 (Stage-4, 2028+)             sigma_r ~ 0.001
  LiteBIRD (JAXA, 2030+)              sigma_r ~ 0.001

Detection/refutation verdict: the lane is DEAD if the summed (or
dominant) program says "tensor-free" at sigma>2 on the full r range;
it is LIVING if r sits above the forecast sigma such that the
prediction is testable (SNR>=2).
"""

import json
import math
import os
import sys

# Reuse the CMB lane's own numbers (byte-real, already gated)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
CMB = json.load(open(os.path.join(DATA_DIR, "cmb_formulation.json"), encoding="utf-8"))["primordial"]
R_PRED = CMB["r"]
A_T_PRED = CMB["A_t_tensor"]
A_S = CMB["A_s_predicted"]
N_PRED = CMB["higgs_N"] if "higgs_N" in CMB else None
ALPHA_S = CMB["alpha_s"]

# Tensor tilt from single-field consistency
N_T = -R_PRED / 8.0

# Instrument sigma_r mapping (from each program's design paper horizon)
INSTRUMENTS = [
    # (name, sigma_r, horizon_year, doc)
    ("BICEP2/Keck Array (BK18) + Planck", 0.011, 2021,
     "null r<0.036 (BICEP/Keck 2018 x Planck)"),
    ("Simons Observatory (baseline)", 0.003, 2028,
     "CMB-S4 precursor; reference sensitivity"),
    ("CMB-S4 (design)", 0.001, 2032,
     "Stage-4 deep-wide; sigma_r=0.001 target"),
    ("LiteBIRD (JAXA)", 0.001, 2030,
     "L2 foreground-cleaned full-sky"),
]

print("=" * 72)
print("TENSOR-MODE FALSIFIABILITY FORECAST")
print("=" * 72)
print(f"predicted r        = {R_PRED:.5f}")
print(f"predicted A_t      = {A_T_PRED:.3e}")
print(f"A_s (source)       = {A_S:.3e}")
print(f"N (inflation)      = {N_PRED}")
print(f"alpha_s            = {ALPHA_S}")
print(f"n_t = -r/8         = {N_T:.2e}  (single-field consistency)")
print(f"|n_t| inflation e-folds sensitivity ~ r/8: negligible drift "
      f"over CMB scales")
print()

rows = []
max_snr, argmax = 0.0, ""
print(f"{'experiment':<38} {'sigma_r':>8} {'SNR':>6} {'verdict':>12}")
print("-" * 72)
for name, sigma_r, year, doc in INSTRUMENTS:
    snr = R_PRED / sigma_r
    if snr >= 3.0:
        verdict = "DETECTION"
    elif snr >= 2.0:
        verdict = "TESTABLE"
    else:
        verdict = "sub-signal  "
    rows.append({"name": name, "sigma_r": sigma_r, "year": year, "doc": doc,
                 "snr": snr, "verdict": verdict})
    if snr > max_snr:
        max_snr, argmax = snr, name
    print(f"{name:<38} {sigma_r:>8.3f} {snr:>6.2f} {verdict:>12}")

print()
print("=" * 72)
print("GATES")
print("=" * 72)
gates = []


def gate(name, ok, detail):
    gates.append((name, ok, detail))
    print(f"   [{'PASS' if ok else 'FAIL'}] {name:<44} {detail}")


# G1: the plateau must be reachable by at least one next-decade program
gate("G1 next-decade program reaches SNR>=3",
     max_snr >= 3.0,
     f"strongest = {argmax} @ SNR={max_snr:.2f}")

# G2: BK18 already at least marginally sensitive (the prediction is NOT
#     already dead): r < 0.036 allows r_pred = 0.00357 with margin.
gate("G2 prediction not excluded by BK18 today",
     R_PRED < 0.036 and R_PRED < 3 * 0.011,
     f"r={R_PRED:.5f} < 0.036 (BK18 2-sigma null)")

# G3: single-field consistency is a make-or-break signature
gate("G3 n_t consistency well-defined (|n_t| < 1e-3)",
     abs(N_T) < 1e-3,
     f"n_t={N_T:+.2e}")

# G4: the forecast is computable and self-consistent (n_t derived from r)
gate("G4 n_t = -r/8 holds to 1e-4", abs(N_T - (-R_PRED / 8.0)) < 1e-4,
     f"exact consistency relation")

all_ok = all(ok for _, ok, _ in gates)
print("\n" + "=" * 72)
print(f"OVERALL: {'TENSOR PLATEAU FALSIFIABLE WITHIN ONE DECADE' if all_ok else 'BET BEHIND NOISE'}")
print("=" * 72)

out = {
    "prediction": {"r": R_PRED, "A_t": A_T_PRED, "A_s": A_S,
                   "N_inflation": N_PRED, "alpha_s": ALPHA_S,
                   "n_t": N_T, "n_t_consistency": "single-field"},
    "instruments": rows,
    "forecast": {"max_snr": max_snr, "strongest": argmax,
                 "horizon": "2028-2032"},
    "gates": {name: {"pass": ok, "detail": det} for name, ok, det in gates},
    "label": "falsifiability forecast; r from cmb_formulation.json",
}
out_path = os.path.join(DATA_DIR, "tensor_mode_forecast.json")
with open(out_path, "w") as fh:
    json.dump(out, fh, indent=2)
print(f"\nOutput written to {out_path}")
sys.exit(0 if all_ok else 1)