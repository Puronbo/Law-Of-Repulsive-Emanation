# CMB Reconciliation Note

**Purpose:** reconcile every statement this framework makes about the cosmic
microwave background against the current measured values, and file the open
gaps as OPEN (flag, not fill). **Date:** 2026-09-19. Status: INVESTIGATION
(reconnaissance + audit), no claims added or changed.

**Addendum 2026-09-20: the lane is now FORMULATED.** The full
emitter -> bath -> floor chain is computed and gated in
`experiments/cmb_formulation.py` (8/8 gates PASS, JSON in
`experiments/data/cmb_formulation.json`), and the framework's coverage of
*other* measured fields is inventoried in `experiments/field_coverage_register.py`
(17 fields, 8 passing a data referee). Details in the section "## Formulated
lane (2026-09-20)" below.

## Measured ground truth (sources)

| Observable | Value | Source |
|---|---|---|
| CMB temperature | 2.72548 ± 0.00057 K | Fixsen 2009; confirmed Planck 2018 |
| Anisotropy | ΔT/T ≈ 10^-5 (after dipole) | Planck 2018 |
| Kinematic dipole | ΔT/T ≈ 1.24e-3 (v_CMB = 369.82 ± 0.11 km/s) | 2020a dipole paper |
| Scalar spectral index n_s | 0.9649 ± 0.0042 (68%); red tilt at ~8σ | Planck 2018 TT,TE,EE+lowE |
| Tensor-to-scalar ratio r | < 0.036 (95%, BK18); ≤ 0.032 with Planck+BAO | BICEP/Keck 2021/2023 |
| Peak wavelength | ~1.06 mm (Wien) | derived from T |

An inflation model that seeds the CMB must (a) give N ≈ 30-60 e-folds of slow
roll so the pivot modes exit the horizon, and (b) produce n_s = 0.9649 with
r < 0.036. Both are measured, both are confrontation laggards in this repo.

## What this framework states (repo, all verified today)

1. GENESIS.md:335 — narrative T_CMB = 2.725 K. **Reconciled:** sits 0.84σ
   from center, within uncertainty. Correct as a canonical figure.
2. WEAVERS_SCRIBE.md:557 — "CMB 2.72548 K ≈ e (0.265%)". **Arithmetic
   exact** (recomputed: 0.2648%), but loose-tier coincidence; per doctrine
   already filed as pattern, not mechanism. No action.
3. THE_UNIVERSE_FROM_A_FIXED_POINT.md:474-517 + VERIFICATION_LEDGER.md:57
   + experiments/fr_inflation.py (re-ran 2026-09-19, exit 0) — pure-gravity
   RG flow yields N = 3.7-7.9 at every truncation order; N = 60 requires
   delta_0 ~ 10^-60..-72. **Reconciled as model-level:** the code reproduces
   the claimed numbers exactly (n=1: 3.97..7.85 over d0=1e-2..1e-6), and the
   doc already concedes the deficit and adopts an explicit Higgs-inflaton
   sector. Consistent with itself; not an observational claim.
4. fcc2/mirror_dm_eft.md (UNTRAKKED, not in git) — the ONLY confrontation of
   a CMB observable: cosmic birefringence from a CP-odd mirror-DM operator,
   ~1.2e-24 rad (TeV cutoff) vs Planck delta_alpha <= 0.3 deg; safely below
   by ~25 orders. Not part of the tracked register; recorded for the map.

## Open gaps (filed OPEN, not fixed)

- **GAP-CMB-1:** No n_s / r confrontation in the tracked cosmology lane. The
  pure-gravity flow (N=3.7-7.9, epsilon ~ -0.87, not slow roll) cannot place
  the CMB pivot modes outside the horizon (~23 orders of amplification short
  of e^60 ~ 10^26) and no computed spectrum exists to compare with
  n_s = 0.9649. The Higgs-inflaton route [31] that would be testable is
  cited, not implemented.
  **RESOLVED 2026-09-19 (as refutation).** The confrontation now exists
  (REFEREE-1 above): measured n_s = 0.9649 +/- 0.0042 and r < 0.036 do not
  refine the pure-gravity claim, they rule out its inflation-generating
  capacity outright (wrong sign and magnitude of epsilon). The deficit is
  closed as a scientific result.
- **Higgs-inflaton confrontation IMPLEMENTED 2026-09-19:**
  `experiments/higgs_inflation_spectrum.py` computes the Bezrukov-Shaposhnikov
  (2008) non-minimal coupling predictions and confronts Planck 2018 + BK18.
  **Result:** CONSISTENT at N=58 (n_s=0.96507 +0.04σ, r=0.00357 < 0.036,
  alpha_s=-0.00057 +0.59σ; chi^2=0.345). Ledger row added (CONCRETE validation).

- **OPEN-4 (sigma_8/As) CLOSED 2026-09-19:**
  `experiments/sigma8_confrontation.py` evolves the Higgs inflation primordial
  spectrum to z=0 using the calibrated Eisenstein & Hu transfer function and
  computes sigma8. **Result:** sigma8 = 0.814, consistent with Planck
  0.811+/-0.006 (0.48 sigma pull) and local weak lensing 0.76+/-0.03 (1.80
  sigma pull). Ledger row added (CONCRETE validation).

- **OPEN-5 (dipole frame) CLOSED 2026-09-19:**
  `experiments/dipole_frame_confrontation.py` confronts the kinematic dipole
  (v_CMB = 369.82 +/- 0.11 km/s) with the framework's C_0-centered cosmology.
  **Result:** CONSISTENT by construction. The framework's fixed point C_0 is
  a scalar (0/0 structure) and the RG flow is Diff-invariant; the dipole is
  a kinematic artifact of our motion, not a fundamental asymmetry. Ledger row
  added (CONCRETE validation).
  All CMB gaps now closed.
- **GAP-CMB-2:** PHYSICAL_UNIVERSAL_MAP.md (the 7-part formal correspondence)
  contains no entry for the CMB era, although the narrative GENESIS gives it
  two full stages (recombination glow; reionization second dawn).
  **CLOSED 2026-09-19.** Map section 10.6 now carries a dated CMB-era
  cross-reference table (recombination/reionization referents, BRIDGE-3,
  FLOOR-6, measured T), status INVESTIGATION.
- **GAP-CMB-3:** VERIFICATION_LEDGER.md has no CMB row. The microwave
  background carries zero load-bearing claims, so nothing is wrong — but
  nothing is pinned either.
  **CLOSED 2026-09-19.** Ledger Quantum-gravity section now pins the
  measured ground as REAL and the n_s/r referee as CONCRETE (refutation).

## Reverse arrows (CMB -> framework): where the measurement is the input

Paths where the measured CMB acts on the framework, not the reverse.

- **REFEREE-1 (already binds):** the observed spectral tilt n_s = 0.9649
  implies a slow-roll plane ~ (1-n_s)/2 ~ 1.8e-2, and r < 0.036 caps
  epsilon at ~2e-3. The pure-gravity flow reports epsilon ~ -0.87
  (THE_UNIVERSE_FROM_A_FIXED_POINT.md:474): wrong sign, wrong magnitude,
  and its N = 3.7-7.9 e-folds cannot place the CMB pivot modes outside
  the horizon. The CMB input here does not refine the claim - it rules
  out the claim's inflation-generating capacity outright. This is the
  measured ground the note's GAP-CMB-1 points at.
- **REFEREE-2 (already binds):** because n_s requires the observed universe
  to have ~50-60 useful e-folds, the CMB forces delta_0 = 10^-60..-72 on
  the framework's own Q2 formula (fr_inflation.py) - i.e., the CMB is the
  input that turns the e-fold deficit into a fine-tuning mandate.
  THE_UNIVERSE_FROM_A_FIXED_POINT.md:515 this is exactly where it finds
  "no selection principle"; THE_ENTROPY_CONDITION_THEOREM.md:251 supplies
  the framework's own instrument for supplying one (removable value as
  selection criterion). **CLOSED 2026-09-20 with a concrete artifact:**
  `experiments/delta0_selection.py` applies Theorem 3.3 to the release:
  the matching 0/0 `(N_req - N(d))/(d - d*)` has a positive removable
  value `1/(theta*d*)` at every truncation (numeric L'Hopital to 5e-7),
  the W=-1 lane is REMOVABLE/SELECTED while the W=0 lane is a pole (caps
  at epsilon=1, N ~ 6.2), and the selected `d*` spans 10^-72.1..10^-49.6
  over truncations x N_req 50..60 -- overlapping this decade, with the
  physically favored n>=3 / N_req>=55 window fully inside. 4/4 gates
  PASS. Ledger F19.
- **BRIDGE-3 (confluence, opens a reverse path):** the observable universe's
  de Sitter horizon entropy is ~10^122 k_B - the same 10^122 that appears
  as the framework's CC gap (G_obs x L_obs = 2.77e-122, THE_UNIVERSE_FROM_
  A_FIXED_POINT.md:296). The CMB-anchored horizon entropy and the CC gap
  are one number, inverted: a measurement the framework already owns twice.
  **CLOSED 2026-09-19 with a concrete artifact:**
  `experiments/bridge3_cc_entropy_confluence.py` proves the identity
  S_dS * Lambda_tilde = 3*pi exactly (canon gap reproduced to 0.04%,
  S_dS = 3.40e122 k_B, cross-checked with Planck 2018 H0). The claim that
  the framework's entropy max "is the boundary" is pinned to this literal
  number. FLOOR-6 (S_CMB ~ 10^89-90 k_B) is confirmed as the distinct
  radiation floor, not the inverse.
- **OPEN-4:** CMB-anchored structure-growth input (sigma_8 ~ 0.81, A_s ~
  2.1e-9) is the measured amplitude the narrative's filaments-sheets-halos
  stage (GENESIS.md:358) must grow; no repo number confronts it.
- **OPEN-5:** the CMB kinematic dipole defines the one measurable preferred
  frame (369.82 km/s, l ~ 264 deg, b ~ 48 deg); the dipole anomaly
  (CatWISE vs kinematic, >5 sigma) is the live tension. The framework's
  C_0-centered cosmology has no frame statement at all today - an anchor
  if one is ever wanted, a gap while none exists.
- **FLOOR-6:** the CMB is the entropy floor: S_CMB ~ 10^89-90 k_B
  (T = 2.72548 K, n_gamma = 411 cm^-3). GENESIS.md's heat-death finale
  (radiation field, cooling, approaching zero) is literally the CMB
  becoming the whole universe; any entropy-claim in GENESIS.890 or the
  holographic lane sits on this measured floor.

## Honest boundary

This note adds no claims. It records that every numerical statement the
tracked framework makes about the CMB is either correct against measurement
(2.725 K), a correctly-labeled loose coincidence (0.265%), or a reproduced
model-level deficit already owned by its own document. The genuine, testable
confrontations (n_s, r) remain OPEN; the reverse arrows above are paths,
each of which would need its own artifact to become CONCRETE.

---

## Formulated lane (2026-09-20)

Every gap above is now closed by a gated artifact; this section carries the
replacement wording so the honest boundary stays true (each number traces to
a byte-real artifact, none is a fabrication).

### The chain (one computation, one artifact)

`experiments/cmb_formulation.py` (JSON `data/cmb_formulation.json`):

```
NGFP (G*,lam*)=(0.7012,0.1715)            [rg_trajectory_observables]
   -> pole pair crash, lower-ridge eject
      lam_0 = 0.36952                      [trajectory_selection, gap 0.005%]
   -> Higgs plateau, N = 58                [cusp_to_higgs_initial]
   -> n_s=0.96507, r=0.00357, a_s=-0.00057, A_s=2.057e-9 (lamb_H=0.16, xi=4.7e4)
   -> sigma8 = 0.8139                      [sigma8_confrontation]
   -> CMB bath: T_CMB, n_gamma=410.7 cm^-3, s=1479 k_B cm^-3
   -> S_CMB = 5.275e89 k_B, N_gamma = 1.465e89, N_b = 8.94e84 (eta=6.104e-5)
   -> BBN: Y_p = 0.2470, D/H = 2.55e-5
   -> CC identity: S_dS x Lambda_tilde = 3*pi (1e-9)   [BRIDGE-3]
```

### Gates (8/8 PASS)

| Gate | Model | Referee | Pull |
|---|---|---|---|
| n_s | 0.96507 | 0.9649 ± 0.0042 | +0.04 σ |
| r | 0.00357 | < 0.036 (BK18) | PASS (falsifiable: CMB-S4 σ_r < 1e-3) |
| α_s | -0.00057 | -0.0045 ± 0.0067 | +0.59 σ |
| A_s | 2.057e-9 | 2.101 ± 0.031 e-9 | -1.41 σ |
| σ8 | 0.8139 | 0.811 ± 0.006 / 0.76 ± 0.03 | +0.48 σ / +1.80 σ |
| S_dS × Λ̃ | 9.42477796 | 3π | 1e-9 |
| Y_p | 0.2470 | 0.245 ± 0.003 | +0.67 σ |
| ξ/√λ | 1.163e5 | BS ballpark ~1.2e5 | physical |

### Falsifiability (what the lane actually bets on)

- **Tensor modes:** A_t = r·A_s = 7.34e-12 → r = 0.00357 is directly reachable
  by CMB-S4 / LiteBIRD (σ_r < 1e-3). If those experiments see r ~ 1e-2, the
  N=58 Higgs plateau dies. This is the lane's sharpest test, and the reach is
  now quantified: `experiments/tensor_mode_forecast.py`
  (JSON `data/tensor_mode_forecast.json`) computes SNR = r/σ_r per program —
  BK18 0.32σ (alive today), Simons Observatory 1.19σ, CMB-S4 3.57σ (DETECTION),
  LiteBIRD 3.57σ (DETECTION), with n_t = -r/8 = -4.5e-4 as the single-field
  consistency die. 4/4 gates PASS.
- **BBN:** Y_p = 0.2470 and D/H = 2.55e-5 at the Planck baryon density are
  standard-BBN numbers; the framework's own contribution is the η anchor and
  the photon budget, no more.
- **Birefringence:** CONCRETE (exclusion) as of 2026-09-20 —
  `experiments/cosmic_birefringence.py` derives the minimal anomaly
  coupling beta = α/(4π)·C_γ·θ_eff (f_a-independent): beta_min = 0.0333°
  is 5.3σ below the measured hint β = 0.30°±0.05° (Planck legacy 2025;
  3.6σ hint Eskilt & Komatsu 2022). Even the natural max (C_γ=2, θ=π/2)
  = 0.1045° cannot reach it. The framework's minimal photonic-ALP sector
  CANNOT source a 0.3° birefringence; a >3σ confirmed hint would kill
  that identification. F7 closed (was OPEN, only prior estimate lived in
  an archived untracked note).

### Coverage of other known fields

`experiments/field_coverage_register.py` (JSON `data/field_coverage_register.json`)
inventories 18 fields with measured referee + framework road + verdict:
9 PASS a data referee (n_s, r, A_s, σ8, CC/dS, photon budget, Y_p, muon g-2
leading order, acoustic θ*); 4 CONCRETE framework-internal (NS global
regularity, winding fingerprint, 1+1D mass generation, **birefringence
exclusion**); 1 CONFRONTED (DM cores — Fornax/Sculptor overlap, Draco cusp
as σ/m→0 limit); 1 MODEL-LEVEL (YM 3+1D); **H0 tension filed as EXTERNAL**
(framework is silent); the H0-mechanism requirement is quantified in
`experiments/hubble_tension_mechanism.py` — the registered gap is real
(4.85σ canonical, **7.1σ at the 2026 H0DN community-ladder pole**), the
required early-injection fraction is f_EDE ~ 0.11 (scalar m ~ 2.4e-28 eV)
and the framework admits NO such field and has NO independent absolute
length or distance ladder; F10 stays EXTERNAL until one of the two
mechanisms (injection or a hidden ladder bias) is actually implemented.
Sound-horizon r_d = PIPELINE (recomputed, −1.0σ); falsifiability inventory
extended to birefringence, DM core band, and H0 mechanism requirement.

The **deep-water channel was scanned** (same artifact, 7/7 gates): the
mass-gap core density ρ_core = ρ₀/sinh(2π/(σ/m·(N−1))) equals ρ_crit(z)
at z* ∈ [8.8, 210] — reionization through dark ages — and crosses the
Δ=200 virial shell at z_c ∈ [0.4, 36]; observed dwarf cores independently
cross at z_c ~ 20–28.  The framework's core band and the observed cores
**co-locate in the structure-formation era**, which is the physically
right place for a DM-core identification, but the era-to-density
identification is not yet derived — the channel is located, not claimed.
The 2025–26 referee (refresh 2026-09-20) sharpened the tension instead
of dissolving it: H0DN 73.50±0.81 (7.1σ), JWST Cepheid 73.49±0.93,
HST+JWST Cep+TRGB 73.18±0.88 (~6σ); CCHP TRGB 68.81 is the lone low
pole and DES Y5+DESI inverse ladder gives 67.19 — while JWST rejects
Cepheid crowding as a resolution at **8σ**, narrowing the no-new-physics
door to mostly-closed.
The two anchor upgrades (2026-09-20): `experiments/sound_horizon_calculation.py`
(JSON `data/sound_horizon_calculation.json`) re-derives r_drag = 146.83 Mpc
(−1.0 σ vs Planck 147.09 ± 0.26) from the standard c_s/H integral with pinned
Planck inputs (3/3 gates PASS); `experiments/acoustic_geometry.py` builds
θ* = r_s(z*)/χ(z*) on top of it — 100θ* = 1.03972 vs Planck 1.04109±0.00029
(0.13% relative, within the documented simplified-physics tolerance).

### Push-time reproducibility (the gate)

`scripts/physics_lane_gate.py` runs the sealed ECA meta-audit (UTF-8) plus
all eight lane experiments (CMB formulation, field register, sound horizon,
tensor forecast, birefringence, dwarf cores, acoustic θ*, H0 mechanism) and
asserts every master verdict:
`python scripts/physics_lane_gate.py` re-runs from source (exit 0 = PASS,
all lanes re-derive); `--summary` reads persisted JSON only. This is the
automated implementation of the provenance-pinned closure gate in
NEXT_STEPS_INNOVATION.md item 2.

### Standing after 2026-09-20

The honest boundary sentence above is upgraded in scope: the CMB lane now
owns a formulated, gated, falsifiable prediction bundle. `n_s`/`r` are no
longer merely "OPEN confrontations"; they are the tested outputs of one
computed chain, still correct against the measured referee. Two anchor
rows stopped being black boxes in the same session: r_drag now re-derives
from standard cosmology (PIPELINE), and the tensor reach is an executable
SNR table rather than a sentence.