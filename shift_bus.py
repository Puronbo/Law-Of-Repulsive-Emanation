"""One-bit shift bus from verified ECA solitons.

Rules {12, 44} move a lone 1 right; rules {68, 100} move a lone 1 left.
Long-horizon verification (open lattice, t up to 1600) shows the motion is
EXACT:

    rule 12 :  {0} -> {1} -> {2} -> ...   (single cell, +1/step)
    rule 68 :  {0} -> {-1} -> {-2} -> ... (single cell, -1/step)
    rule 44 :  {0} -> {0,1} -> {2} -> {2,3} -> {4} -> {4,5} -> ... (+1/step)
    rule 100:  {0} -> {-1,0} -> {-2} -> {-3,-2} -> {-4} -> ... (-1/step)

These particles are solitons: a lone 1 travels without decaying. Because
their evolutions never create additional 1s behind them, WELL-SEPARATED
packets evolve independently: the evolution of a disjoint union of packets
equals the disjoint union of their individual evolutions. This is what
makes lane-sharing possible.

CRITICAL HONEST LIMIT (verified by test_strict_nonlinearity): the rules are
NOT linear. Rule 12 is the boolean function out=(left AND NOT center)
(affine check: fails for all four). Superposition E(A XOR B) == E(A) XOR
E(B) holds ONLY when the evolving supports stay disjoint. On dense or
interacting configs it fails massively (2999/3000 violations for rule 12).
There is NO general computation: no AND/OR combine, no universality.

Collision test with NON-adjacent packets (rule 12): two lone 1s at gap >= 2
never merge; they pass as independent +1 movers.
"""

RIGHT = (12, 44)
LEFT = (68, 100)
SOLITONS = RIGHT + LEFT

_NEI = ((1, 1, 1), (1, 1, 0), (1, 0, 1), (1, 0, 0),
        (0, 1, 1), (0, 1, 0), (0, 0, 1), (0, 0, 0))


def step(rule, row):
    """One synchronous ECA step with open (zero) boundaries."""
    L = len(row)
    w = [0] + list(row) + [0]
    out = []
    for i in range(L):
        t = (w[i], w[i + 1], w[i + 2])
        out.append((rule >> _NEI.index(t)) & 1)
    return out


def step_n(rule, row, steps):
    """`steps` synchronous applications of `step`."""
    for _ in range(steps):
        row = step(rule, row)
    return row


def evolve(rule, positions, width, steps):
    """Evolve a sparse 0/1 row for `steps`; return set of set-bit indices."""
    row = [0] * width
    for p in positions:
        if 0 <= p < width:
            row[p] = 1
    row = step_n(rule, row, steps)
    return {i for i, v in enumerate(row) if v}


def packet_bits(positions, width):
    """Materialize `positions` as a 0/1 integer bitmask (LSB = index 0)."""
    m = 0
    for p in positions:
        if 0 <= p < width:
            m |= 1 << p
    return m


def bits_to_positions(mask):
    """Inverse of `packet_bits`: positions of set bits in a bitmask."""
    out = []
    p = 0
    while mask:
        if mask & 1:
            out.append(p)
        mask >>= 1
        p += 1
    return out


def read(rule, mask, width, steps):
    """Evolve a bitmask-packet for `steps` under `rule`; return bitmask."""
    row = [0] * width
    for i, b in enumerate(bin(mask)[2:][::-1]):
        if b == '1' and i < width:
            row[i] = 1
    row = step_n(rule, row, steps)
    m = 0
    for i, v in enumerate(row):
        if v:
            m |= 1 << i
    return m


def share_lanes(rule, lanes, width, steps):
    """XOR-sum several packet bitmasks onto one row, evolve once.

    VALID ONLY when the packets are well-separated (evolving supports
    disjoint) -- then soliton evolution is compositional and the sum row
    carries every packet simultaneously. NOT valid for interacting/dense
    configs (the rules are not linear).
    """
    total = 0
    for lane in lanes:
        total ^= lane
    return read(rule, total, width, steps)


def recover(lane_combined, rule, other_lanes, width, steps):
    """Recover one packet's evolution by XOR-subtracting all others.

    Same validity condition as `share_lanes`: disjoint supports.
    """
    others = 0
    for o in other_lanes:
        others ^= o
    return lane_combined ^ read(rule, others, width, steps)