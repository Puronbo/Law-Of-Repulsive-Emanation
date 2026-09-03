"""Independent holdout validation for soliton calibration models."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .soliton_calibration import fit_affine_calibration
from .soliton_replicates import aggregate_replicates


@dataclass(frozen=True, slots=True)
class HoldoutPoint:
    input_value: float
    observed_mean: float
    predicted: float
    absolute_error: float


@dataclass(frozen=True, slots=True)
class HoldoutReport:
    points: tuple[HoldoutPoint, ...]
    output_span: float
    mean_absolute_error: float
    max_absolute_error: float
    normalized_max_error: float


def leave_one_input_out(measurements: Sequence[tuple[float, float]], *,
                        saturation: float = 1.0,
                        min_repeats: int = 2) -> HoldoutReport:
    """Predict each input using a fit trained on all other input levels."""
    points = aggregate_replicates(measurements, min_repeats=min_repeats)
    if len(points) < 4:
        raise ValueError("at least four distinct input levels are required")
    output_span = max(p.mean_output for p in points) - min(p.mean_output for p in points)
    holdouts: list[HoldoutPoint] = []
    for point in points:
        training = [(p.input_value, p.mean_output) for p in points if p.input_value != point.input_value]
        fit = fit_affine_calibration(training, saturation=saturation)
        predicted = fit.calibration.gain * point.input_value + fit.calibration.offset
        holdouts.append(HoldoutPoint(point.input_value, point.mean_output,
                                     predicted, abs(predicted - point.mean_output)))
    errors = [p.absolute_error for p in holdouts]
    return HoldoutReport(tuple(holdouts), output_span, sum(errors) / len(errors),
                         max(errors), max(errors) / max(output_span, 1e-12))


def holdout_passes(report: HoldoutReport, *, max_normalized_error: float = 0.25) -> bool:
    """Check the independent prediction error against the deployment budget."""
    if max_normalized_error < 0:
        raise ValueError("max_normalized_error must be non-negative")
    return report.normalized_max_error <= max_normalized_error


def require_holdout(report: HoldoutReport, *, max_normalized_error: float = 0.25) -> None:
    """Raise if any held-out input is predicted outside the configured budget."""
    if not holdout_passes(report, max_normalized_error=max_normalized_error):
        raise ValueError("held-out calibration error exceeds threshold")


def holdout_report(report: HoldoutReport) -> str:
    """Render a compact holdout report."""
    rows = "\n".join(f"| {p.input_value:g} | {p.observed_mean:.9g} | {p.predicted:.9g} | {p.absolute_error:.9g} |"
                      for p in report.points)
    return ("# Leave-One-Input-Out Calibration\n\n"
            "| Input | Observed mean | Predicted | Absolute error |\n"
            "|---:|---:|---:|---:|\n" + rows + "\n\n"
            f"- Mean absolute error: {report.mean_absolute_error:.9g}\n"
            f"- Maximum absolute error: {report.max_absolute_error:.9g}\n"
            f"- Normalized maximum error: {report.normalized_max_error:.9g}\n")
