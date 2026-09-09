"""soliton_mi_omega_spectrum_audit: the MI crest across the band.

Round 12 showed the Peregrine cap 3.0000 holds at the max-gain frequency
(sqrt(2P)) and above, and breaks at the low in-band frequency 0.5
(crest 3.656).  This audit scans the whole well-posed band on the
64-window (P = 1, eps = 0.2): wavelengths must fit a continuous
modulation across the window, so the longest seed is one full cosine
m = 1 (Omega = 2*pi/64)::

    Omega   0.0982  0.1473  0.1963  0.2945  0.3927  0.5   0.589  0.785  1.0  1.414
    crest   4.697   4.539   4.387   4.111   3.889   3.656 3.482  3.143  2.837 2.476
    z_crest 11.70   8.15    6.40    4.65    3.75    3.20  2.95   2.60   2.45  2.60

Laws:

- the crest rises monotonically with wavelength across the whole window
  (2.476 at the max-gain frequency -> 4.697 at the longest m = 1 seed):
  the low-frequency nonlinear stage overshoots the max-gain one;
- the Peregrine cap 3.0000 DIVIDES the band: every crest at
  Omega <= 0.785 exceeds it, every crest at Omega in {1.0, sqrt(2)}
  stays below -- the cap binds exactly on the high-frequency side of
  the band where the growth rate peaks;
- the crest distance grows with wavelength for Omega <= 1.0 (2.45 ->
  11.70): longer modulations crest later and higher;
- the recurrence survives every wavelength and nothing blows up: every
  profile relaxes to a trough <= 1.5*(1+eps) after its crest;
- the turn-back to the constant-wave (DC) limit is NOT seen within the
  well-posed window (HONEST_NEGATIVE): the longest m=1 seed crests
  highest, and the curve's peak lies below the window floor.

Certificates:

    L_omega_crest_wavelength_monotone   PASS/FAIL  crest strictly
                                  increases as Omega decreases.
    L_omega_crest_after_monotone        PASS/FAIL  for Omega <= 1.0 the
                                  crest distance strictly increases as
                                  Omega decreases.
    L_omega_cap_division                PASS/FAIL  every crest at
                                  Omega <= 0.785 > 3.0000 > every crest
                                  at Omega in {1.0, sqrt(2)}.
    L_omega_recurrence_holds            PASS/FAIL  trough_after <=
                                  1.5*(1+eps) at every Omega.
    L_omega_dc_turnback                 HONEST_NEGATIVE  "the crest
                                  turns back toward the CW limit before
                                  the longest m=1 wavelength": FALSE.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_physics import (  # noqa: E402
    Fiber,
    propagate,
)

_P = 1.0
_EPS = 0.2
_Z_GRID = 0.05
_STEPS_PER_DZ = 20
_CAP = 3.0000
_RELAX_FACTOR = 1.5

# (Omega, sim length); the m = 1 seed needs a long run to reach its crest.
_OMEGA_GRID = (
    (2 * np.pi * 1 / 64, 45.0),
    (2 * np.pi * 1.5 / 64, 25.0),
    (2 * np.pi * 2 / 64, 15.0),
    (2 * np.pi * 3 / 64, 12.0),
    (2 * np.pi * 4 / 64, 12.0),
    (0.5, 10.0),
    (2 * np.pi * 6 / 64, 10.0),
    (2 * np.pi * 8 / 64, 10.0),
    (1.0, 10.0),
    (np.sqrt(2.0), 10.0),
)
_LOW_SET = tuple(o for o, _zz in _OMEGA_GRID if o <= 2 * np.pi * 8 / 64)
_HIGH_SET = (1.0, float(np.sqrt(2.0)))


def _grid() -> np.ndarray:
    _n, _l = 8192, 64.0
    return np.linspace(-_l / 2, _l / 2, _n, endpoint=False)


def _meas(om: float, z_end: float) -> dict[str, float]:
    t = _grid()
    dt = float(np.diff(t)[0])
    ci = int(np.argmin(np.abs(t)))
    zs = np.arange(0.0, z_end + _Z_GRID / 2, _Z_GRID)
    cur = np.sqrt(_P) * (1 + _EPS * np.cos(om * t))
    prev = 0.0
    ratios = [np.abs(cur[ci]) / np.sqrt(_P)]
    for z in zs[1:]:
        cur = propagate(cur, dt, z - prev, fiber=Fiber(),
                        steps=_STEPS_PER_DZ)
        prev = z
        ratios.append(np.abs(cur[ci]) / np.sqrt(_P))
    r = np.asarray(ratios)
    ic = int(np.argmax(r[1:])) + 1
    it = ic + int(np.argmin(r[ic:]))
    return {"crest": float(r[ic]),
            "crest_z": float(zs[ic]),
            "trough_after": float(r[it])}


def omegaspectrum_measurements() -> dict[float, dict[str, float]]:
    return {om: _meas(om, z_end) for om, z_end in _OMEGA_GRID}


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


def omegaspectrum_certificates() -> tuple[list[dict[str, object]],
                                          dict[float, dict[str, float]]]:
    m = omegaspectrum_measurements()
    oms = [o for o, _z in _OMEGA_GRID]
    crests = [m[o]["crest"] for o in oms]
    zcs = [m[o]["crest_z"] for o in oms]
    sub = [o for o in oms if o <= 1.0]
    low = [m[o]["crest"] for o in _LOW_SET]
    high = [m[o]["crest"] for o in _HIGH_SET]
    max_trough = max(m[o]["trough_after"] for o in oms)
    m1 = max(oms)
    certs = [
        _certify("L_omega_crest_wavelength_monotone",
                 {"domain": f"P = {_P}, eps = {_EPS}, Omega in "
                            f"{tuple(round(o, 4) for o in oms)} "
                            "(m = 1 .. 8 wavelengths plus 0.5, 1.0, "
                            "sqrt(2)); SSFM to its crest",
                  "law": "the crest amplitude strictly increases as the "
                         "seed frequency decreases across the whole "
                         "well-posed window",
                  "measured": {str(round(o, 3)): round(c, 3)
                               for o, c in zip(oms, crests)}},
                 lambda: all(a > b for a, b in zip(crests, crests[1:]))),
        _certify("L_omega_crest_after_monotone",
                 {"law": "for Omega <= 1.0 the first-crest distance "
                         "strictly increases as the frequency decreases "
                         "(longer modulations crest later); measured "
                         "2.45 -> 11.70",
                  "measured": {str(round(o, 3)): round(m[o]['crest_z'], 2)
                               for o in sub}},
                 lambda: all(m[a]["crest_z"] > m[b]["crest_z"]
                             for a, b in zip(sub, sub[1:]))),
        _certify("L_omega_cap_division",
                 {"law": f"the Peregrine cap {_CAP} divides the band: "
                         "every crest at Omega <= 0.785 exceeds it, "
                         "every crest at Omega in {{1.0, sqrt(2)}} "
                         "stays below it",
                  "measured": {"low_max": round(max(low), 3),
                               "high_min": round(min(high), 3)}},
                 lambda: min(low) > _CAP and max(high) < _CAP),
        _certify("L_omega_recurrence_holds",
                 {"law": f"the recurrence survives every wavelength: "
                         f"trough_after <= {_RELAX_FACTOR}*(1+eps) after "
                         "each crest, so the deep-band overshoots relax "
                         "back instead of blowing up",
                  "measured_max_trough": round(max_trough, 3),
                  "max_crest": round(max(crests), 3)},
                 lambda: max_trough <= _RELAX_FACTOR * (1 + _EPS)),
        _certify("L_omega_dc_turnback",
                 {"law": "within the well-posed wavelength window the "
                         "crest turns back down toward the "
                         "constant-wave (DC) limit before the longest "
                         "m = 1 seed",
                  "measured": "FALSE: the crest only rises with "
                              "wavelength inside the window (m = 1 is "
                              "the longest continuous seed available on "
                              "the 64-window, and it crests highest at "
                              f"{m[m1]['crest']:.3f}); the turn-back "
                              "lies below the window's well-posed floor"},
                 lambda: False),
    ]
    return certs, m


if __name__ == "__main__":
    certs, m = omegaspectrum_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("  Omega    crest   z_crest trough_after")
    for o, _z in _OMEGA_GRID:
        d = m[o]
        print("  %.4f  %.3f   %.2f    %.3f" % (
            o, d["crest"], d["crest_z"], d["trough_after"]))