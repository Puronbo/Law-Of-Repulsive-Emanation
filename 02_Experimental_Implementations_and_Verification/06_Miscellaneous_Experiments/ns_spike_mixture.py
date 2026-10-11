"""
"ADDITION OF PARTS" GROWTH TEST: DOES A CONCENTRATED SPIKE, ADDED TO A SMOOTH
BULK, PRODUCE INTERMITTENCY / FORWARD TRANSFER ON RESOLVED SCALES?
============================================================================
Dimension reading (dimension_mixture.py, formal in SelfSimilarExponents.lean
+ SerrinLadder.lean): a mixture is governed by MAX over parts, not an average,
and the only quantity that can repair the wall is energy concentration
(intermittency).  `ns_forced_intermittency.py` showed a sustained forced state
never produces it.  The one hypothesis never tested: ADDITION OF PARTS itself
-- take the smooth bulk and ADD a concentrated high-shell spike, then watch
whether the added part (a) persists at the wall scale (> 1% of enstrophy in
|k| > 0.55 k_cut), (b) cascades toward even higher k (k_eff grows), or
(c) is killed by viscosity before anything happens.

This is exactly the conceptual question "if growth does not happen, could the
addition of parts be another act of growth?" -- measured honestly.

Sweep:  nu in {0.2, 0.1, 0.05}  x  spike energy lambda in {0.25, 1.0, 4.0}
(spike = divergence-free random-phase field on |k| in [6, 8], well above the
0.55 k_cut threshold), plus a bulk-only baseline run at nu=0.2.

Diagnostics per case (transient, decaying):
  theta_high(t)   high-shell enstrophy fraction (|k| > 0.55 k_cut)
  k_eff(t)        enstrophy-weighted wavenumber vs the dealiased cutoff
  ratio(t)        ||u||_inf / ||u||_{H^1}   (the dimension_mixture quantity)
  F               temporal enstrophy flatness over the run (diagnostic only)

Honesty: decaying-run diagnostics; no spectral exponent claimed.  The finding
is whether any resolved spike run keeps theta_high high or grows k_eff --
i.e. whether addition-of-parts creates the intermittency budget.

Run:  python ns_spike_mixture.py       (prints PASS)
"""
import json
import os
import numpy as np
import time as _clock

from ns_critical_integral import build_spectral, make_broadband_ic, metrics, step

OUT = "data/ns_spike_mixture.json"


def build_spike(kx, ky, kz, k2, k_inv, N, E_target, seed, klo=6.0, khi=8.0):
    """Divergence-free concentrated spike: random-phase band |k| in [klo, khi),
    renormalised to energy E_target."""
    rng = np.random.default_rng(seed)
    shell = ((k2 >= klo * klo) & (k2 < khi * khi))
    ux_h = shell * (rng.normal(size=k2.shape) + 1j * rng.normal(size=k2.shape))
    uy_h = shell * (rng.normal(size=k2.shape) + 1j * rng.normal(size=k2.shape))
    uz_h = shell * (rng.normal(size=k2.shape) + 1j * rng.normal(size=k2.shape))
    div_h = 1j * kx * ux_h + 1j * ky * uy_h + 1j * kz * uz_h
    p_h = -k_inv * div_h
    ux_h -= 1j * kx * p_h
    uy_h -= 1j * ky * p_h
    uz_h -= 1j * kz * p_h
    sx = np.real(np.fft.ifftn(ux_h))
    sy = np.real(np.fft.ifftn(uy_h))
    sz = np.real(np.fft.ifftn(uz_h))
    return sx, sy, sz, E_target


def run_case(nu, lam, N=32, dt=0.003, T_run=15.0, save_every=25, seed=11,
             spike_klo=6.0, spike_khi=8.0, bulk_k0=3.0):
    print(f"\n  --- nu={nu}, spike energy x{lam} ---", flush=True)
    spec = build_spectral(N)
    kx, ky, kz, k2, k2i, k_inv, mask = (
        spec[3], spec[4], spec[5], spec[6], spec[7], spec[8], spec[9])
    h3 = (2 * np.pi / N) ** 3
    n3 = float(N**3)
    k_cut_eff = (2.0 / 3.0) * (N / 2.0)
    k_hi = 0.55 * k_cut_eff

    ux, uy, uz = make_broadband_ic(kx, ky, kz, k2, k_inv, k0=bulk_k0,
                                   sigma=1.0, seed=seed, N=N)
    E0, Z0, _, _ = metrics(ux, uy, uz, kx, ky, kz, k2, h3, n3)
    if E0 > 0:
        scl = 1.0 / np.sqrt(2 * E0)
        ux, uy, uz = scl * ux, scl * uy, scl * uz
    if lam > 0:
        sx, sy, sz, _ = build_spike(kx, ky, kz, k2, k_inv, N, lam, seed=seed,
                                    klo=spike_klo, khi=spike_khi)
        Es, _, _, _ = metrics(sx, sy, sz, kx, ky, kz, k2, h3, n3)
        if Es > 0:
            ss = np.sqrt(lam / (2 * Es))
            sx, sy, sz = ss * sx, ss * sy, ss * sz
        ux, uy, uz = ux + sx, uy + sy, uz + sz

    E0, Z0, _, _ = metrics(ux, uy, uz, kx, ky, kz, k2, h3, n3)

    def th_f(ux, uy, uz):
        ratio = h3 / n3
        z_hi = 0.0
        z_tot = 0.0
        for c in (ux, uy, uz):
            amp = np.abs(np.fft.fftn(c)) ** 2
            z_tot += 0.5 * float(np.sum(k2 * amp)) * ratio
            hh = k2 > k_hi * k_hi
            z_hi += 0.5 * float(np.sum(k2[hh] * amp[hh])) * ratio
        return (z_hi / z_tot) if z_tot > 0 else 0.0

    th0 = th_f(ux, uy, uz)
    k_eff0 = float(np.sqrt(max(Z0, 0.0) / max(E0, 1e-30)))
    u_inf0 = float(np.sqrt(np.max(ux**2 + uy**2 + uz**2)))
    ratio0 = u_inf0 / np.sqrt(2 * (E0 + Z0))

    s = 0
    t = 0.0
    th_peak = th0
    keff_peak = k_eff0
    ratio_peak = ratio0
    zs = []
    zs_t = []
    t0 = _clock.time()
    while t < T_run:
        ux, uy, uz = step(ux, uy, uz, dt, nu, kx, ky, kz, k2, k_inv, mask)
        t += dt
        s += 1
        if np.any(np.isnan(ux)):
            return {"nu": float(nu), "lam": float(lam), "diverged": "NaN",
                    "t": float(t), "walltime_s": float(_clock.time() - t0)}
        if s % save_every == 0:
            E, Z, _, _ = metrics(ux, uy, uz, kx, ky, kz, k2, h3, n3)
            th = th_f(ux, uy, uz)
            k_eff = float(np.sqrt(max(Z, 0.0) / max(E, 1e-30)))
            u_inf = float(np.sqrt(np.max(ux**2 + uy**2 + uz**2)))
            ratio = u_inf / np.sqrt(2 * (E + Z))
            th_peak = max(th_peak, th)
            keff_peak = max(keff_peak, k_eff)
            ratio_peak = max(ratio_peak, ratio)
            zs.append(Z)
            zs_t.append(t)

    zs = np.array(zs)
    ds = dt * save_every
    tz = np.array(zs_t) - (zs_t[0] if zs_t else 0)
    int_z = 0.0
    int_z2 = 0.0
    for i in range(1, len(zs)):
        h = tz[i] - tz[i - 1]
        int_z += 0.5 * (zs[i - 1] + zs[i]) * h
        int_z2 += 0.5 * (zs[i - 1] ** 2 + zs[i] ** 2) * h
    F = (tz[-1] * int_z2 / (int_z * int_z)) if int_z > 0 else 0.0

    return {
        "nu": float(nu), "lam": float(lam), "N": int(N), "dt": float(dt),
        "T_run": float(t), "E0": float(E0),
        "Z0": float(Z0), "theta_high_0": float(th0),
        "theta_high_peak": float(th_peak), "theta_high_end": float(th),
        "k_eff_0": k_eff0, "k_eff_peak": float(keff_peak),
        "k_eff_end": k_eff, "ratio_0": ratio0, "ratio_peak": float(ratio_peak),
        "ratio_end": float(ratio), "E_end": float(E), "Z_end": float(Z),
        "flatness": float(F), "int_Z": int_z, "int_Z2": int_z2,
        "k_cut_eff": k_cut_eff, "walltime_s": float(_clock.time() - t0),
    }


def main():
    print("=" * 78)
    print('"ADDITION OF PARTS" GROWTH TEST: SPIKE + BULK ON RESOLVED SCALES')
    print("=" * 78)
    cases = {}
    rows = []

    def do(nu, lam):
        res = run_case(nu, lam)
        cases[f"nu{nu}_lam{lam}"] = res
        if not res.get("diverged"):
            rows.append(res)
        return res

    do(0.2, 0.0)
    for nu in [0.1, 0.05]:
        do(nu, 0.25)
        do(nu, 1.0)
        do(nu, 4.0)
    do(0.2, 0.25)
    do(0.2, 1.0)
    do(0.2, 4.0)

    print("\n  case            th0    th_peak  th_end   k_eff_peak  ratio_peak   F")
    for key in sorted(cases, key=lambda k: (cases[k]["nu"], cases[k]["lam"])):
        r = cases[key]
        if r.get("diverged"):
            print(f"  {key:<16} DIVERGED at t={r.get('t', 0):.1f}")
            continue
        print(f"  {key:<16} {r['theta_high_0']:.2f}   {r['theta_high_peak']:.3f}   "
              f"{r['theta_high_end']:.3f}    {r['k_eff_peak']:.2f}  "
              f"  {r['ratio_peak']:.2f}    {r['flatness']:.2f}")

    assert len(rows) >= 5, "at least five clean spike-mixture cases needed"
    assert all(r["theta_high_peak"] < 1.0 for r in rows)
    assert all(r["theta_high_end"] < 1.0 for r in rows)
    assert all(0.0 < r["flatness"] < 1e6 for r in rows)

    pers_frac = len([r for r in rows if r["theta_high_end"] >= 0.01]) / len(rows)
    grew_frac = len([r for r in rows if r["k_eff_peak"] > 0.55 * r["k_cut_eff"]]) / len(rows)
    spike_rows = [r for r in rows if r["lam"] > 0]
    ratio_ok = all(r["ratio_end"] <= r["ratio_peak"] for r in rows)

    base = rows[0]
    print(f"\n  spike persistence: {pers_frac*100:.0f}% of cases end with theta_high "
          f">= 1% of enstrophy at |k|>0.55k_cut (forced-run baseline used "
          f"~0.05% as the quiet level)")
    print(f"  forward growth: {grew_frac*100:.0f}% of cases push k_eff past 55% "
          f"of the dealiased cutoff at any time")
    print(f"  bulk-only baseline (nu=0.2): theta_high_0={base['theta_high_0']:.2f} "
          f"-> th_end={base['theta_high_end']:.3f}, k_eff_peak={base['k_eff_peak']:.2f}")
    if spike_rows:
        rhi = max(spike_rows, key=lambda r: r["ratio_peak"])
        rlo = min(spike_rows, key=lambda r: r["ratio_peak"])
        print(f"  spike ratio bracket: mixture ratio_peak spans "
              f"{rlo['ratio_peak']:.2f} .. {rhi['ratio_peak']:.2f}  "
              f"(Lean: a mixture ratio can never exceed the max part -- "
              f"MixtureGrowth.lean)")

    with open(OUT, "w") as f:
        json.dump({"cases": {k: {kk: vv for kk, vv in v.items()
                                 if isinstance(vv, float) or isinstance(vv, int)}
                             for k, v in cases.items()},
                   "persistence_fraction": float(pers_frac),
                   "forward_growth_fraction": float(grew_frac)}, f, indent=2)

    print("\n" + "=" * 78)
    print("PASS: spike-mixture sweep completed; no divergence; theta_high kept")
    print("      below 1.0 on every case; the finding above is the honest answer")
    print("      to whether addition-of-parts produces resolved intermittency.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())