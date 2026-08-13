"""
ai_performable_professions.py
=============================
Test which professions can be done by AI *without any skill-based knowledge*.
The instrument is the rubric in professions/rubric.py:

    skill-based knowledge (S): tacit, embodied, psychomotor, sensorimotor, or
        situational knowledge that cannot be fully stated in language
        (Polanyi: "we know more than we can tell").
    knowledge work (K): explicit, language-representable work (recall,
        reasoning, classification, composition, translation, evaluation).
    licensing gate (gate): output only actionable when signed/acted/held by a
        credentialed or situated human, even if the reasoning is AI-generated.

Every profession is decomposed into tasks (name, share, k, s, gate) with
k + s <= 1. Weighted K and S decide the class:

    A  AI-performable, no skill:     K >= 0.90 and S <= 0.10, no gate
    B  AI-performable, gated:        K >= 0.90 and S <= 0.10, gate exists
    C  augment only:                 K >= 0.50 (skill or gate is material)
    D  skill-dominated:              K <  0.50

The profession decompositions are design assumptions ([hypothesis]), not
measurements: they are stated so the rubric can be audited and re-argued.
Class A is the answer to the question; classes B/C/D are the honest
remainder, and A says nothing about whether a market or regulator will let an
AI occupy the role (capability vs social license - honest wall).

Verdict artifact: ../data/ai_performable_professions_data.json
"""

import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
sys_path = os.path.dirname(HERE)
if sys_path not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path)

from professions.professions_data import GATE_NOTES, PROFESSIONS  # noqa: E402
from professions.rubric import profession_verdict  # noqa: E402


def main():
    print("=" * 72)
    print("AI-performability without skill-based knowledge (%d professions)"
          % len(PROFESSIONS))
    print("=" * 72)
    rows = []
    for name, tasks in PROFESSIONS:
        v = profession_verdict(tasks)
        rows.append({"name": name, "tasks": tasks, **v})
    rows.sort(key=lambda r: (-r["knowledge_fraction"], r["skill_fraction"]))

    print("\n  class  K      S      gate  profession")
    for r in rows:
        gate = "gate" if r["gate"] else ""
        print("   %s    %.3f  %.3f   %-5s  %s"
              % (r["class"], r["knowledge_fraction"], r["skill_fraction"],
                 gate, r["name"]))

    counts = {}
    for r in rows:
        counts[r["class"]] = counts.get(r["class"], 0) + 1
    a_names = [r["name"] for r in rows if r["class"] == "A"]

    print("\n  class counts: %s" % ", ".join("%s=%d" % kv for kv in sorted(counts.items())))
    print("  Class A (AI-performable, no skill, no gate):")
    for n in a_names:
        print("    - %s" % n)

    method = (
        "Each profession is decomposed into tasks (share, k, s, gate), k+s<=1; "
        "K and S are effort-weighted. A: K>=0.90, S<=0.10, no gate. "
        "B: K>=0.90, S<=0.10, gate. C: K>=0.50. D: K<0.50."
    )
    verdict = (
        "The AI-performable set without any skill-based knowledge is exactly "
        "the professions whose output is a language artifact and whose whole "
        "effort decomposes into articulated knowledge work: %s. Add a "
        "certification/attestation duty and the same work drops to Class B "
        "(capable, gated). Everything that requires live physical presence, "
        "live rapport, or embodied judgement lands in C (augment) or D "
        "(skill-dominated): software engineering sits at K=%.2f because live "
        "troubleshooting resists articulation, teaching and therapy lose most "
        "of their value in the alliance that cannot be stated, and surgery/"
        "electrical work are dominated by psychomotor skill. Honest wall: "
        "Class A is capability, not adoption - markets, liability and "
        "licensure (the B gate) decide who may occupy the role, and Class A "
        "verdicts degrade sharply for regulated output."
    ) % (", ".join(a_names),
         [r["knowledge_fraction"] for r in rows if r["name"] == "software engineer"][0])

    out = {
        "claim": ("professions decomposable into pure knowledge work (K>=0.90, "
                  "S<=0.10, no gate) are the ones AI can do without any "
                  "skill-based knowledge: %d of %d tested (%s); every other "
                  "profession retains material skill or a licensing gate")
                  % (len(a_names), len(rows), ", ".join(a_names)),
        "method": method,
        "classes": {"A": "AI-performable, no skill",
                    "B": "AI-performable, gated",
                    "C": "augment only",
                    "D": "skill-dominated"},
        "assumptions_note": ("task decompositions are stated [hypothesis] "
                             "estimates, not measurements; k+s<=1 per task"),
        "class_counts": counts,
        "professions": [
            {
                "name": r["name"],
                "tasks": [
                    {"name": t.name, "share": t.share, "k": t.k, "s": t.s,
                     "gate": t.gate}
                    for t in r["tasks"]
                ],
                "knowledge_fraction": r["knowledge_fraction"],
                "skill_fraction": r["skill_fraction"],
                "gate": r["gate"],
                "gate_note": GATE_NOTES.get(r["name"]),
                "class": r["class"],
            }
            for r in rows
        ],
        "verdict": verdict,
    }
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "ai_performable_professions_data.json"), "w") as f:
        json.dump(out, f, indent=2)
    print()
    print("verdict:", verdict)
    print("wrote data/ai_performable_professions_data.json")


if __name__ == "__main__":
    main()
