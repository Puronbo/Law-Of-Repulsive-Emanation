import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_damage_crystallization_audit import (  # noqa: E402
    _AMP,
    _INV_TOL,
    _RISE_RATIO,
    _SUPERMAJORITY,
    _TIMES,
    _TRANSPORT,
    cry_certificates,
)

certs, tab = cry_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_cry_amplifier_rises"] == "PASS"
assert status["L_cry_transport_const"] == "PASS"
assert status["L_cry_supermajority"] == "HONEST_NEGATIVE"

a = [tab[_AMP][g] for g in _TIMES]
assert all(y > x for x, y in zip(a, a[1:]))
assert a[-1] / a[0] >= _RISE_RATIO
for g in _TIMES:
    assert abs(tab[204][g] - tab[51][g]) <= _INV_TOL
    assert abs(tab[204][g] - tab[204][_TIMES[0]]) <= _INV_TOL
assert max(a) < _SUPERMAJORITY

print("damage crystallization audit validation passed")