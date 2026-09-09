"""validate_soliton_millennium_bridge_audit: independent re-derivation.

Does NOT trust millennium_bridge_certificates(): it re-implements the
three NSE-adjacent numeric laws with its own copies of the ridge scan,
the mass-neutrality defect, and the pump-fraction measurement, and
re-runs its own corpus scan (with its own copied sentinel table) for
the seven Millennium delimitations, then checks the module's live
statuses against an independently redeclared expectation list.

Independently re-derived facts:

  - crest control: the seed sqrt(1)*(1 + eps*cos(Omega t)) at
    (Omega, eps) = (0.5, 0.20) on N = 8192, L = 64 crests inside
    [3.5, 3.9] near z = 3.2 with a window maximum below 4.0;
  - mass neutrality: the Peregrine window defect int(|u|^2-P) dt, L =
    256, N = 16384, P = 1.0, equals 8PL/(1+PL^2) to within 1e-4 at
    z = 0 AND at z = 3 under the shared SSFM, and the defect is
    spread across z <= 1e-4;
  - modal depletion: at the measured crest the pump-sector power
    fraction P0 <= 0.25;
  - delimitations: the corpus (excluding the bridge files themselves)
    contains none of the independently listed settlement sentinels;
  - scope discipline: no un-negated self-attributive resolution line
    exists in the docs.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from soliton_eca.soliton_millennium_bridge_audit import (  # noqa: E402
    millennium_bridge_certificates,
)
from soliton_eca.soliton_physics import (  # noqa: E402
    Fiber,
    propagate,
)

_N = 8192
_L = 64.0
_Z_GRID = 0.05
_STEPS = 20
_OMEGA = 0.5
_EPS = 0.20

_MASS_L = 256.0
_MASS_N = 16384
_MASS_TOL = 1e-4
_MASS_P = 1.0

_EXPECTED = {
    "L_mil_nse_crest_control": "PASS",
    "L_mil_nse_mass_conservation_exact": "PASS",
    "L_mil_nse_modal_depletion": "PASS",
    "L_mil_P_NNP_untouched": "PASS",
    "L_mil_HODGE_untouched": "PASS",
    "L_mil_POINCARE_untouched": "PASS",
    "L_mil_RH_untouched": "PASS",
    "L_mil_YM_untouched": "PASS",
    "L_mil_NSE_untouched": "PASS",
    "L_mil_BSD_untouched": "PASS",
    "L_mil_scope_discipline": "PASS",
}

_SENTINELS = {
    "P_NNP": ("p vs np is settled", "p vs np is proven",
              "p vs np is solved", "proves p vs np",
              "settles p vs np", "pbsp is resolved"),
    "HODGE": ("hodge conjecture is proved", "hodge is settled",
              "proves the hodge conjecture",
              "hodge conjecture proven"),
    "POINCARE": ("poincare conjecture is proved", "poincare is settled",
                 "proves the poincare conjecture"),
    "RH": ("riemann hypothesis is proved", "riemann is settled",
           "proves the riemann hypothesis", "rh is resolved"),
    "YM": ("yang-mills is proved", "yang-mills is settled",
           "proves the yang-mills", "mass gap is established"),
    "NSE": ("navier-stokes is solved", "nse is resolved",
            "nse is proved", "proves the navier-stokes",
            "regularity is established"),
    "BSD": ("bsd is proved", "bsd is settled",
            "proves the birch and swinnerton-dyer",
            "swinnerton-dyer is resolved"),
}


def _corpus_lines() -> list[str]:
    root = Path(__file__).resolve().parent.parent
    for pattern in ("soliton_eca/*.py", "*.py", "*.md"):
        for p in root.glob(pattern):
            if "millennium_bridge" in p.name.lower():
                continue
            try:
                yield p.read_text(encoding="utf-8",
                                  errors="ignore").lower()
            except OSError:
                continue


def _crest_reimpl() -> dict[str, float]:
    t = np.linspace(-_L / 2, _L / 2, _N, endpoint=False)
    dt = float(np.diff(t)[0])
    seed = np.sqrt(1.0) * (1 + _EPS * np.cos(_OMEGA * t))
    cur = np.array(seed)
    prev = 0.0
    best = 0.0
    best_z = 0.0
    maxima = []
    p0 = 1.0
    for z in np.arange(0.0, 18.0 + _Z_GRID / 2, _Z_GRID):
        if z > 0.0:
            cur = propagate(cur, dt, z - prev, fiber=Fiber(),
                            steps=_STEPS)
            prev = z
        peak = float(np.max(np.abs(cur)))
        maxima.append(peak)
        if peak > best:
            best = peak
            best_z = float(z)
        if abs(z - 3.2) <= 1e-9:
            c = np.fft.fftshift(np.fft.fft(cur))
            f = 2 * np.pi * np.fft.fftshift(np.fft.fftfreq(_N, dt))
            k0 = int(np.argmin(np.abs(f - 0.0)))
            tot = float(np.sum(np.abs(c) ** 2))
            p0 = (float(np.abs(c[k0]) ** 2) / tot if tot > 0
                  else 0.0)
    glob_max = max(maxima)
    return {"crest": best, "z_crest": best_z, "max": glob_max,
            "P0": p0}


def _defect(z: float, use_prop: bool) -> float:
    t = np.linspace(-_MASS_L / 2, _MASS_L / 2, _MASS_N,
                    endpoint=False)
    dt = float(np.diff(t)[0])
    u0 = np.sqrt(_MASS_P) * (
        1 - 4 * (1 + 2j * _MASS_P * z)
        / (1 + 4 * _MASS_P * t ** 2 + 4 * _MASS_P ** 2 * z ** 2))
    if z > 0.0 and use_prop:
        u0 = propagate(u0, dt, z, fiber=Fiber(), steps=_STEPS)
    return float(np.sum(np.abs(u0) ** 2 - _MASS_P) * dt)


# ---- live statuses against the independent expectation list ----
certs, stats = millennium_bridge_certificates()
assert len(certs) == len(_EXPECTED), len(certs)
for c in certs:
    assert c["label"] in _EXPECTED, c["label"]
    assert c["status"] == _EXPECTED[c["label"]], (c["label"],
                                                  c["status"])
    assert ("asserted" in c and "negated" in c and
            c["asserted"] != c["negated"])

# ---- independent numeric re-derivation ----
reimpl = _crest_reimpl()
assert 3.5 <= reimpl["crest"] <= 3.9, reimpl["crest"]
assert abs(reimpl["z_crest"] - 3.2) <= 0.5, reimpl["z_crest"]
assert reimpl["max"] < 4.0, reimpl["max"]
assert reimpl["P0"] <= 0.25, reimpl["P0"]

corr = 8 * _MASS_L / (1 + _MASS_L ** 2)
d0 = _defect(0.0, use_prop=False)
d3 = _defect(3.0, use_prop=True)
assert abs(d0 - corr) <= _MASS_TOL, (d0, corr)
assert abs(d3 - corr) <= _MASS_TOL, (d3, corr)
assert abs(d3 - d0) <= _MASS_TOL, (d3, d0)

# ---- analytic exact law (independently re-derived) ----
# int_(-a)^(a) (|u|^2 - P) dt  =  16*P*a / (1 + 4*P*a^2),  a = L/2
# (arctan terms cancel on the symmetric window; the boundary term
#  x/(2(1+x^2)) survives).  At a = L/2 this is 8PL/(1+PL^2), which is
# the documented 8L/(1+L^2) when P = 1; the symmetric two tails close
# the full-line integral to exactly 0 (mass neutrality).
a = _MASS_L / 2.0
exact = 16 * _MASS_P * a / (1 + 4 * _MASS_P * a ** 2)
assert abs(d0 - exact) <= _MASS_TOL, (d0, exact)
assert abs(exact - corr) <= _MASS_TOL, (exact, corr)
# full-line closure: the symmetric two tails beyond +/-a balance the
# window defect exactly (mass neutrality).  Numerically measured on a
# 16x extended grid, independent of the module's window.
tbig = np.linspace(-_MASS_L * 16, _MASS_L * 16, _MASS_N * 16,
                   endpoint=False)
dtt = float(np.diff(tbig)[0])
ubig = np.sqrt(_MASS_P) * (1 - 4 / (1 + 4 * _MASS_P * tbig ** 2))
density = np.abs(ubig) ** 2 - _MASS_P
tail = float(np.sum(density[np.abs(tbig) > a]) * dtt)
# analytic remainder for the region beyond the grid (tails ~ -2/t^2),
# using the same closed form on the outer radius:
b = float(np.abs(tbig).max())
remainder = 16 * _MASS_P * b / (1 + 4 * _MASS_P * b ** 2)
tail_corrected = tail - remainder
assert abs(tail_corrected + exact) <= _MASS_TOL, (tail_corrected, -exact)
assert abs(d0 + tail_corrected) <= 2 * _MASS_TOL, (d0, tail_corrected)

# ---- independent corpus scan ----
corpus = "\n".join(_corpus_lines())
for tag, sentinels in _SENTINELS.items():
    hits = [s for s in sentinels
            if re.search(r"\b" + re.escape(s) + r"\b", corpus)]
    assert not hits, (tag, hits)
    assert stats["delimitations"][tag], tag

print("soliton millennium bridge validation passed:",
      f"crest {reimpl['crest']:.4f} @ z = {reimpl['z_crest']:.2f}, "
      f"max {reimpl['max']:.4f}, P0 {reimpl['P0']:.4f}; ",
      f"defect z0 {d0:.8f} z3 {d3:.8f} vs {corr:.8f}")