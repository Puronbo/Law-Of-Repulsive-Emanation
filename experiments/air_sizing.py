"""
air_sizing.py
=============
Size the compressed-air system for the packaging line and answer the
"excess air" question with numbers instead of folklore.

Demand model (schematic-level, component assumptions stated explicitly):
  * Station 1 vacuum destack: 4 Bernoulli/venturi pads, ~0.5 scfm each,
    running continuously ............ ~2.0 scfm avg / peak
  * Blow-offs (fold settle + reject assist): 2 nozzles ~9 scfm each at
    30 psi, 20% duty ............... ~3.6 scfm avg / ~18 scfm peak
  * Small cylinders / valves (reject gate, guides): ~0.3 scfm avg / 1 scfm peak
  * Peak simultaneous ............... ~21 scfm  (only reached during a
    blow-off burst overlapping a pad surge; the receiver absorbs it)

Sizing rules used (packaging.utilities):
  * FAD = peak x (1 + 30% margin)                     -> covers peak + control
  * average draw = avg x (1 + 25% leak allowance)     -> plant leaks are real
  * VFD compressor follows AVERAGE flow: kW = 0.22 kW/scfm x avg_real
  * receiver: ~1 gal/scfm FAD (VFD/trim rule); ~6 gal/scfm if fixed-speed

The honest answer to "do we need excess air?":
  Yes, headroom is needed -- but it belongs in the receiver tank plus a VFD
  drive, NOT in an oversized fixed-speed compressor that idles at ~25% load
  forever. And the biggest air-side saving is avoiding venturi vacuum in the
  first place: a low-pressure blower at ~0.2 bar uses ~1/10 to ~1/20 the
  energy of venturi pads for the same gripping force.

Verdict artifact: ../data/air_sizing_data.json
"""

import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
sys_path = os.path.dirname(HERE)
if sys_path not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path)

from packaging.utilities import (  # noqa: E402
    annual_energy_kwh,
    avg_power_kw,
    avg_real_scfm,
    fad_scfm,
    receiver_volume_gal,
    vacuum_venturi_demand,
)

# --- assumptions (the honest wall) -----------------------------------------
N_PADS = 4
SCFM_PER_PAD = 0.5            # typical Bernoulli gripper free-air draw
BLOWOFF_NOZZLES = 2
BLOWOFF_SCFM_EACH = 9.0       # 1/8" nozzle restricted to ~30 psi
BLOWOFF_DUTY = 0.20
CYL_SCFM_AVG = 0.3
CYL_SCFM_PEAK = 1.0
MARGIN = 0.30
LEAK = 0.25
SPECIFIC_POWER = 0.22         # kW per scfm, industrial screw compressor
PRICE_PER_KWH = 0.12
HOURS_8H_SHIFT_YEAR = 2080.0  # 260 days x 8 h
HOURS_24_7_YEAR = 8760.0


def main():
    print("=" * 72)
    print("compressed-air sizing: packaging line demand -> compressor -> cost")
    print("=" * 72)

    pad_avg = vacuum_venturi_demand(N_PADS, SCFM_PER_PAD)
    blowoff_avg = BLOWOFF_NOZZLES * BLOWOFF_SCFM_EACH * BLOWOFF_DUTY
    blowoff_peak = BLOWOFF_NOZZLES * BLOWOFF_SCFM_EACH
    avg = pad_avg + blowoff_avg + CYL_SCFM_AVG
    peak = pad_avg + blowoff_peak + CYL_SCFM_PEAK
    print("  continuous vacuum pads : %6.1f scfm" % pad_avg)
    print("  blow-off nozzles       : %6.1f scfm avg, %6.1f scfm peak"
          % (blowoff_avg, blowoff_peak))
    print("  cylinders / valves     : %6.1f scfm avg, %6.1f scfm peak"
          % (CYL_SCFM_AVG, CYL_SCFM_PEAK))
    print("  TOTAL                  : %6.1f scfm avg, %6.1f scfm peak"
          % (avg, peak))

    fad = fad_scfm(peak, MARGIN)
    avg_real = avg_real_scfm(avg, LEAK)
    power = avg_power_kw(avg_real, SPECIFIC_POWER)
    tank_vfd = receiver_volume_gal(fad, 1.0)
    tank_fixed = receiver_volume_gal(fad, 6.0)
    print("  compressor FAD         : %6.1f scfm (%.2f m3/min)  [peak + %.0f%%]"
          % (fad, fad * 0.0283168, 100 * MARGIN))
    print("  average draw w/ leaks  : %6.1f scfm -> duty ~%.0f%% of FAD"
          % (avg_real, 100 * avg_real / fad))
    print("  average power (VFD)    : %6.2f kW  (~0.22 kW/scfm)" % power)
    print("  receiver tank          : %5.1f gal VFD-rule / %5.1f gal fixed-speed"
          % (tank_vfd, tank_fixed))

    print()
    print("  energy and cost:")
    for name, hours in [("8 h shift/yr", HOURS_8H_SHIFT_YEAR),
                        ("24/7 per yr", HOURS_24_7_YEAR)]:
        kwh = annual_energy_kwh(power, hours)
        print("    %-14s : %7.0f kWh  ~ $%6.0f/yr"
              % (name, kwh, kwh * PRICE_PER_KWH))

    print()
    print("  venturi-vs-blower comparison (destack gripping, same force):")
    # Venturi path: pads draw 2.0 scfm of compressed air, charged at the
    # compressor's 0.22 kW/scfm. A low-pressure vacuum blower (~0.2 bar)
    # does the same gripping duty at ~1/4 to ~1/3 the energy -- venturi
    # expansion from ~6 bar is ~1-3% efficient vs blower ~30-50%, but the
    # pads are already small so the practical factor is ~3-4x, not 10-20x.
    venturi_w = SPECIFIC_POWER * pad_avg
    blower_w = 0.13          # ~0.1-0.2 kW for a small 0.2 bar unit
    print("    venturi pads : ~%.2f kW (continuous)" % venturi_w)
    print("    low-P blower : ~%.2f kW (continuous)  -> ~%.0fx less energy"
          % (blower_w, venturi_w / blower_w))

    out = {
        "claim": ("the line needs compressed-air HEADROOM, not excess capacity: "
                  "a receiver tank plus a VFD compressor sized for peak+30% "
                  "that tracks the ~1.5 kW average; the dominant air-side "
                  "saving is replacing venturi vacuum with a low-pressure "
                  "blower (~3-4x less energy for the same grip)"),
        "assumptions": {
            "vacuum_pads": N_PADS, "scfm_per_pad": SCFM_PER_PAD,
            "blowoff_nozzles": BLOWOFF_NOZZLES,
            "blowoff_scfm_each": BLOWOFF_SCFM_EACH, "blowoff_duty": BLOWOFF_DUTY,
            "cyl_scfm_avg": CYL_SCFM_AVG, "cyl_scfm_peak": CYL_SCFM_PEAK,
            "margin_frac": MARGIN, "leak_frac": LEAK,
            "specific_power_kw_per_scfm": SPECIFIC_POWER,
            "price_per_kwh": PRICE_PER_KWH,
        },
        "demand_scfm": {"avg": avg, "peak": peak,
                        "pads_cont": pad_avg, "blowoff_peak": blowoff_peak},
        "sizing": {
            "fad_scfm": fad,
            "avg_real_scfm": avg_real,
            "duty_frac_of_fad": avg_real / fad,
            "avg_power_kw": power,
            "receiver_gal_vfd": tank_vfd,
            "receiver_gal_fixed": tank_fixed,
        },
        "annual_energy_kwh": {
            "8h_shift": annual_energy_kwh(power, HOURS_8H_SHIFT_YEAR),
            "24_7": annual_energy_kwh(power, HOURS_24_7_YEAR),
        },
        "verdict": (
            "Yes, the design needs excess air in the sense of headroom: the "
            "peak blow-off burst (~21 scfm) is ~3.5x the average draw (~6 "
            "scfm). But the correct response is a receiver tank "
            "(~27-30 gal) + VFD compressor (FAD ~27 scfm, ~1.5 kW average) + "
            "a leak/repair program, NOT a bigger fixed-speed compressor "
            "idling at ~25% load. Average air energy is ~1.5 kW, matching "
            "the 1-2 kW line in AUTO_PACKAGING_SYSTEM.md section 5; the "
            "single biggest air-side improvement is a low-pressure vacuum "
            "blower instead of venturi pads (~3-4x less energy for the same "
            "gripping duty)."
        ),
    }
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "air_sizing_data.json"), "w") as f:
        json.dump(out, f, indent=2)
    print()
    print("verdict:", out["verdict"])
    print("wrote data/air_sizing_data.json")


if __name__ == "__main__":
    main()
