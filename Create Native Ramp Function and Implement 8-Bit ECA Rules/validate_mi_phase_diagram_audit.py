import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_mi_phase_diagram_audit import (  # noqa: E402
    _CAP,
    _EPS_SET,
    _OMEGA_GRID,
    phasemap_certificates,
    phasemap_measurements,
)

certs, m = phasemap_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_phd_single_crossing_moderate"] == "PASS"
assert status["L_phd_breaking_rises"] == "PASS"
assert status["L_phd_crest_bump"] == "PASS"
assert status["L_phd_weak_deep_lag"] == "PASS"
assert status["L_phd_all_single_crossing"] == "HONEST_NEGATIVE"

deep = 2 * 3.141592653589793 * 2 / 64
o5, o785, o9 = 0.5, 2 * 3.141592653589793 * 8 / 64, 0.9
for e in (0.10, 0.20, 0.30, 0.45):
    above = [om for om in _OMEGA_GRID if m[e][om] > _CAP]
    below = [om for om in _OMEGA_GRID if m[e][om] < _CAP]
    assert all(m[e][om] > _CAP for om in _OMEGA_GRID if om <= max(above))
    assert all(m[e][om] < _CAP for om in _OMEGA_GRID if om >= min(below))
assert m[0.05][deep] < _CAP
assert m[0.05][0.5] > _CAP
assert all(m[e][o9] > m[e][o785] for e in (0.20, 0.30, 0.45))
assert m[0.05][deep] < m[0.05][o5]

print("mi phase diagram audit validation passed")