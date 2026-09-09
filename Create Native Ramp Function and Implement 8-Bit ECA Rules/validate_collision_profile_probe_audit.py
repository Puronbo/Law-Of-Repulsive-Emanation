import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_collision_profile_probe_audit import (  # noqa: E402
    _CONSTRUCT_MIN,
    _FAR_TOL,
    _R_DISTANCES,
    _R_PROBES,
    _R_WIDTH,
    _T_DISTANCES,
    _T_WIDTH,
    _TIMES,
    _range_mean,
    _timecourse_mean,
    profile_probe_certificates,
    range_profile_per_placement,
    timecourse_per_placement,
)

certs, stats = profile_probe_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_rp_transparent_flat"] == "PASS"
assert status["L_rp_mean_core"] == "PASS"
assert status["L_tp_transparent_exact"] == "PASS"
assert status["L_tp_mean_repro"] == "PASS"
assert status["L_rp_core_steady"] == "HONEST_NEGATIVE"
assert status["L_rp_recovery_halo_majority"] == "HONEST_NEGATIVE"
assert status["L_rp_profile_identical"] == "HONEST_NEGATIVE"
assert status["L_tp_constructive_opening"] == "HONEST_NEGATIVE"
assert status["L_tp_far_flat"] == "HONEST_NEGATIVE"

rp = range_profile_per_placement()
rm = _range_mean(147)
r147 = rp[147]
r204 = rp[204]

for d in _R_DISTANCES:
    for v in r204[d]:
        assert abs(v - 1.0) <= 1 / _R_WIDTH

round13 = {4: 0.546, 8: 0.535, 12: 0.657, 16: 0.595, 24: 0.666,
           32: 0.726, 48: 0.784, 64: 0.858, 96: 1.007, 128: 0.956,
           192: 0.954, 256: 1.039}
for d, v in round13.items():
    assert abs(rm[d] - v) <= 0.002

assert max(rm[d] for d in _R_DISTANCES if d <= 16) <= 0.66
assert min(rm[d] for d in _R_DISTANCES if d >= 96) >= 0.95

core_pp = [max(r147[d][p] for d in _R_DISTANCES if d <= 16)
           for p in range(_R_PROBES)]
assert max(core_pp) > 0.66
assert max(core_pp) > 1.0
assert sum(v <= 0.66 for v in core_pp) == 3

assert any(r147[64][p] < r147[8][p] + 0.30 for p in range(_R_PROBES))

pair_worst = max(abs(r147[d][p] - r147[d][q])
                 for d in _R_DISTANCES
                 for p in range(_R_PROBES)
                 for q in range(p + 1, _R_PROBES))
assert pair_worst > 0.01

tc = timecourse_per_placement()
for r in (204, 51):
    for d in _T_DISTANCES:
        for g in _TIMES:
            for v in tc[r][d][g]:
                assert abs(v - 1.0) <= 1 / _T_WIDTH

tc147 = tc[147]
assert min(tc147[16][2]) < _CONSTRUCT_MIN
assert max(tc147[16][2]) >= 2.0

far_worst = max(abs(tc147[256][g][p] - 1.0)
                for g in _TIMES for p in range(_R_PROBES))
assert far_worst > _FAR_TOL
assert far_worst >= 3.0

tcm = _timecourse_mean(147)
assert tcm[16][2] >= _CONSTRUCT_MIN
assert max(abs(tcm[256][g] - 1.0) for g in _TIMES) <= _FAR_TOL

print("collision profile probe audit validation passed")