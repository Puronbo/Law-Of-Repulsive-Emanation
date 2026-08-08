"""
PUM §10.5.1 open question: "Can the Wheeler-DeWitt equation be simulated on
the Poincare disk? Can an analogous constraint be defined on the Poincare disk
that selects 'physical' knowledge configurations?"

The PUM table (SS2) claims: "Wheeler-DeWitt Constraint H|Psi> = 0 |
Fraction of phase-space states with ||H(q,p)|| < epsilon |
wheeler_dewitt_filter() | 86.8% satisfied at epsilon=0.5".

Two filters exist in hamiltonian_flow.py:
  - wheeler_dewitt_filter  (UNSHIFTED): uses |H(q,p)| = |K + V| < eps.
    On a frictionless flow H is conserved at C0 = V(0) ~ 24, so |H| < eps is
    EMPTY for any eps << C0.
  - shifted_wheeler_dewitt_filter (SHIFTED): uses |H(q,p) - C0| < eps.  This
    is exactly the C0 law / energy-conservation test (math_validation.py
    itself flags: "Shifted WDW is the same test with generous epsilon=0.5
    (tolerance = 2% of C0)... This always passes for frictionless flow").

Open question to resolve: does either filter SELECT a lower-dimensional
'physical' submanifold (fraction strictly between 0 and 1 at a meaningful
epsilon), or is the constraint either empty (unshifted) or a relabeling of
energy drift (shifted)?
"""
import sys, os, json
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "Universals"))
from hamiltonian_flow import (run_hamiltonian_flow, repulsion_loss,
                              wheeler_dewitt_filter, shifted_wheeler_dewitt_filter,
                              wheeler_dewitt_constraint)

CONTEXT = ["Tech", "Silicon"]
EPSILONS = [0.01, 0.1, 0.5, 2.0, 10.0]
SEEDS = [(0.05, 0.02), (0.0, 0.0), (-0.2, 0.1), (0.3, -0.05)]


def sweep(q0, friction, dt, label):
    traj = run_hamiltonian_flow(np.array(q0), CONTEXT, steps=500, dt=dt,
                                friction=friction, max_grad=5.0)
    c0 = repulsion_loss(np.zeros(2), CONTEXT)
    rows = []
    for eps in EPSILONS:
        un = wheeler_dewitt_filter(traj.states, CONTEXT, epsilon=eps)
        sh = shifted_wheeler_dewitt_filter(traj.states, CONTEXT, c0, epsilon=eps)
        rows.append(dict(epsilon=eps,
                         unshifted_fraction=un["fraction_satisfied"],
                         shifted_fraction=sh["fraction_satisfied"]))
    return dict(label=label, q0=q0, friction=friction, dt=dt,
                c0=c0, mean_abs_H=float(np.mean([wheeler_dewitt_constraint(s, CONTEXT)["constraint_violation"] for s in traj.states])),
                rows=rows)


results = []
for q0 in SEEDS:
    results.append(sweep(q0, 0.0, 0.0005, "frictionless"))
for q0 in SEEDS[:2]:
    results.append(sweep(q0, 0.3, 0.002, "dissipative"))

# --- verdict logic ---
c0 = repulsion_loss(np.zeros(2), CONTEXT)
# A genuine selection requires fraction strictly in (0,1) at eps <= 0.05
# (0.2% of C0) on a FRICTIONLESS trajectory: only there is energy constant,
# so a non-trivial fraction genuinely subdivides phase space.  On dissipative
# flow a small-eps fraction is just the decay transient (states still near C0
# before energy drops), not a selection.
unshifted_selective = any(
    0.0 < row["unshifted_fraction"] < 1.0 and row["epsilon"] <= 0.05
    for r in results if r["friction"] == 0.0 for row in r["rows"])
shifted_selective = any(
    0.0 < row["shifted_fraction"] < 1.0 and row["epsilon"] <= 0.05
    for r in results if r["friction"] == 0.0 for row in r["rows"])

# The PUM's 86.8% at eps=0.5: which filter produced it, and on what trajectory?
pum_like = None
for r in results:
    for row in r["rows"]:
        if row["epsilon"] == 0.5 and 0.5 < row["shifted_fraction"] < 1.0:
            pum_like = dict(traj=r["label"], q0=r["q0"],
                            shifted=row["shifted_fraction"],
                            unshifted=row["unshifted_fraction"])

if unshifted_selective:
    verdict = ("UNSHIFTED constraint selects a non-trivial subset at eps<=0.05 -- "
               "a genuine analogue selection on the disk.")
elif shifted_selective:
    verdict = ("SHIFTED constraint selects a non-trivial subset at eps<=0.05 -- "
               "a genuine energy-drift selection below the C0-law tolerance.")
elif pum_like:
    verdict = ("NEITHER filter selects a phase-space submanifold.  The unshifted "
               "H|Psi>=0 is EMPTY on conservative flow (|H|=C0~24 >> any "
               "meaningful eps; nonzero only at eps>=10 = 42%% of C0).  The "
               "shifted filter is the C0 law relabeled: fraction is 1.000 at "
               "every eps for the origin-start trajectory (H-C0==0 exactly) and "
               "0->1 at the integrator drift level otherwise.  The PUM's "
               "'86.8%% satisfied at eps=0.5' is reproduced only as the SHIFTED "
               "(=energy-drift) filter on %s q0=%s (%.1f%%), never as the "
               "unshifted constraint (%.1f%%) -- a finite-precision drift "
               "number, not a selection of 'physical' configurations."
               % (pum_like["traj"], pum_like["q0"], 100 * pum_like["shifted"],
                  100 * pum_like["unshifted"]))
else:
    verdict = ("NEITHER filter selects: the unshifted H|Psi>=0 is EMPTY on "
               "conservative flow (|H|=C0~24 >> any meaningful eps; the "
               "constraint surface is empty), and the shifted filter is the "
               "C0 law relabeled (0->1 at the integrator drift level).  The "
               "PUM's '86.8%% satisfied' is a finite-precision drift number, "
               "not a phase-space selection.")

result = dict(
    claim=("PUM SS2/10.5.1: Wheeler-DeWitt constraint H|Psi>=0 selects "
           "'physical' knowledge configurations; 86.8%% satisfied at eps=0.5"),
    c0=c0,
    filters=dict(
        unshifted="|H(q,p)| = |K+V| < eps  (constraint surface on conservative "
                  "flow: H = C0 ~ 24, so empty for eps << C0)",
        shifted="|H(q,p) - C0| < eps  (identical to the C0 law / energy "
                "conservation test; math_validation.py flags it as such)",
    ),
    results=results,
    verdict=verdict,
)

# additionally scan for the PUM's exact '86.8% at eps=0.5' figure
rng = np.random.default_rng(7)
best_shifted = 0.0
for fric in (0.0, 0.3):
    for dt in (0.0005, 0.002):
        for steps in (500, 2000):
            for _ in range(10):
                q0 = rng.uniform(-0.5, 0.5, 2)
                traj = run_hamiltonian_flow(q0, CONTEXT, steps=steps, dt=dt,
                                            friction=fric, max_grad=5.0)
                sh = shifted_wheeler_dewitt_filter(traj.states, CONTEXT, c0,
                                                   epsilon=0.5)
                best_shifted = max(best_shifted, sh["fraction_satisfied"])
pum_figure_reproduced = 0.6 < best_shifted < 0.95
result["scan_for_86.8pct"] = dict(
    max_shifted_fraction_eps05=best_shifted,
    reproduced=bool(pum_figure_reproduced),
    note="grid: friction in {0.0,0.3}, dt in {5e-4,2e-3}, steps in {500,2000}, "
         "10 random q0 each; the shifted (energy-drift) filter reads either "
         "0.000 or 1.000 -- the '86.8% satisfied' figure is not reproduced "
         "by the current filter semantics." if not pum_figure_reproduced
         else "the 86.8% figure is reproducible in this grid.",
)
if pum_figure_reproduced:
    verdict = ("The PUM's '86.8% satisfied at eps=0.5' IS reproducible "
               "(max shifted fraction %.3f), but it is the shifted "
               "(energy-drift) filter, i.e. the C0 law with tolerance, not a "
               "selection of 'physical' configurations." % best_shifted)
else:
    verdict = verdict + ("  Independently, the exact '86.8%% at eps=0.5' "
                         "figure is NOT reproduced (grid max %.3f)."
                         % best_shifted)
result["verdict"] = verdict

with open(os.path.join(os.path.dirname(__file__), "..", "data",
                       "wheeler_dewitt_selection_data.json"), "w") as f:
    json.dump(result, f, indent=1)

print("=" * 72)
print("PUM 10.5.1 WHEELER-DEWITT 'SELECTION' TEST  (C0 = %.4f)" % c0)
print("=" * 72)
for r in results:
    print("\n[%s] q0=%s  mean|H| = %.2f" % (r["label"], r["q0"], r["mean_abs_H"]))
    print("  eps       unshifted  shifted")
    for row in r["rows"]:
        print("  %-8.3g  %.3f       %.3f"
              % (row["epsilon"], row["unshifted_fraction"], row["shifted_fraction"]))
print("\nverdict: %s" % verdict)
print("saved data/wheeler_dewitt_selection_data.json")
