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
   module -- the declaration is confirmed to *resolve* separately by a `#check`
   probe, this pins the source link;
4. every named experiment script exists;
5. the human map `CLAIM_TRACEABILITY.md` references every card, module and script
   in the table (so the map and this test cannot drift).

Run:  python -m pytest 04_Testing_and_Validation_Suite/03_0_0_Framework_Validation/test_claim_traceability.py -q
"""

import os
import re

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
    }, []),
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
    }, []),
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
        ],
    }, []),
    ("C12", {
        "TheoryOfEverything": [
            "order_sets_rung", "orientation_sets_side", "theoryOfEverything",
            "twoNumbersClose",
        ],
    }, []),
    ("C13", {
        "EmergentTime": ["transfer_conserves_total", "state_determined_by_count"],
    }, []),
    ("C14", {
        "LogicBarrier": [
            "lawvere_fixedpoint", "no_surjective_of_no_fixedpoint",
            "no_surjective_predicates", "diagonal_not_mem_range",
        ],
    }, []),
    ("C15", {
        "ZeroLink": [
            "empty_unique_arrow", "empty_isInitial", "unit_unique_arrow",
            "unit_isTerminal", "empty_classified_initial",
            "unit_classified_terminal", "zero_links_all",
        ],
    }, []),
    ("C16", {
        "ZeroObject": [
            "initial_link", "terminal_link", "zero_isInitial", "zero_isTerminal",
            "zero_links_both_ways", "zero_unique_up_to_iso",
            "modules_haveZeroObject", "modules_exists_zeroObject",
            "modules_zero_links",
        ],
    }, []),
    ("C17", {
        "RemovableValue": [
            "IsRemovableValue", "removable_value_unique",
            "existsUnique_iff_exists_and_unique", "extension_unique",
            "removable_exists_unique", "removable_value_bridge",
            "initial_arrow_schema",
        ],
    }, []),
    ("C18", {
        "VanishOrder": [
            "VanishesToOrder", "divideOut", "vanishes_zero", "vanishes_succ_imp",
            "vanishes_shift", "HasGrade", "hasGrade_canonical", "hasGrade_shift",
            "vanishes_antitone", "grade_unique", "order_is_graded",
        ],
    }, []),
    ("C19", {
        "ZeroProbe": [
            "ProbeValue", "probe_identity", "probe_self", "probe_value_unique",
            "probe_is_removable",
        ],
    }, []),
    ("C20", {
        "ZeroValuation": [
            "HasOrder", "hasOrder_one", "hasOrder_zero_iff", "hasOrder_mul",
            "hasOrder_pow", "hasOrder_canonical", "hasOrder_lt_imp_not",
            "hasOrder_unique", "order_is_valuation",
        ],
    }, []),
    ("C21", {
        "ZeroIndex": [
            "Index", "index_one", "index_additive", "index_pow",
            "index_X_sub_C_self", "index_pow_self", "index_canonical",
            "index_is_multiplicity",
        ],
    }, []),
    ("C22", {
        "ZeroMechanisms": [
            "abs_div_self_tendsto_right", "abs_div_self_tendsto_left",
            "abs_div_self_no_limit", "abs_vanish", "id_vanish",
            "anti_class_nonempty", "mechanisms_close",
        ],
    }, []),
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
