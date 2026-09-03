"""Hardware-in-the-loop style soliton layer and perturbation harness."""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence

from .soliton_mixing import (
    ActivationCalibration, CalibratedMixer, DifferentialEncoder,
    DifferentialSoliton,
)


@dataclass(frozen=True, slots=True)
class Perturbation:
    """Bounded impairments applied to a transmitted differential signal."""
    gain_error: float = 0.0
    timing_jitter: int = 0
    drop_positive: bool = False
    drop_negative: bool = False
    crosstalk: float = 0.0

    def __post_init__(self) -> None:
        if (not all(isfinite(x) for x in (self.gain_error, self.crosstalk))
                or self.timing_jitter < 0 or abs(self.gain_error) > 1):
            raise ValueError("timing_jitter must be non-negative and gain_error in [-1, 1]")
        if self.crosstalk < 0:
            raise ValueError("crosstalk must be non-negative")


def perturb(signal: DifferentialSoliton, *, impairment: Perturbation,
            tick: int, position: int) -> DifferentialSoliton:
    """Apply explicit impairments without mutating the original packet."""
    encoder = DifferentialEncoder()
    value = signal.value * (1.0 + impairment.gain_error)
    if impairment.drop_positive and signal.positive is not None:
        value -= signal.positive.amplitude
    if impairment.drop_negative and signal.negative is not None:
        value += signal.negative.amplitude
    # Crosstalk is modeled as a deterministic leakage fraction into the
    # opposite leg; unlike random noise, this is reproducible and measurable.
    if impairment.crosstalk:
        value *= max(0.0, 1.0 - impairment.crosstalk)
    result = encoder.encode(value, tick=tick + impairment.timing_jitter,
                            position=position)
    return result


class CalibratedSolitonLayer:
    """Dense layer whose every scalar multiply and sum is a calibrated bus."""
    def __init__(self, weights: Sequence[Sequence[float]],
                 biases: Sequence[float] = (), *,
                 calibration: ActivationCalibration = ActivationCalibration()):
        if not weights or not weights[0]:
            raise ValueError("weights must be a non-empty rectangular matrix")
        width = len(weights[0])
        if any(len(row) != width for row in weights):
            raise ValueError("weights must be rectangular")
        if biases and len(biases) != len(weights):
            raise ValueError("bias count must equal output width")
        self.weights = tuple(tuple(float(x) for x in row) for row in weights)
        self.biases = tuple(float(x) for x in (biases or [0.0] * len(weights)))
        self.calibration = calibration
        self.encoder = DifferentialEncoder()
        self._rebuild_mixers()

    def _rebuild_mixers(self) -> None:
        """Refresh bus weights after calibration or optimizer updates."""
        self.mixers = tuple(CalibratedMixer(row, bias=bias,
                                            calibration=calibration)
                            for row, bias in zip(self.weights, self.biases)
                            for calibration in (self.calibration,))

    @property
    def input_width(self) -> int:
        return len(self.weights[0])

    @property
    def output_width(self) -> int:
        return len(self.weights)

    def forward(self, inputs: Sequence[float], *, tick: int = 0, position: int = 0,
                impairment: Perturbation = Perturbation()) -> tuple[float, ...]:
        if len(inputs) != self.input_width:
            raise ValueError(f"expected {self.input_width} inputs, got {len(inputs)}")
        signals = tuple(perturb(self.encoder.encode(value, tick=tick, position=position),
                               impairment=impairment, tick=tick, position=position)
                       for value in inputs)
        outputs = tuple(mixer.mix(signals, tick=tick, position=position).value
                        for mixer in self.mixers)
        return outputs


def relative_error(reference: Sequence[float], observed: Sequence[float]) -> float:
    """Normalized Euclidean output error for an impairment experiment."""
    if len(reference) != len(observed) or not reference:
        raise ValueError("vectors must be non-empty and have equal width")
    denominator = max(sum(x * x for x in reference) ** 0.5, 1e-12)
    return (sum((x - y) ** 2 for x, y in zip(reference, observed)) ** 0.5) / denominator


def perturbation_report(layer: CalibratedSolitonLayer, inputs: Sequence[float],
                        impairments: Sequence[Perturbation]) -> list[dict[str, float]]:
    """Return ideal outputs and normalized errors for a fixed impairment sweep."""
    ideal = layer.forward(inputs)
    report: list[dict[str, float]] = []
    for impairment in impairments:
        try:
            observed = layer.forward(inputs, impairment=impairment)
            error = relative_error(ideal, observed)
        except ValueError as exc:
            if "arrival tick" not in str(exc):
                raise
            # An unsynchronized frame is rejected, not silently mixed.
            error = 1.0
        report.append({"gain_error": impairment.gain_error,
                       "timing_jitter": float(impairment.timing_jitter),
                       "packet_loss": float(impairment.drop_positive or impairment.drop_negative),
                       "crosstalk": impairment.crosstalk,
                       "relative_error": error})
    return report
