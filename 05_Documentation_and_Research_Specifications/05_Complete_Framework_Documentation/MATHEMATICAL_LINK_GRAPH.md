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

The internal graph has **73 module nodes** and **54 directed edges**. An edge
`A -> B` is exactly an `import PunoCalculus.B` line in module `A` (self-edges and
`import Mathlib` excluded). The block below is parsed by the checker; it must
equal the imports actually present in the tree.

<!-- EDGES:BEGIN -->
```
Crease -> ParabolaVertex
CriticalLadder -> SerrinLadder
DissipativeFlow -> OrientationLaw
EmergentTime -> CriticalLadder
ExplicitClaims -> CriticalLadder
GreatAttractor -> CriticalLadder
GreatAttractor -> ZeroFixedPoint
InformationBridge -> OrientationLaw
InformationMixture -> InformationBridge
InformationPhi -> InformationBridge
InformationPhi -> OrientationLaw
InformationPhi -> RemovableValue
InformationTime -> EmergentTime
InformationTime -> InformationPhi
InformationTime -> OrientationLaw
LiouvilleBridge -> RemovableComplexBridge
MillenniumBridge -> EcaIsometry
OnePattern -> GreatAttractor
OrientationBoundedness -> GreatAttractor
OrientationLaw -> OrientationBoundedness
ParabolaVertex -> GreatAttractor
ParabolaVertex -> ZeroZero
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
ShadowZeroZero -> ZeroZero
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
| CriticalLadder | C1 | RemovableComplexBridge | C21 |
| EnstrophyBarrier | C4 | LiouvilleBridge | C22 |
| ExplicitClaims | C4, C5, C6 | SerrinLadder | C23 |
| QuantitativeContinuation | C4 | GreatAttractor | C24 |
| DissipativeFlow | C8 | ForceNetwork | C25 |
| FirstCrossing | C8 | MixtureGrowth | C26 |
| MarginCrossing | C8 | OnsagerCriterion | C27 |
| OrientationLaw | C8, C8-open | ContinuationCriterion | C28 |
| OrientationBoundedness | C8, C9 | StableBounded | C29 |
| TheoryOfEverything | C10 | SufficiencyLoop | C30 |
| EmergentTime | C11 | SelfSimilarExponents | C31 |
| LogicBarrier | C12 | ZeroFixedPoint | C32 |
| ZeroLink | C13 | OnePattern | C33 |
| ZeroObject | C14 | RegularityReduction | C8-open |
| RemovableValue | C15 | SerrinSufficiency | C8-open |
| VanishOrder | C16 | NoetherDiscrete | C34 |
| ZeroProbe | C17 | UniverseGrowth | C35 |
| ZeroValuation | C18 | CriticalAmplitude | C36 |
| ZeroIndex | C19 | | |
| ZeroMechanisms | C20 | | |

The remaining 35 nodes are non-card modules (evidence carriers, not claims):
`BSD`, `Basic`, `Beal`, `CascadeRatio`, `Collatz`, `Core`, `Cosmology.AcousticZeroFlow`,
`Cosmology.OriginWindow`, `Crease`, `Curvature`, `EcaIsometry`, `Goldbach`, `Hodge`,
`InformationBridge`, `InformationMixture`, `InformationPhi`, `InformationTime`,
`Legendre`, `MassGap`, `MillenniumBridge`, `ParabolaVertex`, `NavierStokes`, `Poincare`, `PvsNP`,
`RH.Density`, `RH.Dominance`, `RH.Hankel`, `RH.LiCriterion`, `RH.Monotonicity`,
`Removable`, `ShadowZeroZero`, `TwinPrime`, `Wieferich`, `ZeroZero`, `RH.NewmanFlow`.

## 2. The chains

Reading the edges as "is built on", the graph decomposes into a few load-bearing
columns plus one aggregator. (Card labels on each node.)

- **Wall ladder.** `SerrinLadder (C23) -> CriticalLadder (C1) -> EmergentTime
  (C11)`; `CriticalLadder` also feeds `ExplicitClaims (C4,C5,C6)` and
  `GreatAttractor (C24)`. This is the scaling-critical core of the wall.
- **Orientation column.** `GreatAttractor (C24) -> OrientationBoundedness
  (C8,C9) -> OrientationLaw (C8,C8-open) -> DissipativeFlow (C8)`, and
  `OrientationLaw -> RegularityReduction (C8-open) -> SerrinSufficiency
  (C8-open) -> { CriticalLadder, RegularityReduction, SerrinLadder }`. The loop
  closes the ladder back onto the Serrin core.
- **Continuation block.** `ContinuationCriterion (C28)` and `EnstrophyBarrier
  (C4)` feed `QuantitativeContinuation (C4) -> SufficiencyLoop (C30) ->
  { ContinuationCriterion, EnstrophyBarrier }` — a second closed loop.
- **Zero-mechanism cluster.** `VanishOrder (C16) -> ZeroValuation (C18) ->
  ZeroMechanisms (C20)`, with `ZeroProbe (C17) -> ZeroMechanisms` and
  `ZeroIndex (C19) -> ZeroMechanisms`; and `ZeroProbe -> RemovableValue (C15) ->
  { Removable, ZeroLink (C13) }`.
- **Shadow mirror.** `ShadowZeroZero -> ZeroZero`: the reciprocal mirror
  `x ↦ 1/x` relocates a removable 0/0 (`0 → ∞`) keeping its value, and as the
  term-reciprocal gives the `∞/∞` mirror that inverts it — the one reverse in the
  register proved to be an exact involution.
- **Conic vertex.** `ParabolaVertex -> ZeroZero`: the polar conic `r(θ) =
  l/(1 + e·cos θ)` with focus at the origin (the framework's zero); the radial
  excess above the vertex is a removable 0/0 with value `l·e/(2(1+e)²)` (equals
  `1/8` for the vertex-at-`1/2` parabola), while the escape direction `θ → π` is
  a genuine pole — a Vanishing-Rate instance built on the `ZeroZero` limit family.
  That pole is an **infinity generator** of exact order two (`escape_infinity_rate`:
  `(π−θ)²·r(θ) → 2l`), and reciprocating the radius makes it a removable *zero* of
  rate `1/(2l)` (`shadow_of_pole_is_removable_zero`) — the reciprocal of the
  generator, tying the module to `ShadowZeroZero`.
  Its dynamical reading `ParabolaVertex -> GreatAttractor` reuses the framework's
  own `fixedPoint_repels`: the logistic parabola `4x(1−x)` has `f'(0) = 4 > 1`, so
  the vertex-origin is a fixed point the map repels its neighbourhood from.
- **The crease (cusp normal form).** `Crease -> ParabolaVertex`: the local
  mathematics of *every* generic fold. The fold germ `Φ a x = x³ − a·x` has its
  derivative `3x² − a` vanish exactly on the crease set (`deriv_fold_zero_iff`), so
  a crease exists only for `a ≥ 0`; for `a > 0` there are exactly two, `±√(a/3)`
  (`crease_eq_sqrt_or`), colliding at the cusp `a = 0` (`crease_zero_iff`). The cusp
  potential `V a b x = x⁴/4 − a·x²/2 − b·x` has that fold germ as its gradient
  (`deriv_cusp`), and on the cusp curve `a = 3r²`, `b = −2r³` the crease is a
  **double root** `(x−r)²(x+2r)` (`cusp_curve_factor`) with vanishing discriminant
  `4a³ = 27b²` (`cusp_discriminant`). The instance is shared with `ParabolaVertex`:
  the logistic apex `x = 1/2` is a crease (`deriv_logistic_half`). The brain reading
  (cortical gyri/sulci as these creases, and their universal folding scaling) is
  *empirical* and lives in `BRAIN_CREASE.md` — not claimed here.
- **The arithmetic crease (Wieferich).** `Wieferich` (standalone, Mathlib only):
  the 0/0 theme in number theory. Fermat gives `p | 2^(p-1) − 1` for a prime
  `p ≠ 2` (`fermat_dvd`), so the Fermat quotient `q_p = (2^(p-1) − 1)/p` is an
  integer — a *resolvable* 0/0. A Wieferich prime is exactly where `q_p` again
  vanishes mod `p`, i.e. `p² | 2^(p-1) − 1` (`isWieferich_iff_sq_dvd`,
  `isWieferich_iff_quotient_dvd`): the *second-order* zero — the arithmetic
  analogue of a `Crease`. The two known instances `1093` and `3511` are proved
  (`wieferich_1093`, `wieferich_3511`, kernel-checked by `decide`). Infinitude
  stays OPEN.
- **The Beal crease at exponent three.** `Beal` (standalone, Mathlib only): a
  *proven* modular obstruction behind the finite certificate. A base coprime to `3`
  is a unit of `ZMod 9` and has cube `±1 (mod 9)` (`cube_mod9`), and no two such
  residues sum to a third (`no_unit_cubes_solution`, discharged by `decide` over the
  nine-element ring). Lifting to `ℕ`: `A³ + B³ = C³` forces `3 | A ∨ 3 | B ∨ 3 | C`
  (`three_dvd_of_cubes`) — so a Beal window scan may skip every triple whose three
  bases are all coprime to `3`, and any coprime `a³ + b³ = c³` with `3 ∤ a,b` has
  `3 | c` (`three_dvd_of_cubes_of_not_dvd`). Beal's conjecture stays OPEN.
- **Removable bridge.** `ZeroLink (C13) -> RemovableValue (C15) ->
  RemovableComplexBridge (C21) -> LiouvilleBridge (C22)`: the value mechanism
  lifted to complex analysis and then to Liouville.
- **Aggregator.** `TheoryOfEverything (C10)` imports 13 modules — the single node
  that touches every other column.
- **Certificate link.** `MillenniumBridge -> EcaIsometry` joins the taxonomy
  record to its numerical certificate.
- **RH research.** `RH.Hankel -> RH.NewmanFlow` (the de Bruijn–Newman flow layer
  on top of the Hankel criterion).
- **Standalone cards.** `ForceNetwork (C25)`, `MixtureGrowth (C26)`,
  `SelfSimilarExponents (C31)`, `NoetherDiscrete (C34)` and `CriticalAmplitude (C36)`
  import only Mathlib, so they carry their card without an internal edge (the
  Conservation and Critical-Phenomenon mechanisms are finite-sum / real-algebra facts
  about the register, not built on another module).
- **Growth extension.** `UniverseGrowth (C35) -> NoetherDiscrete (C34)`: the
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
| Crease | Mota & Herculano-Houzel | BRAIN_CREASE.md |
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
| brain / crease | `BRAIN_CREASE.md` |

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
6. all 36 card tokens `C1 … C36` are present in the card list.

## Cards covered

<!-- CARDS:BEGIN -->
C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 C19 C20 C21 C22 C23 C24 C25 C26 C27 C28 C29 C30 C31 C32 C33 C34 C35 C36
<!-- CARDS:END -->
