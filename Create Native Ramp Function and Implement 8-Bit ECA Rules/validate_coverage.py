import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import evaluate_coverage, require_coverage

measured = [(-2.0, 0.0), (-1.0, 0.1), (0.0, 0.5), (1.0, 0.9), (2.0, 1.4)]
in_domain = evaluate_coverage(measured, (-1.5, 1.5))
assert in_domain.covered
assert in_domain.extrapolation_distance == 0.0
require_coverage(in_domain)

out_domain = evaluate_coverage(measured, (-3.0, 1.5))
assert not out_domain.covered
assert out_domain.extrapolation_distance == 1.0
try:
    require_coverage(out_domain)
except ValueError:
    pass
else:
    raise AssertionError('out-of-domain calibration was accepted')
require_coverage(out_domain, allow_extrapolation=True)

gappy = evaluate_coverage([(-2.0, 0.0), (0.0, 0.5), (2.0, 1.4)], (-2.0, 2.0), max_internal_gap=1.0)
assert not gappy.covered
print('coverage validation passed')
print(in_domain)
print(out_domain)
print(gappy)
