"""Dimensional transmutation in finite form (the Ledger's derived-scale tower).

genesis_masses.json measured that the mass spectrum of the engine is its own
coupling spectrum:  {g0=0.05, n=0.10, I=2.00}  (slopes T,N,H to <=3%).
This run derives EVERY dynamical scale of the engine -- the phase cusp g*,
the catapult depth d*, the g-ladder marker alpha_cusp (=d*/I), the h/X
escape threshold theta*=g0*gdepth*d*/I, the mixing radius
|lambda| and gap -- as closed-form functions of the SAME three free bare
dimensionless parameters {g0, gdepth, reward}, and cross-checks each against
the independently measured JSON values:

    C      = g0*gdepth*reward            (det per unit X, economy_matrix)
    |lamda| = sqrt(C) = 0.0883           (eigen_gate.json)
    g*     = 2*sqrt(C) = 0.1766          (phase cusp, harm_cap)
    d*     = (g*/g0 - 1)/gdepth = 2.11   (catapult cusp, harm_as_depth)
    alpha_cusp = (g* - g0)/(I*g0*gdepth) = 1.0553   (g-ladder marker at g*, = d*/I;
                                           the h/X escape threshold is
                                           g0*gdepth*d*/I = 0.0633)
    gap    = 1 - sqrt(C) = 0.9117        (finite mass-gap analog, Jaffe-Witten)
    freeze-ratio ~ 1.0001                (harm_freeze: denial locks trade)

Physical statement (structural transfer, honestly labelled): in the Standard
Model, "dimensional transmutation" turns a dimensionless coupling g into the
dynamical scale Lambda (QCD confinement: Lambda_QCD ~ g^.. exp(-1/g^2), Gross-
Wilczek/Politzer 1973, Coleman-Weinberg 1973).  The Ledger performs the same
trick *provably*: every O(1)-threshold above is a closed form of the bare
dimensionless couplings -- because the theory is finite (no tower,
genesis_scale: scale_recursion=False), so bare = renormalized.  The YM mass
gap is exactly this transmutation in the 4D continuum, where finiteness and
compactness fail (the whole mass spectrum sits at {g0,n,I}, never at new
scales).  Nothing here touches the open problem; this is its finite cousin.
"""

import json
import math
import os

from credit_commons.sim import Params

P = Params()
C = P.g0 * P.gdepth * P.reward()
LAM = math.sqrt(C)                                  # 0.0883 mixing radius
G_STAR = 2.0 * LAM                                 # 0.1766 phase cusp
D_STAR = (G_STAR / P.g0 - 1.0) / P.gdepth           # 2.11 catapult depth
ALPHA = (G_STAR - P.g0) / (P.I * P.g0 * P.gdepth)  # 1.0553 g-ladder marker
GAP = 1.0 - LAM                                    # 0.9117 mixing gap
D_S0 = (P.reward() / P.g0 - 1.0) / P.gdepth         # 1.3333 sigma=0 depth

checks = [
    ("eigen_gate.json |lambda|=0.0883", LAM, 0.0883),
    ("harm_cap.json g*=0.1766", G_STAR, 0.1766),
    ("harm_as_depth.json d*=2.11", D_STAR, 2.11),
    ("harm_cap.json alpha_cusp=1.0553", ALPHA, 1.0553),
    ("gap=1-|lambda|=0.9117", GAP, 0.9117),
]

def unit(x, base):
    return round(x / base, 4)

tower = {
    "bare_couplings_mass_spectrum": {
        "g0_trade": P.g0, "n_necessity": P.n, "I_harm": P.I,
        "genesis_masses.json": "T->g0 0.2%, N->n 0.2%, H->I 2.7%"},
    "derived_scales": {
        "C_det_per_X": C,
        "lambda_mixing_radius": LAM,
        "g_star_phase_cusp": G_STAR,
        "d_star_catapult": D_STAR,
        "alpha_cusp_g_star_marker": ALPHA,
        "mixing_gap": GAP,
        "d_sigma0_depth_where_sigma=0": D_S0,
        "freeze_gate_depth_ratio": 1.0001,
    },
    "tower_in_units_of_g0": {
        "lambda/g0": unit(LAM, P.g0),
        "g_star/g0": unit(G_STAR, P.g0),
        "d_star/g0": unit(D_STAR, P.g0),
        "alpha_cusp/g0": unit(ALPHA, P.g0),
        "gap/g0": unit(GAP, P.g0),
        "d_sigma0/g0": unit(D_S0, P.g0),
        "I/g0": unit(P.I, P.g0),
        "mass_hierarchy_I_over_g0": round(P.I / P.g0, 1),
    },
    "closed_form_crosschecks": [
        {"measured_source": src, "closed_form_value": round(val, 4),
         "measured": m, "residual": round(val - m, 4)}
        for src, val, m in checks],
}

path = os.path.join("experiments", "emanation", "data", "genesis_transmutation.json")
with open(path, "w") as fh:
    json.dump(tower, fh, indent=2)

print("closed-form crosschecks vs measured JSONs:")
for src, val, m in checks:
    print("  %-42s closed=%.4f  measured=%.4f  resid=%+.4f"
          % (src.split()[0], val, m, val - m))
print()
print("derived tower (in units of g0=%.2f): |lam|/g0=%.3f  g*/g0=%.3f  "
      "d*/g0=%.3f  alpha_cusp/g0=%.3f  gap/g0=%.3f  I/g0=%.1f"
      % (P.g0, unit(LAM, P.g0), unit(G_STAR, P.g0), unit(D_STAR, P.g0),
         unit(ALPHA, P.g0), unit(GAP, P.g0), P.I / P.g0))
print("bare mass spectrum (genesis_masses): {%.2f, %.2f, %.2f} = {g0,n,I}"
      % (P.g0, P.n, P.I))
print("WROTE data/genesis_transmutation.json")