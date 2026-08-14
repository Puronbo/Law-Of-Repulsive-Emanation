"""
selberg_paradigm.py
===================
Resolve AUDIT §2 item 2 — the PAPER's Selberg paradigm claim:
  "the finite-disk spectrum (30 eigenvalues) suggests a concrete instance of
   Selberg's framework; the eigenvalues <-> Riemann-zero correspondence is
   'conjectured' — and explicitly undecidable at 30 eigenvalues
   (GUE/Poisson discrimination impossible)."  [claimed]

This is a CORRECTED re-test of the previous 100-mode run. The old artifact's
three supporting statistics each had a defect, fixed here:

  (a) The GOE ratio constant was 0.536; the canonical Atas et al. (2013)
      value is 0.5307 (Poisson 0.3863). The old run never tested the spacing
      DISTRIBUTION; we add a KS test against the GOE Wigner surmise
      P(s) = (pi/2) s exp(-pi s^2 / 4) — the correct ensemble for a real
      symmetric Laplacian (the repo's level_spacing_stats in
      Universals/spectral_analysis.py tested GUE, beta=2, instead).
  (b) "min dist 7.10, 0/100 within 0.5" was vacuous: the 100 disk modes
      have t = sqrt(E - 1/4) in [2.38, 7.03], entirely below the first
      zero t1 = 14.13 — the spectra are at disjoint scales, so "no
      correspondence" is not a tested statement. We report the reachability
      gap and the Weyl-density mismatch (disk density per unit E vs the
      zeros' Riemann-von Mangoldt density) instead. Note the old docstrings
      said "first 100 zeros" while only the 15 in
      Universals/spectral_analysis.py RIEMANN_ZEROS were used.
  (c) The spectral-form-factor test used a DEGENERATE null: random
      permutations of the same 186 lengths give a constant null mean (up to
      floating-point noise), so "mean pct 18.8" was rounding noise and
      "max pct 100.0 / 0 strong" were the same-multiset artifact. The set
      also included the tiny degenerate length ln(32/29) = 0.098 whose
      value sits at the C(ell)->n_t edge artifact. We re-test on the clean
      lengths (ell >= 1, excluding 13 such entries) with a matched-bootstrap
      null (resampling the length set with replacement, which preserves the
      ell-distribution) and a local-percentile peak test.

Verdict artifact: ../data/selberg_paradigm_data.json
"""
import json
import math
import os
import numpy as np
from scipy.stats import ks_2samp

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

# Atas, Bogomolny, Giraud, Roux, PRL 110, 084101 (2013)
POISSON_R = 0.38629
GOE_R = 0.5307


def ratio_stat(eigs):
    """Unfolded consecutive-ratio statistic <r> = mean(min(s_n,s_{n+1}) /
    max(...)), the same convention as the corpus's spectral_extended.py."""
    e = np.sort(np.asarray(eigs, dtype=float))
    n = len(e)
    idx = np.arange(1, n + 1, dtype=float)
    coeffs = np.polyfit(e, idx, deg=min(6, n // 2))
    un = np.poly1d(coeffs)(e)
    s = np.diff(un)
    s = s[s > 0]
    s = s / np.mean(s)
    r = np.minimum(s[:-1], s[1:]) / np.maximum(s[:-1], s[1:])
    return float(r.mean()), float(np.median(r)), float(r.std()), int(r.size)


def ks_vs_ensembles(eigs, seed=42, n_ref=5000):
    """KS test of the unfolded spacing distribution against the GOE Wigner
    surmise P(s) = (pi/2) s exp(-pi s^2/4) and Poisson P(s) = exp(-s)."""
    e = np.sort(np.asarray(eigs, dtype=float))
    n = len(e)
    idx = np.arange(1, n + 1, dtype=float)
    coeffs = np.polyfit(e, idx, deg=min(6, n // 2))
    un = np.poly1d(coeffs)(e)
    s = np.diff(un)
    s = s[s > 0]
    s = s / np.mean(s)
    rng = np.random.default_rng(seed)

    def wigner_goe(ns):
        out = []
        while len(out) < ns:
            x = rng.exponential(1.0)
            u = rng.uniform(0, 1)
            p = (math.pi / 2.0) * x * math.exp(-math.pi * x * x / 4.0)
            if u * math.exp(-x) < p:
                out.append(x)
        return np.array(out[:ns])

    goe = wigner_goe(n_ref)
    poi = rng.exponential(1.0, n_ref)
    ks_g, p_g = ks_2samp(s, goe)
    ks_p, p_p = ks_2samp(s, poi)
    return (float(ks_g), float(p_g), float(ks_p), float(p_p), int(s.size))


def main():
    spec = json.load(open(os.path.join(DATA, "spectral_extended_data.json")))
    eigs = np.array(spec["eigenvalues_all"], dtype=float)
    census = json.load(open(os.path.join(DATA, "googol_census_all_k_c7.json")))
    all_lens = np.array([e["geodesic_length"] for e in census["all_entries"]],
                        dtype=float)
    t_vals = np.sqrt(np.maximum(eigs - 0.25, 0.0))

    print("=" * 72)
    print("SELBERG PARADIGM, CORRECTED RE-TEST (AUDIT §2 item 2)")
    print("=" * 72)

    # (a) level statistics: ratio + distribution test
    r_mean, r_med, r_std, n_r = ratio_stat(eigs)
    se = r_std / math.sqrt(n_r)
    z_poi = (r_mean - POISSON_R) / se
    z_goe = (r_mean - GOE_R) / se
    ks_g, p_g, ks_p, p_p, n_sp = ks_vs_ensembles(eigs)
    if p_p > 0.05 and p_g < 0.05:
        a_verdict = ("POISSON (ratio z(GOE)=%.2f excludes GOE 0.5307; KS p="
                     "%.4f vs GOE Wigner, p=%.4f vs Poisson)" % (z_goe, p_g, p_p))
    elif p_g > 0.05 and p_p < 0.05:
        a_verdict = ("GOE (KS p=%.4f vs GOE Wigner, p=%.4f vs Poisson)"
                     % (p_g, p_p))
    else:
        a_verdict = ("INCONCLUSIVE (ratio z(Poisson)=%.2f, z(GOE)=%.2f; KS "
                     "p=%.4f GOE, p=%.4f Poisson)" % (z_poi, z_goe, p_g, p_p))
    print("(a) <r>=%.4f median=%.4f se=%.4f  (Poisson %.5f / GOE %.5f)"
          % (r_mean, r_med, se, POISSON_R, GOE_R))
    print("    z(Poisson)=%.2f  z(GOE)=%.2f" % (z_poi, z_goe))
    print("    KS n=%d: GOE stat=%.4f p=%.4f ; Poisson stat=%.4f p=%.4f"
          % (n_sp, ks_g, p_g, ks_p, p_p))
    print("    -> %s" % a_verdict)
    print("(b) disk t-range [%.2f, %.2f], t1=%.2f -> gap %.2f; disk density "
          "%.2f/E vs zeros %.5f/E -> factor %.0f; ~%.0f modes to t1, "
          "~%.0f to t15" % (t_min, t_max, t1, reach_gap, disk_density,
                            zero_density_per_E, density_ratio, n_to_t1,
                            n_to_t15))

    # (b) correspondence: reachability + density, not a naive distance
    t1 = 14.134725
    t_min, t_max = float(t_vals.min()), float(t_vals.max())
    reach_gap = t1 - t_max
    # Weyl density of the capped disk, measured from the actual spectrum
    E = np.sort(eigs)
    idx_E = np.arange(1, len(E) + 1, dtype=float)
    disk_density = float(np.polyfit(E, idx_E, 1)[0])   # per unit E
    # zero density at t1 per Riemann-von Mangoldt: dN/dt = (1/2pi)[ln(t/2pi e)+1]
    dNdt = (1.0 / (2.0 * math.pi)) * (math.log(t1 / (2.0 * math.pi * math.e)) + 1.0)
    zero_density_per_E = dNdt / (2.0 * t1)
    density_ratio = disk_density / zero_density_per_E
    n_to_t1 = disk_density * (t1 ** 2 + 0.25)
    n_to_t15 = disk_density * (65.112544 ** 2 + 0.25)
    b_match = False
    b_verdict = ("NOT TESTABLE AT 100 MODES - the disk t-range [%.2f, %.2f] "
                 "never reaches the first zero t1=%.2f (gap %.2f), so "
                 "'min dist 7.10, 0 within 0.5' is a scale mismatch, not a "
                 "measured absence. And the mismatch is structural: the "
                 "capped disk's measured Weyl density is %.2f levels per "
                 "unit E vs the zeros' %.5f per unit E at t1 - a factor "
                 "%.0f - so no number of disk modes can reproduce the "
                 "zeros' spectrum (reaching t1 alone needs ~%.0f modes, "
                 "reaching t15 needs ~%.0f)."
                 % (t_min, t_max, t1, reach_gap, disk_density,
                    zero_density_per_E, density_ratio, n_to_t1, n_to_t15))

    # (c) spectral form factor, corrected null
    clean = all_lens[all_lens >= 1.0]
    n_excl = int(all_lens.size - clean.size)
    ell_grid = np.linspace(1.0, clean.max(), 40001)
    C_all = np.sum(np.cos(np.outer(ell_grid, t_vals)), axis=1)
    bg = np.convolve(C_all, np.ones(401) / 401, mode="same")
    resid = C_all - bg
    C_clean = np.array([float(np.interp(ell, ell_grid, resid)) for ell in clean])

    rng = np.random.default_rng(7)
    n_null = 10000
    null_mean = np.empty(n_null)
    null_max = np.empty(n_null)
    for i in range(n_null):
        lr = rng.choice(clean, size=clean.size, replace=True)
        v = np.abs(np.interp(lr, ell_grid, resid))
        null_mean[i] = float(np.mean(v))
        null_max[i] = float(np.max(v))
    m_m = float(np.mean(np.abs(C_clean)))
    mx_m = float(np.max(np.abs(C_clean)))
    pct_mean = float((null_mean <= m_m).mean())
    pct_max = float((null_max <= mx_m).mean())
    # local-percentile peak test: each Mersenne |C| vs the nearest 1000
    # grid values (controls the ell-dependent amplitude baseline)
    ab = np.abs(resid)
    locs = []
    for le in clean:
        w = np.abs(ell_grid - le)
        idx = np.argsort(w)[:1000]
        locs.append(float((ab[idx] < abs(float(np.interp(le, ell_grid, resid)))).mean()))
    locs = np.array(locs)
    n_local_strong = int((locs > 0.7).sum())
    n_local_exp = int(round(0.3 * clean.size))
    print("(c) clean lengths=%d (excluded %d tiny), matched-bootstrap null: "
          "mean-abs pctile=%.1f, max pctile=%.1f; local-percentile mean=%.1f, "
          "n>70%%=%d (exp %d)"
          % (clean.size, n_excl, 100 * pct_mean, 100 * pct_max,
             100 * locs.mean(), n_local_strong, n_local_exp))
    c_verdict = ("NO TRACE-FORMULA SIGNATURE: the Mersenne lengths' mean "
                 "|C| sits at the %.0fth percentile of matched random "
                 "length-sets (null), their local percentiles average %.1f "
                 "(50 = chance), and %d/%d exceed the 70%% local mark "
                 "(~%d expected by chance). The old 'mean pct 18.8 / max pct "
                 "100.0 / 0 strong' statistics were invalid (degenerate "
                 "permutation null + the ln(32/29)=0.098 edge artifact)."
                 % (100 * pct_mean, 100 * locs.mean(), n_local_strong,
                    clean.size, n_local_exp)) \
        if pct_mean < 0.95 else (
            "PEAKS PRESENT: Mersenne lengths produce stronger than random "
            "oscillations - a weak trace-formula signature.")

    parts = []
    parts.append("(a) level statistics, corrected ensemble: " + a_verdict)
    parts.append("(b) eigenvalue<->zero correspondence: " + b_verdict)
    parts.append("(c) trace-formula length spectrum: " + c_verdict)
    overall = "; ".join(parts)
    verdict = ("SELBERG PARADIGM NOT SUPPORTED as a concrete instance: " +
               overall)
    print("\nverdict:", verdict)

    out = {
        "claim": ("AUDIT §2 item 2: PAPER 'suggests a concrete instance of "
                  "Selberg's framework'; eigenvalues<->Riemann zeros "
                  "'conjectured'; GUE/Poisson 'impossible at 30'"),
        "setup": {"n_modes": int(eigs.size),
                  "n_all_census_lengths": int(all_lens.size),
                  "n_clean_lengths": int(clean.size),
                  "n_excluded_tiny_lengths": n_excl,
                  "n_null_samples": n_null,
                  "length_range": [round(float(clean.min()), 3),
                                   round(float(clean.max()), 3)]},
        "a_level_stats": {
            "r_mean": round(r_mean, 4), "r_median": round(r_med, 4),
            "r_std": round(r_std, 4), "se": round(se, 4),
            "poisson_0.3863": POISSON_R, "goe_0.5307": GOE_R,
            "z_poisson": round(z_poi, 2), "z_goe": round(z_goe, 2),
            "ks_goe_stat": round(ks_g, 4), "ks_goe_p": round(p_g, 4),
            "ks_poisson_stat": round(ks_p, 4), "ks_poisson_p": round(p_p, 4),
            "n_spacings": n_sp,
            "note": ("GOE is the correct ensemble for this real symmetric "
                     "operator; Universals/spectral_analysis.py "
                     "level_spacing_stats tested GUE (beta=2) instead"),
            "verdict": a_verdict},
        "b_zeros": {
            "t_range": [round(t_min, 3), round(t_max, 3)],
            "t1": t1,
            "spectra_overlap": bool(t_max >= t1),
            "reach_gap": round(reach_gap, 3),
            "min_dist_old": 7.1009,
            "within_0.5_old": 0,
            "note_old": ("the old min-dist/within-0.5 were computed against "
                         "only the 15 zeros in RIEMANN_ZEROS (docstrings "
                         "claimed 100) and are vacuous: the disk t-range "
                         "never reaches the first zero"),
            "disk_density_per_E": round(disk_density, 3),
            "zero_density_per_E_at_t1": round(zero_density_per_E, 6),
            "density_ratio": round(density_ratio, 0),
            "modes_needed_to_reach_t1": round(n_to_t1, 0),
            "modes_needed_to_reach_t15": round(n_to_t15, 0),
            "verdict": b_verdict},
        "c_form_factor": {
            "mersenne_mean_abs_pctile": round(100 * pct_mean, 1),
            "mersenne_max_abs_pctile": round(100 * pct_max, 1),
            "local_percentile_mean": round(100 * locs.mean(), 1),
            "n_strong_gt_70pct_local": n_local_strong,
            "expected_gt_70pct": n_local_exp,
            "note": ("matched-bootstrap null (resample the length set with "
                     "replacement, preserving the ell-distribution); the old "
                     "permutation null was degenerate (constant mean) and the "
                     "old 18.8 was floating-point noise"),
            "verdict": c_verdict},
        "verdict": verdict,
    }
    with open(os.path.join(DATA, "selberg_paradigm_data.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("wrote data/selberg_paradigm_data.json")


if __name__ == "__main__":
    main()
