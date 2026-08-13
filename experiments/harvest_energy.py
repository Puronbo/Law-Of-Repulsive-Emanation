"""
harvest_energy.py
=================
The force, energy, and extraction book, reduced to closed forms. Every
number below is recomputed here from its equation with stated constants,
and written to data/harvest_energy_data.json so the book's appendix and the
artifact stay in lockstep. Nothing here is simulated: the verdicts are
ANALYTIC (the equation's output with the stated constants) or HYPOTHESIS
(the equation holds but the input inventory is an assumption).

The six questions, and their closed forms:

 1. SLINGSHOT g-force on passengers. Two slingshots exist:
      gravity assist  - inertial coasting; passengers feel ~0 g
                       flyby mechanics: bend sin(delta/2) = 1/(1 + r_p v_inf^2/mu)
                       boost dv = 2 v_inf sin(delta/2); periapsis gravity
                       a_p = mu / r_p^2  (the passenger load, ~<1-2.6 g)
      centrifuge     - spin a capsule on an arm, release; centripetal
                       acceleration  a = v^2 / r,  G = v^2 / (r g)
      survival corners:  v_max(G, r) = sqrt(G g r)      (max release speed)
                         r_min(v, G) = v^2 / (G g)      (arm for a target v)
      Human tolerances: ~4-5 g sustained crew (Soyuz/crew Dragon),
      ~9 g trained +Gx for seconds, Stapp's 46 g the <1 s ceiling.
      Payload (non-human) spin launches run ~10^4 g.

 2. TERRAFORMING warming budget. One-time heat:
      Q = m_atm c_p dT        (raise the atmosphere)
        + M_CO2 L_subl        (sublimate the polar CO2 ice)
        + rho d A c_s dT      (warm the top layer of regolith)
      Sustaining forcing (blackbody wall):
      P_sustain = sigma (T_target^4 - T_now^4) * A_planet

 3. DISASTER ENERGY. Earthquake (Gutenberg-Richter, Joules):
      log10 E = 1.5 M_w + 4.8
      Hurricane: wind kinetic E_kin ~ 1.3e17 J; latent release ~6e14 W;
      per-turbine capture  P = (16/27) * (1/2) rho A v^3   (Betz)
      Tsunami: E ~ (1/2) rho g H^2 L W   (amplitude-squared scaling)
      Tornado: E ~ 1e9-3e10 J

 4. EARTHQUAKE VIBRATION FEEDING. Resonant harvester (base excitation
    amplitude Y, angular frequency w, proof mass m, damping ratio zeta):
      P_max = m w^3 Y^2 / (4 zeta)        (at resonance, w = w_n)

 5. FOREST HEAT CAPTURE. Forest as solar collector:
      solar input  P_sun = S * A          (annual-mean irradiance)
      stored       E = HHV_wood * m_biomass
      harvest      P = m_dot_fuel * HHV * eta_plant
      photosynthetic efficiency ~ 1%  - the classic wall.

 6. HEAVY CLOUD NETTING. Water inventory and capture:
      M_cloud = LWC * V                    (liquid-water content x volume)
      fog catch Q = eta * A * v_wind * LWC (ground fog nets)
      seeding yields rain ~ depth * footprint

Usage: python harvest_energy.py
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
OUT_FILE = os.path.join(DATA, "harvest_energy_data.json")

G = 9.80665            # m/s^2, standard gravity
SIGMA = 5.670374419e-8  # W/m^2/K^4, Stefan-Boltzmann
RHO_AIR = 1.225         # kg/m^3
RHO_WATER = 1025.0      # kg/m^3 (seawater)
RHO_REGOLITH = 1500.0   # kg/m^3
CP_CO2 = 800.0          # J/(kg K), Mars CO2 atmosphere at ~250 K
L_SUBL_CO2 = 5.74e5     # J/kg, latent heat of CO2 sublimation
HHV_WOOD = 1.8e7        # J/kg dry wood (18 MJ/kg)
SEC_YEAR = 365.25 * 86400.0


def banner(title):
    print("=" * 72)
    print(title)
    print("=" * 72)


# ---------------------------------------------------------------------- #
# 1. slingshot                                                           #
# ---------------------------------------------------------------------- #
def slingshot():
    out = {"G_gravity_assist_g": 0.0,
           "note_gravity_assist": "gravity assist is inertial coasting; "
                                  "no contact force, ~0 g",
           "crew_sustained_g": 4.0,
           "crew_seconds_g": 9.0,
           "stapp_ceiling_g": 46.0}
    v_orb = 7905.0  # m/s, LEO reference
    radii = {}
    for crew_g in (3.0, 4.0, 5.0, 9.0):
        radii["r_km_at_%dg_for_LEO" % crew_g] = \
            v_orb * v_orb / (crew_g * G) / 1000.0
    out["r_km_at_LEO_vs_crew_g"] = radii
    speeds = {}
    for r in (100.0, 1000.0, 100e3):
        speeds["v_ms_at_4g_r%gm" % r] = math.sqrt(4.0 * G * r)
    out["v_ms_at_4g_vs_arm"] = speeds
    out["v_ms_at_9g_r100m"] = math.sqrt(9.0 * G * 100.0)
    out["v_ms_at_46g_r100m"] = math.sqrt(46.0 * G * 100.0)
    out["v_ms_at_1e4g_r100m_payload"] = math.sqrt(1e4 * G * 100.0)
    out["t_s_at_4g_to_LEO"] = v_orb / (4.0 * G)
    # the true astronautical slingshot: the powered flyby. The planet bends
    # the hyperbolic excess-velocity vector by delta, periapsis radius r_p,
    # gravitational parameter mu, excess speed v_inf:
    #   sin(delta/2) = 1 / (1 + r_p v_inf^2 / mu)
    #   dv = 2 v_inf sin(delta/2)          (velocity-vector turn magnitude)
    #   a_p = mu / r_p^2                   (periapsis gravity - the load)
    flybys = {}
    for name, mu, r_p, v_inf in (
            ("earth_low", 3.986004418e14, 7.0e6, 5e3),
            ("jupiter_cloudtops", 1.26686534e17, 7.1e7, 5e3)):
        s_half = 1.0 / (1.0 + r_p * v_inf * v_inf / mu)
        delta_deg = 2.0 * math.degrees(math.asin(s_half))
        flybys[name] = {
            "bend_deg": round(delta_deg, 1),
            "dv_ms": round(2.0 * v_inf * s_half, 0),
            "a_periapsis_g": round((mu / (r_p * r_p)) / G, 2),
        }
    out["flyby_mechanics"] = flybys
    out["verdict"] = ("ANALYTIC: gravity assist = 0 g (inertial). A "
                      "centrifuge launch at 4 g reaches only 63 m/s on a "
                      "100 m arm; LEO at 4 g needs a ~1593 km arm and ~202 s "
                      "of sustained 4 g (crew-survivable, but a machine of "
                      "planetary scale). Human-rated spin launch to orbit is "
                      "arithmetically closed at realistic arm sizes; 10^4 g "
                      "payload slingshots reach ~3.1 km/s on a 100 m arm. The "
                      "true slingshot - the gravity-assist flyby - turns the "
                      "excess-velocity vector for free (Earth at v_inf=5 km/s "
                      "and 620 km periapsis bends 88 deg for dv ~6.9 km/s; "
                      "Jupiter bends ~161 deg for ~9.9 km/s) while the "
                      "passenger load at periapsis is a_p = mu/r_p^2, under "
                      "1 g at Earth and ~2.6 g at Jupiter: a passenger-rated "
                      "slingshot rides the assist at launch-pad gravity, not "
                      "launch gravity.")
    return out


# ---------------------------------------------------------------------- #
# 2. terraforming                                                        #
# ---------------------------------------------------------------------- #
def terraform():
    g_mars = 3.71          # m/s^2
    a_mars = 1.448e14      # m^2 surface area
    p_mars = 636.0         # Pa surface pressure
    m_atm = p_mars * a_mars / g_mars
    dT = 78.0              # 288 K target - 210 K present mean
    m_caps = 1.6e16        # kg CO2 ice in the residual polar caps (stated)
    q_atm = m_atm * CP_CO2 * dT
    q_cap = m_caps * L_SUBL_CO2
    d_surf = 1.0           # m of regolith warmed
    q_surf = RHO_REGOLITH * d_surf * a_mars * 800.0 * dT
    q_total = q_atm + q_cap + q_surf
    e_earth = 5.95e20      # J, Earth primary energy ~2021
    p1tw = q_total / 1e12
    p100tw = q_total / 1e14
    f_req = SIGMA * (288.0 ** 4 - 210.0 ** 4)
    p_sustain = f_req * a_mars
    out = {"m_atm_kg": m_atm,
           "q_atm_J": q_atm,
           "q_cap_J": q_cap,
           "q_surf_J": q_surf,
           "q_total_J": q_total,
           "earth_annual_equivalents": q_total / e_earth,
           "yr_at_1TW": p1tw / SEC_YEAR,
           "yr_at_100TW": p100tw / SEC_YEAR,
           "f_req_W_m2": f_req,
           "p_sustain_W": p_sustain,
           "p_sustain_PW": p_sustain / 1e15,
           "verdict": ("ANALYTIC: one-time warming ~2.4e22 J (~41 Earth "
                       "annuals; ~7.7 yr at 100 TW), but sustaining 288 K "
                       "needs ~40.6 PW of continuous forcing at the blackbody "
                       "wall unless greenhouse gases supply the W/m^2 - the "
                       "binding constraint is sustaining, not heating.")}
    return out


# ---------------------------------------------------------------------- #
# 3. disasters                                                           #
# ---------------------------------------------------------------------- #
def disasters():
    def quake(mw):
        return 10.0 ** (1.5 * mw + 4.8)

    quakes = {"M5.0": quake(5.0), "M6.0": quake(6.0), "M7.0": quake(7.0),
              "M8.0": quake(8.0), "M9.0": quake(9.0), "M9.5": quake(9.5)}
    hurr_kin = 1.3e17
    hurr_latent_w = 6.0e14
    a_turbine = math.pi * 75.0 ** 2        # 150 m rotor
    p_turbine_raw = 0.5 * RHO_AIR * a_turbine * 50.0 ** 3
    p_turbine_betz = (16.0 / 27.0) * p_turbine_raw
    def tsunami(h):
        return 0.5 * RHO_WATER * 9.81 * h * h * 2.0e5 * 1.0e6
    tornado = 1.5e10
    m7_annualized = quakes["M7.0"] * 0.01 / 50.0
    out = {"quake_E_J_GR": quakes,
           "hurricane_Ekin_J": hurr_kin,
           "hurricane_latent_W": hurr_latent_w,
           "turbine_W_at_50ms": p_turbine_betz,
           "tsunami_E_J_H1m": tsunami(1.0),
           "tsunami_E_J_H3m": tsunami(3.0),
           "tornado_E_J": tornado,
           "m7_capture1pc_annualized_W": m7_annualized / SEC_YEAR,
           "verdict": ("ANALYTIC: an M9 quake releases ~2e18 J seismic, a "
                       "hurricane holds ~1.3e17 J of wind kinetic energy and "
                       "~6e14 W of latent release, a 1 m tsunami over a "
                       "1000 km front ~1e15 J. Capture is throttled by Betz "
                       "(16/27), Carnot, and duty cycle: an M7's 1% capture "
                       "annualizes to ~13 kW - the wall is frequency, not "
                       "magnitude.")}
    return out


# ---------------------------------------------------------------------- #
# 4. earthquake vibration feeding                                        #
# ---------------------------------------------------------------------- #
def vibration():
    def p_max(m, f, y, zeta):
        w = 2.0 * math.pi * f
        return m * w ** 3 * y * y / (4.0 * zeta)

    ambient = p_max(0.1, 1.0, 1.0e-4, 0.02)
    tmd = p_max(6.6e5, 0.2, 0.1, 0.05)
    strong = p_max(10.0, 1.0, 1.0e-3, 0.05)
    per_event = tmd * 100.0
    annualized = per_event / 50.0
    out = {"P_ambient_W": ambient,
           "P_TMD_660t_W": tmd,
           "P_strong_ground_W": strong,
           "E_TMD_per_event_J": per_event,
           "E_TMD_per_event_kWh": per_event / 3.6e6,
           "annualized_avg_W": annualized / SEC_YEAR,
           "verdict": ("ANALYTIC: P = m w^3 Y^2 / (4 zeta) gives ~3 uW from "
                       "ambient micro-vibration, ~65 kW from a 660 t tuned "
                       "mass damper during strong shaking (~1.8 kWh per "
                       "event), ~12 mW from a 10 kg harvester on 1 mm ground "
                       "motion. Annualized at one strong event per 50 yr: "
                       "milliwatts. Earthquakes power sensors, not grids.")}
    return out


# ---------------------------------------------------------------------- #
# 5. forest heat                                                         #
# ---------------------------------------------------------------------- #
def forest():
    s_avg = 150.0                       # W/m^2 annual-mean insolation
    p_sun_ha = s_avg * 1.0e4            # W per hectare
    npp = 1.5e4                         # kg dry/ha/yr (15 t/ha/yr)
    e_npp = npp * HHV_WOOD              # J/ha/yr
    eff = e_npp / (p_sun_ha * SEC_YEAR)
    p_harvest = e_npp / SEC_YEAR        # W/ha sustained
    standing = 2.0e5 * HHV_WOOD         # 200 t/ha
    fire = 10.0 * HHV_WOOD * 1.0e8      # 10 kg/m2 burned over 100 km^2
    out = {"solar_W_per_ha": p_sun_ha,
           "NPP_J_per_ha_yr": e_npp,
           "photosynthesis_efficiency": eff,
           "sustained_harvest_W_per_ha": p_harvest,
           "sustained_harvest_W_per_m2": p_harvest / 1.0e4,
           "standing_biomass_J_per_ha": standing,
           "fire_J_100km2": fire,
           "fire_Mt_TNT": fire / 4.184e15,
           "verdict": ("ANALYTIC: a hectare averages ~1.5 MW of solar input "
                       "but stores ~2.7e11 J/ha/yr of biomass at ~0.6% - the "
                       "photosynthetic 1% wall. A 100 km^2 crown fire releases "
                       "~1.8e16 J (~4.3 Mt TNT). Sustainable harvest is ~8.6 "
                       "kW/ha continuous; capture is bounded by the plant's "
                       "efficiency (~35% thermal) not the forest.")}
    return out


# ---------------------------------------------------------------------- #
# 6. clouds                                                              #
# ---------------------------------------------------------------------- #
def clouds():
    lwc_cb = 1.0e-3                     # kg/m^3 (1 g/m^3 cumulonimbus)
    m_cloud_10km3 = lwc_cb * 1.0e10     # kg
    m_cloud_100km3 = lwc_cb * 1.0e11
    eta = 0.3
    q_fog = eta * 1.0 * 3.0 * 0.2e-3    # kg/s per m^2 net
    liters_per_day = q_fog * 86400.0
    q40 = liters_per_day * 40.0
    seed_rain = 1.0e-3 * 1.0e6          # 1 mm over 1 km^2 -> m^3
    out = {"cloud_tonnes_10km3": m_cloud_10km3 / 1.0e3,
           "cloud_tonnes_100km3": m_cloud_100km3 / 1.0e3,
           "fog_L_per_m2_day": liters_per_day,
           "fog_L_per_day_40m2": q40,
           "seed_rain_m3_per_km2": seed_rain,
           "verdict": ("ANALYTIC: a 10 km^3 cumulonimbus carries ~1e4 t of "
                       "water, a 100 km^3 cell ~1e5 t - but that mass sits at "
                       "altitude and nets cannot reach it. Ground fog nets "
                       "catch ~15 L/m^2/day at LWC 0.2 g/m^3 and 3 m/s wind "
                       "(measured sites: 3-10); seeding a 1 km^2 cloud to 1 "
                       "mm yields 1e6 L. Netting works at the ground; the "
                       "cloud is a store, not a tap.")}
    return out


def main():
    results = {"slingshot": slingshot(),
               "terraform": terraform(),
               "disasters": disasters(),
               "vibration": vibration(),
               "forest": forest(),
               "clouds": clouds()}

    banner("HARVEST: force, energy, extraction - analytic verdicts")
    for section, r in results.items():
        print("\n[%s] %s" % (section, r["verdict"]))

    os.makedirs(DATA, exist_ok=True)
    with open(OUT_FILE, "w") as f:
        json.dump(results, f, indent=2)
    print("\nwrote data/harvest_energy_data.json")


if __name__ == "__main__":
    main()
