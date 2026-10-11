"""
THIRD SYSTEM: 2D NAVIER-STOKES -- the globally-regular control.

The discriminator (`GreatAttractor.orientationDiscriminator`) says the orientation
separates systems. We have:
  1D viscous Burgers  -> REPELLING (lambda > 0), singularity-forming;
  3D Navier-Stokes    -> ATTRACTING (lambda < 0), resolved range.
2D Navier-Stokes is the decisive CONTROL: the SAME equation family, but a theorem
(Ladyzhenskaya) proves it is globally regular (no finite-time blowup). If the
order/orientation probe reads ATTRACTING here too, then the "attracting" branch
coincides with provable regularity, and repulsion is the signature of a system
that actually forms a singularity -- not of the dimension or the equation.

Solver: 2D pseudo-spectral, vorticity-streamfunction, 2/3 dealiasing, IMEX.
Probe: identical order/orientation reading (order k of high-shell enstrophy,
orientation lambda = d/dt log(Z_high/Z_low)).

Run:  python ns2d_zero_order.py        (prints PASS)
"""
import json
import os
import numpy as np
import time as _clock

OUT = "data/ns2d_zero_order.json"


def build(N):
    kx = np.fft.fftfreq(N, d=1.0 / N).reshape(N, 1)
    ky = np.fft.fftfreq(N, d=1.0 / N).reshape(1, N)
    k2 = kx * kx + ky * ky
    k2s = np.where(k2 == 0, 1.0, k2)
    K = np.sqrt(k2)
    kmax = (2.0 / 3.0) * (N / 2.0)
    dealias = (K <= kmax).astype(float)
    return kx, ky, k2, k2s, K, dealias, N


def make_ic(N, kx, ky, K, k0=4.0, sigma=1.5, seed=0, h3=1.0):
    rng = np.random.default_rng(seed)
    amp = np.exp(-((K - k0) ** 2) / (2.0 * sigma * sigma)) * (K > 0)
    ph = rng.uniform(0, 2 * np.pi, size=(N, N))
    what = amp * (np.cos(ph) + 1j * np.sin(ph))
    what[0, 0] = 0.0
    what = 0.5 * (what + np.conj(np.roll(np.flip(what), (1, 1), axis=(0, 1))))
    return np.fft.fft2(np.real(np.fft.ifft2(what)))


def step_clean(what, dt, nu, kx, ky, k2s, dealias):
    psi_hat = -what / k2s
    u = np.real(np.fft.ifft2(-1j * ky * psi_hat))
    v = np.real(np.fft.ifft2(1j * kx * psi_hat))
    dxw = np.real(np.fft.ifft2(1j * kx * what))
    dyw = np.real(np.fft.ifft2(1j * ky * what))
    nonlinear = u * dxw + v * dyw
    Nhat = np.fft.fft2(nonlinear) * dealias
    return (what - dt * Nhat) / (1.0 + nu * (kx * kx + ky * ky) * dt)


def radial_spectrum_2d(what, K, nmax):
    mag = np.abs(what)
    ek = np.zeros(nmax + 1)
    kb = np.round(K).astype(int)
    m = (kb >= 1) & (kb <= nmax)
    np.add.at(ek, kb[m], (mag[m] ** 2))
    return ek[1:]


def run_case(nu, N=128, dt=5e-4, T_max=6.0, save_every=40, K0=16, k0=4.0, sigma=1.5, seed=0):
    kx, ky, k2, k2s, K, dealias, N = build(N)
    nmax = int(np.floor((2.0 / 3.0) * (N / 2.0)))
    ken = np.arange(1, nmax + 1).astype(float)
    high = ken >= K0
    low = ~high

    what = make_ic(N, kx, ky, K, k0=k0, sigma=sigma, seed=seed)

    ts, zt_h, zh_h, zl_h = [], [], [], []
    t = 0.0
    s = 0
    t0 = _clock.time()
    steps = int(round(T_max / dt))
    for _ in range(steps):
        what = step_clean(what, dt, nu, kx, ky, k2s, dealias)
        t += dt
        s += 1
        if not np.all(np.isfinite(what)):
            return {"diverged": True, "t": t}
        if s % save_every == 0:
            ek = radial_spectrum_2d(what, K, nmax)
            Zh = float((ek[high] * ken[high] ** 2).sum())
            Zl = float((ek[low] * ken[low] ** 2).sum())
            Zt = Zh + Zl
            if t > 0.2 and Zt > 0 and Zh > 0 and Zl > 0:
                ts.append(t); zt_h.append(Zt); zh_h.append(Zh); zl_h.append(Zl)

    ts = np.array(ts); zt = np.array(zt_h); zh = np.array(zh_h); zl = np.array(zl_h)
    order_k = float(np.polyfit(np.log(zt), np.log(zh), 1)[0])
    repel = float(np.polyfit(ts, np.log(zh / zl), 1)[0])
    return {
        "nu": float(nu), "N": int(N), "n_samples": int(len(ts)),
        "order_of_vanishing_k": order_k,
        "repulsion_rate_lambda": repel,
        "share_start": float((zh / zl)[0]), "share_end": float((zh / zl)[-1]),
        "walltime_s": float(_clock.time() - t0),
    }


def main():
    print("=" * 78)
    print("THIRD SYSTEM: 2D NAVIER-STOKES (globally regular control)")
    print("  Expectation: same equation family, proven no blowup -> ATTRACTING")
    print("  (Burgers was the only REPELLING system so far)")
    print("=" * 78)
    os.makedirs("data", exist_ok=True)
    cases = {}
    rows = []
    for N in [96, 128, 160]:
        res = run_case(0.1, N=N)
        if res.get("diverged"):
            print(f"  N={N}: DIVERGED at t={res['t']:.3f}")
            continue
        cases[str(N)] = res
        rows.append(res)
        orient = "REPELLING" if res["repulsion_rate_lambda"] > 0 else "ATTRACTING"
        print(f"  N={N:4d}:  k = {res['order_of_vanishing_k']:+.4f}   "
              f"lambda = {res['repulsion_rate_lambda']:+.4f}  ({orient})   "
              f"share {res['share_start']:.2e} -> {res['share_end']:.2e}   [{res['walltime_s']:.0f}s]")

    with open(OUT, "w") as f:
        json.dump({"cases": cases}, f, indent=2)

    assert len(rows) >= 2, "2D NS sweep incomplete"
    ks = [r["order_of_vanishing_k"] for r in rows]
    ls = [r["repulsion_rate_lambda"] for r in rows]
    dk = abs(ks[-1] - ks[-2]) / max(abs(ks[-1]), 1e-12)
    dl = abs(ls[-1] - ls[-2]) / max(abs(ls[-1]), 1e-12)
    all_attract = all(l < 0 for l in ls)
    print("-" * 78)
    print(f"  convergence:  |dk|/k = {dk:.4f}   |dlambda|/|lambda| = {dl:.4f}")
    print(f"  ATTRACTING at every resolution: {all_attract}")
    print("  Reading: 2D Navier-Stokes -- the same equation family, but a theorem proves")
    print("  it never blows up -- reads ATTRACTING, exactly like resolved 3D NS and unlike")
    print("  Burgers.  So the 'attracting' branch coincides with provable regularity;")
    print("  REPULSION is the signature of a system that actually forms a singularity,")
    print("  not of the dimension or the equation.  The discriminator has meaning.")
    print("=" * 78)
    assert all_attract, "expected the regular 2D system to read attracting"
    print("PASS: 2D Navier-Stokes (globally regular) reads attracting at every N.  "
          "Diagnostic only; wall OPEN.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
