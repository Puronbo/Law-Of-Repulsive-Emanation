"""Tests for the positivity-certificate falsification experiment.

``experiments/rh_positivity_certificate.py`` tries to repair the
all-order certificate proposed in
``zero_to_riemann_zeta_complete_framework.md``. It fails, in two
different ways, and these tests lock both failures in.

The point of the controls in P5 is subtle and worth stating: the Jensen
real-rootedness condition passes on Xi at every degree tested, which
looks like success, and it is only the control with *purely imaginary*
zeros that reveals the condition is insensitive to where the zeros are.
If someone deletes the control, P5 becomes a vacuous green check.
"""

import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "experiments"))

import regen_data  # noqa: E402
import rh_positivity_certificate as P  # noqa: E402

import mpmath as mp  # noqa: E402


def _artifact():
    path = regen_data.find_data("rh_positivity_certificate_data.json")
    assert path is not None, "artifact missing; run the script"
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _gate(rep, prefix):
    hits = [g for g in rep["gates"] if g["gate"].startswith(prefix)]
    assert len(hits) == 1, "expected exactly one gate starting %r" % prefix
    return hits[0]


# ---------------------------------------------------------------- structure

def test_all_gates_pass():
    rep = _artifact()
    names = [g["gate"] for g in rep["gates"]]
    assert [n.split()[0] for n in names] == ["P1", "P2", "P3", "P4", "P5"]
    assert all(g["passed"] for g in rep["gates"]), \
        "a gate stopped confirming its obstruction: %s" % names


def test_conclusion_claims_no_certificate():
    rep = _artifact()
    c = rep["conclusion"]
    assert "false at n = 0" in c
    assert "vacuous" in c
    assert "Nothing here bears on the truth of RH" in c


# ------------------------------------------------------------------- P1

def test_sturm_selftest_passed_inside_the_script():
    """The script's own self-test must have been clean.

    Three separate bugs in the Sturm implementation each produced
    "no real roots" for every input, which looks like a real negative
    result. The self-test is the only thing standing between that class
    of bug and a wrong conclusion here.
    """
    rep = _artifact()
    g = _gate(rep, "P1")
    assert g["passed"]
    assert "failures: none" in g["detail"]


@pytest.mark.parametrize("coeffs,expect", [
    ([1, -2], 1),          # x - 2
    ([1, 0, -1], 1),       # x^2 - 1:  two real, one positive
    ([1, 0, 1], 0),        # x^2 + 1
    ([1, -1, 0, 1], 0),    # x^3 - x^2 + 1: real root is negative
    ([1, -3, 2], 2),       # (x-1)(x-2)
    ([1, 0, -3, 0, 1], 2),  # x^4-3x^2+1: four real, two positive
    ([2, 0, -2], 1),       # 2(x^2-1)
    ([1, -1, 1, 1], 0),    # x^3-x^2+x+1: real root is negative
    ([1, 0, 0, 0, -1], 1),  # x^4 - 1
    ([1, 0, -10, 0, 9], 2),  # (x^2-1)(x^2-9)
    ([1, -2, -5, 6], 2),   # roots -3, 1, 2
])
def test_sturm_counts_positive_roots(coeffs, expect):
    got = P.count_positive_roots([mp.mpf(c) for c in coeffs])
    assert got == expect, "%s: expected %d positive roots, got %d" % (
        coeffs, expect, got)


def test_derivative_convention():
    """Descending-list derivative is (n-j)*p[j], checked against numpy."""
    for coeffs in ([1, 0, -1], [1, -3, 2], [2, 0, 0, 0, -5], [1, 2, 3, 4]):
        got = [float(x) for x in P.strip(P.derivative(P.strip(
            [mp.mpf(c) for c in coeffs])))]
        n = len(coeffs) - 1
        # reference: coefficient of x^(n-1-j) in the derivative
        ref = [(n - j) * float(coeffs[j]) for j in range(n)]
        while ref and ref[0] == 0:
            ref.pop(0)
        assert got == ref, coeffs


# ------------------------------------------------------------------- P2

def test_turan_ratios_all_exceed_one():
    rep = _artifact()
    q = [float(x) for x in rep["turan_ratios"]]
    assert len(q) >= 10
    assert all(x > 1.0 for x in q), q
    # pinned values, so a coefficient regression is caught
    assert q[0] == pytest.approx(2.7911029, abs=1e-6)
    assert q[1] == pytest.approx(1.5682678, abs=1e-6)


def test_certificate_is_false_at_first_index():
    """The framework's D_0 >= 0 fails, so this is not a degree question."""
    a = P.xi_coefficients(4)
    q0 = a[0] * a[2] / a[1] ** 2
    assert q0 > 1, "if this ever drops below 1 the audit needs revisiting"


# ------------------------------------------------------------------- P3

def _multiplier_coeffs(a, lam):
    """[z^n] exp(lam z) A(z) = sum_{j<=n} a_j lam^(n-j)/(n-j)!."""
    return [sum(a[j] * lam ** (n - j) / mp.factorial(n - j)
                for j in range(n + 1)) for n in range(len(a))]


def test_index_decreasing_shift_is_the_multiplier():
    """The shift that multiplies A(z) by exp(lam z) is b_n' = b_(n-1).

    That is what the code calls forward_shift: the list it builds equals the
    coefficients of exp(lam z) A(z) exactly. If ever a_0 is dropped from the
    sum this test catches data loss.
    """
    a = P.xi_coefficients(8)
    lam = mp.mpf(7) / 10
    got = P.forward_shift(a, lam)
    ref = _multiplier_coeffs(a, lam)
    assert all(got[n] == ref[n] for n in range(len(a))), "no longer a multiplier"
    # and the derivative of that list is the *decreasing* index shift
    h = mp.mpf("1e-6")
    hi = _multiplier_coeffs(a, lam + h)
    lo = _multiplier_coeffs(a, lam - h)
    deriv = [(hi[n] - lo[n]) / (2 * h) for n in range(1, len(a))]
    assert all(abs(deriv[n - 1] - ref[n - 1]) < mp.mpf("1e-6")
               for n in range(1, len(a)))


def test_de_bruijn_flow_is_index_increasing_not_multiplier():
    """The flow a_n' = a_(n+1) is NOT [z^n] exp(lam z) A(z)."""
    a = P.xi_coefficients(8)
    lam = mp.mpf(7) / 10
    flow = P.backward_shift(a, lam)          # sum_{j>=n}: the actual flow
    ref = _multiplier_coeffs(a, lam)         # exp(lam z) A(z)
    err = max(abs(flow[n] - ref[n]) for n in range(len(a)))
    assert err > mp.mpf("1e-6"), "flow became a multiplier; P3 is stale"
    # the flow's generator is d/dl A = (A - A(0))/z, checked coefficient-wise
    h = mp.mpf("1e-6")
    hi = P.backward_shift(a, lam + h)
    lo = P.backward_shift(a, lam - h)
    rhs = [flow[n + 1] for n in range(len(a) - 1)]    # (A - A(0))/z
    worst = max(abs((hi[n] - lo[n]) / (2 * h) - rhs[n]) for n in range(len(a) - 1))
    assert worst < mp.mpf("1e-6"), "d/dl A = (A - A(0))/z failed: %e" % float(worst)


def test_artifact_records_the_asymmetry():
    rep = _artifact()
    g = _gate(rep, "P3")
    assert "index-INCREASING" in g["gate"]
    d = g["detail"]
    assert "exp(lam z)" in d
    assert "0.0e+00" in d               # multiplier-direction error, exactly zero
    assert "3.46e-01" in d              # flow-direction error, pinned to the audit


# ------------------------------------------------------------------- P4

def test_ordinary_generating_function_has_finite_radius():
    rep = _artifact()
    ogf = rep["ordinary_generating_function"]
    assert ogf["ratios_rising_at_top"] is True
    assert float(ogf["radius_bound_1_over_max_ratio"]) < 10.0
    # ratios are still climbing at the end of the computed range
    tail = [float(x) for x in ogf["coefficient_ratios"][-4:]]
    assert tail == sorted(tail) and tail[-1] > tail[0], tail


# ------------------------------------------------------------------- P5

def test_jensen_passes_on_xi():
    rep = _artifact()
    assert rep["jensen_repair"]["xi_failing_degrees"] == []


def test_jensen_also_passes_with_purely_imaginary_zeros():
    """The vacuity witness. 1/(1+t^2/4) has zeros +/-2i, not real ones."""
    rep = _artifact()
    assert rep["jensen_repair"]["control_imaginary_zeros_failing_degrees"] == []


def test_jensen_is_not_completely_blind():
    """It does constrain the decay profile, just not the zero locations."""
    rep = _artifact()
    stretched = rep["jensen_repair"]["control_stretched_decay_failing_degrees"]
    assert stretched, "if the stretched control also passes, P5's wording is wrong"


def test_control_really_has_imaginary_zeros():
    """Guard the guard: the control's zeros must actually be imaginary.

    1/(1+t^2/4) is the function whose Taylor coefficients the P5 control
    feeds to the Jensen construction. If its zeros were real the control
    would prove nothing.
    """
    # 1/(1+t^2/4) vanishes where 1 + t^2/4 = 0, i.e. where t^2 + 4 = 0.
    for root in mp.polyroots([mp.mpf(1), 0, 4], maxsteps=100, extraprec=100):
        assert abs(mp.re(root)) < mp.mpf("1e-30"), root
        assert abs(abs(mp.im(root)) - 2) < mp.mpf("1e-20"), root


def test_jensen_polynomial_indexing_is_by_taylor_degree():
    """jensen_P must key coefficients by 2m, not m.

    Getting this wrong yields degenerate polynomials whose "real-rooted"
    verdict is meaningless, and it is the third indexing slip in this area.
    """
    a = P.xi_coefficients(2)
    b = [a[m] / mp.factorial(2 * m) for m in range(3)]
    poly = P.jensen_P(b, 2)
    assert len(poly) - 1 == 1
    # J_2 as a polynomial in u is [a_0, a_1 / 2]
    assert float(poly[0]) == pytest.approx(float(a[0]), rel=1e-12)
    assert float(poly[1]) == pytest.approx(float(a[1] / 2), rel=1e-12)
