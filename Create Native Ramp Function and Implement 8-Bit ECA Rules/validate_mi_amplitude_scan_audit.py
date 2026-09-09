import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_mi_amplitude_scan_audit import (  # noqa: E402
    _CAP,
    _EPS_SET,
    _OMEGA_SET,
    _RELAX_FACTOR,
    amplitudescan_certificates,
    amplitudescan_measurements,
)

certs, m = amplitudescan_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_amp_crest_grows"] == "PASS"
assert status["L_amp_deep_cap_breaks_all"] == "PASS"
assert status["L_amp_high_cap_weak_seeds"] == "PASS"
assert status["L_amp_deep_period_shortens"] == "PASS"
assert status["L_amp_high_late_crest"] == "HONEST_NEGATIVE"
assert status["L_amp_recurrence"] == "PASS"

for om in _OMEGA_SET:
    cre = [m[om][e]["crest"] for e in _EPS_SET]
    assert all(a < b for a, b in zip(cre, cre[1:]))
for e in _EPS_SET:
    assert m[0.5][e]["crest"] > _CAP
    assert m[1.0][e]["crest"] < _CAP or e == _EPS_SET[-1]
assert all(a > b for a, b in
           zip([m[0.5][e]["crest_z"] for e in _EPS_SET],
               [m[0.5][e]["crest_z"] for e in _EPS_SET][1:]))
z1 = [m[1.0][e]["crest_z"] for e in _EPS_SET]
assert not all(a > b for a, b in zip(z1, z1[1:]))
for om in _OMEGA_SET:
    for e in _EPS_SET:
        assert m[om][e]["trough_after"] <= _RELAX_FACTOR * (1 + e)

print("mi amplitude scan audit validation passed")