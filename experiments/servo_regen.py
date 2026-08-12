"""
servo_regen.py
=============
Quantity the regenerative-braking energy of the packaging line's fold axes
(Station 2 erector) using the actual servo model in packaging/servo.py.

Per fold cycle the axis: drives up to 90+3 deg (motoring), dwells while the
tape/glue locks, then SETTLES back to square 90 deg. During the settle the
restoring moment (spring-back) does work on the motor shaft: the motor is
overdriven by the load, so mechanical power P = tau_motor * omega goes
negative and the drive feeds energy back onto the DC bus.

What we measure per cycle (one axis, one fold):
  * motoring energy  = integral of max(P,0)   [drawn from bus]
  * regen energy     = -integral of min(P,0)  [returned to bus]
  * recovered fraction and net bus energy
  * scaled to the line: 4 axes, 300 cases/h, one 8 h shift and 24/7.

Honest wall: the sim is a schematic-level 2nd-order axis with unit inertias;
real servo drives also lose some regen in the drive's DC/DC stage and a
little in the motor (we assume ideal return to the shared bus). The point is
the ORDER OF MAGNITUDE and the architectural choice (shared DC bus / battery
recapture vs brake-resistor heat), not a metered figure.

Verdict artifact: ../data/servo_regen_data.json
"""

import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
sys_path = os.path.dirname(HERE)
if sys_path not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path)

from packaging.servo import FoldAxis  # noqa: E402


def one_fold_cycle(k_restore=0.02, dwell_s=1.0):
    axis = FoldAxis(k_restore)
    axis.set_goal(90.0, overshoot_deg=3.0, dwell_s=dwell_s)
    motoring = 0.0
    regen = 0.0
    steps = 0
    peak_brake_w = 0.0
    while not axis.in_position and steps < 500_000:
        axis.step()
        p = axis.motor_power
        if p >= 0.0:
            motoring += p * axis.dt
        else:
            regen += -p * axis.dt
            peak_brake_w = max(peak_brake_w, -p)
        steps += 1
    return {
        "motoring_j": motoring,
        "regen_j": regen,
        "net_j": motoring - regen,
        "recovered_fraction": regen / motoring if motoring else 0.0,
        "cycle_s": steps * axis.dt,
        "peak_brake_w": peak_brake_w,
    }


def main():
    print("=" * 72)
    print("servo regenerative braking energy per fold cycle (packaging line)")
    print("=" * 72)

    r = one_fold_cycle()
    print("  one axis, one fold (drive->93, dwell 1 s, settle->90):")
    print("    motoring energy : %8.3f J" % r["motoring_j"])
    print("    regen energy    : %8.3f J   (%.1f%% of motoring)"
          % (r["regen_j"], 100 * r["recovered_fraction"]))
    print("    net from bus    : %8.3f J/cycle" % r["net_j"])
    print("    cycle time      : %8.3f s   peak brake power %.2f W"
          % (r["cycle_s"], r["peak_brake_w"]))

    # line scaling: 4 fold axes (side L, side R, major, minor), 300 cases/h
    cases_per_h = 300
    for name, hours in [("one 8 h shift", 8), ("24/7", 24)]:
        per_case = 4 * r["regen_j"]          # 4 axes fold per case
        per_day = per_case * cases_per_h * hours
        net_saved = 4 * r["net_j"] * cases_per_h * hours
        print("  %-14s : 4 axes x %4d J/case = %.3f kWh/case; %s ~ %.1f kWh"
              % (name, r["regen_j"], per_case / 3.6e6, "regen/day", per_day / 3.6e6))
        print("    net bus draw ~ %.1f kWh/day" % (net_saved / 3.6e6))

    out = {
        "claim": "the erector's settle phase regenerates energy via spring-back "
                 "work; a shared DC bus (or the PV battery) recaptures it "
                 "instead of dumping it in a brake resistor",
        "per_cycle_axis": r,
        "line_scaling": {
            "axes_per_case": 4, "cases_per_h": cases_per_h,
            "regen_kwh_per_8h_shift": 4 * r["regen_j"] * cases_per_h * 8 / 3.6e6,
            "regen_kwh_per_day_24_7": 4 * r["regen_j"] * cases_per_h * 24 / 3.6e6,
        },
        "architecture": "shared EtherCAT DC bus + battery recapture (ties to "
                         "AUTO_PACKAGING_SYSTEM.md 3.36 PV+battery); brake "
                         "resistors only as a fault-tolerance backstop",
        "verdict": (
            "Regen from spring-back is real but small on this line: %.1f%% of "
            "the fold's motoring energy per cycle. Its value is architectural "
            "(DC-bus crosstalk + battery recapture instead of a ~%.0f W peak "
            "brake-resistor heat load in the cabinet) more than numerical. "
            "The dominant recoverable stream on the line is compressed-air "
            "waste heat, not servo regen."
        ) % (100 * r["recovered_fraction"], r["peak_brake_w"]),
    }
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "servo_regen_data.json"), "w") as f:
        json.dump(out, f, indent=2)
    print()
    print("verdict:", out["verdict"])
    print("wrote data/servo_regen_data.json")


if __name__ == "__main__":
    main()
