"""
Incremental class growth with C0 reflow (continual learning).

When a new class arrives, the C0 flow re-spaces all anchors so the new
one gets a valid position while old anchors move only slightly.

Evaluation per stage:
  - old-anchor displacement (should be small -> no forgetting)
  - routing accuracy on ALL classes (new + old)
  - routing accuracy on the original 5 classes only (forgetting measure)

Baseline: "random-add" - new anchor placed at a random disk position,
no reflow. The new anchor can land on an existing anchor -> new class
cannot be routed.
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Universals'))
from manifold.c0_flow import c0_flow, to_disk, pair_stats
from manifold.polysphere import PolysphereRouter

rng = np.random.RandomState(7)

max_r = 0.8
noise = 0.04
pts_per_class = 150

def gen_data(anchors, noise, max_r):
    pts, labels = [], []
    for j in range(len(anchors)):
        p = anchors[j] + rng.randn(pts_per_class, 2) * noise
        pts.append(to_disk(p, max_r=0.9)); labels.extend([j]*pts_per_class)
    return np.vstack(pts), np.array(labels)

def routing_acc(anchors, points, labels, n_trials=150):
    truths = [lambda X, j=j, c=anchors[j]: -np.linalg.norm(X - c, axis=1)
              for j in range(len(anchors))]
    router = PolysphereRouter(n_faces=len(anchors), truths=truths, seed=42)
    n_half = 8
    n_classes = len(anchors)
    correct = 0
    for _ in range(n_trials):
        j_true = rng.randint(n_classes)
        j_fake = (j_true + rng.randint(1, n_classes)) % n_classes
        mt = labels == j_true; mf = labels == j_fake
        if mt.sum() < n_half or mf.sum() < n_half: continue
        bt = rng.choice(np.where(mt)[0], n_half)
        bf = rng.choice(np.where(mf)[0], n_half)
        Xb = np.vstack([points[bt], points[bf]])
        yb = np.array([1.0]*n_half + [0.0]*n_half)
        pred, _ = router.route_batch(Xb, yb, signed=True)
        if pred == j_true: correct += 1
    return correct / n_trials

def routing_acc_subset(anchors, points, labels, subset, n_trials=100):
    truths = [lambda X, j=j, c=anchors[j]: -np.linalg.norm(X - c, axis=1)
              for j in range(len(anchors))]
    router = PolysphereRouter(n_faces=len(anchors), truths=truths, seed=42)
    n_half = 8
    correct = 0
    for _ in range(n_trials):
        j_true = int(rng.choice(subset))
        j_fake = (j_true + rng.randint(1, len(anchors))) % len(anchors)
        mt = labels == j_true; mf = labels == j_fake
        if mt.sum() < n_half or mf.sum() < n_half: continue
        bt = rng.choice(np.where(mt)[0], n_half)
        bf = rng.choice(np.where(mf)[0], n_half)
        Xb = np.vstack([points[bt], points[bf]])
        yb = np.array([1.0]*n_half + [0.0]*n_half)
        pred, _ = router.route_batch(Xb, yb, signed=True)
        if pred == j_true: correct += 1
    return correct / n_trials

# ===================================================================
# Stage 1: 5 classes
# ===================================================================
print("=" * 60)
print("INCREMENTAL CLASS GROWTH WITH C0 REFLOW")
print("=" * 60)

K0 = 5
init = to_disk(rng.randn(K0, 2) * 0.1, max_r=0.3)
anchors = c0_flow(init, n_steps=800, dt=0.02, friction=0.04, max_r=max_r)

d_min, d_mean = pair_stats(anchors)
print(f"\nStage 1 ({K0} classes): min_d={d_min:.4f} mean_d={d_mean:.4f}")

pts, labels = gen_data(anchors, noise, max_r)
acc0 = routing_acc(anchors, pts, labels, 150)
print(f"  routing acc: {acc0:.3f}")

# ===================================================================
# Growth stages
# ===================================================================
print(f"\n{'Stage':<6}{'method':<12}{'min_d':<8}{'disp_old':<10}{'new_acc':<9}{'old_acc':<9}{'all_acc':<8}")
print("-" * 66)

results_reflow, results_rand = [], []
for k in range(K0 + 1, 11):
    for method in ["reflow", "random-add"]:
        # Current anchors for the existing classes (position index 0..k-2)
        old_anchors = anchors.copy()  # starts from previous stage's layout
        n_old = k - 1

        if method == "reflow":
            # New anchor starts at the disk center (weak-repulsion zone),
            # then ALL k anchors re-flow to make room.
            new_init = np.vstack([old_anchors[:n_old], [[0.0, 0.0]]])
            new_anchors = c0_flow(new_init, n_steps=800, dt=0.02, friction=0.04, max_r=max_r)
        else:
            # Random-add baseline: place new anchor at a random position, no reflow.
            new_anchor = to_disk(rng.randn(1, 2) * 0.7)
            new_anchors = np.vstack([old_anchors[:n_old], new_anchor])

        # Data generated around the current anchors (environment co-evolves)
        pts_k, labels_k = gen_data(new_anchors, noise, max_r)

        # Old-anchor displacement (classes present in previous stage)
        disp = np.mean(np.linalg.norm(new_anchors[:n_old] - old_anchors[:n_old], axis=1))

        # Accuracies
        acc_new = routing_acc_subset(new_anchors, pts_k, labels_k, [n_old], 100)
        acc_old = routing_acc_subset(new_anchors, pts_k, labels_k, list(range(n_old)), 100)
        acc_all = routing_acc(new_anchors, pts_k, labels_k, 150)

        d_min, _ = pair_stats(new_anchors)
        print(f"{k:<6}{method:<12}{d_min:<8.4f}{disp:<10.4f}{acc_new:<9.3f}{acc_old:<9.3f}{acc_all:<8.3f}")

        if method == "reflow":
            results_reflow.append((k, d_min, disp, acc_new, acc_old, acc_all))
            anchors = new_anchors.copy()  # next stage starts from the reflowed layout
        else:
            results_rand.append((k, d_min, disp, acc_new, acc_old, acc_all))
            anchors = new_anchors.copy()  # next stage starts from the random-added layout

# ===================================================================
# Summary
# ===================================================================
print(f"\n{'='*60}")
print(f"SUMMARY")
print(f"{'='*60}")
print(f"  Stage 1 ({K0} classes) routing acc: {acc0:.3f}")
print(f"\n  {'Stage':<6}{'new_acc(ref/rand)':<20}{'old_acc(ref/rand)':<20}{'all_acc(ref/rand)'}")
print(f"  {'-'*62}")
for (kr, _, _, nr, or_, ar), (ka, _, _, na, oa, aa) in zip(results_reflow, results_rand):
    print(f"  {kr:<6}{nr:<20.3f}{or_:<20.3f}{ar:.3f}")
    print(f"  {'':<6}{na:<20.3f}{oa:<20.3f}{aa:.3f}   <- random-add")
print(f"\n  Reflow keeps old classes stable while adding new ones.")
print(f"  Random-add risks the new anchor landing on an existing class.")
print(f"\nDone.")
