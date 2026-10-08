import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(
    ROOT, "03_Data_and_Observational_Resources", "02_Experimental_Data_Collections"
)


def load(name):
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        raise AssertionError(
            "PERSISTENCE FAILURE, not a verdict failure: data/%s is absent.\n"
            "This standard is neither tracked in git nor regenerable from any "
            "script in the repository.\n"
            "Recover with:  python regen_data.py --regen-all\n"
            "Audit with:    python regen_data.py --unreproducible" % name
        )
    with open(path) as fp:
        return __import__("json").load(fp)


# key -> (Lean theorem name, removable value)
EXPECTED = {
    "log_one_add_div": ("log_one_add_div_tendsto_one", 1.0),
    "entropy_term": ("entropy_removable_value", 0.0),
    "kl_zero_zero": ("kl_zero_zero_tendsto_zero", 0.0),
    "sin_div": ("sin_x_div_tendsto_one", 1.0),
    "one_sub_cos_div_sq": ("one_sub_cos_div_sq_tendsto_half", 0.5),
    "exp_sub_one_div": ("exp_sub_one_div_tendsto_one", 1.0),
    "tan_div": ("tan_x_div_tendsto_one", 1.0),
    "arcsin_div": ("arcsin_x_div_tendsto_one", 1.0),
    "log_div_sub_one": ("log_div_sub_one_tendsto_one", 1.0),
    "sub_one_div_log": ("sub_one_div_log_tendsto_one", 1.0),
    "self_pow": ("self_pow_tendsto_one", 1.0),
    "csin_div": ("csin_x_div_tendsto_one", 1.0),
}

EXTRA = {
    "one_add_x_rpow_inv": ("one_add_x_rpow_inv_tendsto_e", math.e),
}


def test_zero_zero_family_supported():
    d = load("zero_zero_family_0_over_0_data.json")
    s = d["summary"]
    assert s["supported"]
    assert s["all_passed"]


def test_zero_zero_family_keys_removable_and_lean_correspondence():
    d = load("zero_zero_family_0_over_0_data.json")
    s = d["summary"]
    assert s["lean_module"] == "PunoCalculus.ZeroZero"
    by_key = dict(EXPECTED, **EXTRA)
    for key, (theorem, removable) in by_key.items():
        entry = d[key]
        assert entry["passed"], "per-key probe %s must pass" % key
        assert math.isclose(
            float(entry["removable_value"]), removable, rel_tol=1e-9,
            abs_tol=1e-12,
        ), "removable value for %s" % key
        assert s["lean_theorems"][key] == theorem, (
            "Lean theorem correspondence for %s" % key
        )
        assert s["per_key"][key]


def test_zero_zero_family_limits_converge():
    d = load("zero_zero_family_0_over_0_data.json")
    for key in EXPECTED:
        entry = d[key]
        errors = entry["errors"]
        assert errors[-1] < 1e-6, "last error too large for %s" % key
        assert errors[-1] < errors[0] * 0.01 + 1e-12 or errors[0] == 0, (
            "lattice must be shrinking for %s" % key
        )


def test_zero_zero_family_emitted_by_framework_script():
    import os.path as osp
    import sys

    src = osp.join(
        ROOT,
        "02_Experimental_Implementations_and_Verification",
        "02_Dark_Energy_0_0_Framework",
        "zero_zero_family_0_over_0.py",
    )
    assert osp.exists(src), "regenerator script missing"
    with open(src) as fh:
        text = fh.read()
    assert "zero_zero_family_0_over_0_data.json" in text
    assert "_central_data_dir" in text
    sys.path.insert(0, osp.join(
        ROOT,
        "07_Interdisciplinary_Connections_and_Frameworks",
        "02_Mathematical_Physics_Connections",
    ))
    import regen_data
    amap = regen_data.build_map()
    assert "zero_zero_family_0_over_0_data.json" in amap
    assert "zero_zero_family_0_over_0.py" in osp.basename(amap["zero_zero_family_0_over_0_data.json"][0])