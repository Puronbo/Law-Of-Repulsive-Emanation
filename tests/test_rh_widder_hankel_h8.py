"""Regression tests for experiments/rh_widder_hankel_h8.py.

The emphasis here is on the defects H8 found in its own earlier cuts, each
of which produced confident, self-consistent, wrong numbers:

  * a wrong `xi` whose imaginary part on the critical line manufactured ~110
    phantom zeros per 200 of height, so every max over the spectrum was
    measuring the wrong function;
  * an off-by-one in the window coordinate, s = off instead of s = 1 + off,
    which turned the asymptotic phase law into a spurious "~pi" and looked
    like a 2x failure;
  * reading the Q_1 divergence off critical-line partial sums rather than off
    the tail. Both moves were wrong, in opposite directions: the partial sums
    are bounded, and H9 later showed the full-spectrum tail converges too --
    Q_1 is FINITE, and it is H7b's N-weighted integral that diverges. So the
    divergence this bullet once described does not exist;
  * treating the ASYMPTOTIC phase law |phi|(s-1)/(s+1) as exact, and
    checking it to 1e-3 -- a tolerance that passes an approximation whose
    own error is O(phi^2) ~ 1e-5, hiding the distinction;
  * computing Q_m from a stored `q_real**2` raised to the m power, summing
    q^(2m) against an off-axis q^m;
  * bisecting Q_m for the witness order. Q_m OSCILLATES with period
    2 pi/theta in m and has no monotonicity, so bisection returns whichever
    crossing the bracket happens to contain.

Each is pinned below so it cannot recur silently.
"""

import json
import os

import mpmath as mp

import experiments.rh_widder_hankel_h8 as h8
import experiments.rh_widder_hankel_h9 as h9

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "experiments", "data", "rh_widder_hankel_h8_data.json")

mp.mp.dps = 30


def _report():
    with open(DATA, encoding="utf-8") as fh:
        return json.load(fh)


def test_artifact_exists_and_all_gates_pass():
    rep = _report()
    assert rep["gates"], "no gates recorded"
    assert all(g["passed"] for g in rep["gates"]), [
        g["gate"] for g in rep["gates"] if not g["passed"]]


def test_xi_is_real_on_the_critical_line():
    """REGRESSION: the wrong xi was complex there, and a sign-change scan over
    its real part produced phantoms. Reality is the precondition for the
    whole scan, so it is tested directly rather than only via the count."""
    assert h8.xi_is_real_on_critical_line() < mp.mpf("1e-25")


def test_zero_count_matches_riemann_von_mangoldt():
    """REGRESSION: 189 counted against 79 expected under the wrong xi."""
    ok, n, expected = h8.zero_count_is_plausible(mp.mpf(600))
    assert ok, "counted %d, Riemann-von Mangoldt predicts %.2f" % (n, expected)


def test_exact_identities_of_the_off_axis_pair():
    """H8a is an identity, not a fit: |w| = gamma^2+delta^2 and
    |q_off(|w|)| = 1/(4 gamma^2), both independent of delta."""
    for gam, d in ((mp.mpf(60), mp.mpf("1e-3")), (mp.mpf(150), mp.mpf("0.1"))):
        w = h8.w_of(gam, d)
        assert abs(abs(w) - (gam * gam + d * d)) < mp.mpf("1e-25")
        q = h8.q_off(abs(w), gam, d)
        assert abs(abs(q) - 1 / (4 * gam * gam)) < mp.mpf("1e-25")


def test_real_zeros_never_touch_the_envelope_at_x_equals_r():
    """At x = |w| the off-axis pair sits above every real zero's contribution,
    because g^2/(x+g^2)^2 = 1/(4x) only when g^2 = x."""
    G = h8.real_zeros(mp.mpf(300))
    gam, d = mp.mpf(60), mp.mpf("1e-3")
    x = abs(h8.w_of(gam, d))
    qo = abs(h8.q_off(x, gam, d))
    env = 1 / (4 * x)
    assert qo > env
    for g in G:
        assert abs(h8.q_real(x, g)) <= env
        assert abs(h8.q_real(x, g)) < qo


def test_dominance_ratio_matches_its_closed_form():
    """eta = 4 s^2/(1+s^2+delta^2/gamma^2)^2, equal to 1 only at
    g^2 + delta^2 = gamma^2."""
    for row in _report()["h8_identities"]:
        assert row["rel_err"] < 1e-15, row
        assert row["deficit_measured"] > 0, row


def test_discrete_window_exceeds_the_continuous_bound():
    """REGRESSION: the window is naturally in log s, not in a raw offset.
    Comparing off_max to exp(a) compares different quantities and yields a
    spurious ratio near 0.01."""
    for row in _report()["h8_window"]:
        assert row["half_over_cont"] > 1.0, row
        assert row["ladder_contiguous"], (
            "bisection assumes the admissibility predicate is contiguous in "
            "the offset; a flicker would silently give a non-maximal window")


def test_continuous_half_width_agrees_with_two_delta_over_gamma():
    for row in _report()["h8_window"]:
        assert abs(row["cont_half_width_log_s"] / row["two_delta_over_gamma"] - 1) < 1e-3


def test_phase_deviation_is_the_phi_squared_term_not_noise():
    """REGRESSION: the leading-order phase law was asserted EXACT and checked
    to 1e-3. Its own error is O(phi^2) ~ 1e-5, so the tolerance passed the
    approximation. Measuring (theta_exact/theta_asym - 1)/phi^2 across the
    whole phi range pins the neglected term to the phi^2 term of the atan
    expansion: it must be a CONSTANT, not noise."""
    dev = _report()["h8_phase_deviation_scaled"]
    assert len(dev) == 6, dev
    assert max(dev) / min(dev) < 3.0, dev
    # and the deviation must actually be nonzero, or there is nothing to pin
    assert min(dev) != 0.0, dev


def test_one_row_per_case_not_two_duplicate_lists():
    """REGRESSION: the bracket used to be stored TWICE, as h8_witness and
    h8_witness_scan, with the same six cases under overlapping field names
    (lb_best vs m_lower_bound, witness_m vs m_witness, m_phase_threshold_edge
    vs m_phase_edge).  Two copies of one measurement are two places for it to
    drift, and it did drift -- for three runs H8's copies of H9's tail numbers
    sat at 2.6e-5 while H9's were already 5.9958e-3.

    The consolidation keeps one canonical row per case under single names.
    The duplication is pinned absent here so it cannot quietly return.
    """
    rep = _report()
    for dead in ("h8_witness", "h8_witness_scan"):
        assert dead not in rep, "%s is a duplicate of h8_bracket" % dead
    rows = rep["h8_bracket"]
    assert len(rows) == 6, rows
    keys = set(rows[0])
    for forbidden in ("lb_best", "witness_m", "m_phase_threshold_edge"):
        assert forbidden not in keys, forbidden
    for needed in ("m_lower_bound", "m_witness", "m_phase_edge"):
        assert needed in keys, needed
    # one row per (gamma, delta): no case may appear twice
    seen = [(r["gamma"], r["delta"]) for r in rows]
    assert len(set(seen)) == len(seen), seen


def test_witness_is_bracketed_between_a_rigorous_bound_and_the_naive_infimum():
    """The reported witness is a bracket, not a claimed minimum. The lower
    bound A(m) <= 2 is rigorous because A is monotone; the witness is a
    genuine Q_m < 0 sitting above the naive infimum pi gamma/(4 delta)."""
    for row in _report()["h8_bracket"]:
        assert row["m_lower_bound"] is not None, row
        assert row["m_witness"] is not None, row
        assert row["m_witness"] >= row["m_lower_bound"], row
        # f = -cos(m theta) - A(m)/2 > 0  <=>  Q_m < 0
        assert row["f"] > 0.0, row
        assert row["witness_over_naive"] >= 1.0, row


def test_witness_order_decreases_with_delta_at_fixed_gamma():
    """The 1/delta law, tested as MONOTONICITY only.

    Deliberately NOT asserted: proportionality. That would need off_max to be
    delta-independent, and it is not -- off_max is set by where the squares
    g_k^2 happen to fall near x. An earlier cut asserted lb*delta is constant
    at fixed gamma and was false by a factor of ~12.
    """
    rows = _report()["h8_bracket"]
    by_gam = {}
    for row in rows:
        by_gam.setdefault(row["gamma"], []).append(row)
    for gam, group in by_gam.items():
        if len(group) > 1:
            ordered = sorted(group, key=lambda r: r["delta"])
            for lo, hi in zip(ordered, ordered[1:]):
                assert hi["m_witness"] < lo["m_witness"], (gam, lo, hi)


def test_lower_bound_is_flat_in_delta_so_it_cannot_diverge_as_one_over_delta():
    """REGRESSION: an earlier conclusion asserted the rigorous lower bound
    m_decay "diverges as 1/delta". Its own artifact contradicts that -- at
    fixed gamma the bound is essentially flat in delta (536 and 536 at
    gamma = 60, 6569 and 6530 at gamma = 150). A is built from the REAL
    spectrum, so its size is set by how nearly the squares g_k^2 land on x,
    not by the displacement of a hypothetical off-axis zero.

    The retraction is pinned here so the claim cannot return with the numbers
    unchanged: if m_decay ever really grows like 1/delta this fails, and
    that failure would be information rather than nuisance.
    """
    rows = _report()["h8_bracket"]
    by_gam = {}
    for row in rows:
        by_gam.setdefault(row["gamma"], []).append(row)
    checked = 0
    for gam, group in by_gam.items():
        if len(group) > 1:
            lbs = sorted(r["m_lower_bound"] for r in group)
            spread = lbs[-1] / lbs[0]
            # A 1/delta law at fixed gamma over a 10x change in delta would
            # force a spread of 10.  Anything far below that refutes it; the
            # bound is not required to be numerically flat.
            assert spread < 3.0, (gam, lbs)
            checked += 1
    assert checked >= 2, "no fixed-gamma pairs to check; the test is void"

    # and the conclusion must not claim the retracted law
    concl = _report()["conclusion"]
    assert "does NOT diverge as 1/delta" in concl, concl


def test_lower_bound_is_rigorously_valid_because_A_is_monotone():
    """m_lower_bound = min{m : sum_k rho_k^m <= 2} is only a valid bound if A
    is monotone DECREASING in m. Each rho_k is a fixed ratio < 1 there, so
    rho^m decreases; recomputed here directly rather than trusted."""
    gam, d = mp.mpf(150), mp.mpf("1e-1")
    w = h8.w_of(gam, d)
    r = abs(w)
    G = h8.real_zeros(mp.mpf(600))
    for row in _report()["h8_bracket"]:
        if row["gamma"] != float(gam) or row["delta"] != float(d):
            continue
        x = r * (1 + row["lb_at_frac"] * row["off_max"])
        qo = abs(h8.q_off(x, gam, d))
        rho = sorted((abs(h8.q_real(x, g)) / qo for g in G), reverse=True)[:8]
        assert all(rho[k] > rho[k + 1] for k in range(len(rho) - 1)), rho
        m = row["m_lower_bound"]
        assert sum(v ** m for v in rho) <= 2.0 + 1e-9
        assert sum(v ** (m - 1) for v in rho) > 2.0 - 1e-9
        return
    raise AssertionError("case not found in artifact")


def test_reindex_gate_tracks_the_corrected_tail_magnitudes():
    """REGRESSION: the divergence of Q_1 lives in the DENSITY tail, and
    integrating against N rather than dN makes it look ~170x larger and
    creeping upward with the ceiling. Partial sums over critical-line zeros
    alone are BOUNDED, so reading the divergence off them concludes the
    opposite of the truth.

    The correct m = 1 tail is 5.9958e-3, not 2.6e-5: H9's first correction
    omitted the Jacobian t from dt = t ds.  The threshold gate was blind to
    that because a bounded factor cannot change convergence.  Pin the closed
    form, so the magnitude cannot drift a second time."""
    rep = _report()["h8_reindex"]
    # H8 does not keep its own copy of these numbers.  H9 owns them; H8
    # records where to look and recomputes live.  The duplication is what let
    # H8 advertise 2.6e-5 for three runs after H9 had corrected to 5.9958e-3,
    # so the absence of a stale snapshot is itself part of what is pinned.
    assert "true_tail_m1" not in rep and "h7_tail_m1" not in rep, \
        "H8 must not re-store H9's tails; that duplication already drifted once"
    assert rep["tails_owner"].endswith("rh_widder_hankel_h9_data.json"), rep
    assert rep["tails_field"] == "h9_m1_tails", rep
    true_tail = rep["true_tail_m1_live"]
    h7_tail = rep["h7_tail_m1_live"]
    closed = float((mp.log(h9.T0 / (2 * mp.pi)) + 1) / (2 * mp.pi * h9.T0))
    assert abs(true_tail[-1] - closed) / closed < 1e-8, (true_tail, closed)
    assert true_tail[-1] > 1e-3, "the omitted Jacobian returns a factor-230 slip"
    # settled across ceilings, i.e. an actual limit rather than a drift
    assert abs(true_tail[-1] / true_tail[-2] - 1) < 1e-4, true_tail
    # H7b's N-weighted integral is far too big AND still creeping
    assert h7_tail[-1] > 1000 * true_tail[-1], (h7_tail[-1], true_tail[-1])
    assert h7_tail[-1] / h7_tail[0] > 1.02, h7_tail
    assert rep["critical_line_only"]["Q1"] < 1.0, \
        "critical-line truncation is bounded; that is the trap"
    assert rep["status"].startswith("WITHDRAWN BY H9b"), rep["status"]


def test_reindexed_kernel_starts_at_second_moment():
    """K_N = [Q_{i+j+2}] has smallest entry Q_2; section 3's H_2 needs the
    (finite) Q_1 and the re-indexing is withdrawn regardless."""
    rep = _report()["h8_reindex"]
    assert rep["critical_line_only"]["Q2"] < rep["critical_line_only"]["Q1"]


def test_conclusion_is_scoped_not_an_rh_claim():
    concl = _report()["conclusion"]
    assert "Nothing here proves or refutes RH" in concl
    assert "remains OPEN" in concl


def test_conclusion_does_not_claim_the_phase_law_is_exact():
    """The withdrawn claim must not survive in prose. The conclusion must
    call the leading-order phase law asymptotic and must NOT present the
    witness as an established exact minimum."""
    concl = _report()["conclusion"]
    assert "to leading order" in concl
    assert "exact minimum is not claimed" in concl