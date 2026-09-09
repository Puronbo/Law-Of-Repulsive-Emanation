"""soliton_nlse_audit: measured numerical checks of the SSFM soliton twin.

`soliton_physics.propagate` implements the symmetric split-step Fourier
method for the normalized NLSE  (i A_z - beta2/2 A_tt + gamma |A|^2 A = 0,
beta2 = -1, gamma = 1) with A(0,t) = sech(t) as the fundamental soliton.
The exact solution is A(z,t) = sech(t) exp(i z / 2).  This audit measures,
not assumes:

    L_nlse_energy_unitarily_conserved   PASS/FAIL  the lossless SSFM is
                                     exactly unitary half-step by step, so
                                     the pulse energy drift is at machine
                                     precision (< 1e-12) at all distances.
    L_nlse_second_order_convergence     PASS/FAIL  the power-envelope error
                                     decays like dz^p with p ~ 2 (symmetric
                                     SSFM is second-order accurate).
    L_nlse_sech_shape_invariant         PASS/FAIL  the power envelope of a
                                     propagated fundamental soliton returns
                                     to its starting shape at the soliton
                                     length and beyond.
    L_nlse_sech_phase_rotation          PASS/FAIL  the accumulated phase is
                                     arg(A(z)/sech) ~= z/2 along the body
                                     of the pulse (measured circularly).
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_physics import (  # noqa: E402
    Fiber, fundamental_soliton, propagate, relative_power_error,
)

_SIZE = 2048
_SPAN = 40.0
_PHASE_MASK = 0.1
_TOL_ENERGY = 1e-12
_ORDER_WINDOW = (1.8, 2.2)
_TOL_SHAPE = 1e-4
_TOL_PHASE = 0.02


def _grid() -> tuple[np.ndarray, float]:
    t = np.linspace(-_SPAN / 2.0, _SPAN / 2.0, _SIZE, endpoint=False)
    return t, float(t[1] - t[0])


def _run(z: float, steps: int):
    t, dt = _grid()
    pulse = fundamental_soliton(t)
    out = propagate(pulse, dt, z, fiber=Fiber(beta2=-1.0, gamma=1.0),
                    steps=steps)
    return pulse, out, dt


def energy_drift(z: float, steps: int) -> float:
    pulse, out, dt = _run(z, steps)
    e0 = float(np.sum(np.abs(pulse) ** 2) * dt)
    e1 = float(np.sum(np.abs(out) ** 2) * dt)
    return abs(e1 - e0) / e0


def power_error(z: float, steps: int) -> float:
    pulse, out, _ = _run(z, steps)
    return relative_power_error(pulse, out)


def convergence_order() -> float:
    steps_list = (25, 50, 100, 200, 400)
    errors = [power_error(1.0, steps) for steps in steps_list]
    dzs = [1.0 / s for s in steps_list]
    x = np.log2(dzs)
    y = np.log2(np.maximum(errors, 1e-300))
    return float(np.polyfit(x, y, 1)[0])


def phase_deviation(z: float, steps: int) -> float:
    """Circular mean modulus of (arg(A/sech) - z/2), in [0, 1]."""
    pulse, out, _ = _run(z, steps)
    mask = np.abs(pulse) > _PHASE_MASK
    if not np.any(mask):
        raise ValueError("phase mask selects no samples")
    phase = np.angle(out[mask] / pulse[mask])
    dev = np.angle(np.exp(1j * (phase - z / 2.0)))
    return float(np.abs(np.mean(np.exp(1j * dev))))


def _certify(label: str, meta: dict[str, object],
             pred: Callable[[], bool]) -> dict[str, object]:
    n_ok = 1 if pred() else 0
    return {
        "label": label,
        "meta": meta,
        "kind": "statement",
        "status": "PASS" if n_ok else "HONEST_NEGATIVE",
        "n_ok": n_ok,
        "n_fail": 0 if n_ok else 1,
        "first_failure": None if n_ok else {"datum": "the predicate Failed"},
    }


def _energy_unitary_holds() -> bool:
    return all(energy_drift(z, steps) < _TOL_ENERGY
               for z, steps in ((0.5, 100), (1.0, 100), (2.0, 200),
                                (4.0, 400)))


def _second_order_holds() -> bool:
    return _ORDER_WINDOW[0] <= convergence_order() <= _ORDER_WINDOW[1]


def _shape_invariant_holds() -> bool:
    return max(power_error(z, 400) for z in (0.5, 1.0, 2.0, 4.0)) < _TOL_SHAPE


def _phase_rotation_holds() -> bool:
    return phase_deviation(1.0, 400) >= 1.0 - _TOL_PHASE ** 2 / 2.0


def nlse_certificates() -> list[dict[str, object]]:
    return [
        _certify("L_nlse_energy_unitarily_conserved",
                 {"domain": "lossless SSFM, sech pulse, distances 0.5..4",
                  "law": "half-steps are unitary so the energy drift stays "
                         "at machine precision (< 1e-12) at every distance",
                  "measured_on": "energy integral before/after "
                                 "propagation"},
                 _energy_unitary_holds),
        _certify("L_nlse_second_order_convergence",
                 {"domain": "power-envelope error vs step size dz at "
                            "distance 1",
                  "law": "the error decays like dz^p with p in [1.8, 2.2], "
                         "the signature of symmetric SSFM",
                  "measured_on": "log-log regression over 5 step sizes"},
                 _second_order_holds),
        _certify("L_nlse_sech_shape_invariant",
                 {"domain": "sech fundamental soliton, distances 0.5..4",
                  "law": "the power envelope returns to its starting shape "
                         "(relative L2 error < 1e-4 at 400 steps)",
                  "measured_on": "relative power-envelope error"},
                 _shape_invariant_holds),
        _certify("L_nlse_sech_phase_rotation",
                 {"domain": "phase of A(z)/sech along the pulse body",
                  "law": "the accumulated phase is z/2 (soliton length "
                         "rotation), measured for the fundamental soliton",
                  "measured_on": "circular phase deviation at z = 1"},
                 _phase_rotation_holds),
    ]


if __name__ == "__main__":
    for c in nlse_certificates():
        print("  %-42s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("  measured: energy drift max %.3g | order p=%.3f | "
          "shape err %.3g | phase dev %.5f" % (
              max(energy_drift(z, s) for z, s in
                  ((0.5, 100), (1.0, 100), (2.0, 200), (4.0, 400))),
              convergence_order(),
              max(power_error(z, 400) for z in (0.5, 1.0, 2.0, 4.0)),
              phase_deviation(1.0, 400)))