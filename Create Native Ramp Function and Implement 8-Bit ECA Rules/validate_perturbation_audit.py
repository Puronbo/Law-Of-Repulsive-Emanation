import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_perturbation_audit import (  # noqa: E402
    _NPROBE,
    _W16_REACH,
    perturbation_certificates,
)

certs, tables = perturbation_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_pert_reach_set_16"] == "PASS"
assert status["L_pert_checked_rank"] == "PASS"
assert status["L_pert_stationary_quiet"] == "PASS"
assert status["L_pert_width_nesting"] == "PASS"
assert status["L_pert_fraction_decay"] == "PASS"
assert status["L_pert_checkerboard_degeneracy"] == "HONEST_NEGATIVE"

t16 = tables[16]
reach16 = {r for r, (h, _, _) in t16.items() if h > 0}
assert reach16 == _W16_REACH
assert len(reach16) == 13
assert t16[147][0] >= (_NPROBE * 16) // 2
assert t16[164][0] == 0 and t16[251][0] == 0
assert tables[32][147][1] < tables[16][147][1]

print("perturbation audit validation passed")