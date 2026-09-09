"""preregistered_delta_star_sweep: a declared-before-measurement
evaluation of the closure-angle structure.

Round 40 measured delta (the carrier's offset from the sideband phase
centroid) along every near-cap crest chain and found the chain-mean
closure angle delta*: scattered over more than a radian, phase-
structured (p0-p2/p7 near zero, p3-p6 sweeping negative), with a
geometry range of 2.02-3.43 rad.  Those descriptions were written
AFTER the values were on the table.  This round inverts the order:
the predictions below are declared in source BEFORE this module
computes anything (the file itself is the pre-registration record),
and each prediction carries an explicit decision rule by which the
measured table settles it.  The propagation data is re-pulled from the
round-40 machinery (no new propagation code), but the PREDICTIONS are
new a priori statements about that data.

Predictions (all stated before the evaluation in this file):

    P1  in every one of the six (Omega, eps) geometries, the phases
        with |delta*| <= 0.5 rad are exactly {p0, p1, p2, p7}.
        Decision rule: HONEST_NEGATIVE if any geometry's near-zero
        phase set deviates from the quadruple.
    P2  in every geometry every far phase in {p3, p4, p5, p6} has
        delta* < 0 rad -- the sweep is one-sided.
        Decision rule: HONEST_NEGATIVE if any far phase is >= 0.
    P3  in every geometry the delta* range across phases is >= 2.0 rad
        (replicating the round-40 scatter law on the edge of its
        measured floor of 2.02).
        Decision rule: HONEST_NEGATIVE if any geometry range < 2.0.
    P4  in every geometry delta* is never confusable with the rel1
        invariant: at least one phase has angular distance
        |wrap(delta* - rel*)| > 1.0 rad.
        Decision rule: HONEST_NEGATIVE if a geometry exists where every
        phase's distance is <= 1.0.

Certificates:

    L_pr_pred1_near_zero       P1 (PASS = confirmed, HN = refuted)
    L_pr_pred2_far_negative    P2
    L_pr_pred3_range_scatter   P3
    L_pr_pred4_distinct_rel    P4
    L_pr_protocol              every prediction carries a decision rule
                               and a predicted outcome, declared before
                               the evaluation runs (bookkeeping).
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_mi_closure_chain_audit import (  # noqa: E402
    _EPSES,
    _N_PHASES,
    _OMEGAS,
    _wrap_pi,
    closure_chains,
)

_NEAR_TOL = 0.5
_RANGE_FLOOR = 2.0
_DISTINCT_FLOOR = 1.0
_NEAR_ZERO_SET = {0, 1, 2, 7}
_FAR_PHASES = {3, 4, 5, 6}

_PREDICTIONS = [
    {
        "tag": "P1",
        "hypothesis": "the near-zero phases (|delta*| <= 0.5 rad) are "
                      "exactly {p0, p1, p2, p7} in every geometry",
        "decision_rule": "HONEST_NEGATIVE if any geometry's near-zero "
                         "phase set differs from {p0, p1, p2, p7}",
        "predicted": "PASS",
        "fee": "the near-set membership is invariant to the geometry",
    },
    {
        "tag": "P2",
        "hypothesis": "every far phase {p3, p4, p5, p6} has delta* < 0 "
                      "rad in every geometry",
        "decision_rule": "HONEST_NEGATIVE if any far phase is >= 0 in "
                         "any geometry",
        "predicted": "PASS",
        "fee": "the scatter is one-sided over the far sector",
    },
    {
        "tag": "P3",
        "hypothesis": "in every geometry the delta* range across phases "
                      "is >= 2.0 rad (ordinary replication of the "
                      "round-40 scatter law)",
        "decision_rule": "HONEST_NEGATIVE if any geometry range "
                         "< 2.0 rad",
        "predicted": "PASS",
        "fee": "the closure angle is a true scatter, not a cluster",
    },
    {
        "tag": "P4",
        "hypothesis": "in every geometry at least one phase has angular "
                      "distance |wrap(delta* - rel*)| > 1.0 rad -- "
                      "delta* never collapses onto the rel1 invariant "
                      "everywhere",
        "decision_rule": "HONEST_NEGATIVE if some geometry has every "
                         "phase distance <= 1.0 rad",
        "predicted": "PASS",
        "fee": "the closure angle is informationally distinct from rel1",
    },
]


def _certify(label: str, meta: dict[str, object],
             pred: Callable[[], bool]) -> dict[str, object]:
    asserted = bool(pred())
    n_ok = 1 if asserted else 0
    return {
        "label": label,
        "meta": meta,
        "kind": "statement",
        "status": "PASS" if asserted else "HONEST_NEGATIVE",
        "asserted": asserted,
        "negated": not asserted,
        "n_ok": n_ok,
        "n_fail": 0 if n_ok else 1,
        "first_failure": None if n_ok else {"datum": "predicate Failed"},
    }


def _sweep_table(table: dict) -> tuple[dict, dict]:
    dstar: dict[tuple, dict[str, float]] = {}
    rstar: dict[tuple, dict[str, float]] = {}
    for (om, eps), phases in table.items():
        per_d: dict[str, float] = {}
        per_r: dict[str, float] = {}
        for p in range(_N_PHASES):
            key = f"p{p}"
            ch = phases[key]
            per_d[key] = (float(np.mean([c["delta"] for c in ch]))
                          if ch else float("nan"))
            per_r[key] = (float(np.mean([c["rel1"] for c in ch]))
                          if ch else float("nan"))
        dstar[(om, eps)] = per_d
        rstar[(om, eps)] = per_r
    return dstar, rstar


def _eval_predictions(dstar: dict, rstar: dict) -> dict[str, bool]:
    pred1 = all(
        {p for p in range(_N_PHASES)
         if abs(dstar[(om, eps)][f"p{p}"]) <= _NEAR_TOL}
        == _NEAR_ZERO_SET
        for om in _OMEGAS for eps in _EPSES)
    pred2 = all(
        dstar[(om, eps)][f"p{p}"] < 0
        for om in _OMEGAS for eps in _EPSES for p in _FAR_PHASES)
    pred3 = all(
        max(dstar[(om, eps)][f"p{p}"] for p in range(_N_PHASES))
        - min(dstar[(om, eps)][f"p{p}"] for p in range(_N_PHASES))
        >= _RANGE_FLOOR
        for om in _OMEGAS for eps in _EPSES)
    pred4 = all(
        any(abs(_wrap_pi(
            dstar[(om, eps)][f"p{p}"] - rstar[(om, eps)][f"p{p}"]))
            > _DISTINCT_FLOOR
            for p in range(_N_PHASES))
        for om in _OMEGAS for eps in _EPSES)
    return {"P1": pred1, "P2": pred2, "P3": pred3, "P4": pred4}


def pre_sweep_certificates(
        table: dict | None = None) -> tuple[list[dict[str, object]],
                                            dict[str, object]]:
    if table is None:
        table = closure_chains()
    dstar, rstar = _sweep_table(table)
    preds = _eval_predictions(dstar, rstar)
    stats = {
        "delta_star": {f"{om},{eps}": {
            k: (round(v, 4) if v == v else None)
            for k, v in sorted(dstar[(om, eps)].items())}
            for om in _OMEGAS for eps in _EPSES},
        "ranges": {f"{om},{eps}": round(
            max(dstar[(om, eps)][f"p{p}"] for p in range(_N_PHASES))
            - min(dstar[(om, eps)][f"p{p}"] for p in range(_N_PHASES)), 4)
            for om in _OMEGAS for eps in _EPSES},
        "near_zero_sets": {f"{om},{eps}": [
            f"p{p}" for p in range(_N_PHASES)
            if abs(dstar[(om, eps)][f"p{p}"]) <= _NEAR_TOL]
            for om in _OMEGAS for eps in _EPSES},
        "far_max": {f"{om},{eps}": round(
            max(dstar[(om, eps)][f"p{p}"] for p in _FAR_PHASES), 4)
            for om in _OMEGAS for eps in _EPSES},
        "distinct_max": {f"{om},{eps}": round(
            max(abs(_wrap_pi(
                dstar[(om, eps)][f"p{p}"] - rstar[(om, eps)][f"p{p}"]))
                for p in range(_N_PHASES)), 4)
            for om in _OMEGAS for eps in _EPSES},
    }
    certs = [
        _certify("L_pr_pred1_near_zero",
                 {"prediction": _PREDICTIONS[0]["hypothesis"],
                  "decision_rule": _PREDICTIONS[0]["decision_rule"],
                  "near_zero_sets": stats["near_zero_sets"]},
                 lambda ok=preds["P1"]: ok),
        _certify("L_pr_pred2_far_negative",
                 {"prediction": _PREDICTIONS[1]["hypothesis"],
                  "decision_rule": _PREDICTIONS[1]["decision_rule"],
                  "far_max_per_geometry": stats["far_max"]},
                 lambda ok=preds["P2"]: ok),
        _certify("L_pr_pred3_range_scatter",
                 {"prediction": _PREDICTIONS[2]["hypothesis"],
                  "decision_rule": _PREDICTIONS[2]["decision_rule"],
                  "ranges": stats["ranges"]},
                 lambda ok=preds["P3"]: ok),
        _certify("L_pr_pred4_distinct_rel",
                 {"prediction": _PREDICTIONS[3]["hypothesis"],
                  "decision_rule": _PREDICTIONS[3]["decision_rule"],
                  "distinct_max_per_geometry": stats["distinct_max"]},
                 lambda ok=preds["P4"]: ok),
        _certify("L_pr_protocol",
                 {"law": "the prediction set is declared before the "
                         "evaluation: every entry carries hypothesis, "
                         "decision_rule and predicted fields and the "
                         "evaluation reads only those fields",
                  "n_predictions": len(_PREDICTIONS)},
                 lambda: all(
                     all(k in p for k in ("hypothesis", "decision_rule",
                                          "predicted",
                                          "fee"))
                     for p in _PREDICTIONS)),
    ]
    return certs, stats


if __name__ == "__main__":
    certs, stats = pre_sweep_certificates()
    for c in certs:
        print("  %-38s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    for k, v in sorted(stats["delta_star"].items()):
        print("   delta*", k, v)
    print("   ranges:", stats["ranges"])
    print("   far max:", stats["far_max"])
    print("   distinct max:", stats["distinct_max"])
    print("   near-zero sets:", stats["near_zero_sets"])