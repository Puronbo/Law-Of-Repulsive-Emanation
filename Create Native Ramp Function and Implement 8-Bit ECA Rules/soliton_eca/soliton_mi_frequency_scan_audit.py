"""soliton_mi_frequency_scan_audit: where the Peregrine crest cap holds.

Round-11's recurrence audit found the MI crest stays below the
algebraic Peregrine bound 3.0000 -- at the MAX-GAIN frequency
Omega = sqrt(2P).  This audit scans the seed frequency and maps the
cap's domain: it holds at and above Omega = 1.0 for P = 1 (crest 2.837,
2.476), but a LOW-frequency seed crests ABOVE the cap:
Omega = 0.5 gives crest 3.656 (epsilon = 0.2).  The Peregrine bound is
the ceiling of the nonlinear stage only near the max-gain frequency;
it is not a global cap on MI crests.

Certificates:

    L_freq_crest_overtakes   HONEST_NEGATIVE  "the Peregrine cap 3.0000
                             bounds every MI crest for every frequency"
                             is FALSE: Omega = 0.5 crests at 3.656.
    L_freq_cap_near_max      PASS/FAIL  for Omega in {1.0, sqrt(2)}
                             the crest stays below 3.0000.
    L_freq_crest_grows_low   PASS/FAIL  the crest is increasing as the
                             frequency drops (2.476, 2.837, 3.656 for
                             Omega in {sqrt(2), 1.0, 0.5}).
    L_freq_relaxes_back      PASS/FAIL  every profile returns to a
                             trough <= 1.5*(1+eps) after its crest.
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

_P = 1.0
_EPS = 0.2
_OMEGA_SET = (0.5, 1.0, float(np.sqrt(2.0)))
_Z_END = 10.0
_Z_GRID = 0.05
_STEPS_PER_DZ = 20
_CAP = 3.0000
_RELAX_FACTOR = 1.5


def _grid() -> np.ndarray:
    _N, _L = 8192, 64.0
    return np.linspace(-_L / 2, _L / 2, _N, endpoint=False)


def _meas(om: float) -> dict[str, float]:
    t = _grid()
    dt = float(np.diff(t)[0])
    ci = int(np.argmin(np.abs(t)))
    zs = np.arange(0.0, _Z_END + _Z_GRID / 2, _Z_GRID)
    cur = np.sqrt(_P) * (1 + _EPS * np.cos(om * t))
    prev = 0.0
    ratios = [np.abs(cur[ci]) / np.sqrt(_P)]
    for z in zs[1:]:
        cur = propagate(cur, dt, z - prev, fiber=Fiber(),
                        steps=_STEPS_PER_DZ)
        prev = z
        ratios.append(np.abs(cur[ci]) / np.sqrt(_P))
    r = np.asarray(ratios)
    ic = int(np.argmax(r[1:])) + 1
    it = ic + int(np.argmin(r[ic:]))
    return {"crest": float(r[ic]),
            "crest_z": float(zs[ic]),
            "trough_after": float(r[it])}


def freqscan_measurements() -> dict[float, dict[str, float]]:
    return {om: _meas(om) for om in _OMEGA_SET}


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
        "first_failure": None if n_ok else {"datum": "the predicate Failed"},
    }


def freqscan_certificates() -> tuple[list[dict[str, object]],
                                     dict[float, dict[str, float]]]:
    m = freqscan_measurements()
    cre = [m[om]["crest"] for om in (float(np.sqrt(2.0)), 1.0, 0.5)]
    certs = [
        _certify("L_freq_crest_overtakes",
                 {"domain": f"P = {_P}, eps = {_EPS}, Omega in "
                            f"{tuple(round(o, 3) for o in _OMEGA_SET)}, "
                            f"SSFM to z = {_Z_END}",
                  "law": "the Peregrine cap 3.0000 bounds the MI crest "
                         "for EVERY seed frequency",
                  "measured": "Omega = 0.5 crests at "
                              f"{m[0.5]['crest']:.3f} -- above the cap"},
                 lambda: m[0.5]["crest"] < _CAP),
        _certify("L_freq_cap_near_max",
                 {"law": "at and above Omega = 1.0 the crest stays "
                         f"below the cap {_CAP} (a gently-located "
                         "nonlinear stage)",
                  "measured": {str(round(o, 3)): round(m[o]["crest"], 3)
                               for o in (1.0, float(np.sqrt(2.0)))}},
                 lambda: all(m[o]["crest"] < _CAP
                             for o in (1.0, float(np.sqrt(2.0))))),
        _certify("L_freq_crest_grows_low",
                 {"law": "the crest amplitude INCREASES as the seed "
                         "frequency drops below the max-gain point: "
                         "2.476 (sqrt 2) -> 2.837 (1.0) -> 3.656 (0.5)",
                  "measured": cre},
                 lambda: cre[0] < cre[1] < cre[2]),
        _certify("L_freq_relaxes_back",
                 {"law": f"every profile returns to a trough <= "
                         f"{_RELAX_FACTOR}*(1+eps) after its crest (the "
                         "recurrence holds at every frequency)",
                  "measured": {str(round(o, 3)):
                               round(m[o]["trough_after"], 3)
                               for o in _OMEGA_SET}},
                 lambda: all(m[o]["trough_after"]
                             <= _RELAX_FACTOR * (1 + _EPS)
                             for o in _OMEGA_SET)),
    ]
    return certs, m


if __name__ == "__main__":
    certs, m = freqscan_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("  Omega   crest    z_crest  trough_after")
    for o in _OMEGA_SET:
        d = m[o]
        print("  %.3f   %.3f    %.2f      %.3f" % (
            o, d["crest"], d["crest_z"], d["trough_after"]))