"""
Poincare disk geometry, implemented with PyTorch so that gradients are
computed by autograd instead of hand-rolled finite differences.

Provides the geometric primitives for the Puno Calculus:
  - geodesic_distance: exact hyperbolic distance
  - project_to_disk: clamp to unit disk
  - riemannian_scale: conformal factor for gradient correction
  - pairwise_geodesic_distance: batched all-pairs distance matrix
  - mobius_add: Mobius addition (hyperbolic translation)
  - exp_map / log_map: exponential and logarithmic maps at a point
"""

from __future__ import annotations

import torch

EPS = 1e-7


def project_to_disk(x: torch.Tensor, max_norm: float = 0.999) -> torch.Tensor:
    """Clamp points to stay strictly inside the open unit disk."""
    norm = x.norm(dim=-1, keepdim=True).clamp_min(EPS)
    factor = torch.clamp(max_norm / norm, max=1.0)
    return x * factor


def geodesic_distance(u: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
    """
    Batched geodesic distance in the Poincare disk model.

    u: (..., 2), v: (..., 2) or broadcastable to u's shape.
    Returns a tensor of shape u.shape[:-1].
    """
    sq_norm_u = (u ** 2).sum(-1)
    sq_norm_v = (v ** 2).sum(-1)
    sq_dist = ((u - v) ** 2).sum(-1)
    denom = ((1.0 - sq_norm_u) * (1.0 - sq_norm_v)).clamp_min(EPS)
    arg = (1.0 + 2.0 * sq_dist / denom).clamp_min(1.0 + EPS)
    return torch.acosh(arg)


def pairwise_geodesic_distance(u: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
    """
    All-pairs geodesic distance.

    u: (N, 2), v: (M, 2) -> returns (N, M) distance matrix.
    """
    u_exp = u.unsqueeze(1)
    v_exp = v.unsqueeze(0)
    return geodesic_distance(u_exp, v_exp)


def riemannian_scale(u: torch.Tensor) -> torch.Tensor:
    """Conformal factor: lambda(x)^2 = ((1 - ||x||^2)^2) / 4."""
    sq_norm = (u ** 2).sum(-1, keepdim=True)
    return ((1.0 - sq_norm) ** 2) / 4.0


def mobius_add(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    """
    Mobius addition: x (+) y.

    The hyperbolic analogue of vector addition. For the Poincare disk:
        x (+) y = ((1 + 2<x,y> + ||y||^2)x + (1 - ||x||^2)y) /
                  (1 + 2<x,y> + ||x||^2 ||y||^2)

    This is the group operation of the Poincare disk under hyperbolic
    translation.
    """
    xy = (x * y).sum(-1, keepdim=True)
    sq_x = (x ** 2).sum(-1, keepdim=True)
    sq_y = (y ** 2).sum(-1, keepdim=True)
    denom = 1.0 + 2.0 * xy + sq_x * sq_y
    num = (1.0 + 2.0 * xy + sq_y) * x + (1.0 - sq_x) * y
    return project_to_disk(num / denom.clamp_min(EPS))


def exp_map(x: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
    """
    Exponential map at x: maps tangent vector v at point x to the disk.

        exp_x(v) = x (+) (tanh(lambda_x * ||v||) * v / ||v||)

    where lambda_x = 2 / (1 - ||x||^2) is the conformal factor at x.
    """
    sq_norm_v = (v ** 2).sum(-1, keepdim=True).clamp_min(EPS)
    norm_v = sq_norm_v.sqrt()
    sq_norm_x = (x ** 2).sum(-1, keepdim=True)
    lam = 2.0 / (1.0 - sq_norm_x).clamp_min(EPS)
    direction = v / norm_v
    scaled = torch.tanh(lam * norm_v) * direction
    return mobius_add(x, scaled)


def log_map(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    """
    Logarithmic map at x: maps point y back to the tangent space at x.

        log_x(y) = (1 / lambda_x) * arctanh(||(-x) (+) y||) * ((-x) (+) y) / ||(-x) (+) y||

    where lambda_x = 2 / (1 - ||x||^2).
    """
    neg_x = -x
    diff = mobius_add(neg_x, y)
    sq_norm_diff = (diff ** 2).sum(-1, keepdim=True).clamp_min(EPS)
    norm_diff = sq_norm_diff.sqrt()
    sq_norm_x = (x ** 2).sum(-1, keepdim=True)
    lam = 2.0 / (1.0 - sq_norm_x).clamp_min(EPS)
    direction = diff / norm_diff
    return (1.0 / lam.clamp_min(EPS)) * torch.arctanh(norm_diff.clamp_max(1.0 - EPS)) * direction
