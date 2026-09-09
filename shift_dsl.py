"""shift_dsl: a minimal verified shift-spec language for the 4-rule soliton bus.

A PROGRAM is a text spec declaring lanes, packets, and a run time.  The
semantics are pure synchronous shift/delay: a bit placed at position p on
lane velocity v lands with its HEAD at EXACTLY p + v*t (v in {+1,-1}),
machine-verified in shift_bus.  compile() places and evolves; verify()
recomputes every bit's expected landing independently and checks the
evolved read-out against it.

This is a SPEC language, not a programming language: no branching, no
composition of interacting signals, no stored state beyond position.

Syntax (line based):
    lane <name> rule <12|44|68|100>
    packet <name> on <lane> at <p[,p,...]>
    run <t>
    expect <name> at <p[,p,...]>          # optional: checked by verify
    # ^ comment
"""

import re

import shift_bus as sb

VELOCITY = {12: +1, 44: +1, 68: -1, 100: -1}


class SpecError(ValueError):
    pass


def parse(spec, width=6000):
    """Parse a spec text into a dict of parts (no evolution yet)."""
    lines = [ln.split('#', 1)[0].strip() for ln in spec.splitlines()]
    lines = [ln for ln in lines if ln]
    lanes = {}
    packets = {}
    expect = {}
    T = None
    for ln in lines:
        m = re.match(r'^lane\s+(\w+)\s+rule\s+(12|44|68|100)$', ln)
        if m:
            name, rule = m.group(1), int(m.group(2))
            lanes[name] = {'rule': rule, 'velocity': VELOCITY[rule]}
            continue
        m = re.match(r'^packet\s+(\w+)\s+on\s+(\w+)\s+at\s+([\d,\s]+)$', ln)
        if m:
            name, lane, poss = m.group(1), m.group(2), m.group(3)
            if lane not in lanes:
                raise SpecError('packet %s: unknown lane %r' % (name, lane))
            if name in packets:
                raise SpecError('duplicate packet %r' % name)
            packets[name] = {'lane': lane,
                             'positions': [int(p) for p in poss.split(',')]}
            continue
        m = re.match(r'^run\s+(\d+)$', ln)
        if m:
            T = int(m.group(1))
            continue
        m = re.match(r'^expect\s+(\w+)\s+at\s+([\d,\s]+)$', ln)
        if m:
            name, poss = m.group(1), m.group(2)
            expect[name] = [int(p) for p in poss.split(',')]
            continue
        raise SpecError('unrecognized line: %r' % ln)
    if T is None:
        raise SpecError('missing "run <t>"')
    if not lanes:
        raise SpecError('no lanes declared')
    if not packets:
        raise SpecError('no packets declared')
    return {'lanes': lanes, 'packets': packets, 'expect': expect,
            'time': T, 'width': width}


def compile_(prog):
    """Place all packets, evolve for run-time; return {name: set(positions)}."""
    res = {}
    for name, pkt in prog['packets'].items():
        rule = prog['lanes'][pkt['lane']]['rule']
        res[name] = sb.evolve(rule, pkt['positions'], prog['width'],
                              prog['time'])
    return res


def expected_heads(prog):
    """Independently recompute each bit's HEAD landing: p + v*t.

    Open boundaries drop cells that exit [0, width): the honest semantics is
    that such cells are unobservable.  Heads landing outside the domain are
    therefore clipped away here; trailing blob cells that fall out of the
    lattice are likewise dropped by _allowed_landing.  Packets whose whole
    trajectory touches the boundary are flagged 'boundary-affected' by
    verify() -- for them only the clipped agreement is asserted.
    """
    res = {}
    for name, pkt in prog['packets'].items():
        v = prog['lanes'][pkt['lane']]['velocity']
        ws = prog['width']
        res[name] = sorted(h for h in (p + v * prog['time']
                                       for p in pkt['positions'])
                           if 0 <= h < ws)
    return res


def _allowed_landing(heads, v, width):
    """Allowed read-outs: one cell per head, or the period-2 tail variant.

    Rules 44/100 alternate between a single cell and a 2-cell blob; the tail
    sits at head - v on the +1/-1 lanes respectively.  Rules 12/68 are pure
    single cells, but accepting the blob form is safe: it never occurs for
    them.  Allow {heads} or {heads} with each head possibly gaining a tail;
    any cell outside [0, width) fell off the open boundary and is dropped.
    """
    s1 = set(heads)
    s2 = set(heads) | {h - v for h in heads}
    dom = lambda c: 0 <= c < width
    return {c for c in s1 if dom(c)}, {c for c in s2 if dom(c)}


def boundary_affected(prog):
    """Packets whose trajectory scrapes the lattice edge are 'boundary-affected'.

    A cell's occupied band along the flight: for v=+1 the leftmost cell is
    p (single) down to head-1 (blob tail), so the band is
    [p-1 .. p+t]; for v=-1 the band is [p-t-... ].  If any part of the
    union of occupied cells over the t steps leaves [0, width), the packet
    clips the open boundary and its flight is not the perfect-invariant
    case (the head-landing law is asserted only for interior flights).
    """
    res = {}
    T = prog['time']
    for name, pkt in prog['packets'].items():
        v = prog['lanes'][pkt['lane']]['velocity']
        affected = False
        for p in pkt['positions']:
            for m in range(T + 1):
                low = p + v * m - (1 if v > 0 else 0)
                high = p + v * m + (1 if v < 0 else 0)
                if low < 0 or high >= prog['width']:
                    affected = True
                    break
            if affected:
                break
        res[name] = affected
    return res


def verify(prog, evolved=None):
    """Check the by-construction invariant AND any declared expect clauses.

    Invariant: head of every bit lands exactly at p + v*t, with out-of-domain
    cells dropped by the open boundary.  Boundary-affected packets are
    annotated (only clipped agreement is meaningful for them).  Any 'expect
    <name> at ...' line must match the actual read-out set exactly.
    Returns {name: {'ok': bool, 'expected': [...], 'actual': [...],
    'detail': str}}.
    """
    if evolved is None:
        evolved = compile_(prog)
    heads = expected_heads(prog)
    affected = boundary_affected(prog)
    report = {}
    for name, want in heads.items():
        v = prog['lanes'][prog['packets'][name]['lane']]['velocity']
        got = sorted(evolved[name])
        s1, s2 = _allowed_landing(want, v, prog['width'])
        ok = set(got) in (s1, s2)
        note = ''
        if name in prog['expect']:
            want_cls = sorted(set(prog['expect'][name]))
            if set(want_cls) != set(got):
                ok = False
                note = ' expect-clause %s MISMATCH' % want_cls
        if affected[name]:
            note += ' boundary-affected'
        report[name] = {
            'ok': ok,
            'expected': sorted(set(want)),
            'actual': got,
            'boundary_affected': affected[name],
            'detail': 'heads %s -> actual %s%s%s' % (
                sorted(set(want)), got, '' if ok else '  MISMATCH', note),
        }
    return report


def check_separation(prog, evolved=None):
    """Machine-check the lane-sharing precondition by a fused-lane differential.

    Packets on the same lane are compiled per-packet, which is compositional
    ONLY while their evolving supports stay disjoint.  Ground truth: place
    all same-lane packets into ONE row and evolve once; the read-out must
    equal the disjoint union of the per-packet reads.  Any difference is a
    separation violation.  Returns {lane: bool}.
    """
    if evolved is None:
        evolved = compile_(prog)
    from collections import defaultdict
    per_lane = defaultdict(list)
    for name, pkt in prog['packets'].items():
        per_lane[pkt['lane']].append(name)
    out = {}
    for lane, names in per_lane.items():
        rule = prog['lanes'][lane]['rule']
        fused = sb.evolve(rule,
                          [p for n in names for p in
                           prog['packets'][n]['positions']],
                          prog['width'], prog['time'])
        union = set().union(*(evolved[n] for n in names))
        out[lane] = (fused == union)
    return out


def run_spec(spec, width=6000):
    """One-shot: parse + compile + verify + separation-check.

    Returns (evolved, report, separation)."""
    prog = parse(spec, width)
    evolved = compile_(prog)
    report = verify(prog, evolved)
    separation = check_separation(prog, evolved)
    return evolved, report, separation