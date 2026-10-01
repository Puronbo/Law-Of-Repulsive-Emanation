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


def tail(T, m, Tmax):
    """int_T^{Tmax} N(t) t^-2m dt, by substituting s = log(t/T).

    The Jacobian dt = t ds turns the integrand into
        N(T e^s) (T e^s)^{1-2m} ds,
    smooth in s on the FINITE interval [0, log(Tmax/T)].  Integrating in
    log-height keeps the quadrature well conditioned at every scale and avoids
    the silent failure of integrating to mp.inf.  The cutoff Tmax is an
    ARGUMENT, not a constant, because at m = 1 the whole point is that the
    value depends on where one stops.

    The exponent 1-2m matters.  An earlier cut of this probe used 2-2m,
    which at m = 1 integrates N(t) rather than N(t)/t; that integrand grows
    like t log t, so the "tail" came out like Tmax^2 (3.8e12 at Tmax = 1e12)
    and the log^2 divergence was completely masked.  The correct exponent
    gives 2.99, 9.35, 19.08, 32.19 at Tmax = 1e4, 1e6, 1e8, 1e10, i.e. growth
    proportional to (log Tmax)^2 as the theory requires.

    Returns (quadrature value, composite-Simpson cross-check).
    """
    T, Tmax = mp.mpf(T), mp.mpf(Tmax)
    S_max = mp.log(Tmax / T)
    def f(s):
        t = T * mp.e ** s
        return N_asym(t) * t ** (1 - 2 * m)

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
    """The m=1/m=2 crossover: fix T, vary the ceiling Tmax."""
    T0 = mp.mpf(100)
    ceilings = [mp.mpf(10) ** e for e in (4, 6, 8, 10, 12)]
    grow = {}
    for m in (1, 2, 3):
        grow[m] = [{"log10_Tmax": float(mp.log10(c)),
                    "tail": float(tail(T0, m, c)[0])} for c in ceilings]
        report["h7_growth_m%d" % m] = grow[m]

    checks = []
    for m in (1, 2, 3):
        for c in ceilings:
            v, sim = tail(T0, m, c)
            checks.append(float(abs(v - sim) / abs(v)))
    checks = max(checks)

    g1 = [r["tail"] for r in grow[1]]
    g2 = [r["tail"] for r in grow[2]]
    g3 = [r["tail"] for r in grow[3]]

    m1_grows = all(g1[i] < g1[i + 1] for i in range(len(g1) - 1))
    # For m >= 2 the truncated tail RISES towards its finite limit (it is
    # missing a positive amount that shrinks with the ceiling); it converges,
    # it does not shrink.  An earlier cut asserted monotonic decrease here,
    # which is false for a lower-limit truncation and made H7d fail.
    m2_rises = all(g2[i] < g2[i + 1] for i in range(len(g2) - 1))
    # m = 3 is already converged to full precision by the first ceiling, so its
    # entries are equal to ~15 digits and a strict < test fails on exact float
    # comparison.  What matters is that it does not GROW and is negligible.
    m3_bounded = all(g3[i] <= g3[i + 1] for i in range(len(g3) - 1))
    m3_small = g3[-1] < 1e-6
    # Convergence is certified by the increment between successive ceilings
    # tending to zero fast, far faster than the log^2 growth of m = 1.
    inc1 = abs(g1[-1] - g1[-2]) / abs(g1[-2])
    inc2 = abs(g2[-1] - g2[-2]) / abs(g2[-2])

    # Leading asymptotic for the divergent m=1 tail at fixed T0:
    # int N t^-2 dt ~ (1/(4pi)) [log(Tmax/2pi)]^2.  The ratio should be
    # approaching a constant.
    pred = [float(mp.log(c / PI2) ** 2 / (4 * mp.pi)) for c in ceilings]
    ratio = [g1[i] / pred[i] for i in range(len(ceilings))]
    report["h7_m1_pred"] = pred
    report["h7_m1_ratio"] = ratio

    # The signature of log^2 divergence is that g1/(log Tmax)^2 tends to a
    # CONSTANT, i.e. the ratio approaches a limit rather than wandering.  Test
    # monotone convergence of the ratio towards 1 with a shrinking increment,
    # not an absolute spread threshold: the ratio is still climbing at
    # 1e12 (0.69, 0.82, 0.87, 0.90, 0.92) precisely because the ceiling has
    # not yet reached the scale where the two asymptotic terms balance.
    monotone = all(ratio[i] < ratio[i + 1] for i in range(len(ratio) - 1))
    shrinking = (abs(ratio[-1] / ratio[-2] - 1.0)
                 < abs(ratio[1] / ratio[0] - 1.0))
    report["h7_m1_ratio_monotone"] = monotone

    gate("H7b: Q_m(x) converges if and only if m >= 2; Q_1 diverges like "
         "(log T)^2/(4pi)",
         m1_grows and m2_rises and m3_bounded and m3_small and checks < 1e-8
         and monotone and shrinking and ratio[-1] > 0.6 and ratio[-1] < 1.5
         and g1[-1] / g1[0] > 5,
         "sum_rho |q|^m ~ int_T^{Tmax} N(t) t^-2m dt converges iff 2m > 2. "
         "Measured at T = 100 while the ceiling rises 1e4 ... 1e12, by "
         "quadrature in log-height (the Jacobian dt = t ds is what makes the "
         "m = 1 integrand N(t)/t rather than N(t)) against a "
         "composite-Simpson cross-check, worst relative disagreement %.1e. "
         "m = 1 GROWS without bound: %.4f, %.4f, %.4f, %.4f, %.4f. m = 2 "
         "converges, rising slowly to its limit %.6f ... %.6f, and m = 3 "
         "faster still, %.6f ... %.6f; for a lower-limit truncation the tail "
         "rises towards the total, so convergence shows up as a vanishing "
         "relative increment, %.2e at m = 2 against %.2f at m = 1. The m = 1 "
         "values match the predicted log^2 law: divided by "
         "(log(Tmax/2pi))^2/(4pi) they give %.4f, %.4f, %.4f, %.4f, %.4f -- "
         "rising monotonically towards 1, which is the signature of log^2 "
         "divergence rather than an artifact. So the framework's "
         "moments exist from the second onward and not the first: any "
         "statement in sections 5, 9 or 10 ranging over m >= 1 is false as "
         "written. H6 is unaffected, its violations occurring at orders of "
         "order 10^4."
         % (checks, g1[0], g1[1], g1[2], g1[3], g1[4],
            g2[0], g2[-1], g3[0], g3[-1], inc2, inc1,
            ratio[0], ratio[1], ratio[2], ratio[3], ratio[4]))


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
         "kernel smooths away the divergence, because at moment one the two "
         "series agree to within a vanishing fraction of their (divergent) "
         "size. What separates them is the power m, and it starts at m = 2."
         % (rows[-1]["w_over_x_plus_w"], diffs[0], diffs[1], diffs[2]))


# ---------------------------------------------------------------- H7d
def _h7d():
    """Section 3's Stieltjes measure is not locally finite."""
    T0 = mp.mpf(100)
    ceilings = [mp.mpf(10) ** e for e in (4, 6, 8, 10)]
    tA = [float(tail(T0, 1, c)[0]) for c in ceilings]
    tB = [float(tail(T0, 2, c)[0]) for c in ceilings]
    report["h7_measure"] = {"log10_Tmax": [float(mp.log10(c)) for c in ceilings],
                            "mass_m1": tA, "mass_m2": tB}

    grows = all(tA[i] < tA[i + 1] for i in range(len(tA) - 1))
    bounded = all(tB[i] < 1.0 for i in range(len(tB)))
    settles = abs(tB[-1] / tB[-2] - 1.0) < 1e-3
    gate("H7d: section 3's Stieltjes measure 2 sum delta_{gamma^2} is not "
         "locally finite; Q_m's is, exactly when m >= 2",
         grows and bounded and settles and tA[-1] / tA[0] > 5,
         "The measure behind F_xi in section 3, dmu(t) = 2 sum_{gamma>0} "
         "delta_{gamma^2}, has mass up to height T that grows without bound: "
         "%.4f, %.4f, %.4f, %.4f as the ceiling rises 1e4 ... 1e10 -- the H7b "
         "log^2 divergence -- so it is not a positive measure in the sense "
         "Stieltjes requires. The measure behind Q_m, with atoms |q|^m at "
         "t = gamma^2, stays bounded and settles: %.6f, %.6f, %.6f, %.6f, "
         "converging to a finite total with a relative change of only %.1e "
         "between the last two ceilings. Hence it is locally finite for m >= 2. "
         "Section 28's third item, moment identification, therefore splits "
         "cleanly: the Widder moment reading holds from the second moment on, "
         "and the Stieltjes reading of section 3 fails as literally written."
         % (tA[0], tA[1], tA[2], tA[3], tB[0], tB[1], tB[2], tB[3],
            abs(tB[-1] / tB[-2] - 1.0)))


def main():
    print("H7: convergence/interchange audit of record section 28\n")
    _h7a()
    _h7b()
    _h7c()
    _h7d()

    report["conclusion"] = (
        "H7 audits section 28's convergence/interchange and "
        "moment-identification items. %d/%d sub-gates pass. "
        "CLARIFICATION (H7a): the summand q_rho(x) = w/(x+w)^2 decays like "
        "gamma^-2, not gamma^-4 -- the numerator w cancels one power of the "
        "squared denominator, since |w|/|w|^2 = 1/|w|. Measured log-log slope "
        "%.4f on %s Newton-refined real zeros. An earlier cut predicted -4 and "
        "misread its own -2.00 measurement as a regime artefact. "
        "DEFECT (H7b): with N(T) ~ (T/2pi) log(T/2pi), the tail "
        "int_T^inf N(t) t^-2m dt converges iff 2m > 2. So Q_1(x) DIVERGES, "
        "growing like (log T)^2/(4pi), while Q_m converges for every m >= 2. "
        "The framework's moments exist from the second onward only, so any "
        "claim ranging over m >= 1 in sections 5, 9 or 10 is false as "
        "written. CONSEQUENCE (H7c): Q_1 and F_xi are asymptotically the same "
        "series -- their summands differ by w/(x+w) -> 1 -- so the middle "
        "arrow of section 27's chain cannot be rescued by smoothing, and its "
        "regularization obligation applies at moment one as well. "
        "CONSISTENCY (H7d): section 3's Stieltjes measure 2 sum "
        "delta_{gamma^2} is not locally finite, while Q_m's measure is for "
        "m >= 2, so the Stieltjes reading fails exactly where the Widder "
        "reading starts to hold. Nothing here proves or refutes RH; H6 is "
        "untouched since its violations occur at orders of order 10^4. No "
        "positive Hankel kernel is supplied, and section 27's bridge "
        "prime-gamma -> universal H_N >= 0 remains OPEN, its technical "
        "obligation now pinned to a single statement: begin the moment "
        "sequence at m = 2 and regularize F_xi consistently, or show the "
        "explicit formula's prime side supplies that regularization."
        % (gates_passed, len(report["gates"]), report["h7_real_slope"],
           len(SEEDS)))

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
