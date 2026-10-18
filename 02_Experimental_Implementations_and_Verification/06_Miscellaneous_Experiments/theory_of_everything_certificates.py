"""
REGISTER BUNDLE CERTIFICATE (card C10)
======================================
The numeric half of the *capstone* -- not one brick but the whole conjunction.
Where ``register_ladder_certificates.py`` checks the C10 rung/side arithmetic, this
script shadows the full ``TheoryOfEverything.theoryOfEverything`` statement clause
by clause, plus both reduction theorems:

  theoryOfEverything (7 clauses)
    (1) order sets the rung:        criticalSmoothness a p = sCrit p + (1 - a)
    (2) scale-free on the family:   scalingWeight (criticalSmoothness a p) a p = 0
    (3) Serrin complementarity:     gnExponent p + sCrit p = 1/2   (p /= 0)
    (4) orientation sets the side:  (exists B, r^n A <= B) <-> r <= 1
    (5) log sgn reads the side:     (0 < log r) <-> not bounded;  (log r <= 0) <-> bounded
    (6) barrier by order:           monotone non-increasing => bounded by start;
                                    some quadratic-orbit y is unbounded
    (7) sufficiency loop:           e 0 -> (mirror step) -> for all T, e T
  twoNumbersClose (reduction)  =  clause (1) AND clause (4)
  method_and_margin_barriers   =  unique strict-antitone crossing / first crossing /
                                  no surjection alpha -> (alpha -> Bool)  (diagonal)

The proof is the Lean theorem; this is the arithmetic shadow -- and it must agree
with it.  Scope: finite sums and real arithmetic only.  No PDE, no regularity
result, no Millennium problem (see WHAT_THIS_DOES_NOT_PROVE.md).  Deterministic.
Run:  python theory_of_everything_certificates.py          (prints PASS)
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


def crit_smooth(a, p):
    """GreatAttractor.criticalSmoothness : 3/p - a."""
    return 3.0 / p - a


def scaling_weight(s, a, p):
    """GreatAttractor.scalingWeight : a + s - 3/p."""
    return a + s - 3.0 / p


def geometric(r, a, n):
    """OrientationBoundedness orbit: r^n * A."""
    return (r ** n) * a


# grids shared across clauses
ORDERS = (0.0, 0.5, 1.0, 1.75, 2.0)
FORMS = (1.5, 2.0, 2.5, 3.0, 4.0, 6.0, 8.0, 10.0, 12.0)


# ---------------------------------------------------------------------------
# clauses (1) + (2) -- order sets the rung and the homogeneous norm is scale-free
# ---------------------------------------------------------------------------


def teo_clause12_order_sets_rung():
    e_rung = 0.0
    e_weight = 0.0
    for a in ORDERS:
        for p in FORMS:
            e_rung = max(e_rung, abs(crit_smooth(a, p) - (s_crit(p) + (1.0 - a))))
            e_weight = max(e_weight, abs(scaling_weight(crit_smooth(a, p), a, p)))
    # the shift is affine in the order: a -> sCrit p + (1 - a) is injective
    e_inj = 0
    for p in FORMS:
        seen = {}
        for a in (x / 4.0 for x in range(-8, 13)):
            v = round(crit_smooth(a, p), 9)
            if v in seen and abs(seen[v] - a) > 1e-9:
                e_inj += 1
            seen[v] = a
    print("\n[C10.1-2] order sets the rung; the norm is scale-free on the family")
    print(f"  max |cs(a,p) - (sCrit p + (1-a))|               = {e_rung:.3e}")
    print(f"  max |scalW(cs(a,p),a,p)|                        = {e_weight:.3e}")
    print(f"  rung not injective in the order (violations)    = {e_inj}")
    assert e_rung < 1e-12 and e_weight < 1e-12 and e_inj == 0


# ---------------------------------------------------------------------------
# clause (3) -- Serrin interpolation exponent and the rung are complementary
# ---------------------------------------------------------------------------


def teo_clause3_serrin_complementary():
    e_sum = max(abs(gn_exp(p) + s_crit(p) - 0.5) for p in FORMS)
    print("\n[C10.3] Serrin complementarity  gnExp(p) + sCrit(p) = 1/2")
    print(f"  max |gnExp(p) + sCrit(p) - 1/2| (order one)     = {e_sum:.3e}")
    assert e_sum < 1e-12


# ---------------------------------------------------------------------------
# clauses (4) + (5) -- orientation sets the side, and log r reads that side
# ---------------------------------------------------------------------------


def teo_clause45_orientation_side():
    A = 2.0
    N = 60
    e_bound = 0
    e_sign = 0
    for r in (0.4, 0.9, 1.0, 1.001, 1.2, 3.0):
        seq = [geometric(r, A, n) for n in range(N + 1)]
        bounded = max(seq) <= A * (1.0 + 1e-12)
        if bounded != (r <= 1.0):
            e_bound += 1
        sign = math.log(r)
        if (0.0 < sign) != (not bounded):
            e_sign += 1
        if (sign <= 0.0) != bounded:
            e_sign += 1
    print("\n[C10.4-5] orientation sets the side; sign(log r) reads it")
    print(f"  (exists B, r^n A <= B) <-> r<=1 failures       = {e_bound}")
    print(f"  log-sign reads the side (failures)              = {e_sign}")
    assert e_bound == 0 and e_sign == 0


# ---------------------------------------------------------------------------
# clause (6) -- barrier by order: order <= 1 controlled, order 2 not
# ---------------------------------------------------------------------------


def teo_clause6_barrier_by_order():
    # order <= 1: a non-increasing sequence is bounded by its start
    N0 = 7.0
    mono = [N0 / (n + 1.0) for n in range(81)]
    bounded_ok = all(mono[n] <= N0 + 1e-15 for n in range(len(mono)))

    # order 2: y(n) = 2^n satisfies y(n+1) <= y(n) + y(n)^2 and is unbounded
    y = [2.0 ** n for n in range(0, 41)]
    ineq_ok = all(y[n + 1] <= y[n] + y[n] ** 2 + 1e-9
                  for n in range(len(y) - 1))
    unbounded = y[-1] > 1e9 and y[-1] > y[0]

    print("\n[C10.6] barrier by order (mono controlled vs quadratic unbounded)")
    print(f"  non-increasing bounded by its start             = {bounded_ok}")
    print(f"  y(n+1) <= y(n) + y(n)^2 for y = 2^n             = {ineq_ok}")
    print(f"  y escapes every bound (y_40)                    = {y[-1]:.3e}  grows={unbounded}")
    assert bounded_ok and ineq_ok and unbounded


# ---------------------------------------------------------------------------
# clause (7) -- the sufficiency loop closes for order <= 1
# ---------------------------------------------------------------------------


def _sufficiency_loop(N, e, T):
    """Mirror SufficiencyLoop.global_exists_of_mono: propagate e by the step rule."""
    assert e(0)
    for t in range(0, T):
        bounded_so_far = all(N(s) <= N(0) + 1e-15 for s in range(0, t + 1))
        assert bounded_so_far, "invariant left the bounded register"
        assert e(t)
        e(t + 1)  # the step hypothesis is consumed here
    return e(T)


def teo_clause7_sufficiency_loop():
    N = lambda n: 9.0 / (n + 1.0)          # a non-increasing (bounded) invariant
    e = lambda t: all(N(s) <= N(0) + 1e-15 for s in range(0, t + 1))
    horizon = 50
    ok = all(_sufficiency_loop(N, e, T) for T in range(0, horizon + 1))
    print("\n[C10.7] sufficiency loop (order <= 1): e 0 -> for all T, e T")
    print(f"  predicate survives to horizon T={horizon}        = {ok}")
    assert ok


# ---------------------------------------------------------------------------
# reduction -- twoNumbersClose = clause (1) /\ clause (4) alone
# ---------------------------------------------------------------------------


def teo_two_numbers_close():
    e_rung = max(abs(crit_smooth(a, p) - (s_crit(p) + (1.0 - a)))
                 for a in ORDERS for p in FORMS)
    e_side = 0
    for r in (0.4, 0.9, 1.0, 1.001, 1.5, 3.0):
        seq = [geometric(r, 2.0, n) for n in range(61)]
        if (max(seq) <= 2.0 * (1.0 + 1e-12)) != (r <= 1.0):
            e_side += 1
    print("\n[C10.reduction] twoNumbersClose (rung from order, side from orientation)")
    print(f"  rung clause failures                            = {e_rung:.3e}")
    print(f"  side clause failures                            = {e_side}")
    assert e_rung < 1e-12 and e_side == 0


# ---------------------------------------------------------------------------
# reduction -- method_and_margin_barriers (margin crossing + diagonal)
# ---------------------------------------------------------------------------


def teo_margin_and_method_barriers():
    # (a) unique crossing: a strictly decreasing continuous margin on [a, b].
    # The antitone hypothesis for the register's margin probe lambda(s) is ASSUMED
    # here -- it is the Navier-Stokes-specific content (T3, OPEN), and is NOT proved.
    # The strict-antitone branch therefore uses a *register-shaped stand-in*,
    #     lambda_reg(s) = C - alpha * s     with positive C, alpha
    # (C = 20.0, alpha = 3.7 below -- values consistent with the example).  This is a
    # stand-in only; branch (b), FirstCrossing, is what shows existence without it.
    C = 20.0
    alpha = 3.7

    def lambda_reg(s):
        """Register-shaped stand-in probe lambda_reg(s) = C - alpha * s."""
        return C - alpha * s

    a, b = 4.0, 6.0
    grid = [a + (b - a) * i / 4000.0 for i in range(4001)]
    crossings = sum(1 for i in range(len(grid) - 1)
                    if (lambda_reg(grid[i]) > 0.0) != (lambda_reg(grid[i + 1]) > 0.0))
    strict_anti = all(lambda_reg(grid[i]) > lambda_reg(grid[i + 1])
                      for i in range(len(grid) - 1))
    root = C / alpha

    # (b) first crossing: a *non-monotone* margin g(s) = 0.4 - (s-5.3)^2/2 - 1.2 (s-5.3)
    #     g is concave, peaks near s = 4.1, with g(4) > 0 > g(6).
    g = lambda s: 0.4 - 0.5 * (s - 5.3) ** 2 - 1.2 * (s - 5.3)
    non_monotone = any(g(grid[i]) < g(grid[i + 1]) for i in range(len(grid) - 1))
    first = next(s for s in grid if g(s) <= 0.0)
    first_ok = (0.0 < g(4.0)) and (g(6.0) < 0.0) and all(g(s) > 0.0
                for s in grid if s < first)

    # (c) diagonal: no phi : alpha -> (alpha -> Bool) is surjective  (Cantor/Lawvere)
    def no_surjection(n):
        A = range(n)
        rows = []
        # every function A -> Bool is a bitmask
        for mask in range(1 << n):
            rows.append(tuple(bool((mask >> a) & 1) for a in A))
        # every phi : A -> A -> Bool is a tuple of rows indexed by A
        for phi in __import__("itertools").product(rows, repeat=n):
            img = set(phi)
            diag = tuple(not phi[a][a] for a in A)
            if diag in img:
                return False
        return True

    diagonal_ok = all(no_surjection(n) for n in (1, 2, 3, 4))

    print("\n[C10.reduction] method_and_margin_barriers")
    print("The antitone hypothesis for lambda(s) is ASSUMED (NS-specific, T3 OPEN); "
          "FirstCrossing shows existence without it.")
    print(f"  strict-antitone unique crossing (count={crossings}, "
          f"root≈{root:.6f}) = {strict_anti and crossings == 1}")
    print(f"  non-monotone first crossing (at s≈{first:.6f})   = "
          f"{non_monotone and first_ok}")
    print(f"  no surjection alpha -> (alpha -> Bool), n=1..4  = {diagonal_ok}")
    assert strict_anti and crossings == 1
    assert non_monotone and first_ok
    assert diagonal_ok


def main():
    print("=" * 78)
    print("REGISTER BUNDLE CERTIFICATE: C10 (two numbers close the register)")
    print("=" * 78)
    teo_clause12_order_sets_rung()
    teo_clause3_serrin_complementary()
    teo_clause45_orientation_side()
    teo_clause6_barrier_by_order()
    teo_clause7_sufficiency_loop()
    teo_two_numbers_close()
    teo_margin_and_method_barriers()
    print("\n" + "=" * 78)
    print("PASS: the capstone's seven clauses hold numerically -- order sets the rung")
    print("      (scale-free family), orientation sets the side (log-sign), the barrier")
    print("      splits order<=1 (bounded) from order 2 (unbounded), the sufficiency loop")
    print("      closes, and the two barriers are a crossing and a diagonal escape.")
    print("      The wall itself (order-2 global existence) stays OPEN.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
