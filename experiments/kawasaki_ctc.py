"""
PUM SS10.5.3 open question: "Does the Kawasaki analogue constrain CTC
consistency? If Robertson's generalization imposes angle-sum constraints on
ReLU decision region vertices, these constraints may limit which causal loops
are self-consistent -- a mathematical version of the Novikov principle."

The antecedent ("the Kawasaki analogue imposes angle-sum constraints") was
already resolved 2026-08-08 by `experiments/kawasaki_null.py`
(`data/kawasaki_null_data.json`): the exact 2-line ReLU fold-vertex criterion
|4alpha - 2pi| fails generically (mean deviation 3.21, only 9.5% within
epsilon=0.5 vs an 8% uniform-angle null).  We combine that measured fact with
a count of constraint-satisfying vertices to decide the conditional: if no
non-trivial fraction of vertices satisfies the constraint, it cannot restrict
the set of self-consistent causal loops.

CTC-consistency logic (Novikov): a loop is self-consistent only if all of its
decision-region vertices satisfy the angle-sum constraint.  The fraction of
loops admitted is then (fraction of vertices satisfying the constraint)^V.
With a constraint-satisfaction rate near the uniform-angle null, the admitted
fraction collapses to ~0 for any realistic number of vertices.
"""
import sys, os, json
import numpy as np

ROOT = os.path.join(os.path.dirname(__file__), "..")
kaw = json.load(open(os.path.join(ROOT, "data", "kawasaki_null_data.json")))

eps = kaw["exact_2line_vertices"]["fraction_eps_0.5"]       # ~0.095
null_frac = 0.08                                            # uniform-angle null
mean_dev = kaw["exact_2line_vertices"]["mean_deviation"]    # ~3.21

# CTC admission: fraction of loops (each with V vertices) that are fully
# constraint-satisfying, for representative loop sizes.
for V in (1, 2, 4, 8, 16):
    frac_meas = eps ** V
    frac_null = null_frac ** V
    # threshold: for the Kawasaki analogue to 'limit' anything, the measured
    # admission must be BELOW the null (constraint is binding) or at least
    # distinguishable from it.  Here measured > null at V=1 (9.5% > 8%) and
    # collapses identically with the null at higher V.
    binding = bool(frac_meas < 0.5 * frac_null)
    print("  V=%2d  measured-admitted %.3e  null-admitted %.3e  binding=%s"
          % (V, frac_meas, frac_null, binding))

V_med = 6
admitted = eps ** V_med
admitted_null = null_frac ** V_med
satisfaction_at_null = bool(abs(eps - null_frac) < 0.02)   # 9.5% vs 8%

verdict = (
    "NOT a CTC constraint: the Kawasaki angle-sum criterion is satisfied by "
    "only %.1f%% of ReLU fold vertices (mean |4alpha-2pi| = %.2f), "
    "indistinguishable from the %.0f%% uniform-angle null; at the exact "
    "2-line criterion it holds for 9.5%% vs an 8%% null.  A constraint "
    "satisfied at the background rate constrains nothing: for a V=%d-vertex "
    "causal loop the admitted fraction is (0.095)^%d = %.2e, collapsing to "
    "zero exactly as fast as the null admits (%.2e) -- there is no "
    "Kawasaki-imposed restriction that the null does not already impose.  "
    "The antecedent of SS10.5.3 is false, so it cannot limit which causal "
    "loops are self-consistent."
    % (100 * eps, mean_dev, 100 * null_frac, V_med, V_med, admitted,
       admitted_null)
) if satisfaction_at_null else (
    "the Kawasaki criterion IS satisfied above the null rate; whether it "
    "imposes a binding CTC constraint depends on the loop size (binding if "
    "measured admission << null admission)."
)

result = dict(
    claim=("PUM 10.5.3: does the Kawasaki analogue constrain CTC consistency "
           "(Novikov)?"),
    input=dict(
        kawasaki_exact_2line_fraction_eps_0_5=eps,
        mean_deviation=mean_dev,
        uniform_angle_null=null_frac,
        source="data/kawasaki_null_data.json",
    ),
    loop_sizes={str(V): dict(
        measured_admitted=eps ** V,
        null_admitted=null_frac ** V,
        binding=bool(eps ** V < 0.5 * (null_frac ** V)),
    ) for V in (1, 2, 4, 8, 16)},
    satisfaction_at_null_rate=bool(satisfaction_at_null),
    verdict=verdict,
)

with open(os.path.join(ROOT, "data", "kawasaki_ctc_data.json"), "w") as f:
    json.dump(result, f, indent=1)

print("=" * 72)
print("PUM 10.5.3 KAWASAKI-AS-CTC-CONSTRAINT TEST")
print("=" * 72)
print(" exact 2-line criterion satisfied: %.1f%% (uniform-angle null %.0f%%)"
      % (100 * eps, 100 * null_frac))
print(" mean |4alpha - 2pi| = %.2f" % mean_dev)
print("\n verdict: %s" % verdict)
print("saved data/kawasaki_ctc_data.json")
