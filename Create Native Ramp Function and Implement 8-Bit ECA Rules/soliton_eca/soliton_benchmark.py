"""Measured-curve ingestion and deterministic soliton hardware benchmarking."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Iterable, Sequence

from .soliton_calibration import CalibrationReport, fit_affine_calibration
from .soliton_hardware import CalibratedSolitonLayer, Perturbation, relative_error


@dataclass(frozen=True, slots=True)
class CurveDiagnostics:
    samples: int
    monotonic: bool
    input_span: float
    output_span: float
    rmse: float
    max_abs_residual: float
    saturation_fraction: float


def load_transfer_csv(path: str | Path, *, input_column: str = "input",
                      output_column: str = "output") -> list[tuple[float, float]]:
    """Load a two-column transfer curve without silently accepting bad rows."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or input_column not in reader.fieldnames or output_column not in reader.fieldnames:
            raise ValueError(f"CSV must contain {input_column!r} and {output_column!r} columns")
        rows: list[tuple[float, float]] = []
        for line, row in enumerate(reader, start=2):
            try:
                x, y = float(row[input_column]), float(row[output_column])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"invalid numeric transfer point at CSV line {line}") from exc
            rows.append((x, y))
    if len(rows) < 2:
        raise ValueError("transfer curve requires at least two rows")
    return rows


def diagnose_curve(measured: Sequence[tuple[float, float]],
                    calibration: CalibrationReport) -> CurveDiagnostics:
    """Quantify monotonicity, range, fit error, and near-saturation behavior."""
    if len(measured) != calibration.samples or len(measured) < 2:
        raise ValueError("measured points and calibration report do not match")
    ordered = sorted((float(x), float(y)) for x, y in measured)
    outputs = [y for _, y in ordered]
    residuals = [calibration.calibration.gain * x + calibration.calibration.offset - y
                 for x, y in ordered]
    sat = calibration.calibration.saturation
    saturated = sum(abs(y) >= sat for y in outputs)
    return CurveDiagnostics(
        samples=len(ordered),
        monotonic=all(b >= a for a, b in zip(outputs, outputs[1:])),
        input_span=ordered[-1][0] - ordered[0][0],
        output_span=max(outputs) - min(outputs),
        rmse=calibration.rmse,
        max_abs_residual=max(abs(r) for r in residuals),
        saturation_fraction=saturated / len(outputs),
    )


def calibrate_csv(path: str | Path, *, saturation: float = 1.0) -> tuple[list[tuple[float, float]], CalibrationReport, CurveDiagnostics]:
    """Load, fit, and diagnose a measured transfer curve."""
    measured = load_transfer_csv(path)
    report = fit_affine_calibration(measured, saturation=saturation)
    return measured, report, diagnose_curve(measured, report)


def impairment_sweep(layer: CalibratedSolitonLayer, inputs: Sequence[float], *,
                     gain_errors: Sequence[float] = (-0.1, 0.0, 0.1),
                     timing_jitters: Sequence[int] = (0, 1),
                     crosstalks: Sequence[float] = (0.0, 0.1),
                     packet_loss: Sequence[bool] = (False, True)) -> list[dict[str, float]]:
    """Run a reproducible Cartesian sweep and report normalized output error."""
    ideal = layer.forward(inputs)
    results: list[dict[str, float]] = []
    for gain, jitter, cross, dropped in product(gain_errors, timing_jitters, crosstalks, packet_loss):
        impairment = Perturbation(gain_error=gain, timing_jitter=jitter,
                                  crosstalk=cross, drop_positive=dropped)
        try:
            observed = layer.forward(inputs, impairment=impairment)
            error = relative_error(ideal, observed)
        except ValueError as exc:
            if "arrival tick" not in str(exc):
                raise
            error = 1.0
        results.append({"gain_error": float(gain), "timing_jitter": float(jitter),
                        "crosstalk": float(cross), "packet_loss": float(dropped),
                        "relative_error": float(error)})
    return results


def benchmark_summary(results: Sequence[dict[str, float]]) -> dict[str, float]:
    """Summarize a sweep with mean, worst, and timing-failure counts."""
    if not results:
        raise ValueError("results must not be empty")
    errors = [row["relative_error"] for row in results]
    failures = sum(row["timing_jitter"] != 0 and row["relative_error"] == 1.0 for row in results)
    return {"cases": float(len(results)), "mean_error": sum(errors) / len(errors),
            "worst_error": max(errors), "timing_rejections": float(failures)}
