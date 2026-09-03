import os

from experiments.emanation.chain_audit import chain_certificates

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def test_all_four_certificates_present():
    certs = chain_certificates()
    assert len(certs) == 4
    labels = {c["label"] for c in certs}
    assert labels == {
        "L24_chain_verify_untampered",
        "L25_tamper_no_rehash_detected",
        "L26_rehash_tamper_detected",
        "L27_any_payload_modification_detected",
    }


def test_three_pass_one_negative():
    certs = chain_certificates()
    passers = [c for c in certs if c["status"] == "PASS"]
    negatives = [c for c in certs if c["status"] == "HONEST_NEGATIVE"]
    assert len(passers) == 3
    assert len(negatives) == 1
    assert negatives[0]["label"] == "L27_any_payload_modification_detected"
    assert negatives[0]["first_failure"] is not None


def test_point_counts():
    certs = {c["label"]: c for c in chain_certificates()}
    # lengths 2..9 x 10 seeds = 80 datums
    for label in certs:
        assert certs[label]["points_checked"] == 80


def test_honest_negative_is_the_terminal_tail():
    c = next(c for c in chain_certificates()
             if c["label"] == "L27_any_payload_modification_detected")
    # the law fails at its first datum: length 2, seed 0
    assert c["first_failure"]["datum"][0] >= 2


def test_certificates_in_full_table():
    from experiments.emanation import repo_audit as ra
    full = ra.full_table()
    labels = {c["label"] for c in full}
    assert "L24_chain_verify_untampered" in labels
    assert "L27_any_payload_modification_detected" in labels
    certs = {c["label"]: c for c in full}
    assert certs["L24_chain_verify_untampered"]["points_checked"] == 80


def test_drift_on_chain_table_tamper():
    import json
    path = os.path.join(_DATA, "law_certificates.json")
    with open(path, encoding="utf-8") as fh:
        saved = json.load(fh)
    tampered = [c for c in saved
                if c["label"] != "L24_chain_verify_untampered"]
    drift_path = os.path.join(_DATA, "_chain_tmp.json")
    with open(drift_path, "w", encoding="utf-8") as fh:
        json.dump(tampered, fh)
    try:
        from experiments.emanation import repo_audit as ra
        ok, details = ra.fresh_table_matches(drift_path)
        assert ok is False
        assert any("L24_chain_verify_untampered" in d for d in details)
    finally:
        os.remove(drift_path)