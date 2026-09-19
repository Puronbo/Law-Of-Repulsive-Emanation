"""
HIGGS INFLATION SPECTRUM (Bezrukov-Shaposhnikov 2008 non-minimal coupling)
===========================================================================

The framework adopts an explicit Higgs-inflaton sector for the e-folds
(the pure-gravity flow only supplies the initial scale at the NGFP).
This experiment computes the testable CMB predictions and confronts them
with the pinned n_s/r referee (Planck 2018 + BK18).

Standard Higgs inflation with non-minimal coupling xi:
  Jordan frame:  L = sqrt(-g) [ (M_pl^2/2 + xi h^2) R + ... ]
  Einstein frame: canonically normalized field chi, potential
    V(chi) = (lambda/4) * (M_pl/xi)^4 * (1 - exp(-2*chi/(sqrt(6) M_pl)))^2
  Large-field plateau: V ~ V0 (1 - 2 exp(-2*chi/(sqrt(6) M_pl)) + ...)

Slow-roll on the plateau (chi >> M_pl):
  epsilon = 4/3 * exp(-4*chi/(sqrt(6) M_pl))
  eta = -4/3 * exp(-2*chi/(sqrt(6) M_pl))

Number of e-folds before end of inflation:
  N = (3/4) * exp(2*chi/(sqrt(6) M_pl))  =>  exp(-2*chi/(sqrt(6) M_pl)) = 4/(3N)

Predictions at horizon exit (N ~ 50-60):
  epsilon = 3/(4N^2)
  eta = -1/N
  n_s = 1 - 6*epsilon + 2*eta = 1 - 2/N - 3/(2N^2)
  r = 16*epsilon = 12/N^2
  alpha_s = d n_s / d ln k = 16*epsilon*eta - 24*epsilon^2 - 2*xi^2
           = -2/N^2 + 9/(2N^3)  (subleading; approx -2/N^2)

Planck 2018 (TT,TE,EE+lowE+lensing):  n_s = 0.9649 +/- 0.0042 (68% CL)
BICEP/Keck 2018 (BK18):  r < 0.036 (95% CL, pivot k=0.05 Mpc^-1)
Planck 2018:  alpha_s = -0.0045 +/- 0.0067 (68% CL)
"""

import math
import json
import os
import sys

# Pinned referee values
NS_CENTRAL = 0.9649
NS_SIGMA = 0.0042
R_UPPER_95 = 0.036  # BK18 95% CL
ALPHAS_CENTRAL = -0.0045
ALPHAS_SIGMA = 0.0067


def higgs_predictions(N):
    """Return (n_s, r, alpha_s) for given e-fold N."""
    n_s = 1.0 - 2.0/N - 1.5/(N*N)
    r = 12.0/(N*N)
    alpha_s = -2.0/(N*N) + 4.5/(N*N*N)
    return n_s, r, alpha_s


def chi2(N):
    """Chi^2 against Planck 2018 + BK18 (Gaussian approx for n_s, alpha_s; r upper limit)."""
    n_s, r, alpha_s = higgs_predictions(N)
    # n_s: Gaussian
    chi2_ns = ((n_s - NS_CENTRAL) / NS_SIGMA) ** 2
    # r: one-sided; if r < R_upper, contributes 0; else penalty
    if r <= R_UPPER_95:
        chi2_r = 0.0
    else:
        # approximate: treat 95% CL upper limit as 2-sigma bound
        chi2_r = ((r - R_UPPER_95) / (R_UPPER_95/2.0)) ** 2
    # alpha_s: Gaussian
    chi2_as = ((alpha_s - ALPHAS_CENTRAL) / ALPHAS_SIGMA) ** 2
    return chi2_ns + chi2_r + chi2_as


def main():
    print("=" * 70)
    print("HIGGS INFLATION SPECTRUM vs PLANCK/BK18 REFEREE")
    print("=" * 70)
    print(f"Referee: n_s = {NS_CENTRAL} +/- {NS_SIGMA} (Planck 2018)")
    print(f"         r < {R_UPPER_95} (BK18 95% CL)")
    print(f"         alpha_s = {ALPHAS_CENTRAL} +/- {ALPHAS_SIGMA} (Planck 2018)")
    print()

    results = []
    best_N = None
    best_chi2 = float('inf')

    for N in [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]:
        n_s, r, alpha_s = higgs_predictions(N)
        c2 = chi2(N)
        n_s_sigma = (n_s - NS_CENTRAL) / NS_SIGMA
        r_ok = r <= R_UPPER_95
        as_sigma = (alpha_s - ALPHAS_CENTRAL) / ALPHAS_SIGMA
        results.append({
            "N": N, "n_s": n_s, "r": r, "alpha_s": alpha_s,
            "chi2": c2, "n_s_sigma": n_s_sigma, "alpha_s_sigma": as_sigma,
            "r_ok": r_ok
        })
        marker = "  <-- BEST" if c2 < best_chi2 else ""
        if c2 < best_chi2:
            best_chi2 = c2
            best_N = N
        print(f"N={N:2d}: n_s={n_s:.5f} ({n_s_sigma:+.2f} sigma), "
              f"r={r:.5f} {'OK' if r_ok else 'FAIL'}, "
              f"alpha_s={alpha_s:.5f} ({as_sigma:+.2f} sigma), "
              f"chi2={c2:.3f}{marker}")

    print()
    print(f"Best fit: N = {best_N} (chi^2 = {best_chi2:.3f})")
    n_s, r, alpha_s = higgs_predictions(best_N)
    print(f"  n_s = {n_s:.5f}  (Planck: {NS_CENTRAL} +/- {NS_SIGMA})")
    print(f"  r   = {r:.5f}  (BK18: < {R_UPPER_95})")
    print(f"  alpha_s = {alpha_s:.5f}  (Planck: {ALPHAS_CENTRAL} +/- {ALPHAS_SIGMA})")

    # Confrontation summary
    print("\n" + "=" * 70)
    print("CONFRONTATION")
    print("=" * 70)
    best = results[best_N - 50]
    n_s_ok = abs(best["n_s_sigma"]) < 2.0  # within 2-sigma
    r_ok = best["r_ok"]
    as_ok = abs(best["alpha_s_sigma"]) < 2.0
    print(f"n_s within 2-sigma:  {'PASS' if n_s_ok else 'FAIL'}  ({best['n_s_sigma']:+.2f} sigma)")
    print(f"r below BK18 bound:  {'PASS' if r_ok else 'FAIL'}  (r={best['r']:.5f})")
    print(f"alpha_s within 2-sigma: {'PASS' if as_ok else 'FAIL'} ({best['alpha_s_sigma']:+.2f} sigma)")
    overall = n_s_ok and r_ok and as_ok
    print(f"OVERALL: {'CONSISTENT with referee' if overall else 'TENSION with referee'}")
    print("=" * 70)

    # Output for ledger
    os.makedirs("data", exist_ok=True)
    out = {
        "model": "Higgs inflation (non-minimal coupling, Bezrukov-Shaposhnikov 2008)",
        "referee": {
            "n_s": {"central": NS_CENTRAL, "sigma": NS_SIGMA, "source": "Planck 2018"},
            "r": {"upper_95": R_UPPER_95, "source": "BICEP/Keck 2018 (BK18)"},
            "alpha_s": {"central": ALPHAS_CENTRAL, "sigma": ALPHAS_SIGMA, "source": "Planck 2018"}
        },
        "scan": results,
        "best_fit": {"N": best_N, "chi2": best_chi2, "n_s": n_s, "r": r, "alpha_s": alpha_s},
        "confrontation": {
            "n_s_2sigma": n_s_ok,
            "r_bk18": r_ok,
            "alpha_s_2sigma": as_ok,
            "overall_consistent": overall
        }
    }
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, "higgs_inflation_spectrum.json")
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2)

    print(f"\nOutput written to {out_path}")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()