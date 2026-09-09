import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_nlse_audit import (  # noqa: E402
    nlse_certificates, energy_drift, convergence_order, power_error,
    phase_deviation, _TOL_ENERGY, _TOL_SHAPE,
)

status = {c["label"]: c["status"] for c in nlse_certificates()}
assert status["L_nlse_energy_unitarily_conserved"] == "PASS"
assert status["L_nlse_second_order_convergence"] == "PASS"
assert status["L_nlse_sech_shape_invariant"] == "PASS"
assert status["L_nlse_sech_phase_rotation"] == "PASS"

assert max(energy_drift(z, s) for z, s in
           ((0.5, 100), (1.0, 100), (2.0, 200), (4.0, 400))) < _TOL_ENERGY
assert 1.8 <= convergence_order() <= 2.2
assert max(power_error(z, 400) for z in (0.5, 1.0, 2.0, 4.0)) < _TOL_SHAPE
assert phase_deviation(1.0, 400) >= 0.9998

print("nlse audit validation passed")