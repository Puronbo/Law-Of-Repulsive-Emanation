# Mathematical Link Graph — how the verified insights connect, and what they cite

**Status: reference map, not a dependency.** This file completes the coverage
triangle. `CLAIM_TRACEABILITY.md` joins each card to *our* Lean declarations and
experiments; `PHYSICS_CROSSWALK.md` joins each card to a *physical* phenomenon;
`EXTERNAL_CORPORA_CROSSWALK.md` joins each module to a *neighbouring* corpus. This
file adds the two remaining axes:

- **internal** — which machine-checked insight is built on which, read directly
  off the `import` statements of the Lean sources; and
- **provided reference** — the citation each module header names, joined to the
  framework document that concerns the same result family.

The honesty rule is the same one the other maps carry: **adjacency is not
equivalence.** A `import` edge means one module reuses another's formal context;
it does **not** mean the two state the same theorem, that either is complete, or
that any Millennium obligation is discharged. See `WHAT_THIS_DOES_NOT_PROVE.md`.

## 1. The mesh (verified ↔ verified)

The internal graph has **64 module nodes** and **42 directed edges**. An edge
`A -> B` is exactly an `import PunoCalculus.B` line in module `A` (self-edges and
`import Mathlib` excluded). The block below is parsed by the checker; it must
equal the imports actually present in the tree.

<!-- EDGES:BEGIN -->
```
CriticalLadder -> SerrinLadder
DissipativeFlow -> OrientationLaw
EmergentTime -> CriticalLadder
ExplicitClaims -> CriticalLadder
GreatAttractor -> CriticalLadder
GreatAttractor -> ZeroFixedPoint
InformationBridge -> OrientationLaw
InformationPhi -> InformationBridge
InformationPhi -> OrientationLaw
InformationPhi -> RemovableValue
LiouvilleBridge -> RemovableComplexBridge
MillenniumBridge -> EcaIsometry
OnePattern -> GreatAttractor
OrientationBoundedness -> GreatAttractor
OrientationLaw -> OrientationBoundedness
QuantitativeContinuation -> ContinuationCriterion
QuantitativeContinuation -> EnstrophyBarrier
RH.NewmanFlow -> RH.Hankel
RegularityReduction -> OrientationLaw
RemovableComplexBridge -> RemovableValue
RemovableValue -> Removable
RemovableValue -> ZeroLink
SerrinSufficiency -> CriticalLadder
SerrinSufficiency -> RegularityReduction
SerrinSufficiency -> SerrinLadder
SufficiencyLoop -> ContinuationCriterion
SufficiencyLoop -> EnstrophyBarrier
UniverseGrowth -> NoetherDiscrete
TheoryOfEverything -> ContinuationCriterion
TheoryOfEverything -> CriticalLadder
TheoryOfEverything -> EnstrophyBarrier
TheoryOfEverything -> FirstCrossing
TheoryOfEverything -> GreatAttractor
TheoryOfEverything -> LogicBarrier
TheoryOfEverything -> MarginCrossing
TheoryOfEverything -> OnePattern
TheoryOfEverything -> OnsagerCriterion
TheoryOfEverything -> OrientationBoundedness
TheoryOfEverything -> QuantitativeContinuation
TheoryOfEverything -> StableBounded
TheoryOfEverything -> SufficiencyLoop
ZeroMechanisms -> ZeroIndex
ZeroMechanisms -> ZeroProbe
ZeroMechanisms -> ZeroValuation
ZeroProbe -> RemovableValue
ZeroValuation -> VanishOrder
```
<!-- EDGES:END -->

### Node labels

The 38 card-carrying modules (the "verified findings" of this graph):

| module | card | module | card |
|---|---|---|---|
| CriticalLadder | C1 | RemovableComplexBridge | C23 |
| EnstrophyBarrier | C4/C6 | LiouvilleBridge | C24 |
| ExplicitClaims | C4/C6, C8 | SerrinLadder | C25 |
| QuantitativeContinuation | C4/C6 | GreatAttractor | C26 |
| DissipativeFlow | C10 | ForceNetwork | C27 |
| FirstCrossing | C10 | MixtureGrowth | C28 |
| MarginCrossing | C10 | OnsagerCriterion | C29 |
| OrientationLaw | C10, C10-open | ContinuationCriterion | C30 |
| OrientationBoundedness | C10, C11 | StableBounded | C31 |
| TheoryOfEverything | C12 | SufficiencyLoop | C32 |
| EmergentTime | C13 | SelfSimilarExponents | C33 |
| LogicBarrier | C14 | ZeroFixedPoint | C34 |
| ZeroLink | C15 | OnePattern | C35 |
| ZeroObject | C16 | RegularityReduction | C10-open |
| RemovableValue | C17 | SerrinSufficiency | C10-open |
| VanishOrder | C18 | NoetherDiscrete | C36 |
| ZeroProbe | C19 | UniverseGrowth | C37 |
| ZeroValuation | C20 | CriticalAmplitude | C38 |
| ZeroIndex | C21 | | |
| ZeroMechanisms | C22 | | |

The remaining 26 nodes are non-card modules (evidence carriers, not claims):
`BSD`, `Basic`, `CascadeRatio`, `Collatz`, `Core`, `Cosmology.AcousticZeroFlow`,
`Cosmology.OriginWindow`, `Curvature`, `EcaIsometry`, `Goldbach`, `Hodge`,
`Legendre`, `MassGap`, `MillenniumBridge`, `NavierStokes`, `Poincare`, `PvsNP`,
`RH.Density`, `RH.Dominance`, `RH.Hankel`, `RH.LiCriterion`, `RH.Monotonicity`,
`Removable`, `TwinPrime`, `ZeroZero`, `RH.NewmanFlow`.

## 2. The chains

Reading the edges as "is built on", the graph decomposes into a few load-bearing
columns plus one aggregator. (Card labels on each node.)

- **Wall ladder.** `SerrinLadder (C25) -> CriticalLadder (C1) -> EmergentTime
  (C13)`; `CriticalLadder` also feeds `ExplicitClaims (C4/C6,C8)` and
  `GreatAttractor (C26)`. This is the scaling-critical core of the wall.
- **Orientation column.** `GreatAttractor (C26) -> OrientationBoundedness
  (C10,C11) -> OrientationLaw (C10,C10-open) -> DissipativeFlow (C10)`, and
  `OrientationLaw -> RegularityReduction (C10-open) -> SerrinSufficiency
  (C10-open) -> { CriticalLadder, RegularityReduction, SerrinLadder }`. The loop
  closes the ladder back onto the Serrin core.
- **Continuation block.** `ContinuationCriterion (C30)` and `EnstrophyBarrier
  (C4/C6)` feed `QuantitativeContinuation (C4/C6) -> SufficiencyLoop (C32) ->
  { ContinuationCriterion, EnstrophyBarrier }` — a second closed loop.
- **Zero-mechanism cluster.** `VanishOrder (C18) -> ZeroValuation (C20) ->
  ZeroMechanisms (C22)`, with `ZeroProbe (C19) -> ZeroMechanisms` and
  `ZeroIndex (C21) -> ZeroMechanisms`; and `ZeroProbe -> RemovableValue (C17) ->
  { Removable, ZeroLink (C15) }`.
- **Removable bridge.** `ZeroLink (C15) -> RemovableValue (C17) ->
  RemovableComplexBridge (C23) -> LiouvilleBridge (C24)`: the value mechanism
  lifted to complex analysis and then to Liouville.
- **Aggregator.** `TheoryOfEverything (C12)` imports 13 modules — the single node
  that touches every other column.
- **Certificate link.** `MillenniumBridge -> EcaIsometry` joins the taxonomy
  record to its numerical certificate.
- **RH research.** `RH.Hankel -> RH.NewmanFlow` (the de Bruijn–Newman flow layer
  on top of the Hankel criterion).
- **Standalone cards.** `ForceNetwork (C27)`, `MixtureGrowth (C28)`,
  `SelfSimilarExponents (C33)`, `NoetherDiscrete (C36)` and `CriticalAmplitude (C38)`
  import only Mathlib, so they carry their card without an internal edge (the
  Conservation and Critical-Phenomenon mechanisms are finite-sum / real-algebra facts
  about the register, not built on another module).
- **Growth extension.** `UniverseGrowth (C37) -> NoetherDiscrete (C36)`: the
  increasing point universe lifts the discrete Noether theorem to a growing family
  of active sites, with the newly created points carrying no momentum.

## 3. Reference anchors (provided → verified)

Each row names a citation that literally appears in the module header, and the
tracked framework document that concerns the same result family (a `—` means the
citation lives only in the module). The checker asserts the citation string is in
the module source and that any named document exists in a CI checkout.

<!-- REFS:BEGIN -->
| module | in-header citation | provided doc |
|---|---|---|
| NavierStokes | Prodi 1959 | EXTERNAL_CORPORA_CROSSWALK.md |
| NavierStokes | Serrin 1962 | EXTERNAL_CORPORA_CROSSWALK.md |
| NavierStokes | Ladyzhenskaya 1967 | — |
| RegularityReduction | Beale-Kato-Majda 1984 | SHARED_WALL_AND_PATH_FORWARD.md |
| RegularityReduction | Constantin-Fefferman 1993 | SHARED_WALL_AND_PATH_FORWARD.md |
| RH.NewmanFlow | de Bruijn 1950 | THE_INTERLACING_DE_BRANGES_0_OVER_0.md |
| RH.NewmanFlow | Newman 1976 | THE_INTERLACING_DE_BRANGES_0_OVER_0.md |
| LogicBarrier | Cantor (1891) | EXTERNAL_CORPORA_CROSSWALK.md |
| LogicBarrier | Turing (1936) | EXTERNAL_CORPORA_CROSSWALK.md |
| Hodge | Murty 1979 | EXTERNAL_CORPORA_CROSSWALK.md |
| Poincare | Perelman 2003 | EXTERNAL_CORPORA_CROSSWALK.md |
| MassGap | Gross-Wilczek 1973 | — |
| Goldbach | Silva 2013 | — |
| SelfSimilarExponents | arXiv:2405.10916 | — |
| ZeroFixedPoint | THE_LAW_OF_SINGULARITIES | — |
| ZeroMechanisms | THE_0_OVER_0_ATLAS | — |
| ZeroProbe | THE_0_OVER_0_ATLAS | — |
<!-- REFS:END -->

## 4. Provided reference library (tracked)

The framework documents that are version-controlled (so a CI checkout can cite
them without a network fetch), grouped by what they anchor. This is the *provided*
side of the links above.

| family | tracked document |
|---|---|
| coverage maps | `MODULE_LEDGER.md`, `PHYSICS_CROSSWALK.md`, `EXTERNAL_CORPORA_CROSSWALK.md`, `CLAIM_TRACEABILITY.md`, `EXPLICIT_CLAIMS.md` |
| scope / honesty | `WHAT_THIS_DOES_NOT_PROVE.md`, `SHARED_WALL_AND_PATH_FORWARD.md` |
| index theory | `THE_ATIYAH_SINGER_INDEX_THEOREM_0_OVER_0.md`, `THE_CHERN_GAUSS_BONNET_0_OVER_0.md`, `THE_RIEMANN_ROCH_0_OVER_0.md` |
| de Bruijn–Newman / RH | `THE_INTERLACING_DE_BRANGES_0_OVER_0.md`, `THE_RIEMANN_PROOF_ROADMAP.md` |
| zeta / primes | `THE_SELBERG_ZETA_FUNCTION_0_OVER_0.md`, `THE_SELBERG_TRACE_FORMULA_0_OVER_0.md`, `THE_PRIME_GEODESIC_THEOREM.md` |
| NS / physics | `THE_H_THEOREM_NAVIER_STOKES_0_OVER_0.md`, `THE_QFT_0_OVER_0.md`, `THE_BRODY_BOUNDARY_THEOREM.md`, `THE_ENTROPY_CONDITION_THEOREM.md` |
| structure / synthesis | `THE_COMPLETE_ACCOUNT.md`, `THE_FINAL_SYNTHESIS.md`, `THE_UNIVERSAL_ZERO.md`, `THE_MILLENNIUM_PRIZE_0_OVER_0.md`, `THE_PAPER.md`, `THE_GAP_ANALYSIS.md` |
| other 0/0 entries | `THE_KNOT_INVARIANTS_0_OVER_0.md`, `THE_LAURENT_DECOMPOSITION.md`, `THE_MODULAR_FORMS_0_OVER_0.md` |

## What is not claimed

- **Links are structural.** An edge records a Lean `import`; two linked modules
  share a formal context, not a conclusion. No row asserts an equivalence between
  the two endpoints, and none asserts that a conjecture is resolved.
- **Citations are pointers.** A row says the module header names that source; it
  does not import the source's result or claim that the source proves our card.
- **No verification transfer.** The certificate modules state their own standing
  (open markers included); this map neither upgrades nor downgrades it.

## How this is verified

`04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_mathematical_links.py`
asserts, offline:

1. this file exists and carries the scope banner and the adjacency rule;
2. the edge block equals the `import` statements actually parsed from
   `.../PunoCalculus/**.lean` — no missing, extra, or self edges;
3. every module named in the edges or reference rows exists on disk, and every
   edge target resolves to a module file;
4. every in-header citation string in the reference table appears in its module;
5. every non-`—` provided document exists under the documentation directory;
6. all 38 card tokens `C1 … C38` are present in the card list.

## Cards covered

<!-- CARDS:BEGIN -->
C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 C27 C28 C29 C30 C31 C32 C33 C34 C35 C36 C37 C38
<!-- CARDS:END -->
