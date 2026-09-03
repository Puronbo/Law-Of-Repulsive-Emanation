"""Replicate-aware calibration for noisy soliton device measurements."""
from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Sequence

from .soliton_calibration import CalibrationReport, fit_affine_calibration
from .soliton_quality import QualityGate, QualityResult, evaluate_quality
from .soliton_drift import DriftDiagnostics, drift_passes, estimate_drift


@dataclass(frozen=True, slots=True)
class ReplicatePoint:
    input_value: float
    mean_output: float
    std_output: float
    count: int


@dataclass(frozen=True, slots=True)
class ReplicateReport:
    points: tuple[ReplicatePoint, ...]
    calibration: CalibrationReport
    quality: QualityResult
    max_relative_std: float
    mean_relative_std: float
    drift: DriftDiagnostics


def aggregate_replicates(measurements: Sequence[tuple[float, float]], *,
                         min_repeats: int = 2) -> tuple[ReplicatePoint, ...]:
    """Aggregate repeated ``(input, output)`` observations by exact input value."""
    if min_repeats < 1:
        raise ValueError("min_repeats must be positive")
    groups: dict[float, list[float]] = {}
    for x, y in measurements:
        groups.setdefault(float(x), []).append(float(y))
    if not groups or any(len(values) < min_repeats for values in groups.values()):
        raise ValueError("every input value must have the minimum replicate count")
    return tuple(ReplicatePoint(x, mean(values), pstdev(values), len(values))
                 for x, values in sorted(groups.items()))


def calibrate_replicates(measurements: Sequence[tuple[float, float]], *,
                         saturation: float = 1.0, min_repeats: int = 2,
                         gate: QualityGate = QualityGate(),
                         max_relative_std: float = 0.1,
                         max_normalized_drift: float = 0.01) -> ReplicateReport:
    """Aggregate replicates, fit the mean curve, and apply stability gates."""
    if max_relative_std < 0:
        raise ValueError("max_relative_std must be non-negative")
    points = aggregate_replicates(measurements, min_repeats=min_repeats)
    means = [(point.input_value, point.mean_output) for point in points]
    calibration = fit_affine_calibration(means, saturation=saturation)
    quality = evaluate_quality(means, calibration, gate)
    output_span = max(point.mean_output for point in points) - min(point.mean_output for point in points)
    denominator = max(output_span, 1e-12)
    relative_stds = [point.std_output / denominator for point in points]
    reasons = list(quality.reasons)
    if relative_stds and max(relative_stds) > max_relative_std:
        reasons.append(f"maximum relative replicate std {max(relative_stds):.6g} exceeds {max_relative_std:.6g}")
    drift = estimate_drift(measurements, calibration, output_span=output_span)
    if not drift_passes(drift, max_normalized_slope=max_normalized_drift):
        reasons.append(f"normalized acquisition drift {abs(drift.normalized_slope):.6g} exceeds {max_normalized_drift:.6g}")
    final_quality = QualityResult(not reasons, tuple(reasons), quality.diagnostics,
                                 quality.gain_std_loo, quality.offset_std_loo)
    return ReplicateReport(points, calibration, final_quality,
                           max(relative_stds, default=0.0),
                           mean(relative_stds) if relative_stds else 0.0, drift)


def replicate_report(report: ReplicateReport) -> str:
    """Render a concise reproducibility report."""
    status = "PASS" if report.quality.passed else "FAIL"
    reasons = "none" if not report.quality.reasons else "; ".join(report.quality.reasons)
    rows = "\n".join(f"| {p.input_value:g} | {p.mean_output:.9g} | {p.std_output:.9g} | {p.count} |"
                      for p in report.points)
    return (f"# Replicate Calibration: {status}\n\n"
            "| Input | Mean output | Std. dev. | Count |\n"
            "|---:|---:|---:|---:|\n" + rows + "\n\n"
            f"- Fit RMSE: {report.calibration.rmse:.9g}\n"
            f"- Maximum relative replicate std: {report.max_relative_std:.9g}\n"
            f"- Mean relative replicate std: {report.mean_relative_std:.9g}\n"
            f"- Normalized acquisition drift per sample: {report.drift.normalized_slope:.9g}\n"
            f"- Reasons: {reasons}\n")
