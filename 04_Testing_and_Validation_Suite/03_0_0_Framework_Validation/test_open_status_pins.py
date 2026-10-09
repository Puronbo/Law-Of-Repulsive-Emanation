"""
Open-status pins for the P1 statement-grade formalizations (roadmap items 4-6)
plus the closed path-drift defect (P2).

These tests pin the HONEST side of each artifact: the finite computations are
recorded, and every claim of resolution is asserted absent.  They are
deliberately string/status pins, not value pins -- the value pins live in
test_solvable_theorems.py.

Run:  python -m pytest test_open_status_pins.py -q
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(
    ROOT, "03_Data_and_Observational_Resources", "02_Experimental_Data_Collections"
)
LEAN_DIR = os.path.join(
    ROOT, "01_Core_Mathematical_Framework_Lean", "01_Lean", "PunoCalculus"
)
EXPERIMENTS_DIR = os.path.join(
    ROOT, "02_Experimental_Implementations_and_Verification"
)


def load(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as fp:
        return json.load(fp)


def _lean(rel):
    with open(os.path.join(LEAN_DIR, rel), encoding="utf-8") as fp:
        return fp.read()


def _script(rel):
    with open(os.path.join(EXPERIMENTS_DIR, rel), encoding="utf-8") as fp:
        return fp.read()


def test_p_np_contour_honest_wall_pinned():
    d = load("p_np_contour.json")
    assert (
        "No polynomial-size compilation theorem known for general formulas"
        in d["honest_wall"]
    )
    assert "remains OPEN" in d["key_insight"]
    assert " iff " not in d["key_insight"]


def test_millennium_interpretation_never_claims_resolution():
    d = load("millennium_data.json")
    pnp = d["Q1_p_vs_np"]["p_vs_np"]
    assert pnp["removable_value"] == 0
    assert "remains OPEN" in pnp["interpretation"]
    assert pnp["interpretation"].startswith("consistent with P != NP")

    meanings = {p["name"]: p["meaning"] for p in d["Q3_all_six"]["problems"]}
    for name in (
        "P vs NP",
        "Yang-Mills",
        "Navier-Stokes",
        "Hodge Conjecture",
        "Birch-Swinnerton-Dyer",
    ):
        assert "OPEN" in meanings[name], (name, meanings[name])

    joined = " ".join(meanings.values())
    assert "Smooth solutions exist" not in joined
    assert "Every Hodge class is algebraic" not in joined
    assert "Algebraic rank = analytic rank" not in joined


def test_goldbach_large_is_a_finite_certificate():
    d = load("goldbach_large.json")
    assert d["verification"]["max_n"] == 100000
    assert d["verification"]["even_numbers_tested"] == 49999
    assert d["verification"]["failures"] == 0
    assert "remains OPEN" in d["key_insight"]
    assert "OPEN" in d["honest_wall"]
    last = d["milestones"][-1]
    assert last["n"] == 100000 and last["representations"] == 810


def test_rh_li_correct_is_a_finite_check():
    d = load("rh_li_correct.json")
    assert d["n_max"] == 30 and d["n_zeros"] == 800
    assert d["all_positive"] is True
    assert abs(d["min_lambda"] - 0.02225734932071366) < 1e-15
    script = _script("06_Miscellaneous_Experiments/rh_li_correct.py")
    assert "so RH remains OPEN" in script


def test_lean_open_markers_pinned_and_no_sorry():
    li = _lean("RH/LiCriterion.lean")
    pnp = _lean("PvsNP.lean")
    gb = _lean("Goldbach.lean")

    assert "li_criterion_proof_open : Bool := true" in li
    assert "def liCriterionEquiv" in li
    assert "theorem finitePrefixNeverSettles" in li

    assert "noPolynomialCompilationKnown : Bool := true" in pnp
    assert "theorem compilation_wall_recorded" in pnp

    assert "goldbach_conjecture_open : Bool := true" in gb
    assert "theorem goldbach_even_4_to_100000" in gb

    for src in (li, pnp, gb):
        assert "sorry" not in re.sub(r"`sorry`", "", src)


def test_path_drift_gates_emit_centrally():
    for rel in (
        "02_Dark_Energy_0_0_Framework/log_limits_0_over_0.py",
        "02_Dark_Energy_0_0_Framework/shannon_entropy_0_over_0.py",
        "02_Dark_Energy_0_0_Framework/prime_number_theorem_0_over_0.py",
        "06_Miscellaneous_Experiments/rh_li_correct.py",
        "06_Miscellaneous_Experiments/p_np_contour.py",
        "06_Miscellaneous_Experiments/goldbach_large.py",
        "06_Miscellaneous_Experiments/goldbach_0_over0.py",
    ):
        src = _script(rel)
        assert "_central_data_dir()" in src, rel
        assert '"data/' not in src, rel
