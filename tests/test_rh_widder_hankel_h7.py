"""Regression tests for experiments/rh_widder_hankel_h7.py.

H7 audited the convergence/interchange claims of record section 28 and found
two of its own gates asserting things that were false.  Both errors ran the
same way: a plausible-looking substitution was carried out incorrectly, the
result was large, and the large number was then explained by the physical
question rather than re-derived from it.

  * the measure.  A zero sum is integrated against the COUNTING MEASURE
    dN(t) = (1/2pi) log(t/2pi) dt, not against N(t) dt.  Integrating N(t)
    t^-2m dt weights the count by dt and puts a divergent factor t log t into
    the tail, which is what manufactured a log^2 divergence of Q_1.  The real
    threshold is 2m > 1, so Q_1 converges;
  * the Jacobian.  Substituting t = T e^s gives dt = t ds, so the log-height
    integrand carries t^{1-2m}, not t^{-2m}.  Dropping it understated the
    m = 1 tail by a factor of 230 while leaving every threshold gate green --
    a bounded factor cannot change convergence, so the correction survived its
    own magnitude error.

The zero-counting gate was wrong a third time: it tallied sign changes of
Im zeta(1/2+it), which vanish wherever zeta(1/2+it) is real and therefore
roughly double the true count of zeros of xi.  It also "confirmed" the
Riemann-von Mangoldt asymptotic against a field holding log10(U) rather than
U, so a bound of about 2 was applied to masses of 58, 296 and 1298.

These tests read the artifact rather than calling main(), matching the
convention of the H8 and H9 test modules.
"""

import json
import os

import mpmath as mp

import experiments.rh_widder_hankel_h7 as h7

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "experiments", "data", "rh_widder_hankel_h7_data.json")

mp.mp.dps = 30
T0 = mp.mpf(100)


def _report():
    with open(DATA, encoding="utf-8") as fh:
        return json.load(fh)


def test_all_gates_pass_and_conclusion_is_scoped():
    rep = _report()
    assert rep["gates"], "no gates recorded"
    assert all(g["passed"] for g in rep["gates"]), \
        [g["gate"] for g in rep["gates"] if not g["passed"]]
    concl = rep["conclusion"]
    assert "Nothing here proves or refutes RH" in concl
    assert "remains OPEN" in concl


def test_refined_zeros_really_are_zeta_zeros():
    """The Newton refinement must land on xi(1/2 + i gamma) = 0."""
    gammas = [h7.zeta_zero_gamma(s) for s in h7.SEEDS]
    assert gammas == sorted(gammas)
    assert abs(gammas[0] - mp.mpf("14.134725141734693790")) < mp.mpf("1e-12")
    for g in gammas:
        assert abs(h7._xi(mp.mpc(mp.mpf("0.5"), g))) < mp.mpf("1e-20")


def test_decimal_digits_of_q_are_exponent_minus_two():
    """H7a: q ~ gamma^-2, not gamma^-4.  |w|/|w|^2 = 1/|w|, so the numerator
    cancels one power of the squared denominator.  An earlier cut asserted
    gamma^-4, measured -2.00, and explained the mismatch away as a sampling
    regime; the measurement was right."""
    gammas = [h7.zeta_zero_gamma(s) for s in h7.SEEDS]
    ls = [(mp.log(g), mp.log(g * g / (h7.H7_X + g * g) ** 2)) for g in gammas]
    n = len(ls)
    sx = mp.fsum(a for a, _ in ls)
    sy = mp.fsum(b for _, b in ls)
    sxx = mp.fsum(a * a for a, _ in ls)
    sxy = mp.fsum(a * b for a, b in ls)
    slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    assert abs(float(slope) + 2.0) < 0.05
    assert abs(float(slope) - _report()["h7_real_slope"]) < 1e-3


def test_q1_tail_converges_to_its_closed_form():
    """H7b CORRECTED.  Q_1 is finite, so the log^2 divergence is gone and with
    it the claimed threshold 2m > 2.  Pin the closed form rather than only
    self-consistency between ceilings."""
    tails = [r["tail"] for r in _report()["h7_growth_m1"]]
    closed = (mp.log(T0 / h7.PI2) + 1) / (h7.PI2 * T0)
    assert abs(tails[-1] - float(closed)) / float(closed) < 1e-8, (tails[-1], closed)
    # settled, i.e. an actual limit rather than a drift
    assert abs(tails[-1] / tails[-2] - 1) < 1e-9, tails
    # and the first ceiling is visibly short, so the flatness is not vacuous
    assert tails[0] / tails[-1] < 0.999, tails


def test_threshold_is_twice_m_greater_than_one():
    """m = 1/2 is the borderline and must NOT converge; m = 1 must.  A gate that
    only checked the convergent side would have passed the original error."""
    assert float(h7.tail(T0, 1, mp.mpf(10) ** 14, measure="dN")[0]) < 1e-2
    borderline = [float(h7.tail(T0, mp.mpf("0.5"), mp.mpf(10) ** e,
                               measure="dN")[0])
                 for e in (4, 8, 14)]
    assert borderline == sorted(borderline)
    assert borderline[-1] / borderline[0] > 2, borderline
    for m in (2, 3):
        big = float(h7.tail(T0, m, mp.mpf(10) ** 12, measure="dN")[0])
        assert big < 1e-3, (m, big)


def test_h7b_formula_is_the_dN_less_one():
    """measure="N" is H7's original, wrong integrand; it must stay available so
    the two can be compared, and it must overshoot the correct tail."""
    good = float(h7.tail(T0, 1, mp.mpf(10) ** 14, measure="dN")[0])
    bad = float(h7.tail(T0, 1, mp.mpf(10) ** 14, measure="N")[0])
    assert bad > 1000 * good, (good, bad)
    # and the artifact records the same contrast
    tt = _report()
    n_rows = [r["tail"] for r in tt["h7_growth_m1_Nweighted"]]
    assert n_rows[-1] > 1000 * good, n_rows
    assert n_rows == sorted(n_rows), "the wrong integrand must creep upward"


def test_log_height_quadrature_has_the_jacobian():
    """dt = t ds.  Cross-check against a direct quadrature in t, which cannot
    share the substitution error."""
    T, Tmax = T0, mp.mpf(10) ** 8
    val = h7.tail(T, 1, Tmax, measure="dN")[0]
    direct = mp.quad(lambda t: h7.dN_asym(t) * t ** -2, [T, Tmax])
    assert abs(float(val / direct) - 1.0) < 1e-8, (val, direct)

    # the exponent that was used before the fix drops the t from dt
    buggy = mp.quad(lambda t: h7.dN_asym(t) * t ** -1, [T, Tmax])
    assert float(val) < float(buggy) / 100, (val, buggy)

    # both the quad and the Simpson cross-check agree
    quad, simpson = h7.tail(T, 1, Tmax, measure="dN")
    assert abs(float(quad / simpson) - 1.0) < 1e-8, (quad, simpson)


def test_zero_counter_counts_zeros_of_xi_not_zeros_of_im_zeta():
    """REGRESSION: sign changes of Im zeta(1/2+it) happen wherever
    zeta(1/2+it) is real, which is about twice as often as the zeros of xi.
    At t <= 100 that is 58 against the true 29, and an earlier gate would
    have 'confirmed' Riemann-von Mangoldt against a doubled count."""
    assert h7.count_zeros_upto(100) == 29
    assert h7.count_zeros_upto(200) == 79

    half = mp.mpf("0.5")
    t, wrong = mp.mpf(14), 0
    prev = mp.sign(mp.im(mp.zeta(mp.mpc(half, t))))
    while t < 100:
        t += mp.mpf("0.5")
        cur = mp.sign(mp.im(mp.zeta(mp.mpc(half, t))))
        if prev * cur < 0:
            wrong += 1
        prev = cur
    assert wrong == 58, wrong
    assert wrong > 1.5 * h7.count_zeros_upto(100)


def test_zero_counter_step_is_finer_than_the_close_pairs():
    """A step of 0.5 steps over close pairs below t = 1000 and reports 645
    where the true count is 649 -- four sign changes lost, which is the entire
    margin the Riemann-von Mangoldt comparison rests on."""
    assert h7.count_zeros_upto(1000, step=mp.mpf("0.25")) == 649
    assert abs(float(h7.N_asym(1000)) - 649) < 1.0


def test_dmu_is_locally_finite_as_a_count():
    """H7d CORRECTED.  mu([0,U]) = 2 #{gamma : gamma^2 <= U} is finite for
    every finite U, and grows like U^{1/2} log U, so it is o(U).  Unbounded
    TOTAL mass on unbounded support is what every counting measure has."""
    rows = _report()["h7_dmu_local_mass"]
    assert [r["log10U"] for r in rows] == [4.0, 5.0, 6.0], rows
    for r in rows:
        assert isinstance(r["counted"], int)
        assert r["counted"] < r["U"], r
        assert abs(r["asym"] - r["counted"]) <= 3.0, r
    counts = [r["counted"] for r in rows]
    assert counts == sorted(counts) and len(set(counts)) == 3, counts


def test_q1_and_f_xi_are_asymptotically_the_same_series():
    """H7c: the ratio of summands is w/(x+w) -> 1, so moment identification
    transfers.  No regularization is owed at m = 1 because both series
    converge there."""
    x = mp.mpf("1000")
    ratios = [float(g * g / (x + g * g))
              for g in (x * 10, x * 100, x * 1000, x * 10000)]
    assert ratios == sorted(ratios)
    assert abs(ratios[-1] - 1.0) < 1e-6


def test_n_asym_is_not_clamped():
    """RvM truncated at 7/8 dips negative below T ~ 9.677.  Clamping it to
    >= 1 silently destroys the divergence being measured, which also means the
    callers must stay above that height."""
    assert h7.N_asym(mp.mpf(5)) < 0
    assert h7.N_asym(mp.mpf(10)) > 0
    assert h7.N_asym(mp.mpf(50)) > 0
    assert abs(float(h7.N_asym(100)) - 29.0) < 0.05
    assert abs(float(h7.N_asym(1000)) - 649.0) < 1.0