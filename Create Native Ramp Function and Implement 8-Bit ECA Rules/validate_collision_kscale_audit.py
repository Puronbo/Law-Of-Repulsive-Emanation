import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_collision_kscale_audit import (  # noqa: E402
    _ADD_TOL,
    _KS,
    _WIDTH,
    kscale_certificates,
)

certs, f = kscale_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_kscale_isometries"] == "PASS"
assert status["L_kscale_intersection"] == "PASS"
assert status["L_kscale_251_zero"] == "PASS"
assert status["L_kscale_set_invariant"] == "HONEST_NEGATIVE"

w = _WIDTH
for k in _KS:
    for r in (204, 51):
        assert abs(f[k][r]["f1"] - k / w) <= _ADD_TOL
        assert abs(f[k][r]["f2"] - 2 * k / w) <= _ADD_TOL
        assert abs(f[k][r]["f3"] - 3 * k / w) <= _ADD_TOL
    assert all(abs(f[k][251][key]) <= _ADD_TOL
               for key in ("f1", "f2", "f3"))

sets = {k: {r for r, d in f[k].items()
            if abs(d["f3"] - 3 * d["f1"]) <= _ADD_TOL} for k in _KS}
inter = set.intersection(*sets.values())
assert inter == {204, 51, 251}
assert len({frozenset(v) for v in sets.values()}) > 1

print("collision kscale audit validation passed")