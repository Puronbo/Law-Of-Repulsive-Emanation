import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "experiments"))

import mpmath as mp  # noqa: E402

import rh_widder_hankel_h6 as h6  # noqa: E402

mp.mp.dps = 40


def test_gammas_are_the_first_four_zeta_zeros():
    assert len(h6.GAMMAS) == 4
    assert all(g > 0 for g in h6.GAMMAS)
    assert list(h6.GAMMAS) == sorted(h6.GAMMAS)


def test_arg_q_exact_matches_direct_evaluation():
    """H6b: the closed form is exact, not an approximation."""
    worst = 0.0
    for g in h6.GAMMAS[:2]:
        for d in (mp.mpf("1e-2"), mp.mpf("1e-4")):
            for xs in (mp.mpf("1e-8"), g * g / 10, g * g, g * g * 10):
                direct = abs(mp.arg(h6._q(h6._w(g, d), xs)))
                closed = h6.arg_q_exact(g, d, xs)
                worst = max(worst, float(abs(direct - closed)))
    assert worst < 1e-30


def test_small_x_phase_law_is_linear():
    """At x << gamma^2 the phase tends to 2 delta/gamma (the H4a law)."""
    for g in h6.GAMMAS[:2]:
        for d in (mp.mpf("1e-4"), mp.mpf("1e-6")):
            th = h6.arg_q_exact(g, d, mp.mpf("1e-12"))
            assert float(th / (2 * d / g)) == pytest.approx(1.0, abs=1e-3)


def test_cubic_phase_law_coefficient_is_one():
    """H6c: at x = gamma^2 the phase is (delta/gamma)^3 -- coefficient 1.

    Guards the specific arithmetic error found while building H6: expanding
    2 atan(u) - atan(2u) naively gives 2/3 u^3, which is wrong because at
    x = gamma^2 the atan arguments carry O(u^2) perturbations.
    """
    for g in h6.GAMMAS[:2]:
        for dexp in (-4, -6):
            d = mp.mpf(10) ** dexp
            direct = abs(mp.arg(h6._q(h6._w(g, d), g * g)))
            assert float(direct / ((d / g) ** 3)) == pytest.approx(1.0, abs=1e-3)


def test_cubic_law_rejects_the_naive_two_thirds_coefficient():
    for g in h6.GAMMAS[:2]:
        d = mp.mpf("1e-4")
        direct = abs(mp.arg(h6._q(h6._w(g, d), g * g)))
        wrong = mp.mpf(2) / 3 * (d / g) ** 3
        assert float(direct / wrong) == pytest.approx(1.5, abs=1e-2)


def test_signed_phase_is_strictly_decreasing_in_x():
    """H6d: this is why the cubic point does not govern the route."""
    g = h6.GAMMAS[1]
    d = mp.mpf("1e-3")
    xs = [mp.mpf(10) ** e for e in range(-8, 7)]
    ths = [h6.arg_q_signed(g, d, x) for x in xs]
    assert all(ths[i] > ths[i + 1] for i in range(len(ths) - 1))


def test_absolute_phase_peaks_at_small_x():
    """|arg q| is largest at small x and relaxes to a constant as x -> inf."""
    g = h6.GAMMAS[1]
    d = mp.mpf("1e-3")
    th_small = h6.arg_q_exact(g, d, mp.mpf("1e-6"))
    th_big = h6.arg_q_exact(g, d, mp.mpf("1e8"))
    assert th_small > th_big > 0


def test_linear_law_holds_at_small_reference_x():
    """At x* = 2 delta gamma the phase is linear again, so m ~ pi gamma/(4 delta)."""
    for g in h6.GAMMAS[1:]:
        for d in (mp.mpf("1e-3"), mp.mpf("1e-4")):
            x_star, th = h6.x_phase_min(g, d)
            assert float(th / (2 * d / g)) == pytest.approx(1.0, abs=2e-2)


def test_exact_small_x_dominance_threshold():
    """H6a: dominance at x -> 0 is exactly delta^2 < gamma_2^2 - gamma_1^2.

    The condition is asymptotic in x, so it is tested at a small but finite
    x.  H6_XSMALL = 1e-6 is small enough that the ordering is unambiguous.
    """
    g1, g2 = h6.GAMMAS[0], h6.GAMMAS[1]
    crit = g2 ** 2 - g1 ** 2
    assert float(mp.sqrt(crit)) == pytest.approx(15.56, abs=0.01)
    for d, expect in ((mp.mpf(1), True), (mp.mpf(10), True),
                      (mp.mpf("15.5"), True), (mp.mpf("15.6"), False),
                      (mp.mpf(21), False)):
        w = h6._w(g1, d)
        mags = sorted((abs(h6._q(v, h6.H6_XSMALL))
                       for v in (w, g2 ** 2, h6.GAMMAS[2] ** 2)), reverse=True)
        assert (abs(h6._q(w, h6.H6_XSMALL)) == mags[0]) is expect
        assert (d * d < crit) is expect


def test_lowest_displaced_zero_makes_Q_m_negative():
    """H6a: the chain really produces a violation, at the predicted order."""
    g1 = h6.GAMMAS[0]
    x0 = mp.mpf("1e-3")
    qs = [h6._q(w, x0) for w in h6._spectrum(0, h6.H6_DELTA)]
    m_pred = int(mp.ceil(mp.pi * g1 / (4 * h6.H6_DELTA)))
    m_found = h6._first_negative_order(qs, 20000)
    assert m_found is not None
    assert m_found == pytest.approx(m_pred, rel=1e-3)


def test_on_axis_spectrum_never_violates():
    """Control: with every zero on-axis, all phases vanish and Q_m > 0."""
    ws = [g ** 2 for g in h6.GAMMAS]
    for x in (mp.mpf("1e-3"), mp.mpf(1), mp.mpf(100)):
        qs = [h6._q(w, x) for w in ws]
        assert h6._first_negative_order(qs, 2000) is None


def test_chain_extends_to_higher_displaced_zero():
    """H6e: the reduction to the lowest off-axis zero is NOT needed."""
    for k in (1, 2):
        xw = h6._first_winning_x(k, h6.H6_DELTA)
        assert xw is not None
        qs = [h6._q(w, xw) for w in h6._spectrum(k, h6.H6_DELTA)]
        assert h6._first_negative_order(qs, h6.H6_MCAP) is not None


def test_dominance_window_lies_below_gamma_squared():
    """The window is strictly left of the cubic point x = gamma^2."""
    for k in (1, 2, 3):
        xw = h6._first_winning_x(k, h6.H6_DELTA)
        assert xw is not None
        assert float(xw / h6.GAMMAS[k] ** 2) < 1.0
