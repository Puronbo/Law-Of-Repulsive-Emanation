import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_ruleset_investigation import (  # noqa: E402
    _orbit_partition, _reflect, behavioral_profiles,
    investigation_certificates, structural_certificates,
)

for cert in structural_certificates() + investigation_certificates():
    assert cert["status"] in ("PASS", "HONEST_NEGATIVE")

structural = {c["label"]: c["status"] for c in structural_certificates()}
assert structural["L_struct_reflection_closed"] == "PASS"
assert structural["L_struct_crs_orbit_closed"] == "PASS"
assert structural["L_struct_census_consistency"] == "PASS"

orbits = _orbit_partition()
assert sum(len(o) for o in orbits) == 32
assert len(orbits) == 12
sym = sum(1 for o in orbits if len(o) == 2 and min(o) == _reflect(min(o)))
gen = sum(1 for o in orbits if len(o) == 4)
assert sym == 8 and gen == 4

profiles = behavioral_profiles()
for rule, p in profiles.items():
    assert p["twin"] == 255 - rule
assert profiles[204]["class"] == "conservative"
assert profiles[204]["period_median"] == 1
conservative = sorted(r for r, p in profiles.items()
                      if p["class"] == "conservative")
assert conservative == [204], conservative

inv = {c["label"]: c["status"] for c in investigation_certificates()}
assert inv["L_probe_profiles_reproducible"] == "PASS"
assert inv["L_twin_active_fraction_comp"] == "HONEST_NEGATIVE"
assert inv["L_probe_uniform_short_cycle"] == "HONEST_NEGATIVE"

print("ruleset investigation validation passed")