"""CSV export for the professions report (schema-stable, deterministic).

One row per profession (profession-level) or one row per task (task-level).
Columns are fixed by ``_PROFESSION_FIELDS`` / ``_TASK_FIELDS`` and pinned by
``test_professions_mandate.py.test_export_csv_matches_report``.  The CSV is
produced from ``professions.report.build_report`` so it always agrees with the
CLI, web dashboard and the persisted JSON artifact.
"""

import argparse
import csv
import io
import sys
from collections import OrderedDict

from professions.report import build_report

_PROFESSION_FIELDS = [
    "name",
    "class",
    "knowledge_fraction",
    "skill_fraction",
    "gate",
    "gate_note",
    "mandate_fraction",
    "mandate_status",
]

_TASK_FIELDS = [
    "profession",
    "task",
    "share",
    "k",
    "s",
    "gate",
]


def _fmt(value):
    if value is None:
        return ""
    if isinstance(value, bool):
        return "yes" if value else "no"
    return value


def profession_rows_csv(report):
    """Profession-level CSV text (one row per profession)."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=_PROFESSION_FIELDS,
                            lineterminator="\n")
    writer.writeheader()
    for r in report["professions"]:
        writer.writerow(OrderedDict((f, _fmt(r[f])) for f in _PROFESSION_FIELDS))
    return buf.getvalue()


def task_rows_csv(report):
    """Task-level CSV text (one row per task, profession repeated)."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=_TASK_FIELDS,
                            lineterminator="\n")
    writer.writeheader()
    for r in report["professions"]:
        for t in r["tasks"]:
            writer.writerow(OrderedDict([
                ("profession", r["name"]),
                ("task", t["name"]),
                ("share", t["share"]),
                ("k", t["k"]),
                ("s", t["s"]),
                ("gate", _fmt(t["gate"])),
            ]))
    return buf.getvalue()


def write_csv(path, report, tasks=False):
    """Write the profession- and/or task-level CSV to ``path``.

    With ``tasks=True`` writes a second ``*_tasks.csv`` next to ``path``.
    """
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(profession_rows_csv(report))
    if tasks:
        with open(path.rsplit(".", 1)[0] + "_tasks.csv", "w",
                  encoding="utf-8", newline="") as f:
            f.write(task_rows_csv(report))


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="puno-professions-export",
        description="export the professions report as CSV (schema-stable)")
    ap.add_argument("out", nargs="?", default="puno-mandates-report.csv",
                    help="output CSV path (default: puno-mandates-report.csv)")
    ap.add_argument("--tasks", action="store_true",
                    help="also write a per-task CSV next to the output")
    args = ap.parse_args(argv)

    write_csv(args.out, build_report(), tasks=args.tasks)
    print("wrote %s" % args.out)
    if args.tasks:
        print("wrote %s" % args.out.rsplit(".", 1)[0] + "_tasks.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())