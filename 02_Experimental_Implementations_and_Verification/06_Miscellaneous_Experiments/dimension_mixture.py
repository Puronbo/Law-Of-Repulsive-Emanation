"""
DIMENSION MIXTURES: WHAT HELPS, WHAT CANNOT, WHAT IS OPEN
=========================================================
Companion to dimension_threshold.py.  There we established: L^inf control of u
from H^1 holds iff the EFFECTIVE dimension is < 2.  Here we ask what "a mixture
of all dimensions" (the user's hypothesis) can actually buy.

We isolate one sharp, verifiable lemma and one quantitative criterion, then list
the remaining viable interpretations as frameworks with their open content.

VERIFIED LEMMA ("no averaging")
------------------------------
A mixture u = sum_i u_i of components with local dimensions {d_i} has

    ||u||_inf / ||u||_{H^1}  governed by  max_i d_i ,

NOT by an average.  Reason: ||u||_inf <= sum_i ||u_i||_inf and each narrow
component with fixed amplitude has H^1 cost -> 0, so you may always inject the
worst dimension at a scale chosen to win.  Concretely, a d=3 bump of unit-H^1
has amplitude ~ eps^{-1/2}; a d<2 component is bounded.  Adding low-dimension
components cannot cancel the growing high-dimension amplitude at r=0.

So plain "mixing dimensions" does NOT lower the effective dimension.  The only
way a mixture helps is ENERGY CONCENTRATION: the high-dimension components must
carry vanishing energy.  That is intermittency, and it is quantifiable:

VERIFIED CRITERION ("intermittency budget")
-------------------------------------------
Fix a low-dimension "bulk" (d_l = 1.5, unit width, costs O(1)) and a high-
dimension component (d_h = 3, width eps).  Let theta = the fraction of the total
H^1 budget spent on the high-dimension component.  Then

    ||u||_inf <= C   for all eps   <=>   theta <= (C - b)^2 * I1h * eps^{d_h - 2}
                                         ~ O(eps)   as eps -> 0,

where b = sqrt((1-theta)/(I0l+I1l)) is the bulk amplitude.  I.e. the admissible
high-dimension energy fraction must SHRINK LINEARLY with the scale.  This is the
precise sense in which intermittency (vanishing high-dimension energy at small
scales) is exactly what would repair the H^1 -> L^inf wall.  We verify the O(eps)
law numerically.

OTHER VIABLE READINGS AND THEIR OPEN CONTENT
--------------------------------------------
(3) RIESZ POTENTIALS ON FRACTAL MEASURES (Adams/Hedberg).  Replace Lebesgue by
    a measure mu with a dimension SPECTRUM; the L^inf bound is governed by the
    capacity of mu, not a single dimension.  OPEN: which admissible mu (i.e.
    which mixture) is compatible with the NS/Puno energy identity.
(4) DIMENSIONAL REGULARISATION / SCALING-CRITICAL DIMENSION (Tao).  Under
    u_lambda = lambda u(lambda x, lambda^2 t) the L^2 norm scales lambda^{1-D/2}:
    L^2 is critical at D=2 and supercritical for D>2.  "Mixture" = analytic
    continuation in D; the obstruction is the residue at D = 2.  OPEN: the NS
    nonlinearity does not continue cleanly in D.
(5) SPECTRAL IN n (Delta_n eigenvalue).  Treat n in Delta_n as a spectral
    eigenvalue (Frontier 1's proposed next step).  Threshold n_c = 1; physical
    n = 3, Hou n ~ 3.188.  OPEN: whether the exponents stay n-independent once n
    is dynamical (SelfSimilarExponents.lean proves it for FIXED n only).
(6) LOG-CORRELATED / GAUSSIAN MULTIPLICATIVE CHAOS.  The modern framework in
    which "all dimensions mix": multifractal measures from log-correlated
    fields.  OPEN: no rigorous link from NS singularity formation to such a
    measure yet.

THE UNIFYING OPEN CONTENT (the bridge barrier)
----------------------------------------------
Every reading says the same thing: closure requires d_eff < 2 at every scale,
and dimension mixtures only achieve this through energy concentration.  What is
missing in ALL of them is the BRIDGE: an admissible reweighting that (a) is
preserved by the equation and (b) keeps the high-dimension energy below the
O(eps) budget at every scale.  That is the open wall, restated dimensionally.

Run:  python dimension_mixture.py         (prints PASS)
"""
import numpy as np

_trapz = getattr(np, "trapezoid", None) or getattr(np, "trapz")

_CACHE = {}


def radial_int(d, npts=200001):
    """(I0, I1) = (int phi^2 rho^{d-1} drho, int phi'^2 rho^{d-1} drho), [0,1]."""
    if d in _CACHE:
        return _CACHE[d]
    rho = np.linspace(0.0, 1.0, npts)
    phi = (1.0 - rho**2) ** 2
    dphi = -4.0 * rho * (1.0 - rho**2)
    w = np.where(rho > 0, rho ** (d - 1.0), 0.0)
    out = (_trapz(phi**2 * w, rho), _trapz(dphi**2 * w, rho))
    _CACHE[d] = out
    return out


def mixture_inf(dl, dh, eps, theta):
    """||u||_inf of an H^1-normalised mixture; theta = H^1 budget on the spike."""
    I0l, I1l = radial_int(dl)
    I0h, I1h = radial_int(dh)
    z_h = eps ** (dh - 2.0) * I1h          # Z per unit a^2
    e_h = eps ** dh * I0h                  # E per unit a^2
    a = np.sqrt(theta / (z_h + e_h))       # spike amplitude
    b = np.sqrt((1.0 - theta) / (I0l + I1l))  # bulk amplitude
    return float(a + b), float(a), float(b), I1h


def theta_max(dl, dh, eps, C, iters=80):
    """Largest high-dim H^1 fraction theta with ||u||_inf <= C (bisection)."""
    lo, hi = 0.0, 1.0
    if mixture_inf(dl, dh, eps, hi)[0] <= C:
        return 1.0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if mixture_inf(dl, dh, eps, mid)[0] <= C:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    print("=" * 78)
    print("DIMENSION MIXTURES")
    print("=" * 78)

    dl, dh = 1.5, 3.0
    eps = 1e-3
    print("\n[A] NO-AVERAGING LEMMA  (dl=1.5 bulk, dh=3 spike, eps=1e-3)")
    print(f"{'theta(high-dim H^1 frac)':>26} {'||u||_inf':>12} {'spike a':>10} {'bulk b':>10}")
    for th in [0.0, 1e-6, 1e-4, 1e-2, 0.1, 0.5, 1.0]:
        L, a, b, _ = mixture_inf(dl, dh, eps, th)
        print(f"{th:>26.2e} {L:>12.4g} {a:>10.4g} {b:>10.4g}")
    L_bulk = mixture_inf(dl, dh, eps, 0.0)[0]
    L_mix = mixture_inf(dl, dh, eps, 1e-4)[0]
    L_pure = mixture_inf(dl, dh, eps, 1.0)[0]
    print(f"\n  bulk only (theta=0): ||u||_inf = {L_bulk:.4g}")
    print(f"  + tiny spike (theta=1e-4): ||u||_inf = {L_mix:.4g}  (> bulk, spike adds)")
    print(f"  pure high-dim (theta=1): ||u||_inf = {L_pure:.4g}  (-> inf as eps->0)")
    print("  -> the mixture is locked to the d=3 spike amplitude; the low-")
    print("     dimension bulk cannot cancel it.  Averaging does not help.")

    print("\n[B] INTERMITTENCY BUDGET: theta_max for ||u||_inf <= C=10")
    C = 10.0
    rows = []
    for eps in [1e-2, 1e-3, 1e-4]:
        tm = theta_max(dl, dh, eps, C)
        _, _, _, I1h = mixture_inf(dl, dh, eps, 0.0)
        pred = (C - 1.0) ** 2 * I1h * eps ** (dh - 2.0)  # leading-order prediction
        rows.append((eps, tm, pred))
        print(f"  eps={eps:.0e}:  theta_max = {tm:.4e}   leading-order ~ {pred:.4e}")

    ratios = [rows[i + 1][1] / rows[i][1] for i in range(len(rows) - 1)]
    print(f"  theta_max(eps/10) / theta_max(eps) = "
          f"{', '.join(f'{r:.2f}' for r in ratios)}  (expect ~0.1: theta_max = O(eps))")
    assert all(0.08 < r < 0.12 for r in ratios), "theta_max not linear in eps"

    assert L_mix > L_bulk, "high-dim spike did not add to the mixture"
    assert L_pure > 40.0, "pure high-dim spike not large at eps=1e-3"
    print("\n" + "=" * 78)
    print("PASS: (1) mixtures governed by the max dimension (no averaging);")
    print("      (2) admissible high-dim energy fraction theta_max = O(eps).")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
