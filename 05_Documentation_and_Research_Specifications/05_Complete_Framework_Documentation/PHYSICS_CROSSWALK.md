# Physics Crosswalk

**Status: bridge map, not an equivalence.** This file joins the *claim register*
(`EXPLICIT_CLAIMS.md`, cards C1 … C38) to the physics side of the repository. It is
the physics twin of `EXTERNAL_CORPORA_CROSSWALK.md`: that map links our cards to
*external mathematics*; this one links them to the physics programs under
`07_Interdisciplinary_Connections_and_Frameworks/`.

> **Scope boundary.** This is a *research program*, not a proof of anything. **No
> Millennium problem is solved, proved, or settled by this project.** See
> [`WHAT_THIS_DOES_NOT_PROVE.md`](WHAT_THIS_DOES_NOT_PROVE.md). The governing rule
> here is **adjacency ≠ equivalence**: that a card's arithmetic is the same *shape*
> as a textbook physics object does not make the card a physics result, nor the
> physics a proof.

## How to read a row

| status | meaning |
|---|---|
| `Lean-proved` | the card's arithmetic statement is machine-checked (Mathlib or the register) |
| `physics-known` | the physics object is textbook; the *identification* is standard, not proved here |
| `analogy` | a shared shape only — no theorem and no equivalence is claimed |
| `open` | the physics question is unresolved and the card names the missing entity |
| `excluded` | framing only; excluded by the scope gate (see `VERIFIED_SYNTHESIS_AND_EQUIVALENTS.md`) |

The genuine, defensible hinge is a removable `0/0` — a local divergence that
resolves to a finite value. Three physics joins rest on it (renormalization; the
Yang–Mills mass-gap crossover; the critical-scale boundedness of the
Navier–Stokes / Onsager wall); the rest are shape-analogies and are tagged as such.

## Crosswalk

| Card | Math (Lean) | Physics phenomenon | Standard object / theorem | Status |
|---|---|---|---|---|
| **C23** | `RemovableComplexBridge` | **Renormalization**: a divergent loop integral is a 0/0 and the counterterm is its removable value | dimensional regularization / BPHZ | physics-known |
| **C24** | `LiouvilleBridge` | a bounded whole-plane response cannot vary (global collapse) | Liouville's theorem | Lean-proved |
| **C1** | `CriticalLadder` | scaling-critical function spaces of turbulence | Prodi–Serrin; BMO⁻¹ | physics-known |
| **C4/C6** | `ExplicitClaims`, `EnstrophyBarrier` | exactly one extra power of enstrophy stands between the energy identity and regularity | quantitative continuation (Tao) | open |
| **C25** | `SerrinLadder` | energy + enstrophy control `Lᵖ` iff `p ≤ 6` | Sobolev `H¹ → L⁶` | Lean-proved |
| **C26** | `GreatAttractor` | orientation of a fixed point = its stable/unstable direction | Lyapunov exponent / multiplier | Lean-proved |
| **C28** | `MixtureGrowth` | adding parts transmits, never fabricates, concentration | Minkowski (`‖·‖` triangle) | Lean-proved |
| **C29** | `OnsagerCriterion` | Onsager excess and anomalous dissipation | Onsager (1949) | open |
| **C30** | `ContinuationCriterion` | the logical shape of any blow-up criterion | Beale–Kato–Majda (1984) | physics-known |
| **C31** | `StableBounded` | an attracting response is a bounded one | Banach contraction principle | physics-known |
| **C32** | `SufficiencyLoop` | 2D closes, 3D does not | Ladyzhenskaya (2D NS) | Lean-proved |
| **C33** | `SelfSimilarExponents` | exponents of a self-similar blow-up ansatz | Hou, arXiv:2405.10916 | analogy |
| **C36** | `NoetherDiscrete` | a balanced force conserves momentum under one discrete-Newton step (conservation ↔ translation symmetry) | Noether's theorem (1918) | Lean-proved |
| **C37** | `UniverseGrowth` | an increasing point universe that creates zero-momentum points conserves total momentum (growth as a continuity equation) | Noether's theorem (1918), cosmological particle creation | Lean-proved |
| **C38** | `CriticalAmplitude` | at a phase transition the order parameter and its scale both vanish; their ratio's removable value is the critical amplitude, and the exponents satisfy the classical scaling relations | Widom (1965), Rushbrooke (1963), Josephson (1966), Fisher (1964) | Lean-proved |
| **C19** | `ZeroProbe` | an identity 0/0 resolves to `1` (dimensionless ratios) | gauge-invariant ratios | Lean-proved |
| **C20** | `ZeroValuation` | order of vanishing as a critical scaling exponent | renormalization-group exponent | analogy |
| **C13** | `EmergentTime` | time as a transfer count | — (structural; not a physical claim) | analogy |
| **[cert]** | `MassGap` | Yang–Mills **mass gap** = a removable crossover | exponential correlation length | open |
| **[cert]** | `NavierStokes` | global-regularity wall | Prodi–Serrin sufficiency | open |
| **[cert]** | `Cosmology.AcousticZeroFlow`, `Cosmology.OriginWindow` | Big-Bang / Planck “0/0” narrative | — | excluded |

## Sibling maps (tracked)

- [`EXTERNAL_CORPORA_CROSSWALK.md`](EXTERNAL_CORPORA_CROSSWALK.md) — cards linked to *external mathematics* (the mathematical twin of this file).
- [`SHARED_WALL_AND_PATH_FORWARD.md`](SHARED_WALL_AND_PATH_FORWARD.md) — the honest account of what the wall is and is not.
- [`WHAT_THIS_DOES_NOT_PROVE.md`](WHAT_THIS_DOES_NOT_PROVE.md) — the scope boundary this map obeys.

## Sources (physics documents)

These live in the (larger) research tree and are cited by name; they are not part
of the tracked verification checkout.

- [`PHYSICS_CATEGORIZATION.md`](../../../07_Interdisciplinary_Connections_and_Frameworks/04_Theoretical_Physics_Implementations/j/PHYSICS_CATEGORIZATION.md) — the photon / rubber-ball verification catalogue (sourced, Tier II).
- [`THEORY_CONNECTIONS_SUMMARY.md`](../../../07_Interdisciplinary_Connections_and_Frameworks/04_Theoretical_Physics_Implementations/j/THEORY_CONNECTIONS_SUMMARY.md) — the connection map.
- [`VERIFIED_SYNTHESIS_AND_EQUIVALENTS.md`](../../../07_Interdisciplinary_Connections_and_Frameworks/04_Theoretical_Physics_Implementations/j/VERIFIED_SYNTHESIS_AND_EQUIVALENTS.md) — the honest verdict, including which families are *excluded*.
- [`summary.md`](../../../07_Interdisciplinary_Connections_and_Frameworks/02_Mathematical_Physics_Connections/summary.md) — the L.O.R.E. 0/0-pattern chapter series (statistical mechanics).

## What this does not claim

The crosswalk records *adjacency*, not equivalence. Only the `Lean-proved` status
denotes a kernel-checked statement, and even there the statement is the register's
*arithmetic*, not a physics claim: that a scaling weight vanishes, that a network
average is bracketed, that a contraction is bounded. The `open` rows are the honest
wall (renormalized gravity/Planck, the mass gap, the Navier–Stokes wall) and stay
OPEN. Checked offline by `test_physics_crosswalk.py`.
