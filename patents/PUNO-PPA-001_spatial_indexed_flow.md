---
title: "Provisional Patent Application"
subtitle: "System and Method for Exact O(1)-Expected-Per-Neuron Spatial-Indexed Population Flow"
docket: "PUNO-PPA-001"
inventor: "Michael Grafiel Sayson Puno"
date: "2026-08-04"
---

# PROVISIONAL PATENT APPLICATION

## System and Method for Exact O(1)-Expected-Per-Neuron Spatial-Indexed Population Flow

**Docket:** PUNO-PPA-001
**Inventor:** Michael Grafiel Sayson Puno
**Filed (priority date basis):** 2026-08-04
**Corpus reference:** Puno Calculus T67/T72 (`experiments/decentral_net_t67.py`, `experiments/decentral_net_t72.py`, `Universals/manifold/decentral_net.py`, `data/decentral_net_t67_data.json`, `data/decentral_net_t72_data.json`)

---

## 1. TITLE OF THE INVENTION

System and Method for Exact Spatial-Indexed Population Flow with Provably-Identical Dynamics to All-Pairs Reference Flow.

## 2. FIELD OF THE INVENTION

The invention relates to the computational simulation of interacting populations of agents (also called neurons, particles, or sites) in a metric space, and more particularly to methods for advancing a per-agent dynamics that depends on the k nearest neighbors of each agent, where the reference (all-pairs) dynamics is exactly O(n²) per step and becomes infeasible for populations above roughly 10⁴ agents. The invention makes the per-step cost O(n) expected time and O(n) memory for low dimension (≤ 3) and O(n log n) for higher dimension, **without changing any trajectory value**.

## 3. BACKGROUND OF THE INVENTION

### 3.1 Population-flow dynamics

A large class of computational models updates each agent according to its k nearest neighbors:

    for each agent i in 1..n:
        out   = q[i] - q[nb[i]]                  // vectors to k nearest neighbors
        rep   = sum_j out_j / |out_j|^3          // local repulsion
        g     = -A·m·(q[i] - h[i]) + rep         // home-trap + repulsion
        q[i] += dt · g / (|g| + eps)             // normalized step

Here q[i] is the agent's position, h[i] is a private anchor ("home"), k is the neighborhood size, dt a step size, and A, m, eps parameters. This is a Gauss-Seidel loop: each agent sees the already-updated positions of earlier agents in the same step. The dynamics depends on the positions **only through the neighbor sets** nb[i].

### 3.2 The all-pairs wall

The straightforward implementation computes, each step, the full n×n×dim distance structure to identify neighbor sets. This is O(n²) in time and memory. For float64 2-D data, the distance array alone is n²·16 bytes: n=100,000 requires 160 GB; n=1,914,915 requires 58,670 GB (≈58.7 TB). Populations beyond roughly 2×10⁴ therefore cannot be flowed at all with the reference method on conventional hardware.

### 3.3 Prior approaches and their limitations

1. **Approximate nearest-neighbor (ANN) indexing** (e.g., locality-sensitive hashing, random projection trees): return neighbor sets that are approximately correct. Because the flow dynamics depends exactly on the neighbor sets, approximate neighbor sets produce **different trajectories**, so an approximate index cannot substitute for the reference dynamics when bit-identical reproducibility is required.
2. **Ball trees / kd-trees**: exact for low dimension but their worst-case behavior degrades with dimension and data density; standard implementations give no end-to-end guarantee that the returned neighbor sets equal the true sets for the flow's use.
3. **Spatial hashing without a termination proof**: uniform-grid hashing is common for approximate range queries, but prior grid methods return candidates from a fixed search radius and can silently miss closer neighbors, again changing the dynamics.

None of the prior approaches provides: (a) exact neighbor sets for arbitrary input sets; (b) a termination argument that any unscanned cell cannot contain a closer neighbor; and (c) measured bit-identical equality of the resulting flow trajectories with the all-pairs reference.

## 4. SUMMARY OF THE INVENTION

The invention provides a method and system for flowing a population of n agents under a k-nearest-neighbor dynamics at O(n) expected time and O(n) memory per step in dimension ≤ 3, and O(n log n) in higher dimension, while producing trajectories **bit-identical** to the all-pairs reference.

The method comprises:

- **A) Index construction:** partition the agent positions into uniform grid cells sized so that the expected occupancy is approximately the neighborhood size k. For each agent, compute its cell; store, per cell, the list of contained agents.
- **B) Precomputed ring scan:** precompute, once, the set of Chebyshev-ring offsets used in the scan, so that a query pays only the per-query ring walk, never a re-generation of offsets or a seen-set.
- **C) Exact query with termination proof:** for a query agent, scan its own cell then Chebyshev rings r = 1, 2, …; accumulate candidate agents; stop when at least k candidates are present **and** the k-th smallest candidate distance d_k satisfies d_k ≤ r·cell (the Chebyshev-ring radius). The termination condition is exact: every unscanned agent lies in a cell whose Chebyshev ring is ≥ r+1, so its Euclidean distance to the query is ≥ (r·cell) ≥ d_k, and it cannot be among the k nearest. The returned set is therefore exactly the true k-nearest set for every input set, with no approximation; only the expected number of scanned cells is constant per query.
- **D) High-dimension path:** for dimension ≥ 4, an exact k-d tree (or equivalent exact spatial structure) returns the k+1 nearest per agent with the self-neighbor dropped.
- **E) Dynamics:** advance the agents with the reference Gauss-Seidel update using the index-provided neighbor sets. Because the neighbor sets are identical to the all-pairs sets, the trajectory is bit-identical to the reference flow.

The invention further provides a correctness gate: before and during use, the indexed flow is compared to the all-pairs flow (small n) and required to satisfy bit-level equality of positions, spacing, and predictions; the grid k-NN is compared pointwise to brute-force k-NN across seeds and dimensions.

## 5. DETAILED DESCRIPTION

### 5.1 System

A computing system (one or more processors, memory, storage) holds: agent positions q ∈ R^{n×dim}; optional anchors h ∈ R^{n×dim}; parameters k (default 8), dt (default 0.05), A (default 120.0), m = mu0 + mu (default mu0 = 0.12), a disk-bound max radius (default 0.9), and an epsilon floor (default 1e-3). A spatial index is enabled when use_index = true and n ≥ 512.

### 5.2 Grid index construction (dim ≤ 3)

Let the per-dimension span be span = max(hi − lo, 1e-12) and volume vol = span^dim. Choose cell size

    cell = max( (vol · max(k,1) / max(n,1))^(1/dim), 1e-9 )

so that expected occupancy (n/vol)·cell^dim ≈ k. Set origin = lo − 0.5·cell and per-axis counts ni = max(ceil((span+cell)/cell), 1). Hash each point to the integer cell index

    idx = clip( floor((pts − origin)/cell), 0, ni−1 )

and build cells: {tuple index → list of point ids}. Precompute the Chebyshev-ring offset sets once: ring 0 = own cell; ring r = all offsets o ∈ {−r..r}^dim with max|o| == r.

### 5.3 Exact query

For query i with drop = i (self excluded): scan ring 0, then ring 1, 2, … accumulating candidate ids, until |candidates| ≥ k and the k-th smallest Euclidean distance to candidates satisfies

    d_k = partition(candidate distances, k−1)[k−1] ≤ r·cell

then return the k closest sorted by distance. If the bound never triggers (adversarial cluster), the scan falls back to sorting all ring-unscanned candidates, which returns the exact set unconditionally. Because the L∞ distance from the query to any agent in ring r+1 is at least (r+1−1)·cell = r·cell and Euclidean ≥ L∞, no unscanned agent can be closer than d_k; the result is exact.

### 5.4 High-dimension path (dim ≥ 4)

A scipy.spatial.cKDTree (or equivalent exact tree) is built per step from current positions; each query returns the k+1 nearest and the self-column is dropped. The tree lazily imports its backend and falls back to exact all-pairs on absence, preserving correctness.

### 5.5 Flow step

    nb = index.knn_all(k)                    // exact neighbor sets
    for i in 1..n:                            // sequential Gauss-Seidel
        out  = q[i] − q[nb[i]]
        r3   = max(|out|, eps)^3
        rep  = Σ_j out_j / r3_j
        g    = −A·m·(q[i] − h[i]) + rep
        q[i]+= dt · g / (|g| + 1e-9)
    q = to_disk(q, max_r)                     // optional clamp to a bounded region

### 5.6 Measured results (per the supporting corpus)

Measured on a single 31.7 GB machine (float64):

| n (2-D grid) | exact ms/step | indexed ms/step |
|---|---|---|
| 1,000 | 48.61 | 39.72 |
| 2,000 | 170.73 | 80.60 |
| 4,000 | 606.85 | 162.86 |
| 8,000 | 2,454.21 | 329.27 |
| 16,000 | — | 668.42 |
| 32,000 | — | 1,348.83 |
| 64,000 | — | 2,800.44 |
| 100,000 | — | 4,502.87 |

Fitted exponents over n: exact **1.88** (≈O(n²)); indexed **1.025** (≈O(n)).

- **n = 100,000 in 2-D (internet-scale run with disk clamp and spacing instrumentation):** 5,333.5 ms/step; all-pairs distance array would be 160 GB (physically infeasible). The scaling-series row above (4,502.87 ms/step) is a separate bare-flow measurement of the same size.
- **n = 10,000 × 128-D real domain embeddings:** 2,076 ms/step via the exact tree; all-pairs would be 102.4 GB.
- **n = 1,914,915 (whole-internet population):** 277,218 ms/step; all-pairs distance array would be 58,670 GB. Consensus spacing 0.000327 → 0.000364; after removing 382,983 agents (20%) and one heal step, spacing recovered +7.8%.
- **Bit-identical verification:** 2-D grid vs brute force (2000 agents, 10 steps) and 64-D tree vs brute force (500 agents, 5 steps): `np.array_equal(a.q, b.q) == true`; spacing equal; predictions equal; grid k-NN equal to brute force pointwise across seeds {1,2,3} × dims {1,2,3} × n=1000, k=12.

### 5.7 Honest limits

- In dimension ≥ 4 with dense high-dim data, exact k-d trees degrade (~5–16 s/step at n=10⁴×128-D), so the high-dimension indexed ceiling is ~10⁴ agents; the low-dimension grid flows 10⁵+ on one box.
- The method as measured is single-machine; distributed flow is not part of this application.
- The Gauss-Seidel (sequential) loop is preserved; a vectorized Jacobi variant changes the dynamics and is outside the claimed method.

## 6. CLAIMS (provisional)

1. A computer-implemented method for flowing a population of n agents in a metric space under a k-nearest-neighbor dynamics, comprising: partitioning agent positions into uniform grid cells sized for approximately k points per cell; precomputing Chebyshev-ring offsets; for each agent, scanning cells by ring and accumulating candidates until the number of candidates is at least k and the k-th smallest candidate distance is no greater than the ring radius times the cell size, whereby no unscanned agent can be nearer, thereby returning an exact k-nearest-neighbor set; and advancing each agent's position by a rule that depends on its exact neighbor set.

2. The method of claim 1, wherein for dimensions greater than 3 the exact neighbor set is obtained from an exact tree data structure.

3. The method of claim 1, wherein the advance rule is a Gauss-Seidel update in which each agent's update uses the already-updated positions of earlier agents in the same step.

4. The method of claim 1, wherein the produced trajectory is bit-identical to the trajectory produced by an all-pairs reference that computes the full distance structure, because both use the same neighbor sets.

5. The method of claim 1, further comprising a verification gate that compares indexed flow to all-pairs flow at small n and requires bit-level equality of positions, spacing, and prediction outputs before enabling the index for large n.

6. A system comprising one or more processors and memory, configured to perform the method of any of claims 1–5.

## 7. ABSTRACT

A system and method for flowing a population of agents under a k-nearest-neighbor dynamics at O(n) expected time and memory per step in low dimension (grid spatial index with a Chebyshev-ring scan whose termination is proven exact) and O(n log n) in higher dimension (exact tree). The index returns the true neighbor sets for arbitrary input, so trajectories are bit-identical to the all-pairs reference; measured exponents fall from 1.88 to 1.025, and a 1,914,915-agent population (58.7 TB all-pairs) flows at 277,218 ms/step on one machine.

---

*This document is a provisional disclosure establishing a priority date for the subject matter described. All measured values are reproduced from the inventor's verified corpus (2026-08-04); no assertion is made regarding patentability beyond enablement and written description.*
