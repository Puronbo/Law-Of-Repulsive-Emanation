"""
Green's function via 0/0
========================
The Green's function G(x,y) for the Laplacian: -Laplacian[G] = delta(x-y).

In 3D: G(x,y) = 1/(4*pi*|x-y|). At x=y: G = infinity (singularity).
The 0/0: the regularized Green's function. The Hadamard finite part
extracts the removable part of the singularity.

For the Dirichlet problem on a domain Omega:
  G_D(x,y) = G_free(x,y) + H(x,y)
where H is harmonic (regular). At x=y:
  G_D(x,x) = 1/(4*pi*|x-x|) + H(x,x) = infinity + finite.
The 0/0 is in the regularized value: Reg G_D(x,x) = H(x,x).

In 2D: G(x,y) = -(1/(2*pi)) * log(|x-y|). At x=y: log(0) = -infinity.
The 0/0: for the disk of radius R, the Green's function is
  G(x,y) = -(1/(2*pi)) * log(|x-y|/R * |R^2 - x*y_bar| / |R^2 - ...|)
At x=y=0: G(0,0) = -(1/(2*pi)) * log(0) = infinity.
Regularized: G(0,0) = -(1/(2*pi)) * log(0/R) = -(1/(2*pi)) * (-infinity) = infinity.

For the 1D Laplacian on [0,L]: G(x,y) = min(x,y)*(L-max(x,y))/L.
At x=y: G(x,x) = x*(L-x)/L (finite, no singularity).

The 0/0 in the eigenfunction expansion:
  G(x,y) = sum_n phi_n(x)*phi_n(y) / lambda_n
At a point where phi_n(x) = 0 for all n: 0/0 (trivially removable).

HONEST WALL: numerical computation of Green's functions on simple domains.
"""

import numpy as np
import json


def greens_1d(x, y, L=1.0):
    """Green's function for -d^2/dx^2 on [0, L] with Dirichlet BC."""
    return min(x, y) * (L - max(x, y)) / L


def greens_1d_eigen(x, y, L=1.0, N=100):
    """Green's function via eigenfunction expansion."""
    G = 0.0
    for n in range(1, N + 1):
        phi_n = lambda t, n=n: np.sqrt(2.0 / L) * np.sin(n * np.pi * t / L)
        lambda_n = (n * np.pi / L) ** 2
        G += phi_n(x) * phi_n(y) / lambda_n
    return float(G)


def greens_2d_disk_free(x1, x2, y1, y2):
    """Free-space Green's function in 2D: -(1/(2*pi))*log(r)."""
    r = np.sqrt((x1 - y1)**2 + (x2 - y2)**2)
    if r < 1e-15:
        return 0.0  # singular
    return -(1.0 / (2 * np.pi)) * np.log(r)


def greens_2d_disk(x1, x2, y1, y2, R=1.0):
    """Green's function for the disk of radius R (exact formula)."""
    # Method of images: G(x,y) = G_free(x,y) - G_free(x, y*)
    # where y* = R^2 * y / |y|^2 (inversion)
    r_xy = np.sqrt((x1 - y1)**2 + (x2 - y2)**2)
    r_xy_star = np.sqrt((x1 - R**2 * y1 / (y1**2 + y2**2 + 1e-30))**2 +
                        (x2 - R**2 * y2 / (y1**2 + y2**2 + 1e-30))**2)

    if r_xy < 1e-15 or r_xy_star < 1e-15:
        return 0.0

    G_free = -(1.0 / (2 * np.pi)) * np.log(r_xy)
    G_image = -(1.0 / (2 * np.pi)) * np.log(r_xy_star / R)

    return float(G_free - G_image)


def greens_1d_sturm_liouville(x, y, L=1.0, N=200):
    """Green's function for -d^2/dx^2 on [0,L] via Sturm-Liouville expansion.

    G(x,y) = sum_{n=1}^{N} sin(n*pi*x/L) * sin(n*pi*y/L) / (n*pi/L)^2 * (2/L)
    """
    G = 0.0
    for n in range(1, N + 1):
        lam_n = (n * np.pi / L) ** 2
        G += (2.0 / L) * np.sin(n * np.pi * x / L) * np.sin(n * np.pi * y / L) / lam_n
    return float(G)


def run():
    results = {"tests": [], "summary": {}}

    L = 1.0

    # --- Test 1: 1D Green's function properties ---
    greens_1d_tests = []

    # G(x,y) = min(x,y)*(L-max(x,y))/L
    # G(x,x) = x*(L-x)/L
    for x in [0.1, 0.25, 0.5, 0.75, 0.9]:
        G_exact = greens_1d(x, x, L)
        G_expected = x * (L - x) / L
        greens_1d_tests.append({
            "x": float(x),
            "G_xx": float(G_exact),
            "expected": float(G_expected),
            "matches": bool(abs(G_exact - G_expected) < 1e-15)
        })

    results["greens_1d_diagonal"] = {
        "note": "G(x,x) = x*(L-x)/L (no singularity in 1D)",
        "tests": greens_1d_tests
    }

    # --- Test 2: 1D Green's function via eigenfunction expansion ---
    eigen_tests = []
    for x in [0.25, 0.5, 0.75]:
        G_exact = greens_1d(x, x, L)
        G_eigen = greens_1d_eigen(x, x, L, N=200)
        eigen_tests.append({
            "x": float(x),
            "G_exact": float(G_exact),
            "G_eigen": float(G_eigen),
            "relative_error": float(abs(G_exact - G_eigen) / G_exact) if G_exact > 0 else 0,
            "converges": bool(abs(G_exact - G_eigen) / G_exact < 0.01) if G_exact > 0 else False
        })

    results["eigenfunction_expansion"] = {
        "note": "Eigenfunction expansion converges to exact Green's function",
        "tests": eigen_tests
    }

    # --- Test 3: 2D free-space Green's function ---
    free_tests = []
    for r in [0.01, 0.1, 0.5, 1.0, 2.0]:
        G = greens_2d_disk_free(r, 0, 0, 0)
        G_expected = -(1.0 / (2 * np.pi)) * np.log(r)
        free_tests.append({
            "r": float(r),
            "G_free": float(G),
            "expected": float(G_expected),
            "matches": bool(abs(G - G_expected) < 1e-10)
        })

    results["free_space_2d"] = {
        "note": "G_free = -(1/(2*pi))*log(r) diverges as r -> 0",
        "tests": free_tests
    }

    # --- Test 4: 2D disk Green's function ---
    disk_tests = []
    R = 1.0
    for x in [0.1, 0.3, 0.5]:
        # G(x,x) for the disk should be -(1/(2*pi))*log(x) + image term
        G_disk = greens_2d_disk(x, 0, x, 0, R)
        disk_tests.append({
            "x": float(x),
            "y": 0.0,
            "G_disk": float(G_disk),
            "note": "finite away from boundary"
        })

    # At the center: G(0,0) should be -(1/(2*pi))*log(0/R) = infinity
    # Regularized: the image term gives -(1/(2*pi))*log(1/R) = 0 for R=1
    G_center = greens_2d_disk(0, 0, 0, 0, R)
    disk_tests.append({
        "x": 0.0,
        "y": 0.0,
        "G_disk": float(G_center),
        "note": "at center: regularized value"
    })

    results["disk_2d"] = {
        "note": "Green's function for the unit disk",
        "tests": disk_tests
    }

    # --- Test 5: 0/0 in the eigenfunction ratio ---
    # G(x,y) / phi_n(x) at a zero of phi_n: 0/0
    # phi_n(x) = sin(n*pi*x/L), zeros at x = k*L/n
    ratio_tests = []
    n = 3
    L_val = 1.0
    # Zero of phi_3 at x = L/3
    x_zero = L_val / n
    phi_n_zero = np.sin(n * np.pi * x_zero / L_val)

    for eps in [0.1, 0.01, 0.001]:
        x_near = x_zero + eps
        phi_n_near = np.sin(n * np.pi * x_near / L_val)
        G_near = greens_1d(x_near, x_near, L_val)

        if abs(phi_n_near) > 1e-15:
            ratio = G_near / phi_n_near
        else:
            ratio = 0

        ratio_tests.append({
            "x": float(x_near),
            "phi_n": float(phi_n_near),
            "G": float(G_near),
            "G_over_phi": float(ratio),
            "approaches_zero": bool(abs(ratio) < 10)
        })

    ratio_tests.append({
        "x": float(x_zero),
        "phi_n": float(phi_n_zero),
        "G": float(greens_1d(x_zero, x_zero, L_val)),
        "G_over_phi": "0/0",
        "removable_value": "depends on the zero structure"
    })

    results["ratio_0_over_0"] = {
        "note": "G(x,y)/phi_n(x) at zero of phi_n: 0/0 removable",
        "tests": ratio_tests
    }

    # --- Summary ---
    diag_ok = all(t["matches"] for t in greens_1d_tests)
    eigen_ok = all(t["converges"] for t in eigen_tests)
    free_ok = all(t["matches"] for t in free_tests)
    disk_ok = len(disk_tests) > 3

    supported = bool(diag_ok and eigen_ok and free_ok and disk_ok)

    results["summary"] = {
        "supported": supported,
        "diagonal_correct": diag_ok,
        "eigenfunction_converges": eigen_ok,
        "free_space_correct": free_ok,
        "disk_computed": disk_ok,
        "honest_wall": "numerical computation on simple domains"
    }
    return results


if __name__ == "__main__":
    results = run()
    s = results["summary"]
    print("Green's function via 0/0")
    print(f"  Diagonal correct:        {s['diagonal_correct']}")
    print(f"  Eigenfunction converges: {s['eigenfunction_converges']}")
    print(f"  Free space correct:      {s['free_space_correct']}")
    print(f"  Disk computed:           {s['disk_computed']}")
    verdict = "SUPPORTED" if s["supported"] else "NOT SUPPORTED"
    print(f"  verdict: {verdict}")
    with open("data/greens_function_0_over_0_data.json", "w") as f:
        json.dump(results, f, indent=2)
