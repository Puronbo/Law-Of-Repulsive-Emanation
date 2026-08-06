"""Autonomous search-engine daemon.

A self-contained nearest-neighbour service: units are records (created with
a genesis block), queries are answered by the exact index with ranked hits,
every mutation is appended to an operation ledger, and the whole population
audits itself.  Runs an interactive REPL when invoked directly.

Usage:  python -m puno_flow.apps.search_service

Commands:
  insert x y [label]  - add a record (unit)
  query  x y [k]      - ranked nearest records
  stats               - population / index / ledger snapshot
  consensus           - local agreement (k-NN reciprocity)
  verify              - bit-exactness report of the index
  damage k            - kill k random records
  heal [steps]        - local re-spread after damage
  ops                 - operation ledger summary (verify + head)
  quit
"""

import sys

import numpy as np

from puno_flow import FlowEngine, LedgerChain, verify_exact


class SearchService:
    """A tiny autonomous search service on top of the toy network."""

    def __init__(self, dim=2):
        self.engine = FlowEngine(dim=dim, k=8)
        self.labels = {}
        self.op_chain = LedgerChain()          # append-only op log

    def _log_op(self, text):
        self.op_chain.append(text.encode("utf-8"))

    def insert(self, x, y, label=None):
        i = self.engine.create(np.array([float(x), float(y)]))
        if label:
            self.labels[i] = label
        self._log_op(f"insert {x} {y} {label or ''}")
        return i

    def query(self, x, y, k=5):
        hits, dist = self.engine.search(np.array([float(x), float(y)]), k=k)
        return [(int(i), float(d), self.labels.get(int(i)))
                for i, d in zip(hits, dist)]

    def damage(self, k, rng=None):
        rng = np.random.RandomState(3) if rng is None else rng
        k = min(int(k), self.engine.n)
        drop = rng.choice(self.engine.n, size=k, replace=False)
        self.engine.remove(drop)
        self._log_op(f"damage {k}")
        return sorted(int(i) for i in drop)

    def heal(self, steps=50):
        self.engine.heal(steps, record=True)
        self._log_op(f"heal {steps}")

    def stats(self):
        s = self.engine.status()
        ok, unit, seq = self.engine.verify_ledger()
        s["ledger_verified"] = ok
        s["op_log_verified"] = self.op_chain.verify()[0]
        s["op_log_blocks"] = self.op_chain.length
        return s

    def verify(self, steps=3):
        return verify_exact(self.engine.q, k=min(self.engine.k, 12),
                            steps=steps)[1]

    def ops(self):
        return {
            "blocks": self.op_chain.length,
            "head": self.op_chain.head[:16],
            "verified": self.op_chain.verify()[0],
        }


def dispatch(line, svc):
    """Handle one command line; returns the reply string."""
    parts = line.split()
    if not parts:
        return ""
    cmd = parts[0].lower()
    try:
        if cmd == "insert" and len(parts) >= 3:
            i = svc.insert(parts[1], parts[2],
                           parts[3] if len(parts) > 3 else None)
            return f"record {i} inserted (genesis block written)"
        if cmd == "query" and len(parts) >= 3:
            k = int(parts[3]) if len(parts) > 3 else 5
            rows = svc.query(parts[1], parts[2], k)
            return "\n".join(
                f"  #{i}  d={d:.4f}  {label or '(no label)'}"
                for i, d, label in rows)
        if cmd == "stats":
            s = svc.stats()
            return (f"  n={s['n']}  dim={s['dim']}  k={s['k']}"
                    f"  spacing={s['spacing']:.4f}"
                    f"  consensus={s['consensus']:.3f}\n"
                    f"  unit ledgers: {s['ledger_chains']} chains,"
                    f" {s['ledger_blocks']} blocks,"
                    f" verified={s['ledger_verified']}\n"
                    f"  op log: {s['op_log_blocks']} blocks,"
                    f" verified={s['op_log_verified']}")
        if cmd == "consensus":
            return f"  k-NN reciprocity {svc.engine.consensus():.3f}"
        if cmd == "verify":
            report = svc.verify()
            return (f"  grid==brute {report['grid_knn_equals_bruteforce']}"
                    f"  indexed==exact {report['indexed_flow_bit_identical_to_exact']}"
                    f"  verdict {report['verdict']}")
        if cmd == "damage" and len(parts) >= 2:
            return f"  removed {svc.damage(parts[1])} (heal to reflow)"
        if cmd == "heal":
            steps = int(parts[1]) if len(parts) > 1 else 50
            svc.heal(steps)
            return f"  healed for {steps} steps (local re-spread)"
        if cmd == "ops":
            o = svc.ops()
            return (f"  {o['blocks']} blocks, head {o['head']}...,"
                    f" verified {o['verified']}")
        if cmd in ("quit", "exit"):
            return "bye"
        return f"  unknown command: {cmd}"
    except (ValueError, IndexError) as e:
        return f"  error: {e}"


def main():
    svc = SearchService()
    print("autonomous search service - type a command (help: insert/query/"
          "stats/consensus/verify/damage/heal/ops/quit)")
    for line in sys.stdin:
        line = line.strip()
        if line.lower() in ("quit", "exit"):
            print(dispatch(line, svc))
            break
        reply = dispatch(line, svc)
        if reply:
            print(reply)


if __name__ == "__main__":
    main()
