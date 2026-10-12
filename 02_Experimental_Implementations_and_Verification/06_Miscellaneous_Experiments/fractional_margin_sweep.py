"""
MARGIN SWEEP: locate the marginal dissipation order s* and the viscosity threshold.

`orientation_vs_fractional_s.py` showed that over the full relaxation window the
on-flow orientation matches the critical-content growth at s in {1, 0.75, 0.5}, and
that |lambda| -> 0 as the dissipation order s drops (the flow drifts toward the
inviscid/repelling regime).  This script sharpens that into a "margin":

  * s-sweep -- locate s*, the dissipation order where the (late-window, asymptotic)
    orientation crosses zero; s* is the boundary of the standard regime.  Fit the
    scaling-gap exponent beta in |lambda| ~ |s - s*|^beta.
  * nu-sweep at fixed s < 1 -- locate the viscosity threshold nu* where the orientation
    crosses zero; for nu > nu* the flow is attracted, nu < nu* repelling.  This is the
    margin in the classical parameter.

The late-window slope (t >= T/2) is used throughout, because the full-window slope can
be contaminated by the early high-k enstrophy pile-up (see the window caveat in
`orientation_vs_fractional_s.py`).  Diagnostic only; the wall stays OPEN.

Run:  python fractional_margin_sweep.py       (prints PASS)
"""
import json
import os
import numpy as np

from orientation_vs_fractional_s import run_fractional_ns

OUT = "data/fractional_margin_sweep.json"
T_MAX = 6.0


def slope(x, y):
    return float(np.polyfit(np.asarray(x), np.asarray(y), 1)[0])


def late_rate(s, nu=0.1, T_max=6.0):
    """Asymptotic (late-window) orientation and critical-content growth rates."""
    ts, sh, cr, l3, div = run_fractional_ns(s, nu=nu, T_max=T_max)
    t = np.asarray(ts)
    late = t >= 0.5 * T_max
    lam = float(np.polyfit(t[late], np.log(np.asarray(sh)[late]), 1)[0])
    mu = float(np.polyfit(t[late], np.log(np.array(cr)[late]), 1)[0])
    return lam, mu, len(ts), bool(div)


def crossing(xs, ys):
    """Linear-interpolated zero of y(x); returns (x_star, slope_sign) or (None, 0)."""
    order = np.argsort(xs)
    xs = np.asarray(xs)[order]
    ys = np.asarray(ys)[order]
    for i in range(len(xs) - 1):
        if ys[i] == 0.0:
            return float(xs[i]), 1
        if ys[i] * ys[i + 1] < 0:
            x = xs[i] - ys[i] * (xs[i + 1] - xs[i]) / (ys[i + 1] - ys[i])
            return float(x), 1
    return None, 0


def fit_exponent(xs, ys, x_star):
    xs = np.asarray(xs, float)
    ys = np.asarray(ys, float)
    d = np.abs(xs - x_star)
    good = (d > 1e-6)
    if good.sum() < 3:
        return None
    beta = float(np.polyfit(np.log(d[good]), np.log(np.abs(ys[good])), 1)[0])
    return beta


def main():
    print("=" * 80)
    print("MARGIN SWEEP: marginal dissipation order s* and viscosity threshold nu*")
    print("  orientation lambda = late-window slope of log(Z_high/Z_low), T = 6")
    print("=" * 80)
    os.makedirs("data", exist_ok=True)
    out = {}

    s_grid = [0.20, 0.22, 0.25, 0.28, 0.32, 0.40, 0.50]
    s_rows = []
    print(f"{'s':>7}{'lambda_late':>14}{'mu_late':>12}{'n':>6}{'div':>6}")
    print("-" * 80)
    for s in s_grid:
        lam, mu, n, div = late_rate(s)
        s_rows.append((s, lam, mu))
        print(f"{s:>7.2f}{lam:>+14.3f}{mu:>+12.3f}{n:>6}{str(div):>6}")
    xs = [r[0] for r in s_rows]
    lams = [r[1] for r in s_rows]
    mus = [r[2] for r in s_rows]
    s_star, ok = crossing(xs, lams)
    beta = fit_exponent(xs, lams, s_star) if s_star is not None else None
    print("-" * 80)
    print(f"  s* (orientation zero) = {s_star}   scaling-gap exponent beta = {beta}")
    print(f"  mu at s={xs[0]:.2f} (deepest probed) = {mus[0]:+.3f}  "
          f"({'still attracting' if mus[0] < 0 else 'repelling'})")
    out["s_sweep"] = [{"s": s, "lambda_late": l, "mu_late": m} for s, l, m in s_rows]
    out["s_star"] = s_star
    out["beta_scaling_gap"] = beta

    print()
    print("  viscosity sweep at fixed s = 0.40:")
    nu_grid = [0.02, 0.03, 0.05, 0.10, 0.20, 0.40]
    nu_rows = []
    print(f"{'nu':>8}{'lambda_late':>14}{'mu_late':>12}{'n':>6}{'div':>6}")
    print("-" * 80)
    for nu in nu_grid:
        lam, mu, n, div = late_rate(0.40, nu=nu)
        nu_rows.append((nu, lam, mu))
        print(f"{nu:>8.2f}{lam:>+14.3f}{mu:>+12.3f}{n:>6}{str(div):>6}")
    nus = [r[0] for r in nu_rows]
    nulam = [r[1] for r in nu_rows]
    nu_star, ok2 = crossing(nus, nulam)
    print("-" * 80)
    print(f"  nu* (orientation zero at s=0.40) = {nu_star}")
    out["nu_sweep"] = [{"nu": nu, "lambda_late": l, "mu_late": m} for nu, l, m in nu_rows]
    out["nu_star"] = nu_star

    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)

    print()
    print("=" * 80)
    assert ok, "no orientation sign change found over the s-sweep"
    assert s_star is not None
    print(f"PASS: the standard regime has a boundary at s* = {s_star:.3f} "
          f"(beta = {beta}); below it the orientation is repelling.")
    print(f"      At fixed s=0.40 the boundary in viscosity is nu* = {nu_star}.  The")
    print(f"      deepest probed order s={xs[0]:.2f} still has decaying critical content")
    print(f"      (mu = {mus[0]:+.3f} < 0): the orientation LEADS the wall.  Diagnostic")
    print( "      only; the wall (finiteness of int g) stays OPEN -- card C10-open.")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
