import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES  # noqa: E402
from soliton_eca.soliton_universe_transducer_audit import (  # noqa: E402
    _AFFINE,
    _AFFINE_FLOOR,
    _KS,
    _WEAK_BOUNDARY,
    universe_certificates,
    universe_table,
)

certs, stats = universe_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_univ_transducer_set"] == "PASS"
assert status["L_univ_family_tail"] == "PASS"
assert status["L_univ_strongest_affine"] == "PASS"
assert status["L_univ_transparent_only"] == "HONEST_NEGATIVE"

t = universe_table()

over_floor = {r for r in range(256) if t[r][32] >= _AFFINE_FLOOR}
assert over_floor == set(_AFFINE)

assert max(t[r][32] for r in RULES) < _WEAK_BOUNDARY
strongest = max(range(256), key=lambda r: t[r][32])
assert strongest in _AFFINE
assert t[strongest][32] >= 0.25

exact_all = {r for r in range(256)
             if all(abs(t[r][k] - k / 512) <= 1e-9 for k in _KS)}
assert exact_all != {204, 51}
assert {204, 51} <= exact_all
assert len(exact_all) == 10
assert max(t[r][32] for r in range(256)) >= 0.25

print("universe transducer audit validation passed")