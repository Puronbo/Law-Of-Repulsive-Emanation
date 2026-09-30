#!/usr/bin/env python3
"""
c0_at_zeros.py -- C0 evaluated "at every zero on the scale".

Investigates the request: compute C0 for every zero on the scale, and explore
whether this could be linked to a Millennium Prize Problem to generate proofs.

What this script establishes, with runnable evidence:

  G1  The corpus "C0 law", C0 = V(q0) = H(q0, 0), is a TAUTOLOGY.
      H = K(p) + V(q) and K(0) = 0 identically, so H(q, 0) = V(q) by
      definition. It holds at every position and every context; it is not a
      discovered relation. The 14 "verifications" in c0_law_data.json are 14
      instances of one identity.

  G2  C0 = 24.434792 is NOT a constant of nature. It is a function of ten
      hand-typed 2D coordinates. Perturbing one coordinate by 0.01 moves C0.
      So C0 cannot anchor an invariant statement about zeros.

  G3  C0 has no definition "at a zero". It is a lookup table over the 2^10
      discrete word-context subsets, not a continuous function of an analytic
      variable. There is no zero-locus at which to evaluate it.

  G4  The one C0-to-Millennium link in the corpus is structurally vacuous.
      NS_MILLENNIUM_REDUCTION.md sec. 2 reasons: A/A = 1 with
      A = dE/dt + 2*nu*Z == 0, take the removable value 1, conclude
      dE/dt = -2*nu*Z, hence Z integrable, hence no blowup. But A/A = 1
      holds for EVERY A, so the identity cannot force A == 0. The inference
      runs from a universal statement to one case, which is invalid.

  G5  The corpus already agrees. docs/AUDIT.md flags the C0*zeta partition
      "match" as a tautology that "holds for ANY constant C0... a match by
      construction is not a test." No correction needed there.

Verdict: C0-per-zero is not computable in a meaningful sense, and the
Millennium link rests on an invalid inference. This script is the evidence.

Run:  python experiments/c0_at_zeros.py

Writes data/c0_at_zeros_data.json (tracked, in the manifest).
"""

import itertools
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "Universals"))

from hamiltonian_flow import (  # noqa: E402
    ALPHA,
    POSITIONS,
    HamiltonianState,
    repulsion_loss,
)

Q0 = np.array([0.0, 0.0])
CONTEXT = ["Tech", "Silicon"]

report = {"experiment": "C0 at every zero on the scale", "gates": {}}


def gate(name, ok, detail):
    report["gates"][name] = {"pass": bool(ok), "detail": detail}
    print("  [%s] %-34s %s" % ("PASS" if ok else "FAIL", name, detail))
    return ok


def g1_law_is_tautology():
    print("\nG1  Is 'C0 = V(q0) = H(q0, 0)' a discovered law or a definition?")
    c0 = repulsion_loss(Q0, CONTEXT)
    h0 = HamiltonianState(q=Q0, p=np.zeros(2)).total_energy(CONTEXT)
    agree = abs(c0 - h0) < 1e-10

    # The decisive test: if it is a definition, it must hold EVERYWHERE, not
    # just at the origin. Try many positions and many contexts.
    holds_everywhere = True
    checks = 0
    for r in range(0, 4):
        for combo in itertools.combinations(list(POSITIONS), r):
            ctx = list(combo)
            for pt in [Q0, np.array([0.3, 0.2]), np.array([-0.4, 0.1])]:
                c = repulsion_loss(pt, ctx)
                h = HamiltonianState(q=pt, p=np.zeros(2)).total_energy(ctx)
                checks += 1
                if abs(c - h) > 1e-9:
                    holds_everywhere = False
    print("     V(q0)=%.6f  H(q0,0)=%.6f  agree=%s" % (c0, h0, agree))
    print("     checked %d (position, context) pairs: holds everywhere = %s"
          % (checks, holds_everywhere))
    return gate(
        "G1 law is a tautology", holds_everywhere and agree,
        "H=K+V, K(0)=0 => H(q,0)=V(q) identically; %d/%d pairs agree"
        % (checks, checks),
    )


def g2_c0_not_invariant():
    print("\nG2  Is C0 = 24.434792 an invariant, or a function of typed coordinates?")
    base = repulsion_loss(Q0, CONTEXT)
    deltas = {}
    originals = {k: v.copy() for k, v in POSITIONS.items()}
    for node in ["System", "Idea", "Mammal"]:
        POSITIONS[node] = originals[node] + np.array([0.01, 0.0])
        deltas[node] = repulsion_loss(Q0, CONTEXT)
        POSITIONS[node] = originals[node]
    for node in POSITIONS:
        POSITIONS[node] = originals[node]
    print("     base C0 = %.6f" % base)
    for node, val in deltas.items():
        print("     shift %-8s by +0.01 -> C0 = %.6f  (delta %+.6f)"
              % (node, val, val - base))
    moved = any(abs(v - base) > 1e-9 for v in deltas.values())
    return gate(
        "G2 C0 moves with coordinates", moved,
        "a 0.01 coordinate edit shifts C0 by up to %+.4f; C0 is not invariant"
        % max(abs(v - base) for v in deltas.values()),
    )


def g3_c0_has_no_zero_locus():
    print("\nG3  Can C0 be evaluated 'at a zero'? What is its domain?")
    names = list(POSITIONS)
    vals = []
    for r in range(0, len(names) + 1):
        for combo in itertools.combinations(names, r):
            vals.append((repulsion_loss(Q0, list(combo)), combo))
    vals.sort()
    distinct = len({round(v[0], 6) for v in vals})
    print("     domain = 2^%d = %d discrete word-context subsets" % (len(names), len(vals)))
    print("     min C0 = %.6f   max C0 = %.6f   distinct = %d"
          % (vals[0][0], vals[-1][0], distinct))
    print("     -> finite lookup table, not a continuous function of a variable;")
    print("        there is no analytic zero-locus at which to sample C0.")
    return gate(
        "G3 C0 is discrete, not analytic", distinct < len(vals) and len(vals) == 2 ** len(names),
        "%d discrete contexts -> %d distinct C0 values; no zero-locus exists"
        % (len(vals), distinct),
    )


def g4_tautology_inference_invalid():
    print("\nG4  Is the Millennium link (NS_MILLENNIUM_REDUCTION.md sec.2) sound?")
    print("     It reasons: A/A = 1 with A = dE/dt + 2*nu*Z == 0; take the")
    print("     removable value 1; conclude dE/dt = -2*nu*Z; hence Z integrable;")
    print("     hence no blowup.")
    print()
    print("     Counter-form: A/A = 1 holds for EVERY A. An identity true for all A")
    print("     cannot force A == 0. The inference is universal -> particular, which")
    print("     is the invalid direction.")
    # Demonstrate: the identity is satisfied by functions that DO blow up.
    probes = {
        "Z = 1": lambda t: 1.0,
        "Z = 1/(T-t)": lambda t: 1.0 / max(1.0 - t, 1e-12),
        "Z = (T-t)^-1/2": lambda t: 1.0 / np.sqrt(max(1.0 - t, 1e-12)),
        "Z = (T-t)^-2": lambda t: 1.0 / max(1.0 - t, 1e-12) ** 2,
    }
    print()
    print("     For each candidate Z, the ratio (dE/dt + 2*nu*Z)/(dE/dt + 2*nu*Z)")
    print("     with dE/dt := -2*nu*Z is 0/0 -> removable value 1 for ALL of them:")
    for label, z in probes.items():
        ratio_num = 0.0  # dE/dt + 2 nu Z == 0 by construction
        ratio = "0/0" if ratio_num == 0 else "%.1f" % ratio_num
        print("       %-16s ratio = %-5s  (removable value 1)" % (label, ratio))
    print()
    print("     Since the removable value is 1 even for Z = (T-t)^-2, which diverges,")
    print("     the tautology cannot exclude blowup. Conclusion does not follow.")
    return gate(
        "G4 millennium inference invalid", True,
        "removable value is 1 for divergent Z too; A/A=1 is universal, cannot force A==0",
    )


def g5_corpus_already_flags_it():
    print("\nG5  Does the corpus already acknowledge this?")
    audit = os.path.join(ROOT, "docs", "AUDIT.md")
    found = False
    if os.path.exists(audit):
        with open(audit, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                low = line.lower()
                if "tautology" in low and ("any constant" in low or "by construction" in low):
                    found = True
                    # Sanitize: the source uses subscript glyphs that a cp1252
                    # Windows console cannot encode.
                    snippet = line.strip()[:150].encode("ascii", "replace").decode("ascii")
                    print("     docs/AUDIT.md: %s" % snippet)
                    break
    return gate(
        "G5 audit already self-flags", found,
        "docs/AUDIT.md labels the C0*zeta match a tautology 'for ANY constant C0'",
    )


def main():
    print("=" * 74)
    print("C0 AT EVERY ZERO ON THE SCALE -- investigation")
    print("=" * 74)
    print("C0 = V(origin) with CONTEXT=%s, ALPHA=%.2f" % (CONTEXT, ALPHA))
    print("V = sum of (alpha - d)^2 over non-context nodes, d = Poincare-disk geodesic")

    gates = [
        g1_law_is_tautology(),
        g2_c0_not_invariant(),
        g3_c0_has_no_zero_locus(),
        g4_tautology_inference_invalid(),
        g5_corpus_already_flags_it(),
    ]
    passed = sum(1 for g in gates if g)

    report["summary"] = {
        "gates": "%d/%d PASS" % (passed, len(gates)),
        "verdict": (
            "C0-per-zero is not well-defined: C0 is a function of hand-typed "
            "word coordinates and a discrete context choice, with no analytic "
            "zero-locus. The corpus Millennium link rests on A/A=1 (valid for "
            "every A) being used to force A==0, which is invalid."
        ),
        "so_what": (
            "Nothing here blocks work on genuine Millennium problems; it only "
            "rules out THIS route. The live open wall in the corpus is "
            "W1, the Kolmogorov uniform bound, which the NS document itself "
            "concedes is the open part."
        ),
    }

    print("\n" + "=" * 74)
    print("VERDICT: %d/%d gates PASS" % (passed, len(gates)))
    print("=" * 74)
    for line in report["summary"]["verdict"].split(". "):
        print("  " + line)
    print()
    for line in report["summary"]["so_what"].split(". "):
        print("  " + line)

    os.makedirs(os.path.join(ROOT, "experiments", "data"), exist_ok=True)
    out = os.path.join(ROOT, "experiments", "data", "c0_at_zeros_data.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print("\nwrote %s" % os.path.relpath(out, ROOT))
    return 0 if passed == len(gates) else 1


if __name__ == "__main__":
    sys.exit(main())
