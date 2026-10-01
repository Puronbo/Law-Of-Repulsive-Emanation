"""Tests for the Widder/Hankel H2 experiment.

``experiments/rh_widder_hankel_h2.py`` climbs from H1's first shifted
determinants to the full Hankel structure of the pinned Stieltjes/Widder
framework (rh_infinite_unit_stieltjes_pinned.md sections 9, 10, 14, 16;
rh_framework_pinned_october_2026.md sections 9, 10, 17, 27).  The sub-gates
are

  H2a  the section 17 transform extends to Q_1 .. Q_9 and matches the
       zero + moment-tail expansion,
  H2d  the shifted Schur/Vandermonde identity
       det[Q_{i+j+1}] = sum_{i_0<...<i_N} (prod q) prod (q_a - q_b)^2 holds,
  H2b/H2c  the D_0..D_3 ladder and both the Hamburger Hankel [Q_{i+j+1}] and
       the Stieltjes Hankel [Q_{i+j+2}] are positive through order N = 3,
  H2e  a strictly dominant off-axis pair drives the full shifted Hankel
       determinant negative.

The failure-mode to watch for is again a green gate with no content.  H2d is
exact ALGEBRA and must be orders of magnitude below the H2a translation
residual, or it has started comparing the determinant against a
tail-corrected product.  H2b/H2c positivity is sampled evidence, not proof,
so the test asserts the conclusion refuses RH and the detail says so; H2e
must actually go negative or the obstruction is vacuous.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "experiments"))

import regen_data  # noqa: E402


def _artifact():
    path = regen_data.find_data("rh_widder_hankel_h2_data.json")
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
        ["H2a", "H2d", "H2b/H2c", "H2e"]
    assert all(g["passed"] for g in rep["gates"]), \
        "a gate stopped confirming its number: %s" % names


def test_conclusion_refuses_rh():
    """H2 is an investigation, not a proof: the conclusion must say so."""
    rep = _artifact()
    c = rep["conclusion"]
    assert "Nothing here proves RH" in c
    assert "Widder criterion" in c
    assert "prime-gamma -> Hankel bridge is open" in c


# ------------------------------------------------------------------- H2a

def test_translation_to_nine_moments_is_small():
    rep = _artifact()
    assert rep["h2a_translation_worst_rel"] < 1e-4
    g = _gate(rep, "H2a")
    assert "F_xi" in g["detail"]
    assert "moment series" in g["detail"]


def test_translation_rows_have_positive_moments():
    rep = _artifact()
    assert len(rep["h2_rows"]) >= 3
    for row in rep["h2_rows"]:
        assert row["translation_rel"] < 1e-4
        assert row["Q1"] > 0 and row["Q3"] > 0 and row["Q5"] > 0


# ------------------------------------------------------------------- H2d

def test_schur_identity_is_exact_algebra():
    """The shifted Schur/Vandermonde identity must be near machine-zero -- if
    it is not orders of magnitude below the translation residual, the gate has
    started comparing it against a tail-corrected product."""
    rep = _artifact()
    rows = rep["h2_identity_rows"]
    assert rows, "no Schur identity rows recorded"
    assert max(r["rel"] for r in rows) < 1e-40
    assert max(r["rel"] for r in rows) < \
        1e-6 * rep["h2a_translation_worst_rel"]
    assert {r["N"] for r in rows} == {1, 2, 3}
    g = _gate(rep, "H2d")
    assert "Schur/Vandermonde" in g["detail"]


# ------------------------------------------------------------------- H2b/H2c

def test_ladder_and_hankels_are_positive():
    rep = _artifact()
    rows = rep["h2_rows"]
    for row in rows:
        assert len(row["D_m"]) >= 3
        assert all(d > 0 for d in row["D_m"]), row
        assert all(d > 0 for d in row["hamburger_dets"]), row
        assert all(d > 0 for d in row["stieltjes_dets"]), row
        # a Stieltjes Hankel sits below the Hamburger Hankel it shifts
        assert row["stieltjes_dets"][0] < row["hamburger_dets"][0]


def test_positivity_is_evidence_not_proof():
    g = _gate(_artifact(), "H2b/H2c")
    assert "evidence" in g["detail"]
    assert "not a proof" in g["detail"]


# ------------------------------------------------------------------- H2e

def test_offaxis_pair_actually_kills_the_hankel():
    """H2e is vacuous if the full Hankel determinant never changes sign."""
    rep = _artifact()
    rows = rep["h2e_hankel_obstruction"]
    assert [r["N"] for r in rows] == [1, 2, 3]
    assert all(r["det"] < 0 for r in rows), rows
    g = _gate(rep, "H2e")
    assert "dominant" in g["detail"]
