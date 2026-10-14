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

Option 1 is now explicit. The energy method reaches `L^p` exactly for `p <= 6`
(Gagliardo–Nirenberg exponent `theta(p) = 3/2 - 3/p <= 1`, verified in
`serrin_ladder.py`), and the admissible Serrin route at the ceiling `p = 6`
(`q = 4`) closes only if `int Z^2 dt < inf` — whereas the energy identity gives
only `int Z dt < inf`. The `p = 3` endpoint needs `L^inf` (the dimensional wall).
So the exactly critical quantity is **one extra power of enstrophy**: the
next-order term that would break the marginality is any estimate giving
`int Z^{1+epsilon} dt < inf` for some `epsilon > 0`, or its Besov/Lorentz
generalisation.

Either way the forward step is to **name the exactly critical quantity and the
next-order term that breaks its marginality** — the same move each column of the
table above asks for.

## The wall is dimensional (and what "mixing dimensions" can buy)

The missing control is not a constant; it is a dimension. `H^1` embeds in
`L^inf` **iff the effective dimension `d < 2`** (`dimension_threshold.py`):
a unit-`H^1` bump at width `eps` has `||u||_inf^2 = 10^(d-2)` per decade —
bounded at `d=2`, diverging for `d>2`. Physical `D=3` needs `s>3/2` and has
`s=1`; Hou's effective `n~3.188` is short by `0.594`. So the energy method is
one half-derivative (or one dimension) short, and this is the same wall.

The natural repair is to let the dimension itself vary — "a mixture of all
dimensions". `dimension_mixture.py` pins what that can and cannot do:

- **No averaging.** `||u||_inf/||u||_{H^1}` of a mixture is governed by `max_i d_i`,
  not a mean. Adding a low-dimension bulk to a `d=3` spike does not lower the
  sup (bulk `0.965` -> with a tiny spike `1.461` -> pure spike `49.6`). Dimension
  of a mixture is a sup, so mixing alone cannot push `d_eff` below `2`.
- **Intermittency budget.** The only route is energy concentration: the
  admissible high-dimension H^1 fraction is `theta_max = O(eps)` (measured
  `3.33e-3` at `eps=1e-3` vs leading-order `3.29e-3`; a clean factor `0.10` per
  decade). So closure requires the high-dimension energy to *vanish linearly
  with scale* — which is exactly intermittency, quantified.

Four viable readings of "a mixture of all dimensions", each with its open content:

| Reading | Framework | Open content |
|---|---|---|
| Capacity/dimension spectrum | Riesz potentials on fractal measures (Adams/Hedberg) | which admissible `mu` is compatible with the NS/Puno energy identity |
| Continuous dimension | dimensional regularisation / scaling-critical dimension (Tao; `L^2` critical at `D=2`) | the nonlinearity does not continue cleanly in `D` |
| Dynamical dimension | spectral-in-`n` for `Delta_n` (Frontier 1's next step; threshold `n_c=1`, physical `n=3`) | `n`-independence is proved for *fixed* `n` only (`SelfSimilarExponents.lean`) |
| Multifractal dimension | log-correlated fields / Gaussian multiplicative chaos | no rigorous bridge from NS singularity formation to such a measure yet |

The unifying open content — the **bridge barrier** — is identical in all four:
an equation-preserving reweighting that keeps the high-dimension energy under the
`O(eps)` budget at every scale. Same shape as the refuted-bound wall.

### Where the follow-up steps landed

1. **Log corrections do not repair the wall** (`log_borderline.py`). At `d=2`
   the BG-log ratio is bounded and decreasing (`0.340 -> 0.237`); at `d=3` it
   grows `~22x` per three decades of scale. Every logarithmic rescale costs less
   than one power, so 3D escape is `H^{3/2}` (Besov/Lorentz-class), not `H^1 log`
   — the missed `1/2` derivative is already the dimensional wall.
2. **The dimension is a spectral eigenvalue** (`spectral_in_n.py`).
   `lambda_1(n) = j_{(n-1)/2,1}^2` grows with `n` (`5.783 -> 14.682 -> 26.375`
   at `n = 1, 3, 5`), so the Laplacian stiffens with effective dimension, and the
   threshold `n_c = 1` (`nu = 0`, `J_0`) sits exactly at `d_c = 2`. Carrying a
   dynamical `n(t)` into the exponent balance is Frontier 1's concrete next step
   (currently `n` fixed).
3. **On-flow the marginal quantity is finite with constant flatness**
   (`ns_critical_integral.py`). On resolved pseudo-spectral flows across
   `nu = {0.2, 0.1, 0.05}` the exact identity `int Z dt = (E0-E(T))/(2 nu)` holds
   to `1e-2..1e-3`, `int Z^2 dt` is finite, and temporal enstrophy flatness is
   `F ~ 5-7` with sweep exponent `p = -0.20`: resolved viscous flows do not show
   intermittency growth. Diagnosis: a genuine singularity must push the flatness
   regime into the unresolved near-singular range, the same `O(eps)` energy budget
   quantified by `dimension_mixture.py`.
4. **The one-extra-power is now machine-checked** (`SerrinLadder.lean`, wired
    into the library root and kernel-verified — earlier commits left it out of
    `PunoCalculus.lean`, so `lake build` had not actually compiled it). The
    ladder arithmetic `theta(p) = 3/2 - 3/p` with ceiling `theta(p) <= 1 iff
    p <= 6`, the full Serrin line `2/q + 3/p = 1`, the closed-form critical power
    `theta(p)*q(p)/2 = 3(p-2)/(2(p-3))` (exactly `2` at `p = 6`), the gap
    conditional `1+eps closes (6,4) iff eps >= 1`, and `2 - 1 = 1` are formal
    theorems (eleven substantive, axioms exactly `[propext, Classical.choice,
    Quot.sound]`). The formal target implied by 1-3 is exactly `int Z^{1+eps} dt`
    for some `eps > 0` (or its Besov/Lorentz generalisation) — the next-order
    term that breaks the marginality; whether any such power integrates is the
    OPEN marker `extraEnstrophyPowerIntegralOpen`.
 5. **On-flow the enstrophy scale sits far from the grid** (`ns_spectral_slope.py`).
    `k_eff = sqrt(Z/E)` never exceeds `0.32` of the dealiased cutoff across the
    viscosity sweep, the ratio-vs-`nu` power is `+0.02` (flat), and the spectral
    peak migrates *backward* (`4 -> 3`, no forward cascade): decaying resolved runs
    approach the wall `s_c = 3/2` only in the unresolved near-singular range.
 6. **Even sustained forcing produces no intermittency on resolved scales**
    (`ns_forced_intermittency.py`). With additive forcing pumping the band
    `|k| in [2,3)` to a steady `Z ~ 12`, the enstrophy time series is
    quasi-laminar: flatness `F = 1.008` at both `nu = 0.1` and `0.05` (sweep power
    `+0.00`), the high-shell share peaks at `0.03-0.05%` against the `O(eps)`
    intermittency budget of `dimension_mixture.py` (margin `> 431x`), and
    `k_eff = 22%` of cutoff. No burst mechanism appears on resolved scales.
 7. **Addition of parts is not another act of growth on resolved scales**
    (`ns_spike_mixture.py`; formal arithmetic in `MixtureGrowth.lean`). A
    divergence-free high-shell spike (`|k| in [6,8]`) added to the smooth bulk
    starts at `52-94%` of enstrophy in high shells and is dissipated to `0.00%`
    within the run at every `nu`; `k_eff` peaks just above `55%` of cutoff only
    for the strongest spike (`lambda = 4`) and relaxes back; flatness rises with
    spike fraction but as the transient-decay signature, not bursting. Formally a
    mixture's ratio is bracketed by the parts' ratios (`MixtureGrowth.lean`):
    averaging cannot fabricate concentration, and the added part here never
    reaches the wall scale. Together with 5-6, every resolved route to
    intermittency is quiet — the burst mechanism must live in the unresolved
    near-singular range.
 8. **The flow is a conservative, distributed force network and inertia is what
    holds it** (`ns_force_network.py`; formal arithmetic in `ForceNetwork.lean`).
    Reading change as "everything interconnected in force, each part a collection
    of points held by inertia": nodes = wavenumber shells, inertia `I_m` = shell
    energy, force `T_m` = nonlinear triad transfer, change `dI_m/dt = T_m - D_m`.
    Measured over `nu = {0.2, 0.1, 0.05}`: the interconnection is conservative
    (`|sum T_m|/sum|T_m| ~ 1e-5` — it redistributes, never creates), distributed
    not focused (participation `PR_T ~ 4` of 10 nodes, max single-node share
    `~0.35`), heavier shells change less per unit inertia (`corr = -0.44..-0.50`),
    and all change is accounted for by the network minus the drag (closure
    `1e-2..9e-2`). Formally (`ForceNetwork.lean`) a weighted network's value lies
    between its parts' (`networkValueBetween`) and `force/inertia` is antitone in
    inertia (`inertiaDampsChange`): the network reweights, it cannot mint
    concentration. With 3-7, no resolved mechanism concentrates change.
  9. **The scaling-critical ladder is one invariant in many forms**
     (`CriticalLadder.lean`). Under the NS rescaling the `B^s_{p,q}` norm carries
     factor `lambda^{s+1-3/p}`, invariant exactly on `s = s_crit(p) = 3/p - 1`
     (`L^3`, `H^{1/2}`, `H^{-1/2}` at `p = 3, 2, 6`). The Serrin interpolation
     exponent and the critical smoothness are two faces of one invariant:
     `theta(p) + s_crit(p) = 1/2` for EVERY `p` (`thetaAddSCrit`). The ladder is
     antitone (`L^3` ⊂ `B^{-1+3/p}_{p,∞}` ⊂ `BMO^{-1}` ⊂ `B^{-1}_{∞,∞}`) and
     `s_crit(p) > -1` for finite `p`. The wall becomes a single statement — whether
     the invariant critical norm stays BOUNDED along the flow, equivalently whether
     the Onsager excess `eta > 0` holds (`onsagerExcess_supercritical`;
     `criticalInvariantBoundedOpen`). Eight substantive theorems, axioms exactly
     `[propext, Classical.choice, Quot.sound]`; build green (8737 jobs).
 10. **On-flow the resolved cascade moves toward the Onsager bound as viscosity
     drops** (`ns_onsager_flux.py`). The cumulative spectral flux `I(K) = int |Pi(K)| dt`
     decays as `K^{-a}` with `a = 1.72 / 1.20 / 0.64` at `nu = 0.2 / 0.1 / 0.05`:
     strictly supercritical (`eta_max = a-1 > 0`, "safe") at higher viscosity, and
     CROSSING the Onsager-critical line `a = 1` at `nu = 0.05`. Lowering viscosity
     drives the resolved cascade toward (past) the Onsager rate -- the direction of
     the wall. Caveat: `nu = 0.05` is dissipatively under-resolved at N=32, so the
     crossing may be grid-scale pile-up; diagnostic only. **[RETRACTED this cycle:
     a resolution study (`ns_onsager_flux_resolution.py`) gives `a = 1.20 / 7.96 /
     12.01` at `N = 32/48/64` (`nu = 0.1`) -- NOT grid-converged -- so this trend
     is a resolution artefact. See bullet 15.]**
 11. **The resolved spectrum has a common shape, but the nontrivial rescaling
     variable is not distinguished** (`ns_profile_collapse.py`). "One pattern, many
     forms" tested as a renormalisation fixed point: energy density `d(k) = E(k) k`
     resampled in `xi = k/V` and compared across times and viscosities. Mean relative
     L1 spread is small for every choice (`k_eff` 0.065, `k_peak` 0.168, bare `k`
     0.055) — the resolved spectral shape is approximately invariant — but the
     trivial bare-`k` variable is marginally best, so `k_eff` rescaling does NOT
     improve the collapse at N=32. Whether a nontrivial rescaling is forced in the
     singular limit stays OPEN. Together with 9-10: the single invariant is real and
     formal, but resolved flows neither concentrate it nor single out a nontrivial
     rescaling — the wall is to show the invariant stays bounded in the limit.
 12. **The wall is itself a removable 0/0: zero defines its own position, and it
     scales on how many zeros it has** (`ZeroFixedPoint.lean`). The register reading
     of the honest wall (`THE_LAW_OF_SINGULARITIES.md` §12.1) made arithmetic:
     (a) *self-position* — at a fixed point `T x₀ = x₀` with derivative `L`, the
     change-of-position per change-of-position `(T x - x)/(x - x₀)` has removable
     value `L - 1` (the Banach/Brouwer 0/0, Experiments #34/#35); for the identity
     the self-shift is exactly `0`. `zero` is the point whose own position it
     defines. (b) *scales on the number of zeros* — dividing `(x - x₀)^k · h` by
     `(x - x₀)^j` yields the finite value `h x₀` when `j = k`, `0` when `j < k`,
     and a pole (reciprocal `-> 0`) when `j > k`: the wall shrinks itself to a
     finite value exactly at its order of vanishing `k`, Lemma 2.1 ("0/0 removable
     iff equal order") as three exact limits. This does not prove regularity — it
     recasts the wall as the statement that the singularity is a *removable* 0/0
     (finite order), which is precisely the boundedness the critical ladder (9)
     and the flux probe (10) test on-flow. Five substantive theorems, axioms
     exactly `[propext, Classical.choice, Quot.sound]`; build green (8738 jobs).
 13. **The great attractor: the wall has an orientation, and its number of zeros
     shifts the critical rung** (`GreatAttractor.lean` + `ns_zero_order.py`).
     (a) *Orientation* — at a fixed point `T x₀ = x₀` with derivative `L`, the
     distance ratio `|T x - x₀| / |x - x₀| -> |L|`; the point **repels** nearby
     points (`|x - x₀| < |T x - x₀|`) when `|L| > 1` and **attracts** them ("it
     shrinks itself") when `|L| < 1` — the trichotomy of `orientation`. The
     register's "great attractor that repels the known universe from itself" is
     the `|L| > 1` branch; the sign of the **Lyapunov exponent** `log |L|` is the
     orientation (`fixedPoint_logSign`), the formal twin of the measured rate.
     (b) *Order meets the ladder* — an object of amplitude
     weight `a` in `L^p` has homogeneous-norm scaling weight `a + s - 3/p`,
     vanishing exactly on `s = criticalSmoothness a p = 3/p - a`; the register's
     critical ladder is the **order-one** rung (`criticalSmoothness 1 p = sCrit p`),
     each extra zero buys one order of smoothness, and higher order needs less
     smoothness. So the single invariant (9) is the one-zero form of a
     number-of-zeros family. On-flow (`ns_zero_order.py`, `nu = 0.2/0.1/0.05`):
     the high-shell enstrophy has a FINITE order `k = 6.93 / 4.88 / 3.41 > 1`
     (the wall reads as a removable 0/0 of finite order, not a pole), and the
     share `Z_high/Z_low` has rate `lambda = -5.48 / -3.47 / -1.87 < 0` — the
     resolved flow is ATTRACTING at every `nu`, but `lambda` rises toward `0` and
     `k` falls as `nu -> 0`: both trends point at the wall in the unresolved
     range. The great attractor does not yet repel; repulsion would live beyond
     the resolved range. Resolution convergence (`ns_resolution_study.py`,
     `nu = 0.1/0.05`, `N = 32/48/64`): both `k` and `lambda` settle within 3% from
     `N = 48` to `64`, so the finite order and the attracting orientation are
     grid-converged; refining the grid mimics lowering `nu` (`k` down, `lambda` up
      toward `0`) but never crosses to repulsion. Eleven substantive theorems
      (adding `orientationDiscriminator`, the formal cross-system discriminator),
      axioms exactly `[propext, Classical.choice, Quot.sound]`; build green
      (8741 jobs).
 14. **The one pattern: order sets the rung, orientation sets the direction — two
     numbers, one wall** (`OnePattern.lean`). The synthesis the whole register
     points at. Every guise of the scaling-critical object is the same ladder
     shifted by the order (`criticalCurve_through_ladder :
     criticalSmoothness a p = sCrit p + (1 - a)`; the register ladder is `a = 1`),
     and the recurrence identity `theta + criticalSmoothness a = 1/2 + (1 - a)`
     collapses to `thetaAddSCrit` at order one. Orientation is the second number:
     the sign of `log|L|` (`GreatAttractor.fixedPoint_logSign`). So the wall is
     governed by exactly two quantities — the order of vanishing `k`
     (removability / critical rung) and the multiplier `|L|` (attracting vs
     repelling) — which is why NS, the fixed-point 0/0, and the critical ladder
     are one object in many forms. On-flow both are read and both are robust:
     order `k > 1` finite and orientation ATTRACTING at every `nu`, every
     resolution (`ns_resolution_study.py`), and every initial condition
     (`ns_zero_order_robust.py`). Five substantive theorems, axioms exactly
     `[propext, Classical.choice, Quot.sound]`; build green (8740 jobs). The wall
     itself stays OPEN: the pattern is identified, the singular-limit bound is not.
 15. **The wall's sufficiency half, and where a diagnostic was wrong**
     (`OnsagerCriterion.lean`, `ns_onsager_flux_resolution.py`). Two honest steps
     for the open wall. (a) *Formal sufficiency skeleton*: if the invariant moment
     `Z` is uniformly bounded by `M`, then for every excess order `n` the
     supercritical moment is controlled, `sum Z^{n+1} <= M^n * sum Z`
     (`weighted_sum_le`); its contrapositive (`spike_of_excess`) is the wall — an
     Onsager-violating cascade forces `Z` to exceed `M`. So the missing brick is
     exactly "the invariant moment stays bounded", nothing more. (b) *A correction*:
     the Onsager-flux diagnostic (bullet 10) is RETRACTED — re-running it at
     `N = 32/48/64` gives `a = 1.20 / 7.96 / 12.01` (`nu = 0.1`), not
     grid-converged, so the "approach to the Onsager bound" was a resolution
     artefact. The order/orientation probe, by contrast, IS grid-converged and
     IC-independent (bullet 13). The register keeps only what survives a resolution
     study. Three substantive theorems (adding `excess_majorizes`, the safety
     direction that the excess majorises the critical quantity), axioms exactly
     `[propext, Classical.choice, Quot.sound]`; build green (8741 jobs).
 16. **Cross-system: the order is shared, the orientation is the discriminator**
     (`burgers_zero_order.py`). The same order/orientation probe run on a system
     that *does* form a singularity — viscous Burgers (`2 sin x` IC, `N=512`). It
     shares the finite order of vanishing (`k = 19.4 / 7.8 / 5.0` at
     `nu = 0.1 / 0.02 / 0.004`, decreasing with `nu` exactly as in NS) but flips
     the orientation: `lambda = +15.3 / +16.2 / +17.4 > 0`, REPELLING — the high
     modes pile up at the shock. Resolved Navier-Stokes is ATTRACTING (`lambda < 0`).
     So the one pattern recurs across systems and the two numbers separate them:
     the order is shared, the orientation tells a shock-forming system from a
     purely dissipating one. This sharpens the wall's reading: NS sits on the
      *attracting* side in the resolved range, so any repulsion (and the blowup it
      would signal) must live beyond the resolved range. The Burgers reading is
      itself grid-converged (`burgers_resolution_study.py`: `k = 7.840`,
      `lambda = +16.24` identical to four decimals at `N = 256/512/1024`), so the
      cross-system comparison is rigorous, not a resolution artefact.
 17. **Resolved Navier-Stokes stays attracting under refinement**
      (`ns_resolution_study.py --Ns 64,96`). Pushing the order/orientation probe to
      `N = 96` (from 64) at `nu = 0.1`, fixed `T_max = 3.5`: `lambda = -4.46 -> -4.57`
      and `k = 3.15 -> 3.21`, grid-converged (`|dk|/k = 0.018`,
      `|dlambda|/|lambda| = 0.024`). Nearly three times the original resolution
      still shows no repulsion: the discriminator (16) keeps resolved NS firmly on
      the *attracting* side, so the repelling orientation — and the blowup it would
      signal — is pushed strictly beyond the resolved range. Wall OPEN.
 18. **The discriminator separates singular from regular, not dimensions**
      (`ns2d_zero_order.py`). Third system: 2D Navier-Stokes — the same equation
      family, but a theorem (Ladyzhenskaya) proves global regularity. The probe
      reads ATTRACTING (`lambda = -9.61 / -9.27 / -9.30` at `N = 96/128/160`),
      grid-converged (`|dk|/k = 0.008`, `|dlambda|/|lambda| = 0.004`), exactly like
      resolved 3D NS and unlike Burgers. Across three systems the orientation now
      tracks singular-vs-regular: the sole REPELLING system (Burgers) is the sole
      singularity-former; both NS systems sit on the attracting side, 2D by theorem
      and 3D in the resolved range. So the discriminator (16) has meaning —
      repulsion is the signature of an actual finite-time singularity, and resolved
      NS shows none. Wall OPEN.
 19. **A second singular system confirms the repelling end** (`clm_zero_order.py`).
      The Constantin-Lax-Majda model `d_t w = w H(w)` — a different, nonlocal PDE
      with a *proven* finite-time blowup (Constantin-Lax-Majda 1985), no viscosity —
      reads REPELLING (`lambda = +34.1 / +35.3 / +34.7` at `N = 256/512/1024`), with
      finite order (`k = 1.97 / 2.11 / 2.40`) and blowup detected at
      `t* = 2.44 / 2.20 / 2.09`. So the discriminator now holds across FOUR systems:
      the two independent singularity-formers (Burgers, CLM) both REPEL, the two
      Navier-Stokes systems (2D by theorem, 3D in the resolved range) both ATTRACT.
      The repelling orientation is the signature of a genuine finite-time
      singularity, not of a particular equation or a numerical artefact. Caveat:
      `t*` is grid-dependent (that is what finite-time blowup detection looks like),
      but the orientation and the finite order are consistent across grids. Wall OPEN.
 20. **The wall's logical shape, isolated** (`ContinuationCriterion.lean`). Every
      continuation criterion shares one skeleton: local existence extends while the
      invariant `N` stays bounded, so existence can fail at `T` only if `N` escapes
      every bound on `[0,T)`. Formalised discretely and non-vacuously:
      `exists_upto_of_bounded` (bounded invariant ⟹ the flow reaches every `t ≤ T`)
      and its contrapositive `unbounded_of_first_failure` (a first failure at `T`
      forces `N` to be unbounded — no proposed bound `M` holds anywhere). This is
      the wall in its purest form: sufficiency (bounded ⟹ regular) is classical and
      `OnsagerCriterion.weighted_sum_le` supplies a piece of it; the sole missing
      brick is the boundedness this brick shows is *exactly* what a blowup requires
      to fail. Two substantive theorems, axioms exactly
      `[propext, Classical.choice, Quot.sound]`; build green (8742 jobs). Wall OPEN.
 21. **The orientation reads the wall** (`orientation_vs_invariant.py`). The
      cross-system discriminator (16-19) is tied to the continuation criterion
      (20): in each of four systems the sign of the orientation `lambda` equals the
      sign of `mu = d/dt log`(scaling-critical content). 3D NS `lambda = -3.11`
      with `mu(L3 u) = -0.41`; 2D NS `lambda = -9.27` with `mu(max|omega|) = -0.53`
      (both ATTRACTING, critical norm shrinking); Burgers `lambda = +16.24` with
      `mu(max|u_x|) = +2.39`; CLM `lambda = +34.75` with `mu(max|omega|) = +2.82`
      (both REPELLING, critical content growing). So the orientation is not a
      separate diagnostic: it is the flow's own reading of whether the critical
      invariant escapes its bound — exactly the event
      `ContinuationCriterion.unbounded_of_first_failure` names. Attracting
      (resolved/regular) and repelling (singular) are the two sides of the wall,
      read directly off the flow. Wall OPEN.
 22. **Attracting orbits are bounded** (`StableBounded.lean`). The wall's open half
      is BOUNDEDNESS of the critical invariant; the two shapes of "boundedness for
      free" in the register are now theorems. *Attracting*: a contraction on a
      complete, nonempty metric space has a convergent -- hence bounded -- orbit
      (`attracting_orbit_converges`, `attracting_orbit_bounded`), so "the great
      attractor does not yet repel" is itself a boundedness statement and repulsion
      is the only escape route. This is bullet 21's discriminator at the attracting
      end. *Monotone*: a non-increasing quantity stays below its start
      (`monotone_bounded`), the arithmetic core of the 2D enstrophy Lyapunov shape
      (`dZ/dt <= 0`) that is *not* available in 3D. Three substantive theorems,
      axioms exactly `[propext, Classical.choice, Quot.sound]`; build green (8743
      jobs). Wall OPEN.
 23. **The enstrophy barrier** (`EnstrophyBarrier.lean`). The wall's open half is
      BOUNDEDNESS; the one difference between the 2D interior bound and the 3D
      blow-up-capable regime is the ORDER of the enstrophy increment. *2D*:
      non-increasing (`dZ/dt <= 0`) is bounded by its start (`mono_step_bounded`).
      *3D*: a per-step increment `<= C * Z^2` forces no bound -- the doubling
      schedule `y n = A * 2^n` satisfies it (once `C A >= 1`) yet is unbounded
      (`quadratic_step_unbounded`, `quadratic_no_uniform_bound`). So the wall is
      not a missing estimate of the same shape as the 2D bound: it is exactly the
      gap between a linear (Lyapunov) increment and a quadratic (blow-up-capable)
      one. Four substantive theorems, axioms exactly `[propext, Classical.choice,
      Quot.sound]`; build green (8744 jobs). Wall OPEN.
 24. **The sufficiency loop closes in 2D, cannot start in 3D** (`SufficiencyLoop.lean`).
      Composing the two shapes with the continuation skeleton: a non-increasing
      invariant (2D) is bounded for free (`mono_step_bounded`), and a bounded
      invariant feeds the continuation criterion (`exists_upto_of_bounded`) to give
      existence at every time (`global_exists_of_mono`, bound `M = N 0`). In the 3D
      shape the same engine cannot be started: a quadratic increment admits an
      invariant escaping every bound (`quadratic_criterion_unavailable`), so the
      hypothesis `∀ s ≤ T, N s ≤ M` holds for no `M`. The wall is therefore exactly
      the question of whether the real 3D enstrophy increment is controllable below
      quadratic. Two substantive theorems, axioms exactly `[propext,
      Classical.choice, Quot.sound]`; build green (8745 jobs). Wall OPEN.
 25. **Quantitative continuation: the barrier hierarchy by order**
      (`QuantitativeContinuation.lean`). How much growth the invariant may have and
      still be controlled on a finite window is set by the ORDER of its increment.
      Order 0 (`N_{n+1} <= N_n + C`) is linear (`linear_bound`); order 1
      (`N_{n+1} <= (1+C) N_n`) is geometric (`geometric_bound`); order 2 has no
      uniform bound (the 3D shape). `barrier_hierarchy` states all three at once.
      The payoff is `exists_upto_of_geometric`: an order-one increment yields the
      computable window bound `(1+C)^T N_0`, which feeds the continuation criterion
      to give existence up to `T` -- so a controlled growth rate (not boundedness
      outright) already buys any finite window. This is the discrete shadow of the
      classical double-log continuation bounds. Four substantive theorems, axioms
      exactly `[propext, Classical.choice, Quot.sound]`; build green (8746 jobs).
      Wall OPEN.
 26. **Orientation decides boundedness: the two organizing numbers meet**
      (`OrientationBoundedness.lean`). The register has two organizing numbers --
      the ORDER of the increment (bullets 23/25) and the ORIENTATION `log |L|`
      (bullets 17/21). This brick joins them for the exact geometric orbit
      `N n = r^n A`: `r <= 1` (attracting/marginal) is bounded by its start
      (`geometric_bounded_of_le_one`); `r > 1` (repelling) escapes every bound
      (`geometric_unbounded_of_one_lt`); hence `bounded <=> r <= 1`
      (`geometric_bounded_iff`) and the SIGN of `log r` reads the wall
      (`orientation_decides_boundedness`: `0 < log r` iff unbounded, `log r <= 0`
      iff bounded). With `r = |L|` this IS the `GreatAttractor` orientation
      (`repelling_iff_unbounded`), so the on-flow orientation bridge is now a
      theorem: direction = orientation = which side of the wall. Five substantive
      theorems, axioms exactly `[propext, Classical.choice, Quot.sound]`; build
      green (8747 jobs). Wall OPEN.
 27. **Full-length resolution: the attracting reading is grid-converged at `T=8`**
      (`ns_resolution_study.py --Ns 32,48,64 --Tmax 8`). The prior finest grid
      (N=96) ran only to `T=3.5`; re-running the order/orientation probe for the
      FULL probe length at three resolutions gives `k = 4.140/4.061/3.955`,
      `lambda = -3.753/-3.714/-3.644` (`nu = 0.1`), with `48 -> 64` convergence
      `|dk|/k = 0.027`, `|dlambda|/|lambda| = 0.019` -- CONVERGED and ATTRACTING.
      The residual `N -> infinity` trend reproduces the `nu -> 0` direction
      (refining lowers `k`, raises `lambda` toward `0`): resolution behaves like
      lowering viscosity, moving toward the unresolved repelling range without
      reaching it. So "the great attractor does not repel" holds at full run length,
      not just the transient. Diagnostic only; wall OPEN.
 28. **Theory of everything: the register is one theorem over two numbers**
      (`TheoryOfEverything.lean`). A `Register` is (order `a`, orientation `r`).
      The two reduction lemmas are `order_sets_rung`
      (`criticalSmoothness a p = sCrit p + (1-a)`) and `orientation_sets_side`
      (`bounded ↔ r ≤ 1`). The single theorem `theoryOfEverything` is the whole
      register as a conjunction: order sets the rung; the homogeneous norm is
      scale-free exactly on that family; `gnExponent + sCrit = 1/2`; orientation
      sets the side; the SIGN of `log r` (the `GreatAttractor` Lyapunov sign)
      reads that side; the barrier hierarchy holds (order ≤ 1 controlled, order 2
      not); and the sufficiency loop closes (`global_exists_of_mono`). Every conjunct
      cites an earlier committed brick -- the capstone adds no analytic content, it
      makes the register citable as ONE theorem. Axioms exactly
      `[propext, Classical.choice, Quot.sound]`; build green (8748 jobs). Wall OPEN.
 29. **Emergent time: change is transfer, time is the count** (`EmergentTime.lean`).
      (1) A `Reservoir` of two energies with a `transfer` (remove from one, add to
      the other): `transfer_conserves_total` (a change moves energy, never creates it:
      decay is removal, growth is transfer -- one move, two readings); `transfer_iterate`
      and `state_determined_by_count` (the state is a function of the transfer COUNT
      alone: no clock exists, time is the count). (2) `sqrt_self_consistency`
      (`sqrt b = a (a>0) => b / a = a`): the squaring relation is its own fixed ratio,
      the self-consistency of the order-2 step. (3) dimension-parameter arithmetic
      `sCritN d p = d/p - 1` (`sCritN_three` recovers the ladder at `d=3`),
      `scaleFreeN_iff`, and `sCritN_mono` (higher dimension => higher change cost).
      Axioms exactly `[propext, Classical.choice, Quot.sound]`. Structural reframing /
      toy model, NOT a PDE claim; build green (8749 jobs). Wall OPEN.
 30. **Explicit claims register** (`EXPLICIT_CLAIMS.md` + `ExplicitClaims.lean`).
      The shared insight is distilled into 14 falsifiable claim cards, each tagged
      Theorem / Formal / Empirical / Conjecture with evidence, a falsifier, and a
      named missing entity. The arithmetic cores are machine-checked
      (`morrey_threshold` `0 < 1 - d/2 ↔ d < 2`; `physical_embedding_gap`
      `1 - 3/2 = -1/2`; `extra_power_strengthens_above_unit`
      `z ≤ z^(1+ε) ↔ 1 ≤ z`; `mean_le_dimMixture` `(d+e)/2 ≤ max d e`). The open
      card C5 (boundedness of `‖u‖_{B^{-1}_{∞,∞}}`) and empirical C9/C10 carry
      citations for their missing entities (Cheskidov–Shvydkoy 2010; Ri
      arXiv:2307.11312 unrefereed; Tao 2016/2021; Beale–Kato–Majda 1984;
      Constantin–Fefferman 1993; Deng–Hou–Yu 2015; Adams–Hedberg 1996; Frisch 1995).
      Axioms exactly `[propext, Classical.choice, Quot.sound]`; build green
      (8750 jobs). No Millennium result.
 31. **The orientation law: growth rate equals orientation** (`OrientationLaw.lean`).
      Card C10's model core as a theorem. On the geometric orbit `N n = r^n A` the
      discrete growth rate `mu(n) = log N(n+1) - log N(n)` is constant and EQUALS the
      orientation `lambda = log r` (`logGrowth_geometric`), so `sign(mu) = sign(lambda)`
      (`sign_match`) and that shared sign reads the wall (`orientation_reads_wall`:
      `mu > 0` iff unbounded). On the model the growth rate of the critical content
      and the orientation are the same number, and it is the wall's own reading; the
      analytic residue (that this survives the real flow, `orientation_vs_invariant.py`)
      stays EMPIRICAL/OPEN. Axioms exactly `[propext, Classical.choice, Quot.sound]`;
      build green (8751 jobs).
 32. **Six-system orientation bridge** (`orientation_vs_invariant.py`). Card C10's
      empirical half extended from four to six systems: added 3D Euler (inviscid
      nonlinear, `max|omega|`) and a linear heat dissipation control. All six match
      `sign(lambda) = sign(mu)`, balanced 3 repelling / 3 attracting (3D NS `-3.11/-0.41`;
      2D NS `-9.27/-0.53`; 3D Euler `+1.72/+0.16`; 1D Burgers `+16.24/+2.39`; CLM
      `+34.75/+2.82`; heat `-66.74/-0.13`). The inviscid Euler case is REPELLING, so it
      is the dissipation -- not the nonlinearity -- that makes NS attracting; the heat
      control is the pure attracting limit. `EXIT=0`; diagnostic only; wall OPEN.
 33. **The orientation law, generalized** (`OrientationLaw.lean`). Card C10's model core
      now holds off the geometric orbit. For ANY positive sequence: the growth rate is
      the log of the relative increment (`logGrowth_of_ratio_eq`); positive growth ⟺
      strict increase (`logGrowth_pos_iff`); non-positive growth at every step forces
      boundedness (`bounded_of_nonpos_logGrowth`), so unbounded content forces a strictly
      positive growth rate somewhere (`exists_pos_logGrowth_of_unbounded`). The geometric
      orbit is a corollary (constant relative increment ⇒ `mu = log r`,
      `logGrowth_geometric`). The wall's repelling side is read by the sign of the growth
      rate alone, no self-similarity assumed. It also carries the DISCRETE BKM INTEGRAL:
      `log_eq_sum_logGrowth` (log of content = `log(N 0)` + running sum of growth rates,
      telescoping), `bounded_of_bounded_sum_logGrowth` (bounded growth-sum ⇒ bounded
      content), `unbounded_sum_of_unbounded` (unbounded content ⇒ diverging growth-sum) --
      no blow-up without a diverging critical-content integral. The CONTINUOUS analogue
      is proved too: `contLogGrowth_integral` (`int_0^T g = log X T - log X 0`, Mathlib
      FTC) and `continuous_content_bounded` (bounded `int_0^T g` => `X T <= X 0 * exp B`),
      so the residue is exactly the NS-specific bound on `g = d/dt log X`. The continuous residue
      (that `mu = lambda` survives the real flow) is now an explicit OPEN proposition,
      card **C10-open** in `EXPLICIT_CLAIMS.md`; missing entity: an analytic lower bound
      on `d/dt log ‖u‖` (BKM 1984; Constantin–Fefferman 1993; Deng–Hou–Yu 2015). Axioms
      exactly `[propext, Classical.choice, Quot.sound]`; build green (8751 jobs). Wall OPEN.
 34. **Dissipative flows are attracting** (`DissipativeFlow.lean`). Card C10's PROVABLE
      (energy) face as a theorem. `logGrowth_deriv` (the log-growth rate of a positive
      content is `m / X t`, the content's relative rate of change); `logGrowth_nonpos_of_dissipative`
      (content positive, `m <= 0` => `d/dt log X <= 0`); capstone `content_le_initial_of_dissipative`
      (a continuous `g <= 0` on `[0, T]` => `X T <= X 0`) built on `continuous_content_bounded`
      via interval-integral monotonicity. Scope, stated honestly: this is the L^2-energy face
      (the NS energy identity `dE/dt = -nu ‖∇u‖^2 <= 0` is the motivating instance); the
      scaling-critical content has NO such inner-product identity -- that absence is exactly
      card C10-open. Axioms exactly `[propext, Classical.choice, Quot.sound]`; length
      certificate axiom-free; build green (8752 jobs). Wall OPEN.
 35. **Fractional-NS sweep: the orientation holds one-parameter in the dissipation order**
      (`orientation_vs_fractional_s.py`). Card C10 strengthened from a single PDE to the
      family `u_t + u·∇u = -nu (-Δ)^s u`. Because the dissipation order sets the scaling,
      the critical regularity index is `s`-dependent: the invariant scaling
      `u_lambda = lambda^{2s-1} u(lambda x, lambda^{2s} t)` makes `H^sigma` critical exactly at
      `sigma = 5/2 - 2s` (`sigma = 1/2`, the classical NS critical index, when `s = 1`). Over
      the `s`-correct spectral critical content `‖u‖_{H^sigma}^2 = Σ_k |k|^{2 sigma} E(k)`, the
      on-flow orientation matches at every order: `s = 1.0` `-3.15 / -0.63`; `s = 0.75`
      `-1.29 / -0.67`; `s = 0.5` `-0.30 / -0.56` -- all attracting, `sign(lambda) = sign(mu)`.
      `|lambda|` shrinks monotonically `3.15 -> 1.29 -> 0.30` as dissipation weakens, i.e. the
      flow drifts toward the inviscid/repelling regime while remaining attracted. Window
      caveat: `lambda` is the sampled slope of `log(Z_high/Z_low)`; with weak high-k
      dissipation the ratio first rises (a transient high-k enstrophy pile-up) and only later
      decays, so a SHORT window (`T ≈ 2.5`) reports a spurious `lambda > 0` at `s = 0.5`; the
      sweep is run over the full relaxation window (`T = 6`). `EXIT=0`, artifact
      `data/orientation_vs_fractional_s.json` (untracked). Diagnostic only; wall OPEN.
 36. **The wall is one inequality** (`RegularityReduction.lean`). Packages the two
      `OrientationLaw` facts into the wall statement itself. With `X` the critical content
      and `g = d/dt log X`, the continuous BKM integral gives `X T = X 0 * exp (int_0^T g)`.
      Hence `content_le_exp_of_integral_le` (an integral bound `int_0^T g <= B` forces
      `X T <= X 0 * exp B`); `regularity_reduced_to_integral` (if `int_0^T g` is bounded
      UNIFORMLY in `T` then `X` is bounded uniformly in `T`); the contrapositive
      `integral_unbounded_of_content_unbounded` (unbounded content => unbounded integral);
      and the CONVERSE `integral_le_of_content_le` (bounded content => `int_0^T g` is
      bounded). The two directions give the wall as an EQUIVALENCE
      `regularity_iff_integral_bounded`: content bounded iff the critical-content integral
      is bounded. So the ENTIRE wall is the single analytic question: is `int_0^T d/dt log X` bounded
      along the real flow? The discrete analogue is already `OrientationLaw`; the residue
      is exactly the NS-specific lower bound on `g` (Beale–Kato–Majda 1984;
      Constantin–Fefferman 1993). Axioms exactly `[propext, Classical.choice, Quot.sound]`;
      `regularityReductionFacts_length = 5` axiom-free; build green (8753 jobs). Wall OPEN.
 37. **The margin: the boundary of the standard regime** (`fractional_margin_sweep.py`).
      Reads the late-window orientation (`t >= T/2`, to avoid the early high-k pile-up) over
      `(-Δ)^s`, against the `s`-correct critical Sobolev content `H^{5/2 - 2s}`. The
      orientation crosses zero at the marginal dissipation order `s* = 0.258`, and the
      scaling gap is LINEAR in the order: `|lambda| ~ |s - s*|^beta` with `beta = 1.19`.
      At fixed `s = 0.40` the boundary in viscosity is `nu* = 0.049`, gap exponent
      `gamma = 1.03`. At every order `s` the critical-content rate is still negative even
      where the orientation has flipped repelling (at the deepest probed `s = 0.20`,
      `mu = -0.20`): the orientation LEADS the wall. So standard NS (`s = 1`) sits with a
      finite, healthy margin (`lambda = -3.15`, `nu >> nu*`), and the wall opens only in the
      deeply supercritical regime `s < s*`. Diagnostic only; wall OPEN.
  38. **The margin is not a band artifact** (`fractional_margin_universality.py`).
      Re-locates `s*` across the high/low band split `K0 in {4, 6, 8}` and across a
      different initial condition (seed `1`), at fixed window `T = 5`. Found
      `s* = 0.283 (K0=4)`, `0.300 (K0=6)`, `0.282 (K0=8)`, `0.320 (seed=1)`: overall
      spread `0.037`, so `s*` does NOT track the arbitrary band split (K0-spread `0.018`)
      and moves only mildly with the IC (`0.020`). The standard-regime boundary is thus
      not an artifact of the band split or the seed. Diagnostic only; wall OPEN.
  39. **...and the margin is a shrinking TRANSIENT (no well-resolved critical order)**
      (`fractional_margin_window.py`, `fractional_margin_resolution.py`).
      Locates `s*` by bisection on the order for windows `T = 4, 6, 8, 10, 12`
      (`K0 = 6`, seed `0`, `N = 32`): `s* = 0.355, 0.259, 0.207, 0.176, 0.152`. Over
      `T <= 12` this fits a clean algebraic law `s*(T) = 0.055 + 1.21/T` (rms `0.002`),
      which predicts `s*(T=5) = 0.297`, matching the independent `T = 5` re-location
      `0.300`. At `T = 16`, `N = 32` the crossing is GONE (`lambda < 0` for every
      `s >= 0.01`, down to the numerical-damping floor), but the resolution check shows
      this "vanish" is PARTLY a numerical floor: at `N = 48`, `T = 16` the crossing
      PERSISTS at `s* ~= 0.012` (`lambda(0.01) = +0.001`, `lambda(0.02) = -0.013`).
      The honest reading: `s*(T)` collapses STEEPLY with `T` (`0.36 -> O(0.01)` over
      `T = 4..16`) toward a small value, and whether the limit is exactly `0` is
      resolution-limited at small `s`. So there is no WELL-RESOLVED positive critical
      order; the `lambda > 0` regime is a finite-window TRANSIENT of the high-k
      pile-up, not a sharp regime boundary. A resolution check at `T = 6` gives
      `s* = 0.259 (N=32)` vs `0.265 (N=48)` (agreement `0.006`), so the intermediate-`T`
      values are resolution-stable. Diagnostic only; wall OPEN.
  40. **...and the classical sufficiency direction is now formal too**
      (`SerrinSufficiency.lean`).  `RegularityReduction.lean` gave the wall as an
      equivalence (content bounded iff `int_0^T g` bounded).  The other half of
      Prodi-Serrin -- that a finite *supercritical control* is sufficient -- is added
      in the register's `(X, g)` abstraction: `content_le_of_growth_le_weight` (a
      log-growth rate dominated by a weight of finite action gives
      `X T <= X 0 * exp (R M)`) and `bounded_on_of_serrinAction` (a finite such control
      on every `[0, T]` forbids finite-time blow-up).  The supercriticality is named by
      the Serrin-margin arithmetic `serrinMargin p q = 1 - (2/q + 3/p)` (positive iff
      strictly supercritical; `serrinMargin_eq_neg_ladder` shows a positive margin is
      exactly "above the critical rung" `sCrit`).  Axioms exactly
      `[propext, Classical.choice, Quot.sound]`; length certificate axiom-free.  So the
      register now carries BOTH halves -- a sufficient control and the equivalence --
      and the open residue is exactly the NS-specific *existence* of the control on the
      real flow.  Wall OPEN.
  41. **The margin recurs in a second, shock-forming family** (`fractional_burgers_margin.py`).
      The order/orientation margin above was located on Navier-Stokes.  Running the
      *identical* probe on fractional Burgers `u_t + u u_x = -nu (-∂_xx)^s u` (1D,
      spectral, seed-averaged over 4 ICs) finds a second system with the SAME structure
      and the SAME window dependence: a critical dissipation order separating repelling
      (weak dissipation) from attracting (strong), shrinking as the window grows --
      `s* = 1.51 / 0.35 / 0.27 / 0.22` at `T = 3 / 5 / 8 / 12`, fit `s*(T) = 0.134 +
      1.072/T` (`T >= 5`), next to the NS `0.055 + 1.206/T`.  So the order/orientation
      margin is a property of the class of fractionally-dissipated systems, not of NS
      alone: the recursion recurs across a qualitatively different (shock-forming)
      family.  Noisier than NS (seed spread `~0.5` near the crossing at `N = 256`);
      only the seed-averaged trend is quoted.  A grid/timestep resolution check (`res`
      mode) shows the crossing is resolution-stable once the grid is fine enough:
      at `T = 8`, `s* = 0.288 (N=256) / 0.212 (N=512) / 0.213 (N=768)` -- N=512 and
      N=768 agree to `0.001`, so N=256 is biased `~0.08` high but the margin is not a
      finite-grid artifact.  The converged `window512` mode re-runs the whole table at
      `N = 512, dt = 2.5e-4`: `s* = 1.457 / 0.299 / 0.228 / 0.213` at `T = 3 / 5 / 8 / 12`,
      fit `s*(T) = 0.143 + 0.764/T` (`T >= 5`).  So the shrinking law survives grid
      refinement and its extrapolated limit `s*(inf) ~ 0.14` is grid-stable (same
      intercept as N=256, smaller slope).  Diagnostic only; wall OPEN.
  42. **The margin is a unique crossing, and the method barrier is a diagonal**
      (`MarginCrossing.lean`, `LogicBarrier.lean`).  Two formal bricks close the register's
      bookkeeping.  (a) *Margin:* `MarginCrossing.lean` proves a continuous, strictly
      decreasing `lambda(s)` that is positive on the left and negative on the right has
      exactly one zero (`existsUnique_zero_of_strictAntiOn`), that this zero separates a
      repelling (`lambda > 0`) from an attracting (`lambda < 0`) side (`side_of_crossing`),
      and bundles it (`margin_existsUnique`).  So the marginal order `s*` of the
      order/orientation probe is well-defined the moment `lambda` is antitone in the
      dissipation order `s`; what stays open is the NS-specific *antitonicity*, not the
      arithmetic.  (b) *Method barrier (card C14):* `LogicBarrier.lean` proves Lawvere's
      fixed-point theorem -- a surjection `α → (α → β)` forces every `f : β → β` to have a
      fixed point (`lawvere_fixedpoint`); hence a fixed-point-free `f` forbids any such
      enumeration (`no_surjective_of_no_fixedpoint`), no type enumerates its own predicates
      (`no_surjective_predicates`, Cantor) and the diagonal predicate escapes every
      enumeration (`diagonal_not_mem_range`).  This is the one skeleton shared by Cantor
      (1891), Gödel's diagonal lemma (1931), and Turing's halting problem (1936) -- the
      abstract form of C14's method barrier.  Axiom sets: `MarginCrossing` exactly
      `[propext, Classical.choice, Quot.sound]`; `LogicBarrier` axiom-FREE (stronger).  The
      capstone `TheoryOfEverything.method_and_margin_barriers` attaches both to the two
      organising numbers.  No Millennium problem is touched; the walls stay OPEN.
  43. **The margin recurs in a third family, but the shrinking law does not**
      (`fractional_clm_margin.py`).  Running the identical probe on fractional CLM
      `d_t w = w H(w) - nu (-∂_xx)^s w` -- a PROVEN-blowup family (Constantin-Lax-Majda
      1985) -- finds a third system with a critical dissipation order: repelling (small
      `s`, the CLM blowup regime) below the boundary, attracting above.  At `T = 3`:
      `lambda = 34` at `s = 0.1`, `+2.2` at `s = 2.5`, `-0.05` at `s = 3.0`, and the
      crossing near `s* ~ 2.7-3.0` is resolution-stable (`N = 256` vs `N = 512`
      agree: `lambda(2.0) ~ +3.95`, `lambda(3.0) ~ -0.05` at both; a third grid `N = 1024`
      gives `lambda(2.0) = +3.95`, `lambda(3.0) = -0.02`, so the sign flip between `2.0`
      and `3.0` is grid-robust).  BUT its window dependence is
      NOT the clean shrinking transient of NS / fractional Burgers: `s* ~ 2.66 / 2.70 /
      2.71` at `T = 2 / 3 / 4` (a stable threshold, no shrink), and beyond `s ~ 2.5` the
      orientation hovers inside the noise floor (`|lambda| <~ 0.05`) over a broad band
      `s ~ 2.5..5.5` at every grid -- so at `T = 6` the first sign change jumps out to
      `~5.4`.  So the
      *existence* of an order/orientation margin recurs across three fractionally-
      dissipated families, but the *shrinking-transient law* is specific to the
      NS/Burgers family, not universal.  Diagnostic only; wall OPEN.
  44. **The margin exists as a FIRST crossing -- monotonicity not needed**
      (`FirstCrossing.lean`).  Bullet 42's uniqueness theorem needs `lambda` antitone, but
      the third family shows that hypothesis can FAIL (bullet 43).  This brick keeps the
      weakest hypothesis that still yields a margin: for any `Continuous f` on `a ≤ b` with
      `0 < f a` and `f b < 0`, the set `{x ∈ [a,b] : f x ≤ 0}` is closed and bounded below,
      so it has a least element `c`; `c` is an interior zero with `f > 0` strictly on
      `[a,c)` (`exists_first_zero`), and `c` is the FIRST zero -- no earlier zero exists
      (`margin_exists_firstCrossing`).  So a margin EXISTS whenever the orientation merely
      changes sign; uniqueness is the extra content carried by NS / fractional Burgers.
      Axioms exactly `[propext, Classical.choice, Quot.sound]`; length certificate
      axiom-free.  The capstone `method_and_margin_barriers` now bundles all three: margin
      existence always, margin uniqueness under antitonicity, and the diagonal.  No
      Millennium problem touched; wall OPEN.
  45. **Every claim card is now traceable to its artifact, and the links are machine-checked**
      (`CLAIM_TRACEABILITY.md`).  The card register (`EXPLICIT_CLAIMS.md`) said what each
      card *is*; it did not guarantee that the Lean module or experiment it quotes
      actually exists.  `CLAIM_TRACEABILITY.md` joins them: each card (C1 … C14, C10-open)
      → its type → the exact `PunoCalculus.<File>` module and the declarations it quotes
      → the numerical script(s) supporting its empirical half → the literature anchoring
      its missing entity.  The links are not prose: the checker
      `test_claim_traceability.py` asserts (i) each card heading is present in the claims
      register, (ii) every named Lean module exists and is imported by the library root
      `PunoCalculus.lean` (so `lake build PunoCalculus` really compiles it), (iii) every
      quoted identifier is declared in that module, (iv) every named experiment exists,
      and (v) the map references every card, module and script -- so map, register and
      test cannot drift.  A separate `#check` probe confirmed that all quoted identifiers
      *resolve* (type-check) against `PunoCalculus`, not merely appear.  `pytest` framework
      validation green (769 tests, 1 skip).  No new mathematical content -- a bookkeeping
      brick that makes the register auditable; wall OPEN.
  46. **The register now has an external axis, linked family-by-family to `openai/math`**
      (`EXTERNAL_CORPORA_CROSSWALK.md`).  `CLAIM_TRACEABILITY.md` joins our cards to our
      artifacts; the crosswalk joins our *modules* to the result families of the public
      OpenAI Mathematics collection (`https://github.com/openai/math`, 719 manuscripts /
      372 families, announced 2026-10-06).  The overlaps are real: the C1--C10 wall sits
      beside family **376** (universal computation in *forced* Navier--Stokes -- a Turing
      machine halts iff a designated fluid particle reaches a fixed region, at fixed
      positive computable viscosity), and C14's diagonal engine sits beside the
      fixed-point / undecidability families **206 / 242 / 328 / 314**; `BSD`/`Hodge`/
      `MassGap`/`PvsNP` sit beside **002+006 / 032 / 215 / 102+105+106+274**.  The rule is
      **adjacency, not equivalence**: our modules are numerical certificates that each
      state their own non-settlement, and the external family results are *claimed* by an
      unreleased model and independently unchecked -- so neither side's status transfers.
      In particular family **376** is the *forced* system and does not settle our
      *unforced* C3 / C10-open obligation.  Links pinned offline by
       `test_external_crosswalk.py` (modules exist, are imported by the library root, and
       every quoted family number is present).  No new mathematical content; wall OPEN.
  47. **The origin is machine-checked: nothing is the universal link** (`ZeroLink.lean`,
       card C15).  `Empty` (cardinality `0`) is the *initial object* of `Type` -- into
       every type `α` there is an arrow `Empty → α` and it is **unique**
       (`empty_unique_arrow`); dually `PUnit` is terminal.  Under `+` (coproduct) `0` is
       the identity, under `×` (product) it is absorbing -- `0 + a = a`, `0 * a = 0`,
       rebuilt with sets (`emptySumEquiv`, `prodEmptyEquiv`); initiality is classified
       exactly as `IsEmpty` and terminality as `Subsingleton`.  This is the *structural*
       reading of the register's own 0/0 doctrine (`Removable`, `ZeroZero`,
       `ZeroFixedPoint`): an initial arrow **exists** and is **unique**, exactly as a
       removable 0/0 has an existing, definite value.  The capstone `zero_links_all`
       bundles it (axioms `⊆ [Quot.sound]`, build green).  It is *not* a zero object
       claim: in `Type` the initial object is `Empty` and the terminal object is `PUnit`,
       which are distinct -- the categorical zero object (initial ∧ terminal) needs an
       Ab-enriched category such as modules, and is the named next micro-step.  No
       Millennium problem touched; wall OPEN.
  48. **The zero object completes the link: one object is origin and target**
       (`ZeroObject.lean`, card C16).  Bullet 47 named the next micro-step -- an object
       that is *both* initial and terminal.  This brick delivers it in the category
       where it exists.  Abstractly (`initial_link`, `terminal_link`): a (co)initial
       object links every object by a **unique** arrow, so `zero_links_both_ways` says a
       zero object `Z` is the source of a unique `Z ⟶ Y` into *every* `Y` **and** the
       target of a unique `Y ⟶ Z` from *every* `Y` -- the two directions `Type` splits
       between `Empty` and `PUnit`, joined in one object.  `zero_unique_up_to_iso`: any
       two zero objects are isomorphic.  Concretely (`ModuleCat R`): the module category
       has a zero object (`modules_haveZeroObject`, from `ModuleCat.instHasZeroObject`),
       it exists as an object (`modules_exists_zeroObject`), and it links every module
       both ways (`modules_zero_links`).  So "zero completes the link between all forms"
       is literally true *within one object* exactly when the category has a zero
       object -- and `Type` does not (bullet 47), which is why the two bricks are both
       needed.  Axioms `⊆ [propext, Classical.choice, Quot.sound]`; length certificate
       axiom-free.  `lake build PunoCalculus.ZeroObject` green.  No Millennium problem
       touched; wall OPEN.
  49. **The 0/0 and the initial arrow are one schema: removability is existence +
       uniqueness** (`RemovableValue.lean`, card C17).  Bullets 47-48 made the
       structural face of "zero"; this brick joins it to the *analytic* face.
       `Removable` proves the existence half of the 0/0 doctrine (a shared linear
       factor gives a punctured limit); `ZeroLink` proves the structural half (the
       initial arrow is a `∃!`).  `IsRemovableValue f a L` is `Tendsto f (𝓝[≠] a)
       (𝓝 L)`; `removable_value_unique` shows it is unique when it exists (`ℝ` is
       Hausdorff), so the removable value is a genuine "exactly one".  The schema is
       isolated in `existsUnique_iff_exists_and_unique` (`∃!` = existence +
       uniqueness for any predicate): `removable_exists_unique` feeds it the canonical
       0/0 `(x-a)·g(x)/(x-a)` (value `g a`) and `initial_arrow_schema` feeds it
       `ZeroLink.empty_unique_arrow` -- the *same* lemma yields both.  So
       "removability is existence + uniqueness of a canonical extension"
       (`removable_value_bridge`) and "the initial object is existence + uniqueness of
       an arrow" are one statement; `extension_unique` (a continuous extension of a
       punctured map is unique) is its analytic form.  Axioms
       `⊆ [propext, Classical.choice, Quot.sound]` (`existsUnique_iff_...` and the
        length certificate axiom-free).  `lake build PunoCalculus.RemovableValue` green.
        No Millennium problem touched; wall OPEN.
  50. **Order of vanishing is a graded index: the number of zeros is the degree**
        (`VanishOrder.lean`, card C18).  `ZeroFixedPoint` counts the zeros of a 0/0
        (`zero_count_removable` / `under` / `over`); this brick turns that count into a
        **grade**.  Level `k` of the vanishing filtration is `VanishesToOrder k f x₀`:
        `f` factors as `(· - x₀)^k · g` with `g` continuous at `x₀`.  The filtration is
        **decreasing** (`vanishes_succ_imp`, and `vanishes_antitone`: `k ≤ m` gives
        `F m ⊆ F k` -- one more zero is strictly more restrictive), and -- the grade
        itself -- dividing out one zero lowers the level by exactly one:
        `vanishes_shift` is `F (k+1) f ↔ F k (divideOut x₀ f)` where
        `divideOut x₀ f = f / (· - x₀)`.  Exact order `k` is `HasGrade k f x₀`
        (level `k` but not level `k+1`); the canonical `(· - x₀)^k · h` with `h x₀ ≠ 0`
        sits at exact grade `k` (`hasGrade_canonical`), the exact grade shifts by one
        under `divideOut` (`hasGrade_shift`), and it is well-defined
        (`grade_unique`: `HasGrade k → HasGrade m → k = m`).  So "it scales itself on how
        many zeros it has" is a statement about one `ℕ`-grading, and it completes the
        scaling story of `GreatAttractor` (`criticalSmoothness_shift_order`: each extra
        zero buys one order of smoothness).  Axioms
        `⊆ [propext, Classical.choice, Quot.sound]`; the length certificate is
        axiom-free.  `lake build PunoCalculus.VanishOrder` green.  No Millennium problem
        touched; wall OPEN.

   51. **The mechanism register closes: Probe, Vanishing Rate, Index, and the anti-class**
         (`ZeroProbe.lean` C19, `ZeroValuation.lean` C20, `ZeroIndex.lean` C21,
         `ZeroMechanisms.lean` C22).  `THE_0_OVER_0_ATLAS.md` classifies a *removable* 0/0
         into five mechanisms; this bullet formalises the three with clean analytic /
         algebraic content and, crucially, the **amendment** -- the classification covers
         only the removable ones.  (i) **Probe**: if `f =ᶠ[𝓝[≠] x₀] g` and the
         denominator is nonzero off the point, the ratio resolves to `1`
         (`probe_identity`; `f/f ↦ 1` via `probe_self`); the probe value is unique
         (`probe_value_unique`) and is an `IsRemovableValue` (`probe_is_removable`).
         (ii) **Vanishing Rate**: the *filtration* grade of C18 is **not** additive
         (`|·|`,`|·|` sit at grade `0`, their product at grade `2`), so the mechanism
         uses the residue order `HasOrder k f x₀` (`f/(· - x₀)^k ↦` a nonzero `c`),
         which **is** a valuation: additive under products (`hasOrder_mul`), scale
         `n·` under powers (`hasOrder_pow`), well-defined (`hasOrder_unique`,
         `hasOrder_lt_imp_not`), realised by the canonical `(· - x₀)^n·h`
         (`hasOrder_canonical`).  (iii) **Index**: the root multiplicity
         `Index a p = p.rootMultiplicity a` is additive under products
         (`index_additive`), is `1` at a simple root (`index_X_sub_C_self`), exactly `n`
         on `(X - a)^n` (`index_pow_self`) and on `c·(X - a)^n` with `c ≠ 0`
         (`index_canonical`).  (iv) **Anti-class**: the genuine 0/0 `|x|/x` (both
         numerator and denominator vanish: `abs_vanish`, `id_vanish`) has **no**
         removable value -- `|x|/x ↦ 1` from the right and `↦ -1` from the left
         (`abs_div_self_tendsto_right` / `_left`), so `1 = -1` (`abs_div_self_no_limit`);
         the anti-class is nonempty (`anti_class_nonempty`) and `mechanisms_close`
         bundles the faces.  Axioms `⊆ [propext, Classical.choice, Quot.sound]`; the
         length certificates axiom-free.  `lake build PunoCalculus.ZeroMechanisms` green.
         No Millennium problem touched; wall OPEN.

   52. **Riemann's removable singularity, in the register's 0/0 schema**
         (`RemovableComplexBridge.lean` C23).  Card C17 proved the register's 0/0
         *schema* over `ℝ` (a punctured limit is unique when it exists) but not
         that any given 0/0 has a limit.  This bullet anchors the schema to a
         genuine, named theorem.  Mathlib's **Riemann removable singularity theorem**
         (`Complex.tendsto_limUnder_of_differentiable_on_punctured_nhds_of_bounded_under`)
         says a function complex-differentiable and bounded on a punctured
         neighbourhood of `c` has a punctured limit; read through the register's
         predicate `IsRemovableValueAt f c L := Tendsto f (𝒩[≠] c) (𝒩 L)` it
         yields **existence** (`removable_value_exists`, value `limUnder (𝒩[≠] c) f`)
         and **uniqueness** (`removable_value_unique`), i.e. the same `∃!` schema as
         `RemovableValue.removable_exists_unique` now over `ℂ`
         (`exists_unique_removable_value`).  The **coincidence**
         `limUnder_eq_of_isRemovableValue` records that mathlib's `limUnder` *is* the
         removable value, and `canonical_zero_over_zero` re-proves the concrete
         `(z-c)*g(z)/(z-c) ↦ g c` on `ℂ`.  Axioms
         `⊆ [propext, Classical.choice, Quot.sound]`; the length certificate
         axiom-free.  `lake build PunoCalculus.RemovableComplexBridge` green.
         No Millennium problem touched; wall OPEN.

## Sources for the missing brick (scaling-critical control)

The invariant chain `L^3 ⊂ Ḃ^{-1+3/p}_{p,∞} ⊂ BMO^{-1} ⊂ Ḃ^{-1}_{∞,∞}` and its endpoint theory: Prodi (1959), Serrin (1962), Ladyzhenskaya (endpoint sufficiency `L^p_t L^q_x`, `2/q + 3/p <= 1`); Escauriaza-Seregin-Šverák (2003, endpoint `L^∞ L^3`); Koch-Tataru (2001, `BMO^{-1}`); Cheskidov-Shvydkoy (2010, arXiv:0708.3067 — largest critical space `B^{-1}_{∞,∞}`); Bourgain-Pavlović (2008 — norm inflation / ill-posedness in `Ḃ^{-1}_{∞,∞}`); Ri (arXiv:2307.11312, 2023 — claims a positive lower bound on `L^∞(Ḃ^{-1}_{∞,∞})`; single-author, unrefereed — treat as unverified); Tao (2021) plus Feng-He-Wang 2025 (Lorentz) and arXiv:2411.06483 (Besov) — quantitative triple/double/quadruple-log continuation bounds; Grujić (2024, JMFM, "Asymptotic Criticality" — the scaling gap as a derivative order `k -> ∞`). The **missing brick** is BOUNDEDNESS, not sufficiency: a positive margin (`eta > 0`) is classical and sufficient, but proving the invariant norm stays bounded along the flow is exactly what stays open.

## What this is not

It is not a claim that the five problems are one theorem; the Millennium list is
historical curation, not a designed family. It is not a claim about any problem's
truth value. It is a claim about *why the walls stay open*: local theory finished,
critical-scale control missing — and about *where to push*: the next-order term.
