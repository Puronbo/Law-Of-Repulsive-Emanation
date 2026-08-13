# Autonomous Case-Packaging Line — Complete Machine Specification

> **One consolidated document.** This is the single complete spec for the
> autonomous case-packaging line (flat blank → erected box → packed → sealed →
> inspected). It merges what were four documents into one segment:
>
> | Former doc | Now consolidated into |
> |---|---|
> | `AUTO_PACKAGING_SYSTEM.md` (architecture, stations, control, energy) | §1–§8 |
> | `AUTO_PACKAGING_PATENTS.md` (patents + standards + FTO) | §10 |
> | `AUTO_PACKAGING_ENERGY_FEASIBILITY.md` (energy + build cost) | §7 |
> | `AUTO_PACKAGING_RECOMMENDATIONS.md` (safety, ease of use, utilities) | §4, §6, §9 |
>
> The four files remain in `docs/` as appendices for citations and survey
> depth; every *necessity* is stated here. Newly-added necessities that were
> previously missing are flagged **[ADDED]**: takt/throughput budget (§1.2),
> conveyor + accumulation buffers (§2.6), power distribution & cabinet cooling
> (§6.3), calibration tooling (§9.2), maintenance schedule + spares (§9.3),
> commissioning/acceptance protocol (§9.5), environmental envelope (§1.4),
> rainwater collection & use (§6.4, quantified by
> `experiments/rainwater_sizing.py`), efficiency systems — standby/sleep,
> air-leak monitoring, amplifier nozzles, dust extraction, scrap handling,
> hot-water buffer (§6.5, quantified by `experiments/standby_efficiency.py`),
> accessibility systems — OEE dashboard, human-factors accessibility, remote
> service access, QR asset documentation (§6.6),
> and a master equipment list with specific better-equipment choices (§11).
>
> Claim tags: `[measured]` = repo-verified or physical law · `[hypothesis]` =
> design decision · `[honest wall]` = what this is NOT.
>
> Control code companion: `packaging/` (IEC 61131-3:2025 ST + Python mirror,
> 309-test suite).

---

## 1. System architecture

### 1.1 Topology

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
- **Physical layer** — stations 1–5 on a common transfer conveyor.
- **Perception plane** — every actuator's position, every check's invariant.
- **Control layer** — one master state machine, per-station sub-machines
  (IEC 61131-3:2025, §3).

**Design doctrine (from repo machinery):**
- **Fold theorem (T63/T64)** — the crease is where stiffness is minimal, so
  the fold happens *there*; the geometry selects the fold. Plough guides and
  the tape-head wipe are passive, crease-selected folds.
- **L.O.R.E. — the constant is measured, not chosen** — restoring torque is
  calibrated per blank lot (crease depth → hold torque), never assumed.
- **Clock test (T59/T61)** — inspection accepts on invariants only
  (squareness, seam continuity, content), never on gauge.
- **Fragment bank (T16–T20)** — three independent sensors per critical check;
  <40% disagreement → continue, ≥50% → stop-and-reset (majority honesty, not
  Byzantine).
- **Self-healing, never mix frames (T55c)** — marginal folds corrected
  in-loop; failed boxes diverted to scrap, never re-inserted.
- **Spatial index (T67)** — flow the small core: fold axes at high loop rate,
  magazine/pallet at slow rate.

### 1.2 Throughput & takt budget **[ADDED]**

Target: **300 cases/hour = 12 s/case** (5 cases/min, "RSC line").
Pipeline layout — one case per station per cycle, stations overlap:

| Station | Budget per case | Longest step |
|---|---|---|
| 1 MAG | ≤ 2 s | destack + register |
| 2 ERECT | ≤ 6 s | fold drive (~2 s) + dwell (1 s) + settle + tape (~2 s) |
| 3 INSERT | ≤ 3 s | place product group |
| 4 CLOSE+SEAL | ≤ 5 s | plough + tape + compression 3–5 s (overlapped) |
| 5 INSPECT | ≤ 2 s | 3 checks + reject decision |

The erector's drive→dwell→settle profile is the longest single step and sets
the pipeline pace; a 12 s cycle gives 100% margin over the ~6 s measured fold
cycle. Buffers between stations absorb jitter (see §2.6).

### 1.3 Layout / footprint **[ADDED]**

- In-line: **~8–12 m × 1.5–2 m** machine footprint.
- **~30–60 m² cell area** including guarding envelope, reject lane, blank
  storage, and the compressor/blower enclosure (outside the guarded cell,
  acoustic enclosure for < 70 dB(A)).
- Solar (if self-sufficient): 150–175 m² (24/7) or 55–65 m² (one shift) —
  §7.2.

### 1.4 Environmental envelope **[ADDED]**

- Operating: 10–40 °C, 30–80% RH non-condensing.
- Corrugated **fiber dust** is a housekeeping + motor-sealing issue: sealed
  IP-rated motors, filtered cabinet ventilation, dust extraction at the
  erector/tape zones. **No ATEX** zone is expected (no flammable gas).
- Cabinet cooling: filtered fans or air-to-air heat exchangers, not air
  conditioning unless the ambient exceeds 40 °C (§6.3).

---

## 2. Station-by-station specification (with specific equipment)

Box code: **FEFCO 0201 RSC**, board single/double-wall corrugated, size
change digital (servo) — range defined in the recipe library (§9.2).

### 2.1 Station 1 — Magazine / Destacker

- Stacked blanks, 1-at-a-time vacuum feed; double-sheet detection; register
  (flap-present) check before release.
- **Equipment — the better choice:**
  - **Low-pressure regenerative blower** (e.g., Becker U-range, Busch
    Samos) at ~0.2 bar driving Bernoulli grippers (e.g., Piab) — NOT a
    venturi off the central air ring (~3× less energy for the same grip,
    §6.1; removes the largest continuous air load).
  - Double-sheet detection: **capacitive or ultrasonic sensor** (e.g.,
    SICK, Di-Soric), not just a photoeye.
  - Register photoeye + encoder on the feed belt; magazine hold-open tool
    (§4.3).

### 2.2 Station 2 — Erector (the folding core)

Fold sequence (per case): **GRIP → FOLD_SIDES 90° → FOLD_MAJORS → FOLD_MINORS
→ TAPE_BOTTOM → RAISE → VERIFY square.** Fold servo control law (reference
implementation `packaging/servo.py`, mirrored in ST):

```
target ─►[Σ]─►[PID]─►[SERVO DRIVE]─►[MOTOR+GEAR]─►[FOLD ARM]──► BLANK (crease)
angle     ▲                                                  │
          └──────────[ANGLE ENCODER] ◄── actual fold angle ───┘
              + feedforward: restoring-torque compensator
              (calibrated per blank lot: measured, not chosen)
```

- PID: `kp=0.5, ki=0.5, kd=0.002`, conditional integration within ±1.0° of
  target, integral clamp 2.0.
- Feedforward: `k_restore=0.02` (per-lot calibrated) carries the spring-back
  moment; drive to 90°+3° overshoot, dwell 1 s for the tape/glue lock, settle
  to square 90°. Watchdog: step_timeout 8.0 s → FAULT.
- **Equipment — the better choice:**
  - **4 servo axes**, each: EtherCAT drive with **STO (SIL2 per IEC
    61800-5-2) and regenerative shared DC bus** (e.g., Beckhoff AX5000/AX8000,
    SEW MOVI-AXIS, Kollmorgen AKD) — the shared bus recycles spring-back
    regen (§8) instead of heating brake resistors; brake resistors only as a
    fault backstop.
  - Motors: **low-inertia servos 0.4–1 kW with planetary gearheads** (or
    direct-drive torque motors for maximum fold stiffness), **18–23-bit
    absolute encoders** — not incremental (position survives a power cycle,
    no re-homing on a jam).
  - Vacuum table holds the blank flat; pressure rails hold the folded sides
    during settle.
  - Bottom tape head (end-fold, §10 — US10532842 license/design-around).

### 2.3 Station 3 — Insert (product)

- Collate the product group; place into the erected box; verify content
  present (load cell + photoeye) before close.
- **Equipment — the better choice:**
  - **Delta robot + vision** (e.g., ABB FlexPicker, Fanuc M-3iA) for
    flexible SKU handling, or a servo pusher/collator for a single fixed
    product. Delta is preferred: it absorbs product-arrival jitter without a
    dedicated indexing conveyor.
  - Load cell on the insertion station; robot cell guarded per ISO 10218
    (§4.3).

### 2.4 Station 4 — Close + Seal

- Plough guides fold the top flaps (passive, crease-selected); tape head
  seals top + bottom seams; compression section holds 3–5 s.
- **Equipment — the better choice:**
  - **Automatic case taper with tape end-fold** (Wexxar / 3M-Matic class) —
    the end-fold wipes the tape around the case edges (US10532842 is
    Active; license or design-around required, §10).
  - **Hot-melt applicator** (e.g., Nordson) with thermocouple + PID and an
    **insulated, guarded pot** (§4.3); cold-glue alternative for non-heat
    applications. Never bare heating elements at the ~170 °C melt zone.
  - Compression section: timed hold with jam sensor, guarded nip.

### 2.5 Station 5 — Inspect

- **Clock-test invariants** (§5): squareness (corner-to-corner ratio ≈ 1,
  fold angles ≈ 90°), seam continuity, content present/within volume.
- **Equipment — the better choice:**
  - **2–3 industrial GigE Vision cameras** (e.g., Basler, Balluff) + fixed
    machine-vision **LED bar lights (Class 1 eye-safe)**; optional defect
    model on the blank feed.
  - Reject gate: servo or pneumatic at ≤30 psi; PASS → palletizer, FAIL →
    reject lane → scrap (never re-inserted, T55c).

### 2.6 Transfer conveyor & buffers **[ADDED]**

- **Modular belt or chain conveyor**, accumulation-capable zones between
  stations (each holds 1–2 cases so a slow station doesn't stall the line),
  IP54, jam sensors at every transfer.
- Conveyor speed is slow (12 s/case); power is a minor line item (~0.3 kW,
  included in §7.1 fixed loads).
- Belt material compatible with corrugated board (no scuffing of the print
  surface).

---

## 3. Control system

- **One master state machine + per-station sub-machines**, IEC 61131-3:2025
  structured text (reference ST in `packaging/plc_61131_3.py`, Python mirror
  `packaging/servo.py`, pinned by 309 tests).
- Fieldbus: **EtherCAT** for servo bus + **IO-Link** for sensors; vision PLC
  on the same network.
- **Quorum** on every critical check (box present, flap folded, tape applied):
  3 independent sensors; <40% disagreement → continue (repair margin), ≥50% →
  line stop, operator reset.
- **Watchdogs**: every station times out to a safe state; failures go to the
  reject ledger (self-refutation discipline: refutations are documented, not
  hidden).
- **Equipment — the better choice:**
  - Standard control: **soft-PLC on IEC 61131-3:2025** (e.g., Beckhoff
    TwinCAT, B&R, Codesys-based) — the ST source ships with the machine.
  - **Safety is a SEPARATE safety PLC/relay system** (Pilz PNOZmulti 2,
    SICK Flexi Soft, or Siemens F-hardware), never the recipe PLC (§4).
  - HMI: 12–15" industrial panel (e.g., Beckhoff CP-series, Siemens Comfort)
    with the §9.1 UX.
  - IIoT gateway: **OPC UA** push to the cloud; per-box traceability (blank
    lot, fold torques, QC result) + reject ledger.
  - Cybersecurity per IEC 62443-3-3 on the control + IIoT network.

---

## 4. Safety

`[hypothesis]` until a risk assessment by a competent person. Design target:
**EN 415-10** (type-C), method per **ISO 12100**, safety functions per
**ISO 13849-1 / IEC 62061**, E-stop per **ISO 13850**, electrical per
**IEC 60204-1**.

### 4.1 Risk assessment is the starting point

No table below replaces an ISO 12100 assessment per station, in every mode
(auto, setup, jam-clear, maintenance), with iterations recorded. §4.3 is the
target, not a certificate.

### 4.2 Guarding

| Access need | Guard | Equipment |
|---|---|---|
| No access needed during run | fixed guards (fold zone, tape knife, compression nip) | sheet-steel fixed guards, tool-removable only |
| Regular access (loading, jam clearing) | interlocked doors + light curtains | **dual-channel light curtains** (e.g., SICK deTec), **non-contact coded interlock switches**, dropped into the safety PLC |
| Robotic cell (INSERT) | perimeter guard per ISO 10218 | door interlock → robot STO + brake release |

- Light-curtain distance per **ISO 13855**: `S = K·t + C`, with t = full stop
  time (incl. PLC + STO) measured at commissioning — the formula goes in the
  spec, the value is measured, not assumed. `[honest wall]`
- Guarding drops the drives with **STO, not a coast-down**; drives stay live
  for diagnostics.

### 4.3 Target performance levels

| Function | PLr / SILr | Implementation |
|---|---|---|
| E-stop chain | PLr d, Cat 3 | hardwired red/yellow, dual-channel, independent of PLC, reset-only restart |
| Guard doors / light curtains | PLd / SIL2 | safety PLC, dual-channel inputs with cross-fault detection |
| Servo STO | SIL2 (IEC 61800-5-2) | every fold servo + robot axis |
| Reject gate, blow-off | PLCc | no person-protection role |
| Quorum ≥50% stop | PLCc | stops motion, does not isolate energy |

- **Safety function is never routed through recipe logic** (T55c applied to
  guarding: a recipe change must never re-arm a bypass). Light-curtain muting
  only with permissive conditions + time limit, per EN 415-10.

### 4.4 Station hazard table

| Station | Hazard | Control |
|---|---|---|
| 1 MAG | magazine spring storage; blank edges; feed nip | hold-open tool; chamfered guides; nip guards |
| 2 ERECT | fold-arm pinch/crush (servo torque ~10–20 N·m); overshoot zone; table edges | fixed guard + STO; torque-limited profile; no reach-through |
| 3 INSERT | robot cell crush | perimeter guard, interlock → STO, restricted teaching mode |
| 4 CLOSE+SEAL | tape knife; hot-melt ~170 °C burns; compression nip | blade guard + interlock; insulated guarded pot; nip guard |
| 5 INSPECT | lighting; reject-gate air | Class 1 lighting; ≤30 psi nozzle |
| common | stored energy (air, springs, drive caps); dust; noise | LOTO w/ air exhaust + spring retainer + cap discharge; sealed motors; enclosure |

### 4.5 Compressed-air safety

- Blow-off nozzles **≤30 psi** exit (OSHA 29 CFR 1910.242(b)).
- Whip restraints at every fitting; safety couplings vent on break.
- Receiver is a pressure vessel: stamped, relief valve, auto drain, annual
  inspection (§9.3).
- Lock out + purge air before any air-path maintenance.

### 4.6 Operational safety

- **Operator reset mandatory after any FAULT** — never auto-restart (quorum
  ≥50% is a stop; a stop needs a person).
- Machine marking, LOTO points, access control, training, PPE.
- Safety-related stops are logged separately in the reject ledger.

---

## 5. Inspection — the clock test made physical

Acceptance keys on **invariants**, never on gauge:

| Check | Invariant (the law) | Gauge (ignored for pass/fail) |
|---|---|---|
| Squareness | corner-to-corner distance ratio ≈ 1; fold angles ≈ 90° | absolute camera coords, lighting, scale |
| Seam | tape covers the full top+bottom seam (continuity) | tape brand, head position |
| Content | product present + within box volume (mass/vision) | conveyor speed, camera frame |

Invariants survive rotation/scale/lighting re-encoding (T59/T61); absolute
pixel position does not — so pass/fail is stable across camera replacement,
lighting, and speed changes. Near-crease diagnostics (PPA-002): a fold within
a few degrees of threshold is corrected in-loop, not rejected.

---

## 6. Utilities

### 6.1 Compressed air — the "excess air" question, answered

`[measured]` figures from `experiments/air_sizing.py` (assumptions in its
header; verdict `data/air_sizing_data.json`).

**Do we need excess air? Yes — headroom, not excess capacity.** The line's air
demand is peaky (blow-off burst ~18 scfm ≈ 3.5× the ~6 scfm average), and
plants lose 20–30% of air to leaks. But the headroom belongs in a **receiver
tank + VFD compressor**, not an oversized fixed-speed compressor that idles at
~27% load forever.

| Item | Value |
|---|---|
| Continuous (4 vacuum pads) | ~2.0 scfm |
| Intermittent (2 blow-offs, 20% duty) | ~3.6 avg / ~18 peak scfm |
| Cylinders/valves | ~0.3 avg scfm |
| **Average / peak demand** | **~6 / ~21 scfm** |
| Compressor FAD (peak + 30%) | **~27 scfm (0.77 m³/min)** |
| Avg draw incl. 25% leak allowance | ~7.4 scfm (~27% duty) |
| Avg power (VFD, 0.22 kW/scfm) | **~1.6 kW** (matches §7.1's 1–2 kW line) |
| Receiver tank | ~27–30 gal (VFD rule); ~164 gal if fixed-speed |
| Energy & cost | ~3.4 MWh / ~$405 per yr (8 h shift); ~14 MWh / ~$1.7k per yr (24/7) |

**Equipment — the better choice:**
- **VSD (variable-speed-drive) rotary screw compressor** (~27 scfm FAD, e.g.,
  Atlas Copco GA 5–7 VSD, Kaeser BSD) — tracks average flow, no unloaded
  idling; oil-free variant if food-adjacent packaging.
- **ASME-stamped vertical receiver**, ~30 gal, relief valve + auto drain.
- **Refrigerated dryer + coalescing filters → ISO 8573-1 air quality class
  (e.g., 2/4/4)**; auto condensate drains (also in the daily PM, §9.3).
- **FRL (filter/regulator/lubricator) at every station**, 6 bar ring,
  blow-offs trimmed to 30 psi.
- Quarterly leak audit (leaks are the second-largest air cost; §9.3).

### 6.2 Vacuum — blower, not venturi

- Destack: **regenerative blower at ~0.2 bar** (Becker/Busch) + Bernoulli
  grippers — ~0.13 kW vs ~0.44 kW for the venturi path (~3× less), and it
  removes the 2 scfm continuous load from the compressor.
- Gripper sequencing: air/vacuum only while gripping (§8 demand-side).

### 6.3 Power distribution & cabinet thermal management **[ADDED]**

- **3-phase 208–480 V feed**, main disconnect + lockable, per-branch MCCBs,
  RCD/GFCI, **IEC 60204-1** wiring + grounding, shielded EtherCAT cabling,
  strain relief everywhere; cabinet IP54 (dust envelope, §1.4).
- **Redundant 24 V PSUs** for PLC/safety; **UPS** for PLC + HMI + vision (rides
  through a 2 s mains blip and clean shutdown on outage).
- Cabinet cooling: filtered fans or air-to-air heat exchangers (drive reject
  heat is ducted to preheat in winter, §8); no A/C unless >40 °C ambient.
- Energy metering: a power meter per station (servo bus, compressor, glue
  pot, controls) on the IIoT gateway — turns §7.1's estimates into measured
  values in the first quarter.

### 6.4 Rainwater collection & use **[ADDED]**

`[measured]` sizing from `experiments/rainwater_sizing.py` (assumptions in its
header; verdict `data/rainwater_data.json`). Non-potable uses only.

**Demand it serves (line-related, ~150 L/production day → ~40 m³/yr):**
machine + floor washdown (~90 L), glue-system + tool rinsing (~30 L),
corrugated-dust suppression (~20 L), solar-panel washing (~10 L averaged).

**Supply:** the facility roof (~300 m² metal standing seam) harvests ~184
m³/yr at 800 mm/yr rainfall (`runoff_m3`: 0.85 roof × 0.9 first-flush/leaf/
filter efficiency) — **~4.6× demand, so catchment is not the constraint**;
the tank bridges dry spells. The §7.2 PV array can double as catchment
(smooth modules, low runoff loss).

**Tank sizing** (monthly water balance, smallest zero-deficit tank):

| Rainfall profile | Tank |
|---|---|
| Uniform | ~3.5 m³ (~925 gal) |
| Summer-dry (Jun–Aug @ 5 mm) | ~10 m³ (~2,640 gal) |

**Components & cost (~$13k installed):** gutter/downspout + leaf guards +
first-flush diverters ($2k) · above-ground poly tank 4–10 m³ ($2.5k) · pump +
pressure tank + level control + mains make-up solenoid ($2k) · 50 µm + 5 µm
filtration + UV ($1.5k) · install, plumbing, backflow prevention ($5k).

**Integration — the real value (honest wall):**
- **Waste-heat washdown** (§8 HIGH row): the compressor heat exchanger now
  has a free, soft, low-mineral water supply to preheat — rainwater + waste
  heat together make warm washdown with zero municipal water and minimal
  heating energy.
- **PV-protecting wash**: low-mineral rainwater washing recovers the 5–15%
  output loss dirty modules accumulate on the $67–112k array (§7.2).
- **Stormwater credits**: cities with stormwater utilities may credit
  impervious-surface fees (site-dependent, potentially $0.5–2k/yr).
- **Resilience**: independent non-potable supply during a mains outage — the
  same resilience-only argument the H₂ backup carries (§7.2.3).

**Honest wall:** on the water bill alone (~$160/yr saved) the payback is
~80 yr. This is a systems/integration play, not a money-saver. Non-potable
ONLY: backflow prevention, cross-connection control, labeled piping, and
local rainwater-harvesting rules apply.

### 6.5 Efficiency systems **[ADDED]**

`[measured]` figures from `experiments/standby_efficiency.py` (assumptions in
its header; verdict `data/standby_efficiency_data.json`). These are the
demand-side systems missing from the §7.1 budget: the ~5 kW / ~120 kWh/day
figure assumes flat 24/7 running, but realistic duty (16 h production + 8 h
idle) keeps fixed loads drawing unless they are deliberately dropped.

**1. Standby / idle management (AUTO → IDLE → SLEEP)** — the cheapest
kWh-per-dollar on the line, mostly software:
- **AUTO** (running): full ~5 kW.
- **IDLE** (no blank fed for 2 min): conveyor off, fold drives to **STO
  standby** (SIL2, §4), vacuum blower to idle, compressor VFD trims to
  leakage-only.
- **SLEEP** (no blank for 30 min): IDLE + cabinet lights off, HMI dimmed.
- Effect: idle drops from ~2.3 kW (near-running, no sleep) to **~0.9 kW** —
  an **11.2 kWh/day** cut on a 16+8 day (**~120 → ~87 kWh/day**), ~6,440
  kWh/yr (~$773/yr at $0.12). Capex ~$3k (PLC state logic + drive standby
  enable) → **~4 yr payback**, ~2–3 yr if the line idles more.
- Honest wall: on a *true* 24/7-continuous line the standby savings vanish;
  build the states anyway — they only earn where production actually stops.

**2. Air-flow monitoring & leak detection** — a flow meter per air branch on
the IIoT gateway with a baseline trend; leaks grow quietly toward the 20–30%
allowance, and a ~1 scfm leak is invisible to a quarterly audit. Catching and
repairing ~1 scfm saves ~0.22 kW → ~915 kWh/yr (~$110/yr); the meter pays for
itself by catching one leak.

**3. Amplifier blow-off nozzles** — engineered nozzles (air-amplifier /
coanda) deliver the same 30 psi force at ~30–50% of an open pipe's flow.
Conservative ~1 scfm of the ~3.6 scfm blow-off average saved → another ~915
kWh/yr (~$110/yr).

> Air systems 2+3 combined: ~1,830 kWh/yr (~$220/yr), capex ~$2k (meter +
> nozzle kit) → ~9 yr payback on kWh alone; the real return is that leaks
> also cause pressure loss → higher FAD sizing and nozzle wear.

**4. Dust collection & extraction** — a small cartridge dust collector
(~$5k) at the erector scoring + tape-knife zones. Corrugated fines are the
#1 sensor/camera-killer on a case line (§1.4); extraction keeps photoeyes,
quorum sensors, and inspection cameras clean — this is a *reliability* system
whose payback is downtime-avoidance, not kWh.

**5. Waste & scrap handling** — the reject lane and blank-trim scrap goes to a
**compactor/baler** (~$8k, or shared plant unit) with return-flow accounting
fed by the reject ledger (T55c, never mix frames). Baled corrugated has
recycling value / avoids disposal cost; the ledger makes the reject rate a
measured OEE-quality input (§6.6.1).

**6. Hot-water buffer tank** — a small insulated buffer (~200–500 L) makes the
§8 compressor-waste-heat washdown actually usable: the heat exchanger charges
the buffer, the buffer preheats the §6.4 rainwater washdown supply on demand
instead of dumping heat when nobody is washing.

**7. Equipment-class efficiency** — IE4/IE5 premium-efficiency motors on the
conveyor/fans (all on VFDs), LED high-bay lighting with presence control,
and the already-specified VSD compressor + blower (§6.1–6.2).

**8. Condition monitoring (predictive maintenance)** — the EtherCAT bus and
IIoT gateway already collect the signals, so add trend baselines for: fold-
motor vibration + drive temperature (bearing/load drift), air pressure
trends per branch (leaks and filter loading), vacuum-pad flow (wear), and
glue-pot heater duty. Deviations push a PM suggestion on the §6.6.1
dashboard instead of waiting for the next §9.3 maintenance interval — this is
the efficiency side of uptime (unplanned stops are the line's biggest hidden
cost) and it reuses data already on the bus at near-zero capex.

**Efficiency verdict + honest wall:** sleep + air systems ≈ **~8.3 MWh/yr
(~$1k/yr)** for ~$5k capex — the best kWh-per-dollar on the line; dust/scrap/
buffer/condition-monitoring are reliability and integration systems whose
value the energy figures do not count. All figures are duty-assumption
estimates; the §9.5 energy baseline turns them into measured values.

### 6.6 Accessibility systems **[ADDED]**

Accessibility here means three things: **data accessibility** (every operator
and service engineer can see and act on the line's state), **human-factors
accessibility** (the machine is operable by people of different reach,
strength, vision, hearing, and language), and **service accessibility**
(maintenance reaches the parts, and the docs reach the maintainer).

**1. OEE & production dashboard** — Availability / Performance / Quality live
on the HMI (and reported via the §3 IIoT gateway), fed by data the control
layer already collects: **availability** from watchdog stops and quorum
resets, **performance** from rate vs the §1.2 takt, **quality** from the
reject ledger (§9.1). This is the operational face of EN 415-11 (availability
standard, §10) and turns the reject ledger from a log into a decision tool.

**2. Operator / human-factors accessibility** —
- Controls and HMI within **reach zones** (0.8–1.2 m, no reach >50 cm into
  hazard zones).
- **Ergonomics**: blank loading at 0.8–1.2 m, reject bin and scrap at waist
  height on a chute; **noise < 70 dB(A)** at the operator position (acoustic
  compressor/blower enclosure, muffled blow-offs); **500 lux** task lighting
  at inspection/loading points (camera lighting is separate, Class 1, §4.4).
- **Low-force, low-precision controls** (large buttons, no tight grasping) so
  the machine is operable with gloves and by operators of varied hand
  strength.
- **Adjustable HMI**: font size, high-contrast theme, and a **multilingual
  operator layer** (e.g., English/Spanish) — one recipe, switchable display
  text.
- **Dual-modality alarms**: every alarm is **audible AND visual (strobe)**, so
  it works for hearing- and sight-impaired operators alike; the guided-fix
  (§9.1) is shown as text and as icon-step sequences.
- **Slow / jog-assisted mode** for setup and assisted work: full speed is
  locked out, guarding stays active — accessibility without removing safety.
- E-stop reachable from every operator position (ISO 13850, §4).

**3. Remote service accessibility** — secure **VPN / OPC UA remote
diagnostics** (§3, IEC 62443-3-3) so the integrator can view the same HMI
screens and fault stack the operator sees; a versioned software-update path;
and remote-guided fixes for the top HMI "click → fix" flows. Accessibility of
the machine to its service network, not just to its operator.

**4. QR asset tags + digital documentation** — every major component carries a
**QR/asset tag** linking to its datasheet, wiring reference, PM record, and
spare-part number. The §9.3 maintenance schedule and the spare-parts list
become machine-accessible at the component; MTTR drops because the part is
found, its replacement procedure is shown, and the record is updated in
place.

**Accessibility honest wall:** the human-factors items follow general
accessibility and ergonomics guidance (reach, force, contrast, multimodal
alarm), not a machinery-specific ADA certification — they are design intent
to be validated with the actual operators in §9.5, not a compliance claim.

---

## 7. Energy & cost (consolidated feasibility)

### 7.1 Load & demand scenarios

| Load | Power (avg) |
|---|---|
| Servo motion (folding, transfer) | 2–3 kW |
| Vacuum / compressed air | 1–2 kW (air calc: ~1.6 kW) |
| Tape/glue, controls, vision, HMI | 0.5–1 kW |
| Conveyor + lighting | ~0.3 kW |
| **Total** | **~5 kW → ~120 kWh/day at 24/7** |

| Operation model | Energy/day | Energy/case (at 300/h) |
|---|---|---|
| 24/7 | ~120 kWh | 16.7 Wh |
| 1 shift × 8 h | ~40 kWh | 16.7 Wh |

### 7.2 Feasibility verdict (2026 data, surveyed 2026-08-12)

1. **Grid is trivially feasible** `[measured]`: ~$5.1–6.2k/yr (24/7) or
   ~$1.7–2k/yr (shift); ~1–2% of build cost. Baseline.
2. **Solar sizing corrected (honest wall):** a 4–5 kW array is ~3–6×
   undersized — true self-sufficiency needs **30–35 kW / 150–175 m² / 60–80
   kWh battery (24/7)** or **10–12 kW / 55–65 m² / 15–25 kWh (one shift)**.
   Capex ~$67–112k (24/7) or ~$27–48k (one shift); payback vs grid ~12–20 yr;
   **30% federal ITC expired 2026-07-04** (MACRS remains).
3. **Hydrogen is resilience-only** `[measured→hypothesis]`: at actual $5–8/kg
   H₂, generation is ~$0.25–0.50/kWh, 2–3× grid; module capex $25–100k.
   Becomes competitive only at §3.36's $1–2/kg targets. Recommend battery +
   grid; keep H₂ for worst-case outage coverage.
4. **Waste recovery moves demand ~1–3%** (§8) — recovery is architectural,
   not a resizing driver.

### 7.3 Cost of building (2026 vendor lists)

| Station / item | Low | High |
|---|---|---|
| 1 MAG + destacker | $5k | $15k |
| 2 ERECTOR (servo fold arms) | $30k | $60k |
| 3 INSERT (delta robot + vision) | $30k | $80k |
| 4 CLOSE+SEAL (plough + tape head) | $15k | $40k |
| 5 INSPECT (cameras + lighting + reject) | $10k | $30k |
| Conveyors / transfer / guarding | $15k | $40k |
| Control (PLC + drives + IO-Link + HMI + safety) | $15k | $30k |
| Integration / engineering / commissioning (~20%) | $25k | $60k |
| **Line subtotal** | **~$145k** | **~$355k** |

**Midpoint build ≈ $250k.**

| Configuration | Total |
|---|---|
| Grid-connected, 24/7 | **~$150–370k** |
| Solar self-sufficient, 1 shift | ~$175–405k |
| Solar self-sufficient, 24/7 | ~$215–470k |
| 24/7 solar + H₂ resilience | ~$255–540k |

---

## 8. Waste energy recovery

Ranked recovery streams. Servo-regen figure is `[measured]` (sim, from
`experiments/servo_regen.py`); heat figures are component-rating estimates.

| Stream | Source | Recoverable | Daily (8 h shift) | Capture | Priority |
|---|---|---|---|---|---|
| Compressed-air waste heat | compressor ~1.6 kW input, 75–85% as heat | ~1.3–1.5 kW | ~10–12 kWh as heat | heat exchanger on compressor outlet → **preheat the rainwater washdown supply (§6.4)** / winter shop heat | **HIGH** |
| Servo regen `[measured]` | fold settle phase (spring-back works on the motor) | ~8% of fold motoring, ~196 J/axis-cycle | ~0.5 kWh returned to bus | shared EtherCAT DC bus + battery recapture (§3.36 PV+battery); brake resistors only as backstop | **MEDIUM** |
| Vacuum/blow-off | grippers, reject gate | small, low-grade | ~0.5–1 kWh equiv | sequencing (vacuum/air only while gripping) — demand-side, not recovery | LOW |
| Hot-melt / tape-head heat | glue-pot heater ~0.5 kW | minimal | — | insulated pot, duty-cycled heater | LOW |
| Cabinet heat | drives + PLC reject heat | 0.1–0.3 kW seasonal | ~1–2 kWh winter | passive ducting to preheat shop in winter | LOW |
| H₂ fuel-cell CHP | FC exhaust (if H₂ installed) | ~40–50% fuel LHV as heat | ~15–25 kWh | heat exchanger to buffer tank | IF H₂ used |

**Architecture:**
- **Shared DC-bus crosstalk** — one axis regenerating while another motors
  (the 4 fold axes rarely brake together) recycles energy with zero
  conversion loss (T67 applied to power).
- **Battery recapture** — DC-coupling the servo bus to the §3.36 PV battery
  stores regen surplus instead of heating a brake resistor.
- **Demand-side beats recovery** — the biggest air saving is *not building the
  waste*: blower-over-venturi (§6.2) and right-sizing the compressor (§6.1).

**Honest wall:** regen is numerically small (~0.5 kWh/shift — architectural,
not energy, value); air-heat recovery displaces *heating* energy (seasonal),
not electrical draw; every figure is schematic-level, not metered.

---

## 9. Ease of use, maintenance & commissioning

One operator runs the line; everything must be learnable in one shift and
recoverable in under two minutes.

### 9.1 HMI / UX

- One screen per station + overview; every fault is a **click → guided fix**
  (station, failed check, reset sequence), not a code lookup.
- **Live quorum margins** (3 sensor values + disagreement %) — operators
  intervene at ~40–45% before the line stops itself.
- **Reject ledger visible on the HMI** (self-refutation discipline:
  refutations shown, not buried) + the near-crease correction log (PPA-002).
- Recipe library per box size; **changeover is recipe recall, ~1–2 min, no
  tools** (servo positions are digital; plough guides + vacuum tooling are
  tool-less quick-release).

### 9.2 Calibration workflow & tooling **[ADDED]**

Per blank lot (L.O.R.E. — measured, not chosen):
1. Load a test blank of the new lot.
2. **Measure crease depth with a dial/digital crease-depth gauge** and the
   restoring moment with the fold arm's torque feedback (or a handheld torque
   meter).
3. Enter once → feedforward compensator uses it until the lot changes.
4. Value stored with lot ID in the IIoT traceability log.

Tooling kit in the cabinet: crease-depth gauge, box squareness caliper,
torque meter, air pressure gauge, camera focus target.

### 9.3 Maintenance schedule **[ADDED]**

| Frequency | Actions |
|---|---|
| Daily | auto condensate drains; photoeye wipe; reject bin empty; mag hold-open check |
| Weekly | tape head clean; vacuum filter check; guard + interlock visual check |
| Monthly | lubricate fold-arm gearheads; verify torque calibration; air leak listen-check |
| Quarterly | **air leak audit**; camera calibration; safety-function validation (light curtains, STO, e-stop) |
| Annual | receiver pressure-vessel inspection; full e-stop stop-time measurement (re-affirms ISO 13855 S); FMEA review; energy-meter review vs §7.1 |

PM schedule is annunciated on the HMI. **Top-5 spares** in the cabinet: tape
blades, vacuum pads, photoeyes, air filters, encoder cables.

### 9.4 Jam & fault recovery

- Per-station guided recovery (which guards, what's safe, what order) — the
  jam-clear walk is part of the ISO 12100 assessment (highest-frequency human
  interaction).
- A partially formed box goes to **scrap, never back into the flow** (T55c);
  the machine knows which box was in which station.
- Clear all faults → operator reset → invariant checks re-verified before
  resuming (no silent auto-resume).

### 9.5 Commissioning & acceptance protocol **[ADDED]**

FAT/SAT checklist (before release to production):
1. **1 h continuous run at 300 cases/h**; reject rate ≤ target; no watchdog
   FAULTs.
2. **Fault injection**: quorum at ≥50%, stalled axis, missing blank, tape
   misfeed — each must produce the designed stop/verdict.
3. **Safety validation**: every guard/curtain/e-stop trip → STO; e-stop
   stop-time measured → ISO 13855 S confirmed.
4. **Changeover test**: 2 box sizes, ≤2 min each, no tools.
5. **Energy baseline**: per-station power meters logged 1 week; compare to
   §7.1.
6. **Documentation handover**: FMEA, O&M manual, wiring diagrams, risk
   assessment records, spare-parts list, calibration tooling list — per
   EN 415-10 conformity.

---

## 10. Patents & standards (FTO summary)

**Core patents (both Active — a build needs a license or a design-around):**

| Patent | Mechanism | Status |
|---|---|---|
| US9718570B1 (XPAK robotic carton erector) | erector flap-folding sequence | Active to 2035-11-19 |
| US10532842 (Wexxar tape end fold) | tape applicator end-fold at the case sealer | Active |

Surrounding tape-fold art is occupied (Lamus/Intertape/TREA/Flex-Line active);
the tape head is the highest-risk FTO item. **Standards the line must be
designed to:**

| Standard | Applies to |
|---|---|
| EN 415-1 / -10 / -11 | packaging machinery safety / case-packers / erectors |
| ISO 12100 | risk assessment method |
| ISO 13849-1, IEC 62061 | safety function PLr/SILr |
| ISO 13850 | emergency stop |
| ISO 13855 | safety-distance calculation |
| ISO 10218 | robot cell (INSERT) |
| IEC 61800-5-2 | servo STO |
| IEC 60204-1 | electrical equipment of machinery |
| IEC 61131-3:2025 | control programming (shipped ST) |
| IEC 62443-3-3 | control/IIoT cybersecurity |
| ISO 8573-1 | compressed-air quality class |
| FEFCO 0201 | box construction code (RSC) |

---

## 11. Master equipment list — the better equipment, itemized

| Subsystem | Better choice (specific) | Avoid |
|---|---|---|
| Fold servos (4×) | EtherCAT drives, **STO SIL2, shared DC bus** (Beckhoff AX / SEW MOVI-AXIS / Kollmorgen AKD) | standalone AC drives with brake resistors |
| Fold motors | 0.4–1 kW servo + planetary gearhead, **18–23-bit absolute encoder** | incremental encoders |
| Robot (INSERT) | delta (ABB FlexPicker / Fanuc M-3iA) | fixed indexing machine (if SKU flexibility needed) |
| Safety PLC | Pilz PNOZmulti 2 / SICK Flexi Soft / Siemens F | using the recipe PLC for safety |
| Light curtains / interlocks | dual-channel (SICK deTec + non-contact coded switches) | single-channel reed switches |
| Standard PLC | IEC 61131-3:2025 soft-PLC (TwinCAT / B&R / Codesys) | proprietary ladder-only |
| Destack vacuum | **regenerative blower ~0.2 bar** (Becker / Busch) + Bernoulli pads (Piab) | venturi off the air ring |
| Compressor | **VSD rotary screw ~27 scfm** (Atlas Copco GA VSD / Kaeser BSD), oil-free if food-adjacent | oversized fixed-speed screw |
| Air treatment | refrigerated dryer + coalescing filters, ISO 8573-1 2/4/4, auto drains | bare shop air |
| Receiver | ASME vertical ~30 gal, relief + auto drain | homemade tank |
| Tape heads | automatic case taper with end-fold (Wexxar / 3M-Matic class) — §10 license | hand taping |
| Hot-melt | PID + thermocouple applicator (Nordson), insulated pot | exposed heating elements |
| Vision | 2–3 GigE cameras (Basler / Balluff) + Class 1 LED bars | one wide-angle camera, no lighting |
| Blow-offs | regulated ≤30 psi nozzles, 20% duty sequencing | unrestricted nozzles |
| Power | 3-phase + IEC 60204-1, MCCB + RCD, redundant 24 V PSU, UPS for controls | single-phase undersized feed, no UPS |
| Rainwater (§6.4) | ~300 m² metal-roof catchment + PV modules, first-flush diverters + leaf guards, 50 µm + 5 µm filters + UV, 4–10 m³ tank, pump + pressure tank + mains make-up, backflow prevention | potable reuse without treatment; unlabeled cross-connected piping |
| Idle/sleep control (§6.5) | AUTO/IDLE/SLEEP states: drive STO standby, blower idle, compressor trim | leaving fixed loads on during idle |
| Air monitoring (§6.5) | flow meter per air branch on the IIoT gateway + baseline trend | quarterly audit only |
| Condition monitoring (§6.5) | vibration/temperature/pressure trend baselines on the bus → PM suggestions | waiting for the next scheduled maintenance |
| Blow-offs (§6.5) | amplifier/coanda nozzles at ≤30 psi | open pipes; unrestricted nozzles |
| Dust extraction (§6.5) | small cartridge collector at scoring + tape-knife zones | letting fines coat sensors/cameras |
| Scrap handling (§6.5) | compactor/baler fed by the reject ledger | dumping reject scrap unmeasured |
| Hot-water buffer (§6.5) | 200–500 L insulated buffer charging from compressor waste heat | dumping §8 heat when nobody washes |
| Motors & lighting (§6.5) | IE4/IE5 motors on VFDs; LED high-bay with presence control | IE2/IE3 fixed-speed; always-on lighting |
| OEE dashboard (§6.6) | availability/performance/quality live on HMI (EN 415-11) | a reject log nobody reads |
| HMI accessibility (§6.6) | adjustable font/contrast, multilingual layer, dual-modality alarms, slow/jog mode | fixed small text, single language, audio-only alarms |
| Remote access (§6.6) | secure VPN/OPC UA remote diagnostics (IEC 62443-3-3), versioned updates | unauthenticated cloud port |
| Asset documentation (§6.6) | QR/asset tag on every component → datasheet, wiring, PM record, spare part | paper manuals locked in an office |
| HMI | 12–15" panel + §9.1 UX | numeric-only display |
| IIoT | OPC UA gateway, per-station energy meters, IEC 62443-3-3 | unauthenticated cloud port |

---

## 12. Honest walls

- The fold/crease/emanation mappings are **analogies over real mechatronics**;
  the physical laws are classical (elasticity, friction, servo control); no
  repo parameter transfers to a crease depth or hold torque.
- Corrugated-board variability (moisture, flute direction, anisotropy) is the
  dominant real failure source; every blank lot needs its own calibration.
- Throughput, energy, and BOM figures are schematic-level estimates; §9.5
  turns them into measured values after commissioning.
- §4 is a target safety architecture, not a certificate: PL/SIL, guard
  geometry, and ISO 13855 distances need a competent-person risk assessment
  and measured stop times.
- Air figures are component-assumption estimates (±30% on duty/leaks).
- Rainwater figures are climate-assumption estimates (800 mm/yr, uniform vs
  summer-dry): real tank sizing needs the site's rainfall record and the
  actual roof/PV catchment area; and the system is a systems/integration play
  (~80 yr payback on water alone), not a water-bill saver.
- Efficiency figures (standby, leak monitoring, nozzles) are duty-assumption
  estimates: the standby savings exist only where the line actually idles,
  and the air savings depend on the leak rate; §9.5's energy baseline turns
  them into measured values.
- Accessibility items follow general ergonomics/accessibility guidance, not a
  machinery-specific certification; the human-factors targets need operator
  validation (§9.5), not just design intent.
- Both core patents are **Active** — a build needs license or design-around,
  not an assumed freedom to operate.
