import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_collision_damage_audit import (  # noqa: E402
    _BLOCK,
    _DISTANCES,
    _FAR_TOL,
    _SAT_LEVEL,
    _WIDTH,
    _WIPE_LEVEL,
    collision_certificates,
    collision_table,
)

certs, f1, f2 = collision_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_collision_transparent_exact"] == "PASS"
assert status["L_collision_eraser_wipe"] == "PASS"
assert status["L_collision_amplifier_saturation"] == "PASS"
assert status["L_collision_far_independence"] == "PASS"
assert status["L_collision_synergy"] == "HONEST_NEGATIVE"

base = 2 * _BLOCK / _WIDTH
for r in (204, 51):
    for d in _DISTANCES:
        assert abs(f2[r][d] - base) <= 1 / _WIDTH

wipe = {r for r in f1 if max(f2[r][d] for d in _DISTANCES) <= _WIPE_LEVEL}
assert wipe == {4, 36, 219, 251}

sat = {r for r in f1 if f2[r][4] - 2 * f1[r] <= _SAT_LEVEL}
assert sat == {147}

far = max(abs(f2[r][256] - 2 * f1[r]) for r in f1)
assert far <= _FAR_TOL

assert f1[147] > 0.05 and f1[204] == base / 2

print("collision damage audit validation passed")