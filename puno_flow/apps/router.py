"""Autonomous geographic routing over the toy network.

Units are routers.  A packet is delivered greedily: from the current unit,
hop to the unvisited neighbour closest to the destination.  If greedy gets
stuck in a local void, the packet falls back to the global nearest unit to
the destination (still found through the exact index).  When units die the
mesh reflows with the local dynamics and routing self-heals.

Usage:  python -m puno_flow.apps.router [n] [trials]
"""

import sys

import numpy as np

from puno_flow import FlowEngine


def route(engine, start, dest, k=8, max_hops=200):
    """Greedy geographic route from unit `start` toward point `dest`.
    Returns (path, delivered)."""
    if not (0 <= int(start) < engine.n):
        return [int(start)], False
    path = [int(start)]
    cur = int(start)
    visited = {cur}
    for _ in range(max_hops):
        if np.linalg.norm(engine.q[cur] - dest) <= 1e-9:
            return path, True
        nb, _ = engine.search(engine.q[cur], k=min(k, engine.n))
        nb = nb[1:]
        cand = nb[np.argsort(np.linalg.norm(engine.q[nb] - dest, axis=-1))]
        best = next((int(c) for c in cand if int(c) not in visited), None)
        if best is None:
            g, _ = engine.search(dest, k=1)
            g = int(g[0])
            if g in visited:
                return path, False
            best = g
        cur = best
        visited.add(cur)
        path.append(cur)
    return path, np.linalg.norm(engine.q[cur] - dest) <= 1e-9


def delivered_fraction(engine, pairs, k=8):
    ok = 0
    hops = []
    for s, d in pairs:
        path, delivered = route(engine, s, d, k=k)
        hops.append(len(path))
        ok += delivered
    return ok / len(pairs), int(np.median(hops))


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    rng = np.random.RandomState(23)
    engine = FlowEngine(dim=2, k=8, mu0=0.12).add_many(
        rng.uniform(-0.5, 0.5, (n, 2)))
    engine.settle(60, record=True)

    rng2 = np.random.RandomState(5)
    pairs = [(int(rng2.randint(0, n)), engine.q[int(rng2.randint(0, n))])
             for _ in range(trials)]
    frac, med = delivered_fraction(engine, pairs)
    print(f"router     : n={n}  settled 60 steps, greedy + index fallback")
    print(f"            delivery {frac:.0%}   median hops {med}")

    # damage a third of the routers, then let the mesh reflow locally
    killed = rng2.choice(n, size=n // 3, replace=False)
    engine.remove(killed)
    print(f"            damage: killed {len(killed)} routers, mesh reflows")
    engine.heal(60, record=True)
    pairs = [(int(rng2.randint(0, engine.n)), engine.q[int(rng2.randint(0, engine.n))])
             for _ in range(trials)]
    frac2, med2 = delivered_fraction(engine, pairs)
    print(f"            delivery after self-heal {frac2:.0%}"
          f"   median hops {med2}")

    ok, unit, seq = engine.verify_ledger()
    print(f"            ledger verified {ok}  "
          f"{engine.ledger_audit()['blocks']:,} blocks")


if __name__ == "__main__":
    main()
