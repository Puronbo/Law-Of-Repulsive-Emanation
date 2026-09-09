import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_density_flow_audit import (  # noqa: E402
    _HALF_BIASED,
    _stationary,
    _tail_means,
    density_flow_certificates,
)

status = {c["label"]: c["status"] for c in density_flow_certificates()}
assert status["L_density_exact_invariant"] == "PASS"
assert status["L_density_stationary_settles"] == "PASS"
assert status["L_density_half_attractor"] == "HONEST_NEGATIVE"
assert status["L_density_two_lap_oscillates"] == "PASS"

means = _tail_means()
nonstationary = set(_stationary()) ^ {r for r in means}
assert _HALF_BIASED <= nonstationary
for r in _HALF_BIASED:
    assert abs(means[r] - 0.5) > 0.08

print("density flow audit validation passed")