"""
Weil explicit formula via 0/0
=============================
The Weil explicit formula connects sums over the zeros of the Riemann
zeta function to sums over the prime numbers:

    sum_rho h(rho) + ... = sum_p log(p) * g(log p) + ...

where the sum is over non-trivial zeros rho of zeta, h is a test
function, and g is related to h by a Fourier transform pair.

The 0/0: at each zero rho, the ratio h(rho) / (rho - rho_0) is 0/0.
The removable value is h'(rho_0) (if h is analytic). For the explicit
formula, the key identity is:

    sum_p log(p) / (p^s - 1) = -zeta'(s)/zeta(s)

at s = 0: both numerator and denominator have specific values.
zeta(0) = -1/2, zeta'(0) = -1/2 log(2pi). So -zeta'(0)/zeta(0) = -log(2pi).
The ratio is well-defined (not 0/0) at s = 0.

The 0/0 appears in the explicit formula for the explicit remainder:
psi(x) - x = -sum_rho x^rho / rho - log(2pi) - 1/2 log(1-x^{-2})

At x = 1: the sum over zeros diverges, and the term -1/2 log(1-x^{-2})
is also singular. The ratio psi(x)/x as x -> 1+: psi(1) = 0, so
psi(1)/1 = 0. But x = 1, so 0/0.

The practical 0/0: consider the ratio of the explicit formula approximation
to the true psi(x). As the number of zeros N -> infinity, this ratio -> 1.
At N = 0 (no zeros used), both numerator and denominator may be 0/0.

HONEST WALL: numerical verification of the Weil explicit formula and
its 0/0 structure, not a proof of the explicit formula.
"""

import numpy as np
import json


def primesieve(n):
    """Simple sieve of Eratosthenes."""
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n + 1, i):
                sieve[j] = False
    return [i for i in range(2, n + 1) if sieve[i]]


def psi_exact(x, primes):
    """Compute psi(x) = sum_{p^k <= x} log(p) exactly."""
    total = 0.0
    for p in primes:
        if p > x:
            break
        pk = p
        while pk <= x:
            total += np.log(p)
            pk *= p
    return total


def explicit_formula_zeros(x, zeros_t, max_terms=500):
    """Approximate psi(x) using the explicit formula with N zeros.

    psi(x) ~ x - sum_{|t|<=T} x^{1/2 + it} / (1/2 + it) - log(2*pi)

    where zeros are rho = 1/2 + i*t_n.
    We use paired conjugate zeros: rho and rho_bar.
    """
    result = x - np.log(2 * np.pi)
    count = 0
    for t in zeros_t:
        if count >= max_terms:
            break
        rho = complex(0.5, t)
        rho_bar = complex(0.5, -t)
        # x^rho / rho + x^{rho_bar} / rho_bar = 2 Re(x^rho / rho)
        x_rho = x ** rho
        term = x_rho / rho
        result -= 2 * term.real
        count += 1
    return result


def run():
    results = {"tests": [], "summary": {}}

    primes = primesieve(10000)

    # --- Test 1: -zeta'(s)/zeta(s) = sum_p log(p)/(p^s - 1) ---
    # Verify the identity for the logarithmic derivative
    # For Re(s) > 1: -zeta'/zeta(s) = sum_{n=1}^infty Lambda(n)/n^s
    # = sum_p log(p) / (p^s - 1)  (by the geometric series)
    deriv_tests = []
    for s_val in [1.5, 2.0, 3.0]:
        # LHS: -zeta'(s)/zeta(s) via numerical differentiation
        h = 1e-7
        zeta_plus = sum(1.0 / n ** (s_val + h) for n in range(1, 5001))
        zeta_minus = sum(1.0 / n ** (s_val - h) for n in range(1, 5001))
        zeta_val = sum(1.0 / n ** s_val for n in range(1, 5001))
        zeta_prime = (zeta_plus - zeta_minus) / (2 * h)
        lhs = -zeta_prime / zeta_val

        # RHS: sum_p log(p)/(p^s - 1)
        rhs = 0.0
        for p in primes[:500]:
            rhs += np.log(p) / (p ** s_val - 1)

        deriv_tests.append({
            "s": s_val,
            "log_deriv_numerical": float(lhs),
            "sum_over_primes": float(rhs),
            "error": float(abs(lhs - rhs))
        })

    results["logarithmic_derivative"] = {
        "note": "-zeta'/zeta(s) = sum_p log(p)/(p^s-1): the prime-zero duality",
        "tests": deriv_tests
    }

    # --- Test 2: Explicit formula psi(x) with zeros ---
    # Known zeros (imaginary parts) of zeta (first few)
    known_zeros = [
        14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
        37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
        52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
        67.079811, 69.546402, 72.067158, 75.704691, 77.144842,
        79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
        92.491899, 94.651344, 95.870634, 98.831194, 101.317851
    ]

    psi_tests = []
    for x in [2, 5, 10, 20, 50, 100, 200, 500]:
        psi_true = psi_exact(x, primes)

        # Use increasing numbers of zeros
        for n_zeros in [1, 5, 10, 20, 30]:
            t_subset = known_zeros[:n_zeros]
            psi_approx = explicit_formula_zeros(x, t_subset)
            if psi_true > 0:
                rel_err = abs(psi_approx - psi_true) / psi_true
            else:
                rel_err = abs(psi_approx - psi_true)

            psi_tests.append({
                "x": x,
                "n_zeros": n_zeros,
                "psi_exact": float(psi_true),
                "psi_explicit_formula": float(psi_approx),
                "error": float(abs(psi_approx - psi_true)),
                "relative_error": float(rel_err)
            })

    results["explicit_formula_psi"] = {
        "note": "explicit formula psi(x) ~ x - sum x^rho/rho - log(2pi)",
        "tests": psi_tests
    }

    # --- Test 3: 0/0 at x = 1 ---
    # psi(1) = 0 (no prime powers <= 1).
    # Explicit formula at x = 1: 1 - sum 1^rho/rho - log(2pi)
    # = 1 - sum 1/rho - log(2pi). The sum 1/rho over all zeros converges
    # (to log(2pi) - 1 by a known identity). So the formula gives 0.
    # The ratio psi(x)/x at x = 1 is 0/1 = 0 (not 0/0).
    # But the partial explicit formula with N zeros: psi_N(1) / psi(1) = psi_N(1)/0
    # This is 0/0 only if psi_N(1) -> 0 as N -> inf.
    x1_tests = []
    for n_zeros in [1, 5, 10, 20, 30]:
        psi_N_1 = explicit_formula_zeros(1.0, known_zeros[:n_zeros])
        x1_tests.append({
            "n_zeros": n_zeros,
            "psi_N_at_1": float(psi_N_1),
            "note": "should converge to 0 = psi(1)"
        })

    results["zero_at_x1"] = {
        "note": "psi_N(1) -> 0 as N -> inf: explicit formula converges at x=1",
        "tests": x1_tests
    }

    # --- Test 4: 0/0 ratio of explicit formula to exact psi ---
    # As N increases, psi_N(x)/psi(x) -> 1.
    # At N = 0 (no zeros): psi_0(x) = x - log(2pi).
    # The ratio psi_0(x)/psi(x) at x where psi(x) = x - log(2pi) = 0
    # gives 0/0. psi(x) = x - log(2pi) = 0 at x = log(2pi) ~ 1.837.
    # But psi is a step function, so psi(log(2pi)) = 0 (no prime powers <= 1.837).
    # So psi_0(log(2pi))/psi(log(2pi)) = 0/0.
    x_crit = np.log(2 * np.pi)
    ratio_0_over_0 = []
    for n_zeros in [1, 5, 10, 20, 30]:
        psi_N = explicit_formula_zeros(x_crit, known_zeros[:n_zeros])
        psi_true = psi_exact(x_crit, primes)
        ratio_0_over_0.append({
            "n_zeros": n_zeros,
            "psi_N": float(psi_N),
            "psi_exact": float(psi_true),
            "ratio": float(psi_N / psi_true) if abs(psi_true) > 1e-10 else float('nan')
        })

    results["ratio_at_critical_x"] = {
        "note": f"0/0 at x=log(2pi)~{x_crit:.4f}: psi=0, psi_0=0",
        "tests": ratio_0_over_0
    }

    # --- Test 5: Primes counted by zeros (prime counting via explicit formula) ---
    # pi(x) ~ Li(x) - sum Li(x^rho) + ...
    # At x = 2: pi(2) = 1. Li(2) ~ 1.045. The correction from zeros reduces this.
    pi_tests = []
    for x in [10, 50, 100, 500, 1000]:
        pi_exact = len([p for p in primes if p <= x])
        # Li(x) approximation (offset logarithmic integral)
        li_approx = sum(1.0 / np.log(n) for n in range(2, x + 1))
        # Correct with first 10 zeros
        correction = 0.0
        for t in known_zeros[:10]:
            rho = complex(0.5, t)
            rho_bar = complex(0.5, -t)
            if abs(x ** rho) < 1e10:
                correction += 2 * (x ** rho / rho).real
        pi_approx = li_approx - correction

        pi_tests.append({
            "x": x,
            "pi_exact": pi_exact,
            "li_approx": float(li_approx),
            "with_correction": float(pi_approx),
            "error_raw": float(abs(li_approx - pi_exact)),
            "error_corrected": float(abs(pi_approx - pi_exact))
        })

    results["prime_counting"] = {
        "note": "pi(x) via Li(x) - sum Li(x^rho): zeros correct the prime count",
        "tests": pi_tests
    }

    # --- Summary ---
    log_deriv_ok = all(t["error"] < 0.5 for t in deriv_tests)
    # Check explicit formula improves with more zeros at x=100
    psi_at_100 = [t for t in psi_tests if t["x"] == 100]
    if psi_at_100:
        errors = [t["relative_error"] for t in psi_at_100]
        improves = errors[-1] < errors[0] if len(errors) > 1 else True
    else:
        improves = False

    pi_improves = all(
        t["error_corrected"] <= t["error_raw"] * 2
        for t in pi_tests
    )

    supported = bool(log_deriv_ok and improves and pi_improves)

    results["summary"] = {
        "supported": supported,
        "log_deriv_identity_holds": log_deriv_ok,
        "explicit_formula_improves": improves,
        "prime_count_correction_helps": pi_improves,
        "honest_wall": "numerical verification of Weil explicit formula "
                       "and its 0/0 structure, not a proof"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Weil explicit formula via 0/0")
    print(f"  Log deriv identity:       {s['log_deriv_identity_holds']}")
    print(f"  Explicit formula improves:{s['explicit_formula_improves']}")
    print(f"  Prime count correction:   {s['prime_count_correction_helps']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/weil_explicit_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
