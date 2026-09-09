import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_mi_recurrence_audit import (  # noqa: E402
    _CAP,
    _EPS_SET,
    _RELAX_FACTOR,
    recurrence_certificates,
    recurrence_measurements,
)

certs, m = recurrence_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_recurrence_crest_capped"] == "PASS"
assert status["L_recurrence_relaxes_back"] == "PASS"
assert status["L_recurrence_period_shortens"] == "PASS"
assert status["L_recurrence_linear_crest"] == "HONEST_NEGATIVE"

for e in _EPS_SET:
    assert m[e]["crest"] < _CAP
    assert m[e]["trough_after"] <= _RELAX_FACTOR * (1 + e)
crest_z = [m[e]["crest_z"] for e in (0.05, 0.10, 0.20, 0.30)]
assert all(a > b for a, b in zip(crest_z, crest_z[1:]))

print("mi recurrence audit validation passed")