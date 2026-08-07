"""
spectral_extended.py
====================
Resolve WEAVERS_SCRIBE Ch. 5.1 spectral conjectures C1, C3, C4 and the
Selberg<->Riemann-zero correspondence by recomputing the Laplace-Beltrami
spectrum on the Poincare disk with far more modes than the persisted
30-eigenvalue run (spectral_data.json).

C1 (E1-dozenal):   low spectral radii r_k = sqrt(E_k - 1/4) track ln(k),
                   k in {10, 26, 2000}.
C3 (Mersenne-lambda): a mode exists near lambda(7)  = 1/4 + (3 ln2)^2 ~ 4.574
                   (below the current floor) and lambda(31) = 1/4 + (5 ln2)^2
                   ~ 12.261 fills the old gap [12.06, 12.85].
C4 (intermediate stats): <r> (ratio of consecutive unfolded spacings) sits
                   between Poisson 0.386 and GOE 0.536 at 30 modes; more modes
                   decide whether the "chaos is consistent" (T19) claim is
                   measurable.
Bonus:  min |t_n - t_zeta| over all modes updates the "not a match by any
                   standard" verdict (2.5-9.0 at 30 modes).

Verdict artifact: ../data/spectral_extended_data.json
"""

import json, math, os, sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Universals"))
from spectral_analysis import build_laplacian_matrix, RIEMANN_ZEROS
from hamiltonian_flow import repulsion_loss
from scipy import sparse
from scipy.sparse.linalg import eigsh

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

CONTEXT = ["Tech", "Silicon"]
LN2 = math.log(2.0)
LAM7 = 0.25 + (3 * LN2) ** 2      # Mersenne prime 7  = 2^3 - 1
LAM31 = 0.25 + (5 * LN2) ** 2     # Mersenne prime 31 = 2^5 - 1
C1_K = [10, 12, 26, 2000]
POISSON_R = 0.386
GOE_R = 0.536


def solve(nx=120, ny=120, r_max=0.85, n_eigs=100):
    x = np.linspace(-r_max, r_max, nx)
    y = np.linspace(-r_max, r_max, ny)
    dx = x[1] - x[0]; dy = y[1] - y[0]
    X, Y = np.meshgrid(x, y)
    R2 = X**2 + Y**2
    mask = R2 < r_max**2
    N_active = int(mask.sum())
    print("Grid %dx%d, active points %d, solving for %d eigenvalues..."
          % (nx, ny, N_active, n_eigs))
    Lap = build_laplacian_matrix(nx, ny, dx, dy, mask)
    lam_sq = 4.0 / ((1.0 - R2 + 1e-12) ** 2)
    lam_sq = np.clip(lam_sq, 0, 1000.0)
    V_vals = np.zeros(ny * nx)
    pts = np.column_stack([X.ravel(), Y.ravel()])
    for k in range(nx * ny):
        if mask.ravel()[k]:
            V_vals[k] = repulsion_loss(pts[k], CONTEXT)
    V_active = V_vals[mask.ravel()]
    lam_sq_active = lam_sq.ravel()[mask.ravel()]
    A = Lap + sparse.diags(lam_sq_active * V_active, 0, format='csr')
    B = sparse.diags(lam_sq_active, 0, format='csc')
    n_k = min(n_eigs, N_active - 2)
    eigenvalues, eigenfunctions = eigsh(A, k=n_k, M=B, which='SA', tol=1e-6, maxiter=10000)
    eigenvalues = np.sort(eigenvalues.real)
    return eigenvalues


def nearest(eigs, target):
    i = int(np.argmin(np.abs(np.asarray(eigs) - target)))
    return i, eigs[i], abs(eigs[i] - target)


def ratio_stat(eigs):
    """Consecutive-ratio statistic <r> = mean(min(s_n, s_{n+1})/max(...)) after
    unfolding via polynomial fit (same convention as the corpus's 0.460)."""
    e = np.sort(np.asarray(eigs, dtype=float))
    n = len(e)
    idx = np.arange(1, n + 1, dtype=float)
    coeffs = np.polyfit(e, idx, deg=min(6, n // 2))
    poly = np.poly1d(coeffs)
    un = poly(e)
    s = np.diff(un)
    s = s / np.mean(s)
    s1, s2 = s[:-1], s[1:]
    r = np.minimum(s1, s2) / np.maximum(s1, s2)
    return float(np.mean(r)), float(np.median(r)), float(np.std(r))


def main():
    n_eigs = 100
    try:
        eigs = solve(nx=120, ny=120, r_max=0.85, n_eigs=n_eigs)
    except Exception as exc:
        print("120x120 failed (%s); falling back to 100x100" % exc)
        eigs = solve(nx=100, ny=100, r_max=0.85, n_eigs=n_eigs)
    eigs = np.asarray(eigs)
    print("solved %d eigenvalues; E0=%.6f  E_top=%.6f" % (len(eigs), eigs[0], eigs[-1]))

    # --- C3a: mode near lambda(7)=4.574 below the floor ---
    i7, e7, d7 = nearest(eigs, LAM7)
    c3a = {
        "lambda7": round(LAM7, 4),
        "nearest_mode_index": int(i7),
        "nearest_mode_E": round(float(e7), 4),
        "delta": round(float(d7), 4),
        "below_old_floor_E0=5.58": bool(e7 < 5.58),
        "below_new_floor_E0": bool(e7 < float(eigs[0])),
        "supported": float(d7) < 0.25,
    }

    # --- C3b: mode near lambda(31)=12.261 ---
    i31, e31, d31 = nearest(eigs, LAM31)
    c3b = {
        "lambda31": round(LAM31, 4),
        "nearest_mode_index": int(i31),
        "nearest_mode_E": round(float(e31), 4),
        "delta": round(float(d31), 4),
        "supported": float(d31) < 0.25,
    }

    # --- C1: r_k vs ln(k) ---
    c1 = []
    for k in C1_K:
        Lk = math.log(k)
        E_pred = 0.25 + Lk * Lk
        i, e, d = nearest(eigs, E_pred)
        r_mode = math.sqrt(max(e - 0.25, 0.0))
        c1.append({
            "k": k, "ln(k)": round(Lk, 4), "E_pred": round(E_pred, 4),
            "nearest_mode_index": int(i), "nearest_mode_E": round(float(e), 4),
            "r_mode": round(r_mode, 4), "delta_r": round(abs(r_mode - Lk), 4),
            "rel_err": round(abs(r_mode - Lk) / Lk, 4),
        })
    c1_supported = any(x["rel_err"] < 0.02 for x in c1)

    # --- C4: level-spacing statistics ---
    r_mean, r_med, r_std = ratio_stat(eigs)
    c4 = {
        "r_mean": round(r_mean, 4), "r_median": round(r_med, 4), "r_std": round(r_std, 4),
        "poisson_0.386": POISSON_R, "goe_0.536": GOE_R,
        "position": "poisson" if r_mean < 0.45 else ("goe" if r_mean > 0.49 else "intermediate"),
        "note": "Poisson 0.386 / GOE 0.536 (ratio statistic); 0.460 measured at 30 modes (WEAVERS 5.1)",
    }

    # --- Bonus: Selberg <-> Riemann zeros ---
    t_vals = np.sqrt(np.maximum(eigs - 0.25, 0.0))
    dists = []
    for t in t_vals:
        d = float(np.min(np.abs(t - RIEMANN_ZEROS)))
        dists.append(d)
    dists = np.array(dists)
    zeta = {
        "n_modes_compared": int(len(t_vals)),
        "min_dist": round(float(dists.min()), 4),
        "median_dist": round(float(np.median(dists)), 4),
        "within_0.5": int((dists < 0.5).sum()),
        "old_verdict": "min |t_n - t_zeta| ~ 2.5-9.0 at 30 modes (not a match by any standard)",
    }

    out = {
        "claim": "WEAVERS_SCRIBE Ch.5.1 conjectures C1 (E1-dozenal), C3 (Mersenne-lambda spectrum), C4 (intermediate stats) + Selberg<->zeros",
        "setup": {"nx": 120, "ny": 120, "r_max": 0.85, "n_eigs": n_eigs, "context": CONTEXT},
        "n_modes": int(len(eigs)),
        "E0": round(float(eigs[0]), 6),
        "E_top": round(float(eigs[-1]), 6),
        "first_12": [round(float(e), 4) for e in eigs[:12]],
        "eigenvalues_all": [round(float(e), 6) for e in eigs],
        "c3a": c3a,
        "c3b": c3b,
        "c1": c1,
        "c1_supported_any": c1_supported,
        "c4": c4,
        "selberg_zeros": zeta,
        "verdict": {
            "c3a": "SUPPORTED (sub-floor mode at lambda(7))" if c3a["supported"] else "NOT SUPPORTED",
            "c3b": "SUPPORTED (mode near lambda(31))" if c3b["supported"] else "NOT SUPPORTED",
            "c1": "SUPPORTED (at least one r_k ~ ln(k))" if c1_supported else "NOT SUPPORTED",
            "c4": "MEASURED: r=%.3f (%s)" % (r_mean, c4["position"]),
        },
        "discrepancy_note": (
            "WEAVERS 5.1 claimed eig[5]=12.060 and a gap [12.06, 12.85]; persisted "
            "spectral_data.json has eig[5]=8.5406 (30 modes) — the 12.060 reference is "
            "not reproducible from the persisted file and is re-measured here."
        ),
    }
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "spectral_extended_data.json"), "w") as f:
        json.dump(out, f, indent=2)

    print("\nC3a (lambda(7)=%.3f): nearest mode E=%.4f delta=%.4f -> %s"
          % (LAM7, c3a["nearest_mode_E"], c3a["delta"], out["verdict"]["c3a"]))
    print("C3b (lambda(31)=%.3f): nearest mode E=%.4f delta=%.4f -> %s"
          % (LAM31, c3b["nearest_mode_E"], c3b["delta"], out["verdict"]["c3b"]))
    for row in c1:
        print("C1 k=%d: r_mode=%.4f vs ln(k)=%.4f rel_err=%.4f -> %s"
              % (row["k"], row["r_mode"], row["ln(k)"], row["rel_err"],
                 "hit" if row["rel_err"] < 0.02 else "miss"))
    print("C4: <r>=%.4f median=%.4f -> %s" % (r_mean, r_med, c4["position"]))
    print("Selberg<->zeros: min dist=%.4f over %d modes (was 2.5-9.0 at 30)"
          % (zeta["min_dist"], zeta["n_modes_compared"]))
    print("wrote data/spectral_extended_data.json")


if __name__ == "__main__":
    main()
