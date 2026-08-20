"""Quick long-time verification: R -> 0 for 1D NS at t=100."""
import json
import numpy as np

def run():
    N = 256
    L = 2 * np.pi
    dx = L / N
    x = np.linspace(0, L, N, endpoint=False)
    k = np.fft.fftfreq(N, d=dx) * 2 * np.pi
    dt = 0.0005
    T = 100.0
    si = 500
    n_steps = int(T / dt)
    nu = 0.1

    u0 = np.sin(x) + 0.5 * np.sin(2 * x)
    u_hat = np.fft.fft(u0)

    R_at = {}
    times_to_check = [0.5, 1, 2, 5, 10, 20, 50, 100]

    for step in range(1, n_steps + 1):
        visc = np.exp(-nu * k**2 * dt)
        u_hat = u_hat * visc
        u = np.fft.ifft(u_hat).real
        du = np.fft.ifft(1j * k * u_hat).real
        nl = u * du
        dealias = np.ones(N)
        dealias[N // 3:2 * N // 3 + 1] = 0
        u_hat = u_hat - dt * np.fft.fft(nl) * dealias

        t = step * dt
        # Check if t is close to any target time
        for tt in times_to_check:
            if abs(t - tt) < dt * 0.6 and tt not in R_at:
                u = np.fft.ifft(u_hat).real
                gu = np.gradient(u, dx)
                lu = np.gradient(gu, dx)
                E = 0.5 * np.sum(u**2) * dx
                Z = 0.5 * np.sum(gu**2) * dx
                nl_L2 = np.sqrt(np.sum((u * gu)**2) * dx)
                vi_L2 = np.sqrt(np.sum((nu * lu)**2) * dx)
                R = nl_L2 / vi_L2 if vi_L2 > 1e-15 else 0
                bound = (2 * E)**0.75 / (nu * (2 * Z)**0.25) if Z > 1e-15 else 0
                R_at[tt] = {
                    "R": float(R),
                    "E": float(E),
                    "Z": float(Z),
                    "bound": float(bound),
                }

    print(f"nu={nu}, T={T}")
    for tt in sorted(R_at):
        d = R_at[tt]
        ratio = d["R"] / d["bound"] if d["bound"] > 0 else 0
        print(f"  t={tt:5.1f}: R={d['R']:.4f}, bound={d['bound']:.2f}, "
              f"R/bound={ratio:.4f}, E={d['E']:.6e}")

    # Save
    out = {"nu": nu, "T": T, "times": R_at}
    with open("data/ns_1d_longtime_data.json", "w") as f:
        json.dump(out, f, indent=2)
    print("Saved to data/ns_1d_longtime_data.json")

if __name__ == "__main__":
    run()
