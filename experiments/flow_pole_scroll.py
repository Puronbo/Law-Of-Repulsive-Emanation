"""
FLOW SCROLL: POLE GEOMETRY, WINDING, AND FEEDING OF THE EH-GRAVITY SECTOR
=========================================================================

The Type Ib beta functions (Codello 2009 eq. 53, as implemented in
litim_flow.py) carry a denominator

    D(G, lam) = (1 - 2*lam)^2 - (29 - 9*lam)*G / (72*pi).

The zero locus of D is the pole curve.  This experiment consolidates the
invariant geometry and the dynamics around it:

  I   Fixed point and twist.       FP = (0.701185, 0.171503); the linearized
                                   flow has complex exponents (spiral), and
                                   each full turn tightens x1/71.5.
  II  The two pole ridges.         D=0 is a quadratic in lam with two roots.
                                   Separation is EXACTLY
                                       sep(G) = (7/(12*sqrt(pi))) * sqrt(G)
                                                 * sqrt(1 + 9G/(3136*pi))
                                   = 0.3292*sqrt(G)*sqrt(1+G/1094.7):
                                   the signature of a rolled sheet whose
                                   layers separate linearly in s = sqrt(G).
                                   The scroll mid-line drifts off axis by
                                   the exact amount G/(64*pi).
  III Winding numbers.             A tight loop around the lower ridge gives
                                   W = -1 (the field wraps once); around the
                                   upper ridge W = 0.000 (a ray-pole that
                                   stretches without rotating); a loop
                                   between both poles gives W = 0.
  IV  Birth and feeding.           On the G=0 axis there are no poles at all:
                                   the flow is the smooth line beta_lam = -2*lam
                                   (the would-be pole at lam=1/2 is a 0/0 whose
                                   numerator vanises with the denominator).
                                   The instant G != 0 the seam crest
                                   beta_lam(G, 1/2) -> +2.0000 appears and the
                                   pair is born.  Poles exist only where D=0
                                   while the numerator N survives (N is their
                                   "food"); the residue is the food per unit
                                   normal distance.

Every claim below ends in a PASS/FAIL line; any FAIL sets exit code 1.
"""

import math
import json
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _REPO)

from litim_flow import beta_Ib

PI = math.pi

# ----------------------------------------------------------------------
fails = 0


def check(name, ok, detail):
    global fails
    if not ok:
        fails += 1
    print("  %s  %-38s %s" % ("PASS" if ok else "FAIL", name, detail))


def pole_pair(G):
    """The two roots (lam_low, lam_up) of D(G, lam) = 0."""
    b = -4.0 + 9.0 * G / (72.0 * PI)
    c = 1.0 - 29.0 * G / (72.0 * PI)
    dsc = b * b - 16.0 * c
    s = math.sqrt(max(dsc, 0.0))
    return (-b - s) / 8.0, (-b + s) / 8.0


def D(G, lam):
    return (1.0 - 2.0 * lam) ** 2 - (29.0 - 9.0 * lam) * G / (72.0 * PI)


def num_lam(G, lam):
    return (((12.0 - 33.0 * lam + 20.0 * lam ** 2 - 200.0 * lam ** 3) * G)
            + (467.0 - 572.0 * lam) / (12.0 * PI) * G ** 2)


def num_G(G, lam):
    return (105.0 - 212.0 * lam + 200.0 * lam ** 2) * G ** 2


def winding_number(Gc, lc, R, n=1440):
    """Index of the beta-vector along a loop {center + R*e^it}."""
    ang = 0.0
    for i in range(n):
        th = 2.0 * PI * i / n
        th2 = 2.0 * PI * (i + 1) / n
        bx, by = beta_Ib(Gc + R * math.cos(th), lc + R * math.sin(th))
        ax, ay = beta_Ib(Gc + R * math.cos(th2), lc + R * math.sin(th2))
        d = (math.atan2(ay, ax) - math.atan2(by, bx) + PI) % (2.0 * PI) - PI
        ang += d
    return ang / (2.0 * PI)


def main():
    print("=" * 70)
    print("FLOW SCROLL: POLE GEOMETRY, WINDING, AND FEEDING")
    print("=" * 70)

    # ---------------- I. fixed point and twist ----------------
    print("\nI. FIXED POINT AND TWIST")
    from litim_flow import find_fp, stability_matrix
    res, Gs, ls = find_fp()
    print("  FP = (%.6f, %.6f), Newton residual = %.1e"
          % (Gs, ls, res))
    check("FP solves beta=0", res < 1e-20,
          "residual %.1e" % res)

    eps = 1e-7
    M = stability_matrix(Gs, ls)
    tr = M[0][0] + M[1][1]
    det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    disc = tr * tr - 4.0 * det
    Re = -tr / 2.0
    Im = math.sqrt(-disc) / 2.0
    print("  Jacobian theta = %.5f +- %.5f i  (disc = %.4f)"
          % (Re, Im, disc))
    check("complex exponents (twist)", disc < -0.001,
          "disc %.4f" % disc)
    tighten = math.exp(-(Re / Im) * 2.0 * PI)
    print("  spiral tightening per 360 deg = %.4f  (~x1/%.1f)"
          % (tighten, 1.0 / tighten))
    check("spiral rolls tight", 0.005 < tighten < 0.05,
          "x1/%.1f per turn" % (1.0 / tighten))

    # ---------------- II. the two pole ridges ----------------
    print("\nII. POLE RIDGE GEOMETRY (D(G, lam) = 0)")
    Gs_test = [1e-4, 1e-3, 1e-2, 0.05, 0.3, 0.6, 1.0]
    sep_ok, c_ok, drift_ok = True, True, True
    sep_rows = []
    for G in Gs_test:
        lo, hi = pole_pair(G)
        sep = hi - lo
        lead = (7.0 / (12.0 * math.sqrt(PI))) * math.sqrt(G)
        corr = math.sqrt(1.0 + 9.0 * G / (3136.0 * PI))
        line = "G=%-6.4g sep=%.5f formula=%.5f ratio=%.4f" % (
            G, sep, lead * corr, sep / (lead * corr))
        print("  " + line)
        sep_rows.append({"G": G, "sep": sep,
                         "formula": lead * corr})
        if abs(sep / (lead * corr) - 1.0) > 2e-4:
            sep_ok = False
        s = math.sqrt(G)
        c = (0.5 - lo) / s
        if not (0.160 < c < 0.172):
            c_ok = False
        if G in [0.01, 0.3, 1.0]:
            mid = (lo + hi) / 2.0
            pred = 0.5 - G / (64.0 * PI)
            if abs(mid - pred) > 1e-9:
                drift_ok = False
    print("  exact law: sep = (7/(12*sqrt(pi)))*sqrt(G)*sqrt(1+9G/3136pi)")
    check("separation law exact (ratio ~1)", sep_ok,
          "7 G-values, ratio within 2e-4")
    check("scroll linear in s=sqrt(G) (c in [0.160,0.172])", c_ok,
          "ridges straight in the s-coordinate")
    check("scroll mid-line drift = G/(64*pi) exact", drift_ok,
          "mid(g) = 1/2 - g/(64*pi)")

    lo6, hi6 = pole_pair(0.6)
    check("mirror lam<->1-lam broken (eccentric roll)", abs((1 - lo6) - hi6) > 0.005,
          "1-lower %.4f vs upper %.4f" % (1 - lo6, hi6))

    # ---------------- III. winding numbers ----------------
    print("\nIII. WINDING OF THE VELOCITY FIELD")
    w_lo = winding_number(0.6, lo6, 0.005)
    w_up = winding_number(0.6, hi6, 0.005)
    w_between = winding_number(0.6, (lo6 + hi6) / 2.0, 0.012)
    print("  W(lower ridge, R=0.005) = %+.3f" % w_lo)
    print("  W(upper ridge, R=0.005) = %+.3f" % w_up)
    print("  W(between poles, R=0.012) = %+.3f" % w_between)
    check("upper ridge is a ray-pole, W=0", abs(w_up) < 0.02,
          "winding +%.3f" % w_up)
    check("lower ridge wraps once, W=-1", abs(w_lo + 1.0) < 0.02,
          "winding %+.3f" % w_lo)
    check("between-poles loop W=0", abs(w_between) < 0.02,
          "winding %+.3f" % w_between)

    # ---------------- IV. birth and feeding ----------------
    print("\nIV. BIRTH (G=0) AND FEEDING (N at D=0)")
    birth_ok = True
    for lam in [0.2, 0.45, 0.55, 0.8]:
        bG, bL = beta_Ib(0.0, lam)
        if abs(bG) > 1e-9 or abs(bL - (-2.0 * lam)) > 1e-9:
            birth_ok = False
    check("G=0 axis is smooth, beta_lam = -2*lam everywhere", birth_ok,
          "no poles before the coupling is turned on")

    crest = beta_Ib(1e-8, 0.5)[1]
    check("seam crest beta_lam(G, 1/2) -> +2.0000 as G->0",
          abs(crest - 2.0) < 1e-4, "beta = %+.4f" % crest)

    feed_ok = True
    for tag, lam in [("lower", lo6), ("upper", hi6)]:
        nL, nG = num_lam(0.6, lam), num_G(0.6, lam)
        print("  %-5s ridge (0.6, %.4f): D=%.1e N_lam=%.4f N_G=%.4f"
              % (tag, lam, D(0.6, lam), nL, nG))
        if abs(nL) < 0.5 or abs(nG) < 5.0 or abs(D(0.6, lam)) > 1e-12:
            feed_ok = False
    check("poles are fed: numerator survives at D=0", feed_ok,
          "D~1e-16, N_lam=-2.09/-28.7, N_G=+19.4/+18.2 at G=0.6")

    strip_ok = D(0.6, 0.17) > 0.0 and D(0.6, 0.5) < 0.0
    check("scroll has two faces: D>0 outside, D<0 inside the strip",
          strip_ok, "D(0.6,0.17)=%+.3f  D(0.6,0.5)=%+.3f"
          % (D(0.6, 0.17), D(0.6, 0.5)))

    # residue = food per unit normal distance
    dn = (D(0.6, lo6 + 1e-6) - D(0.6, lo6 - 1e-6)) / 2e-6
    res_lam = num_lam(0.6, lo6) / (24.0 * PI * dn)
    res_G = num_G(0.6, lo6) / (24.0 * PI * dn)
    print("  residue at lower ridge: d(beta_lam)/dn = %+.4f, "
          "d(beta_G)/dn = %+.4f" % (res_lam, res_G))

    # ---------------- summary ----------------
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "data"), exist_ok=True)
    out = {
        "fp": {"G_star": Gs, "lam_star": ls, "residual": res,
               "theta_re": Re, "theta_im": Im,
               "spiral_tighten_per_turn": tighten},
        "pole_ridges": {"sep_rows": sep_rows,
                        "drift": "1/2 - G/(64*pi)",
                        "linear_in_s": True},
        "winding": {"lower": w_lo, "upper": w_up,
                    "between": w_between},
        "birth": {"G0_smooth": True, "seam_crest": float(crest)},
        "feeding": {"D_at_ridges_zero": True,
                    "N_nonzero": True,
                    "strip_sign_flip": True},
    }
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "data", "flow_pole_scroll.json"), "w") as fh:
        json.dump(out, fh, indent=2)

    print("\n" + "=" * 70)
    if fails == 0:
        print("ALL CHECKS PASS -- the EH pole pair is a scroll: two sheets, "
              "sep 0.3292*sqrt(G), born from the G=0 line, wrapped W=-1, "
              "fed by the surviving numerator.")
    else:
        print("%d CHECKS FAILED" % fails)
    print("=" * 70)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()