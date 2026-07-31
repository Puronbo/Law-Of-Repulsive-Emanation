import numpy as np
from scipy.spatial.distance import cdist

# --- polysphere with per-face truth functions ---

def fibonacci_sphere(n_faces):
    pts = []
    phi = np.pi * (3 - np.sqrt(5))
    for i in range(n_faces):
        y = 1 - (i / (n_faces - 1)) * 2
        r = np.sqrt(1 - y*y)
        theta = phi * i
        pts.append([r * np.cos(theta), y, r * np.sin(theta)])
    return np.array(pts)


def face_truths(n_faces, seed=42):
    rng = np.random.RandomState(seed)
    truths = []
    for i in range(n_faces):
        kx = rng.randint(1, 5)
        ky = rng.randint(1, 5)
        phase = rng.uniform(0, 2*np.pi)
        def make_t(kx, ky, phase):
            return lambda X: np.sin(kx*X[:,0]) * np.cos(ky*X[:,1] + phase)
        truths.append(make_t(kx, ky, phase))
    return truths


def make_polysphere(n_faces=6):
    centers = fibonacci_sphere(n_faces)
    truths = face_truths(n_faces)
    return centers, truths


# --- grid-based routing ---
# Each face's truth defines a pattern over the 2D input space.
# A batch of points is assigned to the face whose truth pattern
# best correlates with the batch's output values.

def route_batch(X_batch, y_batch, centers, truths):
    """Route a batch to the face whose truth pattern best matches y_batch."""
    n_faces = len(truths)
    corrs = np.zeros(n_faces)
    for j in range(n_faces):
        t = truths[j](X_batch)
        if np.std(t) > 1e-8 and np.std(y_batch) > 1e-8:
            corrs[j] = abs(np.corrcoef(t, y_batch)[0, 1])
    best = np.argmax(corrs)
    return best, corrs[best]


# --- generate test: each face produces batches from its own truth + noise ---

n_faces = 6
centers, truths = make_polysphere(n_faces)

rng = np.random.RandomState(42)
n_batches = 30
n_pts_per_batch = 40
n_test = n_faces * n_batches

correct = 0
confusion = np.zeros((n_faces, n_faces), dtype=int)

for true_face in range(n_faces):
    for b in range(n_batches):
        X = rng.uniform(-3, 3, size=(n_pts_per_batch, 2))
        y_clean = truths[true_face](X)
        y_noisy = y_clean + 0.15 * rng.randn(n_pts_per_batch)
        pred, conf = route_batch(X, y_noisy, centers, truths)
        confusion[true_face, pred] += 1
        if pred == true_face:
            correct += 1

accuracy = correct / (n_faces * n_batches)
print(f"Polysphere routing ({n_faces} faces, {n_batches} batches/face):")
print(f"  Batch classification accuracy: {accuracy:.3f}  (chance={1/n_faces:.3f})")
print(f"\n  Confusion matrix (rows=true, cols=pred):")
for j in range(n_faces):
    print(f"    Face {j}: {confusion[j]}")

# --- per-point (not batch) routing ---
# Each point individually goes to the face whose truth is closest.

correct_pt = 0
n_pts = n_faces * 200
for true_face in range(n_faces):
    for _ in range(200):
        x = rng.uniform(-3, 3, size=(1, 2))
        y = (truths[true_face](x) + 0.1 * rng.randn(1))[0]
        errs = np.array([abs(truths[j](x) - y)[0] for j in range(n_faces)])
        pred = np.argmin(errs)
        if pred == true_face:
            correct_pt += 1

acc_pt = correct_pt / n_pts
print(f"\n  Per-point accuracy (nearest truth): {acc_pt:.3f}  (chance={1/n_faces:.3f})")

# --- spherical separation of embedded points ---
# Points are embedded at their face center + noise.
# Measure: are same-face points closer than different-face points?

n_embed = 500
embedded_list = []
labels = []
pts_per_face = n_embed // n_faces
for j in range(n_faces):
    x = rng.uniform(-3, 3, size=(pts_per_face, 2))
    labels.extend([j] * pts_per_face)
    truth_j = truths[j](x)
    errs = np.array([np.abs(truths[k](x) - truth_j) for k in range(n_faces)])
    if errs.ndim == 3:
        errs = errs.mean(axis=2)
    preds = np.argmin(errs, axis=0)
    noise = 0.05 * rng.randn(len(preds), 3)
    embedded_list.append(centers[preds] + noise)
embedded = np.vstack(embedded_list)
labels = np.array(labels)
norms = np.linalg.norm(embedded, axis=1, keepdims=True)
embedded = embedded / norms

from scipy.spatial.distance import pdist, squareform
intra_dists = []
inter_dists = []
for j in range(n_faces):
    mask = labels == j
    pts_j = embedded[mask]
    if len(pts_j) > 1:
        intra_dists.extend(pdist(pts_j))
    for k in range(j+1, n_faces):
        mask_k = labels == k
        if mask_k.sum() > 0:
            inter_dists.extend(cdist(pts_j, embedded[mask_k]).ravel())

print(f"\n  Spherical separation:")
print(f"    Intra-face mean dist: {np.mean(intra_dists):.4f}")
print(f"    Inter-face mean dist: {np.mean(inter_dists):.4f}")
sil = (np.mean(inter_dists) - np.mean(intra_dists)) / max(np.mean(inter_dists), 1e-12)
print(f"    Silhouette-like score: {sil:.3f}")
