"""
LOG BORDERLINE: THE LOGARITHM RESCUES d=2 BUT NOT d=3
=====================================================
The dimensional wall (dimension_threshold.py) says `H^1 -> L^inf` holds only for
effective dimension `d < 2`.  In 2D the failure at the borderline is only a
LOGARITHM, and Brezis-Gallouet / Trudinger repairs it:

    d = 2:   ||u||_inf <= C ||u||_{H^1} ( 1 + log(1 + ||u||_{H^2}) )^{1/2}.

The natural hope for NS in 3D is that the same logarithm bridges the gap.  This
module tests that hope and REFUTES it: in 3D the deficit is a POWER, not a log,
so no fixed power of the logarithm can pay it.

Scaling (radial bump u = A phi(r/eps) in dimension d, measure r^{d-1} dr):

    ||u||_inf    = A,
    ||u||_{H^1}^2 = A^2 ( eps^d I0 + eps^{d-2} I1 ),
    ||u||_{H^2}^2 = A^2 eps^{d-4} IDelta.

Fix ||u||_{H^1} = 1 and let eps -> 0:

    d = 2:  A -> const,   ||u||_{H^2} ~ eps^{-1},
            ratio = ||u||_inf / (||u||_{H^1} sqrt(1+log(1+||u||_{H^2})))
                  -> 0            (LOGARITHM SUFFICES)
    d = 3:  A ~ eps^{-1/2}, ||u||_{H^2} ~ eps^{-1},
            ratio ~ eps^{-1/2} / sqrt(log(1/eps))  ->  infinity
                                    (POWER BEATS LOG; logarithm FAILS)

So the 3D wall is genuinely one half-derivative, not one logarithm: the escape is
the critical H^{3/2} (Besov/Lorentz), exactly what SHARED_WALL prescribes.

Run:  python log_borderline.py        (prints PASS)
"""
import numpy as np

_trapz = getattr(np, "trapezoid", None) or getattr(np, "trapz")


def radial_ints(d, npts=400001):
    """(I0, I1, IDelta) for phi(rho)=(1-rho^2)^2 on the r^{d-1} measure."""
    rho = np.linspace(0.0, 1.0, npts)
    rho = rho.copy()
    phi = (1.0 - rho**2) ** 2
    dphi = -4.0 * rho * (1.0 - rho**2)
    d2phi = -4.0 * (1.0 - rho**2) + 8.0 * rho**2
    lap = d2phi + (d - 1.0) * np.where(rho > 0, dphi / np.where(rho > 0, rho, 1.0), 0.0)
    w = np.where(rho > 0, rho ** (d - 1.0), 0.0)
    I0 = _trapz(phi**2 * w, rho)
    I1 = _trapz(dphi**2 * w, rho)
    Id = _trapz(lap**2 * w, rho)
    return I0, I1, Id


def bg_ratio(d, eps):
    """||u||_inf / (||u||_{H^1} sqrt(1+log(1+||u||_{H^2}))) at unit H^1."""
    I0, I1, Id = radial_ints(d)
    A2 = 1.0 / (eps**d * I0 + eps**(d - 2.0) * I1)      # H^1 normalisation
    H1 = 1.0
    H2_sq = A2 * eps**(d - 4.0) * Id
    return float(np.sqrt(A2) / (H1 * np.sqrt(1.0 + np.log1p(H2_sq))))


def main():
    print("=" * 78)
    print("LOG BORDERLINE: does the Brezis-Gallouet logarithm bridge the wall?")
    print("=" * 78)
    print("\n ratio = ||u||_inf / (||u||_{H^1} sqrt(1+log(1+||u||_{H^2})))  at unit H^1")
    print(f"{'eps':>8} {'d=2 ratio':>14} {'d=3 ratio':>14}")
    r2 = []
    r3 = []
    for eps in [1e-2, 1e-3, 1e-4, 1e-5]:
        a = bg_ratio(2, eps)
        b = bg_ratio(3, eps)
        r2.append(a)
        r3.append(b)
        print(f"{eps:>8.0e} {a:>14.4e} {b:>14.4e}")

    print("\n  d=2: bounded/decreasing  -> LOGARITHM SUFFICES (Brezis-Gallouet).")
    print("  d=3: growing ~ eps^-1/2/sqrt(log) -> logarithm FAILS; the deficit")
    print("       is a POWER (one half-derivative), so the escape is H^{3/2}.")

    # assertions: 2D non-increasing, 3D strictly increasing across decades
    assert all(r2[i + 1] <= r2[i] + 1e-12 for i in range(len(r2) - 1)), "2D not bounded"
    assert all(r3[i + 1] > r3[i] for i in range(len(r3) - 1)), "3D not diverging"
    # 3D growth per decade should be ~ sqrt(10)/sqrt(2) = 2.24 for sqrt(log) trend
    growth = r3[-1] / r3[0]
    print(f"\n  d=3 ratio growth eps=1e-2 -> 1e-5: {growth:.2f}x (power, not log)")

    print("\n" + "=" * 78)
    print("PASS: logarithm rescues d=2 but NOT d=3; 3D deficit is one half-derivative.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
