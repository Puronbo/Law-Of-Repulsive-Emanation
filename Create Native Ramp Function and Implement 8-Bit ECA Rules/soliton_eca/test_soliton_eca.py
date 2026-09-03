import pytest
import numpy as np

from soliton_eca import (
    RULES, Fiber, NeuralSoliton, Packet, SolitonECA, SolitonLattice,
    SolitonNeuralNetwork, SolitonNeuron, WeightedSolitonBus, collision,
    evolve, negative_ramp, ramp, soliton_validation,
    ActivationCalibration, CalibratedMixer, DifferentialEncoder,
    ramp_activation, transfer_curve,
)


def test_native_ramps_use_sign_gates():
    assert [ramp(x) for x in (-2, -1, 0, 1, 2)] == [0, 0, 0, 1, 2]
    assert [negative_ramp(x) for x in (-2, -1, 0, 1, 2)] == [-2, -1, 0, 0, 0]


def test_all_requested_rules_are_available():
    assert RULES == (4, 12, 36, 44, 68, 76, 100, 108,
                     132, 140, 164, 172, 196, 204, 228, 236)
    for rule in RULES:
        assert {SolitonECA.apply_rule(rule, a, b, c)
                for a in (0, 1) for b in (0, 1) for c in (0, 1)} <= {0, 1}


def test_rule_204_is_identity():
    initial = (1, 0, 1, 1, 0)
    assert evolve(204, initial, 3) == [initial, initial, initial]


def test_rule_4_single_step():
    initial = (0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0)
    assert evolve(4, initial, 1) == [initial]


def test_boundary_is_zero_and_diagram_is_rendered():
    machine = SolitonECA(204, 3, (1, 0, 1))
    assert machine.diagram(1) == "█·█\n█·█"


def test_weighted_soliton_bus_and_ramp_neuron():
    bus = WeightedSolitonBus(2.5, "w")
    bus.transmit(NeuralSoliton("input", 0, 0, 2.0, 1))
    neuron = SolitonNeuron(0, [bus], bias=-1.0)
    assert neuron.fire(1).value == 4.0


def test_network_forward_is_deterministic_and_validates_width():
    network = SolitonNeuralNetwork((2, 3, 1), seed=3)
    first = network.forward((1.0, 0.0))
    assert first == network.forward((1.0, 0.0))
    with pytest.raises(ValueError):
        network.forward((1.0,))


def test_packet_collision_and_lattice_logging():
    a = Packet(0, 2, 1, 1.0)
    b = Packet(0, 2, -1, 1.0)
    assert collision(a, b, mode="xor") is None
    lattice = SolitonLattice(7)
    lattice.inject((Packet(0, 1, 1, 1.0), Packet(0, 5, -1, 1.0)))
    lattice.run(2)
    assert lattice.tick == 2
    assert len(lattice.log) == 3


def test_fundamental_soliton_digital_twin():
    metrics = soliton_validation(size=512, span=40.0, distance=0.5, steps=100)
    assert metrics["relative_energy_drift"] < 1e-10
    assert metrics["relative_power_error"] < 1e-3
    assert Fiber().beta2 < 0
    assert np.isfinite(metrics["relative_power_error"])


def test_invalid_protocol_inputs():
    with pytest.raises(ValueError):
        Packet(0, 0, 0, 1.0).advance(length=4)
    with pytest.raises(ValueError):
        SolitonLattice(1)


def test_differential_encoding_round_trip_and_cancellation():
    encoder = DifferentialEncoder()
    for value in (-3.5, 0.0, 2.25):
        assert encoder.decode(encoder.encode(value, tick=2, position=4)) == value
    positive = encoder.encode(2.0, tick=2, position=4)
    negative = encoder.encode(-1.0, tick=2, position=4)
    # Separate legs are required; combining them is explicit at the mixer.
    mixed = CalibratedMixer((1.0, 1.0)).mix((positive, negative), tick=2, position=4)
    assert mixed.value == 1.0


def test_calibrated_mixer_saturates_and_activation_is_measurable():
    mixer = CalibratedMixer((2.0,), calibration=ActivationCalibration(saturation=1.0))
    signal = DifferentialEncoder().encode(3.0, tick=0, position=0)
    assert mixer.mix((signal,), tick=0, position=0).value == 1.0
    curve = transfer_curve(lambda x: ramp_activation(x), (-1.0, 0.0, 0.5, 2.0))
    assert curve == [(-1.0, 0.0), (0.0, 0.0), (0.5, 0.5), (2.0, 1.0)]
