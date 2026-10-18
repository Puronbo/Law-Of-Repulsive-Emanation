# External Corpora Crosswalk — this project ↔ `openai/math`

**Status: reference map, not a dependency.** This file links this repository's
certified artifacts to the *result families* of a neighbouring public mathematical
corpus, **[`openai/math`](https://github.com/openai/math)** (the "OpenAI Mathematics
manuscript collection"). It adds an *external* axis to `CLAIM_TRACEABILITY.md`: that
file joins our cards to *our* Lean and experiments; this one joins our modules to
*their* families, so a reader can see at a glance where the two corpora touch, where
they do not, and what is — and is not — shared.

## Snapshot

| field | value |
|---|---|
| corpus | OpenAI Mathematics manuscript collection |
| repo | https://github.com/openai/math |
| catalog | `CONTENTS.md` (manuscript map); `overview.pdf` (research catalog) |
| size at snapshot | 719 manuscripts / 372 result families |
| announced | 2026-10-06 · https://openai.com/index/sharing-ai-progress-in-mathematics/ |
| Lean | `lean/formalization.yaml` + per-family `lean/docs/NNN.md` (partial, ~42%) |

**Provenance caution.** The corpus is stated to be produced by an *unreleased internal
OpenAI model*, and independent mathematical checking of the papers is, as of this
snapshot, **pending**. Quoted results below are therefore recorded as **CLAIMED**, not
established — the same status this register already assigns to an unrefereed preprint
(cf. Ri 2023, `arXiv:2307.11312`, in `EXPLICIT_CLAIMS.md`). Nothing in this repository
imports, depends on, or relies on `openai/math`; every mapping below is informational.

## The honesty rule (paramount)

**Adjacency is not equivalence.** Every artifact on the "this project" side of a row
below is one of:

- a **numerical / decidable certificate** whose own source header states that the
  corresponding Millennium obligation is **NOT discharged** (`MillenniumBridge.lean`
  header; `NavierStokes.nsGlobalRegularityOpen := true`; `Hodge.quintic_codim2_open`),
  or
- an **abstract barrier lemma** (`PunoCalculus.LogicBarrier` — Lawvere/diagonal).

No row below asserts that any conjecture is resolved by either corpus, and no row
asserts an equivalence (or a reduction) between our artifact and their result. The
only claim each row makes is: *these two artifacts concern the same problem family.*

## Crosswalk

| Topic | Ours (module · what it is · standing) | `openai/math` family |
|---|---|---|
| 3D Navier–Stokes | `PunoCalculus.NavierStokes` (`serrinScaling`, `prodiSerrinAdmissible`, `serrin_endpoint_q3_excluded`, `nsGlobalRegularityOpen := true`) + the C1–C8 wall (`ExplicitClaims`, `OrientationLaw`, `RegularityReduction`, `SerrinSufficiency`) | **376. Universal computation in forced Navier–Stokes flows** |
| BSD | `PunoCalculus.BSD` (`namespace BSD`; `verifyCurve`, `verifyAllClose`, `verifyFullBSD`) — float check of the leading-term formula on 4 curves (conductor 11 / 14 / 37 / 389; ranks 0, 0, 1, 2) | **002. The full BSD formula from low Selmer corank** (+ companion *two-primary BSD* / *Selmer converse*), **006. Goldfeld's conjecture** |
| Hodge | `PunoCalculus.Hodge` (`cpnHodgeCount`, `h11`, `h20`, `verifyAbelian`, `quintic_codim2_open := true`) — Hodge-number / count checks for CP^n, curve products, abelian surfaces, the quintic | **032. The rational Hodge conjecture for CM abelian varieties** |
| Mass gap | `PunoCalculus.MassGap` (`massGapVal`, `verifyMassGapPositive`, `sinh_div_self_tendsto_one`, `massGapCrossoverRemovable`) — crossover / removable-singularity certificate | **215. Canonical O(3) continuum limit and exact O(4) mass asymptotics** (positive mass gap) |
| P vs NP / complexity | `PunoCalculus.PvsNP` (`c2k`…`c5k`, `verifyOrdering`, `verify2SATinP`, `verifyNPComplete`, `alphaC3`…) — threshold ordering numerics | **102** (Unique Games / Max-Cut, Vertex Cover), **105** (2-to-1 games), **106** (3-coloring), **274** (parity ∉ QAC⁰) |
| Logic / fixed points / undecidability | `PunoCalculus.LogicBarrier` (`lawvere_fixedpoint`, `no_surjective_of_no_fixedpoint`, `diagonal_not_mem_range`) + `PunoCalculus.ZeroFixedPoint` (`fixedPoint_selfSlope`, `zero_count_removable`) | **206** (finite lattice undecidability), **242** (single-fold Diophantine + undecidability), **328** (nonexpansive fixed points in reflexive Banach spaces), **314** (chromatic fixed-point loss) |
| Riemann hypothesis (adjacent) | `PunoCalculus.MillenniumBridge.rh_adjacent_finite_sector` — a finite, decidable sector, *explicitly not* a zeta statement | **003. The quasi-Riemann hypothesis** (zero-free `Re s > 7/8`) |
| Poincaré | `PunoCalculus.Poincare` | *(no matching family in the snapshot; **305** Wall's conjecture and **315** the Singer conjecture are unrelated)* |
| Millennium taxonomy | `PunoCalculus.MillenniumBridge` (`problemTaxonomy`, `seven_problems_declared_unsolved`, `pnnp_adjacent_classification`, `pnnp_adjacent_isometry_count`) — our standing for all seven problems | the corpus's number-theory / PDE / complexity families, collectively |

### Topics with no counterpart in the snapshot

A keyword scan of the catalog (`Collatz`, `3n+1`, `Syracuse`; `Goldbach`; `twin prime`;
`Legendre`) returned **no** matching family. The corresponding modules —
`PunoCalculus.Collatz`, `PunoCalculus.Goldbach`, `PunoCalculus.TwinPrime`,
`PunoCalculus.Legendre` — therefore have **no** `openai/math` row. (Nearest, and still a
different statement: **026. Positive lower density of large prime gaps**.)

## What is deliberately *not* claimed

- No shared code: this project imports none of `openai/math`'s Lean sources, and vice
  versa. Both use Lean 4 + Mathlib, but the libraries are independent.
- No shared result: where the two corpora touch (e.g. family **376** vs. our C8-open /
  C12), the objects differ — e.g. **376** is about Navier–Stokes *under smooth external
  forcing* (universal computation), whereas our wall C3 / C8-open is the *unforced*
  boundedness obligation; universality of the forced system does not settle it.
- No verification transfer: their family results are *claimed* by an unreleased model
  and independently unchecked; our modules are machine-checked or numerically
  certificate-based, and each states its own standing. Neither status is imported by
  the other.

## Literature anchors (external to both corpora)

The citations in `EXPLICIT_CLAIMS.md` and `CLAIM_TRACEABILITY.md` remain the register's
anchors and are independent of `openai/math`: Prodi (1959), Serrin (1962),
Escauriaza–Seregin–Šverák (2003), Koch–Tataru (2001), Cheskidov–Shvydkoy (2010,
arXiv:0708.3067), Beale–Kato–Majda (1984), Constantin–Fefferman (1993),
Deng–Hou–Yu (2015), Tao (2016, 2021), Adams–Hedberg (1996), and
Cantor (1891) / Gödel (1931) / Turing (1936) / Lawvere (1969) for the diagonal engine.

## How this is verified

`04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_external_crosswalk.py`
asserts, offline:

1. this file exists and names the canonical repo URL and the announcement URL;
2. every module named under **Ours** exists at
   `01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/<File>.lean` **and** is
   imported by the library root `PunoCalculus.lean`;
3. every quoted `openai/math` family number appears in this file's table;
4. the "no counterpart" modules are named and exist.

The external side is *not* fetched at test time (no network dependency): the family
numbers are pinned here, against the snapshot above.
