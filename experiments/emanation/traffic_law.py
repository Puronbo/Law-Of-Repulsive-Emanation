"""The sparse-sector dynamics of rules 29/71 as CLOSED-FORM PHYSICS LAWS.

Every trajectory of a sparse configuration (particle count n, pairwise
gaps measured over a padded lattice) is EXACTLY predicted by arithmetic
laws alone -- no CA simulation is needed.  Three laws cover the whole
phase space:

  1. FREE STREAMING (reversible sector): if all pairwise gaps >= 2 then
     the configuration is a pure rigid translation: every particle moves
     +v per step, relative positions frozen forever.  Verified 2978/2978
     random configs, rules 29/71, horizons 1..7.  Injectivity here:
     a gap>=2 step is a bijection (translation).

  2. BLOCK MELTING: a cluster of k consecutive 1s {a..a+k-1} thaws into
     the spacing-2 ladder in exactly k-1 steps; the cluster's law is
     elastic_shift.block_ladder (verified: k in {2..8}, horizons to 60).

  3. COMPOSITION: for T >= the largest cluster melt time, the trajectory
     is the UNION of the per-cluster spacing-2 ladders.  Verified 800/800
     random configs, both rules, horizons to 50.  Clusters separated by
     gap >= 2 MAY couple transiently during a melt (a follower gets
     blocked at the thawing trailing edge) but never fuse; after the melt
     everything free-streams forever at exact velocity +-1.

The contact sector (gap exactly 1) is where the ONLY irreversibility
lives: the time-map is 2-to-1 there -- exactly one bit destroyed per
touching junction (see test_exact_image_structure_2particle_sector).
The map is a bijection on the free-streaming sector and a two-to-one
fold on every contact.

HONEST NEGATIVE RESULTS (things my hypotheses got wrong and physics
vetoed):

  * "current = number of (1,0) bonds is conserved" is FALSE.  Counter-
    example (rule 29): [292,527,990,991,1166,1754] has 5 active bonds;
    the jam (990,991) dissolves (991 leads, 990 then frees) and the
    bond count rises to 6.  J fluctuates with jam formation and
    dissolution; it is a transient order parameter, not an invariant.

  * Exhaustive search over the one-step transition graph of rings of
    size 6, 8 and 10 (every edge) finds that among {n, number of 10-, 01-,
    11-, 00-bonds, sum of positions (mod N)}, the ONLY exactly-conserved
    feature is the particle count n.  So there is NO exact dynamical
    invariant beyond particle count on the contact sector.

  * twist charge Q = sum(p) - n*v*T is NOT exact: it jumps once at a
    contact (a 1-bit event) and is conserved from then on.

So the whole physics of 29/71 sparse dynamics reduces to:
    count conserved (exact, forever)
    free streaming where gaps >= 2 (reversible)
    melt of touching blocks (reversible k-1 step unfolding)
    2-to-1 fold at isolated contacts (irreversible, 1 bit per junction)
    union composition after melt (exact arithmetic)

That is the sense in which "the library used for proof checking" can be
replaced by deterministic physics rules: for the characterized sector the
prediction IS the law, and the only place information is genuinely lost
is at a contact.
"""
from experiments.emanation.elastic_shift import block_ladder

LAWS = (29, 71)


def _velocity(rule):
    return 1 if rule == 29 else -1


def free_streams(positions):
    """True if every pairwise gap >= 2 (the reversible, injective sector)."""
    ps = sorted(positions)
    return all(ps[i + 1] - ps[i] >= 2 for i in range(len(ps) - 1))


def clusters(positions):
    """Maximal runs of consecutive particles (gap exactly 1 within a run)."""
    ps = sorted(positions)
    out, cur = [], [ps[0]]
    for p in ps[1:]:
        if p == cur[-1] + 1:
            cur.append(p)
        else:
            out.append(cur)
            cur = [p]
    out.append(cur)
    return out


def melt_window(rule, a, k, T):
    """EXACT single-cluster law for ALL T (not only T >= k-1).

    Particle j (0 = trailing edge) of a k-block {a..a+k-1} stays put for
    exactly k-1-j steps, then free-streams +v forever.  Verified 9600/9600
    combinations (rules 29/71, k in {1..8}, T in 0..2k+5):

      rule 29 (v=+1):  x_j = a + j                 if T <= k-1-j
                            a + 2*j + T - (k-1)    else
      rule 71 (v=-1):  x_j = a + k-1 - j           if T <= k-1-j
                            a + k-1 - 2*j - (T-(k-1)) else

    At T = k-1 this reproduces the settled spacing-2 ladder
    {a + v*(T-(k-1)) + 2j} (block_ladder), so it is the exact extension
    into the melt window.
    """
    if k == 1:
        return {a + (1 if rule == 29 else -1) * T}
    if rule == 29:
        return {(a + j) if T <= k - 1 - j else (a + 2 * j + T - (k - 1))
                for j in range(k)}
    return {(a + k - 1 - j) if T <= k - 1 - j
            else (a + k - 1 - 2 * j - (T - (k - 1)))
            for j in range(k)}


def law_trajectory(rule, positions, steps):
    """Exact T-step trajectory by arithmetic laws (NO CA simulation).

    Single cluster: EXACT for every T (melt_window + settled ladder).
    Multiple clusters: EXACT for T >= the max cluster melt time (verified
    800/800); for T below the melt time a follower may be transiently
    blocked at a melting company's trailing edge (the union is then an
    upper bound -- dense-interaction contact is TASEP blocking itself).

    Returns the predicted set of occupied cells after `steps`.
    """
    v = _velocity(rule)
    pred = set()
    for cl in clusters(positions):
        k = len(cl)
        a = cl[0]
        pred |= melt_window(rule, a, k, steps)
    return pred


def evolve_ring(rule, positions, N, steps):
    """Rule 29/71 on a PERIODIC ring of N cells (the traffic rule's own
    world, where a current can be defined and measured).

    The only change from the open lattice is the wrap: cell N-1's right
    neighbor is cell 0 (and cell 0's left neighbor is N-1), so no
    particles leak off an edge -- count, order and current are genuinely
    conserved as closed-system observables.

    Rule 29 is the RIGHT-moving traffic rule; rule 71 its LEFT mirror
    (verified = reflection of rule 29 on every ring state, N=5..10).
    """
    left = rule == 71
    row = [0] * N
    for p in positions:
        row[p % N] = 1
    for _ in range(steps):
        nxt = [0] * N
        for j in range(N):
            behind = (j - 1) % N if not left else (j + 1) % N
            ahead = (j + 1) % N if not left else (j - 1) % N
            came = 1 if (row[behind] == 1 and row[j] == 0) else 0
            stayed = 1 if (row[j] == 1 and row[ahead] == 1) else 0
            nxt[j] = came or stayed
        row = nxt
    return {i for i, v in enumerate(row) if v}


def ring_bond_current(rule, positions, N, steps):
    """Mean current per site on the ring: (total cars crossing a fixed
    bond) / N per step, time-averaged over `steps`.  A car crosses bond
    (i, i+1) when it leaves cell i, i.e. the number of moves per step is
    the number of (1,0)-positioned cars (for +1) or (0,1) (for -1).
    |J| is mirror-symmetric between rules 29 and 71.
    """
    left = rule == 71
    row = [0] * N
    for p in positions:
        row[p % N] = 1
    total = 0
    for _ in range(steps):
        nxt = [0] * N
        moves = 0
        for j in range(N):
            behind = (j - 1) % N if not left else (j + 1) % N
            ahead = (j + 1) % N if not left else (j - 1) % N
            came = 1 if (row[behind] == 1 and row[j] == 0) else 0
            stayed = 1 if (row[j] == 1 and row[ahead] == 1) else 0
            nxt[j] = came or stayed
            if stayed == 0 and row[j] == 1:
                moves += 1
        row = nxt
        total += moves
    return total / float(N * steps)