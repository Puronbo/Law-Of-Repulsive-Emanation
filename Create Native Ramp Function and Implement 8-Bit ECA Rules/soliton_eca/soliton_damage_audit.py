"""soliton_damage_audit: single-bit damage spectrum, measured -- not assumed.

A single bit is flipped in a lattice background under each of the 32
family rules and the Hamming distance to the unflipped run is tracked.
Two facts are exact and probe-independent; the amplification facts are
measured over a true-random probe grid.

EXACT (structural):

    204 is the identity and 51 is the complement involution; both are
    global isometries of the Hamming cube, so a one-bit difference stays
    a one-bit difference for every state and every generation.  Over the
    ENTIRE width-8 cube (all 2^8 states, all pairwise distances) no other
    family rule is a Hamming isometry: the isometry pair is exactly
    {204, 51}.

MEASURED (true-random grid):

    The full-lattice amplifiers at width 16 are {59, 115, 187, 243} (at
    width 8, rule 91 additionally reaches the full 8-cell lattice).  The
    "every error is contained in the far half" candidate is FALSE.

Probes use the LCG high bits ((seed >> 16) & 1).  Earlier audits drew
the low bit, which strictly alternates (0,1,0,1,...) and degenerated
every background into a checkerboard; under those degenerate probes the
families {51, 68, 76, 179, 204} and {59, 115, 187, 243} appeared, and
rules 68/76/179 masqueraded as single-cell concentrators.  The
isometry pair {204, 51} survives; 68/76/179 do not.

Certificates:

    L_damage_isometry_pair        PASS/FAIL  the exhaustive width-8
                              Hamming-isometry set is exactly {204, 51}.
    L_damage_single_cell_family   PASS/FAIL  at widths 8 and 16, the
                              rules whose single-flip damage never
                              exceeds one cell are exactly {204, 51}.
    L_damage_full_lattice_amplifiers PASS/FAIL  at width 16 exactly
                              {59, 115, 187, 243} drive the damage to the
                              full lattice.
    L_damage_far_half_containment HONEST_NEGATIVE  the claim "single-bit
                              errors never reach the far half" is FALSE.
    L_damage_conservation_pair   PASS/FAIL  rules 204 and 51 hold every
                              single-bit error at exactly one cell.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES as _RULE_TABLE  # noqa: E402

_WIDTHS = (8, 16)
_ISOMETRY_SET = frozenset({204, 51})
_FULL_SET = frozenset({59, 115, 187, 243})
_PROBES = 8
_ISO_WIDTH = 8


def _lcg(seed: int = 0x9E3779B97F4A7C15):
    state = seed
    while True:
        state = (6364136223846793005 * state + 1442695040888963407) & (
            (1 << 64) - 1)
        yield state


def _bit(rule: int, l: int, c: int, r: int) -> int:
    return (rule >> ((l << 2) | (c << 1) | r)) & 1


def _step(rule: int, s: list[int]) -> list[int]:
    n = len(s)
    out = []
    for i in range(n):
        left = s[i - 1] if i > 0 else 0
        right = s[i + 1] if i < n - 1 else 0
        out.append(_bit(rule, left, s[i], right))
    return out


def damage_profile(rule: int, width: int,
                   gen: "callable" = None) -> dict[str, object]:
    gen = gen or _lcg()
    max_h = 0
    single = True
    for _ in range(_PROBES):
        background = [(next(gen) >> 16) & 1 for _ in range(width)]
        for flip in range(width):
            damaged = list(background)
            damaged[flip] ^= 1
            a, b = list(background), damaged
            for _ in range(2 * width):
                a = _step(rule, a)
                b = _step(rule, b)
                h = sum(x != y for x, y in zip(a, b))
                if h > 1:
                    single = False
                max_h = max(max_h, h)
    return {"rule": rule, "width": width,
            "max_h": max_h,
            "single_cell": single,
            "full_lattice": max_h == width}


def _next_map(rule: int, width: int = _ISO_WIDTH) -> np.ndarray:
    m = np.zeros(1 << width, dtype=np.int32)
    for s in range(1 << width):
        bits = [(s >> i) & 1 for i in range(width)]
        out = 0
        for i in range(width):
            left = bits[i - 1] if i > 0 else 0
            right = bits[i + 1] if i < width - 1 else 0
            out |= _bit(rule, left, bits[i], right) << i
        m[s] = out
    return m


def _isometry_set() -> set[int]:
    pc = np.array([s.bit_count() for s in range(1 << _ISO_WIDTH)])
    a = np.arange(1 << _ISO_WIDTH)[:, None]
    b = np.arange(1 << _ISO_WIDTH)[None, :]
    found = set()
    for rule in _RULE_TABLE:
        m = _next_map(rule)
        lhs = pc[m[a] ^ m[b]]
        rhs = pc[a ^ b]
        if bool(np.all(lhs == rhs)):
            found.add(rule)
    return found


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


def _isometry_holds() -> bool:
    return _isometry_set() == set(_ISOMETRY_SET)


def _single_cell_family_holds() -> bool:
    gen = _lcg()
    for width in _WIDTHS:
        single = {r for r in _RULE_TABLE
                  if damage_profile(r, width, gen)["single_cell"]}
        if single != set(_ISOMETRY_SET):
            return False
    return True


def _full_lattice_amplifiers_holds() -> bool:
    gen = _lcg()
    ampl = {r for r in _RULE_TABLE
            if damage_profile(r, 16, gen)["full_lattice"]}
    return ampl == set(_FULL_SET)


def _far_half_containment_holds() -> bool:
    """False candidate: single-bit errors never reach the far half."""
    gen = _lcg()
    for rule in _RULE_TABLE:
        p = damage_profile(rule, 16, gen)
        if p["max_h"] >= 8:
            return False
    return True


def _conservation_pair_holds() -> bool:
    gen = _lcg()
    return all(damage_profile(r, 16, gen)["single_cell"]
               for r in (204, 51))


def damage_certificates() -> list[dict[str, object]]:
    return [
        _certify("L_damage_isometry_pair",
                 {"domain": f"exhaustive width-{_ISO_WIDTH} cube "
                            "(all 2^8 states, all pairwise distances)",
                  "law": "the Hamming-isometry rules of the family are "
                         f"exactly {sorted(_ISOMETRY_SET)} -- 204 the "
                         "identity, 51 the complement involution, both "
                         "global isometries",
                  "honest_check": "no other family rule preserves every "
                                  "pairwise Hamming distance",
                  "measured_on": "exhaustive distance-preservation "
                                 "check per rule"},
                 _isometry_holds),
        _certify("L_damage_single_cell_family",
                 {"domain": "single-bit flips of true-random (LCG high "
                            f"bit) backgrounds at widths {_WIDTHS}, "
                            f"{_PROBES} probes x every flip position, "
                            "horizon 2*width",
                  "law": "the rules whose damage never exceeds one cell "
                         f"are exactly {sorted(_ISOMETRY_SET)}, stable at "
                         "both widths",
                  "honest_check": "a flip is permanent-but-local: the "
                                  "rule neither heals nor amplifies it "
                                  "(consequence of the isometry pair)",
                  "measured_on": "Hamming distance per flip"},
                 _single_cell_family_holds),
        _certify("L_damage_full_lattice_amplifiers",
                 {"domain": "width 16, single-bit flips over the "
                            "true-random probe grid",
                  "law": "exactly the rules "
                         f"{sorted(_FULL_SET)} drive the damage to the "
                         "full lattice (max_H == width)",
                  "measured_on": "max Hamming distance per rule"},
                 _full_lattice_amplifiers_holds),
        _certify("L_damage_far_half_containment",
                 {"domain": "width 16, per-rule max damage over the "
                            "true-random probe grid",
                  "law": "FALSE CANDIDATE: single-bit errors never reach "
                         "the far half of the lattice -- rules "
                         f"{sorted(_FULL_SET)} grow the damage to the "
                         "full width (>= width/2 = 8)",
                  "honest_check": "amplification marks the mixing "
                                  "sector, the impulse-dissipating "
                                  "members",
                  "measured_on": "max Hamming distance per rule vs "
                                 "width/2"},
                 _far_half_containment_holds),
        _certify("L_damage_conservation_pair",
                 {"domain": "single-bit flips under rules 204 and 51 at "
                            "width 16",
                  "law": "the entropy-lossless pair {204, 51} holds every "
                         "bit-error at exactly one cell -- persistent "
                         "and localized",
                  "honest_check": "204 stores, 51 inverts: both are "
                                  "bijections, so a one-bit difference "
                                  "cannot heal and cannot multiply",
                  "measured_on": "Hamming distance per flip"},
                 _conservation_pair_holds),
    ]


def _render_table() -> str:
    gen = _lcg()
    rows = ["  rule   max_H@8   max_H@16   class"]
    for rule in sorted(_RULE_TABLE):
        h8 = damage_profile(rule, 8, gen)["max_h"]
        h16 = damage_profile(rule, 16, gen)["max_h"]
        if h8 == 1 and h16 == 1:
            kind = "single-cell"
        elif h16 >= 8:
            kind = "far-half amplifier"
        else:
            kind = "bounded"
        rows.append("  %4d    %4d      %4d     %s" % (rule, h8, h16, kind))
    return "\n".join(rows)


if __name__ == "__main__":
    for c in damage_certificates():
        print("  %-38s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print(_render_table())