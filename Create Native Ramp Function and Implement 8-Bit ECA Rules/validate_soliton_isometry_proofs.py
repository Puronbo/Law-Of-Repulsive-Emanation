"""validate_soliton_isometry_proofs: independent re-derivation.

Does NOT trust isometry_proof_certificates(): it re-implements every
exhaustive check with its own copies of the ring evolution, distance,
affineness, bijectivity, and input-dependence routines, re-classifies
all 256 rules, and re-checks the declared theorem certificates'
live statuses against an independently redeclared expectation list.

Independently re-derived facts:

  - rule 204 is the identity map (truth table returns the center);
  - rule 51 is the bitwise complement;
  - the GF(2)-affine class of the width-8 ring is the 16 low-degree
    rules {0, 15, 51, 60, 85, 90, 102, 105, 150, 153, 165, 170, 195,
    204, 240, 255};
  - the large-extent transducer set measured by the universe census is
    exactly the multi-input part of that class (the four 2-/3-input
    XOR rules 60/90/102/150 and their complements 165/105/153/195);
  - the exact Hamming-isometry class of the ring is the six rotations
    {15, 51, 85, 170, 204, 240};
  - the census's four extras {154, 166, 180, 210} are neither exact
    isometries at width 8 nor width-8 bijections, and are bijections
    exactly for odd ring widths (verified widths 6..14);
  - inside the twin family the isometry class reduces to {204, 51};
  - the affine sector partitions into constants / single-input
    rotations (isometries) / multi-input rules (transducers), with the
    four extras non-affine outsiders.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES  # noqa: E402

from soliton_eca.soliton_isometry_proofs import (  # noqa: E402
    isometry_proof_certificates,
)

_AFFINE16 = {0, 15, 51, 60, 85, 90, 102, 105, 150, 153, 165, 170, 195,
             204, 240, 255}
_TRANSDUCER8 = {60, 90, 102, 105, 150, 153, 165, 195}
_ISO6 = {15, 51, 85, 170, 204, 240}
_EXTRAS = (154, 166, 180, 210)
_CONSTANTS = {0, 255}
_W = 8

_EXPECTED = {
    "L_iso_204_identity": "PASS",
    "L_iso_51_complement": "PASS",
    "L_iso_pair_isometries": "PASS",
    "L_iso_affine_sector": "PASS",
    "L_iso_transducer_affine": "PASS",
    "L_iso_class_six": "PASS",
    "L_iso_class_contains_pair": "PASS",
    "L_iso_four_not_exact": "PASS",
    "L_iso_four_parity": "PASS",
    "L_iso_family_pair": "PASS",
    "L_iso_partition": "PASS",
}


def _bit(rule: int, i: int) -> int:
    return (rule >> i) & 1


def _evolve_ring(rule: int, cfg: int, w: int) -> int:
    out = 0
    for i in range(w):
        left = (cfg >> ((i - 1) % w)) & 1
        mid = (cfg >> i) & 1
        right = (cfg >> ((i + 1) % w)) & 1
        idx = (left << 2) | (mid << 1) | right
        out |= _bit(rule, idx) << i
    return out


def _dist(x: int, y: int) -> int:
    return bin(x ^ y).count("1")


def _is_isometry(rule: int, w: int) -> bool:
    for x in range(1 << w):
        ex = _evolve_ring(rule, x, w)
        for y in range(1 << w):
            if _dist(ex, _evolve_ring(rule, y, w)) != _dist(x, y):
                return False
    return True


def _is_bij(rule: int, w: int) -> bool:
    seen: set[int] = set()
    for x in range(1 << w):
        y = _evolve_ring(rule, x, w)
        if y in seen:
            return False
        seen.add(y)
    return True


def _is_affine(rule: int, w: int) -> bool:
    ref: int | None = None
    for x in range(1 << w):
        for y in range(1 << w):
            v = (_evolve_ring(rule, x, w) ^ _evolve_ring(rule, y, w)
                 ^ _evolve_ring(rule, x ^ y, w)) & ((1 << w) - 1)
            if ref is None:
                ref = v
            elif v != ref:
                return False
    return True


def _n_inputs(rule: int) -> int:
    deps = 0
    for k in range(3):
        for i in range(8):
            if _bit(rule, i) != _bit(rule, i ^ (1 << k)):
                deps += 1
                break
    return deps


# ---- live statuses against the independent expectation list ----
certs, _ = isometry_proof_certificates()
assert len(certs) == 11
for c in certs:
    assert c["label"] in _EXPECTED
    assert c["status"] == _EXPECTED[c["label"]], (
        c["label"], c["status"], _EXPECTED[c["label"]])
    assert ("asserted" in c and "negated" in c and
            c["asserted"] != c["negated"])

# ---- independent re-derivation ----
assert all(_bit(204, i) == ((i >> 1) & 1) for i in range(8))
assert all(_bit(51, i) == 1 - ((i >> 1) & 1) for i in range(8))

affine_found = {r for r in range(256) if _is_affine(r, _W)}
assert affine_found == _AFFINE16, sorted(affine_found ^ _AFFINE16)

trans_found = {r for r in affine_found if _n_inputs(r) >= 2}
assert trans_found == _TRANSDUCER8

iso_found = {r for r in range(256) if _is_isometry(r, _W)}
assert iso_found == _ISO6, sorted(iso_found ^ _ISO6)
assert {204, 51} <= iso_found

for r in _EXTRAS:
    assert not _is_isometry(r, _W)
    assert not _is_bij(r, _W)
    for w in range(6, 15):
        assert _is_bij(r, w) == (w % 2 == 1), (r, w)

assert set(RULES) & iso_found == {204, 51}

assert _ISO6 <= _AFFINE16
assert _AFFINE16 - _CONSTANTS == _ISO6 | _TRANSDUCER8  # disjoint union
assert not (_ISO6 & _TRANSDUCER8)
assert not (set(_EXTRAS) & _AFFINE16)
assert all(_n_inputs(r) == 0 for r in _CONSTANTS)
assert all(_n_inputs(r) == 1 for r in _ISO6)
assert all(_n_inputs(r) >= 2 for r in _TRANSDUCER8)

print("soliton isometry proofs validation passed")