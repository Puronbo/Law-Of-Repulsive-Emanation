import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import QualityGate, aggregate_replicates, calibrate_replicates, replicate_report

stable = []
for x, y in [(-2.0, 0.05), (-1.0, 0.10), (0.0, 0.52), (1.0, 0.95), (2.0, 1.40)]:
    stable.extend(((x, y), (x, y + 0.005)))
report = calibrate_replicates(stable, saturation=2.0, max_relative_std=0.02)
assert len(report.points) == 5
assert report.quality.passed
assert report.max_relative_std < 0.02
assert 'PASS' in replicate_report(report)

unstable = []
for x, y in [(-2.0, 0.05), (-1.0, 0.10), (0.0, 0.52), (1.0, 0.95), (2.0, 1.40)]:
    unstable.extend(((x, y - 0.25), (x, y + 0.25)))
bad = calibrate_replicates(unstable, saturation=2.0, max_relative_std=0.02)
assert not bad.quality.passed
assert any('replicate std' in reason for reason in bad.quality.reasons)
assert len(aggregate_replicates(stable)) == 5
drifting = []
for i, x in enumerate((-2.0, -1.0, 0.0, 1.0, 2.0) * 2):
    drifting.append((x, 0.5 * x + 0.5 + 0.05 * i))
drift_bad = calibrate_replicates(drifting, saturation=3.0,
                                 max_relative_std=0.5,
                                 max_normalized_drift=0.001)
assert not drift_bad.quality.passed
assert any('acquisition drift' in reason for reason in drift_bad.quality.reasons)
print('replicate validation passed')
print(replicate_report(report))
print(replicate_report(bad))
