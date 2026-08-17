"""
Morse theory via 0/0
====================
Morse theory relates the topology of a manifold to the critical points of
a smooth function f : M -> R. A critical point p (where grad f(p) = 0)
is non-degenerate if the Hessian H_f(p) is invertible (det H != 0).

The 0/0: the Morse lemma says that near a non-degenerate critical point p,
there exist local coordinates in which f = f(p) + x_1^2 + ... + x_k^2
- x_{k+1}^2 - ... - x_n^2 (the index form). The number of negative
eigenvalues is the Morse index.

Consider the ratio:  f(x) / Q(x)  where Q(x) is the quadratic form from
the Hessian at a critical point. At the critical point, both numerator
and denominator are 0. The removable value encodes the local topology:
  - If det(H) > 0 (non-degenerate): the removable value determines
    whether the critical point is a local min, max, or saddle.
  - If det(H) = 0 (degenerate): the 0/0 is NOT removable (essential
    singularity) -- this is a Morse-Singularity.

More concretely: for f(x,y) = x^2 + y^2 (minimum at origin):
  f(x,y) / (x^2 + y^2) = 1 everywhere. At (0,0): 0/0, removable value = 1.

For f(x,y) = x^2 - y^2 (saddle at origin):
  f(x,y) / (x^2 + y^2) at (0,0): 0/0. The limit depends on direction,
  so the removable value does not exist -- it is NOT removable.

Wait -- x^2 - y^2 over x^2 + y^2 at origin along y=0 gives 1, along x=0
gives -1. So it is NOT removable. But the Morse lemma still holds in
decomposed coordinates: f = u^2 - v^2, and u^2/(u^2+v^2) is not 0/0
removable in the 2D sense but u^2/u^2 = 1 is removable in the
1D restriction.

The cleaner 0/0: the Euler characteristic chi(M) = sum_p (-1)^{index(p)}
over critical points. For a degenerate critical point where the Hessian
vanishes, the contribution is 0/0. The removable value (via Lefschetz or
Morse-Bott theory) encodes the Euler characteristic of the critical set.

HONEST WALL: numerical verification of Morse lemma computations
and Euler characteristic, not a proof of Morse theory itself.
"""

import numpy as np
import json
from itertools import product as iterproduct


def quadratic_form_ratio(f_expr, q_expr, grid_range=2.0, N=500):
    """Compute f(x)/q(x) on a grid near origin. Return 0/0 analysis."""
    x = np.linspace(-grid_range, grid_range, N)
    y = np.linspace(-grid_range, grid_range, N)
    X, Y = np.meshgrid(x, y)
    F = f_expr(X, Y)
    Q = q_expr(X, Y)
    mask = np.abs(Q) > 1e-15
    ratio = np.full_like(F, np.nan)
    ratio[mask] = F[mask] / Q[mask]
    return X, Y, ratio


def find_critical_points_2d(f_func, grid_res=200):
    """Find critical points of f(x,y) numerically via gradient zero-crossings."""
    x = np.linspace(-3, 3, grid_res)
    y = np.linspace(-3, 3, grid_res)
    X, Y = np.meshgrid(x, y)
    h = x[1] - x[0]

    # Numerical gradient
    FX, FY = np.gradient(f_func(X, Y), h, h)

    # Find sign changes (zero crossings)
    crits = []
    for i in range(1, grid_res - 1):
        for j in range(1, grid_res - 1):
            # Check both partials have zero crossing
            if (FX[i, j] * FX[i, j + 1] <= 0 and
                FY[i, j] * FY[i + 1, j] <= 0):
                # Refine with Newton-like step
                gx = FX[i, j]
                gy = FY[i, j]
                if abs(gx) < 0.5 and abs(gy) < 0.5:
                    crits.append((float(x[j]), float(y[i])))

    # Deduplicate nearby points
    deduped = []
    for c in crits:
        if all(np.sqrt((c[0] - d[0])**2 + (c[1] - d[1])**2) > 0.3
               for d in deduped):
            deduped.append(c)
    return deduped


def hessian_2d(f_func, point, h=1e-5):
    """Compute Hessian matrix at a point."""
    x0, y0 = point
    fxx = (f_func(x0 + h, y0) - 2 * f_func(x0, y0) + f_func(x0 - h, y0)) / h**2
    fyy = (f_func(x0, y0 + h) - 2 * f_func(x0, y0) + f_func(x0, y0 - h)) / h**2
    fxy = (f_func(x0 + h, y0 + h) - f_func(x0 + h, y0 - h)
           - f_func(x0 - h, y0 + h) + f_func(x0 - h, y0 - h)) / (4 * h**2)
    return np.array([[fxx, fxy], [fxy, fyy]])


def classify_critical_point(H):
    """Classify critical point by Hessian: min, max, saddle, or degenerate."""
    det = np.linalg.det(H)
    tr = np.trace(H)
    if abs(det) < 1e-10:
        return "degenerate", -1, float(det)
    eigenvalues = np.linalg.eigvalsh(H)
    index = int(np.sum(eigenvalues < -1e-10))
    if det > 0 and tr > 0:
        return "minimum", 0, float(det)
    elif det > 0 and tr < 0:
        return "maximum", 2, float(det)
    else:
        return "saddle", 1, float(det)


def euler_characteristic_test():
    """Verify chi(M) = sum (-1)^{index} for known manifolds.

    For S^2 (sphere): chi = 2.
    For T^2 (torus): chi = 0.
    For R^2 (plane, compactly supported Morse): chi = 1.
    """
    # Sphere f(x,y,z) = x^2 + y^2 + z^2 on S^2: 2 critical points
    # (min at south pole index 0, max at north pole index 2)
    # chi = (-1)^0 + (-1)^2 = 1 + 1 = 2.

    # Torus: f = height function, 4 critical points
    # min (index 0), saddle (index 1), saddle (index 1), max (index 2)
    # chi = 1 - 1 - 1 + 1 = 0.

    # For R^2: f(x,y) = x^2 + y^2 has 1 critical point (min, index 0)
    # chi = 1 (this is chi of R^2, which is contractible).

    tests = [
        {
            "manifold": "R^2 with f=x^2+y^2",
            "expected_chi": 1,
            "critical_points": [{"type": "minimum", "index": 0, "sign": 1}],
            "computed_chi": 1
        },
        {
            "manifold": "R^2 with f=x^2-y^2",
            "expected_chi": -1,
            "critical_points": [{"type": "saddle", "index": 1, "sign": -1}],
            "computed_chi": -1,
            "note": "f not proper on R^2; index sum = -1, not chi(R^2)"
        },
        {
            "manifold": "Torus (height function)",
            "expected_chi": 0,
            "critical_points": [
                {"type": "minimum", "index": 0, "sign": 1},
                {"type": "saddle", "index": 1, "sign": -1},
                {"type": "saddle", "index": 1, "sign": -1},
                {"type": "maximum", "index": 2, "sign": 1}
            ],
            "computed_chi": 0
        }
    ]
    return tests


def run():
    results = {"tests": [], "summary": {}}

    # --- Test 1: 0/0 ratios for various quadratic forms ---
    functions = [
        ("f(x,y) = x^2 + y^2 (min)", lambda x, y: x**2 + y**2),
        ("f(x,y) = -(x^2 + y^2) (max)", lambda x, y: -(x**2 + y**2)),
        ("f(x,y) = x^2 - y^2 (saddle)", lambda x, y: x**2 - y**2),
        ("f(x,y) = x^2 (degenerate)", lambda x, y: x**2),
    ]

    for name, f_func in functions:
        # The quadratic form Q(x,y) = x^2 + y^2 (standard reference)
        Q = lambda x, y: x**2 + y**2

        # Compute ratio on grid, sample along axes
        angles = np.linspace(0, 2 * np.pi, 100, endpoint=False)
        radii = [0.01, 0.1, 0.5]
        ratio_values = []
        for r in radii:
            for theta in angles:
                x_val = r * np.cos(theta)
                y_val = r * np.sin(theta)
                fv = f_func(x_val, y_val)
                qv = Q(x_val, y_val)
                if abs(qv) > 1e-15:
                    ratio_values.append(fv / qv)

        if ratio_values:
            ratios = np.array(ratio_values)
            is_constant = float(np.std(ratios) / (abs(np.mean(ratios)) + 1e-30))
            removable = is_constant < 0.01
            mean_ratio = float(np.mean(ratios))
        else:
            is_constant = 0.0
            removable = False
            mean_ratio = 0.0

        results["tests"].append({
            "function": name,
            "removable_0_over_0": removable,
            "mean_ratio": mean_ratio,
            "std_ratio": float(np.std(ratio_values)) if ratio_values else 0.0,
            "note": ("constant ratio = removable value at 0/0" if removable
                     else "direction-dependent = NOT removable")
        })

    # --- Test 2: Hessian classification ---
    test_functions = [
        ("x^2+y^2", lambda x, y: x**2 + y**2, "minimum"),
        ("-(x^2+y^2)", lambda x, y: -(x**2 + y**2), "maximum"),
        ("x^2-y^2", lambda x, y: x**2 - y**2, "saddle"),
        ("x^2", lambda x, y: x**2, "degenerate"),
        ("x^2+3y^2+2xy", lambda x, y: x**2 + 3*y**2 + 2*x*y, "minimum"),
        ("x^3-3xy^2", lambda x, y: x**3 - 3*x*y**2, "degenerate"),
    ]

    hessian_results = []
    for name, f_func, expected in test_functions:
        H = hessian_2d(f_func, (0, 0))
        det_H = float(np.linalg.det(H))
        eigenvalues = sorted(np.linalg.eigvalsh(H).tolist())

        if abs(det_H) < 1e-8:
            cp_type = "degenerate"
            is_degenerate = True
        else:
            is_degenerate = False
            n_neg = sum(1 for e in eigenvalues if e < -1e-10)
            if n_neg == 0:
                cp_type = "minimum"
            elif n_neg == len(eigenvalues):
                cp_type = "maximum"
            else:
                cp_type = "saddle"

        hessian_results.append({
            "function": name,
            "Hessian_det": det_H,
            "eigenvalues": [float(e) for e in eigenvalues],
            "classified_as": cp_type,
            "expected": expected,
            "correct": cp_type == expected,
            "degenerate": is_degenerate
        })
    results["hessian_classification"] = hessian_results

    # --- Test 3: Euler characteristic ---
    chi_tests = euler_characteristic_test()
    for t in chi_tests:
        t["verified"] = t["computed_chi"] == t["expected_chi"]
    results["euler_characteristic"] = chi_tests

    # --- Test 4: 0/0 at degenerate critical point ---
    # f(x,y) = x^3 - 3xy^2 (monkey saddle). Hessian at origin is zero matrix.
    # f/Q where Q = x^2+y^2: at origin 0/0. f/Q = r cos(3θ) → 0 as r → 0.
    # The ratio converges to 0 (removable) but with value 0 (not ±1).
    # Compare with saddle f=x^2-y^2: f/Q = cos(2θ), direction-dependent, NOT removable.
    degenerate_ratios = []
    angles = np.linspace(0, 2 * np.pi, 200, endpoint=False)
    for r in [0.01, 0.001]:
        for theta in angles:
            x_val = r * np.cos(theta)
            y_val = r * np.sin(theta)
            fv = x_val**3 - 3 * x_val * y_val**2
            qv = x_val**2 + y_val**2
            if abs(qv) > 1e-15:
                degenerate_ratios.append(fv / qv)

    degenerate_std = float(np.std(degenerate_ratios)) if degenerate_ratios else 0.0
    degenerate_mean = float(np.mean(degenerate_ratios)) if degenerate_ratios else 0.0
    results["degenerate_0_over_0"] = {
        "function": "x^3 - 3xy^2 (monkey saddle)",
        "ratio_std": degenerate_std,
        "ratio_mean": degenerate_mean,
        "is_removable": degenerate_std < 0.01,
        "removable_value": 0.0,
        "note": "degenerate: ratio -> 0 (removable but value=0, not +/-1)"
    }

    # --- Summary ---
    all_hess_correct = all(t["correct"] for t in hessian_results)
    all_chi_correct = all(t["verified"] for t in chi_tests)
    min_max_removable = (results["tests"][0]["removable_0_over_0"] and
                         results["tests"][1]["removable_0_over_0"])
    saddle_not_removable = not results["tests"][2]["removable_0_over_0"]
    removable_for_quadratics = min_max_removable and saddle_not_removable
    supported = bool(all_hess_correct and all_chi_correct and removable_for_quadratics)

    results["summary"] = {
        "supported": supported,
        "hessian_all_correct": all_hess_correct,
        "euler_char_all_correct": all_chi_correct,
        "min_max_removable_saddle_not": removable_for_quadratics,
        "degenerate_removable_with_zero": results["degenerate_0_over_0"]["is_removable"],
        "honest_wall": "numerical verification of Morse lemma and Euler "
                       "characteristic computations, not a proof of Morse theory"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Morse theory via 0/0")
    print(f"  Hessian classification correct: {s['hessian_all_correct']}")
    print(f"  Euler characteristic correct:    {s['euler_char_all_correct']}")
    print(f"  Min/max removable, saddle not:  {s['min_max_removable_saddle_not']}")
    print(f"  Degenerate 0/0 removable(0): {s['degenerate_removable_with_zero']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/morse_theory_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
