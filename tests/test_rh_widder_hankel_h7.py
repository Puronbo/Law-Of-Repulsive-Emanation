import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "experiments"))

import mpmath as mp  # noqa: E402

import rh_widder_hankel_h7 as h7  # noqa: E402

mp.mp.dps = 40


def test_refined_zeros_really_are_zeta_zeros():
    """The Newton refinement must land on xi(1/2 + i gamma) = 0."""
    gammas = [h7.zeta_zero_gamma(s) for s in h7.SEEDS]
    assert len(gammas) == len(h7.SEEDS)
    assert all(g > 0 for g in gammas)
    assert gammas == sorted(gammas)
    assert abs(gammas[0] - mp.mpf("14.134725141734693790")) < mp.mpf("1e-12")
    for g in gammas:
        assert abs(h7._xi(mp.mpc(mp.mpf("0.5"), g))) < mp.mpf("1e-20")


def test_decimal_digits_of_q_are_exponent_minus_two():
    """H7a: q ~ gamma^-2, not gamma^-4.

    Guards the exact arithmetic slip found while building H7.  The numerator w
    cancels one power of the squared denominator, since |w|/|w|^2 = 1/|w|.
    An earlier cut asserted gamma^-4, measured -2.00, and then explained the
    mismatch away as an undersampled asymptotic regime.  The -2.00 was right.
    """
    gammas = [h7.zeta_zero_gamma(s) for s in h7.SEEDS]

    def q_of(g):
        return g * g / (h7.H7_X + g * g) ** 2

    ls = [(mp.log(g), mp.log(q_of(g))) for g in gammas]
    n = len(ls)
    sx = mp.fsum(a for a, _ in ls)
    sy = mp.fsum(b for _, b in ls)
    sxx = mp.fsum(a * a for a, _ in ls)
    sxy = mp.fsum(a * b for a, b in ls)
    slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    assert abs(float(slope) + 2.0) < 0.05

    # And the asymptote q ~ x^2/gamma^4, reached from below with the right
    # SIGN: q gamma^4 / x^2 climbs by ~10 per decade of gamma.
    vals = []
    for mult in (10, 100, 1000, 10000):
        g = h7.H7_X * mult
        vals.append(float(q_of(g) * g ** 4 / h7.H7_X ** 2))
    assert vals == sorted(vals)
    assert vals[-1] / vals[0] > 1000


def test_q1_tail_diverges_and_q2_tail_converges():
    """H7b: the m=1/m=2 crossover, and the log^2 growth law of the m=1 tail."""
    T0 = mp.mpf(100)
    g1 = [float(h7.tail(T0, 1, c)[0])
          for c in (mp.mpf(10) ** 4, mp.mpf(10) ** 8, mp.mpf(10) ** 12)]
    assert g1 == sorted(g1)
    assert g1[-1] / g1[0] > 5

    # Ratio to the predicted (log Tmax)^2/(4pi) climbs monotonically to 1.
    ceilings = (mp.mpf(10) ** 4, mp.mpf(10) ** 8, mp.mpf(10) ** 12)
    ratio = [g1[i] / float(mp.log(c / h7.PI2) ** 2 / (4 * mp.pi))
             for i, c in enumerate(ceilings)]
    assert ratio == sorted(ratio)
    assert 0.6 < ratio[-1] < 1.5

    # m = 2 and m = 3 converge: bounded and settling, not growing.
    for m, ceiling in ((2, mp.mpf(10) ** 8), (3, mp.mpf(10) ** 6)):
        small = float(h7.tail(T0, m, mp.mpf(10) ** 2)[0])
        big = float(h7.tail(T0, m, ceiling)[0])
        assert big <= small * (1 + 1e-6) or big < 1e-3


def test_tail_integrand_uses_the_right_jacobian():
    """Guards the substitution error: dt = t ds gives exponent 1-2m.

    With exponent 2-2m the m=1 tail integrates N(t) instead of N(t)/t, grows
    like t log t, and comes out as ~Tmax^2 (3.8e12 at 1e12), masking the log^2
    divergence completely.
    """
    T, Tmax = mp.mpf(100), mp.mpf(10) ** 6
    val = h7.tail(T, 1, Tmax)[0]
    # Independent direct quadrature in t, which cannot share the Jacobian bug.
    direct = mp.quad(lambda t: h7.N_asym(t) * t ** -2, [T, Tmax])
    assert abs(float(val / direct) - 1.0) < 1e-6

    # The buggy exponent would give something orders of magnitude larger.
    buggy = mp.quad(lambda t: h7.N_asym(t) * t ** -1, [T, Tmax])
    assert float(val) < float(buggy)


def test_q1_and_f_xi_are_asymptotically_the_same_series():
    """H7c: the ratio of summands is w/(x+w) -> 1."""
    x = mp.mpf("1000")
    ratios = []
    for mult in (10, 100, 1000, 10000):
        g = x * mult
        ratios.append(float(g * g / (x + g * g)))
    assert ratios == sorted(ratios)
    assert abs(ratios[-1] - 1.0) < 1e-6


def test_n_asym_is_not_clamped():
    """RvM's truncated formula dips negative below T ~ 9.677; clamping is fatal.

    An earlier probe clamped N(T) to >= 1, which quietly replaced the very
    divergence it was trying to measure.  The sign is a direct check that no
    clamp is present.
    """
    assert h7.N_asym(mp.mpf(5)) < 0
    assert h7.N_asym(mp.mpf(10)) > 0
    assert abs(float(h7.N_asym(100)) - 29.0) < 0.05
    assert abs(float(h7.N_asym(1000)) - 649.0) < 1.0
    assert h7.N_asym(mp.mpf(50)) > 0


def test_all_gates_pass_and_conclusion_is_honest():
    assert h7.main() == 0
    passed = [g for g in h7.report["gates"] if g["passed"]]
    assert len(passed) == len(h7.report["gates"]) == 4

    text = h7.report["conclusion"]
    assert "NOT ALL GATES PASSED" not in text
    # No proof of RH is claimed, and the open bridge is still named open.
    assert "proves or refutes RH" in text
    assert "remains OPEN" in text
