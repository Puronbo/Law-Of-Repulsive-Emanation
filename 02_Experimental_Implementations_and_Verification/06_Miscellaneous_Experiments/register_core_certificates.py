"""
REGISTER CORE CERTIFICATES (cards C1 and C4/C6)
===============================================
Numerical companion to the two *core* cards that pin the wall's arithmetic:

  C1     CriticalLadder          -- the scaling-critical ladder s_crit(p) = 3/p - 1
  C4/C6  ExplicitClaims /        -- one extra power tightens the marginality;
         EnstrophyBarrier /         linear (2D) bounded vs quadratic (3D) unbounded;
         QuantitativeContinuation   order sets the continuation window

Each block re-derives, in floating point, the finite real/rational arithmetic that
the corresponding Lean card proves.  The proof is the Lean theorem; this is the
arithmetic shadow -- and it must agree with it.

Scope: finite sums and real arithmetic only.  No PDE, no regularity result, no
Millennium problem (see WHAT_THIS_DOES_NOT_PROVE.md).  Seeded/deterministic.
Run:  python register_core_certificates.py          (prints PASS)
"""

import math

# ---------------------------------------------------------------------------
# shared register notation (mirrors the Lean definitions exactly)
# ---------------------------------------------------------------------------


def s_crit(p):
    """CriticalLadder.sCrit : 3/p - 1  (the order-one critical smoothness)."""
    return 3.0 / p - 1.0


def gn_exp(p):
    """SerrinLadder.gnExponent : 3/2 - 3/p  (Gagliardo-Nirenberg theta)."""
    return 1.5 - 3.0 / p


# ---------------------------------------------------------------------------
# C1 -- CriticalLadder: the arithmetic of the scaling-critical ladder
# ---------------------------------------------------------------------------


def c1_critical_ladder():
    # anchors s_crit(3)=0, s_crit(2)=1/2, s_crit(6)=-1/2
    anchors = {
        "sCrit_three": abs(s_crit(3.0) - 0.0),
        "sCrit_two": abs(s_crit(2.0) - 0.5),
        "sCrit_six": abs(s_crit(6.0) + 0.5),
        "sCrit_gt_neg_one(2)": abs((-1.0 < s_crit(2.0)) - 1.0),
        "sCrit_gt_neg_one(100)": abs((-1.0 < s_crit(100.0)) - 1.0),
    }
    # scalingInvariant_iff:  s + 1 - 3/p = 0  <->  s = s_crit(p)
    e_inv = 0
    for p in (1.5, 2.0, 2.5, 3.0, 4.0, 6.0, 9.0, 12.0):
        for s in (s_crit(p), s_crit(p) + 0.5, s_crit(p) - 0.25, 0.0, 1.0):
            lhs_zero = abs(s + 1.0 - 3.0 / p) < 1e-12
            rhs_eq = abs(s - s_crit(p)) < 1e-12
            if lhs_zero != rhs_eq:
                e_inv += 1
    # thetaAddSCrit:  theta(p) + s_crit(p) = 1/2  for every form p
    e_theta = max(abs(gn_exp(p) + s_crit(p) - 0.5)
                  for p in (2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 12.0))
    # sCrit_antitone:  p <= q  =>  s_crit(q) <= s_crit(p)
    e_anti = 0
    for p in (1.5, 2.0, 2.5, 3.0, 4.0, 6.0):
        for q in (p, p + 0.5, 2.0 * p, p + 10.0):
            if s_crit(q) > s_crit(p) + 1e-12:
                e_anti += 1
    # onsagerExcess_supercritical:  1 < 1 + eta  <->  0 < eta
    e_ons = 0
    for eta in (-2.0, -0.5, -1e-9, 0.0, 1e-9, 0.25, 1.0, 3.0):
        if (1.0 < 1.0 + eta) != (0.0 < eta):
            e_ons += 1
    print("\n[C1] CriticalLadder (the scaling-critical ladder s_crit(p) = 3/p - 1)")
    for k, v in anchors.items():
        print(f"  |{k}| = {v:.3e}")
    print(f"  scalingInvariant_iff mismatches                 = {e_inv}")
    print(f"  max |theta(p) + sCrit(p) - 1/2|                 = {e_theta:.3e}")
    print(f"  sCrit_antitone violations                       = {e_anti}")
    print(f"  onsagerExcess_supercritical mismatches          = {e_ons}")
    assert max(anchors.values()) < 1e-12
    assert e_inv == 0 and e_theta < 1e-12 and e_anti == 0 and e_ons == 0
    print("  -> one invariant pattern (s_crit) with fixed arithmetic in every guise;")
    print("     the wall itself (boundedness of the norm) stays OPEN.")


# ---------------------------------------------------------------------------
# C4/C6 -- ExplicitClaims: one extra power strengthens exactly above unit level
# ---------------------------------------------------------------------------


def c46_extra_power():
    # extra_power_strengthens_above_unit:  z <= z^(1+eps)  <->  1 <= z   (z>0, eps>0)
    e_pow = 0
    for eps in (0.1, 0.5, 1.0, 2.0):
        for z in (0.01, 0.25, 0.5, 0.999, 1.0, 1.001, 1.5, 2.0, 10.0):
            lhs = z <= (z ** (1.0 + eps)) * (1.0 + 1e-12)
            rhs = 1.0 <= z * (1.0 + 1e-12)
            if lhs != rhs:
                e_pow += 1
    # the excess vanishes exactly at the borderline z = 1
    excess = [z ** (1.0 + 1.0) - z for z in (0.5, 0.9, 1.0, 1.1, 2.0)]
    print("\n[C4/C6] ExplicitClaims (one extra power tightens above unit level)")
    print(f"  z <= z^(1+eps) <-> 1 <= z mismatches            = {e_pow}")
    print(f"  excess z^(2)-z on [0.5,0.9,1.0,1.1,2.0]        = "
          f"{[round(x, 4) for x in excess]}")
    assert e_pow == 0
    assert abs(excess[2]) < 1e-15 and excess[0] < 0 and excess[4] > 0
    print("  -> int Z^(1+eps) dt < inf is strictly stronger than int Z dt < inf,")
    print("     and it bites exactly in the intermittent regime Z > 1.")


# ---------------------------------------------------------------------------
# C4/C6 -- EnstrophyBarrier + QuantitativeContinuation: order sets the bound
# ---------------------------------------------------------------------------


def _mono_step_bounded(y, N):
    """A non-increasing sequence is bounded by its start (2D enstrophy shape)."""
    return all(y[n] <= y[0] + 1e-15 for n in range(N + 1))


def c46_barrier_hierarchy():
    # doubling_succ:  doubling(A, n+1) = 2 * doubling(A, n)
    A = 1.0
    doubling = lambda n: A * (2.0 ** n)
    e_dbl = max(abs(doubling(n + 1) - 2.0 * doubling(n)) for n in range(30))
    # mono_step_bounded (2D):  non-increasing -> bounded by start
    N = 60
    mono = [5.0 / (n + 1.0) for n in range(N + 1)]
    m2 = _mono_step_bounded(mono, N)
    # linear_bound (order 0):  N_(n+1) <= N_n + C  =>  N_t <= N_0 + C t
    e_lin = 0.0
    C, N0 = 1.25, 3.0
    Nn = N0
    for t in range(0, 40):
        e_lin = max(e_lin, Nn - (N0 + C * t))
        Nn = Nn + C
    # geometric_bound (order 1):  N_(n+1) <= (1+C) N_n  =>  N_t <= (1+C)^t N_0
    # (compared relatively: the bound itself grows large, so absolute rounding grows)
    e_geo = 0.0
    Ng = N0
    for t in range(0, 40):
        bound = ((1.0 + C) ** t) * N0
        e_geo = max(e_geo, (Ng - bound) / max(1.0, bound))
        Ng = (1.0 + C) * Ng
    # exists_upto_of_geometric window: the explicit bound (1+C)^T N_0 must
    # dominate the value at every s <= T (so it feeds the continuation engine)
    T = 25
    window = ((1.0 + C) ** T) * N0
    e_win = max((((1.0 + C) ** s) * N0 - window) / max(1.0, window)
                for s in range(0, T + 1))
    # quadratic_step_unbounded (order 2, 3D shape):  y_n = A 2^n, C*A >= 1,
    # satisfies y_(n+1) <= y_n + C y_n^2 and is unbounded
    Cq, Aq = 1.0, 1.0
    quad = [Aq * (2.0 ** n) for n in range(0, 31)]
    ok_ineq = all(quad[n + 1] <= quad[n] + Cq * quad[n] ** 2 + 1e-9
                  for n in range(len(quad) - 1))
    grows = quad[-1] > 1e9 and quad[-1] > quad[0]
    print("\n[C4/C6] EnstrophyBarrier + QuantitativeContinuation (order sets the bound)")
    print(f"  max |doubling(A,n+1) - 2 doubling(A,n)|         = {e_dbl:.3e}")
    print(f"  2D: non-increasing bounded by start             = {m2}")
    print(f"  order 0: max (N_t - (N_0 + C t)) (should be <=0)= {e_lin:.3e}")
    print(f"  order 1: max (N_t - (1+C)^t N_0) (should be <=0)= {e_geo:.3e}")
    print(f"  window bound (1+C)^T N_0 at T={T}               = {window:.6e}")
    print(f"  order 2: doubling satisfies quadratic increment = {ok_ineq}")
    print(f"   order 2: y escapes any bound (y_30)            = {quad[-1]:.6e}  grows={grows}")
    assert e_dbl < 1e-9 and m2
    assert e_lin <= 1e-9 and e_geo <= 1e-9 and abs(e_win) < 1e-9
    assert ok_ineq and grows
    print("  -> order 0/1 increments are bounded on every window (linear/geometric),")
    print("     order 2 (the 3D shape) is not: the continuation engine cannot start.")


def main():
    print("=" * 78)
    print("REGISTER CORE CERTIFICATES: C1 / C4-C6")
    print("=" * 78)
    c1_critical_ladder()
    c46_extra_power()
    c46_barrier_hierarchy()
    print("\n" + "=" * 78)
    print("PASS: C1 critical-ladder arithmetic; C4/C6 extra-power marginality and the")
    print("      order-0/1/2 barrier hierarchy (2D bounded vs 3D blow-up-capable).")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
