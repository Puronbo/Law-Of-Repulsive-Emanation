import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_damage_probe_universality_audit import (  # noqa: E402
    _CONC_FLOOR,
    universality_certificates,
)

certs, (pr, top) = universality_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_pu_conc_universal"] == "PASS"
assert status["L_pu_cry_universal"] == "PASS"
assert status["L_pu_opening_exception"] == "HONEST_NEGATIVE"

n = len(pr[2])
assert all(pr[96][p] < pr[2][p] for p in range(n))
assert min(pr[2][p] / pr[384][p] for p in range(n)) >= _CONC_FLOOR
assert all(top[96][p] > top[2][p] for p in range(n))
assert all(top[384][p] < top[192][p] for p in range(n))
assert any(pr[12][p] > pr[2][p] for p in range(n))
assert any(pr[12][p] < pr[2][p] for p in range(n))

print("damage probe universality audit validation passed")