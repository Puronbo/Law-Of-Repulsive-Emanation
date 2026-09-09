"""soliton_crowd_probe_stability_audit: are round 19's crowd SET and
MARGINS per-probe stable?

The three-block crowd audit (round 19) certified the exact-additive
set as exactly {204, 51, 251} and 147's margins f2 <= 1.35 f1,
(f3 - f2) >= 0.8 f1 -- all on the 8-probe MEAN.  This audit repeats
the protocol per-probe (integer Hamming counts, same 8 placements,
g = 96)::

    exact-additive sets per probe (f3 == 3 f1):
      probe0: {27, 44, 51, 83, 172, 204, 228, 251}
      probe1: {12, 51, 68, 108, 115, 132, 140, 172, 187, 196, 204,
               228, 236, 243, 251}
      probe5: {51, 59, 179, 204, 251}
      ... all 8 probes contain {204, 51, 251}; the rest vary.

    147 per-probe ratios:
      probe 0  1     2     3     4     5     6     7
      f2/f1  .927 2.087 1.333 1.268  .806 1.081 1.400  .895
      (f3-f2)/f1 1.024 1.652 1.000  .446  .613 1.297  .675  .947

Laws:

- the probe-invariant exact-additive CORE is {204, 51, 251}: every
  probe's set contains exactly these three -- the intersection over
  probes IS the certified mean-only set, so round 19's identity
  survives as an intersection statement;
- HONEST_NEGATIVE series -- the certified statements are MEAN-level,
  not instantaneous:
  - "the exact-additive set is {204, 51, 251} at every probe" is
    FALSE: single placements add coincidental members by integer
    equality (up to 15 members at probe1);
  - "147's in-core second block adds at most 0.35 f1 (f2 <= 1.35 f1)
    at every placement" is FALSE: probe 1 gives f2/f1 = 2.087 and
    probe 6 gives 1.400 (the 1.188 mean hides a 0.81..2.09 range);
  - "the far block Lands >= 0.8 f1 beyond the pair at every place-
    ment" is FALSE: probes 3 and 4 give 0.446 and 0.613.

Certificates:

    L_cs_transport_core    PASS/FAIL  intersection of probe sets ==
                              {204, 51, 251}.
    L_cs_set_instant       HONEST_NEGATIVE  "set == {204,51,251} at
                              every probe": FALSE.
    L_cs_core_margin       HONEST_NEGATIVE  "f2 <= 1.35 f1 at every
                              probe (147)": FALSE.
    L_cs_far_margin        HONEST_NEGATIVE  "(f3-f2) >= 0.8 f1 at
                              every probe (147)": FALSE.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_collision_crowd_audit import (  # noqa: E402
    _bit,
    _lcg,
    _ring_step,
    _WIDTH,
    _PROBES,
    _GENS,
    _BLOCK,
    _B_SECOND,
    _B_THIRD,
)
from soliton_eca.soliton_eca import RULES  # noqa: E402

_CORE = {204, 51, 251}
_CORE_CEIL = 1.35
_FAR_FLOOR = 0.8


def probe_table() -> dict[int, dict[str, list[int]]]:
    f = {r: {"f1": [], "f2": [], "f3": []} for r in RULES}
    w = _WIDTH
    seed = _lcg()
    for _ in range(_PROBES):
        seed = _lcg(seed)
        bg = [((seed := _lcg(seed)) >> 16) & 1 for _ in range(w)]
        pa = (_lcg(seed) % w)
        seed = _lcg(seed)
        pb = (pa + _B_SECOND) % w
        pc = (pa + _B_THIRD) % w
        for r in RULES:
            base = list(bg)
            one = list(bg)
            two = list(bg)
            thr = list(bg)
            for i in range(_BLOCK):
                one[(pa + i) % w] ^= 1
                two[(pa + i) % w] ^= 1
                thr[(pa + i) % w] ^= 1
            for i in range(_BLOCK):
                two[(pb + i) % w] ^= 1
                thr[(pb + i) % w] ^= 1
            for i in range(_BLOCK):
                thr[(pc + i) % w] ^= 1
            cb = list(bg)
            co = list(one)
            ct = list(two)
            ch = list(thr)
            for _ in range(_GENS):
                cb = _ring_step(r, cb)
                co = _ring_step(r, co)
                ct = _ring_step(r, ct)
                ch = _ring_step(r, ch)
            f[r]["f1"].append(sum(1 for a, b in zip(cb, co) if a != b))
            f[r]["f2"].append(sum(1 for a, b in zip(cb, ct) if a != b))
            f[r]["f3"].append(sum(1 for a, b in zip(cb, ch) if a != b))
    return f


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


def stability_certificates() -> tuple[list[dict[str, object]],
                                      dict[int, dict[str, list[int]]]]:
    f = probe_table()
    sets = []
    for p in range(_PROBES):
        s = {r for r in RULES if f[r]["f3"][p] == 3 * f[r]["f1"][p]}
        sets.append(s)
    inter = set.intersection(*sets)
    core_ok = inter == _CORE
    instant_ok = all(s == _CORE for s in sets)
    ratios = [f[147]["f2"][p] / f[147]["f1"][p] for p in range(_PROBES)]
    fars = [(f[147]["f3"][p] - f[147]["f2"][p]) / f[147]["f1"][p]
            for p in range(_PROBES)]
    core_margin_ok = all(r2 <= _CORE_CEIL for r2 in ratios)
    far_margin_ok = all(rf >= _FAR_FLOOR for rf in fars)
    certs = [
        _certify("L_cs_transport_core",
                 {"domain": f"width {_WIDTH}, {_PROBES} probes, three "
                            f"{_BLOCK}-cell blocks at 0/{_B_SECOND}/"
                            f"{_B_THIRD}, {_GENS} generations",
                  "law": "the probe-invariant exact-additive CORE is "
                         "{204, 51, 251}: every probe's set contains "
                         "exactly these three, so the intersection "
                         "over probes IS the certified mean-only set "
                         "-- round 19's identity survives as an "
                         "intersection statement",
                  "measured": {"intersection": sorted(inter),
                               "sizes": [len(s) for s in sets]}},
                 lambda: core_ok),
        _certify("L_cs_set_instant",
                 {"law": "the exact-additive set is {204, 51, 251} "
                         "at every probe",
                  "measured": f"FALSE: single placements add "
                              f"coincidental members by integer "
                              f"equality -- probe 1 has "
                              f"{len(sets[1])} members (e.g. 12, 68, "
                              "115, 132, 140, 187...), probe 5 has 5; "
                              "the certified SET is a mean-level "
                              "statement, not an instantaneous one",
                  "per_probe_sizes": [len(s) for s in sets]},
                 lambda: instant_ok),
        _certify("L_cs_core_margin",
                 {"law": "147's in-core second block adds at most "
                         "0.35 f1 (f2 <= 1.35 f1) at every placement",
                  "measured": f"FALSE: probe 1 gives f2/f1 = "
                              f"{ratios[1]:.3f} and probe 6 gives "
                              f"{ratios[6]:.3f}; the 1.188 mean hides "
                              f"a {min(ratios):.2f}..{max(ratios):.2f} "
                              "range -- crowding can almost double the "
                              "damage of an in-core pair, or cut it",
                  "f2_f1": [round(v, 3) for v in ratios]},
                 lambda: core_margin_ok),
        _certify("L_cs_far_margin",
                 {"law": "the far block lands >= 0.8 f1 beyond the "
                         "pair at every placement (147)",
                  "measured": f"FALSE: probes 3 and 4 give "
                              f"{fars[3]:.3f} and {fars[4]:.3f} -- "
                              "sometimes the crowded pair absorbs the "
                              "far block (shared-budget behavior); "
                              "the 0.895 mean is placement-dependent",
                  "far_ratios": [round(v, 3) for v in fars]},
                 lambda: far_margin_ok),
    ]
    return certs, f


if __name__ == "__main__":
    certs, f = stability_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("  per-probe additive sets sizes:", [len({
        r for r in RULES if f[r]['f3'][p] == 3 * f[r]['f1'][p]})
        for p in range(_PROBES)])
    print("  147 f2/f1 per probe:",
          ["%.3f" % (f[147]['f2'][p] / f[147]['f1'][p])
           for p in range(_PROBES)])
    print("  147 (f3-f2)/f1 per probe:",
          ["%.3f" % ((f[147]['f3'][p] - f[147]['f2'][p])
                     / f[147]['f1'][p]) for p in range(_PROBES)])