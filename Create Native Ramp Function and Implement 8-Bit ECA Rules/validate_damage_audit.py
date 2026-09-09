import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_damage_audit import (  # noqa: E402
    _FULL_SET,
    _ISOMETRY_SET,
    _isometry_set,
    damage_certificates,
)

status = {c["label"]: c["status"] for c in damage_certificates()}
assert status["L_damage_isometry_pair"] == "PASS"
assert status["L_damage_single_cell_family"] == "PASS"
assert status["L_damage_full_lattice_amplifiers"] == "PASS"
assert status["L_damage_far_half_containment"] == "HONEST_NEGATIVE"
assert status["L_damage_conservation_pair"] == "PASS"

assert _isometry_set() == set(_ISOMETRY_SET) == {204, 51}
assert len(_FULL_SET) == 4

print("damage audit validation passed")