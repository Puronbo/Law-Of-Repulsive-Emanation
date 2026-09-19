"""Standalone validator for the soliton neural network (feed-forward).

Checks the soliton-only signal flow end to end, all measured:
    1. EXACT FORWARD  : a hand-set weight/bias reproduces ramp(w*x+b)
                       bit-for-bit (positive arm and cut-off arm).
    2. LEARNING       : online squared-error backpropagation actually
                       reduces the epoch loss (final < half the initial).
    3. BUS SEMANTICS  : WeightedSolitonBus scales by weight and renames
                       the bus; SolitonNeuron integrates inbound buses
                       and emits exactly one activation soliton.
    4. VALIDATION     : wrong widths / empty samples / bad epochs and a
                       mismatched inbound target all raise ValueError.
    5. DETERMINISM    : identical seeds -> identical weights and outputs.

Exit 0 iff all checks pass; prints each measured outcome.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from soliton_eca import (  # noqa: E402
    NeuralSoliton, SolitonNeuralNetwork, SolitonNeuron,
    WeightedSolitonBus,
)


def _check_forward_exact():
    net = SolitonNeuralNetwork([1, 1], seed=7)
    net.weights[0][0][0] = 3.0
    net.biases[0][0] = 0.5
    pos = net.forward([2.0])[0]      # ramp(3*2 + 0.5) = 6.5
    cut = net.forward([-1.0])[0]     # ramp(-3 + 0.5) = 0.0
    assert pos == 6.5, "positive arm: got %r" % pos
    assert cut == 0.0, "cut-off arm: got %r" % cut
    print("  exact forward: ramp(3*2+0.5)=%.1f, ramp(-2.5)=%.1f"
          % (pos, cut))
    return True


def _check_learning():
    net = SolitonNeuralNetwork([1, 1], seed=7)
    samples = [([x], [x if x > 0 else 0.0])
               for x in (-1.0, -0.5, 0.5, 1.0)]
    losses = net.train(samples, epochs=60, learning_rate=0.05)
    assert losses[0] > 0, "initial loss must be positive"
    assert losses[-1] < 0.5 * losses[0], (
        "loss did not halve: %r -> %r" % (losses[0], losses[-1]))
    best = min(losses)
    assert best < 0.5 * losses[0]
    print("  learning: epoch loss %.5f -> %.5f (best %.5f)"
          % (losses[0], losses[-1], best))
    return True


def _check_bus_semantics():
    bus = WeightedSolitonBus(2.0, "w")
    bus.transmit(NeuralSoliton("layer:0", 5, 9, 3.5, 7))
    received = bus.receive()
    assert received.value == 7.0 and received.bus == "w"
    assert (received.source, received.target, received.tick) == (5, 9, 7)
    # a neuron integrates all inbound buses once and fires once
    b1 = WeightedSolitonBus(1.0, "b1")
    b2 = WeightedSolitonBus(0.5, "b2")
    neuron = SolitonNeuron(3, [b1, b2], bias=1.0)
    b1.transmit(NeuralSoliton("x", 0, 3, 2.0, 5))
    b2.transmit(NeuralSoliton("x", 1, 3, 4.0, 5))
    result = neuron.fire(5)
    assert result.value == 5.0, "ramp(1+2+2)=5, got %r" % result.value
    out_signal = neuron.output.receive()
    assert out_signal.value == 5.0 and out_signal.bus == "neuron:3"
    print("  bus semantics: transmit scales/renames; neuron fires once")
    return True


def _check_validation():
    try:
        SolitonNeuralNetwork([1])
    except ValueError:
        pass
    else:
        raise AssertionError("single-width sizes accepted")
    net = SolitonNeuralNetwork([2, 1])
    try:
        net.forward([1.0, 2.0, 3.0])
    except ValueError:
        pass
    else:
        raise AssertionError("wrong forward width accepted")
    try:
        net.train([])
    except ValueError:
        pass
    else:
        raise AssertionError("empty training set accepted")
    try:
        SolitonNeuralNetwork([2, 1]).train(
            [([0.0, 1.0], [1.0])], epochs=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("negative epochs accepted")
    bad_bus = WeightedSolitonBus(1.0, "b")
    bad_bus.transmit(NeuralSoliton("b", 0, 99, 1.0, 5))
    try:
        SolitonNeuron(3, [bad_bus], 0.0).fire(5)
    except ValueError:
        pass
    else:
        raise AssertionError("mismatched inbound target accepted")
    print("  validation: widths, samples, epochs, target all rejected")
    return True


def _check_determinism():
    a = SolitonNeuralNetwork([3, 4, 2], seed=11)
    b = SolitonNeuralNetwork([3, 4, 2], seed=11)
    assert a.weights == b.weights and a.biases == b.biases
    out_a = a.forward([0.5, -0.25, 1.0])
    out_b = b.forward([0.5, -0.25, 1.0])
    assert out_a == out_b
    print("  determinism: seed=11 -> identical weights and outputs")
    return True


def main():
    print("soliton neural network validator (feed-forward, soliton-only)")
    ok = (_check_forward_exact() and _check_learning()
          and _check_bus_semantics() and _check_validation()
          and _check_determinism())
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())