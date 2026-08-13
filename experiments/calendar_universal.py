"""experiments/calendar_universal.py - render the universal calendar.

Writes data/calendar_universal_data.json (gitignored) holding the exact p/q
strings for the anchor instants of the calendar - the datum, this instant,
the civil window, the retrace rung, and the giant pre-civilization eon -
plus C0/C_current calibration and every civilization layer. Runs standalone:

    python experiments/calendar_universal.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys_path = os.path.dirname(HERE)
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)

from calendars import c0, deeptime, layers, report  # noqa: E402
from calendars.axis import EPOCH_SECONDS, now_day  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "data", "calendar_universal_data.json")


def main():
    data = {
        "epoch_0d": report.epoch_summary(),
        "anchors": {
            "datum": build_anchor(0),
            "now": build_anchor(now_day()),
            "window_lo": build_anchor(deeptime.WINDOW_LO),
            "window_hi": build_anchor(deeptime.WINDOW_HI),
            "rung_730421": build_anchor(deeptime.RUNG_730421),
            "giant_epoch": build_anchor(-deeptime.giant_as_days()),
        },
        "calibration": c0.adjust(0),
        "giant_era": deeptime.giant_era_epoch_year(),
        "window": deeptime.window_730421(),
        "layers": report.layer_names(),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("wrote %s" % OUT)
    print("anchors:", ", ".join(data["anchors"]))
    print("giant years before epoch:",
          data["giant_era"]["years_before_epoch"])
    return data


def build_anchor(day):
    return {
        "day_of_epoch": layers.frac_str(day),
        "layers": layers.render(day),
        "calibration": c0.adjust(day),
        "deep_time": deeptime.era(day),
    }


if __name__ == "__main__":
    main()
