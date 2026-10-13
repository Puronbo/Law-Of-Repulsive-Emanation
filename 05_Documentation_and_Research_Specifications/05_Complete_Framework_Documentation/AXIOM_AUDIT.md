# Axiom Audit — claim cards C1 … C18

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

- **Declarations audited:** 97, across the 17 cards C1 … C18 (some cards share declarations, e.g. `OrientationLaw` under C10 and C10-open).
- **Axioms observed across the whole register:** `propext`, `Classical.choice`, `Quot.sound` — the standard Lean/Mathlib foundations. Nothing else.
- **`sorryAx`:** absent. No quoted declaration is proved by `sorry`.
- **Axiom-free declarations:** 7 (`diagonal_not_mem_range`, `lawvere_fixedpoint`, `no_surjective_of_no_fixedpoint`, `no_surjective_predicates`, `existsUnique_iff_exists_and_unique`, `empty_classified_initial`, `unit_classified_terminal`).

So every card that is tagged *Formal* or *Theorem* rests, at worst, on the
three standard axioms — and this is checked for the *specific* declarations the
cards quote, not asserted in prose. The empirical and conjecture cards (C3, C9,
C10-open, C2, C4/C6's open half) carry no Lean link of their own, matching the
register's own tagging.

## Footprint by card

### C1

| declaration | axiom footprint |
|---|---|
| `CriticalLadder.scalingInvariant_iff` | `propext`, `Classical.choice`, `Quot.sound` |
| `CriticalLadder.sCrit_three` | `propext`, `Classical.choice`, `Quot.sound` |
| `CriticalLadder.sCrit_two` | `propext`, `Classical.choice`, `Quot.sound` |
| `CriticalLadder.sCrit_six` | `propext`, `Classical.choice`, `Quot.sound` |
| `CriticalLadder.thetaAddSCrit` | `propext`, `Classical.choice`, `Quot.sound` |
| `CriticalLadder.sCrit_antitone` | `propext`, `Classical.choice`, `Quot.sound` |
| `CriticalLadder.sCrit_gt_neg_one` | `propext`, `Classical.choice`, `Quot.sound` |
| `CriticalLadder.onsagerExcess_supercritical` | `propext`, `Classical.choice`, `Quot.sound` |

### C2

| declaration | axiom footprint |
|---|---|

### C3

| declaration | axiom footprint |
|---|---|

### C4/C6

| declaration | axiom footprint |
|---|---|
| `ExplicitClaims.extra_power_strengthens_above_unit` | `propext`, `Classical.choice`, `Quot.sound` |
| `EnstrophyBarrier.mono_step_bounded` | `propext`, `Classical.choice`, `Quot.sound` |
| `EnstrophyBarrier.doubling_succ` | `propext`, `Classical.choice`, `Quot.sound` |
| `EnstrophyBarrier.quadratic_step_unbounded` | `propext`, `Classical.choice`, `Quot.sound` |
| `EnstrophyBarrier.quadratic_no_uniform_bound` | `propext`, `Classical.choice`, `Quot.sound` |
| `QuantitativeContinuation.linear_bound` | `propext`, `Classical.choice`, `Quot.sound` |
| `QuantitativeContinuation.geometric_bound` | `propext`, `Classical.choice`, `Quot.sound` |
| `QuantitativeContinuation.barrier_hierarchy` | `propext`, `Classical.choice`, `Quot.sound` |
| `QuantitativeContinuation.exists_upto_of_geometric` | `propext`, `Classical.choice`, `Quot.sound` |

### C4/C6

| declaration | axiom footprint |
|---|---|
| `ExplicitClaims.morrey_threshold` | `propext`, `Classical.choice`, `Quot.sound` |
| `ExplicitClaims.physical_embedding_gap` | `propext`, `Classical.choice`, `Quot.sound` |

### C8

| declaration | axiom footprint |
|---|---|
| `ExplicitClaims.mean_le_dimMixture` | `propext`, `Classical.choice`, `Quot.sound` |

### C9

| declaration | axiom footprint |
|---|---|

### C10

| declaration | axiom footprint |
|---|---|
| `OrientationLaw.logGrowth_geometric` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.sign_match` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.orientation_reads_wall` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.logGrowth_of_ratio_eq` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.logGrowth_pos_iff` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.bounded_of_nonpos_logGrowth` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.exists_pos_logGrowth_of_unbounded` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.log_eq_sum_logGrowth` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.bounded_of_bounded_sum_logGrowth` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.unbounded_sum_of_unbounded` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.contLogGrowth_integral` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.continuous_content_bounded` | `propext`, `Classical.choice`, `Quot.sound` |
| `DissipativeFlow.logGrowth_deriv` | `propext`, `Classical.choice`, `Quot.sound` |
| `DissipativeFlow.logGrowth_nonpos_of_dissipative` | `propext`, `Classical.choice`, `Quot.sound` |
| `DissipativeFlow.content_le_initial_of_dissipative` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationBoundedness.orientation_decides_boundedness` | `propext`, `Classical.choice`, `Quot.sound` |
| `MarginCrossing.existsUnique_zero_of_strictAntiOn` | `propext`, `Classical.choice`, `Quot.sound` |
| `MarginCrossing.side_of_crossing` | `propext`, `Classical.choice`, `Quot.sound` |
| `MarginCrossing.margin_existsUnique` | `propext`, `Classical.choice`, `Quot.sound` |
| `FirstCrossing.exists_first_zero` | `propext`, `Classical.choice`, `Quot.sound` |
| `FirstCrossing.margin_exists_firstCrossing` | `propext`, `Classical.choice`, `Quot.sound` |

### C10-open

| declaration | axiom footprint |
|---|---|
| `OrientationLaw.contLogGrowth_integral` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.continuous_content_bounded` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.logGrowth_geometric` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.log_eq_sum_logGrowth` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.bounded_of_bounded_sum_logGrowth` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationLaw.unbounded_sum_of_unbounded` | `propext`, `Classical.choice`, `Quot.sound` |
| `RegularityReduction.regularity_iff_integral_bounded` | `propext`, `Classical.choice`, `Quot.sound` |
| `RegularityReduction.regularity_reduced_to_integral` | `propext`, `Classical.choice`, `Quot.sound` |
| `RegularityReduction.integral_le_of_content_le` | `propext`, `Classical.choice`, `Quot.sound` |
| `RegularityReduction.integral_unbounded_of_content_unbounded` | `propext`, `Classical.choice`, `Quot.sound` |
| `RegularityReduction.content_le_exp_of_integral_le` | `propext`, `Classical.choice`, `Quot.sound` |
| `SerrinSufficiency.serrinMargin_pos_iff` | `propext`, `Classical.choice`, `Quot.sound` |
| `SerrinSufficiency.serrinMargin_line` | `propext`, `Classical.choice`, `Quot.sound` |
| `SerrinSufficiency.serrinMargin_eq_neg_ladder` | `propext`, `Classical.choice`, `Quot.sound` |
| `SerrinSufficiency.content_le_of_growth_le_weight` | `propext`, `Classical.choice`, `Quot.sound` |
| `SerrinSufficiency.bounded_on_of_serrinAction` | `propext`, `Classical.choice`, `Quot.sound` |

### C11

| declaration | axiom footprint |
|---|---|
| `OrientationBoundedness.geometric_bounded_iff` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationBoundedness.orientation_decides_boundedness` | `propext`, `Classical.choice`, `Quot.sound` |
| `OrientationBoundedness.repelling_iff_unbounded` | `propext`, `Classical.choice`, `Quot.sound` |

### C12

| declaration | axiom footprint |
|---|---|
| `TheoryOfEverything.order_sets_rung` | `propext`, `Classical.choice`, `Quot.sound` |
| `TheoryOfEverything.orientation_sets_side` | `propext`, `Classical.choice`, `Quot.sound` |
| `TheoryOfEverything.theoryOfEverything` | `propext`, `Classical.choice`, `Quot.sound` |
| `TheoryOfEverything.twoNumbersClose` | `propext`, `Classical.choice`, `Quot.sound` |

### C13

| declaration | axiom footprint |
|---|---|
| `EmergentTime.transfer_conserves_total` | `propext`, `Classical.choice`, `Quot.sound` |
| `EmergentTime.state_determined_by_count` | `propext`, `Classical.choice`, `Quot.sound` |

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
| `ZeroLink.empty_unique_arrow` | `Quot.sound` |
| `ZeroLink.empty_isInitial` | `Quot.sound` |
| `ZeroLink.unit_unique_arrow` | `Quot.sound` |
| `ZeroLink.unit_isTerminal` | `Quot.sound` |
| `ZeroLink.empty_classified_initial` | none (axiom-free) |
| `ZeroLink.unit_classified_terminal` | none (axiom-free) |
| `ZeroLink.zero_links_all` | `Quot.sound` |

### C16

| declaration | axiom footprint |
|---|---|
| `ZeroObject.initial_link` | `propext`, `Classical.choice`, `Quot.sound` |
| `ZeroObject.terminal_link` | `propext`, `Classical.choice`, `Quot.sound` |
| `ZeroObject.zero_isInitial` | `propext`, `Classical.choice`, `Quot.sound` |
| `ZeroObject.zero_isTerminal` | `propext`, `Classical.choice`, `Quot.sound` |
| `ZeroObject.zero_links_both_ways` | `propext`, `Classical.choice`, `Quot.sound` |
| `ZeroObject.zero_unique_up_to_iso` | `Classical.choice` |
| `ZeroObject.modules_haveZeroObject` | `propext`, `Quot.sound` |
| `ZeroObject.modules_exists_zeroObject` | `propext`, `Quot.sound` |
| `ZeroObject.modules_zero_links` | `propext`, `Classical.choice`, `Quot.sound` |

### C17

| declaration | axiom footprint |
|---|---|
| `RemovableValue.IsRemovableValue` | `propext`, `Classical.choice`, `Quot.sound` |
| `RemovableValue.removable_value_unique` | `propext`, `Classical.choice`, `Quot.sound` |
| `RemovableValue.existsUnique_iff_exists_and_unique` | none (axiom-free) |
| `RemovableValue.extension_unique` | `propext`, `Classical.choice`, `Quot.sound` |
| `RemovableValue.removable_exists_unique` | `propext`, `Classical.choice`, `Quot.sound` |
| `RemovableValue.removable_value_bridge` | `propext`, `Classical.choice`, `Quot.sound` |
| `RemovableValue.initial_arrow_schema` | `Quot.sound` |

### C18

| declaration | axiom footprint |
|---|---|
| `VanishOrder.VanishesToOrder` | `propext`, `Classical.choice`, `Quot.sound` |
| `VanishOrder.divideOut` | `propext`, `Classical.choice`, `Quot.sound` |
| `VanishOrder.vanishes_zero` | `propext`, `Classical.choice`, `Quot.sound` |
| `VanishOrder.vanishes_succ_imp` | `propext`, `Classical.choice`, `Quot.sound` |
| `VanishOrder.vanishes_shift` | `propext`, `Classical.choice`, `Quot.sound` |
| `VanishOrder.HasGrade` | `propext`, `Classical.choice`, `Quot.sound` |
| `VanishOrder.hasGrade_canonical` | `propext`, `Classical.choice`, `Quot.sound` |
| `VanishOrder.hasGrade_shift` | `propext`, `Classical.choice`, `Quot.sound` |
| `VanishOrder.vanishes_antitone` | `propext`, `Classical.choice`, `Quot.sound` |
| `VanishOrder.grade_unique` | `propext`, `Classical.choice`, `Quot.sound` |
| `VanishOrder.order_is_graded` | `propext`, `Classical.choice`, `Quot.sound` |

## Scope and honesty

This audits only the declarations each card *quotes* (the traceability-checked
set), not every theorem in every module; other in-module lemmas are helpers whose
axioms are absorbed transitively by the quoted capstone where one exists. The
three axioms are foundational, not mathematical hypotheses: `propext` (propositional extensionality), `Classical.choice` (choice / excluded middle), `Quot.sound` (quotient soundness). Their presence is expected wherever classical
reasoning or quotients enter; their *absence* (the axiom-free declarations above)
marks the fully constructive core. No Millennium problem is touched anywhere in
this register; the wall stays OPEN.
