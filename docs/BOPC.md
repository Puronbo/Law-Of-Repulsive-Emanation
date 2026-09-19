# BOPC — Bandwidth-Optimal Performance Contract (ticket, application lane)

- **Status:** OPEN (first filed on this lane; previously only a
  conversation-level plan)
- **Lane:** application (NOT the sealed soliton register; nothing here is
  load-bearing for it)
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

## 6. Open questions (must be answered before build)

- Resource unit per candidate experiment (which existing experiment
  first)?
- Corpus size and seed policy for the fixed corpus.
- Who owns monitoring when a bound is exceeded (alert vs gate).

## 7. Honest boundary

This ticket is filed but not built. Building it is a real, bounded task
that requires the two decisions in section 6; until then this ticket
carries no measurement and no result claim.