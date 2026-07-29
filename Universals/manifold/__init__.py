"""
Poincare disk geometry.

Provides both NumPy (for the v1 engine) and PyTorch (for autograd-enabled
experiments) implementations of the hyperbolic metric, geodesic distance,
projection, and Riemannian scaling.
"""

from manifold.poincare import (
    geodesic_distance,
    pairwise_geodesic_distance,
    project_to_disk,
    riemannian_scale,
    inverse_metric,
)

__all__ = [
    "geodesic_distance",
    "pairwise_geodesic_distance",
    "project_to_disk",
    "riemannian_scale",
    "inverse_metric",
]
