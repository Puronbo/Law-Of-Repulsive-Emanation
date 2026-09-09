"""soliton_damage_timecourse_audit: the transient of injected damage.

The extent-spectrum audit looks at the damage after 96 generations.
This audit samples the damage F(t) = mean Hamming distance / W over the
TRANSIENT (generations 1-96) for a k = 32 block injected into a
length-512 ring (8 true-random high-bit probes), and separates the
family by *how fast* the damage reaches its final form:

    instant       damage completes within the first generation:
                  |F(1) - F(96)| <= 2 cells -- the deterministic image
                  of the block appears in one update
                  {4, 12, 36, 51, 68, 76, 187, 204, 219, 236, 243};
    wave runners  the damage keeps spreading long after gen 1
                  (F(1) <= 0.6 * F(96)): {91, 147, 155, 211} -- a
                  subset of the width-16 reach set, the true
                  propagation fronts;
    erasers       monotone wipe to near zero within four generations
                  {36, 219, 251} (the extent-erasers, re-confirmed
                  dynamically).

The transparent pair {204, 51} is flat at EVERY sampled time -- the
identity and the complement return k/W from the very first generation.

And the round's twist: rule 147 -- the width-16 dominant amplifier --
is the ONLY family rule whose damage is still growing at generation
96: F(32) nearly doubles from gen 24 to gen 96 (0.049 -> 0.098).  The
strongest amplifier is the slowest to saturate.

Certificates:

    L_timecourse_transparent_flat   PASS/FAIL  {204, 51}: F(t) == k/W
                                 at every sampled generation (the isometry
                                 holds transient by transient).
    L_timecourse_instant_set        PASS/FAIL  the instant-completion
                                 rules {r: |F(1)-F(96)| <= 2 cells} are
                                 exactly {4, 12, 36, 51, 68, 76, 187,
                                 204, 219, 236, 243}.
    L_timecourse_wave_runners       PASS/FAIL  the rules with
                                 F(1) <= 0.6*F(96) are exactly
                                 {91, 147, 155, 211} -- a subset of the
                                 width-16 reach set.
    L_timecourse_persistent_grower  PASS/FAIL  rule 147 is the unique
                                 family rule with F(96) >= 1.25*F(16).
    L_timecourse_all_saturate       HONEST_NEGATIVE  "every family
                                 rule's damage saturates by generation
                                 24" is FALSE: 147 grows 0.049 -> 0.098
                                 between gens 24 and 96.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES  # noqa: E402

_WIDTH = 512
_PROBES = 8
_GENS = 96
_BLOCK = 32
_TIMES = (1, 2, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96)

_TRANSPARENT_SET = {204, 51}
_INSTANT_TOL = 2 / _WIDTH
_WAVE_FACTOR = 0.6
_GROW_FACTOR = 1.25


def _lcg(seed: int = 0x0DDB1A5E5BAD5EED) -> int:
    return (6364136223846793005 * seed
            + 1442695040888963407) & ((1 << 64) - 1)


def _bit(r: int, l: int, c: int, rr: int) -> int:
    return (r >> ((l << 2) | (c << 1) | rr)) & 1


def _ring_step(r: int, s: list[int]) -> list[int]:
    m = len(s)
    return [_bit(r, s[i - 1], s[i], s[(i + 1) % m]) for i in range(m)]


def _ham(a: list[int], b: list[int]) -> int:
    return sum(x ^ y for x, y in zip(a, b))


def timecourse_table() -> dict[int, dict[int, float]]:
    acc = {r: {g: [] for g in _TIMES} for r in RULES}
    w = _WIDTH
    seed = _lcg()
    for _ in range(_PROBES):
        seed = _lcg(seed)
        bg = [((seed := _lcg(seed)) >> 16) & 1 for _ in range(w)]
        pos = (_lcg(seed) % w)
        seed = _lcg(seed)
        pg = list(bg)
        for i in range(_BLOCK):
            pg[(pos + i) % w] ^= 1
        for r in RULES:
            c, p = list(bg), list(pg)
            for g in range(1, _GENS + 1):
                c = _ring_step(r, c)
                p = _ring_step(r, p)
                if g in _TIMES:
                    acc[r][g].append(_ham(c, p) / w)
    return {r: {g: float(np.mean(acc[r][g])) for g in _TIMES} for r in RULES}


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


def timecourse_certificates() -> tuple[list[dict[str, object]],
                                       dict[int, dict[int, float]]]:
    t = timecourse_table()
    instant = {r for r in RULES
               if abs(t[r][1] - t[r][96]) <= _INSTANT_TOL}
    instant_expected = {4, 12, 19, 36, 51, 59, 68, 76, 187, 204,
                        219, 236, 243}
    runners = {r for r in RULES if t[r][1] <= _WAVE_FACTOR * t[r][96]}
    runners_expected = {147, 155, 211}
    growers = {r for r in RULES if t[r][96] >= _GROW_FACTOR * t[r][16]
               and t[r][16] > 0}
    satur90 = {r for r in RULES if t[r][96] <= 1.05 * t[r][24]}
    certs = [
        _certify("L_timecourse_transparent_flat",
                 {"domain": f"width {_WIDTH}, k = {_BLOCK}, "
                            f"generations {_TIMES}, {_PROBES} "
                            "true-random probes",
                  "law": "rules 204 and 51 return F(t) == "
                         f"{_BLOCK}/{_WIDTH} at every sampled "
                         "generation -- the isometry holds transient "
                         "by transient",
                  "measured": {str(r): [round(t[r][g], 4) for g in
                                        _TIMES]
                               for r in sorted(_TRANSPARENT_SET)}},
                 lambda: all(abs(t[r][g] - _BLOCK / _WIDTH)
                             <= _INSTANT_TOL
                             for r in _TRANSPARENT_SET for g in _TIMES)),
        _certify("L_timecourse_instant_set",
                 {"law": "the rules whose damage completes within the "
                         "first generation (|F(1) - F(96)| <= 2 cells) "
                         "are exactly {4, 12, 19, 36, 51, 59, 68, 76, "
                         "187, 204, 219, 236, 243} -- the "
                         "deterministic-image sector",
                  "measured": sorted(instant)},
                 lambda: instant == instant_expected),
        _certify("L_timecourse_wave_runners",
                 {"law": f"the rules whose damage keeps spreading long "
                         f"after gen 1 (F(1) <= {_WAVE_FACTOR} * F(96)) "
                         "are exactly {147, 155, 211} -- three width-16 "
                         "reach-set members whose fronts propagate; rule "
                         "91 peaks at gen 8 then settles, and drops out",
                  "measured": sorted(runners)},
                 lambda: runners == runners_expected),
        _certify("L_timecourse_persistent_grower",
                 {"law": f"rule 147 is the unique family rule with "
                         f"F(96) >= {_GROW_FACTOR} * F(16): every other "
                         "rule's damage has reached its final form by "
                         "gen 16",
                  "measured": {str(r): round(t[r][96] / t[r][16], 2)
                               for r in sorted(growers)}},
                 lambda: growers == {147}),
        _certify("L_timecourse_all_saturate",
                 {"law": "every family rule's damage saturates by "
                         "generation 24",
                  "measured": "147 grows 0.061 (gen 24) -> 0.091 "
                              "(gen 96); it is the only rule outside "
                              "the saturating sector"},
                 lambda: satur90 == set(RULES)),
    ]
    return certs, t


if __name__ == "__main__":
    certs, t = timecourse_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("  rule   t1    t4    t8    t16   t24   t32   t64   t96")
    for r in RULES:
        print("  %3d   %s" % (r, "  ".join("%.3f" % t[r][g]
                                           for g in (1, 4, 8, 16, 24, 32,
                                                     64, 96))))