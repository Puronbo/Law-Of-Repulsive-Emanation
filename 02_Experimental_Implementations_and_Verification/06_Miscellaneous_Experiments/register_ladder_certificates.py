"""
REGISTER LADDER CERTIFICATES (cards C9 / C10 / C11 / C23 / C24 / C33)
======================================================================
Numerical companion to the "two numbers" family: the order ladder, the
orientation wall, and emergent time.  Each block re-derives, in floating point,
the finite real/rational arithmetic that the corresponding Lean card proves.
The proof is the Lean theorem; this is the arithmetic shadow -- and it must
agree with it.

  C9  OrientationBoundedness  -- a geometric orbit r^n A is bounded iff r <= 1
  C10  TheoryOfEverything       -- order sets the rung, orientation sets the side
  C11  EmergentTime             -- a transfer conserves the total; n is the clock
  C23  SerrinLadder             -- the interpolation/companion exponent arithmetic
  C24  GreatAttractor           -- distance ratio -> |L|; scaling weight algebra
  C33  OnePattern               -- one order-one ladder shifted by the order a

Scope: finite sums and real arithmetic only.  No PDE, no regularity result, no
Millennium problem (see WHAT_THIS_DOES_NOT_PROVE.md).  Seeded/deterministic.
Run:  python register_ladder_certificates.py          (prints PASS)
"""

import math

# ---------------------------------------------------------------------------
# shared register notation (mirrors the Lean definitions exactly)
# ---------------------------------------------------------------------------


def gn_exp(p):
    """SerrinLadder.gnExponent : 3/2 - 3/p  (Gagliardo-Nirenberg theta)."""
    return 1.5 - 3.0 / p


def s_crit(p):
    """CriticalLadder.sCrit : 3/p - 1  (the order-one critical smoothness)."""
    return 3.0 / p - 1.0


def crit_smooth(a, p):
    """GreatAttractor.criticalSmoothness : 3/p - a."""
    return 3.0 / p - a


def scaling_weight(s, a, p):
    """GreatAttractor.scalingWeight : a + s - 3/p."""
    return a + s - 3.0 / p


def serrin_q(p):
    """SerrinLadder.serrinQ : 2p/(p-3)."""
    return 2.0 * p / (p - 3.0)


def s_crit_n(d, p):
    """EmergentTime.sCritN : d/p - 1 (d = dimension; d=3 recovers s_crit)."""
    return d / p - 1.0


def scaling_weight_n(s, a, d, p):
    """EmergentTime.scalingWeightN : a + s - d/p."""
    return a + s - d / p


def geometric(r, a, n):
    return (r ** n) * a


# ---------------------------------------------------------------------------
# C9 -- OrientationBoundedness: orientation decides boundedness
# ---------------------------------------------------------------------------


def c11_orientation_boundedness():
    A = 3.0
    N = 50
    worst_bounded = 0.0
    worst_unbounded = math.inf
    for r in (0.5, 0.9, 1.0, 1.0):
        seq = [geometric(r, A, n) for n in range(N + 1)]
        worst_bounded = max(worst_bounded, max(seq) / A)   # r<=1 => <= A
        # log r <= 0  <->  bounded
        assert (math.log(r) <= 0.0) == (max(seq) <= A * (1.0 + 1e-12))
    for r in (1.05, 1.5, 2.0):
        seq = [geometric(r, A, n) for n in range(N + 1)]
        worst_unbounded = min(worst_unbounded, seq[-1] / A)
        # log r > 0  <->  unbounded (the sequence escapes its own start)
        assert (math.log(r) > 0.0) == (seq[-1] > seq[0] * (1.0 + 1e-9))
        # repelling: each step moves AWAY from x0 (distance ratio = r)
        ratios = [seq[n] / seq[n - 1] for n in range(1, N + 1)]
        assert all(abs(ratio - r) < 1e-12 for ratio in ratios)
    print("\n[C9] OrientationBoundedness")
    print(f"  max r^n/A over r<=1 (should be <= 1)            = {worst_bounded:.6f}")
    print(f"  min final value / A over r>1 (should be >> 1)   = {worst_unbounded:.6e}")
    print("  -> geometric orbits are bounded iff r <= 1; the log sign reads the side.")


# ---------------------------------------------------------------------------
# C10 -- TheoryOfEverything: two numbers close the register
# ---------------------------------------------------------------------------


def c12_theory_of_everything():
    vals_a = (0.0, 0.5, 1.0, 1.75, 2.0)
    vals_p = (2.0, 3.0, 4.0, 6.0, 8.0, 10.0)
    e_rung = e_weight = e_sum = 0.0
    for a in vals_a:
        for p in vals_p:
            e_rung = max(e_rung, abs(crit_smooth(a, p) - (s_crit(p) + (1.0 - a))))
            e_weight = max(e_weight, abs(scaling_weight(crit_smooth(a, p), a, p)))
            e_sum = max(e_sum, abs(gn_exp(p) + s_crit(p) - 0.5))
    # clause 4/5: boundedness and its log sign, over a radius grid
    e_bound = 0
    for r in (0.4, 0.9, 1.0, 1.001, 1.2, 3.0):
        seq = [(r ** n) * 2.0 for n in range(60)]
        bounded = max(seq) <= 2.0 * (1.0 + 1e-12)
        claim = r <= 1.0
        if bounded != claim:
            e_bound += 1
        sign = math.log(r)
        if (sign > 0) != (not bounded):
            e_bound += 1
        if (sign <= 0) != bounded:
            e_bound += 1
    print("\n[C10] TheoryOfEverything (order sets the rung, orientation the side)")
    print(f"  max |cs(a,p) - (sCrit p + (1-a))|               = {e_rung:.3e}")
    print(f"  max |scalW(cs(a,p),a,p)|                        = {e_weight:.3e}")
    print(f"  max |gnExp(p) + sCrit(p) - 1/2|                 = {e_sum:.3e}")
    print(f"  boundedness/log-sign clause failures            = {e_bound}")
    assert e_rung < 1e-12 and e_weight < 1e-12 and e_sum < 1e-12 and e_bound == 0
    print("  -> the rung comes from the order a, the side from the orientation r.")


# ---------------------------------------------------------------------------
# C11 -- EmergentTime: a transfer conserves the total, n is the clock
# ---------------------------------------------------------------------------


def c13_emergent_time():
    hot, cold, delta = 10.0, 4.0, 1.5
    total = hot + cold
    # transfer conserves the total
    t = (hot - delta, cold + delta)
    e_cons = abs((t[0] + t[1]) - total)
    # n iterations: state = (hot - n*delta, cold + n*delta)
    worst_state = 0.0
    state = (hot, cold)
    for n in range(1, 21):
        state = (state[0] - delta, state[1] + delta)
        worst_state = max(worst_state,
                          abs(state[0] - (hot - n * delta)),
                          abs(state[1] - (cold + n * delta)))
        assert abs((state[0] + state[1]) - total) < 1e-12
    # the change exponent grows with the dimension
    exps = [s_crit_n(d, 6.0) for d in (1, 2, 3, 4, 5)]
    mono = all(exps[i] < exps[i + 1] for i in range(len(exps) - 1))
    e_ladder = abs(s_crit_n(3.0, 4.0) - s_crit(4.0))
    # order one vanishes in every dimension
    e_w = max(abs(scaling_weight_n(s_crit_n(d, p), 1.0, d, p))
              for d in (1.0, 2.0, 3.0, 4.0) for p in (3.0, 5.0, 7.0))
    print("\n[C11] EmergentTime (transfer conserves the total; n is the clock)")
    print(f"  |(transfer d r).total - r.total|                = {e_cons:.3e}")
    print(f"  max |state after n steps - (hot-n*d, cold+n*d)| = {worst_state:.3e}")
    print(f"  sCritN(d,p): {[round(x, 4) for x in exps]}  increasing = {mono}")
    print(f"  |sCritN(3,p) - sCrit(p)|                        = {e_ladder:.3e}")
    print(f"  max |scalWN(sCritN, a=1, d, p)|                 = {e_w:.3e}")
    assert e_cons < 1e-12 and worst_state < 1e-12 and mono and e_ladder < 1e-12
    assert e_w < 1e-12
    print("  -> the total is conserved by every transfer and the count n fixes the state.")


# ---------------------------------------------------------------------------
# C23 -- SerrinLadder: the exponent arithmetic
# ---------------------------------------------------------------------------


def c25_serrin_ladder():
    checks = {
        "gnExponent_six": abs(gn_exp(6.0) - 1.0),
        "gnExponent_two": abs(gn_exp(2.0) - 0.0),
        "gnExponent_three_half": abs(gn_exp(3.0) - 0.5),
        "ceiling_theta3": abs(gn_exp(3.0) - 0.5),
        "ceiling_theta6": abs(gn_exp(6.0) - 1.0),
        "ceiling_theta8": abs(gn_exp(8.0) - 9.0 / 8.0),
        "serrinQ_six": abs(serrin_q(6.0) - 4.0),
        "criticalPower_six_four": abs(gn_exp(6.0) * serrin_q(6.0) / 2.0 - 2.0),
        "oneExtraPower": abs(gn_exp(6.0) * serrin_q(6.0) / 2.0 - 1.0 - 1.0),
    }
    # identities over a p grid (p != 0, 3)
    ps = [x * 0.5 for x in range(4, 41) if abs(x * 0.5 - 3.0) > 1e-9]
    e_line = max(abs(2.0 / serrin_q(p) + 3.0 / p - 1.0) for p in ps)
    e_id = max(abs(gn_exp(p) * serrin_q(p) / 2.0
                   - 3.0 * (p - 2.0) / (2.0 * (p - 3.0))) for p in ps)
    e_le = 0
    for p in ps:
        if p <= 0:
            continue
        claim = (gn_exp(p) <= 1.0 + 1e-12) == (p <= 6.0)
        if not claim:
            e_le += 1
    # powerClosesCriticalAtSix : (1+eps >= theta6*q6/2) <-> 1 <= eps
    e_close = 0
    for eps in (-1.5, -1.0, -0.25, 0.0, 0.5, 1.0, 2.0):
        lhs = (1.0 + eps >= gn_exp(6.0) * serrin_q(6.0) / 2.0 - 1e-15)
        if lhs != (1.0 <= eps + 1e-15):
            e_close += 1
    print("\n[C23] SerrinLadder (interpolation / companion exponents)")
    for k, v in checks.items():
        print(f"  |{k}| = {v:.3e}")
    print(f"  max |2/q(p)+3/p - 1|                            = {e_line:.3e}")
    print(f"  max |theta*q/2 - 3(p-2)/(2(p-3))|               = {e_id:.3e}")
    print(f"  gnExponent_le_one_iff failures                  = {e_le}")
    print(f"  powerClosesCriticalAtSix failures               = {e_close}")
    assert max(checks.values()) < 1e-12
    assert e_line < 1e-12 and e_id < 1e-12 and e_le == 0 and e_close == 0
    print("  -> theta(6)=1, q(6)=4, the identity holds for all p, and only p<=6 "
          "\n     gives theta <= 1 (one extra power closes the (6,4) route).")


# ---------------------------------------------------------------------------
# C24 -- GreatAttractor: orientation of a fixed point + the scaling algebra
# ---------------------------------------------------------------------------


def c26_great_attractor():
    # a linear map with derivative L fixing x0: T x = x0 + L (x - x0)
    x0 = 1.0
    e_ratio = e_rate = e_rep = 0.0
    for L in (-2.5, -1.4, -0.6, 0.3, 0.7, 1.3, 2.0):
        repels, attracts = [], []
        for k in range(1, 6):
            x = x0 + (0.25 / k) * (1.0 if L >= 0 else -1.0)
            Tx = x0 + L * (x - x0)
            d, dT = abs(x - x0), abs(Tx - x0)
            e_ratio = max(e_ratio, abs(dT / d - abs(L)))
            e_rate = max(e_rate, abs(math.log(dT) - math.log(d) - math.log(abs(L))))
            repels.append(dT > d)
            attracts.append(dT < d)
        # orientation is decided by |L| alone (trichotomy + sign of log|L|)
        assert all(r for r in repels) if abs(L) > 1.0 else not any(repels)
        assert all(attracts) if abs(L) < 1.0 else not any(attracts)
        e_rep = max(e_rep, 0.0 if ((math.log(abs(L)) > 0) == (abs(L) > 1.0)) else 1.0)
    # scaling algebra
    e_shift = e_ant = e_zero = e_one = 0.0
    for a in (0.0, 0.5, 1.0, 1.5, 2.5):
        for p in (2.0, 3.0, 4.0, 6.0, 8.0):
            e_shift = max(e_shift,
                          abs(crit_smooth(a + 1.0, p) - (crit_smooth(a, p) - 1.0)))
            e_one = max(e_one, abs(crit_smooth(1.0, p) - s_crit(p)))
            e_zero = max(e_zero, abs(scaling_weight(crit_smooth(a, p), a, p)))
            for b in (a, a + 0.75, a + 2.0):
                if a <= b and crit_smooth(b, p) > crit_smooth(a, p):
                    e_ant += 1.0
    print("\n[C24] GreatAttractor (distance ratio -> |L|, orientation, scaling weight)")
    print(f"  max | |Tx-x0|/|x-x0| - |L| |                   = {e_ratio:.3e}")
    print(f"  max | log|Tx-x0| - log|x-x0| - log|L| |         = {e_rate:.3e}")
    print(f"  orientation/log-sign mismatches                 = {e_rep:.3e}")
    print(f"  shift identity errors (cs(a+1)=cs(a)-1)         = {e_shift:.3e}")
    print(f"  antitone violations                             = {e_ant:.1f}")
    print(f"  |cs(1,p)-sCrit(p)|                              = {e_one:.3e}")
    print(f"  max |scalW(cs(a,p),a,p)|                        = {e_zero:.3e}")
    assert e_ratio < 1e-12 and e_rate < 1e-12 and e_rep == 0.0
    assert e_shift < 1e-12 and e_ant == 0.0 and e_one < 1e-12 and e_zero < 1e-12
    print("  -> |L| decides repulsion/attraction and the order a slides the rung by "
          "\n     exactly one per unit of order.")


# ---------------------------------------------------------------------------
# C33 -- OnePattern: one ladder shifted by the order
# ---------------------------------------------------------------------------


def c35_one_pattern():
    e_curve = e_one = e_theta = e_theta1 = e_w = 0.0
    for a in (0.0, 0.25, 0.5, 1.0, 1.75, 3.0):
        for p in (2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 12.0):
            e_curve = max(e_curve, abs(crit_smooth(a, p) - (s_crit(p) + (1.0 - a))))
            e_one = max(e_one, abs(crit_smooth(1.0, p) - s_crit(p)))
            e_theta = max(e_theta, abs(gn_exp(p) + crit_smooth(a, p)
                                       - (0.5 + (1.0 - a))))
            e_theta1 = max(e_theta1, abs(gn_exp(p) + crit_smooth(1.0, p) - 0.5))
            e_w = max(e_w, abs(scaling_weight(crit_smooth(a, p), a, p)))
    print("\n[C33] OnePattern (one order-one ladder, shifted by the order)")
    print(f"  max |cs(a,p) - (sCrit p + (1-a))|               = {e_curve:.3e}")
    print(f"  max |cs(1,p) - sCrit(p)|                        = {e_one:.3e}")
    print(f"  max |theta(p) + cs(a,p) - (1/2 + (1-a))|        = {e_theta:.3e}")
    print(f"  max |theta(p) + cs(1,p) - 1/2|                  = {e_theta1:.3e}")
    print(f"  max |scalW(cs(a,p),a,p)|                        = {e_w:.3e}")
    assert max(e_curve, e_one, e_theta, e_theta1, e_w) < 1e-12
    print("  -> every rung is the same ladder translated by the order; the family is "
          "\n     scale-free exactly on the ladder.")


def main():
    print("=" * 78)
    print("REGISTER LADDER CERTIFICATES: C9 / C10 / C11 / C23 / C24 / C33")
    print("=" * 78)
    c11_orientation_boundedness()
    c12_theory_of_everything()
    c13_emergent_time()
    c25_serrin_ladder()
    c26_great_attractor()
    c35_one_pattern()
    print("\n" + "=" * 78)
    print("PASS: C9 boundedness-by-orientation; C10 two-number closure; C11 transfer "
          "conservation;\n      C23 ladder exponents; C24 fixed-point orientation + "
          "scaling algebra; C33 one pattern.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
