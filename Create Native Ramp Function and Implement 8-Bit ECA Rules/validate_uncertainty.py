import sys
from math import isfinite
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import estimate_uncertainty, fit_affine_calibration, require_uncertainty, uncertainty_passes

measured = [(0.0, 1.0), (1.0, 3.0), (2.0, 5.0), (3.0, 7.0), (4.0, 9.0)]
fit = fit_affine_calibration(measured, saturation=20.0)
uncertainty = estimate_uncertainty(measured, fit)
assert uncertainty.degrees_of_freedom == 3
assert uncertainty.gain_ci == (2.0, 2.0)
assert uncertainty.offset_ci == (1.0, 1.0)
assert uncertainty.prediction_half_width(2.0) == 0.0
assert uncertainty_passes(uncertainty, operating_range=(0.0, 4.0), max_prediction_half_width=0.0)
require_uncertainty(uncertainty, operating_range=(0.0, 4.0), max_prediction_half_width=0.0)

noisy = [(0.0, 1.0), (1.0, 3.4), (2.0, 4.8), (3.0, 7.5), (4.0, 8.7)]
noisy_fit = fit_affine_calibration(noisy, saturation=20.0)
noisy_uncertainty = estimate_uncertainty(noisy, noisy_fit)
assert isfinite(noisy_uncertainty.prediction_half_width(2.0))
assert noisy_uncertainty.prediction_half_width(0.0) > 0.0
try:
    require_uncertainty(noisy_uncertainty, operating_range=(-10.0, 10.0), max_prediction_half_width=0.1)
except ValueError:
    pass
else:
    raise AssertionError('wide operating-range uncertainty was accepted')
print('uncertainty validation passed')
print(noisy_uncertainty)
