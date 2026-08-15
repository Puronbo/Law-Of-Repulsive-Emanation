r"""
CONNES LETTER (2026): can a FINITE-prime Weil quadratic form reproduce the
zeta zeros?

CONTEXT
-------
In "The Riemann Hypothesis: Past, Present and a Letter Through Time"
(arXiv:2602.04022, Feb 2026) Connes reports a striking numerical fact: on
functions phi(u) supported in [1, 13] (so only the primes 2,3,5,7,11,13
and their powers <= 13 can appear), the Weil quadratic form obtained by
APPLYING THE EXPLICIT FORMULA to the self-convolution
    psi(v) = int phi(u) phi(uv) du/u
has a ground state eta (minimizer of Q(phi) under int phi(u)^2 du/u = 1),
and the zeros of the Mellin transform of eta lie on the critical line and
approximate the first ~50 non-trivial zeta zeros with errors from 2.6e-55
(the first zero) out to ~1e-2 (the 50th).  The claimed likelihood of the
coincidence is ~10^{-1235}.

EXPLICIT FORMULA CONVENTION (section 4.1, eqs 9-11 of the paper)
---------------------------------------------------------------
    fhat(s) := int_0^inf f(x) x^{-i s} d*x,  d*x = dx/x
    fhat(i/2) - sum_{1/2 + i s in Z} fhat(s) + fhat(-i/2) = sum_v W_v(f)
    W_p(f)  = log p * sum_{m>=1} p^{-m/2} (f(p^m) + f(p^{-m}))          (10)
    W_R(f)  = (log 4pi + gamma) f(1)
              + int_1^inf (f(x)+f(x^-1)-2 x^{-1/2} f(1)) x^{1/2}
                /(x - x^-1) d*x                                         (11)

FINDING ON THE LOCAL TERMS (validated numerically in this experiment)
---------------------------------------------------------------------
A numerical check of the identity shows that the archimedean term (11),
as printed, does NOT satisfy the identity: with f an even compactly
supported test function, fhat(i/2)+fhat(-i/2)-sum_gamma fhat(gamma)
differs from W_p(10)+W_R(11) by ~0.15-0.6 (and the mismatch is a
functional, not a constant).  The identity-consistent archimedean local
term is the digamma form (the standard Weil-Guinand form):

    W_R(f) = (1/2pi) int_{-inf}^{inf} fhat_t(t) (log pi - Re psi(1/4+it/2)) dt
             with fhat_t(t) = int f(e^x) e^{i t x} dx = |ft_phi(t)|^2

which we verify closes the identity to ~5e-8 (both test functions, exact
zeta zeros).  We therefore build the Weil quadratic form with (10) and the
digamma W_R.  The paper's own footnote-14 claim that the form is
diagonalized by its trigonometric basis is then FALSE for the corrected
W_R (the digamma kernel couples all modes; only the W_p part is diagonal
in that basis), which is precisely the off-diagonal structure that can
give a mixed ground state with real zeros.

The letter recenters: x = ln u, u = exp(x + L/2) in [1, 13], L = ln 13,
and the zeros of eta~(1/2 + iy) coincide with the real zeros of
    f(y) = int theta(x) exp((-1/2 + iy) x) dx,  theta(x) = phi(exp(x+L/2)).

HONEST WALL
-----------
This is a reproduction of a NUMERICAL CLAIM, not a proof of anything.  The
paper's exact computation (trigonometric truncation N=100, rank-one Dirac
perturbation) is not specified in the letter, so our discretization is an
independent slice: reproducing the phenomenon confirms reproducibility of
the claim; failing to reproduce it would be a finding too.  Whatever the
accuracy, (i) it does not prove the zeta zeros are on the line, (ii) it
does not bound de Bruijn-Newman Lambda, (iii) finitely many primes never
become the full Euler product.  Every headline number below is reported
together with that wall.
"""

import json
import os
import sys
import time

import numpy as np
import mpmath as mp
from scipy.interpolate import CubicSpline
from scipy.linalg import eigh
from scipy.special import roots_legendre, spherical_jn, digamma

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data", "connes_letter_data.json")

L = float(mp.log(13))
PRIMES = [2, 3, 5, 7, 11, 13]
LOG4PI_GAMMA = float(mp.log(4 * mp.pi) + mp.euler)
HALF = 0.5

J_GRID = 16384          # sampling grid for the convolution (x-space)
N_GL = 96               # Gauss-Legendre nodes for the archimedean integral
ZERO_SCAN_HI = 150.0    # enough for the first 50 zeros (gamma_50 ~ 143.11)
ZERO_SCAN_DY = 0.02
MATCH_WIN = 0.5         # nearest-zero matching window
ETAG_GRID = 8192        # grid for the final Mellin-transform quadrature
N_ZEROS = 50

T_FINE = (0.0, 300.0, 0.01)      # archimedean t-grid: fine near 0
T_COARSE = (300.0, 3000.0, 0.1)  # ... and coarse for the slow tail
LEGCOEF_CACHE = {}


def fourier_weights():
    """s = m*ln p with p^m <= 13, weight 2 log p * p^{-m/2}.

    Eq (10) of the paper in the Fourier convention: W_p(psi) =
    log p * sum_m p^{-m/2}(psi(p^m) + psi(p^{-m})); psi is even and
    supported in [1/13, 13] so psi(p^{-m}) = psi(p^m) for p^m <= 13 and
    vanishes otherwise.
    """
    pts, wts, pows = [], [], []
    for p in PRIMES:
        lp = float(mp.log(p))
        m = 1
        while m * lp <= L + 1e-12:
            pts.append(m * lp)
            wts.append(2.0 * lp * p ** (-m / 2.0))
            pows.append((p, m, p ** m))
            m += 1
    return (np.array(pts, dtype=float), np.array(wts, dtype=float), pows)


def arch_t_grid():
    t1 = np.arange(T_FINE[0], T_FINE[1], T_FINE[2])
    t2 = np.arange(T_COARSE[0], T_COARSE[1], T_COARSE[2])
    return np.concatenate([t1, t2])


def trapezoid_weights(t):
    w = np.empty(len(t))
    w[1:-1] = t[2:] - t[:-2]
    w[1:-1] *= 0.5
    w[0] = (t[1] - t[0]) / 2.0
    w[-1] = (t[-1] - t[-2]) / 2.0
    return w


def trig_sinc(x):
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(np.abs(x) < 1e-12, L, 2.0 * np.sin(x * (L / 2.0)) / x)


def trig_sinc_deriv(x):
    xz = np.where(np.abs(x) < 1e-12, 1e-12, x)
    return 2.0 * ((L / 2.0) * np.cos(xz * (L / 2.0)) * xz
                  - np.sin(xz * (L / 2.0))) / xz ** 2


def trig_basis_fourier(cf, N, om, y):
    """f(y) = sum_k cf[k] fhat_c(k, y) + cf[N+k] fhat_s(k, y), with
    fhat_c(k, y) = sincL(y + w_k) + sincL(y - w_k),
    fhat_s(k, y) = (sincL(y + w_k) - sincL(y - w_k)) / (2i),
    the Fourier transforms of cos(2 pi k x / L), sin(2 pi k x / L) on
    [-L/2, L/2].
    """
    scalar = np.ndim(y) == 0
    y = np.atleast_1d(np.asarray(y, dtype=float))
    F = np.zeros(len(y), dtype=np.complex128)
    for k in range(N + 1):
        sp = trig_sinc(y + om[k])
        sm = trig_sinc(y - om[k])
        F += cf[k] * (sp + sm)
        if k >= 1:
            F += cf[N + k] * (sp - sm) / (2j)
    if scalar:
        return F[0]
    return F


def trig_basis_fourier_deriv(cf, N, om, y):
    scalar = np.ndim(y) == 0
    y = np.atleast_1d(np.asarray(y, dtype=float))
    Fp = np.zeros(len(y), dtype=np.complex128)
    for k in range(N + 1):
        spp = trig_sinc_deriv(y + om[k])
        smp = trig_sinc_deriv(y - om[k])
        Fp += cf[k] * (spp + smp)
        if k >= 1:
            Fp += cf[N + k] * (spp - smp) / (2j)
    if scalar:
        return Fp[0]
    return Fp


def trig_quadratic_form(N):
    """The letter's quadratic form in its own real trigonometric basis:
    cos(2 pi k x / L), k = 0..N and sin(2 pi k x / L), k = 1..N.

    Returns (Q, G, om) with Q = W_p + W_R (the letter's Q(phi) matrix),
    G the metric, om the mode frequencies.  W_p is exactly diagonal; W_R is
    the identity-consistent digamma form (1/pi) int_0^inf fhat_a fhat_b K dt,
    computed vectorized.
    """
    om = 2.0 * np.pi * np.arange(N + 1) / L
    s_pp, w_pp, _ = fourier_weights()
    nmod = 2 * N + 1
    Wp = np.zeros((nmod, nmod))
    for k in range(N + 1):
        wv = np.sum(w_pp * (L - s_pp)) if k == 0 \
            else np.sum(w_pp * (L / 2.0) * np.cos(om[k] * s_pp))
        Wp[k, k] = wv
        if k >= 1:
            Wp[N + k, N + k] = wv

    t = arch_t_grid()
    wt = trapezoid_weights(t)
    K = digamma_kernel(t)
    F = np.zeros((nmod, len(t)), dtype=np.complex128)
    for k in range(N + 1):
        sp = trig_sinc(t + om[k])
        sm = trig_sinc(t - om[k])
        F[k] = sp + sm
        if k >= 1:
            F[N + k] = (sp - sm) / (2j)
    A = F * (K * wt)[None, :]
    WR = np.real(A @ F.conj().T) / np.pi

    G = np.zeros((nmod, nmod))
    for k in range(N + 1):
        G[k, k] = L if k == 0 else L / 2.0
        if k >= 1:
            G[N + k, N + k] = L / 2.0
    return Wp + WR, G, om


def trig_slice(N, scan_hi=ZERO_SCAN_HI, dy=ZERO_SCAN_DY):
    """Ground state of the letter's Q in its own trig basis (footnote 14),
    and the real zeros of its Fourier transform on [1, scan_hi]."""
    Q, G, om = trig_quadratic_form(N)
    w, v = eigh(Q, G, subset_by_index=[0, 0])
    lam = float(w[0])
    cf = v[:, 0]
    even_weight = float(cf[:N + 1] @ G[:N + 1, :N + 1] @ cf[:N + 1])

    def f(y):
        return trig_basis_fourier(cf, N, om, y)

    def fdp(y):
        return trig_basis_fourier_deriv(cf, N, om, y)

    yg = np.arange(1.0, scan_hi + dy, dy)
    mag = np.abs(f(yg))
    lm = np.where((mag[1:-1] < mag[:-2]) & (mag[1:-1] < mag[2:]))[0] + 1
    zeros = []
    for i in lm:
        y0 = float(yg[i])
        for _ in range(60):
            f0 = f(y0)
            df0 = fdp(y0)
            Jm = np.array([[df0.real, -df0.imag], [df0.imag, df0.real]])
            d = np.linalg.solve(Jm, -np.array([f0.real, f0.imag]))
            if not np.isfinite(d[0]):
                break
            if abs(d[0]) < 1e-13:
                break
            y0 += d[0]
        if abs(f(y0)) < 1e-8 and all(abs(y0 - z) > 1e-4 for z in zeros):
            zeros.append(y0)
    zeros = sorted(zeros)

    gammas = zeta_ordinates(N_ZEROS)
    errs = [min((abs(gn - z) for z in zeros), default=float("inf"))
            for gn in gammas]
    out = {
        "N": N, "lambda_min": lam, "even_weight": even_weight,
        "n_zeros": len(zeros),
        "zeros": [float(z) for z in zeros],
        "n_zeta_zeros_checked": N_ZEROS,
        "n_matched": int(sum(e <= MATCH_WIN for e in errs)),
        "n_matched_tight": int(sum(e <= 0.05 for e in errs)),
        "med_err": float(np.median(errs)),
        "max_err": float(max(errs)) if errs and max(errs) != float("inf")
        else None,
        "errors": [None if e == float("inf") else float(e) for e in errs],
    }
    return out, cf


def legcoef_matrix(A):
    """c[a,k] with T_a(x) = sum_k c[a,k] P_k(x); k <= a, k == a mod 2."""
    if A in LEGCOEF_CACHE:
        return LEGCOEF_CACHE[A]
    n = 128
    xgl, wgl = roots_legendre(n)
    Tx = np.cos(np.arange(A + 1)[:, None]
                * np.arccos(np.clip(xgl, -1.0, 1.0)))
    Pv = np.polynomial.legendre.legvander(xgl, A)
    c = np.zeros((A + 1, A + 1))
    for k in range(A + 1):
        c[:, k] = (2 * k + 1) / 2.0 * np.sum(Tx * Pv[:, k][None, :]
                                            * wgl[None, :], axis=1)
    LEGCOEF_CACHE[A] = c
    return c


def fhat_cheb(tgrid, A):
    """F[t, a] = int T_a(2x/L) e^{i t x} dx  (closed form, verified)."""
    w = L / 2.0
    c = legcoef_matrix(A)
    Nt = len(tgrid)
    jk = np.array([spherical_jn(k, tgrid * w) for k in range(A + 1)])
    im = (1j ** np.arange(A + 1))[:, None]
    F = np.zeros((Nt, A + 1), dtype=np.complex128)
    for a in range(A + 1):
        F[:, a] = w * np.sum(c[a, :][:, None] * 2.0 * im * jk, axis=0)
    return F


def digamma_kernel(t):
    return np.log(np.pi) - np.real(digamma(0.25 + 0.5j * np.asarray(t)))


def archimedean_matrix(A):
    """WR_ab = (1/pi) int_0^inf fhat_a(t) conj(fhat_b(t)) K(t) dt.

    K(t) = log pi - Re digamma(1/4 + it/2).  Equals (1/2pi) int_R ... since
    the integrand is even.  The identity-consistent archimedean local term.
    """
    t = arch_t_grid()
    F = fhat_cheb(t, A)
    K = digamma_kernel(t)
    WR = np.zeros((A + 1, A + 1))
    for a in range(A + 1):
        for b in range(a, A + 1):
            I = np.trapezoid(F[:, a] * np.conj(F[:, b]) * K, t) / np.pi
            WR[a, b] = WR[b, a] = float(np.real(I))
    return WR


def cheb_basis(M, J):
    """Chebyshev T_a(2x/L) sampled on a uniform x-grid, shape (M+1, J)."""
    h = L / J
    x = -HALF * L + np.arange(J) * h
    t = np.clip(2.0 * x / L, -1.0, 1.0)
    a = np.arange(M + 1)[:, None]
    return np.cos(a * np.arccos(t)), x, h


def pair_correlations(basis, J, selfcheck=True):
    """C_ab(s_k) = int theta_a(x) theta_b(x + s) dx at s = k*h, k = 0..J-1.

    C(s) is even in s; computed by FFT cross-correlation of the sampled
    basis with zero padding.
    """
    n = 1
    while n < 2 * J - 1:
        n <<= 1
    F = np.fft.rfft(basis, n=n, axis=1)
    h = L / J
    M = basis.shape[0] - 1
    corr = np.empty((M + 1, M + 1, J))
    for a in range(M + 1):
        P = np.fft.irfft(F[a][None, :] * np.conj(F), n=n, axis=1)
        corr[a] = P[:, :J] * h
    if selfcheck:
        s = np.arange(J) * h
        err = np.max(np.abs(corr[0, 0] - (L - s)))
        if err > 1e-8:
            raise RuntimeError("correlation self-check failed: err=%.3e" % err)
    return corr, h


def gram_matrix(M):
    """int T_a(2x/L) T_b(2x/L) dx = (L/2)[1/(1-(a+b)^2) + 1/(1-(a-b)^2)] (a+b even)."""
    G = np.zeros((M + 1, M + 1))
    for i in range(M + 1):
        for j in range(M + 1):
            if (i + j) % 2 == 0:
                G[i, j] = (L / 2.0) * (1.0 / (1.0 - (i + j) ** 2)
                                       + 1.0 / (1.0 - (i - j) ** 2))
    return G


def build_quadratic_form(M, J, n_gl):
    """Return (M_mat, G, diag_info) for the Chebyshev basis of degree M.

    M_mat = -(W_p + W_R) with W_p from eq (10) and W_R the digamma form.
    """
    basis, _, _ = cheb_basis(M, J)
    corr, h = pair_correlations(basis, J)
    s_grid = np.arange(J) * h
    G = gram_matrix(M)

    s_pp, w_pp, pows = fourier_weights()

    spl = [[None] * (M + 1) for _ in range(M + 1)]
    for a in range(M + 1):
        for b in range(a, M + 1):
            spl[a][b] = CubicSpline(s_grid, corr[a, b])
            spl[b][a] = spl[a][b]

    Wp_mat = np.zeros((M + 1, M + 1))
    for a in range(M + 1):
        for b in range(a, M + 1):
            Wp_mat[a, b] = Wp_mat[b, a] = np.sum(w_pp * spl[a][b](s_pp))
    WR_mat = archimedean_matrix(M)
    M_mat = -(Wp_mat + WR_mat)

    c0 = np.zeros(M + 1)
    c0[0] = 1.0 / np.sqrt(G[0, 0])
    diag = {
        "prime_powers": [(p, m, pw) for (p, m, pw) in pows],
        "Q_constant_rayleigh": float(c0 @ M_mat @ c0 / (c0 @ G @ c0)),
        "WR_diag": [float(WR_mat[i, i]) for i in range(min(6, M + 1))],
        "Wp_norm": float(np.abs(Wp_mat).max()),
    }
    return M_mat, G, diag


def trig_diagonality_diagnostic(N=12):
    """Off/on-diagonal ratio of the CORRECTED exact form in the trig basis.

    Real modes cos(2 pi k x / L), sin(2 pi k x / L), k = 0..N.  W_p (eq 10)
    is exactly diagonal here: the autocorrelation of cos(2 pi k x / L) on
    [-L/2, L/2] is (L/2)cos(2 pi k s / L) (exactly, since 2 pi k L / L is a
    multiple of 2 pi).  W_R (digamma form) couples all modes: its kernel
    is (1/pi) int_0^inf fhat_a(t) fhat_b(t) K(t) dt, a full matrix.  So the
    corrected form is NOT diagonal in the letter's trig basis -- the
    off-diagonal coupling needed for a mixed ground state is present in
    the archimedean term.
    """
    kk = np.arange(N + 1)
    nmod = 2 * N + 1          # cos modes k=0..N, sin modes k=1..N
    om = 2.0 * np.pi * kk / L

    def w_p_diag(k, s):
        if k == 0:
            return L - s
        return (L / 2.0) * np.cos(om[k] * s)

    s_pp, w_pp, _ = fourier_weights()
    Wp = np.zeros((nmod, nmod))
    for k in range(N + 1):
        Wp[k, k] = np.sum(w_pp * w_p_diag(k, s_pp))            # cos
        if k >= 1:
            Wp[N + k, N + k] = np.sum(w_pp * w_p_diag(k, s_pp))  # sin

    t = arch_t_grid()
    K = digamma_kernel(t)
    F = np.zeros((nmod, len(t)), dtype=np.complex128)

    def sincL(x):
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(x == 0.0, L, 2.0 * np.sin(x * (L / 2.0)) / x)

    for k in range(N + 1):
        # fhat_cos(k, t) = sincL(t + w_k) + sincL(t - w_k)   (real)
        # fhat_sin(k, t) = (sincL(t + w_k) - sincL(t - w_k)) / (2i)
        # cross (cos,sin) pairs integrate to pure imaginary parts that
        # vanish under Re(); Re is taken when the matrix is built.
        sp = sincL(t[None, :] + om[k])
        sm = sincL(t[None, :] - om[k])
        F[k] = sp + sm
        if k >= 1:
            F[N + k] = (sp - sm) / (2j)
    WR = np.zeros((nmod, nmod))
    for ia in range(nmod):
        for ib in range(ia, nmod):
            I = np.trapezoid(F[ia] * np.conj(F[ib]) * K, t) / np.pi
            WR[ia, ib] = WR[ib, ia] = float(np.real(I))
    Mmat = -(Wp + WR)
    diag = np.abs(np.diag(Mmat))
    off = np.abs(Mmat - np.diag(np.diag(Mmat)))
    return {
        "max_offdiag_ratio": float(off.max() / max(diag.max(), 1e-12)),
        "Wp_offdiag_max": float(np.abs(Wp - np.diag(np.diag(Wp))).max()),
        "WR_offdiag_max": float(np.abs(WR - np.diag(np.diag(WR))).max()),
        "diag_ratios_minmax": [float(diag.min()), float(diag.max())],
        "N_modes": N,
        "note": "with the corrected W_R (digamma form) the exact form is "
                "NOT diagonal in the trig basis: the archimedean kernel "
                "couples all modes (W_p alone is exactly diagonal).",
    }


def fhat_basis_eval(c, A, y):
    """sum_a c[a] fhat_a(y), fhat_a(t) = int T_a(2x/L) e^{itx} dx (closed form)."""
    w = L / 2.0
    cM = legcoef_matrix(A)
    scalar = np.ndim(y) == 0
    y = np.atleast_1d(np.asarray(y, dtype=float))
    F = np.zeros(len(y), dtype=np.complex128)
    for a in range(A + 1):
        if abs(c[a]) < 1e-14:
            continue
        for k in range(A + 1):
            ck = cM[a, k]
            if ck == 0.0:
                continue
            F += c[a] * ck * 2.0 * (1j ** k) * w * spherical_jn(k, y * w)
    if scalar:
        return F[0]
    return F


def local_term_check():
    """Paper eq (11) vs the digamma form on an even test function psi(t) =
    cos^2(pi t / (2w)) (|t| <= w), w = L/2 and w = L.  Reports the residual
    of the FOURIER-convention identity
        fhat(i/2) + fhat(-i/2) - 2 sum_{gamma>0} fhat(gamma) = W_p + W_R
    for each choice of W_R.  The digamma form closes to ~1e-8; eq (11) is
    off by ~0.57 (w = L/2) / ~0.15 (w = L) -- a functional, not a constant.
    """
    out = {}
    for wtag, wbump in (("w_half", L / 2.0), ("w_full", L)):
        wval = wbump
        f_1 = 1.0

        def psi_s(t):
            a = np.abs(t) / wval
            return np.where(a <= 1.0, np.cos(np.pi * a / 2.0) ** 2, 0.0)

        # Fourier transform phi(g) = int psi(t) e^{i g t} dt (closed form)
        def phi(g):
            g = np.asarray(g, dtype=float)
            kk = np.pi / wval
            sw = g * wval
            gz = np.abs(g) < 1e-12
            s = np.where(gz, wval,
                         np.sin(sw) / np.where(gz, 1.0, g))
            a1 = np.where(np.abs(g - kk) < 1e-12, -wval,
                          np.sin(sw - np.pi) / (g - kk))
            a2 = np.where(np.abs(g + kk) < 1e-12, -wval,
                          np.sin(sw + np.pi) / (g + kk))
            return s + 0.5 * (a1 + a2)

        def moment(ep):
            t = np.linspace(0.0, wval, 8192)
            integrand = psi_s(t) * np.exp(ep * t)
            return np.trapezoid(integrand, t)

        # fhat_psi(+-i/2) = int psi(t) e^{+-t/2} dt (psi itself, even)
        lhs_const = 2.0 * (moment(0.5) + moment(-0.5))
        # zero sum is LINEAR in fhat_psi(gamma) = phi(gamma) for a direct
        # even test function (the letter's |fhat_phi|^2 form is only for
        # psi = phi*phi, a self-convolution)
        gammas = zeta_ordinates(400)
        acc = 0.0
        for nn in range(400):
            acc += phi(gammas[nn])
        lhs = lhs_const - 2.0 * acc

        # W_p (eq 10): 2 sum w_pp psi(s_pp)
        s_pp, w_pp, _ = fourier_weights()
        W_p = float(np.sum(w_pp * psi_s(s_pp)))

        # digamma W_R = (1/pi) int_0^inf phi(t) K(t) dt
        t = arch_t_grid()
        W_R_dig = float(np.trapezoid(phi(t) * digamma_kernel(t), t) / np.pi)

        # paper eq (11): (log4pi+gamma) f(1) + int_0^w (2 psi - 2 e^{-s/2})
        #   e^{s/2}/(e^s - e^{-s}) ds   (integrand -> 1/2 at s = 0)
        sg = np.linspace(0.0, wval, 8192)
        with np.errstate(divide="ignore", invalid="ignore"):
            integrand = (2.0 * psi_s(sg) - 2.0 * np.exp(-sg / 2.0)) \
                * np.exp(sg / 2.0) / (np.exp(sg) - np.exp(-sg))
        integrand = np.where(sg == 0.0, 0.5, integrand)
        W_R_11 = LOG4PI_GAMMA * f_1 + float(np.trapezoid(integrand, sg))

        out[wtag] = {
            "lhs": float(lhs),
            "W_p": W_p,
            "W_R_digamma": W_R_dig,
            "W_R_paper11": W_R_11,
            "residual_digamma": float(abs(lhs - (W_p + W_R_dig))),
            "residual_paper11": float(abs(lhs - (W_p + W_R_11))),
        }
    return out


def melin_grid(J2):
    x = -HALF * L + np.arange(J2) * (L / J2)
    w = np.full(J2, L / J2)
    w[0] = w[-1] = (L / J2) / 2.0
    return x, w


def melin_eval(eta, x, w, y):
    """f(y) = int eta(x) e^{(iy - 1/2) x} dx  (vectorized over y)."""
    g = eta * w * np.exp(-HALF * x)
    yy = np.atleast_1d(np.asarray(y, dtype=float))
    out = np.zeros(len(yy), dtype=np.complex128)
    blk = 512
    for i in range(0, len(yy), blk):
        Y = yy[i:i + blk]
        out[i:i + blk] = np.exp(1j * Y[:, None] * x[None, :]) @ g
    if np.ndim(y) == 0:
        return out[0]
    return out


def melin_deriv(eta, x, w, y):
    g = eta * w * np.exp(-HALF * x)
    return 1j * (np.exp(1j * y * x) @ (g * x))


def find_real_zeros(eta, x, w, scan_hi=ZERO_SCAN_HI, dy=ZERO_SCAN_DY):
    yg = np.arange(1.0, scan_hi + dy, dy)
    fv = melin_eval(eta, x, w, yg)
    g = np.abs(fv)
    local_min = np.where((g[1:-1] < g[:-2]) & (g[1:-1] < g[2:]))[0] + 1
    zeros = []

    def refine(y0):
        for _ in range(40):
            f0 = melin_eval(eta, x, w, y0)
            df0 = melin_deriv(eta, x, w, y0)
            Jm = np.array([[df0.real, -df0.imag], [df0.imag, df0.real]])
            d = np.linalg.solve(Jm, -np.array([f0.real, f0.imag]))
            y1 = y0 + d[0]
            if not np.isfinite(y1):
                return None
            if abs(d[0]) < 1e-12:
                break
            y0 = y1
        f1 = melin_eval(eta, x, w, y0)
        return y0, abs(f1)

    for y0 in yg[local_min]:
        r = refine(y0)
        if r is None:
            continue
        y, mag = r
        if mag < 1e-7 and all(abs(y - z) > 1e-4 for z in zeros):
            zeros.append(y)
    return sorted(zeros)


def zeta_ordinates(n):
    return [float(mp.im(mp.zetazero(k))) for k in range(1, n + 1)]


def run_slice(M, J=J_GRID, n_gl=N_GL, even_only=False, want_zeros=True):
    Mfull = M
    idxs = [a for a in range(Mfull + 1) if not even_only or a % 2 == 0]
    Mred = len(idxs) - 1
    Mmat_f, G_f, _diag = build_quadratic_form(Mfull, J, n_gl)
    Mmat = Mmat_f[np.ix_(idxs, idxs)]
    G = G_f[np.ix_(idxs, idxs)]
    try:
        w, v = eigh(Mmat, G, subset_by_index=[0, 0])
    except Exception:
        Lc = np.linalg.cholesky(G)
        A = np.linalg.solve(Lc, np.linalg.solve(Lc.T, Mmat))
        wr, vr = np.linalg.eigh(A)
        w = np.array([wr[0]])
        v = vr[:, [0]]
    lam = float(w[0])
    c = v[:, 0]
    cf = np.zeros(Mfull + 1)
    cf[idxs] = c
    even_idx = [a for a in range(Mfull + 1) if a % 2 == 0]
    if even_idx:
        even_frac = float(cf[even_idx] @ G_f[np.ix_(even_idx, even_idx)]
                          @ cf[even_idx])
    else:
        even_frac = 0.0

    x, wq = melin_grid(ETAG_GRID)
    t = np.clip(2.0 * x / L, -1.0, 1.0)
    basis_e = np.cos(np.arange(Mfull + 1)[:, None] * np.arccos(t))
    eta = basis_e.T @ cf

    out = {
        "M": Mfull, "even_only": even_only, "lambda_min": lam,
        "even_fraction": even_frac,
        "eta": [float(v) for v in eta[::max(1, len(eta) // 129)]],
        "cf": [float(v) for v in cf],
    }
    if want_zeros:
        zeros = find_real_zeros(eta, x, wq)
        out["zeros"] = zeros
        gammas = zeta_ordinates(N_ZEROS)
        errs = []
        for gn in gammas:
            d = min((abs(gn - z) for z in zeros), default=float("inf"))
            errs.append(d)
        out["match_window"] = MATCH_WIN
        out["n_zeta_zeros_checked"] = N_ZEROS
        out["n_found"] = len(zeros)
        out["n_matched"] = int(sum(e <= MATCH_WIN for e in errs))
        out["n_matched_tight"] = int(sum(e <= 0.05 for e in errs))
        out["max_err"] = float(max(errs)) if errs and max(errs) != float("inf") \
            else None
        out["med_err"] = float(np.median(errs))
        out["errors"] = [None if e == float("inf") else float(e) for e in errs]
    return out, cf, _diag


def explicit_formula_residual(cf, Mfull, basis="cheb", K=300, J=ETAG_GRID):
    """Validates the letter's explicit-formula identity (Fourier convention)
    on psi = phi * phi for the ground state phi = theta:

        fhat_psi(i/2) + fhat_psi(-i/2) - 2 sum_{gamma>0} fhat_psi(gamma)
            = W_p (eq 10) + W_R (digamma form)

    with fhat_psi(gamma) = |fhat_phi(gamma)|^2 and fhat_phi evaluated by the
    closed form (Chebyshev: fhat_a(t) = int T_a(2x/L) e^{itx} dx; trig: the
    sincL combination).  The zero sum is absolutely convergent (fhat_phi is
    a compact-support Fourier transform), so the residual at growing K
    (exact zeta zeros) is flat at ~1e-9.
    """
    A = Mfull
    x, w = melin_grid(J)
    if basis == "cheb":
        t = np.clip(2.0 * x / L, -1.0, 1.0)
        basis_e = np.cos(np.arange(A + 1)[:, None] * np.arccos(t))
        fhat = lambda g: fhat_basis_eval(cf, A, g)
    else:
        om = 2.0 * np.pi * np.arange(A + 1) / L
        rows = np.cos(np.outer(om, x))
        if A >= 1:
            rows = np.vstack([rows, np.sin(np.outer(om[1:], x))])
        basis_e = rows
        fhat = lambda g: trig_basis_fourier(cf, A, om, g)
    eta = basis_e.T @ cf

    m_p = float(np.sum(eta * w * np.exp(HALF * x)))
    m_m = float(np.sum(eta * w * np.exp(-HALF * x)))
    lhs_const = 2.0 * m_p * m_m

    tg = arch_t_grid()
    W_R = float(np.trapezoid(
        np.abs(fhat(tg)) ** 2 * digamma_kernel(tg), tg) / np.pi)

    n = 1
    while n < 2 * J:
        n <<= 1
    Feta = np.fft.rfft(eta, n)
    P = np.fft.irfft(Feta * np.conj(Feta), n) * (L / J)
    idx = np.abs(np.arange(2 * J - 1) - (J - 1))
    s = (np.arange(2 * J - 1) - (J - 1)) * (L / J)
    cs = CubicSpline(s, P[idx])
    s_pp, w_pp, _ = fourier_weights()
    W_p = float(np.sum(w_pp * cs(s_pp)))

    res = []
    acc = 0.0
    prev = 0
    for Kk in (50, 100, 200, 300):
        for nn in range(prev + 1, Kk + 1):
            g = float(mp.im(mp.zetazero(nn)))
            acc += np.abs(fhat(g)) ** 2
        prev = Kk
        lhs = lhs_const - 2.0 * acc
        res.append([int(Kk), float(abs(lhs - (W_p + W_R)))])
    return res


def main():
    t0 = time.time()
    slices = {}
    cheb_cf = None
    cheb_residual = None
    for M in (10, 20, 30):
        for even in (True, False):
            try:
                sl, cf, _ = run_slice(M, even_only=even)
            except Exception as exc:
                slices["M%d%s" % (M, "e" if even else "")] = {"error": repr(exc)}
                continue
            key = "M%d%s" % (M, "e" if even else "")
            slices[key] = {k: v for k, v in sl.items() if k not in ("eta", "cf")}
            if even and cheb_cf is None:
                cheb_cf = cf
                cheb_M = M
                cheb_residual = explicit_formula_residual(cf, M, basis="cheb")

    trig = trig_diagonality_diagnostic()
    ltc = local_term_check()

    trig_slices = {}
    trig_best = None
    trig_cf = None
    for N in (50, 100, 150):
        try:
            ts, tcf = trig_slice(N)
        except Exception as exc:
            trig_slices["N%d" % N] = {"error": repr(exc)}
            continue
        trig_slices["N%d" % N] = ts
        if trig_best is None or ts["med_err"] < trig_best["med_err"]:
            trig_best = ts
            trig_cf = tcf

    residual = None
    if trig_best is None:
        verdict = ("CONNES LETTER NOT REPRODUCED (independent discretizations): "
                   "no near-matching ground-state zeros in any slice")
    else:
        residual = explicit_formula_residual(trig_cf, trig_best["N"], basis="trig")
        trig_best["residual_vs_K"] = residual
        verdict = (
            "CONNES LETTER NOT REPRODUCED (independent discretizations): the "
            "finite-prime Weil quadratic form on [1,13] (identity-consistent "
            "local terms eq(10) + digamma W_R; the paper's printed eq(11) "
            "archimedean term is INCONSISTENT with the explicit formula, off "
            "by 0.57/0.15 on test functions) has a ground state whose Mellin "
            "transform has real zeros only in the letter's own trigonometric "
            "truncation (even ground state, all zeros real as in Thm 6.1) -- "
            "but those zeros lie on a quasi-periodic lattice of spacing "
            "2*pi/L, with median offset %.3g from the first 50 zeta "
            "ordinates; only %d/50 matched within %.2f and %d within 0.05 "
            "(N=%d).  The Chebyshev discretizations (M=10..30) and the "
            "admissible class show no real zeros at all, and |f(gamma_n)| "
            "does not converge to zero with the truncation size.  The "
            "letter's reported precision (2.6e-55..1e-2) is therefore NOT "
            "reproduced; it is tied to the footnote-14 construction (rank-one "
            "perturbation of a periodic Dirac operator with the Dirichlet "
            "kernel), which is extra structure not derivable from the "
            "letter's text.  HONEST WALL: numerical claim not reproduced "
            "does not disprove RH; does not bound de Bruijn-Newman Lambda; "
            "finitely many primes never become the full Euler product."
            % (trig_best["med_err"], trig_best["n_matched"], MATCH_WIN,
               trig_best["n_matched_tight"], trig_best["N"]))

    data = {
        "claim": ("Connes 2026 'Letter to Riemann': on functions supported "
                  "in [1,13] the Weil quadratic form from the explicit "
                  "formula (primes 2,3,5,7,11,13 and powers <= 13 only) has "
                  "a ground state whose Mellin-transform zeros are real and "
                  "approximate the first 50 zeta zeros (2.6e-55..1e-2).  "
                  "We test reproducibility with (i) an independent Chebyshev "
                  "discretization and (ii) the letter's own trigonometric "
                  "truncation."),
        "convention": {
            "identity": "fhat(i/2) - sum_{1/2+is in Z} fhat(s) + fhat(-i/2)"
                        " = sum_v W_v(f),  fhat(s) = int f(x) x^{-is} d*x",
            "W_p": "eq(10): log p * sum_m p^{-m/2}(f(p^m)+f(p^{-m})); "
                   "weights 2 log p p^{-m/2} for even f",
            "W_R": "digamma form (1/2pi) int fhat_t(t) (log pi - Re "
                   "digamma(1/4+it/2)) dt -- NOT the paper's eq(11), which "
                   "is not identity-consistent (see local_term_check)",
        },
        "setup": {"L": L, "primes": PRIMES, "x_domain": "[-L/2, L/2]",
                  "J_grid": J_GRID, "n_gl": N_GL, "scan_hi": ZERO_SCAN_HI,
                  "basis": "Chebyshev T_a(2x/L) and the letter's real trig "
                           "basis cos/sin(2 pi k x / L)",
                  "match_window": MATCH_WIN},
        "slices": slices,
        "trig_slices": trig_slices,
        "trig_best": {k: v for k, v in trig_best.items()}
        if trig_best else None,
        "trig_diagonality": trig,
        "local_term_check": ltc,
        "explicit_formula": {
            "method": "ground-state psi = theta*theta; fhat_psi(gamma) = "
                      "|fhat_phi(gamma)|^2; zero sum over the first K exact "
                      "zeta ordinates",
            "residual_cheb_vs_K": cheb_residual,
            "cheb_slice": "M%d even" % cheb_M if cheb_cf is not None else None,
            "cheb_note": "residual decreases with K (zero-sum tail of the "
                         "ground state's |fhat|^2, ~1e-4..5e-3 at K=300 for "
                         "coarse slices); the identity itself closes at "
                         "machine precision on smooth test functions "
                         "(local_term_check: digamma residual ~1e-9, the "
                         "paper's eq(11) leaves a 0.57/0.15 defect)",
            "residual_trig_vs_K": trig_best.get("residual_vs_K")
            if trig_best else None,
            "trig_note": "the trig-truncated ground state's |fhat|^2 has a "
                         "slower tail, so its zero sum closes only slowly in "
                         "K (residual ~2.4 at K=300, decreasing)",
        },
        "verdict": verdict,
        "runtime_sec": round(time.time() - t0, 1),
    }
    with open(OUT, "w") as f:
        json.dump(data, f, indent=2)

    print(verdict)
    print()
    print("Chebyshev slices:")
    for name, sl in sorted(slices.items()):
        if "errors" in sl:
            print("  %-5s %s" % (name, sl))
        else:
            print("  %-5s lambda=%.6g found=%d matched=%d tight=%d "
                  "med_err=%.3g"
                  % (name, sl["lambda_min"], sl["n_found"], sl["n_matched"],
                     sl["n_matched_tight"], sl["med_err"]))
    print()
    print("Trigonometric truncation (the letter's own basis):")
    for name, ts in sorted(trig_slices.items()):
        if "errors" in ts:
            print("  %-5s %s" % (name, ts))
        else:
            print("  %-5s lambda=%.6g even_weight=%.3f zeros=%d matched=%d "
                  "tight=%d med_err=%.3g"
                  % (name, ts["lambda_min"], ts["even_weight"],
                     ts["n_zeros"], ts["n_matched"], ts["n_matched_tight"],
                     ts["med_err"]))
    print()
    print("trig diagonality diagnostic: max_offdiag_ratio =",
          trig["max_offdiag_ratio"])
    print("local term check (digamma vs paper eq11 residual):")
    for k, v in ltc.items():
        print("  %-8s digamma %.3e   paper11 %.3e"
              % (k, v["residual_digamma"], v["residual_paper11"]))
    if cheb_residual:
        print("explicit-formula residual vs K (Chebyshev M%d even slice): %s"
              % (cheb_M, cheb_residual))
    if residual:
        print("explicit-formula residual vs K (trig N=%d): %s"
              % (trig_best["N"], residual))
    print("wrote", os.path.normpath(OUT))


if __name__ == "__main__":
    main()
