"""
W1 TEST: GSUP AND SCALING FOR NON-SELF-SIMILAR CONCENTRATING SOLUTIONS
======================================================================
The self-similar family is irrotational (Lemma 5) and has
K ~ lam^((d-1)/3) (Lemma 4).  But this family is SPECIAL (radial).
The Millennium problem asks: can NON-radial concentrating solutions
exist?

Test: construct a non-radial initial condition (double vortex) and
verify whether:
  (a) K scales the same way (dimensional analysis is universal)
  (b) GSUP (||omega||_inf) grows in a way consistent with the
      Kolmogorov bound ||u||_inf <= C epsilon^{1/3}
  (c) The ratio ||u||_inf / epsilon^{1/3} remains bounded as the
      vortex intensifies

If (c) holds for a non-radial family, it's evidence the Kolmogorov
bound is universal (not just an artifact of radial symmetry).

If (c) fails, it's evidence the bound is tight and the Millennium
problem is genuinely hard.
"""
import numpy as np


def double_vortex_2d(lam, n=301):
    """Non-radial IC: two counter-rotating Gaussian vortices.
    u = sum of two radial profiles centered at (+-d0, 0)."""
    d0 = 0.3  # separation
    ws = 5.0 / lam
    ax = np.linspace(-ws, ws, n)
    h = ax[1] - ax[0]
    X, Y = np.meshgrid(ax, ax, indexing="ij")
    # Two vortices: +涡 at (-d0,0), -涡 at (+d0,0)
    R1 = np.sqrt((X + d0)**2 + Y**2)
    R2 = np.sqrt((X - d0)**2 + Y**2)
    R1[R1 < 1e-30] = 1e-30
    R2[R2 < 1e-30] = 1e-30
    # Velocity from each vortex: u_i = A(r_i) * e_ri
    A1 = lam * np.exp(-lam**2 * R1**2 / 2)
    A2 = -lam * np.exp(-lam**2 * R2**2 / 2)  # opposite sign
    ux = A1 * (X + d0) / R1 + A2 * (X - d0) / R2
    uy = A1 * Y / R1 + A2 * Y / R2
    return ux, uy, h, ax


def kolmogorov_ratio_2d(ux, uy, h):
    """K = ||u||_inf / epsilon^{1/3}, epsilon = int |grad u|^2."""
    g2 = (np.gradient(ux, h, axis=0)**2 + np.gradient(ux, h, axis=1)**2 +
          np.gradient(uy, h, axis=0)**2 + np.gradient(uy, h, axis=1)**2)
    eps = float(np.sum(g2) * h**2)
    u_inf = float(np.max(np.sqrt(ux**2 + uy**2)))
    return u_inf / eps**(1/3) if eps > 0 else 0


def vorticity_sup_2d(ux, uy, h):
    """||omega||_inf for 2D scalar vorticity."""
    omega = (np.gradient(uy, h, axis=0) - np.gradient(ux, h, axis=1))
    return float(np.max(np.abs(omega)))


def radial_vortex_2d(lam, n=301):
    """Single radial vortex (self-similar family) for comparison."""
    ws = 5.0 / lam
    ax = np.linspace(-ws, ws, n)
    h = ax[1] - ax[0]
    X, Y = np.meshgrid(ax, ax, indexing="ij")
    R = np.sqrt(X**2 + Y**2)
    R[R < 1e-30] = 1e-30
    A = lam * np.exp(-lam**2 * R**2 / 2)
    ux = A * X / R
    uy = A * Y / R
    return ux, uy, h, ax


def main():
    print("=" * 70)
    print("W1 TEST: NON-SELF-SIMILAR CONCENTRATING SOLUTIONS")
    print("=" * 70)
    print()
    print("Comparing single radial vortex (self-similar family)")
    print("vs double vortex (non-radial, not in the family).")
    print()

    results = []
    for lam in (1.0, 2.0, 4.0, 8.0, 16.0):
        # Radial (self-similar family)
        ux_r, uy_r, h_r, _ = radial_vortex_2d(lam)
        K_r = kolmogorov_ratio_2d(ux_r, uy_r, h_r)
        gs_r = vorticity_sup_2d(ux_r, uy_r, h_r)
        uinf_r = float(np.max(np.sqrt(ux_r**2 + uy_r**2)))

        # Double vortex (non-radial)
        ux_d, uy_d, h_d, _ = double_vortex_2d(lam)
        K_d = kolmogorov_ratio_2d(ux_d, uy_d, h_d)
        gs_d = vorticity_sup_2d(ux_d, uy_d, h_d)
        uinf_d = float(np.max(np.sqrt(ux_d**2 + uy_d**2)))

        # Kolmogorov bound: ||u||_inf <= C * epsilon^{1/3}
        # => K = ||u||_inf / epsilon^{1/3} <= C (bounded)
        # Also: ||omega||_inf <= C' * epsilon^{1/3} / nu^{2/3} (GSUP)
        # => GSUP/K should be O(1) if the bound is tight

        results.append({
            "lam": lam,
            "K_radial": K_r, "K_double": K_d,
            "gsup_radial": gs_r, "gsup_double": gs_d,
            "K_ratio": K_d / K_r if K_r > 0 else 0,
        })

        print(f"lam={lam:5.1f}:")
        print(f"  Radial:   K={K_r:.6f}  GSUP={gs_r:.2f}  ||u||_inf={uinf_r:.2f}")
        print(f"  Double:   K={K_d:.6f}  GSUP={gs_d:.2f}  ||u||_inf={uinf_d:.2f}")
        print(f"  K_ratio (double/radial): {K_d/K_r:.4f}")
        print()

    # Fit scaling exponents
    lams = [r["lam"] for r in results]
    log_lam = np.log(lams)
    for label, key in [("K_radial", "K_radial"), ("K_double", "K_double"),
                        ("GSUP_radial", "gsup_radial"), ("GSUP_double", "gsup_double")]:
        vals = [r[key] for r in results]
        # skip zeros
        mask = [v > 0 for v in vals]
        if sum(mask) >= 2:
            slope = np.polyfit([log_lam[i] for i in range(len(mask)) if mask[i]],
                               [np.log(vals[i]) for i in range(len(mask)) if mask[i]], 1)[0]
            print(f"  {label}: scaling exponent = {slope:.4f}")

    print()
    print("=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    print("""
If K_double scales the same way as K_radial (exponent ~ (d-1)/3),
then the dimensional analysis is universal: the Kolmogorov bound
depends only on the energy dissipation structure, not on the
specific geometry of the concentrating solution.

If K_double/K_radial remains O(1) across lam, the Kolmogorov
bound is equally tight for radial and non-radial solutions.

If GSUP/K stays O(1), the GSUP condition (||omega||_inf) is
equivalent to the Kolmogorov bound for both families.

If any of these ratios DIVERGES with lam, the Millennium problem
is harder: the bound is geometry-dependent and the self-similar
family is not the extremal case.
""")

    import json, os
    os.makedirs("data", exist_ok=True)
    with open("data/w1_double_vortex.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
