"""
Polysphere routing manifold.

Each face of a spherical polyhedron carries its own truth function.
Points on the sphere route outward through the face whose truth best matches.
"""

from __future__ import annotations

import numpy as np
from scipy.spatial.distance import cdist


# --- sphere utilities ---

def fibonacci_sphere(n_pts: int) -> np.ndarray:
    """Nearly-even distribution of n_pts points on S^2 via Fibonacci spiral."""
    pts = []
    phi = np.pi * (3 - np.sqrt(5))
    for i in range(n_pts):
        y = 1 - (i / (n_pts - 1)) * 2 if n_pts > 1 else 0.0
        r = np.sqrt(max(1 - y*y, 0.0))
        theta = phi * i
        pts.append([r * np.cos(theta), y, r * np.sin(theta)])
    return np.array(pts)


def cosine_sim(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a_norm = np.linalg.norm(a, axis=-1, keepdims=True)
    b_norm = np.linalg.norm(b, axis=-1, keepdims=True)
    return (a @ b.T) / (a_norm * b_norm.T).clip(min=1e-12)


# --- truth function helpers ---

def sine_cosine_truth(kx: int, ky: int, phase: float = 0.0):
    """Periodic truth over 2D input space."""
    def f(X: np.ndarray) -> np.ndarray:
        return np.sin(kx * X[:, 0]) * np.cos(ky * X[:, 1] + phase)
    return f


def random_truths(n: int, seed: int = 42) -> list:
    rng = np.random.RandomState(seed)
    truths = []
    for i in range(n):
        kx = int(rng.randint(1, 5))
        ky = int(rng.randint(1, 5))
        phase = rng.uniform(0, 2 * np.pi)
        truths.append(sine_cosine_truth(kx, ky, phase))
    return truths


# --- core router ---

class PolysphereRouter:
    """Router: embedded points on S^2 route outward through per-face truths.

    Each face has:
      - a center on the sphere surface
      - a truth function f: R^d -> R defining its identity

    Routing: a batch of 2D inputs (X, y) goes to the face whose truth
    pattern best correlates with y over X.
    """

    def __init__(self, n_faces: int = 6, centers: np.ndarray | None = None,
                 truths: list | None = None, seed: int = 42):
        if centers is not None:
            self.centers = np.asarray(centers, dtype=float)
            self.n_faces = len(self.centers)
        else:
            self.n_faces = n_faces
            self.centers = fibonacci_sphere(n_faces)
        if truths is not None:
            self.truths = truths
        else:
            self.truths = random_truths(self.n_faces, seed)
        assert len(self.truths) == self.n_faces

    # --- routing ---

    def route_batch(self, X: np.ndarray, y: np.ndarray) -> tuple[int, float]:
        """Route a batch (X, y) to the best face by truth-pattern correlation.

        Returns (face_index, confidence).
        """
        best_j, best_c = -1, -1.0
        for j in range(self.n_faces):
            t = self.truths[j](X)
            if np.std(t) > 1e-10 and np.std(y) > 1e-10:
                c = abs(np.corrcoef(t, y)[0, 1])
                if c > best_c:
                    best_c = c
                    best_j = j
        return best_j, best_c

    def route_point(self, x: np.ndarray, y: float) -> tuple[int, float]:
        """Route a single (x, y) point to the nearest-matching face.

        Returns (face_index, confidence).
        """
        x = np.asarray(x).reshape(1, -1)
        y = np.asarray(y).reshape(-1)
        best_j, best_err = -1, np.inf
        for j in range(self.n_faces):
            t = self.truths[j](x)
            err = abs(t - y).item()
            if err < best_err:
                best_err = err
                best_j = j
        conf = 1.0 / (1.0 + best_err)
        return best_j, conf

    def confidence(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Per-face correlation confidence for a batch. Shape (n_faces,)."""
        corrs = np.zeros(self.n_faces)
        for j in range(self.n_faces):
            t = self.truths[j](X)
            if np.std(t) > 1e-10 and np.std(y) > 1e-10:
                corrs[j] = abs(np.corrcoef(t, y)[0, 1])
        return corrs

    # --- classification ---

    def predict_batch(self, X: np.ndarray, y: np.ndarray) -> int:
        j, _ = self.route_batch(X, y)
        return j

    def predict_point(self, x: np.ndarray, y: float) -> int:
        j, _ = self.route_point(x, y)
        return j

    # --- anomaly ---

    def is_anomaly(self, X: np.ndarray, y: np.ndarray,
                   threshold: float = 0.5) -> bool:
        _, conf = self.route_batch(X, y)
        return conf < threshold

    # --- embedding ---

    def embed(self, X: np.ndarray, y: np.ndarray,
              noise: float = 0.05) -> np.ndarray:
        """Embed a batch onto the sphere surface at its best face + noise."""
        corrs = self.confidence(X, y)
        best = np.argmax(corrs)
        pt = self.centers[best] + noise * np.random.randn(3)
        return pt / np.linalg.norm(pt)

    def embed_many(self, X_list: list[np.ndarray],
                   y_list: list[np.ndarray]) -> np.ndarray:
        """Embed multiple batches. Returns (n_batches, 3)."""
        pts = []
        for X, y in zip(X_list, y_list):
            pts.append(self.embed(X, y))
        return np.array(pts)

    # --- generation ---

    def sample_face(self, face: int, n: int = 100,
                    noise: float = 0.15) -> tuple[np.ndarray, np.ndarray]:
        """Sample (X, y) pairs approximately matching a face's truth."""
        rng = np.random.RandomState()
        X = rng.uniform(-3, 3, size=(n, 2))
        y = self.truths[face](X) + noise * rng.randn(n)
        return X, y

    def classify_face(self, x: np.ndarray) -> int:
        """Classify a 2D point to the face whose truth it most resembles."""
        vals = np.array([f(x.reshape(1, -1))[0] for f in self.truths])
        return int(np.argmax(vals))

    # --- continual learning ---

    def add_face(self, truth, center: np.ndarray | None = None):
        """Add a new face with given truth function."""
        self.truths.append(truth)
        if center is not None:
            self.centers = np.vstack([self.centers, center])
        else:
            # place at a new Fibonacci point (may not be perfectly even anymore)
            n = self.n_faces
            self.centers = fibonacci_sphere(n + 1)
        self.n_faces += 1

    # --- diagnostics ---

    def separation_score(self, X_by_face: list[np.ndarray],
                         y_by_face: list[np.ndarray]) -> float:
        """Silhouette-like score of spherical class separation.

        X_by_face: list of batches (consecutive same-face batches).
        Face labels are inferred from n_faces and per-face count.
        """
        pts = self.embed_many(X_by_face, y_by_face)
        n = len(X_by_face)
        n_per_face = n // self.n_faces
        labels = np.repeat(np.arange(self.n_faces), n_per_face)
        from scipy.spatial.distance import pdist
        intra, inter = [], []
        for j in range(len(X_by_face)):
            mask = labels == j
            pj = pts[mask]
            if len(pj) > 1:
                intra.extend(pdist(pj))
            for k in range(j + 1, len(X_by_face)):
                pk = pts[labels == k]
                if len(pk) > 0:
                    inter.extend(np.linalg.norm(pj[:, None] - pk[None], axis=-1).ravel())
        if not inter or not intra:
            return 0.0
        return (np.mean(inter) - np.mean(intra)) / max(np.mean(inter), 1e-12)
