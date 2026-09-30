"""experiments/chi_rho_vacuity_0_over_0.py - is the Chi(rho) bridge a test of RH?

The corpus asserts, in ~15 files, that the bridge

    zeta(s) = chi(s) zeta(1-s),   chi(s) = 2^s pi^(s-1) sin(pi s/2) Gamma(1-s)
    g(s)    = |zeta(s)| / |zeta(1-s)|
certifies the Riemann Hypothesis, because at every nontrivial zero rho the
removable value of the 0/0 is |chi(rho)| = 1 (README.md, docs/FRAMEWORK.md
"Verified", docs/THE_LAW_OF_SINGULARITIES.md "SUPPORTED", the RH reduction
paper, and the sigma bridge module).

This entry separates the three things that run together in that sentence:

  A. the removable-value identity   g -> |chi(rho)| as s -> rho     (TRUE)
  B. the level-set statement        |chi(sigma+it)| = 1 <=> sigma = 1/2
       ... which is TRUE only on the critical strip 0 < sigma < 1. Globally
       there are two further roots at 1/2 +- d(t) for t < t*, annihilating at
       t* = 6.2898359888369 where the line becomes a double root.
  C. the certification claim        therefore RH is verified        (VACUOUS)

A and B are elementary and hold exactly. C does not follow, and the reason
is structural rather than numerical: |chi| = 1 is a property of the LINE, so
evaluating it at a zero - which is a point on the line - cannot distinguish
a zero from any other point on the line. The instrument has no teeth.

Writes data/chi_rho_vacuity_data.json (gitignored) holding every measured
number below. Runs standalone:

    python experiments/chi_rho_vacuity_0_over_0.py
"""

import json
import os

import mpmath as mp

mp.mp.dps = 30

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "data", "chi_rho_vacuity_data.json")

# Where the repo looks for the identity to hold. |chi| = 1 to this tolerance.
TOL = mp.mpf("1e-25")


def chi(s):
    """chi(s) = pi^(s-1/2) Gamma((1-s)/2) / Gamma(s/2).

    This is the gamma-RATIO form of the completed factor. It is used here
    rather than the sin*Gamma form 2^s pi^(s-1) sin(pi s / 2) Gamma(1-s)
    that the corpus uses, because the corpus form is a 0 * infinity product at
    every even positive integer and raises outright on a Gamma pole - see
    gate7. The two forms are equal wherever both are defined.
    """
    s = mp.mpc(s)
    return (mp.power(mp.pi, s - mp.mpf("0.5")) * mp.gamma((1 - s) / 2)
            / mp.gamma(s / 2))


def chi_sin_gamma(s):
    """The corpus form: 2^s pi^(s-1) sin(pi s / 2) Gamma(1-s). Pole-prone."""
    s = mp.mpc(s)
    return (2 ** s) * mp.power(mp.pi, s - 1) * mp.sin(mp.pi * s / 2) * mp.gamma(1 - s)


def g(s):
    """The 0/0 the paper studies: |zeta(s)| / |zeta(1-s)|."""
    return abs(mp.zeta(s)) / abs(mp.zeta(1 - s))


def dlog_dsigma(t, sig=mp.mpf("0.5")):
    """Analytic d/dsigma log|chi(sigma+it)| at sigma.

    log|chi| = (sigma-1/2) log pi + Re log Gamma((1-s)/2) - Re log Gamma(s/2)
    and each log Gamma carries a 1/2 from the chain rule (the arguments move
    at rate 1/2 in sigma), so
        d/dsigma log|chi| = log pi - (1/2) Re psi((1-s)/2) - (1/2) Re psi(s/2)
    At sigma = 1/2 the two arguments are conjugates, so the two Re psi terms
    coincide and this collapses to log pi - Re psi(1/4 + i t/2).
    """
    return (mp.log(mp.pi) - mp.re(mp.digamma((1 - mp.mpc(sig, t)) / 2)) / 2
            - mp.re(mp.digamma(mp.mpc(sig, t) / 2)) / 2)


def gate1_identity_about_the_line():
    """|chi(1/2+iy)| = 1 for arbitrary y, including where zeta is NOT zero."""
    pts = [0.0, 0.5, 1.0, 2.0, 5.0, 7.0, 11.0, 20.0, 30.0, 100.0, 1000.0]
    rows = []
    for y in pts:
        s = mp.mpc(0.5, y)
        rows.append({
            "y": float(y),
            "abs_chi": mp.nstr(abs(chi(s)), 25),
            "dev_from_1": mp.nstr(abs(abs(chi(s)) - 1), 5),
            "abs_zeta": mp.nstr(abs(mp.zeta(s)), 8),
            "zeta_is_zero": bool(abs(mp.zeta(s)) < mp.mpf("1e-20")),
        })
    worst = max(float(r["dev_from_1"]) for r in rows)
    non_zero_pts = [r for r in rows if not r["zeta_is_zero"]]
    return {
        "name": "|chi(1/2+iy)| = 1 for arbitrary y, zeta != 0 there",
        "points": rows,
        "n_points": len(rows),
        "n_with_zeta_nonzero": len(non_zero_pts),
        "worst_deviation_from_1": mp.nstr(worst, 5),
        "pass": bool(mp.mpf(worst) < TOL and len(non_zero_pts) == len(rows)),
        "reading": "the identity holds off the zeros too, so it is a property "
                   "of the LINE and says nothing about being a zero",
    }


def gate2_indistinguishability(n=10):
    """A zero and a NON-zero at the same height give the same |chi|.

    This is the falsification gate. If the two agree to far below the
    off-line separation, the corpus's 'verification' cannot tell a zero from
    a non-zero and therefore has no power to decide RH.
    """
    rows = []
    worst = mp.mpf(0)
    for k in range(1, n + 1):
        rho = mp.zetazero(k)
        gamma = mp.im(rho)
        impostor = mp.mpc(0.5, gamma + mp.mpf("0.5"))  # same Re, NOT a zero
        a = abs(chi(rho))
        b = abs(chi(impostor))
        d = abs(a - b)
        worst = max(worst, d)
        rows.append({
            "n": k,
            "gamma": mp.nstr(gamma, 18),
            "abs_chi_at_zero": mp.nstr(a, 25),
            "abs_chi_at_nonzero": mp.nstr(b, 25),
            "difference": mp.nstr(d, 5),
            "impostor_abs_zeta": mp.nstr(abs(mp.zeta(impostor)), 8),
        })
    return {
        "name": "zero vs non-zero at the same height are indistinguishable",
        "rows": rows,
        "worst_difference": mp.nstr(worst, 5),
        "pass": bool(worst < TOL),
        "reading": "the bridge cannot distinguish a zero from a non-zero on "
                   "the same vertical line - zero discriminating power",
    }


def _log_abs_chi(sig, t):
    """log|chi(sigma+it)| - a far better conditioned function to hunt roots of
    than |chi| - 1, which overflows for t above ~100."""
    return mp.log(abs(chi(mp.mpc(sig, t))))


def _bisect(f, a, b, tol=mp.mpf("1e-25"), iters=160):
    fa = f(a)
    for _ in range(iters):
        m = (a + b) / 2
        if (b - a) / 2 < tol:
            return m
        fm = f(m)
        if fm == 0:
            return m
        if (fa < 0) == (fm < 0):
            a, fa = m, fm
        else:
            b = m
    return (a + b) / 2


def _roots_on_sigma_line(t, lo=mp.mpf("-60.25"), hi=mp.mpf("60.25"),
                         step=mp.mpf("0.5"), seed_line=True):
    """All sigma on the real axis with |chi(sigma+it)| = 1, by bracketing.

    The grid is offset by a quarter step so that no probe lands exactly on
    sigma = 1/2. That matters: sigma = 1/2 is always a root with f = 0 there,
    and a strict sign-change test (fa*fb < 0) can never report a root that
    sits on a probe. The line is therefore seeded explicitly, which also
    covers t = t* where it is a DOUBLE root and f does not change sign.
    """
    roots = []
    if seed_line:
        roots.append(mp.mpf("0.5"))
    a = lo
    fa = _log_abs_chi(a, t)
    while a < hi:
        b = min(a + step, hi)
        fb = _log_abs_chi(b, t)
        if fa * fb < 0:
            r = _bisect(lambda x: _log_abs_chi(x, t), a, b)
            if all(abs(r - q) > mp.mpf("1e-6") for q in roots):
                roots.append(r)
        a, fa = b, fb
    roots.sort()
    return roots


def gate3_level_set_structure():
    """The level set of |chi(.|+it)| is NOT {1/2} globally - measure the truth.

    The corpus's Step 4 asserts the *global* claim and justifies it with a
    false monotonicity lemma. The measured truth is finer and this gate
    records all three parts of it:

      (i)   sigma = 1/2 is always a solution, by Schwarz reflection.
      (ii)  For t < t* there are TWO further solutions, symmetric about 1/2,
            at 0.5 +- d(t); d(t) shrinks to 0 as t rises to t*, where the
            line becomes a DOUBLE root (f'(1/2) = 0). For t > t* only the line
            survives. Symmetry is forced: |chi(1-s)| = 1/|chi(s)|, so
            f(1-sigma) = -f(sigma).
      (iii) ALL extra solutions lie outside the open critical strip 0<sigma<1
            (they are at 0.5 +- d with d > 0.5 there), so WITHIN the strip
            the line is the unique solution. This is the only part that bears
            on RH, since every nontrivial zero has 0 < Re(rho) < 1.

    So the global claim is false, the strip claim (the one that matters) is
    true, and the corpus reached the right conclusion by a wrong route.
    """
    t_star = mp.findroot(lambda x: dlog_dsigma(x), (6.0, 7.0))
    ts = ["0.1", "0.5", "1.0", "2.0", "5.0", "6.0", "6.28", "6.5", "7.0",
          "14.134725", "100.0", "1000.0"]
    rows, n_ok, extras_all_outside = [], 0, True
    worst_strip_margin = mp.mpf(0)
    for ts_ in ts:
        t = mp.mpf(ts_)
        rts = _roots_on_sigma_line(t)
        rts.sort()
        extras = [r for r in rts if abs(r - mp.mpf("0.5")) > mp.mpf("1e-6")]
        expected = 3 if t < t_star else 1
        ok = len(rts) == expected and any(abs(r - mp.mpf("0.5")) < mp.mpf("1e-6")
                                          for r in rts)
        n_ok += int(ok)
        for e in extras:
            if mp.mpf(0) < e < mp.mpf(1):
                extras_all_outside = False
        # strip uniqueness: sign of log|chi| constant on each half of (0,1)
        left = [_log_abs_chi(mp.mpf(i) / 2000, t) for i in range(1, 1000)]
        right = [_log_abs_chi(1 - mp.mpf(i) / 2000, t) for i in range(1, 1000)]
        left_ok, right_ok = max(left) < 0, min(right) > 0
        left_ok2, right_ok2 = min(left) > 0, max(right) < 0
        worst_strip_margin = max(worst_strip_margin,
                                 min(abs(max(left)), abs(min(right))))
        rows.append({
            "t": mp.nstr(t, 12),
            "n_roots": len(rts),
            "expected_n_roots": expected,
            "roots": [mp.nstr(r, 14) for r in rts],
            "abs_log_chi_at_line": mp.nstr(abs(_log_abs_chi(mp.mpf("0.5"), t)), 5),
            "extras_offset_d": [mp.nstr(abs(r - mp.mpf("0.5")), 12) for r in extras],
            "matches_expected": bool(ok),
            "strip_has_no_other_zero": bool((left_ok and right_ok)
                                             or (left_ok2 and right_ok2)),
        })
    d_samples = []
    for ts_ in ["1.0", "5.0", "6.0", "6.2", "6.28", "6.35", "7.0"]:
        t = mp.mpf(ts_)
        ex = [abs(r - mp.mpf("0.5")) for r in _roots_on_sigma_line(t)
              if abs(r - mp.mpf("0.5")) > mp.mpf("1e-6")]
        d_samples.append({"t": mp.nstr(t, 10),
                          "d": mp.nstr(max(ex), 12) if ex else "0 (annihilated)"})
    return {
        "name": "level set has 3 solutions for t < t*, 1 for t > t*; extras lie "
                "outside the critical strip",
        "t_star": mp.nstr(t_star, 20),
        "n_tested": len(ts),
        "n_matching_expected": n_ok,
        "rows": rows,
        "d_samples": d_samples,
        "all_extras_outside_strip": extras_all_outside,
        "worst_strip_margin": mp.nstr(worst_strip_margin, 5),
        "pass": bool(n_ok == len(ts) and extras_all_outside),
        "reading": "the GLOBAL claim {sigma : |chi|=1} = {1/2} is FALSE - "
                   "there are two extra roots at 0.5 +- d(t) for t < t*, "
                   "annihilating at t*; but every extra root lies outside the "
                   "critical strip, so the line is the unique solution on "
                   "0<sigma<1, which is the only part RH uses",
    }


def gate4_monotonicity_is_false():
    """Refutes the paper's 'strictly monotone in sigma for fixed t'.

    log|Gamma| is convex on vertical lines, not monotone, and the derivative
    of log|chi| at the line CHANGES SIGN at a finite t*, so sigma = 1/2 is
    approached from below for large t and from above for small t. No single
    monotonicity statement covers both branches.
    """
    samples = []
    for t in [0.5, 1.0, 5.0, 6.0, 7.0, 10.0, 100.0, 1000.0]:
        d = dlog_dsigma(mp.mpf(t))
        samples.append({"t": float(t), "dlog_dsigma_at_half": mp.nstr(d, 12),
                        "direction": "increasing" if d > 0 else "decreasing"})
    t_star = mp.findroot(lambda x: dlog_dsigma(x), (6.0, 7.0))
    n_pos = sum(1 for s in samples if s["direction"] == "increasing")
    return {
        "name": "d/dsigma log|chi| flips sign - not strictly monotone",
        "samples": samples,
        "t_star": mp.nstr(t_star, 20),
        "two_pi": mp.nstr(2 * mp.pi, 20),
        "t_star_minus_2pi": mp.nstr(t_star - 2 * mp.pi, 8),
        "n_increasing": n_pos,
        "n_decreasing": len(samples) - n_pos,
        "pass": bool(n_pos > 0 and n_pos < len(samples)),
        "reading": "the sign flip is real and t* is close to but not equal to "
                   "2*pi (Stirling is only leading order), so the stated "
                   "monotonicity justification is false",
    }


def gate5_chi_is_unbounded_on_a_vertical_line():
    """Refutes 'the gamma ratio does not compensate' (implies |chi| <= 1).

    |chi| is unbounded above on every vertical line. The correct statement is
    a LEVEL-SET statement, not a bound: sigma = 1/2 is the unique solution of
    |chi(sigma+it)| = 1, while |chi| exceeds 1 on one side or the other.
    """
    rows = []
    worst = mp.mpf(0)
    for t in [0.5, 5.0, 20.0, 100.0, 700.0]:
        best_m, best_s = mp.mpf(0), None
        for b in range(-400, 801):
            sig = mp.mpf(b) / 20
            m = abs(chi(mp.mpc(sig, t)))
            if m > best_m:
                best_m, best_s = m, sig
        worst = max(worst, best_m)
        rows.append({"t": float(t), "max_abs_chi": mp.nstr(best_m, 10),
                     "argmax_sigma": mp.nstr(best_s, 6)})
    return {
        "name": "|chi| is unbounded on a vertical line (no |chi| <= 1 bound)",
        "rows": rows,
        "worst_max_abs_chi": mp.nstr(worst, 10),
        "exceeds_one_everywhere": bool(worst > 1),
        "pass": bool(worst > 1),
        "reading": "|chi| > 1 away from the line, so the gamma ratio does "
                   "compensate in the sense the paper denies; the equivalence "
                   "survives only as a level-set statement",
    }


def gate6_g_is_not_identically_one():
    """Refutes the abstract's 'g is identically 1 after removal'.

    By the functional equation g(s) = |chi(s)| identically, so g = 1 exactly
    on the line and nowhere else.
    """
    pts = [mp.mpf(2), mp.mpf(4), mp.mpf(-1), mp.mpc(0.5, 2), mp.mpc(2, 1),
           mp.mpc(0.3, 7.0), mp.mpc(-0.5, 1.0), mp.mpc(0.5, 7.0)]
    rows = []
    identity_holds = True
    n_not_one = 0
    for s in pts:
        gv, cv = g(s), abs(chi(s))
        if abs(gv - cv) > TOL:
            identity_holds = False
        one = abs(gv - 1) < TOL
        if not one:
            n_not_one += 1
        rows.append({
            "s": mp.nstr(s, 8),
            "g": mp.nstr(gv, 20),
            "abs_chi": mp.nstr(cv, 20),
            "g_equals_chi": bool(abs(gv - cv) < TOL),
            "g_equals_1": one,
        })
    return {
        "name": "g(s) = |chi(s)| identically, but g is NOT identically 1",
        "rows": rows,
        "g_equals_chi_identically": identity_holds,
        "n_points_where_g_ne_1": n_not_one,
        "n_points": len(pts),
        "pass": bool(identity_holds and n_not_one > 0),
        "reading": "g carries no information beyond chi (it IS chi), and it "
                   "equals 1 only on the line, so 'g identically 1' is false",
    }


def teeth():
    """Two-sided demonstration that the instrument can and cannot fail.

    NO TEETH: the corpus's own check - |chi(rho)| = 1 at 'zeros' - passes for
    a point that is not a zero, so it cannot fail.
    HAS TEETH: the level-set check - |chi(sigma+it)| = 1 forces sigma = 1/2 -
    does fail when sigma is displaced, so the equivalence is testable. The
    corpus simply never used the half of chi that has teeth.
    """
    rho = mp.zetazero(1)
    gamma = mp.im(rho)
    impostor = mp.mpc(0.5, gamma + mp.mpf("0.5"))
    no_teeth = {
        "check": "|chi(s)| = 1 at the corpus's 'zeros'",
        "planted_input": "a NON-zero point 1/2 + i(gamma + 0.5)",
        "zeta_there": mp.nstr(abs(mp.zeta(impostor)), 8),
        "abs_chi_there": mp.nstr(abs(chi(impostor)), 25),
        "still_passes_1e-25": bool(abs(abs(chi(impostor)) - 1) < TOL),
        "verdict": "CANNOT FAIL - passes on a non-zero, so it certifies nothing",
    }
    has_teeth = []
    for eps in [mp.mpf("1e-1"), mp.mpf("1e-2"), mp.mpf("1e-3"), mp.mpf("1e-6")]:
        s = mp.mpc(0.5 + eps, gamma)
        v = abs(chi(s))
        has_teeth.append({
            "sigma_displacement": mp.nstr(eps, 3),
            "abs_chi": mp.nstr(v, 20),
            "fails_1e-25": bool(abs(v - 1) > TOL),
        })
    return {
        "no_teeth": no_teeth,
        "has_teeth": has_teeth,
        "all_displacements_caught": bool(all(h["fails_1e-25"] for h in has_teeth)),
        "reading": "the level-set half of chi discriminates and the zero-half "
                   "does not; the corpus ran only the blind half",
    }


def gate7_corpus_form_is_singular():
    """The corpus's chi() raises on a Gamma pole at every even positive int.

    bridge.py, rh_conductor_ratio.py and the rest evaluate
    2^s pi^(s-1) sin(pi s / 2) Gamma(1-s). At s = 2, 4, 6, ... this is
    sin(pi s / 2) = 0 against a Gamma pole, so it raises "gamma function
    pole" even though chi is finite there (|chi(2)| = 2 pi^2). The
    gamma-ratio form used in this file is regular. Both forms agree wherever
    both are defined, so this is a robustness defect, not a wrong formula.
    """
    agree, worst = 0, mp.mpf(0)
    for re_s, im_s in [(0.5, 7.3), (0.3, 2.0), (0.7, 11.0), (0.25, 4.0),
                       (0.9, 1.0), (0.5, 100.0)]:
        s = mp.mpc(re_s, im_s)
        d = abs(chi(s) - chi_sin_gamma(s))
        worst = max(worst, d)
        agree += int(d < TOL)
    singular = []
    for k in range(1, 5):
        s = mp.mpf(2 * k)
        try:
            chi_sin_gamma(s)
            singular.append({"s": float(s), "raised": False})
        except ValueError:
            finite = abs(chi(s))
            singular.append({"s": float(s), "raised": True,
                             "chi_is_finite": mp.nstr(finite, 12)})
    return {
        "name": "corpus sin*Gamma form is singular where chi is finite",
        "n_forms_compared": 6,
        "n_agree": agree,
        "worst_form_difference": mp.nstr(worst, 5),
        "even_integers": singular,
        "all_raised": bool(all(r["raised"] for r in singular)),
        "pass": bool(agree == 6 and all(r["raised"] for r in singular)),
        "reading": "the two forms are identical as functions, but the corpus "
                   "form cannot be evaluated at s = 2, 4, 6, ... where chi is "
                   "perfectly finite (|chi(2)| = 2 pi^2); a robustness defect",
    }


def main():
    gates = [
        gate1_identity_about_the_line(),
        gate2_indistinguishability(),
        gate3_level_set_structure(),
        gate4_monotonicity_is_false(),
        gate5_chi_is_unbounded_on_a_vertical_line(),
        gate6_g_is_not_identically_one(),
        gate7_corpus_form_is_singular(),
    ]
    t = teeth()

    print("=" * 74)
    print("CHI(RHO) BRIDGE - DOES THE 'VERIFICATION' TEST ANYTHING ABOUT RH?")
    print("=" * 74)
    npass = 0
    for gdat in gates:
        ok = gdat["pass"]
        npass += bool(ok)
        print()
        print("[%s] %s" % ("PASS" if ok else "FAIL", gdat["name"]))
        print("       %s" % gdat["reading"])

    print()
    print("=" * 74)
    print("TEETH")
    print("=" * 74)
    nt = t["no_teeth"]
    print("  NO TEETH  : %s" % nt["verdict"])
    print("              planted a non-zero where |chi| = %s" % nt["abs_chi_there"])
    print("  HAS TEETH : level set catches every displacement: %s"
          % t["all_displacements_caught"])
    for h in t["has_teeth"]:
        print("              sigma = 1/2 %-8s -> |chi| = %-22s fails? %s"
              % (h["sigma_displacement"], h["abs_chi"], h["fails_1e-25"]))

    print()
    print("=" * 74)
    print("VERDICT")
    print("=" * 74)
    print("  Gates: %d/%d PASS" % (npass, len(gates)))
    print()
    print("  A. removable value of g at rho is |chi(rho)|      TRUE (exact)")
    print("  B. |chi| = 1  <=>  sigma = 1/2  on 0 < sigma < 1    TRUE (exact)")
    print("     globally there are 2 extra roots below t*      FALSE as stated")
    print("  C. therefore RH is verified by this              VACUOUS")
    print()
    print("  The retraction is of C only. A stands; B stands where it is")
    print("  actually used (the strip), and its global form is corrected")
    print("  here rather than repeated.")

    data = {
        "question": "does the Chi(rho) bridge test the Riemann Hypothesis?",
        "verdict": "A and B are TRUE; C (the certification) is VACUOUS",
        "gates": gates,
        "gates_passed": npass,
        "gates_total": len(gates),
        "teeth": t,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print()
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
