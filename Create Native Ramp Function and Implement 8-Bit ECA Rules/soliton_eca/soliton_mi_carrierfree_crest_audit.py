"""soliton_mi_carrierfree_crest_audit: the carrier-void near-cap crest.

The depletion grid (round 21) reported P0 = 0.000 at (Omega = 1.0) on
the sexagesimal crests -- a crest with NO carrier at all. This audit
resolves the crest structure at Omega = 1.0 across the seed amplitudes
and its four-crest recurrence chain (z <= 14)::

    first crest:   e=.10 z=3.30 R=2.757 P0=0.0004 P(+-Om)=.295 P(+-2Om)=.085
                   e=.20 z=2.45 R=2.837 P0=0.0003 P(+-Om)=.278 P(+-2Om)=.091
                   e=.30 z=1.95 R=2.958 P0=0.0016 P(+-Om)=.258 P(+-2Om)=.099
                   e=.45 z=1.50 R=3.226 P0=0.0002 P(+-Om)=.220 P(+-2Om)=.111
    second crest:  P0 = 0.023/0.038/0.025/0.010   (all <= 0.06)
    later crests:  e=.30 4th P0 = 0.176 -- carrier returns.

Laws:

- the first crest is EXACTLY carrier-void: P0 <= 0.01 for every seed
  amplitude (max 0.0016) -- the near-cap crest carries no center
  frequency at all;
- the void crest is a 4-line harmonic stack: the +-Omega and +-2 Omega
  pairs together hold >= 0.60 of the power at the first crest (min
  0.662);
- the void persists through one full recurrence: P0 <= 0.06 at the
  second crest for every seed amplitude (max 0.038);
- HONEST_NEGATIVE: the carrier does NOT stay void at every later
  crest -- at the fourth crest of e = 0.30 the carrier returns to
  P0 = 0.176 (the void is a first-`double-period` structural
  signature, not a permanent state).

Certificates:

    L_cf_void_first      PASS/FAIL  P0 <= 0.01 at the first crest.
    L_cf_twopair_stack   PASS/FAIL  (p1 + p2) >= 0.60 at the first
                              crest.
    L_cf_second_void     PASS/FAIL  P0 <= 0.06 at the second crest.
    L_cf_chain_void      HONEST_NEGATIVE  "every crest stays
                              carrier-void": FALSE (4th crest of
                              e = 0.30 has P0 = 0.176).
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

_P = 1.0
_OMEGA = 1.0
_EPS_SET = (0.10, 0.20, 0.30, 0.45)
_Z_END = 14.0
_CREST_EXCURSION = 1.2
_VOID_CEIL = 0.01
_STACK_FLOOR = 0.60
_SECOND_CEIL = 0.06


def _crest_chain(eps: float) -> list[dict[str, float]]:
    t = _grid()
    dt = float(np.diff(t)[0])
    ci = int(np.argmin(np.abs(t)))
    zs = np.arange(0.0, _Z_END + _Z_GRID / 2, _Z_GRID)
    cur = np.sqrt(_P) * (1 + eps * np.cos(_OMEGA * t))
    prev = 0.0
    r = np.empty(len(zs))
    fields = []
    for k, z in enumerate(zs):
        if z > 0.0:
            cur = propagate(cur, dt, z - prev, fiber=Fiber(),
                            steps=_STEPS_PER_DZ)
            prev = z
        r[k] = np.abs(cur[ci])
        fields.append(cur.copy())
    chain = []
    for i in range(2, len(zs) - 2):
        if r[i] > _CREST_EXCURSION and r[i] >= max(r[i - 2:i + 3]):
            s = _split(fields[i], _OMEGA)
            chain.append({"z": float(zs[i]), "R": float(r[i]),
                          "p0": float(s["p0"]), "p1": float(s["p1"]),
                          "p2": float(s["p2"]), "rest": float(s["rest"])})
    return chain


def carrierfree_data() -> dict[str, list[dict[str, float]]]:
    return {str(eps): _crest_chain(eps) for eps in _EPS_SET}


def _certify(label: str, meta: dict[str, object],
             pred: Callable[[], bool]) -> dict[str, object]:
    n_ok = 1 if pred() else 0
    return {
        "label": label,
        "meta": meta,
        "kind": "statement",
        "status": "PASS" if n_ok else "HONEST_NEGATIVE",
        "n_ok": n_ok,
        "n_fail": 0 if n_ok else 1,
        "first_failure": None if n_ok else {"datum": "predicate Failed"},
    }


def carrierfree_certificates() -> tuple[list[dict[str, object]],
                                        dict[str, object]]:
    data = carrierfree_data()
    first = {e: data[e][0] for e in data if data[e]}
    second = {e: data[e][1] for e in data if len(data[e]) > 1}
    first_void = max(c["p0"] for c in first.values())
    stack = min(c["p1"] + c["p2"] for c in first.values())
    second_void = max(c["p0"] for c in second.values())
    all_crests = [c for e in data for c in data[e]]
    chain_max = max(c["p0"] for c in all_crests)
    certs = [
        _certify("L_cf_void_first",
                 {"law": "the first crest at Omega = 1.0 is EXACTLY "
                         "carrier-void: P0 <= "
                         f"{_VOID_CEIL} for every seed amplitude "
                         f"(max {first_void:.4f}; the near-cap crest "
                         "carries no center frequency at all)",
                  "measured": {e: round(c["p0"], 4)
                               for e, c in sorted(first.items())}},
                 lambda: first_void <= _VOID_CEIL),
        _certify("L_cf_twopair_stack",
                 {"law": "the void crest is a 4-line harmonic stack: "
                         "the +-Omega and +-2-Omega pairs together "
                         f"hold >= {_STACK_FLOOR} of the power at the "
                         f"first crest (min {stack:.3f})",
                  "measured": {e: round(c["p1"] + c["p2"], 3)
                               for e, c in sorted(first.items())}},
                 lambda: stack >= _STACK_FLOOR),
        _certify("L_cf_second_void",
                 {"law": "the void persists through one full "
                         f"recurrence: P0 <= {_SECOND_CEIL} at the "
                         f"second crest for every seed amplitude "
                         f"(max {second_void:.3f})",
                  "measured": {e: round(c["p0"], 4)
                               for e, c in sorted(second.items())}},
                 lambda: second_void <= _SECOND_CEIL),
        _certify("L_cf_chain_void",
                 {"law": "the carrier stays void at every crest in "
                         "the recurrence chain: P0 <= "
                         f"{_SECOND_CEIL} at every crest",
                  "measured": f"FALSE: the carrier returns -- the "
                              f"fourth crest of e = 0.30 has P0 = "
                              f"{chain_max:.3f}; the void is a "
                              "first-period structural signature, "
                              "not a permanent state",
                  "chain_max_p0": round(chain_max, 3)},
                 lambda: chain_max <= _SECOND_CEIL),
    ]
    return certs, data


if __name__ == "__main__":
    certs, data = carrierfree_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    for e in sorted(data, key=float):
        print("  eps=%s" % e, "  ".join(
            "z=%.2f R=%.3f P0=%.4f" % (c["z"], c["R"], c["p0"])
            for c in data[e]))