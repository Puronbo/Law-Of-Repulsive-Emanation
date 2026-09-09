import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_damage_opening_transient_audit import (  # noqa: E402
    _GRID,
    _SPREAD_FLOOR,
    opening_certificates,
)

certs, (pr, mass) = opening_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_ot_mass_growth"] == "PASS"
assert status["L_ot_bgdominated"] == "PASS"
assert status["L_ot_universal_dip"] == "HONEST_NEGATIVE"

fm = [float(np.mean(mass[g])) for g in _GRID]
assert all(fm[i] < fm[i + 1] for i in range(len(fm) - 1))
for g in (2, 6):
    assert max(pr[g]) / min(pr[g]) >= _SPREAD_FLOOR
dips = [(pr[6][p] < pr[2][p] and pr[12][p] > pr[6][p])
        for p in range(len(pr[2]))]
assert not all(dips)

print("damage opening transient audit validation passed")