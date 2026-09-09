"""validate_preregistered_delta_star_sweep: independent re-scoring of
the declared predictions.

Re-pulls the round-40 propagation stream itself, recomputes delta*
and rel* from the raw chains, and applies the SAME decision rules with
independently redeclared thresholds -- then checks each prediction
certificate's status against the validator's own P1..P4 evaluation.
What is checked for independence is the scoring, not the predictions:
the predictions are the audit's a priori record, by design.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_mi_closure_chain_audit import (  # noqa: E402
    _N_PHASES,
    _wrap_pi,
    closure_chains,
)
from soliton_eca.soliton_mi_closure_chain_audit import _OMEGAS as _OMS  # noqa: E402
from soliton_eca.soliton_mi_closure_chain_audit import _EPSES as _EPSS  # noqa: E402
from soliton_eca.preregistered_delta_star_sweep import (  # noqa: E402
    _FAR_PHASES,
    _NEAR_ZERO_SET,
    _PREDICTIONS,
    pre_sweep_certificates,
)

_NEAR_TOL = 0.5
_RANGE_FLOOR = 2.0
_DISTINCT_FLOOR = 1.0

table = closure_chains()
dstar: dict = {}
rstar: dict = {}
for (om, eps), phases in table.items():
    per_d = {}
    per_r = {}
    for p in range(_N_PHASES):
        key = f"p{p}"
        ch = phases[key]
        per_d[key] = float(np.mean([c["delta"] for c in ch])) if ch else float("nan")
        per_r[key] = float(np.mean([c["rel1"] for c in ch])) if ch else float("nan")
    dstar[(om, eps)] = per_d
    rstar[(om, eps)] = per_r

pred1 = all(
    {p for p in range(_N_PHASES)
     if abs(dstar[(om, eps)][f"p{p}"]) <= _NEAR_TOL} == _NEAR_ZERO_SET
    for om in _OMS for eps in _EPSS)
pred2 = all(
    dstar[(om, eps)][f"p{p}"] < 0
    for om in _OMS for eps in _EPSS for p in _FAR_PHASES)
pred3 = all(
    max(dstar[(om, eps)][f"p{p}"] for p in range(_N_PHASES))
    - min(dstar[(om, eps)][f"p{p}"] for p in range(_N_PHASES))
    >= _RANGE_FLOOR
    for om in _OMS for eps in _EPSS)
pred4 = all(
    any(abs(_wrap_pi(dstar[(om, eps)][f"p{p}"] - rstar[(om, eps)][f"p{p}"]))
        > _DISTINCT_FLOOR
        for p in range(_N_PHASES))
    for om in _OMS for eps in _EPSS)

expected = {"L_pr_pred1_near_zero": pred1,
            "L_pr_pred2_far_negative": pred2,
            "L_pr_pred3_range_scatter": pred3,
            "L_pr_pred4_distinct_rel": pred4}

certs, stats = pre_sweep_certificates()
status = {c["label"]: c["status"] for c in certs}
for lab, pred in expected.items():
    want = "PASS" if pred else "HONEST_NEGATIVE"
    assert status[lab] == want, (lab, status[lab], want)

assert len(_PREDICTIONS) >= 4
for p in _PREDICTIONS:
    assert all(k in p for k in ("hypothesis", "decision_rule",
                                "predicted", "fee"))
assert status["L_pr_protocol"] == "PASS"

for (om, eps) in table:
    rng = (max(dstar[(om, eps)][f"p{p}"] for p in range(_N_PHASES))
           - min(dstar[(om, eps)][f"p{p}"] for p in range(_N_PHASES)))
    assert rng >= 0.5  # sanity: the sweep is well-defined

print("pre-registered delta-star sweep validation passed")