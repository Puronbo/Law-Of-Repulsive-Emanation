"""soliton_peregrine_audit: the Peregrine breather of the NLSE twin,
measured -- not assumed.

The first-order Peregrine breather is the exact one-soliton solution of the
focusing NLS i u_z + (1/2)u_tt + |u|^2 u = 0 on a nonzero background
sqrt(P):

    u(t, z) = sqrt(P) e^{iPz} [ 1 - 4(1 + 2iP z) / (1 + 4P t^2 + 4P^2 z^2) ].

At z = 0 it is a localized dip whose center reaches three times the
background amplitude (power ratio 9); as z grows it "breathes" back toward
the background without radiating -- the exact bridge between the stable
fundamental soliton (no background) and modulational instability (flat
background, exponential sideband growth).

Certificates:

    L_peregrine_seed_shape        PASS/FAIL  the seed's center amplitude
                                    ratio is 3.0000 (+- 1e-3) and its
                                    profile matches the analytic form to
                                    RMS < 1e-3 over the breathing core.
    L_peregrine_curve_analytic    PASS/FAIL  the measured center-amplitude
                                    ratio along z in {0, 0.1, 0.25, 0.5,
                                    1, 2, 3} matches the analytic breather
                                    curve within 1% at every point.
    L_peregrine_breathes_back     PASS/FAIL  by z = 3 the center ratio has
                                    fallen from 3.0 to below 1.15: the
                                    breather returns toward the
                                    background (no radiating blowup, in
                                    contrast to the MI sideband).
    L_peregrine_wings_unperturbed PASS/FAIL  far from the center (|t| >=
                                    20) the field stays at the background
                                    sqrt(P) within 1% over the whole run:
                                    no energy is shed to the wings.
    L_peregrine_energy_conserved  PASS/FAIL  relative energy drift < 1e-11
                                    over the full propagation.
    L_peregrine_mass_neutral      PASS/FAIL  the breather carries zero net
                                    mass on the real line: the integrated
                                    defect over the finite window equals
                                    the closed-form window correction
                                    8L/(1 + L^2) (the missing tails), so
                                    the window-corrected defect is zero
                                    within tolerance.
    L_peregrine_center_phase0     PASS/FAIL  at z = 0 the center is
                                    exactly pi out of phase with the
                                    background sqrt(P) e^{iPz}.
    L_peregrine_phase_rotation    PASS/FAIL  the unfolded center phase
                                    (relative to the background) equals
                                    the analytic branch
                                    arg(4P^2 z^2 - 3 - 8iPz) at every
                                    sample z in {0.1, 0.25, 0.5, 1.0} to
                                    within 1e-3 rad.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_physics import (  # noqa: E402
    Fiber,
    energy,
    propagate,
)

_N = 8192
_L = 128.0
_P = 1.0
_STEPS = 800
_Z_POINTS = (0.0, 0.1, 0.25, 0.5, 1.0, 2.0, 3.0)
_WING_EDGE = 20.0
_SEED_RATIO = 3.0
_SEED_TOL = 1e-3
_CURVE_TOL = 0.01
_BREATHE_LIMIT = 1.15
_DRIFT_THRESH = 1e-11
_MASS_N = 16384
_MASS_L = 256.0
_MASS_STEPS = 1600
_MASS_TOL = 1e-4
_PHASE_Z = (0.1, 0.25, 0.5, 1.0)
_PHASE_TOL = 1e-3


def _grid() -> np.ndarray:
    return np.linspace(-_L / 2, _L / 2, _N, endpoint=False)


def _dt() -> float:
    return float(np.diff(_grid())[0])


def _peregrine(z: float) -> np.ndarray:
    t = _grid()
    return (np.sqrt(_P) * np.exp(1j * _P * z)
            * (1 - 4 * (1 + 2j * _P * z)
               / (1 + 4 * _P * t ** 2 + 4 * _P ** 2 * z ** 2)))


def _center_index() -> int:
    return int(np.argmin(np.abs(_grid())))


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


def _seed_shape_holds() -> bool:
    t = _grid()
    u0 = _peregrine(0.0)
    ci = _center_index()
    if abs(np.abs(u0[ci]) / np.sqrt(_P) - _SEED_RATIO) > _SEED_TOL:
        return False
    core = np.abs(t) <= 10.0
    analytic = np.abs(1 - 4 / (1 + 4 * _P * t[core] ** 2))
    measured = np.abs(u0[core]) / np.sqrt(_P)
    return float(np.sqrt(np.mean((measured - analytic) ** 2))) < _SEED_TOL


def _curve_analytic_holds() -> bool:
    u0 = _peregrine(0.0)
    ci = _center_index()
    for z in _Z_POINTS:
        u = u0 if z == 0.0 else propagate(u0, _dt(), z,
                                          fiber=Fiber(), steps=_STEPS)
        an = np.abs(_peregrine(z)[ci]) / np.sqrt(_P)
        me = np.abs(u[ci]) / np.sqrt(_P)
        if abs(me - an) / an > _CURVE_TOL:
            return False
    return True


def _breathes_back_holds() -> bool:
    u0 = _peregrine(0.0)
    ci = _center_index()
    start = np.abs(u0[ci]) / np.sqrt(_P)
    u3 = propagate(u0, _dt(), 3.0, fiber=Fiber(), steps=_STEPS)
    end = np.abs(u3[ci]) / np.sqrt(_P)
    return start > 2.9 and end < _BREATHE_LIMIT


def _wings_unperturbed_holds() -> bool:
    t = _grid()
    wing = np.abs(t) >= _WING_EDGE
    u0 = _peregrine(0.0)
    for z in _Z_POINTS[1:]:
        u = propagate(u0, _dt(), z, fiber=Fiber(), steps=_STEPS)
        if np.max(np.abs(np.abs(u[wing]) - np.sqrt(_P))) > 0.01 * np.sqrt(_P):
            return False
    return True


def _energy_conserved_holds() -> bool:
    u0 = _peregrine(0.0)
    e0 = energy(u0, _dt())
    e3 = energy(propagate(u0, _dt(), 3.0, fiber=Fiber(), steps=_STEPS),
                _dt())
    return abs(e3 - e0) / e0 < _DRIFT_THRESH


def _mass_neutral_holds() -> bool:
    t = np.linspace(-_MASS_L / 2, _MASS_L / 2, _MASS_N, endpoint=False)
    dt = float(np.diff(t)[0])
    u0 = np.sqrt(_P) * (1 - 4 / (1 + 4 * _P * t ** 2))
    defect = float(np.sum(np.abs(u0) ** 2 - _P) * dt)
    correction = 8 * _MASS_L / (1 + _MASS_L ** 2)
    return abs(defect - correction) <= _MASS_TOL


def _center_phase0_holds() -> bool:
    u0 = _peregrine(0.0)
    ci = _center_index()
    ph = np.angle(u0[ci] * np.exp(-1j * _P * 0.0))
    return abs(abs(ph) - np.pi) <= 1e-3


def _phase_rotation_holds() -> bool:
    u0 = _peregrine(0.0)
    ci = _center_index()
    for z in _PHASE_Z:
        u = propagate(u0, _dt(), z, fiber=Fiber(), steps=_STEPS)
        measured = np.angle(u[ci] * np.exp(-1j * _P * z))
        analytic = np.angle((4 * _P ** 2 * z ** 2 - 3) - 8j * _P * z)
        if abs(measured - analytic) > _PHASE_TOL:
            return False
    return True


def peregrine_certificates() -> list[dict[str, object]]:
    return [
        _certify("L_peregrine_seed_shape",
                 {"domain": f"N = {_N}, L = {_L}, P = {_P}",
                  "law": "center amplitude ratio 3.0000 +- 1e-3 and "
                         "profile RMS < 1e-3 over the breathing core",
                  "measured_on": "exact seed vs analytic profile",
                  "source": "analytic Peregrine at z = 0"},
                 _seed_shape_holds),
        _certify("L_peregrine_curve_analytic",
                 {"domain": "center amplitude ratio along z in "
                            f"{tuple(_Z_POINTS)}",
                  "law": f"measured matches the analytic breather curve "
                         f"within {_CURVE_TOL} at every point",
                  "measured_on": "SSFM propagation vs the closed-form "
                                 "breather"},
                 _curve_analytic_holds),
        _certify("L_peregrine_breathes_back",
                 {"domain": "center ratio at z = 3.0",
                  "law": "the breather returns from 3.0 toward the "
                         f"background (final ratio < {_BREATHE_LIMIT}) -- "
                         "no radiating blowup, in contrast to the MI "
                         "sideband on a flat background",
                  "measured_on": "center amplitude ratio at z = 0 vs "
                                 "z = 3"},
                 _breathes_back_holds),
        _certify("L_peregrine_wings_unperturbed",
                 {"domain": f"|t| >= {_WING_EDGE} over all z in "
                            f"{tuple(_Z_POINTS[1:])}",
                  "law": "the far wings stay at the background sqrt(P) "
                         "within 1% -- no energy is shed to the wings",
                  "measured_on": "max deviation of the wing amplitude "
                                 "from sqrt(P) per z"},
                 _wings_unperturbed_holds),
        _certify("L_peregrine_energy_conserved",
                 {"domain": "z = 3 propagation at 800 split-steps",
                  "law": f"relative energy drift < {_DRIFT_THRESH}",
                  "measured_on": "total energy before vs after"},
                 _energy_conserved_holds),
        _certify("L_peregrine_mass_neutral",
                 {"domain": f"window L = {_MASS_L}, N = {_MASS_N}",
                  "law": "the breather carries zero net mass: the window "
                         "defect exactly equals the closed-form tail "
                         "correction 8L/(1 + L^2) (both far tails), so "
                         "the line integral of |u|^2 - P vanishes",
                  "measured_on": "windowed defect vs 8L/(1 + L^2) "
                                 "to within "
                                 f"1e-{int(-np.log10(_MASS_TOL))}"},
                 _mass_neutral_holds),
        _certify("L_peregrine_center_phase0",
                 {"domain": "center phase at z = 0",
                  "law": "the center sits exactly pi out of phase with "
                         "the background sqrt(P) e^{iPz}",
                  "measured_on": "angle(u_center * e^{-iPz})"},
                 _center_phase0_holds),
        _certify("L_peregrine_phase_rotation",
                 {"domain": f"z in {_PHASE_Z}",
"law": "the unfolded center phase relative to the "
                             "background equals the analytic branch "
                             "arg(4P^2 z^2 - 3 - 8iPz) at every sample "
                             f"to within {_PHASE_TOL} rad",
                  "measured_on": "angle(u_center * e^{-iPz}) vs "
                                 "arg(4P^2 z^2 - 3 - 8iPz)"},
                 _phase_rotation_holds),
    ]


def _center_curve() -> list[dict[str, float]]:
    u0 = _peregrine(0.0)
    ci = _center_index()
    rows = []
    for z in _Z_POINTS:
        u = u0 if z == 0.0 else propagate(u0, _dt(), z,
                                          fiber=Fiber(), steps=_STEPS)
        rows.append({"z": z,
                     "analytic": float(np.abs(_peregrine(z)[ci])
                                       / np.sqrt(_P)),
                     "measured": float(np.abs(u[ci]) / np.sqrt(_P))})
    return rows


if __name__ == "__main__":
    for c in peregrine_certificates():
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("  z    analytic  measured   reldiff")
    for r in _center_curve():
        print("  %.2f  %.4f    %.4f    %.2e" % (
            r["z"], r["analytic"], r["measured"],
            abs(r["measured"] - r["analytic"]) / r["analytic"]))