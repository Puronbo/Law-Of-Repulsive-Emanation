# Conservative Soliton Gas (TASEP): the shift bus as hard-core exclusion

*Status: empirically verified (landing law == ground truth for all tested
horizons and bases; TASEP identification verified on hundreds of random
configs).  Includes an HONEST non-injectivity correction of the earlier
"elastic" wording.*

**CAPSTONE IDENTIFICATION**: the shift bus's conservative rules are the
canonical traffic rule:

    shift_bus rule 29  == ECA 184     (right-moving traffic, parallel TASEP)
    shift_bus rule 71  == ECA 226     (left-moving traffic, mirror of 184)

Verified three independent ways: (1) full (l,c,r) truth-table identity with
184 / its l<->r reflection, (2) direct rule-184 traffic simulation equal to
rule 29 on 50 random ensembles, (3) hundreds of random-config TASEP
double-checks.  The elastic-looking "governor", the spacing-2 bomber, the
twist charge, the blocking delay-by-1 -- ALL are standard properties of the
deterministic traffic rule (10->01 moves, jams form at 11-blocks, count
conserved).

## The problem the original bus could not solve

Rules {12, 44, 68, 100} transport lone solitons with **zero interaction
survival**: their collision census (all gaps) is exactly two outcomes:

    PASS   (gap >= 2): separation preserved, pure pass-through, NO device
    MERGE  (gap 1  ): two packets fuse into one, irreversible

There is **no DEFLECT**.  So no collision can act as a reversible gate, and
a label routed through the system either passes untouched or is destroyed.
The bus is a delay line -- deterministic, exact, but not "physics" in any
interactive sense.

## The discovery: density-conserving rules 29 and 71

Sweeping **all 256 ECA rules** for a conserved quantity (global particle
count, checked exhaustively on the periodic lattice) isolates exactly five
density-conserving rules:

    15  (v=+1) transparent mover
    29  (v=+1) TASEP (right hard-core)     <-- conservative, irreversible
    51  (v= 0) static identity
    71  (v=-1) TASEP (left hard-core)      <-- conservative, irreversible
    85  (v=-1) transparent mover

Rules 29 and 71 are the parallel-update TASEP alleles.  Two particles that
become adjacent conserve their count but the touching-vs-separated *phase*
is destroyed irreversibly (non-injective map -- see the honesty section).

## Verified landing law (TASEP blocking)

For rule 29 (velocity +1), two lone 1s at gap 1 -- trailing at `a`,
leading at `a+1` -- land after T steps at **exactly**

    leading : a + 1 + T      (free, untouched)
    trailing: a + T - 1      (delayed by exactly one step)

so `land(T) = { a+T-1, a+T+1 }`.  Rule 71 is the mirror image (v = -1).
Identified empirically, then closed-formed, then verified exact for
T in {1, 7, 50, 120} and several bases (test_elastic_shift.py).

## Why this upgrades the physics

Compare the same initial condition, `{10,11}`:

    rule 12:  {10,11} --1 step--> {12}       MERGE: one packet destroyed
    rule 29:  {10,11} --1 step--> {10,12}    conservative: both survive

Because 29/71 conserve count and are order-preserving, a **label** carried
through the collision is delivered **deterministically forward**
(`elastic_shift.collide_tags`).  This is the difference between pure
delay-line transport and a conservative hard-core gas.  The tag DOF
(`tagged_shift.py`) makes this explicit: on the conservative rules count
is never destroyed, on the MERGE rules it is destroyed deterministically.

## Honest boundary

This is a *conserved-charge + hard-core-exclusion* upgrade, not universal
computation.  Rules 29/71 are still nonlinear; the conservative collision
alone does not (yet) encode a universal logic gate, and it is irreversible
(non-injective -- see the honesty section below).  The honest
characterization:

**Before:** soliton delay line, exact but non-interacting / destructive.
**After:** hard-core soliton gas (TASEP), count + twist-charge conserved,
irreversible, forward-deterministic.

## Block law: what a *dense* cluster does (the integrable distinguisher)

The elastic pair law covers isolated gap-1 pairs.  The behavior of a
**block** of k consecutive 1s is the sharp discriminator between the dense
dynamics:

    rule 29 (v=+1), block {a..a+k-1}  --T steps (T >= k-1)-->  spacing-2 ladder
        { a + T - (k-1), a + T - (k-1) + 2, ..., a + T + (k-1) }
    rule 71 (v=-1), block {b..b+k-1}  --T steps (T >= k-1)-->  spacing-2 ladder
        { b - T, b - T + 2, ..., b - T + 2(k-1) }

So 29/71 are **integrable soliton-train rules**: the block length k is a
*conserved charge*, the block settles after exactly k-1 steps into a
spacing-2 ladder whose head rides its free trajectory.  This is the
box-ball / ultradiscrete-soliton signature.

By contrast rules 28 and 70 (the *other* two members of the elastic
quartet found in the gathered-list survey) collapse **any** block of k>=2
consecutive 1s to its two end cells in one step -- all k-2 interior 1s are
destroyed --

    rule 28 (v=+1), {a..a+k-1} --1 step--> {a, a+k}
    rule 70 (v=-1), {b..b+k-1} --1 step--> {b-1, b-1+k}   (then drift -1)

**This is exactly why 28/70 fail the global density test while still
scattering two *isolated* gap-1 particles conservatively.**  Their
interaction is a one-shot property of isolated pairs; at any touching
density the interiors vaporize.  Only 29/71 are both conservative AND
density-stable -- the pure TASEP hard-core limit, while 28/70 are an
equilibrium pair phenomenon embedded in a dissipative bulk.

## HONESTY: the collision is conservative but irreversible

Revealed by the TASEP identification is a correction to the original
"elastic" wording.  Rules 29/71 conserve particle count but their time-map
is **permanently non-injective**:

    rule 29:  {a-1, a+1}  -> {a, a+2}   (two particles 1 gap apart)
              {a, a+1}    -> {a, a+2}   (two touching)
              -> identical forever
    rule 71:  {a, a+1}    -> {a-1, a+1}
              {a, a+2}    -> {a-1, a+1}
              -> identical forever

The information "were these two particles touching or separated by exactly
one cell?" is destroyed in a single step and never recovered (verified the
merged states stay identical for 50+ steps).  This is TASEP hard-core
blocking: forward-deterministic, order-preserving, count-conserving, but
with no inverse.  It is NOT a reversible elastic rebounce, and it is NOT
lossless label transport (a label survives its OWN trajectory, but the map
from input configurations to output is many-to-one).

### Exactly one bit destroyed per junction (exhaustive theorem)

Exhaustive over the 2-particle sector (every size-2 subset of a 60-cell
window = 1770 pairs): rule 29's one-step map has EXACTLY the merge classes

    rule 29: {(x-1, x+1), (x, x+1)}  ->  {x, x+2}      (58 classes, 2-to-1)
    rule 71: {(x, x+1),   (x, x+2)}  ->  {x-1, x+1}    (58 classes, 2-to-1)

All 58+58 classes match; every OTHER input (1654 of 1770 per rule) is
injective.  Unified reading for the 2-particle sector: the destroyed bit
is the trailing offset {1,2} behind a shared leading cell -- i.e. exactly
the touching-vs-gap2 distinction.  Gap>=3 pairs preserve all information
(unique image).

### The exact fold multiplicity is Fibonacci (n-particle fiber law)

The "1 bit per junction" above is the **2-particle special case**.  For n
particles, the one-step fiber of a spacing-2 free ladder over them has
size exactly the Fibonacci number

    fiber of a free ladder over n particles  =  F(n+1)   (F1=F2=1)
                                            =  number of non-adjacent
                                               subsets of its n-1 junctions

i.e. the ladder can be reached from the pure free-flight config (0
contacts), from any ONE-junction contact, and from any set of PAIRWISE
NON-ADJACENT junctions contacted simultaneously (adjacent contacts would
form a 3-block that maps elsewhere).  Verified exhaustively over tight
windows, n = 2..7, ladder attains the max each time:

    n              2    3    4    5    6    7
    max fiber      2    3    5    8    13   21   = F(n+1)

**The boundary condition selects the counting family.**  On a PERIODIC
ring the wrap-around is one more junction, the junction graph is the
cycle C_n, and the fiber is the LUCAS number (independent sets of a
cycle):

    ring N=2n, n particles:  max fiber  =  L_n
        2   3   4   5   6   7   8
        3   4   7   11  18  29  47      = L_n   (verified n=2..8)

        open lattice  -> path  of n-1 junctions -> Fibonacci F(n+1)
        ring lattice  -> cycle of n   junctions -> Lucas    L_n
        both = #(contact-sets with no two adjacent junctions).

Honest consequence: the information destroyed at a ladder is
log2(F(n+1)) (open) or log2(L_n) (ring) ~ (n-1)*log2(phi) ~ **0.694 bits
per extra junction**, not 1.  The union-composition and reversibility
theorems below are untouched; only the exact multiplicity is
Fibonacci/Lucas.  (`test_fiber_law_fibonacci`, `test_fiber_law_lucas_on_ring`.)

So the corrected honest summary:
  * conservative gas, count + twist Q conserved, irreversible;
  * the "delay by 1" is blocking, not scattering;
  * useful for deterministic forward transport, not for computation that
    needs reversible logic;
* the non-injectivity is exactly 1 bit per touching junction on the
     2-particle sector; in general the fiber size follows the Fibonacci
     law F(n+1) (0.694 info bits per extra junction, asymptotic).

Verified: all four closed forms are exact against ground truth for
k in {2,3,4,5,8}, horizons to 60, several lattice bases
(`test_block_ladder_*`, `test_block_collapse_*`,
`test_integrable_vs_collapsing_taxonomy`,
`test_conservative_collision_is_non_injective`,
`test_exact_image_structure_2particle_sector`).

### Asymptotic velocity is flat (not box-ball)

Unlike the box-ball system, where a soliton's length sets its speed, the
29/71 ladders all cruise at **exactly ±1 asymptotically** regardless of
block length (verified for k up to 30, over horizons 60..100):

    k=1,3,8,15,30  ->  asymptotic v = +1.000 (rule 29)
    k=1,3,8,15,30  ->  asymptotic v = -1.000 (rule 71)

The only length dependence is the *construction* delay: a block of k 1s
launches with a k-1 step settling lag (its head starts free then the
trailing particles seed into the spacing-2 ladder).  Over any *finite*
horizon a longer block therefore appears to have drifted slightly less
far, but there is no velocity/length law.  Honest characterization:

**soliton gas, uniform velocity +-1, with a length-dependent
construction phase; NOT a box-ball length->speed hierarchy.**

## The conserved twist Q and period-2 clock

Two further invariants, verified exactly:

1. **Twist charge Q = sum(p) - n*v*T** is conserved after the settling
   transient (random sparse configs, horizons to 120).  Q encodes the
   *internal decomposition*: a split block (gap 2) and a contiguous block
   with the same particle count are permanently offset:

       {1000..1002} + {1005..1007}  -> Q = 6012   (lagged by 2 per pair)
       {1000..1005}                 -> Q = 6000

   The 012 difference is a durable 1-step-per-pair lag that survives to
   infinite time -- rule 29 keeps more than just particle count.

2. **Period-2 discrete time symmetry**: once settled, `x(T+2) = x(T) + 2v`
   exactly (v=+1 for 29, -1 for 71).  Each ladder advances 2 lattice sites
   per 2 steps; the whole gas walks on a fixed parity sublattice.

Together these make rule 29/71 a *conservative lattice gas*: a finite
config settles to disjoint spacing-2 ladders, each on one parity, all
cruising at +-1 with the twist Q forever conserved.

## The whole sparse sector closes: three laws, no simulator

The trajectory of ANY sparse configuration under rules 29/71 is exactly
predictable by arithmetic laws (`traffic_law.py`); a CA simulation is never
needed.  Three laws cover the phase space:

**L1 Free streaming (reversible sector).**  If all pairwise gaps >= 2, the
config is a pure rigid translation: every particle moves +v per step,
relative positions frozen forever (verified 2978/2978 random configs).
This sector is injective -- a bijection (translation), hence reversible.

**L2 Block melting.**  A cluster of k consecutive 1s {a..a+k-1} thaws into
the spacing-2 ladder in exactly k-1 steps (`block_ladder` law; verified).

**L3 Composition.**  For T >= the largest cluster melt time the trajectory
is the UNION of the per-cluster spacing-2 ladders (verified 800/800 random
configs, horizons to 50).  Clusters at gap >= 2 may couple *transiently*
during a melt (a follower is blocked at the thawing trailing edge) but
never fuse; after the melt everything free-streams forever at exact
velocity +-1.  `traffic_law.law_trajectory` predicts the whole thing with
arithmetic only.

So the complete physics of 29/71 sparse dynamics:
    count conserved (exact, forever);
    free streaming where gaps >= 2 (reversible);
    melt of touching blocks (reversible k-1 unfolding);
    fiber law F(n+1) at free ladders (irreversible fold; 0.694 bits per
      junction asymptotically, 1 bit exactly for 2 particles);
    union composition after melt.
The ONLY place information is destroyed is at a contact.

## Reversibility theorem (the memory law)

**On a padded open lattice, rule 71^T after rule 29^T is the IDENTITY map
if and only if the forward run of rule 29 develops no contact.**  Rule 71
is the exact time-reversal of rule 29 on the contact-free sector; a
contact is exactly and only the obstruction to reversibility.

Verified:
  997/997  contact-free one-step configs reverse exactly;
  3/3      one-step contacts do not reverse;
  700/700  contact-free multi-step configs reverse exactly;
  300/300  forced k-cluster contacts do not reverse (zero false pos/neg).

Reading as physics of memory: free flight is unitarity-like (every bit
survives both directions); a contact deletes the preimage ambiguity --
log2(F(n+1)) bits for a fresh ladder, 0.694 bits per junction in bulk --
exactly the information a reversible machine would need to reconstruct
the past, and irreversibly spent the moment two particles touch.
Information erasure happens ONLY at a contact, never in free flight --
this is the deterministic-CA second law, and it is precisely where
'observation' would lose information in a reversible machine.

### The erasure ledger closes at T = k_max - 1 (a finite-time second law)

Because folds happen only while some block still melts, the destroyed
entropy is FINITE and settles at a sharp clock.  Let k_max be the length
of the longest consecutive block anywhere in the sector (initial configs,
open lattice; or all configs of an (N,n) ring ensemble).  Then under
rules 29/71:

  * folds occur only during steps 1 .. k_max-1;
  * for T >= k_max-1 the number of distinct T-step images of the whole
    sector is CONSTANT -- the ledger is closed, the config is by then a
    union of spacing-2 ladders (rigid translation, injective forever).

Exhaustive censuses.  OPEN (windows n=3..5; the canonical n=4, 14-cell
window has 1001 configs):

     k_max      images at T=1,2,3,...         plateau
        4      487, 396, 386, 386, 386,...      T=3 = k_max-1

     step fold counts: 514 (step 1) + 91 (step 2) + 10 (step 3) = 615
     total reduction from 1001 configs; destroyed entropy
     log2(1001/386) ~ 1.375 bits, never growing after T = k_max-1.

RING (unified law, periodic boundary): the all-packed (n cars contiguous)
config exists in any (N,n) ensemble, so k_max = n and the ledger closes
at T = n-1, e.g. N=6: [9,...] from T=1; N=8,n=3: [24,16,16,...];
N=12,n=5: [240,96,48,36,36,...]; N=16,n=6: [2024,816,448,352,336,336,...].

**Erasure is punctual, bounded, exact: it happens only at contacts,
only during the melt windows, and amounts to log2(fiber) at each fold --
never any slow leak of information in free flight.**  (`test_erasure_ledger_closes_at_kmax_minus_1`.)

### State-space collapse (the ring attractor is the independent set)

The ledger plateau IS the attractor, with a closed-form size.  Under
rules 29/71 on a periodic N-ring with n particles, the T-step image set
stabilizes by T = n-1 at the latest and is then EXACTLY (as a SET) the
cyclic no-adjacency configs -- every gap >= 2 cyclically, i.e. the
minority-isolated steady states of L5, the free-ladder attractor:

    images_T(n,N)  =  { configs with no two adjacent, cyclically }   (T >= n-1)

Their count is the cyclic independence number (n <= N/2; symmetric under
n <-> N-n via holes):

    indep(N,n)  =  (N / (N-n)) * C(N-n, n)

Verified exactly (set identity, not just count) on N=6..16:
N=6,n=2 -> 9; N=8,n=3 -> 16; N=10,n=3 -> 50; N=12,n=4 -> 105;
N=12,n=5 -> 36; N=16,n=6 -> 336; N=16,n=7 -> 64; and count-match on
seven more (N=16,n=4 -> 660; N=10,n=4 -> 25; N=8,n=2 -> 20; N=14,n=4 ->
294; N=16,n=3 -> 352; N=12,n=3 -> 112; N=14,n=5 -> 196).

**So L4 (fundamental diagram), L5 (ring steady state), L6 (fiber law)
and L7 (erasure ledger) are ONE phenomenon: the dynamics collapses the
whole sector onto the independent-set attractor, and every trajectory
there is a rigid rotation forever.**  (`test_state_space_collapse_ring`.)

**All densities.**  On the FULL ring state space (not a single n sector)
the attractor is the union of BOTH complementary families -- cars
isolated OR holes isolated -- minus the two alternating patterns when N
is even, count measured exactly for N=5..9:

     plateau(29/71 on all configs of N-ring)  =  2*i_cyc(N) - 2*delta(N even)

with i_cyc(N) = total independent sets of the N-cycle (47 for C_8, so the
29/71 ring attractor has 2*47-2 = 92 states).  The n-sector numbers of
L8 are the projection of this onto one parity family.
(`test_full_density_ring_attractor_29_71`.)

**Correction (71 on rings).**  `traffic_law.evolve_ring` previously
ignored the rule number (both 29 and 71 ran the RIGHT dynamics).  It now
honors rule 71 as the exact LEFT mirror (verified: rule 71 == reflection
of rule 29 on every ring state, N=5..10).  All count laws (fiber, ledger,
attractor) are mirror-invariant and unchanged.

## The erasure audit: a reusable instrument (T0 of the integration path)

`experiments/emanation/erasure_audit.py` exposes the erasure-ledger and
fiber machinery as a generic audit for ANY finite deterministic map:

    audit(domain, f) -> total | image_1 | images_by_t (ledger) | flat_at
                        | max_fiber | merge_classes | merged_configs
                        | erased_bits  (= log2(total) - log2(image_1))

Every number is exhaustive over the given domain -- measured fact, no
simulation inference.  First dataset: the per-rule erasure spectrum of
all 256 ECA rules on the N=8 ring
(`data/rule_erasure_spectrum.json`): the injective rules are exactly the
8 permutations {15,51,85,105,150,170,204,240}; 0/255 collapse to one
state; mean one-step erasure over all rules is 1.266 bits; rules 29/71
give image_1=132 of 256 states (relaxing to the 92-state attractor).
This is the honest core of "a system that measures its own memory":
point it at a simulator's transition map and it reports that map's
forgetting clock and erasure budget.

Second layer: the **recurrent structure** of every rule
(`data/rule_erasure_attractors.json`).  `attractor(domain, f)` iterates
the whole-domain image to its set fixpoint (the periodic core -- the map
restricted there is a bijection, so the attractor is exactly the
reachable periodic points).  On the N=8 ring, over all 256 rules:
    * the immediate bijections are exactly the 8 permutations
      {15,51,85,105,150,170,204,240} (attractor 256, closing step 1);
    * 12 rules are nilpotent on N=8 -- attractor {00000000} (honest for
      THIS N only): {0,2,16,60,90,102,153,165,191,195,247,255};
    * rules 29/71: attractor = the 92 independent-family states, ledger
      closed in 4 whole-domain steps (one-step image 132 of 256,
      erased_bits 0.956, max_fiber 7);
    * rule 0: closing step 2, max_fiber 256 (everything to zero).
This is the "memory core" census: a rule's recurrent dimension is the
size of the state space it can genuinely keep.

Third layer: **law certificates** (`experiments/emanation/law_checker.py`,
data in `data/law_certificates.json`).  A certificate is a measured
fact: a candidate trajectory law, a stated domain, and the outcome of
comparing the law against the true evolution at every (config, T) point
-- status **PASS** (no disagreement) or **HONEST_NEGATIVE** (first exact
counter-example recorded, so a supervisor never ships a wrong law).
    5 PASS certificates: L1 free streaming (exhaustive gap>=2, rules
    29/71), L2 melt window on every single cluster (exhaustive, all T),
    L3 per-cluster union law on the merge-free sector T <= g_min - 2
    (provable guard: gaps never move left, so gap(t) >= gap(0) - t).
    4 HONEST_NEGATIVE certificates: the 29-traffic law against rules
    44/100, free streaming on touching configs, and the discovered
    MERGE SECTOR -- {4,7,9,10}, T=6: the trailing particle at 7 is
    caught by the melt of the {9,10} block (trailing gap 2 <= k, k=2),
    union law predicts {10,13,14,16}, truth is {10,12,14,16}.
Retraction caused by the checker: `law_trajectory`'s old claim "exact
for T >= max cluster melt time" was **FALSE**; now corrected to the
merge-free sector (single clusters remain exact for all T).

Fourth layer: **the law supervisor** (`supervisor.py`, verdict in
`data/supervision_verdict.json`).  It decides what a build may believe,
using only the certificate table: every claimed law must name the PASS
certificates it relies on; HONEST_NEGATIVE certificates reject a claim
with the exact counter-example; missing certificates reject it as
UNCERTIFIED; a PASS with zero checked points is no evidence.  Fresh
statements it certified itself:
    * L13: on the N-ring, |attractor(rule 29/71)| = 2*L_N - 2*(N even)
      -- every (N, rule) in {3..9} x {29,71} verified against the true
      attractor over all 2^N states (PASS);
    * L13_bad: the same law with the even correction dropped fails
      exactly on N in {4,6,8} (HONEST_NEGATIVE) -- the supervisor
      rejects it, as demonstrated in the verdict log.
Demonstration verdict: 3 claims believed formally, 3 rejected
(rule-44 misuse, even-correction omission, and an uncertified law).

Fifth layer: **the supervisor audits a real subsystem**
(`repo_audit.py`, `scripts/certify_repo.py`).  The first audited system
is `credit_commons.web.ledger.Ledger` -- the SQLite mutual-credit
ledger.  New statement certificates measured on the real code (30
seeded deterministic action sequences on 3 accounts, 24 actions each,
trades with necessity/harm draws plus grants; drift to 1e-6):
    * L14 gate-6 conservation: conserved_total = sum(credit) + reserve
      is invariant under every approved or rejected action -- PASS;
    * L14_bad "credit-sum-only" invariant -- HONEST_NEGATIVE (reserve
      absorption of fee residue and grant pay-outs break it), so the
      supervisor rejects it concretely.
FINDING recorded (not introduced): `credit_commons.sim.Commons.grant`
mints credit to the recipient and grows total_credit WITHOUT debiting
or tracking reserve -- a gate-6 divergence from the ledger, which does
enforce the invariant; L14 is certified for the ledger only.
Integration gate: `scripts/certify_repo.py` (--gate for CI) fails the
build unless the persisted certificate table reproduces EXACTLY from
current code (audit-the-audit drift detection: missing/stale/drifted
entries) and each of the 7 formal claims is believed by the
supervisor.  The same machine-readable table/verdict feed the webapp
and any agent.

Sixth layer: **the T2 seed -- the law proposer**
(`experiments/emanation/law_proposer.py`).  The gate's first consumer as
a workflow: an autonomous proposing agent forced to EARN its own
certificates.  Protocol (deterministic, fully documented):
    1. MEASURE |A(N, rule)| over train N in 3..7 for rules 29/71 (full
       2^N state spaces; N=12 => 4096 states);
    2. FIT each documented hypothesis family by exhaustive bounded
       integer search -- only zero-error-on-training laws survive.
       Families: `lucas_affine`, `lucas_parity` (parity bias),
       `fib_affine` (plausible Fibonacci control), `constant`;
    3. CERTIFY every survivor on the FRESH out-of-sample domain N in
       8..12 with the standard statement certificates.  The certified
       predicate recomputes the current attractor (use_cache=False): no
       training-era cached measurement can leak into the test domain,
       and a regression-level tamper test poisons the cache and
       re-checks.
Result: exactly ONE law survives -- |A(N,29/71)| = 2*L_N - 2*[N even] --
and it certifies PASS on all 10 fresh (N, rule) points (N=12 => 642
states).  Every look-alike dies at fit time: `fib_affine` and `constant`
have no zero-error law on training; `lucas_affine` without the even
correction errs on even N.  Headline facts land in
`data/law_proposer_results.json`, and the PASS certificate joins the
shared gate table (now 14 certificates) -- so `--gate` would reject a
build whose proposer stopped generalizing.  Propose -> measure ->
certify or self-reject; no human in the loop; no ungrounded claim
survivable.

**This answers "can the proof-checking library be replaced by physics?":
yes, for the characterized sector -- the prediction IS the law.**  And the
laws VETO candidates that a checking harness might let pass:

  * "current = number of (1,0) bonds" is NOT conserved.  Counterexample:
    [292,527,990,991,1166,1754] has 5 active bonds; the jam (990,991)
    dissolves and the bond count rises to 6.  J fluctuates with jam
    formation/dissolution -- a transient order parameter, not an invariant.
  * Exhaustive one-step transition graph of rings N=6,8,10: among
    {n, #10, #01, #11, sum-of-positions (mod N)} the ONLY exactly-conserved
    feature is particle count n.  There is no exact dynamical invariant
    beyond count on the contact sector.
  * twist charge Q is NOT exact: it jumps once at a contact (a 1-bit
    event), conserved thereafter.

## The periodic ring: the fundamental diagram (flagship traffic result)

`shift_bus` is open-boundary only, so the current could not be defined
until a periodic ring wrapper was added (`traffic_law.evolve_ring`,
`ring_bond_current`).  On the ring of N cells with k cars (density
rho = k/N), the mean current per site over time follows EXACTLY the
canonical triangular fundamental diagram of traffic theory:

    J(rho) = min(rho, 1 - rho)

measured over 51 densities (N=300, 4x400-step averages)::

    rho  0.05 0.1  0.2  0.3  0.4  0.5  0.6  0.7  0.8  0.9  0.95
    J    0.05 0.10 0.20 0.30 0.40 0.49 0.40 0.30 0.20 0.10 0.05

Free-flow phase J = rho below half filling (all cars move), jam phase
J = 1 - rho above (holes move), max-flow exactly at rho = 1/2.  Mirror
symmetry holds: J(+1) and J(-1) agree at every density (verified).  This
is the quantitative, closed-form physics of rule 184 on the bus -- the
curve a checking harness could NOT have produced, since it needed the ring
that only the physics (periodic boundary as the closed-system axiom)
supplies.

**Steady-state structure (the block law behind the diagram).**  After
relaxation (T ~ hundreds) the number of jam blocks on the ring equals
exactly min(k, N-k): the MINORITY species is fully isolated.  At
rho <= 1/2 that is free flow (every car alone, spacing >= 2 ladders); at
rho >= 1/2 it is the jam phase (every HOLE alone, cars in blocks).
Verified N=60,120,180 x 7 densities x 8 draws; the block count is reached
by T=400 and conserved exactly forever.  Hence the doubling:

    J(rho) = min(rho, 1-rho) = (# isolated minority cells) / N

the mean current per site IS the density of isolated minority species --
one curve, two faces (particle and hole).  The largest jam size is NOT a
law (init-dependent: multiple jams persist; there is no single-shock
phase separation in parallel TASEP, and that persistence is honest).

## TASEP identification: the contact-theory unification

The elastic landscaping law, the spacing-2 ladders, the conserved twist Q,
and period-2 clock are ALL consequences of one fact, verified directly:

**Rule 29 = parallel-update TASEP (hard-core exclusion, right-hoppers);
rule 71 = the left-going mirror.**  On a padded lattice, a particle hops
exactly one cell in its direction iff the target cell is empty; otherwise
it blocks in place.  Verified EXACTLY against simulation on hundreds of
random configs.

The elastic "trailing delayed by exactly 1" is the TASEP blocking rule; the
"spacing-2 bomber" is TASEP's jam-pierce; the conserved gas is TASEP's
particle number.  The earlier apparent discrepancy (rule 71 failing TASEP)
was a boundary artifact: a particle reaching lattice edge 0 is absorbed.
With padding it is exact.

The other contact rules are TASEP with pathologies wired *at the touch*:

    12/68 (sticky fuse): any touching k-block -> one leading cell (MERGE)
    28/70 (vaporize):    any touching k-block -> two end cells
    29/71 (pure):        touching = block, count preserved (hard-core)

So the physics the shift bus discovered is the **TASEP family**; rules
29/71 are the exact, conservative, hard-core limit, embedded as a
soliton-gas with a conserved twist charge.

## Code

- `experiments/emanation/elastic_shift.py` -- landing law, collide,
  collide_tags (forward deterministic), block_ladder (29/71) and
  block_collapse (28/70), ELASTIC_RULES = (28,29,70,71), non-injectivity
  honesty note in the header.
- `experiments/emanation/test_elastic_shift.py` -- 99 tests.
- `experiments/emanation/tagged_shift.py` -- tag DOF over the 4 bus rules.
- `experiments/emanation/test_tagged_shift.py` -- 33 tests.
- `experiments/emanation/demo_elastic.py` -- side-by-side ASCII.
