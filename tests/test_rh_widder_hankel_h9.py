"""Regression tests for experiments/rh_widder_hankel_h9.py.

H9 exists because H7b was wrong in a way that was invisible from inside H7:
the zero sum was integrated against N(t) rather than against the counting
measure dN(t), which put a divergent factor t log t into the tail and
manufactured a log^2 divergence at m = 1 that does not exist.

Three separate defects are pinned here, and the first two are defects in the
CORRECTION itself -- which is the harder case, since the threshold conclusion
survived both of them:

  * the Jacobian.  Substituting t = T e^s gives dt = t ds, so the integrand
    is [log(t/2pi)/(2pi)] t^{1-2m}, not t^{-2m}.  The no-Jacobian version was
    230x too small at m = 1.  A bounded positive factor cannot change
    convergence, so every threshold gate still passed while every magnitude
    was wrong -- the exact signature of a correction that needs its own
    independent check rather than a re-run;
  * settling must be read on the SETTLED windows.  At ceiling 1e4 the m = 1
    tail is still 2.2% short of its limit, which is convergence in progress,
    not drift;
  * mp.quad(..., mp.inf) silently returned a finite value for a provably
    divergent integral, 2.46e57, and reported "converges: True".
"""

import json
import os

import mpmath as mp

import experiments.rh_widder_hankel_h9 as h9

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "experiments", "data", "rh_widder_hankel_h9_data.json")

mp.mp.dps = 30


def _report():
    with open(DATA, encoding="utf-8") as fh:
        return json.load(fh)


def test_artifact_exists_and_all_gates_pass():
    rep = _report()
    assert rep["gates"], "no gates recorded"
    assert all(g["passed"] for g in rep["gates"]), [
        g["gate"] for g in rep["gates"] if not g["passed"]]


def test_true_tail_matches_its_closed_form():
    """REGRESSION: the Jacobian t from dt = t ds was omitted, giving
    2.600e-5 against the true 5.9958e-3. Pin the closed form, not just
    self-consistency between two ceilings."""
    T = mp.mpf(100)
    closed = (mp.log(T / h9.PI2) + 1) / (h9.PI2 * T)
    got = h9.true_tail(1, T, mp.mpf(10) ** 14)
    assert abs(got - closed) / closed < mp.mpf("1e-9"), (got, closed)

    # and the omitted factor is large enough to have been worth checking
    rep = _report()["h9_jacobian_check"]
    assert rep["closed_over_no_jacobian"] > 100, rep
    assert rep["rel_err"] < 1e-9, rep


def test_h7b_integrates_the_count_not_the_measure():
    """dN/dt = log(t/2pi)/(2pi) while N ~ (t/2pi) log(t/2pi), so H7b's
    integrand is too large by a factor that DIVERGES."""
    rep = _report()
    tt = rep["h9_m1_tails"]
    assert tt["true"][-1] < 1e-2, tt
    assert tt["h7"][-1] / tt["h7"][0] > 1.2, "H7b's tail must creep upward"
    # H7b's grows with the ceiling while the correct one has settled
    assert tt["h7"][-1] > 100 * tt["true"][-1], tt


def test_correct_tail_settles_and_h7b_does_not():
    """REGRESSION: flatness asserted over the WARM-UP window fails on the
    warm-up. Flatness is a statement about the settled windows only."""
    rep = _report()
    tt = rep["h9_m1_tails"]
    warm = abs(tt["true"][0] / tt["true"][-1] - 1)
    settled = rep["h9_true_flat_settled"]
    assert warm > 1e-2, "ceiling 1e4 should still be short, else the test is void"
    assert settled < 1e-5, (settled, tt["true"])


def test_threshold_is_twice_m_greater_than_one():
    """m = 1/2, decided by the sharpness of the drift transition rather than
    an absolute tolerance: m = 0.7 is convergent with a slow power-law tail,
    so a fixed tolerance would mislabel it divergent."""
    rows = _report()["h9_threshold"]
    drift = {r["m"]: r["rel_drift"] for r in rows}
    assert drift[0.51] > 1.0, drift
    assert drift[0.7] < 0.1, drift
    assert drift[0.51] / drift[0.7] > 50, drift
    for m in (0.3, 0.45, 0.49, 0.5, 0.51):
        assert drift[m] > 1.0, (m, drift[m])
    assert drift[1.0] < 1e-4, drift
    assert drift[2.0] < 1e-12, drift


def test_mp_inf_quadrature_is_never_used():
    """REGRESSION: mp.quad(..., mp.inf) returned 2.46e57 for an integral that
    provably diverges, and reported convergence. Every tail here must take a
    FINITE ceiling as an argument."""
    T = mp.mpf(100)
    bad = mp.quad(lambda s: (mp.log(T * mp.e ** s / h9.PI2) / h9.PI2)
                            * (T * mp.e ** s) ** (1 - 2 * mp.mpf("0.5")),
                  [0, mp.inf])
    assert not mp.isfinite(bad) or abs(bad) > mp.mpf(10) ** 40, bad
    # the same integral with a finite ceiling grows slowly and modestly:
    # at m = 1/2 the tail is (log(Tmax/2pi))^2, so 1e8 -> 1e14 is a factor
    # of about 3.4, NOT a factor of 10^40.  Slow growth is the signature of
    # the borderline exponent 2m = 1 and is exactly what mp.inf hid.
    a = h9.true_tail(mp.mpf("0.5"), T, mp.mpf(10) ** 8)
    b = h9.true_tail(mp.mpf("0.5"), T, mp.mpf(10) ** 14)
    assert 2 < b / a < 10, (a, b, b / a)


def test_pointwise_factor_approaches_t_from_below():
    """N/(dN/dt) = t up to the O(1) RVM correction, so the measured factor
    approaches t monotonically from below rather than landing inside a
    pre-chosen band."""
    pw = _report()["h9_pointwise_factor"]
    ratios = [r["ratio_over_t"] for r in pw]
    assert ratios[0] < 1.0, ratios
    assert all(ratios[i] < ratios[i + 1] for i in range(len(ratios) - 1)), ratios
    assert ratios[-1] > 0.9, ratios


def test_tail_ratio_rises_because_h7b_is_top_dominated():
    """REGRESSION: an earlier cut asserted the ratio of the two tails is of
    order T. It is not -- the correct tail is bottom-dominated and converges,
    H7b's grows like (log Tmax)^2, so the ratio diverges."""
    rows = _report()["h9_error_factor"]
    ratios = [r["ratio"] for r in rows]
    assert all(ratios[i] < ratios[i + 1] for i in range(len(ratios) - 1)), ratios
    assert ratios[-1] / ratios[0] > 10, ratios


def test_measure_is_locally_finite():
    """dmu = 2 sum delta_{gamma^2}: mass 2N(sqrt T) is a finite COUNT for every
    finite T. mass/T falls, which is the o(T) that local finiteness needs."""
    rows = _report()["h9_measure_mass"]
    assert all(r["mass_2N"] < r["T"] for r in rows), rows
    assert rows[-1]["mass_over_T"] < 0.01, rows


def test_conclusion_is_scoped_and_records_the_jacobian():
    concl = _report()["conclusion"]
    assert "Nothing here proves or refutes RH" in concl
    assert "remains OPEN" in concl
    assert "Jacobian" in concl, "the correction must record its own defect"