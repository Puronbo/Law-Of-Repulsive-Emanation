"""Bounded AGI-like cognitive substrate built on the soliton event model.

This is an auditable research prototype: perception is explicit, memory is
persistent in-process, planning is bounded breadth-first search, salience uses
the event-driven SNN, and every decision is serialized as a cognitive event.
It makes no claim of general intelligence.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import heapq
import hashlib
import json
from math import isfinite
from typing import Iterable, Sequence

from .soliton_snn import AERSpike, LIFNeuron, SolitonSNN


@dataclass(frozen=True, slots=True)
class Fact:
    predicate: str
    value: str

    def __post_init__(self) -> None:
        if not self.predicate or not self.value:
            raise ValueError("fact predicate and value must be non-empty")


@dataclass(frozen=True, slots=True)
class Observation:
    timestamp: int
    facts: frozenset[Fact]
    salience: float = 1.0

    def __post_init__(self) -> None:
        if self.timestamp < 0 or not isfinite(self.salience) or self.salience < 0:
            raise ValueError("timestamp non-negative and salience non-negative")


@dataclass(frozen=True, slots=True)
class Action:
    name: str
    requires: frozenset[Fact] = frozenset()
    adds: frozenset[Fact] = frozenset()
    removes: frozenset[Fact] = frozenset()
    cost: float = 1.0

    def __post_init__(self) -> None:
        if not self.name or not isfinite(self.cost) or self.cost <= 0:
            raise ValueError("action name must be non-empty and cost positive")

    def applicable(self, facts: frozenset[Fact]) -> bool:
        return self.requires <= facts

    def apply(self, facts: frozenset[Fact]) -> frozenset[Fact]:
        if not self.applicable(facts):
            raise ValueError(f"action {self.name!r} is not applicable")
        return (facts - self.removes) | self.adds


@dataclass(frozen=True, slots=True)
class Goal:
    name: str
    desired: frozenset[Fact]

    def satisfied(self, facts: frozenset[Fact]) -> bool:
        return self.desired <= facts


@dataclass(frozen=True, slots=True)
class CognitiveEvent:
    timestamp: int
    kind: str
    payload: dict[str, object]

    def encode(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True, slots=True)
class Episode:
    observation: Observation
    selected_action: str | None
    goal: str | None
    plan_length: int
    salience_spikes: int


class CognitiveAgent:
    """Deterministic perception-memory-planning-action loop."""
    def __init__(self, actions: Sequence[Action], *, plan_horizon: int = 8,
                 salience_threshold: float = 0.5):
        if (plan_horizon < 0 or not isfinite(salience_threshold)
                or salience_threshold < 0):
            raise ValueError("plan horizon and salience threshold must be non-negative")
        if len({action.name for action in actions}) != len(actions):
            raise ValueError("action names must be unique")
        self.actions = tuple(actions)
        self.plan_horizon = plan_horizon
        self.goal: Goal | None = None
        self.facts = frozenset()
        self.episodes: list[Episode] = []
        self.events: list[CognitiveEvent] = []
        self.snn = SolitonSNN([LIFNeuron(0, threshold=salience_threshold or 1e-12)], ())

    def set_goal(self, goal: Goal) -> None:
        self.goal = goal
        self.events.append(CognitiveEvent(0, "goal_set", {"name": goal.name}))

    def remember(self, facts: Iterable[Fact]) -> None:
        self.facts = self.facts | frozenset(facts)

    def plan(self, facts: frozenset[Fact] | None = None) -> tuple[Action, ...] | None:
        """Find the least-cost plan within a bounded search horizon."""
        if self.goal is None:
            return None
        start = facts if facts is not None else self.facts
        if self.goal.satisfied(start):
            return ()
        frontier: list[tuple[float, int, int, frozenset[Fact], tuple[Action, ...]]] = []
        sequence = 0
        heapq.heappush(frontier, (0.0, 0, sequence, start, ()))
        best_cost = {start: 0.0}
        while frontier:
            cost, _, _, state, path = heapq.heappop(frontier)
            if cost > best_cost.get(state, float("inf")):
                continue
            if self.goal.satisfied(state):
                return path
            if len(path) >= self.plan_horizon:
                continue
            for action in self.actions:
                if not action.applicable(state):
                    continue
                next_state = action.apply(state)
                next_cost = cost + action.cost
                if next_cost >= best_cost.get(next_state, float("inf")):
                    continue
                next_path = path + (action,)
                best_cost[next_state] = next_cost
                sequence += 1
                heapq.heappush(frontier, (next_cost, len(next_path), sequence,
                                          next_state, next_path))
        return None

    def observe(self, observation: Observation) -> tuple[Action | None, tuple[Action, ...] | None]:
        """Perceive, update memory, route salience, plan, and execute one action."""
        self.remember(observation.facts)
        self.snn.reset()
        self.snn.ingest((AERSpike(observation.timestamp, -1, 0,
                                  payload=observation.salience),))
        salience_spikes = len(self.snn.run())
        current_plan = self.plan()
        selected = current_plan[0] if current_plan else None
        if selected is not None:
            self.facts = selected.apply(self.facts)
        self.episodes.append(Episode(observation, selected.name if selected else None,
                                     self.goal.name if self.goal else None,
                                     len(current_plan) if current_plan is not None else -1,
                                     salience_spikes))
        self.events.append(CognitiveEvent(observation.timestamp, "observation", {
            "facts": sorted((fact.predicate, fact.value) for fact in observation.facts),
            "salience": observation.salience,
            "selected_action": selected.name if selected else None,
            "plan_length": len(current_plan) if current_plan is not None else None,
            "salience_spikes": salience_spikes,
        }))
        return selected, current_plan

    def trace(self) -> str:
        """Return canonical JSON-lines cognitive trace."""
        return "\n".join(event.encode() for event in self.events)

    def trace_digest(self) -> str:
        return hashlib.sha256(self.trace().encode("utf-8")).hexdigest()
