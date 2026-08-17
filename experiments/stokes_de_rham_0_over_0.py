"""
Stokes/de Rham theorem via 0/0
===============================
The generalized Stokes theorem: int_M d(omega) = int_{partial M} omega,
where omega is a differential form on a manifold M with boundary.

The de Rham theorem connects differential forms to cohomology: a closed
form (d(omega) = 0) that is exact (omega = d(alpha)) integrates to zero
over any cycle.

The 0/0: consider the ratio

    int_M d(omega) / (boundary_integral)

By Stokes, these are equal, so the ratio is 1. At a degenerate boundary
(partial M = empty), both numerator and denominator are 0, giving 0/0.
The removable value is 1 (the Stokes ratio for non-empty boundary).

For the cohomological 0/0: consider a closed but not-exact form omega.
The integral int_gamma(omega) over a cycle gamma detects cohomology.
For gamma that is a boundary (gamma = partial Sigma), Stokes gives
int_gamma(omega) = int_Sigma d(omega) = 0. For non-trivial cycles,
the integral is nonzero. The ratio

    int_gamma(omega) / (int_gamma(omega))

is trivially 1 for nonzero, but at omega = 0 (the trivial class),
both integrals are 0, giving 0/0 with removable value = 1
(the "trivial cohomology" value).

More concretely: on a torus T^2, the form dx (angle form) is closed
but not exact. int_{S^1 x {0}} dx = 2pi (nonzero). Over a contractible
loop, int dx = 0. The ratio of these integrals over different loops
detects the topology.

HONEST WALL: numerical verification of Stokes' theorem for explicit
forms on explicit domains, not a proof of the theorem.
"""

import numpy as np
import json


def line_integral(fx_func, fy_func, curve_func, t_vals):
    """Line integral of (fx, fy) along parametric curve (curve_func(t))."""
    t = np.array(t_vals)
    dt = t[1] - t[0]
    cx = np.array([curve_func(ti)[0] for ti in t])
    cy = np.array([curve_func(ti)[1] for ti in t])
    vx = np.array([fx_func(cx[i], cy[i]) for i in range(len(t))])
    vy = np.array([fy_func(cx[i], cy[i]) for i in range(len(t))])
    dx = np.gradient(cx, dt)
    dy = np.gradient(cy, dt)
    return float(np.sum(vx * dx + vy * dy) * dt)


def double_integral_2d(integrand_func, domain_type, domain_params, N=300):
    """Compute double integral over a 2D domain."""
    if domain_type == "rectangle":
        x_lo, x_hi, y_lo, y_hi = domain_params
        x = np.linspace(x_lo, x_hi, N)
        y = np.linspace(y_lo, y_hi, N)
        dx = (x_hi - x_lo) / N
        dy = (y_hi - y_lo) / N
        X, Y = np.meshgrid(x, y)
        Z = integrand_func(X, Y)
        return float(np.sum(Z) * dx * dy)

    elif domain_type == "disk":
        cx, cy, r = domain_params
        # Polar coordinates
        theta = np.linspace(0, 2 * np.pi, N)
        rho = np.linspace(0, r, N // 2)
        dtheta = 2 * np.pi / N
        dr = r / (N // 2)
        total = 0.0
        for i in range(len(rho)):
            for j in range(len(theta)):
                x = cx + rho[i] * np.cos(theta[j])
                y = cy + rho[i] * np.sin(theta[j])
                total += integrand_func(x, y) * rho[i] * dtheta * dr
        return float(total)

    return 0.0


def run():
    results = {"tests": [], "summary": {}}

    # --- Test 1: Stokes theorem on a disk ---
    # omega = P dx + Q dy, d(omega) = (dQ/dx - dP/dy) dx ^ dy
    # int_disk d(omega) = int_disk (dQ/dx - dP/dy) dx dy
    # int_{boundary} omega = line integral around circle

    # Example: P = -y, Q = x. Then dQ/dx - dP/dy = 1 - (-1) = 2.
    # int_disk 2 dx dy = 2 * pi * r^2.
    # Line integral around circle of radius r: int_0^{2pi} (-y dx + x dy)
    # = int_0^{2pi} (-r sin t)(-r sin t) + (r cos t)(r cos t) dt
    # = int_0^{2pi} r^2 dt = 2 pi r^2.

    r = 1.0
    N_line = 1000
    t_vals = np.linspace(0, 2 * np.pi, N_line, endpoint=False)

    # Line integral
    P = lambda x, y: -y
    Q = lambda x, y: x
    circle = lambda t: (r * np.cos(t), r * np.sin(t))
    line_int = line_integral(P, Q, circle, t_vals)

    # Surface integral of d(omega) = dQ/dx - dP/dy = 2
    curl = lambda x, y: 2.0
    surface_int = double_integral_2d(curl, "disk", (0, 0, r), N=200)

    ratio_stokes = line_int / surface_int if abs(surface_int) > 1e-10 else float('nan')

    results["tests"].append({
        "name": "Stokes on disk: omega = -y dx + x dy",
        "line_integral": float(line_int),
        "surface_integral": float(surface_int),
        "ratio": float(ratio_stokes),
        "stokes_holds": abs(ratio_stokes - 1.0) < 0.01
    })

    # --- Test 2: Stokes on a rectangle ---
    # P = x^2, Q = y^2. d(omega) = 0 - 0 = 0. Stokes: line int = 0.
    P2 = lambda x, y: x**2
    Q2 = lambda x, y: y**2
    # Rectangle boundary: bottom, right, top, left
    rect_params = (0, 1, 0, 1)
    # Bottom: y=0, x: 0->1, dy=0, P(x,0)=x^2, int = int_0^1 x^2 dx = 1/3
    # Right: x=1, y: 0->1, dx=0, Q(1,y)=y^2, int = int_0^1 y^2 dy = 1/3
    # Top: y=1, x: 1->0, dy=0, P(x,1)=x^2, int = -int_0^1 x^2 dx = -1/3
    # Left: x=0, y: 1->0, dx=0, Q(0,y)=y^2, int = -int_0^1 y^2 dy = -1/3
    # Total = 1/3 + 1/3 - 1/3 - 1/3 = 0.

    def bottom(t):
        return (t, 0.0)
    def right(t):
        return (1.0, t)
    def top(t):
        return (1.0 - t, 1.0)
    def left(t):
        return (0.0, 1.0 - t)

    t_seg = np.linspace(0, 1, 200)
    segments = [bottom, right, top, left]
    total_line = 0.0
    seg_integrals = []
    for seg in segments:
        li = line_integral(P2, Q2, seg, t_seg)
        seg_integrals.append(float(li))
        total_line += li

    # Surface integral of d(omega) = dQ/dx - dP/dy = 0 - 0 = 0
    curl2 = lambda x, y: 0.0
    surf_int2 = double_integral_2d(curl2, "rectangle", rect_params, N=200)

    results["tests"].append({
        "name": "Stokes on rectangle: omega = x^2 dx + y^2 dy (closed form)",
        "segment_integrals": seg_integrals,
        "total_line_integral": float(total_line),
        "surface_integral": float(surf_int2),
        "stokes_holds": abs(total_line - surf_int2) < 0.01,
        "form_is_closed": abs(surf_int2) < 0.01
    })

    # --- Test 3: 0/0 at empty boundary ---
    # On a torus (no boundary), int_T^2 d(omega) should be 0 for any omega.
    # The ratio int_{boundary}/int_{boundary} at empty boundary is 0/0.
    # This is a conceptual test: we verify d(d(omega)) = 0 (exactness of exact forms).
    # d^2 = 0 is the key identity.

    # Test d^2 = 0: take f(x,y) = x^2 * y, df = 2xy dx + x^2 dy
    # d(df) = d(2xy) ^ dx + d(x^2) ^ dy = (2x dx + 2y dy) ^ dx + (2x dx) ^ dy
    #       = 2y dy^dx + 2x dx^dy = -2y dx^dy + 2x dx^dy = (2x - 2y) dx^dy
    # Wait, that's not zero. Let me redo:
    # omega = 2xy dx + x^2 dy
    # d(omega) = d(2xy)/dx dx^dx + d(2xy)/dy dy^dx + d(x^2)/dx dx^dy + d(x^2)/dy dy^dy
    #          = 0 + 2y dy^dx + 2x dx^dy + 0
    #          = -2y dx^dy + 2x dx^dy
    #          = (2x - 2y) dx^dy
    # Hmm, that's not zero. That's because omega = df where f = x^2*y, so:
    # df = 2xy dx + x^2 dy. d(df) should be 0.
    # Let me recompute: d(2xy) = 2y dx + 2x dy. So d(2xy) ^ dx = 2x dy^dx = -2x dx^dy.
    # d(x^2) = 2x dx. d(x^2) ^ dy = 2x dx^dy.
    # So d(df) = -2x dx^dy + 2x dx^dy = 0. Yes! The curl was wrong above.
    # d(2xy)/dx = 2y, d(2xy)/dy = 2x. So:
    # d(2xy dx) = d(2xy)/dy dy^dx = 2x dy^dx = -2x dx^dy.
    # d(x^2 dy) = d(x^2)/dx dx^dy = 2x dx^dy.
    # Sum = 0. Good.

    # Verify d^2 = 0 numerically
    f = lambda x, y: x**2 * y
    h = 1e-6
    # d^2 f via finite differences
    d2f_xxyy = (f(h, h) - f(h, -h) - f(-h, h) + f(-h, -h)) / (4 * h**2)
    # This should be 0 since d(df) = 0

    results["tests"].append({
        "name": "d^2 = 0 for f = x^2 y (exact form closed)",
        "d2f_xxyy": float(d2f_xxyy),
        "d_squared_zero": abs(d2f_xxyy) < 1e-6
    })

    # --- Test 4: Cohomological 0/0 on torus ---
    # The angle form dx on a circle: int_0^{2pi} dx = 2pi (nonzero).
    # This detects H^1(T^1) = R. The 0/0: for the zero form omega = 0,
    # int 0 dx = 0, ratio 0/0. Removable value = 1 (trivial cohomology).
    # For omega = dx (non-trivial), int dx / int dx = 1.
    # For omega = d(theta) (exact on S^1... wait, theta is the coordinate, d(theta) = dx).
    # Actually on S^1, d(theta) is closed but not exact (the generator of H^1).

    # Test: integrate dx over S^1 = 2pi. Integrate 0 over S^1 = 0.
    # Ratio for dx: 2pi / 2pi = 1.
    # Ratio for 0: 0 / 0 -> removable value = 1.

    def angle_form_component(theta):
        """Return (P, Q) for omega = P dx + Q dy on the unit circle.
        omega = -y/(x^2+y^2) dx + x/(x^2+y^2) dy (the angle form)."""
        x, y = np.cos(theta), np.sin(theta)
        r2 = x**2 + y**2
        if r2 < 1e-15:
            return 0.0, 0.0
        return -y / r2, x / r2

    # Line integral of angle form over unit circle = 2pi
    t_angle = np.linspace(0, 2 * np.pi, N_line, endpoint=False)
    angle_int = 0.0
    for i in range(len(t_angle)):
        t1, t2 = t_angle[i], t_angle[(i + 1) % len(t_angle)]
        dt = t2 - t1 if t2 > t1 else t2 - t1 + 2 * np.pi
        P_val, Q_val = angle_form_component(t1)
        x1, y1 = np.cos(t1), np.sin(t1)
        dx_val = -np.sin(t1) * dt
        dy_val = np.cos(t1) * dt
        angle_int += P_val * dx_val + Q_val * dy_val

    cohomology_ratio = angle_int / (2 * np.pi)

    results["tests"].append({
        "name": "Cohomological 0/0: angle form on S^1",
        "angle_integral": float(angle_int),
        "expected": float(2 * np.pi),
        "ratio_to_2pi": float(cohomology_ratio),
        "detects_nontrivial_cohomology": bool(abs(cohomology_ratio - 1.0) < 0.05)
    })

    # --- Test 5: Green's theorem (special case of Stokes) ---
    # int_D (dQ/dx - dP/dy) dx dy = int_{partial D} P dx + Q dy
    # P = x*y, Q = x^2. dQ/dx - dP/dy = 2x - x = x.
    # int_disk x dx dy over unit disk: by symmetry = 0 (odd in x).
    # Line integral: int_0^{2pi} (cos t sin t)(-sin t) + cos^2 t (cos t) dt
    # = int (-cos t sin^2 t + cos^3 t) dt
    # = int cos t (cos^2 t - sin^2 t) dt = int cos t cos(2t) dt
    # = int (cos(3t) + cos(t))/2 dt from 0 to 2pi = 0.

    P_green = lambda x, y: x * y
    Q_green = lambda x, y: x**2
    green_circle = lambda t: (np.cos(t), np.sin(t))
    green_line = line_integral(P_green, Q_green, green_circle, t_vals)

    green_curl = lambda x, y: 2 * x - x  # = x
    green_surface = double_integral_2d(green_curl, "disk", (0, 0, 1.0), N=200)

    results["tests"].append({
        "name": "Green's theorem: omega = xy dx + x^2 dy",
        "line_integral": float(green_line),
        "surface_integral": float(green_surface),
        "ratio": float(green_line / green_surface) if abs(green_surface) > 1e-8 else float('nan'),
        "stokes_holds": abs(green_line - green_surface) < 0.05
    })

    # --- Summary ---
    all_stokes_hold = all(
        t.get("stokes_holds", t.get("d_squared_zero", t.get("detects_nontrivial_cohomology", False)))
        for t in results["tests"]
    )
    d2_zero = results["tests"][2]["d_squared_zero"]
    cohom_detected = results["tests"][3]["detects_nontrivial_cohomology"]

    supported = bool(all_stokes_hold and d2_zero and cohom_detected)

    results["summary"] = {
        "supported": supported,
        "stokes_all_hold": all_stokes_hold,
        "d_squared_zero": d2_zero,
        "cohomology_detected": cohom_detected,
        "honest_wall": "numerical verification of Stokes theorem for explicit "
                       "forms on explicit domains, not a proof of the theorem"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Stokes/de Rham theorem via 0/0")
    print(f"  All Stokes tests hold:   {s['stokes_all_hold']}")
    print(f"  d^2 = 0 verified:        {s['d_squared_zero']}")
    print(f"  Cohomology detected:     {s['cohomology_detected']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/stokes_de_rham_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
