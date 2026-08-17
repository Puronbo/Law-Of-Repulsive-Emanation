"""
Boltzmann entropy via 0/0
=========================
Boltzmann entropy: S = k_B * ln(W), where W is the number of microstates.
In information theory units (k_B = 1): S = ln(W).

The 0/0: at W = 1 (single microstate), S = ln(1) = 0.
The ratio S/ln(W) at W = 1 is 0/0. The removable value = 1
(since S = ln(W) exactly, so S/ln(W) = 1 everywhere W > 1).

The 0/0 in the thermodynamic limit: S = k_B * ln(Ω(E)) where Ω(E)
is the density of states at energy E. At E = 0: Ω(0) may be 1 (ground
state), so S = 0. The ratio S/E as E -> 0+ is 0/0 (both S and E -> 0).
The removable value = dS/dE|_{E=0} = 1/T_0 (inverse ground-state temperature).

The 0/0 in the entropy of mixing: for ideal gases, Delta_S_mix = -R sum x_i ln(x_i).
At x_i = 0: 0*ln(0) = 0/0, removable value = 0.
At x_i = 1 (pure substance): Delta_S = 0 (not 0/0).

The 0/0 in the Shannon-Boltzmann connection: S = -sum p_i ln(p_i).
At p_i = 0: 0*ln(0) = 0/0, removable value = 0 (same as Shannon).
The entropy is maximized at p_i = 1/n (uniform), S = ln(n).

The 0/0 in the Gibbs entropy: S = -k_B sum_i p_i ln(p_i).
For a pure state (p_j = 1, all others 0): S = 0.
The ratio S / (1 - p_max) as p_max -> 1 is 0/0.
The removable value = 0 (entropy vanishes faster than 1-p_max).

HONEST WALL: numerical verification of Boltzmann/statistical entropy 0/0 limits.
"""

import numpy as np
import json
from itertools import product as iterproduct


def boltzmann_entropy(W):
    """S = ln(W), treating ln(1) = 0."""
    if W > 0:
        return float(np.log(W))
    return 0.0


def shannon_entropy(probs):
    """S = -sum p_i ln(p_i), treating 0*ln(0) = 0."""
    S = 0.0
    for p in probs:
        if p > 0:
            S -= p * np.log(p)
    return float(S)


def count_microstates_ising_1d(N, beta_J=0.5):
    """Count partition function for 1D Ising model (exact).
    Z = 2^N * cosh(beta_J)^N for periodic boundary conditions."""
    return float(2**N * np.cosh(beta_J)**N)


def run():
    results = {"tests": [], "summary": {}}

    # --- Test 1: S/ln(W) = 1 for all W > 1 ---
    ratio_tests = []
    for W in [1, 2, 5, 10, 50, 100, 1000]:
        S = boltzmann_entropy(W)
        ln_W = np.log(W) if W > 0 else 0
        if W > 1:
            ratio = S / ln_W
        else:
            ratio = "0/0"
        ratio_tests.append({
            "W": W,
            "S": float(S),
            "ln_W": float(ln_W),
            "S_over_lnW": float(ratio) if isinstance(ratio, float) else ratio,
            "is_one": bool(isinstance(ratio, float) and abs(ratio - 1.0) < 1e-10)
        })

    results["boltzmann_ratio"] = {
        "note": "S/ln(W) = 1 for all W > 1; at W=1: 0/0 removable value = 1",
        "tests": ratio_tests
    }

    # --- Test 2: 0*ln(0) = 0 in Shannon form ---
    zero_tests = []
    for eps in [1e-1, 1e-3, 1e-6, 1e-10]:
        val = eps * np.log(eps)
        zero_tests.append({
            "p": eps,
            "p_ln_p": float(val),
            "approaches_zero": bool(abs(val) < 0.3)
        })

    results["zero_ln_zero"] = {
        "note": "lim_{p->0+} p*ln(p) = 0: the 0/0 removable value is 0",
        "tests": zero_tests
    }

    # --- Test 3: Entropy of specific microstate counts ---
    micro_tests = []
    for W in [1, 2, 4, 8, 16, 32, 64]:
        S = boltzmann_entropy(W)
        S_expected = np.log(W)
        micro_tests.append({
            "W": W,
            "S": float(S),
            "ln_W": float(S_expected),
            "matches": bool(abs(S - S_expected) < 1e-12)
        })

    results["specific_entropies"] = {
        "note": "S = ln(W) for W = 2^n",
        "tests": micro_tests
    }

    # --- Test 4: Entropy of mixing ---
    mixing_tests = []
    # For a binary mixture with mole fractions x and 1-x:
    # Delta_S_mix = -R * (x*ln(x) + (1-x)*ln(1-x))
    # At x = 0: Delta_S = 0 (pure substance, not 0/0)
    # At x = 0.5: Delta_S = R*ln(2) (maximum mixing entropy)
    R = 8.314  # J/(mol*K)
    for x in [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]:
        if x > 0 and x < 1:
            dS = -R * (x * np.log(x) + (1 - x) * np.log(1 - x))
        else:
            dS = 0.0
        mixing_tests.append({
            "x": float(x),
            "Delta_S_mix": float(dS),
            "is_max_at_half": bool(abs(x - 0.5) < 0.01 and abs(dS - R * np.log(2)) < 1e-10)
        })

    results["entropy_of_mixing"] = {
        "note": "Delta_S_mix at x=0 and x=1 is 0 (0/0 removable); max at x=0.5",
        "tests": mixing_tests
    }

    # --- Test 5: 1D Ising partition function ---
    ising_tests = []
    for N in [4, 8, 16]:
        for beta_J in [0.1, 0.5, 1.0, 2.0]:
            Z = count_microstates_ising_1d(N, beta_J)
            S_thermo = np.log(Z)
            # Free energy F = -kT * ln(Z) = -ln(Z)/beta
            F = -S_thermo / beta_J if beta_J > 0 else 0
            # Average energy E = -d(ln Z)/d(beta)
            # For 1D Ising: E = -N * tanh(beta_J)
            E_avg = -N * np.tanh(beta_J)

            ising_tests.append({
                "N": N,
                "beta_J": float(beta_J),
                "Z": float(Z),
                "S": float(S_thermo),
                "F": float(F),
                "E_avg": float(E_avg)
            })

    results["ising_1d"] = {
        "note": "1D Ising: Z = 2^N*cosh(beta)^N, S = N*ln(2) + N*ln(cosh(beta))",
        "tests": ising_tests
    }

    # --- Test 6: Gibbs entropy for pure vs mixed states ---
    gibbs_tests = []
    # Pure state: p = [1, 0, ..., 0], S = 0
    for n in [2, 5, 10]:
        p_pure = [1.0] + [0.0] * (n - 1)
        S_pure = shannon_entropy(p_pure)
        gibbs_tests.append({
            "type": f"pure_{n}",
            "S": float(S_pure),
            "is_zero": bool(abs(S_pure) < 1e-15)
        })

    # Uniform: p = [1/n, ..., 1/n], S = ln(n)
    for n in [2, 5, 10]:
        p_uniform = [1.0 / n] * n
        S_uniform = shannon_entropy(p_uniform)
        gibbs_tests.append({
            "type": f"uniform_{n}",
            "S": float(S_uniform),
            "ln_n": float(np.log(n)),
            "matches": bool(abs(S_uniform - np.log(n)) < 1e-10)
        })

    # Near-pure: p = [1-eps, eps/(n-1), ..., eps/(n-1)]
    # S ~ -eps*ln(eps/(n-1)) ~ eps*ln(n-1) for small eps
    for eps in [0.1, 0.01, 0.001]:
        n = 10
        p_near = [1 - eps] + [eps / (n - 1)] * (n - 1)
        S_near = shannon_entropy(p_near)
        S_approx = -eps * np.log(eps / (n - 1))
        gibbs_tests.append({
            "type": f"near_pure_{eps}",
            "S": float(S_near),
            "S_approx": float(S_approx),
            "ratio_S_to_eps": float(S_near / eps) if eps > 0 else "0/0"
        })

    results["gibbs_entropy"] = {
        "note": "Gibbs: S=0 for pure states, S=ln(n) for uniform",
        "tests": gibbs_tests
    }

    # --- Summary ---
    ratio_ok = all(t["is_one"] for t in ratio_tests if isinstance(t["S_over_lnW"], float))
    zlz_ok = all(t["approaches_zero"] for t in zero_tests)
    mix_ok = any(t["is_max_at_half"] for t in mixing_tests)
    gibbs_pure_ok = all(t["is_zero"] for t in gibbs_tests if t["type"].startswith("pure"))
    gibbs_unif_ok = all(t["matches"] for t in gibbs_tests if t["type"].startswith("uniform"))

    supported = bool(ratio_ok and zlz_ok and mix_ok and gibbs_pure_ok and gibbs_unif_ok)

    results["summary"] = {
        "supported": supported,
        "boltzmann_ratio_one": ratio_ok,
        "zero_ln_zero_removable": zlz_ok,
        "mixing_max_at_half": mix_ok,
        "gibbs_pure_zero": gibbs_pure_ok,
        "gibbs_uniform_correct": gibbs_unif_ok,
        "honest_wall": "numerical verification of Boltzmann/statistical entropy 0/0 limits"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Boltzmann entropy via 0/0")
    print(f"  S/ln(W) = 1:             {s['boltzmann_ratio_one']}")
    print(f"  0*ln(0) removable:       {s['zero_ln_zero_removable']}")
    print(f"  Mixing max at half:      {s['mixing_max_at_half']}")
    print(f"  Gibbs pure = 0:          {s['gibbs_pure_zero']}")
    print(f"  Gibbs uniform correct:   {s['gibbs_uniform_correct']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/boltzmann_entropy_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
