import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_damage_concentration_persist_audit import (  # noqa: E402
    _AMP,
    _CONC_RATIO,
    _INV_TOL,
    _TIMES,
    _TRANSPORT,
    persist_certificates,
)

certs, tab = persist_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_cp_conc_persists"] == "PASS"
assert status["L_cp_iso_extended"] == "PASS"
assert status["L_cp_turnover"] == "HONEST_NEGATIVE"

pr147 = [tab[_AMP][g]["pr"] for g in _TIMES]
t2_147 = [tab[_AMP][g]["top2"] for g in _TIMES]
assert all(a > b for a, b in zip(pr147, pr147[1:]))
assert pr147[0] / pr147[-1] >= _CONC_RATIO
for g in _TIMES:
    for r in _TRANSPORT:
        base = tab[r][_TIMES[0]]
        assert abs(tab[r][g]["pr"] - base["pr"]) <= _INV_TOL
        assert abs(tab[r][g]["top2"] - base["top2"]) <= _INV_TOL
    assert abs(tab[204][g]["pr"] - tab[51][g]["pr"]) <= _INV_TOL
    assert abs(tab[204][g]["top2"] - tab[51][g]["top2"]) <= _INV_TOL
assert any(x > y for x, y in zip(t2_147, t2_147[1:]))

print("damage concentration persistence audit validation passed")