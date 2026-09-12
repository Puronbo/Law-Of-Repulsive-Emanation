# Soliton-Bus Elementary Cellular Automata

This package implements the requested 8-bit elementary cellular automata (ECA) family:

`4, 12, 19, 27, 36, 44, 51, 59, 68, 76, 83, 91, 100, 108, 115, 123, 132, 140, 147, 155, 164, 172, 179, 187, 196, 204, 211, 219, 228, 236, 243, 251`.

The family is the **32-rule twin set**. It contains the 16 bitmask rules whose output window is `f(000)=0, f(001)=0, f(010)=1, f(100)=0` (the remaining four output bits are free), and, for every such rule, its bitwise complement `255−r` whose window is `(1,1,0,1)`. Black and white output are therefore treated symmetrically: `rule 4` and `rule 251`, `rule 12` and `rule 243`, and so on, are color-swapped twins. The family is complement-closed by construction, and this closure, together with the characterization of the window condition, is verified exhaustively over all 256 Wolfram rules by `soliton_ruleset_audit.py`.

The audit is honest about the limits of the family. Adding the 16 complement twins does not manufacture conservation: measured over every binary ring configuration with the background treated as data (exhaustively at ring widths 4 through 12), only rule `204` conserves the total active-bit count; the genuinely conservative rules are exactly `{170, 184, 204, 226, 240}`. The twins are implemented for completeness and symmetry, not because they share rule 204's storage identity.

## Rule-family dynamics and transport equivalence

The family is characterized by measurement, not assumption. Three further certificates are produced by `soliton_ruleset_audit.py`.

First, the soliton-bus engine is checked against a direct reference implementation of the same ghost-zero boundary. For every one of the 32 rules, at widths 4 through 9, ten deterministic probe configurations, and five generations, the engine `SolitonECA.step()` output is byte-for-byte equal to the reference step. Transport over buses therefore alters no rule semantics: the bus network is a delivery mechanism, not a behavior-modifying component.

Second, the complement-twin semantics are verified. For any rule `r`, the twin `255 − r` maps a configuration to the bitwise complement of what `r` maps it to, verified exhaustively over all ring configurations at widths 6 through 8. This is the measured meaning of the phrase "black/white-swapped twins."

Third, the rules are pairwise distinguishable. No two of the 32 family members share identical dynamics: every unordered rule pair diverges already at the first generation, verified by an exhaustive sweep over all ring configurations of width 3 through 5. The distinction is exact, not statistical: distinct 8-bit rules differ on some neighborhood triple, and every triple occurs as a width-3 ring state. The family therefore provides 32 genuinely distinct behaviors rather than duplicates under different names.

Run the rule-family audits and the end-to-end transport check with:

```bash
python soliton_eca/soliton_ruleset_audit.py
python validate_eca_engine.py
```

The conservative set is not a small-ring artifact. `soliton_ruleset_audit.py` certifies `{170, 184, 204, 226, 240}` on rings of width 14 and 16 — over 2^16 = 65,536 configurations per rule — using a vectorized census that is first cross-validated bit-for-bit against the serial path at width 12. The measured set persists at both widths, and no other family rule conserves at either.

## Ruleset structure and behavior

`Soliton-Bus Elementary Cellular Automata` also measures the internal structure and dynamics of the 32-rule family. Two symmetry generators act on every 8-bit rule: complement `C(r) = 255 − r` and left–right reflection `R(r)`. Together they form the group `{id, C, R, C·R}` and partition the family into orbits. The measured census is exact: the family is closed under reflection and under the full group, producing twelve orbits — eight size-2 symmetric pairs (`[4, 251]`, `[19, 236]`, `[36, 219]`, `[51, 204]`, `[76, 179]`, `[91, 164]`, `[108, 147]`, `[123, 132]`) and four size-4 general quadruples — with no CR-antisymmetric rules. Every rule and its complement therefore sit in the same group of four, which is why the black/white twins receive a symmetric treatment in `RULES`.

Dynamically, a deterministic probe ensemble (seeded LCG, high bits, ring width 10, 64 probes, 48 generations) assigns each rule an empirical class, a mean active-bit survival fraction, and a median attractor length (the first repeated state). The census is 16 static, 9 mixing, 5 oscillatory, 1 conservative, and 1 filling rule. Rule `204` is the sole conservative rule — the identity that stores any configuration unchanged (survival 0.5, period 1) — consistent with the audit's finding that only `204` conserves population on rings. The bitmask A-side rules are dissipative (static attractors at low density), while the B-side complement twins reach mixing attractors of length 4 through 20, so the family is not uniformly short-cycled.

Two claims that one might expect are measured and honestly rejected. Because the black/white swap holds only while both inputs agree, the survival of a twin is *not* the complement of its rule's survival over complete trajectories (the relation holds for one generation and then breaks). Likewise, the family does not settle everywhere into length-2 cycles. These negatives are printed as `HONEST_NEGATIVE` rather than asserted into existence.

Run the structural and behavioral audit with:

```bash
python soliton_eca/soliton_ruleset_investigation.py
python validate_ruleset_investigation.py
```

## Exact state-space census

`soliton_ruleset_state_space.py` enumerates the complete functional graph of each of the 32 rules on rings of width 8, 10, and 12 — the full state space of 2^8, 2^10, and 2^12 configurations, respectively. For every (rule, width) pair it counts attractors, the maximum attractor length, the maximum transient depth before an attractor, and whether the map is a bijection. The measured facts, encoded as certificates, are:

- **Permutation pair.** Exactly two family rules are bijections of the state space: `204` (the identity — every state a fixed point, zero transient) and its twin `51` (the black/white swap — every state on a length-2 cycle, zero transient). No other family rule is a permutation.
- **Lap dynamics.** The four rules `{27, 59, 83, 115}` each have a maximum attractor of length exactly `2 × width` at every listed width (two-lap gliders), and `{172, 228}` have a maximum attractor of exactly `width` (one-lap gliders). Rule `147` reaches length 30 at width 10.
- **Stationary census.** Exactly eleven rules — `{4, 12, 36, 68, 76, 132, 140, 196, 204, 219, 236}` — have every attractor a fixed point at all listed widths. These are precisely the quiet, dissipative members of the family usable as stable storage.
- **Honest negatives.** Two plausible claims are measured and rejected: permutations are *not* identical to the conservative set `{204}` (rule `51` is a permutation but preserves nothing), and the A-side rules do not uniformly stay in cycles of length ≤ 2 (rules `44`/`100` reach length 3, and `164`/`172`/`228` reach longer cycles at width ≥ 10).

Run the census and its validator with:

```bash
python soliton_eca/soliton_ruleset_state_space.py
python validate_ruleset_state_space.py
```

## Soliton-twin numerical audit

`soliton_nlse_audit.py` measures the normalized NLSE integration in `soliton_physics.py`, where the fundamental soliton `A(0, t) = sech(t)` has the exact solution `A(z, t) = sech(t) · exp(iz/2)`. Four certificates are measured, not assumed:

- **Energy unitarity:** the lossless symmetric SSFM is unitary half-step by half-step, and the measured relative energy drift stays at machine precision — 1.1e-13 at distances up to 4 soliton lengths.
- **Second-order convergence:** over step sizes 1/25 through 1/400 the power-envelope error decays with a measured log-log slope of exactly 2.00, the signature of the symmetric split-step method.
- **Shape invariance:** the power envelope returns to the starting sech shape at distances 0.5, 1, 2, and 4 with a relative error below 1e-4 (measured 1.4e-5).
- **Phase rotation:** along the pulse body (where |sech| > 0.1) the accumulated phase is `z/2`, matching the exact answer — a circular deviation below 0.02 rad at the soliton length.

Run the audit and its validator with:

```bash
python soliton_eca/soliton_nlse_audit.py
python validate_nlse_audit.py
```

## Bus-transport reliability audit

`soliton_transport_audit.py` asks how the family actually *moves and stores a packet* — a contiguous run of 1..3 active cells — on a width-8/10/12 wire, under the engine's ghost-zero (vacuum) bus and under the periodic ring where the census facts live. All 32 rules are swept over every start offset and every generation up to twice the width.

- **Storage pair.** Exactly two rules have zero reconstitution failures over the entire vacuum-bus grid: `204` (the identity) and **`236`, a second exact-storage rule** — measured to store *every contiguous block of any width* at every interior offset on the vacuum bus. `236` is a stationary A-side twin of the 11-rule stationary set, and this is the first place its block-storage role is made explicit.
- **Lap reconstitution is a ring-maximum fact, not a packet fact.** On rings, the one-lap rules `{172, 228}` and two-lap rules `{27, 59, 83, 115}` have the *maximum* cycle lengths `width` and `2·width`, but not every packet returns at the exact lap generation: rule `27` maps block `11000000` (width 8) to `01000000` after 16 generations, not back to the starting block. The exact-lap claim and its vacuum-bus transfer are measured and rejected.
- **No rigid conveyor.** No family rule other than the identity moves a packet as a rigid body with a constant nonzero displacement per generation; the false candidate is rejected over the full horizon.

Run with:

```bash
python soliton_eca/soliton_transport_audit.py
python validate_transport_audit.py
```

## Behavioral-class stability across widths and densities

`soliton_behavioral_scale.py` re-samples the probe classifier on a 5×3 grid — widths 8/10/12/16/24 and densities 0.1/0.25/0.5 — and finds that the behavioral class is a property of the *observation window*, not of the rule:

- **Faithfulness:** with the investigation's exact probe construction, the width-10/density-0.5 cell reproduces the published census class for all 32 rules.
- **Probe sensitivity:** replacing the LCG high-bit sampler by a threshold Bernoulli sampler at the same density silently flips rule `108` between static and oscillatory at the width-10/density-0.5 cell — the median-period boundary (1 vs 2) is probe-sensitive.
- **Width/density dependence:** rule `76` reads as conservative only at (10, 0.1), a probe-window false positive (the exhaustive audit proves only `204` conserves); the glider rules `27/59/83/91/115` alternate between mixing and oscillatory across cells. Exhaustive audits remain the only certificates.

Run with:

```bash
python soliton_eca/soliton_behavioral_scale.py
python validate_behavioral_scale.py
```

## Ensemble entropy cascade

`soliton_entropy_cascade.py` measures the exact information surviving each rule's application: starting from the uniform ensemble over all 2^12 width-12 states, it pushes the full distribution forward and reports H(t) — Shannon entropy after t generations — exactly, over the complete state space.

- **Lossless pair.** Exactly the permutation pair `{204, 51}` retains all 12 bits at every generation. Rule 204 stores the configuration and rule 51 inverts it; every other rule loses ensemble entropy.
- **No side dominance.** The naive reading "the A-side bitmask twin always retains at least as much as its B-side complement" fails: pair (44, 211) retains 0.53 vs 0.73, and other pairs go the other way.
- **The entropy ladder is slow.** Only rules `36/147/164/219/251` halve the ensemble entropy within 32 generations; most dissipative rules plateau above the half-life line. The retained-entropy floor is the filling twin `251` (≈5e-4).

```bash
python soliton_eca/soliton_entropy_cascade.py
python validate_entropy_cascade.py
```

## Multi-packet crosstalk

`soliton_crosstalk_audit.py` places **two or three packets** (contiguous blocks of 1..3 cells) on the same ghost-zero wire and demands every packet reconstitute bit-exact at every generation up to twice the width.

- **Rule 204 is the unique full multiplexer**: zero crosstalk failures over every multi-packet placement; every other family rule fails some placement (236 fails 128 of them).
- **Rule 236's gap law is exact**: its block-storage extends to multi-block payloads iff no pair of consecutive blocks is separated by exactly one zero. A single zero collapses (`1 0 1` → `111`), while adjacent blocks simply merge into a larger stored block and gaps of two or more zeros persist.

```bash
python soliton_eca/soliton_crosstalk_audit.py
python validate_crosstalk_audit.py
```

## Soliton radiation and purity

`soliton_radiation_audit.py` perturbs the fundamental soliton amplitude `A·sech(t)` and measures the radiated energy (fraction leaving the `|t| ≤ 3` core) after z = 8, plus the integrity of the `iz/2` phase law at z = 1.

- **Fundamental clean** (2e-6 radiation) and the **A = 2 breather also clean** (5.8e-4): the NLSE is integrable, so integer soliton orders are exact solutions that shed no radiation.
- **Non-integer amplitudes radiate macroscopically**: A = 0.5 delocalizes 38% of its energy by z = 8; A = 1.5 sheds 5.6%.
- **Monotonicity is rejected**: "radiation grows with |A−1|" fails — A = 2 radiates ~600× less than A = 1.5 because it is an exact soliton order. Radiation is minimized at the exact orders, not by proximity to A = 1.
- The `iz/2` phase law is exact at A = 1 and strictly the best over the measured amplitudes.

```bash
python soliton_eca/soliton_radiation_audit.py
python validate_radiation_audit.py
```

## Two-soliton interactions

`soliton_interaction_audit.py` propagates pairs of fundamental solitons with initial separation `d` and relative phase `phi` through z = 16 and measures the far-field radiative residue (energy beyond `|t| > 12`), the integrator's energy drift, and the centroid separation before vs after.

- **In-phase pairs bind**: at d = 4 the centroid separation collapses 3.83 → 1.24; at d = 6 it collapses 5.93 → 1.49.
- **π-shifted pairs repel**: at d = 4 the separation grows 4.32 → 11.75; at d = 6: 6.09 → 8.00; measured for d ∈ {4, 6, 10}.
- **Equal-amplitude collisions are clean**: far-field residue ≤ 1e-3 over the whole (d × phi) grid, including the violent d = 4, φ = π case (1.0e-3) — the integrable pair exchanges but sheds nothing.
- **Unequal amplitudes radiate — monotone cleanliness is rejected**: the candidate "an unequal pair collides as cleanly as an equal one" is false; (1.0, 0.5) leaves a 3.2% residue and even (1.0, 0.8) leaves 0.97%, because the sub-fundamental component is dispersive.
- Energy drift is ≤ 2.8e-13 in every run.

```bash
python soliton_eca/soliton_interaction_audit.py
python validate_interaction_audit.py
```

## Pulse confinement on the ghost-zero bus

`soliton_pulse_confinement_audit.py` injects a single active impulse into an all-zero bus and measures the support width (span of active cells) over 2·width generations at widths 8/12/16. This is the ECA analogue of the NLSE confinement-vs-radiation split measured above.

- **Exact bifurcation**: confinement (support ≤ 3 forever) holds for exactly the 16 A-side bitmask rules, whose window fixes `(010)→1, (001)→0, (100)→0, (000)→0` — a lone impulse is a stationary fixed point for the entire half-family.
- **The B-side complement fills instead of confining**: every one of the 16 B-side rules spreads the impulse to the full lattice width at some generation — the analogue of the radiating (non-integer-amplitude) NLSE states.
- **No traveling pulse exists** (candidate rejected): everything that confines is stationary; everything that moves spreads. The family has no bounded-support moving impulse.

```bash
python soliton_eca/soliton_pulse_confinement_audit.py
python validate_pulse_confinement_audit.py
```

## Engine stress at large widths

`soliton_bus_stress_audit.py` runs the soliton-bus engine under load.

- **Bit-exact at scale**: at widths 512/1024/2048 the engine matches the ghost-zero reference for every family rule, every LCG probe, every generation.
- **Approximately linear per-step cost**: step times grow 1.00 → 1.94 → 2.01 as the width doubles 2048 → 4096 → 8192.
- **Deterministic**: identical runs (rule 219, width 977, 50 generations) are byte-identical.
- **Marker-impulse fidelity**: a lone impulse on a zero background at width 4096 survives 30 generations unchanged under rule 204 — the bus neither leaks nor ghosts at scale.

```bash
python soliton_eca/soliton_bus_stress_audit.py
python validate_bus_stress_audit.py
```

## Modulational instability

`soliton_mi_audit.py` seeds a continuous wave `sqrt(P)` (P = 1) with a small periodic perturbation and measures the power gain of the seeded sideband against the analytic curve `g(ω) = 2ω√(P − ω²/4)` of the focusing NLS.

- **The measured gain matches the analytic curve within 7%** over five in-band modes (ratios 1.02–1.07; each exponent is read from the late-time log-linear tail, since a real cosine seed excites both the growing and the decaying quadrature).
- **The instability band is real**: a mode at ω = 1.96 (just below the edge 2√P = 2) amplifies; a mode at ω = 2.16 has exactly zero gain.
- **Peak gain ≈ 2P** at ω ≈ √(2P) = 1.41, matching the analytic band shape sampled on the discrete frequency grid.
- **The soliton is the stability island of the same equation**: the identical seed at k = 8 grows 2200× on the CW background but stays flat (ratio ≈ 0.95) on the fundamental soliton — no flat background, no phase-matched four-wave growth.
- Energy drift stays ≤ 2.4e-13 over every bake-off run.

```bash
python soliton_eca/soliton_mi_audit.py
python validate_mi_audit.py
```

## The nonlinear stage of MI: recurrence, not blowup

`soliton_mi_recurrence_audit.py` propagates the phase-matched
max-gain cosine seed (Ω = √(2P), P = 1) far past the linear stage for
ε ∈ {0.05, 0.10, 0.20, 0.30, 0.45} and certifies the recurrence laws:

- **Crest capped**: every profile's crest stays strictly below the
  algebraic Peregrine bound 3.0000 — the bound the breather hits
  exactly at its maximum. Max measured 2.738 (ε = 0.45). The nonlinear
  MI stage and the breather share the same ceiling.
- **Full recombination**: after the crest each profile relaxes back to
  ≤ 1.5·(1+ε) (trough measured 1.048 → 1.621 across the seeds) — the
  modulation recombines; the NLS analogue of the Fermi–Pasta–Ulam
  recurrence, no blowup.
- **Period shortens**: the first-crest distance strictly decreases with
  seed strength (4.05, 3.35, 2.60, 2.20 for ε = 0.05…0.30): nonlinear
  period shortening as the seed amplitude grows.
- **Honest negative**: the crest does NOT sit at the linear optimum
  2π/g_max = π ≈ 3.14 — measured 4.05 at ε = 0.05. The linear band law
  sets the growth rate, but the nonlinear recurrence is governed by the
  algebraic crest and the amplitude-shifted period.

```bash
python soliton_eca/soliton_mi_recurrence_audit.py
python validate_mi_recurrence_audit.py
```

## The nonlinear stage of MI: the cap's frequency domain

`soliton_mi_frequency_scan_audit.py` scans the seed frequency to map
where the recurrence crest cap actually binds (P = 1, ε = 0.2):

- **The cap is frequency-localized**: the Peregrine bound 3.0000 is
  NOT a global ceiling on MI crests. At the max-gain frequency Ω = √2
  the crest is 2.476; at Ω = 1.0 it is 2.837; at the low in-band
  frequency Ω = 0.5 the nonlinear stage crests at **3.656 — above the
  cap** (HONEST_NEGATIVE for "the cap bounds every MI crest"). The
  round-11 cap result holds near and above the max-gain frequency,
  which is exactly where the algebraic breather form lives; low
  frequencies crest higher because their linear-gain stage stays
  coherent longer before the nonlinear turn-around.
- **Crest grows as the frequency drops**: monotone 2.476 → 2.837 →
  3.656 for Ω ∈ {√2, 1.0, 0.5}.
- **Recurrence survives every frequency**: after its crest each profile
  relaxes to a trough ≤ 1.5·(1+ε) (troughs 0.248, 1.198, 1.197) — the
  deep Ω = 0.5 crest even bottoms to 0.248 (20% of background) before
  recombining. No blowup anywhere on the band.

```bash
python soliton_eca/soliton_mi_frequency_scan_audit.py
python validate_mi_frequency_scan_audit.py
```

## The MI crest across the band: wavelength monotonicity

`soliton_mi_omega_spectrum_audit.py` scans the whole well-posed band
(P = 1, ε = 0.2) from one full cosine wavelength (Ω = 2π/64, the
longest continuous seed the 64-window admits) up to the max-gain
frequency √2::

    Ω     0.098  0.147  0.196  0.295  0.393  0.500  0.589  0.785  1.000  1.414
    crest 4.697  4.539  4.387  4.111  3.889  3.656  3.482  3.143  2.837  2.476
    z_cr  11.70  8.15   6.40   4.65   3.75   3.20   2.95   2.60   2.45   2.60

- **Crest rises monotonically with wavelength**: 2.476 at the
  max-gain frequency → 4.697 at the longest m = 1 seed. The
  low-frequency nonlinear stage overshoots the max-gain one — the
  linear gain rate peaks at √2, but the slow modulations stay coherent
  longer and crest higher.
- **The cap 3.0000 divides the band**: every crest at Ω ≤ 0.785
  exceeds it (3.143 min), every crest at Ω ∈ {1.0, √2} stays below
  (2.837 max). Round 12's single honest-negative becomes a measured
  dividing line.
- **Crest distance grows with wavelength** for Ω ≤ 1.0: 2.45 → 11.70.
  Longer modulations crest later and higher (the amplitude-shot
  companion to round 11's period shortening in ε).
- **Recurrence survives every wavelength**: every profile relaxes to a
  trough ≤ 1.5·(1+ε) after its crest (max trough 0.248); nothing blows
  up at any frequency.
- **Honest negative**: the turn-back toward the constant-wave (DC)
  limit is NOT observed inside the well-posed window — the longest
  m = 1 seed crests highest, so the crest-versus-wavelength peak lies
  below the window's floor, not in it.
- **Grid caveat (round 15)**: the monotonicity law is a statement on
  this sampled grid. A denser probe at Ω = 0.9 shows a secondary local
  crest maximum there (see the phase-diagram section), so the crest
  curve is not globally monotone in Ω.

```bash
python soliton_eca/soliton_mi_omega_spectrum_audit.py
python validate_mi_omega_spectrum_audit.py
```

## The crest's amplitude rule: epsilon and the broken cap

`soliton_mi_amplitude_scan_audit.py` scans the seed strength at two
frequencies (P = 1, ε ∈ {0.05…0.45})::

    Ω = 0.5:  crest   3.228  3.377  3.656  3.961  4.422   (rises in ε)
              z_crest 5.55   4.35   3.20   2.60   2.05    (shortens in ε)
    Ω = 1.0:  crest   2.738  2.757  2.837  2.963  3.229
              z_crest 4.10   3.30   2.45   5.90   7.50

- **The crest rises with ε at every frequency** — the cap-breaking is a
  joint (Ω, ε) statement, not a per-frequency line.
- **Deep band breaks at every amplitude**: at Ω = 0.5 even the weak
  seed ε = 0.05 crests at 3.228 > 3.0000. No amplitude threshold
  exists on the low side.
- **The high side holds for weak seeds**: at Ω = 1.0 the cap binds for
  ε ≤ 0.30 (max 2.963) and the strong seed ε = 0.45 crosses at 3.229 —
  the band-dividing frequency rises with ε.
- **Deep-band period shortening**: z_crest falls 5.55 → 2.05 with ε —
  round 11's shortening law is not confined to the max-gain frequency.
- **Honest negative**: shortening is NOT every-frequency: at Ω = 1.0
  the ε = 0.30/0.45 seeds skip the early turn-around and crest very
  late (5.90, 7.50) — a late-crest regime instead.
- Recurrence survives every (Ω, ε) pair (max trough 1.446).

```bash
python soliton_eca/soliton_mi_amplitude_scan_audit.py
python validate_mi_amplitude_scan_audit.py
```

## The crest's modal structure: pump depletion, then carrier recovery

*Correction notice:* the round-15 version of `soliton_mi_modal_audit.py`
reported a ≥ 70% two-mode core "at the crest". Re-audit found the power
split had been taken from the field at the END of the integration
window — the crest heights were correct, the split was not. At the true
crest the picture is opposite and richer — pump depletion (P = 1,
ε = 0.2, integer-fit seeds with exactly carrier + two sidebands)::

    mode     crest@z        P0    P(±Ω)   P(±2Ω)   rest
    m=4   4.387@6.40      0.017   0.237   0.195   0.552
    m=8   3.889@3.75      0.250   0.076   0.122   0.553
    m=16  3.143@2.60      0.061   0.378   0.307   0.254

- **The pump is depleted at every crest**: P0 ≤ 0.25. The deep-band
  crest is built from the sidebands, not from the carrier — the crest
  is a coherent beat of harmonics against a drained pump, the spectral
  fingerprint of the phase-anomaly geometry.
- **The crest is NOT a two-mode core**: carrier + fundamental ≤ 0.44
  everywhere (0.254 / 0.326 / 0.439); at least half the power sits in
  higher harmonics and the broadband rest for m = 4 and m = 8.
- **The carrier recovers by the window end**: P0 ≥ 0.50 and the
  two-mode core ≥ 0.70 at the late window (0.567 / 0.832 / 0.818) —
  the round-15 "modal coherence" observation survives, scoped to the
  late-recurrence state; the depletion is a transient crest-time
  phenomenon.
- **The late-window harmonic share still rises with the overshoot**:
  P(±2Ω) → P(±2Ω) → P(±2Ω) = 0.022 → 0.054 → 0.088 as the seed's
  crest climbs 3.143 → 4.387.
- **Honest negatives**: (a) "the carrier + fundamental hold ≥ 70% at
  the crest" is false — at most 0.44; (b) the crest is not exactly on
  the 2-mode manifold either.
- **Cross-twin note (round 17)**: the pump-depletion here is local and
  reversible (carrier restored at the window), the exact contrast to
  rule 147's mode concentration, which is monotone and final over the
  damage generations.

```bash
python soliton_eca/soliton_mi_modal_audit.py
python validate_mi_modal_audit.py
```

## The spectral gait: depletion at every crest, never a repeat

`soliton_mi_recurrence_chain_audit.py` walks the full recurrence chain
— every local crest above R = 1.3 within long windows (m=4 to z=44,
m=8 to 22, m=16 to 10) — and splits the spectrum at EACH crest::

    m=4  6.40/4.387/0.017  8.75/3.506/0.120  12.00/2.891/0.158
         17.00/2.441/0.088  28.40/1.738/0.251
    m=8  3.75/3.889/0.249  7.10/2.647/0.028  13.90/3.387/0.349
         20.70/2.733/0.107
    m=16 2.60/3.143/0.061  8.85/3.045/0.046

- **Pump-depletion is a crest-arrival property**: P0 ≤ 0.40 at all 11
  crests (max 0.349) — not a first-crest accident, but the fingerprint
  of every arrival at maximum amplitude.
- **Every crest is broadband-bound**: ≥ 0.20 of its power sits outside
  the four lowest lines at every crest (min 0.225).
- **The carrier re-inflates between crests**: max inter-crest P0
  0.846 / 0.946 / 0.918 — the depletion breathes with the recurrence.
- **Honest negative**: the recurrence chain does NOT reproduce the
  first crest's spectral mix — m=8's crest P0 swings 0.028↔0.349 (12×),
  and m=4's crest heights drift 4.387 → 1.738 without re-attaining the
  first crest within 44 units. Amplitude recurrence (round 11) does
  NOT imply spectral recurrence.

```bash
python soliton_eca/soliton_mi_recurrence_chain_audit.py
python validate_mi_recurrence_chain_audit.py
```

## Pump depletion across the (ε, Ω) plane

`soliton_mi_depletion_grid_audit.py` sweeps the crest-time carrier
share over the full phase-diagram grid (8 Ω × 5 ε = 40 cells, z ≤ 10)
plus far scales::

    P0@crest:  e=.05   0.124 0.340 0.246 0.047 0.013 0.001 0.032 0.144
               e=.10   0.062 0.310 0.251 0.054 0.014 0.000 0.101 0.138
               e=.20   0.017 0.249 0.229 0.061 0.055 0.000 0.026 0.132
               e=.30   0.038 0.219 0.237 0.042 0.069 0.025 0.048 0.123
               e=.45   0.060 0.157 0.233 0.064 0.020 0.010 0.057 0.146
              Ω = 0.196 0.393 0.500 0.785 0.900 1.000 1.200 1.414

- **Pump depletion is universal across the sampled growth band**:
  P0 ≤ 0.40 at the crest on all 40 cells (max 0.340) — the round-17
  ceiling holds for every seed amplitude and frequency up to √2.
- **The near-cap crescent exhausts the pump**: for Ω ∈ {0.9, 1.0} the
  crest carries P0 ≤ 0.10 at every ε — the phase diagram's secondary
  maxima are the deepest carrier drains (P0 = 0.000 at Ω = 1.0).
- **The far band keeps the carrier**: at Ω = 8.0 the crest is a
  near-passive carrier state (P0 = 0.950); Ω = 2 and 4 still drain
  (0.138, 0.208) — the depletion trough pokes past the linear band
  edge without reaching every scale.
- **Honest negative**: "P0 ≤ 0.40 at the crest for every scale" fails
  at Ω = 8.0.

```bash
python soliton_eca/soliton_mi_depletion_grid_audit.py
python validate_mi_depletion_grid_audit.py
```

## The carrier-void crest

The depletion grid reported P0 = 0.000 at Ω = 1.0 — a crest with NO
carrier. `soliton_mi_carrierfree_crest_audit.py` resolves the Ω = 1.0
crest structure (ε ∈ {0.10, 0.20, 0.30, 0.45}, z ≤ 14)::

    first crest   P0 = 0.0004/0.0003/0.0016/0.0002,  R = 2.76–3.23
                  P(±Ω) pair ≈ 0.44–0.59, P(±2Ω) pair ≈ 0.17–0.22
    second crest  P0 = 0.023/0.038/0.025/0.010  (carrier ≤ 0.06)
    fourth crest  ε=.30: P0 = 0.176  — the carrier returns.

- **The first crest is EXACTLY carrier-void**: P0 ≤ 0.01 for every
  seed amplitude (max 0.0016) — the near-cap crest carries no center
  frequency at all.
- **The void crest is a 4-line harmonic stack**: the ±Ω and ±2Ω pairs
  hold ≥ 0.60 of the power (min 0.662); the modulation period's own
  lines ARE the field at the crest.
- **The void persists through one full recurrence**: P0 ≤ 0.06 at the
  second crest for every ε (max 0.038).
- **Honest negative**: the carrier does not stay void at every later
  crest — at the fourth crest of ε = 0.30 the carrier returns to
  P0 = 0.176. The void is a first-period structural signature, not a
  permanent state.

```bash
python soliton_eca/soliton_mi_carrierfree_crest_audit.py
python validate_mi_carrierfree_crest_audit.py
```

## Dominant-pair crystallization of 147's damage field

Twin of the carrier-void crest (round 22): does the amplifier's damage
field crystallize onto a dominant wavenumber pair the way the NLSE
crest stacks onto its harmonic lines? Same 8-probe protocol as the
damage-modal round, top-2 non-DC wavenumber joint share::

    rule       top2@2    top2@12   top2@48   top2@96
    204        0.016     0.016     0.016     0.016
    51         0.016     0.016     0.016     0.016
    147        0.019     0.037     0.073     0.127

- **Rule 147 CRYSTALLIZES**: its top-2 share rises strictly at every
  sampled generation (0.019 → 0.127, a 6.7-fold rise) — the
  concentrating caustic locks onto its two dominant wavenumbers, the
  soft ECA mirror of the NLSE stack formation.
- **The transports do NOT crystallize**: 204 and 51 keep an identical,
  time-invariant flat 0.016 share — the flipped block's damage stays
  broadband across its whole footprint, the ECA mirror of the NLSE
  far band keeping the carrier.
- **Honest negative**: the pair never reaches a supermajority — at the
  sampling horizon it holds only 0.127 of the damage power (not
  ≥ 0.60). Concentration without majority: the ECA caustic
  crystallizes 6.7-fold but stays diffuse, so the carrier-void stack
  has no exact ECA supermajority twin.

```bash
python soliton_eca/soliton_damage_crystallization_audit.py
python validate_damage_crystallization_audit.py
```

## De-stacking of the void harmonic stack

Twin of the ECA turnover (round 24): does the NLSE void stack relax as
the carrier returns? Stack share (p1 + p2) at each crest of Ω = 1.0::

    eps=.10  0.759   0.396
    eps=.20  0.738   0.531   0.271
    eps=.30  0.713   0.542   0.418   0.247
    eps=.45  0.662   0.487   0.516   0.454   0.349

- **The stack sheds > 15% within one recurrence**: second-crest stack
  ≤ 0.85× first-crest for every seed amplitude (0.52×–0.76×) — the
  harmonic stack is a first-crest structure with a fast first-cycle
  relaxation.
- **The ≥ 0.60 dominance is a first-crest phenomenon**: by the end of
  the sampled chain the stack is below 0.60 everywhere (as low as
  0.247).
- **The fundamental pair outlives the relaxation**: p1 > p2 at every
  crest of every seed amplitude — the NLSE mirror of the ECA turnover
  is a *relaxation, not an identity flip*: the top pair never changes
  its identity, it only sheds share.
- **Honest negative**: the stack does NOT fall strictly at every crest
  — ε = 0.45 bumps up at crest 3 (0.516 > 0.487); the relaxation is
  monotone for ε ≤ 0.30 but weakly non-monotone at the largest seed.

```bash
python soliton_eca/soliton_mi_destack_audit.py
python validate_mi_destack_audit.py
```

## Concentration beyond the original horizon

`soliton_damage_concentration_persist_audit.py` extends the
damage-modal protocol fourfold to g ∈ {2, 12, 48, 96, 192, 288, 384}::

    147   top2  0.019 0.037 0.073 0.128 0.181 0.146 0.082
    147   PR    207   139   103    53    26    19    13
    204   PR = 186.18, top2 = 0.0156 at EVERY generation (2..384)
    51    PR = 186.18, top2 = 0.0156 at EVERY generation (2..384)

- **The concentration persists and deepens past the horizon**: 147's
  PR falls strictly at all seven samples (207 → 13 effective
  wavenumbers, a ~16-fold contraction) — the caustic keeps locking
  its damage mass onto fewer wavenumbers long after g = 96.
- **The isometry invariance extends 4×**: 204 and 51 keep
  PR = 186.18 and top-2 = 0.0156 exactly through g = 384 — the
  perfect transport constraint is not a short-horizon illusion.
- **Honest negative**: the top-2 pair does NOT keep rising — its share
  peaks at 0.181 (g = 192) and collapses to 0.082 (g = 384) while PR
  keeps falling. The identity of the dominant pair *turns over* as
  the caustic deepens: crystallization is a first-cycle phenomenon at
  the top-2 level even though overall concentration continues.

```bash
python soliton_eca/soliton_damage_concentration_persist_audit.py
python validate_damage_concentration_persist_audit.py
```

## Contraction-rate structure of 147's concentration

`soliton_damage_contraction_rate_audit.py` samples a finer grid to
resolve how 147's PR contracts generation by generation::

    g     PR.       per-generation log-slope (adjacent samples)
    2   207.0
    6   132.5      -0.1115     (steepest RATE, opening drop)
   12   139.2      +0.0082     (RISE -- non-monotone!)
   24   128.1      -0.0084
   48   103.0      -0.0090
   72    73.0      -0.0126     (steepest SUSTAINED, mid-course)
   96    53.1
  192    26.2
  384    13.1

- **The mature caustic contracts at ~3× the early rate**: factor-4
  window shrinking = 0.247/0.254 in the mature regime vs 0.740 early.
- **The fastest rate is the opening transient**: the (2,6) window
  carries |s| = 0.11, an order of magnitude above every later window
  — the seed's first-pass renormalization dominates the rate.
- **Past the transient, the fastest sustained contraction is
  mid-course**: among windows starting at g ≥ 12 the (48,72) window
  is fastest (0.0144), easing toward the tail.
- **Honest negative**: "PR falls at every generation" is FALSE — the
  dip to 132.5 at g=6 rises back to 139.2 at g=12. The sparse-grid
  strict monotonicity of rounds 16/24 was a sampling artifact;
  opening-drop → rise → mid-course acceleration is only visible at
  this resolution.

```bash
python soliton_eca/soliton_damage_contraction_rate_audit.py
python validate_damage_contraction_rate_audit.py
```

## Identity of the opening transient

`soliton_damage_opening_transient_audit.py` checks whether round 26's
opening morphology is a probe-universal structure or a mean-level
artifact, and what the damage MASS does through it::

    per-probe PR:  probe 0   1     2     3     4     5     6     7
        g=2          227.6   95.3  196.9 161.7 341.3 151.1 175.3 307.2
        g=6          128.7   96.7  115.4 167.6 227.6 126.0 120.2  78.3
        g=12         197.5  196.1   87.6 163.8 111.6 163.8 104.1  89.1
    damage mass F:  g=2 4.9   g=6 7.8   g=12 9.6   g=48 19.4   g=96 37.0

- **The damage mass grows strictly through the opening**: F increases
  at every grid sample (4.9 → 37.0) even while the entropy metric
  wobbles — the opening is mass-expansion, not reorganization along.
- **The opening PR is background-position-dominated**: per-probe PR
  spreads at g = 2 and g = 6 span a factor ≥ 2.5 (3.58, 2.91) —
  where the 4-cell block lands in the random ring sets the effective
  wavenumber count of its first-pass footprint.
- **Honest negative**: round 26's opening morphology (dip at 6 then
  rise at 12) is NOT probe-universal — only some probes dip-and-rise;
  probe 4 falls monotonically (341 → 228 → 112) and probe 1 barely
  dents. The morphology is a mean-level artifact and is not an
  intra-probe trajectory law.

```bash
python soliton_eca/soliton_damage_opening_transient_audit.py
python validate_damage_opening_transient_audit.py
```

## Per-probe universality of the certified long-time laws

`soliton_damage_probe_universality_audit.py` checks which certified
147 laws survive per-probe scrutiny (per-probe PR and top-2 at
{2, 12, 48, 96, 192, 384}, same 8-probe protocol)::

    per-probe PR:   probe 0     1     2     3     4     5     6     7
      g=  2           227.6   95.3  196.9  161.7  341.3  151.1  175.3  307.2
      g=384             7.9   17.0   17.3   10.2    6.1    6.8   13.8   25.3
    per-probe top2:   g=2  0.008..0.031   g=96  0.084..0.190
                      g=192 0.143..0.235  g=384 0.020..0.149

- **The concentration law is per-probe universal**: every probe has
  PR(96) < PR(2) and PR(2)/PR(384) ≥ 5.0 (min 5.60) — the 3.5-ratio
  law of round 16 holds on every individual probe, far above the
  mean-only line.
- **Crystallization-and-turnover are per-probe universal**: every
  probe has top2(96) > top2(2) AND top2(384) < top2(192) — the
  dominant pair's rise-and-reverse is a local trajectory structure.
- **Honest negative**: "all certified laws, including the opening,
  are per-probe universal" is FALSE — the opening variable PR(2)→PR(12)
  flips sign across probes (probes 1, 3, 5 rise). Only the long-time
  laws are locally robust; the first-pass footprint is
  background-position-dominated.

```bash
python soliton_eca/soliton_damage_probe_universality_audit.py
python validate_damage_probe_universality_audit.py
```

## The (ε, Ω) phase diagram: where the cap binds

`soliton_mi_phase_diagram_audit.py` maps the crest ≥ 3 region over
(ε, Ω) (P = 1)::

    ε      0.05  0.10  0.20  0.30  0.45
    below  0.500 0.500 0.900 0.900 1.000
    above  0.785 0.785 1.000 1.000 1.200

- **The band-dividing frequency rises with the seed amplitude**:
  weaker seeds keep the algebraic cap on more of the band, stronger
  seeds break it below a higher dividing frequency.
- **Single crossing for moderate seeds**: for ε ≥ 0.10 exactly one
  sampled crossing separates the cap-broken from the cap-kept region.
- **The crest curve is not globally monotone**: at Ω = 0.9 the crest
  exceeds the Ω = 0.785 crest for every ε ≥ 0.20 (3.41 > 3.14; 3.72 >
  3.34; 3.98 > 3.75) — a secondary local maximum, pinning the round-13
  monotonicity law to its grid.
- **Weak seeds lag deepest**: at ε = 0.05 the deepest m=2 wavelength
  crests only 1.480 within z = 10 (late-crest regime), re-crossing the
  cap on the deep side — so "one crossing at every ε" is itself an
  honest-negative; the structure holds from ε = 0.10 up.

```bash
python soliton_eca/soliton_mi_phase_diagram_audit.py
python validate_mi_phase_diagram_audit.py
```

## Single-bit damage spectrum

`soliton_damage_audit.py` flips one bit of a random background and tracks the Hamming distance H(g) between the damaged and undamaged lattices: the ECA analogue of the MI measurement (stable members neither heal nor spread a perturbation; mixing members amplify it into full-lattice chaos). Probes are drawn from the **LCG high bits** (`(seed >> 16) & 1`); see the measurement-integrity section below for why the low bit is unusable.

- **Hamming-isometry pair (exact)**: over the exhaustive width-8 cube (all 2^8 states, all pairs), the rules preserving every pairwise Hamming distance are exactly `{204, 51}` — 204 the identity, 51 the complement involution. Structurally these are the only global isometries in the family, and they are probe-independent.
- **Single-cell family** exactly `{204, 51}` at widths 8 and 16: a flipped bit under these rules stays at Hamming distance 1 forever — persistent and localized. The earlier reading `{51, 68, 76, 179, 204}` included 68/76/179 only because of the checkerboard probe degeneracy.
- **Full-lattice amplifiers** at width 16 exactly `{59, 115, 187, 243}` drive a single flipped bit to the whole lattice (max H = 16); at width 8 rule 91 also reaches the full 8-cell lattice. The "containment" reading is rejected (HONEST_NEGATIVE).
- Amplification is a marker of the mixing sector: the same members whose impulses fill the lattice and whose ensembles cascade.

```bash
python soliton_eca/soliton_damage_audit.py
python validate_damage_audit.py
```

## Exact census at width 16 and the boundary effect

`soliton_census_scaling_audit.py` computes the **exhaustive** functional-graph census over all 2^16 states on the torus, plus the ghost-zero bus next-map for the same states.

- **Conservation survives scaling**: exactly rule 204 conserves the population count over all 65,536 width-16 states.
- **The lap anchors persist**: {172, 228} keep exact max_cycle 16 (= width) and {27, 59, 83, 115} exact max_cycle 32 (= 2·width).
- **The stationary sector accumulates with width**: rules 44, 100 and 164 de-permute (become stationary) at width 16, so the width-12 stationary set `{4, 12, 36, 68, 76, 132, 140, 196, 204, 219, 236}` is strictly contained in the width-16 set.
- **The boundary matters exactly for the cycling sector**: torus and ghost max cycles coincide for every stationary and short-cycle rule — including the transport pair {204, 236} — and differ for all 12 rules with torus cycles ≥ 16, plus rule 123 (a 2-cycle whose `f(000)→1` injects zeros at the ghost boundary, turning its torus 2-cycle into a ghost 4-cycle). The one-/two-lap and glider phenomena are boundary artifacts of the torus.
- 204 fixes every state (identity) and 51 is a pure complement involution at width 16.

```bash
python soliton_eca/soliton_census_scaling_audit.py
python validate_census_scaling_audit.py
```

## The Peregrine breather bridges soliton and instability

`soliton_peregrine_audit.py` propagates the first-order Peregrine breather of
the focusing NLS normal form used here,

```
u(t, z) = sqrt(P) e^{iPz} [ 1 - 4(1 + 2iP z) / (1 + 4P t^2 + 4P^2 z^2) ],
```

the exact one-soliton on a nonzero background sqrt(P): at z = 0 the center
dips to **three times** the background amplitude (power ratio 9) and the
profile "breathes" back toward the background as z grows, without radiating.
It is the precise locus where the soliton-stable world (no background) and
the BI world (flat background, exponential sideband growth) connect.

- **Seed shape**: the analytic seed carries amplitude ratio 3.0000 (± 1e-3)
  at its center and matches the closed form to RMS < 1e-3 over the core.
- **Analytic curve**: the measured center ratio along z ∈ {0, 0.1, 0.25,
  0.5, 1, 2, 3} tracks the closed-form breather to within 1% at every point
  (worst relative deviation 7.6e-4 at z = 3). The SSFM and the formula agree
  to four decimals.
- **Breathes back**: the ratio falls 3.0000 → 1.1020 by z = 3 — the return
  to background, in sharp contrast to the MI sideband, which amplifies
  exponentially on the same equations.
- **Wings unperturbed**: for |t| ≥ 20 the field stays within 1% of the
  background over the whole propagation; no energy is shed.
- **Energy drift**: 2.4e-14 over the full run.
- **Mass neutrality (exact)**: the breather carries zero net mass. The
  window-integrated defect `∫(|u|² − P) dt` equals, to within 1e-4, the
  closed-form two-tail correction `8PL/(1 + PL²)` — the analytic line
  integral of `|u|² − P` is exactly 0, so the breather borrows all its
  extra core energy from the background and pays it back.
- **Phase laws**: at z = 0 the center sits exactly π out of phase with the
  background √P·e^{iPz} (the seed is −3√P), and the unfolded center phase
  equals the analytic branch `arg(4P²z² − 3 − 8iPz)` at every sampled z
  to within 1e-3 rad — a measurable, exact rotation law for the breather.

```bash
python soliton_eca/soliton_peregrine_audit.py
python validate_peregrine_audit.py
```

## The breather's parameter scaling

`soliton_peregrine_pscan_audit.py` rescans the breather at background
powers P ∈ {0.25, 0.5, 2, 4}. The closed form depends on z only through the
product P·z with powers set by the seed, so doubling P must halve the
breather's z-lengths while the peak ratio stays P-independent:

- **Seed ratio**: at z = 0 the center is 3.0000 (± 1e-3) times the
  background at every P (power ratio 9).
- **Universal curve**: at each P the measured center ratio at P·z ∈
  {0.25, 0.5, 1.0, 2.5} matches the closed form to ≤ 1.3e-4 relative —
  the four curves collapse onto one shape (3.0000 → 2.7203 → 2.2361 →
  1.6125 → 1.1435). For P = 0.25 the same ratios appear at z = 1, 2, 4,
  10; for P = 4 at z = 0.0625, …, 0.625 — the data show the scaling, not
  a re-fit.
- **Breathes back**: at P·z = 2.5 the ratio is below 1.15 at every P; no
  blowup, no radiation at any amplitude.
- **Energy**: relative drift stays below 3.4e-13 at every P.

```bash
python soliton_eca/soliton_peregrine_pscan_audit.py
python validate_peregrine_pscan_audit.py
```

## Single-bit damage growth rates

`soliton_perturbation_audit.py` measures the single-flip **dose response**:
on a fixed true-random grid of 24 LCG-high-bit backgrounds × every flip
position (384 events per rule, horizon 96 generations), the probability
that a flip reaches half the lattice (width/2) at widths 16/24/32. This is
the ECA-analogue of the MI gain: an amplification probability per rule
that decays with lattice size.

- **Reach set at width 16**: exactly 13 rules — `{27, 59, 83, 91, 115, 123,
  147, 155, 172, 187, 211, 228, 243}`. Two members differ from the
  checkerboard-era table: rule 91 is a real amplifier (second-ranked), and
  rules 164/251 appear there only under the degenerate probes.
- **Dominant amplifier**: rule 147 reaches half the lattice with event
  fraction 0.78; rule 91 next (0.31); then the tier {59, 115, 211, 155,
  27, 83, 187, 243} (0.06–0.14); the one-laps {172, 228} are rare (~0.005,
  0.003).
- **The stationary sector is silent**: rules 164, 251 (and 4, 12, …, 236)
  register zero half-reach events on the grid — amplification and
  attractor stationarity are opposite axes, and the round-6 "164 is the
  fastest amplifier (t_far = 4)" result was a checkerboard artifact.
- **Width scaling (laws)**: the reach set nests, `reachable(32) ⊆
  reachable(24) ⊆ reachable(16)` (W32 core = the 10 rules `{27, 59, 83,
  91, 115, 147, 155, 187, 211, 243}`), and the half-reach probability is
  monotonically non-increasing with width for **every** reachable rule
  (147: 0.779 → 0.727 → 0.673; 91: 0.31 → 0.09 → 0.02). More lattice
  means bounded damage.

```bash
python soliton_eca/soliton_perturbation_audit.py
python validate_perturbation_audit.py
```

## Damage extent spectrum: how wide a block the rules transduce

`soliton_extent_spectrum_audit.py` widens the probe from one cell to a
contiguous block of k flipped cells (k ∈ {1, 2, 4, 8, 16, 32}) on a
length-512 ring, and tracks F(k), the mean fraction of the lattice that
differs between the clean and perturbed trains after 96 generations:

- **Transparent pair** — {204, 51} pay back exactly the injected damage:
  F(k) = k/512 within one cell at every extent. Identity and complement
  are Hamming isometries, so damage can neither grow nor shrink.
- **Saturating sector** — the rest of the family caps far below the
  injection: even the strongest amplifier (rule 147) tops out at
  F(32) = 0.106–0.107. A single cell already seeds the whole caustic;
  widening the injection 32× barely moves the final damage. The twin
  family contains **no linear (XOR/affine) rule**, so no member
  transduces a large block.
- **Erasers** — {36, 219, 251} wipe the injected block at every size
  (F(k) ≤ 0.005): the same three rules that are the variance-sparse
  basins of the mixing-rate audit are here the extent-erasers — a
  cross-audit identity, certified as `L_regime_eraser_sparse_identity`.
- **External reference** — in the full 256-rule universe the eight
  affine rules {60, 90, 102, 105, 150, 153, 165, 195} transduce a
  32-block to F(32) = 0.250–0.312 (a fixed ~5× gain, extent-independent):
  linear CA is the universe's large-extent transducer. None sit inside
  the twin family, which is why the family saturates.
- **Honest negative** — the width-16 reach ranking does NOT persist to
  large extents: reach members 172/228 sit near the bottom (F(32) =
  0.015–0.017) while non-reach rules 19/76/179/204/51 exceed them.

**Regime audit** (`soliton_amplifier_regime_audit.py`) ties the sectors:
reach ∩ collapse = {172, 228} (only the one-lap pair among the
amplifiers also collapses spatial variance; 147 is variance-neutral);
the transport twins join no growth sector; and "every variance-collapser
is an amplifier" is FALSE — 164 and 251 collapse variance yet register
zero reach events.

```bash
python soliton_eca/soliton_extent_spectrum_audit.py
python validate_extent_spectrum_audit.py
python soliton_eca/soliton_amplifier_regime_audit.py
python validate_amplifier_regime_audit.py
```

### The sectors, re-scoped place by place

`soliton_extent_spectrum_probe_audit.py` replays the identical LCG
stream (same backgrounds, same perturbation positions — the per-probe
values are bit-for-bit the audit's) and asks whether the extent
sectors hold placement-by-placement, not just in the mean:

- **Transparent, placewise-exact** — rules 204/51 pay back exactly
  k/512 at every (placement, extent): the isometry is probe-exact.
- **Erasers** — the placewise picture is richer than the mean:
  - every placement's erase candidates stay INSIDE {36, 219, 251}
    (the family exhausts the erase behaviour anywhere);
  - rule 251 is an ABSOLUTE sink: F(k) = 0.0 at every extent in all
    eight placements;
  - but honest-negative: no single placement raises the full triple —
    the per-placement sets are {36, 251} (probes 0, 4), {219, 251}
    (probe 2), and the triple elsewhere.  Rules 36 and 219 lean on a
    0.005–0.006 residue (one or two cells out of 512) at k ∈ {8, 16,
    32} in some placements; the identification {36, 219, 251} is a
    mean-level fact.
- **Saturation, placewise** — even probe-by-probe, family F(32) max
  ≤ 0.139 < 0.250: no twin-family rule ever out-transduces the
  weakest affine rule in any single placement.

```bash
python soliton_eca/soliton_extent_spectrum_probe_audit.py
python validate_extent_spectrum_probe_audit.py
```

### The full-universe transducer census

`soliton_universe_transducer_audit.py` removes the last external
reference: instead of quoting the affine eight, it measures F(k) for
ALL 256 elementary cellular automata on the same background and
perturbation stream (extents k ∈ {1, 16, 32}, width 512, 96
generations, 8 probes):

- **The affine set is EXACTLY the universe's large-extent transducer
  class**: the rules with F(32) ≥ 0.250 are precisely {60, 90, 102,
  105, 150, 153, 165, 195}, no more and no fewer.  Rule 105 is the
  strongest single transducer at F(32) = 0.3125.
- **No non-linear rule crosses the floor**: the best non-affine rule
  is 126 at 0.2148 (below the weakest affine 0.250), and only 33
  rules sit at/above the 0.125 "weak-transducer" boundary.  The twin
  family max F(32) = 0.108 stays strictly below even that.
- **Honest negative — the isometry class is 10 rules, not 2**: the
  rules returning exactly k/512 at every measured extent are
  {15, 51, 85, 154, 166, 170, 180, 204, 210, 240} — the ring-level
  permutations and their bit complements.  {204, 51} is the twin's
  no-op pair within that class, not its boundary.

The universe census turns the round-27/30 external reference into a
certified classification: F(32) ≥ 0.250 ⇔ affine ⇔ linear
transduction, and the twin family is a strict non-transducer tail.

```bash
python soliton_eca/soliton_universe_transducer_audit.py
python validate_universe_transducer_audit.py
```

## The certificate contract: a mechanical inversion guard

The session's recurring failure class was the predicate-inversion bug:
a predicate that encoded the claim's NEGATION, or a variable named
"ok" that meant "the refutation holds", so a false claim was certified
PASS — caught by hand six times.  `certificate_contract_audit.py`
removes the human step for the six registered modules (retention
mechanism, closure chain, phase mechanism, collision-damage probe,
extent-probe, universe transducer):

- every certificate now carries an explicit `asserted` / `negated`
  polarity pair (the polarization contract), so the status
  `PASS ⇔ asserted` is machine-checkable;
- the audit pulls each module's measured data once, re-evaluates every
  predicate, and compares the live status against an expectation list
  declared INDEPENDENTLY of the predicate code (the corpus's
  documented facts act as the oracle);
- the polarity contract catches exactly the inversion class — an
  inverted predicate flips `asserted`, and the expected-polarity check
  fails before the certificate can enter the register;
- data pins (strongest transducer 105 at 0.3125, family F(32) < 0.125,
  the 10-rule isometry class, closure worst spread > 1 rad, retention
  best phases, the rel1-drift lock ≤ 0.30 rad with the anti-phase
  chain-max winner, the {36, 251} damage-wiper core, rule-251 sink)
  guard silent regeneration drift.

A second, fully independent copy of the expectation list lives in
`validate_certificate_contract_audit.py`, which also re-derives all
six modules' tables and recomputes every predicate from scratch — so
neither the audit's oracle nor the module predicates can drift
undetected.  Twenty-four contract certificates and twenty-seven module
certificates are checked; violations fail loudly.

```bash
python soliton_eca/certificate_contract_audit.py
python validate_certificate_contract_audit.py
```

## The vacuity battery: predicates that cannot read their data

The certificate-contract audit catches the inversion class; it does not
catch the dual defect — a predicate that is INSENSITIVE to its data, a
vacuity install (`lambda: True`, or a threshold so loose the law can
never fail).  `certificate_vacuity_audit.py` runs every registered
module's certificate functions over a battery of data mutants (the two
generic ablations `zero`/`tiny` plus per-module targeted mutants that
break or satisfy each law), and requires, for every certificate:

- **pass-defeasible** — every PASS certificate flips to NOT asserted
  under some mutant: no certified law is unbreechable by construction;
- **hn-witnessed** — every HONEST_NEGATIVE certificate flips to
  asserted under some mutant: no HN statement is a literal
  `lambda: False`;
- **battery-live / domains-stable** — no mutant is inert, and every
  mutant keeps the certificate arity and label set intact.

The battery re-scores certificates over mutated in-memory tables (no
re-propagation), so it is cheap and deterministic.  All 27 registered
certificates flip under the battery, and the battery's own 23
certificates PASS (18 module-level — pass-defeasible /
hn-witnessed / battery-live for each of the six registered modules —
plus 5 global: contract-alignment, all-pass-defeasible,
all-hn-witnessed, all-battery-live, domains-stable).  The validator
re-derives the battery and the flip contracts independently.

The battery immediately repaid itself: the first witness mutant for
`L_ret_closure_resonance` (an HN certificate) set `delta = p0`, which
gives the retention winner the MAXIMUM |delta| — a silent re-instantiation
of the very inversion the audit exists to kill.  The witness was
corrected to `delta = 1 - p0` (winner at the minimum), and the battery
caught the error before registration.

```bash
python soliton_eca/certificate_vacuity_audit.py
python validate_certificate_vacuity_audit.py
```

## Pre-registered delta* sweep: two predictions refuted

The round-40 closure-chain narrative described delta* (the carrier's
offset from the sideband phase centroid, chain-mean at each crest) as
"phase-structured: p0-p2/p7 near zero, the others sweeping to −3 rad".
That description was written after the values were on the table.
`preregistered_delta_star_sweep.py` inverts the order: four predictions
are declared in the source BEFORE the module computes anything, each
with an explicit decision rule, and the measured table settles them:

- **P1** — the near-zero phases (`|delta*| ≤ 0.5 rad`) are exactly
  {p0, p1, p2, p7} in every geometry.  **REFUTED**: the near-zero
  sector migrates with geometry — (0.5,0.2) near = {p0, p1, p2, p6,
  p7}, (0.5,0.3) near = {p0, p7} only, (1.0,0.45) near = {p0, p5}.
  The "half the phases near zero" reading was a post-hoc artifact of
  one geometry.
- **P2** — every far phase {p3, p4, p5, p6} has `delta* < 0` in every
  geometry.  **REFUTED**: the far sector is NOT one-sided — p6 is
  positive in four of the six geometries (up to +1.81 rad at
  (1.0,0.45)), and p3/p4 turn positive at Ω = 1.0, ε 0.45.
- **P3** — the delta* range across phases is ≥ 2.0 rad in every
  geometry (replication on the floor of the round-40 range).  CONFIRMED:
  ranges 2.022 → 3.433 rad, flooring at (1.0,0.3) = 2.02.
- **P4** — delta* is always angularly distinct from rel1 somewhere
  (max |wrap(delta* − rel*)| > 1.0 rad per geometry).  CONFIRMED:
  distinct max ≥ 2.37 rad everywhere.

So the closure angle is genuinely a scatter (P3) that carries
information rel1 does not (P4), but its sign- and near-zero structure
is geometry-migrating, not a frozen phase partition.  Two a priori
predictions were refuted and entered the register as HONEST_NEGATIVE —
the cost the pre-registration protocol had to be prepared to pay.

```bash
python soliton_eca/preregistered_delta_star_sweep.py
python validate_preregistered_delta_star_sweep.py
```

## Damage timecourse: how fast damage reaches its final form

`soliton_damage_timecourse_audit.py` re-injects a k = 32 block into a
length-512 ring but samples the damage F(t) across the transient
(generations 1–96, 12 sample times). The family separates by speed:

- **Transparent pair** — {204, 51} return F(t) = 32/512 at *every*
  sampled generation: the isometry holds transient by transient, not
  only in the limit.
- **Instant sector** — {4, 12, 19, 36, 51, 59, 68, 76, 187, 204, 219,
  236, 243}: the final damage appears within the first generation
  (|F(1) − F(96)| ≤ 2 cells): the deterministic image of the block, no
  diffusion phase.
- **Wave runners** — {147, 155, 211}: the damage keeps spreading long
  after gen 1 (F(1) ≤ 0.6·F(96)). All three are width-16 reach-set
  members; rule 91 peaks at gen 8 and then settles, dropping off the
  runners.
- **Erasers** — {36, 219, 251} wipe the block by gen 4 (251 to 0.000);
  the stationary one-laps {164, 172, 228} also *decay* their damage
  (164: 0.022 → 0.009).
- **Persistent grower** — rule 147 is the *only* family rule whose
  damage is still increasing at gen 96 (F(96) ≥ 1.25·F(16); measured
  0.052 → 0.091). The dominant amplifier is the slowest to saturate:
  the claim "all family damage saturates by gen 24" is FALSE
  (HONEST_NEGATIVE) — 147's damage front keeps expanding long after
  every other rule has settled.

```bash
python soliton_eca/soliton_damage_timecourse_audit.py
python validate_damage_timecourse_audit.py
```

## Density flow: invariant, settling, and biased attractors

`soliton_density_flow_audit.py` follows population density over 32 torus
generations from LCG random seeds at densities {0.25, 0.5, 0.75}. Three
behaviors exist in the family:

- **Exact invariant** — only rule 204 keeps density(t) == density(0) for
  every generation, seed and probe. Even the complement involution 51
  alternates d → 1−d, so it fails on the 0.25/0.75 seeds.
- **Density settling** — every width-16 stationary rule reaches a constant
  density tail for every seed: the A-side attractor levels are distinctly
  below half (mean tail density 0.04–0.46 for the A-side stationary rules),
  while the boundary-insensitive B-side members {219, 236, 251} settle at
  0.96 / 0.56 / 1.00.
- **Biased attractors** — the claim "every non-stationary rule converges to
  half density" is FALSE (HONEST_NEGATIVE): {91, 123, 155, 211} settle at
  mean densities 0.59–0.77, driven by their unbalanced windows. The two-lap
  rules {27, 59, 83, 115} never settle at all — their density oscillates
  with the torus lap (max cycle 32).

```bash
python soliton_eca/soliton_density_flow_audit.py
python validate_density_flow_audit.py
```

## Spatial variance decay: mixing rates

`soliton_mixing_rate_audit.py` tracks the spatial variance V of a
length-512 ring started from true-random (LCG high-bit) half-density seeds,
at generations 2, 20 and 100. Density alone cannot see structure; the
variance separates the family into three measured sectors:

- **Structure preservers** — 28 of 32 rules keep V100/V2 ≥ 0.8: the
  chaotic "mixing" sector holds V100 ≈ 0.20–0.25 (the same value as V2),
  as do all stationary rules and the transport pair. The chaotic rules mix
  state space but do not homogenize space.
- **Spatial collapse sets** — exactly {164, 172, 228, 251} sink to ≤ 60%
  of their initial variance, and the reassembly is already complete at
  generation 20 (V20/V2 ≤ 0.6). These are the de-permuted former rotation
  164 and the one-lap pair {172, 228} from the width-16 census, plus the
  fill rule 251 — the permutation-sector non-isometries that rebuild a
  random pattern into sparse structure.
- **Sparse basins** — exactly {36, 219, 251} reach V100 ≤ 0.06 (36's
  A-side sparse stationary attractor; 219/251 the B-side near-uniform
  attractors); only 251 reaches V100 = 0.000.

- **Exact isometry**: rules 204 and 51 preserve V to machine precision —
  identity and complement are variance isometries.
- **Honest negative**: the claim "every mixing rule homogenizes space
  toward uniform" is FALSE — the chaotic sector keeps V100 ~ 0.20–0.25;
  only {36, 219, 251} flatten the distribution and only 251 flattens it
  all the way to uniform.

```bash
python soliton_eca/soliton_mixing_rate_audit.py
python validate_mixing_rate_audit.py
```

## Two-block collisions: interaction ranges on the bus

`soliton_collision_damage_audit.py` injects TWO k = 4 blocks at
block-center distance d ∈ {4, 16, 64, 128, 256} on the width-512 ring
and measures F2(d) against the independent baseline 2·F1 (the
single-block damage doubled) — the ECA twin of the two-soliton
interaction audit. It separates the family by how packets interact when
they share the bus:

- **The isometry bus never interacts (exact)**: for rules 204 and 51,
  F2(d) = 2k/W = 0.016 at every distance, equal to the baseline to the
  cell. Two packets on the identity/complement bus pass each other with
  zero cross-talk at any separation — the bus-level equivalent of
  solitons passing without exchange.
- **The deep-wipe tier**: {4, 36, 219, 251} bring two 4-blocks to
  ≤ 0.006 at every distance — the erasers plus the deep-local
  stationary rule 4, whose residual is quantized to a couple of cells
  (251 → 0.000).
- **Amplifier saturation (rule 147, unique)**: 147's two caustics
  COMPETE for the same damage budget instead of adding. At d = 4 it
  lands at F2 = 0.075 vs the 0.124 baseline — I(d4) = −0.049, ~40%
  below the independent sum — recovering toward the baseline only by
  d = 256. Rule 147 is the unique rule with I(d4) ≤ −0.03.
- **Far-field independence**: at the antipode every rule's two blocks
  act independently, |F2(256) − 2·F1| ≤ 0.005.
- **No amplification anywhere, a granular residue**: HONEST_NEGATIVE —
  "two blocks never damage more than their sum" is FALSE in the strict
  form, but only because the deep-local rules' damage is cell-quantized
  (rule 4 leaves ~3 residual cells where the additive baseline says 2);
  no rule amplifies. The family's strong interaction is purely
  saturative, and it belongs to the dominant amplifier.

```bash
python soliton_eca/soliton_collision_damage_audit.py
python validate_collision_damage_audit.py
```

## Two-block collisions in time: how saturation builds

`soliton_collision_timecourse_audit.py` tracks the two-block damage
generation by generation (γ ∈ {2…96}) at the interacting distance
d = 16 and the independent antipode d = 256, normalized by the
independent baseline ρ(γ) = F2(γ)/(2·F1(γ)):

- **The isometry bus conserves the two-packet distance at every
  instant**: rules 204 and 51 hold F2 = 2k/W = 0.016 exactly at every
  generation, both distances — ρ = 1.000 forever, no transient at all.
- **Rule 147's saturation is NOT instant**: the collision opens with a
  constructive transient (ρ = 1.14 at γ = 2 — two close caustics first
  add more than their independent sum), holds a plateau near 1 through
  γ ≈ 16, and only beyond γ = 24 does the deficit drive ρ down to
  **0.76–0.77** by γ = 48–96. The amplifier's damage budget is spent
  progressively — an honest-negative against "saturation from the first
  generation" (HONEST_NEGATIVE).
- **The antipode never feels it**: rule 147 at d = 256 wobbles within
  |ρ − 1| ≤ 0.23 across all generations (probe statistics of the two
  independent caustics), flat against the interacting 0.76.
- **The erasers {36, 219, 251}** take both blocks to ≤ 0.006 well
  before γ = 96.

```bash
python soliton_eca/soliton_collision_timecourse_audit.py
python validate_collision_timecourse_audit.py
```

## Rule 147's interaction potential: the range profile

`soliton_collision_range_audit.py` resolves ρ(d) = F2(d)/(2·F1) for
rule 147 at γ = 96 on a fine d-grid:

    d     4     8     12    16    24    32    48    64    96   128   192   256
    ρ    0.546 0.535 0.657 0.595 0.666 0.726 0.784 0.858 1.007 0.956 0.954 1.039

- **The saturative core reaches well beyond the block**: ρ ≤ 0.66 for
  every d ≤ 16 (blocks within four block-lengths share the damage
  budget hard; worst ρ = 0.535 at d = 8).
- **The bottom is a flat bracket**, not a point: deficit ≈ 0.45 at both
  d = 4 and d = 8, at least 0.05 above the deficit at d = 12.
- **Recovery halo**: ρ rises by ≥ 0.30 across the 8 → 64 band and is
  ≥ 0.95 for every d ≥ 96 — independence arrives around 64 cells
  (8 block lengths).
- Rule 204 sits at ρ = 1.000 exactly on the same grid.
- **Honest negative**: "two blocks at any separation add damage
  independently" fails — the core reaches d ≤ 16.

```bash
python soliton_eca/soliton_collision_range_audit.py
python validate_collision_range_audit.py
```

## Three-block crowding: exact additivity for transports, concatenation for 147

`soliton_collision_crowd_audit.py` adds a third 4-cell block (at 16
and 96) and measures the family's f1/f2/f3 Hamming densities at
generation 96::

    rule  f1      f2      f3       f2/f1  (f3-f2)/f1
    204   0.0078  0.0156  0.0234   2.000   1.000
     51   0.0078  0.0156  0.0234   2.000   1.000
    147   0.0723  0.0859  0.1506   1.189   0.895
    251   0.0000  0.0000  0.0000   0.000   0.000

- **The isometry transports are EXACTLY additive**: two blocks damage
  exactly 2·f1, three exactly 3·f1 (8 and 12 live cells per 512) —
  their XOR-of-runs fields are disjoint live cells that never merge or
  cancel. The exactly-additive set is {204, 51, 251} (251 by
  triviality: 0 = 3·0); no other rule is exactly additive.
- **Rule 147's in-core pair demands far less than an independent
  block**: f2 = 1.189 f1 at d = 16 (≤ 1.35) — the saturative core
  keeps crowding cheap.
- **Yet the far block lands nearly full onto the crowded pair**:
  (f3 − f2) = 0.895 f1 (≥ 0.8) — the caustic CONCATENATES; it is not
  a shared, saturating budget (and rule 91, a grower, shows an even
  stronger super-additive far leg, 1.39 f1).
- **Honest negative**: "two-block damage is additive for every rule"
  fails — 147's ratio is 0.59×.

```bash
python soliton_eca/soliton_collision_crowd_audit.py
python validate_collision_crowd_audit.py
```

## Block-size scaling of exact additivity: the intersection is {204, 51, 251}

`soliton_collision_kscale_audit.py` repeats the exact-additivity test
at every block size K ∈ {1, 2, 4, 8}::

    K   exact-additive set at that K
    1   {51, 204, 251}
    2   {44, 51, 123, 204, 251}
    4   {51, 204, 251}
    8   {51, 164, 204, 251}

- **The isometry transports scale EXACTLY in K**: f1 = K/W, f2 = 2K/W,
  f3 = 3K/W to the bit at every block size (their XOR-of-runs fields
  stay disjoint live cells at any width of the seeded block).
- **The exact-additive sets intersect over all K to exactly
  {204, 51, 251}**: only the two isometry transports and the full
  eraser (0 = 3·0) are additivity-exact at every block size. Every
  K-coincidence (44, 123, 164 at single sizes) is K-fragile and
  vanishes elsewhere.
- **Honest negative**: "the exact-additive set is block-size
  independent" fails — the coincidences do not persist across K.

```bash
python soliton_eca/soliton_collision_kscale_audit.py
python validate_collision_kscale_audit.py
```

## Per-probe stability of the crowd conclusions

`soliton_crowd_probe_stability_audit.py` re-examines round 19's
three-block crowd claims a probe at a time (integer Hamming counts,
same 8 placements, g = 96). The mean-based claims need qualifiers::

    exact-additive sets per probe: probe 1 = 15 members, probe 5 = 5,
      probe 0 = 8 ... all 8 probes contain {204, 51, 251}
    147 per-probe:  f2/f1 0.806..2.087   (f3-f2)/f1 0.446..1.652

- **The probe-invariant core IS {204, 51, 251}**: the intersection of
  all per-probe sets equals the mean-certified set exactly — round
  19's identity survives as an intersection statement. The isometry
  and eraser additivity is absolute per placement.
- **Honest negative — the certified set is a mean-level statement**:
  single placements add coincidental members by integer equality (up
  to 15 rules at probe 1, e.g. 12, 68, 115, 132, 187); "only
  {204,51,251} at every probe" is FALSE.
- **Honest negative — 147's core margin breaks per placement**: f2/f1
  reaches 2.087 (probe 1) and 1.400 (probe 6), past the 1.35 ceiling;
  the 1.188 mean hides a 0.81..2.09 range.
- **Honest negative — the far block does not always land**: (f3-f2)/f1
  drops to 0.446 and 0.613 at probes 3 and 4 — sometimes the crowded
  pair absorbs the far block (shared-budget behavior); the 0.895 mean
  overstates the universal concatenation.

```bash
python soliton_eca/soliton_crowd_probe_stability_audit.py
python validate_crowd_probe_stability_audit.py
```

## The far-lands mechanism: an f1-normalization artifact, not a budget

`soliton_crowd_far_budget_audit.py` tests why round 29's far-lands
ratio fails per placement::

    probe          0    1    2    3    4    5    6    7
    f1            41   23   30   56   31   37   40   38
    f2            38   48   40   71   25   40   56   34
    far (f3-f2)   42   38   30   25   19   48   27   36
    (f3-f2)/f1    1.02 1.65 1.00 0.45 0.61 1.30 0.68 0.95

    spearman(f2, far)  = -0.107   (far cells ~ independent of f2)
    pearson(f1, ratio) = -0.685   (ratio variance is f1-dominated)

- **The far block's cell count is pair-demand-independent**: the
  landing stays near a 33-cell mean (range 19–48) no matter how the
  in-core pair itself filled (Spearman −0.107 ≈ 0).
- **The ratio failure is f1-normalization**: Pearson(f1, ratio) =
  −0.685 — probes 3/4 "fail" the ≥ 0.8 margin because their
  single-block damage is large (56, 31 cells), dragging the
  denominator, not because the landing shrank.
- **Honest negative — the shared-budget mechanism is refuted**:
  "the crowded pair consumes the caustic's budget, shrinking the far
  block's cells" is FALSE — the landing is not subtractive.

```bash
python soliton_eca/soliton_crowd_far_budget_audit.py
python validate_crowd_far_budget_audit.py
```

## Per-placement stability of the kscale additivity sets

`soliton_kscale_probe_audit.py` re-examines round 20's exact-additive
sets a placement at a time (the deterministic 8-probe kscale stream,
integer Hamming counts)::

    exact per placement (16 (rule, K) cells x 8 probes):
      {204, 51, 251}   exact at ALL 24 (rule, placement) x K ... 0.0
      44 @K=2          exact on 2 of 8 placements   (max 4 cells off)
      123 @K=2         exact on 4 of 8 placements   (max 6 cells off)
      164 @K=8         exact on 2 of 8 placements   (max 4 cells off)
      residual spectrum: always whole cells n/512, n = 1..87

- **The core is absolute per placement**: {204, 51, 251} satisfy
  f3 = 3 f1 with zero residual on every placement at every K.
- **The probe-by-probe intersection over all K is exactly
  {204, 51, 251} for every placement** — round 20's intersection
  result holds even probe-wise.
- **Honest negative — the coincidences are mean-level artifacts**:
  "44/123/164 achieve exact additivity at every placement" is FALSE;
  each holds exact equality on only 2–4 of the 8 placements, so their
  round-20 set membership is a placement-aligned averaging artifact.
- **Every residual is a whole cell**: |f3 − 3 f1| = exactly n/512
  (n ∈ 1..87), never a fraction — the near-coincidences are discrete
  integer cancellations, and the origin-of-the-coincidence probe shows
  the mean rounds a set of small-integer misses to zero.

```bash
python soliton_eca/soliton_kscale_probe_audit.py
python validate_kscale_probe_audit.py
```

## Initial-phase robustness of the carrier-void crest

`soliton_mi_phase_probe_audit.py` sweeps the modulation's initial
phase (8 draws, k·π/8, eps = 0.20, Omega = 1.0), observing the seed's
brightness column.  The first pass read a sectored void (pump-strong
"crests" at the sine-like phases) -- this audit re-scoped the crest
definition to the near-cap mountain (R >= 2.5) and SUPERSEDES that
reading::

    near-cap first crests (z ~= 2.45, R ~= 2.8):
      P0:  .0003 .0006 .0017 .0021 .0013 .0006 .0003 .0002
      stack: .738  .741  .734  .720  .712  .713  .712  .714
    near-cap second-crest P0: .0381 .018 .0373 .0612 .2101 .0379
                              .0005 .0034

- **Crest formation is phase-inertial**: all 8 phases form the
  near-cap crest (the earlier "sine seed does not focus" read a
  z = 0.35 ridge of R = 1.22 as the crest).
- **The void is phase-inertial at the near-cap crests**: first-crest
  P0 <= 0.01 (max 0.0021), harmonic stack >= 0.60 (min 0.712) on
  8/8 -- the round-22 void no longer looks sector-dependent.
- **Honest negative — the phase sensitivity lives in the
  recurrence**: the near-cap second-crest P0 exceeds 0.06 at
  φ = 3π/8 (0.0612) and φ = π/2 (0.2101), both at genuine crests
  (R >= 2.5).
- **Honest negative — the carrier returns at a later near-cap crest
  for every phase** (chain max P0 = 0.018–0.210), so the round-22
  "void is a first-period signature" survives the re-scope.

```bash
python soliton_eca/soliton_mi_phase_probe_audit.py
python validate_mi_phase_probe_audit.py
```

## Near-cap re-scope of the chain laws: confirmed clean

`soliton_mi_chain_rescope_audit.py` re-runs the round-22/25 crest
chains under the near-cap crest definition (R >= 2.5) to learn
whether the loose-threshold chains hid ridges::

    eps=0.10  R 2.76 @ z 3.30, 9.85            (2 near-cap crests)
    eps=0.20  R 2.84 @ z 2.45, 7.35, 12.25     (3)
    eps=0.30  R 2.96 @ z 1.95, 5.90, 9.80, 13.70   (4)
    eps=0.45  R 3.21-3.27 @ z 1.50, 4.50, 7.50, 10.45, 13.45  (5)

- **The chains were already near-cap**: every round-22/25 crest has
  R >= 2.5; the loose threshold had admitted no ridges at phi = 0
  (the ε=0.30 "fourth crest P0 = 0.176" is a genuine crest, R =
  2.93, and the ε=0.45 crest-3 bump 0.516 > 0.487 sits at R = 3.23).
  The ridge artifact found in round 33 was specific to the phase
  sweep, where displaced alignment produced a low pre-crest ridge
  first in the loose chain.
- **First-crest laws confirmed**: void P0 ≤ 0.01 (max 0.0016) and
  harmonic stack ≥ 0.60 (min 0.662) under the stricter detector.
- **De-stack laws confirmed at near-cap crests**: second-crest stack
  ≤ 0.85× first (ratios 0.52–0.76), final crest stack < 0.60
  (0.247–0.396), p1 > p2 everywhere.
- **Carrier-return confirmed**: every ε has a near-cap crest with
  P0 > 0.01 (chain max up to 0.176), so "void is a first-period
  signature" stands.

```bash
python soliton_eca/soliton_mi_chain_rescope_audit.py
python validate_mi_chain_rescope_audit.py
```

## The three-wave phase invariant and the anti-phase carrier resonance

`soliton_mi_phase_mechanism_audit.py` resolves round 33's open
question -- why the phi = pi/2 second crest keeps the carrier
(P0 = 0.210).  It traces the gauge-invariant sideband phase
difference rel1 = arg(U_{+Omega}) - arg(U_{-Omega}) (well-conditioned:
strong sideband bins) at every near-cap crest of the 8-phase sweep::

    phase      1st crest   2nd crest   3rd crest    2*phi
    p0         +0.000      +0.000      +0.000       0.000
    p1         +0.776      +0.765      -            0.785
    p2         +1.576      +1.502      +1.618       1.571
    p3         +2.392      +2.226      +2.305       2.356
    p4         -3.089      +3.024      -            pi (wrapped)
    p5         -2.310      -2.512      -            3.927
    p6         -1.540      -1.544      -1.428       4.712
    p7         -0.771      -0.764      -0.832       5.498

- **rel1 is a conserved invariant of the recurrence**: rel1 = 2φ
  (mod 2π) at every near-cap crest, max drift 0.156 rad (p5's second
  crest) -- the ±Ω sidebands propagate with a frozen phase lock
  seeded by the initial phase.
- **The exact anti-phase geometry is the unique maximum-retention
  resonance**: chain-max carrier P0(φ=π/2) = 0.210 > every other
  phase's chain max (nearest p7 at 0.123); the pump-retained crest
  is the resonance of exactly-opposed sidebands.
- **Honest negative — rel1 does not alone ORDER the return**: the
  second-crest P0 is not monotone in cos(rel1) there; 0.210 is a
  discrete exact-anti-phase resonance, not one end of a continuum.

```bash
python soliton_eca/soliton_mi_phase_mechanism_audit.py
python validate_mi_phase_mechanism_audit.py
```

## The two-block damage laws, re-measured per placement

`soliton_collision_damage_probe_audit.py` replays the round-14
collision-damage stream (identical LCG draws, backgrounds, and
per-rule placements) but keeps every placement's value, then re-checks
each mean-certified law per placement.  The round-14 statements were
TRUE as mean laws; per placement they split into a small core that
always holds and a long tail of placement-structured violations.

- **The isometry disconnect is placement-exact**: rules 204 and 51
  keep F2(d) == 2·4/512 at every distance at every placement
  (integer-exact) -- the transparent family detaches identically
  everywhere.
- **The wipe core is {36, 251}**: the full wiper set (max_d F2 ≤
  0.006) varies per placement (e.g. probe 2 gives {36, 68, 100, 228,
  251}, probe 3 gives {4, 36, 219, 251}), but its intersection over
  all eight probes is exactly {36, 251}, both wiping at every
  placement; 219 joins six/eight (failing probes 0 and 2).
- **147's short-range saturation is an aggregate, and it inverts
  once**: F2(4) − 2·F1 ≤ −0.03 holds at 7/8 placements (mean −0.048,
  unique on means, matching the round-14 signature), but probe 3 gives
  **+0.039** -- the strongest positive short-range interaction in the
  whole table, at exactly the distance the mean law calls "saturated".
- **The antipode independence was a mean law only**: |F2(256) − 2F1|
  ≤ 0.005 holds on means but per-placement the worst rule reaches
  **0.131** -- 147's wrapped caustic at probe 3, the same probe and rule
  as the short-range inversion; 147 dominates the far cross-talk at
  6/8 placements.
- **"No synergy at any distance" is a mean law only**: per placement
  ~20 rules cross the tight 1.01·2·F1 tolerance in some placement --
  coincidence-based collisions routinely beat the two-block baseline,
  exactly as the mean picture never showed.

The collision-damage laws therefore survive in aggregate, and the
per-placement damage field is as placement-structured as the crowd and
kscale families -- the amplifier's caustics are not local or stable,
they move with the packet's address.

```bash
python soliton_eca/soliton_collision_damage_probe_audit.py
python validate_collision_damage_probe_audit.py
```

## The frozen phase lock, swept over geometry

`soliton_mi_phase_invariant_sweep.py` asks whether round 35's
invariant -- rel1 = arg(U₊Ω) − arg(U₋Ω) ≡ 2φ (mod 2π) at every
near-cap crest, with the exact anti-phase seed the unique
maximum-retention configuration -- survives a change of seed geometry.
Nine geometries (ε ∈ {0.20, 0.30, 0.45}, Ω ∈ {0.5, 1.0, 2.0}) × 8
phases, the identical near-cap protocol; Ω = 2.0 is the MI band edge,
where crest formation is suppressed (crest counts {0, 0, 2}).

- **The lock is a low-modulation property**: at ε ≤ 0.20 it holds at
  every Ω that crests (max drift 0.156 rad, exactly the round-35
  anchor at (0.20, 1.0)); at Ω = 0.5 the drift climbs *monotonically*
  with ε (0.107 → 0.426 → 0.878), and at (0.30, 1.0) it already
  reaches 0.288 -- off-band-center seed power breaks the phase lock
  non-uniformly.
- **The anti-phase resonance is fragile**: the chain-max carrier
  return sits at φ = π/2 only at (0.20, 1.0) and (0.30, 0.5); it
  migrates to φ = 0 at (0.30, 1.0), to φ = π/4 at (0.45, 1.0) and
  (0.45, 2.0), and to φ = 3π/4 at Ω = 0.5 -- round 35's exact
  anti-phase resonance is a property of the low-modulation
  band-center geometry, not a general three-wave law.
- **The anchor reproduces**: at (ε = 0.20, Ω = 1.0) the drift is
  0.156 rad and the resonance sits at φ = π/2, exactly as round 35
  measured it before the sweep moved off it.

Round 35's invariant survives as scoped: conserved at low modulation,
degrading monotonically with off-band-center seed power, and the
retention resonance that made φ = π/2 special is likewise
band-center-only.

```bash
python soliton_eca/soliton_mi_phase_invariant_sweep.py
python validate_mi_phase_invariant_sweep.py
```

## 147's fine profile and time course, re-measured per placement

`soliton_collision_profile_probe_audit.py` replays the round-13 range
audit (147's rho(d) on the 12-point d-grid) and the round-12/13
colliding-timecourse audit (rho(d, g) at d = 16 and d = 256) with their
exact streams, keeping every placement, and re-checks each signature
per placement while re-certifying the aggregate from the same run.

- **The transparent family is placement-exact again**: rule 204 keeps
  rho_p = 1 exactly at every d at every placement; 204 and 51 keep
  |F2_p[g] − 2·F1_p[g]| ≤ 1 cell at every generation at every
  placement.
- **The aggregate reproduces digit-for-digit**: the mean profile
  recomputes the round-13 table (core max 0.657 ≤ 0.66 at d ≤ 16,
  halo min 0.954 ≥ 0.95 at d ≥ 96); the mean transient opens at
  rho(g = 2) ≈ 1.25 ≥ 1.10 and the mean far wobble stays ≤ 0.30.
- **…but 147's per-placement fields are wild**: the core (max
  rho_p(d ≤ 16) ≤ 0.66) fails 5/8 placements, inverting to
  rho = 1.130 at placement 1 — close blocks add more than the
  independent baseline on that packet address; the pairwise profile
  spread reaches 1.17 (d = 128); the constructive opening dips to
  0.875 and spikes to 2.5; and the far field's worst |rho_p − 1| is
  3.375 — a ratio blowup where a placement's 2·F1(g) is tiny (an
  erasure-lucky draw).  The round-13 fine profile and the round-12
  transient/far laws were mean-level laws; the per-placement object is
  placement-structured, exactly like the crowd and damage families.

```bash
python soliton_eca/soliton_collision_profile_probe_audit.py
python validate_collision_profile_probe_audit.py
```

## The detection-parameter audit checklist (rounds 29-38)

The scoping sweep of rounds 29-38 was run under a fixed set of
methodological rules that turned out, in every family, to be the
thing that made the results trustworthy.  Distilled, they are the
checklist any future claim in this program must pass:

1. **Thresholds triple-triangulate a detection.**  Near-cap crests
   (R >= 2.5) are real; the loose ridge threshold (R > 1.2 local max)
   admits linear phase-conjugate RIDGES that masquerade as MI crests
   (rounds 32 -> 33).  Every qualitative claim's oracle (depletion
   grid, scans, chains) must be re-run under a stronger detector and
   the surviving set re-stated.
2. **Alignment is a detection parameter.**  The observation column
   must follow the seed's brightness maximum (argmax |seed|), not a
   fixed coordinate -- at fixed columns the phase sweep's low ridges
   read as "pump-strong crests" (round 32).  The seed geometry (phase,
   eps, Omega) is part of the detector, not part of the ambient.
3. **Predicates encode the claim, both polarities.**  A certified
   statement PASSes only when its predicate is true; a FALSE candidate
   is HONEST_NEGATIVE with the measured counter-instance filed.  The
   recurring bug is the predicate that encodes the OPPOSITE (rounds
   17, 23, 25, 27, 31, 32) or compares across containers (set vs
   list, round 36) -- the validator must recompute the numeric law
   from the module's own exported data.
4. **Mean laws are hypotheses, not certificates.**  Every probe-averaged
   claim got a per-placement replay (crowd 29-30, kscale 31, two-block
   damage 36, profile/timecourse 38).  Certified means routinely hide
   placement-level reversals: 147's saturation core inverts to
   rho = 1.13 on one packet address, its far field blows up to 3.375,
   the wipe set changes per placement, and synergy appears where the
   mean said none.  The surviving aggregate forms are re-certified
   from the same run with the original stream replayed digit-for-digit.
5. **Mechanisms are never claimed from one geometry.**  Round 35's
   rel1 invariant and anti-phase resonance were re-swept over
   (eps x Omega) before being generalized -- and were NOT: the frozen
   lock is a low-modulation property that degrades monotonically with
   off-band-center power, and the retention resonance migrates to
   phi = 0 at deeper modulation (round 37).  An anchor geometry is
   replayed for fidelity before the sweep moves off it.
6. **The measurement is the artifact's provenance.**  Every certificate
   carries its domain (width, gens, probes, stream, thresholds), the
   measured numbers, and the original module it replays.  Certificates
   without their measurement context are not certificates.

If a future audit's claim survives the six checks, it may enter the
register; the register is a statement about what was MEASURED under
these rules, one reproducible command at a time.

## What orders the retention resonance

`soliton_mi_retention_mechanism_audit.py` searches for the phase
geometry that orders the retained carrier.  It introduces the second
gauge-invariant angle of the three-wave triangle,
delta = arg(U₀) − (arg(U₊Ω) + arg(U₋Ω))/2 (the carrier's offset from
the sideband phase centroid; every seed starts at delta = 0) and
measures it at the chain-max retention crest of every (Ω, ε) at Ω ∈
{0.5, 1.0}, ε ∈ {0.20, 0.30, 0.45}::

    Omega=1.0   best  P0      Omega=0.5   best  P0
    eps 0.20    p4    0.210   eps 0.20    p6    0.283
    eps 0.30    p0    0.176   eps 0.30    p4    0.500
    eps 0.45    p2    0.277   eps 0.45    p6    0.497

- **The migration re-measures** (round 37, reproduced): at Ω = 1.0
  the retention winner runs φ = π/2 → 0 → π/4 as ε deepens.
- **Deep-band retention crushes band-center**: at every ε the best P0
  at Ω = 0.5 (up to 0.500) roughly doubles the best at Ω = 1.0
  (≤ 0.277).  The retention amplitude is a function of band location,
  peaking deep inside the MI gain band.
- **The phase-closure mechanism fails**: the winners' deltas (−1.070,
  0.260, 2.817, −0.638…) are never the smallest |delta| among crest
  phases.  The carrier is NOT strongest where it re-emerges best
  centered on the sideband phase centroid.
- **rel1 still does not order** (round 35, re-measured across
  geometries): rel1 is conserved, the winner still travels.
- **The retention amplitude bounces**: along the Ω = 1.0 migration the
  winner's P0 is non-monotone in ε (0.210 → 0.176 → 0.277) — midway
  modulation depresses retention.

The mechanism search closes at the discrete-resonance picture: the
retention crest is a sharp, geometry-traveling resonance whose label
is neither rel1 nor the carrier closure delta — the two scalars a
three-wave triangle can carry.

```bash
python soliton_eca/soliton_mi_retention_mechanism_audit.py
python validate_mi_retention_mechanism_audit.py
```

## The closure angle does not close

`soliton_mi_closure_chain_audit.py` asks the round-35 conservation
question of the second gauge-invariant angle: round 39 introduced
delta = arg(U₀) − (arg(U₊Ω) + arg(U₋Ω))/2 and found it does not order
the retention resonance.  Is delta at least FROZEN along each crest
chain, like rel1?  Its full near-cap chains are measured (6 geometries
× 8 phases, R ≥ 2.5, z ≤ 18) with delta at every crest:

- **The triangle carries exactly one frozen angle.**  rel1 agrees with
  itself crest-to-crest to 0.16 rad; delta's worst crest-to-crest
  spread is 2.99 rad (ceiling 0.30) — the carrier's phase rolls
  freely against the sideband phase centroid while the sidebands stay
  locked to each other.
- **The rolling is phase-structured, not wandering noise.**  The
  chain-mean closure delta* ranges ≥ 2.0 rad across phases in every
  geometry, yet in each geometry roughly half the phases (p0-p2, p7)
  stay locked near zero while the others (p3-p5) sweep into −π/2
  … −3 rad.  delta* is a deterministic function of the seed phase —
  unlike rel1's exact 2-phi law, it has no simple formula.
- **delta* still does not label retention** (round 39 re-confirmed at
  the frozen-value level): retention winners are not the ones whose
  closure angle is smallest.

The three-wave triangle carries ONE invariant (the sideband lock
rel1); its other independent scalar — the carrier's offset from the
frozen pair — rolls, and labels nothing.

```bash
python soliton_eca/soliton_mi_closure_chain_audit.py
python validate_mi_closure_chain_audit.py
```

## The damage field's wavenumber spectrum: concentration, not cascade

`soliton_damage_modal_audit.py` carries the round-15 modal audit to the
ECA bus: it Fourier-decomposes the damage field `D_g(i) = clean XOR
damaged` after `g` generations of a single 4-cell block and reduces the
spectrum to its participation ratio `PR = (Σ p_k²)⁻¹` (effective number
of wavenumbers; 1 = one pure line, 512 = white). 512-ring, 8
true-random probes, block position drawn once per probe::

    rule   PR(2)   PR(12)   PR(48)   PR(96)
     204   186.18  186.18   186.18   186.18
      51   186.18  186.18   186.18   186.18
     147   207.05  139.23   102.97    53.10
     172   200.21  337.78   422.40   422.40
     251    64.00    0.00     0.00     0.00

- **The isometry transports conserve the damage footprint exactly**:
  PR(204, g) = PR(51, g) = 186.18 at every sampled generation — the
  flipped-block shape is preserved under both maps, in wavenumber
  space as in Hamming space.
- **The amplifier concentrates**: rule 147's damage spectrum falls
  from 207 to 53 effective wavenumbers, strict in every sampled
  generation. The growing caustic locks onto a few dominant
  wavenumbers — the ECA mirror of the NLSE nonlinear stage locking
  onto the breather's few modes. The direction is the same as the
  round-15 modal law (fewer modes, sharper peak) and opposite to the
  white-noise picture of diffusion.
- **The collapser delocalizes, then stops**: rule 172's PR rises
  200 → 422 and saturates exactly there (422.40 at both 48 and 96) —
  damage spreads across the wavenumber axis as it drains, a finite
  mixing, not a runaway.
- **The eraser's spectrum empties**: PR(251) reaches 0 by generation
  12, consistent with the erase-at-collisions certificate.
- **Honest negative**: "the amplifier's damage spectrum broadens with
  time" fails. 147 concentrates by a factor ~3.9.

```bash
python soliton_eca/soliton_damage_modal_audit.py
python validate_damage_modal_audit.py
```

## Synthesis: the twin map

The project's premise is a *twin construction*: the 32-rule ECA
family whose rules are paired by a resonance condition with the
normalized nonlinear Schrödinger equation is not a metaphor — it is a
testable claim about two dynamical systems sharing one skeleton.  The
audits above certify that claim channel by channel.  Pulling the arc
together, the registered facts are:

**On the ECA side.**  The family is built from 32-rule twins; the
rules split by behavior into exact sectors that are probe-exact, not
mean artifacts: transports {204, 51} are Hamming isometries
placement-by-placement; amplifiers {147} and the one-lap pair
{172, 228} form reach ∩ collapse; the sparse-attractor rules
{36, 219, 251} are extent-erasers (251 an absolute sink, F ≡ 0);
the crowd-additivity intersection is exactly {204, 51, 251}.  Every
certified long-time law survives per-probe and per-placement
re-scopes (rounds 36-40), and honest negatives — the wavenumber
spectrum *concentrates* rather than cascading, the reach ranking does
not persist to large extents — were certified alongside the passes.

**On the NLSE side.**  The modulational-instability stage is
recurrence, not blowup; the cap's crest is a near-universal
R ≥ 2.5 with a frequency-preserving crest lattice; the crest's
amplitude and its modal structure (pump depletion → carrier
recovery) are separated by the (ε, Ω) phase diagram; the nonlinear
stage locks onto the breather's few modes.  Two gauge-invariant
angles of the three-wave triangle were measured: the sideband lock
rel1 = arg(U₊Ω) − arg(U₋Ω) is a *frozen invariant* (crest-to-crest
drift ≤ 0.156 rad, exactly 2φ), while the carrier closure
δ = arg(U₀) − (arg(U₊Ω)+arg(U₋Ω))/2 *rolls* (worst crest spread
2.99 rad) and labels nothing.  The triangle carries exactly one
frozen angle.

**The twin map.**  Direction for direction, the two sides pass the
same laws: concentration, not diffusion; a discrete resonance, not a
continuum; exact sectors, not smooth hierarchies; placewise-exact
measurability, with single numbers (the eraser triple, the retention
winner) earned by means that per-probe spreads sharpen rather than
obscure.

**The discipline.**  Every load-bearing claim is a certificate with a
predicate that encodes the claim — falsehoods certified as honest
negatives — replayed from a reproducible LCG protocol, and
triangulated across ≥ 6 geometries or 8 placements before it enters
the register.  The register below is therefore not a list of beliefs
but a statement about what was measured, one reproducible command at
a time.

## Measurement integrity: the checkerboard probe fix

Several audits seeded random backgrounds from the **low bit** of the LCG,
`next(gen) & 1`. The LCG low bit strictly alternates (0,1,0,1,…) for
odd-multiplier odd-increment generators (ours is `a = 6364136223846793005`,
`c = 1442695040888963407`), so every such "background" was a
checkerboard — two states at most, regardless of probe count. Degenerate
state families produced degenerate certificates:

- **Before the fix**: single-cell family `{51, 68, 76, 179, 204}`;
  far-half amplifiers `{59, 115, 187, 243, 164, 251, …}`; "rule 164 is the
  fastest amplifier (t_far = 4)".
- **After the fix** (LCG high bits, `(seed >> 16) & 1`): the isometry pair
  `{204, 51}` survives exactly; 68/76/179 do not (they were checkerboard
  artifacts); rule 164 and 251 register zero half-reach events; rule 91 is
  a genuine second-ranked amplifier. The corrected results are in the two
  sections above.

All probe-drawing sites — `soliton_damage_audit`, `soliton_bus_stress_audit`,
`soliton_ruleset_audit` and the rewritten `soliton_perturbation_audit` —
now draw high bits; `soliton_behavioral_scale` and
`soliton_ruleset_investigation` already did. `soliton_density_flow_audit`
seeds densities from the low 16 bits of the LCG, a full-period 2^16
subgenerator (well-distributed, no alternation), and is unaffected.

## The algebra of the isometry class: machine-checked theorems

`validate_soliton_isometry_proofs.py`'s predecessor round left the
"isometry class" ambiguous: the universe-census transducer audit
measures a 10-rule class at width 512, while the damage audit's
exhaustive check finds 2 exact ring isometries in the family.  The
census is a sparse probe — `soliton_isometry_proofs.py` settles the
algebra exhaustively with 11 machine-checked theorem certificates:

- **The affine sector is 16, not 8**: over the full width-8 cube, the
  GF(2)-affine rules are exactly `{0, 15, 51, 60, 85, 90, 102, 105,
  150, 153, 165, 170, 195, 204, 240, 255}`.  My first draft claimed
  8 — the exhaustive check corrected the theorem before it registered.
- **The exact ring isometry class is the six rotations**: `{15, 51,
  85, 170, 204, 240}` — 204 the identity, 51 the complement, and the
  four single-bit XOR rotations.  The census's four extras `{154, 166,
  180, 210}` are NOT exact isometries (violated already at
  (0, single-flip), width 8) and are not even bijections at even
  widths — bijective exactly for odd ring widths (verified 6..14:
  `-T-T-T-T-`).  The width-512 "10-rule isometry class" is a
  sparse-probe overstatement: all ten show F(k) = k/512 there because
  the four extras are odd-width bijections and the probe never tries an
  even-width distance pair.
- **The transducer set is exactly the multi-input affine rules**: the
  measured 8-rule transducer class `{60, 90, 102, 105, 150, 153, 165,
  195}` equals the affine rules whose truth tables depend on ≥ 2 of
  {L, C, R}.  The partition is clean: constants `{0, 255}` +
  single-input rotations (the six isometries) + multi-input transducers,
  and the family ∩ six = `{204, 51}`.

```bash
python soliton_eca/soliton_isometry_proofs.py
python validate_soliton_isometry_proofs.py
```

## The linear origin of delta and rel1, and where it dies

The closure angle delta* (= chain-mean of the carrier's offset from
the sideband phase centroid) was a scatter — no a priori prediction
survived.  `soliton_delta_linear_origin_audit.py` asks where delta and
rel1 come from at all, by forcing the Kerr term to zero and watching
the 48 phase-sweep seeds over the full z grid.  Four exact theorems
(result: PASS):

- **Common sideband advance**: the +Ω and −Ω sideband bins rotate with
  a SINGLE shared per-step phase `−ω_bin² dz /2`, verified step-by-step
  to 3e-15.  The two-phase sideband structure rotates rigidly.
- **Seed identity & exact invariance**: rel1 = 2φ at the seed (to the
  0.019 grid/bin discretization) and rel1 is EXACTLY constant over the
  linear stage (worst drift 8.9e-13).  The round-35 freeze of rel1 is
  analytic before any nonlinearity — the difference of two equal
  advances.
- **delta chirps**: delta, the offset from that common phase, advances
  at exactly `+ω_bin²/2` per unit z (1e-9) between branch-flip steps.
  The few flips (0.43% of steps) are structural: `_delta` forms its
  centroid from WRAPPED sideband angles, so when one sideband angle
  sits at its ±π FFT cut the centroid flips by exactly π; every flip
  is collocated with a cut-crossing angle.  So delta is NOT frozen in
  the linear stage — its crest-chain freeze in the Kerr run is a
  nonlinear quasi-equilibrium reached only around focusing.

Two hypotheses about the reach of the linear law were declared in
advance and both REFUTED (HONEST_NEGATIVE): the linear chirp does not
reach the first near-cap crest (median residual 1.33 rad — the first
focusing event injects a phase-dependent Kerr rephasing that dominates
the chirp already by the first crest), and delta* is not the linear
chirp evaluated at the crests' location (max per-geometry |rho| vs
mean-z only 0.515; the missing variable is the integrated Kerr phase
at the crest event).

```bash
python soliton_eca/soliton_delta_linear_origin_audit.py
python validate_soliton_delta_linear_origin_audit.py
```

## The Millennium bridge and the Lean replica

Round 48 places the whole certification explicitly and rigorously
against the Clay Millennium Prize Problems in two mutually checking
deliverables: a machine-checked **bridge audit** (Python) and a
**Lean 4 formalization** (the exact, provable part).

### The bridge audit (Python)

```bash
python soliton_eca/soliton_millennium_bridge_audit.py
python validate_soliton_millennium_bridge_audit.py
```

Eleven certificates. Three **NSE-adjacent laws are PASS** — each is a
rigorously checked *discrete twin* fact, none reaches into the
continuum problem:

- **Crest magnitude control** (`L_mil_nse_crest_control`): at
  (Ω, ε) = (0.5, 0.20) the measured crest 3.663 at z = 3.20 sits in
  the documented 3.656 cap basin and the window maximum stays below
  the 4.0 ceiling — the checked discrete analog of the a-priori
  control NSE regularity demands.
- **Exact mass conservation** (`L_mil_nse_mass_conservation_exact`):
  the Peregrine breather conserves its mass-neutrality identity — the
  window defect `∫(|u|² − P)dt` equals the closed-form correction
  `8PL/(1+PL²)` (P = 1, L = 256) to within 1e-4, and is constant along z =
  0..3 within 1e-4.  The validator re-derives the correction as an
  **analytic closed form**: the symmetric window integral is
  `∫_{−a}^{a}(|u|² − P)dt = 16Pa/(1 + 4Pa²)` with a = L/2 (the
  arctan terms cancel on the symmetric window and only the boundary
  term `x/(2(1+x²))` survives), which at a = L/2 is exactly the
  documented `8PL/(1+PL²)`; the two tails beyond ±a carry `−16Pa/(1+4Pa²)`
  and close the full-line integral to exactly 0 (mass neutrality).
  Measured and exact agree to 1e-4 on both the interior window and an
  extended 16× grid tail scan (plus the closed remainder beyond it).
- **Modal depletion** (`L_mil_nse_modal_depletion`): at the crest the
  pump fraction P0 = 0.229 ≤ 0.25.

Seven **delimitations are PASS on the non-claim** — one per Millennium
problem, each asserts (and mechanically re-scans, then affirms) that
the corpus contains no settlement claim for that problem, and each
shows the closest certified adjacent result:

- **P vs NP**: the width-8 classifiers run in `≤ (2^w)²` exact
  decidable evaluations (a finite P-style verification) — no claim
  about P vs NP.
- **Hodge**: no adjacent fact (decidable combinatorics of 2⁸-cell
  rings only).
- **Poincaré**: already settled (Perelman); this corpus neither relies
  on nor re-proves it.
- **RH**: the exact discrete spectral phase law is a finite-model
  statement about the twin, not about the zeta function.
- **Yang-Mills**: no gauge machinery; discrete conservation laws only.
- **Navier-Stokes**: the three adjacent laws above, all scoped to the
  twin.
- **BSD**: no elliptic-curve machinery.

One **scope-discipline** certificate (`L_mil_scope_discipline`) PASS:
no un-negated, self-attributive resolution line (resolved / solved /
proved / disproof, attached to a problem token from a "we / this
program / certificate" subject) exists in the docs.

### The Lean 4 replica

`C:\Users\Me\Downloads\Puno_Calculus\PunoCalculus` (the companion
PunoCalculus project, toolchain `leanprover/lean4:v4.33.0`) gains two
modules.  `PunoCalculus.EcaIsometry` formalizes the exact ring
semantics (integer states, deterministic step, Hamming distance,
GF(2) XOR, input dependence) and proves — every theorem closed by
`native_decide`, so each is a fully kernel-verified finite
computation, with no axioms and no approximations:

- `affine_is_sixteen`: the affine sector at width 8 is exactly
  `{0, 15, 51, 60, 85, 90, 102, 105, 150, 153, 165, 170, 195, 204,
  240, 255}` (cardinality 16, `count_affine_sector`);
- `isometry_is_six`: the exact Hamming-isometry class is
  `{15, 51, 85, 170, 204, 240}` (cardinality 6);
- `rule204_identity`, `rule51_complement`: 204 is the identity map,
  51 the bitwise complement, on all 256 states;
- `constants_pair`: the constant affine rules are exactly `{0, 255}`;
- `transducer_is_eight`: the multi-input affine rules are exactly
  `{60, 90, 102, 105, 150, 153, 165, 195}`;
- `extras_not_isometry` / `extras_not_bijective_width8`: the census
  extras `{154, 166, 180, 210}` are neither isometries nor bijections
  at width 8;
- `extras_bijective_iff_odd`: over widths 6..14 they are bijections
  exactly for odd widths;
- `six_is_pair_in_family`: the isometry class's family members are
  exactly `{51, 204}`.

A second, stronger sweep (added alongside) closes the classification
as biconditionals over the full rule space and pushes the general
identity-complement pair across ring widths:

- `affine_class_exact`: for every rule `r`, `affineCheck r 8 = true`
  **iff** `r ∈` the 16-rule affine set — a rule-for-rule decision;
- `isometry_class_exact`: for every rule `r`, `isometryCheck r 8` iff
  `r ∈` the 6-rule isometry class;
- `rule204_identity_widths`: rule 204 is the identity on **every state
  of every ring width 4..16** (all `(2^w)` states, closed and
  enumerated);
- `rule51_complement_widths`: rule 51 equals the width-`w` bitwise
  complement `complementGen s w := 2^w - 1 - s` on every state of
  every ring width 4..16.

All are closed by `native_decide` (kernel-verified finite
computations, no axioms).  The general-`w` unbounded inductive form is
now closed too, as structural proofs by recursion on `w`, in mathlib
(via the twin project's `PunoTwin/TwinRingLaws.lean`): the ring facts
themselves were already fully certified on the enumerated domain, and
the recursion extends them to every ring width `w` at once.

The twin's *exact* Continuum/NLSE half is now formalized too, against
mathlib (toolchain/`mathlib` `v4.33.1`, full imports, no axioms):
`C:\Users\Me\Desktop\Mamamogobyerno\fcc2\Millennium-Prize-Problem-Lean-4-Proof\PunoTwin\TwinAnalyticLaws.lean`,
namespace `PunoTwin`, compiles clean with `lake env lean`:

- `rho_eq_structure`: the defect density `rho(t) = |u|^2 - P` equals
  the closed form `8 P (1 - 4 P t^2) / (1 + 4 P t^2)^2`;
- `rho_eq_abs_profile`: `rho` is literally `u^2 - P` for the real
  profile `u(t) = sqrt(P)(1 - 4/(1 + 4 P t^2))`;
- `antiderivative_deriv` / `antiderivative_hasDerivAt`: the closed-form
  antiderivative `t/(1 + 4 P t^2)` differentiates to
  `(1 - 4 P t^2)/(1 + 4 P t^2)^2`, every `t`;
- `window_defect_exact`: `∫ rho over [-a, a]` is exactly
  `16 P a / (1 + 4 P a^2)`, so at `a = L/2` it is `8 P L/(1 + P L^2)`
  (`defect_at_L`) — the machine-anchored closed form the validator
  checks with margin ~2e-5;
- `defect_tendsto_zero`: the window defect → 0 as `a → +∞` (full-line
  mass neutrality, sandwich + `tendsto_zero_iff_norm_tendsto_zero`).

All proofs are analytic (derivative rules, `Deriv`, `intervalIntegral`,
filters) — the mathlib proof of the bridge's exact mass law is complete.

**T2b — the unbounded ring closure.**  The eager record stayed at ring
widths 4..16 by construction (`native_decide` enumerates); the
structural closure for *every* width now lives in mathlib as
`C:\Users\Me\Desktop\Mamamogobyerno\fcc2\Millennium-Prize-Problem-Lean-4-Proof\PunoTwin\TwinRingLaws.lean`,
namespace `PunoTwin`, compiles clean with `lake env lean`.  (The
vendored `PunoCalculus/PunoCalculus/PunoTwin` copies mirror
`github.com/Puronbo/Millennium-Prize-Problem-Lean-4-Proof @
  7d34ba6fba1014114bc2979cf355d31fa496f21b`, mathlib v4.33.1):

- `step204_eq`: the rule-204 step is exactly the width-`w` reading
  `sumBits s w := Σ_j (bit s j)·2^j` (via per-cell `center_bit` and an
  index fold `foldl_sumBits`);
- `step51_eq`: the rule-51 step is exactly the width-`w` componentwise
  complement `compBits s w := Σ_j (1 − bit s j)·2^j`;
- `sumBits_eq`: the reading is the residue `s % 2^w`, by the shift
  recurrences (`sumBits_shift`, `compBits_shift`) rooted at the
  mod-split identity `s % 2^(w+1) = (s % 2) + 2·((s/2) % 2^w)`;
- `compBits_eq`: the complement closes to `(2^w − 1) − (s % 2^w)`;
- `rule204_identity_all`: rule 204 is the identity on every state of
  every ring width (`s < 2^w → step 204 s w = s`);
- `rule51_complement_all`: rule 51 equals `2^w − 1 − s` on every
  state of every ring width.

The enumerated ECA result is therefore no longer the terminus: widths
4..16 certified the facts, the mathlib recursion certifies all widths
at once, and both artifacts are pinned in the same meta register.

**T3 — the certified closed-form numerics.**  Since the simple NLSE twin
is transcendental-free, the floating checks acquire an exact rational
core: `validate_soliton_millennium_closed_forms.py` re-derives every
algebraic fact with `fractions.Fraction` (directed rounding, no new
dependencies):

- the window defect **`D = 2048/65537`** exactly (P = 1, L = 256,
  a = 128), identical to `8PL/(1 + PL²)` — the Lean `defect_at_L`
  identity, equality of rationals;
- the antiderivative rendering `D = 8P (G(a) − G(−a))`, exact;
- `D` is pinned to width **1e-16** (vs the validator's 1e-4 tolerance),
  and the measured grid sums at z = 0 sit inside `[D − 1e-4, D + 1e-4]`;
- the outer-tail remainder beyond the 16× grid is the exact rational
  `65536/67108865`, **strictly below** the window defect
  (cross-multiplied integers), so the extended-grid closure is a
  quantified, strict descent to 0;
- record (masked) enclosures of the crest printouts — those are the
  deterministic measurements, *not* derived bounds: crest 3.6631 sits
  strictly above the 3.656 basin threshold (margin ≥ 7e-3), crest record
  in `[3.5, 3.9]`, max `< 4.0`, and `P0 ≤ 0.25` with margin ≥ 2e-2.

No Millennium problem is asserted settled here — certified quantities of
the twin mass law only; the seven delimitations live with the bridge
validator.

**T4 — the MP-Operator discriminant bridge (mathlib `v4.33.1`).**  The
window denominators `1 + 4 a²` that appear in T3 are `PunoTwin` hashes of a
`Derivative + Antiderivative` operator spectrum.  The mathlib file
`PunoTwin\MPOperator.lean` (namespace `PunoTwin.MPOperator`, zero-unproved
proofs) formalizes `A_{α,β} = αD + βV` with `D = d/dx`, `V = ∫₀ˣ`, whose
eigenvalue equation `α f″ − λ f′ + β f = 0` has discriminant `Δ = λ² − 4αβ`:

- `operator_discriminant_bridge`: the family `(α,β,λ) = (1, a, 2a+1)` gives
  `Δ = (2a+1)² − 4a = 4a² + 1 = 1 + 4a²`, exactly the T3 denominator;
- `window_discriminant_closed_form`: at `a = 128`, `Δ = 65537`
  (`(2·128 + 1)² − 4·128 = 65537`) — the `2048/65537` window defect is
  therefore `16P·a/Δ` at `P = 1`;
- `tail_discriminant_closed_form`: at `a = 4096`, `Δ = 67108865` — the same
  bridge for the `65536/67108865` tail remainder;
- `fermat_denominator_window`: `1 + 4·128² = 2¹⁶ + 1` (a Fermat number);
- `window_discriminant_pos`: `Δ > 0` for the window parameter, so the
  characteristic polynomial has two distinct real roots — the eigenspace is
  one-dimensional;
- `defect_is_double_antiderivative`: `16P·a/(1+4P·a²) = 2·(8a/(1+4a²))`,
  `tail_is_double_antiderivative`: the same 2× evaluation of the
  antiderivative at `a` and `b = 4096` — the mass law re-expressed as twice
  `Vρ(a)`;
- `antiderivative_first_order_law`: the mass-law antiderivative
  `u(t) = t/(1+4Pt²)` satisfies the exact first-order rational ODE
  `(1 + 4Pt²)·u′(t) + 8Pt·u(t) = 1` for every `t`, `P > 0` (stated with the
  closed-form derivative from `TwinAnalyticLaws.antiderivative_deriv`).  This
  is distinct from the exponential eigen-ODE of `A_{α,β}` — the defect ratio
  pie bridge is an *arithmetic denominator* match, not an analytic
  eigenfunction claim;
- (exact-number footnote) `65537 = 2¹⁶ + 1` is a Fermat **prime**, whereas
  `67108865 = 2²⁶ + 1 = 5·53·157·1613` is **composite** — the "Fermat number"
  wording applies only to the window denominator;
- `mass_radius_identity`: the defect's mass-radius product is exactly
  `D(a)·a = 16a²/(1+4a²) = 4 − 4/(1+4a²)`, so `D(a)·a + 4/(1+4a²) = 4` —
  the mass ceiling **4** bounds the product for every half-window, and at
  `a = 128` the certified rationals give `262144/65537` (with `4/65537` as
  the remainder) — the celebrated window defect is `4` decomposed against
  the denominator;
- `mass_radius_window`: `D(128)·128 = 262144/65537` (rational, exact);
- `mass_radius_tail`: `D(4096)·4096 = 268435456/67108865` (rational, exact),
  keeping the tail product strictly below the mass ceiling 4 by the positive
  remainder `4/(1+4·4096²) = 4/67108865`;
- `mass_radius_tail_lt_ceil`: the explicit ceiling bound `D(4096)·4096 < 4`
  (norm_num), the tail product strictly below the mass ceiling;
- `bridge_discriminant_never_negative`: the bridge-family discriminant
  `4a² + 1 > 0` for every real `a` — the Δ = 0 double-root point and the
  Δ < 0 complex-conjugate (oscillatory) regime exist in the general algebra
  `A_{α,β}`, but never on this exact bridge;
- `bridge_discriminant_window_pos`: `65537 > 0` at `a = 128` explicit;
- `char_poly_at_half`: the window-`a` characteristic polynomial
  `P(1/2) = (1/2)² − (2a+1)·(1/2) + a` equals `−1/4` **exactly, for every
  `a`** — so with leading coefficient 1 the spectral midpoint 1/2 lies
  strictly between the two roots: `r₂ < 1/2 < r₁`.  The small root is
  therefore always contractive below 1/2, the algebraic gap behind the
  mass ceiling 4 (`char_poly_at_half_window` restates at `a = 128`);
- `char_poly_at_zero` / `char_poly_at_one` / `char_poly_at_twice_window`:
  the exact, `a`-proportional evaluations `P(0) = a`, `P(1) = −a`,
  `P(2a+1) = a` for every half-window;
- `spectral_bracket_window` (Round 55): at `a = 128` the four exact
  evaluations `P(0) = 128`, `P(1/2) = −1/4`, `P(1) = −128`,
  `P(2a+1) = 128` certify the sign alternation that, with the
  upward-opening leading coefficient, brackets the two roots
  `0 < r₂ < 1/2 < r₁ < 2a+1` — the spectral bracket;
- `bridge_discriminant_square_squeeze` (Round 56): for every real
  `a > 0` the discriminant Δ = 4a² + 1 is sandwiched strictly between
  the squares `(2a)²` and `(2a+1)²`; with monotone square root this is
  the bare-hands `2a < √Δ < 2a+1` behind the bracket, with
  `bridge_discriminant_square_squeeze_window` (`65536 < 65537 < 66049`)
  and `bridge_discriminant_square_squeeze_tail`
  (`67108864 < 67108865 < 67125249`) stating the exact rational
  squeeze at both certified windows;
- `bridge_discriminant_tight_upper_square` (Round 57): the upper
  endpoint of the squeeze refines to `2a + 1/(4a)`, whose square exceeds
  the discriminant by exactly `1/(16a²)` — the tight rational lid
  `r₁ − r₂ = √Δ < 2a + 1/(4a)`;
- `bridge_discriminant_tight_upper_square_window` /
  `_tail`: at `a = 128` the lid is `65537 + 1/262144`, at `a = 4096`
  `67108865 + 1/268435456` — one part in 2¹⁸ / 2²⁸;
- `discrim_gap_quarter_scaling`: the gap shrinks by exactly 1/4 when
  the half-window doubles — the 32× window→tail step (4096 = 32·128)
  tightens the gap by 2⁻¹⁰;
- `vieta_midpoint_bracket` (Round 58): for any two roots `r₁, r₂` of the
  characteristic polynomial, the product of signed distances from the
  spectral midpoint is exactly `−1/4`, independent of `a` — so the
  midpoint lies strictly between the roots: `r₂ < 1/2 < r₁`;
- `bridge_gap_square_squeeze` + `_window`/`_tail`: the identity
  `(r₁−r₂)² = Δ = 4a²+1` (pure Vieta) is pinched, for every `a > 0`,
  between `(2a)²` and the tight lid `(2a+1/(4a))²` — the
  ordering-free form `2a < |r₁−r₂| < 2a + 1/(4a)` of the spectral-gap
  shadow; at the certified windows: `65536 < (r₁−r₂)² < 65537 + 1/262144`
  and `67108864 < (r₁−r₂)² < 67108865 + 1/268435456`;
- the Round 59 mirror/harmonic/bracket bundle (all `ℝ`, all closed):
  - `spectral_midpoint_distance_sum/_prod`: the two signed distances
    from the spectral midpoint `1/2` sum to `2a` and multiply to `−1/4`,
    so they are the two roots of the mirror quadratic
    `z² − 2a·z − 1/4 = 0`;
  - `spectral_midpoint_between_roots`: `(1/2 − r₁)(1/2 − r₂) < 0` — the
    midpoint lies strictly between the roots, universally;
  - `spectral_distance_mirror_quadratic` +
    `mirror_quadratic_discriminant_is_bridge`: the mirror quadratic
    carries exactly the bridge discriminant `4a² + 1 = Δ`;
  - `spectral_reciprocal_sum_law` (+`_window`/`_tail`): the reciprocal
    roots sum to `2 + 1/a`; at the certified windows `1/r1 + 1/r2 =
    2 + 1/128` and `1/r2`-twin-`1/r1`-sum `= 2 + 1/4096` (ASCII:
    `1/r1 + 1/r2 = 2 + 1/a`, `2 + 1/128`, `2 + 1/4096`);
  - `spectral_roots_bracket_explicit` (+`_window`): under the standard
    ordering `r₂ < 1/2 < r₁` the full rational bracket
    `0 < r₂ < 1/2 < r₁ < 2a+1` is proved for every `a > 0` (ASCII:
    `0 < r2 < 1/2 < r1 < 2a+1`) — the R55 sign analysis, closed;
- the Round 60 operator composition law (all `ℝ[X]`, all closed):
  the MP pair is realized exactly on the polynomial model by
  `D = Polynomial.derivative` and the antiderivative
  `V g = Σₙ cₙ xⁿ⁺¹/(n+1)` (`noncomputable def integral`), with
  `derivative_integral` proving `D(Vp)=p` and
  `integral_derivative_sub_eval0` proving `V(Dp)=p-C(p.coeff 0)`, so
  the anticommutator defect `anticommutator_defect` is
  `DV+VD=2id-E0` (ASCII: `D(Vp)=p`, `V(Dp)=p-C(p.coeff 0)`,
  `DV+VD=2id-E0`);
  - `operator_square_commutation_defect`: for every `α, β ∈ ℝ` and
    polynomial `g`, `A_{α,β}² g = α² D² g + αβ(2g − g(0)) + β² V² g`
    — the exact composition law, closed by linearity of D and V and the
    two commutation relations (ASCII form:
    `A^2 g = a^2 D^2 g + ab(2g-g(0)) + b^2 V^2 g`);
  - `operator_square_bridge_family`: at `α = 1, β = a` — the operator
    form behind the characteristic equation `λ² − (2a+1)λ + a = 0`.
- the Round 61 reverse-Collatz spine (`PunoTwin.CollatzReach`,
  zero-unproved, **NOT SETTLED BY THIS PROJECT** for the full
  conjecture — only the spine family, step identities, and finite
  L1..L7 corridors are certified): `collatzStep` is the standard step
  `x/2` (even) / `3x+1` (odd); `odd_step_even` proves the odd step
  always lands even, `3 * (2 * k + 1) + 1 = 2 * (3 * k + 2)` (ASCII:
  `3*(2k+1)+1=2*(3k+2)`), the root of the reverse branching at `2y`
  and `(y-1)/3`;
  - the integer condition `m = (n*2^k-1)/3` (i.e. `3m+1 = n*2^k`):
    for `n = 1` it forces `2^k ≡ 1 (mod 3)`, `k` even —
    `two_pow_even_mod_three` (`(2 ^ (2 * j)) % 3 = 1`) against
    `two_pow_odd_mod_three` (`(2 ^ (2 * j + 1)) % 3 = 2`);
  - the spine family `spine k = (4^(k+1)-1)/3` (ASCII `(4^j-1)/3`),
    exact division `spine_eq_spineSum` via `geom4_identity`, inverse
    of the odd step (`spine_identity`: `3 * spine k + 1 = 4 ^ (k + 1)`),
    always odd (`spine_odd`);
  - `spine_reaches_one`: every spine element descends to `1` in
    exactly `2(k+1)+1` steps — one `3x+1` onto a power of two, then
    the halving corridors `halve_corridor`;
  - `reverse_tree_levels` (`native_decide`): the reverse-tree census
    L1..L7 collapses to 1, `L5: 5,32 | L6: 10,64 | L7: 3,20,21,128`
    (ASCII pins `L5: 5,32`, `L6: 10,64`, `L7: 3,20,21,128`).
- `mass_radius_window_lt_tail`: `262144/65537 < 268435456/67108865` — the
  mass-radius product rises strictly from window to tail, closing in on the
  ceiling 4.
- `window_discriminant_real_pos`: the bridge-family discriminant
  `1 + 4a² ≥ 1 > 0` for every real `a` — the two-root spectral picture
  never crosses into the Δ = 0 or Δ < 0 regime on the mass law;
- `vieta_discriminant`: `(r₁+r₂)² − 4r₁r₂ = (r₁−r₂)²` universally — the
  Vieta form of the bridge identity `(2a+1)² − 4a = Δ`;
- **E8 (discrete ±1 pairs):** the width-8 isometry class is exactly the
  three XOR-complement pairs `(15, 240), (51, 204), (85, 170)` — each rule's
  bitwise complement `255 − r` is its mate in the class, so every pair is an
  identity/complement pair of its own two-sided orbit (Lean
  `isometry_class_three_pairs`, `native_decide`).

`PunoCalculus.MillenniumBridge` then records, as closed decidable
statements and explicit prose, the pairing with the seven Millennium
problems: `statuses` declares each problem `NOT SETTLED BY THIS
PROJECT` (theorem `seven_problems_declared_unsolved`), and the exact
P-style counts are restated per problem as the adjacent certified
facts (`pnnp_adjacent_classification`, `pnnp_adjacent_isometry_count`,
`rh_adjacent_finite_sector`).  `lake build` completes (32 jobs); the
executable prints all checks:

```text
  [ECA] width-8 ring algebra (exact, native_decide theorems):
    affine sector is the 16 low-degree rules:        true
    isometry class is the 6 rotations:               true
    rule 204 identity all-states:                    true
    rule 51 complement all-states:                   true
  [MillenniumBridge] seven problems declared NOT settled here:
    statuses length: 7
    taxonomy: [P_NNP (P vs NP), HODGE, POINCARE, RH, YANG_MILLS, NAVIER_STOKES, BSD]
```

The bridge is honest by construction: the 87-check suite runs this
round with the three NSE-adjacent laws, the T3 closed-form certificate,
the T4 bridge-meta audit, and the scope discipline as additional
certificates, and nothing anywhere asserts — explicitly or by status
convention — that a Millennium problem has been resolved.

## Audit register

One command reproduces the entire certification: unit suite, all 86
root validators, and every ticket across the rounds.

```bash
python run_all_audits.py
```

The registers above (rounds 5–11) pin the family's measured laws:
`{204, 51}` are the exact Hamming isometries; the width-16 half-reach
sector is 13 rules led by 147; the affine 8 are the universe's
large-extent transducers (absent from the family); `{36, 219, 251}`
are variance-sparse basins, extent-erasers and instant wipers; 147 is
the unique persistent grower and the unique short-range collision
saturator (whose deficit builds late in time after a constructive
transient, with a flat-bottom interaction potential that recovers
over an ~64-cell halo); the isometry pair carries two blocks with zero
interaction at any distance and at every generation; the NLSE side
closes with the Peregrine breather (exact seed, mass-neutrality
`8PL/(1+PL²)`, phase law `arg(4P²z²−3−8iPz)`, P-scaling), the MI
recurrence laws of this round, the frequency-localized crest cap
(Ω = 0.5 crests at 3.656, above the bound 3), the wavelength-monotone
crest spectrum (2.476 → 4.697, the cap dividing the band at
Ω ∈ (0.785, 1.0)), the amplitude law (crest rises in ε everywhere; the
deep band breaks the cap at every ε, the dividing frequency rises
with ε), the modal law (at the crest the pump is depleted — P0 ≤ 0.25,
the sideband pair dominates, and the carrier + fundamental core is
capped at 0.44; the > 77% two-mode coherence of the round-15 report was
a late-window measurement and now carries that scope), and the (ε, Ω)
phase
diagram of the breaking line (rising in ε, with a secondary crest
bump at Ω = 0.9 and a weak-seed deep lag).  On the ECA side the
damage spectrum closes with the wavenumber law (207 → 53); the
round-15 blue-yellow modal audit now split the damage field's spatial
spectrum.  On the NLSE side the modal audit is corrected (the crest
depletes the pump: P0 ≤ 0.25; the ≥ 77% two-mode coherence report was
a late-window measurement), and the recurrence-chain audit shows the
depletion is a crest-arrival property (P0 ≤ 0.40 over 11 crests)
while the spectral mix never repeats.)  The certificate culture now
stands on three mechanical guards: the contract audit (inversion
class), the vacuity battery (insensitive predicates — all 27
registered certificates flip under its mutants), and the
pre-registered delta* sweep (two of four a priori predictions refuted:
the near-zero sector of delta* migrates with geometry, and the far
phases are not uniformly negative — p6 turns positive in four of six
geometries).  Round 47 adds the algebra of the isometry class (the
affine sector is the sixteen low-degree rules; the exact ring
isometry class the six rotations `{15, 51, 85, 170, 204, 240}`; the
census's four extras are odd-width-only bijections; the transducers
are exactly the multi-input affine rules) and the linear origin of the
closure angle (common sideband rotation at `−ω_bin²/2` makes rel1
exactly invariant and delta chirp `+ω_bin²/2` in the linear stage,
while both hypotheses that the linear law reaches the crests are
refuted).  Round 48 adds the Millennium bridge — three NSE-adjacent
certified discrete laws (crest control 3.663 in the 3.656 basin, exact
mass-neutrality `8PL/(1+PL²)` conserved to 1e-4, crest pump fraction
0.229 ≤ 0.25), seven scope delimitations (no settlement claim for any
Millennium problem), and a scope-discipline check — together with the
Lean 4 replica (`PunoCalculus.EcaIsometry`, every theorem closed by
`native_decide`; `PunoCalculus.MillenniumBridge`, all seven problems
declared NOT SETTLED explicitly).  The bridge's mass law is anchored
to its analytic closed form (`∫_{−a}^{a}(|u|²−P)dt = 16Pa/(1+4Pa²)`),
now proved in mathlib (`PunoTwin.TwinAnalyticLaws`: density structure,
square-profile identity, antiderivative derivative, exact window
defect, AND line-mass neutrality), and the Lean isometry module gains
rule-for-rule biconditional classifications plus the identity-
complement pair across all states of ring widths 4..16.  Round 49 adds
the T3 exact-numerics certificate (`validate_soliton_millennium_closed_forms.py`):
the window defect is the exact rational `2048/65537` (pinned to 1e-16,
equal by exact rational arithmetic to `8PL/(1+PL²)` — `defect_at_L`),
the outer-tail remainder `65536/67108865` is strictly below it by
cross-multiplied integers, and the crest/P0 records sit in masked 4-digit enclosures (`3.6631 > 3.656`
basin, `P0 ≤ 0.25`).  Round 50 adds the T4 bridge-meta audit
(`validate_soliton_millennium_meta_audit.py`): it greps the real Lean
sources (`EcaIsometry`, `MillenniumBridge`, `PunoTwin.TwinAnalyticLaws`)
and the docs for every theorem name and certified rational, and refuses
any settlement phrasing anywhere — the suite now stands at **86 root
validators**.  Round 51 closes the general-width pass at the Lean level:
`PunoTwin.TwinRingLaws` (`step204_eq`, `step51_eq`, `sumBits_eq`,
`compBits_eq`, `rule204_identity_all`, `rule51_complement_all`)
extends the enumerated identity/complement facts from widths 4..16 to
every ring width by structural recursion in mathlib, with the same
`native_decide` file kept as the kernel-verified eager certificate.
Round 52 expands the MP-operator register with the exact algebraic core
beneath the mass law: `antiderivative_first_order_law` (the first-order
rational ODE `(1+4Pt²)u′ + 8Pt·u = 1` — honest, distinct from the
exponential eigen-ODE), `mass_radius_identity`/`mass_radius_window`/
`mass_radius_tail` (the mass ceiling: `D(a)·a = 4 − 4/(1+4a²)`, with the
certified window `262144/65537` and tail `268435456/67108865`),
`window_discriminant_real_pos` (the two-root regime never leaves the
disc), `vieta_discriminant` (the Vieta bridge `(r₁+r₂)² − 4r₁r₂`), plus
the discrete transpose `complement_is_involution` and
`isometry_class_three_pairs` — the {204, 51} ±1 eigensquare and the three
XOR-complement pairs of the width-8 isometry class.  Round 53 closes the
monotonicity of the mass-radius product between the two certified windows:
`mass_radius_window_lt_tail` shows `262144/65537 < 268435456/67108865`,
confirming the product rises strictly toward the ceiling 4 as the half-
window grows; `mass_radius_tail_lt_ceil` makes the strict bound explicit.
The dyadic pattern `D(2^k) = 2^(k+4)/(2^(2k+2)+1)` at every power-of-two
window is noted in the register (already implicit in `mass_radius_identity`
evaluated at `a = 2^k`); the denominator `2^(2k+2)+1` is a Fermat number
if and only if `2k+2 = 2^(2^j)` for some `j ≥ 0`, which happens exactly
at the known Fermat primes `F₁ = 5`, `F₂ = 17`, `F₃ = 257`, `F₄ = 65537`
(window), with `F₅ = 4294967297` composite — a number-theoretic fact left
outside the certified core but pinned in the doc as register context.
Round 54 adds the spectral-gap theorem `char_poly_at_half`: the bridge
characteristic polynomial `P(r) = r² − (2a+1)r + a` evaluates at the
spectral midpoint to `P(1/2) = −1/4` **for every half-window `a`**, so
the small eigen-root is strictly contractive (`r₂ < 1/2 < r₁` for all
`a > 0`) and the mass ceiling 4 restates exactly the algebraic gap
between the midpoint 1/2 and the expansive root — the classical
open-upward argument (leading coefficient 1) anchors the bound with a
single exact rational, `−1/4`, unchanged across the whole certified
window.  `char_poly_at_half_window` restates the fact at `a = 128`.
Round 55 completes the spectral bracket: `char_poly_at_zero`,
`char_poly_at_one` and `char_poly_at_twice_window` certify the exact
`a`-proportional evaluations `P(0) = a`, `P(1) = −a`, `P(2a+1) = a`;
together with the Round 54 midpoint `P(1/2) = −1/4` and the upward-
opening leading coefficient, the four sign locations pin the two roots
inside `0 < r₂ < 1/2 < r₁ < 2a+1` for every `a > 0`.  The composite
`spectral_bracket_window` restates all four exact evaluations at the
certified window `a = 128` in one decidable statement.
Round 56 adds the square-squeeze of the discriminant: for every real
`a > 0`, `Δ = 4a² + 1` lies strictly between `(2a)²` and `(2a+1)²`, the
bare-hands statement that `2a < √Δ < 2a+1` (no overt radicand lemma) —
exactly what pins `0 < r₂ < 1/2 < r₁ < 2a+1`; the window and tail forms
`65536 < 65537 < 66049` and `67108864 < 67108865 < 67125249` give the
tightest exact rational brackets at the two certified windows.
Round 57 adds the tight rational lid on the discriminant interval: the
upper endpoint of the squeeze refines from `2a+1` to `2a + 1/(4a)`,
whose square exceeds the discriminant by exactly `1/(16a²)` — bounding
the spectral shadow `r₁ − r₂ = √Δ < 2a + 1/(4a)`.  At the certified
windows the lid is exact: `65537 + 1/262144` (a = 128, one part in
2¹⁸) and `67108865 + 1/268435456` (a = 4096, one part in 2²⁸).
`discrim_gap_quarter_scaling` certifies the exact law the gap obeys: it
shrinks by 1/4 per doubling, so the 32× window→tail step (4096 = 32·128)
tightens the gap by 2⁻¹⁰.
Round 58 completes the rational shadow of the spectral gap.  Vieta's sum
and product for the characteristic polynomial yield, for any two roots,
the exact midpoint bracket `(1/2 − r₁)(1/2 − r₂) = −1/4`, independent of
`a` — the midpoint lies strictly between the roots
(`r₂ < 1/2 < r₁`).  The squared spectral gap `(r₁−r₂)² = Δ = 4a²+1`,
a pure Vieta identity, is then pinched by the square-squeeze and the
tight lid into the ordering-free shadow `2a < |r₁−r₂| < 2a + 1/(4a)`
for every `a > 0`; at the certified windows this reads
`65536 < (r₁−r₂)² < 65537 + 1/262144` and
`67108864 < (r₁−r₂)² < 67108865 + 1/268435456`.  In ASCII:
`65536 < (r1-r2)^2 < 65537 + 1/262144` and
`67108864 < (r1-r2)^2 < 67108865 + 1/268435456`.
Round 59 closes the spectral-core register with three exact laws in
`ℝ`.  Mirror law: the two signed distances from the spectral midpoint
sum to `2a` and multiply to `−1/4`, so they are the two roots of the
mirror quadratic `z² − 2a·z − 1/4 = 0`, whose discriminant is exactly
the bridge discriminant `4a² + 1 = Δ`.  Harmonic law: the reciprocal
roots satisfy `1/r₁ + 1/r₂ = 2 + 1/a`; at the certified windows
`2 + 1/128` and `2 + 1/4096`.  Explicit bracket: under the standard
root ordering `r₂ < 1/2 < r₁`, the sign-analysis window
`0 < r₂ < 1/2 < r₁ < 2a+1` (ASCII `0 < r2 < 1/2 < r1 < 2a+1`) is proved
for every `a > 0` — closing, by `field_simp`/`positivity`, what Round 55
asserted for the polynomial evaluations alone.
Round 60 lifts the operator pair to the polynomial model
(`Polynomial ℝ`): `D = Polynomial.derivative` and the exact discrete
antiderivative `V`, which divides the coefficient of `Xⁿ` by `(n+1)`.
The two commutation relations are proved by coefficient arithmetic
(backbone: `integral_coeff_zero`/`integral_coeff_succ` +
`Finset.sum_ite_eq` + `mem_support_iff`): `derivative_integral` proves
`D(Vp)=p`, `integral_derivative_sub_eval0` proves `V(Dp)=p-C(p.coeff 0)`
(ASCII: `D(Vp)=p`, `V(Dp)=p-C(p.coeff 0)`), and therefore
`anticommutator_defect` gives the twist `DV+VD=2id-E0`
(ASCII `DV+VD=2id-E0`; E0 is evaluation at zero, `E₀ g = g(0)`).
Squaring the MP operator `A_{α,β} = αD + βV` then collapses through the
linearity facts (`integral_add`, `integral_C_mul`, `derivative_C_mul`)
into `operator_square_commutation_defect`:
`A_{α,β}² g = α² D² g + αβ(2g − g(0)) + β² V² g`
(ASCII `A^2 g = a^2 D^2 g + ab(2g-g(0)) + b^2 V^2 g`) — the exact
operator form behind the characteristic equation `λ² − (2a+1)λ + a = 0`,
made fully proved in `operator_square_bridge_family` at `α = 1, β = a`.
Every statement is closed by `ring`/`field_simp`/`positivity`, zero
`sorry`/`axiom`.

Round 61 adds the closed-form **spine family of the reverse Collatz
tree** (`PunoTwin.CollatzReach`).  `collatzStep` is the standard step
`x/2` for even `x`, `3x+1` for odd `x`.  The odd step always lands on
an even number — `odd_step_even`: `3 * (2 * k + 1) + 1 = 2 * (3 * k +
2)` (ASCII `3*(2k+1)+1=2*(3k+2)`) — which is the root reason the
reverse-nodes branch at `2y` and `(y-1)/3`.  For `n = 1` the integer
condition `m = (n*2^k-1)/3` (i.e. `3m+1 = n*2^k`) forces `2^k ≡ 1
(mod 3)`, hence `k` even: `two_pow_even_mod_three`
`(2 ^ (2 * j)) % 3 = 1` against `two_pow_odd_mod_three`
`(2 ^ (2 * j + 1)) % 3 = 2`.  The resulting inverse family is the
spine `spine k = (4^(k+1)-1)/3`, an exact division
(`spine_eq_spineSum` via `geom4_identity` `4^(k+1)=3*spineSum(k)+1`)
and inverse of the odd step (`spine_identity` `3 * spine k + 1 = 4 ^
(k + 1)`; `spine_odd` keeps each member odd so the `3x+1` step applies
first).  `spine_reaches_one` proves every spine element descends to 1
in exactly `2(k+1)+1` steps — one `3x+1` onto a power of two, then `k`
halving corridors (`halve_corridor`).  `reverse_tree_levels` pins the
reverse-tree census L1..L7 by computation (`native_decide`):
`L5: 5,32 | L6: 10,64 | L7: 3,20,21,128`.  The full conjecture — that
*every* positive integer lies in the tree rooted at 1 — remains
**NOT SETTLED BY THIS PROJECT**; only the spine family, the step
identities, and the finite L1..L7 corridors are certified here.

Round 62 adds the **provable spine of the Dirichlet L-function laws**
(`PunoTwin.DirichletLaws`, mathlib `v4.33.1`, zero-unproved).  The
L-function half-plane universality claims of Project Puno remain **NOT
SETTLED BY THIS PROJECT**; only the mathlib-closed spine is certified:

- **functional equation at `s = 1/2`** for every primitive `χ`:
  `center_symmetry` gives `Λ(χ,1/2) = rootNumber χ · Λ(χ⁻¹,1/2)`
  (via mathlib's `IsPrimitive.completedLFunction_one_sub`);
- **Euler product** (`eulerProduct_tprod`): the Dirichlet series
  `L(s,χ)` splits as `∏ₚ (1 − χ(p) p^{−s})⁻¹` on the convergent
  half-plane;
- **special values at negative integers** (`zeta_neg_nat`):
  `ζ(−k) = (−1)ᵏ·Bₖ₊₁/(k+1)` — examples `ζ(−4) = B₅/5` and
  `ζ(2) = π²/6`;
- **concrete primitive quadratic characters**: `χ₄`, `χ₈`, `χ₈'`
  (from `ZMod.χ₄/χ₈/χ₈'`, lifted to `ℂ`) are proved primitive —
  `χ₄ℂ.conductor_eq_four`, `χ₈ℂ.conductor_eq_eight`,
  `χ₈'ℂ.conductor_eq_eight` — so `center_symmetry` applies at `1/2`
  for each;
- **parity (trivial-zero) law**: `χ₄` and `χ₈'` are odd, `χ₈` even
  (`χ₄ℂ_odd`, `χ₈ℂ_even`, `χ₈'ℂ_odd`), giving the trivial zero laws
  `L(χ₄, negative odd) = 0`, `L(χ₈, negative even) = 0`, and
  `L(χ₈', negative odd) = 0` as examples;
- **von Staudt–Clausen + Fermat-spike lattice**
  (`vonStaudt_B16`, `spike_law`, `spike_5_prime/cond`,
  `spike_17_prime/cond`, `spike_257_prime/cond`,
  `spike_65537_prime/cond`): `B₁₆ +
  ∑_{p−1|16} 1/p ∈ ℤ`, and the spike lattice `p = 2^(2^j)+1`
  spikes in `B_{2k}` exactly when `2^(2^j−1) | k` — the instances
  `5 ↔ 2|k`, `17 ↔ 8|k`, `257 ↔ 128|k`, `65537 ↔ 2^15 | k` are the
  Bernoulli-side echo of the Fermat denominators `1+4a²` certified in
  `MPOperator.lean`.  The `fermat_bridge` lemma closes the loop
  exactly: at `a = 2^(2^k−1)` the `MPOperator` window denominator is
  `1 + 4a² = 2^(2^(k+1)) + 1`, so `a = 2` → `17`, `a = 8` → `257`,
  `a = 128` → `65537` — the `k=3`/`a=128` instance is precisely
  `MPOperator.fermat_denominator_window`.

No Millennium problem is asserted settled; the exact transcendental
identities (e.g. `L(2,χ₋₄) = G`) and the universality claims stay
outside the certified core, pinned here as register context only.

## Native ramp primitives

`ramp(x)` is the positive native ramp expressed as a sign gate:

```python
x * (x > 0)
```

`negative_ramp(x)` provides the complementary negative branch:

```python
x * (x < 0)
```

The comparison is kept explicit so the primitives can map directly to a branchless dataflow or hardware implementation.

## Soliton-bus architecture

A **soliton** is a localized immutable message carrying a bus name, spatial position, binary value, and generation number. A `SolitonBus` is a FIFO transport. Every `EcaCell` receives three neighborhood solitons, forms the 3-bit neighborhood index, looks up the corresponding rule bit, and emits exactly one output soliton.

`SolitonECA.step()` injects all neighborhood frames before consuming outputs. This barrier makes the update synchronous, as required by ECA semantics, while keeping all computation and state transfer on soliton buses. Finite-grid boundaries are zero-valued ghost solitons.

## Usage

```python
from soliton_eca import SolitonECA, evolve

machine = SolitonECA(204, width=31, initial=[0] * 15 + [1] + [0] * 15)
for state in machine.run(10):
    print("".join("#" if bit else "." for bit in state))

# Or collect all emitted generations.
rows = evolve(4, [0, 0, 0, 1, 0, 0, 0], generations=8)
```

Run the regression suite from this directory with:

```bash
cd .. && python3 -m pytest -q soliton_eca/test_soliton_eca.py
```

## Soliton neural network

`SolitonNeuralNetwork` is a dense, synchronous feed-forward network. Each
weighted connection is a `WeightedSolitonBus`; each neuron waits for all
incoming synaptic solitons, adds a bias, applies the native positive ramp, and
emits one activation soliton. Training uses online squared-error
backpropagation and the piecewise derivative of the ramp.

```python
from soliton_eca import SolitonNeuralNetwork

net = SolitonNeuralNetwork((2, 4, 1), seed=11)
losses = net.train(
    [((0.0, 0.0), (0.0,)), ((0.0, 1.0), (1.0,)),
     ((1.0, 0.0), (1.0,)), ((1.0, 1.0), (0.0,))],
    epochs=200,
    learning_rate=0.03,
)
prediction = net.forward((1.0, 0.0))
```

The neural architecture is dependency-free and uses a deterministic internal
pseudo-random initializer. The physics digital twin additionally uses NumPy.

## Rigorous soliton prototype

`soliton_protocol.py` defines an explicit packet contract:

```text
(tick, position, velocity, amplitude, channel, phase)
```

`SolitonLattice` implements synchronous transport, reflective or annihilating
boundaries, event logging, and collision modes for XOR, signed summation, and
destructive cancellation. This makes routing testable before mapping it to
optical or neuromorphic hardware.

`soliton_physics.py` provides a generalized nonlinear Schrödinger digital twin
using a symmetric split-step Fourier method. The normalized fundamental pulse
`sech(t)` is used as the first invariance benchmark. `soliton_validation()`
returns relative power-envelope error and relative energy drift.

Run the expanded checks from the project root:

```bash
python3 soliton_eca/validate.py
python3 soliton_eca/validate_rigorous.py
```

The intended development order is: validate propagation, validate packet
routing primitives, add signed weighted mixing, measure a real activation
transfer function, then introduce learning and hardware-in-the-loop
calibration. Accuracy alone is insufficient; report timing error, packet loss,
crosstalk, drift, BER/SER, energy per event, and end-to-end latency.

## Signed differential mixing

`DifferentialEncoder` represents a signed scalar as two explicitly routed
channels: positive and negative. This avoids the invalid assumption that
optical intensity can directly represent a negative weight. `CalibratedMixer`
performs weighted signed accumulation and applies measured gain, offset,
saturation, and deterministic noise parameters.

```python
from soliton_eca import CalibratedMixer, DifferentialEncoder

encoder = DifferentialEncoder()
signals = (
    encoder.encode(+0.75, tick=0, position=8),
    encoder.encode(-0.25, tick=0, position=8),
)
mixer = CalibratedMixer((2.0, 3.0), bias=0.1)
output = mixer.mix(signals, tick=0, position=8)
assert output.value == 0.85
```

`ramp_activation` and `sigmoid_activation` are available as reference
transfer functions. Use `transfer_curve` to sample a device’s measured
input/output behavior. Acceptance tests should verify the signed round trip,
weight error, saturation ceiling, noise sensitivity, and activation monotonicity
before connecting the mixer to a trainable network.

## Hardware-in-the-loop perturbation harness

`CalibratedSolitonLayer` maps a dense layer onto calibrated soliton mixers.
`Perturbation` makes four hardware risks explicit: gain error, arrival-time
jitter, packet loss, and channel crosstalk. Misaligned packets are rejected
with a measured total-error result rather than silently entering the wrong
synchronous frame.

```python
from soliton_eca import CalibratedSolitonLayer, Perturbation, perturbation_report

layer = CalibratedSolitonLayer(((1.0, -0.5), (0.25, 2.0)), (0.1, -0.2))
report = perturbation_report(
    layer,
    (0.8, -0.4),
    (Perturbation(), Perturbation(gain_error=0.1),
     Perturbation(timing_jitter=1), Perturbation(crosstalk=0.2)),
)
```

The report uses normalized Euclidean output error. Ideal transport must have
zero modeled error, timing misalignment must be detected, and every nonzero
impairment must be visible in the measured error. This is a simulation
harness, not a claim of physical-device validation. Run it with:

```bash
python3 soliton_eca/validate_hardware.py
```

## Closed-loop calibration and robust training

`fit_affine_calibration` estimates gain and offset from measured transfer
pairs using ordinary least squares and reports root-mean-square residual. The
resulting `ActivationCalibration` can be applied to every mixer in a layer.
`robust_train` then uses finite-difference optimization against the same fixed
impairment profile used for evaluation. Finite differences are deliberate:
they remain valid across clipping, packet loss, and other non-smooth modeled
effects where an ideal analytical gradient would be misleading.

```python
from soliton_eca import (
    CalibratedSolitonLayer, Perturbation, fit_affine_calibration, robust_train,
)

calibration = fit_affine_calibration(
    [(0.0, 0.1), (1.0, 0.6), (2.0, 1.0)], saturation=2.0,
)
layer = CalibratedSolitonLayer(((0.2, -0.1),), calibration=calibration.calibration)
losses = robust_train(
    layer,
    [((1.0, 0.0), (1.0,)), ((0.0, 1.0), (0.0,))],
    epochs=20,
    impairment=Perturbation(gain_error=0.1),
)
```

Acceptance requires a nonzero measured transfer residual to be reported, a
monotonic calibrated response over the operating range, and lower robust loss
after training. Calibration does not remove physical noise or timing errors;
it only identifies the model used to compensate and retrain the layer.

## End-to-end calibrated network

`CalibratedSolitonNetwork` chains calibrated differential-soliton layers and
applies the native ramp after each layer. Its `train_robust` method evaluates
the complete multilayer impaired path while perturbing each weight, so it does
not optimize one layer against an ideal downstream system. This is currently
a finite-difference optimizer intended for small research prototypes; larger
networks should replace it with analytic or automatic differentiation after
the measured device transfer functions are stable.

```python
from soliton_eca import CalibratedSolitonNetwork, Perturbation

network = CalibratedSolitonNetwork(
    weights=(((0.5, 0.25), (0.25, 0.5)), ((0.5, 0.5),)),
    biases=((0.1, 0.1), (0.0,)),
)
losses = network.train_robust(
    [((1.0, 0.0), (0.75,)), ((0.0, 1.0), (0.75,)),
     ((1.0, 1.0), (1.0,)), ((0.0, 0.0), (0.0,))],
    epochs=8,
    impairment=Perturbation(gain_error=0.05),
)
```

The end-to-end acceptance test requires deterministic inference, dimensionally
valid layer chaining, and decreasing loss under a nonzero gain impairment.
Run it with `python3 soliton_eca/validate_end_to_end.py`.

## Adversarial validation

The implementation includes an adversarial validation pass covering empty-bus
inspection, reflective boundary invariants, invalid collision modes,
degenerate calibration data, malformed layer dimensions, and floating-point
identity behavior at zero propagation distance. The audit also removed private
queue reads from neural computation, rebuilt active mixers during numerical
weight trials, rejected malformed target shapes, and enforced exact bias-layer
counts.

Run the full suite from `/home/ubuntu`:

```bash
python3 soliton_eca/validate.py
python3 soliton_eca/validate_rigorous.py
python3 soliton_eca/validate_mixing.py
python3 soliton_eca/validate_hardware.py
python3 soliton_eca/validate_calibration.py
python3 soliton_eca/validate_end_to_end.py
python3 soliton_eca/validate_adversarial.py
```

The tests are reference-model checks. They do not establish performance or
reliability of a physical optical device; those require measured transfer
curves, timing distributions, packet-loss statistics, crosstalk spectra, and
wall-plug energy measurements.

## Measured-curve benchmark

`load_transfer_csv` accepts explicit `input,output` measurements and rejects
missing columns, malformed numeric rows, and underspecified curves.
`calibrate_csv` fits the affine device model and reports monotonicity, dynamic
range, residual error, and saturation fraction. `impairment_sweep` evaluates a
deterministic Cartesian grid of gain, timing, crosstalk, and packet-loss cases.

The included `sample_transfer.csv` fixture produces a monotonic five-point
curve with fitted RMSE `0.110516967` and a 24-case sweep. The generated
`benchmark_report.md` is an example of the machine-readable acceptance summary.
These values are fixtures, not physical-device claims.

## Measurement-quality gate

`QualityGate` is the promotion barrier before device data can drive robust
training. The default gate requires at least five samples, nonzero input and
output span, a monotonic response, and relative affine-fit RMSE no greater than
25% of the measured output span. `evaluate_quality` also reports leave-one-out
gain and offset standard deviations, which expose calibration sensitivity to
individual measurements. `require_quality` raises instead of silently
proceeding when the gate fails.

This threshold is a starting engineering policy, not a universal physical
standard. Tighten it as measurement noise and device requirements become
known. The benchmark validator now requires the default gate to pass before
running its impairment sweep.

## Replicate-aware calibration

`aggregate_replicates` groups repeated observations at the same input and
reports mean output, population standard deviation, and count. This matters
because a monotonic mean curve can still be physically unstable. `calibrate_replicates`
fits the mean response, applies the ordinary quality gate, and adds a maximum
relative replicate-standard-deviation gate. The default workflow should use
multiple captures per input, randomize capture order where possible, and retain
the raw observations alongside the aggregated curve.

The stable fixture has two observations per input and relative replicate
standard deviation `0.00185185`; the unstable fixture has `0.185185` and is
rejected at a `0.02` threshold. Run:

```bash
python3 soliton_eca/validate_replicates.py
```

## Acquisition-order drift gate

Replicate variance does not detect a slow change that is monotonic across the
whole capture. `estimate_drift` fits calibration residual versus actual
acquisition order, and `calibrate_replicates` rejects the dataset when the
normalized residual slope exceeds its configured threshold. Measurement order
must therefore be recorded; randomized or interleaved input schedules are
preferred so transfer-curve shape is not mistaken for temporal drift.

The default normalized drift limit is `0.01` output-span units per capture
step. This is a policy threshold that must be tightened or relaxed from actual
instrument repeatability data. A drift rejection is a reason to recapture or
segment the run, not a reason to silently discard the time variable.

## Event-driven soliton SNN

`AERSpike` is the wire-level packet: timestamp, source address, target
address, polarity, payload, and channel. `encode_spike` and
`decode_spike_stream` provide canonical JSON-lines serialization suitable for
logging or a transport adapter. `SolitonSNN` schedules events by timestamp,
routes them through integer-tick delayed `Connection` buses, and updates
`LIFNeuron` state only when an event arrives. Refractory suppression, causal
ordering, event budgets, and unknown-address rejection are explicit.

Optional local STDP applies causal potentiation and anti-causal depression to
the same connection table used for routing. This is a reference event-driven
SNN, not a claim that JSON is the final physical-link encoding; a hardware
adapter can map the same fields onto an optical or neuromorphic packet bus.

`SolitonSNN.reset()` clears queued events, membrane state, traces, and prior
event logs; `reset_weights=True` also restores the initial connection table.
`trace_digest` hashes the canonical ordered JSON representation of an event
trace, enabling capture replay checks and fault-recovery audits. Inhibitory
polarity is tested as signed payload cancellation rather than an ad hoc
negative weight convention.

For transport integrity, `AERFrame` wraps each spike with a contiguous
sequence number and SHA-256 checksum over the sequence plus canonical spike
payload. `encode_frames` and `decode_frames` detect payload corruption,
reordering, duplicates, and gaps. Non-contiguous inspection is available only
through an explicit `require_contiguous=False` choice; deployment ingestion
should keep the strict default.

`AdmissionPolicy` is the SNN ingress boundary. `admit_spikes` enforces allowed
channels, finite non-negative payloads, future-time horizon, total batch size,
per-timestamp burst size, and timestamp ordering before queueing. The
`SolitonSNN.ingest_framed` path verifies frame checksums and contiguous sequence
numbers first, then applies admission atomically. This separates wire
integrity, endpoint policy, and neuron execution, making rejected traffic
observable without partially mutating scheduler state.

`max_pending_events` adds cumulative backpressure beyond per-batch limits.
Admission counts the scheduler backlog before queueing; if capacity would be
exceeded, the whole batch is rejected and the existing queue is unchanged.
After events are consumed, capacity becomes available again. A transport
adapter should translate this rejection into flow control or retry behavior,
not drop the batch silently.

STDP traces are connection-local: a pre-event on `(source, target_a)` cannot
potentiate `(source, target_b)` merely because the source address is shared.
This fan-out isolation is explicitly tested in `validate_snn.py`.

The SNN scheduler preserves insertion order for events sharing a timestamp,
applies anti-causal STDP depression only when post activity precedes a later
pre-event, and enforces a configurable `max_events` budget. The budget is a
safety boundary for recurrent networks: exceeding it raises rather than
silently hanging or producing an unbounded packet stream.

```python
from soliton_eca import AERSpike, Connection, LIFNeuron, SolitonSNN

net = SolitonSNN(
    [LIFNeuron(0), LIFNeuron(1)],
    [Connection(0, 1, weight=1.0, delay=1)],
    stdp=True,
)
net.inject([AERSpike(0, source=0, target=1)])
emitted = net.run()
```

Run the protocol and dynamics checks with:

```bash
python3 soliton_eca/validate_snn.py
```

## Parameter uncertainty gate

`estimate_uncertainty` computes normal-approximation confidence intervals for
the fitted gain and offset, residual standard deviation, degrees of freedom,
and prediction half-width at any input. `require_uncertainty` evaluates both
ends of the intended operating range and blocks promotion when predicted
measurement uncertainty exceeds the error budget. With only two points the
residual degrees of freedom are zero, so uncertainty is treated as unbounded
rather than manufactured from insufficient data.

The benchmark applies this gate over `[-2, 2]` before running its impairment
sweep. This is a model-based statistical screen; it does not replace
confidence intervals from repeated physical captures or independent validation
data.

## Operating-domain coverage gate

`evaluate_coverage` verifies that the intended input range lies inside the
measured domain and can also reject large internal gaps between measured input
levels. `require_coverage` blocks promotion by default when extrapolation or
undersampled gaps are present. Extrapolation can be enabled only through an
explicit `allow_extrapolation=True` decision, and the resulting report records
that authorization. Confidence intervals do not make extrapolation equivalent
to measurement.

The benchmark requires complete coverage of `[-2, 2]` with no internal input
gap greater than `1.0` before it runs holdout, uncertainty, or impairment
checks.

## Independent holdout gate

In-sample residuals and confidence intervals can look acceptable when the
affine model is misspecified. `leave_one_input_out` therefore removes each
input level, fits the remaining levels, and predicts the held-out mean.
`require_holdout` blocks promotion when the worst held-out error exceeds the
configured fraction of output span. The benchmark applies a `0.35` normalized
maximum-error threshold before impairment evaluation. For production data,
use repeated captures and reserve an entirely independent validation run in
addition to this leave-one-input-out screen.

## Bounded AGI-like cognitive prototype

`CognitiveAgent` composes the validated substrate into an auditable cognitive
loop: observations become facts and episodic records, a goal defines desired
facts, bounded breadth-first planning selects an applicable action, salience is
processed through an event-driven LIF neuron, and the decision is emitted as a
canonical cognitive trace. Trace hashing makes identical runs replayable.

This is **AGI-like in architecture, not in capability**. It has explicit
symbolic facts, a finite action vocabulary, bounded search, in-process memory,
and no open-ended language grounding, world model, autonomous persistence, or
general transfer claim. Those limits are deliberate: every action is auditable,
every state transition is testable, and no action is invented when the goal is
unreachable.

```python
from soliton_eca import Action, CognitiveAgent, Fact, Goal, Observation

at_a, at_b = Fact('location', 'A'), Fact('location', 'B')
move = Action('move', frozenset({at_a}), frozenset({at_b}), frozenset({at_a}))
agent = CognitiveAgent((move,), plan_horizon=2)
agent.remember((at_a,))
agent.set_goal(Goal('at-B', frozenset({at_b})))
action, plan = agent.observe(Observation(0, frozenset({at_a}), salience=1.0))
```

Run the cognitive validation with:

```bash
python3 soliton_eca/validate_cognitive.py
```

## Bounded language grounding and episodic storage

`parse_command` accepts only a small explicit grammar: `observe` followed by
`predicate=value` facts and optional numeric salience, or `goal` followed by
`predicate=value` desired facts. Unsupported verbs, malformed tokens, and
non-finite salience are rejected; this is intentional grounding, not unrestricted
natural-language understanding.

`EpisodicStore` persists canonical cognitive events as append-only JSONL records
with contiguous sequence numbers and SHA-256 checksums. Loading verifies every
record before returning it. A corrupted record cannot be silently replayed or
extended. JSON normalization means consumers should compare canonical event
encodings rather than relying on Python tuple/list identity.

```python
from soliton_eca import EpisodicStore, apply_command

apply_command(agent, 'observe location=A salience=0.8', timestamp=0)
store = EpisodicStore('/tmp/episodes.jsonl')
store.append(agent.events)
recovered = store.events()
```

Run the grounding and persistence checks with:

```bash
python3 soliton_eca/validate_memory.py
```

## Cost-aware cognitive planning

The planner uses bounded Dijkstra-style search over symbolic fact states. Action
`cost` is now part of the objective, so a longer plan can be preferred when its
accumulated cost is lower than a short expensive alternative. Positive-cost
plans are terminated only when the lowest-cost goal state is removed from the
priority queue; equal-cost alternatives resolve in declared action order. The
finite `plan_horizon` remains a hard safety bound, and unreachable goals still
produce an auditable no-op.

## Numeric trust boundaries

All externally meaningful numeric constructors now reject non-finite values.
This includes AER payloads, synaptic weights, LIF parameters, cognitive action
costs, activation calibration, impairment parameters, and sigmoid parameters.
The rule is deliberate: NaN and infinity can evade ordinary positivity checks,
poison comparisons, and create non-reproducible planner or neuron behavior.
Ingress limits remain necessary even for finite values.

## Packaging, observability, and stress validation

The repository includes `/home/ubuntu/pyproject.toml` for reproducible Python
installation. Use `python3 -m pip install -e .` from that directory. The package
has no hidden runtime service and keeps the physical-device model explicitly
simulated.

`SNNMetrics` reports delivered events, emitted spikes, maximum queue depth,
current simulation time, firing rate, and synaptic weight range. The fixed-seed
stress validator exercises one hundred timestamped signed events and verifies
bounded execution, ordered traces, queue metrics, and exact replay equivalence.

```bash
cd /home/ubuntu
python3 -m pip install -e .
python3 soliton_eca/validate_stress.py
```

## Unified runtime and CLI

`SolitonCognitiveRuntime` is the integrated facade. It accepts bounded grounded
commands, executes cognitive planning, ingests checksummed AER frames through
admission and backpressure, runs the event-driven SNN, records runtime metrics,
and appends cognitive/SNN events to the checksummed episodic store. Its
`snapshot()` result is directly JSON-compatible for monitoring or test output.

The installed `soliton-cognitive` command runs a deterministic demonstration:

```bash
cd /home/ubuntu
python3 -m pip install -e .
soliton-cognitive --store /tmp/soliton_memory.jsonl
```

The complete integrated path is tested by `validate_runtime.py`. A CLI adapter
is intentionally only a local reference endpoint; production transport,
authentication, authorization, and external action side effects still require
separate design and explicit policy.

## Safe simulated body

`SimulatedBody` provides embodiment without real-world side effects. It stores a
2-D position, battery, tick, workspace bounds, and actuator limits. `actuate`
rejects non-finite, over-speed, boundary-colliding, or energy-insufficient
commands without changing position, and records every result. `sense` grounds
position and battery into symbolic cognitive facts. `SolitonCognitiveRuntime`
exposes `sense_body` and `actuate_body`, persisting both sensor and actuator
events in the same checksummed episodic store.

This body is deliberately a simulator. It does not access motors, devices,
networks, or external systems. A physical adapter would require separate
hardware authorization, watchdogs, emergency stop behavior, calibration, and
human-reviewed safety policy.

```python
from soliton_eca import SimulatedBody, SolitonCognitiveRuntime

body = SimulatedBody(bounds=(-1, 1, -1, 1), max_speed=0.5)
runtime = SolitonCognitiveRuntime((), body=body)
runtime.actuate_body('step', 0.2, 0.1, tick=1)
sensor_result = runtime.sense_body(timestamp=1)
```

Run the embodiment checks with:

```bash
python3 soliton_eca/validate_body.py
```

## Reproducible closed-loop simulation

`simulate.py` runs the complete safe-body scenario without real hardware. It
feeds sensor observations through cognition, applies one accepted actuator
movement, attempts speed and boundary violations, injects checksummed AER
traffic, runs the SNN, and persists the resulting audit records.

Run it with:

```bash
cd /home/ubuntu
python3 -m soliton_eca.simulate
```

The report is written to `/tmp/soliton_simulation/simulation_report.json` and
memory to `/tmp/soliton_simulation/episodes.jsonl`. In the reference run, the
body ends at `(x=0.5, y=0.0)` with battery `0.9`; actuator outcomes are
`accepted, rejected, rejected`; two SNN events are delivered and one spike is
emitted; and seven memory records are persisted. These are deterministic
simulator results, not measurements of physical hardware.
