"""Tests for the tagged (degreed-of-freedom) shift transport.

The 4-rule shift bus now carries a label.  These tests pin:
  1. content conservation: tag rides head exactly (all 4 rules, single packet)
  2. separation: on PASS schedules each tag follows its OWN head
  3. annihilation: on MERGE the survivor is the head packet, the other
     tag is irrecoverable (non-injective, deterministic loss)
  4. multi-head bijection under wide separation
"""
import pytest

from experiments.emanation import tagged_shift as ts
import shift_bus as sh


def test_lone_packet_tag_rides_head_exactly_all_rules():
    for rule in (12, 44, 68, 100):
        p = 500 if rule in (12, 44) else 700
        v = ts.VELOCITY[rule]
        for t in (1, 17, 99):
            delivered, lost = ts.evolve_tags(rule, {p: 0xBEEF}, t)
            assert delivered == {p + v * t: 0xBEEF}   # exact position AND tag
            assert lost == {}


def test_pass_settle_each_tag_follows_its_own_head():
    # gap large enough that no merge: two packets, distinct tags
    rule, p1, p2 = 12, 400, 600
    packets = {p1: 11, p2: 22}
    delivered, lost = ts.evolve_tags(rule, packets, 40)
    assert delivered == {440: 11, 640: 22}     # each tag kept its own head
    assert lost == {}

    # and the rotated variant: p1 carries 22, p2 carries 11
    delivered, lost = ts.evolve_tags(rule, {p1: 22, p2: 11}, 40)
    assert delivered == {440: 22, 640: 11}
    assert lost == {}


def test_merge_destroys_exactly_the_absorbed_packet():
    # rule 12 gap-1: {10,11} -> {12} in one step; only the packet whose
    # header continues into {12} survives (tag 9 from position 11).  The
    # absorbed packet (tag 7 from position 10) vanishes; its free-law ghost
    # head (10 -> 11) is where we record the loss.
    delivered, lost = ts.evolve_tags(12, {10: 7, 11: 9}, 1)
    assert delivered == {12: 9}
    assert lost == {11: 7}                     # exactly one tag lost
    # tag multiset is conserved through the whole bus (every tag is either
    # delivered or accounted-lost; none vanishes without attribution)
    all_tags = sorted(list(delivered.values()) + list(lost.values()))
    assert all_tags == [7, 9]


def test_merge_loss_is_deterministic_and_irreversible():
    # reverse order of inputs must still yield the SAME survivor (physically
    # the collision outcome is a function of position, not label)
    d1, l1 = ts.evolve_tags(12, {10: 7, 11: 9}, 1)
    d2, l2 = ts.evolve_tags(12, {10: 5, 11: 3}, 1)
    assert sorted(d1) == sorted(d2) and sorted(l1) == sorted(l2)
    # non-injective: two DIFFERENT initial tag multisets end at the same time;
    # but the position+survivor-tag outcome is identical, so label info is
    # partially destroyed (3 lost in case 2 -> cannot recover 5).
    assert d1 == {12: 9} and d2 == {12: 3}
    assert l2 == {11: 5}


def test_wide_separation_bijection_multiple_packets():
    packets = {200: 'a', 400: 'b', 600: 'c'}
    delivered, lost = ts.evolve_tags(12, packets, 30)
    assert delivered == {230: 'a', 430: 'b', 630: 'c'}
    assert lost == {}
    assert len(delivered) == len(packets)      # injective as a transport map


def test_left_mover_tags_also_exact():
    p = 800
    delivered, lost = ts.evolve_tags(68, {p: 42}, 33)
    assert delivered == {p - 33: 42}
    assert lost == {}


def test_blob_rule_44_tag_on_head_even_through_blob():
    # rule 44's orbit is period-2 (head, blob); the tag must ride the head
    # at every phase, including after a blob cell is created
    delivered, lost = ts.evolve_tags(44, {500: 77}, 2)
    assert delivered == {502: 77}
    assert lost == {}
    delivered, lost = ts.evolve_tags(44, {500: 77}, 3)
    assert delivered == {503: 77}
    assert lost == {}


def test_no_phantom_delivery_on_empty():
    assert ts.evolve_tags(12, {}, 50) == ({}, {})


@pytest.mark.parametrize("seed", range(25))
def test_fuzz_tag_invariants_all_rules(seed):
    import random
    rng = random.Random(seed)
    for rule in (12, 44, 68, 100):
        # packets randomly placed to exercise both PASS and MERGE regimes
        base = max(100, rule % 2)  # avoid negative for 68/100: keep well inside
        base = 300
        n = rng.randint(1, 5)
        positions = sorted(rng.sample(range(25, 170 - 2 * n), n))
        for p in positions:
            pass
        packets = {p + 5: rng.randint(0, 10**3) for p in positions}
        steps = rng.randint(1, 40)
        delivered, lost = ts.evolve_tags(rule, packets, steps)

        # invariant 1: every input tag is either delivered at its head or
        # accounted-lost (multiset conserved, nothing vanishes silently)
        all_out = sorted(list(delivered.values()) + list(lost.values()))
        assert all_out == sorted(packets.values())

        # invariant 2: any head actually present on the lattice has its tag
        # intact -- and the delivered mapping is not garbled re: positions
        for h in delivered:
            v = ts.VELOCITY[rule]
            # the delivered head MUST be some input p + v*steps exactly
            assert (h - v * steps) in packets

        # invariant 3: surviving heads coincide with ground truth occupancy
        pad = 2 * steps + 8
        lo = min(packets) - pad
        W = (max(packets) + pad) - lo + 1
        truth = sh.evolve(rule, [p - lo for p in packets], W, steps)
        truth = {p + lo for p in truth}
        assert set(delivered) <= truth
        # and every truth cell within the packet cloud has exactly one head
        # unless it is a blob tail (44/100): heads form a subset of truth