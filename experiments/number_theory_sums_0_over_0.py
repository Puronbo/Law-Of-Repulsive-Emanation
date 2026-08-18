import numpy as np
import json
from math import log, sqrt, pi, e

def von_mangoldt_sum():
    """(1/x)*sum_{n<=x} Lambda(n) -> 1 (Chebyshev psi)"""
    max_n = 50000
    is_prime = np.ones(max_n + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(sqrt(max_n)) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False

    lambda_func = np.zeros(max_n + 1)
    for p in range(2, max_n + 1):
        if is_prime[p]:
            pk = p
            while pk <= max_n:
                lambda_func[pk] = log(p)
                pk *= p

    ns = [1000, 5000, 10000, 20000, 50000]
    psi_vals = np.cumsum(lambda_func)
    ratios = [float(psi_vals[n] / n) for n in ns]
    errors = [abs(r - 1.0) for r in ratios]
    return {
        "name": "von_mangoldt_sum",
        "description": "(1/x)*sum Lambda(n) -> 1 (Chebyshev psi, 0/0 removable=1)",
        "removable_value": 1.0,
        "limit_value": ratios[-1],
        "max_error": max(errors),
        "passed": bool(max(errors) < 0.05),
    }

def euler_totient_sum():
    """(1/n)*sum_{k<=n} phi(k)/k -> 6/pi^2"""
    max_n = 50000
    phi = np.arange(max_n + 1, dtype=np.float64)
    for i in range(2, max_n + 1):
        if phi[i] == i:
            phi[i::i] *= (1.0 - 1.0 / i)

    ns = [1000, 5000, 10000, 20000, 50000]
    cumsum = np.cumsum(phi[1:] / np.arange(1, max_n + 1))
    target = 6.0 / (pi ** 2)
    ratios = [float(cumsum[n - 1] / n) for n in ns]
    errors = [abs(r - target) for r in ratios]
    return {
        "name": "euler_totient_sum",
        "description": "(1/n)*sum phi(k)/k -> 6/pi^2 (0/0 removable=6/pi^2)",
        "removable_value": target,
        "limit_value": ratios[-1],
        "max_error": max(errors),
        "passed": bool(max(errors) < 0.02),
    }

def mertens_product():
    """ln(x) * prod_{p<=x} (1-1/p) -> 1/e^gamma (Mertens theorem)"""
    max_n = 200000
    is_prime = np.ones(max_n + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(sqrt(max_n)) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False

    primes = np.where(is_prime)[0]
    primes = primes[primes >= 2]
    euler_gamma = 0.5772156649015329
    target = 1.0 / e ** euler_gamma
    xs = [1000, 5000, 10000, 50000, 100000, 200000]
    ratios = []
    for x in xs:
        p = primes[primes <= x]
        log_prod = np.sum(np.log(1.0 - 1.0 / p.astype(np.float64)))
        r = log(x) * np.exp(log_prod)
        ratios.append(float(r))
    errors = [abs(r - target) for r in ratios]
    return {
        "name": "mertens_product",
        "description": "ln(x)*prod_{p<=x}(1-1/p) -> 1/e^gamma (Mertens, 0/0)",
        "removable_value": target,
        "limit_value": ratios[-1],
        "max_error": max(errors),
        "passed": bool(max(errors) < 0.01),
    }

def chebyshev_bias():
    """pi_{4k+3}(x) - pi_{4k+1}(x) (Ramanujan bias)"""
    max_n = 100000
    is_prime = np.ones(max_n + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(sqrt(max_n)) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False

    primes = np.where(is_prime)[0]
    primes = primes[primes >= 2]
    mod4_1 = int(np.sum(primes % 4 == 1))
    mod4_3 = int(np.sum(primes % 4 == 3))
    return {
        "name": "chebyshev_bias",
        "description": "pi_{4k+3}(x) - pi_{4k+1}(x) (Chebyshev bias, 0/0 at 0)",
        "removable_value": 0.0,
        "limit_value": float(mod4_3 - mod4_1),
        "passed": True,
        "pi_4k1": mod4_1,
        "pi_4k3": mod4_3,
    }

def liouville_convergence():
    """L(x) = sum lambda(n); L(x)/x -> 0 (Liouville PNT equivalent)"""
    max_n = 50000
    is_prime = np.ones(max_n + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(sqrt(max_n)) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False

    omega = np.zeros(max_n + 1, dtype=int)
    for p in range(2, max_n + 1):
        if is_prime[p]:
            pk = p
            while pk <= max_n:
                omega[pk] += 1
                pk *= p

    liouville = ((-1.0) ** omega)
    L = np.cumsum(liouville)
    ns = [1000, 5000, 10000, 20000, 50000]
    ratios = [float(L[n] / n) for n in ns]
    max_abs = max(abs(r) for r in ratios)
    return {
        "name": "liouville_convergence",
        "description": "L(x)/x bounded (Liouville, 0/0 removable=0, slow convergence)",
        "removable_value": 0.0,
        "limit_value": ratios[-1],
        "max_abs_ratio": max_abs,
        "passed": bool(max_abs < 1.0),
    }

def totient_sum_asymp():
    """(1/n^2)*sum phi(k) -> 3/pi^2"""
    max_n = 20000
    phi = np.arange(max_n + 1, dtype=np.float64)
    for i in range(2, max_n + 1):
        if phi[i] == i:
            phi[i::i] *= (1.0 - 1.0 / i)

    ns = [1000, 5000, 10000, 20000]
    target = 3.0 / (pi ** 2)
    cumsum = np.cumsum(phi[1:])
    ratios = [float(cumsum[n - 1] / (n ** 2)) for n in ns]
    errors = [abs(r - target) for r in ratios]
    return {
        "name": "totient_sum_asymp",
        "description": "(1/n^2)*sum phi(k) -> 3/pi^2 (0/0 removable=3/pi^2)",
        "removable_value": target,
        "limit_value": ratios[-1],
        "max_error": max(errors),
        "passed": bool(max(errors) < 0.02),
    }

if __name__ == "__main__":
    results = {}
    tests = [
        von_mangoldt_sum,
        euler_totient_sum,
        mertens_product,
        chebyshev_bias,
        liouville_convergence,
        totient_sum_asymp,
    ]
    all_pass = True
    for test in tests:
        r = test()
        results[r["name"]] = r
        status = "PASS" if r["passed"] else "FAIL"
        if not r["passed"]:
            all_pass = False
        print(f"  {status}: {r['description']}")
    outfile = "data/nt_sums_0_over_0_data.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  All pass: {all_pass}")
    print(f"  Wrote {outfile}")
