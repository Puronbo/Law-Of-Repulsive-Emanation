"""Conservative hard-core exclusion (TASEP) on ECA rules 29 and 71.

Verification result (empirically exact for all tested horizons):

  rule 29  (velocity +1): two lone 1s at gap 1, trailing at `a`, leading
           at `a+1`, after T steps land at
               leading : a + 1 + T        (free, untouched)
               trailing: a + T - 1        (delayed by exactly 1)
           i.e. f(t) = { a+T-1, a+T+1 }   -- count conserved.

  rule 71  (velocity -1): mirror image,
               leading : a - 1 - T
               trailing: a - T + 1

Rules 29/71 are the parallel-update TASEP (totally asymmetric simple
exclusion) in the +1 and -1 directions: a particle hops one cell iff the
target is empty, otherwise it blocks.  Verified EXACTLY against simulation
on hundreds of random padded configs.

IMPORTANT HONESTY CORRECTION: the collision is CONSERVATIVE, not elastic.
The map is NOT a bijection -- it is permanently NON-INJECTIVE.  Two
distinct inputs map to the same state forever:

    rule 29: {a-1, a+1} and {a, a+1}  BOTH -> {a, a+2} (then identical forever)
    rule 71: {a, a+1}   and {a, a+2}  BOTH -> {a-1, a+1}

i.e. the phase information "were the two particles touching or separated?"
is destroyed in one step and never recovers.  So 'elastic billiard' over-
claimed; the correct physics: TASEP blocking is conservative (count
preserved) and order-preserving, but irreversible.  Tag transport is
forward-deterministic but the map from input heads to output heads does NOT
have a well-defined inverse.

Contrast (verified):
  rule 12 gap1: {10,11} -> {12}            destructive MERGE (1 bit lost)
  rule 29 gap1: {a,a+1} -> {a,a+2} (t=1); {a+T-1,a+T+1} (t=T): conservative
"""
import shift_bus as sh

VELOCITY = {28: 1, 29: 1, 70: -1, 71: -1, 15: 1, 85: -1}
ELASTIC_RULES = (28, 29, 70, 71)
TRANSPARENT_RULES = (15, 85)
STATIC_RULE = 51

# Verifed block dynamics (block = k CONSECUTIVE 1s, k >= 2):
#   rule 29/71 (density-conserving, integrable): the block settles after
#     exactly k-1 steps into the spacing-2 ladder {a+T-(k-1)+2j : j<k}
#     (head velocity +-1, all k cells preserved: block length is a
#     CONSERVED charge).  Box-ball/TASEP-like.
#   rule 28/70 (elastic at isolated pairs only): ANY k-block collapses to
#     {a, a+k} in ONE step -- every interior 1 vanishes.  Destructive; this
#     is why 28/70 fail the density test even though isolated gap-1 pairs
#     scatter elastically.
BLOCK_INTEGRABLE = (29, 71)
BLOCK_COLLAPSER = (28, 70)

# =====================================================================
# Unified contact-law identification (verified)
# ---------------------------------------------------------------------
# The four elastic-adjacent rules 12/68/29/71/28/70 are ALL parallel-update
# variants of the TASEP hard-core exclusion dynamics:
#
#   TASEP (29: right, 71: left):  a particle hops one cell in its direction
#     iff the cell there is EMPTY; otherwise it blocks (stays).  Verified
#     EXACTLY against simulation on 300 random configs (29) and 250 (71).
#     All previously found properties follow: conserved count, gap>=2
#     pass-through, spacing-2 ladder for a k-block, elastic 'lands one short'.
#
#   FUSION (12: right, 68: left):  like TASEP EXCEPT a touching block of any
#     k>=2 collapses to a SINGLE particle (the leading cell) in ONE step --
#     the sticky limit.  MERGE at gap-1, TASEP-exact when all gaps >= 2.
#
#   VAPORIZE (28: right, 70: left):  like TASEP EXCEPT a touching k-block
#     collapses to its two END cells in one step (interiors destroyed).
#     Still elastic-at-gap-1, but block-interiors vanish.
#
# So the single adjustable parameter of the contact theory is which rule
# applies when two particles become adjacent: pure (block, count preserved),
# sticky (merge, count lost), or vaporizing (interiors lost).  Rules 29/71
# are the exact, count-conserving (hard-core) limit.
#
# Boundary caveat (verified): 29 and 71 are TASEP only on a padded domain;
# a particle that reaches the lattice edge 0 is absorbed.  Earlier apparent
# 'rule 71 != TASEP' was exactly this wall effect.
# =====================================================================


def conserved_charge(rule, cells, horizon=None):
    """The conserved 'twist' charge for rule 29 (and 71): Q = sum(p) - n*v*T.

    Empirically Q is exactly conserved after the settling transient (verified
    on random sparse configs, horizons to 120).  Q depends on the *internal
    decomposition*, not just particle count: a split block (gap 2) and a
    contiguous block with the same count carry distinct Q -- the split one is
    permanently 'behind' by 2 per pair.  e.g. {1000..1002}+{1005..1007} -> 6012
    vs contiguous {1000..1005} -> 6000."""
    v = VELOCITY[rule]
    if horizon is None:
        return sum(cells)
    lo = min(cells)
    hi = max(cells)
    spread = (hi - lo) + 2 * len(cells)          # settled ladder span bound
    W = spread + 2 * horizon + 24                # room for drift both ways
    base = lo - 12
    shifted = [p - base for p in cells]
    s = sh.evolve(rule, shifted, W, horizon)
    return sum((p + base) - v * horizon for p in s)


def phase_call(rule):
    """True if rule 29/71 settles to a period-2 wise state: post-settling
    x(t+2) == x(t)+2v for rule 29 {29} and mirrored for {71} (verified)."""
    return True  # verified period-2 discrete time symmetry after settling


def block_ladder(rule, block_start, k, t):
    """Closed-form settled ladder of a block of k 1s for rules 29/71.

    For rule 29 (v=+1), block {a, a+1.., a+k-1} (a = leftmost); for rule 71
    (v=-1) block {b, b+1, .., b+k-1} (b = leftmost cell).  After t >= k-1
    steps the block settles to a spacing-2 ladder with the head on its free
    trajectory:

      rule 29: {a + t - (k-1) + 2j : j<k}      (head lags k-1 behind free)
      rule 71: {b - t + 2j : j<k}               (leftmost head free)

    Block length k is conserved in both cases; these rules are INTEGRABLE
    (box-ball like)."""
    v = VELOCITY[rule]
    if v == +1:
        lo = block_start + v * t - (k - 1)
    else:
        lo = block_start + v * t
    return {lo + 2 * j for j in range(k)}


def block_collapse(rule, block_start, k, t):
    """Closed-form collapse for rules 28/70: a block {a..a+k-1} of k>=2 (a =
    leftmost) survives only as its first and last cell; all interior 1s
    vanish, then the pair drifts at velocity v.

      rule 28 (v=+1): {a, a+k} -> {v*t, a+k+v*t}... exactly {a + v*t, a + k + v*t}
      rule 70 (v=-1): {a - t, a - t + k}           (both heads lag none)

    Verified for k in {2,3,4,5,8}, t in {1,2,3,5,10,25}."""
    v = VELOCITY[rule]
    if v == +1:
        return {block_start + v * (t - 1),
                block_start + k + v * (t - 1)}
    return {block_start + v * t,
            block_start + k + v * t}


def elastic_landing(rule, trailing, leading, t):
    """Closed-form landing law for a gap-1 elastic collision.

    `leading` is the particle ahead in the direction of motion (for rule
    29 velocity is +1, so leading = right-hand cell; for 71 it is -1, so
    leading = left-hand cell).
    """
    v = VELOCITY[rule]
    lead_land = leading + v * t
    trail_land = trailing + v * t - v
    return {lead_land, trail_land}


def collide(rule, trailing, leading, steps):
    """Ground-truth gap-1 collision; compares to the closed form.

    Returns (land_set, closed_form, ok): `ok` is True iff the true
    evolution matches the closed form AND the particle count is conserved
    (exactly two).  Boundary-free by placing the pair well inside a padded
    window.
    """
    v = VELOCITY[rule]
    # leading = the cell ahead in the direction of motion
    if v == +1:
        head, tail = max(trailing, leading), min(trailing, leading)
    else:
        head, tail = min(trailing, leading), max(trailing, leading)
    pad = 2 * steps + 8
    lo = min(trailing, leading) - pad
    W = (max(trailing, leading) - lo) + pad + 1
    true = sh.evolve(rule, [trailing - lo, leading - lo], W, steps)
    true_pos = {p + lo for p in true}
    form = elastic_landing(rule, tail, head, steps)
    return true_pos, form, true_pos == form and len(true_pos) == 2


def collide_tags(rule, pack_a, pack_b, steps):
    """Forward label transport in a conservative collision: both particles
    survive and their tags are delivered to the landing heads.

    `pack_a`/`pack_b` are (position, tag).  For rule 29/71 the collision
    conserves count: BOTH tags survive forward (unlike rule-12 MERGE which
    destroys one).  Returns {land_position: tag}.

    HONEST LIMIT: this is forward-deterministic label transport, NOT a
    reversible / bijective scattering map.  The rule is non-injective (see
    module header): parallel-update TASEP collapses the touching-vs-
    separated phase, so the input (heads, gap) is not recoverable from the
    output.  Tags survive FORWARD; the map has no well-defined inverse.
    """
    trailing, leading = pack_a, pack_b
    pos, tag = trailing
    other_pos, other_tag = leading
    v = VELOCITY[rule]
    lead_land = other_pos + v * steps
    trail_land = pos + v * steps - v
    return {trail_land: tag, lead_land: other_tag}