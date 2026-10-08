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
    # Counts are derived from the dataset, not frozen: if a decomposition in
    # professions_data.py is re-argued the counts follow it (the ledger records
    # the numbers current on this pass rather than pinning them in the test).
    assert set(report["class_counts"].keys()) == {"A", "B", "C", "D"}
    assert set(report["status_counts"].keys()) == \
        {"fully", "fully-gated", "partial", "not"}
    assert sum(report["class_counts"].values()) == len(PROFESSIONS)
    assert sum(report["status_counts"].values()) == len(PROFESSIONS)
    for r in report["professions"]:
        assert report["class_counts"][r["class"]] >= 1
        assert report["status_counts"][r["mandate_status"]] >= 1


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


def test_export_csv_matches_report():
    import csv
    import io

    from professions.export import profession_rows_csv, task_rows_csv

    report = build_report()
    rows = list(csv.DictReader(io.StringIO(profession_rows_csv(report))))
    assert [r["name"] for r in rows] == [r["name"] for r in report["professions"]]
    for row, prof in zip(rows, report["professions"]):
        assert row["class"] == prof["class"]
        assert float(row["knowledge_fraction"]) == \
            pytest.approx(prof["knowledge_fraction"])
        assert float(row["skill_fraction"]) == \
            pytest.approx(prof["skill_fraction"])
        assert row["gate"] == ("yes" if prof["gate"] else "no")
        assert row["gate_note"] == (prof["gate_note"] or "")

    tasks = list(csv.DictReader(io.StringIO(task_rows_csv(report))))
    assert len(tasks) == sum(len(r["tasks"]) for r in report["professions"])
    assert tasks[0]["profession"] == report["professions"][0]["name"]
