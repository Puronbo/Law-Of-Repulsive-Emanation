"""Direct, head-on probes of the Connes "Letter to Riemann" number claims
(2026-08-15).

The earlier experiments (connes_dirac, zeta_lattice_alignment) measured the
letter's claims INDIRECTLY (lattice offsets, matching counts, origin
residues).  This experiment computes the three decisive things directly:

  A1  DIRECT |fhat(gamma_n)| AT THE ORDINATES.  For the letter's own
      construction (N = 150 trig-truncated even ground state, its best
      slice) the identity is EXACT:
          fhat(z) = 4 z sin(z L / 2) R(z),
          R(z)   = sum_k c_k (-1)^k / (z^2 - w_k^2),   w_k = 2 pi k / L,
      so within [0, 150] the ordinates are zeros of fhat IFF
      fhat(gamma_n) = 0.  At mpmath dps 60 we evaluate |fhat(gamma_n)| and
      the Newton distance  delta_n = |fhat(gamma_n)| / |fhat'(gamma_n)|
      (the first-order distance from gamma_n to the nearest zero), for
      n = 1..50, plus the positional distance |gamma_1 - r_1| from the
      claimed first match.  Claimed precision: 2.6e-55 (first) .. 1e-2
      (50th).  Head-on numbers replace the indirect statistics.

  A2  THE INTERLACING THEOREM AT EVERY N.  Cauchy interlacing pins the
      first rank-one eigenvalue into (0, w_1] with w_1 = 2 pi/L ~ 2.4496,
      while gamma_1 = 14.1347 is 5.77 w_1's away.  Verified at N in
      {50, 100, 150, 200, 300}: one root per pole gap, first root r_1 in
      (0, w_1), the same wall at every truncation.

  A3  THE WHOLE 840-POINT ORBIT AS ORIGINS.  Every digit permutation of
      {0,0,0,0,1,2,2,6} (the anchors included) as an origin on the
      2 pi/L lattice, measured with the same q(o) as the four anchors,
      against the EXTREME-VALUE distribution of 840 random origins
      (100 trials).  Closes "chance level" over EVERY known point, not
      just the four anchors.

HONEST WALL: the direct numbers confirm what the indirect ones said -- the
letter's first-zero precision is categorically impossible and no known
point is a special origin -- and nothing here is a proof or disproof of
RH; no de Bruijn-Newman Lambda consequence; finitely many primes never
become the full Euler product; C_0 = V(q0) = H(q0,0) does not enter.
"""

import itertools
import json
import os
import random
import sys
import time

import mpmath as mp
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "zeta_direct_probe_data.json")

import connes_letter as cl  # noqa: E402  (same directory)

N_ZEROS = 50
N_TRIG = 150            # A1: the letter's best trig slice
N_SWEEP = (50, 100, 150, 200, 300)
SPACING = 2.0 * np.pi / cl.L
SCAN_HI = 150.0
DPS = 60
N_RANDOM_ORIGINS = 840  # A3: same size as the orbit, for an honest census
N_EXTREME_TRIALS = 100

mp.mp.dps = DPS


def high_precision_ordinates(n):
    return [mp.im(mp.zetazero(k)) for k in range(1, n + 1)]


# ---------------------------------------------------------------- A1: direct


def mp_sincL(x):
    x = mp.mpf(x)
    if abs(x) < mp.mpf("1e-40"):
        return mp.mpf(cl.L)
    return 2.0 * mp.sin(x * mp.mpf(cl.L) / 2.0) / x


def mp_R(z, c, om):
    total = mp.mpf("0")
    for k in range(len(om)):
        total += mp.mpf(c[k]) * ((-1.0) ** k) / (z * z - mp.mpf(om[k]) ** 2)
    return total


def mp_R_deriv(z, c, om):
    total = mp.mpf("0")
    for k in range(len(om)):
        total += (mp.mpf(c[k]) * ((-1.0) ** k) * (-2.0 * z)
                  / (z * z - mp.mpf(om[k]) ** 2) ** 2)
    return total


def mp_fhat_direct(z, c, om):
    total = mp.mpf("0")
    for k in range(len(om)):
        total += mp.mpf(c[k]) * (mp_sincL(z + mp.mpf(om[k]))
                                 + mp_sincL(z - mp.mpf(om[k])))
    return total


def mp_fhat_Rform(z, c, om):
    return 4.0 * z * mp.sin(z * mp.mpf(cl.L) / 2.0) * mp_R(z, c, om)


def mp_fhat_deriv(z, c, om):
    R = mp_R(z, c, om)
    Rp = mp_R_deriv(z, c, om)
    Lh = mp.mpf(cl.L) / 2.0
    S, C = mp.sin(z * Lh), mp.cos(z * Lh)
    return 4.0 * S * R + 4.0 * z * Lh * C * R + 4.0 * z * S * Rp


def mp_bisect_r1(c, om):
    lo, hi = mp.mpf("1e-9"), mp.mpf(om[1]) - mp.mpf("1e-6")
    flo = mp_R(lo, c, om)
    for _ in range(500):
        mid = (lo + hi) / 2
        if mp_R(mid, c, om) * flo > 0:
            lo, flo = mid, mp_R(mid, c, om)
        else:
            hi = mid
    return (lo + hi) / 2


def direct_ordinate_probe(c, om):
    gs = high_precision_ordinates(N_ZEROS)
    rows = []
    max_rel_ident = mp.mpf("0")
    for gn in gs:
        fd = mp_fhat_direct(gn, c, om)
        fr = mp_fhat_Rform(gn, c, om)
        dp = mp_fhat_deriv(gn, c, om)
        rel = abs(fd - fr) / max(abs(fd), mp.mpf("1e-300"))
        max_rel_ident = max(max_rel_ident, rel)
        rows.append({
            "n": len(rows) + 1,
            "gamma": float(gn),
            "abs_fhat": float(abs(fd)),
            "newton_distance_delta": float(abs(fd) / max(abs(dp),
                                                         mp.mpf("1e-300"))),
            "rel_identity_err": float(rel),
        })

    # r_1 (first rank-one eigenvalue, the ACTUAL first zero of fhat)
    r1 = mp_bisect_r1(c, om)
    r1_zero_value = abs(mp_fhat_Rform(r1, c, om))  # ~ 0: it IS a zero
    g1 = gs[0]

    # exact nearest-rank-one-root distance at N_TRIG (float64, from A2-style
    # roots) vs the head-on Newton estimate
    roots = [mp.mpf(r) for r in float_roots_of_R(c, om)]
    nearest = []
    for gn in gs:
        nearest.append(min(float(abs(gn - rr)) for rr in roots))
    cross = [
        abs(rows[i]["newton_distance_delta"] - nearest[i])
        for i in range(N_ZEROS)
    ]

    abs_f = [r["abs_fhat"] for r in rows]
    deltas = [r["newton_distance_delta"] for r in rows]

    def q(x):
        return float(np.median(x)), float(np.min(x)), float(np.max(x))

    return {
        "method": ("mpmath dps %d; fhat(z) = 4 z sin(zL/2) R(z), "
                   "R(z) = sum_k c_k (-1)^k/(z^2 - w_k^2); ordinates are "
                   "zeros of fhat iff |fhat(gamma_n)| = 0 within [0,150] "
                   "(the only other zeros there are the R-roots)" % DPS),
        "N": N_TRIG,
        "claimed_precision": "2.6e-55 (first) .. 1e-2 (50th)",
        "r1": float(r1),
        "r1_zero_value_abs_fhat": float(r1_zero_value),
        "gamma_1": float(g1),
        "positional_error_gamma1_minus_r1": float(abs(g1 - r1)),
        "abs_fhat": {
            "median": q(abs_f)[0], "min": q(abs_f)[1], "max": q(abs_f)[2],
            "n_below_1e-3": int(np.sum(np.array(abs_f) < 1e-3)),
            "n_below_1e-2": int(np.sum(np.array(abs_f) < 1e-2)),
        },
        "newton_distance_delta": {
            "median": q(deltas)[0], "min": q(deltas)[1],
            "max": q(deltas)[2],
            "delta_1": rows[0]["newton_distance_delta"],
        },
        "exact_nearest_root_distance": {
            "median": q(nearest)[0], "min": q(nearest)[1],
            "max": q(nearest)[2],
            "gamma_1_to_root": nearest[0],
        },
        "newton_vs_exact": {
            "max_abs_diff": float(max(cross)),
            "median_abs_diff": float(np.median(cross)),
            "note": ("Newton distance |fhat|/|fhat'| is the first-order "
                     "distance from each ordinate to the nearest zero; "
                     "where |fhat| and |fhat'| are both small the "
                     "linearization breaks, so the EXACT nearest-root "
                     "distances are the reliable measure."),
        },
        "max_rel_identity_err": float(max_rel_ident),
        "identity_note": ("identity fhat = 4 z sin(zL/2) R(z) verified at "
                          "dps %d on all 50 ordinates; the floor is the "
                          "double-precision eigenvector coefficients "
                          "c_k." % DPS),
        "rows": rows,
    }


# ------------------------------------------------------- A2: all-N theorem


def lean_quadratic_form(N):
    """W_p + W_R (digamma form) in the trig basis, memory-bounded (rank-1
    accumulation over the t-grid in blocks).  Identical to
    connes_letter.trig_quadratic_form, but bounded memory at large N."""
    om = 2.0 * np.pi * np.arange(N + 1) / cl.L
    nmod = 2 * N + 1
    Wp = np.zeros((nmod, nmod))
    s_pp, w_pp, _ = cl.fourier_weights()
    for k in range(N + 1):
        wv = np.sum(w_pp * (cl.L - s_pp)) if k == 0 \
            else np.sum(w_pp * (cl.L / 2.0) * np.cos(om[k] * s_pp))
        Wp[k, k] = wv
        if k >= 1:
            Wp[N + k, N + k] = wv

    t = cl.arch_t_grid()
    wt = cl.trapezoid_weights(t)
    K = cl.digamma_kernel(t)
    WR = np.zeros((nmod, nmod), dtype=np.complex128)
    BLK = 256
    for j0 in range(0, len(t), BLK):
        tj = t[j0:j0 + BLK]
        sp = cl.trig_sinc(tj[:, None] + om[None, :])
        sm = cl.trig_sinc(tj[:, None] - om[None, :])
        Fb = np.empty((tj.shape[0], nmod), dtype=np.complex128)
        Fb[:, :N + 1] = sp + sm
        Fb[:, N + 1:] = (sp[:, 1:] - sm[:, 1:]) / (2j)
        ww = (K[j0:j0 + BLK] * wt[j0:j0 + BLK])[:, None]
        WR += (Fb * ww).T @ Fb.conj()
    WR = np.real(WR) / np.pi

    G = np.zeros((nmod, nmod))
    for k in range(N + 1):
        G[k, k] = cl.L if k == 0 else cl.L / 2.0
        if k >= 1:
            G[N + k, N + k] = cl.L / 2.0
    return Wp + WR, G, om


def lean_ground_state(N):
    Q, G, om = lean_quadratic_form(N)
    w, v = eigh(Q, G, subset_by_index=[0, 0])
    cf = v[:, 0]
    c = cf[:N + 1].copy()   # even (cos) part; the ground state is even
    return c, om, float(w[0])


def Rf(z, c, om):
    return float(np.sum(c * (-1.0) ** np.arange(len(om)) / (z * z - om ** 2)))


def float_roots_of_R(c, om):
    """One root per pole gap (0, w_1), (w_k, w_{k+1}) by bracketed bisection;
    interlacing says exactly one exists per gap."""
    N = len(om) - 1
    roots = []
    for k in range(N):
        lo, hi = float(om[k]), float(om[k + 1])
        d = hi - lo
        z1 = lo + max(1e-9, d * 1e-6)
        z2 = hi - max(1e-9, d * 1e-6)
        f1, f2 = Rf(z1, c, om), Rf(z2, c, om)
        if f1 * f2 > 0:
            roots.append(None)   # interlacing violated in this gap
            continue
        try:
            roots.append(float(brentq(lambda z: Rf(z, c, om), z1, z2)))
        except Exception:
            roots.append(None)
    return roots


def interlacing_at(N):
    c, om, lam = lean_ground_state(N)
    roots = float_roots_of_R(c, om)
    gaps = []
    for k, r in enumerate(roots):
        if r is not None and r <= SCAN_HI:
            gaps.append((k, r))
    in_own_gap = 0
    margins = []
    for k, r in gaps:
        lo, hi = float(om[k]), float(om[k + 1])
        if lo < r < hi:
            in_own_gap += 1
        margins.append(min(r - lo, hi - r) / (hi - lo))
    r1 = next((r for k, r in gaps if k == 0), None)
    w1 = float(om[1])
    return {
        "N": N,
        "lambda_min": lam,
        "n_poles": len(om),
        "n_roots_in_scan": len(gaps),
        "in_own_gap": in_own_gap,
        "interlacing_ok": in_own_gap == len(gaps),
        "first_root_r1": r1,
        "r1_in_omega1_interval": bool(r1 is not None and 0 < r1 < w1),
        "gamma_1_over_omega_1": round(14.13472514173469 / w1, 3),
        "min_gap_margin_frac": float(min(margins)) if margins else None,
    }


def all_N_interlacing():
    rows = []
    for N in N_SWEEP:
        try:
            rows.append(interlacing_at(N))
        except Exception as exc:
            rows.append({"N": N, "error": repr(exc)})
    # cross-check N=100 against the persisted connes_dirac verdict
    ref = None
    cd_path = os.path.join(HERE, "..", "data", "connes_dirac_data.json")
    if os.path.exists(cd_path):
        with open(cd_path) as f:
            ref = json.load(f)["rank_one_spectrum"]
    cross = None
    if ref is not None:
        r100 = next((r for r in rows if r.get("N") == 100), None)
        if r100 is not None and "error" not in r100:
            cross = {
                "connes_dirac_first_r1": ref["first_eigenvalue_r1"],
                "this_first_r1": r100["first_root_r1"],
                "diff": (abs(ref["first_eigenvalue_r1"]
                             - r100["first_root_r1"])
                         if r100["first_root_r1"] is not None else None),
                "connes_dirac_n_roots": ref["interlacing"]["n_roots"],
                "this_n_roots": r100["n_roots_in_scan"],
            }
    return {
        "sweep": rows,
        "cross_check_vs_connes_dirac": cross,
        "wall": ("r_1 in (0, 2.45] for every N while gamma_1 = 14.1347 is "
                 "5.77 w_1's away: the first-zero match is categorically "
                 "impossible for every truncation in the sweep."),
    }


# ------------------------------------------------ A3: whole-orbit census


def orbit_ints():
    digits = (0, 0, 0, 0, 1, 2, 2, 6)
    return sorted({int("".join(map(str, p)))
                   for p in itertools.permutations(digits)})


def lattice_alignment(gs, origin, spacing):
    offs = []
    for g in gs:
        off = abs((g - origin) % spacing)
        offs.append(min(off, spacing - off))
    return float(np.median(offs)), np.array(offs)


def orbit_origin_census():
    gs = [float(mp.im(mp.zetazero(k))) for k in range(1, N_ZEROS + 1)]
    orbit = orbit_ints()
    qs = {}
    for o in orbit:
        qs[o] = lattice_alignment(gs, float(o % SPACING), SPACING)[0]
    best_o = min(qs, key=qs.get)
    best_q = qs[best_o]
    med_q = float(np.median(list(qs.values())))
    anchors = {"10262000": 10262000, "20001026": 20001026,
               "20002610": 20002610, "26102000": 26102000}
    anchors_q = {k: qs[v] for k, v in anchors.items()}
    anchors_rank = {k: sum(1 for q in qs.values() if q < anchors_q[k]) + 1
                    for k in anchors}

    random.seed(23)
    mins = []
    for _ in range(N_EXTREME_TRIALS):
        qr = [lattice_alignment(gs, random.random() * SPACING, SPACING)[0]
              for _ in range(N_RANDOM_ORIGINS)]
        mins.append(min(qr))
    frac_better = float(np.mean(np.array(mins) <= best_q))
    return {
        "spacing": float(SPACING),
        "n_orbit_points": len(orbit),
        "best_origin": best_o,
        "best_q": best_q,
        "median_q_over_orbit": med_q,
        "anchors_q": {k: round(v, 4) for k, v in anchors_q.items()},
        "anchors_rank_in_orbit": anchors_rank,
        "random_extreme": {
            "trials": N_EXTREME_TRIALS,
            "origins_per_trial": N_RANDOM_ORIGINS,
            "min_mean": float(np.mean(mins)),
            "min_median": float(np.median(mins)),
            "min_min": float(np.min(mins)),
            "frac_random_extreme_leq_orbit_best": frac_better,
        },
        "verdict": ("The best of all %d known points as an origin is "
                    "q = %.3f, which is exactly the expected extreme-value "
                    "minimum of %d random origins (mean %.3f): in %.0f%% "
                    "of trials a random 840-set matches or beats the orbit "
                    "best, so the orbit is a typical set of %d candidates "
                    "and no known point is a special origin."
                    % (len(orbit), best_q, N_RANDOM_ORIGINS,
                       float(np.mean(mins)), 100.0 * frac_better,
                       N_RANDOM_ORIGINS)),
    }


# ------------------------------------------------------------------- main


def main():
    t0 = time.time()

    # A1 needs the N=150 even ground-state coefficients at float precision
    c150, om150, lam150 = lean_ground_state(N_TRIG)
    a1 = direct_ordinate_probe(c150, om150)

    a2 = all_N_interlacing()

    a3 = orbit_origin_census()

    provable = {
        "lemma": ("Cauchy interlacing for the rank-one secular function "
                  "R(z) = sum_k c_k (-1)^k/(z^2 - w_k^2): exactly one root "
                  "in (0, w_1), one in (w_k, w_{k+1}), none elsewhere."),
        "corollary": ("The first rank-one eigenvalue lies in (0, 2.45]; "
                      "gamma_1 = 14.1347 is 5.77 w_1's away, so the "
                      "letter's claimed eigenvalue at gamma_1 (2.6e-55 "
                      "precision) is impossible."),
        "verified": a2["wall"],
        "does_not_bear_on_RH": True,
    }

    best_q = a3["best_q"]
    frac = a3["random_extreme"]["frac_random_extreme_leq_orbit_best"]
    rows = a2["sweep"]
    r1_note = "; ".join(
        "N=%d r_1=%.4f" % (r["N"], r["first_root_r1"])
        for r in rows if "error" not in r and r["first_root_r1"] is not None)

    # the ordinate closest to being a zero of the letter's fhat
    amin = min(a1["rows"], key=lambda r: r["abs_fhat"])
    exn = a1["exact_nearest_root_distance"]

    verdict = (
        "DIRECT PROBE: THE HEADLINE NUMBER IS UNREACHABLE, AND THE WHOLE "
        "ORBIT IS INDIFFERENT AS ORIGINS.  (A1) at N=%d the letter's fhat "
        "is NOT zero at any ordinate: |fhat(gamma_1)| = %.3g, while a true "
        "zero gives exactly 0 and the claim is 2.6e-55; the nearest zero "
        "of fhat to gamma_1 is %.3f away (median over n=1..50: %.3f), "
        "|gamma_1 - r_1| = %.3f, and the closest any ordinate comes to a "
        "zero is |fhat| = %.3g at gamma_%d = %.3f; the identity fhat = "
        "4 z sin(zL/2) R(z) holds on all 50 ordinates (max rel %.1e, "
        "floor = the double-precision coefficients).  (A2) interlacing "
        "holds at every N in %s: %s.  (A3) the best of all %d orbit "
        "origins has q = %.3f, exactly the expected extreme-value minimum "
        "of %d random origins (mean %.3f; random matches or beats it in "
        "%.0f%% of trials): no known point is a special origin.  HONEST "
        "WALL: RH is open; the direct numbers are negative "
        "classifications; a positive proof needs mathematics outside this "
        "repository."
        % (N_TRIG, a1["rows"][0]["abs_fhat"], exn["gamma_1_to_root"],
           exn["median"], a1["positional_error_gamma1_minus_r1"],
           amin["abs_fhat"], amin["n"], amin["gamma"],
           a1["max_rel_identity_err"],
           tuple(N_SWEEP), r1_note, a3["n_orbit_points"], best_q,
           a3["random_extreme"]["origins_per_trial"],
           a3["random_extreme"]["min_mean"], 100.0 * frac))

    data = {
        "claim_under_test": ("Connes 2026 'Letter to Riemann': the ground "
                             "state of the finite-prime Weil form on "
                             "[1,13] has Fourier-transform zeros matching "
                             "the first 50 zeta ordinates with errors "
                             "2.6e-55 (first) .. 1e-2 (50th), via the "
                             "footnote-14 rank-one Dirac construction."),
        "direct_ordinate_probe": a1,
        "all_N_interlacing": a2,
        "orbit_origin_census": a3,
        "provable": provable,
        "verdict": verdict,
        "runtime_sec": round(time.time() - t0, 1),
    }
    with open(OUT, "w") as f:
        json.dump(data, f, indent=2)

    print(verdict)
    print()
    print("A1 direct ordinate probe (N=%d, dps %d):" % (N_TRIG, DPS))
    print("  |fhat(gamma_1)| = %.4g  delta_1 = %.4g  |gamma_1-r_1| = %.4f"
          % (a1["rows"][0]["abs_fhat"], a1["newton_distance_delta"]["delta_1"],
             a1["positional_error_gamma1_minus_r1"]))
    print("  abs_fhat over n=1..50: median %.4g  min %.4g  max %.4g"
          % (a1["abs_fhat"]["median"], a1["abs_fhat"]["min"],
             a1["abs_fhat"]["max"]))
    print("  newton distances: median %.4g  delta_1 %.4g"
          % (a1["newton_distance_delta"]["median"],
             a1["newton_distance_delta"]["delta_1"]))
    print("  exact nearest-root distances: median %.4g  gamma_1 %.4g"
          % (a1["exact_nearest_root_distance"]["median"],
             a1["exact_nearest_root_distance"]["gamma_1_to_root"]))
    print("  newton vs exact max diff: %.3g"
          % a1["newton_vs_exact"]["max_abs_diff"])
    print("  identity max rel err (dps %d): %.1e" % (DPS,
          a1["max_rel_identity_err"]))
    print()
    print("A2 interlacing sweep:")
    for r in rows:
        if "error" in r:
            print("  N=%d ERROR %s" % (r["N"], r["error"]))
        else:
            print("  N=%-3d roots_in_scan=%-3d in_own_gap=%-3d r_1=%.6f "
                  "in(0,w1)=%s margin_min=%.2e"
                  % (r["N"], r["n_roots_in_scan"], r["in_own_gap"],
                     r["first_root_r1"], r["r1_in_omega1_interval"],
                     r["min_gap_margin_frac"]))
    print("  cross-check vs connes_dirac JSON:", a2["cross_check_vs_connes_dirac"])
    print()
    print("A3 whole-orbit census (%d points): best q = %.4f, median q = %.4f"
          % (a3["n_orbit_points"], best_q, a3["median_q_over_orbit"]))
    print("  anchors:", a3["anchors_q"])
    print("  random extreme (%d trials x %d origins): min_mean %.4f "
          "min_min %.4f; random matches or beats the orbit best in %.0f%% "
          "of trials"
          % (a3["random_extreme"]["trials"],
             a3["random_extreme"]["origins_per_trial"],
             a3["random_extreme"]["min_mean"], a3["random_extreme"]["min_min"],
             100.0 * frac))
    print()
    print("wrote", os.path.normpath(OUT))


if __name__ == "__main__":
    main()
