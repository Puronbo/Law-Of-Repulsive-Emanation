import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_mi_omega_spectrum_audit import (  # noqa: E402
    _CAP,
    _EPS,
    _HIGH_SET,
    _LOW_SET,
    _OMEGA_GRID,
    _RELAX_FACTOR,
    omegaspectrum_certificates,
    omegaspectrum_measurements,
)

certs, m = omegaspectrum_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_omega_crest_wavelength_monotone"] == "PASS"
assert status["L_omega_crest_after_monotone"] == "PASS"
assert status["L_omega_cap_division"] == "PASS"
assert status["L_omega_recurrence_holds"] == "PASS"
assert status["L_omega_dc_turnback"] == "HONEST_NEGATIVE"

oms = [o for o, _ in _OMEGA_GRID]
crests = [m[o]["crest"] for o in oms]
assert all(a > b for a, b in zip(crests, crests[1:]))
sub = [o for o in oms if o <= 1.0]
zc = [m[o]["crest_z"] for o in sub]
assert all(a > b for a, b in zip(zc, zc[1:]))
assert min(m[o]["crest"] for o in _LOW_SET) > _CAP
assert max(m[o]["crest"] for o in _HIGH_SET) < _CAP
for o in oms:
    assert m[o]["trough_after"] <= _RELAX_FACTOR * (1 + _EPS)
assert m[min(oms)]["crest"] > m[float(2 ** 0.5)]["crest"]

print("mi omega spectrum audit validation passed")