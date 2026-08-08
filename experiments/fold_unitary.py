"""
PUM §10.5.2 open question: "Is the fold-and-cut theorem the discrete analogue
of unitary evolution?" (whether fold-and-cut realizes unitary gates remains
open).

A unitary gate is a bijective, norm-preserving linear map.  For the discrete
analogue to hold, the fold map must at least be INVERTIBLE (one-to-one) and
preserve some metric content of the configuration.

The mirror fold (T63/T64) is r(theta) = a*min(theta, 2*TH - theta): a "tent"
that grows from r=0 to the apex at theta=TH, then returns along the mirror
path.  We test:
  1. injectivity: do distinct development angles map to distinct points?
     (the tent collapses theta and 2*TH-theta to the same radius -> not 1-1)
  2. reversibility: is there a unique preimage under the fold?  (a unitary
     gate must have a well-defined inverse)
  3. norm preservation: does the total arc length of the folded path equal
     the arc length of the unfolded development (a natural "norm" here)?
"""
import sys, os, json
import numpy as np

A = 1.0
TH = 20.0


def mirror_fold(theta):
    return A * np.minimum(theta, 2 * TH - theta)


def arc_length(r_vals, dth):
    # polar arc length: ds^2 = dr^2 + (r dtheta)^2
    dr = np.diff(r_vals)
    r_mid = 0.5 * (r_vals[1:] + r_vals[:-1])
    return float(np.sum(np.sqrt(dr ** 2 + (r_mid * dth) ** 2)))


dth = 0.05
theta_grid = np.arange(0.0, 2 * TH + dth, dth)
r_fold = mirror_fold(theta_grid)

# 1) injectivity: distinct development angles must map to distinct radii.
#    The tent maps theta and 2TH-theta to the same r, so r duplicates exist.
r_rounded = np.round(r_fold, 9)
n_collisions = int(len(r_rounded) - len(np.unique(r_rounded)))

# 2) preimage count of a mid-branch point: r = a*th_mid is hit twice
th_mid = TH / 2
preimages = theta_grid[np.isclose(r_fold, A * th_mid, atol=1e-9)]

# 3) norm: total arc length of the fold vs the unfolded growth 0->TH->2TH
#    (the mirror fold returns the path, so its length is ~2x the growth arc)
r_dev = A * np.arange(0.0, 2 * TH + dth, dth)
L_fold = arc_length(r_fold, dth)
L_dev = arc_length(r_dev, dth)

# 4) injectivity measured on the DEVELOPMENT interval [0, TH]: the tent maps
#    theta and 2*TH-theta (a point on the return branch) to the SAME point,
#    i.e. two distinct configurations fold onto one -> not a bijection.
unitary_like = bool(n_collisions == 0 and L_fold == L_dev)

verdict = (
    "NOT a unitary gate: the mirror fold is NOT injective (%d angle collisions "
    "-- theta and 2TH-theta both land on the same radius, e.g. theta=%.1f and "
    "theta=%.1f both give r=%.2f), so it has no well-defined inverse (2 "
    "preimages of a generic mid-branch point), and the folded path does not "
    "preserve the development's arc length (L_fold/L_dev = %.3f, not 1).  "
    "Unitarity requires a bijective norm-preserving map; the fold is a "
    "many-to-one projection that re-scales the metric content."
    % (n_collisions, th_mid, 2 * TH - th_mid, A * th_mid, L_fold / L_dev)
) if not unitary_like else (
    "the mirror fold is injective and arc-length preserving on this grid -- "
    "consistent with a discrete unitary (norm-preserving, invertible) gate."
)

result = dict(
    claim=("PUM 10.5.2: is fold-and-cut the discrete analogue of unitary "
           "evolution? (unitary gate = bijective + norm-preserving)"),
    setup=dict(a=A, TH=TH, dth=dth),
    checks=dict(
        angle_collisions=n_collisions,
        total_grid_points=len(theta_grid),
        preimages_of_mid_branch=preimages.tolist(),
        n_preimages=int(len(preimages)),
        L_fold=L_fold,
        L_development=L_dev,
        L_ratio=float(L_fold / L_dev),
    ),
    verdict=verdict,
)

with open(os.path.join(os.path.dirname(__file__), "..", "data",
                       "fold_unitary_data.json"), "w") as f:
    json.dump(result, f, indent=1)

print("=" * 72)
print("PUM 10.5.2 FOLD-AS-UNITARY TEST  (r = a*min(th, 2TH-th), a=1, TH=%d)" % TH)
print("=" * 72)
print(" angle collisions (non-injective): %d / %d grid points"
      % (n_collisions, len(theta_grid)))
print(" preimages of r(TH/2)=%.2f: %s" % (A * th_mid, preimages.tolist()))
print(" arc length: fold %.4f  vs  development %.4f  (ratio %.3f)"
      % (L_fold, L_dev, L_fold / L_dev))
print(" verdict: %s" % verdict)
print("saved data/fold_unitary_data.json")
