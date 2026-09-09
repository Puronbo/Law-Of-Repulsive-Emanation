import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_mi_audit import (  # noqa: E402
    _BAND_MODES,
    _FIT_WINDOWS,
    _gain,
    _analytic_gain,
    mi_certificates,
)

measured = {}
for k, window in _FIT_WINDOWS.items():
    measured[k] = _gain(k, window)
for k, window in _BAND_MODES.items():
    measured[k] = _gain(k, window)

status = {c["label"]: c["status"] for c in mi_certificates(measured)}
assert status["L_mi_gain_matches_analytic"] == "PASS"
assert status["L_mi_band_edge"] == "PASS"
assert status["L_mi_peak_location"] == "PASS"
assert status["L_mi_soliton_stability_island"] == "PASS"
assert status["L_mi_energy_conserved"] == "PASS"

for k in (4, 6, 8, 12, 16):
    assert abs(measured[k] - _analytic_gain(k)) / _analytic_gain(k) <= 0.09
assert measured[20] >= 0.2
assert measured[22] <= 1e-3

print("mi audit validation passed")