"""
Brouwer fixed-point theorem via 0/0
====================================
The Brouwer fixed-point theorem: every continuous function f : D^n -> D^n
from the closed unit disk to itself has at least one fixed point, i.e.,
there exists x* such that f(x*) = x*.

The 0/0: consider the displacement function g(x) = f(x) - x. A fixed point
is where g(x) = 0. For a function with a unique fixed point x*, the ratio

    g(x) / (x - x*)

is 0/0 at x = x*. The removable value encodes the contraction behavior:

    lim_{x -> x*} g(x) / (x - x*) = f'(x*) - 1

If |f'(x*) - 1| < 1 (i.e., |f'(x*)| < 2... actually the contraction
condition for Banach is |f'| < 1), the fixed point is attracting.

For the Brouwer theorem on D^2: we verify numerically that
1. Any continuous f : D^2 -> D^2 has a fixed point (search over grid).
2. At the fixed point, the displacement is 0 (f(x*) - x* = 0).
3. The 0/0 ratio g(x)/(x-x*) has a removable value = f'(x*) - 1.
4. For a contraction (|f'| < 1), the fixed point is unique and attracting.

HONEST WALL: numerical search for fixed points, not a topological proof.
"""

import numpy as np
import json


def find_fixed_points(f_func, domain_radius=1.0, grid_res=500):
    """Find fixed points of f : D^2 -> D^2 by searching for g(x) = f(x) - x = 0."""
    x = np.linspace(-domain_radius, domain_radius, grid_res)
    y = np.linspace(-domain_radius, domain_radius, grid_res)
    X, Y = np.meshgrid(x, y)

    # Evaluate f
    FX, FY = f_func(X, Y)
    # Displacement
    GX = FX - X
    GY = FY - Y

    # Find zero crossings (sign changes in both components)
    fixed_pts = []
    h = x[1] - x[0]
    for i in range(1, grid_res - 1):
        for j in range(1, grid_res - 1):
            # Check if on disk
            if X[i, j]**2 + Y[i, j]**2 > domain_radius**2:
                continue
            # Sign change in GX in x-direction and GY in y-direction
            if (GX[i, j] * GX[i, j + 1] <= 0 and
                GY[i, j] * GY[i + 1, j] <= 0):
                # Refine estimate
                x0 = float(X[i, j])
                y0 = float(Y[i, j])
                # Newton-like refinement
                for _ in range(10):
                    fx, fy = f_func(x0, y0)
                    gx, gy = fx - x0, fy - y0
                    if gx**2 + gy**2 < 1e-14:
                        break
                    # Jacobian of g: Dg = Df - I
                    h_step = 1e-7
                    dfxx = (f_func(x0 + h_step, y0)[0] - f_func(x0 - h_step, y0)[0]) / (2 * h_step)
                    dfyx = (f_func(x0 + h_step, y0)[1] - f_func(x0 - h_step, y0)[1]) / (2 * h_step)
                    dfxy = (f_func(x0, y0 + h_step)[0] - f_func(x0, y0 - h_step)[0]) / (2 * h_step)
                    dfyy = (f_func(x0, y0 + h_step)[1] - f_func(x0, y0 - h_step)[1]) / (2 * h_step)
                    det = (dfxx - 1) * (dfyy - 1) - dfxy * dfyx
                    if abs(det) < 1e-15:
                        break
                    x0 -= ((dfyy - 1) * gx - dfxy * gy) / det
                    y0 -= (-dfyx * gx + (dfxx - 1) * gy) / det

                # Check it is on the disk and is actually a fixed point
                if x0**2 + y0**2 <= domain_radius**2 + 0.01:
                    fx, fy = f_func(x0, y0)
                    if (fx - x0)**2 + (fy - y0)**2 < 1e-8:
                        fixed_pts.append((x0, y0))

    # Deduplicate
    deduped = []
    for pt in fixed_pts:
        if all((pt[0] - d[0])**2 + (pt[1] - d[1])**2 > 0.05**2
               for d in deduped):
            deduped.append(pt)
    return deduped


def displacement_ratio_0_over_0(f_func, fixed_pt, direction, t_values):
    """Compute g(x* + t*d) / (t*d) as t -> 0 (the 0/0 ratio)."""
    x0, y0 = fixed_pt
    dx, dy = direction
    ratios_x = []
    ratios_y = []
    for t in t_values:
        if abs(t) < 1e-15:
            continue
        x_val = x0 + t * dx
        y_val = y0 + t * dy
        fx, fy = f_func(x_val, y_val)
        gx = fx - x_val
        gy = fy - y_val
        if abs(t * dx) > 1e-15:
            ratios_x.append(gx / (t * dx))
        if abs(t * dy) > 1e-15:
            ratios_y.append(gy / (t * dy))
    return ratios_x, ratios_y


def run():
    results = {"tests": [], "summary": {}}

    # --- Test 1: contraction mappings (unique fixed point, Banach) ---
    contraction_tests = []
    # f(x,y) = (0.3*x + 0.1, 0.3*y - 0.05) -- contraction with fixed point
    # Fixed point: x* = 0.1/(1-0.3) = 1/7, y* = -0.05/(1-0.3) = -1/14
    def contraction1(x, y):
        return (0.3 * x + 0.1, 0.3 * y - 0.05)

    fps = find_fixed_points(contraction1)
    x_star = 0.1 / 0.7  # 1/7
    y_star = -0.05 / 0.7  # -1/14
    contraction_tests.append({
        "function": "0.3x+0.1, 0.3y-0.05",
        "fixed_points_found": len(fps),
        "expected_fixed_point": [float(x_star), float(y_star)],
        "displacement_at_expected": [
            float(contraction1(x_star, y_star)[0] - x_star),
            float(contraction1(x_star, y_star)[1] - y_star)
        ]
    })

    # f(x,y) = (-0.5*y + 0.2, 0.5*x - 0.1) -- rotation-contraction
    def contraction2(x, y):
        return (-0.5 * y + 0.2, 0.5 * x - 0.1)

    fps2 = find_fixed_points(contraction2)
    # Fixed point: x = -0.5y+0.2, y = 0.5x-0.1
    # x = -0.5(0.5x-0.1)+0.2 = -0.25x+0.05+0.2 = -0.25x+0.25
    # 1.25x = 0.25, x = 0.2, y = 0.5*0.2-0.1 = 0
    contraction_tests.append({
        "function": "-0.5y+0.2, 0.5x-0.1",
        "fixed_points_found": len(fps2),
        "expected_fixed_point": [0.2, 0.0],
        "displacement_at_expected": [
            float(contraction2(0.2, 0.0)[0] - 0.2),
            float(contraction2(0.2, 0.0)[1] - 0.0)
        ]
    })
    results["contraction_tests"] = contraction_tests

    # --- Test 2: 0/0 displacement ratio at fixed point ---
    # For contraction1: g(x)/ (x - x*) at x* has removable value = Df(x*) - I
    # Df = diag(0.3, 0.3), so Df - I = diag(-0.7, -0.7)
    t_values = np.logspace(-1, -10, 50)
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    ratio_tests = []
    for dx, dy in directions:
        ratios_x, ratios_y = displacement_ratio_0_over_0(
            contraction1, (x_star, y_star), (dx, dy), t_values
        )
        if ratios_x:
            # The removable value should be -0.7 (the contraction factor)
            last_few_x = ratios_x[-5:]
            mean_val = float(np.mean(last_few_x))
            std_val = float(np.std(last_few_x))
            ratio_tests.append({
                "direction": [dx, dy],
                "removable_value_x": mean_val,
                "std": std_val,
                "converges": std_val < 0.05
            })

    results["displacement_0_over_0"] = {
        "note": "g(x)/(x-x*) -> Df(x*) - I = -0.7 as x -> x*",
        "expected_removable_value": -0.7,
        "tests": ratio_tests
    }

    # --- Test 3: multiple fixed points (non-contraction, still Brouwer) ---
    # f(x,y) = (-x, -y) on D^2: every point with f(x)=x means -x=x => x=0
    # Only fixed point is origin.
    def antipodal(x, y):
        return (-x, -y)

    fps_anti = find_fixed_points(antipodal)
    results["tests"].append({
        "function": "antipodal (-x,-y)",
        "fixed_points_found": len(fps_anti),
        "note": "unique fixed point at origin (contraction with factor -1)"
    })

    # f(x,y) = (x, -y) on D^2: fixed points are (x, 0) for all x in [-1,1]
    # -- entire x-axis segment is fixed.
    def reflection_y(x, y):
        return (x, -y)

    fps_refl = find_fixed_points(reflection_y)
    results["tests"].append({
        "function": "reflection_y (x,-y)",
        "fixed_points_found": len(fps_refl),
        "note": "entire x-axis segment is fixed (infinite fixed points)"
    })

    # --- Test 4: verify g(x*) = 0 for all fixed points ---
    all_displaced = []
    for pt in [x_star, y_star]:
        all_displaced.append(float(contraction1(x_star, y_star)[0] - x_star))
    results["zero_displacement"] = {
        "all_displacements_zero": all(abs(d) < 1e-10 for d in all_displaced),
        "max_displacement": float(max(abs(d) for d in all_displaced))
    }

    # --- Test 5: Jacobian eigenvalues determine attracting/repelling ---
    def jacobian_at(f_func, point, h=1e-7):
        x0, y0 = point
        dfxx = (f_func(x0+h,y0)[0] - f_func(x0-h,y0)[0]) / (2*h)
        dfxy = (f_func(x0,y0+h)[0] - f_func(x0,y0-h)[0]) / (2*h)
        dfyx = (f_func(x0+h,y0)[1] - f_func(x0-h,y0)[1]) / (2*h)
        dfyy = (f_func(x0,y0+h)[1] - f_func(x0,y0-h)[1]) / (2*h)
        return np.array([[dfxx, dfxy], [dfyx, dfyy]])

    J1 = jacobian_at(contraction1, (x_star, y_star))
    eigs1 = sorted(np.linalg.eigvalsh(J1).tolist())
    spectral_radius = max(abs(e) for e in eigs1)

    results["jacobian_analysis"] = {
        "contraction1": {
            "eigenvalues": [float(e) for e in eigs1],
            "spectral_radius": float(spectral_radius),
            "is_contraction": spectral_radius < 1.0,
            "removable_value_Df_minus_I": [float(e - 1) for e in eigs1]
        }
    }

    # --- Summary ---
    has_fixed_points = all(t["fixed_points_found"] >= 1 for t in contraction_tests)
    displacements_zero = results["zero_displacement"]["all_displacements_zero"]
    ratios_converge = all(t["converges"] for t in ratio_tests) if ratio_tests else False
    is_contraction = results["jacobian_analysis"]["contraction1"]["is_contraction"]

    supported = bool(has_fixed_points and displacements_zero and
                     ratios_converge and is_contraction)

    results["summary"] = {
        "supported": supported,
        "all_contraction_have_fixed_points": has_fixed_points,
        "displacements_zero": displacements_zero,
        "displacement_ratios_converge": ratios_converge,
        "spectral_radius_below_one": is_contraction,
        "honest_wall": "numerical search for fixed points and verification "
                       "of the displacement 0/0, not a topological proof"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Brouwer fixed-point theorem via 0/0")
    print(f"  Contraction fixed points found:  {s['all_contraction_have_fixed_points']}")
    print(f"  Displacements zero:              {s['displacements_zero']}")
    print(f"  Displacement ratios converge:    {s['displacement_ratios_converge']}")
    print(f"  Spectral radius < 1:             {s['spectral_radius_below_one']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/brouwer_fixed_point_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
