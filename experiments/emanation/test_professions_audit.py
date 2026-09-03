import os

from experiments.emanation.professions_audit import professions_certificates

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def test_all_four_certificates_present():
    certs = professions_certificates()
    assert len(certs) == 4
    labels = {c["label"] for c in certs}
    assert labels == {
        "L35_rubric_score_bounded",
        "L36_profession_names_unique_nonempty",
        "L37_mandate_fraction_is_skill_complement",
        "L38_classA_literal_zero_skill",
    }


def test_three_pass_one_negative():
    certs = professions_certificates()
    passers = [c for c in certs if c["status"] == "PASS"]
    negatives = [c for c in certs if c["status"] == "HONEST_NEGATIVE"]
    assert len(passers) == 3
    assert len(negatives) == 1
    assert negatives[0]["label"] == "L38_classA_literal_zero_skill"
    assert negatives[0]["first_failure"] is not None


def test_point_counts():
    from professions.professions_data import PROFESSIONS
    from professions.rubric import profession_verdict
    certs = {c["label"]: c for c in professions_certificates()}
    n_prof = len(PROFESSIONS)
    n_a = sum(1 for n, t in PROFESSIONS
              if profession_verdict(t)["class"] == "A")
    assert certs["L35_rubric_score_bounded"]["points_checked"] == n_prof
    assert certs["L36_profession_names_unique_nonempty"]["points_checked"] == n_prof
    assert certs["L37_mandate_fraction_is_skill_complement"]["points_checked"] == n_prof
    assert certs["L38_classA_literal_zero_skill"]["points_checked"] == n_a


def test_honest_negative_is_a_nonzero_skill_class_a():
    from professions.professions_data import PROFESSIONS
    from professions.rubric import profession_verdict
    c = next(c for c in professions_certificates()
             if c["label"] == "L38_classA_literal_zero_skill")
    ff = c["first_failure"]["datum"]
    v = profession_verdict(dict(PROFESSIONS)[ff])
    assert v["class"] == "A"
    assert v["skill_fraction"] > 0


def test_labels_from_own_function():
    certs = professions_certificates()
    labels = {c["label"] for c in certs}
    assert labels == {
        "L35_rubric_score_bounded",
        "L36_profession_names_unique_nonempty",
        "L37_mandate_fraction_is_skill_complement",
        "L38_classA_literal_zero_skill",
    }


def test_drift_on_professions_table_tamper():
    import json
    drift_path = os.path.join(_DATA, "_prof_tmp.json")
    tampered = [dict(c, status="PASS") if c["label"] == "L38_classA_literal_zero_skill"
                else c for c in professions_certificates()]
    with open(drift_path, "w", encoding="utf-8") as fh:
        json.dump(tampered, fh)
    try:
        from experiments.emanation import repo_audit as ra
        ok, details = ra.fresh_table_matches(drift_path)
        assert ok is False
        assert any("L38_classA_literal_zero_skill" in d for d in details)
    finally:
        os.remove(drift_path)
