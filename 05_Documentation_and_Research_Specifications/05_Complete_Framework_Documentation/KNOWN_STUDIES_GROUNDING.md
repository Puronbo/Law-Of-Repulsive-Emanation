# KNOWN-STUDIES GROUNDING CROSSWALK

*Status: map / linkage. No external result is claimed as ours; no Millennium
problem is settled here. See `WHAT_THIS_DOES_NOT_PROVE.md` and
`EXPLICIT_CLAIMS.md`.*

---

## Purpose

The register (`EXPLICIT_CLAIMS.md`, cards C1–C38; `VERIFICATION_LEDGER.md`) is
self-contained: each card pairs a Lean theorem half with a numeric certificate
half. This document is the **outward** half of the same honesty contract. It
anchors each of the framework's mechanisms to **named, checkable studies** in the
literature *and* to **our own certified artifacts** at the same time, so a reader
can move in either direction:

* from a classical result to the repository object that is a form of it, or
* from a repository object to the classical result it echoes.

Every *Known studies* cell is a **link**, never an import; every *Ours* cell is
**something the repository actually proves or runs**. The gate
`test_grounding_crosswalk.py` pins these links (files exist, modules exist,
anchors present) so the map cannot drift from the tree.

### How to read a block

* **Ours** — the repository artifacts (docs, Lean modules, numeric certificates).
* **Known studies** — named results/works the mechanism is a form of.
* **Shared content** — the exact statement the two sides actually share.
* **Honest boundary** — what the link does **not** carry.

---

## M1. The 0/0 removable-value law

* **Ours** — `THE_LAW_OF_SINGULARITIES.md`; `REMOVABLE_SINGULARITIES.md`; Lean
  `PunoCalculus/RemovableValue.lean` (`IsRemovableValue`,
  `removable_value_unique`, `existsUnique_iff_exists_and_unique`),
  `PunoCalculus/RemovableComplexBridge.lean` (the Riemann schema).
* **Known studies** — the removable-singularity theorem of **Riemann** (1851);
  the bounded-entire collapse of **Liouville** (`PunoCalculus/LiouvilleBridge.lean`);
  the classical indeterminate-form
  limits and **L'Hôpital**'s rule; the categorical initial/terminal/zero object of
  **Mac Lane**.
* **Shared content** — an indeterminate `0/0` whose surrounding structure forces
  a *unique* finite value: exactly "a removable singularity has a unique
  extension value".
* **Honest boundary** — this is the *general form*; the analytic hypotheses
  (continuity, holomorphy) that make a specific `0/0` removable are the classical
  theorems, cited, not re-proved.

---

## M2. The five 0/0 mechanisms

* **Ours** — `PunoCalculus/ZeroProbe.lean` (C19), `VanishOrder.lean` /
  `ZeroValuation.lean` (C18/C20), `ZeroIndex.lean` (C21),
  `NoetherDiscrete.lean` / `UniverseGrowth.lean` (C36/C37),
  `CriticalAmplitude.lean` (C38); numeric halves
  `zero_mechanism_certificates.py`, `arithmetic_shadow_certificates.py`.
* **Known studies** — root **index** / multiplicity; algebraic **valuations**
  (order of vanishing, `v(xy)=v(x)+v(y)`); discrete conservation laws
  (**Noether**, 1918); critical scaling relations of statistical mechanics —
  **Widom** (1965), **Rushbrooke** (1963), **Josephson** (1967), **Fisher**
  (1968), **Wilson** renormalization (1971).
* **Shared content** — each mechanism is the arithmetic skeleton of a classical
  construction: Probe ⇒ removable value; Vanishing-Rate ⇒ valuation; Index ⇒
  additive multiplicity; Conservation ⇒ momentum/charge balance; Critical
  Phenomenon ⇒ Widom/Rushbrooke/Josephson/Fisher exponent identities.
* **Honest boundary** — each is instantiated on finite models / finite
  enumeration; no phase transition is proved critical, no field theory is
  constructed.

---

## M3. The folding mechanism

* **Ours** — `THE_BOOK_OF_PUNO.md` and `Folding_Calculus_Paper.md` (fold =
  differentiation, unfold = the antiderivative; **crease density** as a
  diagnostic); `PunoCalculus/Curvature.lean`.
* **Known studies** — the **fold-and-cut** theorem (**Demaine**, Demaine & Lubiw,
  1998); isometric folding of Riemannian manifolds (**Robertson**, 1977);
  **Kawasaki**'s flat-foldability condition; ReLU networks as folded
  piecewise-linear maps (**Keup** & Helias, 2022; **Telgarsky**, 2016); the
  space-folding measure (**Lewandowski** et al., TMLR 2025 / AAAI 2026);
  FoldAndCutNetworks (**Stewart**, Layton, Bennett & Driggs, 2025).
* **Shared content** — a piecewise-smooth object is the *unfolding* of its
  creases; differentiation folds, and the crease set is the singular locus; a
  ReLU network is a layered fold.
* **Honest boundary** — "ReLU layer = fold" is a modelling frame with numerical
  support (crease density vs depth / accuracy), not a theorem; the NP-power of
  fold-and-cut does **not** transfer.

---

## M4. The ECA / elementary-cellular-automata family

* **Ours** — `PunoCalculus/EcaIsometry.lean` (affine/isometry classifications;
  the rule-204 / rule-51 identity–complement pair at every ring width 4..16);
  `PunoTwin/TwinRingLaws.lean` (`rule204_identity_all`, `rule51_complement_all`,
  **every** width); `PunoTwin/TwinAnalyticLaws.lean` (NLSE twin mass law);
  `ELASTIC_SOLITON_SCATTERING.md` (shift_bus **rule 29 == ECA 184**,
  **rule 71 == ECA 226**; the five density-conserving rules 15/29/51/71/85; the
  soliton family {12,44,68,100}); certified suite `Create Native Ramp Function
  and Implement 8-Bit ECA Rules/` (`run_all_audits.py`,
  `validate_soliton_isometry_proofs.py`).
* **Known studies** — **Wolfram**'s classification of elementary cellular
  automata (1983; 2002 *A New Kind of Science*); **Cook**'s proof that rule 110
  is universal (2004); rule 184 as the deterministic traffic / **TASEP** model
  (**Nagel**–Schreckenberg, 1992); the Fermat number `F4 = 65537 = 2^16+1` in
  the Fermat denominator window of `MPOperator`.
* **Shared content** — ECA rules form exhaustively enumerable families; identity
  (204) and complement (51) are the "perfect" members, closed under ring width;
  the density-conserving rules are exactly the TASEP/traffic pair together with
  the transparent movers and the static identity.
* **Honest boundary** — rule-110 universality is Cook's theorem, not ours; our
  content is the exact classification / closure for the specific families at each
  width and the exact TASEP identification, not an autonomy result.

---

## M5. The scaling-critical ladder (the Navier–Stokes wall)

* **Ours** — `CriticalLadder.lean` (C1), `SerrinLadder.lean` (C25),
  `OnsagerCriterion.lean` (C29), `ContinuationCriterion.lean` (C30),
  `SufficiencyLoop.lean` (C32), `EnstrophyBarrier.lean`,
  `QuantitativeContinuation.lean`; numeric halves
  `register_core_certificates.py`, `register_ladder_certificates.py`,
  `register_criteria_certificates.py`.
* **Known studies** — the **Prodi** (1959) / **Serrin** (1962) regularity
  criterion; the scaling-critical `L^3` space (**Koch**–Tataru, 2001);
  **Onsager** (1949) anomalous dissipation and its sharp exponent;
  **Beale**–Kato–Majda (1984) and **Constantin**–Fefferman (1993) continuation
  criteria; **Tao** (2016, 2021) quantitative continuation; recent partial
  results (Feng–He–Wang, 2025; Grujic, 2024).
* **Shared content** — the one scaling-invariant index `s_crit(p) = 3/p - 1`,
  the complementary exponent `theta(p) + s_crit(p) = 1/2`, and the Onsager-excess
  borderline `eta = 0`.
* **Honest boundary** — boundedness of the critical norm along the flow is
  **OPEN**; the whole register records it as a marker, never a settlement.

---

## M6. Discrete conservation (Noether)

* **Ours** — `NoetherDiscrete.lean` (`momentum_conserved`),
  `UniverseGrowth.lean` (`universeGrowth_conserves`); numeric half
  `arithmetic_shadow_certificates.py`.
* **Known studies** — **Noether** (1918) symmetry ⇒ conservation; its discrete,
  structure-preserving counterpart (leapfrog / Störmer–Verlet energy and
  momentum preservation).
* **Shared content** — translation invariance ⇒ a conserved momentum; growth
  that enters with zero displacement is neutral.
* **Honest boundary** — finite sums of reals; no continuum limit, no field
  theory.

---

## M7. Orientation and boundedness (the great attractor)

* **Ours** — `GreatAttractor.lean` (C26), `OrientationBoundedness.lean` (C11),
  `OrientationLaw.lean` / `DissipativeFlow.lean` (C10); numeric half
  `register_ladder_certificates.py`.
* **Known studies** — Lyapunov stability and the sign of log-growth; fixed-point
  stability by linearization (`|f'|`); the attractive / neutral / repelling
  trichotomy.
* **Shared content** — the orientation (`|L| ⋚ 1`, sign of `log r`) decides
  boundedness; the log-growth integral is the discriminator, and orientation
  alone sets the wall's side.
* **Honest boundary** — numerical and finite-arithmetic; the analytic wall
  remains that of M5.

---

## M8. The logic barrier

* **Ours** — `PunoCalculus/LogicBarrier.lean` (C14: `lawvere_fixedpoint`,
  `no_surjective_of_no_fixedpoint`, `no_surjective_predicates`,
  `diagonal_not_mem_range`; axiom-free).
* **Known studies** — the **Lawvere** fixed-point theorem (1969); **Cantor**'s
  diagonal argument (1891).
* **Shared content** — a surjection onto predicates forces a fixed point, and the
  absence of that fixed point forbids the surjection — the abstract diagonal
  barrier.
* **Honest boundary** — the barrier is formal/constructive; it constrains proof
  *strategies*, not the truth of the underlying conjectures.

---

## M9. The dimensional wall and mixtures

* **Ours** — `PunoCalculus/ExplicitClaims.lean` (`morrey_threshold`,
  `physical_embedding_gap`, `mean_le_dimMixture`); numeric halves
  `dimension_threshold.py`, `dimension_mixture.py`.
* **Known studies** — **Morrey**'s inequality and the Sobolev embedding
  `H^1 ⊂ L^∞` below dimension 2 (**Adams**–Hedberg, 1996); intermittency and
  dimension regularization in turbulence (**Frisch**, 1995; Constantin, 1994).
* **Shared content** — the `H^1 → L^∞` gain is `1 - d/2`, so the energy method is
  exactly half a derivative short at physical `d = 3`; the dimension of a mixture
  is a sup, not a mean, so averaging never lowers the effective dimension.
* **Honest boundary** — finite arithmetic on the embedding index; the analytic
  embedding theorems are cited, and the regularity wall stays open.

---

## What this crosswalk does not do

* It does not import any external result as a proof of ours, and does not export
  ours as a proof of theirs.
* It does not settle any Millennium problem; the register's marker stays
  **OPEN**.
* It is a map of *shared statements*, and `test_grounding_crosswalk.py` pins the
  links so the map cannot drift from the tree.

---

*Everything folds. Everything unfolds. The crease is where the action is.*
