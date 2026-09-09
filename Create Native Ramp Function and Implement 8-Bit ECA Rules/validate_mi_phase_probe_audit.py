import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_mi_phase_probe_audit import (  # noqa: E402
    _NEAR_CAP,
    _SECOND_CEIL,
    _VOID_CEIL,
    phase_certificates,
    phase_data,
)

certs, stats = phase_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_ph_formed"] == "PASS"
assert status["L_ph_void_first"] == "PASS"
assert status["L_ph_stack_first"] == "PASS"
assert status["L_ph_second"] == "HONEST_NEGATIVE"
assert status["L_ph_chain_void"] == "HONEST_NEGATIVE"

first = stats["first"]
second = stats["second"]
chain_max = stats["chain_max"]
assert len(first) == 8
for k in "p0 p1 p2 p3 p4 p5 p6 p7".split():
    assert first[k]["p0"] <= _VOID_CEIL
    assert first[k]["p1"] + first[k]["p2"] >= 0.60
    assert first[k]["R"] >= _NEAR_CAP
    assert chain_max[k] > _VOID_CEIL
assert second["p4"]["p0"] > _SECOND_CEIL
assert second["p3"]["p0"] > _SECOND_CEIL
assert all(second[k]["p0"] <= _SECOND_CEIL
           for k in second if k not in ("p3", "p4"))

data = phase_data()
assert len(data) == 8
assert all(len(c) >= 2 for c in data.values())

print("mi phase probe audit validation passed")