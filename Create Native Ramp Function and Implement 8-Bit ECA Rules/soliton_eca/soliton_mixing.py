"""Signed soliton channels and calibrated weighted optical-style mixing."""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite
from typing import Iterable, Sequence

from .soliton_protocol import Packet


@dataclass(frozen=True, slots=True)
class DifferentialSoliton:
    """A signed signal represented by positive and negative soliton packets."""
    positive: Packet | None
    negative: Packet | None

    @property
    def value(self) -> float:
        return ((self.positive.amplitude if self.positive else 0.0) -
                (self.negative.amplitude if self.negative else 0.0))


class DifferentialEncoder:
    """Encode signed values using balanced positive/negative optical channels."""
    def __init__(self, *, channel: str = "data", phase: int = 0):
        self.channel, self.phase = channel, phase % 2

    def encode(self, value: float, *, tick: int, position: int,
               velocity: int = 1) -> DifferentialSoliton:
        if velocity not in (-1, 1):
            raise ValueError("velocity must be -1 or +1")
        magnitude = abs(float(value))
        if magnitude == 0:
            return DifferentialSoliton(None, None)
        packet = Packet(tick, position, velocity, magnitude,
                        self.channel, self.phase)
        return (DifferentialSoliton(packet, None) if value > 0
                else DifferentialSoliton(None, packet))

    @staticmethod
    def decode(signal: DifferentialSoliton) -> float:
        if signal.positive and signal.negative:
            if (signal.positive.tick, signal.positive.position) != (signal.negative.tick, signal.negative.position):
                raise ValueError("differential legs are not aligned")
        return signal.value


@dataclass(frozen=True, slots=True)
class ActivationCalibration:
    """Measured transfer parameters for a scalar nonlinear activation."""
    gain: float = 1.0
    offset: float = 0.0
    saturation: float = 1.0
    noise_std: float = 0.0

    def __post_init__(self) -> None:
        if (not all(isfinite(x) for x in (self.gain, self.offset, self.saturation, self.noise_std))
                or self.saturation <= 0 or self.gain < 0 or self.noise_std < 0):
            raise ValueError("saturation must be positive; gain/noise non-negative")


class CalibratedMixer:
    """Synchronous signed weighted mixer with measured calibration parameters."""
    def __init__(self, weights: Sequence[float], *, bias: float = 0.0,
                 calibration: ActivationCalibration = ActivationCalibration(),
                 seed: int = 17):
        if not weights:
            raise ValueError("weights must not be empty")
        self.weights = tuple(float(w) for w in weights)
        self.bias = float(bias)
        if not all(isfinite(w) for w in self.weights) or not isfinite(self.bias):
            raise ValueError("weights and bias must be finite")
        self.calibration = calibration
        self._state = seed & 0x7FFFFFFF

    def _normal(self) -> float:
        # Deterministic Box-Muller-free bounded noise surrogate for reproducible tests.
        self._state = (1664525 * self._state + 1013904223) & 0xFFFFFFFF
        return ((self._state / 0xFFFFFFFF) * 2.0 - 1.0) * self.calibration.noise_std

    def mix(self, signals: Iterable[DifferentialSoliton], *, tick: int,
            position: int, velocity: int = 1) -> DifferentialSoliton:
        signals = tuple(signals)
        values = [DifferentialEncoder.decode(signal) for signal in signals]
        if len(values) != len(self.weights):
            raise ValueError("signal count must equal weight count")
        for signal in signals:
            packets = (signal.positive, signal.negative)
            if any(packet is not None and packet.tick != tick for packet in packets):
                raise ValueError("signal arrival tick does not match mixer tick")
        raw = self.bias + sum(w * x for w, x in zip(self.weights, values))
        measured = self.calibration.gain * raw + self.calibration.offset + self._normal()
        measured = max(-self.calibration.saturation,
                       min(self.calibration.saturation, measured))
        return DifferentialEncoder().encode(measured, tick=tick,
                                            position=position, velocity=velocity)


def ramp_activation(x: float, calibration: ActivationCalibration = ActivationCalibration()) -> float:
    """Measured positive ramp with gain, offset, symmetric saturation, and noise."""
    measured = calibration.gain * float(x) + calibration.offset
    measured = max(-calibration.saturation, min(calibration.saturation, measured))
    if calibration.noise_std:
        # Deterministic model: noise is supplied by the mixer when stochasticity is needed.
        measured += calibration.noise_std
    return max(0.0, measured)


def sigmoid_activation(x: float, *, gain: float = 1.0, offset: float = 0.0) -> float:
    """Bounded reference activation for comparison with native ramp hardware."""
    if not isfinite(gain) or not isfinite(offset) or gain < 0:
        raise ValueError("gain must be non-negative")
    return 1.0 / (1.0 + exp(-gain * (float(x) + offset)))


def transfer_curve(activation, inputs: Sequence[float]) -> list[tuple[float, float]]:
    """Sample an activation transfer function for calibration and plotting."""
    return [(float(x), float(activation(x))) for x in inputs]
