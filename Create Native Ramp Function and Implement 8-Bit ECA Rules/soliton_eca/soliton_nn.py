"""Soliton neural network built from weighted event buses.

The network is a synchronous feed-forward graph. Inputs, weighted synaptic
contributions, biases, activations, and outputs are all carried as solitons.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .soliton_eca import SolitonBus, ramp


@dataclass(frozen=True, slots=True)
class NeuralSoliton:
    """A localized scalar signal transported on a named bus."""
    bus: str
    source: int
    target: int
    value: float
    tick: int


class WeightedSolitonBus(SolitonBus):
    """Soliton bus with a fixed synaptic weight."""
    def __init__(self, weight: float, name: str):
        super().__init__()
        self.weight = float(weight)
        self.name = name

    def transmit(self, signal: NeuralSoliton) -> None:
        self.send(NeuralSoliton(self.name, signal.source, signal.target,
                                signal.value * self.weight, signal.tick))


class SolitonNeuron:
    """Integrate-and-fire style node with ramp activation.

    The node waits for one contribution from every inbound bus, adds the
    bias, applies ``ramp(x)`` and emits exactly one activation soliton.
    """
    def __init__(self, index: int, inbound: Sequence[WeightedSolitonBus],
                 bias: float = 0.0):
        self.index = index
        self.inbound = tuple(inbound)
        self.bias = float(bias)
        self.output = SolitonBus()

    def fire(self, tick: int) -> NeuralSoliton:
        total = self.bias
        for bus in self.inbound:
            signal = bus.receive()
            if (signal.tick != tick or signal.target != self.index or
                    signal.bus != bus.name):
                raise ValueError("inbound soliton does not match neuron tick/target")
            total += signal.value
        activation = float(ramp(total))
        result = NeuralSoliton(f"neuron:{self.index}", self.index, -1,
                               activation, tick)
        self.output.send(result)
        return result


class SolitonNeuralNetwork:
    """Dense feed-forward neural network with soliton-only signal flow.

    ``sizes`` describes input, hidden, and output widths. The default positive
    ramp is used at every layer. Training uses squared error and the exact
    piecewise derivative of the ramp away from zero.
    """
    def __init__(self, sizes: Sequence[int], *, seed: int = 7):
        if len(sizes) < 2 or any(int(n) < 1 for n in sizes):
            raise ValueError("sizes must contain at least two positive widths")
        self.sizes = tuple(int(n) for n in sizes)
        self.tick = 0
        # Local deterministic PRNG avoids a dependency on numpy.
        self._rng = seed & 0x7FFFFFFF
        self.weights: list[list[list[float]]] = []
        self.biases: list[list[float]] = []
        for fan_in, fan_out in zip(self.sizes, self.sizes[1:]):
            scale = (2.0 / fan_in) ** 0.5
            matrix = [[self._random_signed() * scale for _ in range(fan_in)]
                      for _ in range(fan_out)]
            self.weights.append(matrix)
            self.biases.append([0.0] * fan_out)

    def _random_signed(self) -> float:
        self._rng = (1103515245 * self._rng + 12345) & 0x7FFFFFFF
        return (self._rng / 0x3FFFFFFF) - 1.0

    @staticmethod
    def _activation(x: float) -> float:
        return float(ramp(x))

    @staticmethod
    def _derivative(x: float) -> float:
        return 1.0 if x > 0 else 0.0

    def _forward(self, inputs: Sequence[float], *, tick: int,
                 cache: bool = False) -> tuple[list[float], list[list[float]], list[list[float]]]:
        if len(inputs) != self.sizes[0]:
            raise ValueError(f"expected {self.sizes[0]} inputs, got {len(inputs)}")
        activations = [list(map(float, inputs))]
        preacts: list[list[float]] = []
        for layer, (fan_in, fan_out) in enumerate(zip(self.sizes, self.sizes[1:])):
            buses = [[WeightedSolitonBus(self.weights[layer][j][i],
                                         f"synapse:{layer}:{i}>{j}")
                      for i in range(fan_in)] for j in range(fan_out)]
            source_signals = [NeuralSoliton(f"layer:{layer}", i, -1,
                                            activations[-1][i], tick)
                              for i in range(fan_in)]
            layer_pre: list[float] = []
            layer_act: list[float] = []
            for j in range(fan_out):
                for i, signal in enumerate(source_signals):
                    buses[j][i].transmit(NeuralSoliton(signal.bus, i, j,
                                                        signal.value, tick))
                neuron = SolitonNeuron(j, buses[j], self.biases[layer][j])
                # Fire consumes all weighted synaptic solitons and emits a bus
                # signal, preserving event semantics through the complete layer.
                total = self.biases[layer][j] + sum(bus.peek().value for bus in buses[j])
                result = neuron.fire(tick)
                layer_pre.append(total)
                layer_act.append(result.value)
            preacts.append(layer_pre)
            activations.append(layer_act)
        return activations[-1], activations, preacts

    def forward(self, inputs: Sequence[float]) -> tuple[float, ...]:
        """Inject input solitons and return the output bus values."""
        self.tick += 1
        output, _, _ = self._forward(inputs, tick=self.tick)
        return tuple(output)

    def train(self, samples: Iterable[tuple[Sequence[float], Sequence[float]]],
              epochs: int = 100, learning_rate: float = 0.05) -> list[float]:
        """Train with online squared-error backpropagation; return epoch losses."""
        if epochs < 0 or learning_rate <= 0:
            raise ValueError("epochs must be non-negative and learning_rate positive")
        data = list(samples)
        if not data:
            raise ValueError("samples must not be empty")
        losses: list[float] = []
        for _ in range(epochs):
            total_loss = 0.0
            for inputs, target in data:
                self.tick += 1
                output, acts, preacts = self._forward(inputs, tick=self.tick, cache=True)
                if len(target) != self.sizes[-1]:
                    raise ValueError("target width does not match output width")
                deltas: list[list[float]] = [[] for _ in self.weights]
                deltas[-1] = [(output[j] - float(target[j])) * self._derivative(preacts[-1][j])
                              for j in range(self.sizes[-1])]
                for layer in range(len(self.weights) - 2, -1, -1):
                    deltas[layer] = [self._derivative(preacts[layer][i]) *
                                     sum(self.weights[layer + 1][j][i] * deltas[layer + 1][j]
                                         for j in range(self.sizes[layer + 2]))
                                     for i in range(self.sizes[layer + 1])]
                for layer, matrix in enumerate(self.weights):
                    for j in range(len(matrix)):
                        self.biases[layer][j] -= learning_rate * deltas[layer][j]
                        for i in range(len(matrix[j])):
                            matrix[j][i] -= learning_rate * deltas[layer][j] * acts[layer][i]
                total_loss += sum((output[j] - float(target[j])) ** 2
                                  for j in range(len(output))) / len(output)
            losses.append(total_loss / len(data))
        return losses
