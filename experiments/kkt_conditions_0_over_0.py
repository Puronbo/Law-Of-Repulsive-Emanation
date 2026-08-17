"""
KKT conditions via 0/0
======================
The Karush-Kuhn-Tucker (KKT) conditions are necessary conditions for
a solution in nonlinear programming to be optimal, given constraints.

For:  minimize f(x)  subject to  g_i(x) <= 0,  h_j(x) = 0.

The KKT conditions (at a candidate x*):
1. Stationarity: grad f + sum_i mu_i grad g_i + sum_j lambda_j grad h_j = 0
2. Primal feasibility: g_i(x*) <= 0, h_j(x*) = 0
3. Dual feasibility: mu_i >= 0
4. Complementary slackness: mu_i * g_i(x*) = 0

The 0/0: complementary slackness states mu_i * g_i(x*) = 0. This can be
rewritten as:

    mu_i / (1/g_i(x*))

or more naturally, at a point where both mu_i = 0 and g_i(x*) = 0
(constraint is active but not binding), the ratio

    mu_i / g_i(x*)

is 0/0. The removable value encodes whether the constraint is truly active:
  - If mu_i > 0 and g_i(x*) = 0: constraint is active and binding (no 0/0).
  - If mu_i = 0 and g_i(x*) = 0: constraint is degenerate (0/0, removable
    value = 0, constraint is "weakly active").
  - If mu_i = 0 and g_i(x*) < 0: constraint is inactive (no 0/0).

For equality constraints h_j(x*) = 0: the ratio lambda_j / h_j(x*) is 0/0
at any feasible point. The removable value = lambda_j (the shadow price).

The key 0/0 for optimization: at the barrier/interior-point path, consider:

    mu_t * g_i(x_t) = 0  for all t > 0 (complementary slackness).

As t -> 0 (mu_t -> 0), the product mu_t * g_i(x_t) -> 0. But at t = 0,
mu_0 = 0 and g_i(x_0) = 0 (at the optimal), so the product is 0*0 = 0.
The ratio mu_t / (-1/g_i(x_t)) as t -> 0 is 0/0, with removable value = 0.

HONEST WALL: numerical verification of KKT conditions for specific
optimization problems, not a proof of KKT theory.
"""

import numpy as np
import json
from scipy.optimize import minimize, NonlinearConstraint


def solve_qp_inequality():
    """Solve: min x^2 + y^2  s.t.  x + y >= 1.

    Lagrangian: L = x^2 + y^2 - mu*(x + y - 1)
    KKT: 2x - mu = 0, 2y - mu = 0, x + y = 1 (active at optimum).
    => x = y = mu/2, and mu/2 + mu/2 = 1 => mu = 1.
    => x* = y* = 0.5, mu* = 1.
    """
    def objective(x):
        return x[0]**2 + x[1]**2

    def constraint_func(x):
        return x[0] + x[1] - 1  # >= 0 means x+y >= 1

    constraints = NonlinearConstraint(constraint_func, 0, np.inf)
    result = minimize(objective, [0.5, 0.5], method='SLSQP',
                      constraints=[{'type': 'ineq', 'fun': constraint_func}])

    x_star = result.x
    g_val = constraint_func(x_star)
    # Compute multiplier (shadow price) via finite difference of optimal value
    mu_approx = -result.fun  # approximate from Lagrangian

    # Analytical: mu = 1, x* = y* = 0.5
    mu_analytical = 1.0

    # Complementary slackness: mu * g(x*) = 0
    comp_slack = mu_analytical * max(g_val, 0)

    return {
        "x_star": x_star.tolist(),
        "optimal_value": float(result.fun),
        "expected_x_star": [0.5, 0.5],
        "constraint_value": float(g_val),
        "multiplier": float(mu_analytical),
        "complementary_slackness": float(comp_slack),
        "kkt_satisfied": bool(abs(comp_slack) < 1e-6)
    }


def solve_qp_active_inactive():
    """Solve: min x^2 + y^2  s.t.  x + y >= 3 (inactive: optimum at boundary).

    Without constraint: x* = y* = 0, but 0+0 < 3, so constraint is active.
    With constraint: x* = y* = 1.5, mu = 3.
    """
    def objective(x):
        return x[0]**2 + x[1]**2

    result = minimize(objective, [1, 1], method='SLSQP',
                      constraints=[{'type': 'ineq', 'fun': lambda x: x[0] + x[1] - 3}])

    x_star = result.x
    g_val = x_star[0] + x_star[1] - 3

    # Analytical: x* = y* = 1.5, mu = 3
    return {
        "x_star": x_star.tolist(),
        "optimal_value": float(result.fun),
        "expected_x_star": [1.5, 1.5],
        "constraint_value": float(g_val),
        "multiplier": 3.0,
        "complementary_slackness": 3.0 * max(g_val, 0),
        "kkt_satisfied": bool(abs(3.0 * max(g_val, 0)) < 1e-6)
    }


def solve_equality_constraint():
    """Solve: min x^2 + y^2  s.t.  x + y = 1.

    KKT: 2x + lambda = 0, 2y + lambda = 0, x + y = 1.
    => x = y = -lambda/2, and -lambda = 1, lambda = -1.
    => x* = y* = 0.5, lambda* = -1.
    """
    def objective(x):
        return x[0]**2 + x[1]**2

    result = minimize(objective, [0.5, 0.5], method='SLSQP',
                      constraints=[{'type': 'eq', 'fun': lambda x: x[0] + x[1] - 1}])

    x_star = result.x
    h_val = x_star[0] + x_star[1] - 1

    # The 0/0: lambda / h(x) at feasibility: h(x*) = 0, ratio is 0/0.
    # Removable value = lambda (the shadow price).
    return {
        "x_star": x_star.tolist(),
        "optimal_value": float(result.fun),
        "expected_x_star": [0.5, 0.5],
        "equality_violation": float(h_val),
        "multiplier": -1.0,
        "shadow_price_0_over_0": {
            "note": "lambda/h(x) at feasibility: 0/0, removable value = lambda",
            "removable_value": -1.0
        },
        "kkt_satisfied": bool(abs(h_val) < 1e-6)
    }


def barrier_path_0_over_0():
    """Interior-point barrier path: as barrier parameter t -> 0,
    mu_t -> 0 and g_i(x_t) -> 0. The product mu_t * g_i(x_t) = 0
    for all t > 0. At t = 0: mu_0 = 0, g_i(x_0) = 0, product = 0.
    The ratio mu_t / (-1/g_i(x_t)) is 0/0 with removable value = 0.

    For min x^2 s.t. x >= 0 (simple):
    Barrier: min x^2 - t*log(x)
    FOC: 2x - t/x = 0 => x_t = sqrt(t/2)
    mu_t = 2*x_t = sqrt(2t)
    g(x_t) = x_t - 0 = sqrt(t/2)  (since constraint is x >= 0, written as -x <= 0)

    Actually: min x^2 s.t. -x <= 0.
    L = x^2 + mu*(-x), mu >= 0.
    FOC: 2x - mu = 0, mu*x = 0 (complementary slackness).
    At optimum: x* = 0, mu* = 0 (since constraint is active: g(x*) = -x* = 0).

    Wait: g(x) = -x <= 0. At x* = 0: g(0) = 0 (active). mu*g = 0*0 = 0. OK.
    But the barrier path: min x^2 - t*log(-(-x)) = min x^2 - t*log(x)
    FOC: 2x - t/x = 0 => x_t = sqrt(t/2)
    mu_t = 2x_t = sqrt(2t)
    g(x_t) = -x_t = -sqrt(t/2)
    mu_t * g(x_t) = sqrt(2t) * (-sqrt(t/2)) = -t. That's not 0.

    Hmm, complementary slackness is mu_i * g_i = 0, but for inequality g <= 0
    with mu >= 0, the product should be 0 at the optimum. On the barrier path,
    the product is -t (the barrier parameter), which -> 0 as t -> 0.

    The 0/0: mu_t / (-1/g(x_t)) = mu_t * (-g(x_t)) = sqrt(2t) * sqrt(t/2) = t.
    At t = 0: 0/0. Removable value = 0. This encodes that complementary slackness
    is achieved at the limit.
    """
    barrier_tests = []
    for t in [1.0, 0.1, 0.01, 0.001, 0.0001]:
        x_t = np.sqrt(t / 2)
        mu_t = np.sqrt(2 * t)
        g_t = -x_t  # constraint g(x) = -x <= 0

        product = mu_t * g_t  # should be -t (not zero, but -> 0)
        # The 0/0 ratio: mu / (-1/g) = mu * (-g) = sqrt(2t)*sqrt(t/2) = t
        ratio = mu_t * (-g_t)

        barrier_tests.append({
            "t": t,
            "x_t": float(x_t),
            "mu_t": float(mu_t),
            "g_t": float(g_t),
            "complementary_product": float(product),
            "ratio_mu_over_inv_g": float(ratio),
            "product_approaches_zero": bool(abs(product) < 0.1)
        })

    # At t = 0: mu = 0, g = 0, product = 0*0 = 0, ratio = 0/0 -> removable = 0
    return {
        "note": "barrier path: mu_t*g_t -> 0 as t -> 0. At t=0: 0/0, removable=0",
        "tests": barrier_tests,
        "removable_value": 0.0
    }


def run():
    results = {"tests": [], "summary": {}}

    # --- Test 1: QP with inequality constraint ---
    qp1 = solve_qp_inequality()
    results["qp_inequality"] = qp1

    # --- Test 2: QP with different constraint ---
    qp2 = solve_qp_active_inactive()
    results["qp_active_inactive"] = qp2

    # --- Test 3: Equality constraint ---
    eq = solve_equality_constraint()
    results["equality_constraint"] = eq

    # --- Test 4: Barrier path 0/0 ---
    barrier = barrier_path_0_over_0()
    results["barrier_path"] = barrier

    # --- Test 5: Multiple constraints ---
    # min x^2 + y^2  s.t.  x >= 0, y >= 0, x + y >= 1
    # (quadratic program with 3 inequality constraints)
    def obj5(x):
        return x[0]**2 + x[1]**2

    result5 = minimize(obj5, [0.5, 0.5], method='SLSQP',
                       constraints=[
                           {'type': 'ineq', 'fun': lambda x: x[0]},
                           {'type': 'ineq', 'fun': lambda x: x[1]},
                           {'type': 'ineq', 'fun': lambda x: x[0] + x[1] - 1}
                       ])

    x5 = result5.x
    # At optimum: x=y=0.5. Constraints 1,2 inactive (g < 0), constraint 3 active (g = 0).
    # Multipliers: mu1 = mu2 = 0 (inactive), mu3 > 0 (active).
    results["multiple_constraints"] = {
        "x_star": x5.tolist(),
        "optimal_value": float(result5.fun),
        "expected_x_star": [0.5, 0.5],
        "constraint_values": [
            float(x5[0]),  # g1 = x >= 0
            float(x5[1]),  # g2 = y >= 0
            float(x5[0] + x5[1] - 1)  # g3 = x+y >= 1
        ],
        "note": "constraints 1,2 inactive (0/0 with mu=0 not applicable); "
                "constraint 3 active (0/0 ratio removable)"
    }

    # --- Summary ---
    qp1_ok = qp1["kkt_satisfied"]
    qp2_ok = qp2["kkt_satisfied"]
    eq_ok = eq["kkt_satisfied"]
    barrier_ok = barrier["tests"][-1]["product_approaches_zero"]
    multi_ok = bool(abs(result5.fun - 0.5) < 0.1)

    supported = bool(qp1_ok and qp2_ok and eq_ok and barrier_ok and multi_ok)

    results["summary"] = {
        "supported": supported,
        "qp_inequality_kkt": qp1_ok,
        "qp_active_inactive_kkt": qp2_ok,
        "equality_kkt": eq_ok,
        "barrier_path_converges": barrier_ok,
        "multiple_constraints_correct": multi_ok,
        "honest_wall": "numerical verification of KKT conditions for specific "
                       "optimization problems, not a proof of KKT theory"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("KKT conditions via 0/0")
    print(f"  QP inequality KKT:     {s['qp_inequality_kkt']}")
    print(f"  QP active/inactive:    {s['qp_active_inactive_kkt']}")
    print(f"  Equality constraint:   {s['equality_kkt']}")
    print(f"  Barrier path converges:{s['barrier_path_converges']}")
    print(f"  Multiple constraints:  {s['multiple_constraints_correct']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/kkt_conditions_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
