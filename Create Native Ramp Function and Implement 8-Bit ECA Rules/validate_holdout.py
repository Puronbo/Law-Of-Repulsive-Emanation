import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import holdout_passes, holdout_report, leave_one_input_out, require_holdout

stable = []
for x, y in [(0.0, 1.0), (1.0, 3.0), (2.0, 5.0), (3.0, 7.0), (4.0, 9.0)]:
    stable.extend(((x, y), (x, y)))
report = leave_one_input_out(stable, saturation=20.0)
assert report.normalized_max_error == 0.0
assert holdout_passes(report, max_normalized_error=0.0)
require_holdout(report, max_normalized_error=0.0)
assert 'Absolute error' in holdout_report(report)

misspecified = []
for x, y in [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0), (3.0, 9.0), (4.0, 16.0)]:
    misspecified.extend(((x, y), (x, y)))
bad = leave_one_input_out(misspecified, saturation=20.0)
assert bad.normalized_max_error > 0.25
try:
    require_holdout(bad, max_normalized_error=0.25)
except ValueError:
    pass
else:
    raise AssertionError('misspecified calibration passed holdout gate')
print('holdout validation passed')
print(holdout_report(report))
print(holdout_report(bad))
