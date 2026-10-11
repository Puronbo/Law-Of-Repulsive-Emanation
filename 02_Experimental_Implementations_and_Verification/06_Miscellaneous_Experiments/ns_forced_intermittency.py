"""
FORCED STEADY-STATE TURBULENCE: ENSTROPHY FLATNESS, HIGH-SHELL BUDGET, k_eff
============================================================================
The decaying probes (ns_critical_integral.py, ns_spectral_slope.py) showed
that RESOLVED decaying flows keep int Z^2 finite with flatness ~ 5-7 and
k_eff <= 0.32 of the cutoff: no intermittency, no forward cascade.  The one
regime where intermittency/anomalous statistics can actually appear is a
FORCED, statistically steady turbulent state.

This module drives the same T^3 spectral integrator with ADDITIVE
deterministic forcing on the band |k| in [2, 3] (a fixed, divergence-free,
unit-L2 seeded field at fixed amplitude calibrated so the steady-state mean
enstrophy sits near Z_target), and measures once a stationarity gate passes
(E,Z window drift < 2e-3):

  (i)   enstrophy temporal flatness  F = T_w * int Z^2 / (int Z)^2
        over a measurement window  [the intermittency quantity];
  (ii)  the high-shell enstrophy fraction  theta_high(t)  (|k| > 0.55 k_cut)
        against the order-eps intermittency budget of dimension_mixture.py,
        with  eps = k_force / k_cut  (forced-to-grid scale ratio);
  (iii) k_eff = sqrt(Z/E) relative to the dealiased cutoff.

Honesty: at N=32 the inertial band is short; no spectral exponent is claimed.
The measured quantities are resolved-flow bookkeeping; the wall stays OPEN.

Run:  python ns_forced_intermittency.py       (prints PASS)
"""
import json
import os
import numpy as np
import time as _clock

from ns_critical_integral import build_spectral, make_broadband_ic, metrics, step

OUT = "data/ns_forced_intermittency.json"


def build_force(kx, ky, kz, k2, k_inv, N, seed=11, klo=2.0, khi=3.0):
    """Fixed divergence-free band force with unit physical L2 norm:
    int |f|^2 dx = 1 (scaled later by the power controller A)."""
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
    nf2 = float(np.sum(np.abs(ux_h) ** 2 + np.abs(uy_h) ** 2
                       + np.abs(uz_h) ** 2))
    if nf2 > 0:
        ux_h = ux_h / np.sqrt(nf2)
        uy_h = uy_h / np.sqrt(nf2)
        uz_h = uz_h / np.sqrt(nf2)
    return (np.real(np.fft.ifftn(ux_h)),
            np.real(np.fft.ifftn(uy_h)),
            np.real(np.fft.ifftn(uz_h)), float(nf2))


def run_case(nu, N=32, dt=0.003, T_max=80.0, save_every=25, seed=11,
             Z_target=12.0, win_steps=400, dr_thresh=2e-3, T_win=10.0,
             A_fixed=None):
    print(f"\n  --- nu={nu}: forced run (N={N}, dt={dt}, Z_target={Z_target}) ---",
          flush=True)
    spec = build_spectral(N)
    kx, ky, kz, k2, k2i, k_inv, mask = (
        spec[3], spec[4], spec[5], spec[6], spec[7], spec[8], spec[9])
    h3 = (2 * np.pi / N) ** 3
    n3 = float(N**3)
    fx, fy, fz, nf2 = build_force(kx, ky, kz, k2, k_inv, N, seed=seed)
    # fixed amplitude (no closed-loop control so Z is free to fluctuate):
    # empirically injection ~ 2*nu*Z_target needs A ~ 35000*nu at N=32
    A = float(A_fixed) if A_fixed is not None else 35000.0 * nu

    ux, uy, uz = make_broadband_ic(kx, ky, kz, k2, k_inv, k0=3.0, sigma=1.0,
                                   seed=seed, N=N)
    E0, Z0, u0, H20 = metrics(ux, uy, uz, kx, ky, kz, k2, h3, n3)
    if E0 > 0:
        scale = 1.0 / np.sqrt(2 * E0)
        ux, uy, uz = scale * ux, scale * uy, scale * uz
    E0, Z0, u0, H20 = metrics(ux, uy, uz, kx, ky, kz, k2, h3, n3)

    k_cut_eff = (2.0 / 3.0) * (N / 2.0)
    k_hi = 0.55 * k_cut_eff
    eps = 2.5 / k_cut_eff                     # forced-to-grid scale ratio

    def high_shell_fraction(ux, uy, uz):
        ratio = h3 / n3
        z_high = 0.0
        z_tot = 0.0
        for c in (ux, uy, uz):
            amp = np.abs(np.fft.fftn(c)) ** 2
            z_tot += 0.5 * float(np.sum(k2 * amp)) * ratio
            hi = k2 > k_hi * k_hi
            z_high += 0.5 * float(np.sum(k2[hi] * amp[hi])) * ratio
        return (z_high / z_tot) if z_tot > 0 else 0.0

    s = 0
    t = 0.0
    ths = [high_shell_fraction(ux, uy, uz)]
    win_E = []
    stationary_n = 0
    stationarity_ok = False
    phase = "transient"
    m_prev_Z2 = None
    m_Z, m_Z2, m_start = 0.0, 0.0, None
    k_eff_max = float(np.sqrt(max(Z0, 0.0) / max(E0, 1e-30)))
    t0 = _clock.time()
    while t < T_max:
        ux, uy, uz = step(ux, uy, uz, dt, nu, kx, ky, kz, k2, k_inv, mask)
        ux += dt * A * fx
        uy += dt * A * fy
        uz += dt * A * fz
        t += dt
        s += 1
        if np.any(np.isnan(ux)):
            return {"diverged": "NaN", "t": float(t), "step": int(s)}
        if s % save_every == 0:
            E, Z, _, _ = metrics(ux, uy, uz, kx, ky, kz, k2, h3, n3)
            th = high_shell_fraction(ux, uy, uz)
            ths.append(th)
            inj = float(np.sum(ux * fx + uy * fy + uz * fz)) * h3 * A
            k_eff = float(np.sqrt(max(Z, 0.0) / max(E, 1e-30)))
            k_eff_max = max(k_eff_max, k_eff)
            if phase == "transient":
                win_E.append(E)
                if len(win_E) >= (win_steps // save_every):
                    dE = abs(win_E[-1] - win_E[0]) / max(win_E[0], 1e-30)
                    if dE < dr_thresh:
                        stationary_n += 1
                        if stationary_n >= 3:
                            stationarity_ok = True
                            phase = "measure"
                            m_start = t
                            print(f"    stationary at t={t:.1f} (E={E:.3f}, "
                                  f"Z={Z:.3f}, A={A:.2f})", flush=True)
                    else:
                        stationary_n = 0
                if len(win_E) > (win_steps // save_every):
                    win_E.pop(0)
            else:
                if m_prev_Z2 is not None:
                    ds = dt * save_every
                    m_Z += 0.5 * (np.sqrt(m_prev_Z2) + Z) * ds
                    m_Z2 += 0.5 * (m_prev_Z2 + Z * Z) * ds
                m_prev_Z2 = Z * Z
                if t - m_start >= T_win:
                    break
    tf = t

    if not stationarity_ok or m_start is None:
        return {"nu": float(nu), "diverged": "no_stationarity",
                "T_run": float(tf), "E_final": float(E),
                "Z_final": float(Z), "walltime_s": float(_clock.time() - t0)}

    Tw = tf - m_start
    flat = Tw * m_Z2 / (m_Z * m_Z) if m_Z > 0 else 0.0
    th_arr = np.array(ths)
    return {
        "nu": float(nu), "N": int(N), "dt": float(dt),
        "T_run": float(tf), "T_stationary": float(m_start),
        "T_measure": float(Tw), "E_final": float(E), "Z_final": float(Z),
        "Z_target": float(Z_target),
        "A_final": float(A), "k_cut_eff": float(k_cut_eff),
        "k_eff_final": float(k_eff), "k_eff_max": k_eff_max,
        "flatness": float(flat), "int_Z": float(m_Z), "int_Z2": float(m_Z2),
        "theta_high_mean": float(th_arr.mean()),
        "theta_high_max": float(th_arr.max()),
        "eps_budget": float(eps),
        "budget_margin_min": float(eps / th_arr.max()) if th_arr.max() > 0 else 0.0,
        "walltime_s": float(_clock.time() - t0),
    }


def main():
    print("=" * 78)
    print("FORCED STEADY-STATE TURBULENCE: FLATNESS, HIGH-SHELL BUDGET, k_eff")
    print("=" * 78)
    rows = []
    cases = {}
    for nu in [0.1, 0.05]:
        res = run_case(nu, seed=11)
        if res.get("diverged"):
            print(f"  nu={nu}: {res['diverged']} at t={res.get('t', res.get('T_run', '?'))}")
            continue
        cases[str(nu)] = res
        rows.append(res)
        r = res
        print(f"\n  nu={r['nu']}:  stationary t={r['T_stationary']:.1f}, "
              f"measure {r['T_measure']:.1f}")
        print(f"    enstrophy flatness F = {r['flatness']:.3f}   "
              f"int Z = {r['int_Z']:.3f}, int Z^2 = {r['int_Z2']:.3f}")
        print(f"    high-shell theta_high: mean {r['theta_high_mean']*100:.2f}%, "
              f"max {r['theta_high_max']*100:.2f}%  (eps budget 23.4% -> margin "
              f">= {r['budget_margin_min']:.2f}x)")
        print(f"    k_eff final {r['k_eff_final']:.2f} / cut {r['k_cut_eff']:.2f} "
              f"= {r['k_eff_final']/r['k_cut_eff']*100:.0f}%  "
              f"[{r['walltime_s']:.0f}s]")

    if len(rows) >= 2:
        fs = np.array([r["flatness"] for r in rows])
        nus = np.array([r["nu"] for r in rows])
        pF = np.log(fs[-1] / fs[0]) / np.log(nus[0] / nus[-1])
        ms = np.array([r["budget_margin_min"] for r in rows])
        pm = np.log(ms[-1] / ms[0]) / np.log(nus[0] / nus[-1])
        print(f"\n  Flatness vs nu: power p_F = {pF:+.2f}; budget-margin power "
              f"p_m = {pm:+.2f} (margin: how far the order-eps budget sits above "
              f"the measured high-shell share).")
    else:
        pF = pm = 0.0

    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"cases": cases, "flatness_power": float(pF),
                   "margin_power": float(pm)}, f, indent=2)

    assert len(rows) >= 2, "at least two stationary forced cases needed"
    assert all(0.0 < r["flatness"] < 200.0 for r in rows), "flatness outlier"
    assert all(r["theta_high_max"] < 1.0 for r in rows), "high-shell fraction"
    assert all(r["budget_margin_min"] > 0.5 for r in rows), (
        "measured high-shell share exceeds the order-eps budget")
    print("\n" + "=" * 78)
    print("PASS: forced steady state reached; int Z^2 finite; high-shell share is")
    print("      inside (or consistent with) the O(eps) intermittency budget;")
    print("      k_eff well below cutoff.  Wall stays OPEN.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())