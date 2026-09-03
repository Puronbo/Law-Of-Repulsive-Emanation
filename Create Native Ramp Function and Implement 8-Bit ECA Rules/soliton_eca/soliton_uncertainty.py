"""Uncertainty diagnostics and promotion gates for soliton calibration."""
from __future__ import annotations

from dataclasses import dataclass
from math import inf, sqrt
from typing import Sequence

from .soliton_calibration import CalibrationReport


@dataclass(frozen=True, slots=True)
class UncertaintyReport:
    gain_ci: tuple[float, float]
    offset_ci: tuple[float, float]
    residual_std: float
    degrees_of_freedom: int
    z_score: float

    def prediction_half_width(self, x: float) -> float:
        """Approximate two-sided prediction half-width at input x."""
        if self.degrees_of_freedom <= 0:
            return inf
        return self.z_score * self.residual_std * sqrt(1.0 + self._leverage(float(x)))

    # Stored privately through the dynamically assigned calibration context.
    _xbar: float = 0.0
    _sxx: float = 1.0

    def _leverage(self, x: float) -> float:
        return 1.0 / self._n + (x - self._xbar) ** 2 / self._sxx

    _n: float = 1.0


def estimate_uncertainty(measured: Sequence[tuple[float, float]],
                         calibration: CalibrationReport, *,
                         z_score: float = 1.96) -> UncertaintyReport:
    """Estimate normal-approximation confidence intervals for affine fit."""
    if len(measured) != calibration.samples or len(measured) < 2:
        raise ValueError("measured points and calibration report must match")
    if z_score <= 0:
        raise ValueError("z_score must be positive")
    xs = [float(x) for x, _ in measured]
    ys = [float(y) for _, y in measured]
    n = len(xs)
    xbar = sum(xs) / n
    sxx = sum((x - xbar) ** 2 for x in xs)
    if sxx <= 0:
        raise ValueError("inputs must contain at least two distinct values")
    residuals = [calibration.calibration.gain * x + calibration.calibration.offset - y
                 for x, y in zip(xs, ys)]
    dof = n - 2
    if dof <= 0:
        residual_std = inf
        gain_se = offset_se = inf
    else:
        residual_std = sqrt(sum(r * r for r in residuals) / dof)
        gain_se = residual_std / sqrt(sxx)
        offset_se = residual_std * sqrt(1.0 / n + xbar * xbar / sxx)
    report = UncertaintyReport(
        (calibration.calibration.gain - z_score * gain_se,
         calibration.calibration.gain + z_score * gain_se),
        (calibration.calibration.offset - z_score * offset_se,
         calibration.calibration.offset + z_score * offset_se),
        residual_std, dof, z_score,
    )
    return UncertaintyReport(report.gain_ci, report.offset_ci, report.residual_std,
                             report.degrees_of_freedom, report.z_score,
                             xbar, sxx, float(n))


def uncertainty_passes(report: UncertaintyReport, *, operating_range: tuple[float, float],
                       max_prediction_half_width: float) -> bool:
    """Check prediction uncertainty at both ends of the intended input range."""
    lo, hi = operating_range
    if hi < lo or max_prediction_half_width < 0:
        raise ValueError("operating range must be ordered and threshold non-negative")
    return max(report.prediction_half_width(lo), report.prediction_half_width(hi)) <= max_prediction_half_width


def require_uncertainty(report: UncertaintyReport, *, operating_range: tuple[float, float],
                        max_prediction_half_width: float) -> None:
    """Raise when calibration uncertainty is too large for deployment."""
    if not uncertainty_passes(report, operating_range=operating_range,
                              max_prediction_half_width=max_prediction_half_width):
        raise ValueError("calibration uncertainty exceeds operating-range threshold")
