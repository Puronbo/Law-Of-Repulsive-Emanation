"""Autonomous self-healing coverage mesh.

A population of units spreads itself with the local-only balance dynamics,
monitors its own coverage (mean k-NN spacing), and respawns units into the
gaps it detects - using the search engine to find the most isolated unit.
It survives scheduled damage with no central controller.  Every step is
chained to each unit's local ledger, so the whole autonomous history is
tamper-evident.

Usage:  python -m puno_flow.apps.guard_mesh [ticks] [n]
"""

import sys

import numpy as np

from puno_flow import FlowEngine


def deploy(n, dim=2, seed=7, settle=30):
    rng = np.random.RandomState(seed)
    homes = rng.uniform(-0.5, 0.5, (n, dim))
    engine = FlowEngine(dim=dim, k=8, mu0=0.12).add_many(homes)
    if settle:
        engine.settle(settle, record=True)
    return engine


def holes(engine, q=0.9):
    """Units whose mean k-NN distance is at/above the q-th quantile - the
    coverage gaps - ranked from most to least isolated.  Uses search."""
    n = engine.n
    if n < 2:
        return np.array([], dtype=int)
    k = min(8, n)
    _, d = engine.search(engine.q, k=k)
    mean_d = d[:, 1:].mean(axis=1) if d.shape[1] > 1 else np.zeros(n)
    thr = np.quantile(mean_d, q)
    order = np.argsort(mean_d)[::-1]
    return order[mean_d[order] >= thr]


def tick(engine, steps=3, target=0.02, respawn=3, rng=None):
    """One autonomous tick: relax locally, then respawn into the detected
    holes if coverage has thinned beyond target.  Returns event strings."""
    rng = np.random.RandomState(7) if rng is None else rng
    engine.settle(steps, record=True)
    events = []
    s = engine.spacing()
    if s > target:
        made = 0
        for h in holes(engine)[:respawn]:
            x = engine.q[int(h)] + rng.randn(engine.q.shape[1]) * 0.02
            engine.create(x, parent=int(h))
            made += 1
        events.append(f"respawned {made} into holes (spacing {s:.4f})")
    return events


def run_simulation(engine, ticks=14, target=None, damage_at=(3, 7),
                   damage_frac=0.15, seed=1):
    """Autonomous timeline with scheduled damage events.  Returns
    (log, engine); log is a per-tick list of dicts.  target defaults to the
    mesh's settled spacing, so coverage is maintained, not overgrown."""
    if target is None:
        target = engine.spacing()
    rng = np.random.RandomState(seed)
    log = []
    for t in range(ticks):
        events = tick(engine, target=target, rng=rng)
        if t in damage_at:
            removed = max(1, int(engine.n * damage_frac))
            drop = rng.choice(engine.n, size=removed, replace=False)
            engine.remove(drop)
            events.append(f"damage: removed {removed} units")
        log.append({"tick": t, "n": engine.n,
                    "spacing": round(engine.spacing(), 4),
                    "events": events})
    return log, engine


def main():
    ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    engine = deploy(n)
    log, engine = run_simulation(engine, ticks=ticks)
    print(f"guard mesh : autonomous coverage mesh, n={n}, ticks={ticks}")
    print(f"            damage at ticks {sorted({3, 7} & {*range(ticks)})}"
          f" (15% of units each time)")
    print(f"{'tick':>4} {'n':>5} {'spacing':>8}  events")
    for row in log:
        print(f"{row['tick']:>4} {row['n']:>5} {row['spacing']:>8.4f}"
              + (f"  {'; '.join(row['events'])}" if row["events"] else ""))
    ok, unit, seq = engine.verify_ledger()
    print(f"\naudit      : ledger verified {ok}"
          + ("" if ok else f" (first bad unit {unit}, seq {seq})"))
    print(f"            {engine.ledger_audit()['blocks']:,} blocks across "
          f"{engine.ledger_audit()['chains']} chains "
          f"(history of removed units is preserved)")
    print(f"            final spacing {engine.spacing():.4f}, "
          f"consensus {engine.consensus():.3f}, finite "
          f"{np.isfinite(engine.q).all()}")


if __name__ == "__main__":
    main()
