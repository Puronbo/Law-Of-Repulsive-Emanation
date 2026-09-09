import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_damage_modal_audit import (  # noqa: E402
    _INV_TOL,
    _TIMES,
    modal_certificates,
)

certs, tab = modal_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_dmod_transport_invariant"] == "PASS"
assert status["L_dmod_amplifier_concentrates"] == "PASS"
assert status["L_dmod_collapser_broadens"] == "PASS"
assert status["L_dmod_eraser_vanishes"] == "PASS"
assert status["L_dmod_amplifier_broadens"] == "HONEST_NEGATIVE"

t2 = tab[204]
t51 = tab[51]
assert all(abs(t2[g] - t2[2]) <= _INV_TOL for g in _TIMES)
assert all(abs(t51[g] - t51[2]) <= _INV_TOL for g in _TIMES)
assert all(abs(t2[g] - t51[g]) <= _INV_TOL for g in _TIMES)

t147 = tab[147]
pr = [t147[g] for g in _TIMES]
assert all(a > b for a, b in zip(pr, pr[1:]))
assert pr[0] / pr[-1] >= 3.5

t172 = tab[172]
assert t172[2] < t172[48] and t172[96] <= t172[48] * 1.01
assert t172[96] >= t172[48] * 0.99

assert tab[251][12] <= 1e-3 and tab[251][96] <= 1e-3

print("damage modal audit validation passed")