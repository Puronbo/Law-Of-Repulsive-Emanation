"""Standalone validator for the acquisition-order drift diagnostics.

Checks `soliton_drift.py` over hand-constructed captures, all measured:
    1. NO DRIFT  : an ideal transfer curve (zero residual) reports
                   slope 0, normalized slope 0, and passes the
                   default 0.01 threshold.
    2. DRIFT      : residuals growing linearly with acquisition index
                   are caught: the fitted slope equals the exact
                   forced value (within float noise), the direction
                   matches, and the normalized slope trips the gate.
    3. NORMALIZE  : normalized_slope == slope / output_span exactly.
    4. VALIDATION : fewer than two measurements, a non-positive
                   output span, and a negative threshold all raise
                   ValueError.

Exit 0 iff all checks pass; prints each measured outcome.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from soliton_eca import (  # noqa: E402
    ActivationCalibration, CalibrationReport, drift_passes,
    estimate_drift,
)


def _report() -> CalibrationReport:
    return CalibrationReport(
        ActivationCalibration(gain=2.5, offset=-1.0, saturation=8.0),
        rmse=0.0, samples=8)


def _check_no_drift():
    calibration = _report()
    measurements = []
    for step, x in enumerate((-2.0, -1.0, 0.0, 1.0, 2.0)):
        measurements.append((x, calibration.calibration.gain * x
                             + calibration.calibration.offset + 0.0 * step))
    diag = estimate_drift(measurements, calibration)
    assert diag.samples == len(measurements)
    assert abs(diag.residual_slope) < 1e-12, \
        "no-drift slope %r" % diag.residual_slope
    assert abs(diag.normalized_slope) < 1e-12
    assert drift_passes(diag) is True
    print("  no drift: residual slope 0.0, %d samples, passes gate"
          % diag.samples)
    return True


def _check_drift_detected():
    calibration = _report()
    k = 0.05  # forced residual slope per acquisition step (exact)
    measurements = []
    for step, x in enumerate((-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0)):
        y = (calibration.calibration.gain * x
             + calibration.calibration.offset + k * step)
        measurements.append((x, y))
    diag = estimate_drift(measurements, calibration, output_span=1.0)
    # residual r_i = gain*x + offset - y = -k*i -> slope == -k exactly
    assert abs(diag.residual_slope + k) < 1e-12, \
        "slope %r" % diag.residual_slope
    assert diag.residual_slope < 0 and diag.normalized_slope < 0
    assert diag.normalized_slope == diag.residual_slope / 1.0
    assert drift_passes(diag) is False
    print("  drift caught: fitted slope %.3f/step trips the 0.01 gate"
          % diag.residual_slope)
    return True


def _check_validation():
    calibration = _report()
    try:
        estimate_drift([(0.0, 0.0)], calibration)
    except ValueError:
        pass
    else:
        raise AssertionError("single measurement accepted")
    try:
        estimate_drift([(0.0, 0.0), (1.0, 1.0)], calibration,
                       output_span=0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero output span accepted")
    from soliton_eca import DriftDiagnostics
    try:
        drift_passes(DriftDiagnostics(2, 0.0, 0.0, 0.0, 0.0),
                     max_normalized_slope=-0.1)
    except ValueError:
        pass
    else:
        raise AssertionError("negative threshold accepted")
    print("  validation: short captures, bad span, bad threshold rejected")
    return True


def main():
    print("soliton drift validator (acquisition-order residual slope)")
    ok = _check_no_drift() and _check_drift_detected() and _check_validation()
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())