import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_radiation_audit import (  # noqa: E402
    radiation_certificates, radiation_delta, phase_deviation,
)

status = {c["label"]: c["status"] for c in radiation_certificates()}
assert status["L_radiation_fundamental_clean"] == "PASS"
assert status["L_radiation_integral_solitons"] == "PASS"
assert status["L_radiation_phase_exact"] == "PASS"
assert status["L_radiation_monotone_vs_N"] == "HONEST_NEGATIVE"

assert radiation_delta(1.0) < 1e-3
assert radiation_delta(2.0) < 1e-3
assert radiation_delta(0.5) > 0.1
assert radiation_delta(1.5) > radiation_delta(2.0)
assert phase_deviation(1.0) > max(phase_deviation(a) for a in (0.5, 1.5, 2.0))

print("radiation audit validation passed")