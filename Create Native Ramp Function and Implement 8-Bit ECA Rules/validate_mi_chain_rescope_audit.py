import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_mi_chain_rescope_audit import (  # noqa: E402
    _EPS_SET,
    _FINAL_CEIL,
    _NEAR_CAP,
    _SHED_FRAC,
    _STACK_FLOOR,
    _VOID_CEIL,
    rescope_certificates,
    rescope_data,
)

certs, stats = rescope_certificates()
status = {c["label"]: c["status"] for c in certs}
for label in ("L_cr_first_coincide", "L_cr_ridges_in_chain",
              "L_cr_return_survives", "L_cr_destack_survives",
              "L_cr_mono_bump"):
    assert status[label] == "PASS"

for e in _EPS_SET:
    loose = rescope_data()[str(e)]["loose"]
    nc = rescope_data()[str(e)]["nearcap"]
    assert len(loose) == len(nc)
    assert all(c["R"] >= _NEAR_CAP for c in loose)
    assert nc[0]["p0"] <= _VOID_CEIL
    assert nc[0]["p1"] + nc[0]["p2"] >= _STACK_FLOOR
    assert max(c["p0"] for c in nc) > _VOID_CEIL

for e in _EPS_SET:
    nc = rescope_data()[str(e)]["nearcap"]
    assert nc[1]["p1"] + nc[1]["p2"] <= _SHED_FRAC * (
        nc[0]["p1"] + nc[0]["p2"])
    assert nc[-1]["p1"] + nc[-1]["p2"] < _FINAL_CEIL
    assert all(c["p1"] > c["p2"] for c in nc)

e45 = rescope_data()["0.45"]["nearcap"]
stk = [c["p1"] + c["p2"] for c in e45]
assert stk[2] > stk[1]

print("mi chain rescope audit validation passed")