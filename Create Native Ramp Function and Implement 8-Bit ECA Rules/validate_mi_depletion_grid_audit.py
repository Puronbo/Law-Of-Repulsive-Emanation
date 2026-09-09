import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_mi_depletion_grid_audit import (  # noqa: E402
    _BELT_CEIL,
    _CRESCENT_CEIL,
    _CRESCENT_OM,
    _EPS_SET,
    _FAR,
    _FAR_KEEP,
    _OMEGA_GRID,
    depletion_certificates,
)

certs, data = depletion_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_pdep_belt"] == "PASS"
assert status["L_pdep_crescent"] == "PASS"
assert status["L_pdep_far_kept"] == "PASS"
assert status["L_pdep_global"] == "HONEST_NEGATIVE"

belt = data["belt"]
assert max(v for row in belt.values()
           for v in row.values()) <= _BELT_CEIL
assert len(belt) == len(_EPS_SET)
assert all(len(row) == len(_OMEGA_GRID) for row in belt.values())
assert max(belt[e][om] for om in _CRESCENT_OM
           for e in _EPS_SET) <= _CRESCENT_CEIL
assert data["far"][8.0] >= _FAR_KEEP
assert min(data["far"][om] for om in _FAR) <= _BELT_CEIL

print("mi depletion grid audit validation passed")