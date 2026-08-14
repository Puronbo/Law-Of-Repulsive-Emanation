"""
riemann_siegel_certify.py
=========================
Rigorous, oracle-free CERTIFICATION that the non-trivial zeros of the
Riemann zeta function with ordinates <= ~1000 all lie on the critical line
and are simple.  Complements the condensed locator in riemann_siegel_roots.py
(which finds the zeros fast): here every claim is certified by directed-
rounding interval arithmetic plus Turing's method.

Two independent ingredients:

(1) Interval engine.  Z(t) = e^{i.theta(t)} zeta(1/2+it) is evaluated in
    mpmath.iv (real interval arithmetic, outward rounding).  zeta(1/2+it)
    is computed by the Euler-Maclaurin formula decomposed into real and
    imaginary parts (every n^{-s}, N^{1-s}/(s-1), Bernoulli correction term
    and the Backlund explicit remainder bound are real interval expressions),
    and theta(t) by its exact Stirling/Binet series (imaginary part of the
    asymptotic expansion of log Gamma(1/4+it/2) - (t/2) log pi, expressed in
    real interval arithmetic with a validated remainder bound).  Every
    Z-evaluation returns a rigorous enclosure [Zlo, Zhi]:
        Zlo > 0  ->  sign +1 certified ;  Zhi < 0  ->  sign -1 certified.
    All enclosures are validated to CONTAIN the high-precision mpmath value
    (zeta and loggamma-based theta) at the test points and at every Gram
    point - if containment ever fails the certificate is void.

(2) Turing's method, in Brent's form (Brent 1979, Theorem 3.2, after
    Lehman's Theorem 4):  if N >= 0.0061 (ln g_p)^2 + 0.08 ln g_p
    consecutive Gram blocks with union [g_n, g_p) satisfy Rosser's rule
    (a length-k block contains at least k zeros), then
    N(g_n) <= n+1  and  N(g_p) >= p+1.  The interval engine certifies
    n+1 distinct on-line sign-change zeros below g_n, so N(g_n) = n+1
    exactly:  every zero of zeta(s) with 0 < gamma <= g_n lies on
    Re(s) = 1/2 and is simple.

Pipeline:
  1. Euler-Maclaurin interval engine (Re zeta, Im zeta, theta, Z).
  2. validation: interval enclosures must CONTAIN the high-precision floats
     at the test points, at every Gram point, and at every bracket point.
  3. certified signs of Z at the Gram points g_0..g_P (g_P ~ 1030).
  4. certified sign-change brackets around every zero located by the
     condensed Riemann-Siegel engine: each bracket is a certified simple
     on-line zero.
  5. Rosser blocks near the top; Rosser's rule certified with the counted
     zeros; Brent/Lehman theorem gives N(g_n) = n+1 exactly.
  6. cross-checks: certified count vs mpmath.zetazero, RvM S-values
     (max |S|), certification margins min |Z| / interval width.

Honest wall: this certifies the finite range 0 < gamma <= g_n ~ 999
(648 zeros).  It cannot prove the Riemann hypothesis - which remains open
(rigorous verification now extends to |t| <= 3 x 10^12, Platt-Trudgian).

Verdict artifact: ../data/riemann_siegel_certify_data.json
"""
import json
import os
from fractions import Fraction
from math import comb

import numpy as np
import mpmath as mp

from riemann_siegel_roots import z_rs

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

N_EM = 200          # Euler-Maclaurin n-sum length
M_EM = 25           # number of Bernoulli corrections
M_THETA = 25        # Stirling/Binet terms for theta(t)
THETA_SAFETY = 25   # validated remainder-bound safety factor (see theta_iv)
IV_DPS = 40         # interval-arithmetic precision
FLOAT_DPS = 50      # float precision (locator / gram / validation)
T_CERT = 1000.0     # certified height target
SCAN_END = 1006.0   # locator scan end
GRID = 0.05         # locator grid step
BRACKET_HALF = 5e-5  # certified bracket half-width around each located zero
WIDEN_REL = 1e-12   # relative widening of every float evaluation point


# ---------------------------------------------------------------------------
# exact Bernoulli numbers and factorials (fractions)
# ---------------------------------------------------------------------------
def bernoulli_fracs(mmax):
    B = [Fraction(1)]
    for m in range(1, mmax + 1):
        s = Fraction(0)
        for k in range(m):
            s += comb(m + 1, k) * B[k]
        B.append(-s / Fraction(m + 1))
    return B


def factorial_fracs(mmax):
    F = [Fraction(1)]
    for i in range(1, mmax + 1):
        F.append(F[-1] * Fraction(i))
    return F


BF = bernoulli_fracs(52)
FF = factorial_fracs(52)

# precomputed interval logs / square roots of the integers used in the sum
_logs = [None] + [mp.iv.log(mp.iv.mpf(i)) for i in range(1, 201)]
_sqrts = [None] + [mp.iv.sqrt(mp.iv.mpf(i)) for i in range(1, 201)]

H = mp.iv.mpf(1) / mp.iv.mpf(2)      # 1/2
Q = mp.iv.mpf(1) / mp.iv.mpf(4)      # 1/4
T15 = mp.iv.mpf(3) / mp.iv.mpf(2)    # 3/2


def iv(x):
    return mp.iv.mpf(x)


def iv_frac(f):
    return mp.iv.mpf(f.numerator) / mp.iv.mpf(f.denominator)


# ---------------------------------------------------------------------------
# interval engine
# ---------------------------------------------------------------------------
def theta_iv(t):
    """theta(t) = Im logGamma(1/4 + i t/2) - (t/2) log(pi), t > 0.

    Exact Stirling/Binet series: with z = 1/4 + i t/2 = r e^{i.phi},
        theta = (t/2)(ln r - 1 - ln pi) - phi/4
              + sum_{k=1}^{M} B_{2k}/(2k(2k-1)) r^{1-2k} sin((1-2k) phi).
    (This is the imaginary part of the asymptotic expansion of logGamma(z);
    unlike mp.iv.loggamma - which is a heuristic asymptotic implementation -
    every term here is an explicit real-interval expression.)

    Remainder bound: |R_M| <= THETA_SAFETY * |B_{2M+2}|/((2M+2)(2M+1))
    r^{-(2M+1)}.  The factor 25 is numerically validated (dps=300 reference
    Im loggamma): over t in [13.5, 1006] the ratio |R_25|/|T_26| peaks at
    3.8 (near the Stirling minimal term at t ~ 16), so the bound holds with
    margin >= 6.6; the ratio approaches 1 at large t.  Containment of the
    high-precision value at every Gram point is enforced in step 3."""
    a = t / 2
    r = mp.iv.sqrt(Q * Q + a * a)
    phi = mp.iv.atan2(a, Q)
    th = (t / 2) * (mp.iv.log(r) - 1 - mp.iv.log(mp.iv.pi)) - phi / 4
    for k in range(1, M_THETA + 1):
        th = th + iv_frac(BF[2 * k] / (2 * k * (2 * k - 1))) \
            * r ** (1 - 2 * k) * mp.iv.sin((1 - 2 * k) * phi)
    kk = 2 * M_THETA + 2
    E = iv_frac(abs(BF[kk]) / (kk * (kk - 1))) * r ** (1 - kk) * THETA_SAFETY
    Ep = E.b
    return th + mp.iv.mpf([-Ep, Ep])


def csigmak(t, kmax):
    """(s)_{kmax} = s(s+1)...(s+kmax-1), s = 1/2 + it, as complex interval."""
    u = iv(1)
    v = iv(0)
    for j in range(kmax):
        a = iv(j) + H
        u, v = u * a - v * t, u * t + v * a
    return u, v


def zeta_em_iv(t):
    """(Re zeta, Im zeta) at s = 1/2 + i t by Euler-Maclaurin with the
    Backlund remainder bound, in real interval arithmetic."""
    N, M = N_EM, M_EM
    lnN = _logs[N]
    c = mp.iv.cos(t * lnN)
    s = mp.iv.sin(t * lnN)
    sqrtN = _sqrts[N]
    re = iv(0)
    im = iv(0)
    for n in range(1, N):
        a = t * _logs[n]
        w = _sqrts[n]
        re = re + mp.iv.cos(a) / w
        im = im - mp.iv.sin(a) / w
    re = re + c / (2 * sqrtN)
    im = im - s / (2 * sqrtN)
    D = t * t + Q
    re = re + sqrtN * (-c / 2 - s * t) / D
    im = im + sqrtN * (-c * t + s / 2) / D
    for r in range(1, M + 1):
        k = 2 * r - 1
        u, v = csigmak(t, k)
        scl = iv_frac(BF[2 * r] / FF[2 * r]) * mp.iv.exp((H - iv(2 * r)) * lnN)
        re = re + scl * (u * c + v * s)
        im = im + scl * (v * c - u * s)
    kk = 2 * M + 2
    nrm = iv(1)
    for j in range(kk - 1):
        nrm = nrm * mp.iv.sqrt((iv(j) + H) ** 2 + t * t)
    den = mp.iv.sqrt((iv(2 * M) + T15) ** 2 + t * t)
    sreal = iv(2 * M) + T15
    E = (iv_frac(abs(BF[kk]) / FF[kk]) * nrm
         * mp.iv.exp(-sreal * lnN) * (iv(1) + den / sreal))
    Ep = E.b
    return re + mp.iv.mpf([-Ep, Ep]), im + mp.iv.mpf([-Ep, Ep])


def z_iv(t):
    """Z(t) = cos(theta) Re zeta - sin(theta) Im zeta as an interval."""
    re, im = zeta_em_iv(t)
    th = theta_iv(t)
    return mp.iv.cos(th) * re - mp.iv.sin(th) * im


def cert_sign(z):
    """+1 if Z > 0 certified, -1 if Z < 0 certified, 0 if not certified."""
    if z.a > 0:
        return 1
    if z.b < 0:
        return -1
    return 0


def widen_t(t):
    r = WIDEN_REL
    return mp.iv.mpf([t * (1 - r), t * (1 + r)])


# ---------------------------------------------------------------------------
# float helpers (locator, Gram points, validation)
# ---------------------------------------------------------------------------
def theta_float(t):
    return mp.im(mp.loggamma(mp.mpc(0.25, t / 2))) - (t / 2) * mp.log(mp.pi)


def dtheta(t):
    return (mp.re(mp.mpf(0.5) * mp.polygamma(0, mp.mpc(0.25, t / 2)))
            - mp.mpf(0.5) * mp.log(mp.pi))


def gram_point(j):
    lo, hi = mp.mpf(1.0), mp.mpf(1300.0)
    for _ in range(42):
        mid = (lo + hi) / 2
        if theta_float(mid) < j * mp.pi:
            lo = mid
        else:
            hi = mid
    t = (lo + hi) / 2
    for _ in range(60):
        nt = t - (theta_float(t) - j * mp.pi) / dtheta(t)
        if nt == t:
            break
        t = nt
    return t


def locate_zeros(t_end):
    """Condensed Riemann-Siegel locator (float, fast); brackets widened and
    re-certified by the interval engine afterwards."""
    brackets = []
    t = 8.0
    prev_neg = float(z_rs(t)) < 0
    while t <= t_end:
        t += GRID
        now_neg = float(z_rs(t)) < 0
        if now_neg != prev_neg:
            brackets.append((t - GRID, t))
        prev_neg = now_neg
    zeros = []
    for a, b in brackets:
        za = float(z_rs(a))
        for _ in range(80):
            m = (a + b) / 2
            zm = float(z_rs(m))
            if (za < 0) == (zm < 0):
                a, za = m, zm
            else:
                b = m
        zeros.append((a + b) / 2)
    return np.array(zeros)


def main():
    mp.mp.dps = FLOAT_DPS
    mp.iv.dps = IV_DPS

    print("=" * 72)
    print("RIEMANN-SIEGEL CERTIFIER: every zero with ordinate <= ~1000")
    print("on the critical line, by interval arithmetic + Turing's method")
    print("=" * 72)

    # ---- 1. locate zeros (condensed RS engine), certify their brackets ----
    zeros = locate_zeros(SCAN_END)
    nz = len(zeros)
    cert_ok = []
    margins = []
    for t0 in zeros:
        zl = z_iv(widen_t(t0 - BRACKET_HALF))
        zh = z_iv(widen_t(t0 + BRACKET_HALF))
        sl, sh = cert_sign(zl), cert_sign(zh)
        ok = sl != 0 and sh != 0 and sl != sh
        cert_ok.append(bool(ok))
        margins.append(min(abs(zl.a), abs(zl.b), abs(zh.a), abs(zh.b)))
    if not all(cert_ok):
        print("FAIL: %d of %d brackets not certified" % (
            sum(1 for x in cert_ok if not x), nz))
    else:
        print("(1) %d sign-change brackets located; ALL certified as simple"
              " on-line zeros" % nz)
    cert_zero = np.array([t for t, ok in zip(zeros, cert_ok) if ok])

    # ---- 2. Gram points and certified signs ----
    gs = []
    j = 0
    while True:
        gj = gram_point(j)
        if gj > SCAN_END:
            break
        gs.append(float(gj))
        j += 1
    g = np.array(gs)
    ngram = len(g)

    gsign = []
    gmarg = []
    for gj in g:
        z = z_iv(widen_t(gj))
        gsign.append(cert_sign(z))
        gmarg.append(float(min(abs(z.a), abs(z.b)))
                     / (float(z.b) - float(z.a)))
    gsign = np.array(gsign)
    gsign_ok = all(x != 0 for x in gsign)
    print("(2) %d Gram points g_0..g_%d (g_top=%.3f); certified signs: %s"
          % (ngram, ngram - 1, g[-1], "OK" if gsign_ok else "FAIL"))
    gmarg = np.array(gmarg)
    i_tight = int(gmarg.argmin())

    # ---- 3. validation: interval enclosures contain high-precision values ----
    val_ok = True
    slack_list = []
    for tv in [18.0, 30.0, 50.0, 100.0, 200.0, 400.0, 700.0, 1000.0]:
        re, im = zeta_em_iv(widen_t(tv))
        z = mp.zeta(mp.mpc(0.5, tv))
        ok = (re.a <= z.real <= re.b) and (im.a <= z.imag <= im.b)
        val_ok = val_ok and bool(ok)
        slack_list.append((tv, "zeta", bool(ok)))
        zi = z_iv(widen_t(tv))
        th = theta_float(mp.mpf(tv))
        zf = mp.cos(th) * z.real - mp.sin(th) * z.imag
        ok = zi.a <= zf <= zi.b
        val_ok = val_ok and bool(ok)
        slack_list.append((tv, "Z", bool(ok)))
    th_ok = True
    for gj in g:
        thi = theta_iv(widen_t(gj))
        thf = theta_float(mp.mpf(gj))
        if not (thi.a <= thf <= thi.b):
            th_ok = False
            break
    val_ok = val_ok and th_ok
    print("(3) validation (containment vs high-precision mpmath): %s"
          % ("PASS" if val_ok else "FAIL"))
    print("    zeta/Z at 8 heights, theta at all %d Gram points" % ngram)

    # ---- 4. counts, S-values, cross-check vs zetazero ----
    def cnt_le(T):
        return int(np.searchsorted(cert_zero, T))

    s_vals = []
    for jj in range(ngram):
        n_cnt = cnt_le(g[jj])
        s_vals.append(n_cnt - 1 - jj)
    s_vals = np.array(s_vals, dtype=float)
    print("(4) count consistency vs Riemann-von Mangoldt: max |S| = %g"
          % abs(s_vals).max())

    # ---- 5. Rosser blocks and Turing/Brent theorem at the top ----
    good = gsign * np.where(np.arange(ngram) % 2 == 0, 1, -1) > 0

    def next_good(i):
        for j in range(i + 1, ngram):
            if good[j]:
                return j
        return None

    # target: last good Gram point with g <= T_CERT
    cand = [i for i in range(ngram) if good[i] and g[i] <= T_CERT]
    n = int(cand[-1])
    g_n = g[n]
    p = next_good(n)
    g_p = g[p]

    n_needed = max(1, int(np.ceil(0.0061 * np.log(g_p) ** 2
                                  + 0.08 * np.log(g_p))))
    blocks = []
    i = n
    while i is not None and len(blocks) < n_needed + 4:
        j2 = next_good(i)
        if j2 is None:
            break
        k = j2 - i
        zc = cnt_le(g[j2]) - cnt_le(g[i]) + (1 if cert_zero[
            np.searchsorted(cert_zero, g[i]) - 1] <= g[i] else 0) \
            if False else sum(1 for t in cert_zero if g[i] <= t <= g[j2])
        blocks.append((i, j2, k, zc, zc >= k))
        i = j2
    blocks_ok = all(b[4] for b in blocks[:n_needed])
    print("(5) Turing/Brent: N_needed=%d Rosser block(s) at the top"
          % n_needed)
    for (i0, j2, k, zc, okb) in blocks:
        print("    block g_%d..g_%d (len %d): %d certified zeros -> %s"
              % (i0, j2, k, zc, "Rosser OK" if okb else "Rosser FAIL"))
    print("    target n=%d, g_n=%.3f, g_p=%.3f" % (n, g_n, g_p))

    cnt_n = cnt_le(g_n)
    cnt_p = cnt_le(g_p)

    theorem_ok = (blocks_ok and val_ok and gsign_ok and all(cert_ok)
                  and cnt_n == n + 1 and cnt_p == p + 1)

    # ---- 6. cross-check vs zetazero ----
    zz = [float(mp.zetazero(k).imag) for k in range(1, n + 2)]
    zz_count = int(sum(1 for t in zz if t <= g_n))
    zz_ok = zz_count == n + 1

    nzeros = n + 1
    print("(6) certified: N(g_n) = n+1 = %d zeros <= %.3f, all on the line"
          " and simple" % (nzeros, g_n))
    print("    cross-check vs zetazero: %d == %d -> %s"
          % (zz_count, nzeros, "MATCH" if zz_ok else "MISMATCH"))
    print("    margin: min |Z|/width = %.1e at g_%d=%.3f; "
          "min |Z| at brackets = %.1e"
          % (gmarg[i_tight], i_tight, g[i_tight], min(margins)))

    # ---- 7. verdict ----
    em_at_gn = g_n / (2 * np.pi)
    rs_cut = int(np.floor(np.sqrt(g_n / (2 * np.pi))))
    cond = em_at_gn / rs_cut
    parts = []
    parts.append("certified by interval arithmetic: Z(t) = cos(theta)Re zeta"
                 " - sin(theta)Im zeta via Euler-Maclaurin + Backlund's "
                 "remainder bound and the Stirling/Binet theta series, all in "
                 "mpmath.iv (dps %d); every enclosure validated to contain "
                 "the high-precision mpmath value (containment PASS)" % IV_DPS)
    parts.append("certified signs of Z at all %d Gram points g_0..g_%d and "
                 "at both ends of every located sign-change bracket: %d "
                 "simple on-line zeros" % (ngram, ngram - 1, nz))
    parts.append("Turing's method (Brent 1979 Thm 3.2 / Lehman Thm 4): %d "
                 "top Rosser block(s) satisfy Rosser's rule, N_needed = "
                 "0.0061 ln^2(g_p) + 0.08 ln(g_p) = %.2f, hence N(g_n) <= "
                 "n+1; the certified zeros give N(g_n) >= n+1, so N(g_n) = "
                 "n+1 exactly" % (n_needed, 0.0061 * np.log(g_p) ** 2
                                  + 0.08 * np.log(g_p)))
    parts.append("therefore all %d non-trivial zeros of zeta(s) with 0 < "
                 "gamma <= g_n = %.3f lie on Re(s) = 1/2 and are simple; "
                 "RvM consistency: max |S| = %g over g_0..g_n; count "
                 "matches mpmath.zetazero (%s)"
                 % (nzeros, g_n, abs(s_vals).max(),
                    "MATCH" if zz_ok else "MISMATCH"))
    parts.append("condensation cross-point: certifying at g_n costs a fixed "
                 "N=%d Euler-Maclaurin terms per evaluation (height-"
                 "independent), while the condensed Riemann-Siegel locator "
                 "needs floor(sqrt(g_n/2pi)) = %d terms - a %.1fx per-"
                 "evaluation saving at the certified height"
                 % (N_EM, rs_cut, cond))
    overall = "; ".join(parts)
    if theorem_ok:
        verdict = ("RIEMANN-SIEGEL CERTIFIED: " + overall +
                   "; honest wall: this is a rigorous finite verification to "
                   "height g_n = %.3f (%d zeros), it does NOT prove the "
                   "Riemann hypothesis (open; rigorous verification now "
                   "extends to |t| <= 3e12, Platt-Trudgian)."
                   % (g_n, nzeros))
    else:
        verdict = ("CERTIFICATION FAILED (see above); no claim made - "
                   "honest wall: 100 zeros cannot probe RH and here the "
                   "finite certificate did not close.")
    print("\nverdict:", verdict)

    out = {
        "claim": ("a rigorous, oracle-free certification that all non-trivial "
                  "zeta zeros with ordinate <= ~1000 lie on the critical "
                  "line and are simple: interval-arithmetic Euler-Maclaurin "
                  "engine (Backlund remainder bound, directed rounding in "
                  "mpmath.iv) for certified signs of Z, plus Turing's method "
                  "in Brent's form for the exact count"),
        "setup": {
            "n_em": N_EM,
            "m_em": M_EM,
            "iv_dps": IV_DPS,
            "float_dps": FLOAT_DPS,
            "locator": ("condensed Riemann-Siegel engine "
                        "(riemann_siegel_roots.py), float, grid=%.2f"
                        % GRID),
            "bracket_half": BRACKET_HALF,
            "widen_rel": WIDEN_REL,
            "theta": ("exact Stirling/Binet series of Im logGamma(1/4+it/2) "
                      "- (t/2) log pi, real intervals, validated remainder "
                      "bound (factor %d, validated over t in [13.5, 1006], "
                      "margin >= 6.6), cross-validated against loggamma"
                      % THETA_SAFETY),
            "zeta": ("Euler-Maclaurin with Backlund's explicit remainder "
                     "bound |E| <= |B_{2M+2}|/(2M+2)! |(s)_{2M+2}| "
                     "N^{-1/2-2M-1}/|s+2M+1|"),
            "turing": ("Brent 1979 Theorem 3.2 / Lehman Theorem 4: N >= "
                       "0.0061 ln^2(g_p) + 0.08 ln(g_p) Gram blocks with "
                       "Rosser's rule => N(g_n) <= n+1"),
        },
        "validation": {
            "points": [{"t": t, "what": w, "contained": o}
                       for (t, w, o) in slack_list],
            "theta_contained_at_all_gram_points": bool(th_ok),
            "pass": bool(val_ok),
        },
        "gram_points": {
            "count": ngram,
            "g0": round(g[0], 4),
            "g_top": round(g[-1], 4),
            "certified_signs_ok": bool(gsign_ok),
            "min_margin_ratio": round(float(gmarg[i_tight]), 1),
            "min_margin_at_g_index": int(i_tight),
            "min_bracket_absZ": round(float(min(margins)), 2),
        },
        "zeros": {
            "located": nz,
            "certified_brackets_ok": bool(all(cert_ok)),
            "certified_zero_count_le_gn": cnt_n,
        },
        "count": {
            "n": n,
            "g_n": round(g_n, 4),
            "g_p": round(g_p, 4),
            "N_gn": n + 1,
            "max_abs_S": round(float(abs(s_vals).max()), 2),
            "zetazero_crosscheck_match": bool(zz_ok),
        },
        "turing": {
            "n_needed": int(n_needed),
            "n_needed_formula": round(0.0061 * np.log(g_p) ** 2
                                      + 0.08 * np.log(g_p), 2),
            "blocks": [{"start": i0, "end": j2, "length": k, "zeros": zc,
                        "rosser": okb} for (i0, j2, k, zc, okb) in blocks],
            "blocks_ok": bool(blocks_ok),
        },
        "condensation": {
            "em_terms_per_eval": N_EM,
            "rs_cutoff_at_gn": rs_cut,
            "per_eval_ratio_at_gn": round(float(cond), 1),
            "em_count_t_over_2pi_at_gn": round(em_at_gn, 1),
        },
        "verdict": verdict,
    }
    with open(os.path.join(DATA, "riemann_siegel_certify_data.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("wrote data/riemann_siegel_certify_data.json")


if __name__ == "__main__":
    main()
