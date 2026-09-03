import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from soliton_eca import (
    CalibratedSolitonLayer, CalibratedSolitonNetwork, Fiber, Packet,
    SolitonBus, SolitonLattice, fit_affine_calibration, propagate,
)

# Bus API must distinguish observation from consumption.
bus = SolitonBus()
from soliton_eca import Soliton
bus.send(Soliton('test', 0, 3, 0))
assert bus.peek().value == 3
assert bus.peek() == bus.receive()
try:
    bus.peek()
except IndexError:
    pass
else:
    raise AssertionError('empty peek did not fail')

# Reflective propagation keeps packets in-bounds and preserves amplitude.
lattice = SolitonLattice(4)
lattice.inject((Packet(0, 0, 1, 2.0),))
for _ in range(20):
    packets = lattice.step()
    assert all(0 <= p.position < 4 for p in packets)
    assert all(p.amplitude == 2.0 for p in packets)

# Invalid modes fail even without a collision.
try:
    SolitonLattice(4).step(collision_mode='bad')
except ValueError:
    pass
else:
    raise AssertionError('invalid collision mode accepted')

# Exact affine fit and degenerate data rejection.
fit = fit_affine_calibration(((0, 1), (1, 3), (2, 5)), saturation=10)
assert abs(fit.calibration.gain - 2.0) < 1e-12
assert abs(fit.calibration.offset - 1.0) < 1e-12
try:
    fit_affine_calibration(((1, 2), (1, 3)))
except ValueError:
    pass
else:
    raise AssertionError('degenerate calibration accepted')

# Dimension checks must reject malformed networks before training.
try:
    CalibratedSolitonNetwork((((1.0, 2.0),),), biases=((0.0,), (0.0,)))
except ValueError:
    pass
else:
    raise AssertionError('extra bias layer accepted')
try:
    CalibratedSolitonLayer(((1.0,),), (0.0, 1.0))
except ValueError:
    pass
else:
    raise AssertionError('wrong bias width accepted')

# Zero-distance propagation is identity, and zero loss is finite.
field = np.exp(-np.linspace(-2, 2, 64) ** 2).astype(complex)
assert np.allclose(propagate(field, 0.1, 0.0, fiber=Fiber(), steps=1), field, atol=1e-14)
print('adversarial validation passed')
