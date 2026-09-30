"""
Locks the origin/zero findings for the C0 scale.

Each test re-derives a claim made in experiments/c0_zero_locus.py so that a
future edit to POSITIONS, ALPHA, or repulsion_loss cannot quietly restore the
"0/0 has a removable value" story in docs/IF_C0_IS_0_OVER_0.md.
"""

import json
import math
import os

import mpmath as mp
import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys

sys.path.insert(0, os.path.join(ROOT, "Universals"))

from hamiltonian_flow import (  # noqa: E402
    ALPHA,
    POSITIONS,
    R_MAX_GRID,
    hyperbolic_dist,
    repulsion_loss,
)

DATA = os.path.join(ROOT, "experiments", "data", "c0_zero_locus_data.json")
Q0 = POSITIONS["Origin"]
CONTEXT = ["Tech", "Silicon"]
N = len(POSITIONS)


def _load(name):
    with open(os.path.join(ROOT, "experiments", "data", name), encoding="utf-8") as fh:
        return json.load(fh)


def test_recorded_gates_all_pass():
    with open(DATA, encoding="utf-8") as fh:
        rec = json.load(fh)
    failed = [k for k, v in rec["gates"].items() if not v["pass"]]
    assert not failed, "gates no longer pass: %s" % failed


def test_origin_is_not_a_zero():
    assert repulsion_loss(Q0, []) > 1e-12


def test_c0_is_zero_on_the_zero_locus():
    # Points comfortably inside the measured zero region. The inner boundary
    # r*(theta) is not circular, so these were checked against r*(theta)
    # rather than picked by radius alone.
    for q in (np.array([0.95, 0.0]), np.array([0.6364, 0.6364]),
              np.array([0.0, -0.97]), np.array([-0.99, 0.05])):
        assert repulsion_loss(q, []) == 0.0


def test_zero_locus_inner_boundary_is_not_circular():
    rec = json.load(open(DATA, encoding="utf-8"))
    g1 = rec["gates"]["G1 zero set exists, C0 flat on it"]
    lo = g1["r_star_min"]
    hi = g1["r_star_max"]
    assert lo > 0.0
    assert lo <= R_MAX_GRID <= hi or hi <= R_MAX_GRID
    assert hi - lo > 0.01, "inner boundary should be measurably non-circular"


def test_points_below_the_inner_boundary_are_not_zeros():
    """Guards the earlier mistake of reading the zero set as a full annulus."""
    assert repulsion_loss(np.array([0.90, 0.0]), []) > 0.0


def test_zero_over_zero_limit_is_path_dependent():
    """The one-step limit must keep depending on which node survives.

    This is the load-bearing refutation: if this ever becomes unique, the
    'the limit exists' claim in IF_C0_IS_0_OVER_0.md sec.2 could revive.
    """
    finals = {}
    for k in POSITIONS:
        ctx = [n for n in POSITIONS if n != k]
        finals[k] = repulsion_loss(Q0, ctx) / (N - len(ctx))
    # each limit is exactly the surviving node's own term
    for k, v in finals.items():
        term = max(0.0, ALPHA - hyperbolic_dist(Q0, POSITIONS[k])) ** 2
        assert abs(v - term) < 1e-9
    assert len({round(v, 9) for v in finals.values()}) > 1


def test_documented_c0_is_not_the_documented_average():
    raw = repulsion_loss(Q0, CONTEXT)
    per_node = raw / (N - len(CONTEXT))
    assert abs(raw - 24.434791603891032) < 1e-9
    assert abs(raw - per_node) > 1.0, "C0 must stay distinguishable from V/(N-|ctx|)"


def test_context_choice_matters():
    values = {round(repulsion_loss(Q0, list(c)), 6)
              for r in range(N + 1)
              for c in __import__("itertools").combinations(POSITIONS, r)}
    assert len(values) > 1


# --------------------------------------------------------------- G6, corrected
# The first version of G6 claimed the zeta 0/0 "carries no information about
# which side of the critical line rho is on". That was wrong, and the repo's own
# PL-22 work already had the right answer. These tests pin the corrected claim.

GAMMA = mp.mpf("14.13472514173469379045725198356247027")
RHO = mp.mpc(mp.mpf(1) / 2, GAMMA)


def _chi(s):
    return mp.pi ** (s - mp.mpf(1) / 2) * mp.gamma((1 - s) / 2) / mp.gamma(s / 2)


def test_zeta_zero_over_zero_IS_removable():
    """zeta(s)/zeta(1-s) -> chi(rho), the same from every approach direction."""
    mp.mp.dps = 40
    ratio = lambda s: mp.zeta(s) / mp.zeta(1 - s)
    errs = []
    for eps in (mp.mpf("1e-4"), mp.mpf("1e-6"), mp.mpf("1e-8")):
        worst = 0.0
        for ang in (0.0, 0.6, 1.4, 2.3, -1.1):
            v = ratio(RHO + eps * mp.e ** (1j * ang))
            worst = max(worst, abs(complex(v - _chi(RHO))))
        errs.append(worst)
    assert errs[-1] < 1e-7
    # and the error falls linearly with eps, i.e. it is the O(eps) Taylor term
    assert errs[0] / errs[-1] > 1e3


def test_abs_chi_is_one_on_the_whole_line_not_just_at_zeros():
    """|chi| = 1 holds at a NON-zero on the line too, so it cannot detect a zero."""
    mp.mp.dps = 40
    impostor = mp.mpc(mp.mpf(1) / 2, GAMMA + mp.mpf("0.5"))
    assert abs(mp.zeta(impostor)) > 1e-3, "the control point must not be a zero"
    assert abs(complex(abs(_chi(impostor)) - 1)) < 1e-30
    assert abs(complex(abs(_chi(RHO)) - 1)) < 1e-30


def test_abs_chi_does_locate_a_point_relative_to_the_line():
    """It is not vacuous as a location identity -- only as a zero detector."""
    mp.mp.dps = 40
    for sigma in ("0.3", "0.45", "0.55", "0.7", "0.9"):
        v = abs(_chi(mp.mpc(mp.mpf(sigma), GAMMA)))
        assert abs(complex(v - 1)) > 1e-6, "off the line |chi| must depart from 1"


def test_recorded_g6_gate_says_removable_not_information_free():
    """Guard the wording, so the wrong conclusion cannot creep back in."""
    art = _load("c0_zero_locus_data.json")
    g6 = next(v for k, v in art["gates"].items() if k.startswith("G6"))
    assert g6["pass"] is True
    assert g6["zeta_removable"] is True
    assert g6["chi_line_whole"] is True
    assert "information-free" not in g6["detail"]
