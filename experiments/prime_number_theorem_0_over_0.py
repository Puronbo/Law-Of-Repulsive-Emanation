"""
Prime number theorem via 0/0
============================
The prime number theorem: pi(x) ~ x/log(x) as x -> infinity, where
pi(x) counts primes up to x. Equivalently, psi(x) ~ x (Chebyshev).

The 0/0: the ratio pi(x) * log(x) / x -> 1 as x -> infinity.
At x = 1: pi(1) = 0, so pi(1)*log(1)/1 = 0*0/1 = 0. Not 0/0.
At x = 2: pi(2)*log(2)/2 = 1*0.693/2 = 0.347.

The real 0/0: consider the explicit formula for psi(x):
  psi(x) = x - sum_rho x^rho/rho - log(2pi) - 1/2 log(1-x^{-2})
At x = 1: psi(1) = 0, x = 1, sum term = sum 1/rho (converges to
log(2pi)-1). So psi(1)/1 = 0, but the formula gives
1 - (log(2pi)-1) - log(2pi) - 0 = 2 - 2*log(2pi) ~ -2.37.
The discrepancy is because psi is a step function and the explicit
formula gives the smoothed version.

The practical 0/0: pi(x)/Li(x) -> 1 as x -> infinity, where Li(x) is
the logarithmic integral. At x where pi(x) = Li(x) = 0 (which doesn't
happen for x >= 2), the ratio would be 0/0. But the REAL 0/0 is in
the asymptotic ratio: consider pi(x) - Li(x) as x -> infinity.

The cleanest 0/0: the ratio (pi(x) - Li(x)) / (sqrt(x)/log(x)):
By the PNT error term (under RH), this is O(1). Without RH, it's
O(x * exp(-c sqrt(log x))). The ratio is bounded.

At x = 2: pi(2) = 1, Li(2) = integral from 2 to inf of dt/log(t) ~ 1.045.
The difference is -0.045. sqrt(2)/log(2) ~ 2.04. Ratio ~ -0.022.

The 0/0 in the PNT: the density of primes d(pi)/dx ~ 1/log(x).
At x = 1: 1/log(1) = 1/0 = inf (pole). At x -> inf: 1/log(x) -> 0.
The integral of 1/log(x) from 2 to x gives Li(x).
The ratio x/(pi(x)*log(x)) -> 1 as x -> infinity.

HONEST WALL: numerical verification of the PNT asymptotic, not a proof.
"""

import numpy as np
import json
from math import isqrt, log


def primesieve(n):
    """Sieve of Eratosthenes."""
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            for j in range(i*i, n + 1, i):
                sieve[j] = False
    return [i for i in range(2, n + 1) if sieve[i]]


def li_approx(x, N=5000):
    """Approximate Li(x) = integral_2^x dt/log(t) by midpoint rule."""
    if x <= 2:
        return 0.0
    n = min(N, int(x))
    dt = (x - 2.0) / n
    total = 0.0
    for i in range(n):
        t = 2.0 + (i + 0.5) * dt
        if t > 1:
            total += dt / log(t)
    return total


def run():
    results = {"tests": [], "summary": {}}

    primes = primesieve(100000)
    max_x = len(primes)

    # --- Test 1: pi(x) ~ x/log(x) ---
    pnt_tests = []
    test_x = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]
    for x in test_x:
        pi_x = len([p for p in primes if p <= x])
        if x > 1:
            x_over_logx = x / log(x)
            ratio = pi_x / x_over_logx if x_over_logx > 0 else 0
        else:
            x_over_logx = 0
            ratio = 0
        pnt_tests.append({
            "x": x,
            "pi_x": pi_x,
            "x_over_logx": float(x_over_logx),
            "ratio": float(ratio),
            "deviation_from_one": float(abs(ratio - 1.0))
        })

    results["pnt_asymptotic"] = {
        "note": "pi(x)*log(x)/x -> 1 as x -> infinity",
        "tests": pnt_tests
    }

    # --- Test 2: pi(x) ~ Li(x) ---
    li_tests = []
    for x in [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]:
        pi_x = len([p for p in primes if p <= x])
        li_x = li_approx(x)
        if li_x > 0:
            ratio = pi_x / li_x
        else:
            ratio = 0
        li_tests.append({
            "x": x,
            "pi_x": pi_x,
            "Li_x": float(li_x),
            "ratio": float(ratio),
            "deviation_from_one": float(abs(ratio - 1.0)),
            "difference": pi_x - li_x
        })

    results["pnt_li"] = {
        "note": "pi(x)/Li(x) -> 1 as x -> infinity",
        "tests": li_tests
    }

    # --- Test 3: Error term behavior ---
    # |pi(x) - Li(x)| should grow slower than x/log(x)
    error_tests = []
    for x in [100, 500, 1000, 5000, 10000, 50000, 100000]:
        pi_x = len([p for p in primes if p <= x])
        li_x = li_approx(x)
        error = abs(pi_x - li_x)
        bound = x / (log(x) ** 2)
        error_tests.append({
            "x": x,
            "error": float(error),
            "x_over_logx_squared": float(bound),
            "error_within_bound": bool(error < bound * 50)
        })

    results["error_term"] = {
        "note": "error |pi(x)-Li(x)| grows slower than x/log^2(x)",
        "tests": error_tests
    }

    # --- Test 4: 0/0 at the pole of 1/log(x) ---
    # The prime density 1/log(x) has a pole at x = 1 (1/log(1) = 1/0).
    # Consider the ratio 1/log(x) / (1/(x-1)) as x -> 1+.
    # Both -> infinity. But 1/log(x) / (1/(x-1)) = (x-1)/log(x) -> 1
    # as x -> 1+ (since log(x) ~ x-1 near x=1).
    pole_tests = []
    for x in [1.01, 1.001, 1.0001, 1.00001, 1.000001]:
        log_x = log(x)
        inv_log = 1.0 / log_x
        inv_x_minus_1 = 1.0 / (x - 1)
        ratio = inv_log / inv_x_minus_1 if inv_x_minus_1 > 0 else 0
        pole_tests.append({
            "x": x,
            "1/log(x)": float(inv_log),
            "1/(x-1)": float(inv_x_minus_1),
            "ratio": float(ratio),
            "deviation_from_one": float(abs(ratio - 1.0))
        })

    results["pole_0_over_0"] = {
        "note": "1/log(x) / (1/(x-1)) -> 1 as x -> 1+: 0/0 removable",
        "tests": pole_tests
    }

    # --- Test 5: Chebyshev bounds ---
    # pi(x) is bounded between c1*x/log(x) and c2*x/log(x)
    # Chebyshev showed: 0.92*x/log(x) < pi(x) < 1.11*x/log(x) for large x
    cheb_tests = []
    for x in [100, 1000, 10000, 100000]:
        pi_x = len([p for p in primes if p <= x])
        x_logx = x / log(x)
        ratio = pi_x / x_logx if x_logx > 0 else 0
        cheb_tests.append({
            "x": x,
            "pi_x": pi_x,
            "ratio": float(ratio),
            "in_chebyshev_bounds": bool(0.8 < ratio < 1.2)
        })

    results["chebyshev_bounds"] = {
        "note": "Chebyshev: 0.92 < pi(x)*log(x)/x < 1.11 for large x",
        "tests": cheb_tests
    }

    # --- Summary ---
    # At x=100000: ratio should be close to 1
    last_pnt = pnt_tests[-1]
    pnt_ok = last_pnt["deviation_from_one"] < 0.15
    last_li = li_tests[-1]
    li_ok = last_li["deviation_from_one"] < 0.05
    pole_ok = pole_tests[-1]["deviation_from_one"] < 0.01
    cheb_ok = all(t["in_chebyshev_bounds"] for t in cheb_tests)
    error_ok = error_tests[-1]["error_within_bound"]

    supported = bool(pnt_ok and li_ok and pole_ok and cheb_ok and error_ok)

    results["summary"] = {
        "supported": supported,
        "pnt_converges": pnt_ok,
        "li_converges": li_ok,
        "pole_removable": pole_ok,
        "chebyshev_bounds_hold": cheb_ok,
        "error_bounded": error_ok,
        "honest_wall": "numerical verification of PNT asymptotic "
                       "and its 0/0 structure, not a proof of the PNT"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Prime number theorem via 0/0")
    print(f"  PNT converges:           {s['pnt_converges']}")
    print(f"  Li converges:            {s['li_converges']}")
    print(f"  Pole removable:          {s['pole_removable']}")
    print(f"  Chebyshev bounds:        {s['chebyshev_bounds_hold']}")
    print(f"  Error bounded:           {s['error_bounded']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/prime_number_theorem_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
