"""Branches and meeting points of the seven Millennium problems, treated as
SEVEN INDEPENDENT indeterminate functions - not one question in seven guises.

Each problem w_i is its own function over its own domain, returning its own
VALUE-TYPE:

  NSE     : w(u0) = blow-up time T*(u0)         -> measure/set answer
  YM      : w(gauge) = spectrum gap m            -> scalar answer (does m>0)
  P vs NP : w(class) = P=NP?                     -> boolean answer
  RH      : w(zeta) = zeros lie on Re=1/2        -> placement (line) answer
  BSD     : w(E)    = ord L_E(1) = rank(E)       -> integer answer
  Hodge   : w(X)    = every rational (p,q) class is algebraic -> boolean
  Poincare: w(M)    = M homeomorphic to S^3      -> boolean (solved)

Similarity branches (shared PRINCIPLE, not sameness):
  - EXISTENCE family: NSE (a solution exists smooth), YM (a gapped QFT
    exists), Poincare (the canonical form exists), Hodge (an algebraic
    representative).   Branch principle: "demand existence/realization."
  - DUALITY-IDENTITY family: RH (zeros identify the line), BSD (analytic
    order identifies the arithmetic rank), Hodge (class identifies cycle),
    Poincare (homotopy identifies homeotype).  Principle: "two worlds must
    agree at the boundary."
  - SEPARATION branch: P vs NP alone.  Principle: "the only claim of
    INEQUALITY among the seven."

Opposition pairs (rigorous antitheses):
  - classical-continuum (NSE, RH)   vs   quantum/spectral (YM)  and
    discrete (BSD, P/NP, Hodge).
  - separation (P vs NP) is the negation-complement of every equality type.
  - solved (Poincare) vs open: the completed branch is the shape-template
    for the unfinished ones.

MEETING POINTS: the Ledger instantiates one legitimate object per
VALUE-TYPE, and that is where the branches dock:
  measure:   S(theta*) = 0.83 (escape set measure; NSE-type)
  scalar:    theta* = 0.06332, mixing gap 0.9117 (YM-type numbers)
  line:      the smeared 1.09-decade transition band (RH-type placement)
  integer:   n_types=12, n_classes=5, n_gates=8 (BSD-type counts)
  boolean:   C0 = 0/0 = 1, gate outcomes, Dirichlet no-claim (P/NP/Hodge
             type); Poincare inherited true.

MISSING/INCOMPLETE SEGMENTS deduced (the actual charge of this run):
  Seg-A junction RH n BSD n NSE: the discrete-harmony strip census of the
     landmark Dirichlet polynomial (computed here on a grid).
  Seg-B P/NP: no separation witness exists in the toy (all gates O(1));
     a multi-trade realizability search is the citable design target
     (SAT/3CNF), recorded as pending, not built.
  Seg-C YM: no noncommutative deformation exists - a PRINCIPLED absence,
     reason recorded (Connes 1994; Rieffel 1994); the honest move is the
     recorded DROP, not an invented q-parameter.
  Seg-D NSE: no "generic-data" family; a Gini-shaped population run is the
     natural perturbation (CKN 1982 partial-regularity analog).
  Seg-E Poincare-method: no monotone functional certified; the ACTION
     deficit (mirror residual 0.125) is the candidate entropy-production
     analog (Perelman 2002 entropy monotonicity) - flagged, not claim.

No Millennium problem is claimed solved; Poincare inherited solved.
"""

import cmath
import json
import math
import os

# exact ratio landmarks of the threat law (genesis_law/genesis_tail)
LM = [1.0 / 75.0, 2.0 / 15.0, 2.0 / 5.0, 4.0]
LNAMES = ["a/d", "b/d", "a/c", "b/c"]


def harmony(s):
    return sum((v ** (-s)) for v in LM)


def strip_census():
    """Coarse grid scan of |H(sigma+it)| in 0<sigma<1 (RH-type placement)."""
    best = None
    for ks in range(1, 20):
        sigma = 0.03 + ks * 0.05
        for kt in range(0, 63):
            t = kt * 0.1
            z = abs(harmony(complex(sigma, t)))
            if best is None or z < best[0]:
                best = (z, sigma, t)
    return best


def main():
    best = strip_census()
    with open(os.path.join("experiments", "emanation", "data",
                           "harm_as_depth.json")) as fh:
        exp = json.load(fh)
    m = exp["mirror_ln"]
    action_deficit = m["residual"]            # mirror_pred - mean_action

    out = {
        "identity": "seven independent indeterminate functions w_1..w_7, "
                    "each returning its own value-type; linked only by "
                    "principled branches (existence, duality-identity, "
                    "separation) and rigid oppositions; docking at the "
                    "Ledger's one-object-per-value-type meeting points.",
        "functions": [
            {"problem": "NSE", "domain": "divergence-free smooth u0 in R^3",
             "indeterminate": "blow-up time T*(u0)",
             "value_type": "measure/set",
             "ledger_meeting": "S(theta*)=0.83, 95%% band [0.0598,0.0638]"},
            {"problem": "YM", "domain": "nonabelian gauge potential",
             "indeterminate": "spectrum gap m of the QFT Hamiltonian",
             "value_type": "scalar",
             "ledger_meeting": "numbers only: theta*=0.0633, gap 0.9117 "
                               "(Perron-Frobenius); mass-gap object "
                               "WITHDRAWN"},
            {"problem": "P vs NP", "domain": "languages over finite strings",
             "indeterminate": "P = NP?",
             "value_type": "boolean",
             "ledger_meeting": "gate booleans, O(1) decisions; no witness"},
            {"problem": "RH", "domain": "Riemann zeta (analytic continuation)",
             "indeterminate": "all nontrivial zeros on Re s = 1/2",
             "value_type": "line/placement",
             "ledger_meeting": "1.09-decade smeared band; harmony H(s) "
                               "strip census below"},
            {"problem": "BSD", "domain": "elliptic curve E / Q",
             "indeterminate": "ord_{s=1} L(E,s) = rank(E)",
             "value_type": "integer",
             "ledger_meeting": "12 types, 5 classes, 8 gates; mirror "
                               "residual 0.125 (NOT exact)"},
            {"problem": "Hodge", "domain": "smooth complex projective variety",
             "indeterminate": "every rational (p,q)-class is algebraic",
             "value_type": "boolean",
             "ledger_meeting": "realizability tautological (5 classes); "
                               "no projective structure"},
            {"problem": "Poincare", "domain": "closed 3-manifolds",
             "indeterminate": "any simply-connected closed 3-fold = S^3",
             "value_type": "boolean (SOLVED)",
             "ledger_meeting": "inherited true; direction space finite "
                               "(no nontrivial topology)"},
        ],
        "branches": {
            "existence_family": ["NSE", "YM", "Hodge", "Poincare"],
            "duality_identity_family": ["RH", "BSD", "Hodge", "Poincare"],
            "separation_branch": ["P vs NP"],
            "twins": [["NSE", "YM"], ["BSD", "Hodge"], ["RH", "Poincare"]],
            "oppositions": [
                ["classical_continuum: NSE, RH",
                 "quantum/spectral: YM; discrete: BSD, P/NP, Hodge"],
                ["separation: P vs NP", "equality-type: all others"],
                ["solved: Poincare", "open: all others"],
            ],
            "meeting_points": ["measure 0.83", "scalar theta*",
                               "line 1.09 decades", "integers 12/5/8",
                               "booleans C0=1, gates",
                               "method: error-bar + no-claim discipline"],
        },
        "missing_segments": [
            {"id": "Seg-A", "junction": "RH n BSD n NSE",
             "gap": "discrete-analytic interpolation: the harmony strip "
                    "census connects the continuous law to the discrete "
                    "landmark arithmetic",
             "this_run": "grid scan of |H(sigma+it)| in the strip",
             "result": "min |H| = %.5f at sigma=%.2f, t=%.2f; finite "
                       "4-term polynomial curiosity; NO zeta claim"
                       % (best[0], best[1], best[2]),
             "references": "Montgomery & Vaughan 2006 (analytic number "
                           "theory); Kinderman & Monahan 1977 (ratio of "
                           "uniforms gives the law)"},
            {"id": "Seg-B", "junction": "P/NP",
             "gap": "no separation witness (everything O(1)); need a "
                    "multi-trade realizability search over the finite "
                    "semigroup (12 types x 8 gates)",
             "status": "pending design, not built",
             "references": "Garey & Johnson 1979; Papadimitriou 1994 "
                           "(NP-completeness); Razborov & Rudich 1997 "
                           "(natural proofs wall)"},
            {"id": "Seg-C", "junction": "YM",
             "gap": "no noncommutative deformation of the gauge algebra; "
                    "a PRINCIPLED absence",
             "status": "recorded DROP (introducting a q-parameter would be "
                       "an axiom, not a derivation)",
             "references": "Connes 1994 (Noncommutative Geometry); Rieffel "
                           "1994 (quantum tori)"},
            {"id": "Seg-D", "junction": "NSE and measure",
             "gap": "no generic-data family: box-uniform population only; "
                    "Gini-shaped draws are the natural perturbation",
             "status": "pending run",
             "references": "Caffarelli, Kohn & Nirenberg 1982 (partial "
                           "regularity); Prodi 1959; Serrin 1962"},
            {"id": "Seg-E", "junction": "Poincare-method (solved branch)",
             "gap": "no certified monotone functional; the ACTION deficit "
                    "(mirror residual) is the candidate",
             "result": "action_deficit = %.4f (mean action %.4f vs mirror "
                       "%.4f); flagged, NOT claimed as a monotone law"
                       % (action_deficit, m["mean_action_ln_geff"],
                          m["gain_over_draw_plus_harm"]),
             "references": "Perelman 2002 arXiv math.DG/0211159 (entropy "
                           "monotonicity); Hamilton 1982 (Ricci flow)"},
        ],
        "reading": "seven branches, seven value-types, one dock; the "
                   "branches are NOT the same problem - they meet only "
                   "where a ledger object has the same value-type and "
                   "survives the no-claim gate.  Missing segments are made "
                   "explicit and either computed, designed, or dropped with "
                   "a reason.",
    }
    path = os.path.join("experiments", "emanation", "data",
                        "genesis_branches.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print("strip census: min |H| = %.6f at (sigma=%.3f, t=%.3f)"
          % (best[0], best[1], best[2]))
    print("  (finite 4-term Dirichlet polynomial; strip zeros possible; "
          "recorded, no zeta claim)")
    print("action deficit (Seg-E) = %.4f  [mirror %.4f vs mean action %.4f]"
          % (action_deficit, m["gain_over_draw_plus_harm"],
             m["mean_action_ln_geff"]))
    print("Seg-B separation witness: pending design (12 types x 8 gates "
          "realizability).")
    print("Seg-C YM: principled DROP (no noncommutative deformation; "
          "Connes/Rieffel).")
    print("Seg-D NSE: generic-data run pending (Gini-shaped population).")
    print("WROTE data/genesis_branches.json")


if __name__ == "__main__":
    main()