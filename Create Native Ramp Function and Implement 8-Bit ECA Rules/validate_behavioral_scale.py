import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_behavioral_scale import (  # noqa: E402
    scale_certificates, profile,
)

status = {c["label"]: c["status"] for c in scale_certificates()}
assert status["L_scale_reproduces_census"] == "PASS"
assert status["L_scale_deterministic"] == "PASS"
assert status["L_scale_class_probe_insensitive"] == "HONEST_NEGATIVE"
assert status["L_scale_class_stable"] == "HONEST_NEGATIVE"

# Pin the documented probe-sensitivity finding: rule 108 flips between the
# two Bernoulli samplers at (width 10, density 0.5).
high_bits = profile(108, 10, 0.5, high_bits=True)
threshold = profile(108, 10, 0.5)
assert high_bits["class"] == "static" and threshold["class"] == "oscillatory"

# Pin the documented width/density anomaly: rule 76 reads conservative only
# at (width 10, density 0.1) with the threshold sampler.
assert profile(76, 10, 0.1)["class"] == "conservative"
assert all(profile(76, w, d)["class"] == "static"
           for w in (8, 12, 16, 24) for d in (0.1, 0.25, 0.5))

print("behavioral-scale validation passed")