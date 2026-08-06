"""Toy network with ledgers, creation, and search.

Demonstrates the toy-network extras on the local-only dynamics:
  - creation     : units are born with a genesis block over their home;
                   spawn() grows the population locally (GNG-style)
  - blockchains  : every unit keeps its own hash-chained ledger; flow steps
                   append state blocks; tampering is detected by re-hashing
  - search engine: ranked nearest-centroid retrieval over the population
  - consensus    : local agreement (k-NN reciprocity), verified not mined

Usage:  python puno_flow/examples/toy_network.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from puno_flow import FlowEngine


def main():
    rng = np.random.RandomState(11)
    net = FlowEngine(dim=2, k=8, mu0=0.12)

    # creation: 12 class homes on a circle, each born with a genesis block
    th = np.linspace(0, 2 * np.pi, 12, endpoint=False)
    for a in 0.35 * np.column_stack([np.cos(th), np.sin(th)]):
        net.create(a)

    print("birth      : 12 units created, genesis blocks written")
    print(f"            {net.ledger_audit()['chains']} chains, "
          f"{net.ledger_audit()['blocks']} blocks, ledger verified "
          f"{net.verify_ledger()[0]}")

    net.settle(200, record=True)   # local relaxation, each step chained
    print(f"relax      : 200 flow steps chained -> "
          f"{net.ledger_audit()['blocks']} blocks, verified "
          f"{net.verify_ledger()[0]}")

    # creation: grow the population locally (children record their parent)
    grown = net.spawn(60, spread=0.03, rng=rng)
    print(f"growth     : spawned {len(grown)} units, "
          f"n = {net.n}, verified {net.verify_ledger()[0]}")

    net.settle(50, record=True)

    # search engine: ranked nearest-centroid hits for a fresh query cloud
    X = rng.uniform(-0.5, 0.5, (5, 2))
    hits, dist = net.search(X, k=5)
    print("\nsearch     : ranked hits for 5 queries (k=5)")
    for r, (h, d) in enumerate(zip(hits, dist)):
        print(f"  query {r}: units {h.tolist()}  d {np.round(d, 4).tolist()}")

    # identity lookup: search the homes, not the positions
    ih, id_ = net.search_by_identity(0.35 * np.array([1.0, 0.0]), k=3)
    print(f"identity   : nearest homes to (0.35, 0) -> {ih.tolist()}")

    # consensus: local agreement (reciprocity of the k-NN graph)
    print(f"\nconsensus  : k-NN reciprocity {net.consensus():.3f} "
          f"(1.0 = every link mutual)")

    # blockchains: prove tamper-evidence
    head = net.chain_head(3)
    net.chains.chains[3].blocks[net.chains.length(3) - 1]["payload"] = b"tampered"
    ok, unit, seq = net.verify_ledger()
    print(f"tamper     : flipping unit 3's last block -> verified {ok}, "
          f"first bad unit {unit}, block seq {seq}")
    print(f"            head before {head[:16]}... "
          f"(chains are content-addressed; the head no longer matches)")
    print(f"\nstatus     : {net.status()}")


if __name__ == "__main__":
    main()
