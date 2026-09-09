import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_mi_modal_audit import (  # noqa: E402
    _CREST_CORE_CEIL,
    _CORE_LATE,
    _CARRIER_LATE,
    _MODES,
    _PUMP_CEIL,
    modal_certificates,
)

certs, data = modal_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_mod_pump_depleted"] == "PASS"
assert status["L_mod_crest_core_capped"] == "PASS"
assert status["L_mod_late_core_restored"] == "PASS"
assert status["L_mod_late_harmonic_rise"] == "PASS"
assert status["L_mod_carrier_core_at_crest"] == "HONEST_NEGATIVE"
assert status["L_mod_exact_twomode_crest"] == "HONEST_NEGATIVE"

for m, _ in _MODES:
    d = data[m]
    assert d["p0c"] <= _PUMP_CEIL
    assert d["p0c"] + d["p1c"] <= _CREST_CORE_CEIL
    assert d["p0l"] >= _CARRIER_LATE
    assert d["p0l"] + d["p1l"] >= _CORE_LATE
assert data[16]["crest"] < data[8]["crest"] < data[4]["crest"]
assert data[16]["p2l"] < data[8]["p2l"] < data[4]["p2l"]
assert max(d["p0c"] + d["p1c"]
           for d in data.values()) < _CORE_LATE
assert all(abs(1.0 - (d["p0c"] + d["p1c"])) > 1e-9
           for d in data.values())

print("mi modal audit validation passed")