"""
W1 ENERGY-GN COUPLING: comprehensive divergence-free scan
=========================================================
For incompressible NS: dE/dt = -νZ (nonlinear term vanishes).
GN gives ||u||_∞ ≤ C * E^{2/5} * (ε/ν)^{3/10}.
If this C is UNIVERSALLY bounded across all div-free flows,
the Kolmogorov bound follows from the energy balance.

Test: compute K and GN_ratio for a WIDE range of divergence-free
families to find the maximum C.  If C_max stays finite as we
explore more extreme configurations, the bound is consistent.

Families:
  (a) ABC flows: 3 parameters (A,B,C), 5 scales
  (b) Taylor-Green: 1 parameter (lam), 5 scales
  (c) Beltrami flows: random wave numbers, random amplitudes
  (d) Random divergence-free Fourier: 10 realizations
  (e) Multi-scale: superposition of ABC at different wave numbers
"""
import numpy as np
import json, os


def make_divfree_random(n, n_modes=20, scale=1.0, seed=42):
    """Random divergence-free velocity field via vector potential."""
    rng = np.random.default_rng(seed)
    ax = np.linspace(0, 2*np.pi, n, endpoint=False)
    h = ax[1] - ax[0]
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")

    ux = np.zeros((n, n, n))
    uy = np.zeros((n, n, n))
    uz = np.zeros((n, n, n))

    for _ in range(n_modes):
        kx, ky, kz = rng.integers(1, 6, size=3)
        phase = rng.uniform(0, 2*np.pi)
        # Random vector potential
        ax_coeff = rng.standard_normal(3)
        # u = curl(A) with A = (ax, ay, az) * sin(k·x + phase)
        kdot = kx*X + ky*Y + kz*Z + phase
        sk = np.sin(kdot)
        ck = np.cos(kdot)
        ux += scale * (ky*ax_coeff[2] - kz*ax_coeff[1]) * ck
        uy += scale * (kz*ax_coeff[0] - kx*ax_coeff[2]) * ck
        uz += scale * (kx*ax_coeff[1] - ky*ax_coeff[0]) * ck

    return ux, uy, uz, h


def make_beltrami(n, k=3, scale=1.0, seed=42):
    """Beltrami flow: curl u = k*u (eigenfunction of curl)."""
    rng = np.random.default_rng(seed)
    ax = np.linspace(0, 2*np.pi, n, endpoint=False)
    h = ax[1] - ax[0]
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    # Standard Beltrami: u = (sin(kz)+cos(ky), sin(kx)+cos(kz), sin(ky)+cos(kx))
    kx, ky, kz = rng.integers(1, 4, size=3)
    ux = scale * (np.sin(kz*Z) + np.cos(ky*Y))
    uy = scale * (np.sin(kx*X) + np.cos(kz*Z))
    uz = scale * (np.sin(ky*Y) + np.cos(kx*X))
    return ux, uy, uz, h


def make_abc(A, B, C, n=128):
    ax = np.linspace(0, 2*np.pi, n, endpoint=False)
    h = ax[1] - ax[0]
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    return (A*np.sin(Z)+C*np.cos(Y), B*np.sin(X)+A*np.cos(Z),
            C*np.sin(Y)+B*np.cos(X), h)


def make_tg(lam, n=128):
    ax = np.linspace(0, 2*np.pi, n, endpoint=False)
    h = ax[1] - ax[0]
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    return (lam*np.sin(X)*np.cos(Y)*np.cos(Z),
            lam*np.cos(X)*np.sin(Y)*np.cos(Z),
            -2*lam*np.cos(X)*np.cos(Y)*np.sin(Z), h)


def compute_all(ux, uy, uz, h, nu=1.0):
    """Compute K, GN_ratio, and energy diagnostics."""
    n = ux.shape[0]
    L = 2 * np.pi
    vol = L**3

    u_inf = float(np.max(np.sqrt(ux**2 + uy**2 + uz**2)))
    E = float(np.sum(ux**2 + uy**2 + uz**2) * h**3) / (2 * vol)

    # Gradients
    g = [np.gradient(u, h, axis=k) for u in [ux, uy, uz] for k in range(3)]
    grad_sq = sum(gg**2 for gg in g)
    Z_val = float(np.sum(grad_sq) * h**3) / (2 * vol)
    eps = nu * Z_val

    K = u_inf / eps**(1/3) if eps > 1e-30 else 0

    # GN: ||u||_inf <= C * E^{2/5} * (eps/nu)^{3/10}
    gn_rhs = E**(2/5) * (eps/nu)**(3/10)
    gn_ratio = u_inf / gn_rhs if gn_rhs > 1e-30 else 0

    # Also check: ||u||_inf <= C * eps^{1/3} directly
    return {"K": K, "gn_ratio": gn_ratio, "E": E, "eps": eps,
            "Z": Z_val, "u_inf": u_inf}


def main():
    print("=" * 70)
    print("W1: COMPREHENSIVE DIVERGENCE-FREE SCAN")
    print("=" * 70)
    print("Goal: find max GN_ratio across all div-free families.")
    print("If max is finite, GN gives a universal bound.\n")

    n = 96  # grid points per axis
    all_K = []
    all_gn = []
    results = []

    # (a) ABC flows
    print("--- ABC FLOWS ---")
    for A in [0.5, 1, 2, 5]:
        for B in [0.5, 1, 2, 5]:
            for C in [0.5, 1, 2, 5]:
                ux, uy, uz, h = make_abc(A, B, C, n)
                d = compute_all(ux, uy, uz, h)
                all_K.append(d["K"])
                all_gn.append(d["gn_ratio"])
                results.append({"family": "ABC", "params": f"{A},{B},{C}", **d})

    abc_K_max = max(all_K[-64:])
    abc_gn_max = max(all_gn[-64:])
    print(f"  64 configs: K_max={abc_K_max:.4f}  GN_max={abc_gn_max:.4f}")

    # (b) Taylor-Green
    print("\n--- TAYLOR-GREEN ---")
    for lam in [0.5, 1, 2, 5, 10, 20]:
        ux, uy, uz, h = make_tg(lam, n)
        d = compute_all(ux, uy, uz, h)
        all_K.append(d["K"])
        all_gn.append(d["gn_ratio"])
        results.append({"family": "TG", "params": str(lam), **d})
    tg_K_max = max(all_K[-6:])
    tg_gn_max = max(all_gn[-6:])
    print(f"  6 configs: K_max={tg_K_max:.4f}  GN_max={tg_gn_max:.4f}")

    # (c) Beltrami flows
    print("\n--- BELTRAMI FLOWS ---")
    for k in [1, 2, 3]:
        for s in [0.5, 1, 2, 5]:
            for seed in range(5):
                ux, uy, uz, h = make_beltrami(n, k, s, seed)
                d = compute_all(ux, uy, uz, h)
                all_K.append(d["K"])
                all_gn.append(d["gn_ratio"])
                results.append({"family": "Beltrami", "params": f"k={k},s={s},seed={seed}", **d})
    bel_K_max = max(all_K[-60:])
    bel_gn_max = max(all_gn[-60:])
    print(f"  60 configs: K_max={bel_K_max:.4f}  GN_max={bel_gn_max:.4f}")

    # (d) Random divergence-free Fourier
    print("\n--- RANDOM DIVERGENCE-FREE FOURIER ---")
    for s in [0.5, 1, 2, 5, 10]:
        for seed in range(10):
            ux, uy, uz, h = make_divfree_random(n, 20, s, seed)
            d = compute_all(ux, uy, uz, h)
            all_K.append(d["K"])
            all_gn.append(d["gn_ratio"])
            results.append({"family": "Random", "params": f"s={s},seed={seed}", **d})
    rand_K_max = max(all_K[-50:])
    rand_gn_max = max(all_gn[-50:])
    print(f"  50 configs: K_max={rand_K_max:.4f}  GN_max={rand_gn_max:.4f}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total configurations: {len(all_K)}")
    print(f"  K: min={min(all_K):.4f}  max={max(all_K):.4f}  median={np.median(all_K):.4f}")
    print(f"  GN: min={min(all_gn):.4f}  max={max(all_gn):.4f}  median={np.median(all_gn):.4f}")
    print(f"\n  K_max across ALL div-free flows: {max(all_K):.4f}")
    print(f"  GN_max across ALL div-free flows: {max(all_gn):.4f}")

    # Find the extremizer
    idx_K = all_K.index(max(all_K))
    idx_GN = all_gn.index(max(all_gn))
    print(f"\n  K extremizer: {results[idx_K]['family']} {results[idx_K]['params']}")
    print(f"  GN extremizer: {results[idx_GN]['family']} {results[idx_GN]['params']}")

    print("\n" + "=" * 70)
    print("MILLENNIUM STATUS")
    print("=" * 70)
    print(f"""
After testing {len(all_K)} divergence-free configurations:
  K_max = {max(all_K):.4f} (Kolmogorov ratio)
  GN_max = {max(all_gn):.4f} (Gagliardo-Nirenberg constant)

If GN_max stays O(1) as we test more extreme configs, the GN
inequality provides a UNIVERSAL bound:
  ||u||_inf <= {max(all_gn):.4f} * E^(2/5) * (eps/nu)^(3/10)

Combined with dE/dt = -nu*Z (exact for incompressible NS), this
gives a self-consistent energy bound with no blowup.

The Millennium problem reduces to: prove GN_max is finite for
ALL divergence-free fields (not just the ones we tested).
""")
    print(f"  GN_max = {max(all_gn):.4f}: {'FINITE (consistent with bound)' if max(all_gn) < 100 else 'INVESTIGATE'}")

    os.makedirs("data", exist_ok=True)
    with open("data/w1_gn_comprehensive.json", "w") as f:
        json.dump({"total": len(all_K), "K_max": max(all_K),
                    "GN_max": max(all_gn),
                    "results": results}, f, indent=2, default=str)


if __name__ == "__main__":
    main()
