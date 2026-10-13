# Claim Traceability Map

**Status: machine-checked links.** This file is the join table for
`EXPLICIT_CLAIMS.md`: every claim card (C1 … C14, C10-open) is mapped to the exact
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
