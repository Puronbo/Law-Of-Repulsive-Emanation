# Axiom Audit — claim cards C1 … C38

**Status: generated and machine-checked.** This file records the *axiom footprint* of every Lean declaration quoted by a card in `CLAIM_TRACEABILITY.md` — the exact declarations the traceability checker asserts. It answers one question per card: *which axioms does the quoted theorem transitively depend on?*

## Method (reproducible)

The probe `AuditProbe.lean` is generated from the `ENTRIES` table of `04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_claim_traceability.py`: it does `import PunoCalculus` and then `#print axioms` on each quoted declaration. Running it under Lean:

```
cd 01_Core_Mathematical_Framework_Lean/01_Lean
lake env lean AuditProbe.lean
```

yields one footprint per declaration, parsed into the table below
(`depends on axioms: [...]` or `does not depend on any axioms`). The probe is a transient artifact (not tracked); regenerate it from the `ENTRIES` table whenever a card, module, or quoted declaration changes.

## Result

- **Declarations audited:** 233, across the 38 cards C1 … C38 (some cards share declarations, e.g. `OrientationLaw` under C10 and C10-open).
- **Axioms observed across the whole register:** `propext`, `Classical.choice`, `Quot.sound` — the standard Lean/Mathlib foundations. Nothing else.
- **`sorryAx`:** absent. No quoted declaration is proved by `sorry`.
- **Axiom-free declarations:** 9 (`diagonal_not_mem_range`, `lawvere_fixedpoint`, `no_surjective_of_no_fixedpoint`, `no_surjective_predicates`, `existsUnique_iff_exists_and_unique`, `empty_classified_initial`, `unit_classified_terminal`, `profile_existence_is_open`, `type_ii_naming_not_certified`).

So every card that is tagged *Formal* or *Theorem* rests, at worst, on the
three standard axioms — and this is checked for the *specific* declarations the
cards quote, not asserted in prose. The empirical and conjecture cards (C3, C9,
C10-open, C2, C4/C6's open half) carry no Lean link of their own, matching the
register's own tagging.

## Footprint by card

### C1

| declaration | axiom footprint |
|---|---|
| `CriticalLadder.scalingInvariant_iff` | propext, Classical.choice, Quot.sound |
| `CriticalLadder.sCrit_three` | propext, Classical.choice, Quot.sound |
| `CriticalLadder.sCrit_two` | propext, Classical.choice, Quot.sound |
| `CriticalLadder.sCrit_six` | propext, Classical.choice, Quot.sound |
| `CriticalLadder.thetaAddSCrit` | propext, Classical.choice, Quot.sound |
| `CriticalLadder.sCrit_antitone` | propext, Classical.choice, Quot.sound |
| `CriticalLadder.sCrit_gt_neg_one` | propext, Classical.choice, Quot.sound |
| `CriticalLadder.onsagerExcess_supercritical` | propext, Classical.choice, Quot.sound |

### C2

| declaration | axiom footprint |
|---|---|

### C3

| declaration | axiom footprint |
|---|---|

### C4/C6

| declaration | axiom footprint |
|---|---|
| `ExplicitClaims.extra_power_strengthens_above_unit` | propext, Classical.choice, Quot.sound |
| `EnstrophyBarrier.mono_step_bounded` | propext, Classical.choice, Quot.sound |
| `EnstrophyBarrier.doubling_succ` | propext, Classical.choice, Quot.sound |
| `EnstrophyBarrier.quadratic_step_unbounded` | propext, Classical.choice, Quot.sound |
| `EnstrophyBarrier.quadratic_no_uniform_bound` | propext, Classical.choice, Quot.sound |
| `QuantitativeContinuation.linear_bound` | propext, Classical.choice, Quot.sound |
| `QuantitativeContinuation.geometric_bound` | propext, Classical.choice, Quot.sound |
| `QuantitativeContinuation.barrier_hierarchy` | propext, Classical.choice, Quot.sound |
| `QuantitativeContinuation.exists_upto_of_geometric` | propext, Classical.choice, Quot.sound |

### C4/C6

| declaration | axiom footprint |
|---|---|
| `ExplicitClaims.morrey_threshold` | propext, Classical.choice, Quot.sound |
| `ExplicitClaims.physical_embedding_gap` | propext, Classical.choice, Quot.sound |

### C8

| declaration | axiom footprint |
|---|---|
| `ExplicitClaims.mean_le_dimMixture` | propext, Classical.choice, Quot.sound |

### C9

| declaration | axiom footprint |
|---|---|

### C10

| declaration | axiom footprint |
|---|---|
| `OrientationLaw.logGrowth_geometric` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.sign_match` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.orientation_reads_wall` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.logGrowth_of_ratio_eq` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.logGrowth_pos_iff` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.bounded_of_nonpos_logGrowth` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.exists_pos_logGrowth_of_unbounded` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.log_eq_sum_logGrowth` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.bounded_of_bounded_sum_logGrowth` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.unbounded_sum_of_unbounded` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.contLogGrowth_integral` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.continuous_content_bounded` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.boundedOrientation_orientation_sign` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.boundedOrientation_ratio_sign` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.boundedOrientation_geometricOrbit_mem` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.boundedOrientation_geometricOrbit_strictMono` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.boundedOrientation_geometricOrbit_strictAnti` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.boundedOrientation_geometricOrbit_center` | propext, Classical.choice, Quot.sound |
| `DissipativeFlow.logGrowth_deriv` | propext, Classical.choice, Quot.sound |
| `DissipativeFlow.logGrowth_nonpos_of_dissipative` | propext, Classical.choice, Quot.sound |
| `DissipativeFlow.content_le_initial_of_dissipative` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.orientation_decides_boundedness` | propext, Classical.choice, Quot.sound |
| `MarginCrossing.existsUnique_zero_of_strictAntiOn` | propext, Classical.choice, Quot.sound |
| `MarginCrossing.side_of_crossing` | propext, Classical.choice, Quot.sound |
| `MarginCrossing.margin_existsUnique` | propext, Classical.choice, Quot.sound |
| `FirstCrossing.exists_first_zero` | propext, Classical.choice, Quot.sound |
| `FirstCrossing.margin_exists_firstCrossing` | propext, Classical.choice, Quot.sound |

### C10-open

| declaration | axiom footprint |
|---|---|
| `OrientationLaw.contLogGrowth_integral` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.continuous_content_bounded` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.logGrowth_geometric` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.log_eq_sum_logGrowth` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.bounded_of_bounded_sum_logGrowth` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.unbounded_sum_of_unbounded` | propext, Classical.choice, Quot.sound |
| `RegularityReduction.regularity_iff_integral_bounded` | propext, Classical.choice, Quot.sound |
| `RegularityReduction.regularity_reduced_to_integral` | propext, Classical.choice, Quot.sound |
| `RegularityReduction.integral_le_of_content_le` | propext, Classical.choice, Quot.sound |
| `RegularityReduction.integral_unbounded_of_content_unbounded` | propext, Classical.choice, Quot.sound |
| `RegularityReduction.content_le_exp_of_integral_le` | propext, Classical.choice, Quot.sound |
| `SerrinSufficiency.serrinMargin_pos_iff` | propext, Classical.choice, Quot.sound |
| `SerrinSufficiency.serrinMargin_line` | propext, Classical.choice, Quot.sound |
| `SerrinSufficiency.serrinMargin_eq_neg_ladder` | propext, Classical.choice, Quot.sound |
| `SerrinSufficiency.content_le_of_growth_le_weight` | propext, Classical.choice, Quot.sound |
| `SerrinSufficiency.bounded_on_of_serrinAction` | propext, Classical.choice, Quot.sound |

### C11

| declaration | axiom footprint |
|---|---|
| `OrientationBoundedness.geometric_bounded_iff` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.orientation_decides_boundedness` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.repelling_iff_unbounded` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientation_floor` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientation_ceiling` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientation_antisymm` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientation_strictMonoOn` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientation_sign` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientation_reads_the_wall` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientation_eq_tanh` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientation_pow` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.tanh_add` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientation_mul` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientation_right_inv` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientation_left_inv` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientation_image` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientation_bijOn` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientationScale` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientationScale_mem` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientationScale_center` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientationScale_half` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientationScale_mul` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.tanh_eq_exp` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientation_classification` | propext, Classical.choice, Quot.sound |
| `OrientationBoundedness.boundedOrientation_classification_normalized` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.squareOrientation` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.squareOrientation_center` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.squareOrientation_mem` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.squareOrientation_strictMonoOn` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.squareOrientation_antisym` | propext, Classical.choice, Quot.sound |
| `OrientationLaw.squareOrientation_not_scalar_multiple_of_boundedOrientation` | propext, Classical.choice, Quot.sound |

### C12

| declaration | axiom footprint |
|---|---|
| `TheoryOfEverything.order_sets_rung` | propext, Classical.choice, Quot.sound |
| `TheoryOfEverything.orientation_sets_side` | propext, Classical.choice, Quot.sound |
| `TheoryOfEverything.theoryOfEverything` | propext, Classical.choice, Quot.sound |
| `TheoryOfEverything.twoNumbersClose` | propext, Classical.choice, Quot.sound |

### C13

| declaration | axiom footprint |
|---|---|
| `EmergentTime.transfer_conserves_total` | propext, Classical.choice, Quot.sound |
| `EmergentTime.state_determined_by_count` | propext, Classical.choice, Quot.sound |

### C14

| declaration | axiom footprint |
|---|---|
| `LogicBarrier.lawvere_fixedpoint` | none (axiom-free) |
| `LogicBarrier.no_surjective_of_no_fixedpoint` | none (axiom-free) |
| `LogicBarrier.no_surjective_predicates` | none (axiom-free) |
| `LogicBarrier.diagonal_not_mem_range` | none (axiom-free) |

### C15

| declaration | axiom footprint |
|---|---|
| `ZeroLink.empty_unique_arrow` | Quot.sound |
| `ZeroLink.empty_isInitial` | Quot.sound |
| `ZeroLink.unit_unique_arrow` | Quot.sound |
| `ZeroLink.unit_isTerminal` | Quot.sound |
| `ZeroLink.empty_classified_initial` | none (axiom-free) |
| `ZeroLink.unit_classified_terminal` | none (axiom-free) |
| `ZeroLink.zero_links_all` | Quot.sound |

### C16

| declaration | axiom footprint |
|---|---|
| `ZeroObject.initial_link` | propext, Classical.choice, Quot.sound |
| `ZeroObject.terminal_link` | propext, Classical.choice, Quot.sound |
| `ZeroObject.zero_isInitial` | propext, Classical.choice, Quot.sound |
| `ZeroObject.zero_isTerminal` | propext, Classical.choice, Quot.sound |
| `ZeroObject.zero_links_both_ways` | propext, Classical.choice, Quot.sound |
| `ZeroObject.zero_unique_up_to_iso` | Classical.choice |
| `ZeroObject.modules_haveZeroObject` | propext, Quot.sound |
| `ZeroObject.modules_exists_zeroObject` | propext, Quot.sound |
| `ZeroObject.modules_zero_links` | propext, Classical.choice, Quot.sound |

### C17

| declaration | axiom footprint |
|---|---|
| `RemovableValue.IsRemovableValue` | propext, Classical.choice, Quot.sound |
| `RemovableValue.removable_value_unique` | propext, Classical.choice, Quot.sound |
| `RemovableValue.existsUnique_iff_exists_and_unique` | none (axiom-free) |
| `RemovableValue.extension_unique` | propext, Classical.choice, Quot.sound |
| `RemovableValue.removable_exists_unique` | propext, Classical.choice, Quot.sound |
| `RemovableValue.removable_value_bridge` | propext, Classical.choice, Quot.sound |
| `RemovableValue.initial_arrow_schema` | Quot.sound |

### C18

| declaration | axiom footprint |
|---|---|
| `VanishOrder.VanishesToOrder` | propext, Classical.choice, Quot.sound |
| `VanishOrder.divideOut` | propext, Classical.choice, Quot.sound |
| `VanishOrder.vanishes_zero` | propext, Classical.choice, Quot.sound |
| `VanishOrder.vanishes_succ_imp` | propext, Classical.choice, Quot.sound |
| `VanishOrder.vanishes_shift` | propext, Classical.choice, Quot.sound |
| `VanishOrder.HasGrade` | propext, Classical.choice, Quot.sound |
| `VanishOrder.hasGrade_canonical` | propext, Classical.choice, Quot.sound |
| `VanishOrder.hasGrade_shift` | propext, Classical.choice, Quot.sound |
| `VanishOrder.vanishes_antitone` | propext, Classical.choice, Quot.sound |
| `VanishOrder.grade_unique` | propext, Classical.choice, Quot.sound |
| `VanishOrder.order_is_graded` | propext, Classical.choice, Quot.sound |

### C19

| declaration | axiom footprint |
|---|---|
| `ZeroProbe.ProbeValue` | propext, Classical.choice, Quot.sound |
| `ZeroProbe.probe_identity` | propext, Classical.choice, Quot.sound |
| `ZeroProbe.probe_self` | propext, Classical.choice, Quot.sound |
| `ZeroProbe.probe_value_unique` | propext, Classical.choice, Quot.sound |
| `ZeroProbe.probe_is_removable` | propext, Classical.choice, Quot.sound |

### C20

| declaration | axiom footprint |
|---|---|
| `ZeroValuation.HasOrder` | propext, Classical.choice, Quot.sound |
| `ZeroValuation.hasOrder_one` | propext, Classical.choice, Quot.sound |
| `ZeroValuation.hasOrder_zero_iff` | propext, Classical.choice, Quot.sound |
| `ZeroValuation.hasOrder_mul` | propext, Classical.choice, Quot.sound |
| `ZeroValuation.hasOrder_pow` | propext, Classical.choice, Quot.sound |
| `ZeroValuation.hasOrder_canonical` | propext, Classical.choice, Quot.sound |
| `ZeroValuation.hasOrder_lt_imp_not` | propext, Classical.choice, Quot.sound |
| `ZeroValuation.hasOrder_unique` | propext, Classical.choice, Quot.sound |
| `ZeroValuation.order_is_valuation` | propext, Classical.choice, Quot.sound |

### C21

| declaration | axiom footprint |
|---|---|
| `ZeroIndex.Index` | propext, Classical.choice, Quot.sound |
| `ZeroIndex.index_one` | propext, Classical.choice, Quot.sound |
| `ZeroIndex.index_additive` | propext, Classical.choice, Quot.sound |
| `ZeroIndex.index_pow` | propext, Classical.choice, Quot.sound |
| `ZeroIndex.index_X_sub_C_self` | propext, Classical.choice, Quot.sound |
| `ZeroIndex.index_pow_self` | propext, Classical.choice, Quot.sound |
| `ZeroIndex.index_canonical` | propext, Classical.choice, Quot.sound |
| `ZeroIndex.index_is_multiplicity` | propext, Classical.choice, Quot.sound |

### C22

| declaration | axiom footprint |
|---|---|
| `ZeroMechanisms.abs_div_self_tendsto_right` | propext, Classical.choice, Quot.sound |
| `ZeroMechanisms.abs_div_self_tendsto_left` | propext, Classical.choice, Quot.sound |
| `ZeroMechanisms.abs_div_self_no_limit` | propext, Classical.choice, Quot.sound |
| `ZeroMechanisms.abs_vanish` | propext, Classical.choice, Quot.sound |
| `ZeroMechanisms.id_vanish` | propext, Classical.choice, Quot.sound |
| `ZeroMechanisms.anti_class_nonempty` | propext, Classical.choice, Quot.sound |
| `ZeroMechanisms.mechanisms_close` | propext, Classical.choice, Quot.sound |

### C23

| declaration | axiom footprint |
|---|---|
| `RemovableComplexBridge.IsRemovableValueAt` | propext, Classical.choice, Quot.sound |
| `RemovableComplexBridge.removable_value_exists` | propext, Classical.choice, Quot.sound |
| `RemovableComplexBridge.removable_value_unique` | propext, Classical.choice, Quot.sound |
| `RemovableComplexBridge.exists_unique_removable_value` | propext, Classical.choice, Quot.sound |
| `RemovableComplexBridge.limUnder_eq_of_isRemovableValue` | propext, Classical.choice, Quot.sound |
| `RemovableComplexBridge.canonical_zero_over_zero` | propext, Classical.choice, Quot.sound |

### C24

| declaration | axiom footprint |
|---|---|
| `LiouvilleBridge.bounded_entire_const` | propext, Classical.choice, Quot.sound |
| `LiouvilleBridge.bounded_entire_apply_eq` | propext, Classical.choice, Quot.sound |
| `LiouvilleBridge.bounded_entire_value_unique` | propext, Classical.choice, Quot.sound |
| `LiouvilleBridge.eq_zero_of_bounded_of_eq_zero` | propext, Classical.choice, Quot.sound |
| `LiouvilleBridge.bounded_at_infinity_const` | propext, Classical.choice, Quot.sound |

### C25

| declaration | axiom footprint |
|---|---|
| `SerrinLadder.gnExponent` | propext, Classical.choice, Quot.sound |
| `SerrinLadder.gnExponent_six` | propext, Classical.choice, Quot.sound |
| `SerrinLadder.gnExponent_two` | propext, Classical.choice, Quot.sound |
| `SerrinLadder.gnExponent_three_half` | propext, Classical.choice, Quot.sound |
| `SerrinLadder.gnExponent_ceiling_chain` | propext, Classical.choice, Quot.sound |
| `SerrinLadder.serrinQ` | propext, Classical.choice, Quot.sound |
| `SerrinLadder.serrinQ_six` | propext, Classical.choice, Quot.sound |
| `SerrinLadder.serrinQ_line` | propext, Classical.choice, Quot.sound |
| `SerrinLadder.gnExponent_le_one_iff` | propext, Classical.choice, Quot.sound |
| `SerrinLadder.criticalPower_six_four` | propext, Classical.choice, Quot.sound |
| `SerrinLadder.oneExtraPower` | propext, Classical.choice, Quot.sound |
| `SerrinLadder.criticalPowerIdentity` | propext, Classical.choice, Quot.sound |
| `SerrinLadder.powerClosesCriticalAtSix` | propext, Classical.choice, Quot.sound |

### C26

| declaration | axiom footprint |
|---|---|
| `GreatAttractor.fixedPoint_distanceRatio` | propext, Classical.choice, Quot.sound |
| `GreatAttractor.fixedPoint_repels` | propext, Classical.choice, Quot.sound |
| `GreatAttractor.fixedPoint_attracts` | propext, Classical.choice, Quot.sound |
| `GreatAttractor.orientation_trichotomy` | propext, Classical.choice, Quot.sound |
| `GreatAttractor.fixedPoint_logRate` | propext, Classical.choice, Quot.sound |
| `GreatAttractor.fixedPoint_logSign` | propext, Classical.choice, Quot.sound |
| `GreatAttractor.orientationDiscriminator` | propext, Classical.choice, Quot.sound |
| `GreatAttractor.criticalSmoothness` | propext, Classical.choice, Quot.sound |
| `GreatAttractor.scalingWeight` | propext, Classical.choice, Quot.sound |
| `GreatAttractor.criticalSmoothness_one` | propext, Classical.choice, Quot.sound |
| `GreatAttractor.criticalSmoothness_shift_order` | propext, Classical.choice, Quot.sound |
| `GreatAttractor.criticalSmoothness_antitone_order` | propext, Classical.choice, Quot.sound |
| `GreatAttractor.scalingWeight_zero_iff` | propext, Classical.choice, Quot.sound |

### C27

| declaration | axiom footprint |
|---|---|
| `ForceNetwork.weightedValueLeMax` | propext, Classical.choice, Quot.sound |
| `ForceNetwork.leWeightedValueMin` | propext, Classical.choice, Quot.sound |
| `ForceNetwork.networkValueBetween` | propext, Classical.choice, Quot.sound |
| `ForceNetwork.inertiaDampsChange` | propext, Classical.choice, Quot.sound |

### C28

| declaration | axiom footprint |
|---|---|
| `MixtureGrowth.normMixtureLeSum` | propext, Classical.choice, Quot.sound |
| `MixtureGrowth.mixtureRatioBetween` | propext, Classical.choice, Quot.sound |
| `MixtureGrowth.weightedSqBetween` | propext, Classical.choice, Quot.sound |
| `MixtureGrowth.spikeCannotLowerRatio` | propext, Classical.choice, Quot.sound |

### C29

| declaration | axiom footprint |
|---|---|
| `OnsagerCriterion.weighted_sum_le` | propext, Classical.choice, Quot.sound |
| `OnsagerCriterion.spike_of_excess` | propext, Classical.choice, Quot.sound |
| `OnsagerCriterion.excess_majorizes` | propext, Classical.choice, Quot.sound |

### C30

| declaration | axiom footprint |
|---|---|
| `ContinuationCriterion.exists_upto_of_bounded` | propext, Classical.choice, Quot.sound |
| `ContinuationCriterion.unbounded_of_first_failure` | propext, Classical.choice, Quot.sound |

### C31

| declaration | axiom footprint |
|---|---|
| `StableBounded.attracting_orbit_converges` | propext, Classical.choice, Quot.sound |
| `StableBounded.attracting_orbit_bounded` | propext, Classical.choice, Quot.sound |
| `StableBounded.monotone_bounded` | propext, Classical.choice, Quot.sound |

### C32

| declaration | axiom footprint |
|---|---|
| `SufficiencyLoop.global_exists_of_mono` | propext, Classical.choice, Quot.sound |
| `SufficiencyLoop.quadratic_criterion_unavailable` | propext, Classical.choice, Quot.sound |

### C33

| declaration | axiom footprint |
|---|---|
| `SelfSimilarExponents.BalanceSystem` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.forcedP` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.forcedQ` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.forcedS` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.forcedGamma` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.forcedExponentsSatisfy` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.gammaForced` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.sForced` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.qForcedInPoisson` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.pForcedFromOmegaProduction` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.forcedExponentsUnique` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.secondOrderPower` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.secondOrderPowerPrefactorIndependent` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.advectionTermPower` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.advectionTermPowerKappaIndependent` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.uzCoefficientPowerNIndependent` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.kappaMonotone` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.dynamicalNMonotoneStiffening_powersForced` | propext, Classical.choice, Quot.sound |
| `SelfSimilarExponents.profile_existence_is_open` | none (axiom-free) |
| `SelfSimilarExponents.type_ii_naming_not_certified` | none (axiom-free) |

### C34

| declaration | axiom footprint |
|---|---|
| `ZeroFixedPoint.fixedPoint_selfSlope` | propext, Classical.choice, Quot.sound |
| `ZeroFixedPoint.identity_selfSlope` | propext, Classical.choice, Quot.sound |
| `ZeroFixedPoint.zero_count_removable` | propext, Classical.choice, Quot.sound |
| `ZeroFixedPoint.zero_count_under` | propext, Classical.choice, Quot.sound |
| `ZeroFixedPoint.zero_count_over` | propext, Classical.choice, Quot.sound |

### C35

| declaration | axiom footprint |
|---|---|
| `OnePattern.criticalCurve_through_ladder` | propext, Classical.choice, Quot.sound |
| `OnePattern.ladder_is_order_one` | propext, Classical.choice, Quot.sound |
| `OnePattern.theta_add_criticalCurve` | propext, Classical.choice, Quot.sound |
| `OnePattern.theta_add_criticalCurve_one` | propext, Classical.choice, Quot.sound |
| `OnePattern.scalingWeight_vanishes_family` | propext, Classical.choice, Quot.sound |

### C36

| declaration | axiom footprint |
|---|---|
| `NoetherDiscrete.charge_eq_momentum_sub` | propext, Classical.choice, Quot.sound |
| `NoetherDiscrete.charge_self` | propext, Classical.choice, Quot.sound |
| `NoetherDiscrete.charge_translation_invariant` | propext, Classical.choice, Quot.sound |
| `NoetherDiscrete.momentum_from_rate` | propext, Classical.choice, Quot.sound |
| `NoetherDiscrete.momentum_conserved` | propext, Classical.choice, Quot.sound |
| `NoetherDiscrete.momentumAt_conserved` | propext, Classical.choice, Quot.sound |
| `NoetherDiscrete.momentumAt_eq_initial` | propext, Classical.choice, Quot.sound |
| `NoetherDiscrete.conservationLaw` | propext, Classical.choice, Quot.sound |

### C37

| declaration | axiom footprint |
|---|---|
| `UniverseGrowth.chargeOn_eq_momentumOn_sub` | propext, Classical.choice, Quot.sound |
| `UniverseGrowth.momentumOn_grow` | propext, Classical.choice, Quot.sound |
| `UniverseGrowth.momentumOn_grow_eq` | propext, Classical.choice, Quot.sound |
| `UniverseGrowth.chargeOn_grow_eq` | propext, Classical.choice, Quot.sound |
| `UniverseGrowth.universeGrowth_decomp` | propext, Classical.choice, Quot.sound |
| `UniverseGrowth.universeGrowth_conserves` | propext, Classical.choice, Quot.sound |
| `UniverseGrowth.chargeOn_universeGrowth_conserves` | propext, Classical.choice, Quot.sound |
| `UniverseGrowth.momentumOn_univ` | propext, Classical.choice, Quot.sound |

### C38

| declaration | axiom footprint |
|---|---|
| `CriticalAmplitude.amplitudeRatio_eq` | propext, Classical.choice, Quot.sound |
| `CriticalAmplitude.orderParameter_at_critical` | propext, Classical.choice, Quot.sound |
| `CriticalAmplitude.widom_relation` | propext, Classical.choice, Quot.sound |
| `CriticalAmplitude.rushbrooke_relation` | propext, Classical.choice, Quot.sound |
| `CriticalAmplitude.josephson_relation` | propext, Classical.choice, Quot.sound |
| `CriticalAmplitude.fisher_relation` | propext, Classical.choice, Quot.sound |
