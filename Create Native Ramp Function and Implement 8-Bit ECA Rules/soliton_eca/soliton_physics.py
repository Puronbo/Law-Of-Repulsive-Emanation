"""Numerical soliton digital twin using a symmetric split-step Fourier method."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True, slots=True)
class Fiber:
    """Propagation parameters in SI units."""
    beta2: float = -1.0
    gamma: float = 1.0
    loss: float = 0.0


def fundamental_soliton(t: np.ndarray, *, width: float = 1.0,
                        amplitude: float = 1.0) -> np.ndarray:
    """Return a transform-limited sech pulse."""
    return amplitude / np.cosh(t / width)


def _fft_frequencies(size: int, dt: float) -> np.ndarray:
    return 2.0 * np.pi * np.fft.fftfreq(size, d=dt)


def propagate(field: np.ndarray, dt: float, distance: float, *,
              fiber: Fiber = Fiber(), steps: int = 100) -> np.ndarray:
    """Propagate a complex envelope with symmetric SSFM.

    The model includes second-order dispersion, Kerr self-phase modulation,
    and optional linear power loss. Raman and higher-order dispersion are
    intentionally omitted until their coefficients are supplied.
    """
    if field.ndim != 1 or field.size < 8:
        raise ValueError("field must be a 1-D array with at least 8 samples")
    if dt <= 0 or distance < 0 or steps < 1:
        raise ValueError("dt must be positive, distance non-negative, steps positive")
    out = np.asarray(field, dtype=np.complex128).copy()
    dz = distance / steps
    omega = _fft_frequencies(out.size, dt)
    # Linear operator for dA/dz = -i beta2/2 d2A/dt2 + i gamma |A|^2 A.
    linear_half = np.exp((1j * fiber.beta2 * omega**2 / 2.0 - fiber.loss / 2.0) * dz / 2.0)
    for _ in range(steps):
        out = np.fft.ifft(np.fft.fft(out) * linear_half)
        out *= np.exp(1j * fiber.gamma * np.abs(out) ** 2 * dz)
        out = np.fft.ifft(np.fft.fft(out) * linear_half)
    return out


def relative_power_error(before: np.ndarray, after: np.ndarray) -> float:
    """Relative L2 error between power envelopes, useful for soliton invariance."""
    p0, p1 = np.abs(before) ** 2, np.abs(after) ** 2
    scale = max(float(np.linalg.norm(p0)), np.finfo(float).eps)
    return float(np.linalg.norm(p1 - p0) / scale)


def energy(field: np.ndarray, dt: float) -> float:
    """Numerical pulse energy integral."""
    if dt <= 0:
        raise ValueError("dt must be positive")
    return float(np.sum(np.abs(field) ** 2) * dt)


def soliton_validation(*, size: int = 2048, span: float = 40.0,
                       width: float = 1.0, distance: float = 1.0,
                       steps: int = 200) -> dict[str, float]:
    """Run a normalized fundamental-soliton invariance check.

    For beta2=-1, gamma=1, and A(t)=sech(t), the normalized soliton length is
    one. The returned power error and energy drift are acceptance metrics.
    """
    if size < 64 or span <= 0:
        raise ValueError("size must be >= 64 and span positive")
    t = np.linspace(-span / 2, span / 2, size, endpoint=False)
    dt = float(t[1] - t[0])
    pulse = fundamental_soliton(t, width=width)
    propagated = propagate(pulse, dt, distance, fiber=Fiber(beta2=-1.0, gamma=1.0), steps=steps)
    e0, e1 = energy(pulse, dt), energy(propagated, dt)
    return {"relative_power_error": relative_power_error(pulse, propagated),
            "relative_energy_drift": abs(e1 - e0) / e0,
            "energy_before": e0, "energy_after": e1}
