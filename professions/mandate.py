"""Text-mandate analysis: which professions can be *mandated through text*?

A profession is text-mandatable when a complete written instruction set - the
mandate - fully determines the work: an agent handed only the text can
produce the output, with no tacit, embodied, or situational knowledge to fill
in (Polanyi: "we know more than we can tell"). Within each task the
skill-based fraction s is exactly the part a written mandate cannot drive, so

    text_mandate_fraction = 1 - S

where S is the effort-weighted skill fraction from professions.rubric.
Status:

    fully        mandate >= 0.90, no gate  - the written spec is complete
    fully-gated  mandate >= 0.90, gate     - the text is complete, but a
                                             licensed human must act on it
    partial      mandate >= 0.50           - skill residue blocks a pure
                                             text hand-off
    not          mandate <  0.50           - skill-dominated; text alone is
                                             not a usable spec

For fully/fully-gated professions `write_mandate` produces the shape of the
mandate text; for partial/not it is None and `residue_tasks` names the tasks
whose s > 0 resists text. [hypothesis] The thresholds mirror the rubric
(S <= 0.10 admits the practical Class A/B band; a strict "no skill at all"
reading would be S = 0 exactly).
"""

from professions.rubric import profession_verdict

FULLY = 0.90   # mandate fraction needed for a complete text hand-off
PARTIAL = 0.50  # below this the profession is skill-dominated


def text_mandate_fraction(verdict):
    """Fraction of the profession's effort a written mandate can drive."""
    return 1.0 - verdict["skill_fraction"]


def mandate_status(verdict):
    """fully | fully-gated | partial | not, from a rubric verdict."""
    mandate = text_mandate_fraction(verdict)
    if mandate >= FULLY:
        return "fully-gated" if verdict["gate"] else "fully"
    if mandate >= PARTIAL:
        return "partial"
    return "not"


def residue_tasks(tasks):
    """Tasks whose skill fraction is material (s > 0), largest s first."""
    return sorted((t for t in tasks if t.s > 0), key=lambda t: t.s, reverse=True)


def write_mandate(name, tasks):
    """A template mandate text, or None if a written spec cannot be complete.

    Only fully/fully-gated professions (mandate >= 0.90) get a mandate: a
    skill-dominated profession cannot be specified by text alone. The text is
    a template showing the shape of the mandate - a real mandate would carry
    the actual criteria - not a full spec document. [hypothesis]
    """
    mandate = text_mandate_fraction(profession_verdict(tasks))
    if mandate < FULLY:
        return None
    gate = any(t.gate and t.share > 0 for t in tasks)
    lines = []
    lines.append("MANDATE: %s" % name)
    lines.append("DELIVERY: a language artifact produced from this text alone.")
    lines.append("TASKS (each fully specified by written criteria here):")
    for t in tasks:
        lines.append("  - %s (%.0f%% of effort)" % (t.name, t.share * 100))
    lines.append("BOUNDS: no physical presence; no tacit context to infer;")
    lines.append("        every rule, style, and acceptance test stated in text.")
    if gate:
        lines.append("GATE: output is not actionable until a credentialed %s"
                     " attests it." % name)
    else:
        lines.append("GATE: none - the output is actionable on the strength of"
                     " this text alone.")
    return "\n".join(lines)
