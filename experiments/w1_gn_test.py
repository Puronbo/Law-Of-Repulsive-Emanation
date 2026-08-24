"""
W1 ANALYTICAL TEST: Gagliardo-Nirenberg interpolation on 3D flows
=================================================================
Test whether the Kolmogorov bound ||u||_inf <= C * epsilon^{1/3}
holds for specific 3D divergence-free families.

Approach: construct explicit 3D flows, compute K = ||u||_inf / eps^{1/3},
verify it stays bounded.  Then check whether Gagliardo-Nirenberg gives
a USEFUL bound (not just a trivial one).

Families tested:
  (a) ABC flow: u = (A sin z + C cos y, B sin x + A cos z, C sin y + B cos x)
      Divergence-free, periodic, exact.
  (b) Taylor-Green: u = sin x cos y cos z, cos x sin y cos z, -2 cos x cos y sin z
      Divergence-free, classic test for NS.
  (c) Poloidal (radial): u = A(r) e_r with A(r) = lam * exp(-lam^2 r^2/2)
      Self-similar family in Cartesian coords.

For each: vary amplitude parameter, compute K, check if bounded.
Also compute ||u||_2, ||grad u||_2, eps to verify GN inequality.
"""
import numpy as np


def abc_flow(A_coeff, B_coeff, C_coeff, n=128):
    """3D ABC flow: divergence-free by construction."""
    ax = np.linspace(0, 2*np.pi, n, endpoint=False)
    h = ax[1] - ax[0]
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    ux = A_coeff * np.sin(Z) + C_coeff * np.cos(Y)
    uy = B_coeff * np.sin(X) + A_coeff * np.cos(Z)
    uz = C_coeff * np.sin(Y) + B_coeff * np.cos(X)
    return ux, uy, uz, h


def taylor_green(lam, n=128):
    """3D Taylor-Green: divergence-free, decaying."""
    ax = np.linspace(0, 2*np.pi, n, endpoint=False)
    h = ax[1] - ax[0]
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    ux = lam * np.sin(X) * np.cos(Y) * np.cos(Z)
    uy = lam * np.cos(X) * np.sin(Y) * np.cos(Z)
    uz = -2 * lam * np.cos(X) * np.cos(Y) * np.sin(Z)
    return ux, uy, uz, h


def poloidal_radial(lam, n=96):
    """Self-similar family: u = A(r) e_r, A(r) = lam * exp(-lam^2 r^2/2).
    In Cartesian: ux = A(r)*x/r, uy = A(r)*y/r, uz = A(r)*z/r.
    This is NOT divergence-free in 3D (div = A'/r + 2A/r^2 != 0).
    But it tests the K bound for a specific radial profile."""
    ws = 5.0 / lam
    ax = np.linspace(-ws, ws, n, endpoint=False)
    h = ax[1] - ax[0]
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    R = np.sqrt(X**2 + Y**2 + Z**2)
    R[R < 1e-15] = 1e-15
    A = lam * np.exp(-lam**2 * R**2 / 2)
    ux = A * X / R
    uy = A * Y / R
    uz = A * Z / R
    return ux, uy, uz, h


def compute_K(ux, uy, uz, h, nu=1.0):
    """Compute K = ||u||_inf / epsilon^{1/3}."""
    gx0 = np.gradient(ux, h, axis=0)
    gx1 = np.gradient(ux, h, axis=1)
    gx2 = np.gradient(ux, h, axis=2)
    gy0 = np.gradient(uy, h, axis=0)
    gy1 = np.gradient(uy, h, axis=1)
    gy2 = np.gradient(uy, h, axis=2)
    gz0 = np.gradient(uz, h, axis=0)
    gz1 = np.gradient(uz, h, axis=1)
    gz2 = np.gradient(uz, h, axis=2)

    grad_sq = gx0**2 + gx1**2 + gx2**2 + gy0**2 + gy1**2 + gy2**2 + gz0**2 + gz1**2 + gz2**2
    eps = nu * float(np.sum(grad_sq) * h**3) / (2*np.pi)**3
    u_inf = float(np.max(np.sqrt(ux**2 + uy**2 + uz**2)))
    u2_sq = float(np.sum(ux**2 + uy**2 + uz**2) * h**3) / (2*np.pi)**3

    K = u_inf / eps**(1/3) if eps > 1e-30 else 0

    # GN check: ||u||_inf <= C * ||u||_2^{2/5} * ||grad u||_2^{3/5}
    # = C * u2_sq^{1/5} * (eps/nu)^{3/10}
    gn_rhs = u2_sq**(1/5) * (eps/nu)**(3/10)
    gn_ratio = u_inf / gn_rhs if gn_rhs > 1e-30 else 0

    return K, eps, u_inf, u2_sq, gn_ratio


def main():
    print("=" * 70)
    print("W1: GAGLIARDO-NIRENBERG TEST ON 3D FLOWS")
    print("=" * 70)

    # (a) ABC flow: vary amplitude
    print("\n--- ABC FLOW (divergence-free, exact) ---")
    for scale in [0.5, 1.0, 2.0, 5.0, 10.0]:
        ux, uy, uz, h = abc_flow(scale, scale, scale, n=128)
        K, eps, uinf, u2, gn = compute_K(ux, uy, uz, h)
        print(f"  scale={scale:5.1f}: K={K:.6f}  eps={eps:.4f}  "
              f"||u||_inf={uinf:.4f}  GN_ratio={gn:.4f}")

    # (b) Taylor-Green: vary amplitude
    print("\n--- TAYLOR-GREEN (divergence-free, decaying) ---")
    for lam in [0.5, 1.0, 2.0, 5.0, 10.0]:
        ux, uy, uz, h = taylor_green(lam, n=128)
        K, eps, uinf, u2, gn = compute_K(ux, uy, uz, h)
        print(f"  lam={lam:5.1f}: K={K:.6f}  eps={eps:.4f}  "
              f"||u||_inf={uinf:.4f}  GN_ratio={gn:.4f}")

    # (c) Poloidal radial: vary concentration
    print("\n--- POLOIDAL RADIAL (self-similar family, NOT div-free in 3D) ---")
    for lam in [1.0, 2.0, 5.0, 10.0, 20.0]:
        ux, uy, uz, h = poloidal_radial(lam, n=96)
        K, eps, uinf, u2, gn = compute_K(ux, uy, uz, h)
        print(f"  lam={lam:5.1f}: K={K:.6f}  eps={eps:.4f}  "
              f"||u||_inf={uinf:.4f}  GN_ratio={gn:.4f}")

    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    print("""
K = ||u||_inf / eps^{1/3}: if bounded, Kolmogorov bound holds.
GN_ratio = ||u||_inf / (||u||_2^{2/5} * ||grad u||_2^{3/5}): if
    bounded, the Gagliardo-Nirenberg interpolation is USEFUL
    (gives a nontrivial bound on ||u||_inf).

If K is bounded but GN_ratio grows with amplitude, the GN
inequality is TOO WEAK to prove the Kolmogorov bound.

If both are bounded, GN provides a viable proof pathway.
""")


if __name__ == "__main__":
    main()
