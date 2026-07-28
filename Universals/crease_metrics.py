"""
crease_metrics.py

The Puno Calculus crease density diagnostics: hard creases (ReLU),
soft creases (GELU/Swish), and the Kawasaki constraint probe on
synthetic ReLU decision region vertices.

From the Book of Puno, Chapter 4-8 and Chapter 9:
  - Crease density: fraction of near-threshold ReLU units
  - Soft crease intensity: curvature-weighted integral for smooth activations
  - Cost-weighted crease density: only counts straddling units
  - Kawasaki probe: alternating angle-sum test at decision region vertices
"""

from __future__ import annotations

import math
import warnings
from typing import Optional

import numpy as np

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    _HAS_TORCH = True
except ImportError:
    _HAS_TORCH = False


# ---------------------------------------------------------------------------
# Hard crease density (ReLU)
# ---------------------------------------------------------------------------

def raw_crease_density(preacts: np.ndarray, eps: float = 0.05) -> dict:
    """
    Fraction of ReLU pre-activations within eps of zero.

    This is the standard Puno Calculus crease density metric.
    Units near zero are "at the crease" -- undecided between on and off.
    """
    preacts = np.asarray(preacts, dtype=float)
    if preacts.ndim != 2:
        raise ValueError(f"preacts must be 2D [n_samples, n_units], got shape {preacts.shape}")
    near_zero = np.abs(preacts) < eps
    per_unit = near_zero.mean(axis=0)
    return {"per_unit": per_unit, "aggregate": float(per_unit.mean())}


def sign_straddle_density(
    preacts: np.ndarray,
    eps: float = 0.05,
    min_side_frac: float = 0.05,
) -> dict:
    """
    Cost-weighted crease density: only counts units that genuinely straddle
    zero (samples on BOTH sides), not just geometrically close.

    From "Cost weighted crease.py" -- the Sybil crease detector.
    """
    preacts = np.asarray(preacts, dtype=float)
    near_zero = np.abs(preacts) < eps
    near_zero_frac = near_zero.mean(axis=0)
    pos_frac = (preacts > 0).mean(axis=0)
    neg_frac = (preacts < 0).mean(axis=0)
    straddles = (pos_frac >= min_side_frac) & (neg_frac >= min_side_frac)
    per_unit = np.where(straddles, near_zero_frac, 0.0)
    return {
        "per_unit": per_unit,
        "aggregate": float(per_unit.mean()),
        "n_straddling_units": int(straddles.sum()),
        "n_total_units": int(preacts.shape[1]),
        "straddle_fraction": float(straddles.mean()),
    }


# ---------------------------------------------------------------------------
# Soft crease intensity (GELU, Swish, etc.)
# ---------------------------------------------------------------------------

def soft_crease_intensity(
    preacts: np.ndarray,
    activation: str = "gelu",
) -> dict:
    """
    Soft crease intensity for smooth activation functions.

    From the Book of Puno, Section 10.10:
        C_l = E_x[ |sigma''(w_l^T x + b_l)| * ||w_l|| ]

    For ReLU, sigma''(x) = delta(x) (Dirac delta at 0), reducing to
    standard crease density.

    For GELU: sigma(x) = x * Phi(x), sigma''(x) has maximum |sigma''(0)| ~ 0.798
    For Swish: sigma(x) = x * sigmoid(x), sigma''(x) has maximum at x ~ -1.28

    The metric measures how much the activation "bends" the input,
    weighted by data density.
    """
    preacts = np.asarray(preacts, dtype=float)
    n_samples, n_units = preacts.shape

    if activation == "gelu":
        # GELU approximation: sigma(x) = 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))
        # sigma''(x) numerically
        sigma_pp = _gelu_second_derivative(preacts)
    elif activation == "swish":
        sigma_pp = _swish_second_derivative(preacts)
    elif activation == "relu":
        # ReLU: sigma'' is zero everywhere except at x=0 (Dirac delta)
        # Approximate as 1/eps within the eps-band
        eps = 0.05
        sigma_pp = np.where(np.abs(preacts) < eps, 1.0 / eps, 0.0)
    else:
        raise ValueError(f"Unknown activation: {activation}")

    intensity = np.abs(sigma_pp)
    per_unit = intensity.mean(axis=0)
    return {
        "per_unit": per_unit,
        "aggregate": float(per_unit.mean()),
        "max_intensity": float(per_unit.max()),
        "activation": activation,
    }


def _gelu_second_derivative(x: np.ndarray) -> np.ndarray:
    """Numerical second derivative of GELU approximation."""
    h = 1e-4
    gelu_plus = _gelu_approx(x + h)
    gelu_minus = _gelu_approx(x - h)
    gelu_center = _gelu_approx(x)
    return (gelu_plus - 2.0 * gelu_center + gelu_minus) / (h * h)


def _gelu_approx(x: np.ndarray) -> np.ndarray:
    """GELU approximation: x * Phi(x) where Phi is the CDF of N(0,1)."""
    return 0.5 * x * (1.0 + np.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * x**3)))


def _swish_second_derivative(x: np.ndarray) -> np.ndarray:
    """Numerical second derivative of Swish: x * sigmoid(x)."""
    h = 1e-4
    swish_plus = _swish(x + h)
    swish_minus = _swish(x - h)
    swish_center = _swish(x)
    return (swish_plus - 2.0 * swish_center + swish_minus) / (h * h)


def _swish(x: np.ndarray) -> np.ndarray:
    return x / (1.0 + np.exp(-np.clip(x, -500, 500)))


# ---------------------------------------------------------------------------
# Kawasaki constraint probe on synthetic ReLU networks
# ---------------------------------------------------------------------------

def build_synthetic_relu_network(
    layer_widths: list[int] = None,
    seed: int = 42,
) -> "torch.nn.Module":
    """
    Build a small ReLU MLP for testing decision region geometry.

    The network creates hyperplane intersections (ReLU creases) whose
    geometry can be probed for Kawasaki-like angle constraints.
    """
    if not _HAS_TORCH:
        raise ImportError("Requires PyTorch")
    if layer_widths is None:
        layer_widths = [2, 8, 8, 1]

    torch.manual_seed(seed)
    layers = []
    for i in range(len(layer_widths) - 1):
        layers.append(nn.Linear(layer_widths[i], layer_widths[i + 1]))
        if i < len(layer_widths) - 2:
            layers.append(nn.ReLU())
    return nn.Sequential(*layers)


def extract_decision_region_vertices(
    model: "torch.nn.Module",
    n_samples: int = 5000,
    n_dims: int = 2,
    device: str = "cpu",
) -> list[np.ndarray]:
    """
    Sample points near ReLU decision boundaries to approximate
    vertices where multiple hyperplanes intersect.

    Strategy: for each random point, check how many ReLU units are
    simultaneously near zero (multi-crease crossings). Points where
    2+ units are near-zero are candidate vertices.
    """
    if not _HAS_TORCH:
        raise ImportError("Requires PyTorch")

    model.eval()
    vertices = []

    for _ in range(n_samples):
        x = torch.randn(1, n_dims, device=device) * 0.5

        hooks = {}
        activations = {}

        def make_hook(name):
            def hook(module, inp, out):
                activations[name] = out.detach()
            return hook

        for name, module in model.named_modules():
            if isinstance(module, nn.ReLU):
                hooks[name] = module.register_forward_hook(make_hook(name))

        with torch.no_grad():
            model(x)

        for h in hooks.values():
            h.remove()

        # Count how many ReLU units are simultaneously near zero
        n_near_zero = 0
        for name, act in activations.items():
            if act.dim() == 2:
                n_near_zero += (act.abs() < 0.15).sum().item()

        # Multi-crease crossing: 2+ units near zero simultaneously
        if n_near_zero >= 2:
            vertices.append(x.numpy().flatten())

        activations.clear()

    return vertices[:1000]


def kawasaki_angle_test(
    vertices: list[np.ndarray],
    epsilon: float = 0.3,
    max_distance: float = 1.0,
) -> dict:
    """
    Test the Kawasaki alternating angle-sum condition at candidate vertices.

    For each vertex, compute angles to nearby vertices and test the
    alternating sum: theta_1 - theta_2 + theta_3 - theta_4 + ... = 0

    This is the 2D projection of Robertson's (1977) N-dimensional
    generalization of Kawasaki's theorem.
    """
    if len(vertices) < 4:
        return {
            "n_tested": 0, "alternating_sums": [],
            "kawasaki_deviation": 0.0, "kawasaki_fraction": 0.0,
            "mean_alternating_sum": 0.0, "std_deviation": 0.0,
            "epsilon": epsilon,
        }

    verts = [np.asarray(v) for v in vertices]
    sums = []
    deviations = []

    for i, v in enumerate(verts):
        # Find nearby vertices
        distances = [np.linalg.norm(v - verts[j]) for j in range(len(verts)) if j != i]
        nearby_idx = [j for j, d in enumerate(distances) if d < max_distance and d > 1e-10]

        if len(nearby_idx) < 3:
            continue

        angles = []
        for j in nearby_idx:
            diff = verts[j] - v
            angle = math.atan2(diff[1] if len(diff) > 1 else 0, diff[0])
            angles.append(angle)

        if len(angles) < 4:
            continue

        angles.sort()

        gaps = []
        for k in range(len(angles)):
            next_k = (k + 1) % len(angles)
            gap = angles[next_k] - angles[k]
            if gap < 0:
                gap += 2 * math.pi
            gaps.append(gap)

        alt_sum = sum(g if k % 2 == 0 else -g for k, g in enumerate(gaps))
        sums.append(alt_sum)
        deviations.append(abs(alt_sum))  # Kawasaki: alt_sum should be 0

    if not sums:
        return {
            "n_tested": 0, "alternating_sums": [],
            "kawasaki_deviation": 0.0, "kawasaki_fraction": 0.0,
            "mean_alternating_sum": 0.0, "std_deviation": 0.0,
            "epsilon": epsilon,
        }

    return {
        "n_tested": len(sums),
        "alternating_sums": [round(s, 4) for s in sums[:20]],
        "mean_alternating_sum": round(float(np.mean(sums)), 4),
        "kawasaki_deviation": round(float(np.mean(deviations)), 4),
        "std_deviation": round(float(np.std(deviations)), 4),
        "kawasaki_fraction": round(float(np.mean([d < epsilon for d in deviations])), 4),
        "epsilon": epsilon,
    }


# ---------------------------------------------------------------------------
# Crease density trajectory (training diagnostic)
# ---------------------------------------------------------------------------

def crease_density_trajectory(
    model: "torch.nn.Module",
    X: "torch.Tensor",
    layer_names: list[str] = None,
    eps: float = 0.05,
    n_epochs: int = 100,
    lr: float = 0.01,
    task: str = "classification",
) -> dict:
    """
    Track crease density through training.

    From the Book of Puno, Chapter 6:
        Crease density drops during training in two phases:
        1. Fast phase: units settle into on/off states
        2. Slow phase: partition refines gradually

    Returns per-epoch crease density for each layer, plus the rate
    of change (which the Puno Calculus uses as a label-free proxy
    for ongoing learning).
    """
    if not _HAS_TORCH:
        raise ImportError("Requires PyTorch")

    if layer_names is None:
        layer_names = [name for name, m in model.named_modules() if isinstance(m, nn.ReLU)]

    trajectory = {name: [] for name in layer_names}
    activations = {}
    handles = []

    def make_hook(name):
        def hook(module, inp, out):
            activations[name] = out.detach().cpu().numpy()
        return hook

    for name, module in model.named_modules():
        if name in layer_names:
            handles.append(module.register_forward_hook(make_hook(name)))

    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss() if task == "classification" else nn.MSELoss()

    for epoch in range(n_epochs):
        model.train()
        optimizer.zero_grad()
        output = model(X)
        if task == "classification":
            y = (X[:, 0] > 0).long()
            if output.shape[-1] == 1:
                loss = F.binary_cross_entropy_with_logits(output.squeeze(-1), y.float())
            else:
                loss = loss_fn(output, y)
        else:
            y = X[:, 0:1]
            loss = loss_fn(output, y)
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            model(X)

        for name in layer_names:
            if name in activations:
                preacts = activations[name]
                density = raw_crease_density(preacts, eps=eps)["aggregate"]
                trajectory[name].append(density)

    for h in handles:
        h.remove()

    # Compute rate of change
    rates = {}
    for name in layer_names:
        densities = trajectory[name]
        if len(densities) > 1:
            rate = [densities[i] - densities[i - 1] for i in range(1, len(densities))]
            rates[name] = rate

    return {"trajectory": trajectory, "rates": rates, "layer_names": layer_names}


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("  PUNO CALCULUS -- CREASE METRICS")
    print("  Hard / Soft / Kawasaki / Training Trajectory")
    print("=" * 60)

    # --- Hard crease density ---
    print("\n--- Hard Crease Density (ReLU) ---")
    rng = np.random.default_rng(42)
    n_samples, n_units = 500, 32
    preacts = rng.normal(0.0, 0.3, (n_samples, n_units))
    raw = raw_crease_density(preacts, eps=0.05)
    cost = sign_straddle_density(preacts, eps=0.05)
    print(f"Raw crease density:    {raw['aggregate']:.4f}")
    print(f"Cost-weighted density: {cost['aggregate']:.4f}")
    print(f"Straddle fraction:     {cost['straddle_fraction']:.4f}")

    # --- Soft crease intensity ---
    print("\n--- Soft Crease Intensity ---")
    for act in ["gelu", "swish", "relu"]:
        result = soft_crease_intensity(preacts, activation=act)
        print(f"  {act:6s}: aggregate={result['aggregate']:.4f}, max={result['max_intensity']:.4f}")

    # --- Kawasaki test on synthetic network ---
    if _HAS_TORCH:
        print("\n--- Kawasaki Constraint Test (Synthetic ReLU Network) ---")
        model = build_synthetic_relu_network([2, 16, 16, 8, 1], seed=42)
        print(f"Model: {sum(p.numel() for p in model.parameters())} parameters")

        vertices = extract_decision_region_vertices(model, n_samples=3000)
        print(f"Candidate vertices found: {len(vertices)}")

        if vertices:
            kawasaki = kawasaki_angle_test(vertices, epsilon=0.5)
            print(f"  Vertices tested: {kawasaki['n_tested']}")
            print(f"  Mean alternating sum: {kawasaki.get('mean_alternating_sum', 0):.4f}")
            print(f"  Kawasaki deviation: {kawasaki.get('kawasaki_deviation', 0):.4f}")
            print(f"  Kawasaki satisfied (eps={kawasaki['epsilon']}): {kawasaki['kawasaki_fraction']:.4f}")
        else:
            print("  No vertices found (try more samples or wider network)")

        # --- Training trajectory ---
        print("\n--- Crease Density Training Trajectory ---")
        X = torch.randn(200, 2)
        model_small = build_synthetic_relu_network([2, 16, 8, 1], seed=42)
        traj = crease_density_trajectory(model_small, X, n_epochs=50, lr=0.02)
        for name in traj["layer_names"]:
            densities = traj["trajectory"][name]
            if densities:
                print(f"  {name}: {densities[0]:.4f} -> {densities[-1]:.4f} (delta={densities[-1]-densities[0]:.4f})")

    print("\n[DONE]")
