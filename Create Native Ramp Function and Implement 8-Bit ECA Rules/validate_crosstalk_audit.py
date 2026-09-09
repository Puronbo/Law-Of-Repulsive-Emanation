import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_crosstalk_audit import (  # noqa: E402
    crosstalk_certificates, multi_failures, placement_ok, _gap_one, _RULE_TABLE,
)

status = {c["label"]: c["status"] for c in crosstalk_certificates()}
assert status["L_crosstalk_rule204_multiplex"] == "PASS"
assert status["L_crosstalk_unique_carrier"] == "PASS"
assert status["L_crosstalk_236_gap_law"] == "PASS"
assert status["L_crosstalk_236_naive"] == "HONEST_NEGATIVE"

assert multi_failures(204) == 0
assert all(multi_failures(r) > 0 for r in _RULE_TABLE if r != 204)

# Spot-check the gap law: gap-1 choices fail, gap-2 and adjacent choices pass.
assert not placement_ok(236, 8, (0, 2), 1)   # '1 0 1...' collapses
assert placement_ok(236, 8, (0, 3), 1)       # '1 00 1...' persists
assert placement_ok(236, 8, (0, 1), 1)       # adjacent merges into a block
assert _gap_one((0, 2), 1) and not _gap_one((0, 3), 1)

print("crosstalk audit validation passed")