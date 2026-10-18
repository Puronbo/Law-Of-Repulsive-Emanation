# Module Ledger

**Status: machine-checked coverage.** Every Lean module under
`01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/` (recursively) is
classified exactly once in the table below and is imported by the library root
`PunoCalculus.lean`, so `lake build PunoCalculus` compiles all of it. This closes the
last gap in the *claim* graph: `CLAIM_TRACEABILITY.md` links the carded modules, but
unguarded modules could silently exist outside it. Here every module is assigned a
category and, where applicable, the claim card(s) it carries.

Enforced by
`04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_module_ledger.py`: a
module on disk but absent here (or vice versa), a category outside the legend, a module
claimed as a *card* whose ID is not in `test_claim_traceability.py`, or a module not
imported by the root, fails the checker.

## Legend

| category | meaning |
|---|---|
| `card` | carries a named claim card C1 ... C38 in `EXPLICIT_CLAIMS.md` |
| `millennium-cert` | a per-problem numerical record / status entry for a Clay problem; **no** settlement claim |
| `rh-research` | Riemann-hypothesis exploratory / numerical module |
| `number-theory-cert` | a *bounded* numerical certificate for a number-theory question (Collatz, Goldbach, twin primes, Legendre) |
| `fluid-diagnostic` | Navier-Stokes decay-ratio arithmetic / on-flow diagnostic support |
| `numerical-cert` | a finite, bounded enumeration certificate |
| `cosmology` | cosmological model (framing; excluded by the scope gate) |
| `core-scaffold` | library scaffold or the base 0/0 / removable-value mechanism |
| `information-bridge` | an information/thermodynamic bridge brick: arithmetic linking the register to a named physical input (Landauer); **no** physical or settlement claim |

## Ledger

| Module | category | cards | role |
|---|---|---|---|
| `BSD` | millennium-cert | — | numerical BSD record (L-values, Omega, regulator, Sha, Tamagawa, ranks) over a few curves; no settlement claim |
| `Basic` | core-scaffold | — | library smoke module (`def hello := "world"`); no content, wired so `lake build` covers every file |
| `CascadeRatio` | fluid-diagnostic | — | NS energy/enstrophy decay-ratio arithmetic (`energyDecay`, `enstrophyDecay`, `cascadeRatio`, `verifyRDecays`) |
| `Collatz` | number-theory-cert | — | bounded Collatz certificate (`verifyCollatz100`, `maxStopN`); not a proof of Collatz |
| `ContinuationCriterion` | card | C30 | carries card(s) C30 |
| `Core` | rh-research | — | zeta-zero Hadamard-term positivity checks (`hadamardTerm`, `zetaZeros`, `checkAllTestPoints`) |
| `Cosmology.AcousticZeroFlow` | cosmology | — | acoustic 0/0-flow cosmological model (framing; gate-A excluded) |
| `Cosmology.OriginWindow` | cosmology | — | origin-window cosmological model (framing; gate-A excluded) |
| `CriticalAmplitude` | card | C38 | carries card(s) C38 |
| `CriticalLadder` | card | C1 | carries card(s) C1 |
| `Curvature` | rh-research | — | numerical curvature of `xi'` / L-dash positivity at Riemann zeros |
| `DissipativeFlow` | card | C10 | carries card(s) C10 |
| `EcaIsometry` | numerical-cert | — | elementary cellular automaton affine/isometry census (16 affine, 6 isometry classes) |
| `EmergentTime` | card | C13 | carries card(s) C13 |
| `EnstrophyBarrier` | card | C4/C6 | carries card(s) C4/C6 |
| `ExplicitClaims` | card | C4/C6, C8 | carries card(s) C4/C6, C8 |
| `FirstCrossing` | card | C10 | carries card(s) C10 |
| `ForceNetwork` | card | C27 | carries card(s) C27 |
| `Goldbach` | number-theory-cert | — | bounded Goldbach certificate (`goldbach_even_4_to_100000`) plus an explicit open marker |
| `GreatAttractor` | card | C26 | carries card(s) C26 |
| `Hodge` | millennium-cert | — | numerical Hodge record; no settlement claim |
| `InformationBridge` | information-bridge | — | two-state (bit) instance of the Landauer–register schema: `binaryEntropy_half` (`log 2`), `resetCost_two`, `resetCost_eq_neg_orientation` (cost = −k_B T·orientation), `orientation_reset_nonpos`; the physical map `Phi` stays the named missing entity |
| `InformationMixture` | information-bridge | — | classical mixture algebra for a "mixture of two or more" channels: `entropy_mixture` (H(mix) = t·H(a) + (1−t)·H(b) + binaryEntropy t), `binaryEntropy_nonneg`, `entropy_mixture_ge`, `entropy_mixture_half` (a fair mixture adds exactly `log 2`); no measured apparatus is identified |
| `InformationPhi` | information-bridge | — | concrete dynamical 0/0 instance: the relaxation `(1 − r^x)/x` has removable value `−orientation r` (C17), `deficitRate_stateCounting` gives `log n` at `r = 1/n`; the constructed map `Phi` satisfies the claim's three clauses (`Phi_satisfies_claim`); the physical identification stays the missing entity |
| `InformationTime` | information-bridge | — | the time reading of `Phi`: `evolution` is a one-parameter semigroup (`evolution_add`), the orientation is minus the rate (`orientation_evolution_one`), the count is time (`evolution_pow_nat`), and the `{-1,0,+1}` trinity is the decay/stationary/growth arrow (`orientation_arrow`); links `Phi` to `EmergentTime` (C13); no physical claim |
| `Legendre` | number-theory-cert | — | bounded Legendre certificate |
| `LiouvilleBridge` | card | C24 | carries card(s) C24 |
| `LogicBarrier` | card | C14 | carries card(s) C14 |
| `MarginCrossing` | card | C10 | carries card(s) C10 |
| `MassGap` | millennium-cert | — | Yang-Mills mass-gap crossover borrower (`sinh_div_self_tendsto_one`, `massGapCrossoverRemovable`); the gap itself stays OPEN |
| `MillenniumBridge` | millennium-cert | — | the seven-problem status record (`NOT SETTLED BY THIS PROJECT`, `statuses.length = 7`) |
| `MixtureGrowth` | card | C28 | carries card(s) C28 |
| `NavierStokes` | millennium-cert | — | Serrin-scaling arithmetic plus recorded open statements (`serrinScaling`, `prodiSerrinIntegralFiniteCertified = false`, `nsGlobalRegularityOpen = true`) |
| `NoetherDiscrete` | card | C36 | carries card(s) C36 |
| `OnePattern` | card | C35 | carries card(s) C35 |
| `OnsagerCriterion` | card | C29 | carries card(s) C29 |
| `OrientationBoundedness` | card | C10, C11 | carries card(s) C10, C11 |
| `OrientationLaw` | card | C10, C10-open, C11 | carries card(s) C10, C10-open, C11 |
| `Poincare` | millennium-cert | — | numerical Poincare record; no settlement claim |
| `PvsNP` | millennium-cert | — | contour-recorded wall (`noPolynomialCompilationKnown`, `compilation_wall_recorded`); no settlement claim |
| `QuantitativeContinuation` | card | C4/C6 | carries card(s) C4/C6 |
| `RH.Density` | rh-research | — | Riemann-hypothesis zero-density numerical module |
| `RH.Dominance` | rh-research | — | Riemann-hypothesis dominance numerical module |
| `RH.Hankel` | rh-research | — | Riemann-hypothesis Hankel-matrix numerical module |
| `RH.LiCriterion` | rh-research | — | Riemann-hypothesis Li-criterion module (`li_probe`, `finiteNeverSettles`); explicit open marker |
| `RH.Monotonicity` | rh-research | — | Riemann-hypothesis monotonicity numerical module |
| `RH.NewmanFlow` | rh-research | — | Riemann-hypothesis Newman-flow numerical module |
| `RegularityReduction` | card | C10-open | carries card(s) C10-open |
| `Removable` | core-scaffold | — | the field-agnostic removable-value mechanism (`removable_limit`, `quadratic_removable`, `impedance_crosszero`); base of card C17 |
| `RemovableComplexBridge` | card | C23 | carries card(s) C23 |
| `RemovableValue` | card | C17 | carries card(s) C17 |
| `SelfSimilarExponents` | card | C33 | carries card(s) C33 |
| `SerrinLadder` | card | C25 | carries card(s) C25 |
| `SerrinSufficiency` | card | C10-open | carries card(s) C10-open |
| `StableBounded` | card | C31 | carries card(s) C31 |
| `SufficiencyLoop` | card | C32 | carries card(s) C32 |
| `TheoryOfEverything` | card | C12 | carries card(s) C12 |
| `TwinPrime` | number-theory-cert | — | bounded twin-prime certificate |
| `UniverseGrowth` | card | C37 | carries card(s) C37 |
| `VanishOrder` | card | C18 | carries card(s) C18 |
| `ZeroFixedPoint` | card | C34 | carries card(s) C34 |
| `ZeroIndex` | card | C21 | carries card(s) C21 |
| `ZeroLink` | card | C15 | carries card(s) C15 |
| `ZeroMechanisms` | card | C22 | carries card(s) C22 |
| `ZeroObject` | card | C16 | carries card(s) C16 |
| `ZeroProbe` | card | C19 | carries card(s) C19 |
| `ZeroValuation` | card | C20 | carries card(s) C20 |
| `ZeroZero` | core-scaffold | — | the 0/0 doctrine's elementary limit family (`entropy_removable_value`, `sin_x_div_tendsto_one`, ...) |

## Coverage

- **Modules on disk:** 68 (all imported by `PunoCalculus.lean`).
- **Card-carrying modules (`card`):** 38.
- **Non-card modules (millennium-cert / rh-research / number-theory-cert / fluid-diagnostic / numerical-cert / cosmology / core-scaffold / information-bridge):** 30.
