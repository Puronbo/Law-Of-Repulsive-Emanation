"""
Spectral gap (quantum phase transitions) via 0/0
================================================
The spectral gap: Delta = E_1 - E_0 (difference between first excited
and ground state energies).

At a quantum phase transition: the gap closes (Delta -> 0) in the
thermodynamic limit. The 0/0: Delta(L) * L^z -> C as L -> infinity,
where z is the dynamical critical exponent. At the critical point:
Delta = 0 and L^z = infinity, so the ratio Delta * L^z is 0 * inf = 0/0.
The removable value = C (critical amplitude).

Away from criticality: Delta > 0 and Delta * L^z -> infinity.
At criticality: Delta * L^z -> C (finite constant).

For the transverse-field Ising chain:
  H = -J * sum_i sigma_i^z * sigma_{i+1}^z - h * sum_i sigma_i^x
  Critical point: h/J = 1
  Delta ~ |h/J - 1|^z for |h-J| > 0 (gapped)
  Delta ~ 1/L at criticality (z = 1, C = pi*v where v is the velocity)

The 0/0 at criticality: Delta(L) * L -> C = pi.
Away from criticality: Delta(L) * L -> infinity (gap is O(1), not O(1/L)).

HONEST WALL: exact diagonalization of small spin chains.
"""

import numpy as np
import json
from itertools import product


def build_tfim_hamiltonian(L, h):
    """Build the transverse-field Ising model Hamiltonian.

    H = -J * sum_i sigma_z^i * sigma_z^{i+1} - h * sum_i sigma_x^i
    with periodic boundary conditions.

    Returns a 2^L x 2^L sparse matrix representation.
    """
    N = 2**L
    H = np.zeros((N, N))

    for i in range(N):
        # Apply each term
        for site in range(L):
            # -h * sigma_x term: flips bit at site
            j = i ^ (1 << site)
            H[i, j] -= h

            # -J * sigma_z * sigma_z term: diagonal
            bit_i = (i >> site) & 1
            bit_j = (i >> ((site + 1) % L)) & 1
            if bit_i == bit_j:
                H[i, i] -= 1.0
            else:
                H[i, i] += 1.0

    return H


def get_spectrum(L, h, n_states=5):
    """Get the lowest n_states eigenvalues."""
    H = build_tfim_hamiltonian(L, h)
    eigenvalues = np.linalg.eigvalsh(H)
    return sorted(eigenvalues[:n_states].tolist())


def run():
    results = {"tests": [], "summary": {}}

    # --- Test 1: Spectral gap vs h at fixed L ---
    L = 10
    gap_tests = []
    h_values = np.linspace(0.2, 2.0, 20)

    for h in h_values:
        spectrum = get_spectrum(L, h, n_states=3)
        gap = spectrum[1] - spectrum[0]
        gap_tests.append({
            "h": float(h),
            "gap": float(gap),
            "E0": float(spectrum[0]),
            "E1": float(spectrum[1])
        })

    # Find the minimum gap
    min_gap_idx = min(range(len(gap_tests)), key=lambda i: gap_tests[i]["gap"])
    min_gap_h = gap_tests[min_gap_idx]["h"]

    results["gap_vs_h"] = {
        "note": "Gap closes near h = 1 (critical point) for L = 10",
        "L": L,
        "tests": gap_tests,
        "min_gap_h": float(min_gap_h)
    }

    # --- Test 2: Gap scaling at criticality ---
    # At h = 1: Delta(L) ~ pi*v / L where v = 2 (for J=h=1)
    # So Delta(L) * L -> pi * 2 = 2*pi (approximately)
    scaling_tests = []
    for L_val in [4, 6, 8, 10, 12]:
        spectrum = get_spectrum(L_val, 1.0, n_states=2)
        gap = spectrum[1] - spectrum[0]
        gap_times_L = gap * L_val
        scaling_tests.append({
            "L": L_val,
            "gap": float(gap),
            "gap_times_L": float(gap_times_L),
            "note": "should approach constant as L -> infinity"
        })

    results["critical_scaling"] = {
        "note": "Delta(L)*L -> C at h=1 (critical point); z = 1",
        "tests": scaling_tests
    }

    # --- Test 3: Gap scaling away from criticality ---
    # For h != 1: Delta(L) is O(1), so Delta(L)*L -> infinity
    away_tests = []
    for h_val in [0.5, 1.5]:
        for L_val in [4, 6, 8, 10]:
            spectrum = get_spectrum(L_val, h_val, n_states=2)
            gap = spectrum[1] - spectrum[0]
            gap_times_L = gap * L_val
            away_tests.append({
                "h": float(h_val),
                "L": L_val,
                "gap": float(gap),
                "gap_times_L": float(gap_times_L),
            })

    results["away_from_criticality"] = {
        "note": "Delta(L)*L -> infinity away from h=1 (gapped phase)",
        "tests": away_tests
    }

    # --- Test 4: 0/0 at criticality ---
    # Delta(L) * L^z -> C at criticality. At the thermodynamic limit:
    # Delta -> 0 and L -> infinity. The ratio Delta * L is 0 * inf = 0/0.
    # The removable value = C ~ pi * v ~ 2*pi.
    zero_tests = []
    for L_val in [4, 6, 8, 10, 12]:
        spectrum = get_spectrum(L_val, 1.0, n_states=2)
        gap = spectrum[1] - spectrum[0]
        zero_tests.append({
            "L": L_val,
            "gap": float(gap),
            "gap_times_L": float(gap * L_val),
            "ratio_gap_to_1_L": float(gap / (1.0 / L_val)),
            "removable_value": float(gap * L_val)
        })

    results["zero_over_zero"] = {
        "note": "Delta*inf = 0*inf = 0/0 at criticality; removable ~ C",
        "tests": zero_tests
    }

    # --- Test 5: Energy levels at specific h values ---
    level_tests = []
    L_check = 8
    for h_val in [0.0, 0.5, 1.0, 1.5, 2.0]:
        spectrum = get_spectrum(L_check, h_val, n_states=4)
        level_tests.append({
            "h": float(h_val),
            "spectrum": spectrum,
            "gap": float(spectrum[1] - spectrum[0])
        })

    results["energy_levels"] = {
        "note": "Lowest energy levels for L=8 at various h",
        "tests": level_tests
    }

    # --- Summary ---
    # Critical scaling: gap*L converges at h=1
    if len(scaling_tests) >= 3:
        vals = [t["gap_times_L"] for t in scaling_tests]
        # The values should converge: check that the last 3 are close
        last3 = vals[-3:]
        scaling_converges = max(last3) / min(last3) < 1.2 if min(last3) > 0 else False
    else:
        scaling_converges = False

    # Away from criticality: gap*L should be larger than at criticality for h > 1
    crit_val = scaling_tests[-1]["gap_times_L"] if scaling_tests else 0
    away_vals_h15 = [t["gap_times_L"] for t in away_tests if t["h"] == 1.5]
    away_growing = (len(away_vals_h15) > 0 and away_vals_h15[-1] > crit_val * 5)

    supported = bool(scaling_converges and away_growing)

    results["summary"] = {
        "supported": supported,
        "critical_scaling_converges": scaling_converges,
        "away_from_criticality_grows": away_growing,
        "honest_wall": "exact diagonalization of small chains; finite-size effects"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Spectral gap via 0/0")
    print(f"  Critical scaling:        {s['critical_scaling_converges']}")
    print(f"  Away from criticality:   {s['away_from_criticality_grows']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/spectral_gap_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
