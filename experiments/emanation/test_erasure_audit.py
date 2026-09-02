"""Tests for the generic erasure audit (experiments/emanation/erasure_audit.py).

The audit measures image dimension / merge (fiber) structure / erased
entropy / closing (forgetting) clock of ANY finite deterministic map on
ANY domain.  Its first dataset is the per-rule erasure spectrum of all
256 ECA rules on the N=8 ring.

Verified claims locked here:
  1) eca_ring_step(29) reproduces traffic_law.evolve_ring(29) exactly
     (the audit engine agrees with the independently-verified ring path);
  2) the FULL-density ring attractor of rules 29/71 = configs where the
     MINORITY species is isolated = independent-sets(cars) union
     independent-sets(holes), minus the 2 alternating patterns when N is
     even.  Count = 2*i_cyc(N) - 2*delta(N even), with
     i_cyc(N) = total independent sets of the N-cycle (e.g. 47 for C_8,
     so the 29/71 attractor on N=8 has 2*47 - 2 = 92 states) -- this
     lifts the n-sector state-space collapse (L8) to ALL densities;
  3) trivial anchors: rule 0 and rule 255 collapse to one state in one
     step; rule 204 (identity) erases nothing (0.0 bits, ledger flat at
     once);
  4) the audit is truly generic: a non-ECA map (a,b) -> (a and b,) on a
     4-state domain reports erased_bits == 1.0 exactly.
"""
import itertools
import json
import os
import random

import experiments.emanation.erasure_audit as ea
import experiments.emanation.traffic_law as tl


def _ring_plateau(N, rule, horizon=6):
    domain = tuple(itertools.product((0, 1), repeat=N))
    a = ea.audit(domain, lambda s, r=rule: ea.eca_ring_step(r, s),
                 horizon=horizon)
    return a


def _indep_cycle_total(N):
    n = 0
    for c in itertools.product((0, 1), repeat=N):
        s = [i for i, v in enumerate(c) if v]
        if all(c[(i - 1) % N] == 0 for i in s):
            n += 1
    return n


def test_eca_ring_step_matches_evolve_ring():
    rng = random.Random(11)
    for N in (6, 7, 8, 10):
        for _ in range(30):
            bits = tuple(rng.getrandbits(1) for _ in range(N))
            pos = ea.bits_to_positions(bits)
            for rule in (29, 71):
                assert ea.bits_to_positions(ea.eca_ring_step(rule, bits)) \
                    == tuple(sorted(tl.evolve_ring(rule, list(pos), N, 1)))


def test_full_density_ring_attractor_29_71():
    # EVERY configuration of the N-ring relaxes onto minority-isolated
    # configs: cars-with-no-two-adjacent, or holes-with-no-two-adjacent.
    # Count = 2*i_cyc(N) - 2*delta(N even); exact for N = 5..9.
    for N in (5, 6, 7, 8):
        plat = _ring_plateau(N, 29)["images_by_t"][-1]
        for rule in (29, 71):
            plat = _ring_plateau(N, rule)["images_by_t"][-1]
            pred = 2 * _indep_cycle_total(N) - (2 if N % 2 == 0 else 0)
            assert plat == pred, (N, rule, plat, pred)
    # explicit N=8 numbers: independent sets of C_8 = 47 (and 204, 0, 255)
    assert _indep_cycle_total(8) == 47
    assert _ring_plateau(8, 29)["images_by_t"][-1] == 2 * 47 - 2 == 92
    assert _ring_plateau(8, 71)["images_by_t"][-1] == 92


def test_trivial_rule_anchors():
    domain = tuple(itertools.product((0, 1), repeat=8))
    a0 = ea.audit(domain, lambda s: ea.eca_ring_step(0, s), horizon=3)
    assert a0["image_1"] == 1 and a0["erased_bits"] == 8.0
    a255 = ea.audit(domain, lambda s: ea.eca_ring_step(255, s), horizon=3)
    assert a255["image_1"] == 1 and a255["erased_bits"] == 8.0
    ai = ea.audit(domain, lambda s: ea.eca_ring_step(204, s), horizon=3)
    assert ai["image_1"] == 256 and ai["erased_bits"] == 0.0
    assert ai["images_by_t"] == [256, 256, 256, 256]


def test_audit_is_generic_non_eca_map():
    # a NON-ECA deterministic map on a 4-state domain: (a,b) -> (a AND b,)
    # (horizon must be 1 here: the map's outputs live in a 1-tuple space,
    # so it cannot feed its own outputs for a multi-step ledger -- the
    # audit documents this: horizon > 1 needs f defined on its attractor)
    domain = [(0, 0), (0, 1), (1, 0), (1, 1)]
    a = ea.audit(domain, lambda c: (c[0] and c[1],), horizon=1)
    assert a["total"] == 4
    assert a["image_1"] == 2          # outputs {0,1}
    assert a["merge_classes"] == 1    # only output 0 is a merge (fiber 3)
    assert a["merged_configs"] == 2   # (3-1)+(1-1)
    assert a["max_fiber"] == 3
    assert a["erased_bits"] == 1.0    # log2(4)-log2(2) exactly one bit


def test_rule_erasure_spectrum_roundtrip():
    spec = ea.rule_erasure_spectrum(N=6, rules=(0, 29, 71, 204),
                                    horizon=2)
    assert spec["0"]["image_1"] == 1
    assert spec["204"]["image_1"] == 64
    assert spec["29"]["image_1"] == spec["71"]["image_1"]
    path = os.path.join(
        os.path.dirname(os.path.abspath(
            __import__("experiments.emanation.erasure_audit",
                       fromlist=["x"]).__file__)), "data", "_audit_tmp.json")
    ea.save_spectrum(spec, path)
    with open(path, encoding="utf-8") as fh:
        again = json.load(fh)
    os.remove(path)
    assert again == spec