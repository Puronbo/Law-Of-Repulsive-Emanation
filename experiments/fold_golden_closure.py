"""
fold_golden_closure.py
======================
Derive the "golden-ratio closure" of the spring fold (T58 / AUDIT 2.5 /
WEAVERS 5.2): the fold "closes to r = apex * 0.6138 ~ apex/phi", measured,
reason asserted but not derived.

Construction (spring_fold.py A2): the golden fold is DEFINED by
    s_fold = s_growth / phi^2      i.e.   s_growth / (s_growth - s_fold) = phi
so the fold returns to radius r_ret = a * theta* where
    s(theta*) / s(TH) = 1 / phi^2.
For the Archimedean spiral r = a theta the arc-length is
    s(theta) = (a/2) (theta sqrt(1+theta^2) + asinh theta) ~ a theta^2 / 2
for theta >> 1.  In the exactly-quadratic limit,
    (theta*/TH)^2 = 1/phi^2   =>   r_ret/apex = theta*/TH = 1/phi,
which is EXACTLY the golden ratio.  At finite TH the sub-quadratic
correction (sqrt(1+theta^2) + asinh) shifts the ratio below 1/phi:
    r_ret/apex = 0.6137690...   at TH = 20,
matching the measured spring_fold_data.json value 0.613769016722836.

So the measured 0.6138 is NOT an independent golden-ratio law: it is the
exact consequence of the arc-length construction on the spiral's sub-
quadratic metric, with 1/phi as the theta -> infinity limit.

Verdict artifact: ../data/fold_golden_closure_data.json
"""

import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

PHI = (1 + math.sqrt(5)) / 2
A = 1.0
TH = 20.0


def arc_length(a, th):
    return (a / 2.0) * (th * math.sqrt(1 + th * th) + math.asinh(th))


def inv_arc(a, s_target, lo, hi, tol=1e-14):
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if arc_length(a, mid) < s_target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main():
    # 1) Exact construction at TH = 20
    s_g = arc_length(A, TH)
    s_end = s_g / PHI ** 2
    th_end = inv_arc(A, s_end, 0, TH)
    ratio = th_end / TH
    measured = 12.27538033445672 / 20.0
    print("measured r_ret/apex (spring_fold_data.json): %.10f" % measured)
    print("derived  theta*/TH from s(theta*)/s(TH)=1/phi^2: %.10f" % ratio)
    print("delta: %.2e" % abs(ratio - measured))

    # 2) Large-TH limit -> 1/phi
    lim = []
    for THi in [20, 50, 100, 200, 500, 1000, 5000, 10000]:
        sg = arc_length(A, THi)
        te = inv_arc(A, sg / PHI ** 2, 0, THi)
        lim.append({"TH": THi, "theta_star_over_TH": round(te / THi, 8)})
    print("\nconvergence to 1/phi = %.8f:" % (1 / PHI))
    for row in lim:
        print("  TH=%6d  theta*/TH=%.8f" % (row["TH"], row["theta_star_over_TH"]))

    # 3) quadratic-limit identity: s ~ theta^2/2 -> ratio = 1/phi exactly
    q_ratio = 1.0 / PHI
    print("\nquadratic limit s ~ a theta^2/2 gives theta*/TH = 1/phi exactly: %.10f" % q_ratio)

    out = {
        "claim": "golden-ratio closure r = apex*0.6138 ~ apex/phi (T58 / AUDIT 2.5): reason asserted, not derived",
        "construction": {
            "definition": "fold arc length s_fold = s_growth/phi^2 (s_growth/(s_growth - s_fold) = phi)",
            "spiral": "r = a*theta, a = 1, apex TH = 20",
            "arc_length": "s(th) = (a/2)(th*sqrt(1+th^2) + asinh th)",
            "closure_equation": "s(theta*)/s(TH) = 1/phi^2  ->  r_ret/apex = theta*/TH",
        },
        "measured": measured,
        "derived_at_TH_20": ratio,
        "delta": abs(ratio - measured),
        "asymptotic_limit": {
            "1/phi": 1 / PHI,
            "note": "quadratic limit s ~ a th^2/2 gives theta*/TH = 1/phi exactly; finite-TH sub-quadratic correction gives 0.61377",
        },
        "convergence_table": lim,
        "verdict": (
            "DERIVED: the measured 0.613769 is exactly s(theta*)/s(TH)=1/phi^2 solved "
            "on the Archimedean spiral's sub-quadratic arc-length map (delta %.2e). "
            "The 'golden ratio' enters through the construction (arc-length ratio = phi), "
            "not as an independent law; theta*/TH = 1/phi is the theta->infinity limit "
            "of the spiral metric, and 0.61377 is that limit at the finite apex TH=20. "
            "C2 (next-fold ratio in {phi, phi^2}) remains a separate, epoch-chain claim."
            % abs(ratio - measured)
        ),
    }
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "fold_golden_closure_data.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("\nverdict:", out["verdict"])
    print("wrote data/fold_golden_closure_data.json")


if __name__ == "__main__":
    main()
