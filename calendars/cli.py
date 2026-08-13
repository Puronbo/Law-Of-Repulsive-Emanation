"""calendars.cli - the puno-calendar command line surface."""

import argparse
import json
import re
import sys

from calendars import deeptime, layers, report
from calendars.axis import EPOCH_SECONDS_OF_DAY, civil_to_days
from calendars.report import build_report


def _date_to_day(text):
    """'YYYY-MM-DD[ HH:MM:SS]' -> exact day offset.

    Civil time is the corpus clock frame: the datum's own label is
    2000-10-26 10:26:20.00 (= day 0), so a civil midnight sits
    EPOCH_SECONDS_OF_DAY before the datum.
    """
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})(?: (\d{2}):(\d{2}):(\d{2}))?$",
                 text)
    if not m:
        raise ValueError("expected YYYY-MM-DD [HH:MM:SS]")
    y, mo, d = (int(m.group(i)) for i in (1, 2, 3))
    days = civil_to_days(y, mo, d)
    if m.group(4) is not None:
        h, mi, s = (int(m.group(i)) for i in (4, 5, 6))
        from fractions import Fraction
        sod = h * 3600 + mi * 60 + s
        days += Fraction(sod - EPOCH_SECONDS_OF_DAY, 86400)
    return days


def main(argv=None):
    p = argparse.ArgumentParser(prog="puno-calendar",
                                description="the universal calendar")
    sub = p.add_subparsers(dest="command")

    sub.add_parser("today", help="full report for this instant")
    d = sub.add_parser("date", help="report for a civil date")
    d.add_argument("date", help="YYYY-MM-DD [HH:MM:SS]")
    sub.add_parser("deep", help="deep-time and pre-civilization era report")
    sub.add_parser("layers", help="list every calendar layer")

    args = p.parse_args(argv)
    if args.command == "today":
        out = build_report()
    elif args.command == "date":
        day = _date_to_day(args.date)
        out = build_report(day)
    elif args.command == "deep":
        out = {
            "giant_era": deeptime.giant_era_epoch_year(),
            "window_730421": deeptime.window_730421(),
            "layers_at_giant": layers.render(-deeptime.giant_as_days()),
        }
    elif args.command == "layers":
        out = {"layers": [dict(zip(("key", "name", "civilization",
                                    "cycle_days"), r))
                          for r in report.layer_names()]}
    else:
        p.print_help()
        return 2
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
