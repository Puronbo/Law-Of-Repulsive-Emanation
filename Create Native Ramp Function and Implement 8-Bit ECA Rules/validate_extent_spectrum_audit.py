import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_extent_spectrum_audit import (  # noqa: E402
    _ERASE_LEVEL,
    _ERASER_SET,
    _KS,
    _TRANSPARENT_SET,
    _WIDTH,
    extent_certificates,
    extent_table,
)

certs, table = extent_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_extent_transparent_exact"] == "PASS"
assert status["L_extent_family_saturates"] == "PASS"
assert status["L_extent_erasers_exact"] == "PASS"
assert status["L_extent_ranking_preserved"] == "HONEST_NEGATIVE"

for r in _TRANSPARENT_SET:
    for k in _KS:
        assert abs(table[r][k] - k / _WIDTH) <= 1 / _WIDTH
assert max(table[r][32] for r in table) <= 0.12
erasers = {r for r in table if all(table[r][k] <= _ERASE_LEVEL
                                   for k in _KS)}
assert erasers == _ERASER_SET

print("extent spectrum audit validation passed")