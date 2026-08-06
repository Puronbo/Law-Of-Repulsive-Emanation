# puno_flow

Exact, sub-quadratic, local-only balance flow.  Every unit keeps a private
home `h_i` and talks only to its `k` nearest neighbours - no global mean, no
global gradient, no central controller:

```
g_i = -A*(mu0 + mu)*(q_i - h_i)  +  sum_{j in kNN(i)} (q_i - q_j)/|d|^3
q_i <- clamp(q_i + dt * g_i / |g_i|)
```

This package is the standalone embodiment of PPA-001 (the Puno flow
dynamics).  Its distinguishing property is **exactness at scale**: the k-NN
sets come from a spatial index instead of an n x n distance matrix, the
results are *identical* to the all-pairs path (bit for bit, asserted by the
test suite), and the indexed path runs where the all-pairs distance matrix
cannot physically fit.

## Why the index is exact, not approximate

The grid buckets points into cells whose size tracks the local density.  A
query scans an expanding Chebyshev ring of cells and stops once the k-th
candidate distance `d_k` satisfies `d_k <= r * cell`, where `r` is the ring
index.  Every point in an unscanned cell (ring `r+1` or beyond) is at least
`r * cell` away in any coordinate, hence at least `d_k` away in Euclidean
distance - so no closer point can hide outside the scanned region.  The
answer is exact for *any* point set; only the expected work per query is
constant.  The termination bound is the same argument that makes the result
provably true k-NN, so the indexed trajectory is bit-identical to the exact
all-pairs trajectory.

## Verified numbers (see `examples/benchmark_card.py`)

| n (dim=2, k=8) | indexed 2D flow | all-pairs distance matrix |
| -------------- | --------------- | ------------------------- |
| 100,000        | 5.8 s/step      | 160 GB                    |
| 1,000,000      | 63 s/step       | 16,000 GB                 |

The 1M run is physically impossible on the all-pairs path (16 TB matrix);
the grid path runs it in about a minute per step on one CPU.  `verify_exact`
asserts bit-identity between the indexed and exact flows.

## Usage

```python
import numpy as np
from puno_flow import FlowEngine, ExactIndex, brute_knn, verify_exact, to_disk

rng = np.random.RandomState(1)
X = rng.uniform(-0.5, 0.5, (2000, 2))

net = FlowEngine(dim=2, k=8, use_index=True, index_min_n=2).add_many(X, X)
net.settle(100)      # local relaxation (mu = 0)
net.absorb(100)      # tighten toward homes (mu = 0.5)
net.heal(200)        # re-spread survivors after neuron loss
net.predict(X)       # nearest-centroid labels

ok, report = verify_exact(X, k=12, steps=5)   # bit-exactness verdict
```

The index is chosen automatically: a numpy-only uniform grid for `dim <= 3`,
scipy.cKDTree above (the grid path needs nothing beyond numpy; scipy is a
lazy, optional import for high dimensions).

## API

- `FlowEngine(dim, k, mu0, A, dt, max_r, use_index, index_min_n)`: the
  dynamics.  `settle`/`absorb`/`heal`, `predict`/`accuracy`, `spacing`,
  `add`/`add_many`/`remove`.  Inputs are copied on insertion, so several
  engines may share a source array without sharing state.
- `ExactIndex(pts, k, algorithm="auto")`: exact k-NN index
  (`algorithm="grid"` for dim <= 3, `"kdtree"` above, `"auto"` picks).
  `knn(i, k)` / `knn_all(k)` / `nearest(X)`.
- `brute_knn(X, k)`: all-pairs reference (sorted k-NN, self excluded).
- `to_disk(q, max_r=0.9)`: component-free disk clamp.
- `verify_exact(X, k, steps)`: runs indexed and exact flows and returns a
  report of bit-exactness checks (grid vs brute-force k-NN, indexed vs exact
  flow trajectory).

Run the tests with `python -m pytest tests/` and the benchmark card with
`python puno_flow/examples/benchmark_card.py [n]`.

## Toy-network extras

The package also exercises the local-only ethic in other guises
(`examples/toy_network.py`):

- **Creation** - `create(x, home=...)` / `spawn(count, ...)`: units are born
  with a genesis block over their home; `parent=` adds a provenance block.
- **Blockchains** - `ledger.py` gives every unit its own append-only,
  content-addressed chain (`sha256(prev || seq || payload)`).  `flow(record=...)`
  appends a state block per step; `verify_ledger()` audits every chain and
  detects any tamper.  Agreement is *verified locally*, not mined - there is
  no shared ledger and no proof-of-work.
- **Search engine** - `search(X, k)` returns ranked nearest-centroid hits
  (indices + distances); `search_by_identity(home, k)` searches the homes.
- **Consensus** - `consensus()` reports k-NN reciprocity: the fraction of a
  unit's neighbours that also list it among theirs (1.0 = every link mutual).
- **Status** - `status()` returns a compact snapshot (n, dim, spacing,
  consensus, ledger counts).
- **Scale-free networks** - `topology.py` (`examples/scale_free.py`):
  Barabasi-Albert preferential attachment, degree sequence, hubs, and a
  discrete maximum-likelihood power-law exponent fit (Clauset-Shalizi-
  Newman, solved by bisection).  `flow_over(edges, ...)` runs the *same*
  local balance dynamics over a fixed hubs-and-spokes wiring instead of
  k-NN - neighbourhoods are read once and held fixed while the cloud
  relaxes, and each step can still be chained to the ledger.

