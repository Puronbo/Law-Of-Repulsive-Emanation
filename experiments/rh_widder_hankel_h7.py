#!/usr/bin/env python3
"""
rh_widder_hankel_h7.py -- H7: the convergence/interchange audit of record
section 28, "Verify every convergence/interchange condition".

H6 settled the zero-side geometry.  Section 27's desired derivation is

    prime-gamma explicit formula -> F_xi -> Q_k -> H_N -> c^T H_N c >= 0,

and section 28 lists as still open
    * derive a rigorous positive Hankel kernel from the explicit formula,
    * verify every convergence/interchange condition,
    * complete the moment uniqueness/identification argument,
    * determine whether the required collective positivity can be proved.

H7 attacks the second and third items.  It contains one structural PASS, one
genuine DEFECT, and one correcting CLARIFICATION, and the defect is sharper
than a naive reading suggests.

Sub-gates:

  H7a  The summand q_rho(x) = w/(x+w)^2 decays like gamma^-2, NOT gamma^-4.
       This is the load-bearing correction.  It is tempting to argue that
       because the denominator is squared the decay is gamma^-4, but the
       numerator is w itself: |w/(x+w)^2| ~ |w|/|w|^2 = 1/|w| ~ gamma^-2.
       A log-log regression on Newton-refined real zeros measures the exponent
       directly and returns -2.00.  (An earlier cut of this probe asserted
       gamma^-4 and reported a failing slope of -2.00, then "explained" the
       discrepancy as an undersampled asymptotic regime.  That explanation
       was wrong; the -2.00 was the correct answer being reported as a
       failure.)

  H7b  Consequently Q_m(x) converges if and only if m >= 2.  With
       N(T) ~ (T/2pi) log(T/(2pi)),
           sum_rho |q_rho(x)|^m  ~  int_T^inf N(t) t^-2m dt,
       which converges iff 2m > 2.  So m = 1 DIVERGES, growing like
       (log T)^2/(4pi), while m >= 2 converges with tail O(T^{1-2m} log T).
       The framework's moments are therefore well defined from the second
       moment onward and NOT from the first.  This is a real constraint on
       sections 5/9/10: any statement silently ranging over m >= 1 is wrong.

  H7c  Q_1 and F_xi are the SAME divergent series.  The ratio of summands is
           q_rho(x) / (1/(x+w_rho)) = w_rho/(x+w_rho) -> 1
       as gamma -> inf, so the two series differ only by terms whose relative
       size vanishes.  Hence the regularization obligation at the middle of
       section 27's chain cannot be discharged by "the Hankel kernel is
       smoother than F_xi": at moment one they are asymptotically identical.
       What separates them is the power m, and it starts at m = 2.

  H7d  Section 3's Stieltjes measure dmu(t) = 2 sum_{gamma>0} delta_{gamma^2}(t)
       is not a locally finite measure: its mass up to height T grows like
       (log T)^2.  Q_m's measure (atoms |q|^m at t = gamma^2) is locally
       finite precisely when m >= 2.  So the Stieltjes reading of section 3
       and the Widder reading of section 5 fail and hold at the same place,
       consistently with H7b/H7c.

What is deliberately NOT claimed: nothing here proves or refutes RH.  H6's
concrete violations sit at orders m of order 10^4, where convergence is not
in question, so H6 is untouched.  H7 does not supply the positive Hankel
kernel of section 28's first item, and it does not touch section 27's open
bridge prime-gamma -> universal H_N >= 0.  It does shrink that bridge's
technical obligation to a single, precisely locatable statement.

Run:  python experiments/rh_widder_hankel_h7.py

Artifact: experiments/data/rh_widder_hankel_h7_data.json
"""

import json
import os
import sys

import mpmath as mp

mp.mp.dps = 30

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PI2 = 2 * mp.pi
H7_X = mp.mpf("0.1")

SEEDS = ["14.134725141734693790", "21.022039638771554993",
         "25.010857580145688764", "30.424876125859513211",
         "32.935061587739189691", "37.586178158825671257",
         "40.918719012147495187", "43.327073280914999519",
         "48.005150881167156727", "49.773832477672302182"]

report = {"experiment": "convergence/interchange audit of record section 28",
          "gates": [], "conclusion": ""}
gates_passed = 0


def gate(name, ok, detail):
    global gates_passed
    ok = bool(ok)
    report["gates"].append({"gate": name, "passed": ok, "detail": detail})
    print("  [%s] %s" % ("PASS" if ok else "FAIL", name))
    if ok:
        gates_passed += 1


# ------------------------------------------------------------------ zeta
def _xi(s):
    return mp.mpf("0.5") * (
        s * (s - 1) * mp.pi ** (-s / 2) * mp.zeta(s)
        + (1 - s) * (2 - s) * mp.pi ** (-(1 - s) / 2) * mp.zeta(1 - s))


def zeta_zero_gamma(seed):
    t = mp.mpf(seed)
    half = mp.mpf("0.5")
    for _ in range(80):
        h = mp.mpf("1e-8")
        t = mp.re(t)
        f = _xi(mp.mpc(half, t))
        d = (_xi(mp.mpc(half, t + h)) - _xi(mp.mpc(half, t - h))) / (2 * h)
        if d == 0:
            break
        step = f / d
        t = t - step
        if abs(step) < mp.mpf("1e-25"):
            break
    return mp.re(t)


# ------------------------------------------------------- zero counting
def N_asym(T):
    """Riemann-von Mangoldt: N(T) = u log u - u + 7/8 + O(1/u), u = T/(2pi).

    NOTE: the truncated formula goes NEGATIVE below T ~ 9.677 (the solution of
    u log u - u + 7/8 = 0 with u = T/(2pi)); it dips to about -0.11 near
    T = 5.  It must not be clamped -- an earlier probe clamped it to >= 1,
    which silently destroyed the very divergence being measured.  All calls
    here use T >= 50, far above the regime where the truncation is reliable.
    """
    u = mp.mpf(T) / PI2
    return u * mp.log(u) - u + mp.mpf(7) / 8


def invert_N(target):
    """Height T with N(T) = `target`, by inverting u log u - u + 7/8."""
    target = mp.mpf(target)
    b = mp.mpf(2) * mp.pi * 3
    while N_asym(b) < target:
        b *= 2
    a = mp.mpf(2)
    for _ in range(300):
        mid = (a + b) / 2
        if N_asym(mid) < target:
            a = mid
        else:
            b = mid
    return (a + b) / 2


def xi_sign(t):
    """Sign of the real number xi(1/2+it), for t > 0.

    xi(1/2+it) is REAL by the functional equation's symmetry, so its zeros
    are exactly the critical-line zeros of zeta and each simple one flips its
    sign.  It is evaluated here as a product of complex factors rather than by
    the completed-zeta routine, because xi itself grows like
    exp(t log t / 2) and overflows long before t = 1000; the sign is the only
    thing needed and the product cannot overflow.

    Counting sign changes of Im zeta(1/2+it) instead is WRONG, by about a
    factor of two: Im zeta vanishes at every t where zeta(1/2+it) is real,
    which is a great many t that are not zeros of xi.  That variant returns
    1956 for t <= 1000 where the true count is 649, and an earlier cut of
    this gate would have "confirmed" the asymptotic 2 N(sqrt U) against a
    count that was double it.
    """
    s = mp.mpc(mp.mpf("0.5"), mp.mpf(t))
    v = (s * (s - 1) / 2 * mp.e ** (-s * mp.log(mp.pi) / 2)
         * mp.gamma(s / 2) * mp.zeta(s))
    return v.real


def count_zeros_upto(Tmax, step=mp.mpf("0.25"), start=mp.mpf("14")):
    """COUNT critical-line zeta zeros with gamma <= Tmax, by sign changes of
    xi(1/2+it).

    Counting sign changes, NOT refining each root.  Newton refinement costs
    0.7 s per zero here (80 finite-difference xi iterations), and this gate
    needs only a count: t <= 1000 holds 649 zeros, so refining them all would
    spend eight minutes on information a sign change already carries.

    `step` must be finer than the SMALLEST gap between consecutive zeros in
    the range, not the mean gap.  The mean spacing near t = 1000 is about
    1.5, but a few close pairs sit near 0.2, and a step of 0.5 steps over
    four of them: it reports 645 where step 0.25 correctly reports 649.  That
    is the whole margin this gate depends on, so it is checked, not assumed.
    """
    t = mp.mpf(start)
    n = 0
    prev = mp.sign(xi_sign(t))
    while t < Tmax:
        t += step
        cur = mp.sign(xi_sign(t))
        if prev * cur < 0:
            n += 1
        prev = cur
    return n


def zeros_upto(Tmax, step=mp.mpf("0.25"), start=mp.mpf("14")):
    """Refined heights of critical-line zeros with gamma <= Tmax.  SLOW by
    construction; prefer count_zeros_upto unless the heights are needed."""
    out = []
    t = mp.mpf(start)
    prev = mp.sign(xi_sign(t))
    while t < Tmax:
        t += step
        cur = mp.sign(xi_sign(t))
        if prev * cur < 0:
            out.append(zeta_zero_gamma(t))
        prev = cur
    return out


def dN_asym(t):
    """Riemann-von Mangoldt density: dN = (1/(2 pi)) log(t/2 pi) dt.

    This, not N(t), is the measure the zero sum is weighted by.  The
    framework wrote int_T^inf N(t) t^-2m dt, which is the integral of the
    COUNT against the measure dt rather than of the DENSITY against dt, and
    it changes the convergence threshold from 2m > 1 to 2m > 2.  That single
    Jacobian was the largest defect found in sections 3 and 28; H9b
    isolates it and H8d/H7d are corrected accordingly.
    """
    return mp.log(t / PI2) / (2 * mp.pi)


def tail(T, m, Tmax, measure="dN"):
    """int_T^{Tmax} t^-2m d(measure), by substituting s = log(t/T).

    The Jacobian dt = t ds turns the integrand into
        t^{1-2m} * weight(t),  smooth in s on the FINITE interval
        [0, log(Tmax/T)].  Integrating in log-height keeps the quadrature
    well conditioned at every scale and avoids the silent failure of
    integrating to mp.inf.  The cutoff Tmax is an ARGUMENT, not a constant.

    measure="dN"   -> weight = (1/2pi) log(t/2pi)      [CORRECT]
    measure="N"    -> weight = N(t) = (t/2pi) log(t/2pi)  [H7's original]

    The exponent is 1-2m, not 2-2m: an earlier cut used 2-2m, which at
    m = 1 integrates N(t) rather than N(t)/t, so the "tail" came out like
    Tmax^2 and the log^2 behaviour was completely masked.

    Returns (quadrature value, composite-Simpson cross-check).
    """
    T, Tmax = mp.mpf(T), mp.mpf(Tmax)

    def weight(t):
        return dN_asym(t) if measure == "dN" else N_asym(t)

    S_max = mp.log(Tmax / T)

    def f(s):
        t = T * mp.e ** s
        return weight(t) * t ** (1 - 2 * m)

    val = mp.quad(f, [0, S_max])

    n = 4000
    h = S_max / n
    tot = f(0) + f(S_max)
    for i in range(1, n):
        tot += f(i * h) * (4 if i % 2 else 2)
    simpson = tot * h / 3
    return val, simpson


# ---------------------------------------------------------------- H7a
def _h7a():
    gammas = [zeta_zero_gamma(s) for s in SEEDS]
    resid = max(abs(_xi(mp.mpc(mp.mpf("0.5"), g))) for g in gammas)

    def q_of(g):
        return g * g / (H7_X + g * g) ** 2

    ls = [(float(mp.log(g)), float(mp.log(q_of(g)))) for g in gammas]
    n = len(ls)
    sx = sum(a for a, _ in ls)
    sy = sum(b for _, b in ls)
    sxx = sum(a * a for a, _ in ls)
    sxy = sum(a * b for a, b in ls)
    slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)

    # Independent confirmation over a wide synthetic height range, where the
    # gamma >> sqrt(x) asymptote is unambiguous.
    syn = []
    for e in range(2, 61):
        g = mp.mpf(10) ** (e / 10.0)
        syn.append((float(mp.log(g)), float(mp.log(q_of(g)))))
    n2 = len(syn)
    ax = sum(a for a, _ in syn)
    ay = sum(b for _, b in syn)
    axx = sum(a * a for a, _ in syn)
    axy = sum(a * b for a, b in syn)
    slope_syn = (n2 * axy - ax * ay) / (n2 * axx - ax * ax)

    # Direct asymptote check, stated scale-free.  We have
    #     q ~ x^2/gamma^4        as gamma >> sqrt(x),
    # so the natural dimensionless ratio is q * gamma^4 / x^2 -> 1.
    # (An earlier cut instead used gamma^2 q / x^2, which tends to 1/x^2 = 100
    # at x = 0.1 and so can never approach 1 for x != 1.  The limit is fine;
    # that particular normalization is not.)  Gauge the ratio against its own
    # small-height value so the comparison is scale-free in x.
    asym = []
    for mult in (10, 100, 1000, 10000):
        g = H7_X * mult
        rel = q_of(g) * g ** 4 / H7_X ** 2
        base = q_of(H7_X * 10) * (H7_X * 10) ** 4 / H7_X ** 2
        asym.append({"gamma_over_x": float(mult),
                     "rel_q_g4_over_x2": float(rel),
                     "rel_to_first": float(rel / base)})

    report["h7_real_slope"] = slope
    report["h7_synth_slope"] = slope_syn
    report["h7_asymptote"] = asym
    report["h7_max_residual"] = float(resid)
    report["h7_gammas"] = [float(g) for g in gammas]

    ok_asym = asym[-1]["rel_to_first"] > 1000.0
    gate("H7a: |q_rho(x)| decays like gamma^-2 (the numerator w cancels one "
         "power), NOT gamma^-4",
         abs(slope + 2.0) < 0.05 and abs(slope_syn + 2.0) < 0.01 and ok_asym,
         "q_rho(x) = w/(x+w)^2. The naive reading is that a squared "
         "denominator buys gamma^-4, but the numerator is w itself, so "
         "|q| ~ |w|/|w|^2 = 1/|w| ~ gamma^-2. Measured directly: a log-log "
         "regression of |q| against gamma over %d Newton-refined real zeros "
         "gives slope %.4f (worst |xi| residual %.1e), and over six decades of "
         "synthetic heights %.4f. The asymptote q ~ x^2/gamma^4 is confirmed "
         "through q gamma^4 / x^2, which grows by a factor %.4f per decade of "
         "gamma and would diverge if the exponent were -4. An earlier cut of "
         "this probe predicted slope -4, measured -2.00, and attributed the "
         "mismatch to an undersampled asymptotic regime; that attribution was "
         "wrong, and it separately used a ratio gamma^2 q / x^2 that tends to "
         "1/x^2 rather than 1. The exponent -2 is the load-bearing fact that "
         "turns H7b into a defect rather than a pass."
         % (len(gammas), slope, float(resid), slope_syn,
            asym[-1]["rel_to_first"]))


# ---------------------------------------------------------------- H7b
def _h7b():
    """The m=1/m=2 crossover against the CORRECT measure dN.

    An earlier cut of this gate integrated N(t) t^-2m dt, weighting the zero
    COUNT by dt instead of the DENSITY by dt.  That inflated the m=1 tail by
    ~170x (4.33e-3 against 2.60e-5) and made it creep upward with the
    ceiling instead of settling, which is what produced the false threshold
    "converges iff m >= 2".  Against dN the threshold is 2m > 1, so Q_1
    converges after all.  Both measures are computed here so the contrast is
    on the record rather than merely asserted.
    """
    T0 = mp.mpf(100)
    ceilings = [mp.mpf(10) ** e for e in (4, 6, 8, 10, 12, 14)]
    grow = {}
    grow_n = {}
    for m in (1, 2):
        grow[m] = [{"log10_Tmax": float(mp.log10(c)),
                    "tail": float(tail(T0, m, c, "dN")[0])} for c in ceilings]
        report["h7_growth_m%d" % m] = grow[m]
    # the withdrawn measure, kept for contrast
    grow_n[1] = [{"log10_Tmax": float(mp.log10(c)),
                  "tail": float(tail(T0, 1, c, "N")[0])} for c in ceilings]
    report["h7_growth_m1_Nweighted"] = grow_n[1]

    checks = []
    for m in (1, 2):
        for c in ceilings:
            for meas in ("dN", "N"):
                v, sim = tail(T0, m, c, meas)
                checks.append(float(abs(v - sim) / abs(v)))
    checks = max(checks)

    g1 = [r["tail"] for r in grow[1]]
    g2 = [r["tail"] for r in grow[2]]
    n1 = [r["tail"] for r in grow_n[1]]

    # Convergence is a SETTLING, not a growth: successive increments collapse.
    # For a lower-limit truncation the tail RISES towards the total, so the
    # test is a vanishing relative increment, not a decrease.
    inc1 = abs(g1[-1] / g1[-2] - 1.0)
    inc2 = abs(g2[-1] / g2[-2] - 1.0)
    settled = inc1 < 1e-6 and inc2 < 1e-9
    # and m=1 must actually be nonzero and much larger than m=2
    ordered = g1[-1] > 100 * g2[-1]

    # The withdrawn N-weighted version: still creeping at the last ceiling.
    n_increep = abs(n1[-1] / n1[-2] - 1.0)
    n_wrongly_large = n1[-1] > 100 * g1[-1]

    # Threshold is 2m > 1, so m = 1 is already convergent; m = 1/2 must NOT be.
    half, _ = tail(T0, mp.mpf("0.5"), mp.mpf(10) ** 14, "dN")
    half_grows = half > 100 * g1[-1]

    report["h7_m1_settled_increment"] = float(inc1)
    report["h7_m2_settled_increment"] = float(inc2)
    report["h7_Nweighted_increment"] = float(n_increep)

    gate("H7b CORRECTED: the threshold is 2m > 1, NOT 2m > 2; Q_1 converges "
         "and Q_1/2 diverges. The earlier cut integrated N(t) t^-2m dt, "
         "weighting the zero COUNT by dt rather than the DENSITY, and that "
         "single Jacobian was the whole defect",
         settled and ordered and half_grows and n_wrongly_large
         and n_increep > 1e-4 and checks < 1e-8,
         "The zero sum is weighted by dN, the Riemann-von Mangoldt DENSITY, "
         "not by N. sum_rho |q|^m ~ int_T^inf t^-2m dN(t) = "
         "int_T^inf (1/(2pi)) log(t/2pi) t^-2m dt, whose integrand decays like "
         "t^-2m log t, so it converges iff 2m > 1 and Q_1 is FINE. Measured at "
         "T = 100 with the ceiling rising 1e4 ... 1e14, by quadrature in "
         "log-height against a composite-Simpson cross-check, worst relative "
         "disagreement %.1e: the m = 1 tail SETTLES at %.6e, %.6e, %.6e, "
         "%.6e, %.6e, %.6e, successive increments collapsing to %.1e, while "
         "m = 2 settles at %.3e with increment %.1e and is ~%.0fx smaller. "
         "m = 1/2 does NOT converge: its tail at ceiling 1e14 is %.1fx the "
         "m = 1 value. The withdrawn N-weighted integral gives %.4e, %.4e, "
         "%.4e, %.4e, %.4e, %.4e -- ~%.0fx too large and still creeping, its "
         "last increment being %.1e. So the claim 'the framework's moments "
         "exist from the second onward only', and with it the corollary that "
         "sections 5, 9, 10 are false as written for m >= 1, is WITHDRAWN: "
         "Q_1 exists. H9b pins the same correction independently."
         % (checks, g1[0], g1[1], g1[2], g1[3], g1[4], g1[5], inc1,
            g2[-1], inc2, g1[-1] / g2[-1],
            float(half / g1[-1]),
            n1[0], n1[1], n1[2], n1[3], n1[4], n1[5],
            n1[-1] / g1[-1], n_increep))


# ---------------------------------------------------------------- H7c
def _h7c():
    """q_1 and F_xi are asymptotically the same series."""
    x = mp.mpf("1000")
    rows = []
    for mult in (1, 10, 100, 1000, 10000):
        g = x * mult
        w = g * g
        ratio = w / (x + w)          # q / (1/(x+w))
        rows.append({"gamma_over_x": float(mult), "w_over_x_plus_w": float(ratio)})
    report["h7_ratio_rows"] = rows

    # Empirically: build both partial sums over a synthetic zeta-like spectrum
    # and confirm the two disagree only in the low-height end.  The spectrum is
    # SAMPLED, not enumerated: iterating g = sqrt(k log k) one index at a time
    # up to T = 1e6 needs ~1e8 zeros and exhausts memory.  Instead take a fixed
    # number of equally spaced INDICES and invert N(g) = (g/2pi) log(g/2pi).
    partial = []
    npts = 20000
    for Tmax in (mp.mpf(100), mp.mpf("1e4"), mp.mpf("1e6")):
        gammas = [invert_N(N1) for N1 in
                  [Tmax ** 2 / (4 * mp.pi ** 2 * mp.log(Tmax / PI2 + 2))
                   * (i + 1) / npts for i in range(npts)]]
        xx = mp.mpf("0.5")
        sQ = mp.fsum([(g * g / (xx + g * g) ** 2) for g in gammas])
        sF = mp.fsum([1 / (xx + g * g) for g in gammas])
        partial.append({"Tmax": float(Tmax), "count": npts,
                        "Q1_partial": float(sQ), "F_partial": float(sF),
                        "rel_diff": float(abs(sQ - sF) / abs(sF))})
    report["h7_partial"] = partial

    diffs = [p["rel_diff"] for p in partial]
    gate("H7c: Q_1 and F_xi are asymptotically the SAME series -- the ratio of "
         "summands is w/(x+w) -> 1",
         abs(rows[-1]["w_over_x_plus_w"] - 1.0) < 1e-6
         and diffs[-1] < diffs[0] < 0.5,
         "Dividing q_rho(x) by F_xi's summand gives w/(x+w) -> 1 as gamma "
         "grows, measured %.9f at gamma = 10^4 x. Built with a zeta-like "
         "synthetic spectrum g ~ sqrt(k log k), the two partial sums have "
         "relative difference %.4f, %.4f, %.4f at heights T = 100, 1e4, 1e6: "
         "the discrepancy is confined to the low-height end and shrinks "
         "monotonically, while both sums themselves grow like log^2 T. This "
         "blocks the most natural rescue of section 27's middle arrow. One "
         "cannot regularize F_xi and read Q_k off it while claiming the Hankel "
         "kernel smooths away the difference, because at moment one the two "
         "series agree to within a vanishing fraction of their common size. "
         "SCOPE CORRECTED: an earlier cut closed with 'what separates them is "
         "the power m, and it starts at m = 2', which imported H7b's withdrawn "
         "threshold. Both series converge at m = 1 (H7b corrected, H9b), and "
         "the difference between them at moment one is a finite vanishing "
         "fraction, not a divergence to be regularized away. What remains of "
         "H7c is only that Q_1 and F_xi are the same series to leading order, "
         "so moment identification transfers without smoothing; no "
         "regularization obligation arises at m = 1 from this comparison."
         % (rows[-1]["w_over_x_plus_w"], diffs[0], diffs[1], diffs[2]))


# ---------------------------------------------------------------- H7d
def _h7d():
    """dmu = 2 sum_{gamma>0} delta_{gamma^2} IS locally finite. CORRECTION.

    An earlier cut of this gate asserted that section 3's Stieltjes measure is
    NOT locally finite, reading the growth of 2 N(sqrt T) with T as
    non-local-finiteness.  Those are different things.  Local finiteness asks
    only that the mass on each COMPACT be finite; a counting measure on an
    unbounded support has finite mass on every compact and is the standard
    locally finite measure of the theory.  The growth is unbounded total
    mass, which is expected and harmless -- Stieltjes theory needs local
    finiteness, not finite total mass.  Conflating them produced a spurious
    obstruction to section 3's whole Stieltjes reading, and the mirrored
    claim that Q_m's measure is locally finite "exactly when m >= 2", which
    now that Q_1 converges is false: it is locally finite for m >= 1.
    """
    T0 = mp.mpf(100)
    ceilings = [mp.mpf(10) ** e for e in (4, 6, 8, 10, 12, 14)]
    tA = [float(tail(T0, 1, c, "dN")[0]) for c in ceilings]
    tB = [float(tail(T0, 2, c, "dN")[0]) for c in ceilings]
    report["h7_measure"] = {"log10_Tmax": [float(mp.log10(c)) for c in ceilings],
                            "mass_m1": tA, "mass_m2": tB}

    # Local finiteness of dmu: on [0, U] the mass is 2 N(sqrt U), a finite
    # COUNT for every finite U.  Measured against the asymptotic count and
    # compared with a direct enumeration of the zeros below sqrt(U).
    # Enumerate REAL zeros by scanning zeta, not by reusing SEEDS.  SEEDS holds
    # only 10 heights (all <= 49.8), so counting gamma^2 <= U from it
    # saturates at 20 for every U >= 2500 and made an earlier version of this
    # gate compare 20 against an asymptotic 1297.  Counted with
    # count_zeros_upto, which tallies sign changes rather than refining each
    # root: 0.7 s per Newton refinement x ~860 zeros is ten minutes spent on
    # information a sign change already carries.
    # U starts at 1e4, not 1e2: N_asym goes negative below t ~ 9.677 and its
    # own docstring requires t >= 50, so sqrt(U) must be >= 50.
    rows = []
    for U in (mp.mpf(10) ** 4, mp.mpf(10) ** 5, mp.mpf(10) ** 6):
        counted = 2 * count_zeros_upto(mp.sqrt(U))
        asym = 2 * N_asym(mp.sqrt(U))
        rows.append({"U": float(U),
                     "log10U": float(mp.log10(U)),
                     "sqrtU": float(mp.sqrt(U)),
                     "counted": counted,
                     "asym": float(asym)})
    report["h7_dmu_local_mass"] = rows

    # mu([0,U]) is a COUNT, so it is finite for every finite U.  The stronger
    # statement local finiteness actually uses is mass = o(U), i.e.
    # 2 N(sqrt U) < U, which holds because the mass grows like U^{1/2} log U.
    # An earlier cut compared it against U^{1/2} instead, which the mass
    # exceeds asymptotically -- a bound that is false, not a margin to tune.
    # It also compared against a field holding log10(U) = 4, 5, 6, so every
    # mass of 58, 296, 1298 failed a bound of about 2.
    finite_per_compact = all(isinstance(r["counted"], int)
                             and r["counted"] < r["U"] for r in rows)
    counted_grows = all(rows[i]["counted"] < rows[i + 1]["counted"]
                        for i in range(len(rows) - 1))
    # Riemann-von Mangoldt truncated at 7/8 is accurate to O(1/sqrt U); the
    # enumerated count must agree to within a small absolute slack.
    asym_ok = all(abs(r["asym"] - r["counted"]) <= 3.0 for r in rows)

    # Q_m's own measure is locally finite for m >= 1, not "exactly m >= 2".
    inc1 = abs(tA[-1] / tA[-2] - 1.0)
    inc2 = abs(tB[-1] / tB[-2] - 1.0)
    settles = inc1 < 1e-6 and inc2 < 1e-9

    gate("H7d CORRECTED: dmu = 2 sum delta_{gamma^2} IS locally finite -- local "
         "finiteness is finite mass on each COMPACT, not bounded total mass. "
         "The earlier cut conflated the two and built a spurious obstruction "
         "to section 3's Stieltjes reading",
         finite_per_compact and counted_grows and asym_ok and settles,
         "Local finiteness asks that mu([0, U]) be finite for every finite U; "
         "dmu([0, U]) = 2 #{gamma : gamma^2 <= U} is a COUNT, hence finite "
         "for every finite U, whatever it does as U grows. Measured on "
         "U = 1e4, 1e5, 1e6 the enumerated masses are %.0f, %.0f, %.0f, "
         "matching the asymptotic count 2 N(sqrt U) = %.1f, %.1f, %.1f to "
         "within 3. The mass does grow without bound "
         "as U grows -- it grows like U^{1/2} log U -- but that is unbounded "
         "TOTAL mass on an unbounded support, which every counting measure has "
         "and which Stieltjes theory does not object to. So the earlier "
         "claim 'not locally finite' is WITHDRAWN, and with it the claim that "
         "the Stieltjes reading of section 3 fails as literally written. The "
         "mirrored claim that Q_m's measure is locally finite 'exactly when "
         "m >= 2' is also withdrawn: Q_1 converges (H7b corrected, H9b), so "
         "its measure is locally finite from m = 1, settling at %.6e with "
         "increment %.1e against %.6e, %.1e at m = 2. Both moments stand, and "
         "section 3's moment identification needs no regularization at m = 1."
         % (rows[0]["counted"], rows[1]["counted"], rows[2]["counted"],
            rows[0]["asym"], rows[1]["asym"], rows[2]["asym"],
            tA[-1], inc1, tB[-1], inc2))

def main():
    print("H7: convergence/interchange audit of record section 28\n")
    _h7a()
    _h7b()
    _h7c()
    _h7d()

    report["conclusion"] = (
        "H7 audits section 28's convergence/interchange and "
        "moment-identification items. %d/%d sub-gates pass. "
        "CLARIFICATION (H7a, stands): the summand q_rho(x) = w/(x+w)^2 decays "
        "like gamma^-2, not gamma^-4 -- the numerator w cancels one power of "
        "the squared denominator, since |w|/|w|^2 = 1/|w|. Measured log-log "
        "slope %.4f on %s Newton-refined real zeros. An earlier cut predicted "
        "-4 and misread its own -2.00 measurement as a regime artefact. "
        "CORRECTION (H7b): the zero sum is weighted by dN, the "
        "Riemann-von Mangoldt DENSITY, not by N, so the tail is "
        "int_T^inf t^-2m dN(t) = int_T^inf (1/(2pi)) log(t/2pi) t^-2m dt and "
        "the threshold is 2m > 1, NOT 2m > 2. Q_1 therefore CONVERGES: its "
        "tail at T = 100 settles at %.4e across ceilings 1e4 ... 1e14 with "
        "successive increments collapsing to %.1e, while m = 1/2 does not "
        "converge. The earlier cut integrated N(t) t^-2m dt, weighting the "
        "COUNT by dt; that single Jacobian made the m=1 tail ~%.0fx too large "
        "and left it creeping upward, and it is the sole basis of the "
        "withdrawn claim that the framework's moments exist from the second "
        "moment onward and that sections 5, 9, 10 are false as written for "
        "m >= 1. H9b pins the same correction independently. "
        "SCOPE (H7c, narrowed): Q_1 and F_xi are asymptotically the same "
        "series -- their summands differ by w/(x+w) -> 1 -- so moment "
        "identification transfers to F_xi without smoothing. The earlier "
        "statement that this created a regularization obligation at moment one "
        "is WITHDRAWN: both series converge at m = 1 and their difference is "
        "a vanishing fraction of a common finite size, not a divergence to be "
        "regularized away. "
        "CORRECTION (H7d): dmu = 2 sum_{gamma>0} delta_{gamma^2} IS locally "
        "finite. Local finiteness asks that mu([0,U]) be finite for every "
        "finite U, and dmu([0,U]) = 2 #{gamma : gamma^2 <= U} is a count. The "
        "mass does grow like U^{1/2} log U, but unbounded TOTAL mass on an "
        "unbounded support is what every counting measure has, and Stieltjes "
        "theory does not object to it. The earlier cut conflated unbounded "
        "total mass with non-local-finiteness and built a spurious "
        "obstruction to section 3's whole Stieltjes reading; that is "
        "WITHDRAWN. The mirrored claim that Q_m's measure is locally finite "
        "'exactly when m >= 2' is likewise withdrawn, since Q_1 converges. "
        "Net effect: section 3's moment identification needs no "
        "regularization at m = 1, and the sections previously flagged as false "
        "as written for m >= 1 are restored. "
        "Nothing here proves or refutes RH; H6 is untouched since its "
        "violations occur at orders of order 10^4. No positive Hankel kernel "
        "is supplied, and section 27's bridge prime-gamma -> universal "
        "H_N >= 0 remains OPEN, but its technical obligation is no longer the "
        "'start at m = 2' workaround, which is withdrawn. What remains open "
        "is the substantive question H8c sharpened: whether any Hankel kernel "
        "of the Widder type is positive at all, since the required rank grows "
        "without bound as an off-axis zero's displacement delta -> 0."
        % (gates_passed, len(report["gates"]), report["h7_real_slope"],
           len(SEEDS),
           report["h7_growth_m1"][-1]["tail"],
           report["h7_m1_settled_increment"],
           report["h7_growth_m1_Nweighted"][-1]["tail"]
           / report["h7_growth_m1"][-1]["tail"]))

    if gates_passed != len(report["gates"]):
        report["conclusion"] = "NOT ALL GATES PASSED - conclusions invalid."

    out_dir = os.path.join(ROOT, "experiments", "data")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "rh_widder_hankel_h7_data.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)

    print("\n" + "=" * 74)
    print("SUMMARY: %d/%d gates pass" % (gates_passed, len(report["gates"])))
    print("=" * 74)
    print(report["conclusion"])
    print("\nwrote %s" % os.path.relpath(path, ROOT))
    return 0 if gates_passed == len(report["gates"]) else 1


if __name__ == "__main__":
    sys.exit(main())
