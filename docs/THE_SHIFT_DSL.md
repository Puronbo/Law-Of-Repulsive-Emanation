# The Shift-DSL: a verified shift-spec language

`shift_dsl.py` is a tiny line-based language whose *semantics are the exact
soliton-transport invariant* of `shift_bus.py`.  It is a **specification /
delay-line layout language, not a programming language**: no branching, no
composition of interacting signals, no stored state beyond position, no
unbounded loops.  What it offers instead is a by-construction guarantee
about where bits land.

## Grammar

    lane <name> rule <12|44|68|100>     # declare a direction lane
    packet <name> on <lane> at <p,p,...>
    run <t>                             # synchronous steps
    expect <name> at <p,p,...>          # optional, enforced by verify()
    # comment

All tokens are whitespace-tolerant (`packet A on L at 1,2` and
`packet A   on  L  at 1, 2` are the same spec).

## What is verified, and how

1. **Head-landing law.** Every bit placed at position `p` on a lane of
   velocity `v in {+1, -1}` has its head land at **exactly** `p + v*t`.
   `verify()` recomputes this *independently of the simulation* (it never
   inspects `evolve`'s intermediate steps) and requires the evolved read-out
   to equal it.  The period-2 rules (44/100) legitimately alternate between
   a single cell and a 2-cell blob `{head, head - v}`; both forms are
   accepted.
2. **Open-boundary honesty.** Bits that exit `[0, width)` fall off the open
   lattice and are dropped.  `verify()` clips expected landings to the
   domain and flags boundary-affected packets, so an exit is never reported
   as a corrupt read-out and there is no wraparound.
3. **Separation precondition, machine-checked.** Packets on one lane are
   compiled per-packet, which is compositional *only while their evolving
   supports stay disjoint*.  `check_separation()` runs a fused-lane
   differential: it evolves the union of all same-lane packets in one row
   and requires the result to equal the disjoint union of the per-packet
   evolutions.  Any difference is reported as the lane's separation being
   VIOLATED.  This is the tool's real safety-check: per-packet verification
   cannot see an interaction, the fused differential can.
4. **Expect clauses.** Any declared `expect <name> at ...` must equal the
   actual read-out set exactly, or `verify()` reports a mismatch.

## Ground truth independent of the engine

The test suite carries a second, structurally independent simulator
(`oracle_evolve`), written from a standard-Wolfram neighborhood digit
`4L + 2C + R` with a bit-reversed rule number (shift_bus indexes its `_NEI`
tuple in the reversed order).  A 256-rule x 8-neighborhood pinning test
proves the two simulators agree on every truth-table cell, so `verify()`'s
"independent recomputation" is not reading the engine's own opinion.  The
DSL pipeline is additionally fuzzed: random well-separated specs must hold
the landing law, and random clustered multi-packet specs must trigger the
separation detector (with no false alarms).

## Honest limits

- **Not linear, not Turing-complete.** The rules are AND-NOT gates; XOR
  superposition holds only for disjoint supports (verified: fails on dense
  configs).  Nothing here computes.
- **Separation is required.** Packets that drift within interaction range
  (rule 12/44: gap < 2, rule 68/100: gap < 3 for lone cells) break
  compositionality.  `verify()` will *not* catch this on its own — only
  `check_separation()` does.
- **Noise-fragile.** The exact law assumes error-free evolution; any
  per-step bit flip destroys it (measured: ~0 Jaccard fidelity at 5%
  noise/step).  Do not use this for anything that needs robustness.
- **Boundary flight is only partially pinned.** A boundary-affected packet
  keeps the clipped agreement, but we do not assert anything deeper about
  its trajectory near the edge.

## This is NOT the internet (and never will be)

Honest, test-pinned reasons this is a delay-line abstraction and not a
packet network:

- **No routing.** A lane's direction is bound at parse time; the grammar has
  no mid-flight redirect clause (`route`/`redirect`/`then` raise
  `SpecError`).  No routing table, no adaptivity.
- **No content / no payload.** A cell holds exactly one bit.  Two packets
  co-located at one position are one bit — no header, no identifier, no
  payload.  Read-out is a pure function of *positions* (rename- and
  colocation-invariance are tested).  The internet distinguishes packets by
  headers; here only position distinguishes bits.
- **Collision destroys information.** Closing to gap 1 fuses two bits into
  one; the input->output map is non-injective, so no scheme can recover
  which original packet carried what.  No error detection, no redundancy,
  no retransmission exists under any configuration.
- **Errors are permanent.** Injected cells are themselves stable solitons
  and persist forever; there is no correction or repair mechanism.  Measured
  5%/step noise collapses Jaccard fidelity to ~0.
- **Tiny capacity.** Separation-limited bandwidth: 0.5 bits/cell/lane/step
  for single-cell movers (12/68), 0.25 for blob movers (44/100) — a hard,
  verified ceiling.

The internet's defining properties — routing, content addressing, error
control, redundancy, a protocol stack, hop-by-hop recovery, adaptivity —
are each either absent or actively forbidden here.  Its honest use is a
deterministic, verified delay line and shift-spec DSL, not a network
substrate.

## Could a language change make it do other things? (structural answer)

Three frontiers, two of them *structurally closed*:

1. **Collision-based logic: IMPOSSIBLE (verified).** Billiard-ball /
   Fredkin-Toffoli / glider-collision computation requires *elastic*
   deflection — particles interact but survive, exchanging trajectory.
   The full collision census over all 4 rules and all gaps gives exactly
   two outcomes and **never** deflection:
       PASS   (gap >= 2: separation preserved, pure pass-through, NO device)
       MERGE  (gap 1 or blob phase: two bits fuse into one, irreversible)
   A `DEFLECT` outcome is the precondition for any collision-made gate, and
   it does not exist here.  So no amount of grammar change can build logic
   from particle interactions — the physics forbids the gate itself.
2. **Computation / universality: IMPOSSIBLE (previously verified).** The
   rules are non-linear AND-NOT gates with no compositionality except on
   disjoint supports, no self-repair, no routing.  Constitutionally a delay
   line, not a computer.
3. **Language extensions that DO mean something** (all honest, added in
   v2): the DSL can grow in *specification power* without inventing new
   physics — richer invariants (compositionality preconditions), larger
   multi-lane topologies, machine-checked routing *declarations* (as a
   static, verified bookkeeping task, NOT adaptive routing), and
   boundary/bookkeeping conveniences.  These make the delay-line more
   usable as a verified spec tool; they cannot make it a computer, network,
   or universal automaton.

The decisive test is `test_full_collision_census_never_deflects`.

## Test evidence (tests/test_shift_dsl.py)

- Truth-table pinning: oracle == engine for all 256 rules x 8 neighborhoods.
- Landing law, all four rules, at t = 200.
- Wrong-velocity expect clauses FAIL verify; a fake (broken) engine is
  rejected.
- Multi-packet same-lane bus: separation OK and law holds.
- Interacting gap: separation VIOLATED, fused row genuinely differs.
- Boundary: no wraparound; exits drop; boundary-affected packets flagged.
- Fuzz: 60 well-separated specs hold the law; 100 clustered specs trigger
  the detector (>= 1 violation, no false alarms); 40 mutated velocities
  always fail.
- Not-an-internet properties: routing clauses are SpecError; co-located and
  renamed packets carry no content; collision is non-injective; injected
  errors persist with no correction; capacity ceiling (0.5 / 0.25
  bits/cell/lane/step) is exact over a long horizon and the blob rules are
  shown NOT to reach the single-cell ceiling.