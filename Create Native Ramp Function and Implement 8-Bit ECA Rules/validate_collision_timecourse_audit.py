import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_collision_timecourse_audit import (  # noqa: E402
    _BLOCK,
    _DISTANCES,
    _ERASER_SET,
    _FAR_TOL,
    _TIMES,
    _TRANSPARENT_SET,
    _WIDTH,
    _WIPE_LEVEL,
    timecourse_certificates,
    timecourse_table,
)

certs, tab = timecourse_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_coltime_transparent_time_exact"] == "PASS"
assert status["L_coltime_constructive_transient"] == "PASS"
assert status["L_coltime_saturation_builds"] == "PASS"
assert status["L_coltime_far_flat"] == "PASS"
assert status["L_coltime_instant_saturation"] == "HONEST_NEGATIVE"
assert status["L_coltime_erased"] == "PASS"

base = 2 * _BLOCK / _WIDTH
for r in _TRANSPARENT_SET:
    for d in _DISTANCES:
        for g in _TIMES:
            assert abs(tab[r][d][g] - base) <= 1 / _WIDTH

f1 = tab[147][-1]
f2 = tab[147]
rho = {d: {g: f2[d][g] / (2 * f1[g]) for g in _TIMES}
       for d in _DISTANCES}
assert rho[16][2] >= 1.10
assert min(rho[16][g] for g in (2, 4, 6, 8)) >= 0.85
assert max(rho[16][g] for g in (48, 64, 96)) <= 0.85
assert all(abs(rho[256][g] - 1.0) <= _FAR_TOL for g in _TIMES)
assert rho[16][2] > 1.0
assert all(max(tab[r][d][96] for d in _DISTANCES) <= _WIPE_LEVEL
           for r in _ERASER_SET)

print("collision timecourse audit validation passed")