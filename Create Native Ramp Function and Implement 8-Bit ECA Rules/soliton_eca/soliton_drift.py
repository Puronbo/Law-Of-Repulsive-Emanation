"""Acquisition-order drift diagnostics for soliton calibration captures."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .soliton_calibration import CalibrationReport


@dataclass(frozen=True, slots=True)
class DriftDiagnostics:
    samples: int
    residual_slope: float
    normalized_slope: float
    residual_start: float
    residual_end: float


def estimate_drift(measurements: Sequence[tuple[float, float]],
                   calibration: CalibrationReport,
                   *, output_span: float | None = None) -> DriftDiagnostics:
    """Fit residual versus acquisition order using least squares.

    The input sequence must be in actual capture order. A randomized input
    schedule is recommended so drift is not confused with the transfer curve.
    """
    if len(measurements) < 2:
        raise ValueError("at least two ordered measurements are required")
    residuals = [calibration.calibration.gain * float(x) + calibration.calibration.offset - float(y)
                 for x, y in measurements]
    n = len(residuals)
    mean_i = (n - 1) / 2.0
    mean_r = sum(residuals) / n
    denominator = sum((i - mean_i) ** 2 for i in range(n))
    slope = sum((i - mean_i) * (r - mean_r) for i, r in enumerate(residuals)) / denominator
    scale = output_span if output_span is not None else max(max(residuals) - min(residuals), 1e-12)
    if scale <= 0:
        raise ValueError("output_span must be positive")
    return DriftDiagnostics(n, slope, slope / scale, residuals[0], residuals[-1])


def drift_passes(diagnostics: DriftDiagnostics, *, max_normalized_slope: float = 0.01) -> bool:
    """Return whether residual drift per acquisition step is within threshold."""
    if max_normalized_slope < 0:
        raise ValueError("max_normalized_slope must be non-negative")
    return abs(diagnostics.normalized_slope) <= max_normalized_slope
