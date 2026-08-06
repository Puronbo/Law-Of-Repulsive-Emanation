"""Scale-free network on the toy network (Barabasi-Albert).

Builds a power-law (scale-free) wiring with a few hubs and many sparsely
connected units, then runs the local-only balance dynamics over that fixed
topology (flow_over) with ledger recording.

Usage:  python puno_flow/examples/scale_free.py [n]
"""

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from puno_flow import (
    FlowEngine,
    degree_sequence,
    hubs,
    preferential_attachment,
    topology_stats,
)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000
    rng = np.random.RandomState(17)

    # scale-free wiring: each new unit attaches to 2 existing units chosen
    # with probability proportional to their current degree (rich get richer)
    edges = preferential_attachment(n, m=2, rng=rng)
    stats = topology_stats(edges, n)
    print(f"topology   : Barabasi-Albert  n={n:,}  m=2")
    print(f"            edges {stats['edges']:,}  mean degree {stats['mean_degree']:.2f}"
          f"  max degree {stats['max_degree']}  gamma {stats['gamma']:.2f} "
          f"(power-law exponent)")
    h, d = hubs(edges, n, k=3)
    print(f"            hubs {h.tolist()} with degrees {d.tolist()}"
          f" (heavy tail: {stats['heavy_tail']})")

    # the hub fraction of the links: how concentrated is the network?
    deg = degree_sequence(edges, n)
    top = np.argsort(deg)[::-1][: max(n // 10, 1)]
    hub_share = float(deg[top].sum() / (2 * len(edges)))
    print(f"            top 10% of units carry {hub_share:.1%} of all links")

    # wire it: same local dynamics over hubs and spokes instead of k-NN
    homes = rng.uniform(-0.5, 0.5, (n, 2))
    net = FlowEngine(dim=2, k=8).add_many(homes)
    t0 = time.time()
    net.flow_over(edges, steps=20, record=True)
    el = time.time() - t0
    print(f"\nflow_over  : 20 steps over the fixed scale-free wiring "
          f"in {el:.2f}s")
    print(f"            finite {np.isfinite(net.q).all()}  "
          f"max |q| {np.linalg.norm(net.q, axis=-1).max():.3f}  "
          f"spacing {net.spacing():.4f}")
    print(f"            ledger verified {net.verify_ledger()[0]}  "
          f"blocks {net.ledger_audit()['blocks']:,}  "
          f"k-NN reciprocity {net.consensus():.3f}")


if __name__ == "__main__":
    main()
