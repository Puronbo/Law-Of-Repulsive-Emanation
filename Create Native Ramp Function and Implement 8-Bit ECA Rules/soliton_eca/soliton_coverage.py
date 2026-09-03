"""Operating-domain coverage checks for soliton calibration."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True, slots=True)
class CoverageReport:
    measured_min: float
    measured_max: float
    operating_min: float
    operating_max: float
    largest_internal_gap: float
    covered: bool
    extrapolation_allowed: bool

    @property
    def extrapolation_distance(self) -> float:
        below = max(0.0, self.measured_min - self.operating_min)
        above = max(0.0, self.operating_max - self.measured_max)
        return max(below, above)


def evaluate_coverage(measured: Sequence[tuple[float, float]],
                      operating_range: tuple[float, float], *,
                      allow_extrapolation: bool = False,
                      max_internal_gap: float | None = None) -> CoverageReport:
    """Check that the intended operating range lies inside measured inputs."""
    if not measured:
        raise ValueError("measured data must not be empty")
    lo, hi = map(float, operating_range)
    if hi < lo:
        raise ValueError("operating range must be ordered")
    inputs = sorted({float(x) for x, _ in measured})
    measured_min, measured_max = inputs[0], inputs[-1]
    gaps = [b - a for a, b in zip(inputs, inputs[1:])]
    largest_gap = max(gaps, default=0.0)
    if max_internal_gap is not None and max_internal_gap < 0:
        raise ValueError("max_internal_gap must be non-negative")
    domain_covered = measured_min <= lo and hi <= measured_max
    gaps_covered = max_internal_gap is None or largest_gap <= max_internal_gap
    covered = domain_covered and gaps_covered
    return CoverageReport(measured_min, measured_max, lo, hi, largest_gap,
                          covered, bool(allow_extrapolation))


def require_coverage(report: CoverageReport, *, allow_extrapolation: bool | None = None) -> None:
    """Raise unless coverage is complete or explicit extrapolation is enabled."""
    permitted = report.extrapolation_allowed if allow_extrapolation is None else allow_extrapolation
    if report.covered:
        return
    if permitted:
        return
    raise ValueError(
        "calibration domain does not cover operating range: "
        f"extrapolation distance={report.extrapolation_distance:.9g}")
