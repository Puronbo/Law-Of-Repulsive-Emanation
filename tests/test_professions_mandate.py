"""Tests for text-mandate analysis (professions.mandate) and the report."""

import pytest

from professions.mandate import (
    mandate_status,
    residue_tasks,
    text_mandate_fraction,
    write_mandate,
)
from professions.professions_data import GATE_NOTES, PROFESSIONS
from professions.report import build_report
from professions.rubric import Task, profession_verdict


def _verdict(tasks):
    return profession_verdict(tasks)


def test_mandate_fraction_is_one_minus_skill():
    tasks = [
        Task("pure text", 0.8, k=1.0, s=0.0),
        Task("tiny physical", 0.2, k=0.1, s=0.9),
    ]
    v = _verdict(tasks)
    assert text_mandate_fraction(v) == pytest.approx(1 - v["skill_fraction"])
    assert text_mandate_fraction(v) == pytest.approx(0.82)


def test_fully_mandatable_status():
    tasks = [
        Task("translate", 0.7, k=0.98, s=0.02),
        Task("glossary QA", 0.3, k=0.98, s=0.02),
    ]
    assert mandate_status(_verdict(tasks)) == "fully"


def test_gated_fully_mandatable_status():
    tasks = [
        Task("prepare filing", 0.85, k=0.97, s=0.03),
        Task("certify and submit", 0.15, k=0.95, s=0.05, gate=True),
    ]
    assert mandate_status(_verdict(tasks)) == "fully-gated"


def test_partial_status():
    tasks = [
        Task("design and write code", 0.5, k=0.80, s=0.20),
        Task("troubleshoot live systems", 0.3, k=0.70, s=0.30),
        Task("spec and review", 0.2, k=0.95, s=0.05),
    ]
    assert mandate_status(_verdict(tasks)) == "partial"


def test_not_status_when_skill_dominated():
    tasks = [
        Task("operative planning", 0.2, k=0.90, s=0.10),
        Task("surgical execution", 0.6, k=0.20, s=0.80),
        Task("perioperative judgement", 0.2, k=0.40, s=0.60),
    ]
    assert mandate_status(_verdict(tasks)) == "not"


def test_write_mandate_none_for_skill_dominated():
    tasks = [
        Task("surgical execution", 1.0, k=0.3, s=0.7),
    ]
    assert write_mandate("surgeon", tasks) is None


def test_write_mandate_lists_tasks_and_bounds():
    tasks = [
        Task("translate", 0.7, k=0.98, s=0.02),
        Task("glossary QA", 0.3, k=0.98, s=0.02),
    ]
    text = write_mandate("translator", tasks)
    assert text is not None
    assert "MANDATE: translator" in text
    assert "translate (70% of effort)" in text
    assert "no tacit context to infer" in text
    assert "GATE: none" in text


def test_write_mandate_notes_the_gate():
    tasks = [
        Task("translate", 0.65, k=0.98, s=0.02),
        Task("sworn attestation", 0.35, k=0.95, s=0.05, gate=True),
    ]
    text = write_mandate("court translator", tasks)
    assert text is not None
    assert "GATE:" in text and "credentialed" in text


def test_residue_tasks_returns_only_skill_tasks():
    tasks = [
        Task("knowledge", 0.7, k=1.0, s=0.0),
        Task("live delivery", 0.3, k=0.4, s=0.6),
    ]
    residue = residue_tasks(tasks)
    assert [t.name for t in residue] == ["live delivery"]
    assert residue[0].s == 0.6


def test_report_status_counts_match_dataset():
    report = build_report()
    expected = {"fully": 5, "fully-gated": 2, "partial": 5, "not": 2}
    assert report["status_counts"] == expected
    assert report["class_counts"] == {"A": 5, "B": 2, "C": 5, "D": 2}
    assert len(report["professions"]) == len(PROFESSIONS)


def test_report_rows_consistent_with_rubric_and_mandate():
    report = build_report()
    for r in report["professions"]:
        v = profession_verdict([
            Task(t["name"], t["share"], t["k"], t["s"], t["gate"])
            for t in r["tasks"]
        ])
        assert r["knowledge_fraction"] == pytest.approx(v["knowledge_fraction"])
        assert r["skill_fraction"] == pytest.approx(v["skill_fraction"])
        assert r["mandate_fraction"] == pytest.approx(1 - v["skill_fraction"])
        assert r["mandate_status"] == mandate_status(v)
        if r["mandate_status"] in ("fully", "fully-gated"):
            assert r["mandate_text"] is not None
        else:
            assert r["mandate_text"] is None
            assert any(t["s"] > 0 for t in r["residue"])


def test_report_gate_notes_cover_all_gated_rows():
    report = build_report()
    gated = [r for r in report["professions"] if r["gate"]]
    assert gated, "dataset should contain at least one gated profession"
    for r in gated:
        assert r["name"] in GATE_NOTES
        assert r["gate_note"]
        assert r["mandate_status"] in ("fully-gated", "partial", "not")
