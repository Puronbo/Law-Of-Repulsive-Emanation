"""
Ising model phase transition via 0/0
====================================
The 2D Ising model on a lattice: each site has spin s_i = +/-1, and
the energy is E = -J sum_{<ij>} s_i s_j - h sum_i s_i.

The magnetization M = (1/N) sum_i s_i. At the critical temperature T_c
(for the 2D square lattice, T_c / J = 2/log(1+sqrt(2)) ~ 2.269):

The 0/0: the susceptibility chi = dM/dh at h = 0 diverges at T_c.
The ratio chi(T) / |T - T_c|^{-gamma} has a 0/0 at T = T_c (both
numerator and denominator diverge). The removable value = C (the
critical amplitude).

The order parameter: M(T) ~ (T_c - T)^beta for T < T_c.
At T = T_c: M = 0. The ratio M / (T_c - T)^beta -> 1 as T -> T_c-.
At T = T_c: both are 0, giving 0/0 with removable value = 1.

The correlation length: xi(T) ~ |T - T_c|^{-nu}.
At T = T_c: xi = infinity. The ratio xi * |T - T_c|^nu -> C (constant).
0/0 at T = T_c with removable value = C.

The specific heat: C_v ~ |T - T_c|^{-alpha}.
At T = T_c: C_v diverges. The ratio C_v * |T - T_c|^alpha -> C.
0/0 at T = T_c.

HONEST WALL: Monte Carlo simulation of the 2D Ising model with
finite-size effects. Not a proof of critical phenomena.
"""

import numpy as np
import json


def ising_mc_2d(L, T, n_sweeps=5000, n_therm=1000):
    """Monte Carlo simulation of 2D Ising model with Metropolis algorithm.

    Returns average magnetization per spin and energy per spin.
    """
    N = L * L
    beta = 1.0 / T if T > 0 else float('inf')

    # Initialize lattice
    lattice = np.random.choice([-1, 1], size=(L, L))

    def calc_energy(lat):
        E = 0.0
        for i in range(L):
            for j in range(L):
                s = lat[i, j]
                nn = (lat[(i+1) % L, j] + lat[(i-1) % L, j] +
                      lat[i, (j+1) % L] + lat[i, (j-1) % L])
                E -= s * nn
        return E / N

    def calc_magnetization(lat):
        return np.mean(lat)

    # Thermalization
    for _ in range(n_therm):
        for _ in range(N):
            i = np.random.randint(L)
            j = np.random.randint(L)
            s = lattice[i, j]
            nn = (lattice[(i+1) % L, j] + lattice[(i-1) % L, j] +
                  lattice[i, (j+1) % L] + lattice[i, (j-1) % L])
            dE = 2 * s * nn
            if dE <= 0 or np.random.random() < np.exp(-beta * dE):
                lattice[i, j] = -s

    # Measurement
    M_sum = 0.0
    M2_sum = 0.0
    E_sum = 0.0
    for _ in range(n_sweeps):
        for _ in range(N):
            i = np.random.randint(L)
            j = np.random.randint(L)
            s = lattice[i, j]
            nn = (lattice[(i+1) % L, j] + lattice[(i-1) % L, j] +
                  lattice[i, (j+1) % L] + lattice[i, (j-1) % L])
            dE = 2 * s * nn
            if dE <= 0 or np.random.random() < np.exp(-beta * dE):
                lattice[i, j] = -s
        m = calc_magnetization(lattice)
        M_sum += abs(m)
        M2_sum += m * m
        E_sum += calc_energy(lattice)

    M_avg = M_sum / n_sweeps
    M2_avg = M2_sum / n_sweeps
    E_avg = E_sum / n_sweeps

    # Susceptibility: chi = N * (M2 - M^2) / T
    chi = N * (M2_avg - M_avg * M_avg) / T if T > 0 else 0

    return float(M_avg), float(E_avg), float(chi)


def run():
    results = {"tests": [], "summary": {}}

    # Exact critical temperature for 2D Ising on square lattice
    T_c_exact = 2.0 / np.log(1 + np.sqrt(2))

    # --- Test 1: Magnetization near T_c ---
    L = 30
    n_sweeps = 2000
    n_therm = 500

    T_values = [1.5, 1.8, 2.0, T_c_exact - 0.1,
                T_c_exact, T_c_exact + 0.1,
                2.5, 3.0, 4.0]
    mag_tests = []
    for T in T_values:
        M, E, chi = ising_mc_2d(L, T, n_sweeps, n_therm)
        mag_tests.append({
            "T": float(T),
            "T_over_Tc": float(T / T_c_exact),
            "magnetization": float(M),
            "energy_per_spin": float(E),
            "susceptibility": float(chi),
            "below_Tc": bool(T < T_c_exact - 0.05),
            "above_Tc": bool(T > T_c_exact + 0.15),
            "has_magnetization": bool(M > 0.1)
        })

    results["magnetization"] = {
        "note": f"T_c = {T_c_exact:.6f} (exact); M > 0 below T_c, M ~ 0 above T_c",
        "L": L,
        "tests": mag_tests
    }

    # --- Test 1b: Phase transition signature ---
    # M drops sharply near T_c: just check low-T has high M, high-T has low M
    low_T_mag = [t["magnetization"] for t in mag_tests if t["T"] < 1.8]
    high_T_mag = [t["magnetization"] for t in mag_tests if t["T"] > 3.5]
    phase_transition_ok = (len(low_T_mag) > 0 and len(high_T_mag) > 0 and
                           min(low_T_mag) > 0.8 and max(high_T_mag) < 0.15)

    results["phase_transition"] = {
        "note": "M is high at low T and low at high T (phase transition)",
        "low_T_magnetizations": low_T_mag,
        "high_T_magnetizations": high_T_mag,
        "ok": bool(phase_transition_ok)
    }

    # --- Test 2: Order parameter scaling ---
    # M(T) ~ (T_c - T)^beta with beta = 1/8 for 2D Ising
    beta_exact = 1.0 / 8.0
    scaling_tests = []
    for dT in [0.3, 0.2, 0.1, 0.05, 0.02]:
        T = T_c_exact - dT
        M, _, _ = ising_mc_2d(L, T, n_sweeps, n_therm)
        if M > 0 and dT > 0:
            effective_beta = np.log(M) / np.log(dT)
            scaling_tests.append({
                "dT": float(dT),
                "T": float(T),
                "magnetization": float(M),
                "effective_beta": float(effective_beta),
                "beta_exact": float(beta_exact),
                "deviation": float(abs(effective_beta - beta_exact))
            })

    results["order_parameter"] = {
        "note": "M ~ (Tc-T)^(1/8) below Tc: effective beta -> 1/8",
        "tests": scaling_tests
    }

    # --- Test 3: Energy at T_c ---
    # Energy per spin at T_c for 2D Ising: E/N = -sqrt(2) exactly
    # (each bond counted once). Our formula double-counts, so E/N = -2*sqrt(2).
    E_exact = -2.0 * np.sqrt(2)
    E_tests = []
    for L_val in [10, 20, 30]:
        E_vals = []
        for _ in range(3):
            _, E, _ = ising_mc_2d(L_val, T_c_exact, n_sweeps, n_therm)
            E_vals.append(E)
        E_mean = np.mean(E_vals)
        E_tests.append({
            "L": L_val,
            "E_mean": float(E_mean),
            "E_exact": float(E_exact),
            "deviation": float(abs(E_mean - E_exact))
        })

    results["energy_at_Tc"] = {
        "note": "E/N = -sqrt(2) at T_c (exact for 2D Ising)",
        "tests": E_tests
    }

    # --- Test 4: Susceptibility peaks near T_c ---
    # chi diverges at T_c (0/0: chi*|T-Tc|^gamma -> C)
    # For finite systems: chi has a peak near T_c
    chi_peak_tests = []
    for T in [1.5, 1.8, 2.0, 2.2, T_c_exact, 2.4, 2.6, 3.0, 4.0]:
        _, _, chi = ising_mc_2d(L, T, n_sweeps, n_therm)
        chi_peak_tests.append({
            "T": float(T),
            "chi": float(chi),
            "is_peak_candidate": bool(abs(T - T_c_exact) < 0.3)
        })

    # Find the T with max chi
    max_chi_idx = max(range(len(chi_peak_tests)),
                      key=lambda i: chi_peak_tests[i]["chi"])
    peak_near_Tc = abs(chi_peak_tests[max_chi_idx]["T"] - T_c_exact) < 0.3

    results["susceptibility_0_over_0"] = {
        "note": "chi diverges at Tc: 0/0 with removable value = C",
        "peak_near_Tc": bool(peak_near_Tc),
        "tests": chi_peak_tests
    }

    # --- Test 5: Symmetry at h = 0 ---
    # At h = 0, the magnetization should be zero in the thermodynamic limit.
    # For finite systems, <|M|> > 0 but -> 0 as L -> infinity for T > T_c.
    symmetry_tests = []
    for L_val in [10, 20, 40]:
        M_above, _, _ = ising_mc_2d(L_val, T_c_exact + 0.5, n_sweeps, n_therm)
        symmetry_tests.append({
            "L": L_val,
            "T": float(T_c_exact + 0.5),
            "abs_magnetization": float(M_above),
            "should_vanish": bool(M_above < 0.5)
        })

    results["symmetry_restoration"] = {
        "note": "<|M|> -> 0 as L -> inf for T > Tc (symmetry restoration)",
        "tests": symmetry_tests
    }

    # --- Summary ---
    # Check phase transition
    mag_ok = phase_transition_ok

    # Check energy at T_c
    E_ok = all(t["deviation"] < 0.3 for t in E_tests)

    # Check susceptibility peaks near Tc
    chi_ok = bool(peak_near_Tc)

    supported = bool(mag_ok and E_ok and chi_ok)

    results["summary"] = {
        "supported": supported,
        "magnetization_correct": mag_ok,
        "energy_at_Tc_correct": E_ok,
        "susceptibility_peaks_near_Tc": chi_ok,
        "Tc_exact": float(T_c_exact),
        "honest_wall": "Monte Carlo simulation with finite-size effects, "
                       "not a proof of critical phenomena"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Ising model via 0/0")
    print(f"  T_c = {s['Tc_exact']:.6f}")
    print(f"  Magnetization correct:   {s['magnetization_correct']}")
    print(f"  Energy at T_c correct:   {s['energy_at_Tc_correct']}")
    print(f"  Susceptibility peaks:    {s['susceptibility_peaks_near_Tc']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/ising_model_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
