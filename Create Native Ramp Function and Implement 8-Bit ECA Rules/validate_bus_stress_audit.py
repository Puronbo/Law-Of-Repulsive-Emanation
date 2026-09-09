import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_bus_stress_audit import (  # noqa: E402
    stress_certificates,
)

status = {c["label"]: c["status"] for c in stress_certificates()}
assert status["L_stress_reference_large_widths"] == "PASS"
assert status["L_stress_linearity"] == "PASS"
assert status["L_stress_deterministic"] == "PASS"
assert status["L_stress_marker_impulse_fidelity"] == "PASS"

print("bus stress audit validation passed")