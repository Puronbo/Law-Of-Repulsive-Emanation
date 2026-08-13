"""Build the unified text-mandate report.

One builder shared by the verdict experiment (experiments/mandate_report.py),
the CLI report, and the web dashboard (puno_app/mandates_server.py) so all
three always agree. The profession decompositions are stated [hypothesis]
estimates from professions_data.py; the scoring logic is pinned by tests.
"""

from professions.mandate import (
    mandate_status,
    residue_tasks,
    text_mandate_fraction,
    write_mandate,
)
from professions.professions_data import GATE_NOTES, PROFESSIONS
from professions.rubric import profession_verdict

METHOD = (
    "A profession is text-mandatable when a complete written instruction set "
    "fully determines the work. Each profession is decomposed into tasks "
    "(share, k, s, gate) with k + s <= 1; the skill fraction S is the "
    "effort-weighted sum of s, and text_mandate_fraction = 1 - S. "
    "Status: fully (>=0.90, no gate), fully-gated (>=0.90, gate), "
    "partial (>=0.50), not (<0.50)."
)


def _task_dict(t):
    return {"name": t.name, "share": t.share, "k": t.k, "s": t.s, "gate": t.gate}


def build_report():
    rows = []
    for name, tasks in PROFESSIONS:
        v = profession_verdict(tasks)
        mandate = text_mandate_fraction(v)
        rows.append({
            "name": name,
            "tasks": [_task_dict(t) for t in tasks],
            "class": v["class"],
            "knowledge_fraction": v["knowledge_fraction"],
            "skill_fraction": v["skill_fraction"],
            "gate": v["gate"],
            "gate_note": GATE_NOTES.get(name),
            "mandate_fraction": mandate,
            "mandate_status": mandate_status(v),
            "mandate_text": write_mandate(name, tasks),
            "residue": [_task_dict(t) for t in residue_tasks(tasks)],
        })
    rows.sort(key=lambda r: (-r["mandate_fraction"], r["skill_fraction"], r["name"]))

    status_counts = {}
    class_counts = {}
    for r in rows:
        status_counts[r["mandate_status"]] = status_counts.get(r["mandate_status"], 0) + 1
        class_counts[r["class"]] = class_counts.get(r["class"], 0) + 1

    fully = [r["name"] for r in rows if r["mandate_status"] == "fully"]
    verdict = (
        "The professions that can be easily mandated through text are the "
        "language-artifact professions with S <= 0.10 and no gate: %s. "
        "The same work with an attestation/certification duty is still fully "
        "mandatable in text but must route through a credentialed actor "
        "(fully-gated). Everything else keeps a material skill residue that a "
        "written mandate cannot drive: partial professions are 50-90%% "
        "text-driveable (knowledge half is mandatable, the live/embodied half "
        "is not), and the 'not' professions are skill-dominated - their "
        "spec is demonstrated, not dictated. Honest wall: mandate is "
        "capability-in-text, not adoption - the gate is exactly where "
        "licensure decides who may act on the output."
    ) % (", ".join(fully),)

    return {
        "method": METHOD,
        "professions": rows,
        "status_counts": status_counts,
        "class_counts": class_counts,
        "verdict": verdict,
    }
