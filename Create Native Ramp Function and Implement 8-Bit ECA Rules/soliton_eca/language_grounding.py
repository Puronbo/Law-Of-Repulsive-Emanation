"""Strict, bounded text grounding for the cognitive prototype."""
from __future__ import annotations

import re
from typing import Sequence

from .cognitive_agent import Fact, Goal, Observation

_TOKEN = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*=[^\s=]+$")
_VALUE = re.compile(r"^[A-Za-z0-9_.:/-]+$")


def _facts(tokens: Sequence[str]) -> frozenset[Fact]:
    facts: set[Fact] = set()
    for token in tokens:
        if not _TOKEN.match(token):
            raise ValueError("expected predicate=value tokens")
        predicate, value = token.split("=", 1)
        if not _VALUE.match(value):
            raise ValueError("fact value contains unsupported characters")
        facts.add(Fact(predicate, value))
    if not facts:
        raise ValueError("at least one fact is required")
    return frozenset(facts)


def parse_command(text: str, *, timestamp: int = 0) -> Observation | Goal:
    """Parse only ``observe`` and ``goal`` commands; reject everything else."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("command must be non-empty text")
    tokens = text.strip().split()
    verb, args = tokens[0].lower(), tokens[1:]
    if verb == "observe":
        salience = 1.0
        facts_tokens = []
        for token in args:
            if token.startswith("salience="):
                try:
                    salience = float(token.split("=", 1)[1])
                except ValueError as exc:
                    raise ValueError("salience must be numeric") from exc
            else:
                facts_tokens.append(token)
        return Observation(timestamp, _facts(facts_tokens), salience)
    if verb == "goal":
        return Goal("command-goal", _facts(args))
    raise ValueError("unsupported command; use observe or goal")


def apply_command(agent, text: str, *, timestamp: int = 0):
    """Apply a grounded command to an agent and return any decision."""
    command = parse_command(text, timestamp=timestamp)
    if isinstance(command, Goal):
        agent.set_goal(command)
        return None
    return agent.observe(command)
