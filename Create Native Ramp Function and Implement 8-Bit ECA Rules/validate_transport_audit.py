import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_transport_audit import (  # noqa: E402
    transport_certificates, bus_reconstitution_failures, _block_storage_holds,
    _RULE_TABLE,
)

status = {c["label"]: c["status"] for c in transport_certificates()}
assert status["L_transport_rule204_bus_identity"] == "PASS"
assert status["L_transport_storage_pair_exact"] == "PASS"
assert status["L_transport_rule236_block_storage"] == "PASS"
assert status["L_transport_ring_lap_reconstitution"] == "HONEST_NEGATIVE"
assert status["L_transport_bus_lap_reconstitution"] == "HONEST_NEGATIVE"
assert status["L_transport_rigid_conveyor"] == "HONEST_NEGATIVE"

assert bus_reconstitution_failures(204) == 0
assert bus_reconstitution_failures(236) == 0
assert all(bus_reconstitution_failures(r) > 0
           for r in _RULE_TABLE if r not in (204, 236))
assert _block_storage_holds()

print("transport audit validation passed")