import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import (CalibratedSolitonLayer, Perturbation, fit_affine_calibration,
                         robustness_summary, robust_train)

fit = fit_affine_calibration(((0.0, 0.1), (1.0, 0.6), (2.0, 1.0)), saturation=2.0)
assert abs(fit.calibration.gain - 0.45) < 1e-12
assert abs(fit.calibration.offset - 0.11666666666666667) < 1e-12
assert fit.rmse < 0.03
assert fit.samples == 3
layer = CalibratedSolitonLayer(((0.2, -0.1),), (0.0,))
samples = [((1.0, 0.0), (1.0,)), ((0.0, 1.0), (0.0,))]
losses = robust_train(layer, samples, epochs=8, learning_rate=0.05,
                      impairment=Perturbation(gain_error=0.1))
assert losses[-1] <= losses[0]
summary = robustness_summary(layer, (1.0, 0.0),
                             (Perturbation(), Perturbation(gain_error=0.1),
                              Perturbation(crosstalk=0.1)))
assert summary['cases'] == 3.0
print('calibration validation passed')
print('fit:', fit)
print('losses:', losses)
print('robustness:', summary)
