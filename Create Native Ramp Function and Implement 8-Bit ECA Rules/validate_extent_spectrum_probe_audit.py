import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_eca import RULES  # noqa: E402
from soliton_eca.soliton_extent_spectrum_audit import _KS, _PROBES, _WIDTH  # noqa: E402
from soliton_eca.soliton_extent_spectrum_probe_audit import (  # noqa: E402
    _ERS,
    _TRAN,
    extent_probe_certificates,
    extent_probe_table,
)

certs, stats = extent_probe_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_es_transparent_placewise"] == "PASS"
assert status["L_es_erasers_family_exhaust"] == "PASS"
assert status["L_es_eraser_251_absolute"] == "PASS"
assert status["L_es_erasers_triple_placewise"] == "HONEST_NEGATIVE"
assert status["L_es_saturation_placewise"] == "PASS"

acc = extent_probe_table()

for r in _TRAN:
    for k in _KS:
        for p in range(_PROBES):
            assert abs(acc[r][k][p] - k / _WIDTH) <= 1 / _WIDTH

for r in RULES:
    for p in range(_PROBES):
        if all(acc[r][k][p] <= 0.005 for k in _KS):
            assert r in _ERS

for k in _KS:
    for p in range(_PROBES):
        assert acc[251][k][p] == 0.0

per_probe_sets = [
    {r for r in RULES if all(acc[r][k][p] <= 0.005 for k in _KS)}
    for p in range(_PROBES)]
assert all(ps == _ERS for ps in per_probe_sets) is False

for r in RULES:
    for p in range(_PROBES):
        assert acc[r][32][p] < 0.250

print("extent spectrum probe audit validation passed")