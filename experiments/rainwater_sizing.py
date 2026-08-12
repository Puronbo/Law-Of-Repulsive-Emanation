"""
rainwater_sizing.py
===================
Size a rainwater collection & use system for the packaging-line facility and
be honest about what it is worth.

Demand model (line-related, non-potable uses only):
  * machine + floor washdown ..................... ~90 L/day
  * glue-system rinse + tool rinsing ............. ~30 L/day
  * corrugated dust suppression .................. ~20 L/day
  * solar-panel washing (periodic) ............... ~10 L/day averaged
  * TOTAL ........................................ ~150 L/day on production days
    260 production days -> ~39.6 m3/yr (10,500 gal)

Catchment (packaging.utilities.runoff_m3):
  * 300 m2 metal standing-seam roof (the facility roof above the line; the
    PV array from section 7.2 can double as catchment -- smooth, low loss)
  * 800 mm/yr rainfall, runoff_coeff 0.85, collection_eff 0.9 (first-flush
    diverter + leaf screens + filter)
  * harvest potential ~183.6 m3/yr -- ~4.6x the line's demand, so the
    catchment is not the constraint; the tank bridges dry spells instead.

Tank sizing: month-by-month balance (rainwater_balance_series), two rainfall
profiles -- uniform, and a dry-summer variant (Jun-Aug at 5 mm/month, tank
starts empty in January) -- and a sweep to the smallest tank with zero
deficit.

The honest verdict (matches the line's energy-feasibility pattern): on
municipal-water cost alone the payback is decades (~$160/yr saved vs ~$13k
installed). The value is architectural -- integration with the compressor
waste-heat washdown (section 8), solar-panel washing that protects the
section 7.2 PV investment, stormwater-credit potential, and non-potable
resilience during a mains outage.

Verdict artifact: ../data/rainwater_data.json
"""

import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
sys_path = os.path.dirname(HERE)
if sys_path not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path)

from packaging.utilities import (  # noqa: E402
    rainwater_balance_series,
    runoff_m3,
    tank_size_for_zero_deficit,
    water_cost_per_yr,
)

# --- assumptions (the honest wall) -----------------------------------------
AREA_M2 = 300.0
RAIN_MM_YEAR = 800.0
RUNOFF_COEFF = 0.85          # metal standing seam
COLLECTION_EFF = 0.9         # first-flush diverter + leaf guard + filter
DEMAND_L_PER_DAY = 150.0
PROD_DAYS_PER_MONTH = 22.0
PRICE_PER_M3 = 4.0           # US commercial water, ~$0.015/gal
DRY_SUMMER_MM = 5.0          # worst 3 months in the dry-summer profile
INSTALL_COST_USD = 13000.0   # itemized in the table below


def monthly_inflows_m3(monthly_rain_mm):
    return [runoff_m3(AREA_M2, mm, RUNOFF_COEFF, COLLECTION_EFF)
            for mm in monthly_rain_mm]


def monthly_demands_m3():
    per_month = DEMAND_L_PER_DAY * PROD_DAYS_PER_MONTH / 1000.0
    return [per_month] * 12


def main():
    print("=" * 72)
    print("rainwater collection & use sizing: packaging-line facility")
    print("=" * 72)

    annual_harvest = runoff_m3(AREA_M2, RAIN_MM_YEAR, RUNOFF_COEFF, COLLECTION_EFF)
    annual_demand = DEMAND_L_PER_DAY * PROD_DAYS_PER_MONTH * 12 / 1000.0
    print("  catchment           : %6.0f m2 roof" % AREA_M2)
    print("  rainfall            : %6.0f mm/yr -> harvest %.0f m3/yr (%.0f gal)"
          % (RAIN_MM_YEAR, annual_harvest, annual_harvest * 264.172))
    print("  line water demand   : %5.0f L/day prod. -> %.0f m3/yr (%.0f gal)"
          % (DEMAND_L_PER_DAY, annual_demand, annual_demand * 264.172))
    print("  harvest/demand      : %.1fx -> catchment is NOT the constraint"
          % (annual_harvest / annual_demand))

    uniform_rain = [RAIN_MM_YEAR / 12.0] * 12
    # summer-dry climate: Jun-Aug (indices 5-7) at DRY_SUMMER_MM, the tank
    # starts empty in January so it has five wet months to fill first
    wet_month = (RAIN_MM_YEAR - 3 * DRY_SUMMER_MM) / 9.0
    dry_rain = [wet_month] * 5 + [DRY_SUMMER_MM] * 3 + [wet_month] * 4
    demands = monthly_demands_m3()

    print()
    print("  tank sizing (monthly balance, smallest zero-deficit tank):")
    results = {}
    for name, rain in [("uniform rainfall", uniform_rain),
                       ("dry-summer (Jun-Aug %dmm)" % DRY_SUMMER_MM, dry_rain)]:
        inflows = monthly_inflows_m3(rain)
        cap = tank_size_for_zero_deficit(inflows, demands,
                                         cap_max_m3=20.0, step_m3=0.5)
        peak = rainwater_balance_series(cap, inflows, demands)["peak_level_m3"] \
            if cap else float("nan")
        results[name] = {"tank_m3": cap, "peak_hold_m3": peak}
        print("    %-26s : tank %5.1f m3  (peak hold %.1f m3, ~%.0f gal)"
              % (name, cap, peak, peak * 264.172))

    water_saved = water_cost_per_yr(annual_demand, PRICE_PER_M3)
    print()
    print("  cost & payback:")
    print("    installed system    : ~$%s (see table)" % f"{INSTALL_COST_USD:,.0f}")
    print("    municipal water saved: ~$%.0f/yr (%.0f m3 @ $%.2f/m3)"
          % (water_saved, annual_demand, PRICE_PER_M3))
    print("    simple payback      : ~%.0f yr on water alone -- see verdict"
          % (INSTALL_COST_USD / water_saved))

    out = {
        "claim": ("the line's non-potable water uses (washdown, glue rinse, "
                  "dust suppression, solar-panel washing) can be fully served "
                  "by a small rainwater system: ~300 m2 roof harvests ~184 "
                  "m3/yr vs ~40 m3/yr demand, needing only a ~%s m3 tank to "
                  "bridge dry spells; value is integration and resilience, "
                  "not the ~$160/yr water bill")
                  % (results["dry-summer (Jun-Aug %dmm)" % DRY_SUMMER_MM]["tank_m3"]),
        "assumptions": {
            "area_m2": AREA_M2, "rain_mm_yr": RAIN_MM_YEAR,
            "runoff_coeff": RUNOFF_COEFF, "collection_eff": COLLECTION_EFF,
            "demand_l_per_day": DEMAND_L_PER_DAY,
            "prod_days_per_month": PROD_DAYS_PER_MONTH,
            "price_per_m3": PRICE_PER_M3, "install_cost_usd": INSTALL_COST_USD,
        },
        "harvest_m3_yr": annual_harvest,
        "demand_m3_yr": annual_demand,
        "harvest_over_demand": annual_harvest / annual_demand,
        "tank_sizing_m3": {k: v["tank_m3"] for k, v in results.items()},
        "components": {
            "gutters_leaf_guards_first_flush": "$2k",
            "above_ground_poly_tank_4m3": "$2.5k",
            "pump_pressure_tank_level_control_makeup": "$2k",
            "filtration_50um_5um_and_uv": "$1.5k",
            "install_plumbing_backflow_prevention": "$5k",
            "total_installed": "$13k",
        },
        "verdict": (
            "Feasible and cheap to build (~$13k installed), but on the water "
            "bill alone the payback is ~80 yr -- this is not a money-saver, "
            "it is a systems play. Its real value: (1) the compressor waste-"
            "heat washdown in section 8 now has a free low-mineral water "
            "supply to preheat, cutting heating demand; (2) solar-panel "
            "washing with soft rainwater protects the $67-112k PV array from "
            "the 5-15% output loss dirty modules accumulate; (3) stormwater-"
            "fee / impervious-surface credits in cities with stormwater "
            "utilities (site-dependent, potentially $0.5-2k/yr); (4) "
            "non-potable resilience during a mains outage, the same "
            "resilience-only argument the H2 backup carries. Non-potable use "
            "ONLY: backflow prevention, cross-connection control, labeled "
            "piping, and local rainwater-harvesting rules apply."
        ),
    }
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "rainwater_data.json"), "w") as f:
        json.dump(out, f, indent=2)
    print()
    print("verdict:", out["verdict"])
    print("wrote data/rainwater_data.json")


if __name__ == "__main__":
    main()
