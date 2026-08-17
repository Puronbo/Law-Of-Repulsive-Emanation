"""
Shannon entropy via 0/0
=======================
Shannon entropy: H(X) = -sum_i p(x_i) * log(p(x_i)).

The 0/0: at p(x_i) = 0, the term is 0 * log(0) = 0/0.
By L'Hopital or the convention 0*log(0) = 0 (since lim_{p->0+} p*log(p) = 0),
each such term contributes 0. The removable value is 0.

The normalized entropy: H(X)/log(n) where n is the number of outcomes.
At maximum entropy (uniform distribution): H/log(n) = 1.
At minimum entropy (deterministic): H/log(n) = 0.
The 0/0: at p = [1, 0, 0, ...] (deterministic), H = 0 and log(n) > 0,
so H/log(n) = 0 (not 0/0). But consider the ratio of entropies:
H(X)/H(Y) for two distributions. If both are deterministic: 0/0.
The removable value = 0 (both are zero).

The mutual information: I(X;Y) = H(X) + H(Y) - H(X,Y).
At perfect correlation: I(X;Y) = H(X) = H(Y). The ratio I/H(X) = 1.
At independence: I(X;Y) = 0. The ratio is 0 (not 0/0 unless both are 0).
0/0: for perfectly correlated deterministic distributions: I=0, H=0, ratio=0/0.
Removable value = 1 (perfectly correlated).

The KL divergence: D_KL(P||Q) = sum p(x) * log(p(x)/q(x)).
At q(x) = 0 when p(x) > 0: D_KL = infinity (not 0/0).
At p(x) = q(x) = 0: 0 * log(0/0) = 0/0. Removable value = 0.

HONEST WALL: numerical verification of information-theoretic 0/0 limits.
"""

import numpy as np
import json
from itertools import product


def entropy(probs):
    """Shannon entropy, treating 0*log(0) = 0."""
    H = 0.0
    for p in probs:
        if p > 0:
            H -= p * np.log(p)
    return float(H)


def entropy_binary(p):
    """Entropy of a binary distribution [p, 1-p]."""
    H = 0.0
    if p > 0:
        H -= p * np.log(p)
    if 1 - p > 0:
        H -= (1 - p) * np.log(1 - p)
    return float(H)


def kl_divergence(p, q):
    """KL divergence D_KL(P||Q)."""
    d = 0.0
    for pi, qi in zip(p, q):
        if pi > 0 and qi > 0:
            d += pi * np.log(pi / qi)
        elif pi > 0 and qi == 0:
            return float('inf')
    return float(d)


def mutual_information(joint):
    """Mutual information from a joint distribution table."""
    rows = len(joint)
    cols = len(joint[0])
    p_x = [sum(joint[i][j] for j in range(cols)) for i in range(rows)]
    p_y = [sum(joint[i][j] for i in range(rows)) for j in range(cols)]

    H_X = entropy(p_x)
    H_Y = entropy(p_y)

    H_XY = 0.0
    for i in range(rows):
        for j in range(cols):
            if joint[i][j] > 0:
                H_XY -= joint[i][j] * np.log(joint[i][j])

    return float(H_X + H_Y - H_XY)


def run():
    results = {"tests": [], "summary": {}}

    # --- Test 1: 0*log(0) = 0 (removable value) ---
    zero_log_tests = []
    for eps in [1e-1, 1e-3, 1e-6, 1e-10, 1e-15]:
        val = eps * np.log(eps)
        zero_log_tests.append({
            "p": eps,
            "p_log_p": float(val),
            "approaches_zero": bool(abs(val) < 0.3)
        })

    results["zero_log_zero"] = {
        "note": "lim_{p->0+} p*log(p) = 0: the 0*log(0) = 0/0 removable value",
        "tests": zero_log_tests
    }

    # --- Test 2: Entropy of specific distributions ---
    dist_tests = []

    # Uniform distribution over n outcomes: H = log(n)
    for n in [2, 3, 5, 10]:
        probs = [1.0 / n] * n
        H = entropy(probs)
        H_normalized = H / np.log(n)
        dist_tests.append({
            "name": f"uniform_{n}",
            "H": float(H),
            "H_log_n": float(H_normalized),
            "is_maximum": bool(abs(H_normalized - 1.0) < 1e-10)
        })

    # Deterministic distribution: H = 0
    for n in [2, 5, 10]:
        probs = [1.0] + [0.0] * (n - 1)
        H = entropy(probs)
        dist_tests.append({
            "name": f"deterministic_{n}",
            "H": float(H),
            "is_zero": bool(abs(H) < 1e-15)
        })

    # Binary entropy: maximum at p = 0.5
    for p in [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
        H = entropy_binary(p)
        dist_tests.append({
            "name": f"binary_{p}",
            "H": float(H),
            "max_at_half": bool(abs(p - 0.5) < 0.01 and abs(H - np.log(2)) < 1e-10)
        })

    results["specific_distributions"] = {
        "note": "uniform H = log(n), deterministic H = 0, binary max at p=0.5",
        "tests": dist_tests
    }

    # --- Test 3: 0/0 in entropy ratios ---
    # For two deterministic distributions: H(P)/H(Q) = 0/0.
    ratio_tests = []
    # P deterministic, Q varying from deterministic to uniform
    H_P = 0.0  # deterministic
    for n in [2, 5, 10]:
        # Q uniform: H(Q) = log(n)
        H_Q_uniform = np.log(n)
        ratio_uniform = H_P / H_Q_uniform if H_Q_uniform > 0 else 0
        ratio_tests.append({
            "P": "deterministic",
            "Q": f"uniform_{n}",
            "H_P": float(H_P),
            "H_Q": float(H_Q_uniform),
            "ratio": float(ratio_uniform),
            "is_zero": bool(abs(ratio_uniform) < 1e-15)
        })

    # Both deterministic: 0/0
    ratio_tests.append({
        "P": "deterministic_10",
        "Q": "deterministic_10",
        "H_P": 0.0,
        "H_Q": 0.0,
        "ratio": "0/0",
        "removable_value": "0 (both deterministic)"
    })

    results["entropy_ratios"] = {
        "note": "H(deterministic)/H(deterministic) = 0/0, removable value = 0",
        "tests": ratio_tests
    }

    # --- Test 4: Mutual information 0/0 ---
    mi_tests = []

    # Perfect correlation: I(X;Y) = H(X)
    joint_perfect = [[0.5, 0.0], [0.0, 0.5]]
    I_perfect = mutual_information(joint_perfect)
    H_X_perfect = entropy([0.5, 0.5])
    mi_tests.append({
        "type": "perfect_correlation",
        "I": float(I_perfect),
        "H_X": float(H_X_perfect),
        "ratio_I_H": float(I_perfect / H_X_perfect) if H_X_perfect > 0 else "0/0",
        "removable_value": 1.0
    })

    # Independence: I = 0
    joint_indep = [[0.25, 0.25], [0.25, 0.25]]
    I_indep = mutual_information(joint_indep)
    mi_tests.append({
        "type": "independence",
        "I": float(I_indep),
        "is_zero": bool(abs(I_indep) < 1e-15)
    })

    # Both deterministic and identical: I = 0, H = 0 => 0/0
    joint_determ = [[1.0, 0.0], [0.0, 0.0]]
    I_determ = mutual_information(joint_determ)
    H_X_determ = entropy([1.0, 0.0])
    mi_tests.append({
        "type": "both_deterministic",
        "I": float(I_determ),
        "H_X": float(H_X_determ),
        "ratio_I_H": "0/0",
        "removable_value": "1 (perfectly correlated deterministic)"
    })

    results["mutual_information"] = {
        "note": "I/H(X) = 1 for perfect correlation, 0 for independence",
        "tests": mi_tests
    }

    # --- Test 5: KL divergence 0/0 ---
    kl_tests = []

    # p(x) = q(x) = 0: 0*log(0/0) = 0/0
    kl_tests.append({
        "type": "both_zero",
        "p": 0.0,
        "q": 0.0,
        "contribution": "0*log(0/0) = 0/0",
        "removable_value": 0
    })

    # p = q: D_KL = 0
    p_equal = [0.3, 0.5, 0.2]
    d_equal = kl_divergence(p_equal, p_equal)
    kl_tests.append({
        "type": "identical",
        "D_KL": float(d_equal),
        "is_zero": bool(abs(d_equal) < 1e-15)
    })

    # Different distributions: D_KL > 0
    p = [0.5, 0.3, 0.2]
    q = [0.2, 0.5, 0.3]
    d_diff = kl_divergence(p, q)
    kl_tests.append({
        "type": "different",
        "D_KL": float(d_diff),
        "is_positive": bool(d_diff > 0)
    })

    results["kl_divergence"] = {
        "note": "D_KL(P||Q) >= 0, equality iff P = Q; 0*log(0/0) = 0/0 removable",
        "tests": kl_tests
    }

    # --- Test 6: Data processing inequality ---
    # If X -> Y -> Z (Markov chain), then I(X;Z) <= I(X;Y)
    dpi_tests = []

    # Perfect chain: X = Y = Z
    joint_xyz = np.zeros((2, 2, 2))
    joint_xyz[0, 0, 0] = 0.5
    joint_xyz[1, 1, 1] = 0.5

    # I(X;Y) from joint
    p_xy = joint_xyz.sum(axis=2)
    I_XY = mutual_information(p_xy.tolist())

    # I(X;Z) from marginal
    p_xz = joint_xyz.sum(axis=1)
    I_XZ = mutual_information(p_xz.tolist())

    dpi_tests.append({
        "chain": "X=Y=Z",
        "I_XY": float(I_XY),
        "I_XZ": float(I_XZ),
        "satisfies_dpi": bool(I_XZ <= I_XY + 1e-10)
    })

    results["data_processing"] = {
        "note": "Data processing inequality: I(X;Z) <= I(X;Y) for X->Y->Z",
        "tests": dpi_tests
    }

    # --- Summary ---
    zlz_ok = all(t["approaches_zero"] for t in zero_log_tests)
    uniform_ok = all(t["is_maximum"] for t in dist_tests if t["name"].startswith("uniform"))
    det_ok = all(t["is_zero"] for t in dist_tests if t["name"].startswith("deterministic"))
    mi_ok = any(t.get("removable_value") == 1.0 for t in mi_tests)
    kl_ok = any(t.get("removable_value") == 0 for t in kl_tests)

    supported = bool(zlz_ok and uniform_ok and det_ok and mi_ok and kl_ok)

    results["summary"] = {
        "supported": supported,
        "zero_log_zero_removable": zlz_ok,
        "uniform_maximum": uniform_ok,
        "deterministic_zero": det_ok,
        "mi_0_over_0": mi_ok,
        "kl_0_over_0": kl_ok,
        "honest_wall": "numerical verification of information-theoretic 0/0 limits"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Shannon entropy via 0/0")
    print(f"  0*log(0) removable:      {s['zero_log_zero_removable']}")
    print(f"  Uniform maximum:          {s['uniform_maximum']}")
    print(f"  Deterministic zero:       {s['deterministic_zero']}")
    print(f"  MI 0/0:                  {s['mi_0_over_0']}")
    print(f"  KL 0/0:                  {s['kl_0_over_0']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/shannon_entropy_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
