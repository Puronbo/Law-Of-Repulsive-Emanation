import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_damage_timecourse_audit import (  # noqa: E402
    _BLOCK,
    _GROW_FACTOR,
    _INSTANT_TOL,
    _TRANSPARENT_SET,
    _WAVE_FACTOR,
    _WIDTH,
    timecourse_certificates,
    timecourse_table,
)

certs, table = timecourse_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_timecourse_transparent_flat"] == "PASS"
assert status["L_timecourse_instant_set"] == "PASS"
assert status["L_timecourse_wave_runners"] == "PASS"
assert status["L_timecourse_persistent_grower"] == "PASS"
assert status["L_timecourse_all_saturate"] == "HONEST_NEGATIVE"

for r in _TRANSPARENT_SET:
    for g in table[r]:
        assert abs(table[r][g] - _BLOCK / _WIDTH) <= _INSTANT_TOL
instant = {r for r in table
           if abs(table[r][1] - table[r][96]) <= _INSTANT_TOL}
assert instant == {4, 12, 19, 36, 51, 59, 68, 76, 187, 204, 219, 236, 243}
runners = {r for r in table if table[r][1] <= _WAVE_FACTOR * table[r][96]}
assert runners == {147, 155, 211}
growers = {r for r in table if table[r][96] >= _GROW_FACTOR * table[r][16]
           and table[r][16] > 0}
assert growers == {147}

print("damage timecourse audit validation passed")