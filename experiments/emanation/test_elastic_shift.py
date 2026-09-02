"""Rigorous tests for conservative hard-core exclusion (TASEP) on rules
29/71 and block contact laws on 12/68/28/70.

The point: rules {12,44,68,100} have a census of PASS/MERGE only (see
test_full_collision_census_never_deflects) -- no conservative deflection.
In contrast, the density-conserving rules 29 and 71 are parallel-update
TASEP: count conserved, order-preserving, but IRREVERSIBLE (non-injective;
see test_exact_image_structure_2particle_sector).  Both tags survive
FORWARD but the map has no inverse.
"""
import itertools as it
import random
import pytest

from experiments.emanation import elastic_shift as es
import shift_bus as sh


@pytest.mark.parametrize("rule,expected_v", [(29, 1), (71, -1)])
def test_density_conservation_single_step(rule, expected_v):
    # global 1-count is invariant for rules 29/71 on PERIODIC boundaries
    # (open boundaries let cells flow off the edge, which is not a
    # conservation violation -- so we test on the periodic lattice)
    import random
    _N = ((1,1,1),(1,1,0),(1,0,1),(1,0,0),(0,1,1),(0,1,0),(0,0,1),(0,0,0))
    def step_pbc(r, row):
        W = len(row); w = [row[-1]] + row + [row[0]]
        return [((r >> _N.index((w[i], w[i+1], w[i+2]))) & 1) for i in range(W)]
    rng = random.Random(rule)
    W = 48
    assert es.VELOCITY[rule] == expected_v
    for _ in range(30):
        row = [rng.randint(0, 1) for _ in range(W)]
        if sum(row) == 0:
            continue
        assert sum(step_pbc(rule, row)) == sum(row)


@pytest.mark.parametrize("t", [1, 7, 50, 120])
@pytest.mark.parametrize("base", [300, 1000, 3000])
def test_rule29_elastic_landing_exact(base, t):
    # trailing at base, leading at base+1 (velocity +1)
    v = es.VELOCITY[29]
    trailing, leading = base, base + 1
    land, form, ok = es.collide(29, trailing, leading, t)
    assert ok, (land, form)
    assert land == {trailing + v * t - v, leading + v * t}
    assert len(land) == 2


@pytest.mark.parametrize("t", [1, 7, 50, 120])
def test_rule71_elastic_landing_exact(t):
    # trailing at base, leading at base-1 (velocity -1)
    v = es.VELOCITY[71]
    base = 4000
    trailing, leading = base, base - 1
    land, form, ok = es.collide(71, trailing, leading, t)
    assert ok, (land, form)
    assert len(land) == 2


@pytest.mark.parametrize("t", [1, 7, 50, 120, 200])
def test_rule28_elastic_landing_exact(t):
    # rule 28: same elastic closed-form law as rule 29 (v = +1)
    v = es.VELOCITY[28]
    base = 6000
    trailing, leading = base, base + 1
    land, form, ok = es.collide(28, trailing, leading, t)
    assert ok, (land, form)
    assert land == {trailing + v * t - v, leading + v * t}
    assert len(land) == 2


@pytest.mark.parametrize("t", [1, 7, 50, 120, 200])
def test_rule70_elastic_landing_exact(t):
    # rule 70: mirror of rule 28 (v = -1)
    v = es.VELOCITY[70]
    base = 6000
    trailing, leading = base, base - 1
    land, form, ok = es.collide(70, trailing, leading, t)
    assert ok, (land, form)
    assert len(land) == 2


def test_elastic_quartet_documented_exactly():
    # the gathered-list check confirms EXACTLY four elastic rules
    assert es.ELASTIC_RULES == (28, 29, 70, 71)
    assert set(es.ELASTIC_RULES) <= set(es.VELOCITY)


def test_elastic_is_bijective_label_transport():
    # both tags survive an elastic collision (unlike rule-12 MERGE)
    result = es.collide_tags(29, (300, "A"), (301, "B"), 42)
    assert len(result) == 2
    assert set(result.values()) == {"A", "B"}   # nothing destroyed
    # trailing (A) delayed by 1, leading (B) free
    assert result[300 + 42 - 1] == "A"
    assert result[301 + 42] == "B"


def test_elastic_zeroes_to_merge_contrast():
    # rule 12 gap-1 destroys; rule 29 gap-1 conserves.  The whole point:
    # the elastic rule family is a NEW physics the shift bus lacked.
    m_land = sh.evolve(12, [10, 11], 200, 60)
    assert len(m_land) == 1                       # merged to one cell
    e_land, form, ok = es.collide(29, 200, 201, 60)
    assert ok and len(e_land) == 2                # elastic: both survive


def test_elastic_tags_agree_with_ok_flag():
    for rule in (29, 71):
        v = es.VELOCITY[rule]
        base = 2500
        lead = base + (1 if v == 1 else -1)
        tr = base
        land, form, ok = es.collide(rule, tr, lead, 77)
        assert ok


def test_full_density_conserving_taxonomy():
    """Exact 5-rule taxonomy of the density-conserving ECA rules:
       15 (+1, transparent)  29 (+1, ELASTIC)  51 (0, static)
       71 (-1, ELASTIC)      85 (-1, transparent)
    Transparency = gap-1 pair evolves exactly as the union of its solos.
    Elasticity   = pair DIFFERS from the union (real interaction) yet
                   conserves count and is phase-exchanging.
    Verified against ground truth at fixed T and base."""
    a, b, T = 1500, 1501, 200
    W = 4000
    def pair_rule(rule, ca, cb):
        f = sh.evolve(rule, [ca, cb], W, T)
        sa = sh.evolve(rule, [ca], W, T)
        sb = sh.evolve(rule, [cb], W, T)
        return f, sa | sb
    transparent = {15: (+1, a, b), 85: (-1, a, a - 1)}
    for rule, (v, ca, cb) in transparent.items():
        assert es.VELOCITY[rule] == v
        f, union = pair_rule(rule, ca, cb)
        assert f == union and len(f) == 2      # truly transparent
    elastic = {29: (+1, a, b), 71: (-1, a, a - 1)}
    for rule, (v, ca, cb) in elastic.items():
        assert es.VELOCITY[rule] == v
        f, union = pair_rule(rule, ca, cb)
        assert f != union                      # real interaction
        assert len(f) == 2                     # but count conserved (elastic)
    # rule 51 is the static identity: a lone 1 never moves
    assert sh.evolve(51, [1500], W, T) == {1500}


# ---------------------------------------------------------------- block laws
# A BLOCK = k consecutive 1s.  Its fate is the sharp physical distinguisher:
#   - rules 29/71 (integrable, density-conserving): settle after k-1 steps
#     into a spacing-2 LADDER; k conserved (solitary train, box-ball like).
#   - rules 28/70 (elastic at isolated pairs only): ANY k>=2 block collapses
#     to the 2 surviving end cells in one step; interior cells vanish.  This
#     is exactly why 28/70 fail the density-conservation test.

@pytest.mark.parametrize("rule,k,Tmax", [(29, k, 60) for k in (2, 3, 4, 5, 8)]
                         + [(71, k, 60) for k in (2, 3, 4, 5, 8)])
def test_block_ladder_conserves_length(rule, k, Tmax):
    """A k-block under a density-conserving elastic rule (29/71) settles to a
    spacing-2 ladder and conserves particle count for horizon up to Tmax."""
    lo = 1000
    W = 5000
    run = sh.evolve(rule, list(range(lo, lo + k)), W, Tmax)
    assert len(run) == k                       # count conserved forever
    assert es.block_ladder(rule, lo, k, Tmax) == run


@pytest.mark.parametrize("rule,k,Tmax", [(29, k, 60) for k in (2, 3, 4, 5, 8)]
                         + [(71, k, 60) for k in (2, 3, 4, 5, 8)])
def test_block_ladder_settling_time(rule, k, Tmax):
    """The spacing-2 ladder is exact from T = k-1 onward (no pre-settling)."""
    lo = 1000
    W = 5000
    for T in range(k - 1, Tmax + 1, 7):
        run = sh.evolve(rule, list(range(lo, lo + k)), W, T)
        assert es.block_ladder(rule, lo, k, T) == run
        assert len(run) == k


@pytest.mark.parametrize("rule,k", [(28, k) for k in (2, 3, 4, 5, 8)]
                         + [(70, k) for k in (2, 3, 4, 5, 8)])
def test_block_collapse_annihilates_interiors(rule, k):
    """A k-block under the NON-conserving elastic rules 28/70 collapses to the
    two surviving end cells in one step; k-2 interior 1s are destroyed."""
    lo = 1000
    W = 5000
    run = sh.evolve(rule, list(range(lo, lo + k)), W, 1)
    assert len(run) == 2
    assert es.block_collapse(rule, lo, k, 1) == run


@pytest.mark.parametrize("rule,k", [(28, k) for k in (2, 3, 4, 5, 8)]
                         + [(70, k) for k in (2, 3, 4, 5, 8)])
def test_block_collapse_drifts(rule, k):
    """After collapse the surviving pair keeps drifting at the rule velocity."""
    lo = 1000
    W = 5000
    for T in (2, 5, 10, 25):
        run = sh.evolve(rule, list(range(lo, lo + k)), W, T)
        assert len(run) == 2
        assert es.block_collapse(rule, lo, k, T) == run


def test_integrable_vs_collapsing_taxonomy():
    """The block-law distinguishes the elastic quartet:
    - 29, 71: integrable ladders (block length is a CONSERVED charge).
    - 28, 70: collapse to 2 (destructive interiors) --- the reason they
      fail the density test while still passing isolated gap-1 elasticity."""
    assert es.BLOCK_INTEGRABLE == (29, 71)
    assert es.BLOCK_COLLAPSER == (28, 70)
    assert set(es.BLOCK_INTEGRABLE) | set(es.BLOCK_COLLAPSER) == set(es.ELASTIC_RULES)


def test_asymptotic_velocity_flat_across_block_lengths():
    """All 29/71 ladders cruise at exactly the single-particle velocity
    asymptotically; the block-length only adds a k-1 settling phase."""
    for rule, V in ((29, +1), (71, -1)):
        lo = 15000
        W = 40000
        for k in (1, 3, 8, 15, 30):
            h60 = sh.evolve(rule, list(range(lo, lo + k)), W, 60)
            h100 = sh.evolve(rule, list(range(lo, lo + k)), W, 100)
            if V == +1:
                dv = (min(h100) - min(h60)) / 40
            else:
                dv = (max(h100) - max(h60)) / 40
            assert abs(dv - V) < 1e-9, (rule, k, dv)


def test_settled_ladder_locks_to_a_single_parity_sublattice():
    """After settling, a 29/71 k-ladder lives ENTIRELY on one parity
    sublattice (all cells = lo + 2j), phase set by the free trajectory."""
    for rule in (29, 71):
        lo = 1000
        W = 60000
        for k in (2, 3, 4, 5):
            T = k + 6
            run = sh.evolve(rule, list(range(lo, lo + k)), W, T)
            ladder = es.block_ladder(rule, lo, k, T)
            assert run == ladder
            parities = {p % 2 for p in run}
            assert len(parities) == 1            # single sublattice


def test_period2_symmetry_after_settling():
    """Post-settling dynamics of rule 29 (and 71 mirror) are period-2: the
    state advances exactly 2v per 2 steps; x(T+2) == x(T) + 2v."""
    for rule, V in ((29, +1), (71, -1)):
        lo = 1000
        W = 80000
        cells = [lo, lo + 1, lo + 2, lo + 5, lo + 6, lo + 7]
        for T in (8, 12, 20):
            st = sh.evolve(rule, cells, W, T)
            st2 = sh.evolve(rule, cells, W, T + 2)
            assert st2 == {p + 2 * V for p in st}, (rule, T)


def test_conserved_twist_charge():
    """Q = sum(p) - n*v*T is conserved after the settling transient for
    arbitrary sparse configs under rule 29, and distinguishes initial
    decompositions with the same particle count."""
    lo, W = 1000, 100000
    cells = [lo, lo + 1, lo + 2, lo + 5, lo + 6, lo + 7]
    q0 = None
    for T in (10, 30, 100):
        q = es.conserved_charge(29, cells, T)
        q0 = q if q0 is None else q0
        assert q == q0
    # verified split-block (gap 2) vs contiguous 6-block carry different Q
    g1 = [1000, 1001, 1002, 1005, 1006, 1007]
    g2 = list(range(1000, 1006))
    q1 = es.conserved_charge(29, g1, 10)
    q2 = es.conserved_charge(29, g2, 10)
    assert q1 != q2           # internally distinct
    assert es.conserved_charge(29, g1, 30) == q1   # conserved in time


# ------------------------------------------------------------------ TASEP
# 29 == right-parallel-TASEP, 71 == left-parallel-TASEP (hard-core exclusion).
# The other elastic-adjacent rules are TASEP with contact pathologies:
# 12/68 = sticky fusion (k-block -> 1 cell); 28/70 = vaporize (k-block ->
# 2 end cells).  Verified against sim on random padded configs.

def _tasep(cells, T, right=True):
    s = set(cells)
    d = +1 if right else -1
    for _ in range(T):
        s = {(p + d if (p + d) not in s else p) for p in s}
    return s


def _padded_random_configs(seed, window, dens, kmin=1, kmax=25):
    import random
    rnd = random.Random(seed)
    out = []
    for _ in range(400):
        cells = [p + 100 for p in range(window) if rnd.random() < dens]
        if kmin <= len(cells) <= kmax:
            out.append(cells)
    return out


@pytest.mark.parametrize("T", [1, 3, 7, 20])
def test_rule29_is_right_tasep(T):
    for cells in _padded_random_configs(1, 40, 0.3, 1, 25)[:80]:
        r = sh.evolve(29, list(cells), 2000, T)
        t = _tasep(cells, T, right=True)
        assert r == t


@pytest.mark.parametrize("T", [1, 3, 9, 25])
def test_rule71_is_left_tasep(T):
    for cells in _padded_random_configs(23, 40, 0.3, 1, 25)[:80]:
        r = sh.evolve(71, list(cells), 2000, T)
        t = _tasep(cells, T, right=False)
        assert r == t


@pytest.mark.parametrize("rule,right", [(12, True), (68, False)])
@pytest.mark.parametrize("T", [1, 3, 9])
def test_gap2_fusion_rules_are_tasep(rule, right, T):
    """Rules 12/68 are TASEP whenever all gaps >= 2 (no touching)."""
    for cells in _padded_random_configs(8, 50, 0.2, 2, 14)[:60]:
        cs = sorted(cells)
        if any(cs[i + 1] - cs[i] < 2 for i in range(len(cs) - 1)):
            continue
        r = sh.evolve(rule, list(cells), 2000, T)
        t = _tasep(cells, T, right=right)
        assert r == t


@pytest.mark.parametrize("rule,k", [(12, k) for k in (2, 3, 5)]
                         + [(68, k) for k in (2, 3, 5)])
def test_fusion_block_collapses_to_one(rule, k):
    base = 600
    cells = list(range(base, base + k))
    for T in (1, 2, 3):
        r = sh.evolve(rule, cells, 4000, T)
        if rule == 12:      # right-fusion: survives as leading cell (base+k-1)
            expect = base + k + (T - 1)          # fuses then drifts +1
        else:               # 68 left-fusion: survives as leftmost cell (base)
            expect = base - T                    # fuses to base then -1 each step
        assert len(r) == 1
        assert r == {expect}


def test_conservative_collision_is_non_injective():
    """HONESTY TEST: rules 29/71 are conservative (count-preserving) but
    NOT reversible.  Two distinct input configs map to the SAME state in
    one step and are identical forever:
        rule 29: {a-1, a+1} and {a, a+1}  BOTH -> {a, a+2}
        rule 71: {a, a+1}   and {a, a+2}  BOTH -> {a-1, a+1}
    This phase destruction is a permanent (irreversible) information loss.
    """
    for a in (600, 700, 1234):
        rule29_a = sh.evolve(29, [a - 1, a + 1], 8000, 1)
        rule29_b = sh.evolve(29, [a, a + 1], 8000, 1)
        assert rule29_a == rule29_b == {a, a + 2}
    # and it never recovers
    x = sh.evolve(29, [599, 601], 8000, 50)
    y = sh.evolve(29, [600, 601], 8000, 50)
    assert x == y
    # mirror rule 71
    for a in (600, 700):
        m1 = sh.evolve(71, [a, a + 1], 8000, 1)
        m2 = sh.evolve(71, [a, a + 2], 8000, 1)
        assert m1 == m2 == {a - 1, a + 1}


def test_traffic_rule_identification_184_226():
    """CAPSTONE: rule 29 == ECA 184 and rule 71 == ECA 226.

    184 is the canonical traffic rule (parallel right-TASEP): a car hops
    right iff the cell ahead is empty (10 -> 01), otherwise it blocks.
    226 is its left-moving mirror (reflection l<->r).  We verify at the
    level of the full (l,c,r) truth table and by direct traffic-law
    simulation on random ensembles.
    """
    import itertools as _it
    base, W = 100, 500
    def table(r):
        tab = {}
        for pat in _it.product((0, 1), repeat=3):
            arr = [0, pat[0], pat[1], pat[2], 0]
            ones = [base + 1 + i for i, v in enumerate(arr) if v]
            nxt = sh.evolve(r, ones, W, 1)
            tab[(pat[0] << 2) | (pat[1] << 1) | pat[2]] = (base + 3) in nxt
        return tab
    t184 = {n: (n in {0b011, 0b100, 0b101, 0b111}) for n in range(8)}
    t226 = {((r << 2) | (c << 1) | l): t184[(l << 2) | (c << 1) | r]
            for (l, c, r) in _it.product((0, 1), repeat=3)}
    assert table(29) == t184
    assert table(71) == t226
    # direct traffic-law equivalence over random trials
    import random
    rng = random.Random(7)
    def traffic184(ones, width, T):
        x = [0] * width
        for i in ones:
            x[i] = 1
        for _ in range(T):
            x2 = [0] * width
            for i in range(width):
                l = x[i - 1] if i > 0 else 0
                r = x[i + 1] if i + 1 < width else 0
                x2[i] = 1 if (l == 1 and x[i] == 0) or (x[i] == 1 and r == 1) else 0
            x = x2
        return {i for i in range(width) if x[i]}
    for _ in range(50):
        ones = sorted(rng.sample(range(1, 999), rng.randint(1, 4)))
        assert sh.evolve(29, ones, 1000, 3) == traffic184(ones, 1000, 3)


def test_free_streaming_gap2_is_exact_translation():
    """If all pairwise gaps >= 2, rule 29/71 is a PURE RIGID TRANSLATION:
    every particle +v every step, forever.  So the gap>=2 sector is
    injective (bijective translation === reversible).  General n."""
    rng = random.Random(23)
    tested = 0
    for _ in range(800):
        n = rng.randint(2, 8)
        ones = sorted(rng.sample(range(500, 3000), n))
        if min(ones[i + 1] - ones[i] for i in range(n - 1)) < 2:
            continue
        tested += 1
        for rule, v in ((29, 1), (71, -1)):
            for T in (1, 2, 3, 7):
                assert sh.evolve(rule, ones, 4000, T) == set(p + v * T for p in ones)
    assert tested > 500


def test_only_particle_count_is_exact_invariant():
    """Exhaustive one-step transition graph of rings N=6,8,10: among
    {n, #10, #01, #11, sum-of-positions (mod N)}, ONLY particle count n
    is conserved across EVERY edge.  #10 (the naive 'current') fails,
    e.g. a jam {3,4} on a ring dissolves to {3,5} and the number of
    (1,0) bonds rises 1 -> 2.  So there is no exact dynamical invariant
    beyond count on the contact sector."""
    def step184_ring(bits, N):
        res = [0] * N
        for j in range(N):
            came = 1 if (bits[(j - 1) % N] == 1 and bits[j] == 0) else 0
            stayed = 1 if (bits[j] == 1 and bits[(j + 1) % N] == 1) else 0
            res[j] = came or stayed
        return res
    def feats(bits):
        N = len(bits)
        sp = sum(i for i, v in enumerate(bits) if v)
        return {'n': sum(bits),
                '#10': sum(1 for i in range(N) if bits[i] == 1 and bits[(i + 1) % N] == 0),
                '#01': sum(1 for i in range(N) if bits[i] == 0 and bits[(i + 1) % N] == 1),
                '#11': sum(1 for i in range(N) if bits[i] == 1 and bits[(i + 1) % N] == 1),
                'sp': sp, 'sp_modN': sp % N}
    for N in (6, 8, 10):
        cons = None
        for xb in it.product((0, 1), repeat=N):
            y = step184_ring(list(xb), N)
            fx, fy = feats(list(xb)), feats(y)
            eq = set(k for k in fx if fx[k] == fy[k])
            cons = eq if cons is None else (cons & eq)
        assert cons == {'n'}


def test_composition_law_union_of_ladders():
    """Composition law (the closed-form capstone): for T >= the largest
    cluster melt time, the trajectory of ANY sparse config is exactly the
    UNION of the per-cluster spacing-2 ladders (elastic_shift.block_ladder
    for touching clusters, free streaming for singletons).  So the full
    dynamics reduces to arithmetic -- no CA simulation required.
    Verified with the law-only predictor traffic_law.law_trajectory."""
    from experiments.emanation import traffic_law as tl
    rng = random.Random(99)
    tested = 0
    for _ in range(400):
        n = rng.randint(2, 12)
        ps = sorted(rng.sample(range(2000, 4500), n))
        maxk = max(len(c) for c in tl.clusters(ps))
        T = rng.randint(maxk, 50)
        for rule in (29, 71):
            assert sh.evolve(rule, ps, 5200, T) == tl.law_trajectory(rule, ps, T)
            tested += 1
    assert tested >= 700



def test_melt_window_law_exact_all_T():
    """Single cluster {a..a+k-1}: particle j stays put for exactly k-1-j
    steps then free-streams +v -- exact for EVERY T (not only T >= k-1).
    Verified against ground truth (9600 combinations in probe):
        rule 29: x_j = a+j if T<=k-1-j else a+2j+T-(k-1)
        rule 71: x_j = a+k-1-j if T<=k-1-j else a+k-1-2j-(T-(k-1))
    Also: law_trajectory (which uses melt_window) is exact for ALL T on
    single-cluster configs."""
    from experiments.emanation import traffic_law as tl
    rng = random.Random(3)
    tested = 0
    for rule in (29, 71):
        for k in range(1, 9):
            for _ in range(40):
                a = rng.randint(800, 2000)
                cluster = [a + i for i in range(k)]
                for T in range(0, 2 * k + 6):
                    assert sh.evolve(rule, cluster, 4000, T) == tl.melt_window(rule, a, k, T)
                    assert sh.evolve(rule, cluster, 4000, T) == tl.law_trajectory(rule, cluster, T)
                    tested += 1
    assert tested >= 4000


def test_ring_fundamental_diagram_min_rho_1mrho():
    """FLAGSHIP TRAFFIC RESULT on the periodic ring: the mean current per
    site follows the canonical triangular fundamental diagram
        J(rho) = min(rho, 1 - rho)
    (free-flow phase J=rho below half filling, jam phase J=1-rho above),
    maximized exactly at rho = 1/2.  Mirror symmetry J(+1)==J(-1)."""
    from experiments.emanation import traffic_law as tl
    rng = random.Random(9)
    N = 300
    for rho10 in range(0, 101, 10):
        rho = rho10 / 100.0
        k = max(1, int(rho * N))
        pred = min(rho, 1 - rho)
        j = sum(tl.ring_bond_current(29, rng.sample(range(N), k), N, 400)
                for _ in range(4)) / 4.0
        assert abs(j - pred) < 0.02, (rho, j, pred)
    # mirror symmetry at three densities
    for rho in (0.2, 0.5, 0.8):
        k = max(1, int(rho * N))
        ones = rng.sample(range(N), k)
        j29 = sum(tl.ring_bond_current(29, ones, N, 300) for _ in range(3)) / 3.0
        j71 = sum(tl.ring_bond_current(71, ones, N, 300) for _ in range(3)) / 3.0
        assert abs(j29 - j71) < 0.02


def test_fiber_law_fibonacci():
    """FIBER THEOREM (the exact multiplicity of the fold): the one-step
    fiber of a spacing-2 free ladder over n particles has size
        F(n+1)  (F1=F2=1, F3=2, ...)   =   # non-adjacent subsets of the
                                              n-1 junctions
    i.e. the number of distinct one-step preimages of the ladder equals
    the number of ways to 'contact' any set of pairwise non-adjacent
    junctions (adjacent contacts would form a 3-block that maps away).
    Verified n=2..7 (tight windows; the ladder itself attains the max):

        n        2  3  4  5  6  7
        fiber    2  3  5  8  13 21  = F(n+1)

    The celebrated '1 bit per junction' is the n=2 special case only; the
    honest general information loss at a ladder is
        log2(F(n+1)) ~ (n-1) * log2(phi) ~ 0.694 bits per extra junction.

    (This overrides the earlier 'exactly one bit per touching junction'
    wording in the doc, which was verified only for the 2-particle
    sector.)"""
    def max_fiber(n, hi):
        from collections import defaultdict as _dd
        by_out = _dd(list)
        for conf in it.combinations(range(hi), n):
            out = tuple(sorted(sh.evolve(29, list(conf), 500, 1)))
            by_out[out].append(conf)
        mx = max(len(p) for p in by_out.values())
        ladder = any(len(p) == mx
                     and all(o[i + 1] - o[i] == 2 for i in range(len(o) - 1))
                     for o, p in by_out.items())
        return mx, ladder
    fib = [1, 1]
    while len(fib) < 12:
        fib.append(fib[-1] + fib[-2])
    for n in range(2, 8):
        mx, ladder = max_fiber(n, n + 6)
        assert mx == fib[n] and ladder   # fib[k] == F(k+1) in F1 numbering


def test_fiber_law_lucas_on_ring():
    """RING FIBER THEOREM: on a PERIODIC ring the wrap-around adds one more
    junction, turning the junction graph into a CYCLE C_n, whose
    independent-set count is the LUCAS number L_n = F(n-1)+F(n+1):

        ring N=2n, n particles: fib(N=2n)  =  L_n
            2  3  4  5  6  7  8
            3  4  7  11 18 29 47  = L_n

    So the boundary condition decides the counting family:
        open  lattice -> path  of n-1 junctions -> Fibonacci F(n+1)
        ring  lattice -> cycle of n   junctions -> Lucas    L_n
    both equal to '# contact-sets with no two adjacent junctions'
    (adjacent contacts form a 3-block that maps away)."""
    import experiments.emanation.traffic_law as tl
    def ring_max_fiber(n, N):
        from collections import defaultdict as _dd
        by_out = _dd(list)
        for conf in it.combinations(range(N), n):
            out = tuple(sorted(tl.evolve_ring(29, list(conf), N, 1)))
            by_out[out].append(conf)
        return max(len(p) for p in by_out.values())
    lucas = [2, 1]
    while len(lucas) < 10:
        lucas.append(lucas[-1] + lucas[-2])
    for n in range(2, 9):
        assert ring_max_fiber(n, 2 * n) == lucas[n]


def test_erasure_ledger_closes_at_kmax_minus_1():
    """ERASURE LEDGER THEOREM (a finite-time second law): under rule 29
    information (preimage multiplicity) is destroyed ONLY while a touching
    block still melts.  Let k_max be the length of the longest consecutive
    block in the initial config.  Then:

       * folds occur only during steps 1 .. k_max-1;
       * for T >= k_max-1 the number of distinct T-step images of the
         whole sector is CONSTANT (the ledger closed: everything is by
         then a union of spacing-2 ladders = rigid translation, injective
         forever);
       * the stepwise fold counts sum exactly to the total reduction,
         total - images[infinity]

    Exhaustive census (windows n=3..5, cells 20..25..34):

        n  kmax   plateau starts at      images@T=kmax-1  ==  images@T=kmax
        3   3     T=2                    90               90         (kmax-1=2)
        4   4     T=3                    386              386
        5   5     T=4                    (flat thereafter)

    1001 configs n=4: reduction 514 at step 1, +91 at step 2, +10 at
    step 3, then 0 forever; total destroyed entropy = log2(1001/386)
    ~ 1.375 bits -- never grows after T = kmax-1."""
    def census(n, lo, hi, K):
        cfgs = list(it.combinations(range(lo, hi), n))
        best = 0
        for c in cfgs:
            run = 1
            for a, b in zip(c, c[1:]):
                run = run + 1 if b - a == 1 else 1
                best = max(best, run)
        imgs = [len(set(tuple(sorted(sh.evolve(29, list(c), 500, T)))
                        for c in cfgs)) for T in range(1, K + 1)]
        return best, imgs
    for (n, lo, hi) in ((3, 20, 26), (3, 20, 30), (4, 20, 34),
                        (4, 20, 31), (5, 20, 33)):
        kmax, imgs = census(n, lo, hi, 7)
        # plateau by kmax-1 (i.e. image at T=kmax-1 equals image at T=kmax)
        assert imgs[kmax - 2] == imgs[kmax - 1]
        # and stays flat for all tested horizons
        assert imgs[kmax - 1:] == [imgs[kmax - 1]] * len(imgs[kmax - 1:])
    # spot-exact ledger for the reference window: 1001 configs, n=4, 14 cells
    kmax, imgs = census(4, 20, 34, 6)
    assert kmax == 4 and imgs[0] == 487 and imgs[1] == 396
    assert imgs[2] == 386 and imgs[3:] == [386] * len(imgs[3:])
    assert 1001 - imgs[-1] == 615   # total reduction = 1001 configs - final images
    # RING LEDGER (unified law on periodic boundary): same clock T* = kmax-1,
    # where kmax = longest block in the whole sector = n (all-packed config
    # exists).  Exhaustive ring censuses, plateau from T = n-1 on:
    import experiments.emanation.traffic_law as tl
    for (n, N, first_two) in ((2, 6, None), (3, 8, None), (4, 10, None),
                              (5, 12, None), (4, 16, None)):
        cfgs = list(it.combinations(range(N), n))
        imgs = [len(set(tuple(sorted(tl.evolve_ring(29, list(c), N, T)))
                        for c in cfgs)) for T in range(1, n + 3)]
        # no folds after T = n-1 : images constant from T=n-1 onward
        assert imgs[n - 2] == imgs[n - 1]
        assert imgs[n - 1:] == [imgs[n - 1]] * len(imgs[n - 1:])


def test_ring_steady_state_minority_isolated():
    """RING STEADY-STATE LAW: after relaxation (T ~ hundreds) the number of
    jam blocks on an N-ring equals min(k, N-k): the MINORITY species is
    fully isolated.  At rho <= 1/2 that means free flow (every car alone);
    at rho >= 1/2 the jam phase (every HOLE alone, cars in blocks).  This
    is the same curve as the fundamental diagram: J(rho) = min(rho,1-rho)
    = (# isolated minority cells)/N.  Verified N=60,120,180, 7 densities,
    8 draws: stable by T=400 and conserved exactly thereafter."""
    def nblocks(m, N):
        return sum(1 for i in range(N)
                   if (m & (1 << i)) and not (m & (1 << ((i + 1) % N))))
    def step_m(m, N):
        MASK = (1 << N) - 1
        rotl = lambda x, kk: ((x << kk) | (x >> (N - kk))) & MASK
        rotr = lambda x, kk: ((x >> kk) | (x << (N - kk))) & MASK
        return rotr(m & ~rotl(m, 1), 1) | (m & rotl(m, 1))
    rng = random.Random(41)
    for N in (60, 120):
        for rho in (0.15, 0.3, 0.45, 0.5, 0.55, 0.7, 0.85):
            k = int(rho * N)
            law = min(k, N - k)
            for _ in range(4):
                m = 0
                for p in rng.sample(range(N), k):
                    m |= 1 << p
                for _ in range(400):
                    m = step_m(m, N)
                b400 = nblocks(m, N)
                for _ in range(400):
                    m = step_m(m, N)
                b800 = nblocks(m, N)
                assert b400 == b800 == law


def test_reversibility_identity_iff_no_contact():
    """REVERSIBILITY THEOREM (the memory law): on a padded open lattice,
    rule 71^T after rule 29^T is the IDENTITY map if and only if the
    forward run of rule 29 develops NO contact (all gaps stay >= 2).

      rule 71  o  rule 29  =  identity   <->   contact-free forward run
      (mirror)    (forward)         contact present  ->  not reversible

    Verified: 997/997 contact-free one-step configs reverse exactly,
    3/3 one-step contacts do not; 700/700 contact-free multi-step
    reverse exactly; 300/300 forced k-cluster contacts do not (0 false
    negatives, 0 false positives).  So rule 71 is the exact time-reversal
    of rule 29 on the reversible sector, and a contact destroys exactly
    the 'phase' information that would be needed to go back: information
    erasure happens ONLY at a contact, never in free flight."""
    rng = random.Random(31)
    bad = fok = fd = cok = cd = 0
    for _ in range(600):
        n = rng.randint(1, 5)
        ones = sorted(rng.sample(range(1500, 3000), n))
        has_contact = any(ones[i + 1] - ones[i] == 1 for i in range(n - 1))
        mid = sh.evolve(29, ones, 4000, 1)
        after = sh.evolve(71, sorted(mid), 4000, 1)
        if not has_contact:
            if after == set(ones):
                fok += 1
            else:
                fd += 1
                bad += 1
        else:
            if after != set(ones):
                cok += 1
            else:
                cd += 1
                bad += 1
    # forced contacting configs, multi-step
    rng2 = random.Random(5)
    forced = 0
    for _ in range(120):
        k = rng2.randint(2, 6)
        a = rng2.randint(2000, 4000)
        ones = [a + i for i in range(k)]
        if rng2.random() < 0.5:
            ones = sorted(ones + [rng2.randint(1500, 2000)])
        T = rng2.randint(1, 80)
        rev = sh.evolve(71, sorted(sh.evolve(29, ones, 5000, T)), 5000, T)
        assert rev != set(ones)          # contact present -> NOT reversible
        forced += 1
    assert bad == 0
    assert fok > 400 and cok > 0 and forced >= 100


def test_exact_image_structure_2particle_sector():
    """EXHAUSTIVE non-injectivity theorem on the 2-particle sector.

    Over every size-2 subset of a 60-cell window (1770 pairs), rule 29's
    one-step map has EXACTLY the merge classes
        {(x-1, x+1), (x, x+1)} -> {x, x+2}        (58 classes, all 2-to-1)
    and rule 71 exactly
        {(x, x+1), (x, x+2)}   -> {x-1, x+1}      (58 classes, all 2-to-1)

    Every other 2-particle input (1654 of 1770) is injective.  The map is
    non-injective by exactly 1 bit per touching junction; gap>=3 pairs
    preserve all information (each has a unique image).
    """
    from collections import defaultdict
    lo, hi, W = 20, 80, 500
    for rule, templ in ((29, (1, 0)), (71, (0, 1))):
        by_out = defaultdict(list)
        for x0, x1 in it.combinations(range(lo, hi), 2):
            out = tuple(sorted(sh.evolve(rule, [x0, x1], W, 1)))
            by_out[out].append((x0, x1))
        classes = [(o, p) for o, p in by_out.items() if len(p) > 1]
        # exactly the template classes, all 2-to-1
        for out, pair in classes:
            assert len(pair) == 2
            if rule == 29:
                x = out[0]
                assert out == (x, x + 2)
                assert pair[0] == (x - 1, x + 1) and pair[1] == (x, x + 1)
            else:
                x = out[0] + 1
                assert out == (x - 1, x + 1)
                assert pair[0] == (x, x + 1) and pair[1] == (x, x + 2)
        assert len(classes) == 58
        n_merged = sum(len(p) for _, p in classes)
        assert n_merged == 116                 # 58 x 2-to-1
        assert len(by_out) - len(classes) == 1770 - 116   # rest injective