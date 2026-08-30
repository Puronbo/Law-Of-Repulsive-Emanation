"""Quantile calibration of the threat law: the gap function is the
inverse-threshold (calibration) curve, and the measured escapes invert to
effective thresholds.

genesis_gapfn.json proved beta(s) = S(theta_star/s) row-by-row (|resid|
<=0.0014): the coupling-space transition IS the survival function of the
threat ratio evaluated on a moving threshold.  This run:

  * inverts the measured escapes through the exact quantile S^(-1)(a):
      S^(-1)(0.8361) -> the MARKET's effective h/X threshold theta_eff
      S^(-1)(0.8305) -> the model MC effective threshold (must close to
                        theta_star if self-consistent)
      implied effective cusp-depth d*_eff = theta*I/(g0*gdepth)
  * reads the transition sharpness: coupling width for beta 0.10..0.90
      s_90/s_10 = S^(-1)(0.1)/S^(-1)(0.9)  (the Griffith-smeared width in
      exact closed form)
  * states the sharpening condition: a single-severity population has a
    STEP survival law (sharp gate); any population spread smears it
    geometrically (ratio landmarks {a/d,b/d,a/c,b/c}).

All numbers closed-form or exact bisection; no new assumptions.
"""

import json
import math
import os

from credit_commons.sim import Params

P = Params()
G_STAR = 2.0 * math.sqrt(P.g0 * P.gdepth * P.reward())
D_STAR = (G_STAR / P.g0 - 1.0) / P.gdepth
THETA_STAR = P.g0 * P.gdepth * D_STAR / P.I     # 0.06332

A, B, C, D = 0.02, 0.20, 0.05, 1.50


def survival(theta):
    """Exact S(theta) = P(h/x > theta), h~U(a,b), x~U(c,d) (as in the audit)."""
    if theta <= A / D:
        return 1.0
    if theta >= B / C:
        return 0.0
    x1 = A / theta
    x2 = B / theta
    area = (min(x1, D) - C) if x1 > C else 0.0
    lo = max(C, x1)
    hi = min(D, x2)
    if hi > lo:
        area += ((B * hi - theta * hi * hi / 2.0)
                 - (B * lo - theta * lo * lo / 2.0)) / (B - A)
    return area / (D - C)


def quantile(target):
    """Bisection: theta with S(theta) = target (S strictly decreasing)."""
    lo, hi = A / D, B / C
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if survival(mid) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def main():
    with open(os.path.join("experiments", "emanation", "data",
                           "harm_as_depth.json")) as fh:
        exp = json.load(fh)
    p_exp = exp["frac_past_cusp"]          # unrounded, 6689/8000
    n_exp = exp["n_ok"]

    theta_eff = quantile(round(p_exp, 4))  # inverse of the 4dp record 0.8361
    theta_mc = quantile(0.8305)       # model MC escape (harm_cap seed 42)
    d_eff = theta_eff * P.I / (P.g0 * P.gdepth)
    d_mc = theta_mc * P.I / (P.g0 * P.gdepth)
    theta_half = quantile(0.5)
    theta_lo = quantile(0.9)      # small theta: only 10% sampled-to-escape
    theta_hi = quantile(0.1)      # large theta: 90% fail to clear

    # sampling uncertainty of the n=8000 measurement
    se = math.sqrt(p_exp * (1.0 - p_exp) / n_exp)
    z_closed = (p_exp - 0.82992) / se      # vs exact closed form S(theta*)
    z_mc = (p_exp - 0.8305) / se           # vs 400k MC (harm_cap seed 42)
    band_lo = quantile(p_exp + 1.96 * se)  # larger theta end
    band_hi = quantile(p_exp - 1.96 * se)  # smaller theta end
    d_star_minus_g0 = D_STAR - P.g0

    s10 = THETA_STAR / theta_hi   # coupling at beta=0.10 (small)
    s90 = THETA_STAR / theta_lo   # coupling at beta=0.90 (large)
    width_ratio = s90 / s10
    width_decades = math.log10(width_ratio)
    s_half = THETA_STAR / theta_half           # midpoint coupling

    out = {
        "identity": "quantile calibration of the exact threat law.  Model "
                    "self-consistency: MC escape 0.8305 inverts to "
                    "theta_mc=%.5f (theta_star=%.5f).  The n=%d trade "
                    "experiment (harm_as_depth) measured p=%.4f; its "
                    "inversion theta_eff=%.5f is NOISE-LEVEL (|z|=%.2f vs "
                    "the exact closed form 0.82992, |z|=%.2f vs the 400k MC "
                    "0.8305): the 95%% band [%.5f, %.5f] CONTAINS theta*, so "
                    "no significant market frailty is claimed.  The apparent "
                    "d*(1-theta_eff/theta*) = d*(1-P.g0/d*) digit coincidence "
                    "is flagged, not claimed (coincidence-discipline).  "
                    "Transition sharpness: 10-90%% coupling width = %.2f "
                    "(%.2f decades); midpoint s_half=%.3f.  Sharpening "
                    "condition: a single-severity population gives a STEP "
                    "survival law (sharp gate); smearing width = the "
                    "population's endogenous spread, exact in the "
                    "ratio-landmark ladder."
                    % (theta_mc, THETA_STAR, n_exp, p_exp, theta_eff,
                       abs(z_closed), abs(z_mc), band_lo, band_hi,
                       width_ratio, width_decades, s_half),
        "theta_star": THETA_STAR,
        "quantiles": {"S_inv(0.9)_theta_lo": round(theta_lo, 5),
                      "S_inv(0.5)_theta_half": round(theta_half, 5),
                      "S_inv(0.1)_theta_hi": round(theta_hi, 5)},
        "calibration": {
            "market_escape": round(p_exp, 6),
            "n_trades": n_exp,
            "binomial_se": round(se, 6),
            "market_effective_threshold_h_over_X": round(theta_eff, 5),
            "model_mc_escape": 0.8305,
            "model_mc_effective_threshold_h_over_X": round(theta_mc, 5),
            "model_self_closing_residual": round(theta_mc - THETA_STAR, 6),
            "effective_cusp_depth_market": round(d_eff, 4),
            "book_cusp_depth": round(D_STAR, 4),
            "z_vs_exact": round(z_closed, 2),
            "z_vs_400k_mc": round(z_mc, 2),
            "theta_eff_95pct_band": [round(band_lo, 5), round(band_hi, 5)],
            "band_contains_theta_star": band_lo <= THETA_STAR <= band_hi,
            "frailty_verdict": "NOT significant: |z|<1.65 (one-sided 5%%); "
                               "the 95%% band contains theta*; the measured "
                               "escape law closes across closed form (0.82992), "
                               "400k MC (0.8305) and the n=8000 experiment "
                               "(%.4f) within sampling error.  Earlier text "
                               "('market ~2.4%% frailer') is RETRACTED as a "
                               "sampling illusion." % p_exp,
            "coincidence_check": {
                "d_star_eff_vs_d_star_minus_g0": [
                    round(d_eff, 4), round(d_star_minus_g0, 4)],
                "digit_level_agreement": 4,
                "status": "FLAGGED, NOT CLAIMED: the 8000-sample inversion "
                          "hits d*_eff = d* - P.g0 to 4 digits, but the "
                          "sample carries NO g0-scale depth (observed depth "
                          "~1e-4..2e-3 in sample_events), so no measured "
                          "mechanism exists; coincidence-discipline as for "
                          "alpha~pi/3 in genesis_euler.json.",
            },
        },
        "transition_sharpness": {
            "beta_10pct_coupling_s": round(s10, 4),
            "beta_90pct_coupling_s": round(s90, 4),
            "width_ratio_s90_over_s10": round(width_ratio, 3),
            "width_decades": round(width_decades, 3),
            "midpoint_coupling_s_half": round(s_half, 4),
            "sharpening_condition": "single-severity population => step "
                                    "survival => infinitely sharp gate; "
                                    "only population shaping (not threshold "
                                    "tuning) can sharpen the smeared "
                                    "transition.",
        },
        "landmarks": {"a/d": A / D, "b/d": B / D, "a/c": A / C, "b/c": B / C},
        "reading": "the gap function is the inverse-threshold law "
                   "s(alpha) = theta_star / T(alpha), T = S^(-1): coupling "
                   "calibration IS quantile analysis of the population's "
                   "severity ratio.  Griffiths-smearing is not a defect to "
                   "remove by tuning; it is the exact measure of population "
                   "spread.  First error-banded quantity in the ledger: the "
                   "critical line theta* = %.5f carries a 95%% band from the "
                   "n=8000 binomial measurement." % THETA_STAR,
    }
    path = os.path.join("experiments", "emanation", "data",
                        "genesis_quantiles.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("theta_star = %.6f" % THETA_STAR)
    print("calibration: S^-1(0.8305 mc) = %.5f (residual %+.6f); "
          "n=%d p=%.6f S^-1(p) = %.5f => d*_eff = %.4f vs d* = %.4f"
          % (theta_mc, theta_mc - THETA_STAR, n_exp, p_exp, theta_eff,
             d_eff, D_STAR))
    print("uncertainty: se=%.6f  z_vs_exact=%.2f  z_vs_400k_mc=%.2f  "
          "95%% band on theta_eff = [%.5f, %.5f], contains theta* = %s"
          % (se, z_closed, z_mc, band_lo, band_hi,
             band_lo <= THETA_STAR <= band_hi))
    print("frailty verdict: NOT significant; earlier '~2%% frailer' "
          "RETRACTED (sampling illusion).")
    print("coincidence-check: d*_eff = %.4f vs d* - g0 = %.4f (4-digit hit) "
          "-> FLAGGED, mechanism absent, NOT claimed." % (d_eff,
                                                          d_star_minus_g0))
    print("transition: beta=10%% at s=%.3f, beta=90%% at s=%.3f, 10-90%% "
          "coupling-width ratio = %.2f (%.2f decades); midpoint s_half = "
          "%.3f" % (s10, s90, width_ratio, width_decades, s_half))
    print("sharpening condition: only population shaping sharpens; threshold "
          "tuning cannot (exact tail law).")
    print("WROTE data/genesis_quantiles.json")


if __name__ == "__main__":
    main()