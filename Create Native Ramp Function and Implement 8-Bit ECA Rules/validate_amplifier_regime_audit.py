import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_amplifier_regime_audit import (  # noqa: E402
    _COLLAPSE,
    _ERASERS,
    _REACH,
    _SPARSE,
    _TRANSPORT,
    regime_certificates,
)

certs = regime_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_regime_reach_collapse_pair"] == "PASS"
assert status["L_regime_transport_growth_free"] == "PASS"
assert status["L_regime_eraser_sparse_identity"] == "PASS"
assert status["L_regime_collapsers_amplify"] == "HONEST_NEGATIVE"

assert sorted(_REACH & _COLLAPSE) == [172, 228]
assert not (_TRANSPORT & (_REACH | _COLLAPSE | _ERASERS))
assert _ERASERS == _SPARSE

print("amplifier regime audit validation passed")