import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import QualityGate, calibrate_csv, evaluate_quality, fit_affine_calibration, quality_report, require_quality

root = Path(__file__).parent
measured, fit, _ = calibrate_csv(root / 'sample_transfer.csv', saturation=2.0)
result = require_quality(measured, fit)
assert result.passed
assert result.reasons == ()
assert result.gain_std_loo >= 0.0
assert 'PASS' in quality_report(result)

bad = [(0.0, 0.0), (1.0, 1.0), (2.0, 0.1), (3.0, 1.1), (4.0, 0.2)]
bad_fit = fit_affine_calibration(bad, saturation=2.0)
# Use a deliberately strict gate to test explicit failure reporting.
bad_result = evaluate_quality(bad, bad_fit, QualityGate(max_relative_rmse=0.01))
assert not bad_result.passed
assert bad_result.reasons
assert 'FAIL' in quality_report(bad_result)
try:
    require_quality(bad, bad_fit, QualityGate(max_relative_rmse=0.01))
except ValueError as exc:
    assert 'quality gate failed' in str(exc)
else:
    raise AssertionError('failed quality gate was accepted')
print('quality-gate validation passed')
print(quality_report(result))
print(quality_report(bad_result))
