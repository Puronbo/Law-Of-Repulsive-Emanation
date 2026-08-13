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

from professions.rubric import Task, profession_verdict  # noqa: E402

# --- profession dataset (stated assumptions, auditable) ----------------------
PROFESSIONS = [
    # -- Class A candidates: output is a language artifact, no presence needed
    ("technical writer", [
        Task("research and gather context", 0.35, k=0.98, s=0.02),
        Task("draft documentation", 0.40, k=0.98, s=0.02),
        Task("revise against stated criteria", 0.25, k=0.95, s=0.05),
    ]),
    ("data analyst (reporting)", [
        Task("query, clean, transform", 0.40, k=0.97, s=0.03),
        Task("compute metrics, narrate findings", 0.60, k=0.97, s=0.03),
    ]),
    ("translator (document, non-certified)", [
        Task("translate", 0.70, k=0.98, s=0.02),
        Task("glossary and consistency QA", 0.30, k=0.98, s=0.02),
    ]),
    ("copyeditor", [
        Task("line edit", 0.60, k=0.99, s=0.01),
        Task("fact and style check", 0.40, k=0.99, s=0.01),
    ]),
    ("tier-1 text support (async)", [
        Task("resolve from knowledge base", 0.85, k=0.97, s=0.03),
        Task("escalate and hand off", 0.15, k=0.90, s=0.10),
    ]),
    # -- Class B candidates: Class A work plus a licensing/certification gate
    ("translator (court, sworn)", [
        Task("translate", 0.65, k=0.98, s=0.02),
        Task("glossary and consistency QA", 0.25, k=0.98, s=0.02),
        Task("sworn attestation of accuracy", 0.10, k=0.95, s=0.05, gate=True),
    ]),
    ("compliance officer (regulated filings)", [
        Task("prepare filing from rules", 0.85, k=0.97, s=0.03),
        Task("certify and submit", 0.15, k=0.95, s=0.05, gate=True),
    ]),
    # -- Class C candidates: knowledge-heavy but material skill or gate
    ("software engineer", [
        Task("design and write code", 0.50, k=0.80, s=0.20),
        Task("troubleshoot live systems", 0.30, k=0.70, s=0.30),
        Task("specification and review", 0.20, k=0.95, s=0.05),
    ]),
    ("teacher", [
        Task("lesson design", 0.30, k=0.95, s=0.05),
        Task("live classroom delivery", 0.50, k=0.40, s=0.60),
        Task("assessment", 0.20, k=0.90, s=0.10),
    ]),
    ("physician", [
        Task("consult and diagnostic reasoning", 0.50, k=0.85, s=0.15),
        Task("physical examination", 0.30, k=0.10, s=0.90),
        Task("documentation and plan", 0.20, k=0.95, s=0.05),
    ]),
    ("psychotherapist", [
        Task("assessment", 0.35, k=0.90, s=0.10),
        Task("therapeutic alliance sessions", 0.45, k=0.40, s=0.60),
        Task("documentation", 0.20, k=0.95, s=0.05),
    ]),
    ("tier-1 voice support (live)", [
        Task("resolve from knowledge base", 0.70, k=0.90, s=0.10),
        Task("live call handling and rapport", 0.30, k=0.40, s=0.60),
    ]),
    # -- Class D candidates: skill-dominated
    ("surgeon", [
        Task("operative planning", 0.20, k=0.90, s=0.10),
        Task("surgical execution", 0.60, k=0.20, s=0.80),
        Task("perioperative judgement", 0.20, k=0.40, s=0.60),
    ]),
    ("electrician (installation)", [
        Task("plan and apply code", 0.25, k=0.90, s=0.10),
        Task("physical install", 0.50, k=0.05, s=0.95),
        Task("live fault-finding", 0.25, k=0.40, s=0.60),
    ]),
]

GATE_NOTES = {
    "physician": "prescribing, diagnosing, signing - licensed human only",
    "psychotherapist": "licensed practice and duty of care",
    "surgeon": "surgical licensure and institutional credentialing",
    "compliance officer (regulated filings)": "legal certification of submissions",
    "translator (court, sworn)": "court-recognized sworn attestation",
}


def main():
    print("=" * 72)
    print("AI-performability without skill-based knowledge (14 professions)")
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
