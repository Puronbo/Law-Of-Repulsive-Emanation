import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_entropy_cascade import (  # noqa: E402
    entropy_certificates, entropy_cascade,
)

status = {c["label"]: c["status"] for c in entropy_certificates()}
assert status["L_entropy_lossless_pair"] == "PASS"
assert status["L_entropy_reproducible"] == "PASS"
assert status["L_entropy_twin_dominance"] == "HONEST_NEGATIVE"
assert status["L_entropy_fast_dissipation"] == "HONEST_NEGATIVE"

assert entropy_cascade(204)["lossless"] and entropy_cascade(51)["lossless"]
assert all(not entropy_cascade(r)["lossless"]
           for r in (4, 12, 27, 44, 76, 108, 172, 236))
# Atomic anchors of the honest negatives.
assert entropy_cascade(44)["retained"] < entropy_cascade(211)["retained"]
assert entropy_cascade(251)["half_life"] == 2
assert entropy_cascade(27)["half_life"] is None

print("entropy-cascade validation passed")