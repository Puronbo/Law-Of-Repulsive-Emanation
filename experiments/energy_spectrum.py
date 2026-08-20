"""
ENERGY SPECTRUM E(k): Verify the -5/3 Kolmogorov scaling
for turbulent 1D NS solutions. This validates the cascade
structure that underlies the reduction.
"""
import json
import numpy as np
import os

def run():
    N = 4096
    L_domain = 2.0 * np.pi
    dx = L_domain / N
    x = np.linspace(0, L_domain, N, endpoint=False)
    k_arr = np.fft.fftfreq(N, d=dx) * 2.0 * np.pi
    nu = 0.01
    dt = 0.0001
    T_total = 20.0
    si = 200
    n_steps = int(T_total / dt)

    # Turbulent IC: many modes
    np.random.seed(42)
    n_modes = 32
    u0 = np.zeros(N)
    for m in range(1, n_modes + 1):
        amp = 1.0 / m**0.8
        phase = np.random.uniform(0, 2*np.pi)
        u0 += amp * np.sin(m * x + phase)
    u0 *= 3.0

    u_hat = np.fft.fft(u0)
    u0_norm = u0.copy()

    # Record spectra at different times
    spectrum_times = [0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0]
    spectra = {}
    emax_times = []

    for step in range(1, n_steps + 1):
        u_hat_new = np.exp(-nu * k_arr**2 * dt) * u_hat
        u_phys = np.fft.ifft(u_hat_new).real
        du_phys = np.fft.ifft(1j * k_arr * u_hat_new).real
        nl = u_phys * du_phys
        dealias = np.ones(N)
        dealias[N // 3:2 * N // 3 + 1] = 0
        u_hat = u_hat_new - dt * np.fft.fft(nl) * dealias

        t = step * dt
        if any(abs(t - st) < dt / 2 for st in spectrum_times):
            E_k = np.zeros(N // 2)
            u_hat_snap = u_hat.copy()
            u_snap = np.fft.ifft(u_hat_snap).real
            gu_snap = np.fft.ifft(1j * k_arr * u_hat_snap).real
            E_snap = 0.5 * np.sum(u_snap**2) * dx / (2 * np.pi)
            Z_snap = 0.5 * np.sum(gu_snap**2) * dx / (2 * np.pi)

            for k_val in range(1, N // 2 + 1):
                idx_pos = k_val
                idx_neg = N - k_val
                E_k[k_val - 1] = (np.abs(u_hat_snap[idx_pos])**2 + np.abs(u_hat_snap[idx_neg])**2) * (2 * np.pi) / (2 * N**2 * L_domain)

            k_valid = np.arange(1, N // 2 + 1)
            E_k_pos = E_k[E_k > 0]
            k_pos = k_valid[E_k > 0]

            emax = np.max(np.abs(u_phys))
            eps = 2 * nu * Z_snap

            spectra[str(t)] = {
                "k": k_pos.tolist()[:200],
                "E_k": E_k_pos.tolist()[:200],
                "E_total": float(E_snap),
                "Z_total": float(Z_snap),
                "epsilon": float(eps),
                "u_inf": float(emax),
                "k_max": int(k_pos[np.argmax(E_k_pos)]) if len(k_pos) > 0 else 0,
            }

    # Fit the -5/3 slope in the inertial range
    # Use the spectrum at t=10 (well-developed cascade)
    t_ref = "10.0"
    if t_ref in spectra:
        k_data = np.array(spectra[t_ref]["k"], dtype=float)
        E_data = np.array(spectra[t_ref]["E_k"], dtype=float)

        # Inertial range: 5 <= k <= 50
        mask = (k_data >= 5) & (k_data <= 50) & (E_data > 0)
        if np.sum(mask) > 5:
            log_k = np.log(k_data[mask])
            log_E = np.log(E_data[mask])
            coeffs = np.polyfit(log_k, log_E, 1)
            slope = coeffs[0]
            intercept = coeffs[1]
            C_K_measured = np.exp(intercept)

            # Kolmogorov prediction: E(k) = C_K * eps^{2/3} * k^{-5/3}
            eps_ref = spectra[t_ref]["epsilon"]
            C_K_pred = C_K_measured / (eps_ref**(2.0/3.0)) if eps_ref > 0 else 0
        else:
            slope = 0
            C_K_pred = 0
    else:
        slope = 0
        C_K_pred = 0

    output = {
        "nu": nu,
        "N": N,
        "spectra": spectra,
        "inertial_range_fit": {
            "slope": float(slope),
            "target_slope": -5.0/3.0,
            "deviation": float(abs(slope - (-5.0/3.0))),
            "C_K_empirical": float(C_K_pred),
            "C_K_standard": 1.5,
        },
    }

    os.makedirs("data", exist_ok=True)
    with open("data/energy_spectrum_data.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"Energy spectrum analysis:")
    print(f"  Fitted slope in inertial range: {slope:.3f} (target: -1.667)")
    print(f"  Deviation from -5/3: {abs(slope - (-5.0/3.0)):.3f}")
    print(f"  Kolmogorov constant C_K: {C_K_pred:.3f} (standard: 1.5)")
    for t_key in sorted(spectra.keys(), key=float):
        s = spectra[t_key]
        print(f"  t={t_key}: E={s['E_total']:.4f}, Z={s['Z_total']:.4f}, eps={s['epsilon']:.4f}, k_peak={s['k_max']}")
    return output

if __name__ == "__main__":
    run()
