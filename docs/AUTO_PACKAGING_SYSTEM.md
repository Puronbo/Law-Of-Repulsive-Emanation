# Autonomous Packaging System — Folding-Mechanics Schematic

> Design: an autonomous case-packaging line (blank → erected box → packed →
> sealed → inspected) whose core operation is **score-line folding**, built
> from the Puno Calculus machinery's verified geometry + classic mechatronics.
>
> Claim tags: `[measured]` = repo-verified or physical law · `[hypothesis]` =
> design mapping · `[honest wall]` = what this is NOT.
>
> Scope: schematic (system architecture, station detail, control, inspection,
> energy, BOM), not a commissioned build.
>
> Companion docs: `AUTO_PACKAGING_PATENTS.md` (patents + standards + FTO) ·
> `AUTO_PACKAGING_ENERGY_FEASIBILITY.md` (energy feasibility + build cost) ·
> `packaging/` (IEC 61131-3 servo code + Python mirror).

---

## 1. Top-level system architecture

```
FLAT BLANK ─► [1 MAGAZINE/   ] ─► [2 ERECTOR    ] ─► [3 INSERT    ] ─► [4 CLOSE+SEAL ] ─► [5 INSPECT   ] ─► PALLET
(fanfold/    │   DESTACKER   │   │  (FOLD)     │   │  (PRODUCT) │   │  (FLAPS+TAPE)│   │  (CLOCK-TEST)│
 blanks)     │   vacuum feed │   │  score-fold │   │  robot/push│   │  plough +    │   │  square +   │
             │   1 at a time │   │  4 panels   │   │  into box  │   │  tape head   │   │  seam +     │
             └───────┬───────┘   └──────┬──────┘   └─────┬──────┘   └──────┬───────┘   │  content    │
                     │                  │                │                 │           └──────┬──────┘
                     └──────── CONTROL LAYER: PLC master state machine ─────┘                 │
                              EtherCAT servo bus · IO-Link sensors · HMI      [REJECT LANE] ──┘
                                                                    ▲
                                            PERCEPTION PLANE: encoders · photoeyes ·
                                            load cells · 2–3 vision cameras · lighting
```

**Layers:**
- **Physical layer** — stations 1–5 on a common conveyor/transfer system.
- **Perception plane** — every actuator's position, every check's invariant.
- **Control layer** — one master state machine, per-station sub-machines.
- **The "other techniques"** (§6): vacuum destacking, plough guides, servo
  motion with torque control, vision/ML inspection, tape/glue joining,
  compressed air, safety (light curtains / e-stop), IIoT logging.

---

## 2. Station-by-station schematic (RSC line)

Conveyor direction →.

```
 [1 MAG]      [2 ERECTOR]      [3 INSERT]     [4 CLOSE+SEAL]     [5 INSPECT]
 ─────────   ──────────────   ─────────────   ────────────────   ─────────────
 blank │     side panels       product group   top flaps via     cameras +
 stack │     folded 90° by     collated and     plough guides,    squareness,
   ────►     rotary fold       pushed into      tape head folds   seam, content
 vacuum │    arms; bottom      the box;         tape over the     checks;
 destack│    flaps (majors      presence         top+bottom        FAIL ─► reject
 1/each │    then minors)       verified         seams, 3–5 s      lane; PASS ─►
         │    taped to lock      before close     compression       palletizer
         └───────────────────────────────────────────────────────────────────►
```

### 2.1 The erector — the folding core (side/top view)

Flat blank (RSC), score lines dashed:

```
         ┌────────────────┐
         │   END FLAP     │
┌────────┼────────────────┼────────┐
│ SIDE   │   MAIN PANEL   │ SIDE   │   1) side panels folded 90° (rotary arms,
│ PANEL  │   (bottom)     │ PANEL  │      vacuum table holds blank flat)
└────────┼────────────────┼────────┘
         │   END FLAP     │         2) bottom end flaps: MAJOR then MINOR
         └────────────────┘         3) tape head locks the bottom seam
                                     4) box raised to vertical for packing
```

Fold servo control loop (per folding axis):

```
target ─►[Σ]─►[PID]─►[SERVO DRIVE]─►[MOTOR+GEAR]─►[FOLD ARM]──► BLANK (crease)
angle     ▲                                                  │
          └──────────[ANGLE ENCODER] ◄── actual fold angle ───┘
              + feedforward: restoring-torque compensator
              (calibrated per blank lot: the constant is measured, not chosen)
```

### 2.2 Fold mechanics — why it works, in framework terms

- **The crease is the selected structure** `[hypothesis]` — the score line is
  where stiffness is minimal, so the fold happens *there*, not at an arbitrary
  bend. This is the fold theorem's "crease = unique viscosity solution"
  (T63/T64) made physical: the fold is selected by the geometry, not forced by
  the actuator.
- **Spring-back is the repulsive emanation** `[hypothesis]` — the folded
  panel's restoring moment fights the fold; the servo must overshoot the
  target angle and hold for a dwell until the tape/glue lock is in place.
  The hold torque is measured per blank lot (crease depth → restoring
  moment calibration), the L.O.R.E. doctrine: the constant is measured, not
  chosen.
- **The closure is the QC invariant** `[hypothesis]` — a correctly folded
  case closes to *squareness* (corner-to-corner ratios ≈ 1, fold angles ≈
  90°). The golden closure (T58) is the repo's measure of a fold reaching its
  geometry — here the invariant is squareness, not a magic ratio.
- **Near-crease diagnostics** `[hypothesis]` — a fold that comes up short
  (within a few degrees of the 90° threshold) is the efficient unit to fix
  (re-apply pressure in-loop) rather than reject (PPA-002 crease
  diagnostics).

---

## 3. Control architecture

```
                    MASTER STATE MACHINE (PLC / soft-PLC)
     ┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
     │ MAG         │ ERECT        │ INSERT       │ CLOSE+SEAL   │ INSPECT      │
     │ feed/register│ fold seq.   │ collate/place│ flap+tape    │ invariant check
     └──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
                 EtherCAT servo bus + IO-Link sensors + vision PLC
```

- **Flow the small core, route the large static mass** `[hypothesis]` (T67):
  the folding heads and servo axes (small, dynamic) run at high loop rates;
  the blank magazine, palletizer, and conveyor mass are routed slowly. The
  architecture separates high-bandwidth motion from high-mass logistics.
- **Self-healing, never mix frames** `[hypothesis]` (T55c): a marginal fold
  is corrected in-loop; a failed box is diverted at the reject gate and never
  re-inserted into the good flow. Mixing a partially folded case into the
  sealing line is the frame-mix the repo forbids.
- **Quorum, not single points** `[hypothesis]` (T16–T20): three independent
  sensors on each critical check (box present, flap folded, tape applied).
  <40% disagreement → continue (repair margin); ≥50% → line stop and reset.
  This is the fragment-bank result: majority honesty, not Byzantine.
- **Watchdogs**: every station times out to a safe state; the master records
  the failure in the reject log (self-refutation discipline: refutations are
  documented, not hidden).

### 3.1 State machine

```
MAG:  feed blank → register (flap present?) ──► ERECT
ERECT: vacuum grip → fold side panels 90° → fold bottom majors → minors →
      tape bottom seam → raise box → verify square ──► INSERT
INSERT: collate product group → push/robot place → (content present?) ──► CLOSE
CLOSE: plough top flaps → tape head (top+bottom seams) → compression 3–5 s ──► INSPECT
INSPECT: squareness ∧ seam ∧ content ── PASS: out · FAIL: reject lane → recycle/scrap
FAULT: any station watchdog or quorum-fail ≥50% → line stop → operator reset
```

---

## 4. Inspection — the clock test made physical

`[hypothesis]` Acceptance keys on **invariants**, never on gauge:

| Check | Invariant (the law) | Gauge (ignored for pass/fail) |
|---|---|---|
| Squareness | corner-to-corner distance ratio ≈ 1; fold angles ≈ 90° | absolute camera coordinates, lighting, scale |
| Seam | tape covers the full top+bottom seam (continuity) | tape brand, head position |
| Content | product present + within box volume (mass/vision) | conveyor speed, camera frame |

This is T59/T61: a pattern that dies under re-encoding was not a law.
Squareness survives rotation/scale/lighting re-encoding; an absolute pixel
position does not. The line's pass/fail is therefore stable across camera
replacement, lighting changes, and speed changes.

---

## 5. Energy budget (estimate)

~300 cases/hour erector–packer–sealer:

| Load | Power (avg) |
|---|---|
| Servo motion (folding, transfer) | 2–3 kW |
| Vacuum / compressed air | 1–2 kW |
| Tape/glue, controls, vision, HMI | 0.5–1 kW |
| **Total** | **~5 kW → ~120 kWh/day** |

Option (ties to §3.36 hydrogen–photon energy): a 4–5 kW PV array (25–35 m²
at ~20%) + battery covers the day; an H₂ fuel-cell module provides backup.
Honest wall: these are estimates from component ratings, not a measured line.
**Correction — see `AUTO_PACKAGING_ENERGY_FEASIBILITY.md`:** the 4–5 kW array
covers only ~15% of the 24/7 demand (and ~40–45% of a one-shift day); true
solar self-sufficiency needs 30–35 kW (24/7) or 10–12 kW (one shift), and H₂
backup is resilience-only at 2026 hydrogen prices.

---

## 6. The "various other techniques" (supporting subsystems)

1. **Vacuum destacking** — 1-blank-at-a-time magazine feed (Bernoulli/vacuum
   grippers, double-sheet detection by thickness/photoeye).
2. **Plough / guide folding** — passive fold rails for the top flaps (no
   actuator, geometry does the work: another "crease-selected" fold).
3. **Servo motion with torque control** — fold arms with angle feedback +
   restoring-torque feedforward (compensates spring-back per lot).
4. **Vision/ML inspection** — 2–3 cameras; optional defect model for blank
   damage; invariants from §4.
5. **Tape head / hot-melt** — the taping head is itself a folding mechanism
   (wipes the tape around the case edges); compression section holds until
   adhesion.
6. **Compressed air** — grippers, blow-off, reject gate.
7. **Safety** — light curtains, interlock doors, e-stop chain, safe torque off.
8. **IIoT logging** — per-box traceability (blank lot, fold torques, QC
   results), reject ledger (self-refutation discipline).

---

## 7. Representative bill of materials

| Station | Components |
|---|---|
| 1 MAG | vacuum pump, feed belts, double-sheet sensor, photoeyes |
| 2 ERECT | vacuum table, 4× servo fold arms + encoders, pressure rails, bottom tape head, torque sensors |
| 3 INSERT | delta robot + vision, or collator + pusher cylinder, load cell |
| 4 CLOSE+SEAL | plough guides, top tape head, compression section |
| 5 INSPECT | 2–3 cameras + lighting, load cell, reject gate |
| Control | PLC + EtherCAT servo drives, IO-Link masters, HMI, safety relay, IIoT gateway |

---

## 8. Mapping table — repo machinery → packaging subsystem

| Repo asset (verified) | Packaging subsystem | Design consequence |
|---|---|---|
| Fold theorem T63/T64 — crease = unique viscosity solution | Score-line folding at erector | Fold along the score; the crease selects the geometry |
| L.O.R.E. — the constant is measured, not chosen | Crease depth → hold torque | Calibrate restoring moment per blank lot; never assume it |
| Golden closure T58 | Box squareness after lock | Closure-to-squareness is the QC invariant (not a magic ratio) |
| Clock-test T59/T61 | Inspection | Pass/fail on invariants only (squareness, seam, content) |
| Fragment bank T16–T20 — majority honesty | Sensor redundancy | <40% disagreement: continue; ≥50%: stop-and-reset |
| Self-healing mesh T55c — never mix frames | Reject/recycle path | Divert failed boxes; never re-insert into good flow |
| Spatial index T67 — flow core, route mass | Motion architecture | Fold heads at high loop rate; magazine/pallet slow |
| Crease diagnostics PPA-002 — near-crease is the target | Marginal-fold correction | Re-apply pressure in-loop instead of immediate reject |

---

## 9. Waste energy reuse — capabilities and possibilities

Energy-recovery streams on the line, ranked by recoverable size and ease of
capture. The quantified servo-regen figure comes from
`experiments/servo_regen.py`; the heat figures are engineering estimates from
component ratings. `[hypothesis]` unless tagged `[measured]`.

| Stream | Source | Recoverable | Daily (one 8 h shift) | Capture method | Priority |
|---|---|---|---|---|---|
| Compressed-air waste heat | air compressor (~2 kW input, ~75–85% rejected as heat) | ~1.5 kW | ~10–12 kWh as heat | heat exchanger on compressor outlet → washdown hot water / winter shop heat | **HIGH** |
| Servo regenerative braking `[measured]` | fold axes' settle phase (spring-back does work on the motor) | ~8% of fold motoring, ~196 J/axis-cycle | ~0.5 kWh returned to bus | shared EtherCAT DC bus + battery recapture (§3.36 PV+battery); brake resistors only as fault backstop | **MEDIUM** |
| Vacuum/blow-off demand | Bernoulli grippers, reject gate | small, low-grade | ~0.5–1 kWh equivalent | timing/sequencing (air only while gripping) rather than recovery | LOW |
| Hot-melt/tape-head heat | glue-pot heater ~0.5 kW | minimal | — | insulate the pot, duty-cycle the heater | LOW |
| Control-cabinet cooling | servo drives + PLC reject heat | 0.1–0.3 kW, seasonal | ~1–2 kWh winter | passive ducting to preheat the shop in winter | LOW |
| H₂ fuel-cell CHP | FC exhaust (if H₂ backup installed) | ~40–50% of fuel LHV as heat | ~15–25 kWh | heat exchanger to a buffer tank | IF H₂ used |

**Architectural points:**
- **Shared DC-bus crosstalk** — when one axis is regenerating and another is
  motoring simultaneously (the 4 fold axes rarely all brake at once), the
  regen is used directly by the motoring axis with zero conversion loss. This
  is the same "flow the small core" idea (T67) applied to power, and it needs
  no extra hardware beyond a common DC bus.
- **Battery recapture** — DC-coupling the servo bus to the §3.36 PV battery
  lets regen surplus charge the battery instead of heating a brake resistor;
  the battery smooths the fold-to-fold power peaks that would otherwise
  ripple the AC draw.
- **Demand-side beats recovery** — the largest single "waste" saving on this
  line is *not building the waste*: right-sizing the air system (low-pressure
  vacuum blowers for destacking instead of central compressed air) cuts the
  1–2 kW compressed-air load at the source, which is worth more than
  recovering its waste heat.

**Honest wall:** servo regen is numerically small on this line (~0.5 kWh per
8 h shift — architectural value, not energy value); compressed-air heat
recovery displaces *heating* energy (seasonal) rather than the line's
electrical draw; every figure here is schematic-level, not metered.

---

## 10. Honest walls

- The fold/crease/emanation mappings are **analogies over real mechatronics**;
  the physical laws here are classical (elasticity, friction, servo control),
  and no repo parameter transfers to a crease depth or a hold torque.
- Corrugated-board variability (moisture, flute direction, anisotropy) is the
  dominant real failure source; every blank lot needs its own calibration.
- Throughput, energy, and BOM figures are schematic-level estimates, not a
  commissioned build.
- The state machine and quorum thresholds are design choices grounded in the
  repo's results, not measured packaging outcomes.
- The repo's geometry is not required for the machine to work — the machine
  works by classical physics; the framework contributes discipline (crease,
  clock-test, quorum, self-healing) to how it is controlled and inspected.
- Patents and standards are tracked in `AUTO_PACKAGING_PATENTS.md`; both core
  patents (US9718570B1, US10532842) are **Active** — a build needs a license
  or a design-around, not an assumption of freedom to operate.
