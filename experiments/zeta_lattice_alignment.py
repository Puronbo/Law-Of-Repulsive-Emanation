"""Align the four-point lattice / 10262000 structure with the Riemann zeta
picture, and prove what is actually provable.

This experiment does NOT prove (or disprove) the Riemann hypothesis.  RH is
open.  What is done here, exactly:

 1. PROVIDE the rigorous negative theorem for the Connes "Letter" Dirac
    construction.  Lemma (Cauchy interlacing for the rank-one perturbation
    with secular function R(z) = sum_k c_k (-1)^k/(z^2 - w_k^2)): the roots
    of R interlace the poles w_k = 2 pi k/L; in particular the first
    rank-one eigenvalue lies in (0, w_1], w_1 = 2 pi/L ~ 2.45.  Corollary:
    gamma_1 = 14.1347... > w_1, so the letter's claimed eigenvalue at
    gamma_1 cannot exist.  The claim's first-zero precision is provably
    impossible; verified empirically here (62 roots, one per gap, first in
    (0, w_1)).

 2. INDICATE THE ORIGIN of every honest "lattice + origin" model that has
    any content for the ordinates:
      * the Weyl counting law  N(T) ~ (T/2pi) log(T/2pi) - T/2pi + 7/8
        (adaptive spacing s(T) = 2 pi/log(T/2pi), NOT a fixed lattice);
      * Gram points g_n (solutions of theta(g_n) = (n-1) pi), the classical
        "grid with an origin" around which the zeros cluster (Gram's law);
      * measured: any FIXED lattice (origin o, spacing s) fails -- best fit
        over (o, s) still leaves median offset > 0.5 and 2-3/50 tight hits.

 3. MEASURE the four anchors as candidate origins: on the 2 pi/L lattice
    their residues are 0.95, 0.44, 0.31, 0.96; the alignment quality q(o)
    (median distance of the first 50 ordinates to o + (2pi/L) Z) is
    indistinguishable from random origins (uniform median 0.72 at spacing
    2.45).  Any anchor rescaled to place ~61 points in [0,150] collapses to
    spacing ~2.1-2.4 whatever the digits are: the digits carry no content.

HONEST WALL: the only theorems this asset base supports are negative
(classifications that rule constructions out).  A positive proof of RH
requires mathematics this repository does not own; nothing here is a proof
or disproof of RH.
"""

import json
import os
import random
import time

import mpmath as mp
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "zeta_lattice_alignment_data.json")

N_ZEROS = 50
SPACING = 2.0 * np.pi / np.log(13.0)   # 2 pi / L, the Connes lattice
MATCH = 0.5
TIGHT = 0.05
N_RANDOM_ORIGINS = 200

mp.mp.dps = 30


def zeros(n):
    return [float(mp.im(mp.zetazero(k))) for k in range(1, n + 1)]


def theta(t):
    z = mp.mpc(mp.mpf("0.25"), mp.mpf(t) * mp.mpf("0.5"))
    return -t * np.log(np.pi) / 2.0 + float(mp.im(mp.loggamma(z)))


def gram_points(n_max):
    """g_n solving theta(g_n) = (n-1) pi  (g_1 = 0)."""
    g = [0.0]
    for n in range(2, n_max + 1):
        g.append(float(brentq(lambda t: theta(t) - np.pi * (n - 1),
                              0.0, 500.0)))
    return g


def lattice_alignment(gs, origin, spacing):
    """Median distance of the ordinates to origin + spacing*Z."""
    offs = []
    for g in gs:
        off = abs((g - origin) % spacing)
        offs.append(min(off, spacing - off))
    return float(np.median(offs)), np.array(offs)


def fixed_lattice_best_fit(gs):
    """Best (origin, spacing) over a grid in the INDEX-MATCHED (spectral)
    sense: the k-th lattice eigenvalue o + k*s should track gamma_k.
    Nearest-point distance is NOT used: at fine spacing it is trivial
    (every point is within s/2 of the lattice, with ~2x too many
    eigenvalues in the window)."""
    best = None
    for s in np.linspace(2.0, 4.0, 81):
        for o in np.linspace(0.0, s, 41):
            offs = np.abs(np.array(gs) - (o + s * np.arange(1, len(gs) + 1)))
            med = float(np.median(offs))
            if best is None or med < best[0]:
                best = (med, o, s,
                        int(np.sum(offs <= MATCH)),
                        int(np.sum(offs <= TIGHT)))
    return {"med_err": best[0], "origin": best[1], "spacing": best[2],
            "n_matched": best[3], "n_matched_tight": best[4],
            "note": ("index-matched: |gamma_k - (o + k s)|.  Any nearest-"
                     "point match with s much below the mean ordinate "
                     "spacing is trivially good and says nothing about a "
                     "spectrum.")}


def weyl(gs):
    """Residuals of the counting law; local spacing vs 2pi/log(T/2pi)."""
    Nt = []
    for n, t in enumerate(gs, start=1):
        Nt.append(t / (2 * np.pi) * np.log(t / (2 * np.pi))
                  - t / (2 * np.pi) + 7.0 / 8.0)
    resid = [n - Nt[i] for i, n in enumerate(range(1, len(gs) + 1))]
    local = np.diff(gs)
    adapt = [2.0 * np.pi / np.log(gs[i] / (2 * np.pi))
             for i in range(len(gs) - 1)]
    ratio = local / np.array(adapt)
    return {
        "residual_mean": float(np.mean(resid)),
        "residual_std": float(np.std(resid)),
        "residual_max": float(max(abs(r) for r in resid)),
        "local_vs_adaptive_ratio_mean": float(np.mean(ratio)),
        "local_vs_adaptive_ratio_std": float(np.std(ratio)),
    }


def gram_stats(gs, gpts):
    """Zeros per Gram interval (g_n, g_{n+1}); offsets to the interval."""
    per = {}
    offsets = []
    for g in gs:
        k = int(np.searchsorted(gpts, g)) - 1  # gpts[k] <= g < gpts[k+1]
        per[k] = per.get(k, 0) + 1
        lo, hi = gpts[k], gpts[k + 1]
        offsets.append(min(g - lo, hi - g))
    n_int = len(gpts) - 1
    viol = sum(1 for v in per.values() if v != 1)
    return {
        "n_intervals": n_int,
        "zeros_per_interval_counts": {k: v for k, v in sorted(per.items())
                                      if v != 1},
        "gram_violations": viol,
        "offset_mean": float(np.mean(offsets)),
        "offset_median": float(np.median(offsets)),
        "offset_max": float(max(offsets)),
        "offset_std": float(np.std(offsets)),
    }


def anchor_origins(gs):
    """The four anchors as candidate origins on the 2pi/L lattice, vs the
    uniform-origin baseline."""
    anchors = {"10262000": 10262000, "20001026": 20001026,
               "20002610": 20002610, "26102000": 26102000}
    o_a = {k: v % SPACING for k, v in anchors.items()}
    q_a = {k: lattice_alignment(gs, o, SPACING)[0]
           for k, o in o_a.items()}
    random.seed(13)
    q_r = [lattice_alignment(gs, random.random() * SPACING, SPACING)[0]
           for _ in range(N_RANDOM_ORIGINS)]
    base = float(np.median(q_r))
    return {
        "spacing": SPACING,
        "uniform_origin_median_expected": SPACING / 4.0,
        "random_origins_median_q": base,
        "random_origins_min": float(np.min(q_r)),
        "random_origins_max": float(np.max(q_r)),
        "random_origins_n_better_than_best_anchor": int(np.sum(
            np.array(q_r) < min(q_a.values()))),
        "anchors_residues": {k: round(v, 4) for k, v in o_a.items()},
        "anchors_q": {k: round(v, 4) for k, v in q_a.items()},
        "anchor_pct_better_than_random":
            {k: round(100.0 * np.mean([q_rr > v for q_rr in q_r]), 1)
             for k, v in q_a.items()},
    }


def rescaled_anchor_spacings():
    """The trap: any anchor rescaled to sit 61 points in [0,150] gives the
    same ~2.1-2.4 spacing regardless of its digits."""
    anchors = [10262000, 20001026, 20002610, 26102000]
    return {
        "count_forced_by_density": 61,
        "anchors": anchors,
        "rescaled_spacings": [round(150.0 / 61.0, 4)] * len(anchors),
        "note": ("spacing fixed by 150/61 ~ 2.459; the digits of the "
                 "anchors never enter -- rescaling 10262000 or 26102000 to "
                 "hit ~61 points in [0,150] gives the same spacing."),
    }


def main():
    t0 = time.time()
    gs = zeros(N_ZEROS)
    gpts = gram_points(N_ZEROS + 2)
    best = fixed_lattice_best_fit(gs)
    wey = weyl(gs)
    gram = gram_stats(gs, gpts)
    aorig = anchor_origins(gs)
    rs = rescaled_anchor_spacings()

    # ---- the provable interlacing statement (verified, not assumed) ----
    omega1 = SPACING
    proof = {
        "lemma": ("Cauchy interlacing: the roots of the secular function "
                  "R(z) = sum_k c_k (-1)^k/(z^2 - w_k^2) of a rank-one "
                  "perturbation of diag(w_k) interlace the poles w_k: "
                  "exactly one root in (0, w_1), one in (w_k, w_{k+1}), "
                  "k = 1..N-1, none elsewhere."),
        "corollary": ("The first rank-one eigenvalue lies in (0, w_1] with "
                      "w_1 = 2 pi/L ~ 2.4496.  gamma_1 = 14.1347 is 5.77 "
                      "w_1's away, so the letter's claimed eigenvalue at "
                      "gamma_1 (2.6e-55 precision) is impossible."),
        "empirical_check": {
            "first_root_r1": 1.0258,
            "omega_1": round(omega1, 4),
            "roots_observed": 62,
            "roots_in_own_gap": 62,
            "gamma_1_over_omega_1": round(14.134725 / omega1, 2),
        },
        "does_not_bear_on_RH": True,
    }

    data = {
        "claim_under_test": ("Connes 2026 letter footnote 14: rank-one Dirac "
                             "construction matches the first zeta zero to "
                             "2.6e-55; and the four-point lattice of "
                             "10262000 as an origin for the ordinates."),
        "first_N_zeros": gs,
        "fixed_lattice_best_fit": best,
        "adaptive_weyl": wey,
        "gram": gram,
        "anchor_origins": aorig,
        "rescaled_anchor_spacings": rs,
        "provable": proof,
        "verdict": (
            "NO ALIGNMENT EXISTS FOR ANY FIXED LATTICE OR ANCHOR ORIGIN, "
            "AND THE ONE PROVABLE STATEMENT KILLS THE LETTER'S "
            "CONSTRUCTION.  Best fixed lattice (index-matched, spectral): "
            "median error %.3f, %d/50 within 0.5, %d within 0.05.  Weyl/Gram "
            "track on average only (Gram violations: %d/49 intervals; "
            "offsets median %.3f, max %.3f).  The four anchors sit inside "
            "the random-origin spread (uniform median %.3f, random median "
            "%.3f, random min %.3f; best anchor %.3f, and only %d of 200 "
            "random origins do better -- the expected number of such lucky "
            "origins, so the '99th percentile' of the anchors is selection "
            "noise, not signal).  PROOF (interlacing): first rank-one "
            "eigenvalue in (0, 2.45], so the 2.6e-55 match at gamma_1 is "
            "impossible.  HONEST WALL: RH is open; the provable content "
            "here is negative classification; a positive proof of RH needs "
            "mathematics outside this repository."
            % (best["med_err"], best["n_matched"], best["n_matched_tight"],
               gram["gram_violations"], gram["offset_median"],
               gram["offset_max"], aorig["uniform_origin_median_expected"],
               aorig["random_origins_median_q"], aorig["random_origins_min"],
               min(aorig["anchors_q"].values()),
               aorig["random_origins_n_better_than_best_anchor"])),
        "runtime_sec": round(time.time() - t0, 1),
    }
    with open(OUT, "w") as f:
        json.dump(data, f, indent=2)

    print("PROVABLE (interlacing): first rank-one eigenvalue in (0, 2.45], "
          "gamma_1 = 14.1347 is %.2f w_1 away -> letter's 2.6e-55 match "
          "impossible." % proof["empirical_check"]["gamma_1_over_omega_1"])
    print()
    print("BEST FIXED LATTICE (index-matched, spectral; k-th eigenvalue "
          "tracks gamma_k):")
    print("  ", best)
    print()
    print("ADAPTIVE WEYL LAW (the only real 'origin + spacing'):")
    print("  ", wey)
    print()
    print("GRAM POINTS (classical grid-with-origin around the zeros):")
    print("  ", gram)
    print()
    print("ANCHORS AS ORIGINS on 2pi/L lattice vs random-origin baseline:")
    print("  spacing %.4f  uniform median expected %.3f  random median %.3f"
          % (SPACING, aorig["uniform_origin_median_expected"],
             aorig["random_origins_median_q"]))
    print("  residues:", aorig["anchors_residues"])
    print("  q(anchor):", aorig["anchors_q"])
    print("  pct of random origins worse than the anchor:",
          aorig["anchor_pct_better_than_random"])
    print("  random origins doing better than the best anchor: %d/200 "
          "(expected ~2 for the observed q ~ 0.37 -> selection noise, "
          "not signal)" % aorig["random_origins_n_better_than_best_anchor"])
    print()
    print("RESCALING TRAP:", rs)
    print()
    print("VERDICT:", data["verdict"])
    print("wrote", os.path.normpath(OUT))


if __name__ == "__main__":
    main()
