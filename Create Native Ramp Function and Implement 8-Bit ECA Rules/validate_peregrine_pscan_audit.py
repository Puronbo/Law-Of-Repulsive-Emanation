import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_peregrine_pscan_audit import (  # noqa: E402
    _P_SET,
    pscan_certificates,
)
from soliton_eca.soliton_peregrine_pscan_audit import (  # noqa: E402
    _analytic,
    _center,
    _dt,
    _grid,
)
from soliton_eca.soliton_physics import propagate, Fiber  # noqa: E402

status = {c["label"]: c["status"] for c in pscan_certificates()}
assert status["L_pscan_seed_ratio"] == "PASS"
assert status["L_pscan_universal_curve"] == "PASS"
assert status["L_pscan_breathes_back"] == "PASS"
assert status["L_pscan_energy"] == "PASS"

t = _grid()
ci = _center()
for P in _P_SET:
    u0 = _analytic(t, 0.0, P)
    ratio = np.abs(u0[ci]) / np.sqrt(P)
    assert abs(ratio - 3.0) <= 1e-3

print("peregrine p-scan audit validation passed")