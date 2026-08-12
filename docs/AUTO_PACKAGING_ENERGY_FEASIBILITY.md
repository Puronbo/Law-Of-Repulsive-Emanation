# Autonomous Packaging Line — Energy Feasibility & Build Cost

**Purpose:** Answer two questions for the folding-mechanics schematic
(`docs/AUTO_PACKAGING_SYSTEM.md` §5 and its §3.36 hydrogen-photon tie-in):
(1) is the line's energy scheme feasible, and (2) what does building the line
actually cost. Uses 2026 public price data; every figure carries a source and
an honest wall.

**Survey date:** 2026-08-12 · Currency: USD, 2026 market pricing, US context
unless stated.

---

## 0. The load being powered

From `AUTO_PACKAGING_SYSTEM.md` §5 (a schematic-level estimate):

| Load | Power (avg) |
|---|---|
| Servo motion (folding, transfer) | 2–3 kW |
| Vacuum / compressed air | 1–2 kW |
| Tape/glue, controls, vision, HMI | 0.5–1 kW |
| **Total** | **~5 kW** |

Demand scenarios the energy system must cover:

| Operation model | Avg power | Energy/day | Energy/case (at 300/h) |
|---|---|---|---|
| 24/7 run (as §5 assumes) | ~5 kW | **~120 kWh/day** | 16.7 Wh/case |
| 1 shift × 8 h | ~5 kW | ~40 kWh/day | 16.7 Wh/case |
| 1 shift × 10 h | ~5 kW | ~50 kWh/day | 16.7 Wh/case |

> Sanity check `[measured]`: a real servo-driven case erector is rated ~2.1 kW
> at 12–30 cases/min (SiroSilo product data), so ~5 kW average for an
> erector+packer+sealer+inspection line is plausible; the line's low
> throughput (300/h = 5 CPM) means the load is dominated by always-on fixed
> loads (vacuum, controls), not by folding power.

---

## 1. The sizing error in the schematic (honest wall)

`AUTO_PACKAGING_SYSTEM.md` §5 claims *"a 4–5 kW PV array (25–35 m² at ~20%) +
battery covers the day."* **That is true only for a fraction of the stated
demand.**

- 5 kW DC of PV at a US-average ~4.5 peak-sun-hours and 0.8 system efficiency
  yields ~**18 kWh/day** (summer ~25, winter ~10) `[measured, NREL-ish]`.
- The line wants **120 kWh/day** (24/7) or **~40–50 kWh/day** (one shift).
- So the 4–5 kW array covers **~15% of the 24/7 demand**, or ~40–45% of a
  single-shift demand. A battery stores surplus; it does not create energy.
- A 5 kW array is only "covers the day" if the line runs ~4 daylight hours.

**Corrected sizing for 100% solar self-sufficiency** (winter-bounded):

| Operation model | Array needed | Area @ ~200 W/m² | Battery (usable) |
|---|---|---|---|
| 24/7 (120 kWh/day) | **30–35 kW DC** | 150–175 m² | 60–80 kWh |
| 1 shift × 8 h (40 kWh/day) | **10–12 kW DC** | 55–65 m² | 15–25 kWh |

The §5 figure is therefore ~3–6× undersized for true self-sufficiency. The
feasibility analysis below uses the corrected sizes. `[honest wall]`

---

## 2. Energy feasibility — option by option

### 2.1 Grid power (baseline) — trivially feasible

US commercial/industrial power averages ~$0.11–0.16/kWh (2026).

| Model | Energy/yr | Grid cost/yr |
|---|---|---|
| 24/7 | ~43,800 kWh | **~$5,100–6,200** |
| 1 shift × 8 h | ~14,600 kWh | **~$1,700–2,000** |

No generation capex beyond grid connection (~$5–15k one-time, site-dependent).
This is the financially rational baseline: the energy bill is ~1–2% of the
machine's build cost.

### 2.2 Solar PV + battery — feasible, capital-heavy, pays back

2026 installed prices (US): small commercial 10–35 kW ≈ **$1.5–2.5/W**
(EnergySage small-system averages to ~$2.8/W; SEIA/WoodMac commercial
benchmark $1.71/W, up ~9% YoY on tariffs); LFP battery C&I ≈ **$250–450/kWh**
installed (howtostoreelectricity 2026; small systems pay toward the top of
the band).

| Model | PV capex | Battery capex | Inverter/EMS | Total energy system |
|---|---|---|---|---|
| 24/7 self-sufficient | $45–70k | $19–34k | $3–8k | **~$67–112k** |
| 1-shift self-sufficient | $18–30k | $6–12k | $3–6k | **~$27–48k** |

Payback vs grid (24/7, ~$5.6k/yr avoided): **~12–20 yr** at current prices —
only marginally attractive, and it fails if export/self-consumption rules are
unfavorable. Note the 30% federal ITC **expired for projects not started by
2026-07-04** under the One Big Beautiful Bill Act (2026 reporting), and
MACRS/depreciation is the remaining federal benefit — a deadline that matters
if this is a real build `[honest wall]`.

**Verdict:** feasible, and the solar hardware itself is record-cheap (modules
~$0.30/W), but a *self-sufficient* line needs 3–6× the array the schematic
stated, and the payback vs grid is marginal-to-negative at 2026 prices.

### 2.3 Hydrogen fuel cell backup — technically feasible, economically resilience-only

The §3.36 hydrogen-photon tie-in proposes an H₂ fuel-cell module as backup.

**Capex (2026):** a ~5 kW PEM backup system costs **$25–100k installed**
(typical $30–50k for 1–5 kW turnkey; 5–10 kW portable PEM $25–45k; 30 kW with
storage $40–90k). H₂ storage cylinders add ~$8–20k. Stack life 20,000–40,000 h.

**Fuel economics:** PEM at ~50–60% electrical efficiency → ~16–20 kWh(e)/kg H₂.

| H₂ price | Cost/kWh(e) generated | vs grid |
|---|---|---|
| $8/kg (US grey, high) | ~$0.40–0.50 | ~3× grid |
| $5–7/kg (green, actual §3.36) | ~$0.25–0.44 | ~2–3× grid |
| $2/kg (§3.36 *target*) | ~$0.10–0.12 | ≈ grid |
| $1/kg (§3.36 *target*) | ~$0.05–0.06 | below grid |

**Verdict:** at actual 2026 H₂ prices ($5–8/kg), fuel-cell generation is
2–3× grid cost, and the module capex (~$30–50k) exceeds a year of grid power.
It is justified **only as emergency resilience** (multi-day outages, no grid
access), never as the daily energy source. The §3.36 feasibility hinges
exactly on its own measured gap: green H₂ at **$5–7/kg actual vs $2/$1
targets**. At $1–2/kg it becomes competitive; at today's prices it is not.

---

## 3. Cost of building the line (hardware, 2026 market)

Prices from public 2025–2026 vendor lists (Cleveland Equipment, Rocket
Industrial, SiroSilo, Xolertic, MyWay) for RSC erectors/sealers:

| Station / item | Low | High | Notes |
|---|---|---|---|
| 1 MAG + destacker | $5k | $15k | vacuum feed, double-sheet detection |
| 2 ERECTOR (servo fold arms) | $30k | $60k | servo erectors: CE-15 $27k … ERX-15 $46k; robotic $20–200k |
| 3 INSERT (delta robot + vision) | $30k | $80k | robotic packers |
| 4 CLOSE+SEAL (plough + tape head) | $15k | $40k | tape-head end-fold needs license/design-around (US10532842) |
| 5 INSPECT (2–3 cam + lighting + reject) | $10k | $30k | vision + reject gate |
| Conveyors / transfer / guarding | $15k | $40k | EN 415-10 guarding |
| Control: PLC + EtherCAT drives + IO-Link + HMI + safety | $15k | $30k | IEC 61131-3 layer |
| Integration / engineering / commissioning (~20%) | $25k | $60k | |
| **Line subtotal** | **~$145k** | **~$355k** | |

Consistent with the market: entry automatic case formers start ~$5–26k,
integrated erect+pack+seal all-in-ones land $100–300k, and advanced robotic
cells exceed $200k. **Midpoint build ≈ $250k.**

## 4. Total project cost by configuration

| Configuration | Machine | Energy | H₂ backup | **Total** |
|---|---|---|---|---|
| Grid-connected, 24/7 | $145–355k | grid ($5–15k connect) | — | **~$150–370k** |
| Solar self-sufficient, 1 shift | $145–355k | $27–48k | — | **~$175–405k** |
| Solar self-sufficient, 24/7 | $145–355k | $67–112k | — | **~$215–470k** |
| 24/7 solar + H₂ resilience | $145–355k | $67–112k | +$40–70k | **~$255–540k** |

---

## 5. Feasibility verdict

1. **The load is feasible** `[measured]`: ~5 kW average is small, ordinary
   grid infrastructure handles it, and the energy bill (~$2–6k/yr) is noise
   against the machine capex.
2. **The schematic's solar sizing is wrong by 3–6×** `[honest wall]`: true
   self-sufficiency needs 30–35 kW / 150–175 m² (24/7) or 10–12 kW (one
   shift), not 4–5 kW. A 4–5 kW array covers only ~15–45% of demand.
3. **Solar is feasible but marginal vs grid** at 2026 prices (~12–20 yr
   payback, ITC just expired); it makes sense where grid access is
   unavailable or reliability is critical, not on pure economics.
4. **Hydrogen is resilience-only** `[measured → hypothesis]`: 2–3× grid cost
   at actual $5–8/kg H₂; it becomes feasible only if §3.36's $1–2/kg targets
   materialize. Recommend a battery + (if needed) grid tie; keep H₂ for
   worst-case outage coverage.
5. **Cost of building**: ~$150–370k grid-connected (midpoint ~$250k); add
   $27–112k for solar self-sufficiency and $40–70k more for H₂ backup. Energy
   is 10–40% of project cost depending on how self-sufficient you go.

---

## 6. Sources (surveyed 2026-08-12)

- Solar PV installed prices: EnergySage (2026, $2.5–3.5/W res, small-system
  table), SEIA/Wood Mackenzie Q4 2025 ($1.71/W commercial), NREL ATB.
- Battery storage: howtostoreelectricity.com 2026 (C&I $250–450/kWh,
  residential $400–700/kWh, BNEF turnkey $117/kWh global), NREL 2025 storage
  projections, Lazard LCOS 2026 ($210–292/MWh non-ITC US).
- Hydrogen fuel cells: Kurlon 2026 guide (1–5 kW $25–100k), IndexBox US
  portable-H₂ market (PEM $2.5–4.5k/kW), Battelle/DOE PEM backup cost studies,
  Electrical Trader (H₂ $3–8/kg, FC $/kWh ranges), NLR/NREL stationary PEM
  cost analysis.
- Case machinery: Cleveland Equipment, Rocket Industrial, SiroSilo, Xolertic,
  MyWay Machinery (2025–2026 catalog/guide prices).

*This is a desk survey with schematic-level estimates, not a quotation or an
investment recommendation. Confirm all prices with current vendors and review
tax/incentive eligibility before reliance.*
