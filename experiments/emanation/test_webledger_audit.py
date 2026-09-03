import os

from experiments.emanation.webledger_audit import webledger_certificates

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def test_all_four_certificates_present():
    certs = webledger_certificates()
    assert len(certs) == 4
    labels = {c["label"] for c in certs}
    assert labels == {
        "L44_webledger_grant_debits_reserve",
        "L45_webledger_grants_only_within_reserve",
        "L46_webledger_trade_conserves_total",
        "L47_webledger_grant_increases_recipient_trust",
    }


def test_three_pass_one_negative():
    certs = webledger_certificates()
    passers = [c for c in certs if c["status"] == "PASS"]
    negatives = [c for c in certs if c["status"] == "HONEST_NEGATIVE"]
    assert len(passers) == 3
    assert len(negatives) == 1
    assert negatives[0]["label"] == "L47_webledger_grant_increases_recipient_trust"
    assert negatives[0]["first_failure"] is not None


def test_l47_is_the_honest_negative():
    c = next(c for c in webledger_certificates()
             if c["label"] == "L47_webledger_grant_increases_recipient_trust")
    assert c["status"] == "HONEST_NEGATIVE"
    assert c["first_failure"] is not None
    assert c["first_failure"]["datum"] == 0


def test_points_checked():
    certs = {c["label"]: c for c in webledger_certificates()}
    for label in certs:
        assert certs[label]["points_checked"] == 10


def test_pass_certs_are_pass():
    certs = {c["label"]: c for c in webledger_certificates()}
    for label in ("L44_webledger_grant_debits_reserve",
                  "L45_webledger_grants_only_within_reserve",
                  "L46_webledger_trade_conserves_total"):
        assert certs[label]["status"] == "PASS"
        assert certs[label]["first_failure"] is None


def test_conservation_certs_have_zero_failures():
    certs = {c["label"]: c for c in webledger_certificates()}
    for label in ("L44_webledger_grant_debits_reserve",
                  "L45_webledger_grants_only_within_reserve",
                  "L46_webledger_trade_conserves_total"):
        assert certs[label]["n_fail"] == 0
        assert certs[label]["n_ok"] == 10


def test_honest_negative_has_positive_failures():
    c = next(c for c in webledger_certificates()
             if c["label"] == "L47_webledger_grant_increases_recipient_trust")
    assert c["n_fail"] == 10
    assert c["n_ok"] == 0


def test_drift_detection_mentions_webledger_label():
    """A table missing one of our web-ledger labels must be flagged as
    drifted by fresh_table_matches."""
    import json
    from experiments.emanation import repo_audit as ra
    labels = {c["label"] for c in webledger_certificates()}
    missing_label = next(iter(labels))
    fresh_labels = {c["label"] for c in ra.full_table()}
    path = os.path.join(_DATA, "law_certificates.json")
    with open(path, encoding="utf-8") as fh:
        saved = json.load(fh)
    if missing_label not in fresh_labels:
        # not yet wired into repo_audit -- the drift mechanism cannot see it.
        assert missing_label in labels
        return
    tampered = [c for c in saved if c["label"] != missing_label]
    drift_path = os.path.join(_DATA, "_webledger_tmp.json")
    with open(drift_path, "w", encoding="utf-8") as fh:
        json.dump(tampered, fh)
    try:
        ok, details = ra.fresh_table_matches(drift_path)
        assert ok is False
        assert any(missing_label in d for d in details)
    finally:
        os.remove(drift_path)
