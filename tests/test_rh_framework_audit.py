"""Regression tests for the audit of zero_to_riemann_zeta_complete_framework.

These lock in the four corrections found by
``experiments/audit_zero_to_riemann_zeta.py``. Each one is a place where the
source framework document is wrong, so a change that "fixes" the document back
to its original wording will fail here.
"""

import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "experiments"))

import audit_zero_to_riemann_zeta as A  # noqa: E402
import regen_data  # noqa: E402

import mpmath as mp  # noqa: E402


def _artifact():
    path = regen_data.find_data("audit_zero_to_riemann_zeta_data.json")
    assert path is not None, "audit artifact missing; run the script"
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _claim(report, section, needle):
    hits = [c for c in report["claims"]
            if c["section"] == section and needle in c["claim"]]
    assert len(hits) == 1, "expected exactly one sec %s claim matching %r" % (
        section, needle)
    return hits[0]


# ---------------------------------------------------------------- structure

def test_audit_ran_and_is_stable():
    rep = _artifact()
    assert rep["experiment"].startswith("audit of zero_to_riemann")
    # 20 claims, 16 agree, 4 disagree. If this moves, the audit changed scope.
    assert rep["summary"]["checked"] == 20
    assert rep["summary"]["agree"] == 16
    assert rep["summary"]["disagree"] == 4
    assert "no proof" in rep["verdict"].lower()


def test_exactly_the_four_known_errors():
    rep = _artifact()
    bad = {(c["section"], c["claim"]) for c in rep["claims"] if not c["agrees"]}
    assert bad == {
        ("9", "xi'/xi = zeta'/zeta + 1/s + 1/(s-1) - log(pi)/2 - Gamma'/2Gamma"),
        ("7", "D_n = a_(n+1)^2 - a_n a_(n+2) >= 0  (quadratic Jensen)"),
        ("12", "D_n = a_n^2 (1 - r_(n-1) r_n),  boundary r_(n-1) r_n = 1"),
        ("13", "=> a_(k-1)a_(k+1)/a_k^2 <= (2k+1)/(2k+2), margin >= 1/(2k+2)"),
    }


# ----------------------------------------------------------------- error 1

def test_xi_log_derivative_gamma_term_is_positive():
    """sec 9: the gamma term in xi'/xi is +, not -."""
    s = mp.mpc(mp.mpf("0.7"), mp.mpf("3.1"))
    lhs = mp.diff(A.xi, s) / A.xi(s)
    plain = (mp.diff(mp.zeta, s) / mp.zeta(s) + 1 / s + 1 / (s - 1)
             - mp.mpf(1) / 2 * mp.log(mp.pi))
    psi = mp.diff(mp.gamma, s / 2) / mp.gamma(s / 2)
    assert abs(complex(lhs - (plain + psi / 2))) < 1e-20   # correct sign
    assert abs(complex(lhs - (plain - psi / 2))) > 1.0     # document's sign


# ----------------------------------------------------------------- error 2

def test_quadratic_jensen_fails_for_actual_xi_coefficients():
    """sec 7: the real coefficients are strictly log-convex, q_n > 1.

    This is the load-bearing finding: it means the low-order Taylor
    truncations of Xi are not real-rooted, so no truncation-level
    hyperbolicity test is valid for Xi.
    """
    a = A.a_coeffs(12)
    qs = [a[n] * a[n + 2] / a[n + 1] ** 2 for n in range(9)]
    assert all(q > 1 for q in qs), "expected strict log-convexity, got %s" % qs
    assert float(qs[0]) == pytest.approx(2.7911028, abs=1e-6)
    # strictly decreasing but never reaching 1 in the sampled range
    assert all(qs[i] > qs[i + 1] for i in range(8))
    # and the degree-4 truncation in t is not real-rooted:
    # P(t) = a0 - a1 t^2/2! + a2 t^4/4!, a quadratic in y = t^2
    c2, c1, c0 = a[0], -a[1] / 2, a[2] / 24
    assert c1 * c1 - 4 * c2 * c0 < 0, "expected negative discriminant"


def test_q_ratio_is_rescale_invariant():
    """No normalisation choice can rescue sec 7."""
    a = A.a_coeffs(4)
    q_raw = a[0] * a[2] / a[1] ** 2
    b = [v / a[0] for v in a]
    assert float(b[0] * b[2] / b[1] ** 2) == pytest.approx(float(q_raw), rel=1e-30)


# ----------------------------------------------------------------- error 3

def test_twelve_identity_and_index():
    """sec 12: D_n = a_n^2 r_n (r_n - r_(n+1)), and r_n' = -D_n/a_n^2."""
    a = A.a_coeffs(12)
    r = [a[n + 1] / a[n] for n in range(len(a) - 1)]
    for n in range(1, 9):
        D = a[n + 1] ** 2 - a[n] * a[n + 2]
        # correct identity
        assert D == pytest.approx(
            float(a[n] ** 2 * r[n] * (r[n] - r[n + 1])), rel=1e-30)
        # the document's form is genuinely different, not a rounding issue
        assert abs(D - a[n] ** 2 * (1 - r[n - 1] * r[n])) / abs(D) > 1e-3


def test_ratio_derivative_uses_D_n_not_D_n_plus_1():
    """r_n' = -D_n/a_n^2. The document writes -D_(n+1)/a_n^2 (wrong index).

    Verified by finite-differencing r_n along the actual deformation, so this
    tests the index rather than restating the algebra.
    """
    a0 = A.a_coeffs(12)
    h = mp.mpf("1e-6")

    def ratio_at(lam, n):
        c = A.deformed(a0, lam)
        return c[n + 1] / c[n]

    for n in (2, 4, 6):
        num = (ratio_at(h, n) - ratio_at(-h, n)) / (2 * h)
        D_n = a0[n + 1] ** 2 - a0[n] * a0[n + 2]
        D_next = a0[n + 2] ** 2 - a0[n + 1] * a0[n + 3]
        assert float(num) == pytest.approx(float(-D_n / a0[n] ** 2), rel=1e-4)
        # the wrong index gives a materially different number
        assert abs(float(num) - float(-D_next / a0[n] ** 2)) > 1e-3 * abs(float(num))


# ----------------------------------------------------------------- error 4

def test_newton_translation_is_vacuous():
    """sec 13: Newton gives (2k+1)/(2k-1) > 1, not the claimed < 1 margin."""
    a = A.a_coeffs(10)
    e = [((-1) ** k) * a[k] / (mp.factorial(2 * k) * a[0]) for k in range(10)]
    for k in range(2, 8):
        # Newton on e holds
        assert e[k - 1] * e[k + 1] / e[k] ** 2 <= mp.mpf(k) / (k + 1) + 1e-20
        # the document's claimed bound on a is FALSE for real coefficients
        obs = a[k - 1] * a[k + 1] / a[k] ** 2
        assert obs > mp.mpf(2 * k + 1) / (2 * k + 2)
        # and the correct translation is weaker than 1
        assert mp.mpf(2 * k + 1) / (2 * k - 1) > 1


# ------------------------------------------------------------- the good parts

def test_deformation_mechanism_verified():
    """The spine of the framework is right and must keep being right."""
    rep = _artifact()
    for sec, needle in (("10", "a_n' = a_(n+1)"),
                        ("10", "d_lambda Xi_lam = -d_t^2 Xi_lam"),
                        ("14", "sum x_n conserved"),
                        ("14", "E' = -sum_n"),
                        ("7", "q=0.9, r=0.5"),
                        ("8", "generic positive kernels"),
                        ("17", "sec 17 list of insufficient shortcuts")):
        assert _claim(rep, sec, needle)["agrees"] is True


def test_cubic_hyperbolicity_criterion_holds_for_real_roots():
    """sec 7's q^2r^2-6qr+4q+4r-3 <= 0 is the right cubic test."""
    import numpy as np
    rng = np.random.default_rng(11)
    seen = 0
    for _ in range(600):
        s = np.sort(rng.normal(0, 2, 3))
        e1, e2 = s.sum(), s[0] * s[1] + s[0] * s[2] + s[1] * s[2]
        e3 = s[0] * s[1] * s[2]
        if abs(e1) < 1e-9 or abs(e2) < 1e-9:
            continue
        q, r = e2 / e1 ** 2, e1 * e3 / e2 ** 2
        if q <= 0 or r <= 0:
            continue
        assert q <= 1.0 / 3.0 + 1e-12, "real roots force q <= 1/3"
        assert q * q * r * r - 6 * q * r + 4 * q + 4 * r - 3 <= 1e-9
        seen += 1
    assert seen > 100


def test_generic_kernel_deficit_is_a_stable_constant_factor():
    """sec 8: generic concentration has the right 1/n order but a bad constant."""
    rep = _artifact()
    det = _claim(rep, "8", "generic positive kernels")["detail"]
    assert "constant-factor deficit" in det
    # the numbers quoted must be internally consistent with the requirement
    # required (6n+8)/(2n+2)^2, generic ~2.7x larger at n=5,25,125
    for n, gen in ((5, 0.714), (25, 0.157), (125, 0.032)):
        req = (6 * n + 8) / (2 * n + 2) ** 2
        assert gen / req == pytest.approx(2.7, abs=0.1)
