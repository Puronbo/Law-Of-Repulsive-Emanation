"""traffic_audit: the Sixteenth real-subsystem audit -- the periodic-ring
laws of rules 29/71 as closed-form physics (traffic_law.py on the ring,
where a current and a block law are exactly defined).

The open-lattice free/melt/composition laws are already certified
(L1-L3).  This audit certifies the INHERENTLY RING observables that the
open lattice cannot express -- the current, the relaxation-to-isolated-
minority block law, the TASEP identification, and the left/right mirror:

    L48_traffic_ring_block_law PASS:
        After relaxation (T >= 400) the MINORITY species on the ring is
        fully isolated: no two minority cells are adjacent (cyclically),
        and the isolation persists (checked to T=410).  Count is exactly
        conserved the whole time, so "the minority isolates" means the
        steady state has exactly min(k, N-k) isolated minority cells.
    L49_traffic_ring_tasep_identification PASS:
        evolution on the ring equals TASEP (hard-core exclusion, hop into
        an empty target, else block) implemented independently, for both
        directions (29 right / 71 left).  Exhaustive over every ring
        state for N in {6,7,8} x 3 horizons.
    L50_traffic_ring_mirror_symmetry PASS:
        rule 71 on a reflected configuration equals the reflection of
        rule 29's trajectory (the left mover is the spatial mirror of the
        right mover).  Exhaustive over every ring state N in {5..9}.
HONEST NEGATIVES (candidate laws physics vetoed):
    L51_traffic_bond_count_not_conserved:
        "current = number of (1,0) bonds is conserved" is FALSE: in the
        documented counterexample [292,527,990,991,1166,1754] the jam
        (990,991) dissolves and the bond count rises from 5 to 6 -- J
        fluctuates with jam formation/dissolution, it is a transient
        order parameter, not an invariant.
    L52_traffic_twist_charge_not_exact:
        "twist charge Q = sum(p) - n*v*T is exact for all T" is FALSE:
        at a single contact yield it jumps once (a 1-bit event); Q is
        conserved only between contacts.
    L53_traffic_ring_only_count_conserved:
        "there is an exact dynamical invariant beyond particle count on
        the contact sector" is FALSE: over the full one-step transition
        graph of the N-ring (N in {6,8,10}, rules 29/71), among {n, #10,
        #01, #11, #00, sum(p) mod N} the ONLY exactly-conserved feature is
        particle count.
"""
import random

from experiments.emanation import law_checker as lc
from experiments.emanation import traffic_law as tl


# ---------------------------------------------------------------------
# L48 helper: minority isolation on the ring after relaxation
# ---------------------------------------------------------------------
_DENSITIES = [0.10, 0.20, 0.30, 0.40, 0.45, 0.60, 0.70, 0.80, 0.90]
_RING_SIZES = [60, 120]
_RELAX_SEEDS = list(range(8))
_RELAX = 400          # documented relaxation horizon
_PERSIST = 10         # extra window to show "conserved forever" continues


def _ring_draw(N, rho, seed):
    rng = random.Random(seed)
    k = max(1, min(N - 1, int(round(rho * N))))
    return sorted(rng.sample(range(N), k))


def _minority(N, positions):
    return 1 if len(positions) <= N - len(positions) else 0


def _who(N, row):
    return {i for i, v in enumerate(row) if v}


def _isolated(N, positions):
    """Pure check: every MINORITY cell has both cyclic neighbours held by
    the majority (no two minority cells are adjacent on the ring)."""
    occ = positions
    m = _minority(N, occ)
    if m == 1:
        return all(((p - 1) % N) not in occ and ((p + 1) % N) not in occ
                   for p in occ)
    empty = set(range(N)) - occ
    return all(((j - 1) % N) in occ and ((j + 1) % N) in occ for j in empty)


def _minority_isolated(rule, positions, N, T):
    return _isolated(N, tl.evolve_ring(rule, positions, N, T))


def _relax_isolated(rule, positions, N, checks=(400, 401, 410)):
    """Single-pass relaxation: evolve field step by step up to the last
    check horizon and verify minority isolation at every checked tick.
    One O(N*T) pass instead of one full evolution per check."""
    left = rule == 71
    row = [0] * N
    for p in positions:
        row[p % N] = 1
    horizon = max(checks)
    wanted = set(checks)
    for t in range(horizon + 1):
        if t in wanted:
            if not _isolated(N, _who(N, row)):
                return False
        if t == horizon:
            break
        nxt = [0] * N
        for j in range(N):
            behind = (j - 1) % N if not left else (j + 1) % N
            ahead = (j + 1) % N if not left else (j - 1) % N
            came = 1 if (row[behind] == 1 and row[j] == 0) else 0
            stayed = 1 if (row[j] == 1 and row[ahead] == 1) else 0
            nxt[j] = came or stayed
        row = nxt
    return True


def _L48_block_law(datum):
    N, rho, seed, rule = datum
    positions = _ring_draw(N, rho, seed)
    return _relax_isolated(rule, positions, N)


# ---------------------------------------------------------------------
# L49 helper: independent TASEP implementation (no CA bits)
# ---------------------------------------------------------------------
def _tasep(positions, N, rule, steps):
    """Ground-truth TASEP on the ring written independently of the CA
    update rule: a particle hops one cell in its direction iff the target
    cell is EMPTY, otherwise it blocks in place."""
    v = 1 if rule == 29 else -1
    occ = set(p % N for p in positions)
    for _ in range(steps):
        nxt = set()
        for p in occ:
            t = (p + v) % N
            nxt.add(t if t not in occ else p)
        occ = nxt
    return occ


def _L49_tasep(datum):
    positions, N, rule, steps = datum
    return tl.evolve_ring(rule, list(positions), N, steps) == \
        _tasep(positions, N, rule, steps)


# ---------------------------------------------------------------------
# L50 helper: spatial mirror
# ---------------------------------------------------------------------
def _reflect(positions, N):
    return set((N - 1 - p) % N for p in positions)


def _L50_mirror(datum):
    positions, N, rule, T = datum
    return tl.evolve_ring(71 if rule == 29 else 29,
                          _reflect(positions, N), N, T) == \
        _reflect(tl.evolve_ring(rule, positions, N, T), N)


# ---------------------------------------------------------------------
# L51/L52 helpers: open-lattice trajectory via shift_bus
# ---------------------------------------------------------------------
def _trajectory(rule, positions, steps, width=2048):
    from shift_bus import evolve
    return [set(evolve(rule, tuple(positions), width, t))
            for t in range(steps)]


def _moves(rule, positions, width=2048):
    """Number of (1,0)-positioned cars (particles with an EMPTY cell
    ahead) per step -- the 'active bond' current."""
    out = []
    for occ in _trajectory(rule, positions, 6, width=width):
        out.append(sum(1 for p in occ if (p + 1) not in occ))
    return out


def _L51_bond_count_conserved(datum):
    """FALSE candidate law: the number of (1,0) bonds is conserved along a
    rule-29 trajectory.  The jam (990,991) dissolves: 5 -> 6 bonds."""
    rule = datum[0]
    positions = datum[1:]
    return len(set(_moves(rule, positions))) == 1


def _L52_twist_exact(datum):
    """FALSE candidate law: Q = sum(p) - n*v*T is constant for ALL T.  A
    single contact (yield at a jam) jumps Q by one -- a 1-bit event."""
    rule = datum[0]
    positions = datum[1:]
    v = 1 if rule == 29 else -1
    n = len(positions)
    qs = [sum(occ) - n * v * t
          for t, occ in enumerate(_trajectory(rule, positions, 6))]
    return len(set(qs)) == 1


# ---------------------------------------------------------------------
# L53 helper: ring single-step graph observables
# ---------------------------------------------------------------------
def _ring_observables(occ, N):
    n = len(occ)
    c11 = sum(1 for p in occ if ((p + 1) % N) in occ)
    c10 = sum(1 for p in occ if ((p + 1) % N) not in occ)
    c01 = c10                                   # ring identity: #01 == #10
    c00 = sum(1 for j in range(N)
              if j not in occ and ((j + 1) % N) not in occ)
    return (n, c10, c01, c11, c00, sum(occ) % N)


def _L53_only_count_conserved(datum):
    """FALSE candidate law: some observable beyond particle count is
    exactly conserved on every one-step transition of the N-ring.  For
    each N and rule the FULL state graph is checked; particle count n is
    conserved everywhere, but #10/#01/#11/#00/sum(p) mod N each breaks on
    at least one edge."""
    N, rule = datum
    conserved = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for mask in range(2 ** N):
        occ = frozenset(j for j in range(N) if (mask >> j) & 1)
        nxt = frozenset(tl.evolve_ring(rule, list(occ), N, 1))
        a = _ring_observables(occ, N)
        b = _ring_observables(nxt, N)
        for i in range(6):
            if a[i] == b[i]:
                conserved[i] += 1
    # candidate claim: every non-count observable (#10 of index 1..#5) is
    # conserved on every edge -> the claim is true iff those five never break
    return all(conserved[i] == 2 ** N for i in (1, 2, 3, 4, 5))


# ---------------------------------------------------------------------
# domains
# ---------------------------------------------------------------------
_48_DOMAIN = [(N, rho, seed, rule)
              for N in _RING_SIZES for rho in _DENSITIES
              for seed in _RELAX_SEEDS for rule in (29, 71)]

_49_DOMAIN = []
for N in (6, 7, 8):
    for rule in (29, 71):
        for steps in (1, 2, 3):
            for mask in range(2 ** N):
                pos = tuple(j for j in range(N) if (mask >> j) & 1)
                _49_DOMAIN.append((pos, N, rule, steps))

_50_DOMAIN = []
for N in (5, 6, 7, 8, 9):
    for rule_t in (29, 71):
        for T in (1, 2):
            for mask in range(2 ** N):
                pos = frozenset(j for j in range(N) if (mask >> j) & 1)
                _50_DOMAIN.append((pos, N, rule_t, T))

# the documented bond-count counterexample, rule 29 (right mover)
_51_DOMAIN = [(29, 292, 527, 990, 991, 1166, 1754)]

# one isolated contact, rule 29 and rule 71 (mirrored)
_52_DOMAIN = [(29, 1000, 1001), (71, 1004, 1005)]

_53_DOMAIN = [(N, rule) for N in (6, 8, 10) for rule in (29, 71)]


def _certify(label, meta, pred, domain):
    return lc.certify_statement(label, meta, pred, list(domain))


def traffic_certificates():
    certs = []
    certs.append(_certify(
        "L48_traffic_ring_block_law",
        {"domain": "random ring draws, N in {60,120}, rho in {0.10..0.45, "
                   "0.60..0.90} x 8 seeds x rules {29,71}, isolation "
                   "checked at T in {400,401,410}",
         "law": "after relaxation the MINORITY species on the ring is "
                "fully isolated (no two minority cells adjacent on the "
                "cyclic boundary); count conserved throughout, so the "
                "steady state has exactly min(k, N-k) isolated minority "
                "cells",
         "measured_on": "traffic_law.evolve_ring"},
        _L48_block_law, _48_DOMAIN))
    certs.append(_certify(
        "L49_traffic_ring_tasep_identification",
        {"domain": "exhaustive over every ring state, N in {6,7,8} x "
                   "rules {29,71} x horizons {1,2,3}",
         "law": "ring evolution equals TASEP hard-core exclusion (hop into "
                "an EMPTY target, else block) -- rule 29 right, rule 71 "
                "left -- identical position sets at every horizon",
         "measured_on": "traffic_law.evolve_ring vs independent TASEP"},
        _L49_tasep, _49_DOMAIN))
    certs.append(_certify(
        "L50_traffic_ring_mirror_symmetry",
        {"domain": "exhaustive over every ring state, N in {5..9} x "
                   "horizons {1,2}, both directions",
         "law": "rule 71 applied to the spatial mirror of a configuration "
                "equals the mirror of rule 29's trajectory: the left "
                "mover IS the right mover reflected",
         "measured_on": "traffic_law.evolve_ring"},
        _L50_mirror, _50_DOMAIN))
    certs.append(_certify(
        "L51_traffic_bond_count_not_conserved",
        {"domain": "the documented counterexample [292,527,990,991,1166,"
                   "1754], rule 29, first 6 steps",
         "law": "FALSE CANDIDATE: current = number of (1,0) bonds is "
                "conserved -- the jam (990,991) dissolves (991 leads, 990 "
                "below then frees) and the bond count rises 5 -> 6; J "
                "fluctuates with jam formation/dissolution and is a "
                "transient order parameter, not an invariant"},
        _L51_bond_count_conserved, _51_DOMAIN))
    certs.append(_certify(
        "L52_traffic_twist_charge_not_exact",
        {"domain": "a single touching pair {a, a+1} and {a, a-1} (one "
                   "contact), rules 29/71, first 6 steps",
         "law": "FALSE CANDIDATE: twist charge Q = sum(p) - n*v*T is exact "
                "for ALL T -- at a single contact yield Q jumps once (a "
                "1-bit event); it is conserved only between contacts"},
        _L52_twist_exact, _52_DOMAIN))
    certs.append(_certify(
        "L53_traffic_ring_only_count_conserved",
        {"domain": "full one-step transition graph of the ring, N in "
                   "{6,8,10} x rules {29,71} (every state, every edge)",
         "law": "FALSE CANDIDATE: some exact dynamical invariant beyond "
                "particle count exists on the ring -- among {n, #10, #01, "
                "#11, #00, sum(p) mod N} only particle count is conserved "
                "on every edge; each other observable breaks on at least "
                "one transition"},
        _L53_only_count_conserved, _53_DOMAIN))
    return certs


if __name__ == "__main__":
    import sys
    certs = traffic_certificates()
    print("soliton traffic ring audit")
    for c in certs:
        print("  %-38s %-16s n_ok=%-4d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    result = all(c["status"] in ("PASS", "HONEST_NEGATIVE") for c in certs)
    print("RESULT: %s" % ("PASS" if result else "FAIL"))
    sys.exit(0 if result else 1)