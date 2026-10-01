"""Tests for the Widder/Hankel H4 experiment.

``experiments/rh_widder_hankel_h4.py`` does not try to prove or refute RH.  It
asks a question about METHOD that the pinned records raise and then step past.
``rh_widder_stieltjes_explicit_details.md`` section 18 offers an "eventual"
criterion and hedges it -- "If this sparse/eventual criterion is rigorously
sufficient under the relevant analytic hypotheses, then RH follows" -- while
section 23.5 warns that "an off-line zero does not automatically dominate every
Widder sum", section 20 notes that a small displacement only postpones the
contradiction to higher Widder order, and section 24 names "fix x > 0 and
analyze the asymptotic spectrum" as the sharpest next calculation.  H1--H3 all
sampled the criterion.  H4 measures how far out of reach its counterexamples
are.  The sub-gates:

  H4a  for a zero displaced by delta the transformed scale is
       w = gamma^2 - delta^2 - 2i delta gamma, so q(x) = w/(x+w)^2 has phase
       arg q = arg w - 2 arg(x+w) -> -arg w = atan(2 delta gamma/(gamma^2 -
       delta^2)) ~ 2 delta/gamma,
  H4b  a strictly dominant pair contributes 2 Q^m cos(m theta), so the first
       violating order is m_first ~ pi/(2 theta) ~ pi gamma/(4 delta),
  H4c  at delta = 1e-3 no point of a finite x-grid violates up to m = 200, and
       at delta = 1e-4 no violation exists at all below the order cap,
  H4d  displacing a higher zero confines the violating x to a narrow band,
  H4e  a dominant off-axis pair DOES break eventual positivity, so the
       criterion is not vacuous -- it is merely out of reach.

The failure-modes watched for here:

* **A vacuous gate.** No gate may assert ``True`` unconditionally; every gate
  detail must carry a recorded numeric claim.
* **The factor-of-two trap (H4a/H4b).** Since q(0) = w/w^2 = 1/w, the phase is
  ``-arg w``, i.e. ``2 delta/gamma`` and NOT ``delta/gamma``.  A first cut that
  predicts ``delta/gamma`` is wrong by exactly a factor of two and every
  downstream constant (``gamma/2`` instead of ``pi gamma/4``) shifts with it.
  The tests pin the phase law numerically and check the amplification constant
  against ``pi gamma/4`` directly, so a repeat of that error fails loudly.
* **The float-round-trip trap (H4b).** ``mp.mpf(0.1)`` reconstructed from the
  float ``0.1`` is ``0.1000000000000000055...``, i.e. strictly greater than
  ``mp.mpf("0.1")``.  Selecting the asymptotic regime by comparing
  float-stored deltas against an exact ``mpf`` threshold silently drops a row
  and the fit is fitted to the wrong subset.  The test requires the recorded
  delta to round-trip exactly.
* **The "smaller violation is weaker evidence" trap (H4c/H4d).** Finding no
  violation must NOT be reported as partial support for RH.  The tests pin the
  zero-violation counts AND require the conclusion to say a clean scan carries
  no evidential weight.
* **Honesty.** H4 must not claim to refute the framework or to settle the
  prime-gamma -> Hankel bridge; it must keep naming section 27 as open.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "experiments"))

import mpmath as mp  # noqa: E402

import regen_data  # noqa: E402
import rh_widder_hankel_h4 as h4  # noqa: E402


def _artifact():
    path = regen_data.find_data("rh_widder_hankel_h4_data.json")
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
        ["H4a", "H4b", "H4c", "H4d", "H4e"]
    assert all(g["passed"] for g in rep["gates"]), \
        "a gate stopped confirming its number: %s" % names


def test_no_gate_is_trivially_passing():
    """Anti-vacuity: every gate detail must carry a recorded numeric claim."""
    rep = _artifact()
    for g in rep["gates"]:
        d = g["detail"]
        assert any(ch.isdigit() for ch in d), \
            "gate %r has no recorded number: %r" % (g["gate"], d)
        assert len(d) > 200, \
            "gate %r detail is too thin to be a real check" % g["gate"]


def test_conclusion_is_about_method_not_zeta():
    rep = _artifact()
    c = rep["conclusion"]
    assert "NOTHING HERE PROVES" in c
    assert "REFUTES RH" in c
    assert "remains OPEN" in c
    assert "statement about METHOD, not about zeta" in c
    assert "may still be correct and sufficient" in c


# ------------------------------------------------------------------- H4a

def test_phase_law_is_two_delta_over_gamma():
    """q(0) = 1/w, so arg q = -arg w ~ 2 delta/gamma -- NOT delta/gamma."""
    rep = _artifact()
    rows = rep["h4_phase_rows"]
    assert len(rows) >= 3, "phase law not sampled"
    for r in rows:
        assert "two_delta_over_gamma" in r, \
            "H4a must record the factor-2 prediction, got %r" % r
        assert r["rel"] < 5e-3, \
            "arg q deviates from 2 delta/gamma by %.2e at delta=%r" \
            % (r["rel"], r["delta"])


def test_phase_law_is_not_the_factor_of_two_error():
    """Recompute the phase independently: arg q must be ~2*delta/gamma, and
    must be visibly inconsistent with delta/gamma."""
    g1 = h4.GAMMAS[0]
    for d in (mp.mpf("1e-3"), mp.mpf("1e-2"), mp.mpf("1e-1")):
        w = h4._w(g1, d)
        x = mp.mpf("1e-6")
        th = abs(mp.arg(h4._q(w, x)))
        assert abs(th - 2 * d / g1) < 1e-3 * (2 * d / g1), \
            "arg q != 2 delta/gamma at delta=%s (got %s)" % (d, th)
        # the wrong prediction differs by a factor of two: the deviation from
        # delta/gamma is theta/2, i.e. 49-51% of theta
        dev_wrong = abs(th - d / g1) / th
        assert mp.mpf("0.49") < dev_wrong < mp.mpf("0.51"), \
            "deviation from the wrong law is %.4f of theta, not theta/2 " \
            "(delta=%s)" % (float(dev_wrong), d)
        # and the correct law holds to much better than 1%
        assert abs(th - 2 * d / g1) / th < 1e-2


# ------------------------------------------------------------------- H4b

def test_amplification_constant_is_pi_gamma_over_four():
    rep = _artifact()
    rows = [r for r in rep["h4_amplification_rows"] if r["m_first"]]
    assert rows, "no amplification rows recorded"
    pred = mp.pi * h4.GAMMAS[0] / 4
    assert abs(mp.mpf(rep["h4_amplification_pred"]) - pred) < 1e-9, \
        "recorded prediction constant %r != pi gamma/4" \
        % rep["h4_amplification_pred"]
    lin = [r for r in rows if mp.mpf(r["delta_exact"]) <= h4.H4_LINEAR]
    assert len(lin) == 3, \
        "expected 3 small-angle rows in %r" % [r["delta"] for r in rows]
    for r in lin:
        rel = abs(mp.mpf(r["m_first_times_delta"]) - pred) / pred
        assert rel < 5e-2, \
            "m_first*delta deviates from pi gamma/4 by %.2e at delta=%r" \
            % (rel, r["delta"])


def test_delta_round_trips_exactly():
    """The float round-trip trap: mpf(float(0.1)) > mpf('0.1'), which silently
    dropped a row from the asymptotic fit in a first cut."""
    assert mp.mpf(0.1) > mp.mpf("0.1"), \
        "mpf float round-trip behaviour changed; the guard no longer applies"
    rep = _artifact()
    for r in rep["h4_amplification_rows"]:
        assert r["delta_exact"] is not None, \
            "rows must record the exact delta so the regime test is stable"
        back = mp.mpf(r["delta_exact"])
        assert abs(back - mp.mpf(repr(r["delta"]))) < 1e-12 or \
            abs(back - mp.mpf(r["delta"])) < 1e-12, \
            "delta_exact %r is inconsistent with delta %r" \
            % (r["delta_exact"], r["delta"])


def test_m_first_matches_pi_over_two_theta():
    """m_first is measured independently of the law, and must agree with the
    pair-model prediction pi/(2 theta) in the small-angle regime."""
    rep = _artifact()
    rows = [r for r in rep["h4_amplification_rows"]
            if r["m_first"] and mp.mpf(r["delta_exact"]) <= h4.H4_LINEAR]
    assert rows
    for r in rows:
        rel = abs(r["m_first"] - r["pi_over_2theta"]) / r["pi_over_2theta"]
        assert rel < 5e-2, \
            "measured m_first %r disagrees with pi/(2 theta)=%r by %.2e" \
            % (r["m_first"], r["pi_over_2theta"], rel)


# ------------------------------------------------------------------- H4c

def test_small_displacement_is_invisible_on_a_finite_grid():
    rep = _artifact()
    inv = rep["h4_invisible"]
    assert inv["delta"] == 1e-3
    assert inv["n_violated"] == 0, \
        "H4c claims a small displacement is invisible, but %d grid points " \
        "violate" % inv["n_violated"]
    assert inv["n_grid"] > 20, "the x-grid is too coarse to mean anything"


def test_tiny_displacement_exceeds_the_order_cap():
    """At delta = 1e-4 the search must find NOTHING below the cap -- the
    violation is predicted to sit above it.  A reported violation here would
    mean the barrier claim is wrong."""
    rep = _artifact()
    inv = rep["h4_invisible"]
    assert inv["delta_1e4_m_first_within_cap"] is None, \
        "delta=1e-4 produced m_first=%r within the cap, so the claimed " \
        "barrier does not hold" % inv["delta_1e4_m_first_within_cap"]
    assert inv["delta_1e4_predicted_m_first"] > inv["order_cap"], \
        "predicted m_first %.3g should exceed the cap %d" \
        % (inv["delta_1e4_predicted_m_first"], inv["order_cap"])
    assert inv["delta_1e4_predicted_m_first"] > 1e5, \
        "the barrier is only interesting above 1e5, got %.3g" \
        % inv["delta_1e4_predicted_m_first"]


def test_no_violation_is_not_evidence_for_rh():
    """The 'clean scan' trap: zero violations must be reported as absence of
    discriminating power, never as support."""
    rep = _artifact()
    c = rep["conclusion"]
    assert "NO evidential weight" in c
    assert "certifies nothing" in _gate(rep, "H4c")["detail"]


# ------------------------------------------------------------------- H4d

def test_violating_band_can_be_narrow():
    rep = _artifact()
    rows = rep["h4_narrow_rows"]
    assert rows, "narrowness not sampled"
    assert min(r["n_violated"] for r in rows) <= 12, \
        "no narrow band found; H4d's claim is unbacked"
    for r in rows:
        assert r["n_violated"] > 0, \
            "displacing gamma=%r produced no violating x at all" % r["gamma"]
        assert r["x_min"] is not None and r["x_max"] is not None


# ------------------------------------------------------------------- H4e

def test_criterion_is_not_vacuous():
    """The counterweight to H4c/H4d: the criterion CAN fail, so those gates are
    about reach, not about the criterion being broken."""
    rep = _artifact()
    ctl = rep["h4_control"]
    assert ctl["dominant_m_first"] is not None, \
        "a dominant off-axis pair must break eventual positivity"
    assert ctl["dominant_m_first"] <= 12
    assert ctl["dominant_neg_count"] > 50
    assert ctl["rh_neg_count"] == 0, \
        "an all-real-positive (RH-type) spectrum must never violate"


def test_real_spectrum_never_violates_directly():
    """Recompute the RH-type control from scratch rather than trusting the
    artifact."""
    qs = [h4._q(g * g, mp.mpf(1)) for g in h4.GAMMAS]
    negs = sum(1 for m in range(1, 400)
               if mp.re(sum(qv ** m for qv in qs)) < 0)
    assert negs == 0, "RH-type spectrum produced %d negative Q_m" % negs


def test_dominant_pair_does_violate_directly():
    Qm, th = mp.mpf(2), mp.mpf("0.7")
    qs = [Qm * mp.e ** (1j * th), Qm * mp.e ** (-1j * th)] + \
        [mp.mpf(j) / 20 for j in range(1, 8)]
    mf = h4._m_first_negative(qs, 400)
    assert mf is not None and mf <= 12, \
        "dominant pair should violate by m=12, got %r" % mf


def test_w_is_the_transformed_scale_for_a_displaced_zero():
    """Guard the transform itself: w = -(delta + i gamma)^2."""
    for d in (mp.mpf("0.1"), mp.mpf(1), mp.mpf("3.7")):
        g = h4.GAMMAS[1]
        expect = -(d + 1j * g) ** 2
        assert abs(h4._w(g, d) - expect) < 1e-25 * abs(expect)


def test_on_critical_line_w_is_real_positive():
    for g in h4.GAMMAS:
        w0 = h4._w(g, mp.mpf(0))
        assert mp.im(w0) == 0, "w is not real on the critical line: %s" % w0
        assert w0 == g * g
