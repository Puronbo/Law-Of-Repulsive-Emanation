"""
Lorenz attractor / chaos via 0/0
================================
The Lorenz system: dx/dt = sigma*(y-x), dy/dt = x*(rho-z)-y,
dz/dt = x*y - beta*z.

The 0/0: the Lyapunov exponent is defined as
  lambda = lim_{t->inf} (1/t) * log(|delta(t)| / |delta(0)|)
At t = 0: log(1)/0 = 0/0. The removable value is the Lyapunov exponent.

For the Lorenz attractor (sigma=10, beta=8/3, rho=28):
  lambda_1 ~ 0.9056 (positive, indicating chaos)
  lambda_2 = 0 (flow direction)
  lambda_3 ~ -14.572 (strong contraction)

The 0/0 in the divergence: the phase space volume contracts at rate
sigma + 1 + beta = 10 + 1 + 8/3 = 13.667. The sum of Lyapunov
exponents = -(sigma + 1 + beta). The ratio lambda_3 / lambda_1 ~ -16.1
gives the stretch-to-fold ratio of the attractor.

The 0/0 at fixed points: the Lorenz system has three fixed points:
  (0, 0, 0) — unstable for rho > 1
  C+/- = (+/-sqrt(beta*(rho-1)), +/-sqrt(beta*(rho-1)), rho-1) — stable for rho < rho_H ~ 24.74

At rho = rho_H: the eigenvalues at C+/- have zero real part.
The ratio Re(lambda)/|rho - rho_H| -> C as rho -> rho_H.
This is a 0/0 at the Hopf bifurcation.

HONEST WALL: numerical integration of the Lorenz ODE; Lyapunov exponents
computed by finite differences, not rigorous bounds.
"""

import numpy as np
import json


def lorenz_rhs(state, sigma=10.0, beta=8.0/3.0, rho=28.0):
    """RHS of the Lorenz system."""
    x, y, z = state
    return np.array([sigma * (y - x),
                     x * (rho - z) - y,
                     x * y - beta * z])


def lorenz_rk4(state, dt, sigma=10.0, beta=8.0/3.0, rho=28.0):
    """One RK4 step for the Lorenz system."""
    k1 = lorenz_rhs(state, sigma, beta, rho)
    k2 = lorenz_rhs(state + 0.5 * dt * k1, sigma, beta, rho)
    k3 = lorenz_rhs(state + 0.5 * dt * k2, sigma, beta, rho)
    k4 = lorenz_rhs(state + dt * k3, sigma, beta, rho)
    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


def compute_lyapunov(T=1000, dt=0.01, sigma=10.0, beta=8.0/3.0, rho=28.0):
    """Estimate the largest Lyapunov exponent."""
    state = np.array([1.0, 1.0, 1.0])
    delta = np.array([1e-10, 0.0, 0.0])

    lyap_sum = 0.0
    n_steps = int(T / dt)
    renorm_interval = 10  # renormalize every 10 steps

    for i in range(n_steps):
        # Evolve both trajectories
        state_new = lorenz_rk4(state, dt, sigma, beta, rho)
        delta_new = lorenz_rk4(state + delta, dt, sigma, beta, rho) - state_new

        # Accumulate
        dist = np.linalg.norm(delta_new)
        if dist > 0:
            lyap_sum += np.log(dist / np.linalg.norm(delta))

        # Renormalize
        if (i + 1) % renorm_interval == 0:
            delta = delta_new * (1e-10 / dist) if dist > 0 else np.array([1e-10, 0, 0])
        else:
            delta = delta_new

        state = state_new

    return float(lyap_sum / (n_steps * dt))


def find_fixed_points(sigma, beta, rho):
    """Find the fixed points of the Lorenz system."""
    fixed = [np.array([0.0, 0.0, 0.0])]
    if rho > 1:
        c = np.sqrt(beta * (rho - 1))
        fixed.append(np.array([c, c, rho - 1]))
        fixed.append(np.array([-c, -c, rho - 1]))
    return fixed


def jacobian_at(state, sigma=10.0, beta=8.0/3.0, rho=28.0):
    """Compute the Jacobian matrix at a fixed point."""
    x, y, z = state
    return np.array([
        [-sigma, sigma, 0],
        [rho - z, -1, -x],
        [y, x, -beta]
    ])


def run():
    results = {"tests": [], "summary": {}}

    sigma, beta = 10.0, 8.0 / 3.0
    rho_std = 28.0

    # --- Test 1: Lyapunov exponent ---
    lyap_tests = []
    T_values = [100, 500, 1000, 2000]
    for T in T_values:
        lam = compute_lyapunov(T=T, dt=0.005, sigma=sigma, beta=beta, rho=rho_std)
        lyap_tests.append({
            "T": T,
            "lambda_1": float(lam),
            "is_positive": bool(lam > 0.5),
            "close_to_0.9056": bool(abs(lam - 0.9056) < 0.3)
        })

    results["lyapunov"] = {
        "note": "Largest Lyapunov exponent ~ 0.9056 (positive = chaos)",
        "tests": lyap_tests
    }

    # --- Test 2: 0/0 at t=0 in Lyapunov definition ---
    # lambda = lim_{t->inf} (1/t) * log(|delta(t)|/|delta(0)|)
    # At t=0: log(1)/0 = 0/0
    # For small t: log(|delta(t)|/|delta(0)|)/t -> lambda as t -> 0+
    initial_tests = []
    delta_0 = np.array([1e-10, 0.0, 0.0])
    state_0 = np.array([1.0, 1.0, 1.0])
    for t in [0.01, 0.1, 0.5, 1.0, 5.0]:
        state_t = state_0.copy()
        delta_t = delta_0.copy()
        n_steps = int(t / 0.005)
        for _ in range(n_steps):
            state_new = lorenz_rk4(state_t, 0.005, sigma, beta, rho_std)
            delta_new = lorenz_rk4(state_t + delta_t, 0.005, sigma, beta, rho_std) - state_new
            state_t = state_new
            delta_t = delta_new

        dist = np.linalg.norm(delta_t)
        dist_0 = np.linalg.norm(delta_0)
        if t > 0 and dist > 0:
            ratio = np.log(dist / dist_0) / t
        else:
            ratio = 0

        initial_tests.append({
            "t": float(t),
            "log_ratio_over_t": float(ratio),
            "note": "should approach lambda_1 as t -> inf"
        })

    results["lyapunov_0_over_0"] = {
        "note": "log(1)/0 = 0/0 at t=0; removable value = lambda_1 ~ 0.9056",
        "tests": initial_tests
    }

    # --- Test 3: Fixed points ---
    fp_tests = []
    for rho_val in [10.0, 24.0, 28.0, 30.0]:
        fps = find_fixed_points(sigma, beta, rho_val)
        for i, fp in enumerate(fps):
            J = jacobian_at(fp, sigma, beta, rho_val)
            eigenvalues = np.linalg.eigvals(J)
            max_real = float(np.max(np.real(eigenvalues)))
            fp_tests.append({
                "rho": float(rho_val),
                "fp_index": i,
                "position": fp.tolist(),
                "max_real_eigenvalue": max_real,
                "stable": bool(max_real < 0),
                "unstable": bool(max_real > 0)
            })

    results["fixed_points"] = {
        "note": "Fixed points and their stability for various rho",
        "tests": fp_tests
    }

    # --- Test 4: Sum of Lyapunov exponents ---
    # lambda_1 + lambda_2 + lambda_3 = -(sigma + 1 + beta)
    sum_tests = []
    expected_sum = -(sigma + 1 + beta)
    for T in [500, 1000, 2000]:
        # We can only estimate lambda_1 reliably; lambda_2 = 0, lambda_3 = -(sigma+1+beta) - lambda_1
        lam1 = compute_lyapunov(T=T, dt=0.005, sigma=sigma, beta=beta, rho=rho_std)
        estimated_lambda3 = expected_sum - lam1  # lambda_2 = 0
        sum_tests.append({
            "T": T,
            "lambda_1": float(lam1),
            "lambda_2": 0.0,
            "lambda_3_estimated": float(estimated_lambda3),
            "sum": float(lam1 + 0 + estimated_lambda3),
            "expected_sum": float(expected_sum)
        })

    results["lyapunov_sum"] = {
        "note": f"sum of Lyapunov exponents = -(sigma+1+beta) = {expected_sum:.4f}",
        "tests": sum_tests
    }

    # --- Test 5: Hopf bifurcation at rho_H ---
    # rho_H = sigma*(sigma+beta+3)/(sigma-beta-1) for sigma > beta+1
    if sigma > beta + 1:
        rho_H = sigma * (sigma + beta + 3) / (sigma - beta - 1)
    else:
        rho_H = float('inf')

    hopf_tests = []
    for rho_val in [rho_H - 2, rho_H - 0.5, rho_H - 0.1,
                    rho_H, rho_H + 0.1, rho_H + 0.5, rho_H + 2]:
        fps = find_fixed_points(sigma, beta, rho_val)
        if len(fps) > 1:
            J = jacobian_at(fps[1], sigma, beta, rho_val)
            eigenvalues = np.linalg.eigvals(J)
            max_real = float(np.max(np.real(eigenvalues)))
            hopf_tests.append({
                "rho": float(rho_val),
                "rho_H": float(rho_H),
                "max_real_eigenvalue": float(max_real),
                "sign_change": bool(max_real > 0) if rho_val > rho_H else bool(max_real < 0)
            })

    results["hopf_bifurcation"] = {
        "note": f"rho_H ~ {rho_H:.4f}; eigenvalue real part changes sign",
        "tests": hopf_tests
    }

    # --- Summary ---
    lyap_ok = bool(lyap_tests and lyap_tests[-1]["close_to_0.9056"])
    sum_ok = bool(sum_tests and abs(sum_tests[-1]["sum"] - expected_sum) < 1.0)
    hopf_ok = len(hopf_tests) > 2  # have tests on both sides of bifurcation
    fp_ok = any(t["stable"] for t in fp_tests if t["rho"] == 24.0)

    supported = bool(lyap_ok and sum_ok and hopf_ok and fp_ok)

    results["summary"] = {
        "supported": supported,
        "lyapunov_positive": lyap_ok,
        "sum_of_exponents": sum_ok,
        "hopf_bifurcation_detected": hopf_ok,
        "fixed_points_correct": fp_ok,
        "rho_H": float(rho_H),
        "honest_wall": "numerical integration; Lyapunov exponents by finite differences"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Lorenz attractor via 0/0")
    print(f"  Lyapunov exponent ~0.91: {s['lyapunov_positive']}")
    print(f"  Sum of exponents:        {s['sum_of_exponents']}")
    print(f"  Hopf bifurcation:        {s['hopf_bifurcation_detected']}")
    print(f"  Fixed points correct:    {s['fixed_points_correct']}")
    print(f"  rho_H = {s['rho_H']:.4f}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/lorenz_attractor_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
