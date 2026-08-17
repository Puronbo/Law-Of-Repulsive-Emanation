"""
Noether's theorem via 0/0 (Landau/mean-field Ising)
====================================================
Noether's theorem: every continuous symmetry has a conserved charge.
The Z_2 spin-flip symmetry sigma -> -sigma of the Ising Hamiltonian
has the magnetization M = <sigma> as its conserved charge.

The 0/0: at the critical temperature T_c, the order parameter M(T) is 0/0:
  - For T > T_c: M = 0 (symmetric phase, charge = 0)
  - For T < T_c: M > 0 (broken phase, charge nonzero)
  - At T = T_c: M = 0/0 (both phases coexist)

The mean-field self-consistency equation: M = tanh(M/T)
Near T_c = 1: M ~ sqrt(3(1-T)), so M/(1-T)^{1/2} -> sqrt(3).

The removable value sqrt(3) is the Landau critical amplitude -- the
unique finite value encoding how the Noether charge (order parameter)
emerges from the symmetric vacuum.

HONEST WALL: mean-field theory (infinite-range interaction), not a proof
of critical phenomena or the existence of phase transitions in finite
dimensions.
"""

import numpy as np
from scipy.optimize import brentq
import json


def solve_mf_ising(T):
    """Solve M = tanh(M/T) for the nontrivial root (T < T_c=1)."""
    if T >= 1.0:
        return 0.0
    # M - tanh(M/T) = 0, find nonzero root in (0, 1)
    # f(M) = M - tanh(M/T); f(0) = 0, f(eps) < 0, f(1) > 0 for T < 1
    f = lambda M: M - np.tanh(M / T)
    # Find bracket: f(eps) should be negative for small eps > 0
    eps = 1e-6
    if f(eps) >= 0:
        return 0.0
    # Find upper bound where f > 0
    M_upper = 1.0
    while f(M_upper) <= 0 and M_upper < 10:
        M_upper *= 2
    try:
        return float(brentq(f, eps, M_upper, xtol=1e-14))
    except ValueError:
        return 0.0


def solve_mf_ising_iterative(T, n_iter=5000, M0=0.5):
    """Fallback iterative solver."""
    M = M0
    for _ in range(n_iter):
        M_new = np.tanh(M / T)
        if abs(M_new - M) < 1e-15:
            break
        M = M_new
    return float(M)


def run():
    results = {}

    # --- Test 1: solve for T near T_c = 1 from below ---
    Tc = 1.0
    amplitudes = []
    for k in range(1, 11):
        T = Tc - 10.0 ** (-k)
        M = solve_mf_ising(T)
        delta = Tc - T
        amp = M / np.sqrt(delta) if delta > 0 else float("nan")
        amplitudes.append({
            "T": T, "M": M, "delta": delta,
            "amplitude": amp, "error": abs(amp - np.sqrt(3))
        })
    results["critical_amplitude"] = amplitudes

    # --- Test 2: verify M = 0 for T > T_c ---
    above_Tc = []
    for T in [1.01, 1.1, 1.5, 2.0, 5.0]:
        M = solve_mf_ising(T)
        above_Tc.append({
            "T": T, "M": M, "is_zero": 1 if abs(M) < 1e-10 else 0
        })
    results["above_Tc"] = above_Tc

    # --- Test 3: verify M != 0 for T < T_c ---
    below_Tc = []
    for T in [0.5, 0.8, 0.9, 0.99, 0.999]:
        M = solve_mf_ising(T)
        below_Tc.append({"T": T, "M": M, "nonzero": 1 if abs(M) > 1e-6 else 0})
    results["below_Tc"] = below_Tc

    # --- Test 4: free energy minimum at self-consistent M ---
    energy_checks = []
    for T in [0.5, 0.9, 0.99, 0.999]:
        M = solve_mf_ising(T)
        if M > 0:
            dF = -np.tanh(M / T) + M  # dF/dM, should be 0 by self-consistency
            energy_checks.append({"T": T, "dF_dM": float(dF), "is_zero": 1 if abs(dF) < 1e-10 else 0})
        else:
            energy_checks.append({"T": T, "dF_dM": 0.0, "is_zero": 1})
    results["free_energy_minimum"] = energy_checks

    # --- Summary ---
    last_amp = amplitudes[-1]["error"]
    all_above_zero = all(c["is_zero"] for c in above_Tc)
    all_below_nonzero = all(c["nonzero"] for c in below_Tc)
    all_energy = all(c["is_zero"] for c in energy_checks)
    supported = bool(last_amp < 1e-2 and all_above_zero and all_below_nonzero and all_energy)
    results["summary"] = {
        "amplitude_error": last_amp,
        "sqrt_3_expected": float(np.sqrt(3)),
        "above_Tc_all_zero": all_above_zero,
        "below_Tc_all_nonzero": all_below_nonzero,
        "free_energy_minima": all_energy,
        "supported": supported,
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Noether/Landau via 0/0 (mean-field Ising)")
    print(f"  critical amplitude -> sqrt(3)={s['sqrt_3_expected']:.6f}: err={s['amplitude_error']:.2e}")
    print(f"  above Tc all zero: {s['above_Tc_all_zero']}")
    print(f"  below Tc all nonzero: {s['below_Tc_all_nonzero']}")
    print(f"  free energy minima: {s['free_energy_minima']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/noether_landau_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
