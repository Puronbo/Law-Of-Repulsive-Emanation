import sys
from pathlib import Path

# Import the directory as the soliton_eca package, not the legacy module file.
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import (  # noqa: E402
    RULES, NeuralSoliton, SolitonECA, SolitonNeuralNetwork, SolitonNeuron,
    WeightedSolitonBus, evolve, ramp, negative_ramp,
)

assert [ramp(x) for x in (-2, -1, 0, 1, 2)] == [0, 0, 0, 1, 2]
assert [negative_ramp(x) for x in (-2, -1, 0, 1, 2)] == [-2, -1, 0, 0, 0]
assert RULES == (4, 12, 36, 44, 68, 76, 100, 108, 132, 140, 164, 172, 196, 204, 228, 236)
for rule in RULES:
    assert {SolitonECA.apply_rule(rule, a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)} <= {0, 1}
initial = (1, 0, 1, 1, 0)
assert evolve(204, initial, 3) == [initial, initial, initial]
initial = (0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0)
assert evolve(4, initial, 1) == [initial]
machine = SolitonECA(204, 3, (1, 0, 1))
assert machine.diagram(1) == "█·█\n█·█"

bus = WeightedSolitonBus(2.5, "w")
bus.transmit(NeuralSoliton("input", 0, 0, 2.0, 1))
assert SolitonNeuron(0, [bus], bias=-1.0).fire(1).value == 4.0

net = SolitonNeuralNetwork((2, 3, 1), seed=3)
first = net.forward((1.0, 0.0))
assert first == net.forward((1.0, 0.0))
losses = net.train([((0.0, 0.0), (0.0,)), ((1.0, 1.0), (1.0,))], epochs=20)
assert losses[-1] <= losses[0]
print("validation passed")
