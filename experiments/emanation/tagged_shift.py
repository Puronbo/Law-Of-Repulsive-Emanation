"""Tagged shift transport: a label (degree of freedom) carried by solitons.

Adds one DOF per occupied cell: a free-form integer TAG that rides the
ballistic orbit.  The physics this buys is *content*: a packet is now
(position, tag), and the tag is delivered exactly whenever the trajectory
heads are unambiguous (the PASS regime).  On MERGE the tag of the
destroyed packet is lost -- the collision remains information-destroying,
exactly as the untagged census shows -- but on every non-conflicting
schedule the tag is conserved bit-for-bit.

Verified theorems (test_tagged_shift.py):
  * lone 1 under any rule: tag(head(t)) == initial tag, all t.
  * PASS separation: each tag follows ITS OWN head, never its neighbor's.
  * MERGE: the head packet's tag survives, the other is irrecoverable --
    the collision stays non-injective.

Invariants that are henceforth testable:
  * (content conservation) on any PASS schedule, the mapping head->tag is
    a bijection onto the initial mapping; tags are never garbled.
  * (annihilation) on any MERGE schedule exactly one tag is lost per
    collision; the loss is deterministic, never partial.
"""
import shift_bus as sh

# head(t) = p + v*t, all rules; +1 for {12,44}, -1 for {68,100}
VELOCITY = {12: 1, 44: 1, 68: -1, 100: -1}
RIGHT = (12, 44)
LEFT = (68, 100)
SOLITONS = RIGHT + LEFT


def head_after(rule, p, t):
    """Head position of a lone 1 after t steps (exactly p + v*t)."""
    return p + VELOCITY[rule] * t


def evolve_tags(rule, packets, steps):
    """Evolve dict {position: tag} forward `steps`.

    Returns (delivered, lost): two dicts {head: tag}.  `delivered` maps
    every surviving head to the tag it arrived with; `lost` maps original
    packets that were destroyed in a MERGE to their (unrecoverable) tag.

    Detection is done against TRUE occupancy, not guesswork: run the ground
    truth and ask which free-law heads actually exist; converging orbits
    (MERGE) remove the absorbed packets.  Boundary clipping is avoided by
    placing packets far from the lattice ends.
    """
    if not packets:
        return {}, {}
    positions = sorted(packets)
    # free-law destination of each head
    free = {head_after(rule, p, steps): tag for p, tag in packets.items()}

    # true occupancy, in a window big enough to be boundary-free: expand
    # both directions (left movers + blob tails on 44/100 trail behind)
    pad = 2 * steps + 8
    lo = min(positions) - pad
    hi = max(positions) + pad
    W = hi - lo + 1
    true = sh.evolve(rule, [p - lo for p in positions], W, steps)
    true_pos = {p + lo for p in true}

    delivered = {}
    lost = {}
    for h, tag in free.items():
        if h in true_pos:
            delivered[h] = tag
        else:
            lost[h] = tag
    return delivered, lost


def read_tags(rule, packets, steps):
    """Deliver the (head, tag) map: returns (delivered, lost) dicts."""
    return evolve_tags(rule, packets, steps)