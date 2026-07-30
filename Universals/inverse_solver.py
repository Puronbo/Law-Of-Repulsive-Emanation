"""
Two-constraint inverse solver for the C0 law.

Given two distinct contexts and a candidate C0 value, use Newton's
method to solve for the unique q0 such that V(q0; context_i) = C0
for both contexts simultaneously.

This fixes the inverse problem (Section 8.1 / Item 10 in the audit):
a single V(q) = C0 constraint gives a 1D level curve, not a point.
Two constraints intersect at a unique q0.
"""
import numpy as np

try:
    from manifold.poincare import mobius_add, geodesic_distance
except ImportError:
    def mobius_add(x, y):
        r = np.linalg.norm(x)
        if r >= 1: return x
        return (x + y * (1 + 2 * np.dot(x, y) + r**2)) / (1 + 2 * np.dot(x, y) + r**2 * np.linalg.norm(y)**2)
    def geodesic_distance(x, y):
        return 2 * np.arctanh(np.linalg.norm(mobius_add(-x, y)))


def repulsion_loss(q, context, alpha=2.5):
    """V(q) = sum_i max(0, alpha - d(q, xi))^2"""
    total = 0.0
    for word in context:
        xi = np.array([hash(word) % 1000 / 500 - 1 for _ in range(2)])
        xi = xi / max(np.linalg.norm(xi), 0.01) * 0.9
        d = geodesic_distance(q, xi)
        total += max(0, alpha - d) ** 2
    return total


def repulsion_gradient(q, context, alpha=2.5, eps=1e-6):
    """Numerical gradient of V(q)."""
    g = np.zeros_like(q)
    for i in range(len(q)):
        qp, qm = q.copy(), q.copy()
        qp[i] += eps
        qm[i] -= eps
        g[i] = (repulsion_loss(qp, context, alpha) - repulsion_loss(qm, context, alpha)) / (2 * eps)
    return g


def inverse_solve_two_context(c0, context1, context2, q0_guess=None, method='newton'):
    """
    Solve for q0 such that V(q0; context1) = V(q0; context2) = c0.

    Uses scipy.optimize.fsolve (Newton) or grid search.

    Returns (q0, error, n_evals).
    """
    from scipy.optimize import fsolve

    if q0_guess is None:
        q0_guess = np.zeros(2)

    def f(q):
        v1 = repulsion_loss(q, context1) - c0
        v2 = repulsion_loss(q, context2) - c0
        return np.array([v1, v2])

    if method == 'newton':
        sol, infodict, ier, msg = fsolve(f, q0_guess, full_output=True, xtol=1e-12)
        q0 = sol
        error = np.linalg.norm(f(q0))
        n_evals = infodict['nfev']
        return q0, float(error), int(n_evals)

    # Grid search fallback
    X = np.linspace(-0.99, 0.99, 401)
    best_q, best_err = None, float('inf')
    n_evals = 0
    for x in X:
        for y in X:
            q = np.array([x, y])
            err = np.linalg.norm(f(q))
            n_evals += 2
            if err < best_err:
                best_err = err
                best_q = q
    return best_q, float(best_err), int(n_evals)
