# Packaging Line — Design Recommendations (Safety, Ease of Use, Utilities)

> Companion to `AUTO_PACKAGING_SYSTEM.md`. Where that schematic says *what the
> line is*, this doc says *what to add before it is safe, usable, and properly
> serviced*. Claim tags: `[measured]` = repo-verified or physical law ·
> `[hypothesis]` = design recommendation · `[honest wall]` = what this is NOT.
>
> Standards named here are tracked in `AUTO_PACKAGING_PATENTS.md`; air figures
> come from `experiments/air_sizing.py` (verdict in `data/air_sizing_data.json`);
> the energy context is `AUTO_PACKAGING_ENERGY_FEASIBILITY.md`.

---

## 1. Safety and safeguarding

`[hypothesis]` until a risk assessment by a competent person is done. The line
must be designed to EN 415-10 (case-packaging machinery, type-C), using the
ISO 12100 risk-assessment loop (hazard identification → risk estimate →
reduction → iterate) with ISO 13849-1 / IEC 62061 for the safety functions.

### 1.1 Risk assessment is the starting point

No PL/SIL table below replaces one: run an ISO 12100 assessment per station,
walk the whole cycle in every mode (auto, setup, jam-clear, maintenance), and
record the iterations. The table in §1.3 is a *target*, not a certificate.

### 1.2 Guarding and safety distance

| Access need | Guard |
|---|---|
| No access needed (during run) | fixed guards (fold zone at ERECT, tape knife at CLOSE+SEAL) |
| Regular access (blank loading, jam clearing) | interlocked doors + light curtains |
| Robotic cell (INSERT, if delta robot) | perimeter guard per ISO 10218; robot stop + brake release on door open |

- Light-curtain distance per ISO 13855: `S = K·t + C` (K = approach speed,
  t = total system stop time incl. PLC + drive STO, C = intrusion factor).
  The honest wall: the actual value needs the real stop times, so put the
  formula in the spec and compute it after commissioning measurements.
- Guarding must stop the drives with **STO, not a coast-down** — see §1.3.

### 1.3 Safety functions — target performance levels

| Function | PLr / SILr target | Implementation |
|---|---|---|
| E-stop chain (ISO 13850) | PLr d, Cat 3 | hardwired red/yellow, dual-channel, independent of the PLC; reset-only restart |
| Guard doors / light curtains | PLd / SIL2 | dual-channel safety inputs via safety PLC or safety relays; two-channel with cross-fault detection |
| Servo safe torque off (STO) | SIL2 per IEC 61800-5-2 | every fold servo and robot axis — this is what makes guarding *safe* while drives stay live for diagnostics |
| Reject gate, blow-off | PLCc | does not protect a person; STO not required |
| Line stop on quorum ≥50% (§3.1) | PLCc | stops motion, does not isolate energy |

- Keep the **safety function separate from the standard control PLC**: safety
  relays/safety PLC monitor the guards and drop STO + e-stop directly, never
  through the recipe logic. "Do not mix frames" (T55c) has a safety meaning:
  a recipe change must never re-arm a guarding bypass.
- Muting of a light curtain is only allowed with permissive conditions (part
  in place, direction proven) and a time limit — the packaging-specific
  requirements of EN 415-10 apply.

### 1.4 Station-by-station hazard table

| Station | Hazard | Control (add to BOM) |
|---|---|---|
| 1 MAG | spring-loaded magazine retention (energy storage); blank edge cuts; nip at feed rolls | hold-open tool for magazine; nip guards; chamfered/plastisol feed guides |
| 2 ERECT | fold-arm pinch/crush (servo torque ≈ 10–20 N·m at arm); arm overshoot zone; vacuum-table edges | fixed guard + STO; torque-limited motion profile; no reach-through gaps |
| 3 INSERT | robot cell (crush, trapped operator) | perimeter guard, door interlock → STO, restricted-space teaching mode |
| 4 CLOSE+SEAL | tape-head knife; hot-melt burns (~170 °C); compression-section nip | blade guard + interlock; insulated, guarded nozzle; compression nip guard |
| 5 INSPECT | camera lighting (eye safety); reject-gate air | Class 1 eye-safe lighting; nozzle ≤30 psi (§1.5) |
| common | stored energy (air, fold-arm springs, drive capacitors); corrugated dust; noise | LOTO with air exhaust + spring retainer + capacitor discharge time; sealed cabinets + housekeeping; enclosure + muffler |

No ATEX zone is expected (no flammable gas on a corrugated line), but
corrugated fiber dust is a housekeeping and motor-sealing issue — specify
sealed/IP-rated motors in the BOM.

### 1.5 Compressed-air safety

- Blow-off nozzles **≤30 psi** at the exit (OSHA 29 CFR 1910.242(b) rule — a
  chip/debris blow-down safety cap).
- Hose whip restraints at every fitting; safety couplings that vent on break.
- Air receiver is a pressure vessel: stamped/certified, relief valve, daily
  condensate drain (auto drain in BOM), annual inspection.
- Purge and lock out air before any maintenance into the air path.

### 1.6 Operational safety

- **Operator reset is mandatory after any FAULT** (never auto-restart; the
  quorum doctrine makes ≥50% disagreement a stop, and a stop needs a person).
- Machine marking: guards labeled, nameplate with machine ID + standard
  references, LOTO points marked.
- Access control / training / PPE for the one-operator model in §2.
- The reject ledger (self-refutation discipline) should record *safety-related*
  stops separately — refutations documented, not hidden.

---

## 2. Ease of use

`[hypothesis]`. Goal: one operator runs the line; everything the operator does
must be learnable in one shift and recoverable in under two minutes.

### 2.1 HMI and control UX

- One screen per station + an overview; every fault is a **click → guided
  fix** (which station, which check failed, which reset sequence), not a code
  to look up.
- Recipe library per box size (FEFCO 0201 dimensions, fold angles, dwell
  times) — changeover is recipe recall, not tooling.
- Show the **quorum margins live** (T16–T20): three sensor values and the
  disagreement %. Operators learn to intervene at ~40–45% disagreement, before
  the line stops itself.
- Make the **reject ledger visible on the HMI** (self-refutation discipline):
  refutations are shown, not buried — and the near-crease correction log
  (PPA-002) shows what the line fixed before it failed.

### 2.2 Changeover and calibration

- All size changes are **digital** (servo positions + recipes); target ~1–2
  min per size with no tools. Plough guides and vacuum tooling are the only
  physical bits to swap, and they should be tool-less quick-release.
- Blank-lot calibration workflow (the L.O.R.E. doctrine, measured not chosen):
  1. load a test blank of the new lot;
  2. measure crease depth / restoring moment;
  3. enter it once → the feedforward compensator uses it until the lot changes.
  Store the value with the lot ID in the IIoT log for traceability.

### 2.3 Maintenance and service

- Quick-access panels (no tools) to every motor, sensor, tape head, glue pot,
  air filter.
- Tool-less tape roll and blank change; removable glue pot for cleaning.
- Annunciated PM schedule on the HMI (filters, lubrication, blade, vacuum
  pads, condensate drain).
- IIoT gateway streams diagnostics (per-axis torque, drive temperature, air
  pressure) for remote view — same gateway that logs boxes.
- Keep a spare-parts kit list in the cabinet: the top-5 wear items (tape
  blades, vacuum pads, photoeyes, air filters, encoder cables).

### 2.4 Ergonomics

- Blank loading height 0.8–1.2 m; no reaching into any hazard zone to load
  (magazine holds 30+ min of blanks).
- Reject bin and scrap at waist height with a chute.
- Noise target < 70 dB(A) at operator position (compressor in an enclosure
  outside the cell, muffled blow-offs).
- Task lighting 500 lux at inspection points; the cameras' lighting is
  separate (Class 1, §1.4).

### 2.5 Jam and fault recovery

- Per-station guided recovery sequences (which guards to open, what is safe,
  what order to clear) — the jam-clear walk is part of the ISO 12100 risk
  assessment because it is the highest-frequency human interaction.
- After a jam: the partially formed box goes to **scrap, never back into the
  flow** (T55c — never mix frames). The machine knows which box was in which
  station and disposes it.
- Clear all faults → operator reset → the line re-verifies the invariant
  checks before resuming production (no silent auto-resume).

---

## 3. Utilities — compressed air and the "excess air" question

`[measured]` figures from `experiments/air_sizing.py` (component assumptions
stated in its header); verdict artifact `data/air_sizing_data.json`.

### 3.1 Do we need excess air? Yes — headroom, not excess capacity

The line's air demand is **peaky**: a blow-off burst (~18 scfm) is ~3.5× the
average draw (~6 scfm). Compressed-air systems also lose 20–30% of their air
to leaks as they age. So the design does need **excess capacity** — but the
correct container for it is:

1. a **receiver tank** (~27–30 gal) that absorbs the burst, and
2. a **VFD compressor** sized `FAD = peak × 1.3` (~27 scfm, ~0.77 m³/min)
   that *tracks the average flow* rather than cycling on peaks.

An oversized fixed-speed compressor is the classic failure: it idles at ~25%
load forever, wasting more energy on unloaded running than the line uses. Put
the margin in the tank and the drive, not in the iron.

### 3.2 Quantified sizing (run `python experiments/air_sizing.py`)

| Item | Value |
|---|---|
| Continuous demand (4 venturi vacuum pads) | ~2.0 scfm |
| Intermittent (2 blow-offs, 20% duty) | ~3.6 scfm avg / ~18 scfm peak |
| Cylinders / valves | ~0.3 scfm avg |
| **Average / peak demand** | **~6 scfm / ~21 scfm** |
| Compressor FAD (peak + 30%) | ~27 scfm (0.77 m³/min) |
| Average draw incl. 25% leak allowance | ~7.4 scfm → ~27% duty of FAD |
| Average power (VFD, 0.22 kW/scfm) | ~1.6 kW → **matches §5's 1–2 kW line** |
| Receiver (VFD rule 1 gal/scfm / fixed 6 gal/scfm) | ~27 gal / ~164 gal |
| Energy & cost | ~3.4 MWh (~$400/yr) 8 h shift · ~14 MWh (~$1.7k/yr) 24/7 |

### 3.3 The honest recommendations (ordered by size of saving)

1. **Right-size the source**: VFD + receiver + leak/repair program beats a big
   fixed compressor. Leaks are the second-largest air cost on any plant — a
   quarterly leak audit pays for itself.
2. **Replace venturi vacuum with a low-pressure blower** for destacking
   (~0.2 bar). Same gripping duty at ~3–4× less energy (venturi expansion
   from ~6 bar is ~1–3% efficient; a blower is ~30–50%). This is the biggest
   single air-side saving and it lands on the §9 "demand-side beats recovery"
   principle directly.
3. **Run at the lowest usable pressure**: each 1 bar reduction saves ~6–7% of
   air energy. Set the blow-offs at 30 psi (which also satisfies §1.5) and
   trim the ring pressure to the highest genuinely needed device.
4. **Air quality per ISO 8573-1**: dryer + filters + auto condensate drains;
   oil-free compressor if food-adjacent packaging. Wet, dirty air is the main
   cause of failed vacuum pads and sticky valves — i.e., downtime, not just
   energy.
5. **Minimize air at all**: prefer electric actuation where possible (servos
   already power the folds and regenerate — §9); use air only for gripping,
   blow-off, and the reject gate. Fewer air consumers = fewer leak points and
   fewer failure modes.

### 3.4 What NOT to add

- A big dry tank "just in case" — it only delays pressure loss and increases
  blow-down losses; size it per §3.2.
- Fixed-speed compressor with duty cycling — it cannot track the 6→21 scfm
  swing without pressure oscillation.
- Unrestricted blow-off nozzles — they exceed §1.5's 30 psi rule and waste the
  most energy per unit of useful effect on the whole line.

---

## 4. Other "all manner" additions (short list)

- **Energy metering**: a power meter per station (servo bus, compressor, glue
  pot, controls) feeding the same IIoT gateway — turns the §5 budget and
  `AUTO_PACKAGING_ENERGY_FEASIBILITY.md` assumptions into measured values over
  the first quarter.
- **Predictive maintenance**: vibration on fold motors, drive temperature,
  air pressure trends, vacuum-pad flow — all already collected on the bus.
- **Cybersecurity** for the control + IIoT network (IEC 62443-3-3): the
  gateway is a real attack surface once it talks to the cloud.
- **Documentation set**: FMEA, O&M manual, wiring diagrams, risk-assessment
  records — required for EN 415-10 conformity anyway; store them with the
  machine.

---

## 5. Honest walls

- §1 is a *target safety architecture*, not a certified design: final PL/SIL,
  guard geometry, and ISO 13855 distances must come from a risk assessment
  and commissioning stop-time measurements by competent people.
- §3's air numbers are component-assumption estimates (stated in
  `experiments/air_sizing.py`), not a metered plant; duty and leak figures
  will shift the FAD by ±30% in either direction.
- Ease-of-use items are recommendations; usability targets (one-shift
  learning, 2-min recovery) need validation with the actual operators.
