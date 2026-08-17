"""
Poincare recurrence theorem via 0/0
====================================
The Poincare recurrence theorem: for a measure-preserving dynamical
system (T, X, mu) with mu(X) < infinity, almost every point x in X
returns arbitrarily close to x under iteration of T.

The 0/0: the displacement d_n(x) = |T^n(x) - x| vanishes at recurrence
times n (where T^n(x) returns near x). The ratio d_n / d_0 where d_0
is the initial displacement... actually d_0 = 0 (trivially).

The cleaner 0/0: consider the return-time function. For a point x, define
tau_epsilon(x) = min{n >= 1 : d(T^n(x), x) < epsilon}. As epsilon -> 0,
tau_epsilon(x) -> infinity for irrational rotations. The ratio

    epsilon / tau_epsilon(x)

is 0/0 as epsilon -> 0 (both vanish). The removable value encodes the
distribution of return times.

For a rotation R_alpha on the circle (x -> x + alpha mod 1) with alpha
irrational: the recurrence is guaranteed by Poincare. The return time to
an epsilon-ball around x is roughly 1/epsilon (by equidistribution).

The product epsilon * tau_epsilon ~ 1 (constant), so epsilon/tau_epsilon
= epsilon^2 / (epsilon * tau_epsilon) ~ epsilon^2 -> 0. The 0/0 form:
epsilon * tau_epsilon / 1 is constant, while epsilon/tau_epsilon -> 0.

The most natural 0/0: for a measure-preserving map T and a set A of
measure mu(A), the recurrence rate is mu(A intersect T^{-n}(A)) / mu(A).
At n = 0: mu(A) / mu(A) = 1. The ratio for n > 0 measures how much
of A returns. By the Poincare recurrence theorem, this ratio is > 0
for infinitely many n. The 0/0 at mu(A) = 0: both numerator and
denominator are 0.

HONEST WALL: numerical verification of Poincare recurrence and return
time statistics, not a proof of the theorem.
"""

import numpy as np
import json


def rotation_map(x, alpha, n_iter):
    """Iterate the circle rotation x -> x + alpha mod 1."""
    trajectory = np.zeros(n_iter + 1)
    trajectory[0] = x % 1.0
    for i in range(n_iter):
        trajectory[i + 1] = (trajectory[i] + alpha) % 1.0
    return trajectory


def golden_ratio():
    """The golden ratio phi = (1+sqrt(5))/2, the most irrational number."""
    return (1 + np.sqrt(5)) / 2


def is_rational_approx(alpha, max_denom=100):
    """Check if alpha is well-approximated by rationals p/q with q <= max_denom."""
    best_err = 1.0
    best_q = 1
    for q in range(1, max_denom + 1):
        p = round(alpha * q)
        err = abs(alpha - p / q)
        if err < best_err:
            best_err = err
            best_q = q
    return best_q, best_err


def run():
    results = {"tests": [], "summary": {}}

    # --- Test 1: Recurrence of rotation on the circle ---
    n_iter = 50000
    alphas = {
        "golden_ratio": 1.0 / golden_ratio(),  # most irrational
        "sqrt2": np.sqrt(2) - 1,                 # also irrational
        "e_inv": 1.0 / np.e,                     # irrational
        "1/3": 1.0 / 3.0,                        # rational (periodic)
        "1/7": 1.0 / 7.0,                        # rational (periodic)
    }

    recurrence_tests = {}
    for name, alpha in alphas.items():
        x0 = 0.1
        traj = rotation_map(x0, alpha, n_iter)
        epsilons = [0.1, 0.05, 0.01, 0.005, 0.001]
        return_times = []
        for eps in epsilons:
            # Find first return within epsilon
            dists = np.minimum(traj[1:] - x0, 1 - (traj[1:] - x0))
            dists = np.abs(dists)
            first_return = np.argmax(dists < eps) + 1
            if first_return > 1 and dists[first_return - 1] < eps:
                return_times.append({
                    "epsilon": eps,
                    "first_return": int(first_return),
                    "product_eps_tau": float(eps * first_return)
                })
            else:
                return_times.append({
                    "epsilon": eps,
                    "first_return": None,
                    "product_eps_tau": None
                })

        # Also compute recurrence rate: how many of first N iterates return
        rate_tests = []
        for eps in [0.1, 0.05, 0.01]:
            dists = np.abs(np.minimum(traj[1:] - x0, 1 - (traj[1:] - x0)))
            n_return = np.sum(dists < eps)
            rate = n_return / n_iter
            rate_tests.append({
                "epsilon": eps,
                "n_returns": int(n_return),
                "recurrence_rate": float(rate)
            })

        recurrence_tests[name] = {
            "alpha": float(alpha),
            "alpha_type": "rational" if name.startswith("1/") else "irrational",
            "return_times": return_times,
            "recurrence_rates": rate_tests
        }

    results["recurrence"] = recurrence_tests

    # --- Test 2: 0/0 at mu(A) = 0 ---
    # For the recurrence rate R_n = mu(A intersect T^{-n}(A)) / mu(A):
    # At mu(A) = 0: 0/0. Removable value = 0 (since numerator is also 0).
    # Numerically: for a shrinking interval A_eps of width eps,
    # R_n(eps) = measure of return within eps.
    # As eps -> 0, R_n(eps) -> 0 for each fixed n (except n=0).
    # The ratio R_n(eps) / eps -> some limit.

    alpha_irr = 1.0 / golden_ratio()
    x0 = 0.0
    n_iter = 10000
    traj = rotation_map(x0, alpha_irr, n_iter)

    ratio_0_over_0_tests = []
    for eps in [0.1, 0.05, 0.01, 0.005, 0.001]:
        # Count returns to epsilon-neighborhood
        dists = np.abs(np.minimum(traj[1:] - x0, 1 - (traj[1:] - x0)))
        n_returns = np.sum(dists < eps)
        rate = n_returns / n_iter
        # The 0/0: rate/eps as eps -> 0
        ratio = rate / eps if eps > 0 else 0

        ratio_0_over_0_tests.append({
            "epsilon": eps,
            "n_returns": int(n_returns),
            "recurrence_rate": float(rate),
            "rate_over_epsilon": float(ratio)
        })

    results["rate_0_over_0"] = {
        "note": "R_n(eps)/eps as eps -> 0: 0/0 at eps=0, removable value = density",
        "tests": ratio_0_over_0_tests
    }

    # --- Test 3: Product epsilon * tau_epsilon ---
    # For irrational rotations, tau ~ 1/eps (by equidistribution).
    # So eps * tau ~ constant. The 0/0: eps/tau = eps^2/(eps*tau) -> 0,
    # while eps*tau -> constant.

    product_tests = []
    for alpha_name, alpha in [("golden", 1.0/golden_ratio()), ("sqrt2", np.sqrt(2)-1)]:
        x0 = 0.12345
        epsilons = [0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001]
        products = []
        for eps in epsilons:
            # Compute return time
            x = x0
            tau = None
            for n in range(1, int(1e6)):
                x = (x + alpha) % 1.0
                dist = min(abs(x - x0), 1 - abs(x - x0))
                if dist < eps:
                    tau = n
                    break
            if tau is not None:
                products.append({
                    "epsilon": eps,
                    "tau": tau,
                    "eps_times_tau": float(eps * tau),
                    "eps_over_tau": float(eps / tau)
                })

        product_tests.append({
            "alpha_name": alpha_name,
            "products": products
        })

    results["product_eps_tau"] = {
        "note": "eps * tau(eps) -> constant for irrational rotations",
        "tests": product_tests
    }

    # --- Test 4: Rational rotation (periodic, not just recurrent) ---
    # For alpha = 1/q: the orbit is periodic with period q.
    # Every point returns to itself after exactly q steps.
    # The return time is exactly q, independent of epsilon.
    # So eps * tau = eps * q -> 0 as eps -> 0.
    # But eps / tau = eps / q -> 0 as well.
    # The recurrence is TRIVIAL (periodic), not just recurrent.

    periodic_tests = []
    for q in [3, 5, 7, 11]:
        alpha = 1.0 / q
        x0 = 0.1
        traj = rotation_map(x0, alpha, 100)
        # Check period
        period_found = None
        for n in range(1, 101):
            dist = min(abs(traj[n] - x0), 1 - abs(traj[n] - x0))
            if dist < 1e-10:
                period_found = n
                break

        periodic_tests.append({
            "q": q,
            "alpha": float(alpha),
            "period_found": period_found,
            "is_exact": bool(period_found == q)
        })

    results["periodic_rotation"] = {
        "note": "rational rotations are periodic (trivially recurrent)",
        "tests": periodic_tests
    }

    # --- Test 5: Equidistribution (closely related to recurrence) ---
    # For irrational alpha, the orbit {x, x+alpha, x+2alpha, ...} mod 1
    # is equidistributed. Verify by counting hits in intervals.
    equidist_tests = []
    alpha = 1.0 / golden_ratio()
    for N in [100, 1000, 10000, 100000]:
        traj = rotation_map(0.0, alpha, N)
        # Count in [0, 0.5)
        count_half = np.sum(traj < 0.5)
        expected = N / 2
        deviation = abs(count_half - expected) / N
        equidist_tests.append({
            "N": N,
            "count_in_half": int(count_half),
            "expected": expected,
            "deviation": float(deviation)
        })

    results["equidistribution"] = {
        "note": "irrational rotations are equidistributed (implies recurrence)",
        "tests": equidist_tests
    }

    # --- Summary ---
    # Golden ratio has returns for all epsilons tested
    golden_returns = all(
        t["first_return"] is not None
        for t in recurrence_tests["golden_ratio"]["return_times"]
    )
    # Periodic rotations have exact periods
    periodic_ok = all(t["is_exact"] for t in periodic_tests)
    # Equidistribution converges
    equidist_converges = equidist_tests[-1]["deviation"] < 0.05
    # Products eps*tau are roughly constant
    golden_products = [t["eps_times_tau"] for t in
                       product_tests[0]["products"] if t["eps_times_tau"]]
    product_constant = (max(golden_products) / min(golden_products) < 3.0
                        if len(golden_products) > 1 else False)

    supported = bool(golden_returns and periodic_ok and equidist_converges and
                     product_constant)

    results["summary"] = {
        "supported": supported,
        "golden_ratio_recurs": golden_returns,
        "periodic_rotations_exact": periodic_ok,
        "equidistribution_converges": equidist_converges,
        "eps_tau_product_constant": product_constant,
        "honest_wall": "numerical verification of Poincare recurrence "
                       "and return time statistics, not a proof of the theorem"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Poincare recurrence via 0/0")
    print(f"  Golden ratio recurs:      {s['golden_ratio_recurs']}")
    print(f"  Periodic exact:           {s['periodic_rotations_exact']}")
    print(f"  Equidistribution:         {s['equidistribution_converges']}")
    print(f"  eps*tau constant:         {s['eps_tau_product_constant']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/poincare_recurrence_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
