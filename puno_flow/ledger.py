"""Local hash-chained ledgers for the toy decentralized network.

Blockchain-inspired: every unit owns an append-only, content-addressed chain
of state blocks.  A block is ``(prev_hash, seq, payload)`` and its own hash is
``sha256(prev_hash || seq || payload)``, so tampering with past state breaks
the chain from that block on.  Everything is LOCAL: there is no shared ledger,
no miner, no proof-of-work.  Agreement is *verified*, not mined - each unit can
prove its own history, and neighbours can cross-check a unit by asking it to
reproduce the chain (see ``FlowEngine.consensus`` for the local-agreement
check).

This is a toy ledger for the toy network: it shows the local-only ethic
extends to audit.  It is deliberately not a consensus protocol.
"""

import hashlib
import struct

import numpy as np

__all__ = ["sha256", "pack_state", "pack_indices", "LedgerChain", "ChainStore"]


def sha256(b):
    """Hex SHA-256 of a bytes payload."""
    return hashlib.sha256(b).hexdigest()


def pack_state(q):
    """Canonical bytes for a position/home: little-endian IEEE-754 doubles."""
    return np.asarray(q, dtype="<f8").tobytes()


def pack_indices(nb):
    """Canonical bytes for a k-NN index set: little-endian int32."""
    return np.asarray(nb, dtype="<i4").tobytes()


def _block_hash(prev, seq, payload):
    prev_bytes = bytes.fromhex(prev) if prev else b""
    return sha256(prev_bytes + struct.pack("<Q", seq) + payload)


class LedgerChain:
    """Append-only hash-linked chain of state blocks for one unit."""

    def __init__(self, genesis_payload=None):
        self.blocks = []
        if genesis_payload is not None:
            self.append(genesis_payload)

    def append(self, payload):
        """Append a block; returns its hash (the new chain head)."""
        seq = len(self.blocks)
        prev = self.blocks[-1]["hash"] if self.blocks else None
        h = _block_hash(prev, seq, payload)
        self.blocks.append({"seq": seq, "prev": prev, "payload": payload,
                            "hash": h})
        return h

    @property
    def head(self):
        return self.blocks[-1]["hash"] if self.blocks else None

    @property
    def length(self):
        return len(self.blocks)

    def verify(self):
        """Recompute every block hash and check the prev links.
        Returns (ok, first_bad_seq_or_None)."""
        for b in self.blocks:
            if _block_hash(b["prev"], b["seq"], b["payload"]) != b["hash"]:
                return False, b["seq"]
            if b["seq"] > 0 and b["prev"] != self.blocks[b["seq"] - 1]["hash"]:
                return False, b["seq"]
        return True, None


class ChainStore:
    """Per-unit ledgers for the whole population (still fully local)."""

    def __init__(self):
        self.chains = {}

    def genesis(self, i, payload):
        """Start unit i's chain with a genesis block (idempotent)."""
        if i not in self.chains:
            self.chains[i] = LedgerChain(payload)

    def record(self, i, payload):
        """Append a state block to unit i's chain (creating it if needed)."""
        if i not in self.chains:
            self.chains[i] = LedgerChain()
        return self.chains[i].append(payload)

    def head(self, i):
        chain = self.chains.get(i)
        return chain.head if chain else None

    def length(self, i):
        chain = self.chains.get(i)
        return chain.length if chain else 0

    def verify_all(self):
        """(ok, first_bad_unit, first_bad_seq) over every chain."""
        for i, chain in self.chains.items():
            ok, bad = chain.verify()
            if not ok:
                return False, i, bad
        return True, None, None

    def audit(self):
        """Summary: chain count, total blocks, and each chain's head hash."""
        return {
            "chains": len(self.chains),
            "blocks": sum(c.length for c in self.chains.values()),
            "heads": {i: c.head for i, c in self.chains.items()},
        }
