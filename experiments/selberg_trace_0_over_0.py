"""
Heat kernel trace via 0/0
=========================

The heat kernel trace on a compact manifold:

  Tr(e^{-tΔ}) = Σ e^{-t λ_n}

has two 0/0 structures:

1. At t = ∞: all nonzero eigenvalues contribute 0, while the zero eigenvalue
   contributes exactly 1. The removable value is 1 (the zero-mode).
   lim_{t->inf} Tr = 1 = removable value.

2. At t = 0: Tr = Σ 1 = infinity (the Weyl singularity).
   The 0/0 is the ratio Tr(t)/Tr(t_ref) which converges to a finite value.

We verify this on:
1. Flat torus T2 = S1 x S1 (analytical eigenvalues known exactly)
2. S2 via triangulation

HONEST WALL: Computational verification of heat kernel properties, not a
proof of the Selberg trace formula.
"""

import json
import math
import os
import sys

import numpy as np

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(OUT_DIR, exist_ok=True)


def torus_eigenvalues_grid(n_modes=50, L=2.0 * np.pi):
    """Eigenvalues of -Delta on flat torus [0, L]^2 with periodic BC.

    λ_{m,n} = (2π/L)^2 (m² + n²) for m, n in Z.
    """
    eigenvalues = []
    max_k = int(np.sqrt(n_modes)) + 5
    for m in range(-max_k, max_k + 1):
        for n in range(-max_k, max_k + 1):
            lam = (2 * np.pi / L) ** 2 * (m**2 + n**2)
            eigenvalues.append(lam)
    eigenvalues.sort()
    return np.array(eigenvalues[:n_modes])


def sphere_eigenvalues_analytical(n_eigenvalues=20):
    """Eigenvalues of -Delta on unit sphere S2.

    lambda_l = l(l+1) with multiplicity 2l+1, for l = 0, 1, 2, ...
    """
    eigenvalues = []
    l = 0
    while len(eigenvalues) < n_eigenvalues:
        lam = l * (l + 1)
        for _ in range(2 * l + 1):
            eigenvalues.append(lam)
        l += 1
    return np.array(eigenvalues[:n_eigenvalues])


def sphere_eigenvalues_triangulated(n_subdiv=4):
    """Compute eigenvalues of cotangent Laplacian on triangulated S2."""
    phi = (1 + np.sqrt(5)) / 2
    verts = np.array([
        [-1, phi, 0], [1, phi, 0], [-1, -phi, 0], [1, -phi, 0],
        [0, -1, phi], [0, 1, phi], [0, -1, -phi], [0, 1, -phi],
        [phi, 0, -1], [phi, 0, 1], [-phi, 0, -1], [-phi, 0, 1],
    ], dtype=float)
    verts /= np.linalg.norm(verts[0])

    faces = [
        (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
        (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
        (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
        (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1),
    ]

    for _ in range(n_subdiv):
        new_faces = []
        mid_cache = {}
        new_verts = list(verts)
        for i, j, k in faces:
            def get_mid(a, b):
                key = (min(a, b), max(a, b))
                if key not in mid_cache:
                    mid = (new_verts[a] + new_verts[b]) / 2
                    mid /= np.linalg.norm(mid)
                    mid_cache[key] = len(new_verts)
                    new_verts.append(mid)
                return mid_cache[key]
            m01 = get_mid(i, j)
            m12 = get_mid(j, k)
            m20 = get_mid(k, i)
            new_faces.extend([
                (i, m01, m20), (j, m12, m01), (k, m20, m12), (m01, m12, m20)
            ])
        faces = new_faces
        verts = np.array(new_verts)

    V = len(verts)
    A = np.zeros(V)
    L = np.zeros((V, V))

    for face in faces:
        i, j, k = face
        vi, vj, vk = verts[i], verts[j], verts[k]
        e1 = vj - vi
        e2 = vk - vi
        area = 0.5 * np.linalg.norm(np.cross(e1, e2))
        A[i] += area / 3.0
        A[j] += area / 3.0
        A[k] += area / 3.0

    for face in faces:
        i, j, k = face
        vi, vj, vk = verts[i], verts[j], verts[k]

        def cot(a, b):
            cos_a = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)
            cos_a = np.clip(cos_a, -1 + 1e-12, 1 - 1e-12)
            return cos_a / np.sqrt(max(1 - cos_a**2, 1e-12))

        cot_ij = cot(vi - vj, vi - vk)
        cot_jk = cot(vj - vk, vj - vi)
        cot_ki = cot(vk - vi, vk - vj)

        L[i, j] += cot_ij / 2.0
        L[j, i] += cot_ij / 2.0
        L[j, k] += cot_jk / 2.0
        L[k, j] += cot_jk / 2.0
        L[k, i] += cot_ki / 2.0
        L[i, k] += cot_ki / 2.0

    for i in range(V):
        L[i, i] = -np.sum(L[i])

    A_inv = np.diag(1.0 / np.maximum(A, 1e-12))
    L_w = -A_inv @ L
    eigvals = np.sort(np.abs(np.linalg.eigvalsh(L_w)))
    return eigvals


def heat_trace(eigvals, t):
    """Tr(e^{-tΔ}) with eigenvalues clamped to non-negative."""
    return float(np.sum(np.exp(-t * np.maximum(eigvals, 0))))


def find_zero_mode_0_over_0(eigvals):
    """The 0/0: as t->inf, Tr -> 1 (removable value) from nonzero eigenvalues
    that shrink to 0. At t=inf, every term is e^{-inf*lambda} = 0 except
    the zero mode where e^{-inf*0} = e^0 = 1.

    This is a removable singularity: the function Tr(t) has a well-defined
    limit (1) but the individual terms are 0/0.
    """
    eigvals_pos = np.maximum(eigvals, 0)
    n_zero = int(np.sum(eigvals_pos < 0.01))

    t_vals = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0]
    traces = [heat_trace(eigvals, t) for t in t_vals]

    return {
        'n_zero_modes_numerical': n_zero,
        't_values': t_vals,
        'traces': traces,
        'limit_at_inf': traces[-1] if traces else None,
        'removable_value_is_one': abs(traces[-1] - 1.0) < 0.01 if traces else False,
    }


def weyl_singularity_0_over_0(eigvals):
    """The 0/0 at t=0: Tr blows up as Area/(4pi*t) + ... .

    The ratio Tr(t) / (1/t) converges to Area/(4pi) as t -> 0.
    This is the 0/0: both numerator and denominator blow up, but their
    ratio converges to a finite (removable) value.
    """
    t_vals = [0.001, 0.005, 0.01, 0.05, 0.1]
    traces = [heat_trace(eigvals, t) for t in t_vals]
    ratios = [tr * t for tr, t in zip(traces, t_vals)]

    return {
        't_values': t_vals,
        'traces': traces,
        'trace_times_t': ratios,
        'removable_value': ratios[-1] if ratios else None,
    }


def run_experiment():
    print("Heat Kernel Trace via 0/0 Probe")
    print("=" * 50)

    results = {
        'experiment': 'selberg_trace_0_over_0',
        'description': 'Heat kernel trace: 0/0 at t=inf (removable=1) and t=0 (Weyl singularity)',
    }

    # Flat torus (analytical)
    print("\n1. Flat torus T2 (analytical eigenvalues):")
    eigvals_torus = torus_eigenvalues_grid(n_modes=100)
    print(f"   First 5 eigenvalues: {[f'{e:.4f}' for e in eigvals_torus[:5]]}")
    print(f"   Zero mode: {eigvals_torus[0]:.6f}")

    z0_torus = find_zero_mode_0_over_0(eigvals_torus)
    print(f"   n_zero_modes: {z0_torus['n_zero_modes_numerical']}")
    print(f"   Tr at t=100: {z0_torus['traces'][-1]:.6f}")
    print(f"   Removable value = 1: {z0_torus['removable_value_is_one']}")
    results['torus'] = {
        'eigenvalues': eigvals_torus[:10].tolist(),
        'zero_mode_0_over_0': z0_torus,
    }

    # Weyl singularity
    weyl_torus = weyl_singularity_0_over_0(eigvals_torus)
    print(f"   Weyl limit (Tr*t): {[f'{r:.4f}' for r in weyl_torus['trace_times_t']]}")
    results['torus_weyl'] = weyl_torus

    # Sphere (analytical)
    print("\n2. Sphere S2 (analytical eigenvalues):")
    eigvals_sphere = sphere_eigenvalues_analytical(n_eigenvalues=30)
    print(f"   First 8 eigenvalues: {[f'{e:.1f}' for e in eigvals_sphere[:8]]}")
    print(f"   Zero mode: {eigvals_sphere[0]:.6f}")

    z0_sphere = find_zero_mode_0_over_0(eigvals_sphere)
    print(f"   n_zero_modes: {z0_sphere['n_zero_modes_numerical']}")
    print(f"   Tr at t=100: {z0_sphere['traces'][-1]:.6f}")
    print(f"   Removable value = 1: {z0_sphere['removable_value_is_one']}")
    results['sphere_analytical'] = {
        'eigenvalues': eigvals_sphere[:10].tolist(),
        'zero_mode_0_over_0': z0_sphere,
    }

    # Sphere (triangulated)
    print("\n3. Sphere S2 (triangulated, cotangent Laplacian):")
    eigvals_tri = sphere_eigenvalues_triangulated(n_subdiv=3)
    print(f"   V={len(eigvals_tri)}, first 5 eigenvalues: {[f'{e:.4f}' for e in eigvals_tri[:5]]}")

    z0_tri = find_zero_mode_0_over_0(eigvals_tri)
    print(f"   n_zero_modes: {z0_tri['n_zero_modes_numerical']}")
    print(f"   Tr at t=100: {z0_tri['traces'][-1]:.6f}")
    print(f"   Removable value = 1: {z0_tri['removable_value_is_one']}")
    results['sphere_triangulated'] = {
        'V': len(eigvals_tri),
        'eigenvalues': eigvals_tri[:10].tolist(),
        'zero_mode_0_over_0': z0_tri,
    }

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")

    torus_pass = z0_torus['removable_value_is_one']
    sphere_pass = z0_sphere['removable_value_is_one']
    tri_pass = z0_tri['removable_value_is_one']

    print(f"   T2 analytical: Tr -> 1 at t=inf: {'PASS' if torus_pass else 'FAIL'} ({z0_torus['traces'][-1]:.6f})")
    print(f"   S2 analytical: Tr -> 1 at t=inf: {'PASS' if sphere_pass else 'FAIL'} ({z0_sphere['traces'][-1]:.6f})")
    print(f"   S2 triangulated: Tr -> 1 at t=inf: {'PASS' if tri_pass else 'FAIL'} ({z0_tri['traces'][-1]:.6f})")

    overall = 'SUPPORTED' if (torus_pass and sphere_pass) else 'PARTIAL'
    results['overall'] = overall
    print(f"\n   OVERALL: {overall}")

    out_path = os.path.join(OUT_DIR, 'selberg_trace_0_over_0_data.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n   Saved to {out_path}")

    return results


if __name__ == '__main__':
    run_experiment()
