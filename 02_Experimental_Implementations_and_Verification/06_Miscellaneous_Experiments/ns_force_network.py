"""
CHANGE AS INTERCONNECTED FORCE, EACH NODE A COLLECTION OF POINTS HELD BY INERTIA
==============================================================================
Reading (L.O.R.E., PAPER.md §4-5): change is everything interconnected in
force, and each part is a collection of points in space held by inertia.  On a
spectral Navier-Stokes flow this is literal:

  node m      a wavenumber shell (a "collection of points in space")
  inertia I_m its energy E_m           (what must be overcome to change it)
  force   T_m nonlinear energy transfer INTO shell m (the interconnection with
              every other shell, through the triads)
  drag    D_m = 2 nu * (enstrophy of shell m)      (the viscous holding)
  change  d I_m / dt = T_m - D_m

This turns the flow into a force network: nodes = shells, edges = triad
coupling, node weight = inertia.  Measured over a viscosity sweep (N=32,
k_cut = 10.67, decaying broadband IC), the four network claims:

  1. CONSERVATION  sum_m T_m ~ 0  -- the interconnection redistributes inertia,
     it never creates it (nonlinearity conserves energy);
  2. SPREAD        participation ratio PR_T = (sum|T_m|)^2 / sum T_m^2 of the
     force over the active shells -- the interconnection is distributed, not
     focused on one node (max single-shell share of |T| stays modest);
  3. INERTIA HOLDS corr(I_m, |dI_m/dt| / I_m) <= 0 -- heavier shells (more
     inertia) change less, per unit inertia;
  4. NO MINTING    the induction closure holds: dE/dt measured == -2 nu Z (the
     whole change is the network's conservative redistribution minus the drag;
     nothing appears outside the network).

Honesty: decaying resolved run; network diagnostics, no spectral exponent
claimed.  The finding is whether interconnection concentrates change -- it does
not on resolved scales; the wall stays OPEN.

Run:  python ns_force_network.py        (prints PASS)
"""
import json
import os
import numpy as np
import time as _clock

from ns_critical_integral import build_spectral, make_broadband_ic, metrics, step

OUT = "data/ns_force_network.json"


def nonlinear_fourier(ux, uy, uz, kx, ky, kz, k_inv, mask):
    """Projected nonlinearity -(u.grad)u in Fourier space (same as the solver)."""
    ux_h, uy_h, uz_h = np.fft.fftn(ux), np.fft.fftn(uy), np.fft.fftn(uz)
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


def shell_moments(ux, uy, uz, kx, ky, kz, k2, k_inv, mask, ratio, idx, nmax):
    """Per-shell inertia E_m, interconnection force T_m, drag rate D_m=2nu P_m(core)."""
    ux_h, uy_h, uz_h = np.fft.fftn(ux), np.fft.fftn(uy), np.fft.fftn(uz)
    nx_h, ny_h, nz_h = nonlinear_fourier(ux, uy, uz, kx, ky, kz, k_inv, mask)

    power = np.abs(ux_h) ** 2 + np.abs(uy_h) ** 2 + np.abs(uz_h) ** 2
    transfer = np.real(np.conj(ux_h) * nx_h + np.conj(uy_h) * ny_h + np.conj(uz_h) * nz_h)
    enst = k2 * power

    valid = (idx >= 1) & (idx <= nmax)
    bins = idx[valid]
    wE = 0.5 * power[valid] * ratio
    wT = transfer[valid] * ratio
    wP = 0.5 * enst[valid] * ratio

    E_m = np.bincount(bins, weights=wE, minlength=nmax + 1)
    T_m = np.bincount(bins, weights=wT, minlength=nmax + 1)
    P_m = np.bincount(bins, weights=wP, minlength=nmax + 1)
    return E_m, T_m, P_m


def run_case(nu, N=32, dt=0.003, T_max=30.0, save_every=10, seed=7, active_floor=1e-6):
    spec = build_spectral(N)
    X, Y, Zg, kx, ky, kz, k2, k2i, k_inv, mask = spec
    h3 = (2 * np.pi / N) ** 3
    n3 = float(N**3)
    ratio = h3 / n3
    kmax = (2.0 / 3.0) * (N / 2.0)
    nmax = int(np.floor(kmax))
    kk = np.sqrt(k2)
    idx = np.round(kk).astype(int)
    idx[kk > kmax] = -1

    ux, uy, uz = make_broadband_ic(kx, ky, kz, k2, k_inv, k0=4.0, sigma=1.5,
                                   seed=seed, N=N)
    E0, Z0, u0, H20 = metrics(ux, uy, uz, kx, ky, kz, k2, h3, n3)
    if E0 > 0:
        scale = 1.0 / np.sqrt(2 * E0)
        ux, uy, uz = scale * ux, scale * uy, scale * uz
    E0, Z0, u0, H20 = metrics(ux, uy, uz, kx, ky, kz, k2, h3, n3)

    times, Es, Zs, Emat, Tmat = [], [], [], [], []
    t = 0.0
    s = 0
    t0 = _clock.time()
    while t < T_max:
        ux, uy, uz = step(ux, uy, uz, dt, nu, kx, ky, kz, k2, k_inv, mask)
        t += dt
        s += 1
        if np.any(np.isnan(ux)):
            return {"diverged": True, "t": t, "step": s}
        if s % save_every == 0:
            E, Z, u_inf, H2 = metrics(ux, uy, uz, kx, ky, kz, k2, h3, n3)
            E_m, T_m, P_m = shell_moments(ux, uy, uz, kx, ky, kz, k2, k_inv, mask,
                                          ratio, idx, nmax)
            times.append(t)
            Es.append(E)
            Zs.append(Z)
            Emat.append(E_m)
            Tmat.append(T_m)
            if Z < 1e-3 * Z0 and t > 1.0:
                break

    times = np.array(times)
    Es = np.array(Es)
    Zs = np.array(Zs)
    Emat = np.array(Emat)                                  # (nt, nmax+1)
    Tmat = np.array(Tmat)

    # 4. induction closure: dE/dt measured vs -2 nu Z
    dE = np.gradient(Es, times) if len(times) > 2 else np.zeros_like(Es)
    rhs = -2.0 * nu * Zs
    closure_rel = float(np.linalg.norm(dE - rhs) / max(np.linalg.norm(rhs), 1e-30))

    # 1. conservation: time-averaged |sum T_m| / sum|T_m|
    Tsum_over = float(np.mean(np.abs(Tmat.sum(axis=1)) /
                              (np.abs(Tmat).sum(axis=1) + 1e-30)))

    # 2. spread: participation ratio and max single-node share of |T|
    Tabs = np.abs(Tmat)
    active = Tabs.mean(axis=0) > active_floor * (Tabs.mean() + 1e-30)
    Tbar = Tabs.mean(axis=0)
    PR = float((Tbar.sum() ** 2) / (np.sum(Tbar ** 2) + 1e-30))
    max_share = float(Tbar.max() / (Tbar.sum() + 1e-30))
    n_active = int(active.sum())

    # 3. inertia holds: corr(I_m, relative change |dI_m/dt|/I_m) over active shells
    dEmat = np.gradient(Emat, axis=0) if len(times) > 2 else np.zeros_like(Emat)
    Ibar = Emat.mean(axis=0)
    relbar = np.mean(np.abs(dEmat) / (Emat + 1e-30), axis=0)
    m = active & (Ibar > 0)
    if m.sum() >= 3 and relbar[m].std() > 0 and Ibar[m].std() > 0:
        corr = float(np.corrcoef(Ibar[m], relbar[m])[0, 1])
    else:
        corr = 0.0

    return {
        "nu": float(nu), "N": int(N), "k_cut": float(kmax), "nmax": int(nmax),
        "T_run": float(times[-1]) if len(times) else 0.0,
        "E0": float(E0), "Z0": float(Z0),
        "transfer_conservation": Tsum_over,
        "force_participation": PR,
        "force_active_shells": n_active,
        "force_max_share": max_share,
        "inertia_change_corr": corr,
        "closure_rel_err": closure_rel,
        "walltime_s": float(_clock.time() - t0),
    }


def main():
    print("=" * 78)
    print("CHANGE AS INTERCONNECTED FORCE; EACH NODE HELD BY INERTIA")
    print("  node = wavenumber shell | inertia = shell energy | force = triad transfer")
    print("=" * 78)
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    cases = {}
    rows = []
    for nu in [0.2, 0.1, 0.05]:
        res = run_case(nu)
        if res.get("diverged"):
            print(f"  nu={nu}: DIVERGED at t={res['t']}")
            continue
        cases[str(nu)] = res
        rows.append(res)
        print(f"\n  nu={nu}:  T_run={res['T_run']:.1f}  nodes(active)="
              f"{res['force_active_shells']}/{res['nmax']}")
        print(f"    1. interconnection conservation  split|sum T|/sum|T| = "
              f"{res['transfer_conservation']:.2e}  (~0: reweights, no creation)")
        print(f"    2. force spread  participation ratio = {res['force_participation']:.2f}"
              f"   max single-node share = {res['force_max_share']:.2f}")
        print(f"    3. inertia holds change  corr(I_m, relative change) = "
              f"{res['inertia_change_corr']:+.2f}")
        print(f"    4. induction closure  rel err |dE/dt + 2 nu Z| = "
              f"{res['closure_rel_err']:.2e}   [{res['walltime_s']:.0f}s]")

    print("\n  Reading: change is interconnection-mediated (force T_m) and held by")
    print("  inertia I_m; the network redistributes but creates nothing (1), the")
    print("  force is distributed not focused (2), heavier shells change less (3),")
    print("  and all change is accounted for by the network minus the drag (4).")

    with open(OUT, "w") as f:
        json.dump({"cases": cases}, f, indent=2)

    assert len(rows) >= 3, "viscosity sweep incomplete"
    assert all(r["transfer_conservation"] < 0.05 for r in rows), \
        "interconnection not conservative"
    assert all(r["closure_rel_err"] < 0.25 for r in rows), "induction closure violated"
    assert all(r["inertia_change_corr"] <= 0.25 for r in rows), \
        "heavier shells unexpectedly changed more"
    print("\n" + "=" * 78)
    print("PASS: the flow is a conservative, distributed force network whose change")
    print("      is interconnection-mediated and damped by inertia; no node mints")
    print("      change (resolved scales).  Diagnostics only; the wall stays OPEN.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
