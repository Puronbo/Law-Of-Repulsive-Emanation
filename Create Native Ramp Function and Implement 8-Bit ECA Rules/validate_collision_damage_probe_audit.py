import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_collision_damage_probe_audit import (  # noqa: E402
    _PROBES,
    _SAT_LEVEL,
    _WIPE_LEVEL,
    damage_probe_certificates,
    probe_data,
)
from soliton_eca.soliton_eca import RULES  # noqa: E402

certs, stats = damage_probe_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_cdp_detach_exact"] == "PASS"
assert status["L_cdp_wipe_core"] == "PASS"
assert status["L_cdp_saturation_signature"] == "PASS"
assert status["L_cdp_wipe_set_exact"] == "HONEST_NEGATIVE"
assert status["L_cdp_saturation_universal"] == "HONEST_NEGATIVE"
assert status["L_cdp_far_antipode"] == "HONEST_NEGATIVE"
assert status["L_cdp_synergy_none"] == "HONEST_NEGATIVE"

dat = probe_data()
f1 = dat["f1"]
f2 = dat["f2"]
base = 2 * 4 / 512

for r in (204, 51):
    for d in (4, 16, 64, 128, 256):
        for p in range(_PROBES):
            assert abs(f2[r][d][p] - base) < 1e-9

intersection = [r for r in RULES
                if all(max(f2[r][d][p] for d in (4, 16, 64, 128, 256))
                       <= _WIPE_LEVEL for p in range(_PROBES))]
assert set(intersection) == {36, 251}

assigned = {36, 251}
assert all(36 in s and 251 in s for s in stats["wiper_sets"])
assert sum(219 in s for s in stats["wiper_sets"]) == 6

sat = [f2[147][4][p] - 2 * f1[147][p] for p in range(_PROBES)]
assert sum(v <= _SAT_LEVEL for v in sat) == 7
worst_p = max(range(_PROBES), key=lambda p: abs(sat[p]))
assert abs(sat[worst_p]) > 0.03
assert sat[3] > 0.03

f1m = {r: sum(f1[r]) / _PROBES for r in RULES}
f2m = {r: {d: sum(f2[r][d]) / _PROBES for d in (4, 16, 64, 128, 256)}
       for r in RULES}
mean_sat = {r: f2m[r][4] - 2 * f1m[r] for r in RULES}
assert mean_sat[147] <= _SAT_LEVEL
assert {r for r in RULES if mean_sat[r] <= _SAT_LEVEL} == {147}

far_worst = max(abs(f2[r][256][p] - 2 * f1[r][p])
                for r in RULES for p in range(_PROBES))
assert far_worst > 0.005
assert max(abs(f2[147][256][3] - 2 * f1[147][3]),
           abs(f2[147][4][3] - 2 * f1[147][3])) == far_worst

syn = any(any(f2[r][d][p] > 1.01 * 2 * f1[r][p]
              for d in (4, 16, 64, 128, 256))
          for r in RULES for p in range(_PROBES))
assert syn

print("collision damage probe audit validation passed")