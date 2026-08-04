"""
T72: FLOW THE WHOLE INTERNET (T67's unlock, executed).

T55i persisted the real internet net: the 1.9M-site union of two independent
top-1M popularity lists (Cisco Umbrella + Majestic Million), one 128D
character-ngram neuron per site (T55g's geometry).  T55g could only FLOW a
1000-site slice because flow was all-pairs O(n^2); T55h measured the
all-pairs ceiling at ~2x10^4 and T67 built the O(1)-per-neuron spatial index
that makes flow ~linear.  T72 is the point of that work: the ENTIRE 1.9M-site
population is flowed for real.

  PART 0  load the real 1.9M checkpoint (internet_net_full.pkl, T55i)
  PART 1  flow geometry: PCA(2) of the real 1.9M x 128D embeddings - the
          net's dominant 2D shape.  Honest why: the 128D native space hits
          crease #22 (k-d trees degenerate in high dimension), so the
          internet's FLOW space is the low-dim projection while its 128D
          space stays the routing/embedding space (T55i).  The projection
          is real internet topology, not noise - ~11% of embedding variance
          (measured below).
  PART 2  FLOW THE WHOLE INTERNET: settle the entire 1.9M population with
          the T67 grid index.  all-pairs D would be 1.9M^2*2*8 = 58 TB.
  PART 3  self-healing at full population: kill 20% (380k sites), local
          heal, and measure consensus-spacing recovery across the survivors.
  PART 4  the 128D native wall (crease #22): a real cKDTree flow step on a
          10k slice of the actual embeddings, as the honest high-dim bound.

Usage: python decentral_net_t72.py
"""

import json
import os
import pickle
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "Universals"))
from manifold.decentral_net import DecentralNet  # noqa: E402

TOP = os.path.expandvars(r'%LOCALAPPDATA%\Temp\opencode\top1m')
PKL = os.path.join(TOP, 'internet_net_full.pkl')
DATA_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "data", "decentral_net_t72_data.json")

results = {}


def ms_step(net, steps):
    t0 = time.time()
    net.settle(steps)
    return (time.time() - t0) * 1000.0 / steps


# ---------------------------------------------------------------------- #
def main():
    print("=" * 72)
    print("T72: FLOW THE WHOLE INTERNET - the real 1.9M-site population")
    print("=" * 72)

    # ---- PART 0: load the real internet net --------------------------- #
    print("\n--- PART 0: load the real 1.9M checkpoint (T55i) -------------")
    t0 = time.time()
    with open(PKL, "rb") as f:
        art = pickle.load(f)
    net128, domains = art["net"], art["domains"]
    n = net128.n
    load_s = time.time() - t0
    print(f"  loaded n={n:,} real sites, dim={net128.q.shape[1]}, "
          f"q+h={net128.q.nbytes * 2 / 1e9:.2f} GB in {load_s:.1f}s")

    # ---- PART 1: the 2D flow geometry (PCA of the real embeddings) ---- #
    print("\n--- PART 1: 2D flow geometry from the real 128D embeddings ---")
    from sklearn.decomposition import PCA
    t0 = time.time()
    pca = PCA(n_components=2, svd_solver="randomized", random_state=42)
    P = pca.fit_transform(net128.q)
    evr = pca.explained_variance_ratio_
    print(f"  PCA(2) of {n:,} x 128D in {time.time()-t0:.1f}s; "
          f"explained variance = {evr[0]:.3f} + {evr[1]:.3f} "
          f"(~{100*evr.sum():.1f}% of the real internet embedding shape)")
    Pc = P - P.mean(axis=0)
    P2 = Pc * (0.7 / np.max(np.linalg.norm(Pc, axis=1)))
    net = DecentralNet(dim=2, k=8, mu0=0.12, use_index=True).add_many(P2, P2)
    print(f"  flow net: n={net.n:,} dim=2, homes = PCA coords, "
          f"spread to radius 0.7")

    # ---- PART 2: FLOW THE WHOLE INTERNET ------------------------------ #
    print("\n--- PART 2: flow the WHOLE internet population ---------------")
    d_gb = n * n * 2 * 8 / 1e9
    sp0 = net.spacing()
    ms = ms_step(net, 1)
    sp2 = net.spacing()
    print(f"  settle(1) at n={n:,}: {ms:.0f} ms/step "
          f"(all-pairs D would need {d_gb:,.0f} GB)")
    print(f"  consensus spacing (median k-NN distance): {sp0:.4f} -> "
          f"{sp2:.4f} over the whole internet")
    print(f"  (whole step amortizes to ~{ms*1e6/n:.0f} us/neuron "
          f"(index + kNN + loop); flow stays exact but each full-population "
          f"step costs ~{ms/1000:.0f}s)")
    results["flow_whole_internet"] = {
        "n_sites": int(n),
        "ms_per_step": round(ms, 1),
        "allpairs_d_gb": round(d_gb, 0),
        "spacing_before": float(sp0),
        "spacing_after_step": float(sp2),
        "pca_explained_var_2d": float(evr.sum()),
        "verdict": "MEASURED",
    }

    # ---- PART 3: self-healing at full population ---------------------- #
    print("\n--- PART 3: self-healing at full population ------------------")
    rng = np.random.RandomState(42)
    kill = rng.choice(n, size=int(0.2 * n), replace=False)
    net.remove(list(kill))
    sp_k = net.spacing()
    print(f"  killed {len(kill):,} sites (20%) -> survivors {net.n:,}")
    ms_h = ms_step(net, 1)
    sp_h = net.spacing()
    print(f"  local heal(1) at n={net.n:,}: {ms_h:.0f} ms/step; "
          f"spacing {sp_k:.4f} -> {sp_h:.4f} "
          f"(recovery {(sp_h - sp_k) / max(sp_k, 1e-9) * 100:+.1f}%)")
    results["heal_whole_internet"] = {
        "killed": int(len(kill)),
        "survivors": int(net.n),
        "spacing_after_kill": float(sp_k),
        "heal_ms_per_step": round(ms_h, 1),
        "spacing_after_heal": float(sp_h),
        "verdict": "MEASURED",
    }

    # ---- PART 4: the 128D native wall (crease #22) -------------------- #
    print("\n--- PART 4: the 128D native wall (crease #22) ----------------")
    rng = np.random.RandomState(0)
    pick = rng.choice(n, size=10000, replace=False)
    net128b = DecentralNet(dim=128, k=8, mu0=0.12,
                           use_index=True).add_many(net128.q[pick])
    ms_hi = ms_step(net128b, 1)
    d_hi = 10000 * 10000 * 128 * 8 / 1e9
    print(f"  real 128D flow, n=10,000: {ms_hi:.0f} ms/step "
          f"(all-pairs D = {d_hi:,.0f} GB) - the high-dim tree wall that "
          f"keeps 128D-native flow near 10^4; the 2D geometry above is the "
          f"whole-population path")
    results["highdim_wall"] = {
        "n": 10000,
        "ms_per_step": round(ms_hi, 1),
        "allpairs_d_gb": round(d_hi, 0),
        "verdict": "MEASURED",
    }

    results["limits"] = {
        "flow_geometry_is_2d_projection": "the whole internet is flowed in "
            "the PCA(2) projection of its real 128D embeddings (~11% of "
            "variance); the 128D native space is the routing/embedding space "
            "(T55i) and its flow stays near 10^4 (crease #22)",
        "one_machine": "this is still one 31.7 GB box (T20/T67); a true "
            "distributed flow across machines remains unbuilt",
        "sequential_flow": "flow keeps its Gauss-Seidel per-neuron loop "
            "(identical to T67; a vectorized Jacobi update would change the "
            "dynamics)",
    }

    os.makedirs(os.path.dirname(DATA_JSON), exist_ok=True)
    with open(DATA_JSON, "w") as f:
        json.dump(results, f, indent=2)
    print("\n  verdicts written to data/decentral_net_t72_data.json")

    print("=" * 72)
    print("T72: the real 1.9M-site internet, flowed at O(n) per step")
    print(f"  {ms:.0f} ms/step at n={n:,} vs an all-pairs D of {d_gb:,.0f} GB.")
    print("  The whole internet now FLOWS, not just the 1000-site slice.")
    sys.exit(0)


if __name__ == "__main__":
    main()
