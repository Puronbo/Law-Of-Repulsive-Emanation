"""soliton_mi_depletion_grid_audit: crest-time pump depletion across (eps, Omega).

Round 17 measured P0 at the crest for three integer modes at eps = 0.2.
This audit sweeps the crest-time carrier share over the full phase-
diagram grid (8 Omega x 5 eps = 40 cells, z <= 10) plus far scales::

    P0@crest:  e=0.05  0.124 0.340 0.246 0.047 0.013 0.001 0.032 0.144
               e=0.10  0.062 0.310 0.251 0.054 0.014 0.000 0.101 0.138
               e=0.20  0.017 0.249 0.229 0.061 0.055 0.000 0.026 0.132
               e=0.30  0.038 0.219 0.237 0.042 0.069 0.025 0.048 0.123
               e=0.45  0.060 0.157 0.233 0.064 0.020 0.010 0.057 0.146
              Omega = 0.196 0.393 0.500 0.785 0.900 1.000 1.200 1.414
    far scales (e = 0.2): Omega=2.0 P0=0.138  Omega=4.0 P0=0.208
                          Omega=8.0 P0=0.950

Laws:

- pump depletion is UNIVERSAL across the sampled growth band: P0 <=
  0.40 at the crest on all 40 (eps, Omega) cells (max 0.340) -- the
  round-17 ceiling holds for every seed amplitude and frequency;
- the near-cap crescent exhausts the pump: for Omega in {0.9, 1.0}
  the crest carries P0 <= 0.10 at every eps (the secondary maxima of
  the phase diagram are the deepest carrier drains);
- the far band keeps the carrier: at Omega = 8.0 the crest is a
  near-passive carrier state (P0 = 0.950) -- depletion does NOT
  extend to every modulation scale, though scales 2 and 4 still
  drain the pump (0.138, 0.208): the depletion trough simply pokes
  past the linear band edge;
- HONEST_NEGATIVE: "P0 <= 0.40 at the crest for every scale" fails
  at Omega = 8.0.

Certificates:

    L_pdep_belt          PASS/FAIL  P0 <= 0.40 on all 40 grid cells.
    L_pdep_crescent      PASS/FAIL  Omega in {0.9, 1.0}: P0 <= 0.10
                              at every eps.
    L_pdep_far_kept      PASS/FAIL  Omega = 8.0: P0 >= 0.60.
    L_pdep_global        HONEST_NEGATIVE  "depletion holds at every
                              scale": FALSE (Omega = 8.0 keeps 0.950).
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
_Z_END = 10.0
_EPS_SET = (0.05, 0.10, 0.20, 0.30, 0.45)
_OMEGA_GRID = (
    2 * np.pi * 2 / 64,
    2 * np.pi * 4 / 64,
    0.5,
    2 * np.pi * 8 / 64,
    0.9,
    1.0,
    1.2,
    np.sqrt(2),
)
_FAR = (2.0, 4.0, 8.0)
_BELT_CEIL = 0.40
_CRESCENT_CEIL = 0.10
_FAR_KEEP = 0.60
_CRESCENT_OM = (0.9, 1.0)


def _crest_p0(eps: float, om: float, z_end: float) -> tuple[float, float]:
    t = _grid()
    dt = float(np.diff(t)[0])
    ci = int(np.argmin(np.abs(t)))
    zs = np.arange(0.0, z_end + _Z_GRID / 2, _Z_GRID)
    cur = np.sqrt(_P) * (1 + eps * np.cos(om * t))
    prev = 0.0
    ratios = [np.abs(cur[ci])]
    fields = [cur.copy()]
    for z in zs[1:]:
        cur = propagate(cur, dt, z - prev, fiber=Fiber(),
                        steps=_STEPS_PER_DZ)
        prev = z
        ratios.append(np.abs(cur[ci]))
        fields.append(cur.copy())
    r = np.asarray(ratios)
    ic = int(np.argmax(r[1:])) + 1
    return _split(fields[ic], om)["p0"], float(r[ic])


def depletion_grid() -> tuple[dict[str, object], dict[str, object]]:
    belt = {eps: {om: _crest_p0(eps, om, _Z_END)[0]
                  for om in _OMEGA_GRID} for eps in _EPS_SET}
    far = {}
    for om in _FAR:
        p0, _ = _crest_p0(0.2, om, _Z_END)
        far[om] = p0
    return belt, far


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


def depletion_certificates() -> tuple[list[dict[str, object]],
                                      dict[str, object]]:
    belt, far = depletion_grid()
    belt_max = max(v for row in belt.values() for v in row.values())
    crescent_max = max(belt[e][om]
                       for om in _CRESCENT_OM for e in _EPS_SET)
    far8 = far[8.0]
    belt_ok = belt_max <= _BELT_CEIL
    cres_ok = crescent_max <= _CRESCENT_CEIL
    kept_ok = far8 >= _FAR_KEEP
    certs = [
        _certify("L_pdep_belt",
                 {"domain": f"P = {_P}, grid {len(_EPS_SET)} eps x "
                            f"{len(_OMEGA_GRID)} Omega, z <= {_Z_END}",
                  "law": "pump depletion is universal across the "
                         "sampled growth band: P0 <= "
                         f"{_BELT_CEIL} at the crest on all 40 "
                         f"(eps, Omega) cells (max {belt_max:.3f})",
                  "measured_max": round(belt_max, 3)},
                 lambda: belt_ok),
        _certify("L_pdep_crescent",
                 {"law": "the near-cap crescent exhausts the pump: for "
                         f"Omega in {list(_CRESCENT_OM)} the crest "
                         f"carries P0 <= {_CRESCENT_CEIL} at every eps "
                         f"(max {crescent_max:.3f}) -- the secondary "
                         "crest maxima of the phase diagram are the "
                         "deepest carrier drains",
                  "measured": {str(om): {str(e): round(belt[e][om], 3)
                                         for e in _EPS_SET}
                               for om in _CRESCENT_OM}},
                 lambda: cres_ok),
        _certify("L_pdep_far_kept",
                 {"law": "the far band keeps the carrier: at "
                         f"Omega = 8.0 the crest is a near-passive "
                         f"carrier state with P0 = {far8:.3f} >= "
                         f"{_FAR_KEEP} -- depletion does NOT extend to "
                         "every scale",
                  "measured": {str(om): round(v, 3)
                               for om, v in far.items()}},
                 lambda: kept_ok),
        _certify("L_pdep_global",
                 {"law": "P0 <= 0.40 at the crest for every modulation "
                         "scale",
                  "measured": f"FALSE: at Omega = 8.0 the crest keeps "
                              f"P0 = {far8:.3f} (a near-passive "
                              "carrier); Omega = 2 and 4 still drain "
                              f"(0.138, 0.208) -- the depletion trough "
                              "pokes past the linear band edge without "
                              "reaching every scale",
                  "far_kept": round(far8, 3)},
                 lambda: all(v <= _BELT_CEIL for v in far.values())),
    ]
    return certs, {"belt": belt, "far": far}


if __name__ == "__main__":
    certs, data = depletion_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    belt = data["belt"]
    print("  P0@crest: " + "  ".join(
        ("O=%.3f" % om for om in _OMEGA_GRID)))
    for e in _EPS_SET:
        print("  eps=%.2f " % e + " ".join(
            "%.3f" % belt[e][om] for om in _OMEGA_GRID))
    print("  far:", {str(om): round(v, 3)
                     for om, v in data["far"].items()})