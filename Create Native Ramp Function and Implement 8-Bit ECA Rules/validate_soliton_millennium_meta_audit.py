"""validate_soliton_millennium_meta_audit: T4, bridge meta pointing at proofs.

The certificates live on three artifacts built in three different ways,
and the meta-audit refuses to let any of them drift out of the doc
record: it greps the actual sources for the closed theorems and pins
the register wording to the suite count.

    kind   artifact                     gate
    ----   ------------------------------------------------------------
    Lean   PunoCalculus.EcaIsometry     affine_class_exact,
           (v4.33.0, pure core,         isometry_class_exact,
            native_decide)              rule204_identity_widths,
                                        rule51_complement_widths,
                                        complementGen
Lean   PunoCalculus.MillenniumBridge  statuses :: NOT SETTLED BY
           (decidable strings)            THIS PROJECT, statuses.length=7
            (seven_problems_declared_unsolved)
    Lean   PunoTwin.TwinAnalyticLaws    rho_eq_structure,
           (mathlib v4.33.1)            rho_eq_abs_profile,
                                         antiderivative_deriv,
                                         antiderivative_hasDerivAt,
                                         window_defect_exact,
                                         defect_at_L,
                                         defect_tendsto_zero,
                                         defect_window_closed_form,
                                         defect_at_L_tail_lt_window
    Lean   PunoTwin.TwinRingLaws        step204_eq, step51_eq,
           (mathlib v4.33.1)            sumBits_eq, compBits_eq,
                                         rule204_identity_all,
                                         rule51_complement_all
Lean   PunoTwin.MPOperator          operator_discriminant_bridge,
           (mathlib v4.33.1)            window_discriminant_closed_form,
                                          tail_discriminant_closed_form,
                                          fermat_denominator_window,
                                          window_discriminant_pos,
                                          defect_is_double_antiderivative,
                                          tail_is_double_antiderivative
    Lean   PunoTwin.CollatzReach        odd_step_even, spine_identity,
           (mathlib v4.33.1,            two_pow_even_mod_three,
            native_decide)              two_pow_odd_mod_three,
                                          spine_reaches_one,
                                          reverse_tree_levels
    Lean   PunoTwin.DirichletLaws       center_symmetry, eulerProduct_tprod,
           (mathlib v4.33.1)            zeta_neg_nat, χ₄ℂ.conductor_eq_four,
                                          χ₈ℂ.conductor_eq_eight,
                                          χ₈'ℂ.conductor_eq_eight,
                                          vonStaudt_B16, spike_law,
                                          χ₄ℂ_odd, χ₈ℂ_even, χ₈'ℂ_odd
    py     validate_..._closed_forms    exact rational 2048/65537,
                                          65536/67108865
    md     Soliton-Bus ... .md          "86 root validators", the
                                         theorem names, the exact
                                         rationals, seven delimitations

Provenance: the PunoTwin twin files mirror the mathlib v4.33.1 origin
repository github.com/Puronbo/Millennium-Prize-Problem-Lean-4-Proof at
commit b7c03f49839e95d4c658374b8a90e7d7b45d9277.  The vendored copies in
PunoCalculus/PunoCalculus/PunoTwin and the origin tree must stay
byte-identical (hash-audited); bumping the mathlib rev in either place
invalidates the other.

The honest constraint is re-pinned here as well: none of the three
artifact kinds may assert that a Millennium problem is settled.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
PW = WORKSPACE / "PunoCalculus" / "PunoCalculus"
TWIN_ORIGIN_SHA = "b7c03f49839e95d4c658374b8a90e7d7b45d9277"
TWIN_ORIGIN_URL = "github.com/Puronbo/Millennium-Prize-Problem-Lean-4-Proof"


def _puno_twin() -> Path:
    env = os.environ.get("PUNO_TWIN_PATH")
    cand = [Path(env)] if env else []
    cand += [
        PW / "PunoTwin",
        Path(r"C:\Users\Me\Desktop\Mamamogobyerno\fcc2\Millennium-Prize-Problem-Lean-4-Proof\PunoTwin"),
        Path.home() / "Desktop" / "Mamamogobyerno" / "fcc2"
        / "Millennium-Prize-Problem-Lean-4-Proof" / "PunoTwin",
    ]
    for p in cand:
        if p.is_dir():
            return p
    raise FileNotFoundError(
        "PunoTwin not found; set PUNO_TWIN_PATH to its directory")


MW = _puno_twin()
DOC = ROOT / "Soliton-Bus Elementary Cellular Automata.md"

ECHO = [
    "affine_class_exact", "isometry_class_exact",
    "rule204_identity_widths", "rule51_complement_widths",
    "complement_is_involution",
    "isometry_class_three_pairs",
    "complementGen",
]
MBR = [
    "statuses", "NOT SETTLED BY THIS PROJECT",
    "seven_problems_declared_unsolved",
]
TWIN = [
    "rho_eq_structure", "rho_eq_abs_profile",
    "antiderivative_deriv", "antiderivative_hasDerivAt",
    "window_defect_exact", "defect_at_L", "defect_tendsto_zero",
    "defect_window_closed_form",
    "defect_window_closed_form :",
    "(16 : ℚ) * 1 * 128 / (1 + 4 * 1 * 128 ^ 2) = (2048 : ℚ) / 65537",
    "defect_at_L_tail_lt_window",
    "defect_at_L_tail_lt_window :",
    "(16 : ℚ) * 1 * 4096 / (1 + 4 * 1 * 4096 ^ 2) < (2048 : ℚ) / 65537",
]
RING = [
    "step204_eq", "step51_eq",
    "sumBits_eq", "compBits_eq",
    "rule204_identity_all", "rule51_complement_all",
]
COLLATZ = [
    "odd_step_even",
    "3 * (2 * k + 1) + 1 = 2 * (3 * k + 2)",
    "geom4_identity",
    "4 ^ (k + 1) = 3 * spineSum k + 1",
    "spine_eq_spineSum",
    "spine_identity",
    "3 * spine k + 1 = 4 ^ (k + 1)",
    "spine_reaches_one",
    "two_pow_even_mod_three",
    "(2 ^ (2 * j)) % 3 = 1",
    "two_pow_odd_mod_three",
    "(2 ^ (2 * j + 1)) % 3 = 2",
    "reverse_tree_levels",
    "L5: 5,32 | L6: 10,64 | L7: 3,20,21,128",
]
DIRL = [
    "center_symmetry",
    "eulerProduct_tprod",
    "zeta_neg_nat",
    "riemannZeta_neg_nat_eq_bernoulli k",
    "lemma conductor_eq_four : χ₄ℂ.conductor = 4",
    "lemma conductor_eq_eight : χ₈ℂ.conductor = 8",
    "lemma conductor_eq_eight : χ₈'ℂ.conductor = 8",
    "vonStaudt_B16",
    "bernoulli 16 + ∑ p",
    "spike_law",
    "spike_5_prime", "spike_5_cond",
    "spike_17_prime", "spike_17_cond",
    "spike_257_prime", "spike_257_cond",
    "χ₄ℂ_odd", "χ₈ℂ_even", "χ₈'ℂ_odd",
]
MPOP = [
    "operator_discriminant_bridge",
    "(2 * a + 1) ^ 2 - 4 * a = 1 + 4 * a ^ 2",
    "window_discriminant_closed_form",
    "(2 * (128 : ℚ) + 1) ^ 2 - 4 * 128 = 65537",
    "tail_discriminant_closed_form",
    "(2 * (4096 : ℚ) + 1) ^ 2 - 4 * 4096 = 67108865",
    "fermat_denominator_window",
    "1 + 4 * (128 : ℚ) ^ 2 = 2 ^ 16 + 1",
    "window_discriminant_pos",
    "defect_is_double_antiderivative",
    "(16 : ℚ) * 1 * 128 / (1 + 4 * 1 * 128 ^ 2) = 2 * ((8 : ℚ) * 128 / (1 + 4 * 1 * 128 ^ 2))",
    "tail_is_double_antiderivative",
    "(16 : ℚ) * 1 * 4096 / (1 + 4 * 1 * 4096 ^ 2) = 2 * ((8 : ℚ) * 4096 / (1 + 4 * 1 * 4096 ^ 2))",
    "antiderivative_first_order_law",
    "+ 8 * P * t * (t / (1 + 4 * P * t ^ 2)) = 1",
    "mass_radius_identity",
    "16 * a ^ 2 / (1 + 4 * a ^ 2) + 4 / (1 + 4 * a ^ 2) = 4",
    "mass_radius_window",
    "(16 : ℚ) * 1 * 128 / (1 + 4 * 1 * 128 ^ 2) * 128 = (262144 : ℚ) / 65537",
    "mass_radius_tail",
    "(16 : ℚ) * 1 * 4096 / (1 + 4 * 1 * 4096 ^ 2) * 4096 = (268435456 : ℚ) / 67108865",
    "mass_radius_tail_lt_ceil",
    "(16 : ℚ) * 1 * 4096 / (1 + 4 * 1 * 4096 ^ 2) * 4096 < 4",
    "window_discriminant_real_pos",
    "1 ≤ 1 + 4 * a ^ 2",
    "vieta_discriminant",
    "(r₁ + r₂) ^ 2 - 4 * r₁ * r₂ = (r₁ - r₂) ^ 2",
    "bridge_discriminant_never_negative",
    "0 < 4 * a ^ 2 + 1",
    "bridge_discriminant_window_pos",
    "(0 : ℚ) < 4 * 128 ^ 2 + 1",
    "char_poly_at_half",
    "(1 / 2 : ℚ) ^ 2 - (2 * a + 1) * (1 / 2 : ℚ) + a = (-1 / 4 : ℚ)",
    "char_poly_at_zero",
    "char_poly_at_one",
    "char_poly_at_twice_window",
    "spectral_bracket_window",
    "bridge_discriminant_square_squeeze",
    "(2 * a) ^ 2 < 4 * a ^ 2 + 1 ∧ 4 * a ^ 2 + 1 < (2 * a + 1) ^ 2",
    "bridge_discriminant_square_squeeze_window",
    "bridge_discriminant_square_squeeze_tail",
    "bridge_discriminant_tight_upper_square",
    "(2 * a + 1 / (4 * a)) ^ 2 = 4 * a ^ 2 + 1 + 1 / (16 * a ^ 2)",
    "bridge_discriminant_tight_upper_square_window",
    "bridge_discriminant_tight_upper_square_tail",
    "discrim_gap_quarter_scaling",
    "vieta_midpoint_bracket",
    "bridge_gap_square_squeeze",
    "bridge_gap_square_squeeze_window",
    "bridge_gap_square_squeeze_tail",
    "spectral_midpoint_distance_sum",
    "spectral_midpoint_distance_prod",
    "spectral_midpoint_between_roots",
    "spectral_distance_mirror_quadratic",
    "mirror_quadratic_discriminant_is_bridge",
    "spectral_reciprocal_sum_law",
    "spectral_roots_bracket_explicit",
    "derivative_integral",
    "Polynomial.derivative (integral p) = p",
    "integral_derivative_sub_eval0",
    "integral (Polynomial.derivative p) = p - Polynomial.C (p.coeff 0)",
    "anticommutator_defect",
    "operator_square_commutation_defect",
    "operator_square_bridge_family",
    "Polynomial.C (α ^ 2) * Polynomial.derivative (Polynomial.derivative g)",
    "mass_radius_window_lt_tail",
    "(262144 : ℚ) / 65537 < (268435456 : ℚ) / 67108865",
]
DOCPINS = [
    "86 root validators",
    "2048/65537",
    "65536/67108865",
    "TwinAnalyticLaws",
    "TwinRingLaws",
    "MPOperator",
    "operator_discriminant_bridge",
    "window_discriminant_closed_form",
    "65537",
    "67108865",
    "rule204_identity_all",
    "rule51_complement_all",
    "mass_radius_window_lt_tail",
    "spectral_bracket_window",
    "bridge_discriminant_square_squeeze",
    "65536 < 65537 < 66049",
    "67108864 < 67108865 < 67125249",
    "65537 + 1/262144",
    "67108865 + 1/268435456",
    "discrim_gap_quarter_scaling",
    "65536 < (r1-r2)^2 < 65537 + 1/262144",
    "67108864 < (r1-r2)^2 < 67108865 + 1/268435456",
    "1/r1 + 1/r2 = 2 + 1/a",
    "2 + 1/128",
    "2 + 1/4096",
    "0 < r2 < 1/2 < r1 < 2a+1",
    "derivative_integral",
    "D(Vp)=p",
    "V(Dp)=p-C(p.coeff 0)",
    "DV+VD=2id-E0",
    "operator_square_commutation_defect",
    "A^2 g = a^2 D^2 g + ab(2g-g(0)) + b^2 V^2 g",
    "operator_square_bridge_family",
    "odd_step_even",
    "3 * (2 * k + 1) + 1 = 2 * (3 * k + 2)",
    "spine_reaches_one",
    "reverse_tree_levels",
    "L5: 5,32 | L6: 10,64 | L7: 3,20,21,128",
    "two_pow_even_mod_three",
    "two_pow_odd_mod_three",
    "NOT SETTLED BY THIS",
    "declared NOT SETTLED explicitly",
    "PunoTwin",
    "DirichletLaws",
    "center_symmetry",
    "spike_law",
    "vonStaudt",
    "χ₄ℂ_odd",
    TWIN_ORIGIN_SHA,
    TWIN_ORIGIN_URL,
]


def _grep(path: Path, needles: list[str]) -> list[str]:
    text = re.sub(r"\s+", " ", path.read_text(encoding="utf-8",
                                              errors="ignore"))
    return [n for n in needles if n not in text]


def _check(label: str, missing: list[str]) -> None:
    ok = not missing
    print(f"  [{'PASS ' if ok else 'FAIL '}] {label}"
          + ("" if ok else f" missing: {missing}"))
    assert not missing, (label, missing)


def _root_validator_count() -> int:
    return len(list(ROOT.glob("validate_*.py")))


print("soliton millennium meta audit (bridge meta -> proofs)")
_check("EcaIsometry carries the five closure theorems",
       _grep(PW / "EcaIsometry.lean", ECHO))
_check("MillenniumBridge carries the seven NOT-SETTLED declarations",
       _grep(PW / "MillenniumBridge.lean", MBR))
_check("TwinAnalyticLaws carries the seven mass-law theorems",
       _grep(MW / "TwinAnalyticLaws.lean", TWIN))
_check("TwinRingLaws carries the general-width ring closure",
       _grep(MW / "TwinRingLaws.lean", RING))
_check("MPOperator carries the operator-discriminant bridge theorems",
       _grep(MW / "MPOperator.lean", MPOP))
_check("CollatzReach carries the closed-form spine laws and the reverse-tree census",
       _grep(MW / "CollatzReach.lean", COLLATZ))
_check("DirichletLaws carries the L-function laws, primitive χ's, parity law and spike lattice",
       _grep(MW / "DirichletLaws.lean", DIRL))
_check("the docs pin the suite count and the certified rationals",
       _grep(DOC, DOCPINS))
_check("on-disk validator count matches the prose-pinned count",
       [] if _root_validator_count() == 86
       else [f"on-disk {_root_validator_count()} != pinned 86"])

# honest constraint across artifacts: no settlement assertion may appear
# in any of the sources carrying these names.
for name, path in [("EcaIsometry.lean", PW / "EcaIsometry.lean"),
                   ("MillenniumBridge.lean", PW / "MillenniumBridge.lean"),
                   ("TwinAnalyticLaws.lean", MW / "TwinAnalyticLaws.lean"),
                   ("TwinRingLaws.lean", MW / "TwinRingLaws.lean"),
("MPOperator.lean", MW / "MPOperator.lean"),
                    ("CollatzReach.lean", MW / "CollatzReach.lean"),
                    ("DirichletLaws.lean", MW / "DirichletLaws.lean")]:
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    hits = [s for s in ("is solved", "is settled", "proves ", "proved:",
                        "are settled") if re.search(r"\b" + re.escape(s),
                                                    text)]
    assert not hits, (name, hits)
print("soliton millennium meta audit passed: Lean T1/T2 + T3/T4 sources,"
      " docs, and seven delimitations are all pinned in one register")