import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_mi_carrierfree_crest_audit import (  # noqa: E402
    _EPS_SET,
    _SECOND_CEIL,
    _STACK_FLOOR,
    _VOID_CEIL,
    carrierfree_certificates,
)

certs, data = carrierfree_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_cf_void_first"] == "PASS"
assert status["L_cf_twopair_stack"] == "PASS"
assert status["L_cf_second_void"] == "PASS"
assert status["L_cf_chain_void"] == "HONEST_NEGATIVE"

assert set(data) == {str(e) for e in _EPS_SET}
for e in data:
    assert len(data[e]) >= 2
assert max(c["p0"] for e in data for c in data[e][:1]) <= _VOID_CEIL
assert min((c["p1"] + c["p2"]) for e in data for c in data[e][:1]) \
    >= _STACK_FLOOR
assert max(c["p0"] for e in data
           for c in data[e][1:2]) <= _SECOND_CEIL
assert max(c["p0"] for e in data for c in data[e]) > _SECOND_CEIL

print("mi carrier-free crest audit validation passed")