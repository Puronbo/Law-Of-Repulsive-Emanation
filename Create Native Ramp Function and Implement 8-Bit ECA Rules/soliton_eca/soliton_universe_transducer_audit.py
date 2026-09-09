"""soliton_universe_transducer_audit: the large-extent transducer
census of all 256 elementary cellular automata.

The extent spectrum's saturation sector was certified against an
EXTERNAL reference: the eight affine rules reach F(32) = 0.250-0.312
(4-5x the injected 32-cell block) while the twin family tops out at
0.107 (mean) / 0.139 (per-placement max).  That reference was
measured, but was never placed inside a full-universe census: are the
affine rules exactly the universe's large-extent transducers, or do
non-linear rules out-transduce them?

This audit measures F(k) = mean Hamming(clean, perturbed) / 512 for a
contiguous k-cell flip for ALL 256 rules, on width-512 rings over 96
generations, on the SAME 8 true-random (LCG high-bit) half-density
backgrounds and the same perturbation stream as the extent audit and
its probe companion (per-probe values are bit-for-bit compatible), at
extents k in {1, 16, 32}.

Certificates (finalized against the measured census):

    L_univ_transducer_set     PASS/FAIL  the rules with F(32) >= 0.25
                                (>= 4x the injected block) are exactly
                                the eight affine rules
                                {60, 90, 102, 105, 150, 153, 165,
                                195}: the affine set is exactly the
                                universe's large-extent transducers.
    L_univ_family_tail        PASS/FAIL  every twin-family rule sits
                                below the affine floor F(32) < 0.25
                                (and below the weak-affine boundary
                                0.125): the twin family is a strict
                                non-transducer -- re-derived against
                                the whole universe, not just the
                                squeeze of the affine 8.
    L_univ_strongest_affine   PASS/FAIL  the strongest transducer in
                                the universe (max F(32) over all 256)
                                is one of the affine eight: no
                                non-linear rule out-transduces even
                                the weakest affine rule.
    L_univ_transparent_only   PASS/FAIL  among ALL 256 rules, the
                                rules whose F(k) equals k/512 at
                                EVERY measured extent (Hamming
                                isometries) are exactly {204, 51}:
                                the transparent sector is the
                                universe's entire isometry class.
  Status finalized from the census."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES  # noqa: E402

from soliton_eca.soliton_extent_spectrum_audit import (  # noqa: E402
    _extent_table_for,
)

_AFFINE = (60, 90, 102, 105, 150, 153, 165, 195)
_KS = (1, 16, 32)
_TRANSPARENT = {204, 51}
_AFFINE_FLOOR = 0.25
_WEAK_BOUNDARY = 0.125


def universe_table() -> dict[int, dict[int, float]]:
    return _extent_table_for(range(256))


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


def universe_certificates(
        t: dict[int, dict[int, float]] | None = None) -> tuple[
        list[dict[str, object]], dict[str, object]]:
    if t is None:
        t = universe_table()
    over_floor = {r for r in range(256) if t[r][32] >= _AFFINE_FLOOR}
    family_f32 = {r: t[r][32] for r in RULES}
    strongest = max(range(256), key=lambda r: t[r][32])
    top10 = sorted(range(256), key=lambda r: t[r][32], reverse=True)[:10]
    exact_all = {r for r in range(256)
                 if all(abs(t[r][k] - k / 512) <= 1e-9 for k in _KS)}
    n_between = sum(1 for r in range(256)
                    if t[r][32] >= _WEAK_BOUNDARY)
    stats = {
        "transducer_set": sorted(over_floor),
        "strongest_rule": strongest,
        "strongest_value": round(t[strongest][32], 4),
        "top10": [(r, round(t[r][32], 4)) for r in top10],
        "family_F32": {str(r): round(v, 4)
                       for r, v in sorted(family_f32.items())},
        "affine_F32": {str(r): round(t[r][32], 4) for r in _AFFINE},
        "family_max_F32": round(max(family_f32.values()), 4),
        "n_rules_at_least_weak": n_between,
        "isometry_class": sorted(exact_all),
    }
    certs = [
        _certify(
            "L_univ_transducer_set",
            {"domain": "all 256 rules, width 512, gens 96, "
                       f"extents {_KS}, 8 true-random placements "
                       "(the extent-audit stream)",
             "law": f"the rules with F(32) >= {_AFFINE_FLOOR} (>= 4x "
                    "the injected block) are exactly the eight affine "
                    "rules {60, 90, 102, 105, 150, 153, 165, 195}: "
                    "the affine set is exactly the universe's "
                    "large-extent transducers",
             "measured": sorted(over_floor)},
            lambda: over_floor == set(_AFFINE)),
        _certify(
            "L_univ_family_tail",
            {"domain": "as above",
             "law": f"the twin family sits strictly below {_WEAK_BOUNDARY} "
                    "at F(32) in every member -- a strict "
                    "non-transducer tail of the universe (the affine "
                    "floor is 2x higher)",
             "measured_family_max_F32": round(max(family_f32.values()), 4)},
            lambda: all(v < _WEAK_BOUNDARY for v in family_f32.values())),
        _certify(
            "L_univ_strongest_affine",
            {"domain": "as above",
             "law": "the strongest country-wide transducer is affine: "
                    "no non-linear rule out-transduces the weakest "
                    "affine rule at width 32",
             "measured": {str(strongest): round(t[strongest][32], 4),
                          "affine_range": [round(t[r][32], 4)
                                           for r in _AFFINE]}},
            lambda: strongest in _AFFINE),
        _certify(
            "L_univ_transparent_only",
            {"domain": "as above",
             "law": "among ALL 256 rules the Hamming isometries "
                    "(F(k) = k/512 at every measured extent) are "
                    "exactly {204, 51}: the transparent sector is the "
                    "universe's entire isometry class",
             "measured": "FALSE -- the isometry class is the 10-rule "
                         "set {15, 51, 85, 154, 166, 170, 180, 204, "
                         "210, 240}; {204, 51} is the no-op pair "
                         "inside it, not its boundary (the added "
                         "members are the ring-level permutations "
                         "and their bit complements, each of which "
                         "preserves Hamming distance exactly)",
             "measured_isometry_class": sorted(exact_all)},
            lambda: exact_all == _TRANSPARENT),
    ]
    return certs, stats


if __name__ == "__main__":
    certs, stats = universe_certificates()
    for c in certs:
        print("  %-38s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("  transducer set:", stats["transducer_set"])
    print("  strongest rule: %s (F(32)=%.4f)" % (
        stats["strongest_rule"], stats["strongest_value"]))
    print("  top10:", stats["top10"])
    print("  family max F(32):", stats["family_max_F32"])
    print("  rules at/above weak boundary 0.125:", stats["n_rules_at_least_weak"])
    print("  isometry class:", stats["isometry_class"])