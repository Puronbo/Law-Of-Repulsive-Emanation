"""Generic erasure audit: measure the information/erasure structure of ANY
finite deterministic map, in one call.

This is the instrumentation half of the verified 29/71 arc made reusable:
the erasure-ledger and fiber-law machinery, promoted from "rules 29/71 only"
to "give me a map on a finite domain and I will tell you its memory":
    * one-step image dimension  (how many distinct outputs exist);
    * max fiber / merge classes (how many inputs collide onto one output);
    * erased entropy  log2(total) - log2(images)   (bits destroyed, exact);
    * the erasure ledger clock:  after how many steps the image set
      stabilizes (state-space collapse time, the forgetting clock).

Everything is exhaustive over the given domain, so every number here is a
measured fact for that domain/map -- nothing is estimated, nothing is a
simulation inference.  For the rules 29/71 ring sector these numbers are
independently proven closed forms (Fibonacci/Lucas fiber, plateau at
k_max-1, independent-set collapse); the audit re-derives them from scratch.

Vetted usage in this repo (see test_erasure_audit.py):
    * rule 29/71 full ring state spaces (N=8): plateau = total independent
      sets of the N-cycle, e.g. 47 on C_8;
    * all 256 ECA rules on the N=8 ring: per-rule erasure spectrum
      (data/rule_erasure_spectrum.json);
    * any callable on any finite domain (generic f()).

Honesty: the audit reports the DOMAIN's erasure, not the map's global
structure.  A rule that is a bijection on its own attractor looks
erasing-or-not entirely through the lens of the domain you hand it.
"""
import itertools
import json
import math
import os
from collections import defaultdict

from shift_bus import _NEI


def eca_ring_step(rule, state):
    """One synchronous ECA step on a PERIODIC ring, using the repository's
    bit convention (_NEI from shift_bus), so rule numbers interoperate
    with shift_bus/traffic_law.  `state` is a tuple of 0/1 of length N."""
    N = len(state)
    out = []
    for i in range(N):
        t = (state[(i - 1) % N], state[i], state[(i + 1) % N])
        out.append((rule >> _NEI.index(t)) & 1)
    return tuple(out)


def bits_to_positions(state):
    """tuple of 0/1 on a ring -> sorted set of set-bit positions."""
    return tuple(i for i, v in enumerate(state) if v)


def one_step_census(domain, f):
    """f: element -> element.  Returns {output: [inputs...]} grouped by
    output; every multi-input group is a merge (a fiber with len>1)."""
    by_out = defaultdict(list)
    for c in domain:
        by_out[f(c)].append(c)
    return dict(by_out)


def ledger(domain, f, horizon):
    """Image-set counts for steps 1..horizon starting from the whole
    domain: [|im(step 1)|, |im(step 2)|, ...].  Converges on the attractor
    when the map is eventually shrinking (the erasure ledger closes)."""
    cur = set(domain)
    counts = []
    for _ in range(horizon):
        cur = {f(c) for c in cur}
        counts.append(len(cur))
    return counts


def audit(domain, f, horizon=3):
    """Full erasure audit of the map f on the finite domain.

    `f` must map domain elements to domain-COMPATIBLE values, and for
    horizon > 1 its outputs must be in `domain`'s value space again
    (i.e. f feeds its own attractor), otherwise `ledger` stops being
    well-defined -- use horizon=1 for cross-shaped maps whose outputs
    live in a different tuple space.

    Returns a dict of measured facts:
      total          |domain|
      image_1        distinct outputs after one step
      images_by_t    the erasure ledger [.. plateau ..]
      flat_at        first step t with images(t) == images(t-1) (None if
                     the horizon is too short to see the plateau)
      max_fiber       largest merge class (multiplicity of the fold)
      merge_classes  number of distinct outputs with >= 2 preimages
      merged_configs sum over classes of (fiber-1) = total - image_1
      erased_bits    log2(total) - log2(image_1)  (exact destroyed entropy)
    """
    census = one_step_census(domain, f)
    total = len(domain)
    images = len(census)
    classes = [v for v in census.values() if len(v) > 1]
    counts = [total] + ledger(domain, f, horizon)
    flat = None
    for t in range(1, len(counts)):
        if counts[t] == counts[t - 1]:
            flat = t
            break
    return {
        "total": total,
        "image_1": images,
        "images_by_t": counts,
        "flat_at": flat,
        "max_fiber": max((len(v) for v in census.values()), default=0),
        "merge_classes": len(classes),
        "merged_configs": sum(len(v) - 1 for v in classes),
        "erased_bits": math.log2(total) - math.log2(images),
    }


def rule_erasure_spectrum(N=8, rules=tuple(range(256)), horizon=3):
    """Per-rule erasure audit on the full N-ring state space (2**N binary
    states): the erasure spectrum of all 256 ECA rules under one
    convention.  Compact dict {rule: audit} for data/ persistence."""
    domain = tuple(itertools.product((0, 1), repeat=N))
    spec = {}
    for r in rules:
        spec[str(r)] = audit(domain, lambda s, r=r: eca_ring_step(r, s),
                             horizon=horizon)
    return spec


def save_spectrum(spec, path=None):
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "data", "rule_erasure_spectrum.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, indent=1, sort_keys=True)
    return path