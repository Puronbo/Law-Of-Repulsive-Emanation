import numpy as np
import json
from math import log, pi, sqrt, e

def log_removable_singularity():
    """log(1+x)/x at x=0: 0/0, removable = 1"""
    xs = np.array([1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10])
    ratios = np.log(1 + xs) / xs
    removable = 1.0
    errors = np.abs(ratios - removable)
    last_err = float(errors[-1])
    converges = bool(errors[-1] < errors[0] * 0.01)
    return {
        "name": "log_removable_singularity",
        "description": "log(1+x)/x at x=0: 0/0, removable=1",
        "removable_value": removable,
        "limit_value": float(ratios[-1]),
        "last_error": last_err,
        "passed": bool(last_err < 1e-7 and converges),
    }

def log_product_limit():
    """(1/n)*sum k*ln(1+1/k) -> 1 as n->inf"""
    ns = [100, 1000, 10000, 100000]
    results = []
    for n in ns:
        ks = np.arange(1, n + 1, dtype=np.float64)
        log_sum = np.sum(ks * np.log(1.0 + 1.0 / ks))
        avg = log_sum / n
        results.append({"n": n, "avg_log_factor": float(avg), "error": abs(avg - 1.0)})
    last_err = max(r["error"] for r in results[-2:])
    converges = results[-1]["error"] < results[0]["error"] * 0.01
    return {
        "name": "log_product_limit",
        "description": "(1/n)*sum k*ln(1+1/k) -> 1 (0/0 removable=1)",
        "removable_value": 1.0,
        "limit_value": results[-1]["avg_log_factor"],
        "last_error": last_err,
        "passed": bool(last_err < 1e-3 and converges),
        "details": results,
    }

def log_stirling_ratio():
    """log(n!) - (n*log(n)-n+0.5*log(2*pi*n)) -> 0"""
    from scipy.special import gammaln
    ns = np.array([10, 50, 100, 500, 1000], dtype=np.float64)
    log_fact = gammaln(ns + 1)
    stirling = ns * np.log(ns) - ns + 0.5 * np.log(2.0 * np.pi * ns)
    diffs = log_fact - stirling
    max_err = float(np.max(np.abs(diffs)))
    return {
        "name": "log_stirling_ratio",
        "description": "log(n!) - Stirling -> 0 (0*inf = 0/0, removable=0)",
        "removable_value": 0.0,
        "limit_value": float(diffs[-1]),
        "max_error": max_err,
        "passed": bool(max_err < 0.01),
    }

def log_harmonic_difference():
    """H_n - ln(n) -> gamma (Euler-Mascheroni); 0/0 at n=inf"""
    gamma_true = 0.5772156649015329
    ns = [100, 1000, 10000, 100000, 1000000]
    harmonics = [sum(1.0 / k for k in range(1, n + 1)) for n in ns]
    diffs = [h - log(n) for h, n in zip(harmonics, ns)]
    errors = [abs(d - gamma_true) for d in diffs]
    max_err = max(errors)
    return {
        "name": "log_harmonic_difference",
        "description": "H_n - ln(n) -> gamma (0/0 at n=inf, removable=gamma)",
        "removable_value": gamma_true,
        "limit_value": diffs[-1],
        "max_error": max_err,
        "passed": bool(max_err < 0.01),
    }

def log_binet_formula():
    """F_n/phi^n -> 1/sqrt(5); ratio converges"""
    phi = (1 + sqrt(5)) / 2
    target = 1.0 / sqrt(5)
    # Compute Fibonacci iteratively (correctly)
    fibs = {}
    a, b = 0, 1
    fibs[0] = 0
    for i in range(1, 101):
        a, b = b, a + b
        fibs[i] = a
    ns = [20, 50, 100]
    ratios = [fibs[n] / (phi ** n) for n in ns]
    errors = [abs(r - target) for r in ratios]
    last_err = errors[-1]
    converges = errors[-1] < errors[0] * 0.01
    return {
        "name": "log_binet_formula",
        "description": "F_n/phi^n -> 1/sqrt(5) (Binet, 0/0 removable=1/sqrt(5))",
        "removable_value": target,
        "limit_value": ratios[-1],
        "last_error": last_err,
        "passed": bool(last_err < 1e-10 and converges),
    }

def log_gamma_reflection():
    """z*Gamma(z)*Gamma(1-z) -> 1 (Euler reflection: Gamma(z)*Gamma(1-z) = pi/sin(pi*z), so z*pi/sin(pi*z) -> 1)"""
    import mpmath
    mpmath.mp.dps = 40
    zs = [0.1, 0.01, 0.001, 0.0001, 0.00001]
    results = []
    for z in zs:
        val = float(mpmath.mpf(z) * mpmath.gamma(z) * mpmath.gamma(1 - z))
        results.append(val)
    target = 1.0
    errors = [abs(r - target) for r in results]
    last_err = errors[-1]
    converges = errors[-1] < errors[0] * 0.01
    return {
        "name": "log_gamma_reflection",
        "description": "z*Gamma(z)*Gamma(1-z) -> 1 (Euler reflection, 0/0 removable=1)",
        "removable_value": target,
        "limit_value": results[-1],
        "last_error": last_err,
        "passed": bool(last_err < 1e-8 and converges),
    }

if __name__ == "__main__":
    results = {}
    tests = [
        log_removable_singularity,
        log_product_limit,
        log_stirling_ratio,
        log_harmonic_difference,
        log_binet_formula,
        log_gamma_reflection,
    ]
    all_pass = True
    for test in tests:
        r = test()
        results[r["name"]] = r
        status = "PASS" if r["passed"] else "FAIL"
        if not r["passed"]:
            all_pass = False
        print(f"  {status}: {r['description']}")
    outfile = "data/log_limits_0_over_0_data.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  All pass: {all_pass}")
    print(f"  Wrote {outfile}")
