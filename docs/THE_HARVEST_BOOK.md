# THE_HARVEST_BOOK — force, energy, and extraction from natural systems

> **Authority, stated plainly.** This Book answers six questions in closed
> form — slingshot launch loads, terraforming budgets, natural-disaster
> energy, earthquake vibration feeding, forest heat capture, and heavy
> cloud netting. Every equation is written out, every number is recomputed
> by `experiments/harvest_energy.py` from the equation with the stated
> constants, and the artifact `data/harvest_energy_data.json` (gitignored,
> regenerable) is the lockstep record. The verdicts are `ANALYTIC` where
> the equation's output with standard constants is the claim, `HYPOTHESIS`
> where the equation holds but the input inventory is an assumption, and
> `[honest wall]` where the physics itself closes the door. Nothing here is
> simulated; the equations are the measurements.

---

## BOOK I — THE SLINGSHOT AND THE PASSENGER

### Ch. 1  Two slingshots

The word names two machines that feel nothing alike to the passenger.

**The gravity assist** is not a sling at all in the passenger frame — the
spacecraft coasts on an orbit and the planet's gravity bends the path. The
trajectory is free fall the whole way, so the contact force on the body is
zero:

    G_passenger = 0          (gravity assist: inertial coasting)

Survivability is not the question; weightlessness is the experience. Every
interplanetary probe and every Moon-return trajectory is this slingshot,
and no crew has ever felt it as an acceleration. But the assist is a real
machine, and its mechanics are closed form. A hyperbolic flyby at
periapsis radius r_p past a body of gravitational parameter mu, arriving
with excess speed v_inf, bends the incoming velocity vector by delta and
hands the spacecraft a velocity-vector turn of dv:

    sin(delta/2) = 1 / (1 + r_p v_inf^2 / mu)     (bend half-angle)
    dv = 2 v_inf sin(delta/2)                     (velocity-vector turn)
    a_p = mu / r_p^2                              (periapsis gravity: the load)

The bend is set by the periapsis radius alone once v_inf and mu are given —
a "free" boost whose reaction body is the whole planet. The passenger load
is a_p: at closest approach the free-fall trajectory curves at exactly the
planet's gravity at that radius. The numbers (`harvest_energy.py`, flyby
rows; v_inf = 5 km/s):

| Flyby | r_p | bend delta | dv | a_p (passenger load) |
|---|---|---|---|---|
| Earth, 620 km periapsis | 7.0e6 m | 88° | 6.9 km/s | 0.83 g |
| Jupiter, cloud tops | 7.1e7 m | 161° | 9.9 km/s | 2.56 g |

The strongest gravity assist in the Solar System loads its passenger at
**2.6 g for a few minutes**; an Earth assist is **under 1 g**. The true
slingshot is the most survivable launch you can take — the assist's
acceleration is never more than the planet's own surface gravity, and the
boost is free.

**The centrifuge slingshot** is a true sling: a capsule is spun at the end
of a long arm and released. The passenger feels the centripetal force that
holds the capsule on its circle — a sustained radial acceleration:

    a = v^2 / r                    (centripetal acceleration, m/s^2)
    G = a / g = v^2 / (r g)        (in units of Earth gravity)

with v the release speed (m/s), r the arm length (m), g = 9.80665 m/s^2.

### Ch. 2  Survivability, and the corner equations

Two corner equations decide whether the ride is survivable: the release
speed an arm can give at a tolerated g, and the arm a target speed demands.

    v_max(G, r) = sqrt(G g r)      (fastest release at a given G, r)
    r_min(v, G) = v^2 / (G g)      (shortest arm for a target v at G)

Human tolerances, stated with their measured names: sustained crew flight
runs ~4 g (Soyuz, Crew Dragon, ~200 s), trained +Gx for seconds reaches
~9 g, and Stapp's 46 g (rocket sled, <1 s) is the short-duration ceiling.
`[analytic]` These are standard physiology figures, stated so the corners
are checkable.

The numbers (`experiments/harvest_energy.py`, slingshot section):

| Case | Equation | Number |
|---|---|---|
| gravity assist | G = 0 | 0 g — inertial |
| centrifuge, 4 g, 100 m arm | v = sqrt(4·g·100) | 63 m/s (226 km/h) |
| centrifuge, 9 g, 100 m arm | v = sqrt(9·g·100) | 94 m/s (338 km/h) |
| centrifuge, 46 g, 100 m arm | v = sqrt(46·g·100) | 212 m/s (765 km/h) |
| centrifuge, 10^4 g, 100 m arm (payload) | v = sqrt(10^4·g·100) | 3132 m/s (payload-rated) |
| LEO 7905 m/s at 4 g | r = v^2/(4 g) | arm = 1593 km, 202 s sustained |
| LEO 7905 m/s at 9 g | r = v^2/(9 g) | arm = 708 km |
| LEO 7905 m/s at 3 g | r = v^2/(3 g) | arm = 2124 km |

**The finding, plainly.** A passenger-rated "slingshot space shuttle" is
either a gravity assist — 0 g plus a boost of up to 2 v_inf sin(delta/2)
for free, but it is an orbit change, not a launch — or
a centrifuge, and a centrifuge that reaches orbit at crew limits needs an
arm of a thousand-plus kilometers. At any arm a builder can actually erect
(tens to hundreds of meters), the survivable release is suborbital by an
order of magnitude. The 10^4 g spin launch that industry is testing is a
payload machine, not a passenger machine. `[honest wall]` The walls are the
arithmetic, not the materials: no arm material changes a crew limit of ~4 g
sustained, and 46 g is survivable only for about a tenth of a second. The
assist's wall is the same arithmetic: its passenger load is a_p = mu/r_p^2,
and r_p can only approach the planet's own surface — so the ride is capped
at the planet's surface gravity (0.83 g at Earth, 2.56 g at Jupiter), the
gentlest acceleration in spaceflight.

---

## BOOK II — TERRAFORMING: THE WARMING BUDGET

### Ch. 3  The one-time heat budget

Warming a planet is a heat-transfer problem. The closed form sums three
terms — the atmosphere's heat, the polar CO2 sublimation, and the top layer
of regolith:

    Q = m_atm · c_p · dT                      (raise the atmosphere)
      + M_CO2 · L_subl                        (sublimate the polar CO2 ice)
      + rho · d · A · c_s · dT                (warm d meters of regolith)

with the Mars numbers: atmospheric mass m_atm = P·A/g = 636·1.448e14/3.71 =
2.48e16 kg, c_p(CO2) = 800 J/(kg·K), dT = 78 K (288 target − 210 present),
M_CO2 = 1.6e16 kg polar CO2 ice `[hypothesis]` (residual-cap inventory is a
stated assumption), L_subl = 5.74e5 J/kg, rho = 1500 kg/m^3 regolith,
d = 1 m, c_s = 800 J/(kg·K).

    Q_atm  = 2.48e16 · 800 · 78   = 1.55e21 J
    Q_cap  = 1.6e16 · 5.74e5      = 9.18e21 J
    Q_surf = 1500·1·1.448e14·800·78 = 1.36e22 J
    Q_total                        = 2.43e22 J

Compare with Earth's annual primary energy (~5.95e20 J):

    Q_total / E_Earth-annual = 40.8

The timescales at a delivered power: 1 TW → 770 yr; 100 TW → 7.7 yr. A
mirror fleet delivering 100 TW (the Zubrin-class, ~1e12 m^2 of reflector)
warms the one-time budget in under a decade.

### Ch. 4  The sustaining forcing wall

The one-time budget is the easy half. A planet at 288 K must *stay* at
288 K, and it radiates as a blackbody:

    P_sustain = sigma · (T_target^4 − T_now^4) · A_planet

    = 5.670e-8 · (288^4 − 210^4) · 1.448e14
    = 5.670e-8 · 4.94e9 · 1.448e14
    = 4.05e16 W  =  40.5 PW          (280 W/m^2 over the whole planet)

**The finding.** Sustaining 288 K needs ~40.5 PW of continuous forcing —
four orders of magnitude more than the whole of human energy use — unless
greenhouse gases supply the W/m^2. The one-time warm is a few decades at
100 TW; the *sustain* is the binding constraint, and it is a radiative
wall, not an engineering one. `[honest wall]` The blackbody term assumes
present-day emissivity; a thickened CO2 atmosphere changes both emissivity
and albedo, which is precisely why every terraforming plan's first step is
not heating but *thickening* — the equation that decides is this one, read
backward: reduce sigma_effective, and P_sustain falls.

---

## BOOK III — NATURAL DISASTER ENERGY CAPTURE

### Ch. 5  The measured energy of the disasters

**Earthquake.** The Gutenberg–Richter energy-magnitude relation, in
Joules:

    log10 E = 1.5 M_w + 4.8

| M_w | E (J) | Earth annuals |
|---|---|---|
| 6.0 | 6.3e13 | 1e-7 |
| 7.0 | 2.0e15 | 3e-6 |
| 8.0 | 6.3e16 | 1e-4 |
| 9.0 | 2.0e18 | 3e-3 |
| 9.5 | 1.1e19 | 2e-2 |

**Hurricane.** A large hurricane carries wind kinetic energy E_kin ~ 1.3e17 J
and releases latent heat at ~6e14 W (the engine that replenishes the wind).
A 150 m turbine rotor in a 50 m/s eyewall, at the Betz limit:

    P = (16/27) · (1/2) · rho · A · v^3
      = (16/27) · 0.5 · 1.225 · pi·75^2 · 50^3  =  8.0e8 W  =  800 MW

**Tsunami.** Shallow-water energy scales with amplitude squared:

    E = (1/2) · rho · g · H^2 · L · W

    1 m wave over a 1000 km front: 1.0e15 J;  3 m wave: 9.1e15 J.

**Tornado.** Total energy ~1.5e10 J (range 1e9–3e10 J) — city-block-scale
compared with the quake and the storm.

### Ch. 6  The capture limits: Betz, Carnot, and the duty cycle

Every capture path is throttled by a theorem and by the clock:

- **Wind:** Betz, 16/27 of the swept power (already in Ch. 5).
- **Heat:** Carnot, eta ≤ 1 − T_cold/T_hot; a storm's heat is low-grade,
  and the ocean below it is the hot reservoir.
- **Duty cycle:** the wall that decides. An M7 quake is ~1% capturable in
  the most optimistic reading; once per 50 years at a site:

    P_annualized = E · eta / T_between-events
                 = 2.0e15 · 0.01 / (50 yr)  =  12.6 kW

Twelve kilowatts from a once-a-generation catastrophe. The disasters hold
enormous energy; they arrive on a duty cycle of 10^-7 to 10^-3, so their
**capture as infrastructure is a frequency problem, not a magnitude
problem.** `[honest wall]` Capture would require machines inside the event
(a rotor in the eyewall, a TMD in the shaking building); the energy is
concentrated exactly where the equipment cannot stand. The honest use of
disaster energy is not the grid — it is the sensors that survive the event.

---

## BOOK IV — EARTHQUAKE VIBRATION FEEDING

### Ch. 7  The resonant harvester

Ground motion y(t) = Y·sin(w·t) shakes a proof mass m on a spring tuned to
w. At resonance, the power extracted through the damper (electrical +
mechanical, total damping ratio zeta) is

    P_max = m · w^3 · Y^2 / (4 · zeta)

This is the closed form for a linear resonant energy harvester: all of the
power is proportional to the cube of frequency and the square of ground
displacement, and inversely to damping.

### Ch. 8  The verdict: sensors, not grids

The three regimes, computed in `harvest_energy.py`:

| Regime | Inputs | P_max |
|---|---|---|
| ambient micro-vibration | 0.1 kg, 1 Hz, Y = 0.1 mm, zeta = 0.02 | 3.1 µW |
| tuned mass damper, 660 t (Taipei 101 class) | 6.6e5 kg, 0.2 Hz, Y = 0.1 m, zeta = 0.05 | 65.5 kW |
| 10 kg harvester, strong ground motion | 10 kg, 1 Hz, Y = 1 mm, zeta = 0.05 | 12.4 mW |

The TMD case is the interesting one: during strong shaking a building-scale
mass damper extracts ~65 kW — but that is the building's own kinetic energy
being dumped, over ~100 s, yielding ~1.8 kWh per event, once per decades at
any one site. Annualized:

    E_event / T_between-events = 6.5e6 J / (50 yr)  =  4.2 mW average

**The finding.** Earthquake "feeding" is real in the equation and
negligible as a power source: micro-to-kiloWatts for seconds, milliwatts
annualized. What the equation does power is the right thing — a resonant
harvester's 3 µW ambient, 12 mW strong-shaking output is exactly the
budget of a self-powered seismic sensor: the device wakes, records,
transmits, and sleeps, with no line and no battery change. `[honest wall]`
The 65 kW TMD number is not free energy; it is dissipation that already
happens, metered. Feeding a grid on earthquakes is arithmetic; powering the
early-warning network is engineering.

---

## BOOK V — FOREST HEAT CAPTURE

### Ch. 9  The forest as solar collector

A forest is a solar collector with a storage tank. The input and the store:

    P_sun = S · A                       (annual-mean irradiance)
    E_stored = HHV_wood · m_biomass     (chemical store)

    hectare:  S = 150 W/m^2 mean  ->  P_sun = 1.5 MW/ha
              standing 200 t/ha dry  ->  E = 3.6e12 J/ha

### Ch. 10  The 1% wall, and the fire path

Photosynthesis stores a fraction of the sun:

    NPP ~ 15 t dry/ha/yr  ->  E = 2.7e11 J/ha/yr
    eta_photo = E / (P_sun · t_yr) = 2.7e11 / 4.73e13 = 0.006  (0.6%)

Sustainable harvest, burned at ~35% electrical efficiency:

    P_harvest = 2.7e11 J/ha/yr / 3.15e7 s = 8.6 kW/ha  ->  0.3 W/m^2 of electricity

The **fire path** concentrates the store: a crown fire burns ~10 kg/m^2 at
18 MJ/kg over a 100 km^2 fire:

    Q_fire = 10 · 1.8e7 · 1e8 = 1.8e16 J  (~4.3 Mt TNT thermal)

**The finding.** The forest's "heat capture" is bounded by the
photosynthetic ~1% wall — a hectare stores ~0.6% of its solar input as
biomass, and electricity is that times ~35%. The fire path does not beat
the wall; it releases decades of storage in hours, which is the disaster
analog of BOOK III: concentrated, sporadic, and dangerous to stand in.
`[honest wall]` Numbers are for temperate forests with stated NPP; tropical
yields run roughly double. The wall — ~1% of the sun — is universal.

---

## BOOK VI — HEAVY CLOUD NETTING

### Ch. 11  The cloud's water inventory

A cloud's water mass is the liquid-water content times its volume:

    M_cloud = LWC · V

    cumulonimbus at LWC = 1 g/m^3:
      10 km^3 cell  ->  1e4 t
      100 km^3 cell ->  1e5 t

A hundred thousand tonnes of water overhead, unreachable from below.

### Ch. 12  Netting at the ground

Ground fog nets catch the fraction of that inventory that reaches the
surface — the equation is a mass flux through the mesh:

    Q = eta · A · v_wind · LWC

    eta = 0.3, A = 1 m^2, v = 3 m/s, LWC = 0.2 g/m^3:
    Q = 0.3 · 1 · 3 · 0.2e-3 = 1.8e-4 kg/s  =  15.5 L/m^2/day
    a 40 m^2 net: 620 L/day        (measured sites: 3-10 L/m^2/day)

Seeding rearranges, it does not create: a 1 km^2 cloud seeded to 1 mm of
rain yields 1e3 m^3 = 1e6 L — water already in the air, brought down.

**The finding.** "Heavy cloud netting" as a water source is arithmetic at
the ground and a store at altitude: nets work where clouds touch the
ground (fog: liters per square meter per day), and the 1e4–1e5 t cumulus
inventory is out of reach. The conservation that binds all of it: netting
cannot exceed the atmosphere's moisture flux — it collects what already
falls or would have fallen, earlier and at the chosen point. `[honest
wall]` Seeding assumes the precipitable water exists; in a dry air mass
there is nothing to bring down.

---

## BOOK VII — HONEST WALLS AND THE ONE-SENTENCE THEORY

1. **Analytic is not measured.** Every verdict here is `ANALYTIC` — the
   equation with stated constants — or `HYPOTHESIS` where an inventory
   (polar CO2, NPP, LWC) is assumed. The equations are the point; the
   constants are checkable; nothing is simulated.
2. **The duty cycle decides.** Disasters and fires concentrate energy at
   frequencies 10^-7 to 10^-3; their capture annualizes to kilowatts. The
   wall is frequency, not magnitude.
3. **Crew limits are arithmetic, not materials.** 4 g sustained and 46 g
   for a tenth of a second bound every human launch; no arm design moves
   them.
4. **The sustain wall.** Terraforming's binding constraint is the
   continuous forcing a blackbody demands, not the one-time heat.
5. **Extraction obeys conservation.** Every capture — fog, seeding,
   biomass, vibration — collects a flow that already exists; the harvest
   is a tax on a flux, and the tax is bounded by the flux.

**The Book's one-sentence theory:** *Every natural system the Book touches
is a flow — a circle of acceleration, a radiant balance, a moisture flux, a
seismic passing — and the honest question is never how much energy it
holds but at what duty cycle and through which theorem it can be tapped: a
slingshot's passenger survives a gravity assist at 0 g but not a
centrifuge at launch scale, a planet warms for decades but must be forced
forever, disasters hold exa-to-zetta-joules on a 10^-6 clock, an
earthquake feeds sensors not grids, a forest stores 0.6% of the sun, and a
cloud is a store, not a tap.*

---

## Appendix — the equations, the numbers, and the artifact

| Book claim | Equation | Number | Asset |
|---|---|---|---|
| gravity assist passenger load | G = 0 | 0 g | `experiments/harvest_energy.py` |
| flyby bend and boost | sin(delta/2) = 1/(1 + r_p v_inf^2/mu); dv = 2 v_inf sin(delta/2) | Earth 88°, 6.9 km/s; Jupiter 161°, 9.9 km/s | `data/harvest_energy_data.json` |
| flyby passenger load | a_p = mu/r_p^2 | 0.83 g Earth; 2.56 g Jupiter | `data/harvest_energy_data.json` |
| centrifuge acceleration | a = v^2/r, G = v^2/(r g) | 63 m/s at 4 g, 100 m | `data/harvest_energy_data.json` |
| orbital arm corners | r = v^2/(G g) | 708 km at 9 g; 1593 km at 4 g | `data/harvest_energy_data.json` |
| payload spin launch | v = sqrt(G g r) | 3132 m/s at 10^4 g, 100 m | `data/harvest_energy_data.json` |
| terraforming one-time budget | Q = m c_p dT + M L + rho d A c dT | 2.43e22 J (40.8 Earth annuals) | `data/harvest_energy_data.json` |
| terraforming sustain wall | P = sigma(T^4 − T0^4) A | 40.5 PW (280 W/m^2) | `data/harvest_energy_data.json` |
| earthquake energy | log10 E = 1.5 M_w + 4.8 | 2.0e15 J (M7); 2.0e18 J (M9) | `data/harvest_energy_data.json` |
| hurricane capture | P = (16/27)(1/2) rho A v^3 | 800 MW per 150 m rotor at 50 m/s | `data/harvest_energy_data.json` |
| tsunami energy | E = (1/2) rho g H^2 L W | 1.0e15 J (1 m, 1000 km) | `data/harvest_energy_data.json` |
| disaster duty cycle | P_annual = E eta / T | 12.6 kW (M7, 1%, per 50 yr) | `data/harvest_energy_data.json` |
| vibration feeding | P = m w^3 Y^2/(4 zeta) | 3.1 µW ambient; 65.5 kW TMD; 12.4 mW | `data/harvest_energy_data.json` |
| TMD per-event energy | E = P t | 1.8 kWh per strong event | `data/harvest_energy_data.json` |
| forest solar input | P = S A | 1.5 MW/ha at 150 W/m^2 | `data/harvest_energy_data.json` |
| forest storage | E = HHV m | 3.6e12 J/ha (200 t/ha) | `data/harvest_energy_data.json` |
| photosynthesis wall | eta = E/(P t) | 0.6% | `data/harvest_energy_data.json` |
| crown fire heat | Q = q_m · A | 1.8e16 J (4.3 Mt TNT, 100 km^2) | `data/harvest_energy_data.json` |
| cloud water inventory | M = LWC V | 1e4 t (10 km^3); 1e5 t (100 km^3) | `data/harvest_energy_data.json` |
| fog capture | Q = eta A v LWC | 15.5 L/m^2/day; 620 L/day at 40 m^2 | `data/harvest_energy_data.json` |
| seeded rain yield | Q = depth · area | 1e3 m^3 per km^2 at 1 mm | `data/harvest_energy_data.json` |

The artifact `data/harvest_energy_data.json` is regenerated by
`python experiments/harvest_energy.py`; it is gitignored, like every
regenerable verdict in this repository, and the book and the artifact stay
in lockstep because the book's numbers are the artifact's.
