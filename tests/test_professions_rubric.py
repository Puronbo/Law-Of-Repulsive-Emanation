"""Tests for the AI-performability rubric in professions.rubric."""

import pytest

from professions.rubric import Task, profession_verdict


def test_pure_knowledge_profession_is_class_a():
    tasks = [
        Task("research", 0.4, k=0.98, s=0.02),
        Task("compose", 0.4, k=0.98, s=0.02),
        Task("edit against stated criteria", 0.2, k=0.95, s=0.05),
    ]
    v = profession_verdict(tasks)
    assert v["class"] == "A"
    assert v["gate"] is False
    assert v["knowledge_fraction"] >= 0.9
    assert v["skill_fraction"] <= 0.10


def test_same_work_with_gate_is_class_b():
    tasks = [
        Task("analyze", 0.5, k=0.97, s=0.03),
        Task("draft", 0.4, k=0.97, s=0.03),
        Task("sign and issue", 0.1, k=0.9, s=0.1, gate=True),
    ]
    v = profession_verdict(tasks)
    assert v["class"] == "B"
    assert v["gate"] is True


def test_partly_skillful_profession_is_class_c():
    tasks = [
        Task("lesson design", 0.3, k=0.95, s=0.05),
        Task("live classroom management", 0.5, k=0.4, s=0.6),
        Task("assessment", 0.2, k=0.9, s=0.1),
    ]
    v = profession_verdict(tasks)
    assert v["class"] == "C"
    assert v["knowledge_fraction"] == pytest.approx(0.665)


def test_skill_dominated_profession_is_class_d():
    tasks = [
        Task("surgical execution", 0.6, k=0.3, s=0.7),
        Task("operative judgement", 0.3, k=0.45, s=0.55),
        Task("documentation", 0.1, k=0.95, s=0.05),
    ]
    v = profession_verdict(tasks)
    assert v["class"] == "D"
    assert v["knowledge_fraction"] < 0.5


def test_weighting_uses_shares_not_task_count():
    # one big knowledge task dominates a small skill task
    tasks = [
        Task("bulk analysis", 0.9, k=0.99, s=0.01),
        Task("tiny physical demo", 0.1, k=0.1, s=0.9),
    ]
    v = profession_verdict(tasks)
    assert v["knowledge_fraction"] == pytest.approx(0.901)
    assert v["class"] == "A"


def test_material_skill_pushes_off_class_a():
    # under k + s <= 1, material skill (S > 0.10) forces K < 0.90 -> class C
    tasks = [
        Task("explain", 0.5, k=1.0, s=0.0),
        Task("perform live", 0.5, k=0.78, s=0.22),
    ]
    v = profession_verdict(tasks)
    assert v["knowledge_fraction"] == pytest.approx(0.89)
    assert v["skill_fraction"] == pytest.approx(0.11)
    assert v["class"] == "C"


def test_invalid_task_raises():
    with pytest.raises(ValueError):
        profession_verdict([Task("bad", 1.0, k=0.8, s=0.3)])


def test_zero_shares_raise():
    with pytest.raises(ValueError):
        profession_verdict([Task("bad", 0.0, k=0.9, s=0.0)])


def test_shares_are_normalized():
    tasks = [
        Task("a", 2.0, k=1.0, s=0.0),
        Task("b", 2.0, k=0.0, s=1.0),
    ]
    v = profession_verdict(tasks)
    assert v["knowledge_fraction"] == pytest.approx(0.5)
    assert v["class"] == "C"
