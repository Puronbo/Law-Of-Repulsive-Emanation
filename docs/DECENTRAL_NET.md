# DecentralNet — a reusable, self-healing knowledge-graph segment

A numpy-only decentralized network whose units update from **local** information
alone (private home + k nearest neighbours; no global mean, no central
controller).  Routed by plain nearest-centroid.  This file is the "segment"
entry point: what it is, how to reuse the shipped internet artifact, and the
transferable findings the T55a–i series produced.

## Segment inventory

| Piece | Location |
|---|---|
| Module | `Universals/manifold/decentral_net.py` (`DecentralNet`) |
| Internet net artifact | `%LOCALAPPDATA%\Temp\opencode\top1m\internet_net.pkl` (3.17 GB) |
| Source lists | Cisco Umbrella `top-1m.csv` + Majestic Million (merged, 1,914,915 unique domains) |
| Daemon | `experiments/decentral_net_live.py` (indefinite run + checkpoint/resume) |
| Benchmarks | `experiments/decentral_net{,_mnist,_continual,_internet,_union,_ceiling}.py` |

```python
import pickle, numpy as np
art = pickle.load(open(r'%LOCALAPPDATA%\Temp\opencode\top1m\internet_net.pkl','rb'))
net, domains = art['net'], art['domains']          # net.q (n×128), net.h homes
sims = net.q @ net.q[domains.index('google.com')]  # nearest-centroid routing
```

## How it works (one line each)

- **Flow**: `q_i += dt·g/|g|`, `g = -A·(mu0+mu)·(q_i−h_i) + Σ_{j∈kNN(i)} (q_i−q_j)/|d|³`
- **Routing**: `label(x) = argmin_i |x − q_i|` (nearest centroid)
- **Self-healing**: kill neurons at random → survivors keep routing; `heal()` re-spreads
- **Capacity**: `add_many(X, homes=X)` is vectorized; ~2 KB/site at dim=128

## Transferable findings (for any other project)

1. **Training-free routing.** Hashed character-ngram embeddings of *names*
   (`HashingVectorizer(analyzer='char_wb', ngram_range=(2,4), n_features=128,
   norm='l2', alternate_sign=True)`) put related items close with zero labels:
   `google.com→gooogle.com/google.com.om`, `microsoft.com→mp.microsoft.com`.
   A nearest-centroid lookup on those embeddings is a working "knowledge graph"
   with no model training.  Any entity-similarity task (domains, package names,
   malware-families, chemical names) can copy this pattern verbatim.

2. **Damage tolerance without a repair unit.** Randomly deleting 20% of a
   1.9M-neuron net leaves routing intact; killed items re-resolve to their
   nearest living sibling.  Decentralization buys fail-open lookup for free.

3. **The scaling law is not what you fit at small n.** All-pairs kNN flow
   measured n^1.76 at n≤5000 but **n^2.06 between 5k and 20k** (the D array
   leaves cache).  Never extrapolate a fitted exponent past the fitted range.

4. **RAM wall is the *sort temporaries*, not the data.** The n²×8 B distance
   matrix under-estimates peak memory: kNN sort temp peaked at **22.6 GB
   working set at n=20,000 (D itself only 3.2 GB)** → real all-pairs ceiling on
   a 31.7 GB box is ~2×10⁴, not the naive 5×10⁴.  Holding is cheap (~2 KB/node);
   flowing is not.  Scaling flow past 20k needs O(1)-per-neuron spatial search.

5. **Array mutation breaks labels.** After `remove()`, surviving rows no longer
   index the original label list — remap explicitly (survivor→name map), or you
   get similarity 1.000 against the wrong entity.  Applies to any
   delete-then-index pipeline.

6. **Never mix coordinate frames.** Appending a raw centroid to an already
   flowed/anchor-settled set collapses routing (~0.86→~0.04).  Always reflow
   (settle/absorb) after add/remove.  Gauge freedom means the anchor set floats
   as a whole — consistency beats accuracy when homes are data centroids.

7. **Long-running daemon pattern.** Pickle the whole object (state + RNG +
   counters), drain on SIGINT/SIGTERM/stopfile, checkpoint periodically.
   Verified resume keeps exact counters (tick, born, killed).  Reusable for any
   indefinite background worker.

8. **Windows RAM without psutil.** `ctypes` + `psapi.GetProcessMemoryInfo`
   needs `OpenProcess(PROCESS_QUERY_INFORMATION, …)` + `CloseHandle`; the
   `GetCurrentProcess()` pseudohandle fails with ERROR_INVALID_HANDLE (6).

## Series trail (commits)

T55a/T55c multi-seed calibration · T55b flow-reg retest · T55d MNIST · T55e
continual/mixing caveats · T55f indefinite daemon + checkpoint · T55g real
top-1M copy · T55h measured flow ceiling (~2×10⁴) · T55i union fill + persisted
artifact (1.9M widely-used sites).
