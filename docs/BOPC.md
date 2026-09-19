# BOPC — Bandwidth-Optimal Performance Contract (ticket, application lane)

- **Status:** BUILT v1 (2026-09-19) — contract runs and gates; decisions
  in section 6 and build record in section 8. Application lane only
  (NOT the sealed soliton register; nothing here is load-bearing for it)
- **Owner:** lane owner
- **Reporter:** assistant (filing the ticket that was never written down)

## 1. Context

Across several experiments in this repository, a subroutine can be
configured for either correctness-complete or resource-bounded behavior.
There is no repository-wide, machine-checked way to state *how much
bandwidth/CPU/energy a call may consume while still guaranteeing the
contractual result*. Each experiment re-invents its own budget, so there
is no single contract a caller can rely on.

## 2. Problem statement (the contract BOPC would define)

For a given operator `f : inputs -> outputs`, declare, in machine-checked
form, a contract `C(f)` with a *bandwidth bound* `B(f)` such that:
- any call of `f` uses at most `B(f)` of a declared resource (frames,
  cells, comparisons, Joules — the resource is part of the contract), and
- every accepted input either yields the declared output or raises a
  declared failure value; it never silently degrades.
The point is *not* to maximize speed; it is to make an objectively
verifiable upper bound part of the same artifact as correctness.

## 3. Constraints

- Must be single-claim, honest: any bound must be measured or derived,
  never assumed (register philosophy applies even though this is the
  application lane).
- Must not touch the register's pinned counts (125 certificates / 89
  validators).
- First candidate cases suggested by existing code: the wolfram/ECA
  rule-step loops in the soliton lane and the transformed loops in the
  application lane; keep BOPC scoped to ONE reproducible experiment per
  contract at first.

## 4. Proposed contract shape (draft, NOT final)

    BOPC v1 = record {
      operator: string;
      resource: "frames" | "cells" | "comparisons" | "joules";
      upper_bound: nat;      (* closed, integer *)
      unit_invariant: bool;  (* proven/non-`False`, asserted honestly *)
      measurer: path;        (* a real, runnable probe; not a claim *)
      semantics: "correct-or-raise";
    }

No bound may be recorded without the measurer having run and the
`upper_bound` having been observed (not imagined).

## 5. Acceptance criteria

- A `scripts/bopc.py` (or `experiments/bopc/` module) can read a BOPC
  contract file, run the referenced measurer over a fixed seed corpus,
  and exit 0 only if every measured resource usage `<= upper_bound` for
  every token in the corpus and the semantic output is byte-identical to
  the declared output.
- An honest markdown example contract exists for exactly one operator.
- Zero claims of bandwidth-optimality for anything not measured.

## 6. Open questions — RESOLVED (2026-09-19)

1. **Resource unit / first candidate.** DECIDED: resource = `comparisons`;
   first operator = the Wolfram ECA 3-neighborhood step over a byte ring
   (`experiments/bopc_candidate.py`, `eca_step`), the candidate named in
   section 3. Bound is derived, not assumed: the counted implementation
   performs at most 8 counted operations per cell plus one final loop
   compare, so `comparisons <= 8*n + 2` for length n (closed, integer).
2. **Corpus size and seed policy.** DECIDED: frozen corpus of 640 tokens —
   seeds 0..63, cell sizes {8,16,32,64,128}, rules {30,110} — cells drawn
   from `random.Random(seed)` (deterministic, no clock, no network). The
   corpus spec lives in `experiments/bopc_contract.json` and is byte-frozen;
   any change is a new contract revision.
3. **Monitoring owner.** DECIDED: the application-lane owner. BOPC
   self-gates: `scripts/bopc.py` exits non-zero on any bound violation or
   semantic mismatch, and that non-zero exit is hoisted as the lane alert.
   BOPC must never touch the soliton register's pinned counts.

## 7. Honest boundary

This ticket was filed, then built (v1) under the three decisions above.
No bandwidth-*optimality* is claimed for anything not measured; the
contract asserts only a proven upper bound that the runner observed.
`scripts/bopc.py` is application-lane only.

## 8. Build record (v1, 2026-09-19)

- `scripts/bopc.py` reads `experiments/bopc_contract.json`, builds the
  640-token corpus deterministically, runs the counted operator and an
  independent reference, and exits 0 only if every token is byte-identical
  to the reference and `count <= 8*n + 2`.
- Observed: **640/640 tokens pass; measured max comparisons = 1025 at
  n = 128, bound = 1026; exit 0.** No register count touched.

- **Candidate #2 (2026-09-19):** `experiments/bopc_contract2.json` —
  Selection sort on 8 elements, resource=comparisons, proven bound
  n*(n-1)/2 = 28. Corpus: 256 tokens (seeds 0..255, fixed n=8).
  Observed: **256/256 tokens pass; measured max = 28, bound = 28; exit 0.**