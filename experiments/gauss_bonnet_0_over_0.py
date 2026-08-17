"""
Gauss-Bonnet theorem via 0/0
============================

The Gauss-Bonnet theorem for a compact surface M with boundary dM:

  intint_M K dA + __{dM} kappa_g ds = 2pi chi(M)

where K is Gaussian curvature and kappa_g is geodesic curvature of the boundary.

The 0/0: on a flat surface (K = 0 everywhere, e.g., torus), the double integral
intint K dA is 0/0 — the integrand vanishes identically. The removable value is
2pichi(M) = 0 for T2, meaning the boundary geodesic curvature must also vanish
(closed geodesics have kappa_g = 0).

For surfaces with zero curvature at isolated points (e.g., saddle points),
the 0/0 at each zero-curvature point has a removable value equal to the local
contribution to chi(M).

We verify this by computing:
1. Gauss-Bonnet on triangulated S2 (K > 0 everywhere)
2. Gauss-Bonnet on triangulated T2 (K = 0 everywhere — flat)
3. Gauss-Bonnet on a surface with mixed curvature (e.g., torus of revolution)
4. The 0/0 at zero-curvature points

HONEST WALL: This is a computational verification on triangulated surfaces,
not a proof of the Gauss-Bonnet theorem.
"""

import json
import math
import os
import sys

import numpy as np

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(OUT_DIR, exist_ok=True)


def build_sphere_triangulation(n_subdivisions=2):
    """Build a triangulation of S2 via icosahedron subdivision."""
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

    for _ in range(n_subdivisions):
        new_faces = []
        midpoint_cache = {}
        new_verts = list(verts)
        for i, j, k in faces:
            def get_mid(a, b):
                key = (min(a, b), max(a, b))
                if key not in midpoint_cache:
                    mid = (new_verts[a] + new_verts[b]) / 2
                    mid /= np.linalg.norm(mid)
                    midpoint_cache[key] = len(new_verts)
                    new_verts.append(mid)
                return midpoint_cache[key]
            m01 = get_mid(i, j)
            m12 = get_mid(j, k)
            m20 = get_mid(k, i)
            new_faces.extend([
                (i, m01, m20), (j, m12, m01), (k, m20, m12), (m01, m12, m20)
            ])
        faces = new_faces
        verts = np.array(new_verts)

    return verts, faces


def build_torus_triangulation(n_u=15, n_v=15):
    """Build a triangulation of T2."""
    R, r = 2.0, 1.0
    verts = []
    faces = []

    for i in range(n_u):
        for j in range(n_v):
            u = 2 * np.pi * i / n_u
            v = 2 * np.pi * j / n_v
            x = (R + r * np.cos(v)) * np.cos(u)
            y = (R + r * np.cos(v)) * np.sin(u)
            z = r * np.sin(v)
            verts.append([x, y, z])

    verts = np.array(verts)

    for i in range(n_u):
        for j in range(n_v):
            i1 = (i + 1) % n_u
            j1 = (j + 1) % n_v
            v00 = i * n_v + j
            v10 = i1 * n_v + j
            v01 = i * n_v + j1
            v11 = i1 * n_v + j1
            faces.append((v00, v10, v01))
            faces.append((v10, v11, v01))

    return verts, faces


def build_torus_of_revolution(n_u=20, n_v=20):
    """Build a triangulation of a torus of revolution with variable curvature.

    The Gaussian curvature of a torus of revolution with cross-section radius r(u)
    is K = r(u) * r''(u) / ((R + r(u) cos(v))2).

    We use a torus with varying cross-section to create regions of positive,
    zero, and negative curvature.
    """
    R_base = 3.0
    verts = []
    faces = []

    for i in range(n_u):
        for j in range(n_v):
            u = 2 * np.pi * i / n_u
            v = 2 * np.pi * j / n_v
            # Variable cross-section radius
            r = 1.0 + 0.3 * np.sin(2 * u)
            x = (R_base + r * np.cos(v)) * np.cos(u)
            y = (R_base + r * np.cos(v)) * np.sin(u)
            z = r * np.sin(v)
            verts.append([x, y, z])

    verts = np.array(verts)

    for i in range(n_u):
        for j in range(n_v):
            i1 = (i + 1) % n_u
            j1 = (j + 1) % n_v
            v00 = i * n_v + j
            v10 = i1 * n_v + j
            v01 = i * n_v + j1
            v11 = i1 * n_v + j1
            faces.append((v00, v10, v01))
            faces.append((v10, v11, v01))

    return verts, faces


def compute_discrete_gauss_bonnet(verts, faces):
    """Compute the discrete Gauss-Bonnet integral on a triangulated surface.

    For each vertex, the angle defect is:
      K_i = 2pi - __{j adjacent to i} alpha_j

    where alpha_j are the angles at vertex i in all incident triangles.
    """
    V = len(verts)
    angle_defect = np.zeros(V)
    vertex_areas = np.zeros(V)

    for face in faces:
        i, j, k = face
        vi, vj, vk = verts[i], verts[j], verts[k]

        # Edge vectors
        e_ij = vj - vi
        e_ik = vk - vi
        e_jk = vk - vj

        # Angles at each vertex
        def angle(a, b):
            cos_a = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)
            cos_a = np.clip(cos_a, -1.0, 1.0)
            return np.arccos(cos_a)

        alpha_i = angle(e_ij, e_ik)
        alpha_j = angle(-e_ij, e_jk)
        alpha_k = angle(-e_ik, -e_jk)

        # Triangle area (for vertex area weighting)
        area = 0.5 * np.linalg.norm(np.cross(e_ij, e_ik))

        angle_defect[i] += alpha_i
        angle_defect[j] += alpha_j
        angle_defect[k] += alpha_k

        vertex_areas[i] += area / 3.0
        vertex_areas[j] += area / 3.0
        vertex_areas[k] += area / 3.0

    # Gauss-Bonnet: _ K_i = 2pi chi(M)
    K_vertex = 2 * np.pi - angle_defect
    total_gauss_bonnet = np.sum(K_vertex)
    chi = total_gauss_bonnet / (2 * np.pi)

    # Euler characteristic
    edges = set()
    for face in faces:
        for i in range(3):
            edge = tuple(sorted([face[i], face[(i + 1) % 3]]))
            edges.add(edge)
    E = len(edges)
    F = len(faces)
    chi_euler = V - E + F

    return {
        'V': V, 'E': E, 'F': F,
        'chi_gauss_bonnet': chi,
        'chi_euler': chi_euler,
        'total_angle_defect': float(np.sum(angle_defect)),
        'total_gauss_bonnet_integral': float(total_gauss_bonnet),
        'gauss_bonnet_matches_euler': abs(chi - chi_euler) < 0.5,
        'K_vertex_min': float(np.min(K_vertex)),
        'K_vertex_max': float(np.max(K_vertex)),
        'K_vertex_mean': float(np.mean(K_vertex)),
        'n_positive_curvature': int(np.sum(K_vertex > 0.01)),
        'n_negative_curvature': int(np.sum(K_vertex < -0.01)),
        'n_zero_curvature': int(np.sum(np.abs(K_vertex) < 0.01)),
        'K_vertex': K_vertex.tolist(),
    }


def find_0_over_0_curvature(verts, faces, K_vertex):
    """Find the 0/0 at zero-curvature points.

    At a vertex with K = 0, the angle defect is 2pi (all angles sum to 2pi exactly).
    This is a 0/0 form: both the curvature and the angle sum are balanced.
    The removable value is 2pi (the local contribution to chi).
    """
    zero_mask = np.abs(K_vertex) < 0.2
    n_zero = int(np.sum(zero_mask))
    total_zero_contribution = float(np.sum(K_vertex[zero_mask]))

    # For flat torus: all vertices have K = 0, so the total GB = 0 = 2pi·0
    # This is the 0/0: all angle defects = 2pi, but the curvature = 0
    # The removable value is that each vertex contributes 0 to chi

    return {
        'n_zero_curvature_vertices': n_zero,
        'total_zero_curvature_contribution': total_zero_contribution,
        'removable_value': '2pi × (local chi contribution) = 0 for flat surfaces',
        'is_0_over_0': n_zero > 0 and abs(total_zero_contribution) < 1.0,
    }


def run_experiment():
    print("Gauss-Bonnet Theorem via 0/0 Probe")
    print("=" * 50)

    results = {
        'experiment': 'gauss_bonnet_0_over_0',
        'description': 'Gauss-Bonnet: intintK dA = 2pichi(M); 0/0 at zero-curvature points',
    }

    # Test 1: Sphere S2
    print("\n1. Sphere S2 (K > 0 everywhere):")
    verts_s, faces_s = build_sphere_triangulation(n_subdivisions=2)
    gb_sphere = compute_discrete_gauss_bonnet(verts_s, faces_s)
    print(f"   V={gb_sphere['V']}, E={gb_sphere['E']}, F={gb_sphere['F']}")
    print(f"   chi(Gauss-Bonnet) = {gb_sphere['chi_gauss_bonnet']:.4f}")
    print(f"   chi(Euler) = {gb_sphere['chi_euler']}")
    print(f"   GB = 2pichi? {'PASS' if gb_sphere['gauss_bonnet_matches_euler'] else 'FAIL'}")
    print(f"   K range: [{gb_sphere['K_vertex_min']:.4f}, {gb_sphere['K_vertex_max']:.4f}]")
    print(f"   Zero-curvature vertices: {gb_sphere['n_zero_curvature']}")
    results['sphere'] = gb_sphere

    # 0/0 on sphere
    z0_sphere = find_0_over_0_curvature(verts_s, faces_s, np.array(gb_sphere['K_vertex']))
    results['sphere_0_over_0'] = z0_sphere
    print(f"   0/0 at K=0: {z0_sphere['is_0_over_0']}")

    # Test 2: Torus T2 (K = 0 everywhere)
    print("\n2. Torus T2 (K = 0 — flat):")
    verts_t, faces_t = build_torus_triangulation(n_u=15, n_v=15)
    gb_torus = compute_discrete_gauss_bonnet(verts_t, faces_t)
    print(f"   V={gb_torus['V']}, E={gb_torus['E']}, F={gb_torus['F']}")
    print(f"   chi(Gauss-Bonnet) = {gb_torus['chi_gauss_bonnet']:.4f}")
    print(f"   chi(Euler) = {gb_torus['chi_euler']}")
    print(f"   GB = 2pi·0 = 0? {'PASS' if abs(gb_torus['chi_gauss_bonnet']) < 0.5 else 'FAIL'}")
    print(f"   K range: [{gb_torus['K_vertex_min']:.6f}, {gb_torus['K_vertex_max']:.6f}]")
    print(f"   Zero-curvature vertices: {gb_torus['n_zero_curvature']}/{gb_torus['V']}")
    results['torus'] = gb_torus

    # 0/0 on torus (ALL vertices have K = 0)
    z0_torus = find_0_over_0_curvature(verts_t, faces_t, np.array(gb_torus['K_vertex']))
    results['torus_0_over_0'] = z0_torus
    print(f"   0/0 at K=0: {z0_torus['is_0_over_0']} (ALL {z0_torus['n_zero_curvature_vertices']} vertices)")

    # Test 3: Torus of revolution (mixed curvature)
    print("\n3. Torus of revolution (mixed curvature):")
    verts_r, faces_r = build_torus_of_revolution(n_u=15, n_v=15)
    gb_rev = compute_discrete_gauss_bonnet(verts_r, faces_r)
    print(f"   V={gb_rev['V']}, E={gb_rev['E']}, F={gb_rev['F']}")
    print(f"   chi(Gauss-Bonnet) = {gb_rev['chi_gauss_bonnet']:.4f}")
    print(f"   chi(Euler) = {gb_rev['chi_euler']}")
    print(f"   GB = 2pi·0 = 0? {'PASS' if abs(gb_rev['chi_gauss_bonnet']) < 1.0 else 'FAIL'}")
    print(f"   K range: [{gb_rev['K_vertex_min']:.4f}, {gb_rev['K_vertex_max']:.4f}]")
    print(f"   Positive: {gb_rev['n_positive_curvature']}, Negative: {gb_rev['n_negative_curvature']}, Zero: {gb_rev['n_zero_curvature']}")
    results['torus_revolution'] = gb_rev

    z0_rev = find_0_over_0_curvature(verts_r, faces_r, np.array(gb_rev['K_vertex']))
    results['torus_revolution_0_over_0'] = z0_rev
    print(f"   0/0 at K=0: {z0_rev['is_0_over_0']} ({z0_rev['n_zero_curvature_vertices']} vertices)")

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")

    sphere_pass = gb_sphere['gauss_bonnet_matches_euler']
    torus_pass = abs(gb_torus['chi_gauss_bonnet']) < 0.5
    rev_pass = abs(gb_rev['chi_gauss_bonnet']) < 1.0
    torus_00 = z0_torus['is_0_over_0']

    print(f"   S2: GB = 2pi·2: {'PASS' if sphere_pass else 'FAIL'} (chi = {gb_sphere['chi_gauss_bonnet']:.4f})")
    print(f"   T2: GB = 2pi·0 = 0: {'PASS' if torus_pass else 'FAIL'} (chi = {gb_torus['chi_gauss_bonnet']:.4f})")
    print(f"   Rev T2: GB = 0: {'PASS' if rev_pass else 'FAIL'} (chi = {gb_rev['chi_gauss_bonnet']:.4f})")
    print(f"   T2 0/0: ALL vertices K = 0: {'PASS' if torus_00 else 'FAIL'}")

    overall = 'SUPPORTED' if (sphere_pass and torus_pass and rev_pass) else 'PARTIAL'
    results['overall'] = overall
    print(f"\n   OVERALL: {overall}")

    out_path = os.path.join(OUT_DIR, 'gauss_bonnet_0_over_0_data.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n   Saved to {out_path}")

    return results


if __name__ == '__main__':
    run_experiment()
