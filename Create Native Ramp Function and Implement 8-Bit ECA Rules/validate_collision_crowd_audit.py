import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_collision_crowd_audit import (  # noqa: E402
    _B_SECOND,
    _B_THIRD,
    _CORE_CEIL,
    _FAR_FLOOR,
    _ISOMETRIES,
    crowd_certificates,
)

certs, f = crowd_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_crowd_isometry_additive"] == "PASS"
assert status["L_crowd_core_demand"] == "PASS"
assert status["L_crowd_far_lands"] == "PASS"
assert status["L_crowd_all_additive"] == "HONEST_NEGATIVE"

for r in _ISOMETRIES:
    assert f[r]["f3"] == 3 * f[r]["f1"]
assert f[251]["f3"] == 0.0 and f[251]["f1"] == 0.0
additive = {r for r, d in f.items()
            if abs(d["f3"] - 3 * d["f1"]) <= 1e-9}
assert additive == {204, 51, 251}

f147 = f[147]
assert f147["f2"] <= _CORE_CEIL * f147["f1"]
assert (f147["f3"] - f147["f2"]) >= _FAR_FLOOR * f147["f1"]
assert abs(f147["f2"] - 2 * f147["f1"]) > 1e-9
assert f147["f3"] > 3 * f147["f1"] / 2

print("collision crowd audit validation passed")