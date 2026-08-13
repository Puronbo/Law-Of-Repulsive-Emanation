"""
mandate_report.py
=================
Which professions can be *easily mandated through text*? A profession is
text-mandatable when a complete written instruction set (the mandate) fully
determines the work - an agent handed only the text produces the output with
no tacit, embodied, or situational knowledge to supply (Polanyi: "we know
more than we can tell"). Within each task the skill fraction s is the part a
written mandate cannot drive, so (professions/mandate.py):

    text_mandate_fraction = 1 - S            (S = effort-weighted skill)

    fully        mandate >= 0.90, no gate  - the written spec is complete
    fully-gated  mandate >= 0.90, gate     - text complete, licensed actor
                                             must act on the output
    partial      mandate >= 0.50           - skill residue blocks pure text
    not          mandate <  0.50           - skill-dominated

The dataset and scoring are shared with the CLI and web dashboard through
professions.report.build_report(), so the experiment, the `puno mandates`
report, and the browser all agree. Task decompositions are stated
[hypothesis] estimates (professions/professions_data.py); the logic is pinned
by tests/test_professions_mandate.py.

Verdict artifact: ../data/mandate_report_data.json
"""

import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
sys_path = os.path.dirname(HERE)
if sys_path not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path)

from professions.report import build_report  # noqa: E402

OUT_FILE = os.path.join(DATA, "mandate_report_data.json")


def main():
    report = build_report()

    print("=" * 72)
    print("text-mandatable professions (mandate = 1 - skill_fraction)")
    print("=" * 72)
    print("\n  status        mandate  class  profession")
    for r in report["professions"]:
        print("  %-13s  %6.1f%%   %s    %s"
              % (r["mandate_status"], r["mandate_fraction"] * 100, r["class"],
                 r["name"]))
    print("\n  status counts: %s" % ", ".join(
        "%s=%d" % kv for kv in sorted(report["status_counts"].items())))
    print("  class counts:  %s" % ", ".join(
        "%s=%d" % kv for kv in sorted(report["class_counts"].items())))

    os.makedirs(DATA, exist_ok=True)
    with open(OUT_FILE, "w") as f:
        json.dump(report, f, indent=2)
    print()
    print("verdict:", report["verdict"])
    print("wrote data/mandate_report_data.json")


if __name__ == "__main__":
    main()
