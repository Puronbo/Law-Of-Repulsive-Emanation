"""professions_audit: the fifth real-subsystem audit -- the AI-performability
rubric / text-mandate stack (professions/rubric.py, mandate.py,
professions_data.py, report.py).

Audited invariants (pure arithmetic + data, deterministic, reproducible):
    L35_rubric_score_bounded:
        Every task decomposition in the shared dataset keeps k and s in
        [0,1] with k + s <= 1, and the effort-weighted knowledge fraction
        K and skill fraction S therefore also stay in [0,1] with
        K + S <= 1 (a rubric score can never leave the unit square).
        Checked exhaustively over all 14 professions / every task.
    L36_profession_names_unique_nonempty:
        Profession names are non-empty and unique, and each profession has
        at least one task with a strictly positive effort share (so the
        effort-normalizer can never divide by zero).
        Checked exhaustively over every profession entry.
    L37_mandate_fraction_is_skill_complement:
        text_mandate_fraction(v) == 1 - v["skill_fraction"] exactly for
        every profession: the write-driveable fraction and the skill
        residue are exact complements (mandate + S == 1).
        Checked exhaustively over all 14 professions.
HONEST NEGATIVE (rejected, not introduced):
    L38_classA_literal_zero_skill:
        The candidate "Class A = AI-performable, NO skill" read literally as
        S == 0.0 is FALSE: the rubric's Class A bar is the threshold
        S <= 0.10, not S == 0, and every Class A profession in the dataset
        carries a small but nonzero skill residue (e.g. technical writer
        S = 0.0275).  The word "no skill" is a labeling convenience for the
        practical band, not a claim of literal zero -- an honest audit must
        not confuse the threshold with exactness.  first_failure: the first
        Class A profession examined.
"""
from professions.professions_data import PROFESSIONS
from professions.rubric import profession_verdict


def _all_names():
    return [n for n, _ in PROFESSIONS]


def _L35_score_bounded(datum):
    name, tasks = datum
    for t in tasks:
        if not (0.0 <= t.k <= 1.0 + 1e-9):
            return False
        if not (0.0 <= t.s <= 1.0 + 1e-9):
            return False
        if t.k + t.s > 1.0 + 1e-9:
            return False
    v = profession_verdict(tasks)
    K, S = v["knowledge_fraction"], v["skill_fraction"]
    if not (0.0 - 1e-9 <= K <= 1.0 + 1e-9):
        return False
    if not (0.0 - 1e-9 <= S <= 1.0 + 1e-9):
        return False
    return K + S <= 1.0 + 1e-9


def _L36_names_unique_nonempty(datum):
    name, tasks = datum
    if not isinstance(name, str) or name.strip() == "":
        return False
    if _all_names().count(name) != 1:
        return False
    if not tasks:
        return False
    return all(t.share > 0 for t in tasks)


def _L37_mandate_complement(datum):
    from professions.mandate import text_mandate_fraction
    name, tasks = datum
    v = profession_verdict(tasks)
    return abs(text_mandate_fraction(v) - (1.0 - v["skill_fraction"])) < 1e-12


def _L38_classA_literal_zero(datum):
    """The FALSE candidate law: Class A means literally no skill (S == 0).
    Returns True iff S == 0, which fails on the very first Class A
    profession because the actual Class A bar is the threshold S <= 0.10."""
    name = datum
    tasks = dict(PROFESSIONS)[name]
    v = profession_verdict(tasks)
    return v["skill_fraction"] == 0.0


def _certify(label, meta, pred, domain):
    from experiments.emanation import law_checker as lc
    return lc.certify_statement(label, meta, pred, list(domain))


def professions_certificates():
    certs = []
    # L35: per-task and weighted score bounds, every profession.
    certs.append(_certify(
        "L35_rubric_score_bounded",
        {"domain": "all 14 professions in professions_data.PROFESSIONS, "
                   "every task and the effort-weighted K, S",
         "law": "0 <= k, s <= 1 and k + s <= 1 per task, so 0 <= K, S <= 1 "
                "and K + S <= 1 for the weighted score (rubric stays in "
                "the unit square)",
         "measured_on": "professions.rubric.profession_verdict over the "
                        "shared dataset"},
        _L35_score_bounded, list(PROFESSIONS)))
    # L36: unique, non-empty names; >=1 task with positive share.
    certs.append(_certify(
        "L36_profession_names_unique_nonempty",
        {"domain": "every profession entry in the dataset (name, tasks)",
         "law": "name is a non-empty unique string; at least one task and "
                "every task has strictly positive effort share, so the "
                "_normalize divider is never zero"},
        _L36_names_unique_nonempty, list(PROFESSIONS)))
    # L37: mandate fraction is the exact complement of skill fraction.
    certs.append(_certify(
        "L37_mandate_fraction_is_skill_complement",
        {"domain": "all 14 professions (name, tasks)",
         "law": "text_mandate_fraction(verdict) == 1 - verdict[skill_fraction] "
                "exactly: write-driveable fraction and skill residue are "
                "complements (mandate + S == 1)",
         "measured_on": "professions.mandate.text_mandate_fraction"},
        _L37_mandate_complement, list(PROFESSIONS)))
    # L38 HONEST_NEGATIVE: literal "no skill" for Class A is FALSE.
    class_a = [n for n, _ in PROFESSIONS
               if profession_verdict(dict(PROFESSIONS)[n])["class"] == "A"]
    certs.append(_certify(
        "L38_classA_literal_zero_skill",
        {"domain": "the %d Class A professions in the dataset" % len(class_a),
         "law": "FALSE CANDIDATE: Class A means literally no skill-based "
                "knowledge (S == 0.0); the real Class A bar is the threshold "
                "S <= 0.10, and every Class A profession here carries a "
                "small but nonzero skill residue (e.g. technical writer "
                "S = 0.0275)",
         "honest_check": "the first Class A datum must fail the literal "
                         "S == 0 test (its skill_fraction is > 0)"},
        _L38_classA_literal_zero, class_a))
    return certs
