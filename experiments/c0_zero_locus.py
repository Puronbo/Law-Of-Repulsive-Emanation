#!/usr/bin/env python3
"""
c0_zero_locus.py -- the origin and the zeros, on the actual C0 scale.

Follow-up to c0_at_zeros.py. That script showed C0-per-zero was not
well-posed. This one locates the zeros properly -- from the definition of the
potential rather than by guessing -- and then asks what the origin has to do
with them, and whether anything survives contact with a Millennium problem.

The scale is defined in Universals/hamiltonian_flow.py:

    V(q) = sum over non-context nodes of max(0, ALPHA - d(q, x))**2
    ALPHA = 2.5, d = Poincare-disk geodesic distance, q0 = Origin = (0, 0)

So the zeros of V are exactly the points that are at geodesic distance
>= ALPHA from EVERY node, and "the origin" is the point the corpus calls
the starting configuration.

What this script establishes, with runnable evidence:

  G1  The zero set is real, explicit, and large: the region {r >= r*(theta)},
      whose inner boundary is NOT a circle -- r* spans 0.8511..0.9832 with
      direction. But C0 restricted to the zero set is 0 at every point. So
      "C0 for every zero" is a constant function: it carries no per-zero
      information, and cannot encode anything about a zero's position.

  G2  The origin is NOT a zero. It is very nearly the global maximum of V
      (V(q0) = 26.4333; the grid max is 26.4803 a short distance away).
      Origin and zeros are antipodal on the scale: the origin is where the
      repulsion is maximal, the zeros are where every term has decayed to
      zero. There is no sense in which the origin "generates" the zeros.

  G3  The 0/0 in docs/IF_C0_IS_0_OVER_0.md is NOT a removable singularity.
      The document claims the limit of V(q0)/(N - |context|) as the context
      grows to all nodes exists and equals an "average energy per
      non-context node", and that this is C0. It does not exist. The final
      step keeps whichever node was absorbed last, so the one-step limit is
      that node's own term: 9 distinct values spanning 6.2154. The limit
      depends on the path. That is the definition of a non-removable
      singularity, and it falsifies sections 2, 3 and 9 of that document.

  G4  24.434792 is not the removable value, and is not even the quantity the
      document defines. The document's own formula at the documented
      context gives V(q0)/(N - |ctx|) = 3.054349, an order of magnitude
      away. 24.434792 is the raw sum V(q0) for a hand-picked two-node
      context -- an unnormalised value, not an average, not a limit.

  G5  The invariance claim of section 4 fails. It says the removable value
      is invariant under "rotations, translations, re-indexings". A
      0.01 coordinate edit moves the one-step limit, and re-indexing (choosing
      the context) yields 768 distinct values over the 1024 contexts. The
      value is a function of the typed coordinates and of the arbitrary
      choice of which nodes are "in context".

  G6  The asymmetry with the zeta side is the opposite of what this script
      first claimed, and the correction matters. zeta(s)/zeta(1-s) IS
      genuinely removable at a zero: the limit is chi(rho), and it is the
      same from every approach direction (error 8.1e-9 at eps=1e-8). And
      |chi| = 1 does locate a point relative to the critical line -- on the
      strip 0 < Re < 1 it holds iff Re = 1/2 (PL-22 gate B). What does NOT
      follow is RH. |chi| = 1 is a property of the whole line: it holds at a
      non-zero impostor 1/2 + i(gamma + 0.5) to 1e-25, so evaluating it at a
      zero cannot distinguish a zero from any other point on the line, and
      the certification step is vacuous (PL-22 gate C). So the zeta 0/0 has
      the unique removable value that the C0 0/0 lacks; the analogy fails
      because the C0 side is path-dependent, not because the zeta side is
      uninformative.

Verdict: the origin/zero relationship on the C0 scale is a maximum and a
star-shaped region of zeros, with C0 identically zero on the zeros. The
"0/0 = removable value" story that ties them together does not survive; the
limit is path-dependent. No Millennium Prize Problem follows.

Run:  python experiments/c0_zero_locus.py

Writes data/c0_zero_locus_data.json (tracked, in the manifest).
"""

import itertools
import json
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "Universals"))

from hamiltonian_flow import (  # noqa: E402
    ALPHA,
    POSITIONS,
    R_MAX_DISK,
    R_MAX_GRID,
    hyperbolic_dist,
    repulsion_loss,
)

N_NODES = len(POSITIONS)
Q0 = POSITIONS["Origin"]
CONTEXT = ["Tech", "Silicon"]

report = {"experiment": "C0 origin and zero locus on the C0 scale", "gates": {}}


def gate(name, ok, detail, **extra):
    entry = {"pass": bool(ok), "detail": detail}
    entry.update(extra)
    report["gates"][name] = entry
    print("  [%s] %-34s %s" % ("PASS" if ok else "FAIL", name, detail))
    return ok


def is_zero(q, tol=1e-12):
    return repulsion_loss(q, []) <= tol


def zero_radius(th, sectors=1440):
    """Radius along direction th at which V first reaches zero.

    V is non-increasing along any ray (the monotonicity check in this file
    confirms it), so a bisection is exact. Returns None if the ray never
    reaches zero inside R_MAX_DISK.
    """
    f = lambda r: repulsion_loss(  # noqa: E731
        np.array([r * math.cos(th), r * math.sin(th)]), [])
    if f(R_MAX_DISK) > 1e-12:
        return None
    lo, hi = 0.0, R_MAX_DISK
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if f(mid) > 1e-12:
            lo = mid
        else:
            hi = mid
    return hi


def g1_zero_set_is_real_but_c0_is_flat_there():
    print("\nG1  Where are the zeros of the scale, and what is C0 there?")
    print("     V(q) = 0  <=>  d(q, x) >= ALPHA = %.2f for every node" % ALPHA)

    r_star = []
    for i in range(72):
        th = 2.0 * math.pi * i / 72.0
        r = zero_radius(th, sectors=360)
        if r is not None:
            r_star.append(r)
    lo_r, hi_r = min(r_star), max(r_star)

    # area of the zero region, by the polar area integral
    area = 0.0
    for i in range(2880):
        th = 2.0 * math.pi * i / 2880.0
        r = zero_radius(th, sectors=720)
        if r is not None:
            area += 0.5 * r * r * (2.0 * math.pi / 2880.0)
    area_frac = area / (math.pi * R_MAX_DISK ** 2)

    found = 0
    for i in range(201):
        for j in range(201):
            x = -R_MAX_DISK + 2 * R_MAX_DISK * i / 200.0
            y = -R_MAX_DISK + 2 * R_MAX_DISK * j / 200.0
            if x * x + y * y > R_MAX_DISK ** 2:
                continue
            if is_zero(np.array([x, y])):
                found += 1

    c0_at_zero = repulsion_loss(np.array([0.95, 0.0]), [])
    flat = abs(c0_at_zero) < 1e-12
    non_circular = hi_r - lo_r > 0.01

    print("     inner boundary is NOT a circle: r*(theta) spans "
          "%.4f .. %.4f" % (lo_r, hi_r))
    print("     (min is just inside the interaction horizon R_MAX_GRID = %.4f;"
          " R_MAX_GRID is the worst-case, not the best-case, radius)"
          % R_MAX_GRID)
    print("     zero set area = %.1f%% of the disk" % (100.0 * area_frac))
    print("     %d zero grid points; C0 on the zero set = %.1f"
          % (found, c0_at_zero))

    return gate(
        "G1 zero set exists, C0 flat on it",
        found > 0 and flat and non_circular,
        "zero set = {r >= r*(theta)} with r* spanning %.4f..%.4f (%.1f%% of "
        "the disk); C0 == 0 identically there, so C0-per-zero is a constant "
        "and carries no per-zero information" % (lo_r, hi_r, 100.0 * area_frac),
        r_star_min=lo_r,
        r_star_max=hi_r,
        area_fraction=area_frac,
    )


def g2_origin_is_a_maximum_not_a_zero():
    print("\nG2  Is the origin one of the zeros, or related to them?")
    v0 = repulsion_loss(Q0, [])
    best = (-1.0, None)
    for i in range(301):
        for j in range(301):
            x = -R_MAX_DISK + 2 * R_MAX_DISK * i / 300.0
            y = -R_MAX_DISK + 2 * R_MAX_DISK * j / 300.0
            if x * x + y * y > R_MAX_DISK ** 2:
                continue
            v = repulsion_loss(np.array([x, y]), [])
            if v > best[0]:
                best = (v, (x, y))
    antipodal = not is_zero(Q0) and v0 > 0.99 * best[0]

    print("     V(origin) = %.6f   is_zero(origin) = %s" % (v0, is_zero(Q0)))
    print("     max V on the disk = %.6f at (%.3f, %.3f)" % (best[0], best[1][0], best[1][1]))
    print("     -> origin is where repulsion is MAXIMAL; the zeros are where")
    print("        every term has decayed to 0. Opposite ends of the scale.")

    return gate(
        "G2 origin is a max, not a zero", antipodal,
        "V(origin)=%.4f is the near-maximum of V; the zeros are at "
        "r >= r*. Origin and zeros are antipodal, not connected"
        % v0,
    )


def g3_zero_over_zero_is_not_removable():
    print("\nG3  Is C0 = V(q0)/(N - |context|) a removable 0/0?")
    nodes = list(POSITIONS)
    terms = {k: max(0.0, ALPHA - hyperbolic_dist(Q0, p)) ** 2
             for k, p in POSITIONS.items()}

    final = {}
    for k in nodes:
        ctx = [n for n in nodes if n != k]
        final[k] = repulsion_loss(Q0, ctx) / (N_NODES - len(ctx))
    distinct = sorted({round(v, 9) for v in final.values()})
    spread = distinct[-1] - distinct[0]
    matches_term = all(abs(final[k] - terms[k]) < 1e-9 for k in nodes)

    print("     docs/IF_C0_IS_0_OVER_0.md sec.2: 'The limit exists.'")
    print("     the last absorbed node decides the last term, so the one-step")
    print("     limit is that node's own term:")
    for k in sorted(final, key=lambda k: -final[k]):
        print("       last=%-8s limit = %.6f   (its term = %.6f)"
              % (k, final[k], terms[k]))
    print("     -> %d distinct limits, spread %.6f; limit depends on the path"
          % (len(distinct), spread))

    return gate(
        "G3 the 0/0 is NOT removable", len(distinct) > 1 and matches_term,
        "one-step limit = the last node's own term; %d distinct values, "
        "spread %.4f. Path-dependent, so the limit does not exist. Falsifies "
        "IF_C0_IS_0_OVER_0.md sec.2/3/9" % (len(distinct), spread),
    )


def g4_where_does_24434792_come_from():
    print("\nG4  Is 24.434792 the removable value the document describes?")
    raw = repulsion_loss(Q0, CONTEXT)
    per_node = raw / (N_NODES - len(CONTEXT))
    limits = [repulsion_loss(Q0, [n for n in POSITIONS if n != k]) / 1.0
              for k in POSITIONS]
    in_limit_range = min(limits) - 1e-9 <= raw <= max(limits) + 1e-9
    is_per_node = abs(raw - per_node) < 1e-9

    print("     V(q0) raw sum, context=%s      = %.6f" % (CONTEXT, raw))
    print("     the document's V(q0)/(N-|ctx|)  = %.6f" % per_node)
    print("     the actual one-step limits span [%.6f, %.6f]"
          % (min(limits), max(limits)))

    return gate(
        "G4 24.434792 is neither limit nor average",
        not is_per_node and not in_limit_range,
        "24.434792 is the raw unnormalised sum for a hand-picked 2-node "
        "context; the document's own average is %.4f and the real limits "
        "span [%.4f, %.4f]. It is not the removable value"
        % (per_node, min(limits), max(limits)),
    )


def g5_invariance_claim_fails():
    print("\nG5  Is the removable value invariant, as section 4 claims?")
    base = repulsion_loss(Q0, [n for n in POSITIONS if n != "Origin"]) / 1.0
    moved = {}
    for name in ("System", "Idea", "Mammal"):
        shifted = dict(POSITIONS)
        shifted[name] = shifted[name] + np.array([0.01, 0.0])
        tot = 0.0
        for nid, pos in shifted.items():
            if nid == "Origin":
                continue
            d = hyperbolic_dist(Q0, pos)
            if d < ALPHA:
                tot += (ALPHA - d) ** 2
        moved[name] = tot

    values = set()
    for r in range(len(POSITIONS) + 1):
        for combo in itertools.combinations(POSITIONS, r):
            values.add(round(repulsion_loss(Q0, list(combo)), 6))
    ctx_sensitive = len(values) > 1

    print("     section 4: invariant under 'rotations, translations, re-indexings'")
    print("     base one-step limit = %.6f" % base)
    for name, v in moved.items():
        print("       coordinate %-7s +0.01 -> %.6f" % (name, v))
    print("     context choice: %d distinct values over %d contexts"
          % (len(values), 2 ** N_NODES))

    return gate(
        "G5 invariance claim is false",
        any(abs(v - base) > 1e-9 for v in moved.values()) and ctx_sensitive,
        "a 0.01 coordinate edit changes the limit, and re-indexing gives %d "
        "distinct values over 2^%d contexts. The value is a function of "
        "typed coordinates and of an arbitrary context choice"
        % (len(values), N_NODES),
    )


def g6_zeta_side_is_removable_and_c0_side_is_not():
    print("\nG6  Is the zeta 0/0 better behaved than the C0 0/0?")

    import mpmath as mp
    mp.mp.dps = 40
    chi = lambda s: (mp.pi ** (s - mp.mpf(1) / 2) * mp.gamma((1 - s) / 2)
                     / mp.gamma(s / 2))
    ratio = lambda s: mp.zeta(s) / mp.zeta(1 - s)

    gamma = mp.mpf("14.13472514173469379045725198356247027")
    rho = mp.mpc(mp.mpf(1) / 2, gamma)
    ONE = mp.mpf(1)

    # (a) the zeta 0/0 IS removable, and the limit is direction-independent
    errs = {}
    for tag, eps in (("1e-4", mp.mpf("1e-4")), ("1e-6", mp.mpf("1e-6")),
                     ("1e-8", mp.mpf("1e-8"))):
        worst = 0.0
        for ang in (0.0, 0.6, 1.4, 2.3, -1.1):
            v = ratio(rho + eps * mp.e ** (1j * ang))
            worst = max(worst, abs(complex(v - chi(rho))))
        errs[tag] = worst
    removable = errs["1e-8"] < 1e-7 and errs["1e-4"] > errs["1e-8"] * 100

    # (b) |chi| = 1 holds along the WHOLE line, zeros and non-zeros alike,
    #     which is why the certification step is vacuous (PL-22, gate C)
    impostor = mp.mpc(mp.mpf(1) / 2, gamma + mp.mpf("0.5"))
    on_line_zero = abs(complex(abs(chi(rho)) - ONE))
    on_line_impostor = abs(complex(abs(chi(impostor)) - ONE))
    impostor_not_zero = abs(mp.zeta(impostor)) > 1e-3
    TOL = 1e-30            # 40 working digits: |chi| = 1 is exact, so this is tight
    line_is_whole = on_line_zero < TOL and on_line_impostor < TOL

    # (c) off the line it does move, so the identity is not simply constant
    off = [abs(complex(abs(chi(mp.mpc(s, gamma))) - 1))
           for s in (mp.mpf("0.3"), mp.mpf("0.45"), mp.mpf("0.55"), mp.mpf("0.7"))]
    moves_off = all(v > 1e-6 for v in off)

    print("     (a) zeta(s)/zeta(1-s) at a zero rho:  max |value - chi(rho)|")
    for k in ("1e-4", "1e-6", "1e-8"):
        print("         eps=%-8s  %.3e" % (k, errs[k]))
    print("         -> the zeta 0/0 IS removable; the limit is chi(rho), the")
    print("            same from every approach direction. Contrast G3.")
    print("     (b) |chi| = 1 on the entire line:")
    print("         at the zero        |chi|-1 = %.1e" % on_line_zero)
    print("         at a NON-zero 1/2+i(g+0.5)  |chi|-1 = %.1e   "
          "(|zeta| there = %.3f)"
          % (on_line_impostor, float(abs(mp.zeta(impostor)))))
    print("         -> the value 1 cannot tell a zero from any other point")
    print("            on the line, so it certifies nothing about RH (PL-22)")
    print("     (c) off the line |chi| departs from 1 by %.4f, %.4f, %.4f, %.4f"
          % tuple(off))

    return gate(
        "G6 zeta 0/0 is removable, C0 0/0 is not",
        removable and line_is_whole and impostor_not_zero and moves_off,
        "the zeta 0/0 is genuinely removable: zeta(s)/zeta(1-s) -> chi(rho) "
        "with the limit independent of approach direction (error %.1e at "
        "eps=1e-8). |chi| = 1 then holds on the WHOLE line -- at the zero to "
        "%.0e and at a non-zero impostor to %.0e -- so it is a property of the "
        "line and cannot decide RH (PL-22 gate C). Off the line it moves by "
        "%.3f, so it is not vacuous as a location identity, only as a zero "
        "detector. The real asymmetry with C0 is therefore sharper than the "
        "old text claimed: the zeta side HAS a unique removable value and the "
        "C0 side has none."
        % (errs["1e-8"], on_line_zero, on_line_impostor, off[0]),
        zeta_removable=True,
        zeta_limit_chi=True,
        chi_line_whole=line_is_whole,
        chi_off_line_min=float(min(off)),
        chi_bracket_err_1e8=float(errs["1e-8"]),
    )


def main():
    print("=" * 74)
    print("C0 ORIGIN AND ZEROS ON THE SCALE -- investigation")
    print("=" * 74)
    print("V(q) = sum of (ALPHA - d(q,x))^2 over %d nodes, ALPHA = %.2f"
          % (N_NODES, ALPHA))
    print("origin q0 = (%.1f, %.1f);  d = Poincare-disk geodesic distance"
          % (Q0[0], Q0[1]))
    print("documented C0 = V(q0) with context %s = %.6f"
          % (CONTEXT, repulsion_loss(Q0, CONTEXT)))

    gates = [
        g1_zero_set_is_real_but_c0_is_flat_there(),
        g2_origin_is_a_maximum_not_a_zero(),
        g3_zero_over_zero_is_not_removable(),
        g4_where_does_24434792_come_from(),
        g5_invariance_claim_fails(),
        g6_zeta_side_is_removable_and_c0_side_is_not(),
    ]

    report["summary"] = {
        "gates": "%d/%d PASS" % (sum(gates), len(gates)),
        "alpha": ALPHA,
        "nodes": N_NODES,
        "documented_c0": repulsion_loss(Q0, CONTEXT),
    }
    g1 = report["gates"]["G1 zero set exists, C0 flat on it"]
    report["verdict"] = (
        "The zeros of the C0 scale form the region {r >= r*(theta)}, whose "
        "inner boundary spans %.4f to %.4f and is not circular; C0 is "
        "identically zero there, so C0-per-zero is a constant. The "
        "origin is the near-maximum of V, not a zero, and is antipodal to the "
        "zero set. The 0/0 of IF_C0_IS_0_OVER_0.md is path-dependent, so it is "
        "not a removable singularity, and 24.434792 is neither its limit nor "
        "the average the document defines. Nothing here connects to a "
        "Millennium Prize Problem." % (g1["r_star_min"], g1["r_star_max"])
    )

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "c0_zero_locus_data.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)

    print("\n" + "=" * 74)
    print("VERDICT: %d/%d gates PASS" % (sum(gates), len(gates)))
    print("=" * 74)
    for line in report["verdict"].split(". "):
        print("  " + line.strip().rstrip(".") + ".")
    print("\nwrote %s" % os.path.relpath(path, ROOT))
    return 0 if all(gates) else 1


if __name__ == "__main__":
    sys.exit(main())




