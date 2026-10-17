"""Claim traceability: every card in ``EXPLICIT_CLAIMS.md`` must point at a real,
resolvable artifact.

`EXPLICIT_CLAIMS.md` distils the register into falsifiable claim cards. This test
closes the last hole: a card may *name* a Lean file and a quoted declaration, but
nothing forced the name to exist. Here every card is mapped (card -> type -> Lean
module + declarations -> experiment -> citation) and each link is asserted:

1. card heading present in `EXPLICIT_CLAIMS.md`;
2. Lean module file present under `.../PunoCalculus/` and imported by the library
   root `PunoCalculus.lean` (so `lake build PunoCalculus` actually compiles it);
3. every quoted identifier is declared (`theorem`/`lemma`/`def`/`abbrev`) in that
   module, and -- when a Lean toolchain and a built library are present -- is
   confirmed to actually *resolve* by a generated `#check` probe (skipped in a
   toolchain-free CI checkout), this pins the source link;
4. every named experiment script exists;
5. the human map `CLAIM_TRACEABILITY.md` references every card, module and script
   in the table (so the map and this test cannot drift).

Run:  python -m pytest 04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_claim_traceability.py -q
"""

import os
import re
import shutil
import subprocess
import tempfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEAN_DIR = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus"
)
LEAN_ROOT = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus.lean"
)
EXP_DIR = os.path.join(
    ROOT,
    "02_Experimental_Implementations_and_Verification",
    "06_Miscellaneous_Experiments",
)
DOC_DIR = os.path.join(
    ROOT,
    "05_Documentation_and_Research_Specifications",
    "05_Complete_Framework_Documentation",
)
CLAIMS_MD = os.path.join(DOC_DIR, "EXPLICIT_CLAIMS.md")
TRACE_MD = os.path.join(DOC_DIR, "CLAIM_TRACEABILITY.md")

# card -> (Lean {module: [declared names]}, [experiment scripts])
# A card may repeat (C4/C6 carries two distinct statements); the same token then
# appears twice, which is fine for link checking.
ENTRIES = [
    ("C1", {
        "CriticalLadder": [
            "scalingInvariant_iff", "sCrit_three", "sCrit_two", "sCrit_six",
            "thetaAddSCrit", "sCrit_antitone", "sCrit_gt_neg_one",
            "onsagerExcess_supercritical",
        ],
    }, ["register_core_certificates.py"]),
    ("C2", {}, []),
    ("C3", {}, []),
    ("C4/C6", {
        "ExplicitClaims": ["extra_power_strengthens_above_unit"],
        "EnstrophyBarrier": [
            "mono_step_bounded", "doubling_succ", "quadratic_step_unbounded",
            "quadratic_no_uniform_bound",
        ],
        "QuantitativeContinuation": [
            "linear_bound", "geometric_bound", "barrier_hierarchy",
            "exists_upto_of_geometric",
        ],
    }, ["register_core_certificates.py"]),
    ("C4/C6", {
        "ExplicitClaims": ["morrey_threshold", "physical_embedding_gap"],
    }, ["dimension_threshold.py"]),
    ("C8", {"ExplicitClaims": ["mean_le_dimMixture"]}, ["dimension_mixture.py"]),
    ("C9", {}, ["dimension_mixture.py"]),
    ("C10", {
        "OrientationLaw": [
            "logGrowth_geometric", "sign_match", "orientation_reads_wall",
            "logGrowth_of_ratio_eq", "logGrowth_pos_iff",
            "bounded_of_nonpos_logGrowth", "exists_pos_logGrowth_of_unbounded",
            "log_eq_sum_logGrowth", "bounded_of_bounded_sum_logGrowth",
            "unbounded_sum_of_unbounded", "contLogGrowth_integral",
            "continuous_content_bounded",
            "boundedOrientation_orientation_sign", "boundedOrientation_ratio_sign",
            "boundedOrientation_geometricOrbit_mem",
            "boundedOrientation_geometricOrbit_strictMono",
            "boundedOrientation_geometricOrbit_strictAnti",
            "boundedOrientation_geometricOrbit_center",
        ],
        "DissipativeFlow": [
            "logGrowth_deriv", "logGrowth_nonpos_of_dissipative",
            "content_le_initial_of_dissipative",
        ],
        "OrientationBoundedness": ["orientation_decides_boundedness"],
        "MarginCrossing": [
            "existsUnique_zero_of_strictAntiOn", "side_of_crossing",
            "margin_existsUnique",
        ],
        "FirstCrossing": [
            "exists_first_zero", "margin_exists_firstCrossing",
        ],
    }, [
        "orientation_vs_invariant.py",
        "orientation_vs_fractional_s.py",
        "fractional_margin_sweep.py",
        "fractional_margin_universality.py",
        "fractional_margin_window.py",
        "fractional_margin_resolution.py",
    ]),
    ("C10-open", {
        "OrientationLaw": [
            "contLogGrowth_integral", "continuous_content_bounded",
            "logGrowth_geometric", "log_eq_sum_logGrowth",
            "bounded_of_bounded_sum_logGrowth", "unbounded_sum_of_unbounded",
        ],
        "RegularityReduction": [
            "regularity_iff_integral_bounded", "regularity_reduced_to_integral",
            "integral_le_of_content_le", "integral_unbounded_of_content_unbounded",
            "content_le_exp_of_integral_le",
        ],
        "SerrinSufficiency": [
            "serrinMargin_pos_iff", "serrinMargin_line",
            "serrinMargin_eq_neg_ladder", "content_le_of_growth_le_weight",
            "bounded_on_of_serrinAction",
        ],
    }, [
        "orientation_vs_invariant.py",
        "fractional_burgers_margin.py",
        "fractional_clm_margin.py",
    ]),
    ("C11", {
        "OrientationBoundedness": [
            "geometric_bounded_iff", "orientation_decides_boundedness",
            "repelling_iff_unbounded",
            "boundedOrientation_floor", "boundedOrientation_midpoint",
            "boundedOrientation_ceiling", "boundedOrientation_floor_midpoint_ceiling",
            "boundedOrientation_antisymm", "boundedOrientation_strictMonoOn",
            "boundedOrientation_sign", "boundedOrientation_reads_the_wall",
            "boundedOrientation_eq_tanh", "boundedOrientation_pow",
            "boundedOrientation_mul", "boundedOrientation_right_inv",
            "boundedOrientation_left_inv", "boundedOrientation_image",
            "boundedOrientation_surjOn", "boundedOrientation_bijOn",
        ],
    }, ["register_ladder_certificates.py"]),
    ("C12", {
        "TheoryOfEverything": [
            "order_sets_rung", "orientation_sets_side", "theoryOfEverything",
            "twoNumbersClose", "method_and_margin_barriers",
            "order_sets_rung_bijective", "orientation_not_injective_on_side",
        ],
    }, ["register_ladder_certificates.py", "theory_of_everything_certificates.py"]),
    ("C13", {
        "EmergentTime": ["transfer_conserves_total", "state_determined_by_count"],
    }, ["register_ladder_certificates.py"]),
    ("C14", {
        "LogicBarrier": [
            "lawvere_fixedpoint", "no_surjective_of_no_fixedpoint",
            "no_surjective_predicates", "diagonal_not_mem_range",
        ],
    }, ["register_criteria_certificates.py"]),
    ("C15", {
        "ZeroLink": [
            "empty_unique_arrow", "empty_isInitial", "unit_unique_arrow",
            "unit_isTerminal", "empty_classified_initial",
            "unit_classified_terminal", "zero_links_all",
        ],
    }, ["zero_mechanism_certificates.py"]),
    ("C16", {
        "ZeroObject": [
            "initial_link", "terminal_link", "zero_isInitial", "zero_isTerminal",
            "zero_links_both_ways", "zero_unique_up_to_iso",
            "modules_haveZeroObject", "modules_exists_zeroObject",
            "modules_zero_links",
        ],
    }, ["zero_mechanism_certificates.py"]),
    ("C17", {
        "RemovableValue": [
            "IsRemovableValue", "removable_value_unique",
            "existsUnique_iff_exists_and_unique", "extension_unique",
            "removable_exists_unique", "removable_value_bridge",
            "initial_arrow_schema",
        ],
    }, ["zero_mechanism_certificates.py"]),
    ("C18", {
        "VanishOrder": [
            "VanishesToOrder", "divideOut", "vanishes_zero", "vanishes_succ_imp",
            "vanishes_shift", "HasGrade", "hasGrade_canonical", "hasGrade_shift",
            "vanishes_antitone", "grade_unique", "order_is_graded",
        ],
    }, ["zero_mechanism_certificates.py"]),
    ("C19", {
        "ZeroProbe": [
            "ProbeValue", "probe_identity", "probe_self", "probe_value_unique",
            "probe_is_removable",
        ],
    }, ["zero_mechanism_certificates.py"]),
    ("C20", {
        "ZeroValuation": [
            "HasOrder", "hasOrder_one", "hasOrder_zero_iff", "hasOrder_mul",
            "hasOrder_pow", "hasOrder_canonical", "hasOrder_lt_imp_not",
            "hasOrder_unique", "order_is_valuation",
        ],
    }, ["zero_mechanism_certificates.py"]),
    ("C21", {
        "ZeroIndex": [
            "Index", "index_one", "index_additive", "index_pow",
            "index_X_sub_C_self", "index_pow_self", "index_canonical",
            "index_is_multiplicity",
        ],
    }, ["zero_mechanism_certificates.py"]),
    ("C22", {
        "ZeroMechanisms": [
            "abs_div_self_tendsto_right", "abs_div_self_tendsto_left",
            "abs_div_self_no_limit", "abs_vanish", "id_vanish",
            "anti_class_nonempty", "mechanisms_close",
        ],
    }, ["zero_mechanism_certificates.py"]),
    ("C23", {
        "RemovableComplexBridge": [
            "IsRemovableValueAt", "removable_value_exists",
            "removable_value_unique", "exists_unique_removable_value",
            "limUnder_eq_of_isRemovableValue", "canonical_zero_over_zero",
        ],
    }, ["zero_mechanism_certificates.py"]),
    ("C24", {
        "LiouvilleBridge": [
            "bounded_entire_const", "bounded_entire_apply_eq",
            "bounded_entire_value_unique", "eq_zero_of_bounded_of_eq_zero",
            "bounded_at_infinity_const",
        ],
    }, ["zero_mechanism_certificates.py"]),
    ("C25", {
        "SerrinLadder": [
            "gnExponent", "gnExponent_six", "gnExponent_two", "gnExponent_three_half",
            "gnExponent_ceiling_chain", "serrinQ", "serrinQ_six", "serrinQ_line",
            "gnExponent_le_one_iff", "criticalPower_six_four", "oneExtraPower",
            "criticalPowerIdentity", "powerClosesCriticalAtSix",
        ],
    }, ["register_ladder_certificates.py"]),
    ("C26", {
        "GreatAttractor": [
            "fixedPoint_distanceRatio", "fixedPoint_repels", "fixedPoint_attracts",
            "orientation_trichotomy", "fixedPoint_logRate", "fixedPoint_logSign",
            "orientationDiscriminator", "criticalSmoothness", "scalingWeight",
            "criticalSmoothness_one", "criticalSmoothness_shift_order",
            "criticalSmoothness_antitone_order", "scalingWeight_zero_iff",
        ],
    }, ["register_ladder_certificates.py"]),
    ("C27", {
        "ForceNetwork": [
            "weightedValueLeMax", "leWeightedValueMin", "networkValueBetween",
            "inertiaDampsChange",
        ],
    }, ["register_criteria_certificates.py"]),
    ("C28", {
        "MixtureGrowth": [
            "normMixtureLeSum", "mixtureRatioBetween", "weightedSqBetween",
            "spikeCannotLowerRatio",
        ],
    }, ["register_criteria_certificates.py"]),
    ("C29", {
        "OnsagerCriterion": [
            "weighted_sum_le", "spike_of_excess", "excess_majorizes",
        ],
    }, ["register_criteria_certificates.py"]),
    ("C30", {
        "ContinuationCriterion": [
            "exists_upto_of_bounded", "unbounded_of_first_failure",
        ],
    }, ["register_criteria_certificates.py"]),
    ("C31", {
        "StableBounded": [
            "attracting_orbit_converges", "attracting_orbit_bounded", "monotone_bounded",
        ],
    }, ["register_criteria_certificates.py"]),
    ("C32", {
        "SufficiencyLoop": [
            "global_exists_of_mono", "quadratic_criterion_unavailable",
        ],
    }, ["register_criteria_certificates.py"]),
    ("C33", {
        "SelfSimilarExponents": [
            "BalanceSystem", "forcedP", "forcedQ", "forcedS", "forcedGamma",
            "forcedExponentsSatisfy", "gammaForced", "sForced", "qForcedInPoisson",
            "pForcedFromOmegaProduction", "forcedExponentsUnique", "secondOrderPower",
            "secondOrderPowerPrefactorIndependent", "advectionTermPower",
            "advectionTermPowerKappaIndependent", "uzCoefficientPowerNIndependent",
            "kappaMonotone", "dynamicalNMonotoneStiffening_powersForced",
            "profile_existence_is_open", "type_ii_naming_not_certified",
        ],
    }, ["register_criteria_certificates.py"]),
    ("C34", {
        "ZeroFixedPoint": [
            "fixedPoint_selfSlope", "identity_selfSlope", "zero_count_removable",
            "zero_count_under", "zero_count_over",
        ],
    }, ["register_criteria_certificates.py"]),
    ("C35", {
        "OnePattern": [
            "criticalCurve_through_ladder", "ladder_is_order_one",
            "theta_add_criticalCurve", "theta_add_criticalCurve_one",
            "scalingWeight_vanishes_family",
        ],
    }, ["register_ladder_certificates.py"]),
    ("C36", {
        "NoetherDiscrete": [
            "charge_eq_momentum_sub", "charge_self",
            "charge_translation_invariant", "momentum_from_rate",
            "momentum_conserved", "momentumAt_conserved",
            "momentumAt_eq_initial", "conservationLaw",
        ],
    }, ["arithmetic_shadow_certificates.py"]),
    ("C37", {
        "UniverseGrowth": [
            "chargeOn_eq_momentumOn_sub", "momentumOn_grow", "momentumOn_grow_eq",
            "chargeOn_grow_eq", "universeGrowth_decomp", "universeGrowth_conserves",
            "chargeOn_universeGrowth_conserves", "momentumOn_univ",
        ],
    }, ["arithmetic_shadow_certificates.py"]),
    ("C38", {
        "CriticalAmplitude": [
            "amplitudeRatio_eq", "orderParameter_at_critical", "widom_relation",
            "rushbrooke_relation", "josephson_relation", "fisher_relation",
        ],
    }, ["arithmetic_shadow_certificates.py"]),
]

def _read(path):
    with open(path, encoding="utf-8") as fp:
        return fp.read()


def _declared(src, name):
    """True if `src` declares `name` with a top-level Lean keyword."""
    pat = re.compile(
        r"(?m)^\s*(?:protected\s+|private\s+|noncomputable\s+|partial\s+|"
        r"unsafe\s+|scoped\s+)*(?:theorem|lemma|def|abbrev|instance)\s+"
        + re.escape(name)
        + r"\b"
    )
    return bool(pat.search(src))


def _card_heading_present(claims, token):
    return bool(
        re.search(r"(?m)^#{2,3}\s*" + re.escape(token) + r"(?=\s|—|$)", claims)
    )


def test_traceability_doc_exists():
    assert os.path.isfile(TRACE_MD), TRACE_MD


def test_every_card_has_a_heading_in_the_claims_register():
    claims = _read(CLAIMS_MD)
    tokens = {tok for tok, _, _ in ENTRIES}
    missing = [t for t in sorted(tokens) if not _card_heading_present(claims, t)]
    assert not missing, f"cards with no heading in EXPLICIT_CLAIMS.md: {missing}"


def test_every_named_lean_module_is_imported_by_the_library_root():
    root_src = _read(LEAN_ROOT)
    modules = {m for _, lean, _ in ENTRIES for m in lean}
    not_imported = [
        m for m in sorted(modules) if f"import PunoCalculus.{m}" not in root_src
    ]
    assert not not_imported, (
        "modules named by cards but not imported by PunoCalculus.lean "
        f"(so never built): {not_imported}"
    )


def test_every_quoted_identifier_is_declared():
    problems = []
    for token, lean, _ in ENTRIES:
        for module, names in lean.items():
            path = os.path.join(LEAN_DIR, module + ".lean")
            if not os.path.isfile(path):
                problems.append(f"{token}: missing module {module}.lean")
                continue
            src = _read(path)
            for name in names:
                if not _declared(src, name):
                    problems.append(f"{token}: {module}.lean does not declare {name}")
    assert not problems, "\n".join(problems)


def _find_lake():
    """Locate the Lean build tool: explicit override, PATH, then elan's default."""
    candidates = []
    override = os.environ.get("LAKE")
    if override:
        candidates.append(override)
    on_path = shutil.which("lake")
    if on_path:
        candidates.append(on_path)
    home = os.path.expanduser("~")
    candidates += [
        os.path.join(home, ".elan", "bin", "lake"),
        os.path.join(home, ".elan", "bin", "lake.exe"),
    ]
    return next((c for c in candidates if c and os.path.isfile(c)), None)


def test_quoted_identifiers_resolve_by_check_probe():
    """Generate `#check PunoCalculus.<module>.<name>` for every quoted declaration
    and assert the Lean compiler resolves every one. Requires a toolchain and a
    built library; skipped in a toolchain-free (CI) checkout so the honesty gates
    stay runnable everywhere."""
    lake = _find_lake()
    if lake is None:
        pytest.skip("no Lean toolchain (`lake`) found; resolve probe skipped")
    lean_dir = os.path.dirname(LEAN_ROOT)
    lib_olean = os.path.join(
        lean_dir, ".lake", "build", "lib", "lean", "PunoCalculus.olean"
    )
    if not os.path.isfile(lib_olean):
        pytest.skip("library not built (no PunoCalculus.olean); run `lake build`")

    lines = ["import PunoCalculus", ""]
    for _token, lean, _ in ENTRIES:
        for module, names in lean.items():
            for name in names:
                lines.append(f"#check PunoCalculus.{module}.{name}")

    fd, probe = tempfile.mkstemp(suffix=".lean", prefix="resolve_probe_")
    os.close(fd)
    try:
        with open(probe, "w", encoding="utf-8", newline="\n") as fp:
            fp.write("\n".join(lines) + "\n")
        proc = subprocess.run(
            [lake, "env", "lean", probe],
            cwd=lean_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert proc.returncode == 0, (
            "the #check probe failed to resolve some quoted declaration(s):\n"
            + (proc.stdout or "")
            + (proc.stderr or "")
        )
    finally:
        os.remove(probe)


def test_mapped_lean_modules_have_no_sorry():
    modules = {m for _, lean, _ in ENTRIES for m in lean}
    offenders = []
    for module in sorted(modules):
        src = _read(os.path.join(LEAN_DIR, module + ".lean"))
        stripped = re.sub(r"`[^`]*`", "", src)  # ignore code spans in docstrings
        if re.search(r"\bsorry\b", stripped):
            offenders.append(module)
    assert not offenders, f"modules containing `sorry`: {offenders}"


def test_every_named_experiment_exists():
    missing = []
    for token, _, exps in ENTRIES:
        for name in exps:
            if not os.path.isfile(os.path.join(EXP_DIR, name)):
                missing.append(f"{token}: {name}")
    assert not missing, "missing experiment scripts:\n" + "\n".join(missing)


def test_traceability_doc_references_every_link():
    doc = _read(TRACE_MD)
    problems = []
    for token, lean, exps in ENTRIES:
        if f"**{token}**" not in doc:
            problems.append(f"map is missing card {token}")
        for module in lean:
            if module not in doc:
                problems.append(f"map is missing module {module}")
        for name in exps:
            if name not in doc:
                problems.append(f"map is missing experiment {name}")
    assert not problems, "\n".join(problems)
