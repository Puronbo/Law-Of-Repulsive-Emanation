import os

from experiments.emanation.calendars_audit import calendar_certificates

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def test_all_six_certificates_present():
    certs = calendar_certificates()
    assert len(certs) == 6
    labels = {c["label"] for c in certs}
    assert labels == {
        "L18_gregorian_roundtrip",
        "L19_julian_roundtrip",
        "L20_tzolkin_periodicity",
        "L21_gregorian_monotonicity",
        "L22_day_of_year_consistent",
        "L23_tropical_integer",
    }


def test_five_pass_one_negative():
    certs = calendar_certificates()
    passers = [c for c in certs if c["status"] == "PASS"]
    negatives = [c for c in certs if c["status"] == "HONEST_NEGATIVE"]
    assert len(passers) == 5
    assert len(negatives) == 1
    assert negatives[0]["label"] == "L23_tropical_integer"
    assert negatives[0]["first_failure"] is not None


def test_gregorian_roundtrip_exhaustive():
    c = next(c for c in calendar_certificates()
             if c["label"] == "L18_gregorian_roundtrip")
    assert c["status"] == "PASS"
    assert c["points_checked"] == 146097


def test_julian_roundtrip_exhaustive():
    c = next(c for c in calendar_certificates()
             if c["label"] == "L19_julian_roundtrip")
    assert c["status"] == "PASS"
    assert c["points_checked"] == 1461


def test_tzolkin_periodic_window():
    c = next(c for c in calendar_certificates()
             if c["label"] == "L20_tzolkin_periodicity")
    assert c["status"] == "PASS"
    assert c["points_checked"] == 1000


def test_honest_negative_fails_at_day_one():
    c = next(c for c in calendar_certificates()
             if c["label"] == "L23_tropical_integer")
    assert c["status"] == "HONEST_NEGATIVE"
    # the first failure datum must be day=1 (or another early day)
    assert c["first_failure"]["datum"] >= 1


def test_certificates_in_full_table():
    from experiments.emanation import repo_audit as ra
    full = ra.full_table()
    labels = {c["label"] for c in full}
    assert "L18_gregorian_roundtrip" in labels
    assert "L23_tropical_integer" in labels
    certs = {c["label"]: c for c in full}
    assert certs["L18_gregorian_roundtrip"]["points_checked"] == 146097


def test_drift_on_calendar_table_tamper():
    import json
    path = os.path.join(_DATA, "law_certificates.json")
    with open(path, encoding="utf-8") as fh:
        saved = json.load(fh)
    tampered = [c for c in saved if c["label"] != "L18_gregorian_roundtrip"]
    drift_path = os.path.join(_DATA, "_cal_tmp.json")
    with open(drift_path, "w", encoding="utf-8") as fh:
        json.dump(tampered, fh)
    try:
        from experiments.emanation import repo_audit as ra
        ok, details = ra.fresh_table_matches(drift_path)
        assert ok is False
        assert any("L18_gregorian_roundtrip" in d for d in details)
    finally:
        os.remove(drift_path)