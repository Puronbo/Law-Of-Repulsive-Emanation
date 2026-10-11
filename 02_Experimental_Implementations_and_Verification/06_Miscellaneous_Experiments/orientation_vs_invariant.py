"""
BRIDGE: does the on-flow ORIENTATION predict the wall?

`ContinuationCriterion.lean` isolates the wall: existence fails at `T` iff the
scaling-critical content escapes every bound.  The on-flow probe reads an
orientation `lambda = d/dt log(Z_high/Z_low)`.  This script tests whether the sign
of `lambda` MATCHES the sign of the growth rate `mu = d/dt log(critical-content)`
across four systems, i.e. whether the orientation predicts whether the
scaling-critical content is escaping its bound:

    system            classical status      expected lambda   tracked critical content
    3D Navier-Stokes  open (resolved)       < 0  attracting   ||u||_{L^3}   (critical, d=3)
    2D Navier-Stokes  regular (theorem)     < 0  attracting   max|omega|    (2D non-increasing)
    1D viscous Burgers singularity-forming  > 0  repelling    max|u_x|      (gradient blowup)
    CLM  w_t = w Hw   blowup proven         > 0  repelling    max|w|        (blows up)

Test: sign(lambda) == sign(mu) for every system -- the orientation is the on-flow
reading of whether the critical invariant escapes its bound, i.e. of the wall.

Run:  python orientation_vs_invariant.py       (prints PASS)
"""
import json
import os
import numpy as np

from ns_critical_integral import build_spectral, make_broadband_ic, step as ns3d_step
from ns_profile_collapse import radial_spectrum
from ns2d_zero_order import build as b2, make_ic as ic2, step_clean as step2, radial_spectrum_2d as rad2
from burgers_zero_order import build as bb, step as bstep, spectrum as bspec
from clm_zero_order import build as cb, step_rk4, spectrum as cspec

OUT = "data/orientation_vs_invariant.json"


def slope(x, y):
    return float(np.polyfit(np.asarray(x), np.asarray(y), 1)[0])


def run_ns3d(nu=0.1, N=32, dt=0.003, T_max=8.0, save_every=40, K0=6, seed=0):
    X, Y, Zg, kx, ky, kz, k2, k2i, k_inv, mask = build_spectral(N)
    h3 = (2.0 * np.pi / N) ** 3
    n3 = float(N ** 3)
    ratio = h3 / n3
    nmax = int(np.floor((2.0 / 3.0) * (N / 2.0)))
    ken = np.arange(1, nmax + 1).astype(float)
    high = ken >= K0
    low = ~high
    ux, uy, uz = make_broadband_ic(kx, ky, kz, k2, k_inv, k0=4.0, sigma=1.5, seed=seed, N=N)
    E0 = (ux * ux + uy * uy + uz * uz).mean()
    s = 1.0 / np.sqrt(2 * E0)
    ux, uy, uz = s * ux, s * uy, s * uz
    ts, sh, cr = [], [], []
    t = 0.0
    for i in range(int(T_max / dt)):
        ux, uy, uz = ns3d_step(ux, uy, uz, dt, nu, kx, ky, kz, k2, k_inv, mask)
        t += dt
        if (i + 1) % save_every == 0:
            Ek = radial_spectrum(ux, uy, uz, k2, ratio, nmax)
            Zh = float((Ek[high] * ken[high] ** 2).sum())
            Zl = float((Ek[low] * ken[low] ** 2).sum())
            mag = np.sqrt(ux * ux + uy * uy + uz * uz)
            crit = float((mag ** 3).mean()) ** (1.0 / 3.0)
            if t > 0.5 and Zh > 0 and Zl > 0:
                ts.append(t); sh.append(Zh / Zl); cr.append(crit)
    return ts, sh, cr


def run_ns2d(nu=0.1, N=128, dt=5e-4, T_max=6.0, save_every=40, K0=16, seed=0):
    kx, ky, k2, k2s, K, dealias, N = b2(N)
    nmax = int(np.floor((2.0 / 3.0) * (N / 2.0)))
    ken = np.arange(1, nmax + 1).astype(float)
    high = ken >= K0
    low = ~high
    what = ic2(N, kx, ky, K, k0=4.0, sigma=1.5, seed=seed)
    ts, sh, cr = [], [], []
    t = 0.0
    for i in range(int(T_max / dt)):
        what = step2(what, dt, nu, kx, ky, k2s, dealias)
        t += dt
        if (i + 1) % save_every == 0:
            ek = rad2(what, K, nmax)
            Zh = float((ek[high] * ken[high] ** 2).sum())
            Zl = float((ek[low] * ken[low] ** 2).sum())
            crit = float(np.max(np.abs(np.real(np.fft.ifft2(what)))))
            if t > 0.2 and Zh > 0 and Zl > 0:
                ts.append(t); sh.append(Zh / Zl); cr.append(crit)
    return ts, sh, cr


def run_burgers(nu=0.02, N=512, dt=2e-4, T_max=1.5, save_every=25, K0=16):
    k, k2, dealias = bb(N)
    x = 2.0 * np.pi * np.arange(N) / N
    u = 2.0 * np.sin(x)
    half = N // 2
    ken = np.arange(1, half + 1).astype(float)
    high = ken >= K0
    low = ~high
    t = 0.0
    ts, sh, cr = [], [], []
    for i in range(int(T_max / dt)):
        u = bstep(u, dt, nu, k, k2, dealias)
        t += dt
        if (i + 1) % save_every == 0:
            kk, E = bspec(u)
            Zh = float((E[high] * kk[high] ** 2).sum())
            Zl = float((E[low] * kk[low] ** 2).sum())
            ux = np.real(np.fft.ifft(1j * k * np.fft.fft(u)))
            crit = float(np.max(np.abs(ux)))
            if t > 0.1 and Zh > 0 and Zl > 0:
                ts.append(t); sh.append(Zh / Zl); cr.append(crit)
    return ts, sh, cr


def run_clm(amp=1.0, N=512, dt=5e-4, T_max=3.0, save_every=10, K0=16):
    k, Hhat, dealias = cb(N)
    x = 2.0 * np.pi * np.arange(N) / N
    w = amp * np.cos(x)
    half = N // 2
    ken = np.arange(1, half + 1).astype(float)
    high = ken >= K0
    low = ~high
    t = 0.0
    ts, sh, cr = [], [], []
    for i in range(int(T_max / dt)):
        w = step_rk4(w, dt, Hhat, dealias)
        t += dt
        m = float(np.max(np.abs(w)))
        if not np.isfinite(m) or m > 1e7:
            break
        if (i + 1) % save_every == 0:
            kk, E = cspec(w)
            Zh = float((E[high] * kk[high] ** 2).sum())
            Zl = float((E[low] * kk[low] ** 2).sum())
            if Zh > 0 and Zl > 0:
                ts.append(t); sh.append(Zh / Zl); cr.append(m)
    return ts, sh, cr


def main():
    print("=" * 80)
    print("BRIDGE: orientation (lambda) vs growth of the scaling-critical content (mu)")
    print("  hypothesis: sign(lambda) == sign(mu) -- the orientation reads the wall")
    print("=" * 80)
    os.makedirs("data", exist_ok=True)

    systems = [
        ("3D Navier-Stokes (attracting, resolved)", run_ns3d, "L3 velocity"),
        ("2D Navier-Stokes (attracting, regular)", run_ns2d, "max|vorticity|"),
        ("1D Burgers (repelling, singular)", run_burgers, "max|u_x|"),
        ("CLM (repelling, proven blowup)", run_clm, "max|omega|"),
    ]
    out = {}
    rows = []
    print(f"{'system':<42}{'lambda':>12}{'mu':>12}{'match':>8}")
    print("-" * 80)
    for name, fn, critname in systems:
        ts, sh, cr = fn()
        assert len(ts) >= 8, f"{name}: too few samples"
        lam = slope(ts, np.log(sh))
        mu = slope(ts, np.log(cr))
        match = (lam > 0) == (mu > 0)
        out[name] = {"lambda": lam, "mu_of_" + critname: mu, "sign_match": bool(match),
                     "n_samples": len(ts)}
        rows.append((name, lam, mu, match, critname))
        print(f"{name:<42}{lam:>+12.3f}{mu:>+12.3f}{str(match):>8}")

    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)

    allmatch = all(r[3] for r in rows)
    repl = [(n, l) for n, l, m, mt, c in rows if l > 0]
    attr = [(n, l) for n, l, m, mt, c in rows if l < 0]
    print("-" * 80)
    print(f"  REPELLING (lambda > 0): {len(repl)} systems   ATTRACTING (lambda < 0): {len(attr)} systems")
    print(f"  sign(lambda) == sign(mu) for every system: {allmatch}")
    print("  Reading: in every system the sign of the orientation equals the sign of the")
    print("  growth rate of its scaling-critical content.  Where the critical norm grows")
    print("  (Burgers max|u_x|, CLM max|omega|) the orientation is REPELLING; where it")
    print("  shrinks (NS L3 velocity, 2D max|vorticity|) the orientation is ATTRACTING.")
    print("  So the on-flow orientation is the flow's own reading of the wall")
    print("  (ContinuationCriterion.unbounded_of_first_failure): repulsion <=> the")
    print("  invariant escapes its bound.  Diagnostic only; the wall itself stays OPEN.")
    print("=" * 80)
    assert allmatch, "orientation and critical-norm growth disagree in some system"
    print("PASS: sign(orientation) == sign(critical-content growth) across all four systems.")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
