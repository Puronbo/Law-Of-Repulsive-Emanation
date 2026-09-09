import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_mi_recurrence_chain_audit import (  # noqa: E402
    _MODES,
    _PUMP_CHAIN_CEIL,
    _REINFLATE_LEVEL,
    _REST_CHAIN_FLOOR,
    chain_certificates,
)

certs, data = chain_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_chain_pump_ceiling"] == "PASS"
assert status["L_chain_rest_floor"] == "PASS"
assert status["L_chain_reinflation"] == "PASS"
assert status["L_chain_periodic"] == "HONEST_NEGATIVE"

for m, _ in _MODES:
    chain = data[m]["chain"]
    assert len(chain) >= 2
    assert all(c["p0"] <= _PUMP_CHAIN_CEIL for c in chain)
    assert all(1.0 - c["p0"] >= _REST_CHAIN_FLOOR for c in chain)
    assert max(data[m]["inter_max"]) >= _REINFLATE_LEVEL
assert max(c["p0"] for d in data.values() for c in d["chain"]) <= \
    _PUMP_CHAIN_CEIL
assert min(1.0 - c["p0"] for d in data.values()
           for c in d["chain"]) >= _REST_CHAIN_FLOOR
assert len({round(c["p0"], 3) for d in data.values()
            for c in d["chain"]}) > 1

print("mi recurrence chain audit validation passed")