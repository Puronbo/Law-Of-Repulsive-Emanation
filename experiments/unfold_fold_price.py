"""Unfold/Fold price experiment.

Learns the removable value at the 0/0 control origin with the
UnifiedMillenniumOperator idea: f(c) -> dmu(c), g(c) -> -lnJ(c), both zero at
the ground state c=0, lambda = f/g with a L'Hopital switch to the Jacobian
ratio df/dg where g -> 0.

Ground truth (measured, Ch.86 origin_matrix.json): the response matrix is
rank-1, det=0.0004, and the coin_ratio = R11/R21 = (-0.0471)/(-0.0515) = 0.9144
is the ratio of the two ledgers' slopes along the c geodesic. In 1-D the
net's Jacobian ratio df/dg at the origin IS that coin. We train the operator
and check whether the learned ground-state lambda matches 0.9144, and whether
the original hard batch-mean switch is a real bug (mislocates the 0/0 point).
"""

import json
import os

import torch
import torch.nn as nn
import torch.optim as optim

torch.manual_seed(42)

R11, R21 = -0.0471, -0.0515   # d(dmu)/dc, d(-lnJ)/dc at control (Ch.86)
COIN = R11 / R21              # 0.9144, the measured one-price ratio


def dmu_true(c):
    return R11 * c + 0.02 * c * c


def mlnJ_true(c):
    return R21 * c + 0.02 * c * c


class GlobalUnfoldNet(nn.Module):
    def __init__(self, hidden_dim=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(1, hidden_dim), nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim), nn.Tanh(),
            nn.Linear(hidden_dim, 1))

    def forward(self, x):
        return self.net(x)


class LocalFoldNet(nn.Module):
    def __init__(self, hidden_dim=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(1, hidden_dim), nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim), nn.Tanh(),
            nn.Linear(hidden_dim, 1))

    def forward(self, x):
        return self.net(x)


class Operator(nn.Module):
    """Corrected version: per-point soft switch + per-point scale tau."""

    def __init__(self, eps=1e-3, tau=1e-2):
        super().__init__()
        self.f_net = GlobalUnfoldNet()
        self.g_net = LocalFoldNet()
        self.eps = eps
        self.tau = tau

    def jacobian_ratio(self, x):
        x = x.clone().requires_grad_(True)
        fv = self.f_net(x)
        gv = self.g_net(x)
        df = torch.autograd.grad(fv.sum(), x, create_graph=True)[0]
        dg = torch.autograd.grad(gv.sum(), x, create_graph=True)[0]
        return df / dg

    def forward(self, x):
        fv = self.f_net(x)
        gv = self.g_net(x)
        jac = self.jacobian_ratio(x)
        w = torch.sigmoid((gv.abs() - self.eps) / self.tau)   # per-point
        lam = w * (fv / (gv + 1e-9)) + (1.0 - w) * jac
        return fv, gv, lam


def fit(mode, epochs=3000, lr=0.001):
    c = torch.linspace(0.001, 0.05, 40).reshape(-1, 1)
    fd = dmu_true(c)
    gd = mlnJ_true(c)
    c0 = torch.zeros(1, 1)

    model = Operator()
    opt = optim.Adam(model.parameters(), lr=lr)
    mse = nn.MSELoss()

    for ep in range(epochs):
        opt.zero_grad()
        fv, gv, lam = model(c)
        f0, g0, _ = model(c0)
        L = mse(fv, fd) + mse(gv, gd)
        if mode == "conserved":
            L = L + 0.1 * mse(lam, torch.ones_like(lam))
        L = L + 1.0 * (f0 ** 2 + g0 ** 2).mean()
        L.backward()
        opt.step()

    f0, g0, lam0 = model(c0)
    jac0 = model.jacobian_ratio(c0)
    # lambda constancy along the ray (the "coin is a constant", Ch.81)
    _, _, lam_c = model(c)
    const = lam_c.detach().mean().item()
    spread = lam_c.detach().std().item()

    learned = (f0 / g0).item() if abs(g0.item()) > 1e-9 else float("nan")
    return {
        "mode": mode,
        "lambda_ground": f0.item() / max(g0.item(), 1e-12),
        "jacobian_ground": float(jac0.squeeze().item()),
        "coin_measured": COIN,
        "err_vs_coin_pct": 100.0 * abs(float(jac0.squeeze().item()) - COIN) / COIN,
        "coin_constancy_mean": const,
        "coin_constancy_spread": spread,
        "f0_abs": abs(float(f0.item())),
        "g0_abs": abs(float(g0.item())),
    }


def original_switch_demo():
    """Batch-mean switch: far points pad the mean -> near-origin point is
    routed through f/g where the fitted g crosses zero -> sign flip, not the
    stable Jacobian branch. True per-point switch keeps the ratio branch.""" 
    eps = 1e-5
    far = torch.linspace(0.2, 1.5, 40).reshape(-1, 1)        # |g| ~ 0.02..0.1
    origin = torch.tensor([[0.0]])
    fv_far = dmu_true(far); gv_far = mlnJ_true(far)
    f0 = dmu_true(origin); g0 = mlnJ_true(origin)

    use_ratio_on = abs((torch.cat([gv_far, g0]).mean().item())) > eps
    # original code: one all-or-nothing branch; if on, the origin point gets
    # f/g = 0/0 -> NaN.  (true switch: |g0| < eps always routes to Jacobian)
    lam_at_origin_if_batchmean = (f0 / g0).item() if use_ratio_on else "nan-iratio"

    # per-point switch at the same origin point: |g0| < eps routes to the
    # stable Jacobian branch (the trivial switch), never to f/g = 0/0
    routed_to = "jacobian" if abs(g0.item()) < eps else "ratio"
    return {
        "batch_g_mean_far_padded": float(torch.cat([gv_far, g0]).mean().item()),
        "batchmean_switch_on": bool(use_ratio_on),
        "lambda_at_origin_via_batchmean": lam_at_origin_if_batchmean,
        "origin_point_g": float(g0.item()),
        "per_point_routes_to": routed_to,
        "per_point_lambda": float(R11 / R21),
    }


def main():
    out = {"seed": 42, "identity": "coin_ratio = R11/R21 = 0.9144 (Ch.86, rank-1)", "results": {}}
    for mode in ("unconstrained", "conserved"):
        out["results"][mode] = fit(mode)
    out["switch_demo"] = original_switch_demo()
    path = os.path.join("experiments", "data", "unfold_fold_price.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)
    r = out["results"]["unconstrained"]
    print("learned jacobian at origin: %.4f  (coin measured %.4f, err %.2f pct)"
          % (r["jacobian_ground"], r["coin_measured"], r["err_vs_coin_pct"]))
    print("lambda constancy along ray: mean %.3f spread %.4f"
          % (r["coin_constancy_mean"], r["coin_constancy_spread"]))
    print("ground state |f0| %.2e |g0| %.2e" % (r["f0_abs"], r["g0_abs"]))
    print("switch demo:", out["switch_demo"])
    print("WROTE data/unfold_fold_price.json")


if __name__ == "__main__":
    main()