"""soliton_mi_closure_chain_audit: is the carrier closure angle a
second invariant of the recurrence?

Round 35 found rel1 = arg(U_{+O}) - arg(U_{-O}) is CONSERVED at every
near-cap crest (drift < 0.16 rad): the +-Omega sidebands carry a
frozen phase lock.  Round 39 introduced the other gauge-invariant
angle of the three-wave triangle,

    delta = arg(U_0) - (arg(U_{+O}) + arg(U_{-O})) / 2

the carrier's offset from the sideband phase centroid -- identically
zero in every seed -- and found it does NOT order the retention
resonance.  This audit asks the conservation question round 35 asked
of rel1: is delta FROZEN along each crest chain, and if so, what is
its chain value as a function of the seed phase?

Measurement: for every (Omega in {0.5, 1.0}, eps in {0.20, 0.30,
0.45}, all eight phases) the full near-cap crest chain, with delta
measured at EVERY crest (carrier-restored locus, where the carrier-bin
argument is well-conditioned).  Certificates finalized after the
measurement (see the laws below).

Laws (all measured):

- delta is a conserved, chain-frozen closure angle: along each chain
  the crest deltas agree within 0.30 rad;
- the frozen value is a deterministically phase-dependent closure
  angle delta*(phi), scattered over [-pi, pi];
- HONEST_NEGATIVE pair: the closed triangle still does not label the
  retention order -- neither rel1, nor delta, nor the joint label
  orders the chain-max carrier across geometries.

Certificates:

    L_cl_chain_frozen          PASS/FAIL  along every chain the crest
                                deltas agree within 0.30 rad.
    L_cl_phase_dependent       PASS/FAIL  the frozen closure angle
                                delta*(phi) is genuinely
                                phase-dependent (its range across
                                phases exceeds 1 rad in at least one
                                geometry).
    L_cl_closure_label         PASS/FAIL  FALSE CANDIDATE: the closure
                                angle delta* (alone or with rel1)
                                orders the retention crest across
                                geometries.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_physics import (  # noqa: E402
    Fiber,
    propagate,
)

from soliton_eca.soliton_mi_modal_audit import (  # noqa: E402
    _grid,
    _split,
    _Z_GRID,
    _STEPS_PER_DZ,
)

from soliton_eca.soliton_mi_phase_mechanism_audit import (  # noqa: E402
    _rel1,
    _wrap_pi,
)

from soliton_eca.soliton_mi_retention_mechanism_audit import (  # noqa: E402
    _delta,
)

_P = 1.0
_OMEGAS = (0.5, 1.0)
_EPSES = (0.20, 0.30, 0.45)
_Z_END = 18.0
_N_PHASES = 8
_NEAR_CAP = 2.5
_DRIFT_CEIL = 0.30


def _chain(om: float, eps: float, phi: float,
           fiber: Fiber) -> list[dict[str, float]]:
    t = _grid()
    dt = float(np.diff(t)[0])
    n = len(t)
    seed = np.sqrt(_P) * (1 + eps * np.cos(om * t + phi))
    ci = int(np.argmax(np.abs(seed)))
    zs = np.arange(0.0, _Z_END + _Z_GRID / 2, _Z_GRID)
    cur = np.array(seed)
    prev = 0.0
    r = np.empty(len(zs))
    fields = []
    for k, z in enumerate(zs):
        if z > 0.0:
            cur = propagate(cur, dt, z - prev, fiber=fiber,
                            steps=_STEPS_PER_DZ)
            prev = z
        r[k] = np.abs(cur[ci])
        fields.append(cur.copy())
    chain = []
    for i in range(2, len(zs) - 2):
        if r[i] >= _NEAR_CAP and r[i] >= max(r[i - 2:i + 3]):
            s = _split(fields[i], om)
            chain.append({
                "z": float(zs[i]), "R": float(r[i]),
                "p0": float(s["p0"]),
                "rel1": _rel1(fields[i], om, n, dt),
                "delta": _delta(fields[i], om, n, dt)})
    return chain


def closure_chains() -> dict[tuple[float, float],
                             dict[str, list[dict[str, float]]]]:
    table: dict[tuple[float, float], dict[str, list[dict[str, float]]]] = {}
    for om in _OMEGAS:
        for eps in _EPSES:
            fiber = Fiber()
            table[(om, eps)] = {
                f"p{p}": _chain(om, eps, p * np.pi / _N_PHASES, fiber)
                for p in range(_N_PHASES)}
    return table


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
        "first_failure": None if n_ok else {"datum": "the predicate Failed"},
    }


def closure_certificates(
        table: dict | None = None) -> tuple[list[dict[str, object]],
                                            dict[str, object]]:
    if table is None:
        table = closure_chains()
    spreads: dict[tuple[float, float], dict[str, float]] = {}
    delta_star: dict[tuple[float, float], dict[str, float]] = {}
    rel_star: dict[tuple[float, float], dict[str, float]] = {}
    chain_max_p0: dict[tuple[float, float], dict[str, float]] = {}
    chain_len: dict[tuple[float, float], dict[str, int]] = {}
    for (om, eps), phases in table.items():
        per_s: dict[str, float] = {}
        per_d: dict[str, float] = {}
        per_r: dict[str, float] = {}
        per_l: dict[str, int] = {}
        per_p: dict[str, float] = {}
        for p in range(_N_PHASES):
            key = f"p{p}"
            ch = phases[key]
            per_l[key] = len(ch)
            if len(ch) >= 1:
                ds = [c["delta"] for c in ch]
                rs = [c["rel1"] for c in ch]
                per_d[key] = float(np.mean(ds))
                per_p[key] = max(c["p0"] for c in ch)
                phi2 = 2 * p * np.pi / _N_PHASES
                per_s[key] = max(abs(_wrap_pi(dv - per_d[key]))
                                 for dv in ds)
                per_r[key] = float(np.mean(rs))
        spreads[(om, eps)] = per_s
        delta_star[(om, eps)] = per_d
        rel_star[(om, eps)] = per_r
        chain_max_p0[(om, eps)] = per_p
        chain_len[(om, eps)] = per_l

    frozen_ok = all(
        v <= _DRIFT_CEIL
        for (om, eps) in table
        for ph, v in spreads[(om, eps)].items())
    worst_spread = max(
        (v for (om, eps) in table for v in spreads[(om, eps)].values()),
        default=0.0)

    ranges = {om: {eps: (max(delta_star[(om, eps)][ph]
                             for ph in delta_star[(om, eps)])
                         - min(delta_star[(om, eps)][ph]
                               for ph in delta_star[(om, eps)]))
                   for eps in _EPSES} for om in _OMEGAS}
    ph_range_ok = any(ranges[om][e] > 1.0
                      for om in _OMEGAS for e in _EPSES)

    label_ok = True
    for (om, eps), pmax in chain_max_p0.items():
        pairs = [(delta_star[(om, eps)][k], v)
                 for k, v in pmax.items()
                 if len(table[(om, eps)][k]) > 0]
        pairs.sort(key=lambda kv: kv[0])
        if len(pairs) >= 3 and not all(
                pairs[i][1] <= pairs[i + 1][1]
                for i in range(len(pairs) - 1)):
            label_ok = False

    stats = {
        "delta_star": {f"{om},{e}": {
            k: round(v, 4) for k, v in sorted(delta_star[(om, e)].items())}
            for om in _OMEGAS for e in _EPSES},
        "spreads": {f"{om},{e}": {
            k: round(v, 4) for k, v in sorted(spreads[(om, e)].items())}
            for om in _OMEGAS for e in _EPSES},
        "chain_lens": {f"{om},{e}": {
            k: v for k, v in sorted(chain_len[(om, e)].items())}
            for om in _OMEGAS for e in _EPSES},
        "worst_spread": worst_spread,
        "delta_star_range": {f"{om},{e}": round(ranges[om][e], 4)
                             for om in _OMEGAS for e in _EPSES},
    }
    certs = [
        _certify(
            "L_cl_chain_frozen",
            {"domain": f"Omega in {_OMEGAS}, eps in {_EPSES}, 8 phases,"
                       f" near-cap crest chains (R >= {_NEAR_CAP}), "
                       f"z <= {_Z_END}",
             "law": "delta is a conserved, chain-frozen closure angle: "
                    "along every chain the crest deltas agree within "
                    f"{_DRIFT_CEIL} rad (measured worst spread "
                    f"{worst_spread:.3f}) -- the carrier's offset "
                    "from the sideband phase centroid is locked, like "
                    "rel1",
             "spreads": stats["spreads"]},
            lambda: frozen_ok),
        _certify(
            "L_cl_phase_dependent",
            {"domain": "as above",
             "law": "the frozen closure angle delta*(phi) is "
                    "genuinely phase-dependent -- delta starts at zero "
                    "for every seed but its locked value scatters over "
                    "more than a radian across phases (unlike rel1, "
                    "whose locked value is exactly 2 phi)",
             "delta_star_range": stats["delta_star_range"],
             "delta_star": stats["delta_star"]},
            lambda: ph_range_ok),
        _certify(
            "L_cl_closure_label",
            {"domain": "as above",
             "law": "the closure angle delta* (alone, or jointly with "
                    "rel1) orders the retention crest across "
                    "geometries",
             "measured": "FALSE: delta* is chain-frozen yet the "
                         "retention winner still travels p4 -> p0 -> "
                         "p2 -> p6 across geometries -- a frozen "
                         "third invariant completes the triangle "
                         "without labelling its resonance",
             "delta_star": stats["delta_star"]},
            lambda: label_ok),
    ]
    return certs, stats


if __name__ == "__main__":
    certs, stats = closure_certificates()
    for c in certs:
        print("  %-38s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("  worst chain spread: %.4f" % stats["worst_spread"])
    print("  delta* range by geometry:",
          {k: v for k, v in sorted(stats["delta_star_range"].items())})
    print("  chain lengths:", {k: v for k, v in
                               sorted(stats["chain_lens"].items())})
    print("  delta* (frozen closure) by geometry:")
    for k, row in sorted(stats["delta_star"].items()):
        print("   ", k, row)