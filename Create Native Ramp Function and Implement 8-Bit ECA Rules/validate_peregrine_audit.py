import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_peregrine_audit import (  # noqa: E402
    _Z_POINTS,
    _center_curve,
    peregrine_certificates,
)

status = {c["label"]: c["status"] for c in peregrine_certificates()}
assert status["L_peregrine_seed_shape"] == "PASS"
assert status["L_peregrine_curve_analytic"] == "PASS"
assert status["L_peregrine_breathes_back"] == "PASS"
assert status["L_peregrine_wings_unperturbed"] == "PASS"
assert status["L_peregrine_energy_conserved"] == "PASS"

curve = {r["z"]: r for r in _center_curve()}
assert abs(curve[_Z_POINTS[0]]["measured"] - 3.0) <= 1e-3
for z in _Z_POINTS:
    assert abs(curve[z]["measured"] - curve[z]["analytic"]) / \
        curve[z]["analytic"] <= 0.01
assert curve[_Z_POINTS[-1]]["measured"] < 1.15

print("peregrine audit validation passed")