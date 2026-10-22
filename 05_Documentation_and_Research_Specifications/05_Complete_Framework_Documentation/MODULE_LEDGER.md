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
| `card` | carries a named claim card C1 ... C36 in `EXPLICIT_CLAIMS.md` |
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
| `Beal` | core-scaffold | — | the exponent-three Beal/FLT modular crease: a base coprime to `3` is a unit of `ZMod 9` with cube `±1` (`cube_mod9`), and no two such residues sum to a third (`no_unit_cubes_solution`, by `decide` over `ZMod 9`); lifts to `A³ + B³ = C³ ⟹ 3 ∣ A ∨ 3 ∣ B ∨ 3 ∣ C` (`three_dvd_of_cubes`), so any coprime `a³ + b³ = c³` with `3 ∤ a, b` has `3 ∣ c` (`three_dvd_of_cubes_of_not_dvd`); the finite certificate `beal_certificate.py` rests on this reduction. Beal's conjecture OPEN |
| `CascadeRatio` | fluid-diagnostic | — | NS energy/enstrophy decay-ratio arithmetic (`energyDecay`, `enstrophyDecay`, `cascadeRatio`, `verifyRDecays`) |
| `Collatz` | number-theory-cert | — | bounded Collatz certificate (`verifyCollatz100`, `maxStopN`); not a proof of Collatz |
| `ContinuationCriterion` | card | C28 | carries card(s) C28 |
| `Core` | rh-research | — | zeta-zero Hadamard-term positivity checks (`hadamardTerm`, `zetaZeros`, `checkAllTestPoints`) |
| `Cosmology.AcousticZeroFlow` | cosmology | — | acoustic 0/0-flow cosmological model (framing; gate-A excluded) |
| `Cosmology.OriginWindow` | cosmology | — | origin-window cosmological model (framing; gate-A excluded) |
| `Crease` | core-scaffold | — | the local normal form of every fold: the fold germ `Φ a x = x³ − a·x` with crease set `3x² = a` (`deriv_fold_zero_iff`), two creases `±√(a/3)` for `a > 0` colliding at the cusp `a = 0` (`crease_eq_sqrt_or`, `crease_zero_iff`), the cusp potential `V a b x = x⁴/4 − a·x²/2 − b·x` whose gradient is the fold germ (`deriv_cusp`), the crease as a double root on the cusp curve `(x−r)²(x+2r)` with vanishing discriminant `4a³ = 27b²` (`cusp_curve_factor`, `cusp_discriminant`), and the logistic apex `x = 1/2` as a crease (`deriv_logistic_half`); the brain-folding reading is empirical (see `BRAIN_CREASE.md`) |
| `Wieferich` | core-scaffold | — | the arithmetic crease: Wieferich primes (base 2) as the second-order zero of the Fermat resolvent. Fermat gives `p ∣ 2^(p-1) − 1` (`fermat_dvd`), so the quotient `q_p = (2^(p-1) − 1)/p` is an integer (a resolvable 0/0); Wieferich ⟺ `p² ∣ 2^(p-1) − 1` (`isWieferich_iff_sq_dvd`) ⟺ `p ∣ q_p` (`isWieferich_iff_quotient_dvd`). Kernel-checked instances `1093` and `3511` (`wieferich_1093`, `wieferich_3511`) plus their quotients (`quotient_1093_dvd`, `quotient_3511_dvd`); infinitude OPEN. Carries the first-order no-go: `p ∣ 2^(p-1) − 1` holds for every odd prime while `¬ IsWieferich 3`, so no first-order certificate can detect the crease (`first_order_not_iff_isWieferich`) |
| `Wilson` | core-scaffold | — | the Wilson arithmetic crease: Wilson primes as the second-order zero of the Wilson resolvent. Wilson's theorem gives `p ∣ (p-1)! + 1` for every prime (`wilson_dvd`), a universal first-order zero; a Wilson prime ⟺ `p² ∣ (p-1)! + 1` ⟺ `p ∣ w_p` (`isWilsonPrime_iff_quotient_dvd`). Exact modular factorial `factMod` with bridge `factMod_eq` certifies `562! ≡ −1 (mod 563²)` by `decide`, so all three instances `5`, `13`, `563` are kernel-checked (`wilson_five`, `wilson_thirteen`, `wilson_563`); `first_order_tests_are_universal` puts Fermat's and Wilson's first-order tests side by side. Infinitude OPEN |
| `CriticalAmplitude` | card | C36 | carries card(s) C36 |
| `CriticalLadder` | card | C1 | carries card(s) C1 |
| `Curvature` | rh-research | — | numerical curvature of `xi'` / L-dash positivity at Riemann zeros |
| `DissipativeFlow` | card | C8 | carries card(s) C8 |
| `EcaIsometry` | numerical-cert | — | elementary cellular automaton affine/isometry census (16 affine, 6 isometry classes) |
| `EmergentTime` | card | C11 | carries card(s) C11 |
| `EnstrophyBarrier` | card | C4 | carries card(s) C4 |
| `ErdosMoser` | number-theory-cert | — | bounded Erdős–Moser certificate: the `(3,1)` solution and the empty window `4 ≤ m ≤ 80, 1 ≤ k ≤ 12` certified by kernel `decide` (`em_solution_3_1`, `em_window`), with the power sum tied to Mathlib's `Finset` sum (`powerSum_10_2_eq`); uniqueness of `(3,1)` stays OPEN |
| `ExplicitClaims` | card | C4, C5, C6 | carries card(s) C4, C5, C6 |
| `Factorization` | core-scaffold | — | trial-division factoriser `primeFacGo` and `totientFac`, with the proved invariant that every emitted factor divides the input (`primeFacGo_dvd`) and is prime (`primeFacGo_prime`); the machine-checked product law (`primeFacGo_prod_window`) the number-theory certificates rest on |
| `FiniteScan` | core-scaffold | — | shared finite-scan primitives (`primesUpTo`, `isPrimeB`, `anyPrime`, `absDiff`, `gilbreathHolds`, `firstConstellation`) for the bounded number-theory certificates |
| `FirstCrossing` | card | C8 | carries card(s) C8 |
| `ForceNetwork` | card | C25 | carries card(s) C25 |
| `FrontierCensus` | core-scaffold | — | the synthesised census/crease theory of the arithmetic open-status rows (G30/G31/G32/G34/G36): `census_window_agree` (a window cannot separate two predicates), the `Crease` structure with `refine_sub`/`undershoot`, the compiled Wieferich and Giuga crease instances, a five-row `registry`; decides no open row (see `THE_FRONTIER_CENSUS_SPECIFICATION.md`) |
| `Giuga` | number-theory-cert | — | bounded Giuga certificate: the window `30, 858, 1722` below `10^4`, the instance `66198`, the Carmichael window, and the absence of any Giuga-and-Carmichael number below `10^4` (`giuga_window`, `no_giuga_carmichael_window`); Giuga's conjecture OPEN |
| `Goldbach` | number-theory-cert | — | bounded Goldbach certificate (`goldbach_even_4_to_100000`) plus an explicit open marker |
| `GreatAttractor` | card | C24 | carries card(s) C24 |
| `Hodge` | millennium-cert | — | numerical Hodge record; no settlement claim |
| `InformationBridge` | information-bridge | — | two-state (bit) instance of the Landauer–register schema: `binaryEntropy_half` (`log 2`), `resetCost_two`, `resetCost_eq_neg_orientation` (cost = −k_B T·orientation), `orientation_reset_nonpos`; the physical map `Phi` stays the named missing entity |
| `InformationMixture` | information-bridge | — | classical mixture algebra for a "mixture of two or more" channels: `entropy_mixture` (H(mix) = t·H(a) + (1−t)·H(b) + binaryEntropy t), `binaryEntropy_nonneg`, `entropy_mixture_ge`, `entropy_mixture_half` (a fair mixture adds exactly `log 2`); no measured apparatus is identified |
| `InformationPhi` | information-bridge | — | concrete dynamical 0/0 instance: the relaxation `(1 − r^x)/x` has removable value `−orientation r` (C15), `deficitRate_stateCounting` gives `log n` at `r = 1/n`; the constructed map `Phi` satisfies the claim's three clauses (`Phi_satisfies_claim`); the physical identification stays the missing entity |
| `InformationTime` | information-bridge | — | the time reading of `Phi`: `evolution` is a one-parameter semigroup (`evolution_add`), the orientation is minus the rate (`orientation_evolution_one`), the count is time (`evolution_pow_nat`), and the `{-1,0,+1}` trinity is the decay/stationary/growth arrow (`orientation_arrow`); links `Phi` to `EmergentTime` (C11); no physical claim |
| `Legendre` | number-theory-cert | — | bounded Legendre certificate |
| `Lehmer` | number-theory-cert | — | bounded Lehmer certificate: the empty Lehmer window below `10^4` (`lehmer_window`) and the six 2-Lehmer solutions `561, 1105, 1729, 2465, 6601, 8481`, with `totientFac` cross-checked against Mathlib's `Nat.totient`; Lehmer's problem OPEN |
| `LiouvilleBridge` | card | C22 | carries card(s) C22 |
| `LogicBarrier` | card | C12 | carries card(s) C12 |
| `MarginCrossing` | card | C8 | carries card(s) C8 |
| `MassGap` | millennium-cert | — | Yang-Mills mass-gap crossover borrower (`sinh_div_self_tendsto_one`, `massGapCrossoverRemovable`); the gap itself stays OPEN |
| `MillenniumBridge` | millennium-cert | — | the seven-problem status record (`NOT SETTLED BY THIS PROJECT`, `statuses.length = 7`) |
| `MixtureGrowth` | card | C26 | carries card(s) C26 |
| `NavierStokes` | millennium-cert | — | Serrin-scaling arithmetic plus recorded open statements (`serrinScaling`, `prodiSerrinIntegralFiniteCertified = false`, `nsGlobalRegularityOpen = true`) |
| `NoetherDiscrete` | card | C34 | carries card(s) C34 |
| `OnePattern` | card | C33 | carries card(s) C33 |
| `OnsagerCriterion` | card | C27 | carries card(s) C27 |
| `OrientationBoundedness` | card | C8, C9 | carries card(s) C8, C9 |
| `OrientationLaw` | card | C8, C8-open, C9 | carries card(s) C8, C8-open, C9 |
| `ParabolaVertex` | core-scaffold | — | the conic vertex as a removable 0/0: the radial excess `(r(θ) − r(0))/θ² → l·e/(2(1+e)²)` (`vertex_removable`), `1/8` for the vertex-at-`1/2` parabola (`vertex_removable_one`), the escape direction as a pole, not a removable value (`escape_pole`), the parabola as the extremal conic maximising the coefficient (`vertexCoefficient_le`, equality iff `e = 1`), and the logistic apex/doubling-map reading (`logistic_vertex`, `logistic_conjugacy`) |
| `PerfectNumbers` | number-theory-cert | — | bounded perfect-number certificate: the four known perfect numbers, the even/odd windows, and the complete Mersenne-primality classification for prime exponents `≤ 31` (`perfect_8128`, `even_perfect_window`, `odd_perfect_window`, `mersenne_primality_window`); odd perfect numbers and Mersenne infinitude stay OPEN |
| `Poincare` | millennium-cert | — | numerical Poincare record; no settlement claim |
| `PrimeGaps` | number-theory-cert | — | bounded prime-gap certificates (G15–G20, G22–G24, G26): Fermat numbers and the Euler no-go, Andrica, Oppermann, Brocard, Gilbreath, Polignac, Sophie Germain, Landau `n²+1`, and the k-tuple constellations, each on a finite window (`primeGapsFacts`); the infinitude claims stay OPEN |
| `PvsNP` | millennium-cert | — | contour-recorded wall (`noPolynomialCompilationKnown`, `compilation_wall_recorded`); no settlement claim |
| `QuantitativeContinuation` | card | C4 | carries card(s) C4 |
| `RH.Density` | rh-research | — | Riemann-hypothesis zero-density numerical module |
| `RH.Dominance` | rh-research | — | Riemann-hypothesis dominance numerical module |
| `RH.Hankel` | rh-research | — | Riemann-hypothesis Hankel-matrix numerical module |
| `RH.LiCriterion` | rh-research | — | Riemann-hypothesis Li-criterion module (`li_probe`, `finiteNeverSettles`); explicit open marker |
| `RH.Monotonicity` | rh-research | — | Riemann-hypothesis monotonicity numerical module |
| `RH.NewmanFlow` | rh-research | — | Riemann-hypothesis Newman-flow numerical module |
| `RegularityReduction` | card | C8-open | carries card(s) C8-open |
| `Removable` | core-scaffold | — | the field-agnostic removable-value mechanism (`removable_limit`, `quadratic_removable`, `impedance_crosszero`); base of card C15 |
| `RemovableComplexBridge` | card | C21 | carries card(s) C21 |
| `RemovableValue` | card | C15 | carries card(s) C15 |
| `RoleCollision` | core-scaffold | — | the role-collision lesson (G39): `x = x + 1` read as an *equation* is unsatisfiable (`eq_reading_unsat`, and `eq_reading_implies_zero_eq_one` derives `0 = 1` by ex falso), while read as a *recurrence* it is a state map with closed form `(Step^[t]) x0 = x0 + t` (`recurrence_closed_form`); `recurrence_as_equation_is_collision` pins where the two readings coincide (only at the impossible `0 = 1`), and `readings_differ` proves they are distinct propositions -- the `0 = 1` "paradox" is a symbol used in two incompatible roles (value vs. state, equality vs. assignment) |
| `NumberParity` | number-theory-cert | — | elementary parity: `even_iff_dvd` (even = divisible by 2), `evens_closed_add`/`evens_closed_mul` (the evens are closed under + and *), `doubling_injective` and `even_range_is_doubling` (the evens are exactly the image of doubling), `sum_evens` (the first n evens sum to `n(n+1)`) with `sum_evens_even` (the pile-up never escapes: every partial sum of evens is even), and `two_unique_even_prime` (2 is the unique even prime) |
| `NullAbundance` | number-theory-cert | — | measure-theoretic "nothing as abundant substrate": `singleton_null` (a point is null), `countable_null` (any countable set is null), `rationals_countable`/`rationals_dense`/`rationals_null_and_dense` (the rationals are dense yet null -- presence without magnitude), `evens_countable`/`evens_pile_is_null` (the evens pile up without end and still measure nothing), and `unit_interval_not_null` (uncountable need not be null; `[0,1]` has measure 1) -- infinite count does not buy positive measure |
| `EulerPolynomial` | number-theory-cert | — | G22 no-go: `euler_forty_not_prime` refutes "n^2+n+41 is prime for all n" (fails at n=40 = 41^2), `euler_zero_prime`/`euler_thirtynine_prime` record the long initial run, and `shifted_not_prime_at_pred` gives the **structural reason**: for any `p > 1`, `n^2+n+p` is composite at `n = p-1` (it equals `p^2`, via `shifted_at_pred_eq_square`) |
| `SolarBounds` | information-bridge | — | thermodynamic/accounting ceilings on solar harvesting (no settlement claim): `carnot` (heat-engine efficiency `1 - Tc/Th`), `carnot_mono_source`/`carnot_strict_mono_source` (hotter source is better), `carnot_lt_one` (no perfect engine), `exergy_budget_squeeze`/`more_electric_less_thermal` (fixed budget: more electric strictly squeezes thermal -- no free lunch), `hybridExergy` + `hybrid_beats_pure_pv` (a PV-T mixture never loses on total exergy) -- the provable skeleton of "the most efficient harvesters are mixtures". The full Shockley-Queisser detailed-balance integral is NOT formalized (empirical spectrum input) |
| `ShockleyQueisser` | information-bridge | — | the SQ interior-optimum shape (no settlement claim): `absorbed_strict_decreasing` (higher bandgap absorbs fewer photons) and `voltage_strict_increasing` (higher bandgap extracts more per photon) are opposite monotonicities, so `efficiency_not_monotone`/`efficiency_not_antitone` prove the efficiency has an **interior optimum**; the concrete `efficiency g = (1-g)*g` attains its unique maximum at `g = 1/2` on `[0,1]` (`efficiency_zero_lt_half`, `efficiency_one_lt_half`, `half_is_max`). The empirical AM1.5 detailed-balance integral is NOT formalized |
| `TandemCells` | information-bridge | — | tandem diminishing returns (no settlement claim): `ceiling L r n = L - L*r^n`; `ceiling_monotone` (more junctions never hurt), `ceiling_le_limit` (never exceeds the asymptotic limit -- no free lunch), and `ceiling_increments_shrink` (the gain per added junction is at most the previous, via `ceiling_increment = L*r^n*(1-r)`) -- why a 4th/5th junction buys little |
| `NoUniversalResolve` | information-bridge | — | G21 no-go (a topology brick, no settlement claim): `signStep` (two-sided sign function, a canonical 0/0 at 0) with `signStep_has_no_limit` -- its punctured limit does NOT exist (left limit -1, right limit +1, and a Hausdorff limit would equal both), refuting "every 0/0 resolves"; contrasted with `id_over_id_resolves` (the genuine removable 0/0 `x/x` does resolve to 1) -- removability is a condition, not a universal |
| `SelfSimilarExponents` | card | C31 | carries card(s) C31 |
| `SerrinLadder` | card | C23 | carries card(s) C23 |
| `SerrinSufficiency` | card | C8-open | carries card(s) C8-open |
| `ShadowZeroZero` | core-scaffold | — | the shadow mechanism: the reciprocal mirror `x ↦ 1/x` relocates a removable 0/0 (`0 → ∞`) preserving its value (`shadow_preserves_value`) and, as the term-reciprocal, becomes the `∞/∞` mirror inverting it (`shadow_inverts_value`) |
| `StableBounded` | card | C29 | carries card(s) C29 |
| `SufficiencyLoop` | card | C30 | carries card(s) C30 |
| `TheoryOfEverything` | card | C10 | carries card(s) C10 |
| `TwinPrime` | number-theory-cert | — | bounded twin-prime certificate |
| `UniverseGrowth` | card | C35 | carries card(s) C35 |
| `VanishOrder` | card | C16 | carries card(s) C16 |
| `ZeroFixedPoint` | card | C32 | carries card(s) C32 |
| `ZeroIndex` | card | C19 | carries card(s) C19 |
| `ZeroLink` | card | C13 | carries card(s) C13 |
| `ZeroMechanisms` | card | C20 | carries card(s) C20 |
| `ZeroObject` | card | C14 | carries card(s) C14 |
| `ZeroProbe` | card | C17 | carries card(s) C17 |
| `ZeroValuation` | card | C18 | carries card(s) C18 |
| `ZeroZero` | core-scaffold | — | the 0/0 doctrine's elementary limit family (`entropy_removable_value`, `sin_x_div_tendsto_one`, ...) |

## Coverage

- **Modules on disk:** 82 (all imported by `PunoCalculus.lean`).
- **Card-carrying modules (`card`):** 38.
- **Non-card modules (millennium-cert / rh-research / number-theory-cert / fluid-diagnostic / numerical-cert / cosmology / core-scaffold / information-bridge):** 44.
