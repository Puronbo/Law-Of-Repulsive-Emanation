"""
W1 CONTINUED: multi-vortex test + Kolmogorov bound verification
==============================================================
Test: triple vortex (3-fold symmetry) + random 5-vortex IC.
Check whether non-radial geometry systematically reduces K.

Key question for Millennium: is the self-similar (single radial)
family the WORST CASE for the Kolmogorov bound?  If yes, proving
the bound for the radial family suffices.  If no, the bound is
geometry-dependent and harder.
"""
import numpy as np
import json, os


def multi_vortex_2d(lam, centers, signs, n=301):
    """General multi-vortex IC: sum of radial profiles at given centers."""
    ws = 5.0 / lam
    ax = np.linspace(-ws, ws, n)
    h = ax[1] - ax[0]
    X, Y = np.meshgrid(ax, ax, indexing="ij")
    ux = np.zeros_like(X)
    uy = np.zeros_like(Y)
    for (cx, cy), s in zip(centers, signs):
        R = np.sqrt((X - cx)**2 + (Y - cy)**2)
        R[R < 1e-30] = 1e-30
        A = s * lam * np.exp(-lam**2 * R**2 / 2)
        ux += A * (X - cx) / R
        uy += A * (Y - cy) / R
    return ux, uy, h


def K_and_gsup(ux, uy, h):
    g2 = (np.gradient(ux, h, axis=0)**2 + np.gradient(ux, h, axis=1)**2 +
          np.gradient(uy, h, axis=0)**2 + np.gradient(uy, h, axis=1)**2)
    eps = float(np.sum(g2) * h**2)
    u_inf = float(np.max(np.sqrt(ux**2 + uy**2)))
    omega = np.gradient(uy, h, axis=0) - np.gradient(ux, h, axis=1)
    gs = float(np.max(np.abs(omega)))
    K = u_inf / eps**(1/3) if eps > 0 else 0
    return K, gs, u_inf, eps


def main():
    print("=" * 70)
    print("W1: MULTI-VORTEX KOLMOGOROV BOUND TEST")
    print("=" * 70)

    # Configurations
    configs = {
        "single_radial":  ([(0, 0)],              [1]),
        "double":         ([(0.3, 0), (-0.3, 0)], [1, -1]),
        "triple":         ([(0.3, 0), (-0.15, 0.26), (-0.15, -0.26)], [1, 1, 1]),
        "triple_mixed":   ([(0.3, 0), (-0.15, 0.26), (-0.15, -0.26)], [1, -1, 1]),
        "quintet":        ([(0.3, 0), (0.093, 0.276), (-0.243, 0.170),
                            (-0.243, -0.170), (0.093, -0.276)],
                           [1, -1, 1, -1, 1]),
    }

    lams = [1.0, 2.0, 4.0, 8.0, 16.0]
    all_results = {}

    for name, (centers, signs) in configs.items():
        rows = []
        for lam in lams:
            ux, uy, h = multi_vortex_2d(lam, centers, signs)
            K, gs, uinf, eps = K_and_gsup(ux, uy, h)
            rows.append({"lam": lam, "K": K, "gsup": gs, "u_inf": uinf, "eps": eps})
        # fit exponent
        log_lam = np.log(lams)
        log_K = np.log([r["K"] for r in rows])
        exp = float(np.polyfit(log_lam, log_K, 1)[0])
        all_results[name] = {"rows": rows, "exponent": exp}
        print(f"\n{name} ({len(centers)} vortices):")
        for r in rows:
            print(f"  lam={r['lam']:5.1f}  K={r['K']:.6f}  GSUP={r['gsup']:.2f}  "
                  f"||u||={r['u_inf']:.2f}  eps={r['eps']:.2f}")
        print(f"  K scaling exponent: {exp:.4f}")

    # Summary table
    print("\n" + "=" * 70)
    print("SUMMARY: K SCALING EXPONENTS")
    print("=" * 70)
    for name, data in all_results.items():
        n_v = len(configs[name][0])
        print(f"  {name:20s} ({n_v} vortices): exponent = {data['exponent']:.4f}")

    print("\n" + "=" * 70)
    print("MILLENNIUM IMPLICATION")
    print("=" * 70)
    print("""
If the K exponent for non-radial configurations is ALWAYS <= (d-1)/3,
then the self-similar (single radial) family is the WORST CASE:
it has the largest K for given energy dissipation.

This means: proving the Kolmogorov bound ||u||_inf <= C*eps^{1/3}
for the self-similar family suffices to establish it as a UNIVERSAL
bound for all concentrating solutions.

The self-similar family would then be the extremal case of the
Kolmogorov inequality — the configuration that makes the bound
tightest.
""")

    os.makedirs("data", exist_ok=True)
    with open("data/w1_multi_vortex.json", "w") as f:
        json.dump(all_results, f, indent=2, default=str)


if __name__ == "__main__":
    main()
