import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_mi_phase_mechanism_audit import (  # noqa: E402
    _DRIFT_CEIL,
    _N_PHASES,
    _wrap_pi,
    mechanism_certificates,
    mechanism_data,
)

certs, stats = mechanism_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_ph_rel1_conserved"] == "PASS"
assert status["L_ph_antiphase_peak"] == "PASS"
assert status["L_ph_rel1_mechanism"] == "HONEST_NEGATIVE"

data = mechanism_data()
for p in range(_N_PHASES):
    phi2 = 2 * p * np.pi / _N_PHASES
    for c in data[f"p{p}"]:
        assert abs(_wrap_pi(c["rel1"] - phi2)) <= _DRIFT_CEIL

chain_max = stats["chain_max"]
assert chain_max["p4"] > max(v for k, v in chain_max.items()
                             if k != "p4")
second = stats["second"]
pairs = sorted((float(np.cos(c["rel1"])), c["p0"])
               for c in second.values())
assert any(pairs[i][1] > pairs[i + 1][1]
           for i in range(len(pairs) - 1))

print("mi phase mechanism audit validation passed")