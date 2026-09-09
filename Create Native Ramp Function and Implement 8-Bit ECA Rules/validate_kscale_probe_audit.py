import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_kscale_probe_audit import (  # noqa: E402
    _CORE,
    _COINCIDENCES,
    _KS,
    _PROBES,
    _TOL,
    per_placement_measurements,
    probe_certificates,
)
from soliton_eca.soliton_eca import RULES  # noqa: E402

certs, stats = probe_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_ks_core_abs"] == "PASS"
assert status["L_ks_intersect"] == "PASS"
assert status["L_ks_coincidence"] == "HONEST_NEGATIVE"
assert status["L_ks_whole_cells"] == "PASS"

res = stats["residuals"]
w = 512
for k in _KS:
    for r in _CORE:
        for p in range(_PROBES):
            assert res[k][r][p] <= _TOL
assert all(0 < res[k][r][p] * w <= 200
           for k in _KS for r in _COINCIDENCES
           for p in range(_PROBES)
           if res[k][r][p] > _TOL)

print("kscale probe audit validation passed")