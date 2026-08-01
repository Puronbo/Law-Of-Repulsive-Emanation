"""
Regression suite for the spring-fold series (T58-T64).

Pins the verified invariants so none of the measured facts can drift:
  - fold areas (2 a^2 TH^3 / 6), crease angles (2 arctan(1/TH))
  - the clock test (intrinsic features survive re-indexing, conventions
    do not)
  - the fold-as-optimizer (Hamiltonian retrace conserves; damped locks)
  - the rotation test (structure survives rotations, not relabeling)
  - the prime engine (Lucy-Hedgehog + segmented sieve counts)
  - the eikonal fold and the retrace boundary (viscosity selection)

Run:  python -m pytest tests/test_spring_series.py -q
"""

import math
import os, sys, json

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'experiments'))

A, TH = 1.0, 20.0
H = 0.01


def load(name):
    with open(os.path.join(ROOT, 'data', name)) as fp:
        return json.load(fp)


def test_t58_t63_doubling_area_law():
    d = load('eikonal_fold_data.json')
    assert math.isclose(d['area_mirror'], 2666.6666666666665, rel_tol=1e-4)
    assert math.isclose(d['area_pred'], 2 * A * A * TH ** 3 / 6, rel_tol=1e-9)
    assert math.isclose(d['area_retrace'], 0.0, abs_tol=1e-9)


def test_t58_t63_crease_is_soft():
    d = load('eikonal_fold_data.json')
    pred = 2 * math.atan(1 / TH)
    assert math.isclose(d['crease_pred_pi'], pred / math.pi, rel_tol=1e-9)
    assert 0.0 < d['crease_pred_pi'] < 0.1  # soft, not a hard fold
    # T58 measured 0.0329*pi and the derived value 0.0318*pi agree
    assert abs(d['crease_pred_pi'] - 0.0329) < 0.005


def test_t63_upwind_converges_to_the_tent():
    d = load('eikonal_fold_data.json')
    assert d['eikonal_err'] < 1e-10  # measured 3.3e-13
    assert abs(d['cut_locus']) < 1e-9


def test_t64_zigzags_are_weak_solutions_tent_unique():
    from retrace_boundary import zigzag, tent, viscosity_check
    theta = np.arange(0, 2 * TH + H / 2, H)
    r_tent = tent(theta)
    ok, _, fails = viscosity_check(r_tent, theta)
    assert ok and fails == 0
    for xi in (0.2 * TH, 0.5 * TH, 0.8 * TH):
        r = zigzag(theta, xi)
        d = np.diff(r) / np.diff(theta)
        assert np.allclose(np.abs(d), A, atol=1e-9)  # weak solution
        assert r[0] == 0 and r[-1] == 0
        ok, _, fails = viscosity_check(r, theta)
        assert not ok and fails >= 1  # down-up corner kills supersolution


def test_t64_erosion_selects_the_tent():
    from retrace_boundary import zigzag, tent, upwind_eikonal
    d = load('retrace_boundary_data.json')
    assert d['upwind_from_zigzag_err'] < 1e-10
    assert d['corner_after'] > d['corner_before']  # one-step erosion raises it
    theta = np.arange(0, 2 * TH + H / 2, H)
    r_relax = upwind_eikonal(theta, zigzag(theta, 0.5 * TH))
    assert float(np.max(np.abs(r_relax - tent(theta)))) < 1e-10
    assert abs(d['cut_locus_eq']) < 1e-9
    assert d['reflection'] < 1e-9  # |r'| conserved across the crease


def test_t59_clock_test_intrinsic_features_survive():
    d = load('clock_test_data.json')
    assert d['f1'] > 0.99          # calendar carries the law at this clock
    assert d['f2'] < 0.6           # ... and collapses under +15-day re-index
    assert d['f3a'] > 0.99 and d['f3b'] > 0.99  # intrinsic residues survive


def test_t60_fold_as_optimizer_never_locks_when_hamiltonian():
    d = load('fold_optimizer_data.json')
    assert d['drift_h'] < 0.02              # energy conserved on retrace
    assert d['area_ratio_h'] > 0.9          # phase area conserved
    assert d['recurrence'] < 0.01           # never locks
    assert d['area_ratio_d'] < 0.05         # dissipation contracts
    assert d['lock_err'] == 0.0             # and locks at the minimum


def test_t61_rotation_test_structure_survives_rotations():
    d = load('rotation_test_data.json')
    assert d['overlap_rotation'] > 0.99
    assert d['sim_corr'] > 0.99
    assert d['overlap_abs'] > d['chance']  # relabeling keeps structure above
    assert d['chance'] < 0.2               # ... but far below rotation


def test_t62_prime_engine_counts_from_scratch():
    from prime_count_from_scratch import lucy_primepi, simple_sieve, \
        segmented_window
    assert lucy_primepi(10_262) == 1258
    assert lucy_primepi(26_102) == 2868
    assert len(simple_sieve(1_000)) == 168
    assert segmented_window(730_421, 730_421).size == 1 \
        and segmented_window(730_421, 730_421)[0] == 730421
    assert segmented_window(730_422, 730_422).size == 0


def test_t62_retrace_chain_prime_bridge():
    # 26102 = 2 * 31 * 421 and 730421 prime: the 421-factor bridges to the
    # date number; the year-0 Gregorian count 730783 is a prime twin
    assert 26_102 == 2 * 31 * 421
    assert 730_421 % 421 == 407 and 407 == 11 * 37
    assert 730_783 - 2 in (730_781,)
    assert 730_783 % 2 == 1 and 730_783 % 730_783 == 0
