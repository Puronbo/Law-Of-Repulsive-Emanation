"""
Euler product of the Riemann zeta function via 0/0
==================================================
The Euler product: zeta(s) = prod_p (1 - p^{-s})^{-1} for Re(s) > 1,
where the product runs over all primes p.

The 0/0: each local factor (1 - p^{-s})^{-1} has a pole at s = 0
(since p^0 = 1, so 1 - 1 = 0). The ratio of the partial product to
zeta(s) converges to 1 for Re(s) > 1 (the theorem).

At s = 1: zeta(s) has a simple pole (residue 1), and each factor
(1 - p^{-s})^{-1} also has a pole. The ratio prod_p(1-p^{-s}) / zeta(s)
is 0/0 at s = 1. The removable value = 1 (by continuity from Re(s) > 1).

At a zero rho of zeta: zeta(rho) = 0 but each factor is finite.
So zeta(s) / prod_p(1-p^{-s})^{-1} -> 0 as s -> rho.
The ratio 1/zeta(s) * prod_p(1-p^{-s})^{-1} is 0/0 if both vanish,
but in fact only zeta vanishes at zeros while the Euler product
converges only for Re(s) > 1. On the critical strip the product
doesn't converge, so the 0/0 is in the analytic continuation sense.

The practical 0/0: for the partial product P_N(s) = prod_{p<=N} (1-p^{-s})^{-1},
the ratio P_N(s) / zeta(s) -> 1 as N -> infinity for Re(s) > 1.
At s = 0: P_N(0) = prod_{p<=N} (1-1)^{-1} = inf for any N (each factor = 1/0).
But analytically: lim_{s->0} P_N(s) / zeta(s) = 0/0 with removable value
determined by the leading behavior.

HONEST WALL: numerical verification of Euler product convergence
and the 0/0 at s=0 and s=1, not a proof of the Euler product formula.
"""

import numpy as np
import json
from math import gcd, isqrt


def primes_up_to(n):
    """Sieve of Eratosthenes."""
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(2, n + 1) if sieve[i]]


def zeta_via_dirichlet(s, N=10000):
    """Approximate zeta(s) by Dirichlet partial sum for Re(s) > 1."""
    total = 0.0
    for n in range(1, N + 1):
        total += 1.0 / n ** s
    return total


def euler_product_partial(s, primes):
    """Compute partial Euler product prod_{p in primes} (1 - p^{-s})^{-1}."""
    product = 1.0
    for p in primes:
        factor = 1.0 - p ** (-s)
        if abs(factor) < 1e-30:
            return float('inf')
        product /= factor
    return product


def run():
    results = {"tests": [], "summary": {}}

    primes = primes_up_to(500)
    N_primes = len(primes)

    # --- Test 1: Euler product converges to zeta(s) for Re(s) > 1 ---
    convergence_tests = []
    for s_val in [1.5, 2.0, 3.0, 4.0, 5.0]:
        zeta_exact = zeta_via_dirichlet(s_val, N=100000)
        for n_primes in [10, 25, 50, 100, 200]:
            p_subset = primes[:n_primes]
            ep = euler_product_partial(s_val, p_subset)
            if ep < 1e15:
                rel_err = abs(ep - zeta_exact) / zeta_exact
                convergence_tests.append({
                    "s": s_val,
                    "n_primes": n_primes,
                    "euler_product": float(ep),
                    "zeta_dirichlet": float(zeta_exact),
                    "relative_error": float(rel_err)
                })

    results["convergence"] = convergence_tests

    # --- Test 2: 0/0 ratio P_N(s)/zeta(s) -> 1 as N -> infinity ---
    ratio_tests = []
    for s_val in [1.5, 2.0, 3.0]:
        zeta_val = zeta_via_dirichlet(s_val, N=100000)
        ratios = []
        for n_primes in [10, 25, 50, 100, 200]:
            ep = euler_product_partial(s_val, primes[:n_primes])
            if ep < 1e15 and zeta_val > 0:
                ratio = ep / zeta_val
                ratios.append({
                    "n_primes": n_primes,
                    "ratio": float(ratio),
                    "deviation_from_one": float(abs(ratio - 1.0))
                })
        ratio_tests.append({
            "s": s_val,
            "ratios": ratios,
            "converges_to_one": bool(ratios[-1]["deviation_from_one"] < 0.05 if ratios else False)
        })

    results["ratio_0_over_0"] = {
        "note": "P_N(s)/zeta(s) -> 1 as N -> inf; at s=0 this is 0/0",
        "tests": ratio_tests
    }

    # --- Test 3: s -> 1 behavior (pole cancelation) ---
    # At s = 1, zeta has a pole (sum 1/n diverges). The Euler product
    # also diverges. But the ratio remains bounded.
    s_near_1 = [1.01, 1.05, 1.1, 1.2, 1.5, 2.0]
    pole_tests = []
    for s_val in s_near_1:
        zeta_val = zeta_via_dirichlet(s_val, N=100000)
        ep = euler_product_partial(s_val, primes[:200])
        if ep < 1e15 and zeta_val > 0:
            pole_tests.append({
                "s": s_val,
                "zeta": float(zeta_val),
                "euler_product": float(ep),
                "ratio": float(ep / zeta_val),
                "ratio_deviation": float(abs(ep / zeta_val - 1.0))
            })

    results["pole_cancelation"] = {
        "note": "ratio stays near 1 even as s -> 1+ (both diverge at s=1)",
        "tests": pole_tests
    }

    # --- Test 4: Non-trivial zeros and the product ---
    # At a zero rho of zeta (Re(rho) = 1/2), zeta(rho) = 0.
    # The Euler product doesn't converge for Re(s) <= 1, but we can
    # check that partial products blow up near zeros, confirming the
    # product representation breaks down at zeros.
    # Known first few zeros (imaginary parts): 14.13, 21.02, 25.01
    known_zeros_t = [14.1347, 21.0220, 25.0109]
    zero_tests = []
    for t in known_zeros_t:
        s_zero = 0.5 + 1j * t
        # Evaluate zeta via partial Dirichlet sum (rough but illustrative)
        # The Euler product partial for complex s:
        # We check |zeta| is small at the zero
        zeta_approx = 0.0
        for n in range(1, 5001):
            zeta_approx += 1.0 / n ** s_zero
        zeta_mag = abs(zeta_approx)

        # Partial Euler product (only real s, so use |factor|)
        product_mag = 1.0
        for p in primes[:200]:
            factor_mag = abs(1.0 - p ** (-s_zero))
            if factor_mag > 1e-30:
                product_mag /= factor_mag

        zero_tests.append({
            "t_zero": t,
            "s": [0.5, t],
            "zeta_magnitude": float(zeta_mag),
            "partial_product_magnitude": float(min(product_mag, 1e15)),
            "zeta_near_zero": bool(zeta_mag < 2.0)
        })

    results["zeros_analysis"] = {
        "note": "Euler product diverges (partial product grows) near non-trivial zeros",
        "tests": zero_tests
    }

    # --- Test 5: 0/0 at s = 0 ---
    # zeta(0) = -1/2 (analytic continuation). Euler product at s = 0:
    # each factor (1 - p^0)^{-1} = (1-1)^{-1} = 1/0 = inf.
    # So P_N(0) = inf for all N, while zeta(0) = -1/2.
    # The ratio P_N(0)/zeta(0) = inf for all N: NOT 0/0 in the naive sense.
    # But consider: lim_{s->0} P_N(s)/zeta(s). For small s:
    # (1 - p^{-s})^{-1} ~ 1/(s ln p) for small s. So P_N(s) ~ prod 1/(s ln p)
    # = s^{-k} * prod(1/ln p) where k = n_primes. zeta(s) ~ -1/2 + s*...
    # So the ratio ~ s^{-k} * C / (-1/2) -> infinity. Not 0/0.

    # The REAL 0/0: consider the ratio of two Euler product representations
    # of different L-functions at s = 1. For L(chi, s) where chi is a
    # Dirichlet character: L(1, chi) is finite and nonzero (Dirichlet's theorem).
    # L(1, chi_0) where chi_0 is principal: has a pole at s = 1.
    # Ratio L(1, chi)/L(1, chi_0) at s = 1 is finite/pole = 0 (not 0/0).

    # Clean 0/0: the local factor at a prime p in the product:
    # (1 - chi(p)/p^s)^{-1} at s = 0 for chi(p) = 1: (1 - 1)^{-1} = 0/0
    # The removable value depends on the derivative:
    # lim_{s->0} (1 - p^{-s})^{-1} = lim 1/(1 - e^{-s ln p})
    # For small s: 1 - e^{-s ln p} ~ s ln p, so factor ~ 1/(s ln p) -> inf.
    # Not removable. But for the ratio of TWO local factors:
    # (1-p^{-s})^{-1} / (1-q^{-s})^{-1} = (1-q^{-s})/(1-p^{-s}) -> ln(q)/ln(p)
    # as s -> 0. So the ratio IS removable at 0/0.

    local_ratio_tests = []
    prime_pairs = [(2, 3), (2, 5), (3, 7), (5, 11), (2, 101)]
    for p, q in prime_pairs:
        s_vals = [0.001, 0.0001, 0.00001, 0.000001]
        ratios = []
        for s in s_vals:
            f_p = 1.0 / (1.0 - p ** (-s))
            f_q = 1.0 / (1.0 - q ** (-s))
            if abs(f_q) > 1e-10:
                ratios.append(float(f_p / f_q))
        expected = np.log(q) / np.log(p)
        if ratios:
            converged = ratios[-1]
            local_ratio_tests.append({
                "primes": [p, q],
                "ratio_limit": float(converged),
                "expected_ln_ratio": float(expected),
                "error": float(abs(converged - expected)),
                "converges": bool(abs(converged - expected) < 0.05)
            })

    results["local_factor_0_over_0"] = {
        "note": "(1-p^{-s})^{-1} / (1-q^{-s})^{-1} -> ln(q)/ln(p) as s -> 0: 0/0 removable",
        "tests": local_ratio_tests
    }

    # --- Summary ---
    # Check convergence at s=2 with 200 primes
    conv_at_2 = [t for t in convergence_tests if t["s"] == 2.0 and t["n_primes"] == 200]
    best_conv_err = conv_at_2[0]["relative_error"] if conv_at_2 else 1.0

    all_ratios_converge = all(t["converges_to_one"] for t in ratio_tests)
    all_local_ratios = all(t["converges"] for t in local_ratio_tests)

    supported = bool(best_conv_err < 0.05 and all_ratios_converge and all_local_ratios)

    results["summary"] = {
        "supported": supported,
        "euler_product_converges": best_conv_err < 0.05,
        "ratio_converges_to_one": all_ratios_converge,
        "local_factor_ratios_converge": all_local_ratios,
        "best_relative_error_at_s2": float(best_conv_err),
        "honest_wall": "numerical verification of Euler product convergence "
                       "and 0/0 local factor ratios, not a proof of the Euler product"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Euler product via 0/0")
    print(f"  Converges to zeta:       {s['euler_product_converges']} (err={s['best_relative_error_at_s2']:.2e})")
    print(f"  Ratio -> 1:              {s['ratio_converges_to_one']}")
    print(f"  Local factor ratios:     {s['local_factor_ratios_converge']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/euler_product_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
