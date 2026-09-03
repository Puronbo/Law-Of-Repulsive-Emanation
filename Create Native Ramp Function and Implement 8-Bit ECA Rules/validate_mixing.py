import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import (ActivationCalibration, CalibratedMixer, DifferentialEncoder,
                         ramp_activation, transfer_curve)

encoder = DifferentialEncoder()
for value in (-3.5, 0.0, 2.25):
    assert encoder.decode(encoder.encode(value, tick=2, position=4)) == value
positive = encoder.encode(2.0, tick=2, position=4)
negative = encoder.encode(-1.0, tick=2, position=4)
mixed = CalibratedMixer((1.0, 1.0)).mix((positive, negative), tick=2, position=4)
assert mixed.value == 1.0
mixer = CalibratedMixer((2.0,), calibration=ActivationCalibration(saturation=1.0))
signal = encoder.encode(3.0, tick=0, position=0)
assert mixer.mix((signal,), tick=0, position=0).value == 1.0
curve = transfer_curve(lambda x: ramp_activation(x), (-1.0, 0.0, 0.5, 2.0))
assert curve == [(-1.0, 0.0), (0.0, 0.0), (0.5, 0.5), (2.0, 1.0)]
print('signed-mixing validation passed')
print('transfer curve:', curve)
