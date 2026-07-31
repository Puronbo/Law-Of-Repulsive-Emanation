"""
C0 Hamiltonian flow on the Poincare disk (numpy).

The C0 energy potential V = sum_{i<j} 1/|x_i - x_j| drives a repulsive
interaction between concept points. Hamiltonian dynamics on the disk
with leapfrog integration separate concept positions while friction
lets the system settle.

The flow operates at the CONCEPT level: class centroids / face anchors
are the points that evolve, keeping them well-separated for routing.
"""

from __future__ import annotations

import numpy as np


def to_disk(qs: np.ndarray, max_r: float = 0.85) -> np.ndarray:
    """Clamp points to stay inside the disk of radius max_r."""
    r = np.linalg.norm(qs, axis=-1, keepdims=True)
    scale = np.minimum(max_r / np.maximum(r, 1e-12), 1.0)
    return qs * scale


def c0_gradient(qs: np.ndarray, labels: np.ndarray | None = None,
                attract: float = 1.0) -> np.ndarray:
    """
    Gradient of C0 repulsion (+ optional same-class attraction).

    Without labels: pure repulsion, grad_i = sum_j (x_i - x_j)/|r|^3.
    With labels: attraction between same-class points balanced so the
    net same-class pull matches the net different-class push.
    """
    n = len(qs)
    grad = np.zeros_like(qs)
    if labels is None:
        for i in range(n):
            diff = qs[i] - qs
            dist = np.linalg.norm(diff, axis=-1)
            dist[i] = np.inf
            with np.errstate(divide='ignore', invalid='ignore'):
                grad[i] = np.sum(diff / np.maximum(dist**3, 1e-12)[:, None], axis=0)
        return grad
    same = labels[:, None] == labels[None]
    np.fill_diagonal(same, False)
    n_same_global = max(same.sum(axis=1).max(), 1)
    n_diff_global = max((~same).sum(axis=1).max(), 1)
    attract_scaled = attract * n_diff_global / n_same_global
    for i in range(n):
        diff = qs[i] - qs
        dist = np.linalg.norm(diff, axis=-1)
        dist[i] = np.inf
        with np.errstate(divide='ignore', invalid='ignore'):
            rep = np.sum(diff / np.maximum(dist**3, 1e-12)[:, None], axis=0)
            attr = np.sum(same[i, :, None] * diff / np.maximum(dist**2, 1e-8)[:, None], axis=0)
        grad[i] = rep - attract_scaled * attr
    return grad


def c0_flow(qs: np.ndarray, labels: np.ndarray | None = None,
            attract: float = 1.0, n_steps: int = 500,
            dt: float = 0.02, friction: float = 0.03,
            max_r: float = 0.85) -> np.ndarray:
    """
    Leapfrog (velocity Verlet) integration of the C0 Hamiltonian flow
    on the Poincare disk with friction. Returns the evolved points.

    The C0 repulsion is a Newtonian force F = +grad (pushing points
    apart), so the momentum update is p += dt*F.
    """
    qs = qs.copy()
    ps = np.zeros_like(qs)
    for _ in range(n_steps):
        g = c0_gradient(qs, labels, attract)
        ps_half = ps + 0.5 * dt * g
        ps_half *= (1.0 - friction * dt)
        qs_new = qs + dt * ps_half
        qs_new = to_disk(qs_new, max_r)
        g_new = c0_gradient(qs_new, labels, attract)
        ps = ps_half + 0.5 * dt * g_new
        ps *= (1.0 - friction * dt)
        qs = qs_new
    return qs


def pair_stats(points: np.ndarray) -> tuple[float, float]:
    """Min and mean off-diagonal pairwise distance."""
    n = len(points)
    d = np.linalg.norm(points[:, None] - points[None], axis=-1)
    d = d + np.eye(n) * 10
    return float(np.min(d)), float(np.mean(d[d < 10]))


def separation(points: np.ndarray, labels: np.ndarray) -> tuple[float, float]:
    """Mean intra-class and inter-class Euclidean distance."""
    from scipy.spatial.distance import pdist, cdist
    classes = np.unique(labels)
    intra, inter = [], []
    for j in classes:
        m = labels == j
        if m.sum() > 1:
            intra.extend(pdist(points[m]))
    for a in range(len(classes)):
        for b in range(a + 1, len(classes)):
            ma = labels == classes[a]
            mb = labels == classes[b]
            if ma.sum() and mb.sum():
                inter.extend(cdist(points[ma], points[mb]).ravel())
    return float(np.mean(intra)), float(np.mean(inter))
