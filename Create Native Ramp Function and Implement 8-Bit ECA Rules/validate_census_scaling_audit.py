import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_census_scaling_audit import (  # noqa: E402
    _W12_STATIONARY,
    _ONE_LAP,
    _TWO_LAP,
    census_data,
    census_scaling_certificates,
)

data = census_data()
status = {c["label"]: c["status"] for c in census_scaling_certificates(data)}
assert status["L_census16_conservation_unique"] == "PASS"
assert status["L_census16_lap_anchors_persist"] == "PASS"
assert status["L_census16_stationary_accumulates"] == "PASS"
assert status["L_census16_boundary_insensitive"] == "PASS"
assert status["L_census16_permutation_pair"] == "PASS"

assert data[204]["fixpoints"] == 1 << 16
assert data[51]["fixpoints"] == 0 and data[51]["torus_max_cycle"] == 2
assert data[204]["conserves"]
assert not any(data[r]["conserves"] for r in data if r != 204)
assert all(data[r]["torus_max_cycle"] == 16 for r in _ONE_LAP)
assert all(data[r]["torus_max_cycle"] == 32 for r in _TWO_LAP)
assert _W12_STATIONARY < {r for r, d in data.items()
                          if d["torus_max_cycle"] == 1}
assert (data[123]["torus_max_cycle"] == 2 and
        data[123]["ghost_max_cycle"] == 4)

print("census scaling audit validation passed")