# Claim Traceability Map

**Status: machine-checked links.** This file is the join table for
`EXPLICIT_CLAIMS.md`: every claim card (C1 … C38, C10-open) is mapped to the exact
Lean artifact that carries it, the numerical experiment that supports its
empirical half, and the literature that anchors its missing entity. The links are
not prose — they are checked by `test_claim_traceability.py` (see *How this is
verified* at the bottom).

The register's own rule applies: a card is "explicit and factual" only when it has
(i) a precise statement, (ii) a falsifier, and (iii) a source for the entity it is
missing. This map adds the fourth item the register needs to stay honest: a
**resolvable pointer** from each card to the code or literature that carries it.

## Legend

| column | meaning |
|---|---|
| **Card** | ID in `EXPLICIT_CLAIMS.md` |
| **Type** | Theorem / Formal / Empirical / Conjecture (as the register tags it) |
| **Lean artifact** | module `PunoCalculus.<File>` and the named declarations the card quotes |
| **Experiment** | script under `…/06_Miscellaneous_Experiments` (empirical half, if any) |
| **Citation** | literature anchor for the theorem / missing entity |
| **Link** | what the checker asserts (empty = no machine-checkable Lean link, cited only) |

## Map

| Card | Type | Lean artifact | Experiment | Citation | Link |
|---|---|---|---|---|---|
| **C1** | Theorem | `CriticalLadder` (`scalingInvariant_iff`, `sCrit_three`, `sCrit_two`, `sCrit_six`, `thetaAddSCrit`, `sCrit_antitone`, `sCrit_gt_neg_one`, `onsagerExcess_supercritical`) | — | Prodi (1959); Serrin (1962); Koch–Tataru (2001, *Adv. Math.*); Cheskidov–Shvydkoy (2010, arXiv:0708.3067) | Lean declared |
| **C2** | Theorem | — | — | Prodi–Serrin; Escauriaza–Seregin–Šverák (2003) | (cited) |
| **C3** | Conjecture/Open | — | — | Cheskidov–Shvydkoy (2010, arXiv:0708.3067); Ri (2023, arXiv:2307.11312, unrefereed); Bourgain–Pavlovic (2008, JAMS) | — |
| **C4/C6** (extra power) | Formal + Theorem | `ExplicitClaims` (`extra_power_strengthens_above_unit`); support `EnstrophyBarrier`, `QuantitativeContinuation` | — | Tao (2016, 2021); Feng–He–Wang (2025, Lorentz); arXiv:2411.06483; Grujic (2024, JMFM) | Lean |
| **C4/C6** (dim. threshold) | Formal | `ExplicitClaims` (`morrey_threshold`, `physical_embedding_gap`) | `dimension_threshold.py` (ledger-backed) | Adams–Hedberg (1996); Morrey | Lean |
| **C8** | Formal | `ExplicitClaims.mean_le_dimMixture` | `dimension_mixture.py` | Adams–Hedberg (1996); Tao (dimensional regularisation) | Lean + file |
| **C9** | Empirical | — | `dimension_mixture.py` | Constantin (1994); Frisch, *Turbulence* (1995) | file |
| **C10** | Empirical + Formal | `OrientationLaw` (`logGrowth_geometric`, `sign_match`, `orientation_reads_wall`, `logGrowth_of_ratio_eq`, `logGrowth_pos_iff`, `bounded_of_nonpos_logGrowth`, `exists_pos_logGrowth_of_unbounded`, `log_eq_sum_logGrowth`, `bounded_of_bounded_sum_logGrowth`, `unbounded_sum_of_unbounded`, `contLogGrowth_integral`, `continuous_content_bounded`); `DissipativeFlow` (`logGrowth_deriv`, `logGrowth_nonpos_of_dissipative`, `content_le_initial_of_dissipative`); `OrientationBoundedness.orientation_decides_boundedness`; `MarginCrossing`; `FirstCrossing` | `orientation_vs_invariant.py`, `orientation_vs_fractional_s.py`, `fractional_margin_sweep.py`, `fractional_margin_universality.py`, `fractional_margin_window.py`, `fractional_margin_resolution.py` | Beale–Kato–Majda (1984); Constantin–Fefferman (1993); Deng–Hou–Yu (2015) | Lean + files |
| **C10-open** | Conjecture/Open | `OrientationLaw` (`contLogGrowth_integral`, `continuous_content_bounded`, `logGrowth_geometric`, `log_eq_sum_logGrowth`, `bounded_of_bounded_sum_logGrowth`, `unbounded_sum_of_unbounded`); `RegularityReduction` (`regularity_iff_integral_bounded`, `regularity_reduced_to_integral`, `integral_le_of_content_le`, `integral_unbounded_of_content_unbounded`, `content_le_exp_of_integral_le`); `SerrinSufficiency` (`serrinMargin_pos_iff`, `serrinMargin_line`, `serrinMargin_eq_neg_ladder`, `content_le_of_growth_le_weight`, `bounded_on_of_serrinAction`) | `orientation_vs_invariant.py`, `fractional_burgers_margin.py`, `fractional_clm_margin.py` | Beale–Kato–Majda (1984); Constantin–Fefferman (1993); Deng–Hou–Yu (2015); Cheskidov–Shvydkoy (2010) | Lean + files |
| **C11** | Formal | `OrientationBoundedness` (`geometric_bounded_iff`, `orientation_decides_boundedness`, `repelling_iff_unbounded`) | — | register (`GreatAttractor.fixedPoint_logSign`) | Lean |
| **C12** | Formal | `TheoryOfEverything` (`theoryOfEverything`, `twoNumbersClose`, `order_sets_rung`, `orientation_sets_side`) | — | register capstone | Lean |
| **C13** | Formal | `EmergentTime` (`transfer_conserves_total`, `state_determined_by_count`) | — | structural; not a physical claim | Lean |
| **C14** | Formal / Interpretive | `LogicBarrier` (`lawvere_fixedpoint`, `no_surjective_of_no_fixedpoint`, `no_surjective_predicates`, `diagonal_not_mem_range`) | — | Cantor (1891); Gödel (1931); Turing (1936); Lawvere (1969); Baker–Gill–Solovay (1975); Razborov–Rudich (1997); Aaronson–Wigderson (2008) | Lean |
| **C15** | Formal (structural) | `ZeroLink` (`empty_unique_arrow`, `empty_isInitial`, `unit_unique_arrow`, `unit_isTerminal`, `empty_classified_initial`, `unit_classified_terminal`, `zero_links_all`) | — | Awodey, *Category Theory* (2010); Mac Lane (1998); the register's own 0/0 doctrine (`Removable`, `ZeroZero`, `ZeroFixedPoint`) | Lean |
| **C16** | Formal (structural / categorical) | `ZeroObject` (`initial_link`, `terminal_link`, `zero_isInitial`, `zero_isTerminal`, `zero_links_both_ways`, `zero_unique_up_to_iso`, `modules_haveZeroObject`, `modules_exists_zeroObject`, `modules_zero_links`) | — | Awodey (2010); Mac Lane (1998); completes C15 (the zero object in `ModuleCat R`) | Lean |
| **C17** | Formal (analytic ↔ categorical schema) | `RemovableValue` (`IsRemovableValue`, `removable_value_unique`, `existsUnique_iff_exists_and_unique`, `extension_unique`, `removable_exists_unique`, `removable_value_bridge`, `initial_arrow_schema`) | — | standard topology (uniqueness of Hausdorff limits); the register's `Removable` + `ZeroLink` | Lean |
| **C18** | Formal (graded index / valuation) | `VanishOrder` (`VanishesToOrder`, `divideOut`, `vanishes_zero`, `vanishes_succ_imp`, `vanishes_shift`, `HasGrade`, `hasGrade_canonical`, `hasGrade_shift`, `vanishes_antitone`, `grade_unique`, `order_is_graded`) | — | order-of-vanishing / valuation theory; the register's `ZeroFixedPoint` + `GreatAttractor` | Lean |
| **C19** | Formal (analytic mechanism: Probe) | `ZeroProbe` (`ProbeValue`, `probe_identity`, `probe_self`, `probe_value_unique`, `probe_is_removable`) | — | the register's own atlas (Probe mechanism, removable value `1`); `EXPLICIT_CLAIMS` C19 | Lean |
| **C20** | Formal (analytic mechanism: Vanishing Rate) | `ZeroValuation` (`HasOrder`, `hasOrder_one`, `hasOrder_zero_iff`, `hasOrder_mul`, `hasOrder_pow`, `hasOrder_canonical`, `hasOrder_lt_imp_not`, `hasOrder_unique`, `order_is_valuation`) | — | order-of-vanishing / valuation theory; the register's `ZeroFixedPoint` + `VanishOrder` | Lean |
| **C21** | Formal (algebraic mechanism: Index) | `ZeroIndex` (`Index`, `index_one`, `index_additive`, `index_pow`, `index_X_sub_C_self`, `index_pow_self`, `index_canonical`, `index_is_multiplicity`) | — | polynomial algebra (root multiplicity in a UFD); the register's Index mechanism | Lean |
| **C22** | Formal (analytic mechanism / closure) | `ZeroMechanisms` (`abs_div_self_tendsto_right`, `abs_div_self_tendsto_left`, `abs_div_self_no_limit`, `abs_vanish`, `id_vanish`, `anti_class_nonempty`, `mechanisms_close`) | — | the register's atlas (amendment: the anti-class); one-sided-limit theory | Lean |
| **C23** | Formal (analytic bridge / named theorem) | `RemovableComplexBridge` (`IsRemovableValueAt`, `removable_value_exists`, `removable_value_unique`, `exists_unique_removable_value`, `limUnder_eq_of_isRemovableValue`, `canonical_zero_over_zero`) | - | Riemann's removable singularity theorem (Mathlib, `Complex.tendsto_limUnder_of_differentiable_on_punctured_nhds_of_bounded_under`); the register's `RemovableValue` | Lean |
| **C24** | Formal (analytic bridge / named theorem) | `LiouvilleBridge` (`bounded_entire_const`, `bounded_entire_apply_eq`, `bounded_entire_value_unique`, `eq_zero_of_bounded_of_eq_zero`, `bounded_at_infinity_const`) | - | Liouville's theorem (Mathlib, `Differentiable.exists_eq_const_of_bounded`); the register's `RemovableComplexBridge` | Lean |

| **C25** | Formal | `SerrinLadder` (`gnExponent`, `gnExponent_six`, `gnExponent_two`, `gnExponent_three_half`, `gnExponent_ceiling_chain`, `serrinQ`, `serrinQ_six`, `serrinQ_line`, `gnExponent_le_one_iff`, `criticalPower_six_four`, `oneExtraPower`, `criticalPowerIdentity`, `powerClosesCriticalAtSix`) | - | Prodi (1959); Serrin (1962); Sobolev `H^1 -> L^6`; Tao (2016, 2021 quantitative continuation). | Lean |
| **C26** | Formal | `GreatAttractor` (`fixedPoint_distanceRatio`, `fixedPoint_repels`, `fixedPoint_attracts`, `orientation_trichotomy`, `fixedPoint_logRate`, `fixedPoint_logSign`, `orientationDiscriminator`, `criticalSmoothness`, `scalingWeight`, `criticalSmoothness_one`, `criticalSmoothness_shift_order`, `criticalSmoothness_antitone_order`, `scalingWeight_zero_iff`) | - | the register's own `THE_LAW_OF_SINGULARITIES.md` §12.1; `HasDerivAt.tendsto_slope`; `CriticalLadder`. | Lean |
| **C27** | Formal | `ForceNetwork` (`weightedValueLeMax`, `leWeightedValueMin`, `networkValueBetween`, `inertiaDampsChange`) | - | the register's own reading, `PAPER.md` §4–5; on-flow companion `ns_force_network.py`. | Lean |
| **C28** | Formal | `MixtureGrowth` (`normMixtureLeSum`, `mixtureRatioBetween`, `weightedSqBetween`, `spikeCannotLowerRatio`) | - | the register's `dimension_mixture.py`; `norm_add_le`. | Lean |
| **C29** | Formal | `OnsagerCriterion` (`weighted_sum_le`, `spike_of_excess`, `excess_majorizes`) | - | Onsager (1949); the register's `CriticalLadder`. | Lean |
| **C30** | Formal | `ContinuationCriterion` (`exists_upto_of_bounded`, `unbounded_of_first_failure`) | - | Beale–Kato–Majda (1984) continuation criterion; the register's `OnsagerCriterion`, `GreatAttractor`. | Lean |
| **C31** | Formal | `StableBounded` (`attracting_orbit_converges`, `attracting_orbit_bounded`, `monotone_bounded`) | - | Mathlib metrization (`tendsto_iterate_fixedPoint`); the register's `orientation_vs_invariant.py` bridge. | Lean |
| **C32** | Formal | `SufficiencyLoop` (`global_exists_of_mono`, `quadratic_criterion_unavailable`) | - | the register's `EnstrophyBarrier` + `ContinuationCriterion`. | Lean |
| **C33** | Formal | `SelfSimilarExponents` (`BalanceSystem`, `forcedP`, `forcedQ`, `forcedS`, `forcedGamma`, `forcedExponentsSatisfy`, `gammaForced`, `sForced`, `qForcedInPoisson`, `pForcedFromOmegaProduction`, `forcedExponentsUnique`, `secondOrderPower`, `secondOrderPowerPrefactorIndependent`, `advectionTermPower`, `advectionTermPowerKappaIndependent`, `uzCoefficientPowerNIndependent`, `kappaMonotone`, `dynamicalNMonotoneStiffening_powersForced`, `profile_existence_is_open`, `type_ii_naming_not_certified`) | - | Hou, arXiv:2405.10916; `Linear Stability of Candidate Swirl Profiles.md` Frontier 1. | Lean |
| **C34** | Formal | `ZeroFixedPoint` (`fixedPoint_selfSlope`, `identity_selfSlope`, `zero_count_removable`, `zero_count_under`, `zero_count_over`) | - | the register's `THE_LAW_OF_SINGULARITIES.md` §12.1; `Removable`. | Lean |
| **C35** | Formal | `OnePattern` (`criticalCurve_through_ladder`, `ladder_is_order_one`, `theta_add_criticalCurve`, `theta_add_criticalCurve_one`, `scalingWeight_vanishes_family`) | - | the register capstone; `CriticalLadder`, `GreatAttractor`. | Lean |
| **C36** | Formal | `NoetherDiscrete` (`charge_eq_momentum_sub`, `charge_self`, `charge_translation_invariant`, `momentum_from_rate`, `momentum_conserved`, `momentumAt_conserved`, `momentumAt_eq_initial`, `conservationLaw`) | - | Noether, *Invariante Variationsprobleme* (1918); the register's Conservation mechanism (`ZeroMechanisms.lean`). | Lean |
| **C37** | Formal | `UniverseGrowth` (`chargeOn_eq_momentumOn_sub`, `momentumOn_grow`, `momentumOn_grow_eq`, `chargeOn_grow_eq`, `universeGrowth_decomp`, `universeGrowth_conserves`, `chargeOn_universeGrowth_conserves`, `momentumOn_univ`) | - | the register's discrete Noether card C36 (`NoetherDiscrete.lean`); the Conservation mechanism. | Lean |
| **C38** | Formal | `CriticalAmplitude` (`amplitudeRatio_eq`, `orderParameter_at_critical`, `widom_relation`, `rushbrooke_relation`, `josephson_relation`, `fisher_relation`) | - | Widom (1965); Rushbrooke (1963), Josephson (1966), Fisher (1964); the register's Critical Phenomenon mechanism. | Lean |

## Supporting bricks (not cards, but named by cards)

| Brick | Lean artifact | Carries |
|---|---|---|
| Critical ladder arithmetic | `SerrinLadder` (`gnExponent`, `serrinQ_line`, `criticalPowerIdentity`) | C1/C2 ladder |
| Order family through the ladder | `OnePattern.criticalCurve_through_ladder` | C12 `order_sets_rung` |
| Onsager excess | `OnsagerCriterion` (`weighted_sum_le`, `spike_of_excess`) | C3/C4-C6 wall |
| Barrier hierarchy by order | `EnstrophyBarrier`, `QuantitativeContinuation` | C4/C6, C10 |
| Sufficiency loop | `SufficiencyLoop.global_exists_of_mono`, `ContinuationCriterion` | C2/C10-open |
| Attracting ⇒ bounded | `StableBounded` (`attracting_orbit_bounded`, `monotone_bounded`) | C10/C11 |
| Growth by addition | `MixtureGrowth` | C8/C9 |
| Fixed-point orientation | `GreatAttractor` (`fixedPoint_logSign`, `fixedPoint_repels`) | C10/C11 |
| Capstone bundle | `TheoryOfEverything.method_and_margin_barriers` (existence ∧ uniqueness ∧ diagonal) | C10/C10-open/C14 |

## How this is verified

`04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_claim_traceability.py`
asserts, for every row above:

1. each card ID appears in `EXPLICIT_CLAIMS.md`;
2. each named Lean module exists at
   `01_Core_Mathematical_Framework_Lean/01_Lean/PunoCalculus/<File>.lean` and
   contains a declaration line (`theorem`/`lemma`/`def`/`abbrev`) for every quoted
   identifier;
3. each named experiment exists under
   `02_Experimental_Implementations_and_Verification/06_Miscellaneous_Experiments/`;
4. this map (`CLAIM_TRACEABILITY.md`) itself references every card ID, Lean module
   and experiment filename in the table.

The declarations were additionally confirmed to *resolve* (not merely appear) by a
`#check` probe over `PunoCalculus` — all identifiers type-check and the root module
imports every file, so `lake build PunoCalculus` covers them. No card here is a
Millennium result; the wall stays OPEN (card C3 / C10-open).

## Axiom audit

For the *axiom footprint* of every quoted declaration — the transitive list of
axioms each card's Lean link rests on — see **`AXIOM_AUDIT.md`**. It is generated by
`#print axioms` over the `ENTRIES` table of the checker (all 233 quoted declarations,
cards C1 … C38): every footprint is `⊆ {propext, Classical.choice, Quot.sound}`, no
quoted declaration uses `sorryAx`, and nine declarations are axiom-free.

## Related external corpora

This map joins our cards to *our* artifacts. For the **external** axis — where this
repository's modules (including the MillenniumBridge set: `NavierStokes`, `BSD`,
`Hodge`, `MassGap`, `PvsNP`, `LogicBarrier`, `ZeroFixedPoint` … ) touch neighbouring public
mathematical corpora — see **`EXTERNAL_CORPORA_CROSSWALK.md`**. It links, family by
family, to the **[`openai/math`](https://github.com/openai/math)** manuscript
collection (cards C1–C10 touch its family **376**, Navier–Stokes universal computation;
C14 touches its fixed-point/undecidability families **206 / 242 / 328 / 314**), under an
explicit *adjacency ≠ equivalence* rule, and is checked offline by
`test_external_crosswalk.py`.
