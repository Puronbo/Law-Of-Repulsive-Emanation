"""
standby_efficiency.py
=====================
Quantify the demand-side efficiency systems missing from the line's energy
budget: standby/idle management, air-leak monitoring, and engineered
blow-off nozzles. Dust extraction and scrap handling are covered
qualitatively in the spec (reliability/recycling value, not kWh).

Context: the energy budget (AUTO_PACKAGING_SYSTEM.md section 7.1) states ~5 kW
average -> ~120 kWh/day, which assumes the line runs flat out 24/7. Realistic
operation is rarely flat-out-24/7. If the line produces 16 h/day and idles
8 h, the fixed loads (controls, cabinet fans, vacuum blower, unloaded
compressor) keep drawing power unless a sleep state drops them.

The three efficiency systems quantified here:
  1. Standby/idle management (AUTO -> IDLE -> SLEEP): drives to STO standby,
     vacuum blower to idle, VFD compressor trimmed to leakage-only, controls
     retained. Idle drops from ~2.3 kW (near-running, no sleep) to ~0.9 kW.
  2. Air-leak monitoring: a flow meter per air branch + IIoT baseline; catch
     and repair ~1 scfm of the 20-30% leak allowance that leaks quietly.
  3. Amplifier blow-off nozzles: engineered nozzles cut blow-off demand
     ~30-50% vs open pipes; conservative ~1 scfm of the ~3.6 scfm blow-off
     average saved.

Honest wall: the savings only exist if the line actually idles; a true
24/7-continuous line (as the solar sizing assumed) earns the air savings but
not the standby savings. Per-system payback is itemized so the cheap,
software-only sleep state stands alone.

Verdict artifact: ../data/standby_efficiency_data.json
"""

import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
sys_path = os.path.dirname(HERE)
if sys_path not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path)

from packaging.utilities import (  # noqa: E402
    annual_cost_usd,
    annual_energy_kwh,
    scfm_saved_power_kw,
    standby_savings_kwh_yr,
)

# --- assumptions (the honest wall) -----------------------------------------
RUNNING_KW = 5.0            # section 7.1 total
IDLE_KW_NO_SLEEP = 2.3      # controls 0.5 + fans 0.1 + blower 0.13 + compressor unloaded ~1.6
IDLE_KW_SLEEP = 0.9         # controls 0.5 + fans 0.1 + blower idle 0.05 + compressor trim 0.25
PROD_H_PER_DAY = 16.0
IDLE_H_PER_DAY = 24.0 - PROD_H_PER_DAY
WEEKEND_DAYS = 105.0        # 52 weekends + holidays, fully idle 24 h
DAYS_PER_YEAR = 260.0
PRICE_PER_KWH = 0.12
SCFM_SAVED_LEAKS = 1.0      # recovered half the ~2 scfm leak allowance
SCFM_SAVED_NOZZLES = 1.0    # amplifier nozzles, conservative
AIR_SAVING_RUN_HOURS = PROD_H_PER_DAY * DAYS_PER_YEAR
CAPEX_SLEEP_USD = 3000.0    # PLC state logic + drive standby enable (mostly software)
CAPEX_AIR_USD = 2000.0      # air flow meter + amplifier nozzle kit
CAPEX_DUST_USD = 5000.0     # small cartridge dust collector (reliability, not kWh)
CAPEX_BALER_USD = 8000.0    # optional scrap baler/compactor (shared plant units cheaper)


def main():
    print("=" * 72)
    print("demand-side efficiency systems: standby, leak monitor, blow-off nozzles")
    print("=" * 72)

    sleep_kwh = standby_savings_kwh_yr(IDLE_H_PER_DAY, IDLE_KW_NO_SLEEP,
                                       IDLE_KW_SLEEP, DAYS_PER_YEAR)
    weekend_kwh = standby_savings_kwh_yr(24.0, IDLE_KW_NO_SLEEP,
                                         IDLE_KW_SLEEP, WEEKEND_DAYS)
    standby_kwh = sleep_kwh + weekend_kwh
    air_kw = scfm_saved_power_kw(SCFM_SAVED_LEAKS + SCFM_SAVED_NOZZLES)
    air_kwh = annual_energy_kwh(air_kw, AIR_SAVING_RUN_HOURS)

    print("  idle-state comparison (16 h prod / 8 h idle day):")
    print("    no-sleep idle  : %4.1f kW   -> 98.4 kWh/day" % IDLE_KW_NO_SLEEP)
    print("    sleep idle     : %4.1f kW   -> 87.2 kWh/day  (-11.2 kWh/day)"
          % IDLE_KW_SLEEP)
    print("    (section 7.1's 120 kWh/day assumes flat 24/7 with no idle at all)")
    print()
    print("  1. standby/sleep management:")
    print("    weekday idle  : %8.0f kWh/yr" % sleep_kwh)
    print("    weekend/holiday: %8.0f kWh/yr" % weekend_kwh)
    print("    total         : %8.0f kWh/yr  ~ $%.0f/yr"
          % (standby_kwh, annual_cost_usd(standby_kwh, PRICE_PER_KWH)))
    print("    capex ~$%.0f (software-first) -> ~%.1f yr payback"
          % (CAPEX_SLEEP_USD, CAPEX_SLEEP_USD / annual_cost_usd(standby_kwh, PRICE_PER_KWH)))
    print()
    print("  2+3. leak monitor + amplifier nozzles (2 scfm at 0.22 kW/scfm):")
    print("    %8.0f kWh/yr  ~ $%.0f/yr   capex ~$%.0f -> ~%.1f yr payback"
          % (air_kwh, annual_cost_usd(air_kwh, PRICE_PER_KWH), CAPEX_AIR_USD,
             CAPEX_AIR_USD / annual_cost_usd(air_kwh, PRICE_PER_KWH)))
    print()
    total_kwh = standby_kwh + air_kwh
    total_cost = annual_cost_usd(total_kwh, PRICE_PER_KWH)
    print("  efficiency package total:")
    print("    %8.0f kWh/yr  ~ $%.0f/yr  capex ~$%.0f (excl. dust/baler)"
          % (total_kwh, total_cost, CAPEX_SLEEP_USD + CAPEX_AIR_USD))

    out = {
        "claim": ("the cheapest efficiency system on this line is demand-side: "
                  "standby/idle management (~%.0f kWh/yr from the 8 h of daily "
                  "idle + weekends), air-leak monitoring and amplifier blow-off "
                  "nozzles (~%.0f kWh/yr); together ~%.0f kWh/yr (~$%.0f/yr) "
                  "for ~$%.0f of sleep+air capex, while dust extraction and "
                  "scrap handling pay in reliability and recycling, not kWh")
                  % (standby_kwh, air_kwh, total_kwh, total_cost,
                     CAPEX_SLEEP_USD + CAPEX_AIR_USD),
        "assumptions": {
            "running_kw": RUNNING_KW,
            "idle_kw_no_sleep": IDLE_KW_NO_SLEEP,
            "idle_kw_sleep": IDLE_KW_SLEEP,
            "prod_h_per_day": PROD_H_PER_DAY,
            "weekend_days": WEEKEND_DAYS,
            "days_per_yr": DAYS_PER_YEAR,
            "price_per_kwh": PRICE_PER_KWH,
            "scfm_saved_leaks": SCFM_SAVED_LEAKS,
            "scfm_saved_nozzles": SCFM_SAVED_NOZZLES,
            "capex_usd": {"sleep": CAPEX_SLEEP_USD, "air": CAPEX_AIR_USD,
                          "dust": CAPEX_DUST_USD, "baler": CAPEX_BALER_USD},
        },
        "kwh_per_yr": {
            "standby_weekday": sleep_kwh, "standby_weekend": weekend_kwh,
            "standby_total": standby_kwh, "air_total": air_kwh,
            "package_total": total_kwh,
        },
        "cost_per_yr_usd": {
            "standby": annual_cost_usd(standby_kwh, PRICE_PER_KWH),
            "air": annual_cost_usd(air_kwh, PRICE_PER_KWH),
            "package": total_cost,
        },
        "payback_yr": {
            "sleep_alone": CAPEX_SLEEP_USD / annual_cost_usd(standby_kwh, PRICE_PER_KWH),
            "air_alone": CAPEX_AIR_USD / annual_cost_usd(air_kwh, PRICE_PER_KWH),
        },
        "kwh_per_day_with_sleep": PROD_H_PER_DAY * RUNNING_KW
                                  + IDLE_H_PER_DAY * IDLE_KW_SLEEP,
        "kwh_per_day_without_sleep": PROD_H_PER_DAY * RUNNING_KW
                                     + IDLE_H_PER_DAY * IDLE_KW_NO_SLEEP,
        "verdict": (
            "The demand-side efficiency package is the best kWh-per-dollar on "
            "the line: sleep-mode control is software-first (~$%.0f) and pays "
            "back in ~%.0f yr whenever the line actually idles (16 h prod + "
            "8 h idle cuts the daily energy from ~120 to ~87 kWh/day); air-"
            "leak monitoring and amplifier nozzles recover ~%.0f kWh/yr of "
            "quiet losses. Dust extraction ($~%.0f) and scrap baling are "
            "reliability/recycling systems, not kWh savers -- their payback is "
            "downtime and waste-avoidance, which the energy figures do not "
            "count. Honest wall: on a true 24/7-continuous line the standby "
            "savings vanish (air savings remain), so the sleep state must be "
            "built but only 'earns' where production actually stops."
        ) % (CAPEX_SLEEP_USD, CAPEX_SLEEP_USD / annual_cost_usd(standby_kwh, PRICE_PER_KWH),
             air_kwh, CAPEX_DUST_USD),
    }
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "standby_efficiency_data.json"), "w") as f:
        json.dump(out, f, indent=2)
    print()
    print("verdict:", out["verdict"])
    print("wrote data/standby_efficiency_data.json")


if __name__ == "__main__":
    main()
