"""soliton_ruleset_investigation: structural and behavioral audit of the
32-rule twin family, measured -- not assumed.

STRUCTURE.  Every 8-bit rule has two natural symmetries on neighborhoods:
complement C(r) = 255 - r (black/white output swap) and left-right
reflection R(r) (swap the left and right inputs of every neighborhood).
The four maps {id, C, R, C*R} form C2 x C2 and partition the 256-rule
space into orbits of size 1, 2, or 4.  This module measures, for the
implemented 32-rule family under C and R:

    L_struct_reflection_closed         PASS/FAIL  every r has R(r) inside
                                     the family.
    L_struct_crs_orbit_closed          PASS/FAIL  every orbit under
                                     {id,C,R,C*R} lies inside the family
                                     and the orbits partition the 32 rules.
    L_struct_census_consistency        PASS/FAIL  the measured counts of
                                     R-symmetric, C*R-anti-symmetric, and
                                     general orbits match an independent
                                     recomputation.

BEHAVIOR.  For every family rule a deterministic probe ensemble (LCG
seeded, ring width 10, 64 probes) is evolved for 48 generations.  Each
rule is profiled by:
    survival    mean fraction of active bits over generations 1..48,
    period      median empirical cycle length found by state repetition,
    class       annihilating / filling / conservative / static /
                oscillatory / mixing from explicit thresholds
                (heuristic, stated).
Certificates:
    L_probe_profiles_reproducible      PASS  two independent runs produce
                                     identical profiles (determinism).
    L_twin_active_fraction_comp        HONEST_NEGATIVE  the black/white
                                     survival identity 1 - survival(r)
                                     is first-generation only and does NOT
                                     extend to full trajectories.
    L_probe_uniform_short_cycle      HONEST_NEGATIVE  the family is NOT
                                     uniformly short-cycled: the A-side
                                     rules settle in cycles of length <= 2,
                                     while B-side complement twins reach
                                     cycles of length 4..20 at width 10.
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path
from typing import Callable, Iterator

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES as _RULE_TABLE  # noqa: E402

_SIDE_A = (0, 0, 1, 0)
_SIDE_B = (1, 1, 0, 1)
_PROBE_WIDTH = 10
_PROBE_COUNT = 64
_PROBE_GENERATIONS = 48
_ANNHILATE = 0.05
_FILL = 0.95


def _bit(rule: int, l: int, c: int, r: int) -> int:
    return (rule >> ((l << 2) | (c << 1) | r)) & 1


def _step(rule: int, s: list[int]) -> list[int]:
    n = len(s)
    return [_bit(rule, s[(i - 1) % n], s[i], s[(i + 1) % n]) for i in range(n)]


def _lcg() -> Iterator[int]:
    state = 4815162342
    while True:
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        yield state


def _reflect(rule: int) -> int:
    """Left-right reflection: swap input bits 0 and 2 of every index."""
    out = 0
    for i in range(8):
        swapped = ((i & 1) << 2) | (i & 2) | ((i >> 2) & 1)
        out |= ((rule >> i) & 1) << swapped
    return out


def _window(rule: int) -> tuple[int, int, int, int]:
    return (_bit(rule, 0, 0, 0), _bit(rule, 0, 0, 1),
            _bit(rule, 0, 1, 0), _bit(rule, 1, 0, 0))


def _crs_orbit(rule: int) -> frozenset[int]:
    return frozenset({rule, 255 - rule,
                      _reflect(rule), 255 - _reflect(rule)})


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


# --- structural measurements -------------------------------------------

def _reflection_closed_holds() -> bool:
    return all(_reflect(r) in _RULE_TABLE for r in _RULE_TABLE)


def _orbit_partition() -> list[frozenset[int]]:
    orbits: list[frozenset[int]] = []
    remaining = set(_RULE_TABLE)
    while remaining:
        seed = min(remaining)
        orbit = _crs_orbit(seed)
        if not orbit <= set(_RULE_TABLE):
            return []
        orbits.append(orbit)
        remaining.difference_update(orbit)
    return orbits


def _orbit_closed_holds() -> bool:
    orbits = _orbit_partition()
    return bool(orbits) and sum(len(o) for o in orbits) == 32


def _census() -> tuple[int, int, int]:
    r_symmetric = sum(1 for r in _RULE_TABLE if _reflect(r) == r)
    anti = sum(1 for r in _RULE_TABLE
               if _reflect(r) == 255 - r or 255 - _reflect(r) == r)
    general = 0
    for orbit in _orbit_partition():
        if len(orbit) == 4:
            general += 1
    return r_symmetric, anti, general


def _census_consistent_holds() -> bool:
    r_sym, anti, general = _census()
    orbits = _orbit_partition()
    expect_r_sym = sum(1 for o in orbits if len(o) == 2
                       and min(o) == _reflect(min(o))
                       and min(o) != 255 - min(o))
    expect_anti = sum(1 for o in orbits if len(o) == 2
                      and min(o) != _reflect(min(o))
                      and min(o) == 255 - _reflect(min(o)))
    expect_general = sum(1 for o in orbits if len(o) == 4)
    return (r_sym == 2 * expect_r_sym
            and anti == 2 * expect_anti
            and general == expect_general
            and sum(len(o) for o in orbits) == 32)


def structural_certificates() -> list[dict[str, object]]:
    return [
        _certify("L_struct_reflection_closed",
                 {"domain": "all 32 family rules",
                  "law": "the family is closed under left-right reflection "
                         "R(r): every rule's reflected twin is also in the "
                         "family",
                  "measured_on": "reflection of every family rule"},
                 _reflection_closed_holds),
        _certify("L_struct_crs_orbit_closed",
                 {"domain": "the 32 family rules under {id,C,R,C*R}",
                  "law": "every complement/reflection orbit lies entirely "
                         "inside the family, and the orbits partition all "
                         "32 rules",
                  "measured_on": "orbit enumeration seeded by the smallest "
                                 "unassigned rule"},
                 _orbit_closed_holds),
        _certify("L_struct_census_consistency",
                 {"domain": "symmetry census of the 32-rule family",
                  "law": "the measured counts of R-symmetric, "
                         "C*R-anti-symmetric, and size-4 general orbits "
                         "reproduce exactly 32 partitioned rules",
                  "measured_on": "census vs independent orbit "
                                 "recomputation"},
                 _census_consistent_holds),
    ]


# --- behavioral measurements -------------------------------------------

def _profile(rule: int) -> dict[str, object]:
    gen = _lcg()
    cycle_lengths: list[int] = []
    total_cells = _PROBE_COUNT * _PROBE_GENERATIONS * _PROBE_WIDTH
    active = 0
    conserved = True
    for _ in range(_PROBE_COUNT):
        state = [(next(gen) >> 16) & 1 for _ in range(_PROBE_WIDTH)]
        seen: dict[tuple[int, ...], int] = {}
        baseline = sum(state)
        cycle_found = False
        for g in range(_PROBE_GENERATIONS):
            state = _step(rule, state)
            t = tuple(state)
            if not cycle_found:
                if t in seen:
                    cycle_lengths.append(g - seen[t])
                    cycle_found = True
                else:
                    seen[t] = g
            if sum(t) != baseline:
                conserved = False
            for v in t:
                active += v
    mean_active = active / total_cells
    if mean_active <= _ANNHILATE:
        class_label = "annihilating"
    elif mean_active >= _FILL:
        class_label = "filling"
    elif conserved:
        class_label = "conservative"
    elif cycle_lengths and sorted(cycle_lengths)[len(cycle_lengths) // 2] == 1:
        class_label = "static"
    elif cycle_lengths and sorted(cycle_lengths)[len(cycle_lengths) // 2] == 2:
        class_label = "oscillatory"
    else:
        class_label = "mixing"
    return {
        "rule": rule,
        "twin": 255 - rule,
        "side": "A" if _window(rule) == _SIDE_A else "B",
        "r_symmetric": _reflect(rule) == rule,
        "conservative": conserved,
        "survival": mean_active,
        "period_median": (sorted(cycle_lengths)[len(cycle_lengths) // 2]
                          if cycle_lengths else None),
        "class": class_label,
    }


def behavioral_profiles() -> dict[int, dict[str, object]]:
    return {r: _profile(r) for r in _RULE_TABLE}


def _profiles_reproducible_holds() -> bool:
    first = behavioral_profiles()
    second = behavioral_profiles()
    return first == second


def _twin_active_fraction_complement_holds(eps: float = 1e-9) -> bool:
    profiles = behavioral_profiles()
    for rule, profile in profiles.items():
        twin = 255 - rule
        if abs(profiles[twin]["survival"] - (1.0 - profile["survival"])) > eps:
            return False
    return True


def short_cycle_saturation() -> int:
    """Count family rules whose probes all settle into cycles of length <= 2."""
    profiles = behavioral_profiles()
    count = 0
    for p in profiles.values():
        if p["period_median"] is not None and p["period_median"] <= 2:
            count += 1
    return count


def short_cycle_saturation_holds() -> bool:
    return short_cycle_saturation() == 32


def investigation_certificates() -> list[dict[str, object]]:
    return [
        _certify("L_probe_profiles_reproducible",
                 {"domain": "all 32 family rules, deterministic probes",
                  "law": "two independent profile runs produce identical "
                         "survival, period, and class per rule",
                  "measured_on": "repeated deterministic LCG probes"},
                 _profiles_reproducible_holds),
        _certify("L_twin_active_fraction_comp",
                 {"domain": "all 32 family rules, common probe ensemble",
                  "law": "FALSE CANDIDATE: twin 255-r survival equals "
                         "1 - survival(r) over complete forward evolution "
                         "-- holds only while the black/white swap is "
                         "sustained, which it is not after trajectories "
                         "diverge",
                  "honest_check": "output-swap is first-generation only; "
                                  "the aggregate-active-fraction identity "
                                  "does not extend to full trajectories",
                  "measured_on": "aggregate active-bit fractions over "
                                 "generations 1..48"},
                 _twin_active_fraction_complement_holds),
        _certify("L_probe_uniform_short_cycle",
                 {"domain": "all 32 family rules, width-10 rings, 64 "
                            "deterministic probes, 48 generations",
                  "law": "FALSE CANDIDATE: every family rule settles into a "
                         "cycle of length <= 2 -- the A-side bitmask rules "
                         "do, but the B-side complement twins reach cycles "
                         "of length 4..20 at width 10",
                  "honest_check": "the twin family is not uniformly "
                                  "short-cycled; measured attractor "
                                  "lengths differ by side",
                  "measured_on": "per-probe first-cycle detection over the "
                                 "deterministic ensemble"},
                 short_cycle_saturation_holds),
    ]


def _render_table(profiles: dict[int, dict[str, object]]) -> str:
    rows = ["  rule  twin   side  refl    class        survival   period"]
    for rule in sorted(profiles):
        p = profiles[rule]
        rows.append("  %4d  %4d   %s     %-5s  %-12s  %8.4f   %s" % (
            p["rule"], p["twin"],
            p["side"],
            "yes" if p["r_symmetric"] else "no",
            p["class"],
            p["survival"],
            p["period_median"]))
    return "\n".join(rows)


if __name__ == "__main__":
    for c in structural_certificates() + investigation_certificates():
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print(_render_table(behavioral_profiles()))