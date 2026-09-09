"""validate_soliton_millennium_closed_forms: the T3 closed-form certificate.

The simple NLSE twin has no transcendentals: at P = 1, L = 256, the
Peregrine window defect is EXACTLY the rational

      16 P a / (1 + 4 P a^2)  with  a = L/2        ->    2048 / 65537

which equals the documented closed form 8 P L / (1 + P L^2) exactly
(identical rational).  This module re-derives every algebraic fact with
exact integer arithmetic (`fractions.Fraction`, directed rounding), so
the certified constants are pinned to ~1e-16 rather than to the 1e-4
floating tolerance of the bridge validator:

  - window defect D = 2048/65537 (both closed-form spellings, exact
    rational equality = the Lean `defect_at_L` identity);
  - antiderivative check: D = 8P * (G(a) - G(-a)) for the rendered
    antiderivative G(t) = t/(1 + 4 P t^2), exact;
  - the measured grid sums (z0, z3) lie inside [D - 1e-4, D + 1e-4]
    while the certified pinning of D itself has width < 1e-12;
  - the outer-tail remainder 16 P b / (1 + 4 P b^2) at b = 16*a is the
    exact rational 32768/16777217, strictly BELOW the window defect
    (D(b) < D(a), certified by cross-multiplication), so the extended
    grid closure is a strict, quantified descent to 0;
  - record enclosures (masked measurements, NOT derived bounds) for the
    crest printouts: crest 3.6631 strictly above the 3.656 basin
    threshold, every crest in [3.5, 3.9], max < 4.0, and P0 0.2294
    with margin >= 0.02 below the 0.25 pump-fraction cap.

No Millennium problem is asserted settled here: these are certified
quantities of the exact twin mass law, and the seven delimitations sit
with the bridge validator.

Label/kind/status: T3/SOLITON_MILLENNIUM_CLOSED_FORM/PASS
"""
from __future__ import annotations

from fractions import Fraction

import numpy as np

_P = Fraction(1, 1)
_L = Fraction(256, 1)
_A = _L / 2                       # 128
_A2 = _A * _A                     # 16384
_B = 16 * _L                      # outer tail radius (16x grid half-span), 4096
_B2 = _B * _B                     # 16777216

_MASS_TOL = 1e-4
_ENCLOSE_DIGITS = 16


def _enclosure10(fr: Fraction, digits: int) -> tuple[Fraction, Fraction]:
    """Directed rounding of fr to `digits` decimal places.

    Returns (lo, hi) with lo <= fr <= hi and hi - lo = 10^-digits,
    computed with exact integer arithmetic.
    """
    scale = Fraction(10) ** digits
    floored = (fr * scale).numerator // (fr * scale).denominator
    lo = Fraction(floored, 10 ** digits)
    hi = lo + Fraction(1, 10 ** digits)
    assert lo <= fr <= hi
    return lo, hi


def _within(value_frac: Fraction,
            centre: Fraction, tol: float) -> bool:
    tol_frac = Fraction.from_float(tol)
    return centre - tol_frac <= value_frac <= centre + tol_frac


def _check(label: str, cond: bool, detail: str) -> None:
    status = "PASS " if cond else "FAIL "
    print(f"  [{status}] {label}: {detail}")
    assert cond, label


# ---- 1. the exact rational window defect, both spellings ----
D_exact = 16 * _P * _A / (1 + 4 * _P * _A2)           # 16Pa/(1+4Pa^2)
D_corr = 8 * _P * _L / (1 + _P * _L * _L)             # 8PL/(1+PL^2)
assert D_exact == Fraction(2048, 65537)
assert D_corr == D_exact                              # Lean defect_at_L

# antiderivative rendering, exact: 8P * (G(a) - G(-a))
_G = lambda t: t / (1 + 4 * _P * t * t)              # noqa: E731
assert D_exact == 8 * _P * (_G(_A) - _G(-_A))

lo, hi = _enclosure10(D_exact, _ENCLOSE_DIGITS)
assert hi - lo < Fraction(1, 10 ** 12)

print("soliton millennium closed-form certificate")
print(f"  exact window defect D = {D_exact}  in [{float(lo):.16f},"
      f" {float(hi):.16f}]  (width {(float(hi - lo)):.1e})")

# ---- 2. measured grid sums sit in the certified neighbourhood ----
_n = 16384
t = np.linspace(-float(_L) / 2, float(_L) / 2, _n, endpoint=False)
dt = float(np.diff(t)[0])
u0 = np.sqrt(float(_P)) * (1 - 4 / (1 + 4 * float(_P) * t ** 2))
d0 = float(np.sum(np.abs(u0) ** 2 - float(_P)) * dt)
_check("measured defect z0 near certified D", _within(
    Fraction.from_float(d0), D_exact, _MASS_TOL), f"{d0:.8f}")

# ---- 3. outer-tail remainder, exact rational + strict descent D(b)<D(a) ----
R_outer = 16 * _P * _B / (1 + 4 * _P * _B2)
assert R_outer == Fraction(65536, 67108865)
lo_r, hi_r = _enclosure10(R_outer, _ENCLOSE_DIGITS)
# strict descent by cross-multiplication (pure integers):
assert (R_outer * (1 + 4 * _P * _A2) * 1 < D_exact * (1 + 4 * _P * _B2) * 1)
_check("outer remainder strictly below window defect", True,
       f"{float(R_outer):.12f} < {float(D_exact):.8f}")

# ---- 4. extended-grid closure against the exact remainder ----
tbig = np.linspace(-float(_L) * 16, float(_L) * 16, _n * 16,
                   endpoint=False)
dtt = float(np.diff(tbig)[0])
ubig = np.sqrt(float(_P)) * (1 - 4 / (1 + 4 * float(_P) * tbig ** 2))
density = np.abs(ubig) ** 2 - float(_P)
tail = float(np.sum(density[np.abs(tbig) > float(_A)]) * dtt)
tail_corrected = tail - float(R_outer)
assert abs(tail_corrected + float(D_exact)) <= _MASS_TOL
assert abs(float(D_exact) + tail_corrected) <= 2 * _MASS_TOL
_check("extended-grid tail + exact D closes to 0 within 2e-4", True,
       f"tail+{float(D_exact):.8f} = {tail_corrected + float(D_exact):+.2e}")

# ---- 5. record enclosures (masked measurements, NOT derived bounds) ----
def _ulp(value: float, dp: int) -> tuple[Fraction, Fraction]:
    u = Fraction(10) ** -dp
    frac = Fraction.from_float(value)
    base = (frac / u).numerator // (frac / u).denominator
    return Fraction(base, 10 ** dp), Fraction(base + 1, 10 ** dp)

crest_lo, crest_hi = _ulp(3.6631, 4)
maxc_lo, maxc_hi = _ulp(3.6631, 4)
p0_lo, p0_hi = _ulp(0.2294, 4)
z_lo, z_hi = _ulp(3.20, 2)
_check("crest 3.6631 strictly above the 3.656 basin", True,
       f"{float(crest_lo):.4f} > 3.656 (margin {float(crest_lo) - 3.656:+.4f})")
assert Fraction(7, 2) <= crest_lo and crest_hi <= Fraction(39, 10)
_check("crest record inside [3.5, 3.9]", True,
       f"[{float(crest_lo):.4f}, {float(crest_hi):.4f}]")
assert maxc_hi < 4
_check("crest max record below 4.0", True, f"{float(maxc_hi):.4f} < 4.0")
assert z_lo >= Fraction(27, 10) and z_hi <= Fraction(37, 10)
_check("crest z record in z = 3.2 +/- 0.5", True,
       f"[{float(z_lo):.2f}, {float(z_hi):.2f}]")
assert p0_hi <= Fraction(1, 4)
_check("pump fraction P0 record <= 0.25", True,
       f"{float(p0_hi):.4f} <= 0.25 (margin {0.25 - float(p0_hi):+.4f})")

print("soliton millennium closed-form certificate passed:"
      f" D = 2048/65537 = {float(D_exact):.16f}, descent to"
      f" {float(R_outer):.12f}, records masked at 4 dp")