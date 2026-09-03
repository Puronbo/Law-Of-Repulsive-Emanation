import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import (
    CalibratedSolitonLayer, benchmark_summary, calibrate_csv, impairment_sweep,
    require_quality,
    estimate_uncertainty, require_uncertainty,
    leave_one_input_out, require_holdout,
    evaluate_coverage, require_coverage,
)

root = Path(__file__).parent
measured, fit, diagnostics = calibrate_csv(root / 'sample_transfer.csv', saturation=2.0)
assert len(measured) == 5
assert diagnostics.samples == 5
assert diagnostics.monotonic
assert diagnostics.input_span == 4.0
assert abs(diagnostics.output_span - 1.35) < 1e-12
quality = require_quality(measured, fit)
uncertainty = estimate_uncertainty(measured, fit)
require_uncertainty(uncertainty, operating_range=(-2.0, 2.0),
                    max_prediction_half_width=1.0)
holdout = leave_one_input_out(measured, saturation=2.0, min_repeats=1)
require_holdout(holdout, max_normalized_error=0.35)
coverage = evaluate_coverage(measured, (-2.0, 2.0), max_internal_gap=1.0)
require_coverage(coverage)
layer = CalibratedSolitonLayer(((1.0, -0.5), (0.25, 2.0)), (0.1, -0.2),
                               calibration=fit.calibration)
results = impairment_sweep(layer, (0.8, -0.4))
summary = benchmark_summary(results)
assert summary['cases'] == 24.0
assert summary['timing_rejections'] == 12.0
assert summary['worst_error'] >= summary['mean_error'] >= 0.0
report = root / 'benchmark_report.md'
report.write_text(
    '# Soliton Calibration Benchmark\n\n'
    f'- Samples: {diagnostics.samples}\n'
    f'- Gain: {fit.calibration.gain:.9f}\n'
    f'- Offset: {fit.calibration.offset:.9f}\n'
    f'- Fit RMSE: {fit.rmse:.9f}\n'
    f'- Monotonic: {diagnostics.monotonic}\n'
    f'- Quality gate: {"PASS" if quality.passed else "FAIL"}\n'
    f'- Leave-one-out gain std: {quality.gain_std_loo:.9f}\n'
    f'- Leave-one-out offset std: {quality.offset_std_loo:.9f}\n'
    f'- Prediction half-width at range endpoints: '
    f'{max(uncertainty.prediction_half_width(-2.0), uncertainty.prediction_half_width(2.0)):.9f}\n'
    f'- Holdout normalized maximum error: {holdout.normalized_max_error:.9f}\n'
    f'- Domain coverage: {"PASS" if coverage.covered else "FAIL"}\n'
    f'- Largest internal input gap: {coverage.largest_internal_gap:.9f}\n'
    f'- Sweep cases: {int(summary["cases"])}\n'
    f'- Mean relative error: {summary["mean_error"]:.9f}\n'
    f'- Worst relative error: {summary["worst_error"]:.9f}\n'
    f'- Timing rejections: {int(summary["timing_rejections"])}\n',
    encoding='utf-8')
print('benchmark validation passed')
print(diagnostics)
print(summary)
print(report)
