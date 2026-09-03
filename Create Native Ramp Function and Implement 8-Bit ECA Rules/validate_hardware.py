import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import CalibratedSolitonLayer, Perturbation, perturbation_report

layer = CalibratedSolitonLayer(((1.0, -0.5), (0.25, 2.0)), (0.1, -0.2))
inputs = (0.8, -0.4)
ideal = layer.forward(inputs)
assert len(ideal) == 2
report = perturbation_report(layer, inputs, (
    Perturbation(),
    Perturbation(gain_error=0.1),
    Perturbation(timing_jitter=1),
    Perturbation(drop_positive=True),
    Perturbation(crosstalk=0.2),
))
assert report[0]['relative_error'] == 0.0
assert report[1]['relative_error'] > 0.0
assert report[2]['relative_error'] == 1.0
assert report[3]['relative_error'] > 0.0
assert report[4]['relative_error'] > 0.0
print('hardware perturbation validation passed')
for row in report:
    print(row)
