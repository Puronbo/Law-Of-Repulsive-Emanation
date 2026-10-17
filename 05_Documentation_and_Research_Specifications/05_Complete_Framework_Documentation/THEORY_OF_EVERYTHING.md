# THE THEORY OF EVERYTHING (register form)

*Status: **research program / map**, not a proof. This document fixes what
"theory of everything" means *inside this repository*: the structural
unification already formalized as **card C12** (`PunoCalculus/TheoryOfEverything.lean`).
It does **not** claim to settle any Millennium problem. Where this document and
`WHAT_THIS_DOES_NOT_PROVE.md` disagree, that boundary wins.*

---

## 0. What "theory of everything" means here

In this repository, "theory of everything" does **not** mean a physical unified
field theory or a theory of quantum gravity. Nothing in the Lean core models
spacetime, forces, or matter.

It means the register's own claim, and only that claim:

> **A scaling-critical system is governed by exactly two organizing numbers.**

Those two numbers — the **order** and the **orientation** — are defined over the
repository's own register (cards C1–C38), and the entire register is packaged as
one theorem. That theorem is card **C12** in `EXPLICIT_CLAIMS.md`, formalized in
`PunoCalculus/TheoryOfEverything.lean` and recorded in `VERIFICATION_LEDGER.md`
as a **capstone synthesis** that *"proves no new analytic content — it makes the
whole register citable as one theorem."*

This is the honest, and the only defensible, sense in which the project has a
"theory of everything". The ambition that a physical or Millennium-level TOE
follows from the 0/0 doctrine is **narrative**, kept outside this boundary (see
`WHAT_THIS_DOES_NOT_PROVE.md` and the legacy `UNIFIED_PROOF.md` / `MILLENNIUM.md`).

---

## 1. The two organizing numbers

| Number | Meaning | Law |
|---|---|---|
| **order** `a` | slides the critical rung of the ladder | `criticalSmoothness a p = sCrit p + (1 - a)` |
| **orientation** `r` | magnitude of the local multiplier (Lyapunov base) | invariant bounded `↔ r <= 1`; `sign(log r)` reads the side |

* **Order** is realized in `PunoCalculus/OnePattern.lean`
  (`criticalCurve_through_ladder`, `scalingWeight_vanishes_family`): the
  one-parameter family through the critical ladder `sCrit` of
  `PunoCalculus/CriticalLadder.lean`, on which the homogeneous norm is scale-free.
* **Orientation** is realized in `PunoCalculus/OrientationBoundedness.lean`
  (`geometric_bounded_iff`, `orientation_decides_boundedness`,
  `repelling_iff_unbounded`), with the formal Lyapunov sign from
  `PunoCalculus/GreatAttractor.lean` (`criticalSmoothness`, `scalingWeight`,
  `fixedPoint_logSign`).

*Interpretive note (structural, not physical):* A minimal trinity {-1,0,+1} maps heuristically to C12: 0 is the center/margin boundary (neutral crossing), -1 and +1 are the orientation sides (r<1 attracting/bounded, r>1 repelling/unbounded); order a is the scale that sets the rung s_crit(p)+(1-a). This is a heuristic correspondence within the register only (no claim to physical unification or Millennium settlement).

**How far the correspondence goes (increment T2).** The order half is a genuine
*bijection*: for a fixed form `p`, the map `a ↦ criticalSmoothness a p` is
injective (recover the order, `a = 3/p - s`) and surjective — this is
`order_sets_rung_bijective`. The orientation half is **not** a bijection: the side
predicate `r ↦ r <= 1` is many-to-one, so orientation is *not* recovered from the
side — `orientation_not_injective_on_side` exhibits two distinct admissible
orientations on the same side. So "two numbers close the register" means the pair
`(order, orientation) ↦ (rung, side)` is a surjection that is injective in the
order coordinate and many-to-one in the orientation coordinate; it is not a
bijection of pairs. See §6, row **T2**.

---

## 2. The capstone: the register as one theorem

`PunoCalculus.TheoryOfEverything.theoryOfEverything` is a conjunction of the
whole register chain:

1. **Order sets the rung** — `criticalSmoothness a p = sCrit p + (1 - a)`
   (`order_sets_rung`, from `OnePattern`).
2. **Scale-invariance on the family** — `scalingWeight (criticalSmoothness a p) a p = 0`
   (`OnePattern.scalingWeight_vanishes_family`).
3. **Serrin complementarity** — `gnExponent p + sCrit p = 1 / 2`
   (`CriticalLadder.thetaAddSCrit`; the `SerrinLadder` exponent `gnExponent`).
4. **Orientation sets the side** — bounded `↔ r <= 1`
   (`OrientationBoundedness.geometric_bounded_iff`).
5. **`sign(log r)` reads the side** — `0 < log r ↔ ¬ bounded`, `log r <= 0 ↔ bounded`
   (`OrientationBoundedness.orientation_decides_boundedness`).
6. **Barrier hierarchy** — order-≤1 shapes are controlled
   (`EnstrophyBarrier.mono_step_bounded`), order-2 shapes are not
   (`EnstrophyBarrier.quadratic_no_uniform_bound`).
7. **Sufficiency loop** — bounded invariant ⇒ global existence
   (`SufficiencyLoop.global_exists_of_mono`).

Two further reductions sit beside it:

* **`twoNumbersClose`** — both the *which-rung* question (order) and the
  *which-side* question (orientation) are functions of the two numbers alone;
  nothing else enters. **(T2 resolved, in part.)** The order↔rung is bijective
  (`order_sets_rung_bijective`); the side does not determine orientation
  (`orientation_not_injective_on_side`), so "bijection of pairs" does **not** hold.
* **`method_and_margin_barriers`** — the margin is a unique / first crossing
  (`MarginCrossing.existsUnique_zero_of_strictAntiOn`,
  `FirstCrossing.exists_first_zero`) and the method barrier is the diagonal
  (`LogicBarrier.no_surjective_predicates`): one skeleton for Cantor (1891),
  Gödel (1931), Turing (1936).

The build imports only the register's own bricks plus `Mathlib`; no external
result is imported as a proof of ours.

---

## 3. The brick map

Every conjunct traces to a committed brick and a card. The capstone is an
**aggregator**: it introduces no new analytic content, it joins existing bricks.

| Conjunct / reduction | Brick module (`PunoCalculus/`) | Card |
|---|---|---|
| order sets the rung; scale-invariance | `OnePattern.lean` | C12 (via C1) |
| critical ladder, `s_crit`, complementarity | `CriticalLadder.lean` | C1 |
| Serrin exponent `gnExponent` | `SerrinLadder.lean` | C25 |
| Onsager-excess borderline | `OnsagerCriterion.lean` | C29 |
| continuation criterion | `ContinuationCriterion.lean` | C30 |
| quantitative continuation | `QuantitativeContinuation.lean` | C31 |
| stability of bounded states | `StableBounded.lean` | C-stable |
| barrier hierarchy | `EnstrophyBarrier.lean` | C-barrier |
| sufficiency loop | `SufficiencyLoop.lean` | C32 |
| orientation decides the side | `OrientationBoundedness.lean` | C11 |
| Lyapunov sign / great attractor | `GreatAttractor.lean` | C26 |
| margin: unique / first crossing | `MarginCrossing.lean`, `FirstCrossing.lean` | C-margin |
| method barrier (diagonal) | `LogicBarrier.lean` | C14 |
| **capstone aggregator** | `TheoryOfEverything.lean` | **C12** |

---

## 4. The one open content

The capstone is honest about its own gap. Uniqueness of the margin
(`MarginCrossing`) needs the probe `lambda(s)` to be **antitone** in the
dissipation order `s`. That antitoneity is **not** proved here — it is the
Navier–Stokes-specific content (**T3** of this program). `FirstCrossing` keeps the
weakest hypothesis (continuity + one sign change) so that a margin *exists*
regardless, but its uniqueness and the whole analytic wall stay **OPEN** (cards
**C3** and **C10-open**; see `VERIFICATION_LEDGER.md`: *"no Millennium problem
touched. Wall OPEN."*).

* **The C12 numeric certificate ties that assumption to the certificate and
  does not prove it.** The numeric half of the capstone,
  `02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/theory_of_everything_certificates.py`,
  encodes the strict-antitone probe as a register-shaped *stand-in*
  (`lambda_reg(s) = C - alpha * s`, positive `C`, `alpha`) rather than a proved
  model: the antitone hypothesis is assumed here (NS-specific, T3 OPEN) and is
  not proved here. The certificate prints exactly that -- *"The antitone
  hypothesis for lambda(s) is ASSUMED (NS-specific, T3 OPEN); FirstCrossing shows
  existence without it."* -- so the numeric half registers the assumption instead
  of proving it. (The non-monotone `FirstCrossing` branch needs no such
  assumption.)

---

## 5. What this does not claim

* It does **not** solve, prove, or settle any Millennium problem
  (`WHAT_THIS_DOES_NOT_PROVE.md`; `PunoCalculus.MillenniumBridge`).
* It does **not** model physics; it is a structural statement about this
  register.
* It does **not** import an external result as a proof of ours.
* The register marker stays **OPEN**.

---

## 6. Program: falsifiable increments

The TOE *program* is the list of increments that would strengthen the
two-numbers claim. Each is stated with its **falsifier**, so it can fail.

| ID | Increment | Falsifier |
|---|---|---|
| **T1** | Extend the order family from the one-pattern slide to every card's own order. | a register brick whose rung is not `sCrit p + (1 - a)`. **Coverage (current):** explicit shift family appears in `OnePattern` (`criticalCurve_through_ladder`), `GreatAttractor` (`criticalSmoothness_*`), and is aggregated in `TheoryOfEverything` (`order_sets_rung`, `order_sets_rung_bijective`). Many base bricks define only `sCrit` (order-1); extending the family means re-parameterizing each card’s order to satisfy the same affine shift. |
| **T2** | Sharpen `twoNumbersClose` to a *bijection* (order/orientation recovered from the register state). | **Realized (negative):** order half is a bijection (`order_sets_rung_bijective`); orientation half is *not* injective (`orientation_not_injective_on_side`) — side does not recover orientation. No single-pair bijection. |
| **T3** | Close the margin gap: prove `lambda(s)` antitone for the NS/Burgers family. | a Leray–Hopf solution with `lambda <= 0` but unbounded critical norm. **Numerical evidence:** fractional Burgers shows a single sign flip with roughly monotone post-flip behavior across windows; fractional CLM shows multiple orientation flips (non-monotone `lambda(s)`) in sweep data, so antitonicity is **not universal** across fractionally-dissipated families. The margin uniqueness hypothesis remains **NS-specific** and **OPEN**. |
| **T4** | Attach a numeric certificate to C12 as a whole (mirroring the per-card certificates). | **Done:** `theory_of_everything_certificates.py` exists, runs green (PASS), and is wired into C12 evidence/traceability. |
| **T5** | Add a cross-domain mechanism card C39+ only if it is expressible via `(order, orientation)`. | a new mechanism that is not. **Boundary rule (active):** any new card C39+ must satisfy the two-numbers reduction (rung/side functions of `(order, orientation)` only); adding a mechanism that cannot be expressed via `(order, orientation)` is disallowed by this program. |

---

## 7. How it is verified

`test_theory_of_everything.py` (in
`04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/`) pins this
program so it cannot drift:

* the capstone module and all 14 of its register imports exist on disk and are
  named here (the brick map);
* the capstone exposes `order_sets_rung`, `orientation_sets_side`,
  `twoNumbersClose`, `order_sets_rung_bijective`, `orientation_not_injective_on_side`,
  `theoryOfEverything`, `method_and_margin_barriers`,
  `theoryOfEverythingFacts`;
* the facts register `theoryOfEverythingFacts` has exactly **5** entries
  (`theoryOfEverythingFacts_length`);
* this document states the honesty boundary (no Millennium problem settled; the
  wall is **OPEN**) and names card **C12**.

Axiom footprint of every quoted capstone declaration is recorded in
`AXIOM_AUDIT.md` (`⊆ {propext, Classical.choice, Quot.sound}`; the length
certificate is axiom-free).

---

## Related

* `EXPLICIT_CLAIMS.md` — card **C12** is this document's source of truth.
* `CLAIM_TRACEABILITY.md` — C12 → `TheoryOfEverything.lean` → `register_ladder_certificates.py`,
  `theory_of_everything_certificates.py`.
* `VERIFICATION_LEDGER.md` — the capstone's dated entry ("Wall OPEN").
* `AXIOM_AUDIT.md` — axiom footprint of the capstone declarations.
* `WHAT_THIS_DOES_NOT_PROVE.md` — the boundary this program obeys.
* `LANDAUER_BOUND_AND_THE_REGISTER.md` — an interpretive note on the
  information/thermodynamic reading (not a card, no physical claim).
* `PunoCalculus/TheoryOfEverything.lean` — the theorem itself.

---

*Two numbers close the register: order sets the rung, orientation sets the side.
Everything else is narrative. The wall stays OPEN.*
