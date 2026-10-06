"""Regression tests for 02_Experimental_Implementations_and_Verification/
01_Poincare_Universe_and_Cosmological_Models/origin_consistency_window_n7.py.

N7 reduces the FLATNESS and HORIZON initial-value problems to two sign tests on a
single stiffness integral

    S := int (1 + 3w) dln a

which is additive over eras and path independent.  Because `eps_obs < eps_i`,
the flatness bound `S < ln(eps_obs/eps_i)` is strictly stronger than the horizon
bound `S < 0`, so ONE inequality does both jobs.

WHAT IS PINNED, AND WHY.

  * The EXACT curvature law `eps = 1/(D a^(-1-3w) - sigma)`, against direct
    Friedmann integration.  This is a solved ODE, not an expansion.

  * THE SIGN OF `sigma`.  The denominator carries `- sigma`, not `+ sigma`,
    because `-k = -sigma |k|`.  With the sign flipped an OPEN universe
    (`sigma = -1`) sends `eps` negative at late times -- and `eps` is
    `|Omega - 1|`, a magnitude, so a negative value is not a small error but a
    broken identity.  `test_the_sigma_sign_is_minus_not_plus` pins both
    directions: the correct form stays positive for all `a > 0`, and the
    wrong form demonstrably does not, so the test has teeth.

  * The exact correction ratios

        eps_exact / eps_leading = 1/(1 - sigma/X)
        r_exact   / r_leading   = (1 - sigma/X)^(-1/2),   X = D a^(-1-3w)

    and, with them, that the familiar power laws are ASYMPTOTIC.  A first draft
    of this node probed `eps ~ a^(1+3w)` at large `N`, i.e. LATE times, where
    `X -> 0` and the leading law is wrong by orders of magnitude.  The gates
    were numerically self-consistent and physically meaningless.
    `test_the_leading_laws_are_asymptotic_and_fail_at_late_time` is the
    regression that keeps `n7b`/`n7c` honest.

  * The `1/sqrt(D)` normalisation in the radius leading law, and its
    `(1+3w)/2` exponent.

  * THE HORIZON DIRECTION.  The requirement is `r_f < r_i`, i.e. the comoving
    Hubble radius must SHRINK, i.e. `S < 0`.  A first draft had `S > 0`.  Since
    the matter era contributes `S = +80` on its own, the flipped sign does not
    fail loudly -- it silently makes the matter era a *fix* for the horizon
    problem when it is in fact an aggravation.

  * THAT `w = -1/3` IS A BOUNDARY OF THE LAW, NOT A SOLUTION.  The stiffness
    density vanishes exactly there, so `eps` and `r` are invariant under any
    length at `w = -1/3`.  Read carelessly that looks like "the beginning is
    free"; it is not an admissible history, and matter afterwards ruins it.

  * THAT STRICTNESS MATTERS: `S == S_req` is INADMISSIBLE (`<`, not `<=`).

  * THE LIMITS, as tests rather than as prose, because prose drifts:
      - `eps_i` is an INPUT; nothing here fixes `|Omega_i - 1|`;
      - the cause / beginning is NOT ADDRESSED;
      - `w = -1` is exact de Sitter; quasi-de Sitter changes the NUMBER of
        e-folds, not the sign test;
      - the claims are conditional on an assumed FLRW + GR history.
    A suite that only checked the numerics would let the scope creep silently,
    so the scope block is asserted to be present and to say what it says.
"""

import glob
import io
import json
import math
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))

EXPERIMENTS = os.path.join(
    REPO,
    "02_Experimental_Implementations_and_Verification",
    "01_Poincare_Universe_and_Cosmological_Models",
)
DATA_DIR = os.path.join(
    REPO,
    "03_Data_and_Observational_Resources",
    "02_Experimental_Data_Collections",
)

if not os.path.isdir(EXPERIMENTS):
    _found = glob.glob(
        os.path.join(REPO, "0[1-5]_*", "*", "origin_consistency_window_n7.py")
    )
    if not _found:
        raise RuntimeError(
            "cannot locate origin_consistency_window_n7.py beneath %s" % REPO
        )
    EXPERIMENTS = os.path.dirname(_found[0])

if EXPERIMENTS not in sys.path:
    sys.path.insert(0, EXPERIMENTS)

import origin_consistency_window_n7 as n7  # noqa: E402

DATA = os.path.join(DATA_DIR, "origin_consistency_window_n7_data.json")

# the numerical slice the gates actually run on
RHO_I, K, D, SIGMA = n7.normalisation()

WS = [0.0, 0.5, n7.W_RAD, 1.0]


def _report():
    if not os.path.exists(DATA):
        pytest.skip("artifact not generated yet: %s" % DATA)
    with open(DATA, encoding="utf-8") as fh:
        return json.load(fh)


def _eps_plus_sigma(a, w, d, sigma):
    """The WRONG-sign variant, kept here so the sign test can show it fails."""
    return 1.0 / (d * a ** (-1.0 - 3.0 * w) + sigma)


# ---------------------------------------------------------------------------
# the normalisation: D, rho_i, sigma must all come out of Friedmann at a_i = 1
# ---------------------------------------------------------------------------
def test_normalisation_satisfies_friedmann_at_the_initial_slice():
    """h_i^2 = (8piG/3) rho_i - k with h_i = 1, so rho_i = (3/8pi)(1 + k)."""
    for eps_i in [1e-4, 1e-2, 5e-2, 0.4]:
        rho_i, k, d, sigma = n7.normalisation(eps_i)
        assert abs(k + eps_i) < 1e-18          # k = -eps_i, open
        assert sigma == -1.0                   # open => no turnaround point
        assert abs((8.0 * math.pi / 3.0) * rho_i - k - 1.0) < 1e-14
        assert abs(d - (1.0 + k) / abs(k)) < 1e-12 * abs(d)
        assert abs((8.0 * math.pi / 3.0) * rho_i / abs(k) - d) < 1e-12 * abs(d)


def test_the_slice_normalisation_constants():
    assert n7.EPS_I_NUM == 1e-2
    assert abs(K - (-0.01)) < 1e-18
    assert abs(D - 99.0) < 1e-12
    assert SIGMA == -1.0
    assert abs(RHO_I - 0.118173) < 1e-6


def test_eps_at_the_initial_slice_equals_eps_i_regardless_of_w():
    """eps(1) = 1/(D - sigma), independent of w.  If this drifts, the run does
    not start from the curvature it claims to start from."""
    for w in WS + [-1.0, -1.0 / 3.0]:
        assert abs(n7.eps_closed(1.0, w, D, SIGMA) - n7.EPS_I_NUM) < 1e-15


# ---------------------------------------------------------------------------
# the exact curvature law
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("w", WS)
def test_closed_form_curvature_law_matches_direct_friedmann(w):
    """The closed form is a SOLVED ODE.  It is checked against Friedmann + the
    continuity equation, not against itself."""
    for a in [1e-3, 0.05, 0.5, 1.0, 3.0, 40.0, 1e4, 1e6]:
        got = n7.eps_from_friedmann(a, RHO_I, K, w)
        want = n7.eps_closed(a, w, D, SIGMA)
        assert abs(got - want) <= 1e-12 * want


def test_the_sigma_sign_is_minus_not_plus():
    """`eps` is a MAGNITUDE, so a negative value is not a small error but a
    broken identity.  The correct `- sigma` keeps it positive for every a > 0;
    the `+ sigma` draft does not.  Both halves are asserted so this test cannot
    pass vacuously."""
    probe = [1e-6, 1e-3, 0.1, 1.0, 10.0, 1e3, 1e6]
    for w in WS:
        for a in probe:
            assert n7.eps_closed(a, w, D, SIGMA) > 0.0
            assert n7.eps_from_friedmann(a, RHO_I, K, w) > 0.0
    # the wrong sign is genuinely broken somewhere on the probe grid
    assert any(
        _eps_plus_sigma(a, w, D, SIGMA) < 0.0 for w in WS for a in probe
    )


def test_open_universe_eps_grows_with_a_and_never_exceeds_unity():
    """Sanity on the direction of travel: curvature RELATIVE to matter grows as
    matter dilutes faster than curvature does, so for w = 0 open, eps rises
    from eps_i toward 1 as a -> infinity."""
    vals = [n7.eps_closed(a, 0.0, D, SIGMA) for a in [1.0, 10.0, 100.0, 1e4, 1e8]]
    assert all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))
    assert vals[-1] < 1.0 + 1e-9
    assert abs(vals[-1] - 1.0) < 1e-3


# ---------------------------------------------------------------------------
# the exact correction ratios, and the asymptotic status of the leading laws
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("w", WS)
def test_exact_correction_ratio_for_eps(w):
    """eps_exact / eps_leading = 1/(1 - sigma/X) exactly."""
    for n in [0.02, 0.1, 0.25, 0.5, 0.75, 1.5]:
        a = math.exp(n)
        x = D * a ** (-1.0 - 3.0 * w)
        ex = n7.eps_closed(a, w, D, SIGMA)
        ld = n7.eps_leading(a, w, D)
        assert abs(ex / ld - 1.0 / (1.0 - SIGMA / x)) < 1e-12


@pytest.mark.parametrize("w", WS)
def test_exact_correction_ratio_for_radius(w):
    """r_exact / r_leading = (1 - sigma/X)^(-1/2) exactly."""
    for n in [0.02, 0.1, 0.25, 0.5, 0.75, 1.5]:
        a = math.exp(n)
        x = D * a ** (-1.0 - 3.0 * w)
        ex = n7.r_closed(a, w, D, SIGMA, K)
        ld = n7.r_leading(a, w, D, K)
        assert abs(ex / ld - 1.0 / math.sqrt(1.0 - SIGMA / x)) < 1e-12


def test_the_leading_laws_are_asymptotic_and_fail_at_late_time():
    """THE REGRESSION.  `X = D a^(-1-3w) >> 1` is EARLY time -- which is exactly
    the flatness regime.  Probing the leading laws at large N (late time) tests
    nothing but arithmetic, and the draft did precisely that."""
    w = 0.0
    # early: X >> 1, the power law is excellent
    for a in [1e-2, 1e-3, 1e-4]:
        x = D * a ** -1.0
        ratio = n7.eps_closed(a, w, D, SIGMA) / n7.eps_leading(a, w, D)
        assert x > 100.0
        assert abs(ratio - 1.0) < 1e-2
    # late: X -> 0, the power law is wrong by orders of magnitude.  For an OPEN
    # slice the ratio is X/(X+1), which falls to ZERO: the leading law
    # OVERSHOOTS eps badly once curvature stops being negligible.
    for a in [1e3, 1e4, 1e6]:
        x = D * a ** -1.0
        ratio = n7.eps_closed(a, w, D, SIGMA) / n7.eps_leading(a, w, D)
        assert x < 1.0
        assert ratio < 0.5
        assert abs(ratio - 1.0 / (1.0 - SIGMA / x)) < 1e-12
    assert n7.eps_closed(1e6, w, D, SIGMA) / n7.eps_leading(1e6, w, D) < 1e-3


def test_radius_leading_law_carries_the_inverse_sqrt_D_normalisation():
    """r_leading(1, w, D, k) = 1/sqrt(|k| D).  A first draft omitted the
    sqrt(D), which is a pure constant offset -- invisible in any ratio of two
    leading-law values, and fatal as a normalisation."""
    for d in [1.5, 99.0, 1e4]:
        for w in WS + [-1.0]:
            assert abs(n7.r_leading(1.0, w, d, K) - 1.0 / math.sqrt(abs(K) * d)) < 1e-15


def test_radius_leading_law_has_the_half_exponent():
    """r ~ a^((1+3w)/2), not a^(1+3w).  Pinned as a scaling relation."""
    for w in WS + [-1.0]:
        a1, a2 = 2.0, 8.0
        got = n7.r_leading(a2, w, D, K) / n7.r_leading(a1, w, D, K)
        assert abs(got - (a2 / a1) ** ((1.0 + 3.0 * w) / 2.0)) < 1e-12


# ---------------------------------------------------------------------------
# S itself: the stiffness density, additivity, path independence
# ---------------------------------------------------------------------------
def test_stiffness_vanishes_exactly_at_w_minus_one_third():
    assert n7.stiffness(-1.0 / 3.0) == 0.0
    assert n7.stiffness(-1.0) == -2.0
    assert n7.stiffness(0.0) == 1.0
    assert n7.stiffness(n7.W_RAD) == 2.0
    # only w < -1/3 contributes negatively
    assert n7.stiffness(-0.9) < 0.0
    assert n7.stiffness(-0.1) > 0.0


def test_s_is_additive_and_order_independent_over_eras():
    paths = [
        [(n7.W_INFL, 60.0), (0.0, n7.N_MATTER)],
        [(n7.W_INFL, 10.0), (-0.5, 3.0)],
        [(0.0, 7.0), (n7.W_RAD, 11.0)],
        [(n7.W_INFL, 5.0), (-0.9, 2.0), (0.0, 30.0), (n7.W_RAD, 4.0)],
    ]
    for eras in paths:
        s = n7.s_of_path(eras)
        assert abs(s - n7.s_of_path(list(reversed(eras)))) < 1e-12
        # splitting an era into pieces of the same w must not change S
        w0, n0 = eras[0]
        thirds = [(w0, n0 / 3.0)] * 3 + eras[1:]
        assert abs(s - n7.s_of_path(thirds)) < 1e-12
        # and it must equal the sum of the individual contributions
        assert abs(s - sum(n7.stiffness(w) * n for w, n in eras)) < 1e-12
        # concatenation of two histories is the sum of their S
        assert abs(n7.s_of_path(eras + paths[1]) - (s + n7.s_of_path(paths[1]))) < 1e-12


def test_s_total_matches_the_two_era_form():
    for n_infl in [0.0, 12.0, 42.2549, 60.0]:
        assert abs(
            n7.s_total(n7.W_INFL, n_infl, 0.0, n7.N_MATTER)
            - (n7.stiffness(n7.W_INFL) * n_infl + n7.stiffness(0.0) * n7.N_MATTER)
        ) < 1e-12


# ---------------------------------------------------------------------------
# the two admissibility conditions
# ---------------------------------------------------------------------------
def test_s_required_is_negative_when_eps_obs_is_below_eps_i():
    """This negativity is what makes flatness the BINDING condition."""
    assert n7.s_required(n7.EPS_OBS, n7.EPS_I) < 0.0
    assert abs(n7.s_required(n7.EPS_OBS, n7.EPS_I) - math.log(0.011 / 1.0)) < 1e-15
    for eps_i in [0.5, 1.0, 2.0, 10.0]:
        assert n7.s_required(n7.EPS_OBS, eps_i) < 0.0
    # and it is only non-negative if the initial curvature is ALREADY at or
    # below the observed one, i.e. if there is no flatness problem to solve
    assert n7.s_required(n7.EPS_OBS, 1e-3) > 0.0


def test_horizon_condition_is_S_negative_and_the_radius_shrinks():
    """THE SIGN REGRESSION.  The requirement is `r_f < r_i`: the comoving
    Hubble radius must SHRINK, so `S < 0`.  A draft had `S > 0`, which does not
    fail loudly because the matter era's `S = +80` then looks like a fix."""
    for s in [-1e-9, -0.5, -4.50986, -80.0]:
        assert n7.radius_amplification(s) < 1.0
        _flat, horz = n7.classify(s, n7.EPS_OBS, n7.EPS_I)
        assert horz is (s < 0.0)
    for s in [0.0, 0.5, 80.0, 800.0]:
        assert n7.radius_amplification(s) >= 1.0
        _flat, horz = n7.classify(s, n7.EPS_OBS, n7.EPS_I)
        assert horz is (s < 0.0)
    # strictly: S = 0 is NOT a resolution
    assert n7.radius_amplification(0.0) == 1.0
    assert n7.classify(0.0, n7.EPS_OBS, n7.EPS_I)[1] is False


def test_a_decelerating_era_makes_the_horizon_problem_worse():
    """Matter alone gives S = +80: it GROWS the comoving Hubble radius."""
    s_matter = n7.s_of_path([(0.0, n7.N_MATTER)])
    assert s_matter == 80.0
    assert s_matter > 0.0
    assert n7.radius_amplification(s_matter) > 1e17
    assert n7.classify(s_matter, n7.EPS_OBS, n7.EPS_I) == (False, False)


def test_flatness_implies_horizon_wherever_eps_obs_is_below_eps_i():
    """The linking statement: S < S_req < 0 <= S is false, so flatness suffices.
    Scanned densely rather than asserted at one point."""
    for eps_i in [0.5, 1.0, 2.0, 10.0]:
        s_req = n7.s_required(n7.EPS_OBS, eps_i)
        assert s_req < 0.0
        for k in range(0, 400):
            s = n7.s_total(n7.W_INFL, 0.05 * k, 0.0, n7.N_MATTER)
            flat, horz = n7.classify(s, n7.EPS_OBS, eps_i)
            if flat:
                assert horz, "flatness held at S=%.4f but horizon failed" % s
                assert s < 0.0


def test_the_conditions_are_nested_not_identical():
    """A horizon-only band exists (flatness is stronger); a flat-only band
    cannot.  If these ever coincide, the linking claim has become vacuous."""
    rows = []
    for k in range(0, 200):
        n_infl = 0.25 * k
        s = n7.s_total(n7.W_INFL, n_infl, 0.0, n7.N_MATTER)
        rows.append((n_infl,) + n7.classify(s, n7.EPS_OBS, n7.EPS_I))
    only_flat = [r for r in rows if r[1] and not r[2]]
    only_horz = [r for r in rows if r[2] and not r[1]]
    assert len(only_horz) > 0
    assert len(only_flat) == 0


def test_the_threshold_is_strict_so_the_boundary_is_inadmissible():
    """`S < S_req`, not `S <= S_req`."""
    s_req = n7.s_required(n7.EPS_OBS, n7.EPS_I)
    assert n7.classify(s_req, n7.EPS_OBS, n7.EPS_I)[0] is False
    assert n7.classify(n7.s_required(n7.EPS_OBS, n7.EPS_I) - 1e-9,
                       n7.EPS_OBS, n7.EPS_I)[0] is True
    assert n7.classify(n7.s_required(n7.EPS_OBS, n7.EPS_I) + 1e-9,
                       n7.EPS_OBS, n7.EPS_I)[0] is False


def test_threshold_length_lands_exactly_on_eps_obs():
    n_star = n7.n_infl_needed(n7.EPS_OBS, n7.EPS_I, n7.N_MATTER, n7.W_INFL)
    assert abs(n_star - 42.254930) < 1e-5
    s = n7.s_total(n7.W_INFL, n_star, 0.0, n7.N_MATTER)
    eps_f = n7.EPS_I * n7.eps_amplification(s)
    assert abs(eps_f - n7.EPS_OBS) / n7.EPS_OBS < 1e-9
    # and just past the threshold it is admissible
    s2 = n7.s_total(n7.W_INFL, n_star + 1.0, 0.0, n7.N_MATTER)
    assert n7.classify(s2, n7.EPS_OBS, n7.EPS_I) == (True, True)


def test_threshold_length_matches_a_brute_force_search():
    """Solve `S < S_req` by scanning instead of by the closed form."""
    for eps_i in [0.5, 0.9, 1.0, 2.0, 10.0]:
        want = n7.n_infl_needed(n7.EPS_OBS, eps_i, n7.N_MATTER, n7.W_INFL)
        lo, hi = 0.0, 200.0
        # admissible side
        assert n7.classify(n7.s_total(n7.W_INFL, hi, 0.0, n7.N_MATTER),
                           n7.EPS_OBS, eps_i)[0] is True
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if n7.classify(n7.s_total(n7.W_INFL, mid, 0.0, n7.N_MATTER),
                           n7.EPS_OBS, eps_i)[0]:
                hi = mid
            else:
                lo = mid
        assert abs(hi - want) < 1e-6


def test_no_finite_length_exists_without_stiffness():
    """If `1 + 3w >= 0` the era cannot shrink S at all, so flatness is
    unreachable -- not 'easy', unreachable."""
    for w_infl in [0.0, -1.0 / 3.0, 0.5, 1.0]:
        assert n7.n_infl_needed(n7.EPS_OBS, n7.EPS_I, n7.N_MATTER, w_infl) == math.inf
    # a barely accelerating era needs strictly MORE length than exact de Sitter
    assert n7.n_infl_needed(n7.EPS_OBS, n7.EPS_I, n7.N_MATTER, -0.9) > \
        n7.n_infl_needed(n7.EPS_OBS, n7.EPS_I, n7.N_MATTER, -1.0)


def test_required_length_grows_with_eps_i():
    """A larger assumed initial curvature demands more inflation, never less."""
    prev = -math.inf
    for eps_i in [0.5, 0.9, 1.0, 2.0, 10.0, 100.0]:
        n_need = n7.n_infl_needed(n7.EPS_OBS, eps_i, n7.N_MATTER, n7.W_INFL)
        assert math.isfinite(n_need)
        assert n_need > prev
        prev = n_need


def test_the_matter_length_enters_the_threshold_through_S():
    """More post-inflation matter means more e-folds required: the matter era
    is a cost, not a subsidy."""
    base = n7.n_infl_needed(n7.EPS_OBS, n7.EPS_I, 80.0, n7.W_INFL)
    assert n7.n_infl_needed(n7.EPS_OBS, n7.EPS_I, 0.0, n7.W_INFL) == \
        n7.s_required(n7.EPS_OBS, n7.EPS_I) / -2.0
    assert n7.n_infl_needed(n7.EPS_OBS, n7.EPS_I, 200.0, n7.W_INFL) > base


# ---------------------------------------------------------------------------
# w = -1/3: a boundary of the law, emphatically not a solution
# ---------------------------------------------------------------------------
def test_w_minus_one_third_is_invariant_but_not_admissible():
    """Zero stiffness density means zero change in eps AND in r, at any length.
    Read carelessly that looks like a free beginning; it is not an admissible
    history, and the matter era that follows ruins it."""
    for n in [1.0, 50.0, 1e6]:
        assert n7.eps_amplification(n7.S_of(-1.0 / 3.0, n)) == 1.0
        assert n7.radius_amplification(n7.S_of(-1.0 / 3.0, n)) == 1.0
    s_mixed = n7.s_total(-1.0 / 3.0, 60.0, 0.0, n7.N_MATTER)
    assert s_mixed == 80.0
    assert n7.classify(s_mixed, n7.EPS_OBS, n7.EPS_I) == (False, False)


def test_only_stiffness_negative_eras_help():
    """The sign test is about `w < -1/3`, not about inflation as a word."""
    for eras, want in [([(-1.0, 10.0)], -20.0), ([(-0.5, 10.0)], -5.0),
                       ([(-0.2, 10.0)], 4.0), ([(0.0, 10.0)], 10.0),
                       ([(1.0, 10.0)], 40.0)]:
        assert abs(n7.s_of_path(eras) - want) < 1e-12
    assert n7.s_of_path([(-1.0, 10.0)]) < 0.0
    assert n7.s_of_path([(-1.0 / 3.0, 10.0)]) == 0.0
    assert n7.s_of_path([(0.0, 10.0)]) > 0.0


# ---------------------------------------------------------------------------
# the filter does not constrain eps_i
# ---------------------------------------------------------------------------
def test_eps_i_is_free_and_only_sets_the_required_length():
    """THE SCOPE LIMIT AS A TEST.  Every `eps_i` yields a finite required
    length.  Nothing in N7 excludes a value of `eps_i`, because N7 does not
    derive one.  A filter that cannot exclude anything cannot explain the
    initial condition."""
    for eps_i in [0.5, 0.9, 1.0, 2.0, 10.0, 1e6]:
        n_need = n7.n_infl_needed(n7.EPS_OBS, eps_i, n7.N_MATTER, n7.W_INFL)
        assert math.isfinite(n_need)
        assert n_need > 0.0
    # the free input is unbounded above: an arbitrarily huge initial curvature
    # is always 'repairable' by a long enough acceleration
    assert n7.n_infl_needed(n7.EPS_OBS, 1e12, n7.N_MATTER, n7.W_INFL) < math.inf


def test_a_filter_that_never_excludes_cannot_claim_to_derive():
    """Every tested eps_i is reachable by SOME inflation length, so admissibility
    is vacuous as a selection principle.  This is the honest statement of what
    the node achieves."""
    for eps_i in [0.1, 0.5, 1.0, 2.0, 10.0, 100.0]:
        n_need = n7.n_infl_needed(n7.EPS_OBS, eps_i, n7.N_MATTER, n7.W_INFL)
        assert n7.classify(n7.s_total(n7.W_INFL, n_need + 5.0, 0.0, n7.N_MATTER),
                           n7.EPS_OBS, eps_i) == (True, True)


# ---------------------------------------------------------------------------
# the measurement floor on the curvature criterion  (n7k)
# ---------------------------------------------------------------------------
def test_required_length_is_affine_in_log_eps_obs():
    """dN/dln(eps_obs) = 1/(1+3w) exactly, so the inverse below is exact too."""
    slope = 1.0 / n7.stiffness(n7.W_INFL)
    assert abs(slope - (-0.5)) < 1e-15
    base = n7.n_infl_needed(1e-2, n7.EPS_I, n7.N_MATTER, n7.W_INFL)
    for factor in [0.1, 10.0, 1e6]:
        got = n7.n_infl_needed(1e-2 * factor, n7.EPS_I, n7.N_MATTER, n7.W_INFL)
        want = base + slope * math.log(factor)
        assert abs(got - want) < 1e-9
    # a TIGHTER curvature bound demands a LONGER history
    assert (n7.n_infl_needed(1e-4, n7.EPS_I, n7.N_MATTER, n7.W_INFL)
            > n7.n_infl_needed(1e-2, n7.EPS_I, n7.N_MATTER, n7.W_INFL))


def test_the_affine_law_and_the_inverse_agree():
    """eps_obs_needed_for inverts n_infl_needed: round-tripping is exact."""
    for n_target in [42.0, 45.0, 45.5537, 46.7]:
        eps = n7.eps_obs_needed_for(n_target, n7.EPS_I, n7.N_MATTER, n7.W_INFL)
        back = n7.n_infl_needed(eps, n7.EPS_I, n7.N_MATTER, n7.W_INFL)
        assert abs(back - n_target) < 1e-9


def test_curvature_saturates_below_the_sixty_efold_convention():
    """THE LIMIT AS A TEST.  At the 1.5e-5 cosmic-variance level the curvature
    criterion reaches 45.55 e-folds, so curvature alone cannot certify the
    conventional ~60 -- it would need eps_obs below 1e-17, over ten decades
    under the floor.  The 45.55 figure is an UNREACHABLE ASYMPTOTE: the sources
    judge that floor unattainable even by Stage IV and expect ~1e-3, i.e. 43.45
    e-folds, so the realistic cap is lower still and the conclusion is stronger
    for being so."""
    sat = n7.n_infl_needed(n7.SIGMA_OMEGA_K_COSMIC_VARIANCE, n7.EPS_I,
                           n7.N_MATTER, n7.W_INFL)
    assert abs(sat - 45.5536) < 1e-3
    assert sat < n7.N_EFOLDS_CONVENTION
    cap = n7.n_infl_needed(n7.EPS_OBS_FORESEEABLE, n7.EPS_I,
                           n7.N_MATTER, n7.W_INFL)
    assert abs(cap - 43.4539) < 1e-3
    assert cap < sat  # the attainable bound is looser than the asymptote
    eps_60 = n7.eps_obs_needed_for(n7.N_EFOLDS_CONVENTION, n7.EPS_I,
                                   n7.N_MATTER, n7.W_INFL)
    assert 1e-19 < eps_60 < 1e-17
    decades = (math.log10(n7.SIGMA_OMEGA_K_COSMIC_VARIANCE)
               - math.log10(eps_60))
    assert decades > 10.0


def test_saturation_is_a_precision_limit_not_a_mathematical_one():
    """The formal requirement diverges as eps_obs -> 0; only the achievable
    measurement saturates.  Conflating the two would be the overclaim."""
    # the requirement grows without bound as the bound shrinks, but stays
    # finite for every non-zero eps_obs
    prev = 0.0
    for e in [1e-4, 1e-6, 1e-8, 1e-12]:
        n_need = n7.n_infl_needed(e, n7.EPS_I, n7.N_MATTER, n7.W_INFL)
        assert math.isfinite(n_need)
        assert n_need > prev
        prev = n_need
    # exactly zero curvature is not a limit of the formula: log(0) has no value
    with pytest.raises(ValueError):
        n7.n_infl_needed(0.0, n7.EPS_I, n7.N_MATTER, n7.W_INFL)


def test_measurement_floor_shifts_with_eps_i_by_a_pure_offset():
    """eps_i moves the requirement by log(eps_i)/|1+3w| and does nothing else;
    only eps_obs sets where the geometric limit sits."""
    diff = (n7.n_infl_needed(n7.SIGMA_OMEGA_K_COSMIC_VARIANCE, 1.0,
                             n7.N_MATTER, n7.W_INFL)
            - n7.n_infl_needed(n7.SIGMA_OMEGA_K_COSMIC_VARIANCE, 10.0,
                               n7.N_MATTER, n7.W_INFL))
    assert abs(diff + math.log(10.0) / 2.0) < 1e-12


def test_no_finite_eps_obs_is_needed_when_there_is_no_stiffness():
    assert n7.eps_obs_needed_for(60.0, n7.EPS_I, n7.N_MATTER, -1.0 / 3.0) == math.inf
    assert n7.eps_obs_needed_for(60.0, n7.EPS_I, n7.N_MATTER, 0.0) == math.inf


# ---------------------------------------------------------------------------
# the filter needs a model to test  (n7l)
# ---------------------------------------------------------------------------
def test_curvature_verdict_is_admissible_inside_and_falsified_outside():
    """A model that predicts its own curvature is decidable.  The boundary is
    inclusive, matching the strictness convention used elsewhere: at exactly
    eps_obs the window `S < S_req` is NOT satisfied, yet |Omega_k| == eps_obs is
    not an excess, so the verdict is 'admissible' here and the strictness lives
    in the S-boundary test instead."""
    assert n7.curvature_verdict(0.0, 1e-2) == "admissible"
    assert n7.curvature_verdict(5e-3, 1e-2) == "admissible"
    assert n7.curvature_verdict(1e-2, 1e-2) == "admissible"
    assert n7.curvature_verdict(1.01e-2, 1e-2) == "FALSIFIED"
    assert n7.curvature_verdict(1.0, 1e-2) == "FALSIFIED"


def test_curvature_verdict_is_symmetric_in_the_sign():
    """It tests |Omega_k| only.  The sign statement that actually discriminates
    eternal-inflation variants is deliberately not encoded here."""
    for om in [2e-4, 5e-3]:
        assert n7.curvature_verdict(om, 5e-3) == n7.curvature_verdict(-om, 5e-3)


def test_the_eternal_inflation_threshold_is_not_yet_decisive():
    """Kleban & Schillo (2012) need |Omega_k| resolved to 1e-4.  The best bound
    verified from a primary source here is 5e-3, exactly 50x looser, so the test
    cannot yet run."""
    assert abs(n7.EPS_OBS_QUOTED_2016 / n7.OMEGA_K_ETERNAL_INFLATION_THRESHOLD
               - 50.0) < 1.0
    # a model predicting 2e-4 escapes the current bound ...
    assert n7.curvature_verdict(2e-4, n7.EPS_OBS_QUOTED_2016) == "admissible"
    # ... but would be excluded at the threshold
    assert n7.curvature_verdict(2e-4, n7.OMEGA_K_ETERNAL_INFLATION_THRESHOLD) == "FALSIFIED"
    # a prediction BELOW the threshold survives even the ideal measurement
    assert n7.curvature_verdict(5e-5, n7.OMEGA_K_ETERNAL_INFLATION_THRESHOLD) == "admissible"
    # the discriminating probes are exactly those in the decade above 1e-4
    assert n7.curvature_verdict(2e-4, n7.EPS_OBS_QUOTED_2016) == "admissible"
    assert n7.curvature_verdict(2e-4, 1e-4) == "FALSIFIED"


def test_the_filter_excludes_nothing_without_a_model_prediction():
    """THE VACUITY CONDITION AS A TEST.  N7 supplies no Omega_k and derives none,
    so the model filter is inert unless a caller passes a prediction.  This is
    why n7l is a wrapper and not evidence about inflation model space."""
    # every eps_i remains admissible for a sufficiently long history
    for eps_i in [0.1, 1.0, 10.0]:
        n_need = n7.n_infl_needed(n7.EPS_OBS, eps_i, n7.N_MATTER, n7.W_INFL)
        assert n7.classify(n7.s_total(n7.W_INFL, n_need + 5.0, 0.0, n7.N_MATTER),
                           n7.EPS_OBS, eps_i) == (True, True)
    # and the observational bounds used by n7l do not restrict eps_i at all
    for bound in [n7.EPS_OBS_PLANCK_2018, n7.EPS_OBS_QUOTED_2016,
                  n7.EPS_OBS_FORESEEABLE,
                  n7.OMEGA_K_ETERNAL_INFLATION_THRESHOLD]:
        assert math.isfinite(
            n7.n_infl_needed(bound, 1e9, n7.N_MATTER, n7.W_INFL))


# ---------------------------------------------------------------------------
# the artifact
# ---------------------------------------------------------------------------
def test_main_returns_zero_and_writes_the_artifact():
    """Also pins the convention: importing the module must have no side
    effects, and `main()` must be re-runnable (GATES is reset, not appended
    to)."""
    saved = list(n7.GATES)
    n7.GATES.clear()
    try:
        rc = n7.main()
        n_gates = len(n7.GATES)
        all_ok = all(ok for _n, ok, _d in n7.GATES)
    finally:
        n7.GATES[:] = saved
    assert rc == 0
    assert n_gates == 12
    assert all_ok
    assert os.path.exists(DATA)


def test_all_gates_pass():
    rep = _report()
    assert all(g["pass"] for g in rep["gates"].values())
    assert len(rep["gates"]) == 12
    for name in ["n7a", "n7b", "n7c", "n7d", "n7e",
                 "n7f", "n7g", "n7h", "n7i", "n7j", "n7k", "n7l"]:
        # gate keys carry the id as a PREFIX followed by the description
        assert any(k.startswith(name + " ") for k in rep["gates"]), \
            "missing gate %s" % name


def test_artifact_records_the_headline_numbers():
    rep = _report()
    assert rep["node"] == "N7"
    assert rep["generated_by"] == "origin_consistency_window_n7.py"
    assert abs(rep["inputs"]["eps_obs"] - 0.011) < 1e-15
    assert rep["inputs"]["eps_i"] == 1.0
    assert rep["inputs"]["w_infl"] == -1.0
    assert abs(rep["s_required"] - math.log(0.011)) < 1e-12
    assert abs(rep["n_infl_needed"] - 42.254930) < 1e-5
    assert "INITIAL CONDITIONS NOT DERIVED" in rep["overall"]


def test_artifact_window_rows_are_self_consistent():
    rep = _report()
    rows = rep["window"]
    assert len(rows) >= 5
    # S decreases with inflation length (stiffness(de Sitter) = -2)
    assert all(rows[i]["S"] > rows[i + 1]["S"] for i in range(len(rows) - 1))
    for r in rows:
        want_flat, want_horz = n7.classify(r["S"], n7.EPS_OBS, n7.EPS_I)
        assert r["flat"] is want_flat
        assert r["horizon"] is want_horz
        # eps_f = eps_i e^S
        assert abs(r["eps_f"] - n7.EPS_I * n7.eps_amplification(r["S"])) < 1e-12
        if r["flat"]:
            assert r["horizon"] is True


def test_artifact_eps_i_freedom_rows_are_all_finite():
    rep = _report()
    rows = rep["eps_i_freedom"]
    assert len(rows) >= 5
    for r in rows:
        assert math.isfinite(r["N_infl_needed"])


def test_artifact_measurement_floor_block_is_self_consistent():
    rep = _report()
    mf = rep["measurement_floor"]
    assert abs(mf["slope_dN_dln_eps_obs"] + 0.5) < 1e-15
    for r in mf["rows"]:
        assert math.isfinite(r["N_infl_needed"])
        # recomputed from the affine law, so a drifting ladder cannot pass
        # silently -- this replaces an earlier magic bound that broke when a
        # looser rung was added
        assert abs(r["N_infl_needed"]
                   - n7.n_infl_needed(r["eps_obs"], n7.EPS_I, n7.N_MATTER,
                                      n7.W_INFL)) < 1e-12
        # every rung sits far above the ~30 e-folds observationally required and
        # far below the ~60 e-fold convention
        assert 40.0 < r["N_infl_needed"] < n7.N_EFOLDS_CONVENTION
    # a tighter measurement demands a longer history, monotonically
    epss = [r["eps_obs"] for r in mf["rows"]]
    ns = [r["N_infl_needed"] for r in mf["rows"]]
    assert epss == sorted(epss, reverse=True)
    assert ns == sorted(ns)
    assert abs(mf["asymptotic_N_infl"]
               - n7.n_infl_needed(n7.SIGMA_OMEGA_K_COSMIC_VARIANCE, n7.EPS_I,
                                  n7.N_MATTER, n7.W_INFL)) < 1e-9
    assert mf["asymptotic_N_infl"] < n7.N_EFOLDS_CONVENTION
    assert mf["decades_below_cosmic_variance_level"] > 10.0
    assert mf["eps_obs_for_60_efolds"] < mf["sigma_omega_k_cosmic_variance"]
    # the attainable cap is strictly below the unreachable asymptote
    assert mf["realistic_cap_N_infl"] < mf["asymptotic_N_infl"]


def test_artifact_model_filter_block_is_self_consistent():
    rep = _report()
    mf = rep["model_filter"]
    assert len(mf["rows"]) >= 5
    for r in mf["rows"]:
        assert r["verdict_at_current_bound"] in ("admissible", "FALSIFIED")
        assert r["verdict_at_1e-4"] in ("admissible", "FALSIFIED")
    # tightening the bound can only ever exclude more models
    assert mf["excluded_at_1e_4"] >= mf["excluded_at_current_bound"]
    assert mf["excluded_at_current_bound"] >= 1
    assert mf["ratio_bound_over_threshold"] > 1.0
    assert mf["omega_k_eternal_inflation_threshold"] == 1e-4
    # the unverified ACT DR6 value is recorded but must drive no verdict
    assert mf["eps_obs_current_bound"] == n7.EPS_OBS_QUOTED_2016
    assert mf["eps_obs_current_bound"] != n7.EPS_OBS_ACT_DR6_UNVERIFIED


# ---------------------------------------------------------------------------
# THE LIMITS, pinned as tests
# ---------------------------------------------------------------------------
def test_artifact_says_eps_i_is_an_input_not_a_derivation():
    rep = _report()
    txt = rep["scope"]["epsilon_i status"]
    assert "INPUT, NOT derived" in txt
    assert "Nothing here fixes" in txt
    assert "separate open problem" in txt


def test_artifact_says_the_beginning_is_not_addressed():
    rep = _report()
    txt = rep["scope"]["cause / beginning"]
    assert "NOT ADDRESSED" in txt
    assert "does not produce initial conditions" in txt
    assert "does not explain why there is a history" in txt
    what = rep["scope"]["what this is"]
    assert "FILTER" in what
    assert "not a mechanism" in what


def test_artifact_records_the_flatness_implies_horizon_link():
    rep = _report()
    txt = rep["scope"]["linking statement"]
    assert "IMPLIES horizon" in txt
    assert "one" in txt and "inequality" in txt
    assert "binding one" in txt


def test_artifact_records_the_matter_era_sign():
    """The matter era is an aggravation, not a subsidy."""
    rep = _report()
    txt = rep["scope"]["matter era sign"]
    assert "+80" in txt
    assert "NOT free" in txt
    assert "worsen" in txt


def test_artifact_quarantines_the_leading_laws_as_asymptotic():
    rep = _report()
    txt = rep["scope"]["leading laws are asymptotic"]
    assert "EARLY-time limit" in txt
    assert "1/(1 - sigma/X)" in txt
    assert "(1 - sigma/X)^(-1/2)" in txt
    assert "tests nothing but arithmetic" in txt


def test_artifact_quarantines_w_minus_one_third():
    rep = _report()
    txt = rep["scope"]["n7i caveat"]
    assert "DENSITY vanishes" in txt
    assert "boundary of the scaling laws" in txt
    assert "not an admissible history" in txt


def test_artifact_records_the_de_sitter_idealisation():
    rep = _report()
    txt = rep["scope"]["de Sitter caveat"]
    assert "w_infl = -1 is exact" in txt
    assert "quasi-de Sitter" in txt
    assert "NOT the sign test" in txt
    assert "w < -1/3" in txt


def test_artifact_records_that_the_curvature_law_is_exact():
    rep = _report()
    txt = rep["scope"]["closed-form curvature law"]
    assert "EXACT" in txt
    assert "-k = -sigma|k|" in txt


def test_artifact_scopes_the_claims_to_gr_and_flrw():
    """The node is conditional on an assumed FLRW + GR history; the artifact
    must not read as a statement about GR or FLRW themselves."""
    rep = _report()
    blob = " ".join(rep["scope"].values()).lower()
    assert "flrw" in blob or "assumed history" in blob
    assert "initial conditions" in blob


def test_artifact_credits_the_measurement_floor_to_leonard():
    """The 1.5e-5 level is Leonard, Bull & Allison's, not this node's -- and it
    is a NOISE level, not the floor they adopt, so the artifact must not let the
    two be conflated."""
    rep = _report()
    txt = rep["scope"]["n7k provenance"]
    assert "Leonard, Bull & Allison" in txt
    assert "PRD 94 023502" in txt
    assert "1604.01410" in txt
    assert "arithmetic, not novel" in txt
    assert "quantifies, rather than discovers" in txt
    # the conflation guard
    assert "NOISE level" in txt
    asym = rep["scope"]["n7k floor is an ASYMPTOTE"]
    assert "unreachable" in asym.lower()
    assert "1e-3" in asym
    # the qualifications the same paper supplies, so the negative result is
    # not overstated in the other direction either
    assert "CONSERVATIVE" in asym
    assert "NOT unreachable in principle" in asym


def test_artifact_credits_the_curvature_test_to_kleban_schillo():
    """Falsifying eternal inflation by measured curvature is Kleban & Schillo's
    claim; N7 contributes the wrapper only.  This attribution must stay in the
    artifact so the node cannot later be cited as the discovery.  Pinned to the
    CORRECTED citation: an earlier pass credited this to Freivogel et al. with
    arXiv:1112.0332, both of which are a different (Born-Infeld) paper."""
    rep = _report()
    txt = rep["scope"]["n7l provenance"]
    assert "Kleban & Schillo" in txt
    assert "Freivogel" not in txt
    assert "1112.0332" not in txt
    assert "1202.5037" not in txt.split("NOT this node's")[0]  # cited after it
    assert "NOT this node's" in txt
    assert "excludes slow-roll eternal inflation" in txt
    assert "what this node contributes" in txt.lower()


def test_every_gated_observational_input_has_a_verified_source():
    """PROVENANCE GATE.  Every constant that drives a verdict must be traceable
    to a primary source that was actually retrieved.  Each of the four
    gated values below was read off arxiv.org/abs/<id> or the arXiv HTML full
    text, verbatim:

    arXiv:1604.01410 (Leonard, Bull & Allison, PRD 94 023502):
      abstract, "Current constraints ... |Omega_K| \\lesssim 5 \\times 10^{-3}
      (95% CL)"
      abstract, "the curvature floor is unreachable - by an order of magnitude -
      even with Stage IV experiments"
      full text: "an irreducible cosmic variance \\"noise\\" level,
      sigma(Omega_K) \\approx 1.5 \\times 10^{-5}"  [their ref 10 =
      Waterhouse & Zibin, arXiv:0804.1771]
      full text: "We adopt this more stringent value as the \\"curvature floor\\""
      -- i.e. the ADOPTED floor is 1e-4, not 1.5e-5
      full text: "10^{-3} (95% CL) is the most likely achievable constraint on
      Omega_K for the foreseeable future"
    arXiv:1202.5037 (Kleban & Schillo, JCAP 06 029):
      abstract, "a measurement of |Omega_k| > 10^{-4} would rule out slow-roll
      eternal inflation ... while a measurement of Omega_k < -10^{-4} ...
      rules out false-vacuum eternal inflation as well"
    arXiv:1807.06209v4 (Planck Collaboration, A&A 641 A6 2020), Sect. 7.3:
      base-LambdaCDM parameter table, Omega_k row,
      TT,TE,EE+lowE+lensing+BAO: Omega_K = -0.011^{+0.013}_{-0.012}  (95%)
        -> 0.011 is the MAGNITUDE OF THE 95% CENTRAL VALUE, not a bound
      the same row implies a 95% interval Omega_k in [-0.023, +0.002]
        -> |Omega_k| < 0.023 is the genuine upper limit
      eq. (45b): Omega_K = 0.0007 +/- 0.0019  (68%, TT,TE,EE+lowE+lensing+BAO)
      text: "spatially flat to a 1 sigma accuracy of 0.2%"

    If any of these values is changed, this test is where the new source goes.
    """
    import re as _re

    src = io.open(n7.__file__, encoding="utf-8").read()

    # (constant name, expected value, provenance that must be in the file)
    expect = [
        ("SIGMA_OMEGA_K_COSMIC_VARIANCE", 1.5e-5, "1604.01410"),
        ("OMEGA_K_ETERNAL_INFLATION_THRESHOLD", 1e-4, "1202.5037"),
        ("EPS_OBS_QUOTED_2016", 0.005, "1604.01410"),
        ("EPS_OBS_FORESEEABLE", 1e-3, "1604.01410"),
        ("EPS_OBS_PLANCK_2018", 0.011, "1807.06209"),
        ("EPS_OBS_PLANCK_2018_UPPER", 0.023, "1807.06209"),
        ("EPS_OBS_PLANCK_2018_68CL", 0.0007, "1807.06209"),
        ("EPS_OBS_PLANCK_2018_68CL_ERR", 0.0019, "1807.06209"),
    ]
    for name, val, prov in expect:
        m = _re.search(r"^%s\s*=\s*([0-9.e+-]+)" % _re.escape(name), src, _re.M)
        assert m, "constant %s not found" % name
        assert abs(float(m.group(1)) - val) <= 1e-12 * max(abs(val), 1e-30), \
            "%s changed to %s; update the primary source first" % (name, m.group(1))
        # the value must appear with its arXiv id somewhere in the file
        assert prov in src, "%s must cite arXiv:%s" % (name, prov)


def test_planck_2018_rung_is_labelled_a_central_value_not_a_bound():
    """REGRESSION GUARD for a real mislabelling found by auditing arXiv:1807.06209.

    0.011 was described as '|Omega_k| at recombination (Planck 2018 ...)'.
    It is in fact the magnitude of the 95% CL CENTRAL VALUE of Omega_k, from
    the table row Omega_K = -0.011^{+0.013}_{-0.012}.  Since eps_obs in this
    window is a PRECISION THRESHOLD, calling a central value a bound is a
    category error, so the label must not regress.
    """
    rep = _report()
    src = io.open(n7.__file__, encoding="utf-8").read()

    # the mislabelled phrase must be gone from live code and comments
    assert "at recombination (Planck 2018" not in src, \
        "the 'at recombination' mislabel must not come back"

    # the artifact must expose the central value under a name that denies it
    # is a bound, and the genuine upper limit alongside it
    fl = rep["measurement_floor"]
    assert fl["eps_obs_planck_2018_central_95_not_a_bound"] == 0.011
    assert fl["eps_obs_planck_2018_upper_95"] == 0.023

    # and the ladder row itself must say so on its face
    labels = [r["label"] for r in fl["rows"]]
    assert any("NOT a bound" in lbl for lbl in labels), labels

    # the correction must be recorded in the scope block, not silently applied
    assert any("MISLABELLED" in k for k in rep["scope"]), \
        "the Planck mislabelling and its correction must stay on the record"

    # the unverified value must be named as such, and must appear ONLY in its
    # own definition and in the artifact payload -- never in a comparison that
    # could decide a verdict
    lines = [l for l in src.splitlines() if "EPS_OBS_ACT_DR6_UNVERIFIED" in l]
    assert len(lines) == 2, "unexpected uses of the unverified input: %r" % lines
    assert lines[0].startswith("EPS_OBS_ACT_DR6_UNVERIFIED")
    for l in lines:
        for gate_fn in ("curvature_verdict(", "n_infl_needed(",
                        "eps_obs_needed_for(", "gate("):
            assert gate_fn not in l, "unverified input reaches %s" % gate_fn
    assert "EPS_OBS_QUOTED_2016" in src
    # the adopted floor is 1e-4; conflating it with the noise level is the error
    # this test exists to prevent
    assert "curvature floor" in src


def test_artifact_records_the_unverified_observational_input():
    """Numbers that could not be traced to a primary source are recorded as
    UNVERIFIED and excluded from every gate.  The attributed 5e-3 is what the
    verdicts actually rest on."""
    rep = _report()
    txt = rep["scope"]["current bound is borrowed and dated"]
    assert "5e-3" in txt
    assert "UNVERIFIED" in txt
    assert "drives no verdict" in txt
    mf = rep["measurement_floor"]
    assert "eps_obs_act_dr6_unverified_unused" in mf
    assert rep["model_filter"]["eps_obs_current_bound"] == 0.005


def test_artifact_states_the_vacuity_condition():
    """Without a model-supplied Omega_k the filter is empty.  Pinned so the
    non-claim cannot be dropped silently."""
    rep = _report()
    txt = rep["scope"]["n7l vacuity condition"]
    assert "EMPTY until a model predicts" in txt
    assert "n7j" in txt
    assert "Do not read n7l as evidence" in txt


def test_artifact_does_not_claim_a_sign_test():
    """The sign discrimination between eternal-inflation variants is NOT
    implemented; the artifact must say so rather than implying coverage."""
    rep = _report()
    txt = rep["scope"]["n7l sign is NOT encoded"]
    assert "tests |Omega_k| only" in txt
    assert "deliberately not implemented" in txt
