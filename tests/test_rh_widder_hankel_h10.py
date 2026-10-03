"""Regression tests for experiments/rh_widder_hankel_h10.py.

H10 asks what record section 27's Widder-Hankel criterion can actually
certify.  RH/Hankel.lean (commit 190e87c) proved the criterion's algebra and
its sufficiency direction, so the criterion's content is settled; what remains
open is the application, universal positivity for the zeta atoms.  H10 settles
the structural part exactly and measures the numerical part.

Four things are pinned here, and two of them are defects in this file's own
first draft rather than in the experiment:

  * the determinant factorisation `det H_K = (prod q_k) * Vandermonde^2` is a
    statement about the SQUARE case `N = K` only.  The first draft claimed it
    for `N <= K`, which is false: for `N < K` the term `sum_{k>N} q_k v_k v_k'`
    survives, and the truncated product is not the determinant.  H10a carries a
    negative control that demonstrates the failure, and the test below asserts
    the control actually fires, so the wrong generalisation cannot come back;
  * the sign test is vacuous for `N > K` (rank at most K), so a certificate
    search is confined to `N <= K`.  Without this, roundoff alone would
    manufacture apparent negative eigenvalues;
  * the raw form overflows float64 at small order, and the wall moves DOWN as
    more zeros are used -- more data makes the unnormalised criterion worse.
    This is a property of the formulation, not of the arithmetic;
  * after the Sylvester normalisation the computed smallest eigenvalue turns
    negative at order ~15 even though the exact matrix is positive definite
    there.  Those negatives are provably roundoff, so any pipeline testing
    `lambda_min < 0` would declare RH FALSE from that order.  The honest output
    past the wall is "not decidable", not "false".
"""

import json
import os

import numpy as np
import sympy as sp

import experiments.rh_widder_hankel_h10 as h10

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "experiments", "data", "rh_widder_hankel_h10_data.json")


def _report():
    with open(DATA, encoding="utf-8") as fh:
        return json.load(fh)


def test_artifact_exists_and_all_gates_pass():
    rep = _report()
    assert rep["gates"], "no gates recorded"
    failed = [g["gate"] for g in rep["gates"] if not g["passed"]]
    assert not failed, "gates failed: %s" % failed


# ------------------------------------------------------- H10a, exact algebra

def test_congruence_residuals_are_exactly_zero():
    """H_N = V D V' exactly, at every admissible order, over the rationals."""
    for row in _report()["h10a_exact_rows"]:
        qs = [sp.Rational(q) for q in row["atoms"]]
        K = len(qs)
        assert sp.simplify(sp.Integer(row["residual_at_N_eq_K"])) == 0
        for N in range(1, K + 1):
            V = sp.Matrix(N, K, lambda i, k: qs[k] ** i)
            H = h10._hankel(qs, N)
            assert (H - V * sp.diag(*qs) * V.T) == sp.zeros(N, N)


def test_product_formula_holds_at_N_eq_K_and_sign_tracks_atom_product():
    for row in _report()["h10a_exact_rows"]:
        qs = [sp.Rational(q) for q in row["atoms"]]
        det = sp.expand(h10._hankel(qs, len(qs)).det())
        vand = h10._vandermonde(qs, len(qs)).det()
        assert sp.simplify(det - sp.prod(qs) * vand ** 2) == 0
        assert int(sp.sign(det)) == int(sp.sign(sp.prod(qs)))
        assert row["sign_actual"] == row["sign_pred"]


def test_negative_control_fires():
    """The product formula must be demonstrably FALSE for N < K.

    Without this the H10a claim would silently generalise to `N <= K`, which is
    the bug this file's first draft contained.
    """
    ctrl = _report()["h10a_negative_control_rows"]
    assert ctrl, "no negative-control rows recorded"
    assert any(not c["truncated_product_holds"] for c in ctrl), \
        "the truncated-product formula was expected to fail for some N < K"


def test_product_formula_really_does_fail_for_N_lt_K_directly():
    """Recompute one failing case rather than trusting the artifact."""
    qs = [sp.Rational(2), sp.Rational(3), sp.Rational(5), sp.Rational(7)]
    K = len(qs)
    for N in range(1, K):
        det = sp.expand(h10._hankel(qs, N).det())
        trunc = sp.expand(sp.prod(qs[:N]) * h10._vandermonde(qs, N).det() ** 2)
        assert sp.simplify(det - trunc) != 0, \
            "N < %d: the truncated product unexpectedly equals the determinant" % K


# ------------------------------------------------------------- H10b, the rank wall

def test_rank_wall_exact():
    rows = _report()["h10b_rank_wall_rows"]
    for row in rows:
        k = row["K"]
        det = sp.expand(h10._hankel(
            [sp.Rational(2), sp.Rational(3), sp.Rational(5)], row["N"]).det())
        assert sp.simplify(det - sp.Integer(row["det_exact"])) == 0
        if row["N"] > k:
            assert det == 0, "det must vanish for N > K"
        else:
            assert det != 0, "det must be non-zero for N <= K"


# --------------------------------------------- H10c, the constructive witness

def test_witness_is_exact_rational_and_negative():
    row = _report()["h10c_constructive_witness"]
    qs = [sp.Rational(q) for q in row["atoms"]]
    K = len(qs)
    c = sp.Matrix([sp.Rational(v) for v in row["witness_c"]])
    form = sp.expand((c.T * h10._hankel(qs, K) * c)[0])
    assert sp.simplify(form - sp.Integer(row["quadratic_form_exact"])) == 0
    assert form == qs[h10.H10_NEG_AT - 1]
    assert form < 0, "the witness quadratic form must be strictly negative"
    assert any(v != 0 for v in c), "the witness must be a non-zero vector"


def test_witness_reproduces_vandermonde_transpose_equations():
    row = _report()["h10c_constructive_witness"]
    qs = [sp.Rational(q) for q in row["atoms"]]
    K = len(qs)
    c = sp.Matrix([sp.Rational(v) for v in row["witness_c"]])
    V = h10._vandermonde(qs, K)
    assert (V.T * c) == sp.eye(K).col(h10.H10_NEG_AT - 1)


# ------------------------------------------------------ H10d, the overflow wall

def test_overflow_wall_exists_and_moves_down_with_more_zeros():
    walls = _report()["h10d_overflow_wall"]
    vals = []
    for K in h10.H10_KZERO:
        assert walls["K=%d" % K] is not None, "no wall found for K=%d" % K
        assert 0 < walls["K=%d" % K] < h10.H10_NMAX
        vals.append(walls["K=%d" % K])
    assert vals == sorted(vals, reverse=True), \
        "the wall must move DOWN as K grows, got %s" % vals


def test_measured_overflow_matches_the_asymptotic_prediction():
    for row in _report()["h10d_overflow_rows"]:
        assert row["measured_first_inf_moment_index"] is not None
        # moment index m = 2N-1, so N = (m+1)/2, within rounding
        assert abs(row["measured_wall_N"] - row["predicted_wall_N"]) <= 1


# ------------------------------------------------------- H10e, the precision wall

def test_normalised_matrix_has_unit_diagonal_and_stays_finite():
    g = np.array(h10._zero_ordinates(min(h10.H10_KZERO)))
    logM = h10._log_moments(g, 20)
    mats = h10._normalised_matrices(logM, 20)
    for N, Hn in mats.items():
        assert np.all(np.isfinite(Hn)), "normalised form overflowed at N=%d" % N
        assert np.allclose(np.diag(Hn), 1.0), "diagonal must be exactly 1 at N=%d" % N


def test_normalisation_preserves_inertia_direction_on_a_known_case():
    """D^-1/2 H D^-1/2 must be congruent to H, hence share its inertia.

    Checked on a small exact-rational case where the answer is known by hand:
    three positive atoms give a positive definite Hankel form, one negative
    atom gives an indefinite one.
    """
    qs = [sp.Rational(2), sp.Rational(3), sp.Rational(5)]
    H = np.array(h10._hankel(qs, 3).evalf(40), dtype=float)
    d = np.sqrt(np.diag(H))
    Hn = H / np.outer(d, d)
    assert np.all(np.linalg.eigvalsh(Hn) > 0), \
        "all-positive atoms must give a positive definite normalised form"

    qs_neg = [sp.Rational(2), sp.Rational(3), sp.Rational(-4)]
    assert all(sp.simplify(h10._hankel(qs_neg, 3)[i, i]) != 0 for i in range(3)), \
        "pick atoms with no vanishing moment, else the scaling divides by zero"
    Hn_neg = np.array(h10._hankel(qs_neg, 3).evalf(40), dtype=float)
    # any invertible diagonal rescaling preserves inertia; signs are irrelevant
    dn = np.sqrt(np.abs(np.diag(Hn_neg)))
    assert np.all(dn > 0)
    ev = np.linalg.eigvalsh(Hn_neg / np.outer(dn, dn))
    assert ev.min() < 0 < ev.max(), \
        "one negative atom must give an indefinite normalised form"


def test_computed_negatives_are_provably_roundoff():
    """The exact matrix is PD, so any computed negative is an artifact."""
    rep = _report()
    rows = rep["h10e_normalised_eigenvalue_rows"]
    neg = [r["N"] for r in rows if r["computed_negative_but_exact_is_PD"]]
    assert neg, "expected spurious negatives at large order"
    assert rep["h10e_first_spurious_negative_N"] == min(neg)
    # the wall is a precision wall, not the rank wall: far below N = K
    assert min(neg) <= max(h10.H10_KZERO) // 10
    # and double precision does still work at small order
    assert min(neg) > 5
    # the negative plateau is roundoff-sized and flat, not growing
    plateau = [r["lambda_min"] for r in rows if r["N"] >= min(neg)]
    assert max(abs(v) for v in plateau) < 1e-10, \
        "the plateau must sit at the noise floor, got %s" % plateau


def test_digits_lost_per_order_is_negative():
    slope = _report()["h10e_digits_lost_per_order"]
    assert slope is not None and slope < 0


def test_conclusion_does_not_claim_rh():
    text = _report()["conclusion"].lower()
    assert "neither a proof of rh nor a counterexample" in text
    assert "open" in text
