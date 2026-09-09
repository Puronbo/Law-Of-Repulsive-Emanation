import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_mi_frequency_scan_audit import (  # noqa: E402
    _CAP,
    _EPS,
    _OMEGA_SET,
    _RELAX_FACTOR,
    freqscan_certificates,
    freqscan_measurements,
)

certs, m = freqscan_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_freq_crest_overtakes"] == "HONEST_NEGATIVE"
assert status["L_freq_cap_near_max"] == "PASS"
assert status["L_freq_crest_grows_low"] == "PASS"
assert status["L_freq_relaxes_back"] == "PASS"

assert m[0.5]["crest"] >= _CAP
assert m[0.5]["crest"] > m[1.0]["crest"] > m[float(2 ** 0.5)]["crest"]
for o in _OMEGA_SET:
    assert m[o]["trough_after"] <= _RELAX_FACTOR * (1 + _EPS)

print("mi frequency scan audit validation passed")