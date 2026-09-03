"""Measurement-quality gates for soliton device calibration."""
from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Sequence

from .soliton_calibration import CalibrationReport, fit_affine_calibration
from .soliton_benchmark import CurveDiagnostics, diagnose_curve


@dataclass(frozen=True, slots=True)
class QualityGate:
    """Acceptance thresholds for a measured transfer curve."""
    min_samples: int = 5
    min_input_span: float = 1e-9
    min_output_span: float = 1e-6
    max_relative_rmse: float = 0.25
    require_monotonic: bool = True


@dataclass(frozen=True, slots=True)
class QualityResult:
    passed: bool
    reasons: tuple[str, ...]
    diagnostics: CurveDiagnostics
    gain_std_loo: float
    offset_std_loo: float


def evaluate_quality(measured: Sequence[tuple[float, float]],
                     calibration: CalibrationReport,
                     gate: QualityGate = QualityGate()) -> QualityResult:
    """Evaluate hard acceptance criteria and leave-one-out sensitivity."""
    diagnostics = diagnose_curve(measured, calibration)
    reasons: list[str] = []
    if diagnostics.samples < gate.min_samples:
        reasons.append(f"samples {diagnostics.samples} < minimum {gate.min_samples}")
    if diagnostics.input_span <= gate.min_input_span:
        reasons.append("input span is too small")
    if diagnostics.output_span <= gate.min_output_span:
        reasons.append("output span is too small")
    relative_rmse = diagnostics.rmse / max(diagnostics.output_span, 1e-12)
    if relative_rmse > gate.max_relative_rmse:
        reasons.append(f"relative RMSE {relative_rmse:.6g} exceeds {gate.max_relative_rmse:.6g}")
    if gate.require_monotonic and not diagnostics.monotonic:
        reasons.append("transfer curve is not monotonic")

    fits = [fit_affine_calibration(measured[:i] + measured[i + 1:],
                                   saturation=calibration.calibration.saturation)
            for i in range(len(measured)) if len(measured) > 2]
    gain_std = pstdev([fit.calibration.gain for fit in fits]) if fits else 0.0
    offset_std = pstdev([fit.calibration.offset for fit in fits]) if fits else 0.0
    return QualityResult(not reasons, tuple(reasons), diagnostics, gain_std, offset_std)


def require_quality(measured: Sequence[tuple[float, float]],
                    calibration: CalibrationReport,
                    gate: QualityGate = QualityGate()) -> QualityResult:
    """Raise a concise error if measured data fails the configured gate."""
    result = evaluate_quality(measured, calibration, gate)
    if not result.passed:
        raise ValueError("calibration quality gate failed: " + "; ".join(result.reasons))
    return result


def quality_report(result: QualityResult) -> str:
    """Render a stable Markdown acceptance report."""
    status = "PASS" if result.passed else "FAIL"
    reasons = "none" if not result.reasons else "; ".join(result.reasons)
    return (f"# Calibration Quality Gate: {status}\n\n"
            f"- Samples: {result.diagnostics.samples}\n"
            f"- Monotonic: {result.diagnostics.monotonic}\n"
            f"- Input span: {result.diagnostics.input_span:.9g}\n"
            f"- Output span: {result.diagnostics.output_span:.9g}\n"
            f"- RMSE: {result.diagnostics.rmse:.9g}\n"
            f"- Maximum absolute residual: {result.diagnostics.max_abs_residual:.9g}\n"
            f"- Leave-one-out gain standard deviation: {result.gain_std_loo:.9g}\n"
            f"- Leave-one-out offset standard deviation: {result.offset_std_loo:.9g}\n"
            f"- Reasons: {reasons}\n")
