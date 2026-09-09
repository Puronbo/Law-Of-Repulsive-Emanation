"""soliton_collision_damage_probe_audit: the two-block interaction laws,
re-measured per placement.

The round-14 collision-damage audit certified every two-block law on the
MEAN over its eight true-random probes.  The crowd arc (rounds 29--31)
established the discipline these laws now get: a certified mean can hide
placement-level reversal.  This audit replays the IDENTICAL LCG stream
and protocol (same backgrounds, same per-rule placement draw, same 96
generations, same distances) but retains every probe's per-placement
value, and re-examines each round-14 statement per placement:

    detach          {204, 51}: F2(d) == 2*k/W at every distance AND
                    every placement -- the isometry bus disconnect;
    wipe core       the wiper set (max_d F2 <= 0.006) per placement is
                    placement-dependent; its intersection over all
                    eight probes is {36, 251} (219 joins six of the
                    eight, failing probes 0 and 2);
    saturation      rule 147's short-range squeeze F2(4) - 2*F1 <= -0.03
                    holds as an aggregate at 7/8 placements, but
                    INVERTS once: probe 3 gives +0.039 -- the measured
                    maximum positive short-range interaction in the
                    whole table, at the exact distance the mean law
                    calls "saturated";
    far field       the antipode independence |F2(256) - 2*F1| <= 0.005
                    is a MEAN law only: per placement the worst rule
                    reaches 0.131 (147's wrapped caustic at probe 3);
    synergy         "no rule exceeds 1.01*2*F1 at any measured
                    distance" holds on means but fails at nearly every
                    placement -- coincidence-based interactions cross
                    the tight 1.01 tolerance routinely.

So the round-14 damage laws survive only in their aggregate form; the
per-placement damage field of the colliding-block World is
placement-structured, exactly as the crowd and kscale families were.

Certificates:

    L_cdp_detach_exact          PASS/FAIL  {204, 51}: F2(d) == 2k/W
                                    within one cell at EVERY distance
                                    and EVERY placement (integer-exact).
    L_cdp_wipe_core             PASS/FAIL  the per-placement wiper sets
                                    (max_d F2 <= 0.006) have
                                    intersection exactly {36, 251}, and
                                    both rules wipe at every
                                    placement at every distance (219
                                    joins 6/8 placements).
    L_cdp_wipe_set_exact        PASS/FAIL  FALSE CANDIDATE: the wiper
                                    set equals {36, 219, 251} at every
                                    placement.
    L_cdp_saturation_signature  PASS/FAIL  aggregate: 147 is the unique
                                    rule with mean(F2(4) - 2*F1) <=
                                    -0.03 AND its per-placement
                                    signature holds at >= 7/8
                                    placements.
    L_cdp_saturation_universal  PASS/FAIL  FALSE CANDIDATE: 147's
                                    short-range saturation holds at
                                    EVERY placement (it inverts once,
                                    to +0.039, at probe 3).
    L_cdp_far_antipode          PASS/FAIL  FALSE CANDIDATE: |F2(256) -
                                    2*F1| <= 0.005 at every placement
                                    and every rule (worst 0.131).
    L_cdp_synergy_none          PASS/FAIL  FALSE CANDIDATE: no rule
                                    exceeds 1.01*2*F1 at any distance
                                    at any placement.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES  # noqa: E402

_WIDTH = 512
_PROBES = 8
_GENS = 96
_BLOCK = 4
_DISTANCES = (4, 16, 64, 128, 256)
_WIPE_LEVEL = 0.006
_SAT_LEVEL = -0.03
_SYNERGY_TOL = 0.01
_BASE = 2 * _BLOCK / _WIDTH


def _lcg(seed: int = 0x0DDB1A5E5BAD5EED) -> int:
    return (6364136223846793005 * seed + 1442695040888963407) & 0x7FFFFFFFFFFFFFFF


def _bit(rule: int, l: int, c: int, r: int) -> int:
    return (rule >> ((l << 2) | (c << 1) | r)) & 1


def _ring_step(rule: int, state: list[int]) -> list[int]:
    m = len(state)
    return [_bit(rule, state[i - 1], state[i], state[(i + 1) % m])
            for i in range(m)]


def _ham(a: list[int], b: list[int]) -> int:
    return sum(x ^ y for x, y in zip(a, b))


def probe_data() -> dict[str, object]:
    """Per-placement f1/f2 arrays using the round-14 protocol's exact
    LCG stream (backgrounds and per-rule placement draws verbatim)."""
    f1: dict[int, list[float]] = {r: [] for r in RULES}
    f2: dict[int, dict[int, list[float]]] = {
        r: {d: [] for d in _DISTANCES} for r in RULES}
    seed = _lcg()
    w = _WIDTH
    for _ in range(_PROBES):
        seed = _lcg(seed)
        bg = [((seed := _lcg(seed)) >> 16) & 1 for _ in range(w)]
        for r in RULES:
            clean = list(bg)
            for _ in range(_GENS):
                clean = _ring_step(r, clean)
            pa = (_lcg(seed) % w)
            seed = _lcg(seed)
            one = list(bg)
            for i in range(_BLOCK):
                one[(pa + i) % w] ^= 1
            for _ in range(_GENS):
                one = _ring_step(r, one)
            f1[r].append(_ham(clean, one) / w)
            for d in _DISTANCES:
                pb = (pa + d) % w
                two = list(bg)
                for i in range(_BLOCK):
                    two[(pa + i) % w] ^= 1
                    two[(pb + i) % w] ^= 1
                for _ in range(_GENS):
                    two = _ring_step(r, two)
                f2[r][d].append(_ham(clean, two) / w)
    return {"f1": f1, "f2": f2}


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


def damage_probe_certificates(
        dat: dict[str, object] | None = None) -> tuple[
        list[dict[str, object]], dict[str, object]]:
    if dat is None:
        dat = probe_data()
    f1: dict[int, list[float]] = dat["f1"]
    f2: dict[int, dict[int, list[float]]] = dat["f2"]

    def max_d(p: int, r: int) -> float:
        return max(f2[r][d][p] for d in _DISTANCES)

    wiper_sets = [sorted(r for r in RULES if max_d(p, r) <= _WIPE_LEVEL)
                  for p in range(_PROBES)]
    core = ({36, 251},)
    wiper_intersection = sorted(set.intersection(
        *({r for r in RULES if max_d(p, r) <= _WIPE_LEVEL}
          for p in range(_PROBES))))

    sat_p = [f2[147][4][p] - 2 * f1[147][p] for p in range(_PROBES)]
    f1m = {r: sum(f1[r]) / _PROBES for r in RULES}
    f2m = {r: {d: sum(f2[r][d]) / _PROBES for d in _DISTANCES}
           for r in RULES}
    mean_sat = {r: f2m[r][4] - 2 * f1m[r] for r in RULES}
    sat_unique_mean = {r for r in RULES if mean_sat[r] <= _SAT_LEVEL}

    far_max_p = [max(abs(f2[r][256][p] - 2 * f1[r][p]) for r in RULES)
                 for p in range(_PROBES)]
    syn_p: list[list[int]] = []
    for p in range(_PROBES):
        syn_p.append([r for r in RULES
                      if any(f2[r][d][p] > (1 + _SYNERGY_TOL)
                             * 2 * f1[r][p]
                             for d in _DISTANCES)])

    stats = {
        "detach_probe_ok": all(
            abs(f2[r][d][p] - _BASE) < 1e-9
            for r in (204, 51) for d in _DISTANCES
            for p in range(_PROBES)),
        "wiper_sets": wiper_sets,
        "wiper_intersection": wiper_intersection,
        "rule219_wipe_count": sum(219 in s for s in wiper_sets),
        "sat_p": sat_p,
        "sat_hold_count": sum(v <= _SAT_LEVEL for v in sat_p),
        "sat_invert_count": sum(v > -_SAT_LEVEL for v in sat_p),
        "sat_max": max(sat_p),
        "sat_min": min(sat_p),
        "sat_unique_mean": sorted(sat_unique_mean),
        "sat_mean_147": mean_sat[147],
        "far_max_p": far_max_p,
        "far_worst": max(far_max_p),
        "synergy_p": syn_p,
    }

    detach = stats["detach_probe_ok"]
    wp_mean = f2m
    wipers_mean = {r for r in RULES
                   if max(wp_mean[r][d] for d in _DISTANCES)
                   <= _WIPE_LEVEL}
    far_mean = max(abs(f2m[r][256] - 2 * f1m[r]) for r in RULES)

    certs = [
        _certify(
            "L_cdp_detach_exact",
            {"domain": f"width {_WIDTH}, blocks k = {_BLOCK}, "
                       f"distances {_DISTANCES}, gens {_GENS}, "
                       f"{_PROBES} probes, per placement",
             "law": f"rules 204, 51 keep F2(d) == 2*{_BLOCK}/{_WIDTH} "
                    "at EVERY distance and EVERY placement",
             "measured": {"base": _BASE, "all_placements_exact":
                          bool(detach)}},
            lambda: detach),
        _certify(
            "L_cdp_wipe_core",
            {"domain": "as above",
             "law": "the per-placement wiper sets (max_d F2 <= "
                    f"{_WIPE_LEVEL}) have intersection exactly "
                    "{36, 251}; both wipe at every placement",
             "measured": {"intersection":
                          stats["wiper_intersection"],
                          "rule219_wipe_count":
                          stats["rule219_wipe_count"]}},
            lambda: set(stats["wiper_intersection"]) == {36, 251}
                     and all(36 in s and 251 in s
                             for s in stats["wiper_sets"])),
        _certify(
            "L_cdp_wipe_set_exact",
            {"domain": "as above",
             "law": "the wiper set equals {36, 219, 251} at every "
                    "placement",
             "measured": {"per_placement_sets":
                          stats["wiper_sets"]}},
            lambda: all(set(s) == {36, 219, 251}
                        for s in stats["wiper_sets"])),
        _certify(
            "L_cdp_saturation_signature",
            {"domain": "as above",
             "law": "aggregate 147: mean(F2(4) - 2*F1) <= -0.03, 147 "
                    "unique among rules on means, AND its short-range "
                    "signature holds at >= 7/8 placements",
             "measured": {"mean_147":
                          round(stats["sat_mean_147"], 4),
                          "unique_on_means":
                          stats["sat_unique_mean"],
                          "hold_count": stats["sat_hold_count"],
                          "per_placement": [
                              round(v, 4) for v in stats["sat_p"]]}},
            lambda: mean_sat[147] <= _SAT_LEVEL
                    and sat_unique_mean == {147}
                    and stats["sat_hold_count"] >= _PROBES - 1),
        _certify(
            "L_cdp_saturation_universal",
            {"domain": "as above",
             "law": "147's short-range saturation (F2(4) - 2*F1 <= "
                    f"{_SAT_LEVEL}) holds at EVERY placement",
             "measured": {"inversion": "probe 3: +0.0391", "hold_count":
                          stats["sat_hold_count"], "max":
                          round(stats["sat_max"], 4),
                          "min": round(stats["sat_min"], 4)}},
            lambda: stats["sat_hold_count"] == _PROBES),
        _certify(
            "L_cdp_far_antipode",
            {"domain": "as above",
             "law": "|F2(256) - 2*F1| <= 0.005 at every placement and "
                    "every rule",
             "measured": {"per_placement_worst":
                          [round(v, 4) for v in stats["far_max_p"]],
                          "worst": round(stats["far_worst"], 4),
                          "mean_level": round(far_mean, 4)}},
            lambda: stats["far_worst"] <= 0.005),
        _certify(
            "L_cdp_synergy_none",
            {"domain": "as above",
             "law": "no rule exceeds (1 + 0.01)*2*F1 at any distance "
                    "at any placement",
             "measured": {"rules_violating_per_probe":
                          [[r for r in syn] for syn in stats["synergy_p"]]}},
            lambda: all(len(syn) == 0 for syn in stats["synergy_p"])),
    ]
    return certs, stats


if __name__ == "__main__":
    certs, stats = damage_probe_certificates()
    print(f"  L_cdp_per_placement damage laws (mean-level 147 sat "
          f"{round(stats['sat_mean_147'], 4)})")
    for c in certs:
        print(f"  {c['label']:<36} {c['status']:<16} "
              f"n_ok={c['n_ok']} n_fail={c['n_fail']}")
    print("  wiper sets per probe:",
          [sorted(s) for s in stats["wiper_sets"]])
    print("  147 F2(4)-2F1 per probe:",
          [round(v, 4) for v in stats["sat_p"]])
    print("  far worst per probe:",
          [round(v, 4) for v in stats["far_max_p"]])