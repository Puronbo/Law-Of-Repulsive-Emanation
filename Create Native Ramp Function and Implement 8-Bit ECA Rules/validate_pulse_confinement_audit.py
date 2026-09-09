import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_pulse_confinement_audit import (  # noqa: E402
    _SIDE_A,
    confinement_certificates,
    impulse_profile,
)
from soliton_eca.soliton_eca import RULES  # noqa: E402

status = {c["label"]: c["status"] for c in confinement_certificates()}
assert status["L_pulse_a_side_stationary"] == "PASS"
assert status["L_pulse_confined_is_a_side"] == "PASS"
assert status["L_pulse_traveling_impulse"] == "HONEST_NEGATIVE"
assert status["L_pulse_b_side_fills"] == "PASS"

for rule in _SIDE_A:
    assert all(impulse_profile(rule, w)["stationary"] for w in (8, 12, 16))

for rule in set(RULES) - set(_SIDE_A):
    assert all(impulse_profile(rule, w)["fills"] for w in (8, 12, 16))

assert len(_SIDE_A) == 16

print("pulse confinement audit validation passed")