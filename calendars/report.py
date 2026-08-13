"""calendars.report - one shared, exact report for every surface.

CLI, experiment, tests and (optionally) a web layer all call build_report();
the p/q exact strings travel unchanged, so no surface can introduce a float
truncation.
"""

from calendars import c0, deeptime, layers
from calendars.axis import now_day


def build_report(day=None):
    """Exact full calendar report for a day offset (default: this instant)."""
    day = now_day() if day is None else day
    return {
        "day_of_epoch": layers.frac_str(day),
        "layers": layers.render(day),
        "calibration": c0.adjust(day),
        "deep_time": deeptime.era(day),
        "giant_era": deeptime.giant_era_epoch_year(),
        "window_730421": deeptime.window_730421(),
    }


def layer_names():
    return [(k, v["name"], v["civilization"], v["cycle_days"])
            for k, v in layers.LAYERS.items()]


def epoch_summary():
    """The repo-measured datum identity, for the top of any report."""
    return {
        "epoch_0d": "2000-10-26 10:26:20.00",
        "unix_seconds": "972527180",
        "day_of_year": "300 (5 x 60, sexagenary-complete)",
        "weekday": "Thursday",
        "tau_mmddyyyy": "80",          # 10262000 and 26102000 both tau=80
        "digit_sum": "11",
        "giant_nested": "943901200001",
    }
