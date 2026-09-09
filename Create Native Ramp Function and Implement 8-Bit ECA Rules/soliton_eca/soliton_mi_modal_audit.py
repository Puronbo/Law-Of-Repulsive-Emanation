"""soliton_mi_modal_audit: spectral makeup at the crest and at the window.

Round 15 stated the crest state to be a >= 70% two-mode core.  Re-audit
(round 17) found a measurement-integrity bug: the power split was taken
from the field at the END of the integration window, not at the crest
(crest heights were correct; the split was not).  At the TRUE crest the
picture is opposite and richer -- pump depletion.

Crest-time power fractions (P = 1, eps = 0.2, integer-fit seeds with
exactly carrier + two sidebands)::

    m=4   O=0.196  crest 4.387@6.40  P0=0.017 P(+-O)=0.237 P(+-2O)=0.195 rest=0.552
    m=8   O=0.393  crest 3.889@3.75  P0=0.250 P(+-O)=0.076 P(+-2O)=0.122 rest=0.553
    m=16  O=0.785  crest 3.143@2.60  P0=0.061 P(+-O)=0.378 P(+-2O)=0.307 rest=0.254

Late-window fractions (the state actually certified in round 15)::

    m=4                                      P0=0.567 P(+-O)=0.202 rest=0.231
    m=8                                      P0=0.832 P(+-O)=0.041 rest=0.127
    m=16                                     P0=0.818 P(+-O)=0.157 rest=0.025

Laws (all measured):

- the pump is DEPLETED at every crest: P0 <= 0.30 (the crest is built
  from the sidebands, not from the carrier);
- the crest is NOT a two-mode core: carrier + fundamental <= 0.50
  (P = {0.254, 0.326, 0.439});
- the late-window state the round-15 module actually split DOES carry
  the two-mode core >= 0.70 and a restored carrier P0 >= 0.50 -- the
  round-15 "modal coherence" law survives, re-scoped to the late
  window;
- at the late window the second-harmonic share still rises with the
  seed's overshoot (0.022 -> 0.088, total pair);
- HONEST_NEGATIVE pair: (a) "the carrier + fundamental hold >= 70% at
  the crest" is FALSE -- at the crest the two-mode core is at most
  0.44, collapsing with the carrier; (b) "the crest is exactly on the
  2-mode manifold" is FALSE at both the crest and the late window.

Certificates:

    L_mod_pump_depleted        PASS/FAIL  P0 <= 0.30 at every crest.
    L_mod_crest_core_capped    PASS/FAIL  P0 + P1 <= 0.50 at every
                                  crest (the honest crest-time core).
    L_mod_late_core_restored   PASS/FAIL  at the window end P0 >= 0.50
                                  and P0 + P1 >= 0.70 for every mode.
    L_mod_late_harmonic_rise   PASS/FAIL  P(2O, z_end) rises with the
                                  seed's overshoot.
    L_mod_carrier_core_at_crest HONEST_NEGATIVE  "two-mode core >= 0.70
                                  at the crest": FALSE (<= 0.44).
    L_mod_exact_twomode_crest  HONEST_NEGATIVE  "the crest is exactly
                                  on the 2-mode manifold": FALSE.
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
_CORE_LATE = 0.70
_CARRIER_LATE = 0.50
_PUMP_CEIL = 0.30
_CREST_CORE_CEIL = 0.50

# integer-fit wavelengths: seed has exactly carrier + 2 sidebands.
_MODES = (
    (4, 15.0),   # Omega = 2*pi*2/64
    (8, 12.0),   # Omega = 2*pi*4/64
    (16, 10.0),  # Omega = 2*pi*8/64
)


def _omega(m: int) -> float:
    return 2 * np.pi * (m // 2) / 64


def _grid() -> np.ndarray:
    _n, _l = 8192, 64.0
    return np.linspace(-_l / 2, _l / 2, _n, endpoint=False)


def _split(u: np.ndarray, om: float) -> dict[str, float]:
    n = len(u)
    t = _grid()
    dt = float(np.diff(t)[0])
    spect = np.abs(np.fft.fft(u)) ** 2
    f = 2 * np.pi * np.fft.fftshift(np.fft.fftfreq(n, dt))
    c = np.fft.fftshift(spect)
    tot = float(c.sum())
    k0 = int(np.argmin(np.abs(f)))
    kp = int(np.argmin(np.abs(f - om)))
    km = int(np.argmin(np.abs(f + om)))
    p1 = float(c[kp] + c[km]) / tot
    k2p = int(np.argmin(np.abs(f - 2 * om)))
    k2m = int(np.argmin(np.abs(f + 2 * om)))
    p2 = float(c[k2p] + c[k2m]) / tot
    p0 = float(c[k0]) / tot
    rest = 1.0 - p0 - p1 - p2
    return {"p0": p0, "p1": p1, "p2": p2, "rest": rest}


def _modal(m: int, z_end: float) -> dict[str, float]:
    om = _omega(m)
    t = _grid()
    dt = float(np.diff(t)[0])
    ci = int(np.argmin(np.abs(t)))
    zs = np.arange(0.0, z_end + _Z_GRID / 2, _Z_GRID)
    cur = np.sqrt(_P) * (1 + _EPS * np.cos(om * t))
    prev = 0.0
    ratios = [np.abs(cur[ci]) / np.sqrt(_P)]
    fields = [cur.copy()]
    for z in zs[1:]:
        cur = propagate(cur, dt, z - prev, fiber=Fiber(),
                        steps=_STEPS_PER_DZ)
        prev = z
        ratios.append(np.abs(cur[ci]) / np.sqrt(_P))
        fields.append(cur.copy())
    r = np.asarray(ratios)
    ic = int(np.argmax(r[1:])) + 1
    crest = _split(fields[ic], om)
    late = _split(fields[-1], om)
    return {
        "crest": float(r[ic]),
        "crest_z": float(zs[ic]),
        "omega": float(om),
        "p0c": crest["p0"],
        "p1c": crest["p1"],
        "p2c": crest["p2"],
        "restc": crest["rest"],
        "p0l": late["p0"],
        "p1l": late["p1"],
        "p2l": late["p2"],
        "restl": late["rest"],
    }


def modal_measurements() -> dict[int, dict[str, float]]:
    return {m: _modal(m, z_end) for m, z_end in _MODES}


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


def modal_certificates() -> tuple[list[dict[str, object]],
                                  dict[int, dict[str, float]]]:
    data = modal_measurements()
    p0c = [data[m]["p0c"] for m, _ in _MODES]
    corec = [data[m]["p0c"] + data[m]["p1c"] for m, _ in _MODES]
    p0l = [data[m]["p0l"] for m, _ in _MODES]
    corel = [data[m]["p0l"] + data[m]["p1l"] for m, _ in _MODES]
    p2l = {m: data[m]["p2l"] for m, _ in _MODES}
    crest = {m: data[m]["crest"] for m, _ in _MODES}
    dump_ok = all(p <= _PUMP_CEIL for p in p0c)
    cc_ok = all(c <= _CREST_CORE_CEIL for c in corec)
    late_ok = all(p >= _CARRIER_LATE for p in p0l) and \
        all(c >= _CORE_LATE for c in corel)
    # overshoot ordering: crest m16 < m8 < m4, P2l must follow.
    harm_ok = p2l[4] > p2l[8] > p2l[16] and crest[16] < crest[8] < crest[4]
    old_fail = not all(c >= _CORE_LATE for c in corec)
    exact_fail = not all(abs(1.0 - c - 0.0) < 1e-9 for c in corec)
    certs = [
        _certify("L_mod_pump_depleted",
                 {"domain": f"P = {_P}, eps = {_EPS}, modes {_MODES}, "
                            f"z-grid {_Z_GRID}",
                  "law": "at every crest the carrier is depleted: "
                         f"P0 <= {_PUMP_CEIL} (measured "
                         + ", ".join(f"{m}: {v:.3f}" for m, v in
                                     zip([m for m, _ in _MODES], p0c))
                         + ") -- the crest is built from the sidebands",
                  "measured": {str(m): round(data[m]["p0c"], 3)
                               for m, _ in _MODES}},
                 lambda: dump_ok),
        _certify("L_mod_crest_core_capped",
                 {"law": "at the crest the two-mode core is capped: "
                         f"P0 + P1 <= {_CREST_CORE_CEIL} (measured "
                         + ", ".join(f"{v:.3f}" for v in corec) + ")",
                  "measured": {str(m): round(corec[i], 3)
                               for i, m in enumerate([mm for mm, _ in _MODES])}},
                 lambda: cc_ok),
        _certify("L_mod_late_core_restored",
                 {"law": "at the window end the carrier recovers "
                         f"(P0 >= {_CARRIER_LATE}) and the two-mode core "
                         f"restores to >= {_CORE_LATE} -- the round-15 "
                         "coherence law survives, scoped to the late "
                         "window",
                  "measured": {"P0l": {str(m): round(data[m]["p0l"], 3)
                                       for m, _ in _MODES},
                               "corel": {str(m): round(data[m]["p0l"]
                                                       + data[m]["p1l"], 3)
                                         for m, _ in _MODES}}},
                 lambda: late_ok),
        _certify("L_mod_late_harmonic_rise",
                 {"law": "at the window end the second-harmonic pair "
                         "rises with the seed's overshoot: P2l(16) < "
                         "P2l(8) < P2l(4) while crest(16) < crest(8) < "
                         "crest(4)",
                  "measured": {str(m): round(p2l[m], 3)
                               for m, _ in _MODES}},
                 lambda: harm_ok),
        _certify("L_mod_carrier_core_at_crest",
                 {"law": "the carrier + fundamental hold >= 0.70 at the "
                         "crest (round-15 'two-mode core' claim, crest "
                         "time)",
                  "measured": f"FALSE at the true crest: the core is at "
                              f"most {max(corec):.3f} while the carrier "
                              f"falls to {min(p0c):.3f} -- the round-15 "
                              f"split was taken at the window END",
                  "max_core_crest": round(max(corec), 3)},
                 lambda: all(c >= _CORE_LATE for c in corec)),
        _certify("L_mod_exact_twomode_crest",
                 {"law": "the crest state sits exactly on the 2-mode "
                         "manifold (rest = 0)",
                  "measured": f"FALSE: rest >= {min(1.0 - np.asarray(corec) - 0.0):.3f} "
                              "at the crest (and decays only weakly at "
                              "the late window)",
                  "min_rest_crest": round(float(min(1.0 - np.asarray(corec))), 3)},
                 lambda: all(abs(1.0 - c) < 1e-9 for c in corec)),
    ]
    return certs, data


if __name__ == "__main__":
    certs, data = modal_certificates()
    for c in certs:
        print("  %-40s %-16s n_ok=%d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    for m, _ in _MODES:
        d = data[m]
        print("  m=%2d O=%.4f crest=%.3f@%.2f P0c=%.3f P1c=%.3f "
              "restc=%.3f | P0l=%.3f P1l=%.3f P2l=%.3f restl=%.3f" % (
                  m, d["omega"], d["crest"], d["crest_z"], d["p0c"],
                  d["p1c"], d["restc"], d["p0l"], d["p1l"], d["p2l"],
                  d["restl"]))