"""det(J_F/J_G) = 1 — the determinant (multivariate) L'Hopital constraint.

For maps F, G : R^2 -> R^2 with F(0)=G(0)=0 (the 0/0 at the origin), the
scalar that makes the removable value well-defined is
        lambda = det(J_F) / det(J_G),   J_F = dF/dx, J_G = dG/dx,
and lambda = 1 is the statement that the two ledgers exchange one unit of
area (volume) for one — the determinant version of "the coin is a constant"
(Ch.81), i.e. F and G are volume-equivalent maps at the origin.

Measured ground truths used here:
  - physics   origin_matrix.json:  R_F = [[dmu_dc,dmu_dv],[dlnJ_dc,dlnJ_dv]]
        = [[-0.0471, 0.0355],[-0.0515, 0.0314]], det(R_F) = 0.0004, rank 1.
  - economy   economy_matrix.json: R_G(trust) = [[-0.05,-0.06],[0.13, 0]],
        det = 0.0078 (buy output); the credit side is singular (conserved).
  - ideal     Ch.85 quadratic-manifold: a(1/2) = -ln J_act, F'(1/2)=F(1),
        det-ratio = 1 EXACTLY (E +/- 0.0004) — the only place lambda=1 holds.

Experiment: train a 2D->2D net F to match the measured matrix while a
separate G matches the identity coordinates (det J_G = 1), under the loss
|det(J_F)/det(J_G) - target|. We measure (a) what forcing lambda=1 does to
the data fit (the ideal violates the measured tangent), and (b) the honest
volume-coin lambda_m = det(R_F)/1 = 0.0004 (physics) and 0.0078 (economy).
"""

import json
import os

import torch
import torch.nn as nn
import torch.optim as optim

torch.manual_seed(42)

# measured physics tangent (origin_matrix.json)
R11, R12, R21, R22 = -0.0471, 0.0355, -0.0515, 0.0314
DET_PHYS = R11 * R22 - R12 * R21

# measured economy trust tangent (economy_matrix.json)
E11, E12, E21, E22 = -0.05, -0.06, 0.13, 0.0
DET_ECON = E11 * E22 - E12 * E21


class MapF(nn.Module):
    """2D -> 2D net approximating the F-ledger map near the origin."""
    def __init__(self, h=32):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(2, h), nn.Tanh(),
                                 nn.Linear(h, h), nn.Tanh(), nn.Linear(h, 2))

    def forward(self, x):
        return self.net(x)


class IdentityMap(nn.Module):
    """G(x) = x : the coordinate map, so J_G = Identity and det J_G = 1."""
    def forward(self, x):
        return x


def jacobian(net, x):
    x = x.clone().requires_grad_(True)
    out = net(x)                      # (n,2)
    j = torch.stack([
        torch.autograd.grad(out[:, i].sum(), x, create_graph=True)[0]
        for i in range(2)
    ], dim=-1)                        # (n,2,2)
    return j


def det(j):
    return j[:, 0, 0] * j[:, 1, 1] - j[:, 0, 1] * j[:, 1, 0]


def train(target_lambda, epochs=1500, lr=0.002):
    # training points on a small patch of (c,v) around the origin
    c = torch.linspace(-0.2, 0.2, 9)
    grid = torch.stack([c.repeat(9), c.repeat_interleave(9)], dim=-1)  # (81,2)
    # measured data: F_true(x) = R x + small quadratic
    xt, yt = grid[:, 0:1], grid[:, 1:2]
    fd = (R11 * xt + R12 * yt + 0.05 * xt * yt).squeeze()
    g0_ = (R21 * xt + R22 * yt - 0.05 * xt * yt).squeeze()
    ydata = torch.stack([fd, g0_], dim=-1)   # (81,2)

    netF = MapF()
    netG = IdentityMap()

    opt = optim.Adam(list(netF.parameters()), lr=lr)
    mse = nn.MSELoss()

    for _ in range(epochs):
        opt.zero_grad()
        pred = netF(grid)
        jF = det(jacobian(netF, grid))
        jG = det(jacobian(netG, grid))
        lam = jF / jG                     # det(J_F)/det(J_G)
        loss = mse(pred, ydata) + 0.8 * mse(lam, torch.full_like(lam, target_lambda))
        loss.backward()
        opt.step()

    x0 = torch.zeros(1, 2)
    jF0 = det(jacobian(netF, x0)).item()
    jG0 = det(jacobian(netG, x0)).item()
    return {
        "lambda_target": target_lambda,
        "detJF_detJG_at_origin": jF0 / jG0 if jG0 else float("nan"),
        "detJF_origin": jF0,
        "data_mse_last": float(mse(netF(grid), ydata).item()),
        "measured_det_physics": DET_PHYS,
        "measured_det_economy": DET_ECON,
    }


def main():
    out = {
        "seed": 42,
        "identity": "lambda = det(J_F)/det(J_G); lambda=1 ONLY on the "
                    "quadratic manifold (Ch.85 E+/-0.0004); on measured "
                    "tangents lambda is a measured volume coin.",
        "forcings": [train(1.0), train(DET_PHYS), train(0.0)],
    }
    path = os.path.join("experiments", "data", "volume_coin.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    for r in out["forcings"]:
        print("target=%.4f | learned det(JF)/det(JG)@0 = %.4f | data_mse=%.2e"
              % (r["lambda_target"], r["detJF_detJG_at_origin"], r["data_mse_last"]))
    print("measured det(R) physics = %.4f ; economy(trust) = %.4f"
          % (DET_PHYS, DET_ECON))
    print("WROTE data/volume_coin.json")


if __name__ == "__main__":
    main()