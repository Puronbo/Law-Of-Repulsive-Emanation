"""
Scaling test for GN inequality: does ||u||_inf / (E^a * Z^b) stay
bounded when u -> lambda * u?

If the inequality ||u||_inf <= C * E^a * Z^b is scaling-correct,
then under u -> lambda*u:
  LHS -> lambda * ||u||_inf
  RHS -> lambda^{2a+2b} * E^a * Z^b

So we need 2a+2b = 1, i.e. a+b = 1/2.

Test the exponents (2/5, 3/10) from previous work:
  a+b = 4/10 + 3/10 = 7/10 != 1/2  (NOT scaling-correct)

And test correct exponents with a+b=1/2.
"""
import numpy as np


def spectral_div(ux, uy, uz, h, n):
    k = np.fft.fftfreq(n, d=h/(2*np.pi))
    kx = k.reshape(n,1,1); ky = k.reshape(1,n,1); kz = k.reshape(1,1,n)
    return np.real(np.fft.ifftn(1j*kx*np.fft.fftn(ux) + 1j*ky*np.fft.fftn(uy) + 1j*kz*np.fft.fftn(uz)))


def tg_flow(lam, n=128):
    ax = np.linspace(0, 2*np.pi, n, endpoint=False); h = ax[1]-ax[0]
    X,Y,Z = np.meshgrid(ax,ax,ax,indexing="ij")
    return (lam*np.sin(X)*np.cos(Y)*np.cos(Z),
            lam*np.cos(X)*np.sin(Y)*np.cos(Z),
            -2*lam*np.cos(X)*np.cos(Y)*np.sin(Z), h)


def abc_flow(s, n=128):
    ax = np.linspace(0, 2*np.pi, n, endpoint=False); h = ax[1]-ax[0]
    X,Y,Z = np.meshgrid(ax,ax,ax,indexing="ij")
    return (s*np.sin(Z)+s*np.cos(Y), s*np.sin(X)+s*np.cos(Z),
            s*np.sin(Y)+s*np.cos(X), h)


def random_divfree(n, n_modes=30, scale=1.0, seed=42):
    rng = np.random.default_rng(seed)
    ax = np.linspace(0, 2*np.pi, n, endpoint=False); h = ax[1]-ax[0]
    X,Y,Z = np.meshgrid(ax,ax,ax,indexing="ij")
    ux = np.zeros((n,n,n)); uy = np.zeros((n,n,n)); uz = np.zeros((n,n,n))
    for _ in range(n_modes):
        kx,ky,kz = rng.integers(1,8,size=3)
        phase = rng.uniform(0, 2*np.pi)
        a = rng.standard_normal(3)
        kd = kx*X + ky*Y + kz*Z + phase
        ck = np.cos(kd)
        ux += scale*(ky*a[2]-kz*a[1])*ck
        uy += scale*(kz*a[0]-kx*a[2])*ck
        uz += scale*(kx*a[1]-ky*a[0])*ck
    return ux, uy, uz, h


def compute_quantities(ux, uy, uz, h):
    n = ux.shape[0]
    vol = (2*np.pi)**3
    u_inf = float(np.max(np.sqrt(ux**2+uy**2+uz**2)))
    E = float(np.sum(ux**2+uy**2+uz**2)*h**3/(2*vol))

    kx = np.fft.fftfreq(n,d=h/(2*np.pi)).reshape(n,1,1)
    ky = np.fft.fftfreq(n,d=h/(2*np.pi)).reshape(1,n,1)
    kz = np.fft.fftfreq(n,d=h/(2*np.pi)).reshape(1,1,n)
    ux_h = np.fft.fftn(ux); uy_h = np.fft.fftn(uy); uz_h = np.fft.fftn(uz)
    Z = float(np.sum(sum(
        np.real(np.fft.ifftn(1j*a*hhat))**2
        for a,hhat in [(kx,ux_h),(ky,ux_h),(kz,ux_h),
                       (kx,uy_h),(ky,uy_h),(kz,uy_h),
                       (kx,uz_h),(ky,uz_h),(kz,uz_h)]
    ))*h**3/vol)
    eps = Z  # nu=1

    return u_inf, E, Z, eps


def main():
    n = 96
    print("="*75)
    print("SCALING TEST: u -> lambda * u")
    print("="*75)

    # Test exponents
    exponents = [
        (2/5, 3/10, "OLD (2/5, 3/10)  a+b=0.70"),
        (1/4, 1/4, "CORRECTED (1/4, 1/4)  a+b=0.50"),
        (3/10, 1/5, "ALTERNATE (3/10, 1/5)  a+b=0.50"),
        (1/3, 1/6, "ALTERNATE (1/3, 1/6)  a+b=0.50"),
        (2/5, 1/10, "MIXED (2/5, 1/10)  a+b=0.50"),
    ]

    flows = [("TG", lambda lam: tg_flow(lam, n)),
             ("ABC", lambda lam: abc_flow(lam, n)),
             ("Rand", lambda lam: random_divfree(n, 30, lam, 42))]

    for a, b, label in exponents:
        print(f"\n--- Exponents: {label} ---")
        for name, gen in flows:
            ratios = []
            for lam in [0.125, 0.25, 0.5, 1, 2, 4, 8, 16]:
                ux,uy,uz,h = gen(lam)
                u_inf, E, Z, eps = compute_quantities(ux,uy,uz,h)
                rhs = E**a * Z**b if E > 0 and Z > 0 else 0
                ratio = u_inf / rhs if rhs > 0 else 0
                ratios.append((lam, ratio))
            # Check scaling: ratio should be CONSTANT if a+b=1/2
            r_vals = [r for _,r in ratios]
            if min(r_vals) > 0:
                spread = max(r_vals) / min(r_vals)
            else:
                spread = float('inf')
            print(f"  {name:5s}: ratio range [{min(r_vals):.4f}, {max(r_vals):.4f}], "
                  f"spread={spread:.2f}x, "
                  f"at lam=1: {ratios[3][1]:.4f}")

    # Also check Millennium ratio: u_inf / eps^{1/3}
    print(f"\n--- Millennium ratio: u_inf / eps^(1/3) ---")
    for name, gen in flows:
        ratios = []
        for lam in [0.125, 0.25, 0.5, 1, 2, 4, 8, 16]:
            ux,uy,uz,h = gen(lam)
            u_inf, E, Z, eps = compute_quantities(ux,uy,uz,h)
            rhs = eps**(1/3)
            ratio = u_inf / rhs if rhs > 0 else 0
            ratios.append((lam, ratio))
        r_vals = [r for _,r in ratios]
        spread = max(r_vals) / min(r_vals) if min(r_vals) > 0 else float('inf')
        print(f"  {name:5s}: ratio range [{min(r_vals):.4f}, {max(r_vals):.4f}], "
              f"spread={spread:.2f}x, at lam=1: {ratios[3][1]:.4f}")

    # Check scaling of Millennium ratio under u -> lambda*u
    print(f"\n--- SCALING ANALYSIS ---")
    print("  u -> lambda*u:  ||u||_inf -> lambda * ||u||_inf")
    print("                  eps = nu*Z -> lambda^2 * eps")
    print("                  eps^{1/3} -> lambda^{2/3} * eps^{1/3}")
    print("                  Mill ratio -> lambda^{1/3} * Mill_ratio")
    print("  => Mill ratio is NOT scaling-invariant either!")
    print("  => The Millennium bound ||u||_inf <= C * eps^{1/3} is")
    print("     only expected at a FIXED scale (inertial range),")
    print("     NOT as a universal bound for all divergence-free fields.")


if __name__ == "__main__":
    main()
