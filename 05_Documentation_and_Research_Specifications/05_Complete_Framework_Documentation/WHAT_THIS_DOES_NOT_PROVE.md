# What this repository does *not* prove

**Status: scope boundary.** This file is the single honest line between what the
repository *checks* and what it *narrates*. Every other document in the project
is subordinate to it: where a narrative and this boundary disagree, this boundary
wins.

## No Millennium problem is settled here

The seven Clay Millennium Prize Problems are **not solved, not proved, and not
settled by this project**. `PunoCalculus.MillenniumBridge` records exactly this:
each of the seven carries the status `NOT SETTLED BY THIS PROJECT`
(`MillenniumBridge.lean`, `statuses` / `seven_problems_declared_unsolved`), and
the Python meta-audit refuses any settlement phrasing that drifts into the audit
sources.

| Problem | This project's status |
|---|---|
| P vs NP (`P_NNP`) | NOT SETTLED |
| Hodge | NOT SETTLED |
| Poincaré | historically settled by Perelman (2003); **not re-proved here**, not relied on |
| Riemann hypothesis | NOT SETTLED |
| Yang–Mills existence & mass gap | NOT SETTLED |
| Navier–Stokes existence & smoothness | NOT SETTLED |
| Birch–Swinnerton-Dyer | NOT SETTLED |

Any text that reads as "we prove RH", "we solved NS", "complete proof of YM",
"rigorous proof of the mass gap", or "unifies the seven Millennium problems" is
**interpretive narrative**, not a result. Heroic status labels in older documents
(`README.md` release notes, `MILLENNIUM_PROOF.md`, `THE_*_0_OVER_0.md`,
`YANG_MILLS_MASS_GAP_PROOF.md`, the `papers/*.pdf` set) predate this boundary and
carry the *aspiration*, not a proof.

## The wall stays open

The register itself says so. In `EXPLICIT_CLAIMS.md` the honest open cards are
**C3** and **C10-open**; `CLAIM_TRACEABILITY.md` states outright "No card here is
a Millennium result; the wall stays OPEN." That sentence is authoritative.

## What *is* machine-checked

The boundary is **not** a blanket disclaimer — real, verifiable work sits inside
it. Every quoted declaration in `EXPLICIT_CLAIMS.md` is linked to a Lean artifact
by `CLAIM_TRACEABILITY.md` and checked by
`04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_claim_traceability.py`.
The axiom footprint of every quoted declaration is recorded in `AXIOM_AUDIT.md`
(all footprints ⊆ `{propext, Classical.choice, Quot.sound}`, no `sorryAx`).

The honest summary of *scope*:

- **Formal (Lean, kernel-checked):** the elementary mechanism lemmas — removable
  values, order of vanishing, polynomial root multiplicity, the categorical zero
  object, one-sided-limit non-removability of `|x|/x` (cards C15–C22), plus the
  register's earlier structural lemmas.
- **Empirical (scripts, reproducible):** numerical experiments tagged as such.
- **Interpretive / narrative (not a proof):** every claim that a Millennium
  problem, the mass gap, or a cosmological model follows from the 0/0 doctrine.

## The rule for new text

A sentence may use a settlement word ("prove", "solve", "settle", "complete
proof", "rigorous proof") **only** if, on the same line, it is negated or hedged
— e.g. "does **not** prove", "**open**", "**candidate**", "**analogy**". This is
enforced by `test_scope_boundary.py`, which scans `README.md` and this file
line-by-line and fails on any unhedged settlement claim. Adding a new heroic
claim to the front pages is now a **test failure**, not a free edit.

## Related

- `EXPLICIT_CLAIMS.md` — the falsifiable card register (source of truth).
- `CLAIM_TRACEABILITY.md` — card → Lean artifact → experiment join table.
- `AXIOM_AUDIT.md` — the axiom footprint of every quoted declaration.
- `EXTERNAL_CORPORA_CROSSWALK.md` — adjacency (not equivalence) to public corpora.
- `PunoCalculus.MillenniumBridge` — the machine-enforced non-settlement record.
