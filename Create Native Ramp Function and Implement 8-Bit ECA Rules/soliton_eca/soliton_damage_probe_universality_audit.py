"""soliton_damage_probe_universality_audit: are the certified 147 laws
per-probe universal?

Round 27 showed the OPENING (g <= 12) morphology of rounds 26 is a
mean-level artifact -- not every probe dips at 6 then rises at 12.
This audit asks the complement: which of the certified long-time laws
survive per-probe scrutiny?  Per-probe PR and top-2 for 147 at
{2, 12, 48, 96, 192, 384}, same 8-probe protocol::

    per-probe PR:      probe 0     1     2     3     4     5     6     7
        g=  2           227.6   95.3  196.9  161.7  341.3  151.1  175.3  307.2
        g= 12           197.5  196.1   87.6  163.8  111.6  163.8  104.1   89.1
        g= 96            49.0   87.5   65.3   24.9   58.7   54.4   42.9   42.1
        g=384             7.9   17.0   17.3   10.2    6.1    6.8   13.8   25.3
    per-probe top2:     g=  2  0.016..0.031   g= 96  0.084..0.190
                        g=192  0.143..0.235   g=384  0.020..0.149

Laws:

- the concentration law (rounds 16/24) is PER-PROBE universal: every
  probe satisfies PR(96) < PR(2) and PR(2)/PR(384) >= 5.6 (min 5.60,
  threshold 3.5) -- the caustic's effective-wavenumber contraction is
  not a mean artifact;
- the crystallization-and-turnover laws (rounds 23/24) are PER-PROBE
  universal: every probe has top2(96) > top2(2) AND top2(384) <
  top2(192) -- the dominant pair rises then reverses for every seed;
- HONEST_NEGATIVE: "every certified 147 trajectory law is per-probe
  universal, including the opening" is FALSE -- the opening variable
  PR(2) -> PR(12) is probe-dependent (probes 1, 3, 5 RISE, the rest
  fall): only the long-time laws are locally robust; the first-pass
  footprint is background-position-dominated.

Certificates:

    L_pu_conc_universal   PASS/FAIL  every probe: PR(96) < PR(2) and
                            PR(2)/PR(384) >= 5.0.
    L_pu_cry_universal    PASS/FAIL  every probe: top2(96) > top2(2)
                            and top2(384) < top2(192).
    L_pu_opening_exception HONEST_NEGATIVE  "all trajectory laws are
                            per-probe universal including the
                            opening": FALSE.
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
from soliton_eca.soliton_damage_crystallization_audit import (  # noqa: E402
    _top2_share,
)

_GRID = (2, 12, 48, 96, 192, 384)
_AMP = 147
_CONC_FLOOR = 5.0


def universality_table() -> tuple[dict[int, list[float]],
                                  dict[int, list[float]]]:
    pr = {g: [] for g in _GRID}
    top = {g: [] for g in _GRID}
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
        for g in range(1, 385):
            clean = _ring_step(_AMP, clean)
            one = _ring_step(_AMP, one)
            if g in _GRID:
                flat = [1 if a != b else 0
                        for a, b in zip(clean, one)]
                pr[g].append(_participation(flat))
                top[g].append(_top2_share(flat))
    return pr, top


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


def universality_certificates() -> tuple[list[dict[str, object]],
                                         tuple[dict[int, list[float]],
                                                dict[int, list[float]]]]:
    pr, top = universality_table()
    conc_ok = all(pr[96][p] < pr[2][p] for p in range(_PROBES)) \
        and min(pr[2][p] / pr[384][p] for p in range(_PROBES)) \
        >= _CONC_FLOOR
    cry_ok = all(top[96][p] > top[2][p] for p in range(_PROBES)) \
        and all(top[384][p] < top[192][p] for p in range(_PROBES))
    opening_ok = all(pr[12][p] < pr[2][p] for p in range(_PROBES))
    min_ratio = min(pr[2][p] / pr[384][p] for p in range(_PROBES))
    rises = [p for p in range(_PROBES) if pr[12][p] > pr[2][p]]
    certs = [
        _certify("L_pu_conc_universal",
                 {"domain": f"width {_WIDTH}, single {_BLOCK}-cell "
                            f"block, rule 147, {_PROBES} probes, "
                            f"grid {_GRID}",
                  "law": "the concentration law (rounds 16/24) is "
                         "PER-PROBE universal: every probe has "
                         "PR(96) < PR(2) and PR(2)/PR(384) >= 5.0 "
                         f"(min {min_ratio:.2f}, threshold 3.5) -- "
                         "the effective-wavenumber contraction is not "
                         "a mean artifact",
                  "measured": {"min_ratio": round(min_ratio, 2),
                               "pr_2": [round(v, 1) for v in pr[2]],
                               "pr_96": [round(v, 1) for v in pr[96]],
                               "pr_384": [round(v, 1) for v in pr[384]]}},
                 lambda: conc_ok),
        _certify("L_pu_cry_universal",
                 {"law": "the crystallization-and-turnover laws "
                         "(rounds 23/24) are PER-PROBE universal: "
                         "every probe has top2(96) > top2(2) AND "
                         "top2(384) < top2(192) -- the dominant pair "
                         "rises then reverses for every seed",
                  "measured": {"top2_2": [round(v, 3) for v in top[2]],
                               "top2_96": [round(v, 3) for v in top[96]],
                               "top2_192": [round(v, 3) for v in top[192]],
                               "top2_384": [round(v, 3) for v in top[384]]}},
                 lambda: cry_ok),
        _certify("L_pu_opening_exception",
                 {"law": "all certified 147 trajectory laws are "
                         "per-probe universal, including the opening",
                  "measured": f"FALSE: the opening variable "
                              f"PR(2) -> PR(12) is probe-dependent -- "
                              f"probes {rises} RISE while the rest "
                              "fall (round 27's morphology); only the "
                              "long-time laws (concentration, "
                              "crystallization, turnover) are locally "
                              "robust -- the first-pass footprint is "
                              "background-position-dominated",
                  "n_opening_rises": len(rises),
                  "pr_12": [round(v, 1) for v in pr[12]]},
                 lambda: opening_ok),
    ]
    return certs, (pr, top)


if __name__ == "__main__":
    certs, (pr, top) = universality_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    for g in _GRID:
        print("  g=%3d  PR:%s  top2:%s" % (
            g,
            " ".join("%5.1f" % v for v in pr[g]),
            " ".join("%.3f" % v for v in top[g])))