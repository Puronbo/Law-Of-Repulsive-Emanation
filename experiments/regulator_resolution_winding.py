"""
REGULATOR-RESOLUTION WINDING: WHICH COARSENING DESTROYS THE EJECTOR?
===================================================================

delta0_selection.py's falsification clause (last line of the F19
ledger row, echoed by F20): "falsifiable via regulators that flip
lower-ridge W at release".  F20 mapped the flip along the LOOP-RADIUS
axis: the W = -1 ejector lives in the release annulus
R_trans(0.6) ~ 0.0039 < R < R_flip_back(0.6) ~ 0.22 of the lower
ridge (G,lam)-projection, and the selector statement is:
   W = -1  (LANE-2, REMOVABLE/SELECTED)   iff  R in the annulus,
   W =  0  (LANE-1, POLE)                 otherwise.

This experiment executes the clause LIVE: it asks WHICH operational
meaning of "regulator resolution" actually realizes the
W -> 0 destruction, testing two candidate prescriptions on the same
release loop (G_c = 0.6, lam_lo = 0.36952):

  P1  FIELD-COARSENING (ball-convolution): beta_s = 9-point disk mean
      of the flow map on a ball of width s.  Excluded: the scan is
      chaotic (W takes >= 4 distinct integers; the loop image's
      crossing of the beta-origin is a |beta|-dip, never a clean 0/0:
      min|beta_s| stays >= 1e-2).  Prescribing the falsification via
      field-blurring of the singular locus is NOT legitimate.

  P2  PROBE-UNDERSAMPLING (angular Nyquist): winding from a polygon
      loop with n vertices.  Nominal: W stays -1 down to n ~ 14 and
      steps sharply to 0 at n ~ 12 for both R = 0.05 and R = 0.10.
      The threshold is R-INDEPENDENT as a FRACTION of the loop radius:
      tangent arc step step_crit = 2 pi R / n_crit ~ (0.50+-0.05) R
      (n_crit ~ 12.6), i.e. the polygon must have more than ~13 sides
      before the argument-principle sum can carry the winding.  The
      step_crit length (0.024 at R=0.05, 0.052 at R=0.10) sits INSIDE
      the annulus band [0.004, 0.22].

Combined selector domain (the falsifiability statement made precise):
   W = -1  iff  R in (R_trans, R_flip_back)  AND  n > n_crit.
Coarsening loop radius past R_flip_back (F20) OR undersampling the
probe below ~13 vertices (P2) destroys the removable agent; blurring
the field (P1) does not realize the flip honestly and is withdrawn.

Honesty notes: the ball-blur is a 9-point stencil; points near the
D=0 locus contribute 1/D spikes, which is why P1's winding is noisy --
that noise is itself the reason the prescription is excluded, not a
bug to be smoothed over.  The claim "k ~ 1/step as physical cutoff"
is interpretive and flagged; the quantitative claims are on the
projection resolution.
"""

import math
import json
import os
import sys

from winding_phase_diagram import beta_AB, pole_pair

PI = math.pi
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

A = 29.0 / (72.0 * PI)
B = 9.0 / (72.0 * PI)


def blur_beta(G, lam, s):
    acc_g, acc_l, n = 0.0, 0.0, 0
    for dx, dy in [(0.0, 0.0),
                   (s, 0.0), (-s, 0.0), (0.0, s), (0.0, -s),
                   (s / math.sqrt(2.0), s / math.sqrt(2.0)),
                   (s / math.sqrt(2.0), -s / math.sqrt(2.0)),
                   (-s / math.sqrt(2.0), s / math.sqrt(2.0)),
                   (-s / math.sqrt(2.0), -s / math.sqrt(2.0))]:
        bg, bl = beta_AB(G + dx, lam + dy, A, B)
        acc_g += bg
        acc_l += bl
        n += 1
    return acc_g / n, acc_l / n


def winding(Gc, lc, R, n=None, use_blur=False, s=0.0):
    ang = 0.0
    mnd = float("inf")
    for i in range(n):
        th = 2.0 * PI * i / n
        th2 = 2.0 * PI * (i + 1) / n
        if use_blur:
            bx, by = blur_beta(Gc + R * math.cos(th), lc + R * math.sin(th), s)
            ax, ay = blur_beta(Gc + R * math.cos(th2),
                               lc + R * math.sin(th2), s)
        else:
            bx, by = beta_AB(Gc + R * math.cos(th), lc + R * math.sin(th),
                             A, B)
            ax, ay = beta_AB(Gc + R * math.cos(th2), lc + R * math.sin(th2),
                             A, B)
        d = (math.atan2(ay, ax) - math.atan2(by, bx) + PI) % (2.0 * PI) - PI
        ang += d
        if use_blur:
            m = math.hypot(bx, by)
            if m < mnd:
                mnd = m
    return ang / (2.0 * PI)


def flip_n(Gc, lc, R, lo_n, hi_n):
    """n where W goes from the interior value to 0 while sampling coarsens."""
    hi, lo = hi_n, lo_n
    for _ in range(40):
        mid = (lo + hi) // 2
        if abs(winding(Gc, lc, R, mid)) < 0.5:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    print("=" * 70)
    print("REGULATOR-RESOLUTION WINDING: WHICH COARSENING DESTROYS")
    print("THE EJECTOR? (falsification clause of delta0_selection)")
    print("=" * 70)

    rt6, rb6 = 0.003938, 0.222368
    print(f"\nF20 annulus at release: R in ({rt6:.4f}, {rb6:.4f}) -> W=-1")

    Gc = 0.6
    lc = pole_pair(Gc, A, B)[0]
    R = 0.05

    # P1: field coarse-graining (ball blur) -- candidate, to be excluded
    s_grid = [1e-4, 3e-4, 1e-3, 3e-3, 6e-3, 1e-2, 2e-2, 3e-2,
              5e-2, 8e-2, 1.2e-1, 1.8e-1, 2.5e-1, 4e-1]
    print(f"\nP1 FIELD-COARSENING (candidate prescription): R = {R}, n = 1800")
    print(f"  {'s':>9} {'W(s)':>10} {'min|beta_s|':>12}")
    scan1 = []
    distinct_ints = set()
    min_dip = float("inf")
    for s in s_grid:
        w = winding(Gc, lc, R, 1800, use_blur=True, s=s)
        scan1.append({"s": s, "W": w})
        distinct_ints.add(round(w))
        min_dip = min(min_dip, _min_blur_mag(Gc, lc, R, s))
        print(f"  {s:>9.2e} {w:>10.3f}")
    print(f"  -> distinct integers taken: {sorted(distinct_ints)}; "
          f"min|beta_s| dip = {min_dip:.1e}")

    # P2: probe undersampling (angular Nyquist)
    print(f"\nP2 PROBE-UNDERSAMPLING (candidate prescription), unblurred: ")
    rows2 = []
    for R2 in [0.05, 0.10]:
        ngrid = [720, 360, 180, 90, 45, 30, 24, 20, 18, 16, 14, 12, 10, 8]
        seq = []
        for n in ngrid:
            w = winding(Gc, lc, R2, n)
            seq.append((n, round(w)))
            print(f"  R={R2:.2f} n={n:3d} step={2*PI*R2/n:.4f} W={w:+.2f}")
        ncrit = flip_n(Gc, lc, R2, 8, 45)
        step_crit = 2.0 * PI * R2 / ncrit
        rows2.append({"R": R2, "n_crit": ncrit,
                      "step_crit": step_crit,
                      "step_over_R": step_crit / R2})
        print(f"  -> flip at n_crit ~ {ncrit} (tangent step {step_crit:.4f}, "
              f"step/R = {step_crit/R2:.3f})")

    # combined selector domain verification
    w_annulus_fine = winding(Gc, lc, 0.05, 3600)
    w_annulus_coarse = winding(Gc, lc, 0.05, 12)
    w_outside_fine = winding(Gc, lc, 0.3, 3600)
    w_outside_coarse = winding(Gc, lc, 0.3, 12)
    print(f"\nCombined domain (G_c=0.6): ")
    print(f"  R=0.05 n=3600 (annulus, fine):   W = {w_annulus_fine:+.1f}")
    print(f"  R=0.05 n=12   (annulus, coarse):  W = {w_annulus_coarse:+.1f}")
    print(f"  R=0.30 n=3600 (outside, fine):    W = {w_outside_fine:+.1f}")
    print(f"  R=0.30 n=12   (outside, coarse):  W = {w_outside_coarse:+.1f}")

    # gates
    g1 = abs(scan1[0]["W"] + 1.0) < 0.05            # blur small-s consistency
    g2 = (min_dip > 1e-3) and (len(distinct_ints) >= 4)   # P1 excluded cleanly
    g3r = []
    for r2 in rows2:
        g3r.append(0.45 <= r2["step_over_R"] <= 0.65)
    g3 = all(g3r) and len(rows2) == 2               # P2 R-independent flip
    g4 = (abs(w_annulus_fine + 1.0) < 0.05 and abs(w_annulus_coarse) < 0.05
          and abs(w_outside_fine) < 0.05 and abs(w_outside_coarse) < 0.05)
    g5 = (rows2[0]["step_crit"] < rb6 and rows2[1]["step_crit"] < rb6)

    print("\n" + "-" * 70)
    print("INTERPRETATION")
    print("-" * 70)
    print("1. P1 (field-blurring the singular locus) is EXCLUDED: the")
    print("   winding on the blur axis is chaotic (>= 4 distinct integers)")
    print("   and never cleanly reaches a 0/0 (min|beta_s| stalls at")
    print("   ~1e-2). The falsification clause must NOT be read as")
    print("   'blur the field'; the theta condition of the entropy")
    print("   theorem (THE_ENTROPY_CONDITION_THEOREM.md:251) acts on the")
    print("   argument-principle observable, whose topology lives on the")
    print("   probe, not on the field's smeared image.")
    print("2. P2 (loop/probe undersampling) is NOMINAL: W steps -1 -> 0")
    print("   when the polygon has fewer than ~13 sides, for loop radius")
    print("   independent of R as a fraction: step_crit ~ 0.5 R.")
    print("3. The extended selector domain: W = -1 iff the probe lives in")
    print("   the release annulus AND the probe resolves it (n > ~12).")
    print("   This makes delta0_selection's falsifiability EXPLICIT:")
    print("   any legitimate probe realization of the lower-ridge flow at")
    print("   release must (a) sit in (R_trans, R_flip_back) and")
    print("   (b) resolve the tangent scale (n > n_crit ~ 12.6, step < 0.5R).")

    gates = {
        "G1 blur consistency: W=-1 at s->0": g1,
        "G2 P1 EXCLUDED: blur axis chaotic (>=4 integers), no 0/0 "
        "(min|beta| >= 1e-3)": g2,
        "G3 P2 NOMINAL: sharp -1->0 flip, step_crit/R ~ 0.5 at R in "
        "{0.05,0.10}": g3,
        "G4 combined domain: annulus+fine -> -1, else 0 (all four)":
            g4,
        "G5 P2 step_crit lies inside the annulus band (< R_flip_back)":
            g5,
    }
    overall = all(gates.values())

    print("\n" + "=" * 70)
    for k, v in gates.items():
        print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    print(f"OVERALL: {'PASS' if overall else 'FAIL'}")

    os.makedirs(DATA, exist_ok=True)
    out = {
        "release": {"G_c": 0.6, "lam_lo": lc,
                    "annulus": (rt6, rb6)},
        "P1_field_blur_scan": scan1,
        "P1_min_dip": min_dip,
        "P1_distinct_integers": sorted(distinct_ints),
        "P2_probe_undersampling": rows2,
        "combined_domain": {
            "R05_n3600": w_annulus_fine,
            "R05_n12": w_annulus_coarse,
            "R30_n3600": w_outside_fine,
            "R30_n12": w_outside_coarse,
        },
        "selector_domain": "W=-1 iff R in (R_trans, R_flip_back) AND "
                           "n > ~12.6 (step < ~0.5 R)",
        "gates": {k: v for k, v in gates.items()},
        "overall": overall,
        "ties_to": "delta0_selection.py LANE-1/2; F20 annulus; "
                   "THE_ENTROPY_CONDITION_THEOREM.md:224-231,251-256",
    }
    with open(os.path.join(DATA, "regulator_resolution_winding.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nWrote data/regulator_resolution_winding.json")
    sys.exit(0 if overall else 1)


def _min_blur_mag(Gc, lc, R, s, n=1800):
    mnd = float("inf")
    for i in range(n):
        th = 2.0 * PI * i / n
        bx, by = blur_beta(Gc + R * math.cos(th), lc + R * math.sin(th), s)
        m = math.hypot(bx, by)
        if m < mnd:
            mnd = m
    return mnd


if __name__ == "__main__":
    main()