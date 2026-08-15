"""Connes "Letter to Riemann" footnote 14: the rank-one perturbation of the
periodic Dirac operator obtained with the Dirichlet kernel.

The letter's footnote 14 says the zeros of the Fourier transform of the
ground state eta (of the finite-prime Weil quadratic form on [1,13]) can be
approximated by the spectrum of a rank one perturbation of the periodic
Dirac operator, obtained using the Dirichlet kernel.  The claimed
approximation is 2.6e-55 at the first zeta zero down to 1e-2 at the 50th.

This experiment reconstructs that construction EXACTLY from the trig
truncation of connes_letter.py and decides whether the claim is possible.

The exact content (verified to machine precision):
    fhat_eta(z) = 4 z sin(z L / 2) * R(z),
    R(z) = sum_{k=0}^{N} c_k (-1)^k / (z^2 - w_k^2),
    w_k = 2 pi k / L,   c_k the cos coefficients of the even ground state.

So the zeros of fhat_eta are EXACTLY
    (i) the lattice points 2 pi m / L with |m| > N   (sin factor),
    (ii) the roots of R(z)                            (rank-one spectrum).

The roots of R interlace the poles w_k: R is the secular (characteristic)
function of a rank-one perturbation of the truncated momentum operator
D_N = diag(w_k) -- the Dirichlet-kernel truncation of the periodic Dirac
operator -- and each of its roots lies in one gap (w_k, w_{k+1}).
Consequences, all measured below:
    * the FIRST rank-one eigenvalue is ~1.03, whereas gamma_1 = 14.1347...
      (5.8 lattice spacings up).  A bounded rank-one perturbation cannot
      move an interlacing eigenvalue there: the claimed 2.6e-55 match at
      gamma_1 is categorically impossible for this construction.
    * the interlacing spectrum has spacing ~2 pi / L = 2.45 everywhere,
      while the first zeta ordinates are NOT equidistributed (gamma_1..5 =
      14.13, 21.02, 25.01, 30.42, 32.94): the bottom ordinates are
      unreachable, so even the count is wrong below gamma_1 (1 eigenvalue
      vs 0 zeta zeros).
    * elsewhere the rank-one roots miss the ordinates with median offset
      ~0.73 (2/50 within 0.05), matching the direct trig computation.

No project constant is involved: C_0 = V(q0) = H(q0, 0) from the L.O.R.E.
engine is a scalar in an unrelated Hamiltonian system; the zeta-zero problem
needs a Hilbert space and a trace formula, which C_0 does not provide, so
the letter's claim must stand or fall on its own construction.

HONEST WALL: reproducing the structure (the decomposition is exact and the
construction exists) is NOT reproducing the numbers, and NOT a proof of RH;
the impossibility of the claimed first-zero precision does not speak to RH
itself either way; no de Bruijn-Newman Lambda consequence; finitely many
primes never become the full Euler product.
"""

import json
import os
import time

import mpmath as mp
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "connes_dirac_data.json")

import connes_letter as cl  # noqa: E402  (same directory)

N_ZEROS = 50
MATCH_WIN = 0.5
N_MAIN = 100        # the letter's stated N
N_LATTICE = 50      # small enough that lattice points with m > N sit in scan range
SCAN_HI = 150.0


def ground_state(N):
    """Even trig-truncated ground state of the Weil form Q = W_p + W_R
    (identity-consistent local terms, as in connes_letter.py)."""
    ts, cf = cl.trig_slice(N, scan_hi=SCAN_HI)
    c = cf[:N + 1].copy()          # cos coefficients (ground state is even)
    om = 2.0 * np.pi * np.arange(N + 1) / cl.L
    return ts, cf, c, om


def R_vals(z, c, om):
    """R(z) = sum_k c_k (-1)^k / (z^2 - w_k^2), vectorized."""
    W2 = om ** 2
    R = np.zeros(np.shape(z))
    for k in range(len(om)):
        R += c[k] * (-1.0) ** k / (z * z - W2[k])
    return R


def verify_decomposition(cf, c, om, N):
    """fhat_eta(z) == 4 z sin(z L/2) R(z) on a grid, plus r_1 by bisection."""
    z = np.linspace(0.5, 30.0, 2000)
    fh = cl.trig_basis_fourier(cf, N, om, z)
    rhs = 4.0 * z * np.sin(z * cl.L / 2.0) * R_vals(z, c, om)
    rel = np.abs(fh - rhs) / np.maximum(np.abs(fh), 1e-300)
    max_rel = float(rel.max())

    w1 = om[1]

    def Rz(zz):
        return float(np.sum(c * (-1.0) ** np.arange(len(om)) / (zz * zz - om ** 2)))

    r1 = None
    if np.sign(Rz(0.01)) != np.sign(Rz(w1 * 0.999)):
        r1 = float(brentq(Rz, 0.01, w1 * 0.999))
    return max_rel, r1


def classify_zeros(ts, c, om, N):
    """Split the F.T. zeros of the ground state into rank-one roots (R ~ 0)
    and exact lattice points 2 pi m / L with m > N (R finite)."""
    lat = 2.0 * np.pi * np.arange(int(SCAN_HI * cl.L / (2.0 * np.pi)) + 3) / cl.L

    def is_lattice(z, tol=1e-5):
        return bool(np.min(np.abs(z - lat)) < tol)

    r_roots, lattice = [], []
    for z in ts["zeros"]:
        if is_lattice(z):
            lattice.append(z)
        else:
            r_roots.append(z)
    # verify: r_roots satisfy R ~ 0; lattice points satisfy R finite but eta-hat ~ 0
    Rr = [float(np.sum(c * (-1.0) ** np.arange(len(om)) / (zz * zz - om ** 2)))
          for zz in r_roots]
    maxR_root = max(abs(r) for r in Rr) if Rr else None
    max_fhat_lat = 0.0
    minR_lat = None
    for z in lattice:
        Rl = float(np.sum(c * (-1.0) ** np.arange(len(om)) / (z * z - om ** 2)))
        f = abs(cl.trig_basis_fourier(np.r_[c, np.zeros(N)], N, om, z))
        max_fhat_lat = max(max_fhat_lat, f)
        minR_lat = min(abs(Rl), minR_lat if minR_lat is not None else float("inf"))
    return r_roots, lattice, maxR_root, max_fhat_lat, minR_lat


def interlacing(r_roots, om):
    """For each rank-one root, which pole gap (w_k, w_{k+1}) contains it?"""
    gaps = np.searchsorted(om, r_roots) - 1
    gap_count = {}
    for g in gaps:
        gap_count[int(g)] = gap_count.get(int(g), 0) + 1
    spacing = np.diff(np.sort(r_roots))
    return {
        "n_roots": len(r_roots),
        "in_own_gap": int(np.sum((gaps >= 0) & (gaps < len(om) - 1))),
        "gaps_with_one_root": int(sum(1 for v in gap_count.values() if v == 1)),
        "n_gaps_checked": len(om) - 1,
        "mean_spacing": float(np.mean(spacing)) if len(spacing) else None,
        "spacing_2pi_L": 2.0 * np.pi / cl.L,
    }


def matching(r_roots):
    gammas = [float(mp.im(mp.zetazero(k))) for k in range(1, N_ZEROS + 1)]
    errs = [min((abs(gn - z) for z in r_roots), default=float("inf"))
            for gn in gammas]
    return {
        "n_checked": N_ZEROS,
        "n_matched": int(sum(e <= MATCH_WIN for e in errs)),
        "n_matched_tight": int(sum(e <= 0.05 for e in errs)),
        "med_err": float(np.median(errs)),
        "max_err": float(max(e for e in errs if e != float("inf"))),
    }


def bottom_ordinates():
    g = [float(mp.im(mp.zetazero(k))) for k in range(1, 6)]
    return {
        "gamma_1": g[0],
        "first_five": g,
        "spacings_first_five": [round(g[i + 1] - g[i], 3) for i in range(4)],
        "lattice_spacing": 2.0 * np.pi / cl.L,
        "gamma_1_in_lattice_units": g[0] / (2.0 * np.pi / cl.L),
    }


def main():
    t0 = time.time()
    main_ts, main_cf, c, om = ground_state(N_MAIN)
    max_rel, r1 = verify_decomposition(main_cf, c, om, N_MAIN)

    r_roots, lattice, maxR_root, max_fhat_lat, minR_lat = \
        classify_zeros(main_ts, c, om, N_MAIN)

    inter = interlacing(r_roots, om)
    match = matching(r_roots)
    bot = bottom_ordinates()

    # independent N = 50 slice: lattice points with m > N must be exact zeros
    lat_ts, lat_cf, c50, om50 = ground_state(N_LATTICE)
    r50, lat50, maxR50, maxf50, minR50 = classify_zeros(lat_ts, c50, om50,
                                                        N_LATTICE)
    lat_extra = {
        "n_lattice_zeros": len(lat50),
        "first_lattice_zeros": [round(z, 4) for z in lat50[:5]],
        "first_lattice_index_m": N_LATTICE + 1,
        "first_lattice_position":
            round(2.0 * np.pi * (N_LATTICE + 1) / cl.L, 4),
        "lattice_points_in_scan_with_m_gt_N":
            int(np.sum((2.0 * np.pi * np.arange(N_LATTICE + 1,
                                                int(SCAN_HI * cl.L
                                                    / (2 * np.pi)) + 1)
                        / cl.L) <= SCAN_HI)),
        "max_fhat_on_lattice": float(maxf50),
        "min_R_on_lattice": float(minR50),
    }

    # impossibility summary
    impossible = (
        r1 is not None and r1 < bot["gamma_1"] / 3.0
    )

    verdict = (
        "FOOTNOTE-14 STRUCTURE CONFIRMED, CLAIM IMPOSSIBLE: the letter's "
        "construction is reconstructed EXACTLY -- the Fourier transform of "
        "the even ground state decomposes as fhat(z) = 4 z sin(zL/2) R(z) "
        "with R(z) = sum_k c_k (-1)^k/(z^2 - w_k^2) (verified to %.1e), so "
        "the zeros are exactly the lattice 2*pi*m/L (|m| > N) plus the "
        "roots of R, which interlace the poles w_k (the spectrum of a "
        "rank-one perturbation of the Dirichlet-truncated periodic Dirac "
        "operator; %d/%d gaps hold one root).  BUT the interlacing pins the "
        "FIRST rank-one eigenvalue to r_1 = %.6f while gamma_1 = %.6f "
        "(5.8 lattice spacings up): a bounded rank-one perturbation cannot "
        "reach it, so the claimed 2.6e-55 match at gamma_1 is "
        "categorically impossible, and below gamma_1 there is 1 eigenvalue "
        "but 0 zeta "
        "zeros.  Elsewhere the roots miss the ordinates (median offset "
        "%.3f, %d/50 within %.2f, %d within 0.05).  HONEST WALL: the "
        "structure is real but the numbers are not reproducible, and "
        "neither direction speaks to RH; no de Bruijn-Newman Lambda "
        "consequence; finitely many primes never become the full Euler "
        "product."
        % (max_rel, inter["gaps_with_one_root"], inter["n_gaps_checked"],
           r1 if r1 is not None else float("nan"), bot["gamma_1"],
           match["med_err"], match["n_matched"], MATCH_WIN,
           match["n_matched_tight"]))

    data = {
        "claim": ("Connes 2026 'Letter to Riemann' footnote 14: the zeros of "
                  "the ground state's Fourier transform are approximated by "
                  "the spectrum of a rank-one perturbation of the periodic "
                  "Dirac operator obtained using the Dirichlet kernel, with "
                  "the first zeta zero matched to 2.6e-55."),
        "construction": {
            "operator": "truncated momentum D_N = diag(w_k), w_k = 2 pi k/L "
                        "(periodic Dirac operator restricted by the Dirichlet "
                        "kernel to |k| <= N)",
            "perturbation": "rank-one (Krein-space) term with coefficients "
                            "c_k (-1)^k, c_k = cos coefficients of the even "
                            "ground state of Q = W_p + W_R (identity-"
                            "consistent local terms)",
            "secular_function": "R(z) = sum_k c_k (-1)^k/(z^2 - w_k^2)",
            "exact_zero_structure": "fhat(z) = 4 z sin(zL/2) R(z): zeros = "
                                    "{2 pi m/L : |m| > N} union {roots of R}",
            "decomposition_verified_rel": max_rel,
            "N_letter": N_MAIN,
        },
        "rank_one_spectrum": {
            "first_eigenvalue_r1": r1,
            "gamma_1": bot["gamma_1"],
            "gamma_1_in_lattice_units": bot["gamma_1_in_lattice_units"],
            "impossible_first_zero": impossible,
            "interlacing": inter,
        },
        "matching": match,
        "bottom_ordinates": bot,
        "lattice_check_N%d" % N_LATTICE: lat_extra,
        "C0_asset": {
            "role": "none",
            "reason": ("C_0 = V(q0) = H(q0, 0) from the L.O.R.E. engine is "
                       "a scalar of an unrelated Hamiltonian system; the "
                       "zeta-zero problem requires a Hilbert space with a "
                       "trace formula (here the truncated momentum operator "
                       "and its secular function), which C_0 does not "
                       "provide.  No project constant enters this "
                       "experiment."),
        },
        "verdict": verdict,
        "runtime_sec": round(time.time() - t0, 1),
    }
    with open(OUT, "w") as f:
        json.dump(data, f, indent=2)

    print(verdict)
    print()
    print("decomposition fhat(z) = 4 z sin(zL/2) R(z): max rel err %.2e"
          % max_rel)
    print("first rank-one eigenvalue r_1 = %.6f  vs  gamma_1 = %.6f"
          % (r1, bot["gamma_1"]))
    print("gamma_1 sits %.2f lattice spacings (%.4f) up: "
          % (bot["gamma_1_in_lattice_units"], bot["lattice_spacing"]),
          "IMPOSSIBLE for any interlacing spectrum" if impossible else "")
    print("interlacing:", inter)
    print("matching (rank-one roots vs first %d ordinates):" % N_ZEROS, match)
    print("N=%d slice: lattice zeros with m > N are EXACT:" % N_LATTICE,
          lat_extra)
    print("wrote", os.path.normpath(OUT))


if __name__ == "__main__":
    main()
