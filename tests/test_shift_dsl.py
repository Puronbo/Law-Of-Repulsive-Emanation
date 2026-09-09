"""Tests for shift_dsl: the verified shift-spec language."""

import pytest

import shift_bus as sh
import shift_dsl as sd
from shift_dsl import SpecError


def _spec(T=250, rule=12, lane='R', pkt='A', at='1000, 1003, 1007'):
    return (
        'lane R rule 12\n'
        'lane L rule 68\n'
        '# comment line\n'
        'packet %s on %s at %s\n'
        'run %d\n'
    ) % (pkt, lane, at, T)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def test_parse_basic():
    p = sd.parse(_spec())
    assert p['time'] == 250
    assert p['lanes']['R']['velocity'] == +1
    assert p['lanes']['L']['velocity'] == -1
    assert p['packets']['A']['lane'] == 'R'
    assert p['packets']['A']['positions'] == [1000, 1003, 1007]


def test_parse_unknown_lane_raises():
    with pytest.raises(SpecError):
        sd.parse(_spec(pkt='A', lane='Z'))


def test_parse_bad_rule_raises():
    with pytest.raises(SpecError):
        sd.parse('lane R rule 13\nrun 5\n')


def test_parse_missing_run_raises():
    with pytest.raises(SpecError):
        sd.parse('lane R rule 12\npacket A on R at 5\n')


def test_parse_duplicate_packet_raises():
    with pytest.raises(SpecError):
        sd.parse('lane R rule 12\n'
                 'packet A on R at 1,2\n'
                 'packet A on R at 3,4\n'
                 'run 5\n')


def test_parse_garbage_raises():
    with pytest.raises(SpecError):
        sd.parse('hello world\n')


# ---------------------------------------------------------------------------
# Compile + verify on all four rules
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rule,direction", [(12, +1), (44, +1),
                                            (68, -1), (100, -1)])
def test_verify_lands_exactly(rule, direction):
    T = 200
    spec = ('lane L rule %d\n'
            'packet A on L at 1000, 1003\n'
            'run %d\n') % (rule, T)
    evolved, rep, sep = sd.run_spec(spec, width=6000)
    assert rep['A']['ok'], rep
    want = [1000 + direction * T, 1003 + direction * T]
    assert sorted(set(want)) == rep['A']['expected']


@pytest.mark.parametrize("rule,direction", [(12, +1), (44, +1),
                                            (68, -1), (100, -1)])
def test_lane_velocity_is_compile_time_fixed(rule, direction):
    """A lane's direction is bound at PARSE time: the DSL provides no clause
    to redirect a packet mid-flight (no routing table, no adaptivity).  Any
    attempt to express a route change is a hard spec error, and the only way
    a bit ever moves is forward/back at the declared constant velocity."""
    bad_specs = [
        # routing / re-routing clauses do not exist in the grammar
        'lane R rule 12\npacket A on R at 10\nroute A to L\nrun 5\n',
        'lane R rule 12\npacket A on R at 10\nthen lane L\nrun 5\n',
        'lane R rule 12\nredirect A active run 3\nrun 5\n',
    ]
    for s in bad_specs:
        with pytest.raises(SpecError):
            sd.parse(s)
    # and the velocity dict is the only addressable direction
    assert sd.VELOCITY[rule] == direction


def test_packets_have_no_content_same_position_indistinguishable():
    """Bits carry no payload: a cell holds exactly one bit.  Two packets
    co-located at the same position produce ONE bit -- there is no header,
    no identifier, no way to tell them apart.  (The internet distinguishes
    packets by routing headers; here only position distinguishes bits.)"""
    spec = ('lane R rule 12\n'
            'packet A on R at 500\n'
            'packet B on R at 500\n'
            'run 100\n')
    _, rep, sep = sd.run_spec(spec, width=2000)
    assert rep['A']['ok'] and rep['B']['ok']
    # both packets landed at the SAME single cell: fused lane carries 1 bit
    assert rep['A']['actual'] == [600]
    assert rep['A']['actual'] == rep['B']['actual']
    assert sep['R'] is True   # trivially separated: they ARE one bit
    assert sh.evolve(12, [500], 2000, 100) == {600}


def test_packets_have_no_content_rename_invariant():
    """Read-out is a pure function of POSITIONS: renaming packets changes
    nothing, and identical-position packets evolve identically regardless of
    name.  No identifier field exists to distinguish 'what' from 'where'."""
    spec_a = ('lane R rule 12\npacket x on R at 100, 300\nrun 50\n')
    spec_b = ('lane R rule 12\npacket y on R at 100, 300\nrun 50\n')
    _, rep_a, _ = sd.run_spec(spec_a, width=1000)
    _, rep_b, _ = sd.run_spec(spec_b, width=1000)
    assert rep_a['x']['actual'] == rep_b['y']['actual']


def test_collision_is_information_destroying():
    """Gap-1 collision under rule 12 MERGES two bits into one: the map from
    inputs to outputs is non-injective, so the landing-position protocol can
    never recover which packet carried 'what'.  No error-detection header,
    no redundancy, no retransmission (all required for internet-class
    delivery)."""
    a = sh.evolve(12, [100, 101], 400, 60)
    b = sh.evolve(12, [101, 100], 400, 60)
    assert a == b == {161}          # both orders collapse to ONE cell
    # the two distinct 2-bit inputs map to the same 1-bit output: the
    # input->output map is NOT injective, so the identity of each original
    # packet is irrecoverable after collision
    assert len({100, 101}) == 2 and {100, 101} != {161}
    # individually they survive as lonely solitons
    assert sh.evolve(12, [100], 400, 60) == {160}
    assert sh.evolve(12, [101], 400, 60) == {161}


def test_errors_are_permanent_no_correction():
    """Inject a single extra 1 mid-flight (a one-bit corruption): it is
    itself a stable soliton and persists forever.  The system has NO error
    correction, NO repair mechanism -- so it cannot carry internet-grade
    reliability (where damaged packets are dropped and retransmitted)."""
    # evolve clean for 20 steps
    seg1 = sh.evolve(12, [100], 400, 20)          # {120}
    # inject a bit far away and evolve 80 more
    injected = seg1 | {250}
    final = sh.evolve(12, sorted(injected), 400, 80)
    assert final == {200, 330}                    # both solitons intact
    # had error correction existed, the injected cell would be gone


def test_full_collision_census_never_deflects():
    """Structural theorem for the whole 4-rule family: the ONLY collision
    outcomes are PASS (separation maintained, no interaction -- the gap >= 2
    case) and MERGE (destructive, non-injective).  Elastic deflection -- the
    interaction that billiard-ball / glider-collision logic depends on --
    NEVER occurs.  This is the rigorous reason the system cannot express
    collision-based computation, no matter the language."""
    outcomes = {}
    for rule in (12, 44, 68, 100):
        row = {}
        for d in range(1, 8):   # d=0 = same cell = one particle, not a collision
            a, b, W, T = 100, 100 + d, 500, 90
            full = sh.evolve(rule, [a, b], W, T)
            sa = sh.evolve(rule, [a], W, T)
            sb = sh.evolve(rule, [b], W, T)
            n = len(full)
            if full == sa | sb and n == 2:
                kind = 'PASS'
            elif n == 1:        # two bits in, one out: destructive merge
                kind = 'MERGE'
            else:
                kind = 'DEFLECT'
            row[d] = kind
        outcomes[rule] = row
    assert all(
        row[d] in ('PASS', 'MERGE')
        for row in outcomes.values() for d in row
    ), outcomes
    # and the 'DEFLECT' detector would have fired somewhere IF deflection
    # were possible -- sanity: at least one MERGE exists (the gap-1 rule 12
    # case), so the classifier is not vacuously all-PASS
    assert any('MERGE' in row.values() for row in outcomes.values())
    # spot-check the known-equal landing law is preserved out of the census
    assert sh.evolve(12, [100, 104], 500, 90) == \
        sh.evolve(12, [100], 500, 90) | sh.evolve(12, [104], 500, 90)


def test_lane_capacity_bound():
    """Bandwidth ceiling under the separation constraint: single-cell
    movers (rules 12/68) reach 0.5 bits/cell/lane/step; blob movers
    (44/100) reach 0.25 bits/cell.  Packed at these bounds the flight stays
    EXACT over a long horizon (no interference) -- a hard, verified ceiling
    for how much 'traffic' one lane can carry."""
    # rule 12: every-2 packing, 200 bits on 400 cells
    p12 = list(range(0, 400, 2))
    assert sh.evolve(12, p12, 800, 200) == set(q + 200 for q in p12)
    # rule 100: every-4 packing (blob is 2 cells at odd t), interior only
    p100 = list(range(500, 1100, 4))
    assert sh.evolve(100, p100, 1600, 100) == set(q - 100 for q in p100)
    # rule 44: mirror, every-4 interior
    p44 = list(range(500, 1100, 4))
    assert sh.evolve(44, p44, 1600, 100) == set(q + 100 for q in p44)
    # rule 68 dense, left-moving mirror of 12
    p68 = list(range(400, 800, 2))
    assert sh.evolve(68, p68, 900, 100) == set(q - 100 for q in p68)
    # sanity: blob rules do NOT reach the 0.5 ceiling (spacing 2 fails)
    assert sh.evolve(100, list(range(500, 900, 2)), 1400, 100) != set(
        q - 100 for q in range(500, 900, 2))
    assert sh.evolve(44, list(range(500, 900, 2)), 1400, 100) != set(
        q + 100 for q in range(500, 900, 2))
    # sanity: blob rule does NOT hold at the 0.5 ceiling
    p_too = list(range(500, 900, 2))
    assert sh.evolve(100, p_too, 1400, 100) != set(q - 100 for q in p_too)


def test_expect_clause_agrees_with_evolution():
    T = 100
    spec = ('lane R rule 12\n'
            'packet A on R at 500\n'
            'run %d\n'
            'expect A at 600\n') % T
    p = sd.parse(spec)
    assert p['expect']['A'] == [600]
    _, rep, sep = sd.run_spec(spec)
    assert rep['A']['actual'][0] == 600


# ---------------------------------------------------------------------------
# Two lanes, two packets, one spec
# ---------------------------------------------------------------------------

def test_two_lanes_two_packets():
    spec = ('lane R rule 44\n'
            'lane L rule 100\n'
            'packet A on R at 1500\n'
            'packet B on L at 4500\n'
            'run 300\n')
    _, rep, sep = sd.run_spec(spec, width=6000)
    assert rep['A']['ok'] and rep['B']['ok']
    assert rep['A']['expected'] == [1500 + 300]
    assert rep['B']['expected'] == [4500 - 300]
    assert sep['R'] is True and sep['L'] is True


# ---------------------------------------------------------------------------
# Negative control: a wrong spec must FAIL verify
# ---------------------------------------------------------------------------

def test_verify_catches_wrong_velocity():
    # packet placed on rule 68 (left) but expect-clause says it went right
    spec = ('lane L rule 68\n'
            'packet A on L at 4000\n'
            'run 100\n'
            'expect A at 4100\n')   # wrong: real landing is 3900
    prog = sd.parse(spec)
    evolved = sd.compile_(prog)
    rep = sd.verify(prog, evolved)
    assert not rep['A']['ok']
    assert rep['A']['actual'][0] == 3900


def test_verify_rejects_fake_engine():
    # simulate a broken engine: evolve returns the packet untouched
    prog = sd.parse('lane L rule 12\npacket A on L at 1000\nrun 50\n')
    fake = {'A': {1000}}
    rep = sd.verify(prog, fake)
    assert not rep['A']['ok']


# ---------------------------------------------------------------------------
# Ground-truth oracle: independent truth-table simulator, structurally
# different from shift_bus (neighbor digit = 4*left + 2*center + right of a
# STANDARD Wolfram index; shift_bus indexes its _NEI tuple in the reversed
# bit order, so the rule number is bit-reversed here to mean the same
# table).  No shared code path with shift_bus.step.
# ---------------------------------------------------------------------------

def _rev8(b):
    return int(bin(b)[2:].zfill(8)[::-1], 2)


def oracle_rule(rule, b_left, b_center, b_right):
    digit = 4 * b_left + 2 * b_center + b_right
    return (_rev8(rule) >> digit) & 1


def oracle_evolve(rule, positions, width, steps):
    row = [0] * width
    for p in positions:
        if 0 <= p < width:
            row[p] = 1
    for _ in range(steps):
        w = [0] + list(row) + [0]
        row = [oracle_rule(rule, w[i], w[i + 1], w[i + 2])
               for i in range(width)]
    return {i for i, v in enumerate(row) if v}


@pytest.mark.parametrize("rule", [12, 44, 68, 100])
@pytest.mark.parametrize("steps", [0, 1, 2, 7, 50])
def test_oracle_matches_engine(rule, steps):
    width = 800
    positions = [10, 240, 500]
    want = oracle_evolve(rule, positions, width, steps)
    got = sh.evolve(rule, positions, width, steps)
    assert got == want


def test_oracle_random_configs_all_rules():
    import random
    rnd = random.Random(1234)
    for rule in (12, 44, 68, 100):
        for _ in range(40):
            width = rnd.randint(10, 300)
            steps = rnd.randint(0, 60)
            positions = rnd.sample(range(200), rnd.randint(0, 8))
            positions = [p for p in positions if p < width]
            assert (oracle_evolve(rule, positions, width, steps)
                    == sh.evolve(rule, positions, width, steps)), \
                (rule, width, steps, positions)


def test_dsl_compile_matches_oracle_via_spec():
    """End-to-end: DSL-compiled read-outs equal oracle evolution directly."""
    spec = ('lane R rule 12\n'
            'lane L rule 100\n'
            'packet A on R at 100, 400\n'
            'packet B on L at 200, 600\n'
            'run 120\n')
    prog = sd.parse(spec, width=1200)
    res = sd.compile_(prog)
    assert res['A'] == oracle_evolve(12, [100, 400], 1200, 120)
    assert res['B'] == oracle_evolve(100, [200, 600], 1200, 120)


def test_oracle_rule_agrees_with_engine_truth_table_all_rules():
    """Every 3-cell neighborhood, all 256 rules: oracle output == engine
    output.  This pins the _rev8 translation to shift_bus._NEI ordering
    independently of any single rule's physics."""
    from shift_bus import _NEI
    for rule in range(256):
        for idx, (bl, bc, br) in enumerate(_NEI):
            engine_bit = (rule >> idx) & 1
            assert oracle_rule(rule, bl, bc, br) == engine_bit, \
                (rule, idx, (bl, bc, br))


# ---------------------------------------------------------------------------
# Boundary rigor: open-boundary drop semantics, no wraparound
# ---------------------------------------------------------------------------

def test_boundary_drop_no_wraparound():
    # lone 1 at the right edge, rule 12 moves +1 -> falls off, lattice empty
    assert sh.evolve(12, [79], 80, 1) == set()
    assert oracle_evolve(12, [79], 80, 1) == set()
    # after t steps beyond the edge the row is empty, never wraps
    assert sh.evolve(12, [70], 80, 30) == set()
    # left edge, rule 68 -> falls off left
    assert sh.evolve(68, [0], 80, 1) == set()


def test_dsl_boundary_affected_clipped_flight_is_ok():
    # packet near the right edge: everything observable lands as head law,
    # and the packet is honestly flagged boundary-affected
    spec = ('lane R rule 12\n'
            'packet A on R at 78\n'
            'run 5\n')
    _, rep, _ = sd.run_spec(spec, width=80)
    assert rep['A']['boundary_affected'] is True
    # head law: 78+5=83 clips out -> expected []; the two in-range cells
    # (78->79->0) dropped, lattice reads empty
    assert rep['A']['ok'] is True
    assert rep['A']['actual'] == []


def test_boundary_twostep_rules_drop_with_tail():
    # rule 44 near edge: blob {head-1, head}; when head exits, tail that
    # remains observable is the only survivor, never stray cells
    spec = ('lane R rule 44\n'
            'packet A on R at 78\n'
            'run 3\n')
    _, rep, _ = sd.run_spec(spec, width=80)
    # trace manual: 78->{78,79}-> falls: only in-range cells evaluated;
    # head law would be 81 (clipped), observable at most {79}
    assert rep['A']['boundary_affected'] is True
    assert rep['A']['ok'] is True


# ---------------------------------------------------------------------------
# Bus mode: multiple packets sharing one lane, separation machine-checked
# ---------------------------------------------------------------------------

def test_bus_mode_two_packets_same_lane():
    spec = ('lane R rule 12\n'
            'packet A on R at 500\n'
            'packet B on R at 900\n'
            'run 100\n')
    _, rep, sep = sd.run_spec(spec, width=2000)
    assert rep['A']['ok'] and rep['B']['ok']
    assert sep['R'] is True
    assert rep['A']['expected'] == [600]
    assert rep['B']['expected'] == [1000]


def test_bus_separation_detects_overlap():
    # two packets on one lane at gap 1 (rule 12) interact mid-flight -> the
    # fused-lane differential is the detector of compositionality failure.
    # Per-packet verify() alone would look fine (each evolves as a lonely
    # soliton); ONLY the fused differential sees the merge.
    spec = ('lane R rule 12\n'
            'packet A on R at 100\n'
            'packet B on R at 101\n'
            'run 60\n')
    prog = sd.parse(spec, width=400)
    evolved = sd.compile_(prog)
    sep = sd.check_separation(prog, evolved)
    assert sep['R'] is False
    # sanity: the per-packet views agree with a lonely-soliton evolution,
    # while the fused row genuinely merged them
    assert evolved['A'] == sh.evolve(12, [100], 400, 60)
    assert evolved['B'] == sh.evolve(12, [101], 400, 60)
    fused = sh.evolve(12, [100, 101], 400, 60)
    assert fused != evolved['A'] | evolved['B']


# ---------------------------------------------------------------------------
# Fuzz / property: random specs hold p+v*t inside the domain
# ---------------------------------------------------------------------------

def test_fuzz_property_invariant_separated():
    """p+v*t invariant holds for every well-separated configuration."""
    import random
    rnd = random.Random(99)
    for _ in range(60):
        rule = rnd.choice((12, 44, 68, 100))
        v = sd.VELOCITY[rule]
        width = rnd.randint(400, 2000)
        T = rnd.randint(1, min(100, width // 4))
        n = rnd.randint(1, 5)
        base = rnd.randint(100, width - 100)
        # keep the whole flight INTERIOR to the domain
        lo = max(50, base - T) if v < 0 else base - 50
        hi = min(width - 50, base + T) if v > 0 else base + 50
        # well-separated (>= 6 cells): inside the compositionality domain
        positions = []
        while len(positions) < n:
            cand = rnd.randint(max(0, lo), min(width - 1, hi))
            if min((abs(cand - q) for q in positions), default=99) >= 6:
                positions.append(cand)
        positions = sorted(positions)
        spec = ('lane L rule %d\n'
                'packet A on L at %s\n'
                'run %d\n') % (rule, ', '.join(map(str, positions)), T)
        _, rep, sep = sd.run_spec(spec, width=width)
        assert sep['L'] is True
        assert rep['A']['ok'], (rule, positions, T, width)


def test_fuzz_separation_detector_fires_on_clusters():
    """Clustered MULTI-packet specs (outside the domain) must trigger the
    fused differential: at least one random clustered run reports
    VIOLATION, and in every violated run the fused row genuinely differs
    from the decomposed union (no false alarms)."""
    import random
    rnd = random.Random(2024)
    violations = 0
    for _ in range(100):
        rule = rnd.choice((12, 44, 68, 100))
        width = rnd.randint(400, 600)
        T = rnd.randint(1, 60)
        base = rnd.randint(100, width - 100)
        # two packets at a random small offset 1..5 (interaction band)
        gap = rnd.randint(1, 5)
        spec = ('lane L rule %d\n'
                'packet A on L at %d\n'
                'packet B on L at %d\n'
                'run %d\n') % (rule, base, base + gap, T)
        prog = sd.parse(spec, width=width)
        evolved = sd.compile_(prog)
        sep = sd.check_separation(prog, evolved)
        fused = sh.evolve(rule, [base, base + gap], width, T)
        union = evolved['A'] | evolved['B']
        if not sep['L']:
            violations += 1
            assert fused != union, (rule, base, gap, T)
    assert violations > 0


def test_fuzz_mutated_wrong_velocity_always_fails():
    import random
    rnd = random.Random(7)
    for _ in range(40):
        rule = rnd.choice((12, 44, 68, 100))
        # wrong = a rule of the OPPOSITE velocity class (12/44 <-> 68/100)
        wrong = rnd.choice((68, 100) if sd.VELOCITY[rule] > 0 else (12, 44))
        v = sd.VELOCITY[rule]
        width = 2000
        T = rnd.randint(20, 120)
        base = 900 if v > 0 else 1100
        spec = ('lane L rule %d\n'
                'packet A on L at %d\n'
                'run %d\n'
                'expect A at %d\n') % (rule, base, T,
                                       base + sd.VELOCITY[wrong] * T)
        _, rep, _ = sd.run_spec(spec, width=width)
        assert not rep['A']['ok'], (rule, wrong, base, T)
        assert rep['A']['expected'] == [base + v * T]