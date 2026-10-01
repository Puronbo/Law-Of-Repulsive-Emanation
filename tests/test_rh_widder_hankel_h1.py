"""Tests for the Widder/Hankel H1 experiment.

``experiments/rh_widder_hankel_h1.py`` opens the Stieltjes/Widder/Hankel stage
of the pinned records (rh_infinite_unit_stieltjes_pinned.md sections 10 and 14;
rh_framework_pinned_october_2026.md sections 9, 10, 17, 18, 27).  The
immediate target named in section 14 is the first shifted-Hankel determinant
D_0 = Q_1 Q_3 - Q_2^2, then D_1 = Q_3 Q_5 - Q_4^2.  The sub-gates are

  H1a  the section 17 finite differential transform of F_xi reproduces Q_k,
  H1b  the section 18 explicit formula F_xi = F_rational + F_Gamma + F_prime
       closes, and the (1/2)log pi gamma-term sign is load-bearing,
  H1c  the section 10 Vandermonde identity
       D_m = sum_{i<j} (q_i q_j)^{2m+1} (q_i - q_j)^2 holds exactly,
  H1d  D_0 and D_1 are positive on the sampled half-line,
  H1e  a strictly dominant synthetic off-axis pair drives D_m negative for
       large m (the derived obstruction, not a proof).

The failure-mode to watch for is a gate that is green for a circular reason.
H1a must not compare the differential transform against itself: the RHS must
be the zero + moment-tail expansion, and the slowly-converging Q_1 entry must
use the exact log-Xi moment tail (without it, Q_1 is off by ~6% and H1d would
silently inherit the error).  H1c's Vandermonde identity is exact ALGEBRA and
must be checked against the truncated products built from the SAME 400 q's,
NOT against the moment-tail-extended products (the tail runs past the 400
zeros and the pair sum does not); if it is compared to the extended product it
reports a spurious ~11% mismatch.  H1d must be positive but a positive result
is evidence, not proof: the test asserts the conclusion refuses RH, and H1e
must actually go negative or the obstruction is vacuous.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "experiments"))

import regen_data  # noqa: E402


def _artifact():
    path = regen_data.find_data("rh_widder_hankel_h1_data.json")
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
        ["H1a", "H1b", "H1c", "H1d", "H1e"]
    assert all(g["passed"] for g in rep["gates"]), \
        "a gate stopped confirming its number: %s" % names


def test_conclusion_refuses_rh():
    """H1 is an investigation, not a proof: the conclusion must say so."""
    rep = _artifact()
    c = rep["conclusion"]
    assert "Nothing here proves RH" in c
    assert "Widder criterion" in c
    assert "prime-gamma -> Hankel bridge is open" in c


# ------------------------------------------------------------------- H1a

def test_translation_is_small_and_recorded():
    rep = _artifact()
    assert rep["h1a_translation_worst_rel"] < 1e-4
    assert rep["h1_translation_residual"] == rep["h1a_translation_worst_rel"]
    g = _gate(rep, "H1a")
    assert "F_xi^{(2k-j-1)}" in g["detail"]
    assert "moment tail" in g["detail"]


def test_translation_rows_have_all_five_moments():
    """H1a must actually evaluate Q_1 .. Q_5, not just one entry."""
    rep = _artifact()
    for row in rep["h1_rows"]:
        assert row["translation_rel"] < 1e-4
        assert row["Q1"] > 0 and row["Q3"] > 0 and row["Q5"] > 0


# ------------------------------------------------------------------- H1b

def test_explicit_formula_closes_and_gamma_sign_matters():
    """H1b is vacuous if the wrong-sign variant also closes: pin both."""
    rep = _artifact()
    rows = rep["h1b_explicit_formula"]
    assert rows, "no explicit-formula rows recorded"
    assert max(r["split_rel"] for r in rows) < 1e-30
    assert min(r["wrong_gamma_rel"] for r in rows) > 1e-3
    g = _gate(rep, "H1b")
    assert "F_Gamma" in g["detail"] or "gamma" in g["detail"]
    assert "log pi" in g["detail"]


# ------------------------------------------------------------------- H1c

def test_pair_identity_is_exact_algebra():
    """The Vandermonde identity must be near machine-zero -- if this is not
    orders of magnitude below the translation residual, the gate has started
    comparing the identity against a tail-corrected product (the ~11% bug)."""
    rep = _artifact()
    assert rep["h1c_pair_identity_worst_rel"] < 1e-25
    assert rep["h1c_pair_identity_worst_rel"] < \
        1e-6 * rep["h1a_translation_worst_rel"]
    for row in rep["h1_rows"]:
        assert row["pair_identity_rel"] < 1e-25


# ------------------------------------------------------------------- H1d

def test_d0_d1_positive_on_the_grid():
    rep = _artifact()
    rows = rep["h1_rows"]
    assert len(rows) >= 5
    assert all(r["D0"] > 0 and r["D1"] > 0 for r in rows), rows
    # D_1 is a product of two differences and sits far below D_0 for the
    # sampled x; a wildly different magnitude would signal a broken transform
    assert all(r["D0"] < 1e-8 for r in rows)


def test_positivity_is_evidence_not_proof():
    g = _gate(_artifact(), "H1d")
    assert "evidence" in g["detail"]
    assert "not a proof" in g["detail"] or "not a\nproof" in g["detail"]


# ------------------------------------------------------------------- H1e

def test_obstruction_actually_goes_negative():
    """H1e is vacuous if D_m never changes sign: require a negative tail."""
    rep = _artifact()
    rows = rep["h1e_obstruction"]
    assert rows and rows[-1]["D_m"] < 0
    assert any(r["D_m"] < 0 for r in rows)
    # the determinant identity must hold on the synthetic multiset too
    assert all(r["det_check"] < 1e-40 for r in rows)
    g = _gate(rep, "H1e")
    assert "dominant" in g["detail"] or "dominates" in g["detail"]
