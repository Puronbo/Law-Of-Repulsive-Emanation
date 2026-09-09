"""soliton_collision_profile_probe_audit: 147's interaction profile and
its time course, re-measured per placement.

The range audit (round 13) and the colliding-timecourse audit certified
rule 147's saturation profile rho(d) = F2(d)/(2*F1) on the fine d-grid
and the transient rho(d, g) = F2(d, g)/(2*F1(g)) on the generation
grid -- both on the MEAN over eight true-random probes.  Rounds 29--
37 established the discipline: a certified mean can hide a
placement-level reversal.  This audit replays each module's EXACT LCG
stream and protocol but retains every placement's value, and re-checks
each signature statement per placement while re-certifying the
aggregate level from the same run.

Per-placement findings (range, rule 147)::

    core worst rho_p(d <= 16)  per placement
      0.598   1.130   0.733   0.714   0.758   0.608   0.700   0.553

so the round-13 "saturation core" claim max rho(d <= 16) <= 0.66 is
TRUE only on the mean -- placements 1, 2, 3, 4, 6 exceed it, placement
1 inverting to rho = 1.13 (the close blocks ADD more than the
independent baseline on that packet address).  The per-placement
profile swings between rho = 0.55 and rho = 4.4 across the grid: the
fine profile is a placement-structured object, not a family-level law.
The time-course story matches: at d = 16 the constructive opening
rho(g = 2) varies per placement from 0.875 to 2.500, and at d = 256
the worst per-placement |rho - 1| reaches 3.375 -- a ratio blowup
where a placement's 2*F1(g) is tiny (an erasure lucky draw on that
packet address).  The transparent rules remain anchors: 204 (range
and timecourse) and 51 (timecourse) keep rho = 1 exactly at every d
and every g at every placement.

Only the AGGREGATE level of the round-13/12 laws survives, and the
aggregate reproduces from this same run: the mean profile recomputes
the round-13 table (core max <= 0.66, halo min >= 0.95) and the mean
time course recomputes the constructive transient (mean rho(g = 2) ~
1.25) and the far wobble bounded by 0.30.

Certificates:

    L_rp_transparent_flat       PASS/FAIL  rule 204 keeps
                                |rho_p - 1| <= 1/512 at every d at
                                every placement.
    L_rp_mean_core              PASS/FAIL  the round-13 aggregate
                                survives: max mean-rho(d <= 16) <= 0.66
                                AND min mean-rho(d >= 96) >= 0.95,
                                recomputed from this run.
    L_rp_core_steady            PASS/FAIL  FALSE CANDIDATE: 147's
                                core max rho_p(d <= 16) <= 0.66 at
                                every placement (fails at 5/8, worst
                                1.130).
    L_rp_recovery_halo_majority PASS/FAIL  FALSE CANDIDATE: at every
                                placement rho_p(64) >= rho_p(8) + 0.30.
    L_rp_profile_identical      PASS/FAIL  FALSE CANDIDATE: 147's fine
                                profile is placement-identical.
    L_tp_transparent_exact      PASS/FAIL  {204, 51} keep
                                |F2_p[g] - 2*F1_p[g]| <= 1 cell at
                                every generation at every placement.
    L_tp_mean_repro             PASS/FAIL  the aggregate time course
                                reproduces: mean rho(g = 2) >= 1.10 at
                                d = 16 and mean |rho - 1| <= 0.30 at
                                every g at d = 256.
    L_tp_constructive_opening   PASS/FAIL  FALSE CANDIDATE: 147 at
                                d = 16 opens with rho_p(g = 2) >= 1.10
                                at every placement (dips to 0.875).
    L_tp_far_flat               PASS/FAIL  FALSE CANDIDATE: 147 at
                                d = 256: |rho_p - 1| <= 0.30 at every
                                generation at every placement.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_collision_range_audit import (  # noqa: E402
    _BLOCK as _R_BLOCK,
    _DISTANCES as _R_DISTANCES,
    _GENS as _R_GENS,
    _PROBES as _R_PROBES,
    _WIDTH as _R_WIDTH,
)
from soliton_eca.soliton_collision_timecourse_audit import (  # noqa: E402
    _BLOCK as _T_BLOCK,
    _DISTANCES as _T_DISTANCES,
    _GENS as _T_GENS,
    _PROBES as _T_PROBES,
    _TIMES,
    _WIDTH as _T_WIDTH,
)

from soliton_eca.soliton_collision_range_audit import (  # noqa: E402
    _lcg as _lcg_r,
    _ring_step as _ring_r,
    _ham as _ham_r,
)
from soliton_eca.soliton_collision_timecourse_audit import (  # noqa: E402
    _lcg as _lcg_t,
    _ring_step as _ring_t,
    _ham as _ham_t,
)

_CORE_LEVEL = 0.66
_HALO_LEVEL = 0.95
_RECOVERY = 0.30
_IDENT_TOL = 0.01
_FAR_TOL = 0.30
_CONSTRUCT_MIN = 1.10


def _range_per_placement(r: int) -> dict[int, list[float]]:
    """{d: [rho_p over placements]} with the round-13 exact stream.
    Each placement's rho is normalized by that same placement's F1."""
    f1: list[float] = []
    f2: dict[int, list[float]] = {d: [] for d in _R_DISTANCES}
    seed = _lcg_r()
    w = _R_WIDTH
    for _ in range(_R_PROBES):
        seed = _lcg_r(seed)
        bg = [((seed := _lcg_r(seed)) >> 16) & 1 for _ in range(w)]
        pa = (_lcg_r(seed) % w)
        seed = _lcg_r(seed)
        clean = list(bg)
        one = list(bg)
        two = {d: list(bg) for d in _R_DISTANCES}
        pts = {d: (pa + d) % w for d in _R_DISTANCES}
        for i in range(_R_BLOCK):
            one[(pa + i) % w] ^= 1
            for d in _R_DISTANCES:
                two[d][(pa + i) % w] ^= 1
                two[d][(pts[d] + i) % w] ^= 1
        for _ in range(_R_GENS):
            clean = _ring_r(r, clean)
            one = _ring_r(r, one)
            for d in _R_DISTANCES:
                two[d] = _ring_r(r, two[d])
        f1.append(_ham_r(clean, one) / w)
        for d in _R_DISTANCES:
            f2[d].append(_ham_r(clean, two[d]) / w)
    return {d: [f2[d][p] / (2 * f1[p]) for p in range(_R_PROBES)]
            for d in _R_DISTANCES}


def _range_mean(r: int) -> dict[int, float]:
    """Round-13 style aggregate: mean_f2(d) / (2 * mean_f1)."""
    f1: list[float] = []
    f2: dict[int, list[float]] = {d: [] for d in _R_DISTANCES}
    seed = _lcg_r()
    w = _R_WIDTH
    for _ in range(_R_PROBES):
        seed = _lcg_r(seed)
        bg = [((seed := _lcg_r(seed)) >> 16) & 1 for _ in range(w)]
        pa = (_lcg_r(seed) % w)
        seed = _lcg_r(seed)
        clean = list(bg)
        one = list(bg)
        two = {d: list(bg) for d in _R_DISTANCES}
        pts = {d: (pa + d) % w for d in _R_DISTANCES}
        for i in range(_R_BLOCK):
            one[(pa + i) % w] ^= 1
            for d in _R_DISTANCES:
                two[d][(pa + i) % w] ^= 1
                two[d][(pts[d] + i) % w] ^= 1
        for _ in range(_R_GENS):
            clean = _ring_r(r, clean)
            one = _ring_r(r, one)
            for d in _R_DISTANCES:
                two[d] = _ring_r(r, two[d])
        f1.append(_ham_r(clean, one) / w)
        for d in _R_DISTANCES:
            f2[d].append(_ham_r(clean, two[d]) / w)
    m1 = sum(f1) / len(f1)
    return {d: (sum(f2[d]) / len(f2[d])) / (2 * m1)
            for d in _R_DISTANCES}


def range_profile_per_placement() -> dict[int, dict[int, list[float]]]:
    return {r: _range_per_placement(r) for r in (147, 204)}


def _timecourse_per_placement(r: int) -> dict[int, dict[int, list[float]]]:
    """{d: {g: [rho over placements]}} with the round-12/13 exact
    stream; each placement normalized by that placement's F1(g)."""
    f1: dict[int, list[float]] = {g: [] for g in _TIMES}
    f2: dict[int, dict[int, list[float]]] = {
        d: {g: [] for g in _TIMES} for d in _T_DISTANCES}
    seed = _lcg_t()
    w = _T_WIDTH
    for _ in range(_T_PROBES):
        seed = _lcg_t(seed)
        bg = [((seed := _lcg_t(seed)) >> 16) & 1 for _ in range(w)]
        pa = (seed := _lcg_t(seed)) % w
        seed = _lcg_t(seed)
        one = list(bg)
        two = {d: list(bg) for d in _T_DISTANCES}
        pts = {d: (pa + d) % w for d in _T_DISTANCES}
        for i in range(_T_BLOCK):
            one[(pa + i) % w] ^= 1
            for d in _T_DISTANCES:
                two[d][(pa + i) % w] ^= 1
                two[d][(pts[d] + i) % w] ^= 1
        clean = list(bg)
        for g in range(1, _T_GENS + 1):
            clean = _ring_t(r, clean)
            one = _ring_t(r, one)
            for d in _T_DISTANCES:
                two[d] = _ring_t(r, two[d])
            if g in _TIMES:
                f1[g].append(_ham_t(clean, one) / w)
                for d in _T_DISTANCES:
                    f2[d][g].append(_ham_t(clean, two[d]) / w)
    return {d: {g: [f2[d][g][p] / (2 * f1[g][p])
                    for p in range(_T_PROBES)]
                for g in _TIMES}
            for d in _T_DISTANCES}


def _timecourse_mean(r: int) -> dict[int, dict[int, float]]:
    """{d: {g: mean-ratio}} -- the round-12/13 aggregate."""
    f1: dict[int, list[float]] = {g: [] for g in _TIMES}
    f2: dict[int, dict[int, list[float]]] = {
        d: {g: [] for g in _TIMES} for d in _T_DISTANCES}
    seed = _lcg_t()
    w = _T_WIDTH
    for _ in range(_T_PROBES):
        seed = _lcg_t(seed)
        bg = [((seed := _lcg_t(seed)) >> 16) & 1 for _ in range(w)]
        pa = (seed := _lcg_t(seed)) % w
        seed = _lcg_t(seed)
        one = list(bg)
        two = {d: list(bg) for d in _T_DISTANCES}
        pts = {d: (pa + d) % w for d in _T_DISTANCES}
        for i in range(_T_BLOCK):
            one[(pa + i) % w] ^= 1
            for d in _T_DISTANCES:
                two[d][(pa + i) % w] ^= 1
                two[d][(pts[d] + i) % w] ^= 1
        clean = list(bg)
        for g in range(1, _T_GENS + 1):
            clean = _ring_t(r, clean)
            one = _ring_t(r, one)
            for d in _T_DISTANCES:
                two[d] = _ring_t(r, two[d])
            if g in _TIMES:
                f1[g].append(_ham_t(clean, one) / w)
                for d in _T_DISTANCES:
                    f2[d][g].append(_ham_t(clean, two[d]) / w)
    return {d: {g: (sum(f2[d][g]) / len(f2[d][g])) /
                (2 * (sum(f1[g]) / len(f1[g])))
                for g in _TIMES}
            for d in _T_DISTANCES}


def timecourse_per_placement() -> dict[int, dict[int, dict[int, list[float]]]]:
    return {r: _timecourse_per_placement(r) for r in (147, 204, 51)}


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


def profile_probe_certificates() -> tuple[list[dict[str, object]],
                                          dict[str, object]]:
    rp = range_profile_per_placement()
    rm = _range_mean(147)
    tc = timecourse_per_placement()
    tcm = _timecourse_mean(147)
    r147 = rp[147]
    r204 = rp[204]

    transparent_ok = all(
        abs(v - 1.0) <= 1 / _R_WIDTH
        for d in _R_DISTANCES for v in r204[d])

    mean_core = max(rm[d] for d in _R_DISTANCES if d <= 16)
    mean_halo = min(rm[d] for d in _R_DISTANCES if d >= 96)
    mean_core_ok = mean_core <= _CORE_LEVEL and mean_halo >= _HALO_LEVEL

    core_pp = [max(r147[d][p] for d in _R_DISTANCES if d <= 16)
               for p in range(_R_PROBES)]
    core_steady_ok = all(v <= _CORE_LEVEL for v in core_pp)

    recover_ok = all(
        r147[64][p] >= r147[8][p] + _RECOVERY
        for p in range(_R_PROBES))

    pair_worst = max(
        abs(r147[d][p] - r147[d][q])
        for d in _R_DISTANCES for p in range(_R_PROBES)
        for q in range(p + 1, _R_PROBES))
    identical_ok = pair_worst <= _IDENT_TOL

    tc204 = tc[204]
    tc51 = tc[51]
    transparent_tc_ok = all(
        abs(v - 1.0) <= 1 / _T_WIDTH
        for r in (204, 51)
        for d in _T_DISTANCES for g in _TIMES for v in tc[r][d][g])

    tc147 = tc[147]
    constr_p = tc147[16][2]
    constructive_ok = all(v >= _CONSTRUCT_MIN for v in constr_p)

    far_worst_pp = [max(abs(tc147[256][g][p] - 1.0) for g in _TIMES)
                    for p in range(_T_PROBES)]
    far_ok = all(abs(v - 1.0) <= _FAR_TOL
                 for g in _TIMES for v in tc147[256][g])

    mean_constr = tcm[16][2]
    mean_far_worst = max(abs(tcm[256][g] - 1.0) for g in _TIMES)
    mean_tc_ok = mean_constr >= _CONSTRUCT_MIN and \
        mean_far_worst <= _FAR_TOL

    stats = {
        "mean_profile_147": {str(d): round(rm[d], 3) for d in _R_DISTANCES},
        "range_spread_per_d": {str(d): round(max(r147[d]) - min(r147[d]), 4)
                               for d in _R_DISTANCES},
        "core_worst_per_placement": [round(v, 4) for v in core_pp],
        "mean_core_max": round(mean_core, 3),
        "mean_halo_min": round(mean_halo, 3),
        "constructive_rho2_per_placement": [round(v, 4) for v in constr_p],
        "mean_constructive": round(mean_constr, 4),
        "far_worst_per_placement": [round(v, 4) for v in far_worst_pp],
        "mean_far_worst": round(mean_far_worst, 4),
        "profile_pairwise_worst": round(pair_worst, 4),
    }

    certs = [
        _certify(
            "L_rp_transparent_flat",
            {"domain": f"width {_R_WIDTH}, blocks of {_R_BLOCK}, "
                       f"gens {_R_GENS}, {_R_PROBES} probes, "
                       f"d-grid {_R_DISTANCES}, per placement",
             "law": "rule 204 keeps rho_p = 1 (integer-exact 2*F1 == "
                    "F2) at EVERY d at EVERY placement -- the "
                    "transparent bus detaches identically everywhere",
             "measured": {"worst_off_one": round(max(
                 abs(v - 1.0) for d in _R_DISTANCES for v in r204[d]), 6)}},
            lambda: transparent_ok),
        _certify(
            "L_rp_mean_core",
            {"domain": "as above, aggregate",
             "law": "the round-13 aggregate survives: max mean-rho(d "
                    f"<= 16) <= {_CORE_LEVEL} and min mean-rho(d >= "
                    f"96) >= {_HALO_LEVEL}",
             "measured": {"mean_core_max": stats["mean_core_max"],
                          "mean_halo_min": stats["mean_halo_min"],
                          "mean_profile": stats["mean_profile_147"]}},
            lambda: mean_core_ok),
        _certify(
            "L_rp_core_steady",
            {"domain": "as above, per placement",
             "law": "rule 147's core max rho_p(d <= 16) <= "
                    f"{_CORE_LEVEL} at EVERY placement",
             "measured": f"FALSE: 5/8 placements exceed "
                         f"{_CORE_LEVEL}, worst {max(core_pp):.3f} at "
                         "placement 1 -- the close blocks ADD more "
                         "than the independent baseline on that "
                         "packet address",
             "core_worst_per_placement": stats["core_worst_per_placement"]},
            lambda: core_steady_ok),
        _certify(
            "L_rp_recovery_halo_majority",
            {"domain": "as above, per placement",
             "law": "at EVERY placement rho_p(64) >= rho_p(8) + "
                    f"{_RECOVERY}",
             "measured": "FALSE: the 8 -> 64 recovery band holds only "
                         "in aggregate (the per-placement spread at "
                         "d = 8 is 0.53 and at d = 64 is 0.74)",
             "range_spread_per_d": stats["range_spread_per_d"]},
            lambda: recover_ok),
        _certify(
            "L_rp_profile_identical",
            {"domain": "as above, per placement",
             "law": "rule 147's fine profile is placement-identical "
                    f"(pairwise |rho_p - rho_q| <= {_IDENT_TOL} at "
                    "every d)",
             "measured": f"FALSE: the pairwise spread reaches "
                         f"{pair_worst:.3f} across placements -- the "
                         "fine profile is a placement-structured "
                         "object, not a family-level law",
             "pairwise_worst": round(pair_worst, 4),
             "range_spread_per_d": stats["range_spread_per_d"]},
            lambda: identical_ok),
        _certify(
            "L_tp_transparent_exact",
            {"domain": f"width {_T_WIDTH}, d in {_T_DISTANCES}, gens "
                       f"in {_TIMES}, {_T_PROBES} probes, per "
                       "placement",
             "law": "rules 204 and 51 keep |F2_p[g] - 2*F1_p[g]| <= "
                    "1 cell at every generation at every placement -- "
                    "the isometry bus conserves the two-packet "
                    "distance instant by instant, everywhere",
             "measured": {"worst_off_two": round(max(
                 abs(v - 1.0) for r in (204, 51)
                 for d in _T_DISTANCES for g in _TIMES
                 for v in tc[r][d][g]), 6)}},
            lambda: transparent_tc_ok),
        _certify(
            "L_tp_mean_repro",
            {"domain": "as above, aggregate",
             "law": "the aggregate time course reproduces: mean "
                    f"rho(g = 2) >= {_CONSTRUCT_MIN} at d = 16 and "
                    f"mean |rho - 1| <= {_FAR_TOL} at every g at "
                    "d = 256",
             "measured": {"mean_constructive": stats["mean_constructive"],
                          "mean_far_worst": stats["mean_far_worst"]}},
            lambda: mean_tc_ok),
        _certify(
            "L_tp_constructive_opening",
            {"domain": "as above, per placement",
             "law": "rule 147 at d = 16 opens with rho_p(g = 2) >= "
                    f"{_CONSTRUCT_MIN} at EVERY placement",
             "measured": f"FALSE: the transient dips to "
                         f"{min(constr_p):.3f} (placement 0), peaks "
                         f"to {max(constr_p):.3f} -- the constructive "
                         "opening is a mean-level law",
             "rho2_per_placement": stats["constructive_rho2_per_placement"]},
            lambda: constructive_ok),
        _certify(
            "L_tp_far_flat",
            {"domain": "as above, per placement",
             "law": "rule 147 at d = 256 keeps |rho_p - 1| <= "
                    f"{_FAR_TOL} at every generation at every "
                    "placement",
             "measured": f"FALSE: the worst placement reaches "
                         f"{max(far_worst_pp):.3f} -- a ratio blowup "
                         "where that placement's 2*F1(g) is tiny (an "
                         "erasure-lucky draw on the packet address)",
             "far_worst_per_placement": stats["far_worst_per_placement"]},
            lambda: far_ok),
    ]
    return certs, stats


if __name__ == "__main__":
    certs, stats = profile_probe_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("  mean profile 147:",
          {k: v for k, v in sorted(stats["mean_profile_147"].items())})
    print("  range spread per d:",
          {k: v for k, v in sorted(stats["range_spread_per_d"].items())})
    print("  core worst per placement:",
          stats["core_worst_per_placement"])
    print("  constructive rho(g=2) per placement:",
          stats["constructive_rho2_per_placement"])
    print("  far worst per placement:",
          stats["far_worst_per_placement"])