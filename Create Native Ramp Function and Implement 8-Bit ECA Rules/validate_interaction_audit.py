import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_interaction_audit import (  # noqa: E402
    _measure,
    interaction_certificates,
)

rows = _measure()
status = {c["label"]: c["status"] for c in interaction_certificates(rows)}
assert status["L_interaction_in_phase_binds"] == "PASS"
assert status["L_interaction_pi_phase_repels"] == "PASS"
assert status["L_interaction_equal_amplitude_clean"] == "PASS"
assert status["L_interaction_unequal_amplitude_clean"] == "HONEST_NEGATIVE"
assert status["L_interaction_energy_conserved"] == "PASS"

for r in rows:
    if r["amps"] != (1.0, 1.0):
        assert abs(r["far_delta"]) >= 5e-3
    else:
        assert abs(r["far_delta"]) <= 1e-2

for r in rows:
    if r["phi"] == 0.0 and r["d"] in (4, 6) and r["amps"] == (1.0, 1.0):
        assert r["sepf"] < r["sep0"]
    elif r["phi"] == 3.141592653589793 and r["d"] in (4, 6, 10):
        assert r["sepf"] > r["sep0"]

print("interaction audit validation passed")