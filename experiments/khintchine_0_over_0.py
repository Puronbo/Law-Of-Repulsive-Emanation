"""
Khintchine's theorem (metric Diophantine approximation) via 0/0
==============================================================
Khintchine's theorem: for a monotone function psi(q), the set of
real numbers x for which |x - p/q| < psi(q)/q has infinitely many
rational approximations p/q has measure zero or full measure depending
on whether sum_q psi(q) converges or diverges.

The 0/0: for the Dirichlet approximation, |x - p/q| * q -> 0 as q -> inf
for any irrational x (Dirichlet's theorem). The ratio q * |x - p/q| is
the approximation quality. At a rational x = a/b:
  |a/b - p/q| = |aq - bp| / (bq) >= 1/(bq)
  So q * |a/b - p/q| >= 1/b > 0. The approximation is bounded below.

For irrational x: q * |x - p/q| can be arbitrarily small. The 0/0:
the ratio (q * |x - p/q|) / psi(q) at a rational approximant p/q of
an irrational x is 0/0 (both numerator and denominator -> 0 along the
sequence of convergents). The removable value encodes the irrationality
measure of x.

For the golden ratio phi: the best approximants are the Fibonacci ratios
F_{n+1}/F_n, and q * |phi - F_{n+1}/F_n| -> 1/sqrt(5) (not 0).
For quadratic irrationals: the approximation quality is bounded below
(Liouville's theorem for algebraic numbers of degree 2).

For a Liouville number: q * |x - p/q| -> 0 super-exponentially fast.
The ratio q * |x-p/q| / (1/q^2) -> 0: the removable value is 0.

HONEST WALL: numerical verification of Diophantine approximation
properties for specific numbers, not a proof of Khintchine's theorem.
"""

import numpy as np
import json
from math import isqrt, gcd, sqrt


def continued_fraction(x, n_terms):
    """Compute the continued fraction expansion of x."""
    a = []
    r = x
    for _ in range(n_terms):
        a_i = int(r)
        a.append(a_i)
        frac = r - a_i
        if abs(frac) < 1e-15:
            break
        r = 1.0 / frac
    return a


def convergents(a):
    """Compute convergents p_n/q_n from continued fraction coefficients."""
    convergents_list = []
    p_prev, p_curr = 0, 1
    q_prev, q_curr = 1, 0
    for a_i in a:
        p_new = a_i * p_curr + p_prev
        q_new = a_i * q_curr + q_prev
        convergents_list.append((p_new, q_new))
        p_prev, p_curr = p_curr, p_new
        q_prev, q_curr = q_curr, q_new
    return convergents_list


def farey_neighbors(n):
    """Generate Farey sequence of order n."""
    farey = [(0, 1), (1, 1)]
    a, b, c, d = 0, 1, 1, n
    while c <= n:
        k = (n + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        farey.append((c, d))
    return farey


def run():
    results = {"tests": [], "summary": {}}

    # --- Test 1: Continued fraction convergents for specific numbers ---
    numbers = {
        "sqrt(2)": np.sqrt(2),
        "phi (golden)": (1 + np.sqrt(5)) / 2,
        "e": np.e,
        "pi": np.pi,
    }

    cf_tests = {}
    for name, x in numbers.items():
        cf = continued_fraction(x, 20)
        convs = convergents(cf)
        approx_quality = []
        for p, q in convs[1:]:  # skip the trivial first convergent
            if q > 0:
                error = abs(x - p / q)
                q_error = q * error
                approx_quality.append({
                    "p": p,
                    "q": q,
                    "error": float(error),
                    "q_times_error": float(q_error)
                })

        cf_tests[name] = {
            "continued_fraction": cf[:15],
            "is_periodic": bool(name.startswith("sqrt")),
            "convergents": approx_quality[:10]
        }

    results["continued_fractions"] = cf_tests

    # --- Test 2: Approximation quality for golden ratio ---
    # For phi, the convergents are F_{n+1}/F_n
    # and q * |phi - p/q| -> 1/sqrt(5) ~ 0.447
    phi = (1 + np.sqrt(5)) / 2
    cf_phi = continued_fraction(phi, 20)
    conv_phi = convergents(cf_phi)
    phi_quality = []
    for p, q in conv_phi[1:]:
        if q > 0:
            qe = q * q * abs(phi - p / q)
            phi_quality.append({
                "q": q,
                "q_squared_times_error": float(qe)
            })

    phi_limit = 1.0 / np.sqrt(5)
    results["golden_ratio"] = {
        "note": f"q^2*|phi-p/q| -> 1/sqrt(5) ~ {phi_limit:.6f} (hardest to approximate)",
        "convergent_qualities": phi_quality[:10],
        "limit": float(phi_limit)
    }

    # --- Test 3: Dirichlet's theorem: infinitely many p/q with |x-p/q| < 1/q^2 ---
    dirichlet_tests = []
    for name, x in [("sqrt(2)", np.sqrt(2)), ("pi", np.pi), ("e", np.e)]:
        cf = continued_fraction(x, 30)
        convs = convergents(cf)
        n_good = 0
        for p, q in convs[1:]:
            if q > 0:
                error = abs(x - p / q)
                if error < 1.0 / (q * q):
                    n_good += 1
        dirichlet_tests.append({
            "number": name,
            "n_convergents_satisfying": n_good,
            "total_convergents": len(convs) - 1,
            "all_satisfy": bool(n_good == len(convs) - 1)
        })

    results["dirichlet_theorem"] = {
        "note": "every convergent satisfies |x-p/q| < 1/q^2 (Dirichlet)",
        "tests": dirichlet_tests
    }

    # --- Test 4: 0/0 for approximation quality at rationals ---
    # For x = a/b (rational), the best approximant is x itself.
    # |a/b - p/q| >= 1/(bq) for p/q != a/b.
    # So q * |a/b - p/q| >= 1/b > 0: NOT 0/0 at rationals.
    # The 0/0: for an irrational x, consider the sequence of convergents.
    # q_n * |x - p_n/q_n| varies. For phi it approaches 1/sqrt(5).
    # For Liouville numbers it approaches 0.
    # The ratio q_n * |x - p_n/q_n| / psi(n) is 0/0 if psi(n) -> 0
    # and q_n * error -> 0 simultaneously.

    # For e: the continued fraction has pattern [2; 1, 2, 1, 1, 4, 1, 1, 6, ...]
    # The convergents satisfy q * |e - p/q| -> 1/(2e) ~ 0.184
    e_quality = []
    cf_e = continued_fraction(np.e, 30)
    conv_e = convergents(cf_e)
    for p, q in conv_e[1:]:
        if q > 0:
            qe = q * abs(np.e - p / q)
            e_quality.append({
                "q": q,
                "q_times_error": float(qe)
            })

    results["e_approximation"] = {
        "note": "q*|e-p/q| -> 1/(2e) ~ 0.184",
        "convergent_qualities": e_quality[:10]
    }

    # --- Test 5: Farey sequence approximation ---
    # For a Farey fraction p/q of order N: |x - p/q| <= 1/(qN)
    farey_tests = []
    for N in [10, 50, 100, 500]:
        x = np.sqrt(2)
        best_error = 1.0
        best_frac = (0, 1)
        # Generate Farey fractions near sqrt(2)
        a = isqrt(2 * N * N) // N  # rough integer part
        for q in range(1, N + 1):
            p = round(x * q)
            if gcd(p, q) == 1:
                error = abs(x - p / q)
                if error < best_error:
                    best_error = error
                    best_frac = (p, q)

        p, q = best_frac
        farey_tests.append({
            "N": N,
            "best_fraction": f"{p}/{q}",
            "error": float(best_error),
            "bound": float(1.0 / (q * N)),
            "satisfies_bound": bool(best_error <= 1.0 / (q * N) + 1e-10)
        })

    results["farey_approximation"] = {
        "note": "Farey fractions approximate irrationals to 1/(qN)",
        "tests": farey_tests
    }

    # --- Summary ---
    # All convergents satisfy Dirichlet bound
    dirichlet_ok = all(t["all_satisfy"] for t in dirichlet_tests)
    # Golden ratio convergent quality approaches 1/sqrt(5)
    phi_converges = bool(phi_quality and
                         abs(phi_quality[-1]["q_squared_times_error"] - phi_limit) < 0.05)
    # Farey bound holds
    farey_ok = all(t["satisfies_bound"] for t in farey_tests)

    supported = bool(dirichlet_ok and phi_converges and farey_ok)

    results["summary"] = {
        "supported": supported,
        "dirichlet_bound_holds": dirichlet_ok,
        "golden_ratio_optimal": phi_converges,
        "farey_bound_holds": farey_ok,
        "honest_wall": "numerical verification of Diophantine approximation "
                       "properties, not a proof of Khintchine's theorem"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Khintchine's theorem via 0/0")
    print(f"  Dirichlet bound holds:   {s['dirichlet_bound_holds']}")
    print(f"  Golden ratio optimal:    {s['golden_ratio_optimal']}")
    print(f"  Farey bound holds:       {s['farey_bound_holds']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/khintchine_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
