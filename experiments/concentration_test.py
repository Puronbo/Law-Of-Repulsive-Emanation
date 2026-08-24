"""
CONCENTRATION TEST: can divergence-free fields concentrate energy
into a tiny ball while keeping ||u||_inf large?

Physical analogy:
- "Ball" = region of high velocity
- "Heating" = energy concentration
- "Vacuum" = no dissipation (Euler, not NS)
- "Keeping shape" = energy stays concentrated (no spreading)

If div-free fields CAN concentrate: GN(1/4,1/4) might fail.
If div-free fields CANNOT concentrate: GN(1/4,1/4) holds.

Test: construct div-free fields with energy in a ball of radius R,
check if ||u||_inf / (||u||_L2 * ||grad u||_L2)^{1/2} blows up as R -> 0.
"""
import numpy as np


def spectral_div(ux,uy,uz,h,n):
    k = np.fft.fftfreq(n,d=h/(2*np.pi))
    kx=k.reshape(n,1,1); ky=k.reshape(1,n,1); kz=k.reshape(1,1,n)
    return np.real(np.fft.ifftn(1j*kx*np.fft.fftn(ux)+1j*ky*np.fft.fftn(uy)+1j*kz*np.fft.fftn(uz)))


def make_concentrated_divfree(n, R, scale=1.0, seed=42):
    """
    Try to concentrate a div-free field into a ball of radius R.

    Method 1: High-k random modes (div-free by construction)
    Method 2: Poloidal field (div-free by construction)
    Method 3: Vortex ring (div-free by construction)
    """
    ax = np.linspace(0, 2*np.pi, n, endpoint=False)
    h = ax[1] - ax[0]
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    cx, cy, cz = np.pi, np.pi, np.pi  # center of domain

    results = {}

    # === Method 1: High-k random Fourier modes ===
    # High k means short wavelength = concentrated
    k_max = int(max(2, min(n//3, 1.0/R)))
    rng = np.random.default_rng(seed)
    ux = np.zeros((n,n,n)); uy = np.zeros((n,n,n)); uz = np.zeros((n,n,n))
    n_modes = min(50, k_max**3)
    for _ in range(n_modes):
        kvec = rng.integers(max(1, k_max//2), k_max+1, size=3)
        phase = rng.uniform(0, 2*np.pi)
        a = rng.standard_normal(3)
        kd = kvec[0]*X + kvec[1]*Y + kvec[2]*Z + phase
        ck = np.cos(kd)
        ux += scale*(kvec[1]*a[2]-kvec[2]*a[1])*ck
        uy += scale*(kvec[2]*a[0]-kvec[0]*a[2])*ck
        uz += scale*(kvec[0]*a[1]-kvec[1]*a[0])*ck
    results["high_k_random"] = analyze(ux, uy, uz, h, n, R)

    # === Method 2: Localized poloidal field ===
    # A poloidal field is automatically div-free
    r = np.sqrt((X-cx)**2 + (Y-cy)**2 + (Z-cz)**2)
    # Gaussian envelope centered at (pi,pi,pi) with width R
    envelope = np.exp(-r**2 / (2*R**2))
    # Poloidal: u = curl(curl(f * e_r)) = div-free by construction
    # Simpler: u = curl(A) where A = f(r) * e_r is radial
    # Then div(u) = div(curl(A)) = 0 automatically
    fr = envelope  # radial function
    # A = fr * e_r (radial vector potential)
    # u = curl(A) = (1/r) d/dr(r * A_theta)... let me use a simpler form
    # For a sphere: u = curl(A x hat{r}) is automatically div-free
    # Let's use: u = grad x (fr * e_z) = (-d(fr)/dy, d(fr)/dx, 0)
    # But this is 2D. For 3D, use: u = curl(curl(fr * e_z))
    # = curl(-d(fr)/dy e_x + d(fr)/dx e_z)
    # = (d^2(fr)/dx dz, d^2(fr)/dy dz, -d^2(fr)/dx^2 - d^2(fr)/dy^2)
    # This is getting complicated. Let me use a simpler div-free construction.
    # u = curl(psi) where psi = (0, 0, fr * sin(theta))
    # Actually, simplest: u = (d(g)/dy, -d(g)/dx, 0) is div-free in 2D
    # For 3D, use: u = curl(A) with A = (0, 0, g(x,y,z))
    # Then u = (dg/dy, -dg/dx, 0) -- 2D-like
    # Or: u = (dg/dz, 0, -dg/dx) -- 2D-like in xz
    # Or: u = (0, dg/dz, -dg/dy) -- 2D-like in yz

    # Let's use the most concentrated one: a single poloidal mode
    # with angular momentum along z, concentrated at radius R
    theta = np.arctan2(Y-cy, X-cx)
    phi = np.arctan2(Z-cz, np.sqrt((X-cx)**2 + (Y-cy)**2))

    # Vortex ring: concentrated torus of radius R
    rho = np.sqrt((X-cx)**2 + (Y-cy)**2)
    z_local = Z - cz
    ring_r = np.sqrt((rho - R)**2 + z_local**2)
    ring_env = np.exp(-ring_r**2 / (2*(R/3)**2))

    # Velocity of vortex ring (dipole-like)
    # ux = -z_local * ring_env / (ring_r^2 + eps)
    # uy = (rho - R) * cos(theta) * ring_env / (ring_r^2 + eps)
    # This is not smooth. Use spectral construction instead.

    # Simplest concentrated div-free field: single high-k mode
    k_conc = int(2*np.pi / R)
    ux2 = np.sin(k_conc * X) * np.cos(k_conc * Y)
    uy2 = -np.cos(k_conc * X) * np.sin(k_conc * Y)
    uz2 = np.zeros_like(X)
    # Check div: d(ux)/dx + d(uy)/dy = k_conc*cos*cos + (-k_conc)*cos*cos = 0. Div-free!
    # But this is NOT concentrated in a ball -- it's periodic with wavelength 2pi/k_conc.
    # The "concentration" is in Fourier space (single mode), not physical space.

    results["single_mode_k"] = analyze(ux2, uy2, uz2, h, n, R)

    # === Method 3: Actually concentrated in physical space ===
    # Use a Gaussian envelope times a div-free oscillation
    # u = envelope(r) * (cos(kz), -sin(kz), 0) -- not div-free
    # Need to make it div-free. Use: u = curl(A) with A concentrated
    # A_z = envelope(r) * cos(kz)
    # u_x = dA_z/dy = -y * envelope'(r) * cos(kz) / r  ... messy

    # Simpler: use the poloidal-toroidal decomposition
    # A poloidal field: u = L(w) where L is the vector Laplacian-like operator
    # and w is a scalar stream function
    # u = (d^2 w/dx dz, d^2 w/dy dz, -d^2 w/dx^2 - d^2 w/dy^2 + d^2 w/dz^2)

    # Even simpler: u = curl(curl(w * e_z)) where w is concentrated
    # u = (d^2w/dxdz, d^2w/dydz, -d^2w/dx^2 - d^2w/dy^2)
    # This is automatically div-free!
    w = np.exp(-r**2 / (2*R**2))  # concentrated Gaussian
    # Compute curl(curl(w * e_z)) spectrally
    kx = np.fft.fftfreq(n, d=h/(2*np.pi)).reshape(n,1,1)
    ky = np.fft.fftfreq(n, d=h/(2*np.pi)).reshape(1,n,1)
    kz = np.fft.fftfreq(n, d=h/(2*np.pi)).reshape(1,1,n)
    w_hat = np.fft.fftn(w)

    # curl(w*e_z) = (dw/dy, -dw/dx, 0)
    curl_x = np.real(np.fft.ifftn(1j*ky*w_hat))
    curl_y = np.real(np.fft.ifftn(-1j*kx*w_hat))
    curl_z = np.zeros((n,n,n))

    # curl(curl(w*e_z)) = curl(curl_x, curl_y, 0)
    # = (d(0)/dy - d(curl_y)/dz, d(curl_x)/dz - d(0)/dx, d(curl_y)/dx - d(curl_x)/dy)
    curl_x_hat = np.fft.fftn(curl_x)
    curl_y_hat = np.fft.fftn(curl_y)
    ux3 = np.real(np.fft.ifftn(-1j*kz*curl_y_hat))
    uy3 = np.real(np.fft.ifftn(1j*kz*curl_x_hat))
    uz3 = np.real(np.fft.ifftn(1j*kx*curl_y_hat - 1j*ky*curl_x_hat))

    results["poloidal_concentrated"] = analyze(ux3, uy3, uz3, h, n, R)

    return results


def analyze(ux, uy, uz, h, n, R):
    """Compute all norms and GN ratio."""
    vol = (2*np.pi)**3
    u_sq = ux**2 + uy**2 + uz**2
    u_inf = float(np.max(np.sqrt(u_sq)))
    E = float(np.sum(u_sq)*h**3/(2*vol))
    L2 = np.sqrt(2*E)

    # L4 norm
    L4_4 = float(np.sum(u_sq**2)*h**3/vol)
    L4 = L4_4**(1/4)

    # Gradient norms
    kx = np.fft.fftfreq(n,d=h/(2*np.pi)).reshape(n,1,1)
    ky = np.fft.fftfreq(n,d=h/(2*np.pi)).reshape(1,n,1)
    kz = np.fft.fftfreq(n,d=h/(2*np.pi)).reshape(1,1,n)
    ux_h = np.fft.fftn(ux); uy_h = np.fft.fftn(uy); uz_h = np.fft.fftn(uz)
    grad_sq = sum(np.real(np.fft.ifftn(1j*a*hh))**2
                  for hh in [ux_h,uy_h,uz_h] for a in [kx,ky,kz])
    Z = float(np.sum(grad_sq)*h**3/vol)
    grad_L2 = np.sqrt(Z)

    # Divergence check
    div = spectral_div(ux,uy,uz,h,n)
    max_div = float(np.max(np.abs(div)))
    div_rel = max_div / u_inf if u_inf > 0 else 0

    # Physical-space concentration: where is the energy?
    # Compute "effective radius" of energy concentration
    # <r^2>_E = integral r^2 |u|^2 / integral |u|^2
    ax = np.linspace(0, 2*np.pi, n, endpoint=False)
    X,Y,Zg = np.meshgrid(ax,ax,ax,indexing="ij")
    cx = cy = cz = np.pi
    r2 = (X-cx)**2 + (Y-cy)**2 + (Zg-cz)**2
    r2_avg = float(np.sum(r2 * u_sq) * h**3 / np.sum(u_sq * h**3))
    r_eff = np.sqrt(r2_avg)

    # GN ratios
    gn14_rhs = L2**(1/2) * grad_L2**(1/2)
    gn14 = u_inf / gn14_rhs if gn14_rhs > 0 else 0

    gn1316_rhs = E**(1/3) * Z**(1/6) if E > 0 and Z > 0 else 0
    gn1316 = u_inf / gn1316_rhs if gn1316_rhs > 0 else 0

    return {
        "R": R, "r_eff": r_eff,
        "u_inf": u_inf, "E": E, "L2": L2, "L4": L4,
        "Z": Z, "grad_L2": grad_L2,
        "gn14": gn14, "gn1316": gn1316,
        "div_rel": div_rel,
    }


def main():
    n = 128
    print("="*75)
    print("CONCENTRATION TEST: can div-free fields concentrate energy?")
    print("="*75)
    print()
    print("If GN(1/4,1/4) can fail, we'll see gn14 -> infinity as R -> 0.")
    print("If GN(1/4,1/4) holds, gn14 stays bounded for all R.")
    print()

    # Test with decreasing radius R
    radii = [2.0, 1.0, 0.5, 0.25, 0.125, 0.0625]

    for method in ["high_k_random", "single_mode_k", "poloidal_concentrated"]:
        print(f"--- Method: {method} ---")
        gn14_vals = []
        for R in radii:
            res = make_concentrated_divfree(n, R, scale=1.0)
            d = res[method]
            gn14_vals.append(d["gn14"])
            print(f"  R={R:6.3f}: r_eff={d['r_eff']:.3f}  u_inf={d['u_inf']:.4f}  "
                  f"E={d['E']:.4f}  Z={d['Z']:.4f}  "
                  f"gn14={d['gn14']:.4f}  div={d['div_rel']:.1e}")

        gn14_arr = np.array(gn14_vals)
        if gn14_arr[-1] > gn14_arr[0] * 2:
            print(f"  WARNING: gn14 GROWING as R decreases! Might indicate failure.")
        else:
            print(f"  gn14 range: [{gn14_arr.min():.4f}, {gn14_arr.max():.4f}]  BOUNDED.")
        print()

    # Additional test: what is the theoretical minimum r_eff for div-free fields?
    print("--- Theoretical question ---")
    print("For a div-free field, can r_eff -> 0 while keeping E and Z fixed?")
    print("If r_eff -> 0, the field is concentrated in a point.")
    print("For div-free fields, this requires all 3 velocity components")
    print("to be large in the same small region, which is constrained by")
    print("div u = du_1/dx + du_2/dy + du_3/dz = 0.")
    print("The div-free constraint forces the components to 'cancel',")
    print("preventing arbitrary concentration.")


if __name__ == "__main__":
    main()
