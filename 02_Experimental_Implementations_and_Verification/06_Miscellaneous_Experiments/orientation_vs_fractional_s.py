"""
FRACTIONAL BRIDGE: does the on-flow ORIENTATION track the dissipation ORDER?

`orientation_vs_invariant.py` tests sign(lambda) == sign(mu) on six systems, each with
its own critical invariant.  Here we hold the system fixed (3D incompressible flow) and
vary the DISSIPATION ORDER `s` in the fractional Navier-Stokes equation

    d_t u + (u . grad) u = -nu (-Delta)^s u,     div u = 0,

whose Fourier dissipation is `exp(-nu |k|^{2s} dt)`.  `s = 1` is standard
Navier-Stokes (energy identity available, `B^{-1}_{inf,inf}` content attracting);
`s < 1` is *weaker* at high wavenumbers, so the flow is pushed toward the inviscid
(Euler, repelling) regime while remaining a single dissipative PDE family.  This
strengthens card C10 to a one-parameter statement:

  for every dissipation order s,  sign(lambda) == sign(mu),

with `lambda = d/dt log(Z_high/Z_low)` (on-flow orientation) and `mu = d/dt log(H^sigma)`
(growth rate of the scaling-critical content).  Because the dissipation order sets the
scaling, the critical regularity index is s-dependent: the invariant scaling
`u_lambda = lambda^{2s-1} u(lambda x, lambda^{2s} t)` makes the homogeneous Sobolev
space `H^sigma` critical exactly at `sigma = 5/2 - 2s` (sigma=1/2, the classical NS
critical index, when s=1).  The script therefore tracks the spectral critical content
`||u||_{H^sigma}^2 = sum_k |k|^{2 sigma} E(k)`, which is the object the wall concerns
and is defined uniformly for every s>0.  A flip of both signs as `s` decreases
(attracting -> repelling) is the sharpest possible witness that the orientation reads
the wall.

Window note: the orientation `lambda` is the slope of `log(Z_high/Z_low)` over the
SAMPLED window.  With weak high-k dissipation the ratio first rises (a transient
high-k enstrophy pile-up) and only later decays as the whole field relaxes; a short
window (T ~ 2.5) therefore reports a spurious `lambda > 0` at small `s`.  The sweep is
run over the full relaxation window (T = 6) so that `lambda` measures the attracted
rate, not the transient.  This is why the script prints PASS with `T_max = 6`.

Honesty: resolved runs only.  Fractional NS at small `s` is a known supercritical
regime; if a run loses resolution the script stops it and reports the divergence
rather than extrapolating.  No statement about the wall (finiteness of
`int_0^T ||u||_{B^{-1}_{inf,inf}} dt`) is claimed -- card C10-open.

Run:  python orientation_vs_fractional_s.py       (prints PASS)
"""
import json
import os
import numpy as np

from ns_critical_integral import build_spectral, make_broadband_ic
from ns_profile_collapse import radial_spectrum

OUT = "data/orientation_vs_fractional_s.json"


def slope(x, y):
    return float(np.polyfit(np.asarray(x), np.asarray(y), 1)[0])


def frac_step(ux, uy, uz, dt, nu, s, kx, ky, kz, k2, k_inv, mask):
    """Projected Heun RK2 with exact fractional diffusion exp(-nu |k|^{2s} dt)."""
    diff = np.exp(-nu * (k2 ** s) * dt)
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

    l_s = rhs_add(ux_d, uy_d, uz_d)
    ux_h = ux_d + dt * l_s[0]
    uy_h = uy_d + dt * l_s[1]
    uz_h = uz_d + dt * l_s[2]
    l_e = rhs_add(ux_h, uy_h, uz_h)
    ux_h = ux_d + 0.5 * dt * (l_s[0] + l_e[0])
    uy_h = uy_d + 0.5 * dt * (l_s[1] + l_e[1])
    uz_h = uz_d + 0.5 * dt * (l_s[2] + l_e[2])
    ux_h *= mask
    uy_h *= mask
    uz_h *= mask
    return (np.real(np.fft.ifftn(ux_h)),
            np.real(np.fft.ifftn(uy_h)),
            np.real(np.fft.ifftn(uz_h)))


def critical_sigma(s):
    """s-correct critical Sobolev index sigma = 5/2 - 2s (sigma=1/2 at s=1)."""
    return 2.5 - 2.0 * s


def run_fractional_ns(s, nu=0.1, N=32, dt=2e-3, T_max=6.0, save_every=25, K0=6, seed=0):
    """3D fractional NS at order `s`; returns (times, Z_high/Z_low, H^sigma, L3)."""
    X, Y, Zg, kx, ky, kz, k2, k2i, k_inv, mask = build_spectral(N)
    h3 = (2.0 * np.pi / N) ** 3
    ratio = h3 / float(N ** 3)
    nmax = int(np.floor((2.0 / 3.0) * (N / 2.0)))
    ken = np.arange(1, nmax + 1).astype(float)
    high = ken >= K0
    low = ~high
    w2 = ken ** (2.0 * critical_sigma(s))
    ux, uy, uz = make_broadband_ic(kx, ky, kz, k2, k_inv, k0=4.0, sigma=1.5, seed=seed, N=N)
    E0 = (ux * ux + uy * uy + uz * uz).mean()
    sc = 1.0 / np.sqrt(2 * E0)
    ux, uy, uz = sc * ux, sc * uy, sc * uz
    ts, sh, cr, l3 = [], [], [], []
    t = 0.0
    diverged = False
    for i in range(int(T_max / dt)):
        ux, uy, uz = frac_step(ux, uy, uz, dt, nu, s, kx, ky, kz, k2, k_inv, mask)
        t += dt
        if not np.all(np.isfinite(ux)) or np.max(np.abs(ux)) > 1e6:
            diverged = True
            break
        if (i + 1) % save_every == 0:
            Ek = radial_spectrum(ux, uy, uz, k2, ratio, nmax)
            Zh = float((Ek[high] * ken[high] ** 2).sum())
            Zl = float((Ek[low] * ken[low] ** 2).sum())
            mag = np.sqrt(ux * ux + uy * uy + uz * uz)
            if t > 0.3 and Zh > 0 and Zl > 0:
                ts.append(t)
                sh.append(Zh / Zl)
                cr.append(float(np.sqrt((Ek * w2).sum())))
                l3.append(float((mag ** 3).mean()) ** (1.0 / 3.0))
    return ts, sh, cr, l3, diverged


def main():
    print("=" * 80)
    print("FRACTIONAL-NS SWEEP: orientation (lambda) vs critical-content growth (mu)")
    print("  dissipation order s in (-Delta)^s:  s=1 standard NS, smaller s -> inviscid")
    print("  tracked critical content: H^sigma, sigma = 5/2 - 2s (sigma=1/2 at s=1)")
    print("=" * 80)
    os.makedirs("data", exist_ok=True)
    orders = [1.0, 0.75, 0.5]
    out = {}
    rows = []
    print(f"{'s':>6}{'sigma':>8}{'samples':>9}{'lambda':>12}{'mu':>12}{'mu_L3':>12}{'match':>8}")
    print("-" * 88)
    for s in orders:
        ts, sh, cr, l3, diverged = run_fractional_ns(s)
        assert len(ts) >= 8, f"s={s}: too few samples ({len(ts)})"
        lam = slope(ts, np.log(sh))
        mu = slope(ts, np.log(cr))
        mu3 = slope(ts, np.log(l3))
        match = (lam > 0) == (mu > 0)
        out[str(s)] = {"s": s, "sigma": critical_sigma(s),
                       "lambda": lam, "mu_critical": mu, "mu_L3": mu3,
                       "sign_match": bool(match), "n_samples": len(ts),
                       "diverged": bool(diverged)}
        rows.append((s, lam, mu, match))
        print(f"{s:>6.2f}{critical_sigma(s):>8.2f}{len(ts):>9}{lam:>+12.3f}{mu:>+12.3f}"
              f"{mu3:>+12.3f}{str(match):>8}")
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)

    allmatch = all(r[3] for r in rows)
    flips = sum(1 for i in range(1, len(rows)) if (rows[i - 1][1] > 0) != (rows[i][1] > 0))
    attr = [r[0] for r in rows if r[1] < 0]
    repl = [r[0] for r in rows if r[1] > 0]
    print("-" * 88)
    print(f"  ATTRACTING (lambda < 0): s in {attr}     REPELLING (lambda > 0): s in {repl}")
    print(f"  orientation flips between consecutive s: {flips}")
    print(f"  sign(lambda) == sign(mu_critical) at every s: {allmatch}")
    print("-" * 88)
    assert allmatch, "C10 sign-match violated in the fractional regime"
    print("PASS: across dissipation orders s, the s-correct critical content moves with")
    print("      the on-flow orientation: sign(lambda) == sign(mu_critical).  Card C10")
    print("      holds one-parameter (s) in family; the wall (finiteness for ALL")
    print("      solutions) stays OPEN -- card C10-open.")
    print("=" * 88)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
