import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_mi_retention_mechanism_audit import (  # noqa: E402
    _EPSES,
    _OMEGAS,
    retention_certificates,
    retention_table,
)

certs, stats = retention_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_ret_migration"] == "PASS"
assert status["L_ret_band_amplitude"] == "PASS"
assert status["L_ret_closure_resonance"] == "HONEST_NEGATIVE"
assert status["L_ret_rel1_insufficient"] == "HONEST_NEGATIVE"
assert status["L_ret_amplitude_bounces"] == "HONEST_NEGATIVE"

table = retention_table()


def best_of(row):
    cand = {k: v for k, v in row.items() if v is not None}
    return max(cand, key=lambda k: cand[k]["p0"]) if cand else None


mig = {om: {e: best_of(table[(om, e)]) for e in _EPSES}
       for om in _OMEGAS}
assert mig[1.0][0.20] == "p4"
assert mig[1.0][0.30] == "p0"
assert mig[1.0][0.45] == "p2"

best_p0 = {om: {e: table[(om, e)][mig[om][e]]["p0"] for e in _EPSES}
           for om in _OMEGAS}
for e in _EPSES:
    assert best_p0[0.5][e] > best_p0[1.0][e]
assert best_p0[0.5][0.30] > 0.45

amp1 = [best_p0[1.0][e] for e in _EPSES]
assert not (amp1[0] < amp1[1] < amp1[2]
            or amp1[0] > amp1[1] > amp1[2])

for (om, e), row in table.items():
    cand = {k: v for k, v in row.items()
            if v is not None and v["p0"] > 0}
    if not cand:
        continue
    best = max(cand, key=lambda k: cand[k]["p0"])
    assert any(abs(v["delta"]) < abs(cand[best]["delta"])
               for k, v in cand.items() if k != best)

for (om, e), row in table.items():
    cand = {k: v for k, v in row.items() if v is not None}
    if len(cand) >= 3:
        others = sorted(cand.values(), key=lambda v: v["rel1"])
        assert any(others[i]["p0"] > others[i + 1]["p0"]
                   for i in range(len(others) - 1))

print("mi retention mechanism audit validation passed")