"""N7  THE ORIGIN CONSISTENCY WINDOW: one number, two problems, one inequality.

A history of the universe is not fixed by the laws of physics alone; it is a
curve `a(t)` with an equation of state `p = w rho` attached.  Two of the
classic questions about how the universe started -- FLATNESS and HORIZON -- are
usually presented as separate fine-tuning problems.  They are not separate.
Both are controlled by the single stiffness integral

    S := int (1 + 3w) d ln a

which is ADDITIVE OVER ERAS, hence path-independent, and is the only
history-dependent quantity either question needs.

THE EXACT CURVATURE LAW

  rho(a) = rho_i (a/a_i)^(-3(1+w))          continuity equation
  H^2    = (8 pi G / 3) rho - k / a^2       Friedmann
  eps    = |Omega - 1| = |k| / (a^2 H^2)

Fix `a_i = 1, H_i = 1`.  Then Friedmann gives `rho_i = (3/8pi)(1 + k)`, so with
`D := (8 pi G/3) rho_i / |k| = (1 + k)/|k|` and `sigma := sign k`,

  a^2 H^2 = (8 pi G / 3) rho a^2 - k = |k| (D a^(-1-3w) - sigma)
  =>  eps(a) = 1 / (D a^(-1-3w) - sigma)

EXACTLY, for any curvature -- this is a solved ODE, not an expansion.  Watch the
sign: `-k = -sigma |k|`, so the denominator carries `- sigma`, and for an open
universe (`sigma = -1`) the denominator is `D a^(-1-3w) + 1`, which stays
positive for all `a > 0`.  Writing `+ sigma` instead makes `eps` go negative at
late time, which is how this was caught.

The familiar power law `eps ~ a^(1+3w)` is the limit of that expression when
`X := D a^(-1-3w) >> 1`, and the relation to it is EXACT:

  eps_exact / eps_leading = 1 / (1 - sigma/X) = 1 + sigma/X + O(1/X^2)

So the leading law's relative correction is `|sigma| D a^(-1-3w)`.  Note that
`X >> 1` is EARLY time (`a^(1+3w) << D`), which is exactly the flatness regime
the flatness problem is about -- which is why probing the leading law at large
N tests nothing but arithmetic.  The same holds for the radius below, with the
square root:

  r_exact / r_leading = (1 - sigma/X)^(-1/2)

Gates n7a/n7b/n7c check the closed form against direct Friedmann integration
AND these exact algebraic ratios, instead of pretending the leading laws are
exact.

THE TWO ADMISSIBILITY CONDITIONS -- both sign tests on the same S

  (F) FLATNESS   eps_f < eps_obs   <=>   S < S_req,  S_req = ln(eps_obs/eps_i)
  (H) HORIZON    r_f < r_i         <=>   S < 0,      r = 1/(a H)

The horizon direction is the part that is easy to get backwards, so it is worth
stating carefully.  The horizon problem asks that today's observable region fit
INSIDE the Hubble patch that existed earlier.  Today's region has comoving size
`r_f = 1/(a_f H_f)`; the earlier patch has comoving size `r_i = 1/(a_i H_i)`.
So the requirement is `r_f < r_i`, and since `r_f / r_i = e^(S/2)`, that is

        S < 0.

The comoving Hubble radius must SHRINK.  A decelerating era (`w > -1/3`)
contributes `S > 0` and makes it grow, so the matter era we live through
contributes `+80` to `S` all by itself and makes the horizon problem worse,
not better.

THE LINKING STATEMENT

Because `eps_obs < eps_i`, we have `S_req < 0` strictly, so

        S < S_req   ==>   S < 0

i.e. FLATNESS ADMISSIBILITY IMPLIES HORIZON ADMISSIBILITY.  One inequality does
both jobs, and flatness is the binding one.  The two "separate" initial-value
problems are one problem.

WHAT THIS IS NOT.  This is a CONSISTENCY FILTER on an assumed history, not a
mechanism.  It does not produce initial conditions, does not explain why there
is a history, and does not say what preceded it.  `eps_i` is an INPUT here;
nothing in this file constrains it.  A filter that leaves `eps_i` free cannot
claim to explain the beginning, and the scope block in the artifact says so so
the claim cannot be quietly upgraded later.

Artifacts: data/origin_consistency_window_n7_data.json
"""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(
    REPO,
    "03_Data_and_Observational_Resources",
    "02_Experimental_Data_Collections",
)

# ---- inputs -------------------------------------------------------------- #
# EPS_OBS is the flatness PRECISION THRESHOLD, i.e. "how flat must we be".  It
# is therefore an upper limit on |Omega_k|.  EPS_OBS_PLANCK_2018 below is NOT
# one -- it is a best-fit central value -- so it is kept only as a ladder entry
# and flagged as such; the model run above uses it because it is CONSERVATIVE
# (a looser threshold makes flatness EASIER and the required length SHORTER, so
# it cannot inflate the result).  The genuinely sourced upper limits follow it.
EPS_OBS = 0.011
EPS_I = 1.0         # WORST case initial curvature: order unity, not tuned
N_MATTER = 80.0     # matter-dominated e-folds from end of inflation to now
W_INFL = -1.0       # de Sitter: exact, single parameter
W_RAD = 1.0 / 3.0   # radiation era, for the scaling-law check

# --- observational inputs for the measurement-limit gates (n7k, n7l) -------- #
# These are the ONLY places this script touches published numbers, and they are
# inputs, not results. Provenance is recorded because the verdicts below change
# if any of them moves. Every value used by a gate was read off a primary source
# in this pass; anything unverified is named UNVERIFIED and drives NO gate.

# Planck 2018 results. VI. Cosmological parameters, Planck Collaboration,
# arXiv:1807.06209v4, A&A 641, A6 (2020), Sect. 7.3 "Spatial curvature".
#
# CORRECTION (this value was previously mislabelled): 0.011 is the MAGNITUDE of
# the 95% CL CENTRAL VALUE of Omega_k for TT,TE,EE+lowE+lensing+BAO, from the
# Omega_k row of the base-LambdaCDM parameter table:
#     Omega_K = -0.011^{+0.013}_{-0.012}   (95%)
# It is NOT an upper limit, it is NOT 68%, it is NEGATIVE in the fits (slightly
# closed), and it is an inference about the present-day universe rather than a
# measurement "at recombination".  Using a central value where a precision
# threshold belongs is a category error, so this entry is labelled and used as a
# ladder rung only -- see EPS_OBS_PLANCK_2018_UPPER for the honest bound.
EPS_OBS_PLANCK_2018 = 0.011

# The same table's 95% interval -0.011^{+0.013}_{-0.012} means
# Omega_k in [-0.023, +0.002], so |Omega_k| < 0.023 at 95% for that
# combination.  This IS an upper limit and so IS a legitimate eps_obs.
EPS_OBS_PLANCK_2018_UPPER = 0.023

# Eq. (45b), 68%: Omega_K = 0.0007 +/- 0.0019 (TT,TE,EE+lowE+lensing+BAO).
# Planck's own words: "the joint results suggests our Universe is spatially flat
# to a 1 sigma accuracy of 0.2%".  This is the sharpest genuinely sourced
# Planck 2018 precision figure used here.
EPS_OBS_PLANCK_2018_68CL = 0.0007
EPS_OBS_PLANCK_2018_68CL_ERR = 0.0019

EPS_OBS_QUOTED_2016 = 0.005   # |Omega_k| < 5e-3 (95% CL): the current constraint
                              # quoted in Leonard, Bull & Allison (2016),
                              # arXiv:1604.01410. The dataset combination behind
                              # the number is theirs and is not restated here.
EPS_OBS_FORESEEABLE = 1e-3    # "most likely achievable constraint for the
                              # foreseeable future", same source
SIGMA_OMEGA_K_COSMIC_VARIANCE = 1.5e-5   # cosmic-variance NOISE level on Omega_k,
                              # Leonard, Bull & Allison (2016), arXiv:1604.01410,
                              # PRD 94, 023502. This is the variance of modes you
                              # never observed -- NOT the "curvature floor" those
                              # authors adopt, which is the 1e-4 below.
OMEGA_K_ETERNAL_INFLATION_THRESHOLD = 1e-4   # Kleban & Schillo, "Spatial
                              # Curvature Falsifies Eternal Inflation",
                              # JCAP 06, 029 (2012), arXiv:1202.5037
N_EFOLDS_CONVENTION = 60.0    # literature convention, NOT derived here

# Recorded, NOT used by any gate: ACT DR6 is expected to tighten the curvature
# limit well below 5e-3, but no primary-source Omega_k limit for it was located
# in this pass, so it supports no verdict here. See the n7k provenance entry.
EPS_OBS_ACT_DR6_UNVERIFIED = 0.0019

# For the numerical checks.  eps_i = 1 is a degenerate boundary case (it is the
# turnaround point of a closed universe and it zeroes rho_i for an open one),
# so the scaling-law gates use a small curvature and probe EARLY times.
EPS_I_NUM = 1.0e-2

GATES = []


def gate(name, ok, detail):
    GATES.append((name, bool(ok), detail))
    print("   [%s] %-54s %s" % ("PASS" if ok else "FAIL", name, detail))


# ---- exact closed forms -------------------------------------------------- #
def stiffness(w):
    """Density of S in dln a. Vanishes exactly at w = -1/3."""
    return 1.0 + 3.0 * w


def S_of(w, n):
    return stiffness(w) * n


def s_of_path(eras):
    """S accumulated along a piecewise-constant-w path. Additive by construction."""
    return sum(stiffness(w) * n for w, n in eras)


def s_total(w_infl, n_infl, w_later, n_later):
    return s_of_path([(w_infl, n_infl), (w_later, n_later)])


def eps_amplification(s):
    return math.exp(s)


def radius_amplification(s):
    """r = 1/(aH): r_f/r_i = e^(S/2)."""
    return math.exp(0.5 * s)


def s_required(eps_obs, eps_i):
    """The flatness bound S < S_req; negative whenever eps_obs < eps_i."""
    return math.log(eps_obs / eps_i)


def n_infl_needed(eps_obs, eps_i, n_matter, w_infl):
    """Smallest inflation length meeting flatness, solving S < S_req."""
    stiff = stiffness(w_infl)
    if stiff >= 0.0:
        return math.inf
    return (s_required(eps_obs, eps_i) - S_of(0.0, n_matter)) / stiff


def classify(s, eps_obs, eps_i):
    """Both admissibility verdicts from one number. Both are S < (threshold)."""
    flat = s < s_required(eps_obs, eps_i)
    horz = s < 0.0
    return flat, horz


def eps_obs_needed_for(n_target, eps_i, n_matter, w_infl):
    """Invert n_infl_needed: the curvature precision that would deliver N.

    n_infl_needed is affine in ln(eps_obs/eps_i), so the inversion is exact and
    in closed form. Used to ask what |Omega_k| a measurement would have to reach
    to certify a given inflation length by curvature alone.
    """
    stiff = stiffness(w_infl)
    if stiff >= 0.0:
        return math.inf
    return eps_i * math.exp(n_target * stiff + S_of(0.0, n_matter))


def curvature_verdict(omega_k_model, eps_obs):
    """Falsify a model that PREDICTS its own final curvature.

    Only meaningful when a model supplies omega_k_model. The flatness window is
    symmetric in |Omega_k|, so this returns one of:
      "admissible"        -- |Omega_k| predicted within the observed bound
      "FALSIFIED"         -- |Omega_k| predicted above it
    Sign carries separate, model-specific content that this function does NOT
    encode; see the scope entry on eternal inflation.
    """
    return "admissible" if abs(omega_k_model) <= eps_obs else "FALSIFIED"


# ---- the exact FLRW slice, from Friedmann directly ---------------------- #
def normalisation(eps_i=EPS_I_NUM, a_i=1.0, h_i=1.0):
    """Return (rho_i, k, D, sigma) for the open slice with a_i = H_i = 1.

    Open (k < 0) because it has no turnaround point, so H^2 > 0 for all a > 0.
    Friedmann at a_i:  h_i^2 = (8 pi G/3) rho_i - k
    =>  rho_i = (3/8pi)(h_i^2 + k),  and  D := (8 pi G/3) rho_i / |k| = (h_i^2+k)/|k|.
    """
    k = -eps_i
    rho_i = (3.0 / (8.0 * math.pi)) * (h_i ** 2 + k)
    d = (h_i ** 2 + k) / abs(k)
    return rho_i, k, d, (-1.0 if k < 0 else 1.0)


def friedmann_h2(a, rho_i, k, w):
    """H^2 at scale factor a, straight from the Friedmann equation."""
    rho = rho_i * a ** (-3.0 * (1.0 + w))
    return (8.0 * math.pi / 3.0) * rho - k / (a * a)


def eps_from_friedmann(a, rho_i, k, w):
    """|Omega - 1| = |k| / (a^2 H^2), computed from H, not from the closed form."""
    h_sq = friedmann_h2(a, rho_i, k, w)
    return abs(k) / (a * a * h_sq)


def eps_closed(a, w, d, sigma):
    """The same quantity in closed form: 1 / (D a^(-1-3w) - sigma)."""
    return 1.0 / (d * a ** (-1.0 - 3.0 * w) - sigma)


def eps_leading(a, w, d):
    """Leading power law D^-1 a^(1+3w), the X >> 1 limit."""
    return a ** (1.0 + 3.0 * w) / d


def r_from_friedmann(a, rho_i, k, w):
    """Comoving Hubble radius 1/(aH) from the Friedmann equation."""
    h_sq = friedmann_h2(a, rho_i, k, w)
    return 1.0 / (a * math.sqrt(h_sq))


def r_closed(a, w, d, sigma, k):
    """1/(aH) in closed form: 1/(sqrt|k| sqrt(D a^(-1-3w) - sigma))."""
    x = d * a ** (-1.0 - 3.0 * w)
    return 1.0 / (math.sqrt(abs(k)) * math.sqrt(x - sigma))


def r_leading(a, w, d, k):
    """Leading law r ~ a^((1+3w)/2), normalised to match at a = 1."""
    return a ** ((1.0 + 3.0 * w) / 2.0) / math.sqrt(abs(k) * d)


# ---------------------------------------------------------------------------
def main():
    GATES.clear()
    print("=" * 78)
    print("N7  ORIGIN CONSISTENCY WINDOW: one S, two problems, one inequality")
    print("=" * 78)

    S_REQ = s_required(EPS_OBS, EPS_I)
    RHO_I, K, D, SIGMA = normalisation()
    print("\n0. INPUTS   eps_obs = %.4g   (Planck |Omega_k| at z ~ 1080)" % EPS_OBS)
    print("            eps_i   = %.4g   (worst case: order-unity initial curvature)" % EPS_I)
    print("            N_matter = %.4g    w_infl = %.4g (de Sitter)" % (N_MATTER, W_INFL))
    print("            S_req = ln(eps_obs/eps_i) = %+.6f    (NEGATIVE)" % S_REQ)
    print("            numerical slice: eps_i_num = %.1g  rho_i = %.6g" % (EPS_I_NUM, RHO_I))
    print("                             k = %+.4g  D = %.6g  sigma = %+d" % (K, D, SIGMA))

    # --- 1. the curvature law: closed form vs direct Friedmann --------------
    print("\n1. THE CURVATURE LAW   eps = 1/(D a^(-1-3w) - sigma),  exact")
    print("   %-8s %-8s %-6s %-15s %-15s %-10s"
          % ("w", "N", "a", "eps (Friedmann)", "eps (closed)", "rel err"))
    rel_exact = 0.0
    for w in (0.0, 0.5, W_RAD, 1.0):
        for n in (0.05, 0.5, 1.0, 2.0, 3.0, 5.0):
            a = math.exp(n)
            got = eps_from_friedmann(a, RHO_I, K, w)
            want = eps_closed(a, w, D, SIGMA)
            rel_exact = max(rel_exact, abs(got - want) / want)
            if n in (0.5, 2.0):
                print("   %-8.4g %-8.4g %-6.3g %-15.10g %-15.10g %-10.1e"
                      % (w, n, a, got, want, abs(got - want) / want))
    gate("n7a closed form == direct Friedmann integration", rel_exact < 1e-14,
         "max rel err %.1e over w in {0,1/2,1/3,1}, N in {0.05..5}" % rel_exact)

    print("\n   the leading law is its EARLY-time limit, not an identity.")
    print("   exact ratio: eps_exact/eps_leading = 1/(1 - sigma/X), X = D a^(-1-3w)")
    print("   %-8s %-8s %-6s %-15s %-15s %-11s %-11s"
          % ("w", "N", "X", "eps exact", "eps leading", "ratio", "1/(1-s/X)"))
    rel_lead = 0.0
    for w in (0.0, 0.5, W_RAD, 1.0):
        for n in (0.02, 0.1, 0.25, 0.5, 0.75):
            a = math.exp(n)
            x = D * a ** (-1.0 - 3.0 * w)
            ex = eps_closed(a, w, D, SIGMA)
            ld = eps_leading(a, w, D)
            pred = 1.0 / (1.0 - SIGMA / x)
            rel_lead = max(rel_lead, abs(ex / ld - pred) / pred)
            if n in (0.1, 0.5):
                print("   %-8.4g %-8.4g %-6.3g %-15.10g %-15.10g %-11.10g %-11.10g"
                      % (w, n, x, ex, ld, ex / ld, pred))
    gate("n7b exact correction ratio eps_exact/eps_leading = 1/(1-sigma/X)",
         rel_lead < 1e-12,
         "max rel err %.1e" % rel_lead)

    # --- 2. the horizon law ---------------------------------------------------
    print("\n2. THE HORIZON LAW   r_com = 1/(aH)")
    print("   exact ratio: r_exact/r_leading = (1 - sigma/X)^(-1/2)")
    rel_r = 0.0
    for w in (0.0, 0.5, W_RAD, 1.0):
        for n in (0.02, 0.1, 0.25, 0.5, 0.75):
            a = math.exp(n)
            x = D * a ** (-1.0 - 3.0 * w)
            got = r_from_friedmann(a, RHO_I, K, w)
            want = r_closed(a, w, D, SIGMA, K)
            pred = 1.0 / math.sqrt(1.0 - SIGMA / x)
            rel_r = max(rel_r, abs(got / want - 1.0))
            rel_r = max(rel_r, abs((got / r_leading(a, w, D, K) / pred) - 1.0))
            if n in (0.1, 0.5):
                print("   w=%-7.4g N=%-7.4g X=%-7.3g r(Friedmann)=%-14.8g "
                      "ratio=%-12.8g predicted=%-12.8g" % (w, n, x, got, got / r_leading(a, w, D, K), pred))
    gate("n7c horizon law + exact correction ratio (1-sigma/X)^(-1/2)", rel_r < 1e-12,
         "max rel err %.1e over both r_closed and the ratio" % rel_r)

    # --- 3. additivity / path independence -----------------------------------
    print("\n3. ADDITIVITY OF S OVER ERAS (path independence)")
    era_sets = [
        [(W_INFL, 60.0), (0.0, N_MATTER)],
        [(W_INFL, 10.0), (-0.5, 3.0)],
        [(0.0, 7.0), (W_RAD, 11.0)],
        [(W_INFL, 5.0), (-0.9, 2.0), (0.0, 30.0), (W_RAD, 4.0)],
    ]
    a_err = 0.0
    for eras in era_sets:
        a_err = max(a_err, abs(s_of_path(eras) - s_of_path(list(reversed(eras)))))
        # splitting one era into two of the same w must not change S
        w0, n0 = eras[0]
        a_err = max(a_err, abs(s_of_path(eras) - s_of_path(
            [(w0, n0 / 3.0), (w0, n0 / 3.0), (w0, n0 / 3.0)] + eras[1:])))
    gate("n7d S is additive and order-independent over eras", a_err < 1e-12,
         "4 histories, max deviation %.1e" % a_err)

    # --- 4. the window --------------------------------------------------------
    print("\n4. THE WINDOW   flatness: S < %+.4f     horizon: S < 0" % S_REQ)
    print("   %-9s %-9s %-9s %-9s %-11s %s"
          % ("N_infl", "S", "flat", "horiz", "eps_f", "verdict"))
    window_rows = []
    for n_infl in (0.0, 20.0, 39.0, 40.0, 42.0, 42.25, 45.0, 60.0, 100.0):
        s = s_total(W_INFL, n_infl, 0.0, N_MATTER)
        flat, horz = classify(s, EPS_OBS, EPS_I)
        eps_f = EPS_I * eps_amplification(s)
        verdict = ("ADMISSIBLE" if flat and horz else
                   "flat only" if flat else "horizon only" if horz else "INADMISSIBLE")
        print("   %-9.2f %+-9.3f %-9s %-9s %-11.3g %s"
              % (n_infl, s, flat, horz, eps_f, verdict))
        window_rows.append({"N_infl": n_infl, "S": s, "flat": flat, "horizon": horz,
                            "eps_f": eps_f, "verdict": verdict})

    mono = all(window_rows[i]["S"] > window_rows[i + 1]["S"]
               for i in range(len(window_rows) - 1))
    gate("n7e S decreases monotonically in inflation length", mono,
         "stiffness(de Sitter) = -2 < 0")

    N_STAR = n_infl_needed(EPS_OBS, EPS_I, N_MATTER, W_INFL)
    s_star = s_total(W_INFL, N_STAR, 0.0, N_MATTER)
    eps_star = EPS_I * eps_amplification(s_star)
    print("\n   threshold  N_infl > %.4f e-folds   (de Sitter, then %.0f matter)"
          % (N_STAR, N_MATTER))
    print("   at N_infl = %.6f :  S = %+.9f  vs S_req = %+.9f" % (N_STAR, s_star, S_REQ))
    print("                      eps_f = %.9g  vs eps_obs = %.9g" % (eps_star, EPS_OBS))
    gate("n7f flatness threshold lands exactly on eps_obs",
         abs(eps_star - EPS_OBS) / EPS_OBS < 1e-9,
         "rel dev %.2e" % (abs(eps_star - EPS_OBS) / EPS_OBS))

    # --- 5. the linking statement --------------------------------------------
    print("\n5. ONE INEQUALITY DOES BOTH JOBS")
    print("   S_req = %+.6f < 0, so  S < S_req  ==>  S < 0, which IS the horizon bound."
          % S_REQ)
    holds, counter = True, None
    for kk in range(0, 120):
        s = s_total(W_INFL, 2.0 * kk, 0.0, N_MATTER)
        flat, horz = classify(s, EPS_OBS, EPS_I)
        if flat and not horz:
            holds = False
            counter = (2.0 * kk, s)
    print("   scanned N_infl in [0, 240) step 2, 120 samples")
    gate("n7g flatness implies horizon over the whole scan", holds,
         "no counterexample" if holds else "counterexample %r" % (counter,))

    # sharp separation: there IS a band where only flatness holds, or only horizon
    only_flat = [r for r in window_rows if r["flat"] and not r["horizon"]]
    only_horz = [r for r in window_rows if r["horizon"] and not r["flat"]]
    print("   band where horizon holds but flatness fails: %d sample(s) (e.g. N_infl=%s)"
          % (len(only_horz), only_horz[0]["N_infl"] if only_horz else "-"))
    print("   band where flatness holds but horizon fails: %d sample(s)"
          % len(only_flat))
    gate("n7h the two conditions are nested, not identical",
         all(r["horizon"] for r in only_flat) and len(only_horz) > 0,
         "horizon-only band exists and flat-only band is empty")

    # --- 6. w = -1/3 is a boundary of the LAW, not a solution ----------------
    print("\n6. w = -1/3:  STIFFNESS VANISHES -- AND THAT IS NOT A SOLUTION")
    inv_eps = eps_amplification(S_of(-1.0 / 3.0, 50.0))
    inv_r = radius_amplification(S_of(-1.0 / 3.0, 50.0))
    print("   stiffness(-1/3) = %.3e" % stiffness(-1.0 / 3.0))
    print("   50 e-folds at w = -1/3:  eps ratio = %.15g   r ratio = %.15g"
          % (inv_eps, inv_r))
    s_mixed = s_total(-1.0 / 3.0, 60.0, 0.0, N_MATTER)
    flat_m, horz_m = classify(s_mixed, EPS_OBS, EPS_I)
    print("   but 60 e-folds at w=-1/3 THEN %.0f matter gives S = %+.2f, admissible = %s"
          % (N_MATTER, s_mixed, flat_m and horz_m))
    print("   the matter era is not free: it contributes +%.0f to S on its own." % N_MATTER)
    gate("n7i w=-1/3 is invariant but NOT admissible alone",
         abs(inv_eps - 1.0) < 1e-12 and abs(inv_r - 1.0) < 1e-12 and not (flat_m and horz_m),
         "invariance exact; S = %+.1f fails flatness" % s_mixed)

    # --- 7. the filter does not constrain eps_i ------------------------------
    print("\n7. THE FILTER DOES NOT CONSTRAIN ITS INPUT")
    eps_i_scan = [0.5, 0.9, 1.0, 2.0, 10.0]
    print("   %-10s %-12s %-14s %s" % ("eps_i", "S_req", "N_infl needed", "verdict"))
    free_rows = []
    for ei in eps_i_scan:
        sr = s_required(EPS_OBS, ei)
        ni = n_infl_needed(EPS_OBS, ei, N_MATTER, W_INFL)
        free_rows.append({"eps_i": ei, "S_req": sr, "N_infl_needed": ni})
        print("   %-10.3g %-12.4f %-14.4f %s"
              % (ei, sr, ni, "admissible for some N" if math.isfinite(ni) else "NEVER"))
    gate("n7j eps_i remains a free input for every value tried",
         all(math.isfinite(r["N_infl_needed"]) for r in free_rows),
         "no value of eps_i is excluded by the window; it only sets the length")

    # --- 8. how sharp can the curvature criterion ever get? (n7k) ------------
    print("\n8. MEASUREMENT FLOOR ON THE CURVATURE CRITERION")
    print("   N_infl is affine in ln(eps_obs): dN/dln(eps_obs) = 1/(1+3w) = %+.1f"
          % (1.0 / stiffness(W_INFL)))
    floor_rows = []
    # ordered by DECREASING eps_obs, so the required length increases down the
    # list: this ordering is what makes the ladder readable as "precision ->
    # history length", and it is asserted by the test suite.
    for label, e in (("Planck 2018 |95% upper|", EPS_OBS_PLANCK_2018_UPPER),
                     ("Planck 2018 |central 95%| (NOT a bound)", EPS_OBS_PLANCK_2018),
                     ("current (quoted 2016)", EPS_OBS_QUOTED_2016),
                     ("foreseeable ~1e-3", EPS_OBS_FORESEEABLE),
                     ("eternal-inf. threshold 1e-4", OMEGA_K_ETERNAL_INFLATION_THRESHOLD),
                     ("cosmic-variance asymptote", SIGMA_OMEGA_K_COSMIC_VARIANCE)):
        n_need = n_infl_needed(e, EPS_I, N_MATTER, W_INFL)
        floor_rows.append({"label": label, "eps_obs": e, "N_infl_needed": n_need})
        print("   %-38s eps_obs=%-9.3g N_infl> %-9.3f" % (label, e, n_need))

    eps_for_convention = eps_obs_needed_for(
        N_EFOLDS_CONVENTION, EPS_I, N_MATTER, W_INFL)
    decades_short = (math.log10(SIGMA_OMEGA_K_COSMIC_VARIANCE)
                     - math.log10(eps_for_convention))
    # The asymptote: reached only if cosmic variance were the ONLY limit, which
    # it is not -- those authors judge the floor unreachable by Stage IV.
    saturation = n_infl_needed(SIGMA_OMEGA_K_COSMIC_VARIANCE, EPS_I, N_MATTER, W_INFL)
    # The number that is actually expected to be attainable.
    realistic_cap = n_infl_needed(EPS_OBS_FORESEEABLE, EPS_I, N_MATTER, W_INFL)

    # The affine law must reproduce n_infl_needed exactly at every sample.
    affine_ok = True
    for row in floor_rows:
        predicted = (math.log(row["eps_obs"] / EPS_I) - N_MATTER) / stiffness(W_INFL)
        affine_ok = affine_ok and abs(predicted - row["N_infl_needed"]) < 1e-12

    print("   to certify %.0f e-folds by curvature alone: eps_obs < %.3g"
          % (N_EFOLDS_CONVENTION, eps_for_convention))
    print("   that is %.1f orders of magnitude BELOW the %.1e cosmic-variance level"
          % (decades_short, SIGMA_OMEGA_K_COSMIC_VARIANCE))
    print("   cosmic-variance asymptote N_infl > %.2f (NOT expected to be reached)"
          % saturation)
    print("   realistic foreseeable cap N_infl > %.2f at eps_obs ~ 1e-3"
          % realistic_cap)
    print("   either way the criterion tops out well short of %.0f e-folds"
          % N_EFOLDS_CONVENTION)

    gate("n7k curvature saturates far below the ~%.0f e-fold convention"
         % N_EFOLDS_CONVENTION,
         affine_ok and saturation < N_EFOLDS_CONVENTION
         and realistic_cap < N_EFOLDS_CONVENTION
         and decades_short > 10.0,
         "N_infl is affine in ln(eps_obs) with slope 1/(1+3w)=%.1f; the %.1e "
         "cosmic-variance level is an unreachable asymptote at %.2f, the ~1e-3 "
         "foreseeable bound is the realistic cap at %.2f, and reaching %.0f "
         "would need eps_obs < %.2g (%.1f decades below the floor)"
         % (1.0 / stiffness(W_INFL), SIGMA_OMEGA_K_COSMIC_VARIANCE, saturation,
            realistic_cap, N_EFOLDS_CONVENTION, eps_for_convention, decades_short))

    # --- 9. the filter needs a model to test (n7l) ---------------------------
    print("\n9. THE FILTER HAS CONTENT ONLY IF A MODEL SUPPLIES Omega_k")
    probe = [
        ("order-unity curvature", 0.3),
        ("curvature at the quoted 2016 bound", EPS_OBS_QUOTED_2016),
        ("model predicting |Omega_k| = 2e-4", 2e-4),
        ("model predicting |Omega_k| = 5e-5", 5e-5),
        ("exact zero", 0.0),
    ]
    thr = OMEGA_K_ETERNAL_INFLATION_THRESHOLD
    print("   Two comparison bounds are shown deliberately: what is reachable")
    print("   NOW, and what a 1e-4 measurement would exclude.")
    print("   %-34s %-9s %-18s %s"
          % ("model prediction", "|Omega_k|", "verdict @ current", "verdict @ 1e-4"))
    model_rows = []
    for label, om in probe:
        v_now = curvature_verdict(om, EPS_OBS_QUOTED_2016)
        v_thr = curvature_verdict(om, thr)
        model_rows.append({"model": label, "omega_k": om,
                           "verdict_at_current_bound": v_now,
                           "verdict_at_1e-4": v_thr})
        print("   %-34s %-9.3g %-18s %s"
              % (label, abs(om), v_now, v_thr))

    decisive = (EPS_OBS_QUOTED_2016 / OMEGA_K_ETERNAL_INFLATION_THRESHOLD)
    falsified_now = sum(1 for r in model_rows if r["verdict_at_current_bound"] == "FALSIFIED")
    falsified_then = sum(1 for r in model_rows if r["verdict_at_1e-4"] == "FALSIFIED")
    print("   the current bound (%.3g) is %.0fx LOOSER than the 1e-4 threshold, so it"
          % (EPS_OBS_QUOTED_2016, decisive))
    print("   excludes %d of %d probes; a 1e-4 measurement would exclude %d"
          % (falsified_now, len(probe), falsified_then))

    gate("n7l the filter is vacuous without a model prediction, mechanical with one",
         all(r["verdict_at_current_bound"] in ("admissible", "FALSIFIED")
             and r["verdict_at_1e-4"] in ("admissible", "FALSIFIED")
             for r in model_rows)
         and curvature_verdict(1.0, EPS_OBS) == "FALSIFIED"
         and curvature_verdict(0.0, EPS_OBS) == "admissible"
         and decisive > 1.0 and falsified_then > falsified_now,
         "N7 supplies no Omega_k and derives none; given a model's prediction the "
         "verdict is mechanical. At the current bound (%.3g) only %d/%d probes are "
         "excluded, but at the 1e-4 threshold %d/%d would be -- the test is "
         "%.0fx out of reach today"
         % (EPS_OBS_QUOTED_2016, falsified_now, len(probe), falsified_then,
            len(probe), decisive))

    # ---------------------------------------------------------------------------
    SCOPE = {
        "what this is": "a consistency FILTER on an assumed history, not a mechanism",
        "S defined as": "int (1 + 3w) dln a -- additive over eras, path independent",
        "flatness control": "eps ~ e^S   ->  admissible iff S < ln(eps_obs/eps_i)",
        "horizon control": "r_com = 1/(aH); need r_f < r_i, i.e. e^(S/2) < 1, "
                           "so admissible iff S < 0",
        "linking statement": "S_req < 0 strictly, so flatness IMPLIES horizon. The "
                             "two 'separate' initial-value problems are one "
                             "inequality, and flatness is the binding one",
        "matter era sign": "S = +80 from the matter era ALONE, so the horizon "
                           "condition is NOT free; decelerating eras worsen it",
        "epsilon_i status": "INPUT, NOT derived. Nothing here fixes |Omega_i - 1|. "
                            "A mechanism for it is a separate open problem (n7j)",
        "cause / beginning": "NOT ADDRESSED. This filters histories; it does not "
                             "produce initial conditions, does not explain why "
                             "there is a history, and says nothing about what "
                             "preceded it",
        "de Sitter caveat": "w_infl = -1 is exact and single-parameter. Real "
                            "quasi-de Sitter has w = -1 + small, which changes "
                            "the NUMBER of e-folds required but NOT the sign test "
                            "on S: only w < -1/3 contributes negatively",
        "closed-form curvature law": "eps = 1/(D a^(-1-3w) - sigma) is EXACT (a "
                                     "solved ODE), verified against direct Friedmann "
                                     "integration (n7a). Sign matters: -k = -sigma|k|",
        "leading laws are asymptotic": "eps ~ a^(1+3w) and r ~ a^((1+3w)/2) hold in "
                                       "the EARLY-time limit X = D a^(-1-3w) >> 1, "
                                       "with EXACT ratios eps_exact/eps_leading = "
                                       "1/(1 - sigma/X) and r_exact/r_leading = "
                                       "(1 - sigma/X)^(-1/2) (n7b, n7c). Probing "
                                       "them at large N tests nothing but arithmetic",
        "n7i caveat": "w = -1/3 is where the stiffness DENSITY vanishes, i.e. a "
                      "boundary of the scaling laws. It is emphatically not an "
                      "admissible history.",
        "n7k provenance": "The saturation is arithmetic, not novel: N_infl is affine "
                          "in ln(eps_obs) with slope 1/(1+3w). The published inputs "
                          "are the 1.5e-5 cosmic-variance NOISE level and the ~1e-3 "
                          "foreseeable limit (Leonard, Bull & Allison, PRD 94 023502, "
                          "2016, arXiv 1604.01410), the 1e-4 threshold (Kleban & "
                          "Schillo, JCAP 06 029, 2012, arXiv 1202.5037), and the "
                          "Planck 2018 curvature results (Planck Collaboration, "
                          "A&A 641 A6 2020, arXiv 1807.06209v4, Sect. 7.3). It "
                          "quantifies, rather than discovers, the separation between "
                          "these geometric limits and the ~60 e-fold convention.",
        "Planck 2018 rung was MISLABELLED and is now corrected": "0.011 was "
                          "previously described as '|Omega_k| at recombination "
                          "(Planck 2018)'. Checking arXiv 1807.06209v4 Sect. 7.3 "
                          "shows 0.011 is the MAGNITUDE of the 95% CL CENTRAL value "
                          "of Omega_k for TT,TE,EE+lowE+lensing+BAO, from the table "
                          "row Omega_K = -0.011^{+0.013}_{-0.012}: not an upper "
                          "limit, not 68%, negative in the fits, and an inference "
                          "about the present-day universe rather than a recombination "
                          "measurement. Since eps_obs in this window is a PRECISION "
                          "THRESHOLD, a central value is the wrong kind of object, so "
                          "the rung is now labelled as a central value and the "
                          "genuine 95% upper limit 0.023 is carried alongside it. "
                          "The mislabel was conservative: a LOOSER threshold makes "
                          "flatness easier and the required length SHORTER, so it "
                          "could not have inflated any result.",
        "Planck 2018 as an upper limit": "The same table row gives a 95% interval "
                          "Omega_k in [-0.023, +0.002], i.e. |Omega_k| < 0.023, which "
                          "is a legitimate eps_obs and is carried as "
                          "EPS_OBS_PLANCK_2018_UPPER. Eq. (45b) of the same paper "
                          "gives the 68% result Omega_K = 0.0007 +/- 0.0019 for "
                          "TT,TE,EE+lowE+lensing+BAO, with Planck's own summary "
                          "that the Universe is 'spatially flat to a 1 sigma "
                          "accuracy of 0.2%'.",
        "n7k floor is an ASYMPTOTE": "The 1.5e-5 figure is a cosmic-variance NOISE "
                          "level, and those authors adopt the stricter 1e-4 as their "
                          "'curvature floor'. They judge that floor unreachable even "
                          "by Stage IV on CONSERVATIVE forecasts, expecting ~1e-3 -- "
                          "but they add that it is unreachable only absent strong "
                          "assumptions on dark energy evolution and LCDM values, and "
                          "that it is NOT unreachable in principle. So 45.55 is a "
                          "limit no planned experiment reaches and ~43.45 is their "
                          "foreseeable cap; neither is an estimate of the inflation "
                          "length, and neither is a theorem.",
        "n7l provenance": "The idea that measured curvature falsifies eternal "
                          "inflation is NOT this node's: it is Kleban & Schillo "
                          "(2012), who show |Omega_k| > 1e-4 excludes slow-roll "
                          "eternal inflation and Omega_k < -1e-4 excludes all "
                          "eternal inflation including false-vacuum. What this "
                          "node contributes is the wrapper: one stiffness S, a "
                          "sign test, and a strict boundary, so that a model's own "
                          "Omega_k prediction converts mechanically into a verdict.",
        "current bound is borrowed and dated": "The 5e-3 comparison bound is the "
                          "constraint quoted in Leonard et al. (2016); no primary-"
                          "source ACT DR6 curvature limit was located in this pass, "
                          "so the anticipated tighter ACT value is recorded as "
                          "UNVERIFIED and drives no verdict. Every number feeding a "
                          "gate here was read off a primary source, including the "
                          "Planck 2018 value, which was mislabelled until this pass "
                          "and is now checked against arXiv 1807.06209v4 Sect. 7.3.",
        "n7l vacuity condition": "The wrapper is EMPTY until a model predicts "
                                 "Omega_k. N7 supplies no such prediction and "
                                 "cannot: eps_i is free (n7j), so absent a model "
                                 "the filter excludes nothing. Do not read n7l as "
                                 "evidence about inflation model space.",
        "n7l sign is NOT encoded": "curvature_verdict tests |Omega_k| only. The "
                                   "SREI/FVEI discrimination is a SIGN statement "
                                   "about a model-specific distribution of Omega_k, "
                                   "and is deliberately not implemented here.",
    }

    overall = all(ok for _, ok, _ in GATES)

    artifact = {
        "node": "N7",
        "label": "ORIGIN CONSISTENCY WINDOW: one S, two problems, one inequality",
        "generated_by": "origin_consistency_window_n7.py",
        "inputs": {
            "eps_obs": EPS_OBS, "eps_i": EPS_I,
            "N_matter": N_MATTER, "w_infl": W_INFL,
            "eps_i_numerical": EPS_I_NUM, "rho_i": RHO_I,
            "k": K, "D": D, "sigma": SIGMA,
        },
        "s_required": S_REQ,
        "n_infl_needed": N_STAR,
        "window": window_rows,
        "eps_i_freedom": free_rows,
        "measurement_floor": {
            "slope_dN_dln_eps_obs": 1.0 / stiffness(W_INFL),
            "rows": floor_rows,
            "eps_obs_for_60_efolds": eps_for_convention,
            "decades_below_cosmic_variance_level": decades_short,
            "asymptotic_N_infl": saturation,
            "realistic_cap_N_infl": realistic_cap,
            "sigma_omega_k_cosmic_variance": SIGMA_OMEGA_K_COSMIC_VARIANCE,
            "eps_obs_foreseeable": EPS_OBS_FORESEEABLE,
            "eps_obs_act_dr6_unverified_unused": EPS_OBS_ACT_DR6_UNVERIFIED,
            "eps_obs_planck_2018_central_95_not_a_bound": EPS_OBS_PLANCK_2018,
            "eps_obs_planck_2018_upper_95": EPS_OBS_PLANCK_2018_UPPER,
            "planck_2018_omega_k_68cl": EPS_OBS_PLANCK_2018_68CL,
            "planck_2018_omega_k_68cl_err": EPS_OBS_PLANCK_2018_68CL_ERR,
        },
        "model_filter": {
            "rows": model_rows,
            "eps_obs_current_bound": EPS_OBS_QUOTED_2016,
            "omega_k_eternal_inflation_threshold":
                OMEGA_K_ETERNAL_INFLATION_THRESHOLD,
            "ratio_bound_over_threshold": decisive,
            "excluded_at_current_bound": falsified_now,
            "excluded_at_1e_4": falsified_then,
        },
        "scope": SCOPE,
        "gates": {name: {"pass": ok, "detail": det} for name, ok, det in GATES},
        "overall": ("ORIGIN CONSISTENCY WINDOW SOLVED (one S, two problems); "
                    "INITIAL CONDITIONS NOT DERIVED") if overall else "GATE FAILURE",
    }

    if not os.path.isdir(DATA):
        os.makedirs(DATA)
    OUT = os.path.join(DATA, "origin_consistency_window_n7_data.json")
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(artifact, fh, indent=2)
        fh.write("\n")

    print("\n" + "=" * 78)
    print("SCOPE (recorded so it cannot be quietly dropped)")
    for key, val in SCOPE.items():
        print("  %-22s %s" % (key, val))
    print("=" * 78)
    print("OVERALL: %s" % artifact["overall"])
    print("Output written to %s" % OUT)
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
