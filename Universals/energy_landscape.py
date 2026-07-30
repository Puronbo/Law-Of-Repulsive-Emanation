"""
energy_landscape.py
===================
Analyze the energy landscape V(q) on the Poincare disk.

The repulsion potential V(q) defines a gradient flow on the Poincare disk.
The origin is an unstable fixed point (source), the boundary is an
attractor (sink). Morse theory connects the topology of sublevel sets
to the critical points.

Connections: Morse theory, gradient flow, dynamical systems, the
Poincare-Hopf theorem (index sum = Euler characteristic).
"""

import numpy as np, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from hamiltonian_flow import repulsion_loss, repulsion_gradient, inverse_metric, POSITIONS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def compute_gradient_field(
    context: list[str],
    alpha: float = 2.5,
    grid: int = 25
) -> dict:
    """Compute V(q) and grad V on a grid for contour visualization."""
    xs = np.linspace(-0.9, 0.9, grid)
    ys = np.linspace(-0.9, 0.9, grid)
    field = {"x": xs.tolist(), "y": ys.tolist(), "V": [], "grad_x": [], "grad_y": [], "grad_norm": []}

    for j in range(grid):
        v_row = []
        gx_row = []
        gy_row = []
        gn_row = []
        for i in range(grid):
            q = np.array([xs[i], ys[j]])
            if np.linalg.norm(q) >= 0.95:
                v_row.append(None)
                gx_row.append(None)
                gy_row.append(None)
                gn_row.append(None)
            else:
                v_row.append(round(float(repulsion_loss(q, context, alpha)), 6))
                g = repulsion_gradient(q, context, alpha)
                gx_row.append(round(float(g[0]), 6))
                gy_row.append(round(float(g[1]), 6))
                gn_row.append(round(float(np.linalg.norm(g)), 6))
        field["V"].append(v_row)
        field["grad_x"].append(gx_row)
        field["grad_y"].append(gy_row)
        field["grad_norm"].append(gn_row)
    return field


def radial_scan(context: list[str], alpha: float = 2.5, n_theta: int = 36, n_r: int = 30) -> dict:
    """Scan V(q) along rays from origin to boundary."""
    thetas = np.linspace(0, 2 * np.pi, n_theta, endpoint=False)
    rs = np.linspace(0.01, 0.95, n_r)
    v_vals = np.zeros((n_theta, n_r))
    g_norms = np.zeros((n_theta, n_r))

    for ti, th in enumerate(thetas):
        for ri in range(n_r):
            q = np.array([rs[ri] * np.cos(th), rs[ri] * np.sin(th)])
            v_vals[ti, ri] = repulsion_loss(q, context, alpha)
            g_norms[ti, ri] = float(np.linalg.norm(repulsion_gradient(q, context, alpha)))

    return {
        "thetas": thetas.tolist(),
        "radii": rs.tolist(),
        "V_mean": [round(float(v_vals.mean(axis=0)[ri]), 6) for ri in range(n_r)],
        "V_min": [round(float(v_vals.min(axis=0)[ri]), 6) for ri in range(n_r)],
        "V_max": [round(float(v_vals.max(axis=0)[ri]), 6) for ri in range(n_r)],
        "grad_mean": [round(float(g_norms.mean(axis=0)[ri]), 6) for ri in range(n_r)],
    }


def hessian_at(q: np.ndarray, context: list[str], alpha: float = 2.5, eps: float = 1e-5) -> np.ndarray:
    """Numerical Hessian of V(q) via central differences."""
    H = np.zeros((2, 2))
    for i in range(2):
        qp = q.copy()
        qm = q.copy()
        qp[i] += eps
        qm[i] -= eps
        gp = repulsion_gradient(qp, context, alpha)
        gm = repulsion_gradient(qm, context, alpha)
        H[:, i] = (gp - gm) / (2 * eps)
    return H


def run(context: list[str] | None = None, alpha: float = 2.5):
    """Map the energy landscape."""
    if context is None:
        context = ['Tech', 'Silicon']

    print(f"\n[ENERGY LANDSCAPE] V(q) on the Poincar\u00e9 disk")
    print(f"  Context: {context}, alpha={alpha}")

    # Radial profile
    radial = radial_scan(context, alpha)
    print(f"  Radial scan: {len(radial['radii'])} radii x {len(radial['thetas'])} angles")
    print(f"  V at origin: {radial['V_mean'][0]:.4f}")
    print(f"  V near boundary: {radial['V_mean'][-1]:.4f}")
    print(f"  |grad| at origin: {radial['grad_mean'][0]:.4f}")
    print(f"  |grad| near boundary: {radial['grad_mean'][-1]:.4f}")

    # Gradient field for dashboard
    field = compute_gradient_field(context, alpha, grid=25)
    gn_vals = [v for row in field["grad_norm"] for v in row if v is not None]
    max_grad = max(gn_vals) if gn_vals else 0
    print(f"  Gradient field: {(len(field['x']), len(field['y']))} grid, max |grad|={max_grad:.2f}")

    # Hessian at select key points
    key_points = {
        "origin": np.array([0.0, 0.0]),
        "mid_NE": np.array([0.4, 0.4]),
        "mid_E": np.array([0.5, 0.0]),
    }
    hessian_data = {}
    for name, q in key_points.items():
        H = hessian_at(q, context, alpha)
        evals = np.linalg.eigvalsh(H)
        morse_index = sum(1 for ev in evals if ev < -1e-6)
        hessian_data[name] = {
            "q": [float(q[0]), float(q[1])],
            "V": round(float(repulsion_loss(q, context, alpha)), 6),
            "grad_norm": round(float(np.linalg.norm(repulsion_gradient(q, context, alpha))), 6),
            "hessian_evals": [round(float(ev), 6) for ev in evals],
            "morse_index": morse_index,
            "type": ["local min", "saddle", "local max"][morse_index] if morse_index < 3 else "degenerate",
        }
        print(f"  {name}: V={hessian_data[name]['V']:.4f}, "
              f"|grad|={hessian_data[name]['grad_norm']:.2f}, "
              f"Morse={hessian_data[name]['morse_index']}, "
              f"evals={hessian_data[name]['hessian_evals']}")

    # Poincare-Hopf: sum of indices over critical points = Euler characteristic of disk = 1
    index_map = {0: 1, 1: -1, 2: 1}  # (-1)^morse
    index_sum = sum(index_map.get(d["morse_index"], 0) for d in hessian_data.values())
    poincare_hopf = {
        "euler_characteristic": 1,
        "index_sum": index_sum,
        "n_critical": len(hessian_data),
        "note": f"Poincare-Hopf: sum(indices) = chi(disk) = 1. Computed index sum = {index_sum} across {len(hessian_data)} sampled points.",
    }

    export = {
        "context": context,
        "alpha": alpha,
        "radial_profile": radial,
        "gradient_field": field,
        "key_points": hessian_data,
        "poincare_hopf": poincare_hopf,
    }

    with open(os.path.join(BASE_DIR, "landscape_data.json"), "w") as f:
        json.dump(export, f, indent=2)
    print(f"  [EXPORTED] landscape_data.json")
    print(f"  [ENERGY LANDSCAPE COMPLETE]\n")


if __name__ == "__main__":
    run()
