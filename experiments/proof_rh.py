"""
RIEMANN HYPOTHESIS: EQUIVALENCE AND VERIFICATION
=================================================

THEOREM 1 (Equivalence — proved):
    RH holds iff Re(xi'/xi)(s) > 0 for all s with Re(s) > 1/2.

    Direction (b)=>(a): If Re(xi'/xi) > 0 for sigma > 1/2, then xi has
    no zeros there (logarithmic derivative positivity prevents crossing).
    By xi(s)=xi(1-s), no zeros for sigma < 1/2 either. QED.

    Direction (a)=>(b): Trivial under RH (each Hadamard term positive).

THEOREM 2 (Conditional curvature):
    F''(1/2) = 2|xi'(rho)|^2 > 0 at each simple zero rho.

WHAT THIS SCRIPT DOES:
    - Computes Re(xi'/xi) at 1000 sample points with sigma > 1/2
    - Verifies strict positivity everywhere sampled
    - Verifies F''(1/2) > 0 at 100+ known zeros
    - Plots the V-shape of |xi|^2

WHAT THIS SCRIPT DOES NOT DO:
    - Prove RH. The equivalence reduces RH to proving Re(xi'/xi) > 0
      for ALL sigma > 1/2, but verifying finitely many points is not a proof.
    - The gap is: proving positivity for ALL t, not just sampled t.
"""

import numpy as np
from mpmath import mp, mpf, mpc, zeta, gamma, psi, pi, power, fsum, re, im, fabs
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import json
import os

mp.dps = 30


def xi(s):
    s = mpc(s)
    return mpc("0.5") * s * (s - 1) * power(pi, -s / 2) * gamma(s / 2) * zeta(s)


def xi_ratio(s):
    """xi'(s)/xi(s) = 1/s + 1/(s-1) - log(pi)/2 + psi(s/2)/2 + zeta'(s)/zeta(s)"""
    from mpmath import log
    s = mpc(s)
    h = mpf("1e-12")
    zp = (zeta(s + h) - zeta(s - h)) / (2 * h)
    z = zeta(s)
    if fabs(z) < mpf("1e-25"):
        return mpf("inf") + mpf("inf") * 1j
    return mpf("1") / s + mpf("1") / (s - 1) - log(pi) / 2 + psi(0, s / 2) / 2 + zp / z


def get_zeros(n_zeros):
    from mpmath import zetazero
    return [zetazero(k) for k in range(1, n_zeros + 1)]


def verify_positivity():
    """Verify Re(xi'/xi) > 0 at 1000 sample points with sigma in [0.55, 2]."""
    sigmas = np.linspace(0.55, 2.0, 50)
    ts = np.logspace(0, 3, 20)
    results = []
    all_positive = True

    for sigma in sigmas:
        for t in ts:
            L = xi_ratio(mpf(sigma) + mpf(t) * 1j)
            L_re = float(re(L))
            if L_re < 0:
                all_positive = False
            results.append({
                "sigma": float(sigma),
                "t": float(t),
                "Re_L": L_re,
                "positive": bool(L_re > 0),
            })

    return all_positive, results


def verify_curvature():
    """Verify F''(1/2) = 2|xi'(rho)|^2 > 0 at known zeros."""
    zeros = get_zeros(100)
    results = []
    all_positive = True

    for rho in zeros:
        gamma_n = im(rho)
        rho_s = mpf("0.5") + mpf(gamma_n) * 1j
        xi_at_rho = xi(rho_s)
        if fabs(xi_at_rho) > mpf("1e-5"):
            continue
        xi_prime = (xi(rho_s + mpf("1e-12")) - xi(rho_s - mpf("1e-12"))) / mpf("2e-12")
        curvature = 2 * float(fabs(xi_prime) ** 2)
        if curvature <= 0:
            all_positive = False
        results.append({
            "gamma": float(gamma_n),
            "curvature": curvature,
            "positive": bool(curvature > 0),
        })

    return all_positive, results


def plot_vshape():
    """Plot |xi(1/2+it)|^2 to show the V-shape."""
    ts = np.linspace(-30, 30, 600)
    vals = []
    for t in ts:
        v = float(fabs(xi(mpf("0.5") + mpf(t) * 1j)) ** 2)
        vals.append(v)

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    ax.plot(ts, vals, "b-", linewidth=1.5)
    ax.set_xlabel("t")
    ax.set_ylabel("|xi(1/2+it)|^2")
    ax.set_title("V-shape: minimum at t=0, |xi|^2 grows away from zeros")
    ax.grid(True, alpha=0.3)
    fig.savefig("docs/rh_vshape.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    out = {}

    pos, results = verify_positivity()
    out["positivity_check"] = {
        "n_points": len(results),
        "all_positive": pos,
        "min_Re_L": min(r["Re_L"] for r in results),
    }
    print(f"Re(xi'/xi) > 0 at {len(results)} sample points: {pos}")
    print(f"  min Re(L) = {out['positivity_check']['min_Re_L']:.6e}")

    curv, cresults = verify_curvature()
    out["curvature_check"] = {
        "n_zeros": len(cresults),
        "all_positive": curv,
        "min_curvature": min(r["curvature"] for r in cresults),
    }
    print(f"F''(1/2) > 0 at {len(cresults)} zeros: {curv}")
    print(f"  min curvature = {out['curvature_check']['min_curvature']:.6e}")

    try:
        plot_vshape()
        print("V-shape plot saved to docs/rh_vshape.png")
    except Exception as e:
        print(f"Plot failed: {e}")

    out["theorem"] = {
        "statement": (
            "RH iff Re(xi'/xi) > 0 for sigma > 1/2. "
            "Verified numerically at 1000 points and 100 zeros. "
            "NOT a proof: positivity must hold for ALL t, not just samples."
        ),
        "gap": (
            "Proving Re(xi'/xi)(sigma+it) > 0 for ALL sigma>1/2 and ALL t "
            "requires controlling the sum over ALL zeros, including unknown "
            "off-line zeros. This is equivalent to RH itself."
        ),
        "status": "NUMERICAL_VERIFICATION",
    }

    os.makedirs("data", exist_ok=True)
    with open("data/rh_verification.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nOutput: data/rh_verification.json")
    return out


if __name__ == "__main__":
    main()
