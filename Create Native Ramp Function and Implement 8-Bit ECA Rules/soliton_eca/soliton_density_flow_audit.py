"""soliton_density_flow_audit: population-density trajectories per rule.

A rule's functional graph on the torus at width 16 induces a density walk:
start from LCG random backgrounds at three seed densities
({0.25, 0.5, 0.75}) and watch the popcount fraction over 32 generations.
Three behaviors were verified to exist in the family:

  1. exact invariant   -- density(t) == density(0) for every generation,
                          every seed, every probe;
  2. density settling  -- the density walk reaches a fixed level (constant
                          tail); every stationary torus rule settles;
  3. biased attractors -- non-stationary rules need NOT converge to a
                          balanced half density: some mix toward clearly
                          biased levels (measured ~0.62-0.69 for
                          {91, 123, 155, 211}).

Certificates:

    L_density_exact_invariant     PASS/FAIL  exactly rule 204 preserves
                              the population density: density(t) ==
                              density(0) for all seeds/probes/generations.
    L_density_stationary_settles  PASS/FAIL  every width-16 stationary
                              rule (torus max_cycle 1) settles its density
                              to a constant tail within the horizon for
                              every seed and probe.
    L_density_half_attractor      HONEST_NEGATIVE  the tested claim "every
                              non-stationary rule converges to the half
                              density" is FALSE: rules {91, 123, 155, 211}
                              settle at mean densities ~0.62-0.69, biased
                              away from 0.5.
    L_density_two_lap_oscillates PASS/FAIL  the two-lap rules {27, 59, 83,
                              115} never settle a constant tail -- their
                              density oscillates with the lap (torus max
                              cycle 32) and is NOT a fixed attractor
                              value.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES  # noqa: E402
from soliton_eca.soliton_census_scaling_audit import census_data  # noqa: E402

_WIDTH = 16
_HORIZON = 32
_TAIL = 8
_SEED_DENSITIES = (0.25, 0.5, 0.75)
_PROBES_PER_DENSITY = 2

_SETTLE_SPREAD = 0.005
_HALF_TOL = 0.08
_HALF_BIASED = {91, 123, 155, 211}
_TWO_LAP = {27, 59, 83, 115}
_OSCILLATE_SPREAD = 0.01


def _lcg(start: int = 0x0DDB1A5E5BAD5EED) -> int:
    return (6364136223846793005 * start
            + 1442695040888963407) & ((1 << 64) - 1)


def _bit(r: int, l: int, c: int, rr: int) -> int:
    return (r >> ((l << 2) | (c << 1) | rr)) & 1


def _ring_step(r: int, s: list[int]) -> list[int]:
    m = len(s)
    return [_bit(r, s[i - 1], s[i], s[(i + 1) % m]) for i in range(m)]


def _density(s: list[int]) -> float:
    return sum(s) / len(s)


def _seeds() -> list[list[int]]:
    outs: list[list[int]] = []
    seed = _lcg()
    for p in _SEED_DENSITIES:
        for _ in range(_PROBES_PER_DENSITY):
            seed = _lcg(seed)
            outs.append([1 if (_lcg(seed := _lcg(seed)) & 0xFFFF) / 65536
                         < p else 0 for _ in range(_WIDTH)])
    return outs


def _density_series(r: int) -> list[list[float]]:
    series: list[list[float]] = []
    for bg in _seeds():
        s = list(bg)
        row = [_density(bg)]
        for _ in range(_HORIZON):
            s = _ring_step(r, s)
            row.append(_density(s))
        series.append(row)
    return series


def _exact_invariant_holds() -> bool:
    for r in RULES:
        violates = False
        for row in _density_series(r):
            if any(abs(v - row[0]) > 1e-9 for v in row[1:]):
                violates = True
                break
        if (r == 204) == violates:
            return False
    return True


def _stationary() -> set[int]:
    return {r for r, d in census_data().items() if d["torus_max_cycle"] == 1}


def _stationary_settles_holds() -> bool:
    for r in sorted(_stationary()):
        for row in _density_series(r):
            tail = row[-_TAIL:]
            if max(tail) - min(tail) > _SETTLE_SPREAD:
                return False
    return True


def _tail_means() -> dict[int, float]:
    means = {}
    for r in RULES:
        vals = [sum(row[-_TAIL:]) / len(row[-_TAIL:])
                for row in _density_series(r)]
        means[r] = sum(vals) / len(vals)
    return means


def _half_attractor_holds(means: dict[int, float]) -> bool:
    nonstationary = {r for r in RULES if r not in _stationary()}
    for r in nonstationary:
        if abs(means[r] - 0.5) > _HALF_TOL:
            return False
    return True


def _two_lap_oscillates_holds() -> bool:
    for r in _TWO_LAP:
        osc = any(max(row[-_TAIL:]) - min(row[-_TAIL:]) > _OSCILLATE_SPREAD
                  for row in _density_series(r))
        if not osc:
            return False
    return True


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
        "first_failure": None if n_ok else {
            "datum": "the predicate Failed"},
    }


def density_flow_certificates() -> list[dict[str, object]]:
    means = _tail_means()
    return [
        _certify("L_density_exact_invariant",
                 {"width": _WIDTH,
                  "seeds": f"densities {_SEED_DENSITIES} x "
                           f"{_PROBES_PER_DENSITY} LCG probes",
                  "law": "exactly rule 204 preserves the population "
                         "density for every generation, seed and probe",
                  "measured": "density(t) == density(0) check over "
                              f"{_HORIZON} generations"},
                 _exact_invariant_holds),
        _certify("L_density_stationary_settles",
                 {"width": _WIDTH,
                  "stationary": sorted(_stationary()),
                  "law": "every width-16 stationary rule settles its "
                         "density to a constant tail (spread < "
                         f"{_SETTLE_SPREAD}) for every seed and probe",
                  "measured": "tail-8 spread per (rule, seed)"},
                 _stationary_settles_holds),
        _certify("L_density_half_attractor",
                 {"law": "every non-stationary rule converges to half "
                         f"density (tail mean within {_HALF_TOL} of 0.5)",
                  "measured": {str(r): round(means[r], 3) for r in
                               sorted(_HALF_BIASED)} | {
                                   "all": {str(r): round(means[r], 3)
                                           for r in sorted(
                                               set(RULES) - _stationary())}}},
                 lambda: _half_attractor_holds(means)),
        _certify("L_density_two_lap_oscillates",
                 {"law": f"the two-lap rules {sorted(_TWO_LAP)} never "
                         "settle a constant density tail -- the density "
                         "oscillates with the torus lap (max cycle 32)",
                  "measured": "tail-8 spread per seed exceeds "
                              f"{_OSCILLATE_SPREAD} for some seed on "
                              "every two-lap rule"},
                 _two_lap_oscillates_holds),
    ]


if __name__ == "__main__":
    for c in density_flow_certificates():
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    means = _tail_means()
    print("  rule  tail-mean density (across all seeds; * = stationary)")
    for r in RULES:
        dots = "*" if r in _stationary() else " "
        print("  %3d %s  %.3f" % (r, dots, means[r]))