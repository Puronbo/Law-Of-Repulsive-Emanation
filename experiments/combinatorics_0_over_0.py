import numpy as np
import json
from math import comb, factorial, log, e, pi, sqrt
from scipy.special import gammaln, stirling2

def stirling_number_ratio():
    """S(n,k)/k^n -> 1/k! for fixed k, n->inf"""
    ks = [2, 3, 4, 5]
    n_test = 200
    results = []
    for k in ks:
        s_nk = stirling2(n_test, k)
        ratio = s_nk / (k ** n_test)
        target = 1.0 / factorial(k)
        results.append({"k": k, "ratio": float(ratio), "target": target, "error": abs(ratio - target)})
    max_err = max(r["error"] for r in results)
    return {
        "name": "stirling_number_ratio",
        "description": "S(n,k)/k^n -> 1/k! (Stirling 2nd kind, 0/0 removable=1/k!)",
        "max_error": max_err,
        "passed": bool(max_err < 0.01),
        "details": results,
    }

def catalan_asymptotic():
    """C_n * n^{3/2} / 4^n -> 1/sqrt(pi) via log-space"""
    target = 1.0 / sqrt(pi)
    ns = [50, 100, 200, 500]
    ratios = []
    for n in ns:
        log_cn = gammaln(2 * n + 1) - gammaln(n + 2) - gammaln(n + 1)
        ratio = np.exp(log_cn - n * log(4) + 1.5 * log(n))
        ratios.append(float(ratio))
    errors = [abs(r - target) for r in ratios]
    max_err = max(errors)
    return {
        "name": "catalan_asymptotic",
        "description": "C_n * n^(3/2) / 4^n -> 1/sqrt(pi) (Catalan, 0/0 removable=1/sqrt(pi))",
        "removable_value": target,
        "limit_value": ratios[-1],
        "max_error": max_err,
        "passed": bool(max_err < 0.02),
    }

def binomial_limit():
    """binom(n,k)/n^k -> 1/k! for fixed k, n->inf"""
    ks = [2, 3, 5, 10]
    ns = [100, 500, 1000, 5000]
    results = []
    for k in ks:
        target = 1.0 / factorial(k)
        errs = []
        for n in ns:
            r = comb(n, k) / (n ** k)
            errs.append(abs(r - target))
        results.append({"k": k, "max_error": max(errs)})
    max_err = max(r["max_error"] for r in results)
    return {
        "name": "binomial_limit",
        "description": "binom(n,k)/n^k -> 1/k! (0/0 removable=1/k!)",
        "max_error": max_err,
        "passed": bool(max_err < 0.01),
    }

def motzkin_convergence():
    """M_n * n^{3/2} / 3^n converges"""
    ns_target = [50, 100, 200, 500]
    motzkin = [1.0, 1.0]
    for i in range(2, max(ns_target) + 1):
        m = ((2 * i - 1) * motzkin[-1] + 3 * (i - 2) * motzkin[-2]) / (i + 1)
        motzkin.append(m)
    ratios = []
    for n in ns_target:
        r = motzkin[n] * (n ** 1.5) / (3.0 ** n)
        ratios.append(float(r))
    err = abs(ratios[-1] - ratios[-2])
    return {
        "name": "motzkin_convergence",
        "description": "M_n * n^(3/2) / 3^n converges (Motzkin, 0/0 removable=const)",
        "limit_value": ratios[-1],
        "convergence_error": err,
        "passed": bool(err < 0.01),
    }

def partition_function_hardy():
    """log(p(n))/sqrt(n) -> pi*sqrt(2/3) (Hardy-Ramanujan)"""
    def pentagonal_numbers(max_n):
        nums = []
        k = 1
        while True:
            g1 = k * (3 * k - 1) // 2
            g2 = k * (3 * k + 1) // 2
            if g1 > max_n and g2 > max_n:
                break
            sign = 1 if k % 2 == 1 else -1
            if g1 <= max_n:
                nums.append((g1, sign))
            if g2 <= max_n:
                nums.append((g2, sign))
            k += 1
        nums.sort()
        return nums

    def partition(n):
        p = [0] * (n + 1)
        p[0] = 1
        penta = pentagonal_numbers(n)
        for i in range(1, n + 1):
            s = 0
            for g, sign in penta:
                if g > i:
                    break
                s += sign * p[i - g]
            p[i] = s
        return p[n]

    target = pi * sqrt(2.0 / 3.0)
    ns = [50, 100, 200, 500]
    ratios = []
    for n in ns:
        p_n = partition(n)
        r = log(float(p_n)) / sqrt(float(n))
        ratios.append(float(r))
    errors = [abs(r - target) for r in ratios]
    last_err = errors[-1]
    converges = errors[-1] < errors[0] * 0.5
    return {
        "name": "partition_function_hardy",
        "description": "log(p(n))/sqrt(n) -> pi*sqrt(2/3) (Hardy-Ramanujan, 0/0)",
        "removable_value": target,
        "limit_value": ratios[-1],
        "last_error": last_err,
        "passed": bool(last_err < 0.5 and converges),
    }

def derangement_limit():
    """D_n/n! -> 1/e as n->inf; 0/0 at n=inf"""
    from scipy.special import factorial as fact_func
    ns = [5, 10, 20, 50, 100]
    results = []
    for n in ns:
        D_n = int(round(sum((-1)**k / float(factorial(k)) for k in range(n+1)) * factorial(n)))
        ratio = D_n / factorial(n)
        results.append({"n": n, "ratio": ratio, "error": abs(ratio - 1.0/e)})
    last_err = results[-1]["error"]
    converges = results[-1]["error"] < results[0]["error"] * 0.01
    return {
        "name": "derangement_limit",
        "description": "D_n/n! -> 1/e (derangements, 0/0 removable=1/e)",
        "removable_value": 1.0 / e,
        "limit_value": results[-1]["ratio"],
        "last_error": last_err,
        "passed": bool(last_err < 1e-6 and converges),
    }

if __name__ == "__main__":
    results = {}
    tests = [
        stirling_number_ratio,
        catalan_asymptotic,
        binomial_limit,
        motzkin_convergence,
        partition_function_hardy,
        derangement_limit,
    ]
    all_pass = True
    for test in tests:
        r = test()
        results[r["name"]] = r
        status = "PASS" if r["passed"] else "FAIL"
        if not r["passed"]:
            all_pass = False
        print(f"  {status}: {r['description']}")
    outfile = "data/combinatorics_0_over_0_data.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  All pass: {all_pass}")
    print(f"  Wrote {outfile}")
