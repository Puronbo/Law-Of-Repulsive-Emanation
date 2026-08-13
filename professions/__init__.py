"""professions - AI-performability and text-mandate rubric for professions.

A test instrument that classifies professions by whether they can be done
without any skill-based knowledge - i.e., whether the work decomposes into
articulated, language-representable knowledge tasks - and how completely a
written instruction set (a text mandate) can drive the work. Verdicts are
programmatic and pinned by tests; the profession decompositions are stated
assumptions (`[hypothesis]`), not measurements.
"""

from professions.mandate import (
    mandate_status,
    residue_tasks,
    text_mandate_fraction,
    write_mandate,
)
from professions.professions_data import GATE_NOTES, PROFESSIONS
from professions.rubric import Task, profession_verdict

__all__ = [
    "GATE_NOTES",
    "PROFESSIONS",
    "Task",
    "mandate_status",
    "profession_verdict",
    "residue_tasks",
    "text_mandate_fraction",
    "write_mandate",
]
