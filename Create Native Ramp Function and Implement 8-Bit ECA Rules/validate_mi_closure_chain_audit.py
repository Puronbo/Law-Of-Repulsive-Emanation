import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_mi_closure_chain_audit import (  # noqa: E402
    _DRIFT_CEIL,
    _EPSES,
    _N_PHASES,
    _OMEGAS,
    _wrap_pi,
    closure_certificates,
    closure_chains,
)

import numpy as np  # noqa: E402

certs, stats = closure_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_cl_chain_frozen"] == "HONEST_NEGATIVE"
assert status["L_cl_phase_dependent"] == "PASS"
assert status["L_cl_closure_label"] == "HONEST_NEGATIVE"

table = closure_chains()
spreads = {}
delta_star = {}
chain_max_p0 = {}
for (om, eps), phases in table.items():
    per_s = {}
    per_d = {}
    per_p = {}
    for p in range(_N_PHASES):
        key = f"p{p}"
        ch = phases[key]
        if len(ch) >= 1:
            ds = [c["delta"] for c in ch]
            per_d[key] = float(np.mean(ds))
            per_p[key] = max(c["p0"] for c in ch)
            per_s[key] = max(abs(_wrap_pi(dv - per_d[key])) for dv in ds)
        else:
            per_s[key] = 0.0
    spreads[(om, eps)] = per_s
    delta_star[(om, eps)] = per_d
    chain_max_p0[(om, eps)] = per_p

worst = max(v for (om, eps) in table
            for v in spreads[(om, eps)].values())
assert worst > _DRIFT_CEIL

for e in _EPSES:
    for om in _OMEGAS:
        vals = list(delta_star[(om, e)].values())
        assert max(vals) - min(vals) > 1.0

label_broken = False
for (om, eps), pmax in chain_max_p0.items():
    pairs = [(delta_star[(om, eps)][k], v)
             for k, v in pmax.items() if len(table[(om, eps)][k]) > 0]
    pairs.sort(key=lambda kv: kv[0])
    if len(pairs) >= 3 and not all(
            pairs[i][1] <= pairs[i + 1][1]
            for i in range(len(pairs) - 1)):
        label_broken = True
assert label_broken

print("mi closure chain audit validation passed")