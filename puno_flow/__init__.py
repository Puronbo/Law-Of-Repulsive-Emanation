"""puno_flow: exact, bit-identical large-scale agent flow (Puno PPA-001).

Public API:
    ExactIndex   - exact k-NN: uniform grid for dim <= 3, scipy.cKDTree above.
    FlowEngine   - local-only balance flow (settle / absorb / heal / predict).
    verify_exact - prove that the indexed path equals brute force, bit for bit.
    brute_knn    - all-pairs reference implementation.

The exactness guarantee is testable, not claimed: tests/test_puno_flow.py and
puno_flow.verify.assert the indexed k-NN sets equal brute force and that
indexed flow trajectories are bit-identical to the exact all-pairs path.
"""

from .engine import FlowEngine, to_disk
from .index import ExactIndex, brute_knn
from .ledger import ChainStore, LedgerChain, pack_indices, pack_state, sha256
from .topology import (
    degree_sequence,
    hubs,
    power_law_exponent,
    preferential_attachment,
    topology_stats,
)
from .verify import verify_exact

__version__ = "0.1.0"

__all__ = ["ExactIndex", "FlowEngine", "brute_knn", "to_disk", "verify_exact",
           "ChainStore", "LedgerChain", "pack_indices", "pack_state", "sha256",
           "preferential_attachment", "degree_sequence", "power_law_exponent",
           "hubs", "topology_stats"]
