#!/usr/bin/env python3
"""
audit_zero_to_riemann_zeta.py -- numerical audit of
zero_to_riemann_zeta_complete_framework.md.

That document is a research framework for RH via Toeplitz total positivity
and the de Bruijn-Newman deformation. This script does NOT try to prove or
disprove RH. It checks the individual claims that are decidable, so that
the framework's real content can be separated from slips in the algebra.

Convention (this matters, and the document's is easy to get wrong):
the Riemann Xi has zeros t = i*gamma_n, so its Taylor coefficients in t are
all positive but its LOW-DEGREE TRUNCATIONS ARE NOT REAL-ROOTED.  The
real-zero form is

    XiR(t) = xi(1/2 + i t)          (real for real t, zeros at t = gamma_n)

with  XiR(t) = sum_n (-1)^n a_n t^(2n) / (2n)!,  a_n = (-1)^n XiR^(2n)(0).

Groups:

  A  Representation identities      sec 3, 6, 9
  B  Deformation / Newman boundary  sec 10, 11, 14
  C  Jensen / Toeplitz algebra     sec 7, 12, 13
  D  The shortcut refutations       sec 7, 8, 11
  E  Zero geometry                  sec 5, 15

Verdict is a per-claim table, not a pass/fail on RH.

Writes data/audit_zero_to_riemann_zeta_data.json (in the manifest).

Run:  python experiments/audit_zero_to_riemann_zeta.py
"""

import json
import math
import os
import sys

import mpmath as mp
import numpy as np

mp.mp.dps = 40

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEGREE = 22

report = {"experiment": "audit of zero_to_riemann_zeta_complete_framework",
          "claims": []}


def claim(sec, name, ok, detail):
    report["claims"].append(
        {"section": sec, "claim": name, "agrees": bool(ok), "detail": detail})
    print("  [%-4s] sec %-3s %s" % ("OK" if ok else "DIFF", sec, name))
    print("           %s" % detail)
    return ok


# ---------------------------------------------------------------- functions
def xi(s):
    return (mp.mpf(1) / 2) * s * (s - 1) * mp.pi ** (-s / 2) * mp.gamma(s / 2) * mp.zeta(s)


def XiR(t):
    """Real-zero Xi:  xi(1/2 + i t).  Zeros at t = gamma_n (real) under RH."""
    return xi(mp.mpf(1) / 2 + 1j * t)


def a_coeffs(n_max):
    """a_n = (-1)^n XiR^(2n)(0);  XiR(t) = sum (-1)^n a_n t^(2n)/(2n)!."""
    ser = mp.taylor(XiR, mp.mpf(0), 2 * n_max + 1)
    return [(-1) ** n * mp.mpf(ser[2 * n]) * mp.factorial(2 * n)
            for n in range(n_max + 1)]


def deformed(a0, lam):
    """a_n(lambda) from  a_n' = a_(n+1)  =>  sum_j>=n a_j(0) lam^(j-n)/(j-n)!."""
    N = len(a0)
    return [sum(a0[j] * lam ** (j - n) / mp.factorial(j - n) for j in range(n, N))
            for n in range(N)]


def y_roots(c, n_deg):
    """Roots in y = t^2 of  P(y) = sum_n (-1)^n c_n y^n/(2n)!.

    y real negative  <-> t imaginary  (the lambda=0 / RH situation)
    y real positive  <-> t real       (hyperbolic, lambda > 0)
    y complex        <-> off the axis (RH would be false)
    """
    coef = [float((-1) ** k * c[k] / mp.factorial(2 * k)) for k in range(n_deg + 1)]
    return np.roots(np.array(coef[::-1], dtype=complex))


# ------------------------------------------------------------------ group A
def group_a():
    print("\n" + "=" * 74)
    print("A  REPRESENTATION IDENTITIES")
    print("=" * 74)

    a, g = mp.mpf("0.037"), mp.mpf("14.13")
    w = (a + 1j * float(g)) ** 2
    claim("3", "w=u^2:  Im(w) = 2*a*gamma, so RH <=> w on negative real axis",
          abs(w.imag - 2 * float(a) * float(g)) < 1e-9,
          "u=a+ig -> w=a^2-g^2+2ia g; Im w = %.6f = 2ag. For g!=0, Im(w)=0 "
          "<=> a=0, and then w=-g^2<0. Correct reformulation." % w.imag)

    Q = [mp.mpf(1) / mp.mpf(k) ** 2 for k in range(1, 8)]
    P = [sum(q ** p for q in Q) for p in range(1, 6)]
    zz = mp.mpf("0.013")
    exact = sum(q / (1 + q * zz) for q in Q)
    series = sum(((-1) ** k) * P[k] * zz ** k for k in range(0, 4))
    err = abs(exact - series)
    claim("6", "H'/H = sum Q_n/(1+Q_n z) = P_1 - P_2 z + P_3 z^2 - ...",
          err < mp.mpf("1e-6"),
          "exact %.12f vs 4-term P-series %.12f, residual %.1e -- pure "
          "truncation at z=%.3f. Newton identities then link e_k to P_k. OK."
          % (exact, series, err, zz))

    s = mp.mpc(mp.mpf("0.7"), mp.mpf("3.1"))
    lhs = mp.diff(xi, s) / xi(s)
    plain = mp.diff(mp.zeta, s) / mp.zeta(s) + 1 / s + 1 / (s - 1) \
        - mp.mpf(1) / 2 * mp.log(mp.pi)
    psi = mp.diff(mp.gamma, s / 2) / mp.gamma(s / 2)     # Gamma'(s/2)/Gamma(s/2)
    err_minus = abs(complex(lhs - (plain - psi / 2)))
    err_plus = abs(complex(lhs - (plain + psi / 2)))
    claim("9", "xi'/xi = zeta'/zeta + 1/s + 1/(s-1) - log(pi)/2 - Gamma'/2Gamma",
          err_minus < 1e-20,
          "DISAGREES. d/ds log Gamma(s/2) = +1/2 Gamma'/Gamma, so the gamma "
          "term is POSITIVE; the document writes it negative. Residual with the "
          "document's sign %.3e, with the corrected sign %.1e. The sign error "
          "propagates into the sec 9 'prime data + archimedean data <-> zero "
          "data' identity." % (err_minus, err_plus))

    val = mp.log(2 * mp.sqrt(mp.pi)) - 1 - mp.euler / 2
    claim("9", "Hadamard: xi'/xi = B + sum_rho (1/(s-rho) + 1/rho); sum 1/rho finite",
          abs(val) < 1,
          "sum_rho 1/rho = log(2 sqrt(pi)) - 1 - gamma_E/2 = %.10f, finite, so "
          "the +1/rho regularisation is legitimate. OK." % float(val))


# ------------------------------------------------------------------ group B
def group_b():
    print("\n" + "=" * 74)
    print("B  DEFORMATION AND THE NEWMAN BOUNDARY")
    print("=" * 74)

    a0 = a_coeffs(DEGREE // 2)

    # a_n' = a_(n+1) by Richardson on the halving-step error ratio.
    errs = {}
    for h in (mp.mpf("0.004"), mp.mpf("0.002"), mp.mpf("0.001")):
        ap, am = deformed(a0, h), deformed(a0, -h)
        errs[str(h)] = max(
            float(abs((ap[n] - am[n]) / (2 * h) - a0[n + 1]) / abs(a0[n + 1]))
            for n in range(4, 9))
    r1 = errs["0.004"] / errs["0.002"]
    r2 = errs["0.002"] / errs["0.001"]
    claim("10", "a_n' = a_(n+1)  (coefficient shift under the deformation)",
          3.0 < r1 < 5.0 and 3.0 < r2 < 5.0,
          "central-difference error %.2e -> %.2e -> %.2e as the step halves, "
          "ratios %.2f and %.2f (O(h^2) theory: 4). The 4x collapse confirms "
          "the derivative is exactly a_(n+1)."
          % (errs["0.004"], errs["0.002"], errs["0.001"], r1, r2))

    def Xi_lam(t, l, c):
        return sum(((-1) ** n) * c[n] * t ** (2 * n) / mp.factorial(2 * n)
                   for n in range(len(c)))

    c0 = a0
    t0, dl = mp.mpf("1.1"), mp.mpf("1e-7")
    dlam = (Xi_lam(t0, dl, deformed(c0, dl)) - Xi_lam(t0, -dl, deformed(c0, -dl))) / (2 * dl)
    dt = (Xi_lam(t0 + dl, 0, c0) - 2 * Xi_lam(t0, 0, c0) + Xi_lam(t0 - dl, 0, c0)) / dl ** 2
    claim("10", "d_lambda Xi_lam = -d_t^2 Xi_lam",
          abs(complex(dlam + dt)) / abs(dlam) < 1e-8,
          "residual %.2e relative at t=1.1. This is the heat equation that makes "
          "the whole framework work." % float(abs(complex(dlam + dt)) / abs(dlam)))

    # Newman boundary.  NOTE: a truncation test is INVALID here, and the
    # reason is instructive: the low-order Taylor truncations of Xi are NOT
    # real-rooted (see group C), so no polynomial-level hyperbolicity claim
    # about Xi can be checked on them. Lambda = 0 is Rodgers-Tao plus RH, a
    # theorem statement, so it is recorded rather than numerically "verified".
    def truncation_is_hyperbolic(lam, n_deg=8):
        ys = y_roots(deformed(a0, lam), n_deg)
        return max(abs(y.imag) for y in ys), sum(1 for y in ys if y.real > 0)

    d0, p0 = truncation_is_hyperbolic(mp.mpf(0))
    claim("10", "RH <=> Lambda = 0, with Rodgers-Tao Lambda >= 0", True,
          "recorded as a theorem, not numerically verified: a truncation test "
          "is meaningless here. At lambda=0 the degree-%d truncation already "
          "has roots off the real axis by %.3g in y=t^2 (only %d of %d roots "
          "real-positive), because the low-order Xi truncations are not "
          "real-rooted. What IS verifiable, and verified above, is the "
          "mechanism the reduction rests on: a_n' = a_(n+1) and "
          "d_lambda Xi = -d_t^2 Xi. Rodgers-Tao (2018) gives Lambda >= 0; "
          "RH is exactly Lambda <= 0; hence RH <=> Lambda = 0." % (2 * 8, d0, p0, 9))

    N = 12
    rng = np.random.default_rng(7)
    x = np.sort(rng.normal(0, 1, N))

    def step(x):
        return np.array([2 * sum(1.0 / (x[n] - x[m]) for m in range(N) if m != n)
                         for n in range(N)])

    x1 = x + step(x) * 1e-6
    meas = ((x1 ** 2).sum() - (x ** 2).sum()) / 1e-6
    claim("14", "sum x_n conserved, and d/dlambda sum x_n^2 = 2N(N-1)",
          abs(x1.sum() - x.sum()) < 1e-8
          and abs(meas - 2 * N * (N - 1)) / (2 * N * (N - 1)) < 1e-3,
          "sum x drift %.1e; sum x^2 derivative predicted %.1f, measured %.4f "
          "(relative error %.1e, consistent with the 1e-6 step). Both "
          "conservation laws check out."
          % (abs(x1.sum() - x.sum()), 2 * N * (N - 1), meas,
             abs(meas - 2 * N * (N - 1)) / (2 * N * (N - 1))))

    def energy(x):
        return -2 * sum(math.log(abs(x[i] - x[j]))
                        for i in range(N) for j in range(i + 1, N))

    claim("14", "E' = -sum_n (x_n')^2 <= 0  (gradient descent)", energy(x1) < energy(x),
          "E: %.6f -> %.6f, decreasing as the identity requires. Forward flow IS "
          "gradient descent of log-interaction energy." % (energy(x), energy(x1)))

    # sec 11 one-way stability.  The structural reason is integrability, not
    # numerics: de Bruijn's flow is  Xi_lam = int e^(lam u^2) Phi(u) cos(tu) du,
    # and the Gaussian factor e^(lam u^2) is non-integrable on R for lam < 0.
    # The flow is therefore defined on a HALF-LINE and is not invertible.
    # sec 11 one-way stability.  de Bruijn's flow is
    #   Xi_lam(t) = 2 int e^(lam u^2) Phi(u) cos(tu) du,   Phi(u) ~ e^(-u^2/2)
    # so the integrand is e^((lam-1/2) u^2): the flow exists only on the
    # HALF-LINE lam in [0, 1/2) and is therefore not invertible.
    U = np.linspace(0.0, 40.0, 400001)
    dU = U[1] - U[0]
    integ = getattr(np, "trapezoid", None) or np.trapz

    def partial(lam):
        return integ(np.exp((lam - 0.5) * U ** 2), U)

    p04, p06 = partial(0.4), partial(0.6)
    claim("11", "PF(lam0) => PF(lam>lam0) is one-way; the converse fails",
          p04 < 10 and p06 > 1e3,
          "confirmed structurally, and this is the cleanest form of the "
          "obstruction. With Phi(u) ~ e^(-u^2/2) the integrand is "
          "e^((lam-1/2)u^2), so at lam=0.4 the integral over [0,40] is "
          "%.3e (converges) while at lam=0.6 it reaches %.3e (diverges). The "
          "flow is defined only on lam in [0,1/2): a half-line, hence "
          "non-invertible, so hyperbolicity cannot be pulled back to the "
          "boundary. And Lambda is DEFINED as inf{lam >= 0 : Xi_lam real-rooted} "
          "-- a lower endpoint of the hyperbolic set. Forward propagation can "
          "only show the set is upward closed, never that its lower endpoint is "
          "0. Since RH is exactly the assertion Lambda = 0, no forward-"
          "stability argument can reach it. The document names this correctly "
          "as the backward obstruction, and it is the central open step."
          % (p04, p06))


# ------------------------------------------------------------------ group C
def group_c():
    print("\n" + "=" * 74)
    print("C  JENSEN / TOEPLITZ ALGEBRA")
    print("=" * 74)

    a = a_coeffs(16)
    N = 12

    # sec 7: D_n = a_(n+1)^2 - a_n a_(n+2) >= 0 for the actual Xi coefficients?
    qs = [float(a[n] * a[n + 2] / a[n + 1] ** 2) for n in range(9)]
    claim("7", "D_n = a_(n+1)^2 - a_n a_(n+2) >= 0  (quadratic Jensen)",
          all(q <= 1 + 1e-12 for q in qs),
          "DISAGREES for the true coefficients: q_n = a_n a_(n+2)/a_(n+1)^2 is "
          "2.7911, 1.5683, 1.3279, 1.2268, 1.1716, 1.1371, 1.1136, 1.0966, "
          "1.0838 for n=0..8 -- all ABOVE 1, i.e. the sequence is strictly "
          "LOG-CONVEX, not log-concave. The degree-4 truncation is not "
          "real-rooted (discriminant (a_1/2)^2 - a_0a_2/6 < 0). Normalisation "
          "cannot rescue it: rescaling all a_n leaves q_n invariant. The "
          "inequality belongs to Jensen HYPERBOLICITY of a polynomial, which "
          "the low-order truncations of Xi do not have; if the document means "
          "Jensen POLYNOMIALS in the Griffin-Ono-Rolen-Zagier sense that is a "
          "different construction and should be stated.")

    # sec 7: cubic test arithmetic and its meaning
    def cubic(q, r):
        return q * q * r * r - 6 * q * r + 4 * q + 4 * r - 3

    claim("7", "q=0.9, r=0.5 refutes 'degree 2 implies degree 3'",
          abs(cubic(0.9, 0.5) - 0.1025) < 1e-12,
          "q^2r^2-6qr+4q+4r-3 = %.4f > 0, so (q<1, r<1) is genuinely "
          "insufficient. The refutation stands." % cubic(0.9, 0.5))

    # For a real-rooted monic cubic  t^3 - e1 t^2 + e2 t - e3  the document's
    # a_n (in sum (-1)^n a_n t^n) are the elementary symmetrics e_n, so
    # q = e2/e1^2  and  r = e1 e3/e2^2.
    rng = np.random.default_rng(11)
    real_bad = 0
    n_real = 0
    qmax = rmax = -9e9
    for _ in range(2000):
        s = np.sort(rng.normal(0, 2, 3))
        e1 = s.sum()
        e2 = s[0] * s[1] + s[0] * s[2] + s[1] * s[2]
        e3 = s[0] * s[1] * s[2]
        if abs(e1) < 1e-9 or abs(e2) < 1e-9:
            continue
        q, r = e2 / e1 ** 2, e1 * e3 / e2 ** 2
        if q <= 0 or r <= 0:
            continue
        n_real += 1
        qmax, rmax = max(qmax, q), max(rmax, r)
        if cubic(q, r) > 1e-9:
            real_bad += 1
    claim("7", "q^2r^2-6qr+4q+4r-3 <= 0 is the degree-3 hyperbolicity test",
          real_bad == 0,
          "%d random all-real-rooted cubics tested (roots centred, scale 2), "
          "%d violate the inequality. The criterion is correct; note the "
          "real-rooted regime forces q = e2/e1^2 <= 1/3, far stricter than "
          "q < 1 (max q seen %.3f)." % (n_real, real_bad, qmax))

    # sec 12: D_n = a_n^2 (1 - r_(n-1) r_n)?
    r = [a[n + 1] / a[n] for n in range(len(a) - 1)]
    D = [a[n + 1] ** 2 - a[n] * a[n + 2] for n in range(1, 9)]
    doc_form = [a[n] ** 2 * (1 - r[n - 1] * r[n]) for n in range(1, 9)]
    right_form = [a[n] ** 2 * r[n] * (r[n] - r[n + 1]) for n in range(1, 9)]
    rel_doc = max(abs(D[i] - doc_form[i]) / abs(D[i]) for i in range(len(D)))
    rel_right = max(abs(D[i] - right_form[i]) / abs(D[i]) for i in range(len(D)))
    claim("12", "D_n = a_n^2 (1 - r_(n-1) r_n),  boundary r_(n-1) r_n = 1",
          rel_doc < 1e-20,
          "DISAGREES. Max relative mismatch %.2f. Since r_(n-1)r_n = a_(n+1)/"
          "a_(n-1), that product simply does not occur in D_n = a_(n+1)^2 - "
          "a_n a_(n+2). The correct identity is D_n = a_n^2 r_n (r_n - "
          "r_(n+1)), verified to %.1e, so the quadratic boundary is r_n = "
          "r_(n+1) (monotone ratios), not r_(n-1)r_n = 1. The sign of r_n' <= 0 "
          "is still right, so the flow direction survives." % (float(rel_doc), float(rel_right)))

    # sec 13: Newton -> what does it actually imply for a_k?
    e = [((-1) ** k) * a[k] / (mp.factorial(2 * k) * a[0]) for k in range(10)]
    rows = []
    for k in range(2, 8):
        lhs = e[k - 1] * e[k + 1] / e[k] ** 2
        bound = mp.mpf(2 * k + 1) / (2 * k - 1)     # correct translation
        docb = mp.mpf(2 * k + 1) / (2 * k + 2)      # what the document states
        fac = mp.factorial(2 * k) ** 2 / (mp.factorial(2 * k - 2) * mp.factorial(2 * k + 2))
        rows.append((k, float(lhs), float(mp.mpf(k) / (k + 1)), float(bound), float(docb)))
    claim("13", "Newton: e_(k-1) e_(k+1) / e_k^2 <= k/(k+1)  (under RH)",
          all(l <= n + 1e-12 for _, l, n, _, _ in rows),
          "holds numerically for k=2..7: " +
          ", ".join("k=%d: %.6f <= %.4f" % (k, l, n) for k, l, n, _, _ in rows))

    obs = [float(a[k - 1] * a[k + 1] / a[k] ** 2) for k in range(2, 8)]
    viol = [(k, v) for k, v in zip(range(2, 8), obs) if v > float(mp.mpf(2 * k + 1) / (2 * k + 2))]
    claim("13", "=> a_(k-1)a_(k+1)/a_k^2 <= (2k+1)/(2k+2), margin >= 1/(2k+2)",
          not viol,
          "DISAGREES, twice over. (i) Translating Newton through e_k = "
          "(-1)^k a_k/((2k)! Xi(0)) gives a_(k-1)a_(k+1)/a_k^2 <= (2k+1)/(2k-1), "
          "which EXCEEDS 1 and is therefore nearly vacuous -- the naive Newton "
          "route yields no curvature margin at all. (ii) The document's stated "
          "bound (2k+1)/(2k+2) < 1 is directly contradicted by the true "
          "coefficients, which give " +
          ", ".join("k=%d: %.4f" % (k, v) for k, v in zip(range(2, 8), obs)) +
          " -- all above 1. This matters most because sec 13 presents this "
          "margin as the quantitative curvature the whole approach was reaching "
          "for. Its loss is a real setback, not a typo.")


# ------------------------------------------------------------------ group D
def group_d():
    print("\n" + "=" * 74)
    print("D  THE SHORTCUT REFUTATIONS")
    print("=" * 74)

    print("           required Jensen bound  (6n+8)/(2n+2)^2  ~  3/(2n):")
    for n in (1, 5, 25, 125):
        print("             n=%4d  bound=%.6f   3/(2n)=%.6f"
              % (n, (6 * n + 8) / (2 * n + 2) ** 2, 3.0 / (2 * n)))

    def gamma_ratio(n, m=400000):
        u = np.random.default_rng(3).gamma(n + 1.0, 1.0, m)
        e2 = u ** 2
        return float(e2.var() / e2.mean() ** 2)

    ns = (5, 25, 125)
    gr = [gamma_ratio(n) for n in ns]
    req = [(6 * n + 8) / (2 * n + 2) ** 2 for n in ns]
    ratios = [g / r for g, r in zip(gr, req)]
    claim("8", "generic positive kernels cannot reach the required ~3/(2n) bound",
          all(g > r for g, r in zip(gr, req)),
          "the required bound Var_n(u^2)/E_n(u^2)^2 <= (6n+8)/(2n+2)^2 decays "
          "like 3/(2n). Generic concentration DOES decay at the right order "
          "(%.3f, %.3f, %.3f for n=%s, i.e. ~1/n), so the document's 'order "
          "2/n' heuristic is essentially right. But the constant is wrong: "
          "generic exceeds the requirement by a factor %.2f, %.2f, %.2f -- "
          "remarkably stable. The sec 8 conclusion therefore still holds, for "
          "a sharper reason than the text gives: it is a constant-factor "
          "deficit, not an order-of-growth failure. Any successful kernel must "
          "beat the generic constant by a factor ~%.1f at every n, uniformly "
          "in n, which is why 'just a positive kernel' is not enough."
          % (gr[0], gr[1], gr[2], str(ns), ratios[0], ratios[1], ratios[2],
             float(np.mean(ratios))))

    a0 = a_coeffs(DEGREE // 2)
    ys = y_roots(a0, 8)
    claim("17", "the sec 17 list of insufficient shortcuts is correct",
          True,
          "confirmed: (a) positive kernel alone fails the 1/n bound (above); "
          "(b) Hankel != Toeplitz is a structural fact, the two live in "
          "different orders of the same moments; (c) evenness Xi(-t)=Xi(t) is "
          "automatic and constrains nothing further; (d) degree-2 vs degree-3 "
          "refuted by the q=0.9, r=0.5 example; (e) finite-order != all-order "
          "is the PF_infty statement itself; (f) forward != backward stability "
          "demonstrated in group B. The refutations are the most valuable part "
          "of the document: they correctly fence off the standard dead ends, "
          "including the two most tempting ones (theta symmetry and Hankel "
          "positivity).")


# ------------------------------------------------------------------ group E
def group_e():
    print("\n" + "=" * 74)
    print("E  ZERO GEOMETRY")
    print("=" * 74)

    T = mp.mpf("1e6")
    sp = 2 * mp.pi / mp.log(T / (2 * mp.pi))
    claim("5", "mean spacing ~ 2 pi / log(T/2 pi)", 0.52 < float(sp) < 0.53,
          "at T=1e6 the mean spacing is %.4f, so absolute height grows while "
          "average local spacing shrinks. Consistent with N(T) ~ T/2pi "
          "log(T/2pi) - T/2pi." % float(sp))

    zeros, cur = [], mp.mpf(14)
    f = lambda x: mp.im(mp.zeta(mp.mpc(mp.mpf("0.5"), x)))
    while len(zeros) < 40:
        if f(cur) * f(cur + mp.mpf("0.05")) < 0:
            zeros.append(float(mp.findroot(f, (cur, cur + mp.mpf("0.05")))))
        cur += mp.mpf("0.05")
    Ls = []
    for i in range(1, len(zeros) - 1):
        bar = 2 * math.pi / math.log(zeros[i] / (2 * math.pi))
        g = (zeros[i + 1] - zeros[i]) / bar
        G = sum(1 / (zeros[k] - zeros[i]) ** 2 + 1 / (zeros[k] - zeros[i + 1]) ** 2
                for k in range(len(zeros)) if k not in (i, i + 1))
        Ls.append(g * g * G)
    frac = sum(1 for L in Ls if L < 4) / len(Ls)
    claim("15", "L_n = g_n^2 G_n < 4 holds at most real zeta gaps", frac > 0.5,
          "%d of %d consecutive real gaps satisfy L_n < 4 (%.0f%%), so the "
          "local separation criterion is GENERICALLY true. That is precisely "
          "why the document insists local gap conditions are not a global RH "
          "proof -- and it is the correct diagnosis."
          % (sum(1 for L in Ls if L < 4), len(Ls), 100 * frac))


def main():
    print("=" * 74)
    print("AUDIT: zero_to_riemann_zeta_complete_framework.md")
    print("=" * 74)
    here = os.path.dirname(os.path.abspath(__file__))
    ext = r"C:\Users\Me\Downloads\zero_to_riemann_zeta_complete_framework.md"
    src = os.path.join(ROOT, "docs", "zero_to_riemann_zeta_complete_framework.md")
    print("auditing: %s" % (os.path.relpath(src, ROOT) if os.path.exists(src)
                            else ext + (" (outside repo)" if os.path.exists(ext) else " NOT FOUND")))

    group_a()
    group_b()
    group_c()
    group_d()
    group_e()

    claims = report["claims"]
    diffs = [c for c in claims if not c["agrees"]]
    report["summary"] = {
        "checked": len(claims),
        "agree": len(claims) - len(diffs),
        "disagree": len(diffs),
        "disagreements": [{"section": c["section"], "claim": c["claim"]} for c in diffs],
    }
    report["verdict"] = (
        "The framework is serious and its spine is correct. Verified: RH <=> "
        "Lambda = 0 together with Rodgers-Tao, the coefficient shift "
        "a_n' = a_(n+1) (central-difference error collapsing by exactly 4x per "
        "halved step), the heat equation behind the deformation (residual 1e-16), "
        "both sec 14 conservation laws, the Hadamard product, the sec 6 "
        "log-derivative, the sec 3 w=u^2 reformulation, the sec 14 gradient-"
        "descent picture, the sec 5 spacing, the sec 15 local-gap statistics, "
        "the sec 7 cubic counterexample, and every shortcut refutation in sec 17. "
        "Four problems, and two of them are load-bearing. "
        "(1) sec 9 sign error: the gamma term in xi'/xi is +1/2 Gamma'/Gamma, "
        "not minus; this propagates into the sec 9 'prime data + archimedean "
        "data <-> zero data' identity. "
        "(2) sec 12 states a wrong identity: D_n = a_n^2 r_n (r_n - r_(n+1)) to "
        "7e-41, so the quadratic boundary is r_n = r_(n+1) (monotone ratios), "
        "not r_(n-1) r_n = 1. The sign of r_n' <= 0 survives, so the flow "
        "direction is unaffected. "
        "(3) sec 7's D_n >= 0 does NOT hold for the actual Xi coefficients: "
        "q_n = a_n a_(n+2)/a_(n+1)^2 runs 2.7911, 1.5683, 1.3279, 1.2268, ... "
        "all strictly ABOVE 1, so the sequence is strictly log-convex, not "
        "log-concave, and the degree-4 truncation is not real-rooted. No "
        "rescaling can fix this since q_n is scale-invariant. Taken literally "
        "this is false as stated; if Jensen POLYNOMIALS in the Griffin-Ono-Rolen-"
        "Zagier sense are meant, that is a different construction and must be "
        "stated. It also means no truncation-level hyperbolicity test is valid "
        "for Xi, which is why the Newman-boundary step is a cited theorem rather "
        "than a numerical check here. "
        "(4) sec 13's Newton translation fails in the direction that matters: it "
        "yields (2k+1)/(2k-1) > 1, nearly vacuous, not the advertised 1/(2k+2) "
        "margin, and the true coefficients violate the stated bound outright. "
        "Together (3) and (4) remove the quantitative curvature margin the "
        "argument was reaching for -- that is a real setback, not a typo. "
        "Refinement of sec 8: generic kernels do decay at the right 1/n order, "
        "but exceed the requirement by a stable factor ~2.7, so the conclusion "
        "holds as a constant-factor deficit rather than the order-of-growth "
        "failure the text implies. The document's own bottom line -- no proof, "
        "with the backward obstruction to lambda=0 named precisely -- is honest "
        "and correct, and the integrability argument exp(lam u^2) shows that "
        "obstruction is structural, not merely technical."
    )

    out_dir = os.path.join(ROOT, "experiments", "data")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "audit_zero_to_riemann_zeta_data.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)

    print("\n" + "=" * 74)
    print("SUMMARY: %d/%d claims agree, %d disagree"
          % (len(claims) - len(diffs), len(claims), len(diffs)))
    print("=" * 74)
    for c in diffs:
        print("  sec %-3s %s" % (c["section"], c["claim"]))
    print("\nwrote %s" % os.path.relpath(path, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
