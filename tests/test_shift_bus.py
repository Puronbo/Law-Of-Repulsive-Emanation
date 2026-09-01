"""Tests for shift_bus: the verified soliton shift bus.

Claims verified here:
  * exact ballistic paths for all four rules (single-1 solitons)
  * the rules are NOT linear -- verified strictly on dense configs
  * lane-sharing works for the separating case it's designed for
"""

import random

import pytest

import shift_bus as sb


# ---------------------------------------------------------------------------
# Exact ballistic paths (soliton invariants)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rule,direction", [(12, +1), (44, +1),
                                            (68, -1), (100, -1)])
def test_exact_soliton_path(rule, direction):
    W, C, T = 4000, 2000, 400
    got = sb.evolve(rule, {C}, W, T)
    # all four rules deliver the particle head exactly at C + direction*T
    if rule in (12, 68):
        assert got == {C + direction * T}, "rule %d single cell" % rule
    else:
        # rule 44/100 period-2: head is at C + direction*T, plus a tail cell
        head = min(got) if direction > 0 else max(got)
        assert head == C + direction * T
        assert len(got) in (1, 2)


def test_exact_velocity_long_horizon():
    for rule, d in ((12, +1), (44, +1), (68, -1), (100, -1)):
        W, C = 4000, 2000
        for t in (200, 400, 800, 1600):
            got = sb.evolve(rule, {C}, W, t)
            head = min(got) if d > 0 else max(got)
            assert (head - C) == d * t, "rule %d drift at t=%d" % (rule, t)


# ---------------------------------------------------------------------------
# NOT linear: strict check on dense/interacting configs
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rule", list(sb.SOLITONS))
def test_strict_nonlinearity(rule):
    """Superposition must hold on dense configs for a linear rule.

    These rules fail it almost always -> they are NOT linear. This is the
    honest self-correction of an earlier overclaim.
    """
    W, T, trials = 80, 20, 500
    violations = 0
    rng = random.Random(7)
    for _ in range(trials):
        a = rng.getrandbits(W)
        b = rng.getrandbits(W)
        e_ab = sb.read(rule, a ^ b, W, T)
        ea = sb.read(rule, a, W, T)
        eb = sb.read(rule, b, W, T)
        if e_ab != (ea ^ eb):
            violations += 1
    assert violations > trials * 0.9, \
        "rule %d was unexpectedly (almost) linear: %d/%d violations" \
        % (rule, violations, trials)


# ---------------------------------------------------------------------------
# Separation compositionality (the TRUE usable property)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rule", list(sb.SOLITONS))
def test_separated_packets_compose(rule):
    """For well-separated packets, union-evolution == evolution-union."""
    W, T = 6000, 300
    a = {1000, 1003, 1007}
    b = {4000, 4004}
    sum_mask = sb.packet_bits(a, W) ^ sb.packet_bits(b, W)
    got = sb.read(rule, sum_mask, W, T)
    expected = sb.read(rule, sb.packet_bits(a, W), W, T) \
        ^ sb.read(rule, sb.packet_bits(b, W), W, T)
    assert got == expected


# ---------------------------------------------------------------------------
# Lane sharing + recovery (valid only when separated)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rule", list(sb.SOLITONS))
def test_lane_sharing_recover_both(rule):
    W, T = 6000, 250
    a = {1000, 1003, 1007}
    b = {4000, 4004}
    ma = sb.packet_bits(a, W)
    mb = sb.packet_bits(b, W)

    combined = sb.share_lanes(rule, [ma, mb], W, T)

    ea = sb.evolve(rule, a, W, T)
    eb = sb.evolve(rule, b, W, T)

    rec_a = sb.recover(combined, rule, [mb], W, T)
    rec_b = combined ^ sb.read(rule, ma, W, T)

    assert rec_a == sb.packet_bits(ea, W)
    assert rec_b == sb.packet_bits(eb, W)


# ---------------------------------------------------------------------------
# Direction invariants
# ---------------------------------------------------------------------------

def test_right_lane_never_moves_left():
    W, T = 2000, 200
    for rule in (12, 44):
        got = sb.evolve(rule, {0}, W, T)
        assert min(got) >= T - 1


def test_left_lane_never_moves_right():
    W, T = 2000, 200
    for rule in (68, 100):
        got = sb.evolve(rule, {W - 1}, W, T)
        assert max(got) <= (W - 1) - T + 1


# ---------------------------------------------------------------------------
# Bitmask helpers
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mask", [0b1010, 0b110011, 0b100000001, 0])
def test_mask_roundtrip(mask):
    assert sb.packet_bits(sb.bits_to_positions(mask), 64) == mask


def test_evolve_small_manual_invariant():
    W, T, k = 2000, 100, 555
    got = sb.evolve(12, {k}, W, T)
    assert got == {k + T}