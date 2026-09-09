import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_collision_range_audit import (  # noqa: E402
    _BOTTOM,
    _BOTTOM_SPREAD,
    _CORE_LEVEL,
    _DISTANCES,
    _HALO_LEVEL,
    _RECOVERY,
    range_certificates,
    range_profile,
)

certs, prof = range_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_range_saturation_core"] == "PASS"
assert status["L_range_deepest_bracket"] == "PASS"
assert status["L_range_recovery_band"] == "PASS"
assert status["L_range_transparent_flat"] == "PASS"
assert status["L_range_independent_at_all"] == "HONEST_NEGATIVE"

r = prof[147]
assert max(r[d] for d in _DISTANCES if d <= 16) <= _CORE_LEVEL
assert min(r[d] for d in _DISTANCES if d >= 96) >= _HALO_LEVEL
for d in (4, 8):
    assert 1 - r[d] >= _BOTTOM
    assert 1 - r[d] >= 1 - r[12] + _BOTTOM_SPREAD
assert r[64] >= r[8] + _RECOVERY
for d in _DISTANCES:
    assert abs(prof[204][d] - 1.0) <= 1 / 512
assert r[8] <= 0.6

print("collision range audit validation passed")