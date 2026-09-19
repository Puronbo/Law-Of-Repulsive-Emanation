# CMB Reconciliation Note

**Purpose:** reconcile every statement this framework makes about the cosmic
microwave background against the current measured values, and file the open
gaps as OPEN (flag, not fill). **Date:** 2026-09-19. Status: INVESTIGATION
(reconnaissance + audit), no claims added or changed.

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
  selection criterion).
- **BRIDGE-3 (confluence, opens a reverse path):** the observable universe's
  de Sitter horizon entropy is ~10^122 k_B - the same 10^122 that appears
  as the framework's CC gap (G_obs x L_obs = 2.77e-122, THE_UNIVERSE_FROM_
  A_FIXED_POINT.md:296). The CMB-anchored horizon entropy and the CC gap
  are one number, inverted: a measurement the framework already owns twice.
  A claim that the framework's entropy max (PHYSICAL_UNIVERSAL_MAP.md:86)
  "is the boundary" can be pinned to this literal number.
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