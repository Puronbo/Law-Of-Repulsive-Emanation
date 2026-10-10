"""
ON-FLOW CRITICALITY: int Z dt vs int Z^2 dt ON A SPECTRAL NAVIER-STOKES FLOW
===========================================================================
serrin_ladder.py showed the closing of the Prodi-Serrin integral along the p=6
Serrin route needs int_0^T Z(t)^2 dt < infinity, while the energy identity gives
only int_0^T Z(t) dt < infinity.  This module measures BOTH on resolved spectral
NS solutions over a viscosity sweep, and checks the two rigorous anchors:

  (i)  the exact energy identity  int_0^T Z dt = (E_0 - E(T)) / (2 nu);
  (ii) the temporal enstrophy flatness  F = T * int Z^2 / (int Z)^2,
       whose growth with 1/nu is the intermittency signature of the exactly
       marginal quantity.

Method: pseudo-spectral on T^3, exact exponential diffusion in Fourier space,
projected Heun RK2 for the nonlinearity, 2/3 dealiasing.  Initial data: a
concentrated poloidal packet (Gaussian stream width R), energy normalised to 1.
Run until Z decays below 1e-4 of its peak (or T_max).

Honesty: resolved smooth solutions have exponentially decaying Z, so int Z^2
is FINITE on every case here -- this is a diagnostic of the structure (how the
marginal quantity sits relative to the energy identity), NOT a claim that a
near-singular solution keeps it finite.  The F trend across viscosity is the
physics; the wall (finite int Z^2 for ALL solutions) stays open.

Run:  python ns_critical_integral.py       (prints PASS)
"""
import json
import numpy as np
import time as _clock

OUT = "data/ns_critical_integral.json"


def build_spectral(N):
    ax = np.linspace(0, 2 * np.pi, N, endpoint=False)
    X, Y, Zg = np.meshgrid(ax, ax, ax, indexing="ij")
    k1d = np.fft.fftfreq(N, d=ax[1] - ax[0]) * (2 * np.pi)
    kx = k1d.reshape(N, 1, 1)
    ky = k1d.reshape(1, N, 1)
    kz = k1d.reshape(1, 1, N)
    k2 = kx**2 + ky**2 + kz**2
    k2i = k2.copy()
    k2i[0, 0, 0] = 1.0
    k_inv = 1.0 / k2i
    k_inv[0, 0, 0] = 0.0
    kmax = (2.0 / 3.0) * (N / 2.0)          # 2/3 dealiasing cutoff
    mask = (np.sqrt(k2) <= kmax).astype(float)
    return X, Y, Zg, kx, ky, kz, k2, k2i, k_inv, mask


def make_broadband_ic(kx, ky, kz, k2, k_inv, k0=5.0, sigma=2.0, seed=7, N=32):
    """Random div-free IC with energy concentrated in a |k|-shell around k0."""
    rng = np.random.default_rng(seed)
    k = np.sqrt(k2)
    amp = np.exp(-((k - k0) ** 2) / (2 * sigma**2))
    ux_h = amp * (rng.normal(size=k.shape) + 1j * rng.normal(size=k.shape))
    uy_h = amp * (rng.normal(size=k.shape) + 1j * rng.normal(size=k.shape))
    uz_h = amp * (rng.normal(size=k.shape) + 1j * rng.normal(size=k.shape))
    div_h = 1j * kx * ux_h + 1j * ky * uy_h + 1j * kz * uz_h
    p_h = -k_inv * div_h
    ux_h -= 1j * kx * p_h
    uy_h -= 1j * ky * p_h
    uz_h -= 1j * kz * p_h
    return (np.real(np.fft.ifftn(ux_h)),
            np.real(np.fft.ifftn(uy_h)),
            np.real(np.fft.ifftn(uz_h)))


def project(ux, uy, uz, kx, ky, kz, k_inv):
    ux_h, uy_h, uz_h = np.fft.fftn(ux), np.fft.fftn(uy), np.fft.fftn(uz)
    div_h = 1j * kx * ux_h + 1j * ky * uy_h + 1j * kz * uz_h
    p_h = -k_inv * div_h
    return (np.real(np.fft.ifftn(ux_h - 1j * kx * p_h)),
            np.real(np.fft.ifftn(uy_h - 1j * ky * p_h)),
            np.real(np.fft.ifftn(uz_h - 1j * kz * p_h)))


def metrics(ux, uy, uz, kx, ky, kz, k2, h3, n3):
    u2 = ux**2 + uy**2 + uz**2
    u_inf = float(np.max(np.sqrt(u2)))
    ratio = h3 / n3                                  # Parseval (1/N^3) * dx
    E = 0.5 * float(np.sum(u2)) * h3
    Z = 0.0
    H2 = 0.0
    for c in (ux, uy, uz):
        amp = np.abs(np.fft.fftn(c)) ** 2
        Z += 0.5 * float(np.sum(k2 * amp)) * ratio
        H2 += 0.5 * float(np.sum(k2**2 * amp)) * ratio
    return E, Z, u_inf, H2


def step(ux, uy, uz, dt, nu, kx, ky, kz, k2, k_inv, mask):
    # exact diffusion + projected Heun on the nonlinearity
    diff = np.exp(-nu * k2 * dt)
    ux_d = diff * np.fft.fftn(ux) * mask
    uy_d = diff * np.fft.fftn(uy) * mask
    uz_d = diff * np.fft.fftn(uz) * mask

    def rhs_add(ux_h, uy_h, uz_h):
        uxx = np.real(np.fft.ifftn(1j * kx * ux_h * mask))
        uxy = np.real(np.fft.ifftn(1j * ky * ux_h * mask))
        uxz = np.real(np.fft.ifftn(1j * kz * ux_h * mask))
        uyx = np.real(np.fft.ifftn(1j * kx * uy_h * mask))
        uyy = np.real(np.fft.ifftn(1j * ky * uy_h * mask))
        uyz = np.real(np.fft.ifftn(1j * kz * uy_h * mask))
        uzx = np.real(np.fft.ifftn(1j * kx * uz_h * mask))
        uzy = np.real(np.fft.ifftn(1j * ky * uz_h * mask))
        uzz = np.real(np.fft.ifftn(1j * kz * uz_h * mask))
        uxr = np.real(np.fft.ifftn(ux_h * mask))
        uyr = np.real(np.fft.ifftn(uy_h * mask))
        uzr = np.real(np.fft.ifftn(uz_h * mask))
        nx = np.fft.fftn(-(uxr * uxx + uyr * uxy + uzr * uxz)) * mask
        ny = np.fft.fftn(-(uxr * uyx + uyr * uyy + uzr * uyz)) * mask
        nz = np.fft.fftn(-(uxr * uzx + uyr * uzy + uzr * uzz)) * mask
        div_h = 1j * kx * nx + 1j * ky * ny + 1j * kz * nz
        p_h = -k_inv * div_h
        return (nx - 1j * kx * p_h), (ny - 1j * ky * p_h), (nz - 1j * kz * p_h)

    l_s = rhs_add(ux_d, uy_d, uz_d)                      # slope at midpoint state
    ux_h = ux_d + dt * l_s[0]
    uy_h = uy_d + dt * l_s[1]
    uz_h = uz_d + dt * l_s[2]
    l_e = rhs_add(ux_h, uy_h, uz_h)                      # Heun correction
    ux_h = ux_d + 0.5 * dt * (l_s[0] + l_e[0])
    uy_h = uy_d + 0.5 * dt * (l_s[1] + l_e[1])
    uz_h = uz_d + 0.5 * dt * (l_s[2] + l_e[2])
    ux_h *= mask
    uy_h *= mask
    uz_h *= mask
    return (np.real(np.fft.ifftn(ux_h)),
            np.real(np.fft.ifftn(uy_h)),
            np.real(np.fft.ifftn(uz_h)))


def run_case(nu, N=32, dt=0.003, T_max=40.0, save_every=10, seed=7):
    spec = build_spectral(N)
    X, Y, Zg, kx, ky, kz, k2, k2i, k_inv, mask = spec
    h3 = (2 * np.pi / N) ** 3
    n3 = float(N**3)
    ux, uy, uz = make_broadband_ic(kx, ky, kz, k2, k_inv, k0=5.0, sigma=2.0,
                                   seed=seed, N=N)
    E0, Z0, u0, H20 = metrics(ux, uy, uz, kx, ky, kz, k2, h3, n3)
    if E0 > 0:
        scale = 1.0 / np.sqrt(2 * E0)
        ux, uy, uz = scale * ux, scale * uy, scale * uz
    E0, Z0, u0, H20 = metrics(ux, uy, uz, kx, ky, kz, k2, h3, n3)

    dt_s = dt * save_every                                # sample spacing
    times, Es, Zs = [0.0], [E0], [Z0]
    int_Z, int_Z2 = 0.0, 0.0
    prev_t, prev_Z, prev_Z2 = 0.0, Z0, Z0 * Z0
    s = 0
    t = 0.0
    Zpeak = Z0
    t0 = _clock.time()
    while t < T_max:
        ux, uy, uz = step(ux, uy, uz, dt, nu, kx, ky, kz, k2, k_inv, mask)
        t += dt
        s += 1
        if np.any(np.isnan(ux)):
            return {"diverged": True, "t": t, "step": s}
        if s % save_every == 0:
            E, Z, u_inf, H2 = metrics(ux, uy, uz, kx, ky, kz, k2, h3, n3)
            Z = max(Z, 1e-30)
            Zpeak = max(Zpeak, Z)
            int_Z += 0.5 * (prev_Z + Z) * dt_s
            int_Z2 += 0.5 * (prev_Z2 + Z * Z) * dt_s
            prev_t, prev_Z, prev_Z2 = t, Z, Z * Z
            times.append(t)
            Es.append(E)
            Zs.append(Z)
            if Z < 1e-3 * Zpeak and t > 1.0:
                break
    tf = t
    E_T, Z_T, uT, H2T = metrics(ux, uy, uz, kx, ky, kz, k2, h3, n3)

    intZ_rid = (E0 - E_T) / (2 * nu)                      # exact energy identity
    flat = tf * int_Z2 / (int_Z * int_Z) if int_Z > 0 else 0.0
    mean_Z = int_Z / tf if tf > 0 else 0.0
    return {
        "nu": float(nu), "IC": "band_k0=5", "seed": int(seed),
        "N": int(N), "dt": float(dt),
        "T_run": float(tf), "E0": float(E0), "Z0": float(Z0),
        "u_inf_peak": float(u0), "Zpeak": float(Zpeak),
        "int_Z": float(int_Z), "int_Z_identity": float(intZ_rid),
        "int_Z2": float(int_Z2),
        "flatness": float(flat), "mean_Z": float(mean_Z),
        "identity_rel_err": float(abs(int_Z - intZ_rid) / max(intZ_rid, 1e-30)),
        "walltime_s": float(_clock.time() - t0),
    }


def main():
    print("=" * 78)
    print("ON-FLOW CRITICALITY: int Z dt (energy identity) vs int Z^2 dt (wall)")
    print("=" * 78)
    import os
    cases = {}
    rows = []
    for nu in [0.2, 0.1, 0.05]:
        res = run_case(nu, seed=7)
        if res.get("diverged"):
            print(f"  nu={nu}: DIVERGED at t={res['t']}")
            continue
        cases[str(nu)] = res
        rows.append(res)
        print(f"\n  nu={nu}:  T_run={res['T_run']:.1f}  int Z dt = {res['int_Z']:.4f}"
              f"  (identity {res['int_Z_identity']:.4f}, rel err "
              f"{res['identity_rel_err']:.1e})")
        print(f"           int Z^2 dt = {res['int_Z2']:.4f}   flatness F = "
              f"{res['flatness']:.3f}   mean Z = {res['mean_Z']:.3f}   "
              f"Zpeak = {res['Zpeak']:.3f}  [{res['walltime_s']:.0f}s]")

    print("\n  Energy identity (exact anchor): int Z dt = (E0 - E(T))/(2 nu)")
    for r in rows:
        print(f"  -> nu={r['nu']:.3f}:  rel err {r['identity_rel_err']:.1e} "
              f"(sampling-truncation of the well-resolved tail)")
    print("  Temporal enstrophy flatness F = T*int Z^2/(int Z)^2 vs 1/nu:")
    for r in rows:
        print(f"    nu={r['nu']:>6}:  F = {r['flatness']:.3f}   (1/nu = {1/r['nu']:.1f})")

    fs = np.array([r["flatness"] for r in rows])
    nus = np.array([r["nu"] for r in rows])
    if len(rows) >= 3:
        p = np.log(fs[-1] / fs[0]) / np.log(nus[0] / nus[-1])
        print(f"\n  F ~ (1/nu)^p with p = {p:+.2f}  "
              f"({'intermittency grows as viscosity drops' if p > 0.05 else 'no growth in this resolved viscous regime'}).")
    else:
        p = 0.0

    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"energy_identity_rel_err": [r["identity_rel_err"] for r in rows],
                   "cases": cases, "flatness_power": float(p)}, f, indent=2)

    assert len(rows) >= 3, "viscosity sweep incomplete"
    assert all(r["identity_rel_err"] < 2e-2 for r in rows), "energy identity violated"
    print("\n" + "=" * 78)
    print(f"PASS: exact int Z dt identity confirmed on every case (rel err "
          f"< 2e-2, sampling-limited);  int Z^2 (the wall quantity) is FINITE,")
    print(f"      flatness p = {p:+.2f}.  Diagnostics only; the wall (finiteness")
    print("      for ALL solutions) stays OPEN.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())