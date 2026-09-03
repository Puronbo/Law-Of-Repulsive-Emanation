import os

from experiments.emanation.puno_flow_audit import puno_flow_certificates

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def test_all_four_certificates_present():
    certs = puno_flow_certificates()
    assert len(certs) == 4
    labels = {c["label"] for c in certs}
    assert labels == {
        "L28_to_disk_inside_preserved",
        "L29_to_disk_rim_exact",
        "L30_flow_over_dedup_and_self_loop_invariant",
        "L31_settle_conserves_centroid",
    }


def test_three_pass_one_negative():
    certs = puno_flow_certificates()
    passers = [c for c in certs if c["status"] == "PASS"]
    negatives = [c for c in certs if c["status"] == "HONEST_NEGATIVE"]
    assert len(passers) == 3
    assert len(negatives) == 1
    assert negatives[0]["label"] == "L31_settle_conserves_centroid"
    assert negatives[0]["first_failure"] is not None


def test_certificates_in_full_table():
    from experiments.emanation import repo_audit as ra
    full = ra.full_table()
    labels = {c["label"] for c in full}
    assert "L28_to_disk_inside_preserved" in labels
    assert "L31_settle_conserves_centroid" in labels
    certs = {c["label"]: c for c in full}
    assert certs["L28_to_disk_inside_preserved"]["points_checked"] == 12


def test_drift_on_puno_flow_table_tamper():
    import json
    path = os.path.join(_DATA, "law_certificates.json")
    with open(path, encoding="utf-8") as fh:
        saved = json.load(fh)
    tampered = [c for c in saved
                if c["label"] != "L28_to_disk_inside_preserved"]
    drift_path = os.path.join(_DATA, "_punoflow_tmp.json")
    with open(drift_path, "w", encoding="utf-8") as fh:
        json.dump(tampered, fh)
    try:
        from experiments.emanation import repo_audit as ra
        ok, details = ra.fresh_table_matches(drift_path)
        assert ok is False
        assert any("L28_to_disk_inside_preserved" in d for d in details)
    finally:
        os.remove(drift_path)