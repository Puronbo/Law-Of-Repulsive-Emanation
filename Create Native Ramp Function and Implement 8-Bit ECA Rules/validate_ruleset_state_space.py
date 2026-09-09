import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_ruleset_state_space import (  # noqa: E402
    census, state_space_certificates,
)

for cert in state_space_certificates():
    assert cert["status"] in ("PASS", "HONEST_NEGATIVE")

status = {c["label"]: c["status"] for c in state_space_certificates()}
assert status["L_state_census_reproducible"] == "PASS"
assert status["L_state_permutation_pair"] == "PASS"
assert status["L_state_lap_glider_dynamics"] == "PASS"
assert status["L_state_stationary_census"] == "PASS"
assert status["L_state_census_sanity"] == "PASS"
assert status["L_state_permutation_equals_consv"] == "HONEST_NEGATIVE"
assert status["L_state_period_side_split"] == "HONEST_NEGATIVE"

profiles = census()
# Identity rule: every state is a fixed point, image is the whole space.
assert profiles[204][12] == {"width": 12, "attractors": 4096, "max_cycle": 1,
                             "max_transient": 0, "bijective": True}
# Color-swap twin 51: bijective length-2 permutation with zero transient.
assert profiles[51][12]["bijective"] and profiles[51][12]["max_cycle"] == 2
assert profiles[51][12]["max_transient"] == 0
# Two-lap gliders reach 2*width cycles; one-lap gliders reach width.
assert profiles[27][12]["max_cycle"] == 24
assert profiles[59][12]["max_cycle"] == 24
assert profiles[172][12]["max_cycle"] == 12
assert profiles[228][12]["max_cycle"] == 12
# Exactly the documented eleven rules are stationary at every width.
stationary = sorted(r for r, widths in profiles.items()
                    if all(p["max_cycle"] == 1 for p in widths.values()))
assert stationary == [4, 12, 36, 68, 76, 132, 140, 196, 204, 219, 236], \
    stationary

print("ruleset state-space validation passed")