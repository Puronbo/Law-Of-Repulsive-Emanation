"""
ARITHMETIC SHADOWS OF THREE CARDS (C36 / C37 / C38)
===================================================
Numerical companion to three formal cards.  Each Lean card proves a fact about
finite sums of reals (C36, C37) or real powers (C38); this script re-derives the
same arithmetic independently in floating point and asserts it holds.  It is the
*empirical half* of each card, not a proof: the proof is the Lean theorem.  Where
the checker (`test_claim_traceability.py`) confirms the declaration *resolves*,
this confirms the *arithmetic* the declaration names is the arithmetic that
actually happens.

  C36  `NoetherDiscrete`   -- the discrete Noether theorem (Conservation mechanism)
  C37  `UniverseGrowth`    -- the increasing point universe is momentum-neutral
  C38  `CriticalAmplitude` -- the critical amplitude is the removable value of a 0/0

Scope, as everywhere: finite sums and real powers.  No continuum limit, no PDE, no
statistical-mechanics model, no Millennium problem (see WHAT_THIS_DOES_NOT_PROVE.md).
Deterministic (seeded); prints a table and ends with PASS.
"""

import numpy as np

RNG = np.random.default_rng(20261015)

# ---------------------------------------------------------------------------
# C36 -- NoetherDiscrete.lean
#   momentum v = sum v ;  charge q qm = sum (q - qm) ;
#   step F qm q = 2q - qm + F q ;  momentumAt u k = charge (u (k+1)) (u k).
# The card proves: (a) charge = momentum q - momentum qm;
# (b) charge is translation-invariant; (c) momentum is the removable value of
# (sum v*dt)/dt; (d) for a *balanced* force (sum_i F_i = 0) the symmetric step
# conserves the charge, so it is a constant of the motion.
# ---------------------------------------------------------------------------


def momentum(v):
    return float(np.sum(v))


def charge(q, qm):
    return float(np.sum(q - qm))


def make_balanced_force(n, dt2=1e-2):
    """A pairwise-central force: F_i = dt2 * sum_j k_ij (q_j - q_i), F_ji = -F_ij,
    so sum_i F_i(q) = 0 for EVERY configuration q (the infinitesimal symmetry).
    The small `dt2` is the integrator's step^2: it keeps the symmetric leapfrog
    `q_{k+2} = 2q_{k+1} - q_k + F(q)` in its stable regime (|omega*dt| < 2)."""
    k = RNG.uniform(0.5, 1.5, size=(n, n))
    k = np.tril(k, -1) + np.tril(k, -1).T  # symmetric coupling, zero diagonal

    def force(q):
        diff = q[None, :] - q[:, None]          # diff[i, j] = q_j - q_i
        return dt2 * np.sum(k * diff, axis=1)

    return force


def c36_noether_discrete():
    n = 8
    q0 = RNG.normal(size=n)
    q1 = q0 + RNG.normal(scale=1e-2, size=n)
    F = make_balanced_force(n)

    steps = [q0, q1]
    for _ in range(40):
        qm, q = steps[-2], steps[-1]
        steps.append(2.0 * q - qm + F(q))

    # (a) charge = difference of momenta
    ez_a = abs(charge(steps[3], steps[2])
               - (momentum(steps[3]) - momentum(steps[2])))

    # (b) translation invariance of the charge
    c = RNG.normal()
    ez_b = abs(charge(steps[5] + c, steps[4] + c) - charge(steps[5], steps[4]))

    # balanced force: total force vanishes on every configuration (relative)
    net = max(abs(np.sum(F(s))) / (1.0 + np.max(np.abs(F(s))))
              for s in steps)

    # (c) momentum is the removable value of (sum v*dt)/dt as dt -> 0
    v = RNG.normal(size=n)
    dt = 1e-9
    ez_c = abs(np.sum(v * dt) / dt - momentum(v))

    # (d) momentumAt u k = charge(u(k+1), u k) is constant along the trajectory
    mom = np.array([charge(steps[k + 1], steps[k]) for k in range(40)])
    drift_d = float(np.max(np.abs(mom - mom[0])))

    print("\n[C36] discrete Noether (Conservation mechanism)")
    print(f"  (a) |charge - (momentum q - momentum qm)|        = {ez_a:.3e}")
    print(f"  (b) |charge(q+c,qm+c) - charge(q,qm)|            = {ez_b:.3e}")
    print(f"       max |sum_i F_i(q)| over configs             = {net:.3e}")
    print(f"  (c) |(sum v*dt)/dt - momentum v|  (dt=1e-9)      = {ez_c:.3e}")
    print(f"  (d) max_k |momentumAt k - momentumAt 0|          = {drift_d:.3e}")
    assert ez_a < 1e-12 and ez_b < 1e-12 and ez_c < 1e-12
    assert net < 1e-12
    assert drift_d < 1e-12, "trajectory momentum not conserved"
    print("  -> charge is a difference of momenta, translation-invariant, and a")
    print("     constant of the motion for a balanced (translation-symmetric) force.")


# ---------------------------------------------------------------------------
# C37 -- UniverseGrowth.lean
#   momentumOn U v = sum_{x in U} v x ;  influx U v k = momentumOn (U(k+1)\U k) v.
# The card proves: momentumOn_grow (a split), the continuity equation
# momentumOn (U(k+1)) = momentumOn (U k) + influx, and neutrality/conservation
# when every newly created point enters with ZERO velocity.
# ---------------------------------------------------------------------------


def c37_universe_growth():
    v = RNG.normal(size=8)
    U0 = np.arange(4)               # starting universe {0,1,2,3}
    added = np.arange(4, 8)         # newly created points
    U1 = np.arange(8)
    v = v.copy()
    v[added] = 0.0                  # new points enter with zero velocity

    mom0 = momentum(v[U0])
    mom1 = momentum(v[U1])
    influx = momentum(v[added])     # momentumOn (U1 \ U0) v

    # split + continuity equation
    ez_split = abs(mom1 - (mom0 + influx))
    # neutrality / conservation
    ez_cons = abs(mom1 - mom0)

    # the same for the register's charge, new points with zero displacement
    q = RNG.normal(size=8)
    qm = q - RNG.uniform(size=8)
    q[added] = qm[added]            # displacement q - qm vanishes on new points
    ch0 = momentum(q[U0] - qm[U0])
    ch1 = momentum(q[U1] - qm[U1])
    ez_chg = abs(ch1 - ch0)

    # on a saturated universe this is exactly the C36 total momentum
    ez_univ = abs(momentum(v[U1]) - momentum(v))

    print("\n[C37] increasing point universe (growth is momentum-neutral)")
    print(f"  momentumOn U0 = {mom0:+.6f}   momentumOn U1 = {mom1:+.6f}")
    print(f"  influx (new sites) = {influx:+.3e}")
    print(f"  |momentumOn U1 - (momentumOn U0 + influx)|      = {ez_split:.3e}")
    print(f"  |momentumOn U1 - momentumOn U0| (conservation)  = {ez_cons:.3e}")
    print(f"  |chargeOn U1 - chargeOn U0|                     = {ez_chg:.3e}")
    print(f"  |momentumOn univ - momentum|                    = {ez_univ:.3e}")
    assert ez_split < 1e-12 and ez_cons < 1e-12 and ez_chg < 1e-12
    assert ez_univ < 1e-12
    print("  -> growth splits the momentum as old + influx; points created with")
    print("     zero velocity leave the total momentum (and charge) unchanged.")


# ---------------------------------------------------------------------------
# C38 -- CriticalAmplitude.lean
#   orderParameter A beta x = A * |x|^beta ;  amplitudeRatio A beta x = op / |x|^beta.
#   gamma = beta*(delta-1) ; alpha = 2 - beta*(delta+1) ;
#   nu = (2 - alpha)/d ; eta = 2 - gamma/nu.
# The card proves: orderParameter vanishes at x=0 for beta != 0; amplitudeRatio is
# the removable value of the 0/0 (= A) off the critical point; and the classical
# scaling relations (Widom / Rushbrooke / Josephson / Fisher) hold identically.
# ---------------------------------------------------------------------------


def gamma(beta, delta):
    return beta * (delta - 1.0)


def alpha(beta, delta):
    return 2.0 - beta * (delta + 1.0)


def nu(d, beta, delta):
    return (2.0 - alpha(beta, delta)) / d


def eta(d, beta, delta):
    return 2.0 - gamma(beta, delta) / nu(d, beta, delta)


def c38_critical_amplitude():
    # (i) the 0/0: numerator and denominator both vanish at x = 0 ...
    A = RNG.uniform(0.3, 2.0)
    beta = RNG.uniform(0.5, 1.5)
    xs = np.array([1e-2, 1e-3, 1e-4, 1e-5, 1e-6])
    num = A * np.abs(xs) ** beta          # orderParameter
    den = np.abs(xs) ** beta              # |x|^beta
    ratio = num / den                     # amplitudeRatio
    op0 = A * np.abs(0.0) ** beta         # orderParameter at the critical point
    print("\n[C38] critical amplitude (removable value of a 0/0) and scaling relations")
    print(f"  A = {A:.6f}, beta = {beta:.6f}")
    print("    x          orderParameter      |x|^beta        ratio")
    for x, n_, d_, r_ in zip(xs, num, den, ratio):
        print(f"    {x:.0e}    {n_:.3e}       {d_:.3e}    {r_:.9f}")
    ez_ratio = float(np.max(np.abs(ratio - A)))
    ez_op0 = abs(op0)
    assert ez_op0 < 1e-15, "order parameter not vanishing at the critical point"
    assert ez_ratio < 1e-12, "amplitude ratio is not the removable value A"
    print(f"  |amplitudeRatio - A| (removable value)          = {ez_ratio:.3e}")
    print(f"  orderParameter at x = 0                         = {ez_op0:.3e}")

    # (ii) the classical scaling relations, as identities over a (beta,delta,d) grid
    worst = {"widom": 0.0, "rushbrooke": 0.0, "josephson": 0.0, "fisher": 0.0}
    for b in np.linspace(0.3, 1.5, 13):
        for de in np.linspace(2.0, 6.0, 9):
            for d in np.linspace(2.0, 4.0, 5):
                g = gamma(b, de)
                a = alpha(b, de)
                n = nu(d, b, de)
                e = eta(d, b, de)
                worst["widom"] = max(worst["widom"], abs(g - b * (de - 1.0)))
                worst["rushbrooke"] = max(worst["rushbrooke"], abs(a + 2.0 * b + g - 2.0))
                worst["josephson"] = max(worst["josephson"], abs(n * d - (2.0 - a)))
                worst["fisher"] = max(worst["fisher"], abs(n * (2.0 - e) - g))
    print("  max identity residual over the grid:")
    for k in ("widom", "rushbrooke", "josephson", "fisher"):
        print(f"    {k:>11} = {worst[k]:.3e}")
        assert worst[k] < 1e-12, f"{k} relation violated"
    print("  -> the amplitude is the removable value of the order-parameter 0/0, and")
    print("     Widom / Rushbrooke / Josephson / Fisher hold identically.")


def main():
    print("=" * 78)
    print("ARITHMETIC SHADOWS OF CARDS C36 / C37 / C38")
    print("=" * 78)
    c36_noether_discrete()
    c37_universe_growth()
    c38_critical_amplitude()
    print("\n" + "=" * 78)
    print("PASS: (C36) charge = difference of momenta, conserved for balanced force;")
    print("      (C37) zero-velocity growth is momentum- and charge-neutral;")
    print("      (C38) amplitude = removable value of the 0/0; scaling relations exact.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
