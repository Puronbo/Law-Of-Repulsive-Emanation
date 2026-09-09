import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_mi_phase_invariant_sweep import (  # noqa: E402
    _DRIFT_CEIL,
    _EPSES,
    _N_PHASES,
    _OMEGAS,
    _wrap_pi,
    geometry_data,
    invariant_sweep_certificates,
)

certs, stats = invariant_sweep_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_inv_lock_low_mod"] == "PASS"
assert status["L_inv_drift_band_mono"] == "PASS"
assert status["L_inv_omega1_reference"] == "PASS"
assert status["L_inv_lock_geometry"] == "HONEST_NEGATIVE"
assert status["L_inv_antiphase_fragile"] == "HONEST_NEGATIVE"

data = geometry_data()


def drift_max(eps, om):
    worst = 0.0
    for p in range(_N_PHASES):
        phi2 = 2 * p * np.pi / _N_PHASES
        for c in data[(eps, om)][f"p{p}"]:
            worst = max(worst, abs(_wrap_pi(c["rel1"] - phi2)))
    return worst


def chain_max(eps, om):
    out = {}
    for p in range(_N_PHASES):
        chain = data[(eps, om)][f"p{p}"]
        if chain:
            out[f"p{p}"] = max(c["p0"] for c in chain)
    return out


for om in _OMEGAS:
    if any(data[(0.20, om)][f"p{p}"] for p in range(_N_PHASES)):
        assert drift_max(0.20, om) <= _DRIFT_CEIL

d05 = [drift_max(e, 0.5) for e in _EPSES]
assert d05[0] < d05[1] < d05[2]

cm = chain_max(0.20, 1.0)
assert abs(drift_max(0.20, 1.0) - 0.156) <= 0.01
assert max(cm, key=lambda k: cm[k]) == "p4"

assert drift_max(0.45, 0.5) > _DRIFT_CEIL
assert drift_max(0.30, 1.0) > _DRIFT_CEIL

cm31 = chain_max(0.30, 1.0)
assert cm31 and max(cm31, key=lambda k: cm31[k]) != "p4"
cm451 = chain_max(0.45, 1.0)
assert max(cm451, key=lambda k: cm451[k]) != "p4"

assert all(not data[(0.20, 2.0)][f"p{p}"] for p in range(_N_PHASES))
assert all(not data[(0.30, 2.0)][f"p{p}"] for p in range(_N_PHASES))

print("mi phase invariant sweep validation passed")