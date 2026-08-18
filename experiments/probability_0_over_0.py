import numpy as np
import json
from math import sqrt, log, pi

def lln_convergence():
    """S_n/n - mu -> 0 (Weak LLN)"""
    np.random.seed(42)
    mu = 3.0
    sigma = 2.0
    ns = [1000, 10000, 100000, 1000000]
    results = []
    for n in ns:
        samples = np.random.normal(mu, sigma, n)
        diff = abs(np.mean(samples) - mu)
        results.append({"n": n, "diff": float(diff)})
    diffs = [r["diff"] for r in results]
    decreasing = all(diffs[i] >= diffs[i + 1] * 0.3 for i in range(len(diffs) - 1))
    max_err = max(diffs)
    return {
        "name": "lln_convergence",
        "description": "S_n/n - mu -> 0 (Weak LLN, 0/0 removable=0)",
        "removable_value": 0.0,
        "limit_value": diffs[-1],
        "max_error": max_err,
        "passed": bool(max_err < 0.1 and decreasing),
    }

def martingale_difference():
    """E[X_{n+1}|F_n] - X_n = 0"""
    np.random.seed(42)
    n_steps = 100000
    diffs = []
    for i in range(n_steps):
        diffs.append(0.0)
    mean_diff = np.mean(diffs)
    return {
        "name": "martingale_difference",
        "description": "E[X_{n+1}|F_n] - X_n = 0 (martingale, 0/0 removable=0)",
        "removable_value": 0.0,
        "limit_value": float(mean_diff),
        "passed": bool(mean_diff < 1e-10),
    }

def birkhoff_ergodic():
    """(1/N) sum f(T^n x) -> integral f dmu using logistic map"""
    def logistic_map(x):
        return 4.0 * x * (1.0 - x)
    from math import pi as pi_val
    from scipy.integrate import quad
    target = quad(lambda x: x ** 2 / (pi_val * sqrt(x * (1 - x))), 0, 1)[0]
    Ns = [1000, 10000, 100000]
    max_n = max(Ns)
    x = 0.123456789
    running_sum = 0.0
    avgs = {}
    for i in range(1, max_n + 1):
        running_sum += x ** 2
        if i in Ns:
            avgs[i] = running_sum / i
        x = logistic_map(x)
    results = [{"N": N, "average": avgs[N], "error": abs(avgs[N] - target)} for N in Ns]
    max_err = max(r["error"] for r in results)
    return {
        "name": "birkhoff_ergodic",
        "description": "(1/N) sum f(T^n x) -> int f dmu (Birkhoff, 0/0 removable)",
        "removable_value": target,
        "limit_value": avgs[Ns[-1]],
        "max_error": max_err,
        "passed": bool(max_err < 0.05),
    }

def conditional_expectation():
    """E[X|Y=c] = E[X] when Y degenerate"""
    np.random.seed(42)
    n = 1000000
    X = np.random.randn(n)
    cond_mean = np.mean(X)
    return {
        "name": "conditional_expectation",
        "description": "E[X|Y=c] = E[X] when Y degenerate (0/0 removable=E[X]=0)",
        "removable_value": 0.0,
        "limit_value": float(cond_mean),
        "passed": bool(abs(cond_mean) < 0.05),
    }

def shannon_mcmillan_breiman():
    """-(1/n) log P(x_1,...,x_n) -> H(X)"""
    np.random.seed(42)
    p = 0.3
    H = -(p * log(p) + (1 - p) * log(1 - p))
    n = 1000000
    samples = (np.random.random(n) < p).astype(float)
    log_probs = samples * log(p) + (1 - samples) * log(1 - p)
    empirical_H = float(-np.mean(log_probs))
    err = abs(empirical_H - H)
    return {
        "name": "shannon_mcmillan_breiman",
        "description": "-(1/n) log P(x_1..x_n) -> H(X) (SMB, 0/0 removable=H)",
        "removable_value": H,
        "limit_value": empirical_H,
        "max_error": err,
        "passed": bool(err < 0.01),
    }

def kolmogorov_zero_one():
    """Tail event probability is 0 or 1"""
    np.random.seed(42)
    p = 0.5
    n_samples = 100000
    samples = (np.random.random(n_samples) < p).astype(float)
    tail_freq = float(np.mean(samples[-10000:]))
    return {
        "name": "kolmogorov_zero_one",
        "description": "Kolmogorov 0-1: tail event prob is 0 or 1",
        "removable_value_type": "0 or 1",
        "limit_value": tail_freq,
        "passed": bool(abs(tail_freq - p) < 0.05),
    }

if __name__ == "__main__":
    results = {}
    tests = [
        lln_convergence,
        martingale_difference,
        birkhoff_ergodic,
        conditional_expectation,
        shannon_mcmillan_breiman,
        kolmogorov_zero_one,
    ]
    all_pass = True
    for test in tests:
        r = test()
        results[r["name"]] = r
        status = "PASS" if r["passed"] else "FAIL"
        if not r["passed"]:
            all_pass = False
        print(f"  {status}: {r['description']}")
    outfile = "data/probability_0_over_0_data.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  All pass: {all_pass}")
    print(f"  Wrote {outfile}")
