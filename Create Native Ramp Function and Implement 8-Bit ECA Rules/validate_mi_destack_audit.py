import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca.soliton_mi_destack_audit import (  # noqa: E402
    _SHED_FRAC,
    _SUB,
    destack_certificates,
)

certs, stacks = destack_certificates()
status = {c["label"]: c["status"] for c in certs}
assert status["L_dst_sheds"] == "PASS"
assert status["L_dst_submajority"] == "PASS"
assert status["L_dst_fund_persist"] == "PASS"
assert status["L_dst_monotone_de"] == "HONEST_NEGATIVE"

for e in stacks:
    assert stacks[e][1] / stacks[e][0] <= _SHED_FRAC
    assert stacks[e][-1] < _SUB
finite = [e for e in stacks if stacks[e]]
assert max(stacks[e][-1] for e in finite) < _SUB
assert any(a < b for e in stacks
           for a, b in zip(stacks[e], stacks[e][1:]))

print("mi de-stacking audit validation passed")