"""The profession dataset shared by every verdict runner and the dashboard.

Each profession is decomposed into tasks `(name, share, k, s, gate)` with
`k + s <= 1`; the decompositions are stated [hypothesis] estimates, not
measurements - edit here and every artifact (experiment JSON, CLI report,
web dashboard) changes at once. The rubric logic that consumes them is
pinned by tests in tests/.
"""

from professions.rubric import Task

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
