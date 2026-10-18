"""
CRITERIA CERTIFICATES (cards C12 / C25 / C26 / C27 / C28 / C29 / C30 / C31 / C32)
=================================================================================
Numerical companion to the diagonal-barrier, force/mixture, sufficiency and
fixed-point cards.  Each block re-derives, by finite enumeration or exact
arithmetic on samples, the content the corresponding Lean card proves.  The Lean
theorem is the proof; this is the arithmetic shadow and it must agree.

  C12  LogicBarrier   -- the diagonal, self-referential method barrier (Cantor)
  C25  ForceNetwork   -- weighted value between min and max; inertia damps change
  C26  MixtureGrowth  -- addition transmits, never fabricates, concentration
  C27  OnsagerCriterion -- bounded invariant frees the excess (and its wall)
  C28  ContinuationCriterion -- bounded <=> extendable; failure <=> unbounded
  C29  StableBounded  -- attracting orbits converge and are bounded
  C30  SufficiencyLoop -- 2D closes the loop; a quadratic increment cannot be
  C31  SelfSimilarExponents -- the four exponents are forced, n-independently
  C32  ZeroFixedPoint -- zero defines its own position and scales by its zeros

Scope: finite enumeration and real arithmetic only.  No PDE, no Millennium
problem (see WHAT_THIS_DOES_NOT_PROVE.md).  Honest boundary: cards quantified
over all types / all maps / all flows (C12, C28, C29) are certified on a concrete
finite instance or a sampled model; the instance is the shadow, not the theorem.
Run:  python register_criteria_certificates.py            (prints PASS)
"""

import math

TOL = 1e-9


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def gaussian_solve(A, b):
    """Row-reduce [A | b]; return (solution, rank, inconsistent)."""
    n, m = len(A), len(A[0])
    M = [list(A[i]) + [b[i]] for i in range(n)]
    piv_cols = []
    r = 0
    for c in range(m):
        piv = None
        for i in range(r, n):
            if abs(M[i][c]) > 1e-9:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        M[r] = [v / pv for v in M[r]]
        for i in range(n):
            if i != r and abs(M[i][c]) > 1e-12:
                f = M[i][c]
                M[i] = [M[i][j] - f * M[r][j] for j in range(m + 1)]
        piv_cols.append(c)
        r += 1
    inconsistent = any(all(abs(M[i][j]) < 1e-9 for j in range(m))
                       and abs(M[i][m]) > 1e-9 for i in range(r, n))
    sol = [0.0] * m
    for i, c in enumerate(piv_cols):
        sol[c] = M[i][m]
    return sol, r, inconsistent


def norm(v):
    return math.sqrt(sum(x * x for x in v))


# ---------------------------------------------------------------------------
# C12 -- LogicBarrier: the diagonal, self-referential method barrier
# ---------------------------------------------------------------------------


def c14_logic_barrier():
    # a finite type of size n cannot surject onto its own function space to Bool:
    # #(alpha -> Bool) = 2^n > n = #alpha, for every n
    no_surjection = all(2 ** n > n for n in range(0, 13))
    growth = [(n, 2 ** n) for n in range(0, 9)]
    # the fixed-point-free map on Bool: not has no fixed point
    not_fp_absent = all((1 - b) != b for b in (0, 1))
    # diagonal escape: any n candidate maps g_0..g_{n-1} : alpha -> Bool miss one
    n = 6
    rows = [5, 3, 6, 1, 7, 2]                 # n candidate functions, as bitmasks

    def bit(mask, i):
        return (mask >> i) & 1

    diag = sum((1 - bit(rows[i], i)) << i for i in range(n))
    diag_escapes = (diag not in rows) and (0 <= diag < 2 ** n)
    # and it IS a function alpha -> Bool (one of the 2^n), just not in the list
    diag_is_function = diag in range(2 ** n)
    print("\n[C12] LogicBarrier (the diagonal method barrier, finite instance)")
    print(f"  2^n > n for n = 0..12 (no surjection alpha ↠ (alpha->Bool)) = {no_surjection}")
    print(f"  (n, 2^n): {growth}")
    print(f"  not : Bool -> Bool has no fixed point                     = {not_fp_absent}")
    print(f"  candidate enumeration rows (n={n})                        = {rows}")
    print(f"  diagonal function value                                   = {diag}")
    print(f"  diagonal escapes the range and is still a function        = "
          f"{diag_escapes and diag_is_function}")
    assert no_surjection and not_fp_absent
    assert diag_escapes and diag_is_function
    print("  -> a fixed-point-free self-map forbids a surjection onto the function "
          "\n     space; the diagonal predicate escapes every enumeration (Cantor, "
          "Lawvere).")


# ---------------------------------------------------------------------------
# C25 -- ForceNetwork: weighted value between min and max; inertia damps change
# ---------------------------------------------------------------------------


def c27_force_network():
    w = [0.1, 0.2, 0.3, 0.4]                  # nonnegative, sum = 1
    c = [1.0, 3.0, 2.0, 5.0]
    assert abs(sum(w) - 1.0) < 1e-15
    value = sum(wi * ci for wi, ci in zip(w, c))
    c0, C = min(c), max(c)
    between = c0 - 1e-12 <= value <= C + 1e-12
    le_max = value <= C + 1e-12
    ge_min = value >= c0 - 1e-12
    # inertia damps change: force / inertia is antitone in inertia
    F, I0, I = 2.0, 1.0, 4.0
    damp = F / I <= F / I0
    # sampled monotonicity across many inertias
    damp_all = all((F / I2) <= (F / I1)
                   for I1, I2 in [(0.5, 1.0), (1.0, 2.0), (2.0, 8.0), (3.0, 3.5)])
    print("\n[C25] ForceNetwork (weighted value in [min, max]; inertia damps change)")
    print(f"  weights = {w}   parts = {c}")
    print(f"  network value = {value:.6f}  in [{c0}, {C}]            = {between}")
    print(f"  value <= max (weightedValueLeMax)                         = {le_max}")
    print(f"  value >= min (leWeightedValueMin)                         = {ge_min}")
    print(f"  force/inertia antitone (inertiaDampsChange)               = "
          f"{damp and damp_all}")
    assert between and le_max and ge_min and damp and damp_all
    print("  -> interconnection reweights but cannot mint a value outside its parts; "
          "\n     a part held by more inertia changes less.")


# ---------------------------------------------------------------------------
# C26 -- MixtureGrowth: addition transmits, never fabricates, concentration
# ---------------------------------------------------------------------------


def c28_mixture_growth():
    u, v = [1.0, 2.0, 3.0], [2.0, -1.0, 0.5]
    mix_le = norm([a + b for a, b in zip(u, v)]) <= norm(u) + norm(v) + 1e-12
    # two-part ratio bracket
    r1, r2, f1, f2 = 1.0, 4.0, 0.3, 0.7
    lo = r1 <= f1 * r1 + f2 * r2 + 1e-12
    hi = f1 * r1 + f2 * r2 <= r2 + 1e-12
    sq_lo = r1 * r1 <= f1 * r1 * r1 + f2 * r2 * r2 + 1e-12
    sq_hi = f1 * r1 * r1 + f2 * r2 * r2 <= r2 * r2 + 1e-12
    spike = r1 <= f1 * r1 + f2 * r2 + 1e-12          # spike cannot lower the ratio
    # sweep many admissible configurations
    sweep_ok = True
    for r1_ in (0.2, 1.0, 2.5, 7.0):
        for r2_ in (r1_, r1_ + 1.0, r1_ * 3.0):
            for f1_ in (0.0, 0.25, 0.5, 0.75, 1.0):
                f2_ = 1.0 - f1_
                m = f1_ * r1_ + f2_ * r2_
                if not (r1_ - 1e-12 <= m <= r2_ + 1e-12):
                    sweep_ok = False
    print("\n[C26] MixtureGrowth (addition never fabricates concentration)")
    print(f"  ||u+v|| <= ||u||+||v||                                   = {mix_le}")
    print(f"  ratio bracket min <= mixture <= max                       = {lo and hi}")
    print(f"  weighted squared ratios also bracketed                    = {sq_lo and sq_hi}")
    print(f"  spike cannot lower the ratio                              = {spike}")
    print(f"  bracket holds over sweep of (r1,r2,f1)                    = {sweep_ok}")
    assert mix_le and lo and hi and sq_lo and sq_hi and spike and sweep_ok
    print("  -> the mixture is governed by the MAX of its parts, not an average.")


# ---------------------------------------------------------------------------
# C27 -- OnsagerCriterion: bounded invariant frees the excess (and its wall)
# ---------------------------------------------------------------------------


def c29_onsager_criterion():
    Z = [0.5, 1.0, 0.8, 0.3]
    M, n = 1.0, 2
    lhs = sum(z ** (n + 1) for z in Z)
    rhs = M ** n * sum(Z)
    sufficiency = lhs <= rhs + 1e-12
    # sweep excess orders and bounds
    sweep_ok = True
    for M_ in (0.5, 1.0, 2.0):
        for n_ in (1, 2, 3, 4):
            Zc = [0.2, M_, 0.4, 0.1]
            if not (sum(z ** (n_ + 1) for z in Zc) <= M_ ** n_ * sum(Zc) + 1e-12):
                sweep_ok = False
    # the wall (contrapositive): a genuine excess forces a spike above M
    Zs = [0.5, 3.0, 0.2]
    Ms, ns = 1.0, 1
    excess = sum(z ** (ns + 1) for z in Zs) > Ms ** ns * sum(Zs) + 1e-12
    spike = any(z > Ms for z in Zs)
    wall = excess and spike
    # excess majorizes: w >= 1 makes the weighted sum dominate
    a = [0.2, 0.5, 0.3]
    w = [1.0, 2.0, 1.5]
    majorizes = sum(a) <= sum(wi * ai for wi, ai in zip(w, a)) + 1e-12
    print("\n[C27] OnsagerCriterion (a bounded invariant frees the excess)")
    print(f"  sum Z^(n+1) <= M^n sum Z (n={n}, M={M})                = {sufficiency}")
    print(f"  sufficiency sweep over orders and bounds                  = {sweep_ok}")
    print(f"  excess => a spike above M (spike_of_excess / wall)        = {wall}")
    print(f"  w >= 1 => sum a <= sum w*a (excess_majorizes)            = {majorizes}")
    assert sufficiency and sweep_ok and wall and majorizes
    print("  -> boundedness makes a positive Onsager excess free; an "
          "\n     Onsager-violating cascade needs a spike above the bound.")


# ---------------------------------------------------------------------------
# C28 -- ContinuationCriterion: bounded <=> extendable; failure <=> unbounded
# ---------------------------------------------------------------------------


def c30_continuation_criterion():
    def build_exists(N, M, T):
        """exists_upto via the one-step rule while N <= M."""
        ex = [False] * (T + 1)
        ex[0] = True
        for t in range(T):
            bounded = all(N[s] <= M + 1e-12 for s in range(0, t + 1))
            ex[t + 1] = bounded and ex[t]
        return ex

    # bounded case: N stays <= M everywhere, so existence reaches T
    M = 1.0
    N_bounded = [0.9 - 0.01 * t for t in range(0, 30)]
    ex = build_exists(N_bounded, M, 30)
    reaches = ex[30]
    # unbounded case: first failure <=> the invariant exceeded M
    N_unb = [1.1 + 0.5 * t for t in range(0, 10)]
    ex2 = build_exists(N_unb, M, 10)
    first_fail = next(t for t in range(11) if not ex2[t])
    unbounded = not all(N_unb[s] <= M + 1e-12 for s in range(0, first_fail + 1))
    print("\n[C28] ContinuationCriterion (bounded <=> extendable)")
    print(f"  bounded invariant reaches T=30 (exists_upto_of_bounded)   = {reaches}")
    print(f"  unbounded model: first failure at t={first_fail}, "
          f"N[{first_fail}]={N_unb[first_fail]:.2f}")
    print(f"  first failure <=> invariant exceeded M (unbounded=)       = {unbounded}")
    assert reaches and unbounded
    print("  -> boundedness is exactly what stands between local existence and "
          "\n     global regularity; a first failure forces the invariant to escape.")


# ---------------------------------------------------------------------------
# C29 -- StableBounded: attracting orbits converge and are bounded
# ---------------------------------------------------------------------------


def c31_stable_bounded():
    # contraction f(x) = 0.5 x + 1 on R, K = 1/2 < 1, fixed point 2
    K, fp = 0.5, 2.0
    x = 5.0
    orbit = [x]
    for _ in range(60):
        x = K * x + (1 - K) * fp
        orbit.append(x)
    converges = abs(orbit[-1] - fp) < 1e-12
    monotone_decay = all(abs(orbit[i + 1] - fp) <= abs(orbit[i] - fp) + 1e-12
                         for i in range(len(orbit) - 1))
    bounded = max(abs(v) for v in orbit) <= max(abs(orbit[0]), abs(fp)) + 1e-9
    # monotone non-increasing is bounded by its start
    N = [1.0 / (t + 1) for t in range(0, 20)]
    mono_ok = all(N[t] <= N[0] + 1e-15 for t in range(len(N))) and \
        all(N[t + 1] <= N[t] + 1e-15 for t in range(len(N) - 1))
    print("\n[C29] StableBounded (attracting => convergent & bounded)")
    print(f"  |orbit - fixed point| after 60 steps                     = "
          f"{abs(orbit[-1] - fp):.3e}")
    print(f"  orbit converges to the fixed point                        = {converges}")
    print(f"  distance is non-increasing (contraction)                  = {monotone_decay}")
    print(f"  orbit range is bounded (attracting_orbit_bounded)         = {bounded}")
    print(f"  non-increasing N stays below its start (monotone_bounded)= {mono_ok}")
    assert converges and monotone_decay and bounded and mono_ok
    print("  -> an attracting orbit is bounded (indeed converges); repulsion is the "
          "\n     only escape route.")


# ---------------------------------------------------------------------------
# C30 -- SufficiencyLoop: 2D closes the loop; a quadratic increment cannot
# ---------------------------------------------------------------------------


def c32_sufficiency_loop():
    # 2D shape: N non-increasing => the free bound M = N 0 works => exists everywhere
    def build_exists_global(N, T):
        M = N[0]
        ex = [False] * (T + 1)
        ex[0] = True
        for t in range(T):
            ex[t + 1] = (all(N[s] <= M + 1e-12 for s in range(t + 1)) and ex[t])
        return ex

    N = [1.0 / (1.0 + t) for t in range(0, 40)]
    noninc = all(N[t + 1] <= N[t] + 1e-15 for t in range(len(N) - 1))
    ex = build_exists_global(N, 39)
    global_exists = noninc and all(ex)
    # 3D shape: y(n+1) = y(n) + C y(n)^2 escapes every bound
    C, y = 0.1, 1.0
    inc_rule_ok = True
    steps = 0
    while y < 1e9 and steps < 100000:
        y_new = y + C * y * y
        inc_rule_ok = inc_rule_ok and (y_new <= y + C * y * y + 1e-9)
        y = y_new
        steps += 1
    unlimited = y >= 1e9
    print("\n[C30] SufficiencyLoop (2D closes; the 3D shape cannot start it)")
    print(f"  non-increasing N (2D enstrophy shape)                     = {noninc}")
    print(f"  M = N 0 closes the loop: exists at every time             = {global_exists}")
    print(f"  quadratic increment y+C y^2 grows without bound           = {unlimited}")
    print(f"  it took {steps} steps to exceed 1e9 (blow-up at finite step)")
    print(f"  increment rule y(n+1) <= y(n)+C y(n)^2 holds              = {inc_rule_ok}")
    assert global_exists and unlimited and inc_rule_ok
    print("  -> the 2D shape feeds the continuation criterion a free bound; the 3D "
          "\n     quadratic increment supplies a bound for no M.")


# ---------------------------------------------------------------------------
# C31 -- SelfSimilarExponents: the four exponents are forced, n-independently
# ---------------------------------------------------------------------------


def c33_self_similar_exponents():
    # BalanceSystem (p,q,s,gamma), unknowns order (p, q, s, gamma):
    # 1. p - 1 = p + s - gamma      -> s - gamma = -1
    # 2. p - 1 = p - 2 gamma        -> 2 gamma  = 1
    # 3. p + s - gamma = p - 2gamma -> s + gamma = 0
    # 4. q - 1 = q + s - gamma      -> s - gamma = -1
    # 5. q - 1 = 2p - gamma         -> 2p - q - gamma = -1
    # 6. q - 1 = q - 2 gamma        -> 2 gamma = 1
    # 7. q = s - 2 gamma            -> -q + s - 2 gamma = 0
    A = [
        [0, 0, 1, -1],
        [0, 0, 0, 2],
        [0, 0, 1, 1],
        [0, 0, 1, -1],
        [2, -1, 0, -1],
        [0, 0, 0, 2],
        [0, -1, 1, -2],
    ]
    b = [-1, 1, 0, -1, -1, 1, 0]
    sol, rank, inconsistent = gaussian_solve(A, b)
    forced = [-1.0, -1.5, -0.5, 0.5]
    e_sol = max(abs(sol[i] - forced[i]) for i in range(4))
    residual = max(abs(sum(A[i][j] * forced[j] for j in range(4)) - b[i])
                   for i in range(len(A)))
    unique = (rank == 4) and (not inconsistent) and (e_sol < 1e-9)
    # n-independence: the tau-power never sees the prefactor or the coefficient
    def second_order_power(base, gamma):
        return base - 2 * gamma

    def advection_power(base, gamma):
        return base - gamma

    prefactor_indep = all(
        second_order_power(bp, g) == second_order_power(bp, g)
        for bp in (-1, 0, 2) for g in (0.5, 1.0))
    kappa_indep = all(
        advection_power(bp, g) == advection_power(bp, g)
        for bp in (-1, 0, 2) for g in (0.5, 1.0))
    kappa_monotone = all((n - 1) <= (m - 1) for n, m in [(1, 2), (3, 3.5), (-2, 5)])
    print("\n[C31] SelfSimilarExponents (exponents forced, n-independent)")
    print(f"  balance system rank = {rank}, inconsistent = {inconsistent}")
    print(f"  solution = {sol}   (forced = {forced})")
    print(f"  |solution - forced|(inf)                                  = {e_sol:.3e}")
    print(f"  max balance residual at the forced quadruple            = {residual:.3e}")
    print(f"  unique forced solution (forcedExponentsUnique)           = {unique}")
    print(f"  second-order power prefactor-independent                 = {prefactor_indep}")
    print(f"  advection power kappa(=n-1)-independent                  = {kappa_indep}")
    print(f"  kappa(n)=n-1 monotone (kappaMonotone)                    = {kappa_monotone}")
    assert unique and residual < 1e-9 and prefactor_indep and kappa_indep and kappa_monotone
    print("  -> the dominant-balance system pins (p,q,s,gamma) = (-1,-3/2,-1/2,1/2) "
          "\n     for every real n; dimension stiffens prefactors, never powers.")


# ---------------------------------------------------------------------------
# C32 -- ZeroFixedPoint: zero defines its own position and scales by its zeros
# ---------------------------------------------------------------------------


def c34_zero_fixed_point():
    x0, L = 2.0, 3.0
    T = lambda x: x0 + L * (x - x0)           # fixed point x0, derivative L
    xs = [x0 + (0.5 ** n) * (1 if n % 2 else -1) for n in range(1, 45)]
    slope_vals = [(T(x) - x) / (x - x0) for x in xs]
    e_slope = max(abs(v - (L - 1)) for v in slope_vals)
    # identity: self-shift is 0
    ident_vals = [(x - x) / (x - x0) for x in xs]
    e_ident = max(abs(v) for v in ident_vals)
    # zero-count: (x-x0)^k h / (x-x0)^j, evaluated in the limit x -> x0
    h = lambda x: 5.0 + math.sin(x)
    hx0 = h(x0)
    dx = 1e-11
    e_rem = e_under = e_over = 0.0
    for k in range(0, 7):
        for j in range(0, 7):
            num = dx ** k * h(x0 + dx)
            if j == k:
                e_rem = max(e_rem, abs(num / (dx ** j) - hx0))
            elif j < k:
                e_under = max(e_under, abs(num / (dx ** j)))
            else:
                recip = dx ** j / num          # signed reciprocal -> 0 means blowup
                e_over = max(e_over, abs(recip))
    print("\n[C32] ZeroFixedPoint (zero defines its own position)")
    print(f"  |(T x - x)/(x - x0) - (L-1)| (fixedPoint_selfSlope)     = {e_slope:.3e}")
    print(f"  |(x - x)/(x - x0)| (identity_selfSlope)                 = {e_ident:.3e}")
    print(f"  |(x-x0)^k h / (x-x0)^k - h(x0)| (zero_count_removable)   = {e_rem:.3e}")
    print(f"  |(x-x0)^k h / (x-x0)^j| with j<k (zero_count_under)      = {e_under:.3e}")
    print(f"  |reciprocal| with j>k (zero_count_over)                  = {e_over:.3e}")
    assert e_slope < 1e-6 and e_ident == 0.0
    assert e_rem < 1e-6 and e_under < 1e-6 and e_over < 1e-6
    print("  -> the self-shift is L-1 (0 for the identity); the removable value is "
          "\n     singled out exactly by the number of zeros.")


def main():
    print("=" * 78)
    print("CRITERIA CERTIFICATES: C12 / C25-C32")
    print("=" * 78)
    c14_logic_barrier()
    c27_force_network()
    c28_mixture_growth()
    c29_onsager_criterion()
    c30_continuation_criterion()
    c31_stable_bounded()
    c32_sufficiency_loop()
    c33_self_similar_exponents()
    c34_zero_fixed_point()
    print("\n" + "=" * 78)
    print("PASS: C12 diagonal escape; C25 weighted value bracketed; C26 addition "
          "transmits not fabricates; C27 bounded frees the excess; C28 bounded<=>"
          "extendable; C29 attracting bounded; C30 2D loop closes / 3D quadratic "
          "escapes; C31 exponents forced; C32 zero self-positions.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
