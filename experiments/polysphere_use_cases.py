"""
Use-case demos for the PolysphereRouter.

Runs in order: (1) classifier, (2) anomaly detection, (3) generation, (4) continual learning.
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Universals'))
from manifold.polysphere import PolysphereRouter

rng = np.random.RandomState(42)

# ====================================================================
# 1. Multi-class classifier
# ====================================================================
print("=" * 60)
print("USE CASE 1: Multi-class classifier")
print("=" * 60)

router = PolysphereRouter(n_faces=6, seed=42)

n_per_class = 100
X_all, y_all, labels = [], [], []
for j in range(router.n_faces):
    X_j = rng.uniform(-3, 3, size=(n_per_class, 2))
    y_j = router.truths[j](X_j) + 0.1 * rng.randn(n_per_class)
    X_all.extend(X_j)
    y_all.extend(y_j)
    labels.extend([j] * n_per_class)

correct = 0
for X, y, true_j in zip(X_all, y_all, labels):
    pred = router.predict_point(np.array([X]), y)
    if pred == true_j:
        correct += 1

print(f"  Per-point classification accuracy: {correct}/{len(labels)} = {correct/len(labels):.3f}  (chance={1/router.n_faces:.3f})")

# Batch classification
n_batches = 30
batch_correct = 0
for j in range(router.n_faces):
    for _ in range(n_batches):
        X = rng.uniform(-3, 3, size=(40, 2))
        y = router.truths[j](X) + 0.1 * rng.randn(40)
        pred = router.predict_batch(X, y)
        if pred == j:
            batch_correct += 1
print(f"  Batch classification accuracy: {batch_correct}/{router.n_faces*n_batches} = {batch_correct/(router.n_faces*n_batches):.3f}")

# ====================================================================
# 2. Anomaly detection
# ====================================================================
print("")
print("=" * 60)
print("USE CASE 2: Anomaly detection")
print("=" * 60)

# In-distribution batches (from known faces)
in_conf = []
for j in range(router.n_faces):
    for _ in range(20):
        X = rng.uniform(-3, 3, size=(40, 2))
        y = router.truths[j](X) + 0.1 * rng.randn(40)
        _, conf = router.route_batch(X, y)
        in_conf.append(conf)

# Out-of-distribution batches (random noise, not matching any truth)
ood_conf = []
for _ in range(60):
    X = rng.uniform(-3, 3, size=(40, 2))
    y = rng.randn(40) * 2  # random noise, no structure
    _, conf = router.route_batch(X, y)
    ood_conf.append(conf)

in_mean = np.mean(in_conf)
ood_mean = np.mean(ood_conf)
print(f"  In-distribution mean confidence: {in_mean:.3f}")
print(f"  Out-of-distribution mean confidence: {ood_mean:.3f}")
print(f"  Gap: {in_mean - ood_mean:.3f}")

# Threshold at 0.5: what fraction detected?
threshold = 0.5
in_detected = sum(1 for c in in_conf if c >= threshold) / len(in_conf)
ood_detected = sum(1 for c in ood_conf if c < threshold) / len(ood_conf)
print(f"  In-distribution kept (conf>={threshold}): {in_detected:.2%}")
print(f"  Anomalies rejected (conf<{threshold}): {ood_detected:.2%}")

# ====================================================================
# 3. Generative routing
# ====================================================================
print("")
print("=" * 60)
print("USE CASE 3: Generative routing")
print("=" * 60)

# Generate samples from each face and verify they route correctly
for j in range(router.n_faces):
    X_gen, y_gen = router.sample_face(j, n=100, noise=0.15)
    pred = router.predict_batch(X_gen, y_gen)
    correct_pct = np.mean([router.predict_point(x.reshape(1,-1), y) == j
                           for x, y in zip(X_gen, y_gen)])
    print(f"  Face {j} generated samples: batch routed to face {pred}, "
          f"per-point accuracy={correct_pct:.2%}")

# Cross-generation: sample from one face, route through all
print("  Cross-generation test:")
for src in range(router.n_faces):
    X_gen, y_gen = router.sample_face(src, n=100, noise=0.125)
    pred, conf = router.route_batch(X_gen, y_gen)
    match = "OK" if pred == src else "MIS"
    print(f"    Face {src} -> routed to face {pred} {match} (conf={conf:.3f})")

# ====================================================================
# 4. Continual learning
# ====================================================================
print("")
print("=" * 60)
print("USE CASE 4: Continual learning (adding a new face)")
print("=" * 60)

# Start with 4 faces
router4 = PolysphereRouter(n_faces=4, seed=42)
print(f"  Initial faces: {router4.n_faces}")

# Test accuracy on original 4 faces
correct_4 = 0
total_4 = 200
for j in range(4):
    for _ in range(50):
        X = rng.uniform(-3, 3, size=(20, 2))
        y = router4.truths[j](X) + 0.1 * rng.randn(20)
        pred = router4.predict_batch(X, y)
        if pred == j:
            correct_4 += 1
acc_before = correct_4 / total_4
print(f"  Accuracy before adding face: {acc_before:.3f}")

# Add a 5th face
new_truth = lambda X: np.sin(6*X[:,0]) * np.cos(6*X[:,1])
router4.add_face(new_truth)
print(f"  Faces after adding: {router4.n_faces}")

# Test accuracy on all 5 faces (without retraining old ones)
correct_5 = 0
total_5 = 250
for j in range(5):
    for _ in range(50):
        X = rng.uniform(-3, 3, size=(20, 2))
        y = router4.truths[j](X) + 0.1 * rng.randn(20)
        pred = router4.predict_batch(X, y)
        if pred == j:
            correct_5 += 1
acc_after = correct_5 / total_5
print(f"  Accuracy after adding face: {acc_after:.3f}")
print(f"  No memory loss on original 4 faces: previous={acc_before:.3f}, new={acc_after:.3f}")

# Separation on sphere (multiple embeddings per face)
X_by_face = []
y_by_face = []
n_embed = 20
for j in range(5):
    for _ in range(n_embed):
        X_j = rng.uniform(-3, 3, size=(25, 2))
        y_j = router4.truths[j](X_j) + 0.1 * rng.randn(25)
        X_by_face.append(X_j)
        y_by_face.append(y_j)
sil = router4.separation_score(X_by_face, y_by_face)
print(f"  Spherical separation after 5 faces: {sil:.3f}")

print("")
print("Done.")
