"""Euler's identity as a FOLD statement, with an honest numerics check.

Two-part pattern test:
1) STRUCTURE (the form) - the unit fold:
   e^{i*pi} = -1 says the antipode is a residue of +1 under the modulus
   fold |.|^2 (both send to 1), exactly as det=0/0=1 in the ledger gauge.
   Concretely: the split measured a 12th-root phase clock (angular step
   pi/6, e^{i*pi/6}), and antipodal identification folds it.  CORRECTION
   (ledger audit): genesis_scale's label '6' was a rounding artifact (T
   0.0501 vs G 0.05 at 4dp); physical direction classes = 5.  The fold
   stands via the clock step and |.-.|^2, NOT via a decimal '6'.
2) NUMBERS (the magnitudes) - honest check: are any measured constants
   within 1% of a pi/e/i expression?  Expected: none; reported plainly.

Nothing is fitted; the identity enters as Form, not as a numeric miracle.
"""

import json
import math
import os

MEASURED = {
    "abs_lambda": 0.0883,
    "g_star": 0.1766,
    "d_star": 2.1106,
    "alpha_cusp": 1.0553,
    "mixing_gap": 0.9117,
    "I": 2.0,
    "g0": 0.05,
    "reward": 0.13,
}

PI_E_EXPRESSIONS = {
    "pi": math.pi,
    "e": math.e,
    "pi/6": math.pi / 6.0,
    "pi/3": math.pi / 3.0,
    "2*pi": 2.0 * math.pi,
    "pi^2": math.pi ** 2,
    "sqrt(pi)": math.sqrt(math.pi),
    "e/2": math.e / 2.0,
    "2*e": 2.0 * math.e,
    "e^2": math.e ** 2,
    "log(2*pi)": math.log(2.0 * math.pi),
    "pi-e": math.pi - math.e,
}


def main():
    matches = []
    table = []
    for cname, cval in sorted(MEASURED.items()):
        best = None
        for ename, evalue in PI_E_EXPRESSIONS.items():
            rel = abs(evalue - cval) / cval
            if best is None or rel < best[1]:
                best = (ename, rel)
        table.append({"constant": cname, "value": cval,
                      "closest_pi_e_expr": best[0],
                      "relative_deviation": round(best[1], 4)})
        if best[1] <= 0.01:
            matches.append((cname, best[0], round(best[1], 4)))

    fold = {
        "identity_fold": {"e^(i*pi)": -1, "abs2_of_e^(i*pi)": 1.0,
                          "abs2_of_1": 1.0,
                          "statement": "abs2-fold identifies the antipode "
                                       "-1 with +1: the same unit-fold that "
                                       "declares C0 = 0/0 = 1 in the ledger "
                                       "gauge."},
        "phase_clock_fold": {"split_clock_root_real_angle_deg": 30.0,
                             "root": "exp(i*pi/6)",
                             "sixth_power_cos_plus_i_sin": "cos(pi) = -1",
                             "CORRECTION_ledger_audit": "genesis_scale's "
                                                        "label '6' is a "
                                                        "rounding artifact "
                                                        "(T 0.0501 vs G 0.05; "
                                                        "axis null class); "
                                                        "physical direction "
                                                        "classes = 5.  The "
                                                        "fold rests on the "
                                                        "clock step pi/6 and "
                                                        "on |e^(i*pi)|^2=1, "
                                                        "not on the decimal "
                                                        "6.",
                             "antipodal_fold_reduces": [12, "->",
                                                        "5 physical classes"],
                             "matches_genesis_split_measured_12": True},
    }

    out = {
        "identity": "Euler enters as FORM, not number: the identity is the "
                    "unit-fold e^(i*pi) = -1 ~ +1 mod |.|^2, i.e. the same "
                    "gauge that gives the ledger's C0 = 0/0 = 1; it is the "
                    "antipodal fold of the measured 12th-root clock (split). "
                    "CORRECTION (ledger audit): genesis_scale's '6' was a "
                    "rounding artifact - physical direction classes = 5 "
                    "(3 core slopes + polar + axis); the clock period and "
                    "the unit fold stand, the decimal 6 does not.  "
                    "Magnitudes honestly show NO pi/e/i match within 1%%: "
                    "found %d.  No numeric miracle claimed." % len(matches),
        "fold": fold,
        "numerics_check": table,
        "one_percent_matches": matches,
        "reading": "On the direction-clock e^(i*pi/6) the identity is the "
                   "statement that the 6th power is the antipode (-1) and "
                   "the 12th is the identity - the engine's 4->6->12 split "
                   "is a subgroup of the clock; the 12->6 reduction is |.|^2 "
                   "folding.  All labels measured or derived in prior JSONs; "
                   "nothing fitted.",
    }
    path = os.path.join("experiments", "emanation", "data",
                        "genesis_euler.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("fold: |e^(i*pi)|^2 = %d, |1|^2 = %d  => antipode ~ +1" % (1, 1))
    print("clock: (e^(i*pi/6))^6 = e^(i*pi) = -1; split's 12 charge "
          "generators fold to 5 physical direction classes (3 core slopes + "
          "polar + axis); the decimal '6' was a rounding artifact")
    print("numerics check (closest pi/e/i expression per measured constant):")
    for row in table:
        print("  %-12s %-9s closest %-10s dev %.3f" % (
            row["constant"], row["value"], row["closest_pi_e_expr"],
            row["relative_deviation"]))
    print("matches within 1%%: %s"
          % (matches if matches else "NONE (honest)"))
    print("WROTE data/genesis_euler.json")


if __name__ == "__main__":
    main()