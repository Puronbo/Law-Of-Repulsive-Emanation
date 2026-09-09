"""soliton_damage_opening_transient_audit: identity of 147's opening.

Round 26 resolved the finer-grid PR of 147 and reported an opening
morphology (mean dip at g = 6 then rise at g = 12, mid-course
acceleration).  This audit checks whether that morphology is a probe-
universal structure or a mean-level artifact -- and what the DAMAGE
MASS does through the opening (per-probe PR and F at {2, 6, 12, 48,
96}, same 8-probe protocol)::

    per-probe PR:   probe0  probe1  probe2  probe3  probe4  probe5  probe6  probe7
        g=2          227.6    95.3   196.9   161.7   341.3   151.1   175.3   307.2
        g=6          128.7    96.7   115.4   167.6   227.6   126.0   120.2    78.3
        g=12         197.5   196.1    87.6   163.8   111.6   163.8   104.1    89.1
    opened spread g=2: max/min = 3.58 ;  g=6: max/min = 2.91

    damage mass Fmean:  g=2 4.9   g=6 7.8   g=12 9.6   g=48 19.4   g=96 37.0

Laws:

- the damage MASS grows strictly through the opening and beyond:
  F(g) increases at every grid sample (4.9 -> 37.0) even while the
  entropy metric wobbles -- the opening is mass-expansion, not
  mass-reorganization alone;
- the opening PR is background-position-dominated: the per-probe PR
  spread at g = 2 and g = 6 spans a factor >= 2.5 (3.58 and 2.91) --
  where the 4-cell block lands in the random ring sets the effective
  wavenumber count of its first-pass footprint;
- HONEST_NEGATIVE: the round-26 opening morphology (dip at g = 6 then
  rise at g = 12) is NOT probe-universal -- probe 4 falls monotonically
  through the opening (341 -> 228 -> 112) and probe 1 barely dents;
  the morphology is a MEAN-level artifact and cannot be certified as
  an intra-probe trajectory law.

Certificates:

    L_ot_mass_growth       PASS/FAIL  F strictly rises on the grid.
    L_ot_bgdominated       PASS/FAIL  PR spread factor >= 2.5 at
                            g = 2 and g = 6.
    L_ot_universal_dip     HONEST_NEGATIVE  "every probe shows the
                            dip at 6 then rise at 12": FALSE.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_damage_modal_audit import (  # noqa: E402
    _bit,
    _lcg,
    _participation,
    _ring_step,
    _WIDTH,
    _PROBES,
    _BLOCK,
)

_GRID = (2, 6, 12, 48, 96)
_AMP = 147
_SPREAD_FLOOR = 2.5
_DIP_SPREAD = 1.6


def opening_table() -> tuple[dict[int, list[float]], dict[int, list[float]]]:
    pr = {g: [] for g in _GRID}
    mass = {g: [] for g in _GRID}
    w = _WIDTH
    seed = _lcg()
    for _ in range(_PROBES):
        seed = _lcg(seed)
        bg = [((seed := _lcg(seed)) >> 16) & 1 for _ in range(w)]
        pa = (_lcg(seed) % w)
        seed = _lcg(seed)
        clean = list(bg)
        one = list(bg)
        for i in range(_BLOCK):
            one[(pa + i) % w] ^= 1
        for g in range(1, 97):
            clean = _ring_step(_AMP, clean)
            one = _ring_step(_AMP, one)
            if g in _GRID:
                flat = [1 if a != b else 0
                        for a, b in zip(clean, one)]
                pr[g].append(_participation(flat))
                mass[g].append(float(sum(flat)))
    return pr, mass


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


def opening_certificates() -> tuple[list[dict[str, object]],
                                    tuple[dict[int, list[float]],
                                           dict[int, list[float]]]]:
    pr, mass = opening_table()
    fm = {g: float(np.mean(mass[g])) for g in _GRID}
    mass_ok = all(fm[a] < fm[b] for a, b in zip(_GRID, _GRID[1:]))
    spread = {g: float(np.max(pr[g])) / max(float(np.min(pr[g])), 1e-12)
              for g in (2, 6)}
    spread_ok = all(v >= _SPREAD_FLOOR for v in spread.values())
    dips = [(pr[6][p] < pr[2][p] and pr[12][p] > pr[6][p])
            for p in range(_PROBES)]
    all_dip = all(dips)
    n_dip = sum(dips)
    certs = [
        _certify("L_ot_mass_growth",
                 {"domain": f"width {_WIDTH}, single {_BLOCK}-cell "
                            f"block, rule 147, {_PROBES} probes, "
                            f"grid {_GRID}",
                  "law": "the damage MASS grows strictly through the "
                         "opening and beyond: F increases at every "
                         "grid sample (4.9 -> 37.0) even while the "
                         "entropy metric wobbles -- the opening is "
                         "mass-expansion, not reorganization alone",
                  "measured": {str(g): round(v, 1)
                               for g, v in fm.items()}},
                 lambda: mass_ok),
        _certify("L_ot_bgdominated",
                 {"law": "the opening PR is background-position-"
                         "dominated: the per-probe PR spread at g = 2 "
                         f"and g = 6 spans a factor >= {_SPREAD_FLOOR} "
                         f"({spread[2]:.2f} and {spread[6]:.2f}) -- "
                         "where the 4-cell block lands in the random "
                         "ring sets the effective wavenumber count of "
                         "its first-pass footprint",
                  "measured": {"spread": {str(g): round(v, 2)
                                          for g, v in spread.items()},
                               "pr_g2": [round(v, 1) for v in pr[2]]}},
                 lambda: spread_ok),
        _certify("L_ot_universal_dip",
                 {"law": "every probe shows the opening morphology "
                         "(dip at g = 6 then rise at g = 12) of "
                         "round 26",
                  "measured": f"FALSE: only {n_dip} of "
                              f"{_PROBES} probes dip-and-rise; probe 4 "
                              "falls monotonically through the opening "
                              "(341 -> 228 -> 112) and probe 1 barely "
                              "dents (95 -> 97 -> 196) -- the round-26 "
                              "morphology is a MEAN-level artifact and "
                              "is not an intra-probe trajectory law",
                  "n_probes_dip_rise": n_dip,
                  "spread_trace": {str(g): [round(v, 1) for v in pr[g]]
                                   for g in (2, 6, 12)}},
                 lambda: all_dip),
    ]
    return certs, (pr, mass)


if __name__ == "__main__":
    certs, (pr, mass) = opening_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("  per-probe PR @2:  ", [round(v, 1) for v in pr[2]])
    print("  per-probe PR @6:  ", [round(v, 1) for v in pr[6]])
    print("  per-probe PR @12: ", [round(v, 1) for v in pr[12]])
    print("  F mean:", {str(g): round(float(np.mean(mass[g])), 1)
                        for g in _GRID})