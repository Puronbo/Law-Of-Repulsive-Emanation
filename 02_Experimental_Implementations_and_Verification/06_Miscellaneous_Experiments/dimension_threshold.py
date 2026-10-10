"""
DIMENSION IS THE OBSTRUCTION
============================
The refuted NS bound (see fourier_bound_scaling.py) failed because it tried to
get L^inf control of u from E = (1/2)||u||_2^2 and Z = ||grad u||_2^2, i.e. from
the H^1 norm.  Sobolev embedding says that is possible only BELOW a critical
dimension:

        H^1(R^D)  embeds in  L^inf(R^D)     <=>   D < 2.

At D = 3 we are one half-derivative short: we need H^{s} with s > D/2, we have
s = 1.  So the wall is dimensional, not a missing constant.

This module makes the threshold concrete for REAL dimension D (and for the
generalised radial weight r^n of the Delta_n operator), by rescaling a bump at
the origin and measuring L^inf with H^1 NORMALISED.  Then it defines precisely
what "a mixture of dimensions" can mean.

Setup: on R^D use the radial measure r^{D-1} dr.  For u = A*phi(r/eps),
with phi a fixed bump (phi(0)=1, support [0,1]),

    E  = int u^2  r^{D-1} dr  ~  A^2 eps^D   * I0,
    Z  = int u'^2 r^{D-1} dr  ~  A^2 eps^{D-2} * I1,     I0,I1 = O(1),
    ||u||_inf = A.

Normalise H^1 = E + Z = 1.  Then  ||u||_inf^2 = A^2 = 1 / (eps^D I0 + eps^{D-2} I1):

    D < 2 :  eps^{D-2} dominates -> A^2 -> 0   (L^inf controlled; embedding HOLDS)
    D = 2 :  both are O(1)       -> A^2 -> const (borderline: BMO, log)
    D > 2 :  eps^{D-2} -> 0      -> A^2 -> inf (L^inf NOT controlled; FAILS)

So the critical dimension is exactly 2, and this is what "dimension is the
problem" means numerically.  (D is a real parameter here: the weight r^{D-1},
so the same integral interpolates continuously across dimensions.)

THE "MIXTURE OF ALL DIMENSIONS" READING
---------------------------------------
Two precise readings, both already present in this repo's objects:

 (i) CONTINUOUS / ANALYTIC DIMENSION.  The reduced operator
         Delta_n = d_rr + (n/r) d_r + d_zz          (weight r^n dr, self-adjoint)
     has n as a continuous parameter.  Physical axisymmetric swirl is n = 3
     (worse than the scalar D = 3 case, n = 2); Hou's fitted effective dimension
     is n ~ 3.188.  A "mixture" is a superposition int Delta_n dmu(n).  The
     threshold above is n_c = 1 (equivalently D_c = 2), and every physical n
     sits ABOVE it -- so no fixed-n member of the family closes the energy
     method.  This is exactly Frontier 1's proposed next step: make n a
     dynamical eigenvalue rather than a constant (SelfSimilarExponents.lean
     already proves the EXPONENTS are n-independent, but the SHAPE is not).

 (ii) MULTIFRACTAL / INTERMITTENCY SPECTRUM.  The standard physical meaning of
     "a mixture of all dimensions" is that dissipation concentrates on a
     multifractal set with a continuum of local dimensions alpha, described by
     the singularity spectrum f(alpha).  The energy method sees the WORST local
     dimension where mass concentrates; intermittency can make that effective
     dimension strictly less than the ambient 3.  This is the genuine hope --
     and the genuinely open part: no admissible mixture is known that (a)
     preserves the equation's structure and (b) lands the effective dimension
     below 2 at every scale.

Honesty: this note reconstructs the wall as a DIMENSIONAL threshold and locates
"mixing dimensions" precisely.  It does NOT close the wall: it shows that the
closure condition is d_eff < 2, and that no fixed-dimension member of the
Delta_n family achieves it.  Whether a dynamical/multifractal mixture can is
the open content.

Run:  python dimension_threshold.py       (prints PASS)
"""
import numpy as np

_trapz = getattr(np, "trapezoid", None) or getattr(np, "trapz")


def normalised_inf(d, eps, npts=400001):
    """||u||_inf^2 for a unit-H^1 bump of width eps in effective dimension d.

    Measure r^{d-1} dr on [0,1]; u = A*phi(r/eps) with phi(rho)=(1-rho^2)^2.
    H^1 normalised: A^2 (eps^d I0 + eps^{d-2} I1) = 1.
    """
    rho = np.linspace(0.0, 1.0, npts)
    phi = (1.0 - rho**2) ** 2
    dphi = -4.0 * rho * (1.0 - rho**2)
    w = np.where(rho > 0, rho ** (d - 1.0), 0.0)   # d >= 1 here, so finite
    I0 = _trapz(phi**2 * w, rho)
    I1 = _trapz(dphi**2 * w, rho)
    A2 = 1.0 / (eps**d * I0 + eps**(d - 2.0) * I1)
    return A2, I0, I1


def main():
    print("=" * 78)
    print("DIMENSIONAL THRESHOLD FOR L^inf CONTROL FROM H^1")
    print("=" * 78)
    print("||u||_inf^2 of a unit-H^1 bump at two widths (should DIVERGE as eps->0")
    print("only for d > 2, stay bounded for d <= 2):\n")
    ds = [1.0, 1.5, 1.9, 2.0, 2.1, 2.5, 3.0, 3.5]
    print(f"{'d':>5} {'eps=1e-3':>16} {'eps=1e-4':>16} {'ratio(x10)':>12}  verdict")
    diverging = []
    for d in ds:
        a3, _, _ = normalised_inf(d, 1e-3)
        a4, _, _ = normalised_inf(d, 1e-4)
        ratio = a4 / a3
        verdict = "UNBOUNDED (fails)" if ratio > 1.05 else "bounded (holds)"
        if ratio > 1.05:
            diverging.append(d)
        print(f"{d:>5} {a3:>16.6g} {a4:>16.6g} {ratio:>12.4g}  {verdict}")

    print()
    first_div = min(diverging)
    print(f"  -> bounded at d = 2.0, diverging by d = {first_div:.1f}; threshold d_c = 2.")
    print("  -> physical D=3 sits ABOVE threshold: energy method is short.")
    print()

    # D = 3 quantitatively: how short are we?  need s > D/2 = 1.5, have s = 1.
    for D in [2.0, 3.0, 3.188]:
        print(f"  D = {D:>5}: required s > D/2 = {D/2:.3f}; available s = 1; "
              f"gap = {D/2 - 1:.3f} derivative")

    print()
    print("  'mixture of all dimensions' readings:")
    print("   (i)  Delta_n family (weight r^n): threshold n_c = 1; physical n=3")
    print("        and Hou's n~3.188 are both ABOVE it -> no fixed n closes it.")
    print("   (ii) multifractal intermittency: effective local dimension < 3 is")
    print("        the hope; proving d_eff < 2 at every scale is the open part.")
    print("=" * 78)
    assert 2.0 < first_div <= 2.1, "threshold moved off d=2"
    print("PASS: threshold verified: bounded at =2, fails above; d_c = 2.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
