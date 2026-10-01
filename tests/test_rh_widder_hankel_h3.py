"""Tests for the Widder/Hankel H3 experiment.

``experiments/rh_widder_hankel_h3.py`` attacks the pinned bottleneck
(rh_framework_pinned_october_2026.md section 27): can the prime--gamma
explicit formula force universal Hankel positivity of the transformed-zero
quadratic form?  The sub-gates are

  H3a  the section 18 split F_xi = F_rational + F_Gamma + F_prime closes
       against the genuine von Mangoldt Dirichlet series, in the half-plane
       Re s > 1 where that series represents zeta'/zeta,
  H3b  the critical-line heat trace is completely monotone, but the section 22
       Widder kernels P_m change sign, so h's positivity is not enough,
  H3c  the section 9 quadratic form identity c^T H_N c = sum_rho q_rho P(q_rho)^2
       is exact algebra, for real and for complex q-multisets,
  H3d  the per-zero peak excess 4x|q_rho| = 1 + delta^2/gamma^2 is exact and
       equals 1 exactly on the critical line,
  H3e  maximal-shell isolation (P_m = u^m R) makes the form oscillate in sign,
  H3f  the differential transform is linear and the Hankel entries are a
       cancellation of same-order rational / gamma / prime pieces.

The failure-modes watched for here:

* **A vacuous gate.** H3 must contain no gate that asserts ``True``
  unconditionally -- every gate has to be a falsifiable numeric comparison.
  The test asserts no gate is trivially passing.
* **The truncated-series trap (H3a).** The series -sum Lambda(n) n^{-s}
  represents zeta'/zeta only for Re s > 1; its tail is O(N^{1-s}).  Sampling
  x where Re s <= 1 reports a huge spurious residual.  H3a must be confined to
  Re s > 1 and must pass on the real numbers, not on a loosened tolerance.
* **The cancellation trap (H3f).** The total Q_k is a near-cancellation of
  same-order pieces (|Q_k| falls to ~1e-12 by k = 5), so conditioning the
  linearity residual on |Q_k| explodes to O(1e4) for arithmetic reasons alone.
  The residual must be conditioned on the sum of the piece magnitudes, and
  linearity must only be asserted at low order where the prime-series
  truncation is negligible -- the growth at higher k must be recorded, not
  hidden.
* **The sign-transfer trap (H3f).** F_prime < 0 on the real axis but its
  Q_k contribution is POSITIVE, because the transform mixes alternating-sign
  high-order derivatives.  The test pins both signs so a future edit cannot
  quietly reintroduce the naive sign argument.
* **Honesty.** H3 investigates the bridge; it does not close it.  The
  conclusion must say so and must still name the open step.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "experiments"))

import regen_data  # noqa: E402


def _artifact():
    path = regen_data.find_data("rh_widder_hankel_h3_data.json")
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
        ["H3a", "H3b", "H3c", "H3d", "H3e", "H3f"]
    assert all(g["passed"] for g in rep["gates"]), \
        "a gate stopped confirming its number: %s" % names


def test_no_gate_is_trivially_passing():
    """Anti-vacuity: every gate detail must carry a recorded numeric claim, so
    a gate cannot be green just because it was hardcoded True."""
    rep = _artifact()
    for g in rep["gates"]:
        d = g["detail"]
        has_number = any(ch.isdigit() for ch in d)
        assert has_number, "gate %r has no recorded number: %r" % (g["gate"], d)
        assert len(d) > 120, "gate %r detail is too thin to be a real check" \
            % g["gate"]


def test_conclusion_refuses_rh():
    """H3 investigates the bottleneck; it does not prove it."""
    rep = _artifact()
    c = rep["conclusion"]
    assert "NOTHING HERE PROVES RH" in c
    assert "Widder criterion is posited" in c
    assert "remains OPEN" in c


# ------------------------------------------------------------------- H3a

def test_split_uses_the_convergent_half_plane():
    """The von Mangoldt series only represents zeta'/zeta for Re s > 1; a
    sample with Re s <= 1 would report a huge spurious residual."""
    rep = _artifact()
    rows = rep["h3_split_rows"]
    assert rows, "no split rows recorded"
    for r in rows:
        assert r["s"] > 1.0 + 1e-12, \
            "split sampled s = %r, outside the series' convergence half-plane" \
            % r["s"]
    assert max(r["split_rel"] for r in rows) < 1e-5


def test_split_detail_names_the_truncation_law():
    g = _gate(_artifact(), "H3a")
    assert "Re s > 1" in g["detail"]
    assert "N^{1-s}" in g["detail"]
    assert "NEGATIVE" in g["detail"] or "negative" in g["detail"]


# ------------------------------------------------------------------- H3b

def test_heat_trace_monotone_but_kernels_change_sign():
    rep = _artifact()
    ht = rep["h3_heat_trace"]
    assert ht["monotone_worst_rel"] < 1e-30
    assert [r["n"] for r in ht["rows"]] == [0, 1, 2, 3, 4]
    assert all(r["positive"] for r in ht["rows"])
    kern = rep["h3_widder_kernels"]
    assert [r["m"] for r in kern] == [1, 2, 3, 4]
    # every P_m must take both signs, else the "kernels spoil termwise
    # positivity" claim is vacuous
    assert all(r["changes_sign"] for r in kern)
    assert all(r["min"] < 0 < r["max"] for r in kern)


# ------------------------------------------------------------------- H3c

def test_quadratic_form_identity_is_exact_algebra():
    rep = _artifact()
    rows = rep["h3_quadform_rows"]
    assert rows, "no quadratic-form rows recorded"
    assert max(r["rel"] for r in rows) < 1e-40
    kinds = {r["kind"] for r in rows}
    assert kinds == {"real", "complex"}, \
        "the identity must also be checked on a complex multiset"
    # the complex multiset must actually be able to violate positivity, else
    # checking it says nothing
    assert any(r["quad_matrix_side"] < 0 for r in rows
               if r["kind"] == "complex"), \
        "complex rows are all non-negative: the identity check is vacuous"


def test_quadform_detail_does_not_claim_positivity():
    g = _gate(_artifact(), "H3c")
    assert "its positivity is not" in g["detail"]


# ------------------------------------------------------------------- H3d

def test_excess_is_exact_and_one_on_the_line():
    rep = _artifact()
    rows = rep["h3_excess_rows"]
    assert rows, "no excess rows recorded"
    assert max(r["rel"] for r in rows) < 1e-30
    zeros = [r for r in rows if r["delta"] == 0]
    assert zeros, "no critical-line rows recorded"
    for r in zeros:
        assert abs(r["peak_4x_absq"] - 1.0) < 1e-12
        assert abs(r["excess_formula"] - 1.0) < 1e-12
    # a genuine displacement must produce a strictly greater-than-one peak
    assert any(r["peak_4x_absq"] > 1 + 1e-9 for r in rows if r["delta"] > 0)


# ------------------------------------------------------------------- H3e

def test_shell_isolation_actually_oscillates():
    """H3e is vacuous if the isolated form never changes sign."""
    rep = _artifact()
    rows = rep["h3_shell_rows"]
    vals = [r["S_m"] for r in rows]
    assert any(v < 0 for v in vals) and any(v > 0 for v in vals)
    flips = sum(1 for a, b in zip(vals, vals[1:]) if a * b < 0)
    assert flips >= 4, "expected repeated sign flips, got %d" % flips
    assert [r["m"] for r in rows] == sorted(r["m"] for r in rows)


# ------------------------------------------------------------------- H3f

def test_linearity_is_conditioned_on_the_pieces_not_the_total():
    """The total Q_k is a cancellation; conditioning on it explodes the
    residual for arithmetic reasons.  The residual must be scaled by the sum
    of the piece magnitudes."""
    rep = _artifact()
    summary = rep["h3_q_split_summary"]
    assert summary["lin_tol"] == 1e-3
    assert summary["worst_rel_low_k"] < summary["lin_tol"]
    rows = rep["h3_q_split_rows"]
    for r in rows:
        assert r["cancellation_ratio"] < 1.0
    # the recorded growth at high k must be visible, not hidden
    assert rows[-1]["rel"] > rows[0]["rel"], \
        "expected the truncation residual to grow with k"
    assert rows[-1]["rel_to_total"] > rows[-1]["rel"], \
        "the total must be the worse conditioning, else the trap is absent"


def test_prime_piece_sign_does_not_follow_from_f_prime_sign():
    """F_prime < 0 on the real axis yet its Q_k contribution is positive:
    pin both so the naive sign-transfer argument cannot come back."""
    rep = _artifact()
    rows = rep["h3_q_split_rows"]
    assert all(r["Q_prime"] > 0 for r in rows), \
        "Q_prime flipped sign; the cancellation analysis must be revisited"
    assert rep["h3_q_split_summary"]["mixed_signs"] is True
    assert any(r["Q_rational"] < 0 for r in rows)
    assert any(r["Q_gamma"] < 0 for r in rows)
    g = _gate(rep, "H3f")
    assert "does NOT determine the sign" in g["detail"]


def test_bridge_is_reported_open():
    """H3f must locate the bottleneck rather than claim to close it."""
    g = _gate(_artifact(), "H3f")
    assert "CANCELLATION" in g["detail"]
    assert "cannot be read off any one piece" in g["detail"]
