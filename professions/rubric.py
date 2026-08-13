"""Rubric: which professions need NO skill-based knowledge, so an LLM/AI can do them.

Definitions
-----------
skill-based knowledge (S)
    Tacit, embodied, psychomotor, sensorimotor, or situational knowledge that
    cannot be fully stated in language (Polanyi: "we know more than we can
    tell"). Includes physical manipulation, live-environment improvisation,
    trust/rapport that exists only in face-to-face presence, and stress/VR
    judgement under real physical risk.

knowledge work (K)
    Explicit, language-representable work: recall, retrieval, reasoning,
    classification, composition, translation, evaluation against stated
    criteria. Fully articulable, hence fully testable by a language model.

licensing gate (gate)
    The output is only actionable when signed/acted/held by a credentialed or
    situated human, even when the reasoning itself is fully AI-generated
    (diagnosis, legal filing, certified statement, prescription).

Method
------
A profession is decomposed into tasks (name, share of effort, k, s, gate)
with k + s <= 1. The profession's knowledge fraction K and skill fraction S
are the effort-weighted sums. Classification:

    A  "AI-performable, no skill":  K >= 0.90 and S <= 0.10 and no gate
    B  "AI-performable, gated":     K >= 0.90 and S <= 0.10 and a gate exists
    C  "augment only":             K >= 0.50 (skill or gate is material)
    D  "skill-dominated":          K <  0.50

Class A is the answer to "professions without any use of skill-based
knowledge that AI can do." Classes B/C/D are the honest remainder: Class A
says nothing about whether a market or regulator will let an AI *occupy* the
role - capability and social license are different axes (`[honest wall]`).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    name: str
    share: float     # share of the profession's effort (fractions sum to 1)
    k: float         # knowledge-work fraction of this task (0-1)
    s: float         # skill-based fraction of this task (0-1); k + s <= 1
    gate: bool = False


def _normalize(tasks):
    total = sum(t.share for t in tasks)
    if total <= 0:
        raise ValueError("task shares must sum to > 0")
    return [t.share / total for t in tasks]


def profession_verdict(tasks):
    """Classify a profession from its task decomposition.

    Returns dict with knowledge_fraction, skill_fraction, gate, and the
    A/B/C/D class.
    """
    shares = _normalize(tasks)
    for t in tasks:
        if t.k < 0.0 or t.s < 0.0 or t.k + t.s > 1.0 + 1e-9:
            raise ValueError(
                "task %r must satisfy 0 <= k, 0 <= s, k + s <= 1" % t.name)
    K = sum(sh * t.k for sh, t in zip(shares, tasks))
    S = sum(sh * t.s for sh, t in zip(shares, tasks))
    gate = any(t.gate and sh > 0 for sh, t in zip(shares, tasks))

    if K >= 0.90 and S <= 0.10:
        cls = "B" if gate else "A"
    elif K >= 0.50:
        cls = "C"
    else:
        cls = "D"

    return {
        "knowledge_fraction": K,
        "skill_fraction": S,
        "gate": gate,
        "class": cls,
    }
