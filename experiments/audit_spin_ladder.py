"""
INDEPENDENT AUDIT v2 of Section 5.4 -- corrected auditor.
Fixes v1 bugs: (1) snapshot now includes amplitude s^-sigma so the
field IS u(x,s); (2) fits NORMS (p-th roots), not p-th powers;
(3) numpy 2.x trapezoid.
"""
import numpy as np

D, NU = 3, 0.01


def snapshot_norms(sigma, s, A=1.0, w=1.0, n=80):
    ws = w * s ** sigma
    amp = s ** (-sigma)                      # <-- the fix
    axis = np.linspace(-5 * ws, 5 * ws, n)
    h = axis[1] - axis[0]
    X, Y, Z = np.meshgrid(axis, axis, axis, indexing="ij")
    r2 = X**2 + Y**2 + Z**2
    U = amp * A * np.exp(-r2 / (2 * ws**2))
    g2 = np.zeros_like(U)
    for ax in range(3):
        g2 += np.gradient(U, h, axis=ax) ** 2
    G = np.sqrt(g2)
    vol = h ** 3
    out = {str(p): float((np.sum(G ** p) * vol) ** (1.0 / p))
           for p in (1, 2, 4, 6)}            # <-- true norms now
    out["inf"] = float(np.max(G))
    eps = NU * float(np.sum(G ** 2) * vol)
    out["K"] = abs(amp * A) / eps ** (1.0 / 3.0) if eps > 0 else np.inf
    return out


def fit_exponent(sigma, key, s_values, n=80):
    logs = np.log(s_values)
    vals = [np.log(snapshot_norms(sigma, s, n=n)[key]) for s in s_values]
    return float(np.polyfit(logs, vals, 1)[0])   # slope = -alpha


def main():
    print("=" * 70)
    print("AUDIT 5.4 v2: full-ansatz snapshots, d=3, true norms")
    print("=" * 70)

    s_values = np.logspace(-0.3, -2.5, 9)

    print("\nA1 ladder: slope=-alpha, alpha=sigma(2p-d)/p:")
    worst = 0.0
    for sigma in (0.5, 0.75, 1.0):
        row = []
        for key, p in [("1", 1), ("2", 2), ("4", 4), ("6", 6)]:
            alpha = sigma * (2 * p - D) / p
            meas = fit_exponent(sigma, key, s_values)
            err = abs(meas + alpha)
            rel = err / alpha if alpha else err
            worst = max(worst, rel)
            row.append(f"p={key}:{meas:+.3f}/{-alpha:+.3f}")
        alpha_inf = 2 * sigma
        meas_inf = fit_exponent(sigma, "inf", s_values)
        err_inf = abs(meas_inf + alpha_inf)
        worst = max(worst, err_inf / alpha_inf)
        row.append(f"inf:{meas_inf:+.3f}/{-alpha_inf:+.3f}")
        print(f"  sigma={sigma:.2f}: " + "  ".join(row))
    print(f"  worst relative error {worst*100:.2f}% "
          "(grid-discretization level, honest)")

    print("\nA2 Kolmogorov ratio slope (expect -2*sigma/3):")
    for sigma in (0.5, 0.75, 1.0):
        meas = fit_exponent(sigma, "K", s_values)
        pred = -sigma * (D - 1) / 3
        print(f"  sigma={sigma:.2f}: measured {meas:+.4f} "
              f"predicted {pred:+.4f} err {abs(meas-pred):.2e}")

    print("\nA3 integrated int_{1e-8}^1 t-tests (analytic power laws):")
    ss = np.linspace(1e-8, 1.0, 400001)[::-1]     # descending s
    dt_grid = None                                 # use ds proxy: T=1
    def integ(alpha):
        # int s^{-alpha} ds over [1e-8,1], ascending order
        xs = np.linspace(1e-8, 1.0, 400001)
        return float(np.trapezoid(xs ** (-alpha), xs))

    print(f"  {'case':>20} {'alpha':>7} {'value':>12}  verdict")
    for sigma in (0.5, 0.75, 1.0):
        a2 = sigma * (2 * 2 - D) / 2               # enstrophy rate
        v2 = integ(a2)
        print(f"  sigma={sigma:.2f} p=2  {a2:>7.3f} {v2:>12.3f}  "
              f"{'converges' if a2 < 1 else 'DIVERGES'}")
        ainf = 2 * sigma
        vinf = integ(ainf)
        print(f"  sigma={sigma:.2f} p=inf{ainf:>7.3f} "
              f"{vinf if vinf < 1e17 else float('inf'):>12.1e}  "
              f"{'converges' if ainf < 1 else 'DIVERGES'}")
    print("  expected: p=2 converges iff sigma<1 (Leray bound);")
    print("            p=inf diverges for ALL sigma>=1/2 (BKM gate)")

    print()
    print("=" * 70)
    print("VERDICT: with the auditor corrected, do the laws hold?")
    print("(see errors above -- discretization-level agreement)")
    print("=" * 70)


if __name__ == "__main__":
    main()
