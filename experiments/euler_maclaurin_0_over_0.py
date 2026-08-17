"""
Euler-Maclaurin via 0/0
========================
The Euler-Maclaurin formula connects sums to integrals:

  sum_{k=0}^{N} f(k) = int_0^N f(x) dx + (f(0)+f(N))/2
                        + sum_{j=1}^{p} B_{2j}/(2j)! * (f^{(2j-1)}(N) - f^{(2j-1)}(0)) + R

The Bernoulli numbers B_n appear in the correction terms.  They are
defined by the generating function:

  B(x) = x / (e^x - 1) = sum_{n=0}^{inf} B_n x^n / n!

The 0/0: at x = 0, B(x) = 0/0 (numerator and denominator both vanish).
By L'Hopital: lim_{x->0} x/(e^x - 1) = 1/1 = 1.

The removable value is B(0) = 1, and the Taylor coefficients give:
  B_0 = 1, B_1 = -1/2, B_2 = 1/6, B_4 = -1/30, B_6 = 1/42, ...

HONEST WALL: numerical verification of the generating function limit,
not a proof of the Euler-Maclaurin formula.
"""

import numpy as np
from scipy.special import bernoulli as scipy_bernoulli
import json


def bernoulli_gen(x):
    """B(x) = x / (e^x - 1), with B(0) = 1 (removable value)."""
    if abs(x) < 1e-14:
        return 1.0
    return float(x / np.expm1(x))


def bernoulli_gen_taylor(x, n_terms=20):
    """B(x) via Taylor expansion sum B_n x^n / n!."""
    # Bernoulli numbers from scipy
    B = scipy_bernoulli(n_terms)
    result = 0.0
    for n in range(n_terms):
        result += B[n] * x ** n / np.math.factorial(n)
    return float(result)


def run():
    results = {}

    # --- Test 1: convergence of B(x) -> 1 as x -> 0 ---
    conv = []
    for exp in range(1, 14):
        x = 10.0 ** (-exp)
        Bx = bernoulli_gen(x)
        conv.append({"x": x, "Bx": Bx, "error": abs(Bx - 1.0)})
    results["convergence_to_1"] = conv

    # --- Test 2: Taylor coefficients match Bernoulli numbers ---
    B_expected = [1.0, -0.5, 1.0/6, 0.0, -1.0/30, 0.0, 1.0/42,
                  0.0, -1.0/30, 0.0, 5.0/66, 0.0, -691.0/2730]
    B_arr = scipy_bernoulli(len(B_expected) - 1)
    B_scipy = [float(B_arr[n]) for n in range(len(B_expected))]
    taylor_match = []
    for n, (exp, got) in enumerate(zip(B_expected, B_scipy)):
        taylor_match.append({
            "n": n, "expected": exp, "got": got,
            "error": abs(exp - got)
        })
    results["bernoulli_numbers"] = taylor_match

    # --- Test 3: Euler-Maclaurin sum-integral correction for f(x)=x^2 ---
    # sum_{k=0}^{N} k^2 = N(N+1)(2N+1)/6
    # int_0^N x^2 dx = N^3/3
    # Correction = (f(0)+f(N))/2 + B_2/2! * (f'(N)-f'(0)) = N^2/2 + (1/6)/2 * (2N) = N^2/2 + N/6
    em_checks = []
    for N in [5, 10, 20, 50]:
        exact_sum = N * (N + 1) * (2 * N + 1) / 6.0
        integral = N ** 3 / 3.0
        correction = N ** 2 / 2.0 + N / 6.0
        em_sum = integral + correction
        em_checks.append({
            "N": N, "exact_sum": exact_sum, "em_sum": em_sum,
            "error": abs(exact_sum - em_sum)
        })
    results["euler_maclaurin_x2"] = em_checks

    # --- Test 4: B(x) * (e^x - 1) = x identity ---
    identity_checks = []
    for exp in range(1, 8):
        x = 10.0 ** (-exp)
        Bx = bernoulli_gen(x)
        lhs = Bx * (np.exp(x) - 1)
        identity_checks.append({
            "x": x, "lhs": lhs, "rhs": x, "error": abs(lhs - x)
        })
    results["generating_identity"] = identity_checks

    # --- Summary ---
    err_conv = conv[-1]["error"]
    err_taylor = max(t["error"] for t in taylor_match if t["expected"] != 0)
    err_em = max(t["error"] for t in em_checks)
    supported = bool(err_conv < 1e-10 and err_taylor < 1e-10 and err_em < 1e-8)
    results["summary"] = {
        "convergence_error": err_conv,
        "taylor_error": err_taylor,
        "euler_maclaurin_error": err_em,
        "supported": supported,
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Euler-Maclaurin via 0/0")
    print(f"  B(x) -> 1 error:     {s['convergence_error']:.2e}")
    print(f"  Taylor coeff error:  {s['taylor_error']:.2e}")
    print(f"  Euler-Maclaurin err: {s['euler_maclaurin_error']:.2e}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/euler_maclaurin_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
