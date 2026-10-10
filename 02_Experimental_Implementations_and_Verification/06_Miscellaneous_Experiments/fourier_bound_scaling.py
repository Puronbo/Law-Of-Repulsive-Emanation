"""
REFUTATION OF THE LINCHPIN BOUND   ||u||_inf^2 <= 4*E*Z
-------------------------------------------------------
close_the_gap.py (line 2) and final_proof.py (lines 74-92) assert, as the
load-bearing step of a claimed proof of 3D periodic Navier-Stokes global
regularity,

        ||u||_inf^2  <=  4 * E * Z          "for ALL smooth div-free u on T^3",

with   E = (1/2)||u||_2^2,   Z = ||grad u||_2^2,   ||u||_inf = max|u|.

The claim is FALSE.  This module proves it two independent ways and then
shows the Cauchy-Schwarz route cannot be repaired -- which is the real wall.

The square root in ||u||_inf = sqrt(max u^2) is removed by squaring it away
(the a = b^2  =>  a/b = b move): we compare the PERFECT SQUARES
||u||_inf^2 and 4*E*Z directly, so no radical appears anywhere.  The flaw is
then a raw degree count, which no numerical constant can hide.

  (1) DEGREE COUNT (exact; no numerics, no radicals).
      Under u -> a*u  (a > 0):
          ||u||_inf^2  ->  a^2 * ||u||_inf^2     (degree 2 in amplitude)
          E * Z        ->  a^4 * (E * Z)          (degree 4 in amplitude)
      A homogeneous inequality must match degrees, so no constant C makes
      ||u||_inf^2 <= C*E*Z hold for all u: the ratio behaves like 1/a^2 -> inf.
      Hence the bound can only hold on a fixed amplitude slice, which is not
      what is claimed and not enough.

  (2) EXPLICIT GRID FIELD.  Using the repo's OWN metrics(), the scaled family
      u = a*(sin y, sin z, sin x) drives ratio = ||u||_inf^2/(4EZ) past 1
      near a ~ 3e-3, with ratio*a^2 held constant (ratio ~ 1/a^2).

  (3) WHY CAUCHY-SCHWARZ CANNOT FIX IT.  The route needs
          sum_k |u^_k| <= sqrt(Z) * sqrt( sum_{k!=0} 1/|k|^2 ),
      and sum_{k!=0} 1/|k|^2 DIVERGES on Z^3 (partial sums ~ 4*pi*R).  So the
      second factor is infinite: there is NO bound ||u||_inf <= F(E,Z) at all.
      This is not a tuning problem -- H^1(T^3) is not embedded in L^inf(T^3)
      in 3D (the sharp embedding needs H^{3/2+}).  The energy identity reaches
      only H^1, and that gap IS the wall.

PATH FORWARD (interpretive, not a machine-checked claim)
--------------------------------------------------------
The failure is not special to Navier-Stokes; it is the shared skeleton of the
open Millennium walls -- a completed LOCAL/perturbative theory plus one
CRITICAL-SCALE control quantity that is exactly marginal, so it neither decays
enough to close an integral nor is controlled by the available (sub-critical)
norms.  Reconstructing the wall means, in each case, naming the exactly
critical quantity and the next-order term that breaks its marginality:

  problem | local theory that works        | critical quantity that fails        | next-order target
  --------+-------------------------------+--------------------------------------+-------------------------------
  NS      | Serrin/Sobolev scaling        | L^inf control from H^1 (needs H^3/2+)| Besov/Lorentz refinement of ||u||_inf
  RH      | analytic continuation, formula| square-root cancellation in N(T)     | the arithmetic of the O(sqrt T) error term
  PvsNP   | every explicit upper bound    | a uniform circuit lower-bound measure| a non-relativizing (GCT/algebraic) measure
  YM      | perturbative QFT              | non-perturbative measure (marginal g)| Osterwalder-Schrader + mass-gap inequality
  BSD     | each curve's L-function       | uniform analytic-to-arithmetic bridge| Iwasawa/derived correction to the moment

So the "same wall, different perspective" reading is earned only at the level
of this skeleton; the content (method-barrier vs. existence-barrier vs.
bridge-barrier) differs per problem.  For NS the concrete forward step is to
replace the impossible E,Z-only L^inf bound with a critical-space estimate that
is genuinely sub-critical (or to accept the dynamic-rescaling/Type-II route),
rather than to keep sampling O(1)-amplitude fields on which the false bound
looks true.

Run:  python fourier_bound_scaling.py        (prints PASS on success)
"""
import numpy as np


def repo_metrics(ux, uy, uz, kx, ky, kz, N):
    """The metrics() used verbatim by close_the_gap.py / final_proof.py."""
    u2 = ux**2 + uy**2 + uz**2
    vol = (2 * np.pi) ** 3
    h = 2 * np.pi / N
    u_inf = float(np.max(np.sqrt(u2)))
    E = float(np.sum(u2) * h**3 / (2 * vol))
    k2 = kx**2 + ky**2 + kz**2
    Z = sum(float(np.sum(k2 * abs(np.fft.fftn(c)) ** 2)) * h**3 / vol for c in (ux, uy, uz))
    return E, Z, u_inf


def grid(N):
    ax = np.linspace(0, 2 * np.pi, N, endpoint=False)
    X, Y, Zg = np.meshgrid(ax, ax, ax, indexing="ij")
    k1d = np.fft.fftfreq(N, d=(2 * np.pi / N) / (2 * np.pi))
    kx = k1d.reshape(N, 1, 1)
    ky = k1d.reshape(1, N, 1)
    kz = k1d.reshape(1, 1, N)
    return X, Y, Zg, kx, ky, kz


def step0_original_test_looked_fine():
    """Reproduce the original sampling check to show WHY it looked fine."""
    N = 20
    X, Y, Zg, kx, ky, kz = grid(N)
    k2 = kx**2 + ky**2 + kz**2
    k2i = k2.copy(); k2i[0, 0, 0] = 1
    k_inv = 1.0 / k2i; k_inv[0, 0, 0] = 0.0
    np.random.seed(42)
    ratios = []
    for _ in range(200):
        uh = np.random.randn(N, N, N, 3) + 1j * np.random.randn(N, N, N, 3)
        div = 1j * kx * uh[:, :, :, 0] + 1j * ky * uh[:, :, :, 1] + 1j * kz * uh[:, :, :, 2]
        uh[:, :, :, 0] -= 1j * kx * k_inv * div
        uh[:, :, :, 1] -= 1j * ky * k_inv * div
        uh[:, :, :, 2] -= 1j * kz * k_inv * div
        uh[0, 0, 0, :] = 0
        ux = np.real(np.fft.ifftn(uh[:, :, :, 0]))
        uy = np.real(np.fft.ifftn(uh[:, :, :, 1]))
        uz = np.real(np.fft.ifftn(uh[:, :, :, 2]))
        E, Z, inf = repo_metrics(ux, uy, uz, kx, ky, kz, N)
        if E > 1e-10 and Z > 1e-10:
            ratios.append(inf**2 / (4 * E * Z))
    ratios = np.array(ratios)
    print("[0] original sampling check (O(1)-amplitude random fields), N=20:")
    print(f"    {len(ratios)} fields, max ratio = {ratios.max():.4f}  (<< 1 -> looked safe)")
    print("    -> these fields never probe the small-amplitude / concentrated regime.")
    return ratios.max()


def step1_scaling_counterexample():
    N = 40
    X, Y, Zg, kx, ky, kz = grid(N)
    u0x, u0y, u0z = np.sin(Y), np.sin(Zg), np.sin(X)
    div_h = 1j * kx * np.fft.fftn(u0x) + 1j * ky * np.fft.fftn(u0y) + 1j * kz * np.fft.fftn(u0z)
    div_max = float(np.max(np.abs(div_h)))
    print("\n[1] scaled div-free family u = a*(sin y, sin z, sin x), N=40:")
    print(f"    max|div u0| (spectral) = {div_max:.2e}")
    print(f"    {'a':>10} {'||u||_inf^2':>14} {'4EZ':>14} {'ratio':>12} {'ratio*a^2':>12}")
    consts = []
    broke = False
    for a in [1.0, 0.5, 0.1, 0.01, 1e-3, 1e-4]:
        E, Z, inf = repo_metrics(a * u0x, a * u0y, a * u0z, kx, ky, kz, N)
        r = inf**2 / (4 * E * Z)
        consts.append(r * a * a)
        if r > 1.0:
            broke = True
        print(f"    {a:>10.0e} {inf**2:>14.6g} {4*E*Z:>14.6g} {r:>12.4g} {r*a*a:>12.6g}")
    spread = max(consts) / min(consts)
    print(f"    ratio*a^2 spread over 5 decades = {spread:.3f}  (constant => ratio ~ 1/a^2)")
    return broke and spread < 1.01


def step2_single_mode():
    N = 40
    X, Y, Zg, kx, ky, kz = grid(N)
    print("\n[2] single div-free mode u = a*(cos(kz), sin(kz), 0):")
    ok = True
    for k in [1, 4, 8]:
        for a in [1.0, 0.01]:
            cz, sz = np.cos(k * Zg), np.sin(k * Zg)
            E, Z, inf = repo_metrics(a * cz, a * sz, 0.0 * cz, kx, ky, kz, N)
            r = inf**2 / (4 * E * Z)
            print(f"    k={k} a={a:<5}: E={E:.4g} Z={Z:.6g} ||u||_inf^2={inf**2:.4g} ratio={r:.4g}")
    return ok


def step3_cauchy_schwarz_divergence():
    print("\n[3] Cauchy-Schwarz route needs sum_{k!=0} 1/|k|^2 on Z^3 -- it diverges:")
    K = 40
    pts = [(i, j, l) for i in range(-K, K + 1) for j in range(-K, K + 1) for l in range(-K, K + 1)]
    vals = []
    for R in [5, 10, 20, 40]:
        s = sum(1.0 / (kk[0] ** 2 + kk[1] ** 2 + kk[2] ** 2)
                for kk in pts if 0 < kk[0] ** 2 + kk[1] ** 2 + kk[2] ** 2 <= R * R)
        vals.append(s)
        print(f"    sum_(0<|k|<=R) R={R:>3}: {s:>10.3f}   (4*pi*R = {4*np.pi*R:.3f})")
    growth = (vals[-1] - vals[-2]) / (vals[1] - vals[0])
    print(f"    -> linear growth (last increment / early increment = {growth:.2f}); no finite bound.")
    return vals[-1] > vals[0] * 5


def main():
    print("=" * 78)
    print("REFUTATION: ||u||_inf^2 <= 4*E*Z is FALSE for all div-free u on T^3")
    print("=" * 78)
    step0_original_test_looked_fine()
    broke = step1_scaling_counterexample()
    step2_single_mode()
    diverges = step3_cauchy_schwarz_divergence()
    print("\n" + "=" * 78)
    print("VERDICT: the linchpin bound is refuted (degree mismatch); the")
    print("         Cauchy-Schwarz route needs the divergent sum 1/|k|^2, so")
    print("         H^1 cannot control L^inf in 3D.  Global-regularity claim")
    print("         via this route does NOT close.")
    print("=" * 78)
    assert broke, "scaling counterexample failed to break the bound"
    assert diverges, "1/|k|^2 sum unexpectedly looked finite"
    print("PASS: refutation verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
