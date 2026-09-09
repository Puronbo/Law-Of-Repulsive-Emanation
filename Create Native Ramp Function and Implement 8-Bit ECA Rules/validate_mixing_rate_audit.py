import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_mixing_rate_audit import (  # noqa: E402
    _COLLAPSE_SET,
    _SPARSE_SET,
    mixing_rate_certificates,
)

certs, table = mixing_rate_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_variance_collapse_pair"] == "PASS"
assert status["L_variance_collapse_fast"] == "PASS"
assert status["L_variance_sparse_basins"] == "PASS"
assert status["L_variance_isometry_exact"] == "PASS"
assert status["L_variance_homogenizer"] == "HONEST_NEGATIVE"

for r in _COLLAPSE_SET:
    assert table[r]["ratio"] <= 0.6 and table[r]["ratio20"] <= 0.6
for r in _SPARSE_SET:
    assert table[r]["V100"] <= 0.06
assert table[204]["V100"] == table[204]["V2"]
assert table[51]["V100"] == table[51]["V2"]
assert table[251]["V100"] <= 0.01

print("mixing rate audit validation passed")