"""
EXTREME AMPLITUDE TEST: Does R*nu <= 4.68 hold for A = 1, 5, 10, 50, 100?
"""
import json
import numpy as np
import os

def spectral_step(u_hat, dx, dt, nu, k):
    n = len(u_hat)
    viscous = np.exp(-nu * k**2 * dt)
    u_hat_v = u_hat * viscous
    u = np.fft.ifft(u_hat_v).real
    du = np.fft.ifft(1j * k * u_hat_v).real
    nl = u * du
    dealias = np.ones(n)
    dealias[n // 3:2 * n // 3 + 1] = 0
    return u_hat_v - dt * np.fft.fft(nl) * dealias

def run():
    N = 512
    L_domain = 2.0 * np.pi
    dx = L_domain / N
    x = np.linspace(0, L_domain, N, endpoint=False)
    k = np.fft.fftfreq(N, d=dx) * 2.0 * np.pi
    dt = 0.0002
    T = 10.0
    si = 100
    n_steps = int(T / dt)

    amplitudes = [1, 2, 5, 10, 20, 50, 100]
    viscosities = [0.01, 0.05, 0.1]
    ic_types = ["single", "multi", "turbulent"]

    results = {}

    for A in amplitudes:
        for nu in viscosities:
            for ic_type in ic_types:
                if ic_type == "single":
                    u0 = A * np.sin(x)
                elif ic_type == "multi":
                    u0 = A * (np.sin(x) + 0.5*np.sin(2*x) + 0.3*np.sin(3*x))
                else:
                    u0 = A * (np.sin(x) + 0.3*np.sin(3*x) + 0.2*np.sin(5*x) +
                              0.1*np.sin(7*x) + 0.05*np.sin(11*x))

                u_hat = np.fft.fft(u0)
                E0 = 0.5 * np.sum(u0**2) * dx

                R_max = 0
                Rnu_max = 0
                C0_max = 0

                for step in range(1, n_steps + 1):
                    u_hat = spectral_step(u_hat, dx, dt, nu, k)
                    if step % si == 0:
                        u = np.fft.ifft(u_hat).real
                        gu = np.gradient(u, dx)
                        lu = np.gradient(gu, dx)
                        E = 0.5 * np.sum(u**2) * dx
                        Z = 0.5 * np.sum(gu**2) * dx
                        epsilon = 2 * nu * Z

                        nl_L2 = np.sqrt(np.sum((u * gu)**2) * dx)
                        vi_L2 = np.sqrt(np.sum((nu * lu)**2) * dx)
                        R = nl_L2 / vi_L2 if vi_L2 > 1e-15 else 0

                        u_inf = np.max(np.abs(u))
                        C0 = u_inf / (epsilon**(1.0/3.0)) if epsilon > 1e-15 else 0

                        R_max = max(R_max, R)
                        Rnu_max = max(Rnu_max, R * nu)
                        C0_max = max(C0_max, C0)

                key = f"A{A}_nu{nu}_{ic_type}"
                results[key] = {
                    "A": A, "nu": nu, "ic": ic_type, "E0": float(E0),
                    "R_max": float(R_max),
                    "Rnu_max": float(Rnu_max),
                    "C0_max": float(C0_max),
                }

    # Check if Rnu > 4.68 ever
    Rnu_all = [r["Rnu_max"] for r in results.values()]
    violations = [(k, r) for k, r in results.items() if r["Rnu_max"] > 4.68]

    output = {
        "results": results,
        "summary": {
            "n_cases": len(results),
            "Rnu_global_max": float(max(Rnu_all)),
            "Rnu_global_mean": float(np.mean(Rnu_all)),
            "violations_of_4.68": len(violations),
            "violation_details": {k: r["Rnu_max"] for k, r in violations},
        },
    }

    os.makedirs("data", exist_ok=True)
    with open("data/extreme_amplitude_data.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"Extreme amplitude test: {len(results)} cases")
    print(f"R*nu global max: {max(Rnu_all):.4f}")
    print(f"Violations of 4.68: {len(violations)}")
    for k, r in violations:
        print(f"  {k}: R*nu = {r['Rnu_max']:.4f}")
    return output

if __name__ == "__main__":
    run()
