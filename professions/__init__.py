"""professions - AI-performability rubric for professions.

A test instrument that classifies professions by whether they can be done
without any skill-based knowledge - i.e., whether the work decomposes into
articulated, language-representable knowledge tasks. Verdicts are
programmatic and pinned by tests; the profession estimates are stated
assumptions (`[hypothesis]`), not measurements.
"""

from professions.rubric import Task, profession_verdict

__all__ = ["Task", "profession_verdict"]
