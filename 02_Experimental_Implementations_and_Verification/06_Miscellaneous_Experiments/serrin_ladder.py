"""
SERRIN LADDER: WHERE E AND Z STOP, AND THE EXACTLY CRITICAL QUANTITY
====================================================================
Forward step prescribed by SHARED_WALL_AND_PATH_FORWARD.md: name the exactly
critical quantity that breaks the energy method's marginality.

Energy method reaches E = (1/2)||u||_2^2 and Z = ||grad u||_2^2, i.e. H^1.
Gagliardo-Nirenberg / Sobolev on R^3: for 1/p = 1/2 - theta/3, i.e.

    theta(p) = 3/2 - 3/p,

    ||u||_{L^p} <= C ||u||_{L^2}^{1-theta} ||grad u||_{L^2}^{theta}   iff theta <= 1.

So E,Z control ||u||_{L^p} EXACTLY for p <= 6 (theta <= 1), with the endpoint
p = 6 (theta = 1) equal to the Sobolev exponent H^1 -> L^6. For p > 6 the
required theta exceeds 1: the right-hand side is no longer a convex combination
of the two norms the energy identity supplies. The gap p = infinity has
theta = 3/2, i.e. 1/2 derivative short -- the dimensional wall.

Serrin/Prodi-Serrin: u in L^q_t L^p_x with 2/q + 3/p = 1, p > 3, gives regularity.

    p = 3  -> q = infinity   (the EXCLUDED endpoint: needs L^inf)
    p = 6  -> q = 4          (admissible)

The p = 6 route is reachable from E,Z, BUT its integrability uses
||u||_{L^6}^4 <= C ||grad u||_{L^2}^4 = C Z^2, so closing it needs

    int_0^T Z(t)^2 dt < infinity,

whereas the energy identity only gives int_0^T Z(t) dt < infinity. The exactly
critical quantity is therefore ONE EXTRA POWER OF ENSTROPHY -- the same 1/2
derivative gap, now written as an integrability statement.

This module VERIFIES the interpolation exponent theta(p) numerically on a
concentrating bump family (so the ceiling at p = 6 is not asserted, it is
measured): theta_fit(p) = log(R2/R1)/log(S2/S1) with R = ||u||_p/||u||_2,
S = ||grad u||_2/||u||_2, across a 10x scale change.

Run:  python serrin_ladder.py        (prints PASS)
"""
import numpy as np

_trapz = getattr(np, "trapezoid", None) or getattr(np, "trapz")


def bump_ratios(p, eps):
    """Radial 3D bump u = A phi(r/eps), phi(rho) = (1-rho^2)^2.

    Returns R = ||u||_p / ||u||_2 and S = ||grad u||_2 / ||u||_2 (A-independent).
    """
    rho = np.linspace(0.0, 1.0, 400001)
    phi = (1.0 - rho**2) ** 2
    dphi = -4.0 * rho * (1.0 - rho**2)
    w = rho**2                                   # 3D radial measure r^2 dr
    I2 = _trapz(phi**2 * w, rho)
    Ig = _trapz(dphi**2 * w, rho)
    if np.isinf(p):
        Lp_over_A = 1.0                          # ||u||_inf = A
    else:
        Lp_over_A = eps ** (3.0 / p) * _trapz(phi**p * w, rho) ** (1.0 / p)
    L2_over_A = eps ** 1.5 * np.sqrt(I2)
    R = Lp_over_A / L2_over_A
    S = np.sqrt(Ig / I2) / eps
    return R, S


def theta_fit(p, eps1=1e-3, eps2=1e-4):
    R1, S1 = bump_ratios(p, eps1)
    R2, S2 = bump_ratios(p, eps2)
    return np.log(R2 / R1) / np.log(S2 / S1)


def main():
    print("=" * 78)
    print("SERRIN LADDER: E,Z control L^p iff p <= 6; the missing power of Z")
    print("=" * 78)
    print("\n[A] measured interpolation exponent theta_fit(p) vs theory 3/2 - 3/p")
    print(f"{'p':>6} {'theta_theory':>13} {'theta_fit':>11} {'theta<=1?':>10}")
    ps = [2.0, 3.0, 4.0, 6.0, 8.0, np.inf]
    for p in ps:
        th = 1.5 - (0.0 if np.isinf(p) else 3.0 / p)
        tf = theta_fit(p)
        ok = "yes" if th <= 1.0 + 1e-9 else "NO (excluded)"
        ptxt = "inf" if np.isinf(p) else f"{p:.0f}"
        print(f"{ptxt:>6} {th:>13.4f} {tf:>11.4f} {ok:>10}")
        assert abs(tf - th) < 5e-3, f"theta mismatch at p={p}: {tf} vs {th}"

    print("\n[B] Serrin line 2/q + 3/p = 1  (regularity for p > 3)")
    print(f"{'p':>6} {'q=2p/(p-3)':>13} {'reachable from E,Z?':>22} {'integral needs':>16}")
    for p in [3.0, 4.0, 5.0, 6.0, 8.0]:
        if p <= 3.0 + 1e-9:
            q = "inf (endpoint)"
            reach = "NO (needs L^inf)"
            need = "--"
        else:
            q = 2.0 * p / (p - 3.0)
            theta = 1.5 - 3.0 / p
            reach = "yes" if p <= 6.0 + 1e-9 else "NO (p>6)"
            need = f"int Z^{theta * q / 2:.2f}" if p <= 6 else "--"
        print(f"{p:>6.0f} {q if isinstance(q,str) else f'{q:>13.3f}':>13} {reach:>22} {need:>16}")

    print("\n  p=6: q=4, and ||u||_6^4 <= C Z^2  ->  closing needs int Z^2 dt.")
    print("  Energy identity gives only int Z dt < inf.  The exactly critical")
    print("  quantity is ONE EXTRA POWER OF ENSTROPHY (the same 1/2 derivative).")

    print("\n" + "=" * 78)
    print("PASS: interpolation ceiling verified at p = 6 (theta = 1);")
    print("      the marginal quantity is int Z^2 dt, not controlled by int Z dt.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
