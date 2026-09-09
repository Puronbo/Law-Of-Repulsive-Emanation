"""soliton_mi_audit: modulational instability in the NLSE twin, measured --
not assumed.

A plane wave sqrt(P) seeded with a small periodic perturbation at spatio-
temporal frequency omega grows exponentially if omega < 2*sqrt(P) -- the
modulational-instability band.  The analytic power gain for the focusing
NLS i u_z + (1/2)u_tt + |u|^2 u = 0 at pump power P is

    g(omega) = 2*omega*sqrt(P - omega^2/4)   for omega < 2*sqrt(P),

with zero gain above the band edge and its peak near omega = sqrt(2P),
where g ~ 2P.  Because a real cosine seed excites both the growing and the
decaying quadrature, the exponent is read from the late-time log-linear
tail after the decaying component has died out.

Certificates:

    L_mi_gain_matches_analytic   PASS/FAIL  for five modes inside the band,
                                    the measured power gain matches the
                                    analytic g(omega) within 9%.
    L_mi_band_edge               PASS/FAIL  a mode below the edge (omega =
                                    1.96, near 2*sqrt(P)) still amplifies;
                                    a mode above the edge (omega = 2.16)
                                    has zero gain.
    L_mi_peak_location           PASS/FAIL  the sampled gain curve exceeds
                                    1.9 and the peak mode sits within two
                                    frequency bins of omega* = sqrt(2P).
    L_mi_soliton_stability_island  PASS/FAIL  the SAME seed placed on the
                                    fundamental soliton instead of the CW
                                    background stays flat (sideband ratio
                                    ~ 1) while the CW sideband grows by
                                    >= 100x over z = 5 -- the soliton is
                                    the stability island of the same
                                    equation.
    L_mi_energy_conserved        PASS/FAIL  relative energy drift < 1e-11
                                    in every propagated run.
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
    fundamental_soliton,
    propagate,
)

_N = 4096
_L = 64.0
_P = 1.0
_EPS = 1e-3
_STEPS = 400
_GAIN_TOL = 0.09
_PEAK_FLOOR = 1.9
_DRIFT_THRESH = 1e-11
_FIT_WINDOWS = {4: (2.0, 9.0), 6: (2.5, 7.0), 8: (2.0, 5.5),
                12: (1.5, 4.0), 16: (1.25, 3.0)}
_BAND_MODES = {20: (1.0, 2.5), 22: (1.0, 2.0)}


def _grid() -> np.ndarray:
    return np.linspace(-_L / 2, _L / 2, _N, endpoint=False)


def _dt() -> float:
    return float(np.diff(_grid())[0])


def _sideband(k: int, field: np.ndarray) -> float:
    spec = np.abs(np.fft.fft(field)) ** 2
    return float(spec[k] + spec[_N - k])


def _gain(k: int, window: tuple[float, float]) -> float:
    t = _grid()
    om = 2 * np.pi * k / _L
    u0 = np.sqrt(_P) + _EPS * np.cos(om * t) + 0j
    base = _sideband(k, u0)
    z0, z1 = window
    zs = np.round(np.arange(z0, z1, 0.25), 3)
    vals = []
    for z in zs:
        u = propagate(u0, _dt(), z, fiber=Fiber(), steps=_STEPS)
        vals.append(np.log(max(_sideband(k, u) - base, 1e-40)))
    coef = np.polyfit(zs, np.array(vals), 1)
    return float(coef[0])


def _analytic_gain(k: int) -> float:
    om = 2 * np.pi * k / _L
    return 2.0 * om * np.sqrt(_P - om * om / 4.0)


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


def _gain_matches_holds(measured: dict[int, float]) -> bool:
    for k in _FIT_WINDOWS:
        g_an = _analytic_gain(k)
        if g_an <= 0:
            continue
        if abs(measured[k] - g_an) / g_an > _GAIN_TOL:
            return False
    return True


def _band_edge_holds(measured: dict[int, float]) -> bool:
    g_below = measured[20]
    g_above = measured[22]
    if not (g_below >= 0.2 and g_above <= 1e-3):
        return False
    return True


def _peak_location_holds(measured: dict[int, float]) -> bool:
    peak_k = max(_FIT_WINDOWS, key=lambda k: measured[k])
    if measured[peak_k] < _PEAK_FLOOR:
        return False
    om_star = np.sqrt(2 * _P)
    om_peak = 2 * np.pi * peak_k / _L
    dk = 2 * np.pi / _L
    return abs(om_peak - om_star) <= 2 * dk


def _soliton_island_holds() -> bool:
    t = _grid()
    om = 2 * np.pi * 8 / _L
    cw0 = 1.0 + _EPS * np.cos(om * t) + 0j
    sol0 = fundamental_soliton(t) + _EPS * np.cos(om * t) + 0j
    cw5 = propagate(cw0, _dt(), 5.0, fiber=Fiber(), steps=_STEPS)
    sol5 = propagate(sol0, _dt(), 5.0, fiber=Fiber(), steps=_STEPS)
    cw_ratio = _sideband(8, cw5) / _sideband(8, cw0)
    sol_ratio = _sideband(8, sol5) / _sideband(8, sol0)
    return cw_ratio >= 100.0 and sol_ratio <= 1.1


def _energy_conserved_holds() -> bool:
    t = _grid()
    om = 2 * np.pi * 8 / _L
    for u0 in (1.0 + _EPS * np.cos(om * t) + 0j,
               fundamental_soliton(t) + _EPS * np.cos(om * t) + 0j):
        u5 = propagate(u0, _dt(), 5.0, fiber=Fiber(), steps=_STEPS)
        e0, e1 = energy(u0, _dt()), energy(u5, _dt())
        if abs(e1 - e0) / e0 >= _DRIFT_THRESH:
            return False
    return True


def mi_certificates(measured: dict[int, float]) -> list[dict[str, object]]:
    return [
        _certify("L_mi_gain_matches_analytic",
                 {"domain": f"modes k in {{{', '.join(map(str, _FIT_WINDOWS))}}}, "
                            f"pump P = {_P}, z-window per mode (late-time "
                            "log-linear tail)",
                  "law": "|measured gain - 2*om*sqrt(P - om^2/4)| / analytic "
                         f"<= {_GAIN_TOL}",
                  "measured_on": "log-linear slope of the far-sideband "
                                 "power in the fit window"},
                 lambda: _gain_matches_holds(measured)),
        _certify("L_mi_band_edge",
                 {"domain": f"mode k=20 (om = {2*np.pi*20/_L:.3f} < "
                            f"2*sqrt(P) = {2*np.sqrt(_P):.3f}) and "
                            f"k=22 (om = {2*np.pi*22/_L:.3f} > edge)",
                  "law": "below-edge mode amplifies (gain >= 0.2) while "
                         "the above-edge mode has bounded-zero gain "
                         "(<= 1e-3)",
                  "measured_on": "log-linear slope per mode"},
                 lambda: _band_edge_holds(measured)),
        _certify("L_mi_peak_location",
                 {"domain": f"sampled gain over k={min(_FIT_WINDOWS)}.."
                            f"{max(_FIT_WINDOWS)}",
                  "law": "peak gain >= 1.9 (analytic g_max = 2P = 2) and "
                         "the peak mode sits within two frequency bins of "
                         "om* = sqrt(2P)",
                  "measured_on": "measured gain curve vs analytic peak "
                                 "and location"},
                 lambda: _peak_location_holds(measured)),
        _certify("L_mi_soliton_stability_island",
                 {"domain": "identical seed at k=8 on the CW background "
                            "vs on the fundamental soliton, z = 5",
                  "law": "the CW sideband grows by >= 100x while the "
                         "soliton sideband stays within 10% of its seed "
                         "-- the soliton is the stability island of the "
                         "same equation",
                  "honest_check": "no flat background means no "
                                  "phase-matched four-wave growth on the "
                                  "soliton",
                  "measured_on": "sideband power ratio at z = 5 vs z = 0"},
                 _soliton_island_holds),
        _certify("L_mi_energy_conserved",
                 {"domain": "CW and soliton bake-off runs, z = 5, 400 "
                            "steps",
                  "law": f"relative energy drift < {_DRIFT_THRESH}",
                  "measured_on": "total energy before vs after "
                                 "propagation"},
                 _energy_conserved_holds),
    ]


def _gain_table() -> str:
    measured = {}
    for k, window in _FIT_WINDOWS.items():
        measured[k] = _gain(k, window)
    for k, window in _BAND_MODES.items():
        measured[k] = _gain(k, window)
    rows = ["  k    om       g_measured  g_analytic   ratio"]
    for k in sorted(measured):
        om = 2 * np.pi * k / _L
        g_an = _analytic_gain(k) if om < 2 * np.sqrt(_P) else 0.0
        ratio = measured[k] / g_an if g_an else float("inf")
        rows.append("  %2d  %6.3f  %10.4f  %10.4f  %6.3f" % (
            k, om, measured[k], g_an, ratio))
    return "\n".join(rows)


if __name__ == "__main__":
    measured = {}
    for k, window in _FIT_WINDOWS.items():
        measured[k] = _gain(k, window)
    for k, window in _BAND_MODES.items():
        measured[k] = _gain(k, window)
    for c in mi_certificates(measured):
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print(_gain_table())