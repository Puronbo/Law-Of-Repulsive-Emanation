# The Shared Wall and a Path Forward

**Status: interpretive. Not a machine-checked claim, and not a Millennium result.**
This note records the *structure* exposed by the refutation of the Navier–Stokes
"Fourier bound" (`experiments/fourier_bound_scaling.py`) and asks what, if
anything, generalises across the open Millennium problems. It is a map of a
recurring obstruction, not a proof of anything.

## The skeleton

Every one of the open walls has the same shape:

> a **completed local / perturbative theory**, plus **one critical-scale control
> quantity that is exactly marginal** — so it neither decays fast enough to make
> an integral converge, nor is bounded by the norms the local theory supplies.

The Navier–Stokes instance is now concrete rather than rhetorical: the energy
identity reaches `H^1`, but closing the Prodi–Serrin integral needs `L^inf`
control, which in 3D requires `H^{3/2+}`. The attempted bridge
(`||u||_inf^2 <= 4 E Z`) was a degree-mismatched, false inequality whose
Cauchy–Schwarz route needs the divergent sum `sum 1/k^2` on `Z^3`. The wall is
exactly the missing `H^{1} -> H^{3/2+}` gap: control at the critical exponent.

## Per-problem map

| Problem | Local theory that works | Critical quantity that fails | Next-order target (forward) |
|---|---|---|---|
| Navier–Stokes | Serrin / Sobolev scaling; local smoothness | `L^inf` control from `H^1` (needs `H^{3/2+}`); `sum 1/k^2` diverges | a genuinely sub-critical Besov/Lorentz estimate for `||u||_inf`, or the dynamic-rescaling / Type-II route |
| Riemann | analytic continuation; explicit formula per zero | square-root cancellation in `N(T)` / `zeta` error term | arithmetic of the `O(sqrt T)` fluctuation |
| P vs NP | every explicit upper bound / algorithm | a uniform circuit lower-bound *measure* | a non-relativising measure (geometric complexity theory / algebraic) |
| Yang–Mills | perturbative QFT; renormalisation | construction of the non-perturbative measure at marginal coupling | Osterwalder–Schrader positivity + a mass-gap inequality |
| BSD | each curve's `L`-function, local factors | uniform analytic-to-arithmetic bridge | Iwasawa / derived correction to the moment |

The "same wall from different perspectives" reading is earned **only** at the
level of this skeleton. The *content* differs and matters:

- **method-barriers** (P vs NP): theorems — relativisation, natural proofs,
  algebrization — say whole *families of proof techniques* cannot work;
- **existence-barriers** (NS, YM): the object (a smooth global solution / a QFT
  measure) must be *constructed*, and averages don't pin every realisation;
- **bridge-barriers** (RH, BSD): two independently-defined worlds must be shown
  to coincide, and the difficulty is the bridge itself.

## Concrete next step for the Navier–Stokes wall

Do **not** keep sampling `O(1)`-amplitude fields on which the false bound looks
true. The honest options are:

1. replace the `E,Z`-only `L^inf` bound with a critical-space estimate that is
   actually sub-critical (a Besov `B^{s}_{p,q}` with `s > 3/p`, or a Lorentz
   refinement), so that the quantity integrated along the flow is controlled by
   `int Z dt`; or
2. accept that the naive self-similar (Type-I) route is kinematically forced but
   dynamically inadmissible, and pursue the two-scale dynamic-rescaling object
   (consistent with Frontier 1 of `Linear Stability of Candidate Swirl
   Profiles.md` and with `SelfSimilarExponents.lean`).

Either way the forward step is to **name the exactly critical quantity and the
next-order term that breaks its marginality** — the same move each column of the
table above asks for.

## What this is not

It is not a claim that the five problems are one theorem; the Millennium list is
historical curation, not a designed family. It is not a claim about any problem's
truth value. It is a claim about *why the walls stay open*: local theory finished,
critical-scale control missing — and about *where to push*: the next-order term.
