"""End-to-end trainable network using calibrated soliton layers."""
from __future__ import annotations

from typing import Iterable, Sequence

from .soliton_hardware import CalibratedSolitonLayer, Perturbation
from .soliton_mixing import ramp_activation


class CalibratedSolitonNetwork:
    """Multi-layer network with calibrated bus impairments in every layer.

    Each layer is a synchronous bank of differential soliton mixers. The
    native ramp is applied after every layer, including the output layer. The
    optimizer deliberately evaluates the complete impaired forward path.
    """
    def __init__(self, weights: Sequence[Sequence[Sequence[float]]],
                 biases: Sequence[Sequence[float]] = ()):
        if not weights:
            raise ValueError("weights must contain at least one layer")
        if biases and len(biases) != len(weights):
            raise ValueError("bias layer count must equal weight layer count")
        self.layers = []
        previous_width = len(weights[0][0]) if weights[0] else 0
        if previous_width < 1:
            raise ValueError("first weight matrix must be non-empty")
        for index, matrix in enumerate(weights):
            if not matrix or any(len(row) != previous_width for row in matrix):
                raise ValueError("weight matrices must be non-empty and dimensionally linked")
            bias = biases[index] if biases else ()
            layer = CalibratedSolitonLayer(matrix, bias)
            self.layers.append(layer)
            previous_width = layer.output_width

    @property
    def input_width(self) -> int:
        return self.layers[0].input_width

    @property
    def output_width(self) -> int:
        return self.layers[-1].output_width

    def forward(self, inputs: Sequence[float], *, tick: int = 0,
                impairment: Perturbation = Perturbation()) -> tuple[float, ...]:
        values = tuple(float(x) for x in inputs)
        if len(values) != self.input_width:
            raise ValueError(f"expected {self.input_width} inputs, got {len(values)}")
        for layer in self.layers:
            values = tuple(ramp_activation(x) for x in layer.forward(
                values, tick=tick, impairment=impairment))
        return values

    def _loss(self, samples: Sequence[tuple[Sequence[float], Sequence[float]]],
              impairment: Perturbation) -> float:
        total = 0.0
        for inputs, target in samples:
            if len(target) != self.output_width or not target:
                raise ValueError("target width must equal network output width and be nonzero")
            try:
                output = self.forward(inputs, impairment=impairment)
                total += sum((y - float(t)) ** 2 for y, t in zip(output, target)) / len(target)
            except ValueError:
                total += 1.0
        return total / len(samples)

    def train_robust(self, samples: Iterable[tuple[Sequence[float], Sequence[float]]],
                     *, epochs: int = 20, learning_rate: float = 0.05,
                     impairment: Perturbation = Perturbation(),
                     epsilon: float = 1e-4) -> list[float]:
        """Train all layers against the complete impaired forward path."""
        data = list(samples)
        if not data or epochs < 0 or learning_rate <= 0 or epsilon <= 0:
            raise ValueError("samples non-empty; epochs non-negative; rates positive")
        losses: list[float] = []
        for _ in range(epochs):
            losses.append(self._loss(data, impairment))
            for layer in self.layers:
                for row in range(layer.output_width):
                    for col in range(layer.input_width):
                        original = layer.weights[row][col]
                        rows = [list(r) for r in layer.weights]
                        rows[row][col] = original + epsilon
                        layer.weights = tuple(tuple(r) for r in rows)
                        layer._rebuild_mixers()
                        plus = self._loss(data, impairment)
                        rows[row][col] = original - epsilon
                        layer.weights = tuple(tuple(r) for r in rows)
                        layer._rebuild_mixers()
                        minus = self._loss(data, impairment)
                        gradient = (plus - minus) / (2.0 * epsilon)
                        rows[row][col] = original - learning_rate * gradient
                        layer.weights = tuple(tuple(r) for r in rows)
                        layer._rebuild_mixers()
        return losses
