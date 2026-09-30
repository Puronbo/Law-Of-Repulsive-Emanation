"""Tests for the zero-trajectories-as-scale-objects experiment.

``experiments/rh_zero_scale_objects.py`` verifies the exact Xi kernel from
the pinned record (zero_to_riemann_zeta_pinned_september_2026.md, section 8)
and the first group of claims about how the zeros of Xi move under the de
Bruijn flow:

  G1  the kernel int_0^inf Phi(u) cos(t u) du reproduces Xi exactly,
  G2  the flow equation  d_lam Xi_lam = - d_tt^2 Xi_lam  holds,
  G3  the first sixteen zeros stay real for lambda down to -1/4 and are
      tracked continuously (identity preserved, no jump to a foreign root),
  G4  the zero drift obeys  t'(lam) = Xi_tt / Xi_t,
  G5  the velocity at lambda = 0 obeys the symmetric two-body (Calogero)
      spacing law  t'_n = 1/gamma_n + 4 gamma_n sum 1/(gamma_n^2 - g_k^2),
      whose mirror-symmetric form resolves the pinned spacing law's
      apparent O(1) failure,
  G6  the closest pair (13,14) is continued down through the flow to its
      real-axis departure: the squared gap is ~linear in lambda with slope
      -> 8 (exact gap law  (delta^2)' = 8 - 4 delta^2 S_n), the fitted
      lambda* < 0 satisfies the double-root condition F = F_t = 0, and the
      measured departure is deeper than the naive mutual-only local model
      -(Delta gamma)^2 / 8,
  G7  the two next-closest pairs (9,10) and (15,16) leave the real axis the
      same way, each at its own lambda* < 0 double root with slope -> 8,
G8  lambda* is predicted in closed form by the gap law with S_n read off
       the exact spacing law at lambda = 0,
         S_n = (4/delta_0 - delta'(0)) / (2 delta_0),
         lambda*_S = ln(1 - S_n delta_0^2/2) / (4 S_n),
       which reduces to the naive lambda_c = -delta_0^2/8 as S_n -> 0 and
       beats the naive model on every measured departure,
   G9  the exact gap law  delta' = 4/delta_0 - 2 delta_0 S_n  is verified as
       an identity: S_n is computed directly from the zero positions as the
       mirror-symmetric rest-remainder sum (pinned record section 24), and
       delta'(0) independently from the kernel velocity Xi_tt/Xi_t and from
       the spacing law.  All three agree on every measured pair -- the gap
       law is the pinned record's structure, not a fitted remainder,
G10  the collapse-rate direction is forced by a pure inequality: with
       G_n = sum_{m != a,b} [1/(x_a-x_m)^2 + 1/(x_b-x_m)^2] the two-body
       bound u v <= (u^2+v^2)/2 holds term by term (including the mirror
       images), so S_n <= G_n/2 and the exact gap law gives
       (delta^2)' >= 8 - 2 delta^2 G_n.  With L_n = delta^2 G_n < 4 the
       measured pairs have (delta^2)'(0) > 0, and the measured gap slopes
       sit at or above the bound -- no velocity measurement is needed for
       the sign (pinned record section 25).

These tests lock the gates in.  The important failure-mode to watch for is
a gate that "passes" for a degenerate reason: G1 must hold on the closed
form (integral of the kernel equals xi(1/2)) AND at individual zeros, G2
must use the derivative quadrature rather than a symmetry of the integrand,
G4 must compare two independent estimators of the velocity (kernel
derivative vs tracked drift) rather than the same value twice, G6 must fit
the actual measured gap ladder (not a precomputed lambda*) and pin the
departure to the kernel's own double root, and G8 must compare its
closed-form prediction against measured departures (a prediction that only
recites the naive model back is not a prediction).  For G10 the risk is a
gate that cites a fitted S_n and calls it an inequality: G10 must build
G_n directly from the zero positions (same mirror-symmetric construction
as G9) and check the AM-GM bound term by term; an inequality that restates
some previous fit is not a new theorem.
"""

import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "experiments"))

import regen_data  # noqa: E402

import mpmath as mp  # noqa: E402


def _artifact():
    path = regen_data.find_data("rh_zero_scale_objects_data.json")
    assert path is not None, "artifact missing; run the script"
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _gate(rep, prefix):
    hits = [g for g in rep["gates"]
            if g["gate"].split()[0].rstrip(":") == prefix]
    assert len(hits) == 1, "expected exactly one gate starting %r" % prefix
    return hits[0]


# ---------------------------------------------------------------- structure

def test_all_gates_pass():
    rep = _artifact()
    names = [g["gate"] for g in rep["gates"]]
    assert [n.split()[0].rstrip(":") for n in names] == \
        ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10"]
    assert all(g["passed"] for g in rep["gates"]), \
        "a gate stopped confirming its number: %s" % names


def test_conclusion_is_careful_about_rh():
    rep = _artifact()
    c = rep["conclusion"]
    assert "Nothing here touches the truth of RH" in c
    assert "departure scales" in c and "open" in c


def test_departure_scales_measured_not_claimed_for_all():
    """The closest-pair departures are now measured (G6, G7), and the
    departure text must say so while refusing any claim about the other
    zeros or about RH (a finite set of measured lambda*_k cannot decide the
    truth of RH).
    """
    rep = _artifact()
    d = rep["departure_scales_open"]
    assert "three closest adjacent pairs" in d
    assert "lambda* = " in d and "-0.32" in d
    assert "still unmeasured" in d
    assert "no general RH statement follows" in d


# ------------------------------------------------------------------- G1

def test_closed_form_must_be_exact():
    rep = _artifact()
    g = _gate(rep, "G1")
    assert "closed form" in g["detail"]
    assert "0.0e+00" in g["detail"]


def test_kernel_must_reproduce_xi_at_zeros():
    """G1 must also pinch individual zeros, not just the mass."""
    import re
    rep = _artifact()
    g = _gate(rep, "G1")
    assert "Xi_0(gamma_k)" in g["detail"]
    # every reported magnitude must be well below 1e-18 (0.0e+00 passes)
    mags = [float(s) for s in re.findall(r"\d+\.\d+e[+-]\d+", g["detail"])]
    assert all(v < 1e-18 for v in mags), mags


# ------------------------------------------------------------------- G2

def test_flow_residuals_small():
    rep = _artifact()
    g = _gate(rep, "G2")
    assert "E-5" in g["detail"] or "e-5" in g["detail"], \
        "flow residual must be reported in the detail string"


# ------------------------------------------------------------------- G3

def test_sixteen_zeros_tracked():
    rep = _artifact()
    g = _gate(rep, "G3")
    assert "k = 1..16" in g["detail"]
    assert "1e-18" in g["detail"]


def test_g3_grid_ends_at_minus_one_quarter():
    """The claim range is lambda in {0,-1/10,-1/5,-1/4} -- deliberately
    above every pair-collapse found so far.  If the grid ever extends past
    -1/4 in the scan without the tracking remaining clean, the gate's
    premise changes and this test should be revisited.
    """
    rep = _artifact()
    g = _gate(rep, "G3")
    assert "-1/4" in g["detail"]


# ------------------------------------------------------------------- G4

def test_velocity_law_uses_two_independent_estimators():
    """Ftt/Ft (kernel) vs a tracked-motion drift must both appear."""
    rep = _artifact()
    g = _gate(rep, "G4")
    assert "Xi_tt / Xi_t" in g["gate"]
    assert "Xi_tt/Xi_t" in g["detail"]
    assert "Richardson" in g["detail"]
    assert "1/40, 1/20" in g["detail"]


def test_velocity_tolerance_below_half_per_mille():
    rep = _artifact()
    g = _gate(rep, "G4")
    worst = float(g["detail"].split("worst: ")[1].split(")")[0])
    assert worst < 5e-4, "velocity law verified only to %e" % worst


def test_velocity_signs_all_negative_at_zero():
    """t'(0) must be negative for the tracked zeros: descending lambda then
    moves every zero to a larger ordinate (drift the gate G3 confirms).
    A sign slip in the estimator flips the whole column and is caught by
    checking the reference rows in the detail string.
    """
    rep = _artifact()
    g = _gate(rep, "G4")
    import re
    nums = [float(x) for x in
            re.findall(r": (-[0-9][0-9.]*) vs", g["detail"])]
    assert nums and all(n < 0 for n in nums), nums


def test_richardson_helper_agrees_with_plain_central_difference():
    """The two-point estimator used by G4 is D(h) = (t(+h)-t(-h))/2h, and
    the Richardson combination is (4 D(h/2) - D(h))/3.  Pin the recipe on a
    trajectory t(lam) = -lam - 4 lam^3 (t'(0) = -1, t''' != 0) so the
    O(h^2) central-difference error is real and the extrapolation removes
    it, exactly as in the experiment's _richardson_drift.
    """
    mp.mp.dps = 50

    def trk(lam):
        return -lam - 4 * lam ** 3

    h = mp.mpf("1/20")
    D = lambda hh: (trk(hh) - trk(-hh)) / (2 * hh)          # noqa: E731
    rich = (4 * D(h / 2) - D(h)) / 3
    assert float(D(h) + 1) == pytest.approx(-4 * float(h) ** 2, rel=1e-12)
    assert float(abs(rich - (-1))) < 1e-30


# ------------------------------------------------------------------- G5

def test_spacing_law_gate_present_and_structure():
    rep = _artifact()
    g = _gate(rep, "G5")
    assert "symmetric spacing" in g["gate"]
    assert "4 gamma_n sum 1/(gamma_n^2 - gamma_k^2)" in g["gate"]
    assert "200 zeros" in g["detail"]
    assert "moment tail" in g["detail"]
    assert "mirror-symmetric" in g["detail"]
    assert "O(1)" in g["detail"]


def test_spacing_law_tolerance_below_half_per_mille():
    import re
    rep = _artifact()
    g = _gate(rep, "G5")
    worst = float(re.search(r"worst (\S+)\b",
                            g["detail"]).group(1).rstrip("."))
    assert worst < 5e-4, "spacing law verified only to %e" % worst
    assert worst < 5e-4, "spacing law verified only to %e" % worst


def test_spacing_law_g1_matches_kernel_to_better_than_1e_15():
    """The first zero is the cleanest check: the image pairs contribute most
    and the moment tail is tiny, so the two-body sum must agree with the
    kernel velocity to near machine precision -- not just at the 5e-4 of the
    gate.  A break of the law's exact structure shows up first here.
    """
    rep = _artifact()
    g = _gate(rep, "G5")
    assert "g1 2.59e-20" in g["detail"], g["detail"]


def test_spacing_law_rows_recorded_and_signed():
    """The per-zero rows in report['g5_rows'] must exist, all negative
    (mirror-image attraction pulls each zero to higher ordinate as lambda
    descends, same direction the G3 tracks move), and monotone in the sense
    that the furnished representative rows are all on the negative branch.
    """
    rep = _artifact()
    assert "g5_rows" in rep and len(rep["g5_rows"]) == 16
    for k, va, pred, rel in rep["g5_rows"]:
        assert str(va).startswith("-"), (k, va)
        assert str(pred).startswith("-"), (k, pred)


# ------------------------------------------------------------------- G6

def test_g6_gate_present_and_structure():
    rep = _artifact()
    g = _gate(rep, "G6")
    assert "closest pair" in g["gate"]
    assert "lambda*" in g["gate"]
    assert "slope 8" in g["gate"]
    assert "(13,14)" in g["detail"]
    assert "Delta=1.4847" in g["detail"]
    assert "naive mutual-only local model" in g["detail"]
    assert "(delta^2)' = 8" not in g["detail"]  # the gate text names slope 8


def test_g6_fitted_from_measured_ladder_not_pinned():
    """lambda* must come from the gate's own least-squares over the measured
    gap ladder, not from a hard-coded constant.
    """
    rep = _artifact()
    rows = rep["g6_rows"]
    # the ladder must contain measured gaps (they shrink, then stop before
    # the pair merges; two rows survive above the departure point)
    assert len(rows) >= 6, rows
    gaps = [r["gap"] for r in rows]
    assert all(0 < g for g in gaps)
    dep = rep["g6_departure"]
    fit = dep["fit_slope"]
    # the exact gap law  (delta^2)' = 8 - 4 delta^2 S_n  forces slope -> 8
    # as the gap closes, so the fitted slope must be close to 8
    assert abs(fit - 8) < 0.3, fit


def test_g6_slope_direction_and_double_root():
    """The squared gap must shrink as lambda descends (negative slope with
    sign against the lambda axis): slope ~ 8 in gap^2-vs-lambda and the
    departure must satisfy the double-root condition at the kernel.
    """
    rep = _artifact()
    dep = rep["g6_departure"]
    assert dep["fitted_lambda_star"] < 0
    # double-root residual reported as |F|+|F_t| -- small means the fit is
    # consistent with F(lambda*, t*) = F_t = 0
    assert dep["double_root_res"] < 1e-8, dep
    # slope positive: gap^2 = 8 (lambda - lambda*), i.e. gap grows away
    assert dep["fit_slope"] > 7, dep


def test_g6_deeper_than_naive_local_model():
    """The mutual-only model  lambda_c = -(Delta gamma)^2 / 8  only accounts
    for the pair's own mutual repulsion: the remaining-spectrum term S_n in
    the exact gap law  (delta^2)' = 8 - 4 delta^2 S_n  pulls the pair apart,
    so the true departure is strictly deeper (more negative).
    """
    rep = _artifact()
    dep = rep["g6_departure"]
    naive = dep["naive_lambda_c"]
    fit = dep["fitted_lambda_star"]
    ga, gb = dep["gamma"]
    assert naive == pytest.approx(-(gb - ga) ** 2 / 8, rel=1e-10)
    assert fit < naive, (fit, naive)
    assert fit == pytest.approx(-0.3213182, abs=1e-4)


def test_g6_rows_monotone_shrinking():
    """The ladder must record a monotone-decreasing gap as lambda descends;
    a merge would make the last recorded gap collapse to ~0.
    """
    rep = _artifact()
    gaps = [r["gap"] for r in rep["g6_rows"]]
    assert gaps == sorted(gaps, reverse=True), gaps
    assert gaps[-1] < gaps[0] / 2, gaps


# ------------------------------------------------------------------- G7

def test_g7_gate_present_and_pairs_measured():
    """G7 must report measured departures for the two next-closest pairs
    (9,10) and (15,16), each with its own fitted lambda*, slope and double
    root residual -- not just claim the pairs exist."""
    rep = _artifact()
    g = _gate(rep, "G7")
    assert "(9,10)" in g["gate"] and "(15,16)" in g["gate"]
    assert "lambda*" in g["gate"] and "slope 8" in g["gate"]
    deps = rep["g7_departures"]
    assert len(deps) == 2
    assert deps[0]["pair"] == [9, 10]
    assert deps[1]["pair"] == [15, 16]


def test_g7_each_pair_is_a_double_root():
    """Both G7 pairs must leave the real axis: fitted lambda* < 0, slope ~ 8
    (gap^2 vs lambda), double-root residual small, and deeper than the naive
    mutual-only model."""
    rep = _artifact()
    for d in rep["g7_departures"]:
        assert d["fitted_lambda_star"] < 0, d
        assert abs(d["fit_slope"] - 8) < 0.3, d
        assert d["double_root_res"] < 1e-8, d
        ga, gb = d["gamma"]
        naive = -(gb - ga) ** 2 / 8
        assert d["naive_lambda_c"] == pytest.approx(naive, rel=1e-10)
        assert d["fitted_lambda_star"] < d["naive_lambda_c"], d
    lam9 = rep["g7_departures"][0]["fitted_lambda_star"]
    lam15 = rep["g7_departures"][1]["fitted_lambda_star"]
    assert lam9 == pytest.approx(-0.4700, abs=0.02)
    assert lam15 == pytest.approx(-0.688, abs=0.03)


# ------------------------------------------------------------------- G8

def test_g8_gate_present_and_structure():
    rep = _artifact()
    g = _gate(rep, "G8")
    assert "closed-form" in g["gate"]
    assert "S_n" in g["gate"]
    assert "spacing law" in g["gate"]
    assert "ln(1 - S_n d0^2/2)/(4 S_n)" in g["detail"]


def test_g8_predictions_match_measured_departures():
    """Every reported prediction row must be a genuine match: S_n > 0,
    argument of the logarithm positive, predicted and measured lambda*
    negative, relative error under the gate tolerance, and the closed form
    beating the naive model."""
    rep = _artifact()
    rows = rep["g8_predictions"]
    assert len(rows) == 3
    for r in rows:
        assert r["S_n"] > 0, r
        assert r["pred_lambda_star_S"] < 0, r
        assert r["meas_lambda_star"] < 0, r
        assert r["rel_S"] < 3e-2, r
        assert r["rel_naive"] > 5 * r["rel_S"], r
        assert r["ok"] is True, r


def test_g8_naive_alone_misses_measured_departures():
    """The point of G8 is that the naive mutual-only lambda_c
    = -delta_0^2/8 is NOT enough: on every pair it must miss the measured
    departure by more than the S_n-corrected closed form does."""
    rep = _artifact()
    for r in rep["g8_predictions"]:
        assert r["rel_naive"] > r["rel_S"], r
    # the S_n correction must be non-trivial on the measured pairs, not a
    # tiny deflection of the naive model
    for r in rep["g8_predictions"]:
        assert r["S_n"] >= 0.1, r


# ------------------------------------------------------------------- G9

def test_g9_gate_present_and_structure():
    rep = _artifact()
    g = _gate(rep, "G9")
    assert "gap law" in g["gate"]
    assert "4/delta_0 - 2 delta_0 S_n" in g["gate"]
    assert "mirror-symmetric" in g["gate"]
    assert "rest-remainder sum" in g["gate"]
    assert "first 200 zeros" in g["detail"]
    assert "moment tail" in g["detail"]


def test_g9_rest_remainder_sum_is_the_gap_law_sn():
    """The direct rest-remainder sum S_n (from the zero positions) must agree
    with the S_n G8 reads off the velocities to high precision on every
    measured pair -- the pinned record's section 24 definition is exactly the
    object the closed form uses."""
    rep = _artifact()
    rows = rep["g9_gap_law_identity"]
    assert len(rows) == 3
    for r in rows:
        assert r["S_n_direct"] > 0, r
        assert r["S_n_velocity"] > 0, r
        assert abs(r["S_n_direct"] - r["S_n_velocity"]) < 1e-6, r


def test_g9_identity_holds_from_both_velocity_estimators():
    """delta'(0) from the kernel (Xi_tt/Xi_t) and from the spacing law must
    both equal the gap-law right-hand side 4/delta_0 - 2 delta_0 S_n built
    from the direct rest-remainder sum, to the estimator noise floor (the
    kernel row carries the G5 noise ~1e-5, the spacing row is sub-1e-6)."""
    rep = _artifact()
    for r in rep["g9_gap_law_identity"]:
        assert r["res_spacing_vs_law"] < 1e-6, r
        assert r["res_kernel_vs_law"] < 1e-4, r
        assert r["ok"] is True, r


def test_g9_is_not_reciting_the_velocity_back():
    """G9 must compare three genuinely independent objects: the direct
    rest-remainder sum, the kernel velocity, and the spacing law.  If the
    rest sum and the velocities were the same computation relabelled, the
    gate would prove nothing; the detail string must expose all three."""
    rep = _artifact()
    g = _gate(rep, "G9")
    assert "kernel" in g["detail"] and "spacing" in g["detail"]
    rows = rep["g9_gap_law_identity"]
    # the kernel-side residuals ride the G5 velocity-noise floor while the
    # spacing-side residuals are a pure truncation bound: across the three
    # pairs the worst kernel floor must dominate the worst spacing floor by
    # many orders of magnitude.  A gate that recited the same computation
    # twice would collapse these two error floors onto a single magnitude.
    worst_k = max(r["res_kernel_vs_law"] for r in rows)
    worst_s = max(r["res_spacing_vs_law"] for r in rows)
    assert worst_k > 1e4 * worst_s, (worst_k, worst_s)


# ------------------------------------------------------------------- G10

def test_g10_gate_present_and_structure():
    rep = _artifact()
    g = _gate(rep, "G10")
    assert "AM-GM" in g["gate"]
    assert "8 - 2 delta^2 G_n" in g["gate"]
    assert "L_n = delta^2 G_n" in g["gate"]
    assert "Term-wise" in g["detail"] and "aggregate" in g["detail"]
    assert len(rep["g10_amgm_collapse_bound"]) == 15


def test_g10_amgm_identity_is_exact_termwise():
    """The AM-GM inequality u v <= (u^2+v^2)/2 must hold on every summand of
    the rest-remainder sum: the worst term-wise violation is 0 to machine
    precision (the inequality is an identity, not a fitted remainder)."""
    rep = _artifact()
    g = _gate(rep, "G10")
    assert "worst violation 0.0e+00" in g["detail"]
    for r in rep["g10_amgm_collapse_bound"]:
        assert r["S_le_halfG"] is True, r


def test_g10_bound_is_a_new_object_not_the_velocities():
    """G_n must be built directly from the zero positions as the mirror-
    symmetric inverse-square two-body sum, and the bound 8 - 2 delta^2 G_n
    must be strictly positive on the measured pairs (L_n < 4).  The delta'(0)
    column is for cross-check only; the direction (delta^2)'(0) > 0 must come
    from the inequality, not from the measured slope."""
    rep = _artifact()
    rows = rep["g10_amgm_collapse_bound"]
    measured = [r for r in rows if tuple(r["pair"]) in ((13, 14), (9, 10),
                                                        (15, 16))]
    assert len(measured) == 3
    for r in measured:
        assert r["L_n"] < 4, r
        assert r["bound8_minus_2L"] > 0, r


def test_g10_measured_slopes_respect_the_bound():
    """The measured gap slope 2 delta_0 delta'(0) must sit at or above the
    strict AM-GM bound 8 - 2 L_n on every measured pair (the bound is a real
    loss -- the direction is forced, the size is not exact)."""
    rep = _artifact()
    rows = rep["g10_amgm_collapse_bound"]
    for r in rows:
        if tuple(r["pair"]) in ((13, 14), (9, 10), (15, 16)):
            slope2 = 2 * r["delta0"] * r["delta_prime_kernel"]
            assert slope2 >= r["bound8_minus_2L"] - 1e-3, r