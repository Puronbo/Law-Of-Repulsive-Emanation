import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_crowd_probe_stability_audit import (  # noqa: E402
    _CORE,
    _CORE_CEIL,
    _FAR_FLOOR,
    _PROBES,
    stability_certificates,
)
from soliton_eca.soliton_eca import RULES  # noqa: E402

certs, f = stability_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_cs_transport_core"] == "PASS"
assert status["L_cs_set_instant"] == "HONEST_NEGATIVE"
assert status["L_cs_core_margin"] == "HONEST_NEGATIVE"
assert status["L_cs_far_margin"] == "HONEST_NEGATIVE"

sets = []
for p in range(_PROBES):
    s = {r for r in RULES if f[r]["f3"][p] == 3 * f[r]["f1"][p]}
    sets.append(s)
assert set.intersection(*sets) == _CORE
assert any(len(s) > len(_CORE) for s in sets)
assert any(f[147]["f2"][p] / f[147]["f1"][p] > _CORE_CEIL
           for p in range(_PROBES))
assert all(f[147]["f1"][p] > 0 for p in range(_PROBES))
assert any((f[147]["f3"][p] - f[147]["f2"][p]) / f[147]["f1"][p]
           < _FAR_FLOOR for p in range(_PROBES))

print("crowd probe stability audit validation passed")