import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_damage_contraction_rate_audit import (  # noqa: E402
    _EARLY_FLOOR,
    _EARLY_WINDOW,
    _GRID,
    _MATURE_CEIL,
    _MATURE_WINDOWS,
    _OPEN_WINDOW,
    _SUSTAINED_PEAK,
    contraction_certificates,
)

certs, tab = contraction_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_ca_accel"] == "PASS"
assert status["L_ca_open_drop"] == "PASS"
assert status["L_ca_sustained_peak"] == "PASS"
assert status["L_ca_every_gen_fall"] == "HONEST_NEGATIVE"

early = tab[_EARLY_WINDOW[1]] / tab[_EARLY_WINDOW[0]]
assert early >= _EARLY_FLOOR
for w in _MATURE_WINDOWS:
    assert tab[w[1]] / tab[w[0]] <= _MATURE_CEIL
slopes = []
for ga, gb in zip(_GRID, _GRID[1:]):
    slopes.append((ga, gb, abs(__import__("numpy").log(tab[gb])
                                - __import__("numpy").log(tab[ga]))
                   / (gb - ga)))
peak = max(slopes, key=lambda s: s[2])
assert peak[0] == _OPEN_WINDOW[0] and peak[1] == _OPEN_WINDOW[1]
sust = [s for s in slopes if s[0] >= 12]
peak_s = max(sust, key=lambda s: s[2])
assert peak_s[0] == _SUSTAINED_PEAK[0] and peak_s[1] == _SUSTAINED_PEAK[1]
vals = [tab[g] for g in _GRID]
assert vals[2] > vals[1]

print("damage contraction rate audit validation passed")