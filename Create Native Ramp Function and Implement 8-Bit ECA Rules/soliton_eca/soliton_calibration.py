"""Closed-loop calibration and robustness-aware training for soliton layers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .soliton_hardware import CalibratedSolitonLayer, Perturbation, relative_error
from .soliton_mixing import ActivationCalibration


@dataclass(frozen=True, slots=True)
class CalibrationReport:
    """Least-squares affine fit and residual quality."""
    calibration: ActivationCalibration
    rmse: float
    samples: int


def fit_affine_calibration(measured: Iterable[tuple[float, float]], *,
                           saturation: float = 1.0) -> CalibrationReport:
    """Fit ``observed = gain * input + offset`` by ordinary least squares."""
    pairs = [(float(x), float(y)) for x, y in measured]
    if len(pairs) < 2:
        raise ValueError("at least two measured transfer points are required")
    if saturation <= 0:
        raise ValueError("saturation must be positive")
    mean_x = sum(x for x, _ in pairs) / len(pairs)
    mean_y = sum(y for _, y in pairs) / len(pairs)
    denominator = sum((x - mean_x) ** 2 for x, _ in pairs)
    if denominator == 0:
        raise ValueError("measured inputs must not all be identical")
    gain = sum((x - mean_x) * (y - mean_y) for x, y in pairs) / denominator
    gain = max(0.0, gain)
    offset = mean_y - gain * mean_x
    rmse = (sum((gain * x + offset - y) ** 2 for x, y in pairs) / len(pairs)) ** 0.5
    return CalibrationReport(ActivationCalibration(gain=gain, offset=offset,
                                                   saturation=saturation),
                             rmse, len(pairs))


def _loss(layer: CalibratedSolitonLayer,
          samples: Sequence[tuple[Sequence[float], Sequence[float]]],
          impairment: Perturbation) -> float:
    total = 0.0
    for inputs, target in samples:
        if len(target) != layer.output_width or not target:
            raise ValueError("target width must equal layer output width and be nonzero")
        try:
            observed = layer.forward(inputs, impairment=impairment)
            total += sum((y - float(t)) ** 2 for y, t in zip(observed, target)) / len(target)
        except ValueError:
            total += sum(float(t) ** 2 for t in target) / len(target) + 1.0
    return total / len(samples)


def robust_train(layer: CalibratedSolitonLayer,
                 samples: Iterable[tuple[Sequence[float], Sequence[float]]],
                 *, epochs: int = 50, learning_rate: float = 0.05,
                 impairment: Perturbation = Perturbation(),
                 epsilon: float = 1e-4) -> list[float]:
    """Finite-difference SGD against a fixed hardware impairment profile.

    Finite differences are intentional here: the same routine can optimize
    through nondifferentiable packet loss, clipping, and measured transfer
    curves. Use analytic/autodiff gradients later when the physical transfer
    function is established and differentiable.
    """
    data = list(samples)
    if not data or epochs < 0 or learning_rate <= 0 or epsilon <= 0:
        raise ValueError("samples non-empty; epochs non-negative; rates positive")
    losses: list[float] = []
    for _ in range(epochs):
        losses.append(_loss(layer, data, impairment))
        for row in range(layer.output_width):
            for col in range(layer.input_width):
                original = layer.weights[row][col]
                # Tuples are replaced because the public layer state is immutable.
                rows = [list(r) for r in layer.weights]
                rows[row][col] = original + epsilon
                layer.weights = tuple(tuple(r) for r in rows)
                layer._rebuild_mixers()
                plus = _loss(layer, data, impairment)
                rows[row][col] = original - epsilon
                layer.weights = tuple(tuple(r) for r in rows)
                layer._rebuild_mixers()
                minus = _loss(layer, data, impairment)
                gradient = (plus - minus) / (2.0 * epsilon)
                rows[row][col] = original - learning_rate * gradient
                layer.weights = tuple(tuple(r) for r in rows)
                # Rebuild buses so they observe the updated weights.
                layer._rebuild_mixers()
    return losses


def robustness_summary(layer: CalibratedSolitonLayer,
                       inputs: Sequence[float],
                       impairments: Sequence[Perturbation]) -> dict[str, float]:
    """Summarize worst and mean normalized error over an impairment sweep."""
    ideal = layer.forward(inputs)
    errors: list[float] = []
    for impairment in impairments:
        try:
            errors.append(relative_error(ideal, layer.forward(inputs, impairment=impairment)))
        except ValueError:
            errors.append(1.0)
    if not errors:
        raise ValueError("impairments must not be empty")
    return {"mean_relative_error": sum(errors) / len(errors),
            "worst_relative_error": max(errors),
            "cases": float(len(errors))}
