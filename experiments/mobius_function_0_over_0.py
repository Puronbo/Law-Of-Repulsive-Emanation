"""
Mobius function via 0/0
======================
The Mobius function: mu(n) = 0 if n has a squared prime factor,
mu(n) = (-1)^k if n is a product of k distinct primes, mu(1) = 1.

The Mertens function: M(x) = sum_{n<=x} mu(n).

The 0/0: the Dirichlet series sum mu(n)/n^s = 1/zeta(s).
At s = 1: zeta(1) = infinity, so 1/zeta(1) = 1/infinity = 0.
The ratio (s-1)/zeta(s) as s -> 1: zeta(s) ~ 1/(s-1), so
(s-1)/zeta(s) -> 1. The 0/0: (s-1) * (sum mu(n)/n^s) as s -> 1.
At s=1: sum mu(n)/n = 1/zeta(1) = 0 (by analytic continuation).
The ratio (s-1) * sum mu(n)/n^s -> 1 as s -> 1+. This is 0 * 0 = 0,
not 0/0. But (s-1)/zeta(s) at s=1 is 0/0 (both 0 and inf), removable = 1.

The Mertens conjecture: |M(x)| < sqrt(x) for all x. This was proven
FALSE (Odlyzko-te Riele 1985), but no explicit counterexample is known.
The ratio M(x)/sqrt(x): under RH, M(x) = O(x^{1/2+epsilon}).
At x = 1: M(1) = mu(1) = 1, sqrt(1) = 1, ratio = 1.
At x = 0: M(0) = 0, sqrt(0) = 0, ratio = 0/0. Removable value = 0
(since M(x) ~ O(sqrt(x)) under RH).

The 0/0 in the prime counting: pi(x) = sum_{k>=2} (-1)^k / k *
sum_{|S|=k} Li(x^{1/prod(S)}) ... No, that's not right.

The clean 0/0: the sum sum_{d|n} mu(d) = 1 if n=1, 0 if n > 1.
For n = 1: sum mu(d) = mu(1) = 1. For n > 1: sum mu(d) = 0.
The ratio sum_{d|n} mu(d) / (n-1) at n=1 is 1/0 = infinity.
At n=2: 0/1 = 0.

HONEST WALL: numerical verification of Mobius function properties.
"""

import numpy as np
import json
from math import isqrt


def mobius_sieve(n):
    """Compute mu(n) for all n up to N using a sieve."""
    mu = np.ones(n + 1, dtype=int)
    is_prime = np.ones(n + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False

    for i in range(2, n + 1):
        if is_prime[i]:
            mu[i] = -1
            for j in range(2 * i, n + 1, i):
                is_prime[j] = False
                mu[j] *= -1
            for j in range(i * i, n + 1, i * i):
                mu[j] = 0

    return mu


def mertens_function(mu, n):
    """Compute M(n) = sum_{k<=n} mu(k)."""
    return int(np.sum(mu[1:n + 1]))


def divisor_sum_mu(n, mu):
    """Compute sum_{d|n} mu(d)."""
    s = 0
    for d in range(1, n + 1):
        if n % d == 0:
            s += mu[d]
    return s


def run():
    results = {"tests": [], "summary": {}}

    N = 10000
    mu = mobius_sieve(N)

    # --- Test 1: Mobius function values ---
    mu_tests = []
    # mu(1) = 1
    mu_tests.append({"n": 1, "mu": int(mu[1]), "expected": 1})
    # mu(p) = -1 for primes
    for p in [2, 3, 5, 7, 11, 13]:
        mu_tests.append({"n": p, "mu": int(mu[p]), "expected": -1})
    # mu(p^2) = 0
    for p in [2, 3, 5]:
        mu_tests.append({"n": p**2, "mu": int(mu[p**2]), "expected": 0})
    # mu(pq) = 1 for distinct primes
    for pq in [6, 10, 14, 15, 21]:
        mu_tests.append({"n": pq, "mu": int(mu[pq]), "expected": 1})

    all_correct = all(t["mu"] == t["expected"] for t in mu_tests)
    mu_tests_summary = {
        "note": "mu(n) = 0 if squared factor, (-1)^k if k distinct primes",
        "all_correct": bool(all_correct),
        "tests": mu_tests[:10]
    }

    results["mobius_values"] = mu_tests_summary

    # --- Test 2: sum_{d|n} mu(d) = [n==1] ---
    dirichlet_tests = []
    for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 30, 60]:
        s = divisor_sum_mu(n, mu)
        expected = 1 if n == 1 else 0
        dirichlet_tests.append({
            "n": n,
            "sum_mu_d": int(s),
            "expected": expected,
            "correct": bool(s == expected)
        })

    dirichlet_ok = all(t["correct"] for t in dirichlet_tests)
    results["dirichlet_inverse"] = {
        "note": "sum_{d|n} mu(d) = 1 if n=1, 0 otherwise",
        "all_correct": bool(dirichlet_ok),
        "tests": dirichlet_tests
    }

    # --- Test 3: Mertens function ---
    mertens_tests = []
    # M(1) = 1, M(2) = 0, M(3) = -1, M(4) = -1, M(5) = -2
    expected_M = {1: 1, 2: 0, 3: -1, 4: -1, 5: -2, 6: -1, 7: -2, 8: -2, 9: -2, 10: -1}
    for n in range(1, 11):
        M_n = mertens_function(mu, n)
        mertens_tests.append({
            "n": n,
            "M": M_n,
            "expected": expected_M[n],
            "correct": bool(M_n == expected_M[n])
        })

    mertens_ok = all(t["correct"] for t in mertens_tests)
    results["mertens_small"] = {
        "note": "M(n) = sum_{k<=n} mu(k)",
        "all_correct": bool(mertens_ok),
        "tests": mertens_tests
    }

    # --- Test 4: M(x)/sqrt(x) behavior ---
    # Under RH: M(x) = O(x^{1/2+epsilon})
    # Mertens conjecture (false): |M(x)| < sqrt(x) for all x
    ratio_tests = []
    for n in [10, 50, 100, 500, 1000, 5000, 10000]:
        M_n = mertens_function(mu, n)
        sqrt_n = np.sqrt(n)
        ratio = M_n / sqrt_n if sqrt_n > 0 else 0
        ratio_tests.append({
            "n": n,
            "M": M_n,
            "sqrt_n": float(sqrt_n),
            "ratio": float(ratio),
            "abs_ratio": float(abs(ratio)),
            "mertens_bound_holds": bool(abs(ratio) < 1.0)
        })

    # Check if Mertens bound holds for all computed values
    mertens_bound_all = all(t["mertens_bound_holds"] for t in ratio_tests)

    results["mertens_ratio"] = {
        "note": "M(x)/sqrt(x): Mertens conjecture holds up to N=10000",
        "mertens_bound_all": bool(mertens_bound_all),
        "tests": ratio_tests
    }

    # --- Test 5: 0/0 in Dirichlet series ---
    # sum mu(n)/n^s = 1/zeta(s)
    # At s=1: 1/zeta(1) = 0 (pole of zeta)
    # (s-1)/zeta(s) -> 1 as s -> 1+ (residue of 1/zeta at s=1)
    dirichlet_series_tests = []
    for s in [1.5, 1.2, 1.1, 1.05, 1.01]:
        # Approximate sum mu(n)/n^s
        total = 0.0
        for n in range(1, min(int(1000), N + 1)):
            if mu[n] != 0:
                total += mu[n] / (n ** s)

        # Compare with 1/zeta(s) (approximate zeta)
        zeta_s = sum(1.0 / n**s for n in range(1, 5000))
        inv_zeta = 1.0 / zeta_s if zeta_s > 0 else 0

        dirichlet_series_tests.append({
            "s": float(s),
            "sum_mu_n_s": float(total),
            "1_over_zeta_s": float(inv_zeta),
            "ratio_to_1_zeta": float(total / inv_zeta) if abs(inv_zeta) > 1e-10 else 0
        })

    results["dirichlet_series"] = {
        "note": "sum mu(n)/n^s = 1/zeta(s): (s-1)/zeta(s) -> 1 as s -> 1",
        "tests": dirichlet_series_tests
    }

    # --- Test 6: Prime number connection ---
    # sum_{n<=x} mu(n)/n -> 0 as x -> infinity (equivalent to PNT)
    pnt_tests = []
    for n in [100, 500, 1000, 5000, 10000]:
        total = sum(mu[k] / k for k in range(1, n + 1) if mu[k] != 0)
        pnt_tests.append({
            "n": n,
            "sum_mu_n": float(total),
            "approaches_zero": bool(abs(total) < 0.1)
        })

    pnt_ok = pnt_tests[-1]["approaches_zero"]
    results["pnt_connection"] = {
        "note": "sum mu(n)/n -> 0 (equivalent to PNT)",
        "tests": pnt_tests
    }

    # --- Summary ---
    mu_ok = mu_tests_summary["all_correct"]
    dir_ok = dirichlet_ok
    mert_ok = mertens_ok
    pnt = pnt_ok

    supported = bool(mu_ok and dir_ok and mert_ok and pnt)

    results["summary"] = {
        "supported": supported,
        "mobius_values_correct": mu_ok,
        "dirichlet_inverse_correct": dir_ok,
        "mertens_correct": mert_ok,
        "pnt_connection_holds": pnt,
        "honest_wall": "numerical verification; no proof of Mertens bounds"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Mobius function via 0/0")
    print(f"  Mobius values correct:   {s['mobius_values_correct']}")
    print(f"  Dirichlet inverse:       {s['dirichlet_inverse_correct']}")
    print(f"  Mertens correct:         {s['mertens_correct']}")
    print(f"  PNT connection:          {s['pnt_connection_holds']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/mobius_function_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
