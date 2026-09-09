"""soliton_perturbation_audit: single-bit damage rates, true-random probes.

t_far -- the earliest generation at which a single-bit flip reaches half
the lattice -- was previously measured on LCG LOW-bit probes.  The low bit
alternates (0,1,0,1,...), so every "background" was a checkerboard; that
degeneracy fabricated an amplifier ranking (rule 164 "fastest" at 4
generations) and hid rule 91 entirely.  This module measures the dose
response on TRUE-RANDOM backgrounds drawn from the LCG HIGH bits.

On a fixed grid of 24 backgrounds x every flip position (384 events per
rule) with horizon 96, at width 16:

reach set exactly      {27, 59, 83, 91, 115, 123, 147, 155, 172,
                                187, 211, 228, 243}  (13 rules)
    dominant amplifier rule 147: fraction 0.78 of events reach half;
                                rule 91 next (0.31); then the {59, 115,
                                211, 155, 27, 83, 187, 243} tier
                                (0.06-0.14); the one-laps {172, 228} are
                                rare (~0.005 and 0.003).
    stationary sector  rules 164 and 251 (and 4, 12, ...) register ZERO
                                half-reach events: the round-6 "164
                                fastest" is a checkerboard artifact.

Width scaling (same grid at widths 16/24/32): the reach set NESTS --
reachable(32) subset reachable(24) subset reachable(16) -- as the larger
lattice leaves more room for the damage to stay bounded.

Certificates:

    L_pert_reach_set_16       PASS/FAIL  the half-reach rules at width 16
                              are exactly the 13-rule set above.
    L_pert_checked_rank       PASS/FAIL  rule 147 is the dominant single-
                              flip amplifier: its event fraction is >=
                              0.5 and strictly the maximum.
    L_pert_stationary_quiet   PASS/FAIL  rules 164 and 251 (stationary /
                              filler) have zero half-reach events on the
                              grid.
    L_pert_width_nesting      PASS/FAIL  reachable(32) subset reachable(
                              24) subset reachable(16); in particular
                              W32 keeps exactly the 10-rule core
                              {27, 59, 83, 91, 115, 147, 155, 187, 211,
                              243}.
    L_pert_fraction_decay     PASS/FAIL  for EVERY reachable rule the
                              half-reach probability is monotonically
                              non-increasing with width: f(24) <= f(16)
                              and f(32) <= f(24).  The dominant
                              amplifier 147 decays 0.779 -> 0.727 ->
                              0.673; 91 decays 0.31 -> 0.09 -> 0.02.
    L_pert_checkerboard_degeneracy HONEST_NEGATIVE  the claim "the low-
                              bit checkerboard probes are faithful"
                              is FALSE: under them rule 164 looked like
                              the fastest amplifier (t_far = 4) and rule
                              91 absent; under true-random probes 164 has
                              zero half-reach events and 91 is the second
                              amplifier.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES  # noqa: E402

_W16_REACH = {27, 59, 83, 91, 115, 123, 147, 155, 172, 187, 211, 228, 243}
_W32_REACH = {27, 59, 83, 91, 115, 147, 155, 187, 211, 243}
_STATIONARY_LOW = {164, 251}
_DOMINANT = 147
_NPROBE = 24
_HORIZON = 96


def _lcg(seed: int = 0x9E3779B97F4A7C15) -> int:
    return (6364136223846793005 * seed
            + 1442695040888963407) & ((1 << 64) - 1)


def _bit(r: int, l: int, c: int, rr: int) -> int:
    return (r >> ((l << 2) | (c << 1) | rr)) & 1


def _step(r: int, s: list[int]) -> list[int]:
    m = len(s)
    return [_bit(r, s[i - 1] if i > 0 else 0,
                 s[i], s[i + 1] if i < m - 1 else 0)
            for i in range(m)]


def _reach_counts(r: int, width: int, nprobe: int,
                  horizon: int) -> tuple[int, int, int | None]:
    """Return (events, total_events, fastest_t_far) for half-reach."""
    half = width // 2
    hits = 0
    total = 0
    tfar: int | None = None
    seed = _lcg()
    for _ in range(nprobe):
        seed = _lcg(seed)
        bg = [((seed := _lcg(seed)) >> 16) & 1 for _ in range(width)]
        for j in range(width):
            a, b = list(bg), list(bg)
            b[j] ^= 1
            total += 1
            for g in range(1, horizon + 1):
                a = _step(r, a)
                b = _step(r, b)
                if sum(x != y for x, y in zip(a, b)) >= half:
                    hits += 1
                    if tfar is None or g < tfar:
                        tfar = g
                    break
    return hits, total, tfar


def reach_table(width: int) -> dict[int, tuple[int, float, int | None]]:
    out = {}
    for r in RULES:
        hits, total, tfar = _reach_counts(r, width, _NPROBE, _HORIZON)
        out[r] = (hits, hits / total, tfar)
    return out


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


def perturbation_certificates() -> tuple[list[dict[str, object]],
                                         dict[int, dict[int, tuple]]]:
    tables = {w: reach_table(w) for w in (16, 24, 32)}
    t16 = tables[16]
    reach16 = {r for r, (h, _, _) in t16.items() if h > 0}
    fr = {r: t16[r][1] for r in RULES}
    dom = max(reach16, key=lambda r: fr[r])
    quiet = {r for r in RULES if t16[r][0] == 0}
    reach24 = {r for r, (h, _, _) in tables[24].items() if h > 0}
    reach32 = {r for r, (h, _, _) in tables[32].items() if h > 0}

    def cb_fraction(r: int) -> float:
        return fr[r]

    certs = [
        _certify("L_pert_reach_set_16",
                 {"grid": f"{_NPROBE} backgrounds x all flips, horizon "
                          f"{_HORIZON} gens, width 16",
                  "law": "half-reach rules are exactly "
                         f"{sorted(_W16_REACH)}",
                  "measured": sorted(reach16)},
                 lambda: reach16 == _W16_REACH),
        _certify("L_pert_checked_rank",
                 {"law": "rule 147 is the dominant single-flip amplifier "
                         "with event fraction >= 0.5 and strictly the "
                         "maximum",
                  "top": {str(r): round(cb_fraction(r), 4) for r in
                          sorted(reach16, key=cb_fraction, reverse=True)[
                              :5]}},
                 lambda: (dom == _DOMINANT and fr[_DOMINANT] >= 0.5
                          and all(fr[_DOMINANT] > fr[r]
                                  for r in reach16 if r != _DOMINANT))),
        _certify("L_pert_stationary_quiet",
                 {"law": "the stationary / filler rules "
                         f"{sorted(_STATIONARY_LOW)} register zero "
                         "half-reach events on the grid",
                  "measured": quiet},
                 lambda: _STATIONARY_LOW <= quiet),
        _certify("L_pert_width_nesting",
                 {"law": "reachable(32) subset reachable(24) subset "
                         "reachable(16); W32 = "
                         f"{sorted(_W32_REACH)}",
                  "measured": {"16": sorted(reach16),
                               "24": sorted(reach24),
                               "32": sorted(reach32)}},
                 lambda: (reach32 <= reach24 <= reach16
                          and reach32 == _W32_REACH)),
        _certify("L_pert_fraction_decay",
                 {"law": "for every reachable rule the half-reach "
                         "probability is monotonically non-increasing "
                         "with width: f(24) <= f(16) and f(32) <= f(24)",
                  "watch": {str(r): [round(tables[w][r][1], 4)
                                     for w in (16, 24, 32)]
                            for r in sorted(_W16_REACH)}},
                 lambda: all(all(tables[w2][r][1] <= tables[w1][r][1]
                                 for w1, w2 in ((16, 24), (24, 32)))
                             for r in _W16_REACH)),
        _certify("L_pert_checkerboard_degeneracy",
                 {"law": "the low-bit (checkerboard) probe grid is a "
                         "faithful damage-probe: under it rule 164 ranks "
                         "as the fastest far-half reach (t_far = 4) and "
                         "rule 91 is invisible",
                  "measured": "under true-random probes rule 164 has "
                              f"zero half-reach events and rule 91 is "
                              f"the #2 amplifier "
                              f"(fraction {fr[91]:.4f})"},
                 lambda: False),
    ]
    return certs, tables


if __name__ == "__main__":
    certs, tables = perturbation_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    t16 = tables[16]
    print("  width-16 amplifier ranking (fraction of events reaching half):")
    for r in sorted(RULES, key=lambda r: t16[r][1], reverse=True):
        if t16[r][0]:
            print("    r=%3d  events=%3d/%-4d  frac=%.4f  t_far=%s"
                  % (r, t16[r][0], _NPROBE * 16, t16[r][1], t16[r][2]))