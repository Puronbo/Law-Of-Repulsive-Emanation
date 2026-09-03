"""Unified soliton cognitive runtime."""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Iterable, Sequence

from .cognitive_agent import Action, CognitiveAgent, CognitiveEvent
from .episodic_store import EpisodicStore
from .language_grounding import apply_command
from .soliton_admission import AdmissionPolicy
from .soliton_metrics import metrics
from .soliton_snn import Connection, LIFNeuron, SolitonSNN
from .simulated_body import SimulatedBody


class SolitonCognitiveRuntime:
    """Single auditable facade for cognition, SNN events, and persistence."""
    def __init__(self, actions: Sequence[Action], *, neurons: Iterable[LIFNeuron] = (),
                 connections: Iterable[Connection] = (), store_path: str | Path | None = None,
                 admission_policy: AdmissionPolicy = AdmissionPolicy(),
                 plan_horizon: int = 8, body: SimulatedBody | None = None):
        self.agent = CognitiveAgent(actions, plan_horizon=plan_horizon)
        neuron_list = list(neurons) or [LIFNeuron(0)]
        self.snn = SolitonSNN(neuron_list, tuple(connections))
        self.store = EpisodicStore(store_path) if store_path is not None else None
        self.admission_policy = admission_policy
        self.body = body
        self._persisted_events = 0

    def _persist_new_events(self) -> None:
        if self.store is None:
            return
        new_events = self.agent.events[self._persisted_events:]
        self.store.append(new_events)
        self._persisted_events = len(self.agent.events)

    def command(self, text: str, *, timestamp: int = 0) -> dict[str, object]:
        """Ground and execute one bounded cognitive command."""
        result = apply_command(self.agent, text, timestamp=timestamp)
        self._persist_new_events()
        if result is None:
            return {"kind": "goal", "goal": self.agent.goal.name if self.agent.goal else None}
        action, plan = result
        return {"kind": "decision", "action": action.name if action else None,
                "plan": [item.name for item in plan] if plan is not None else None,
                "facts": sorted((fact.predicate, fact.value) for fact in self.agent.facts)}

    def framed_events(self, text: str, *, start_sequence: int = 0) -> dict[str, object]:
        """Verify, admit, execute, and persist a framed AER batch."""
        before = len(self.snn.delivered)
        emitted_before = len(self.snn.emitted)
        self.snn.ingest_framed(text, start_sequence=start_sequence,
                              policy=self.admission_policy)
        self.snn.run()
        delivered = self.snn.delivered[before:]
        emitted = self.snn.emitted[emitted_before:]
        event = CognitiveEvent(self.snn.time, "snn_batch", {
            "delivered": [spike.to_dict() for spike in delivered],
            "emitted": [spike.to_dict() for spike in emitted],
            "metrics": asdict(metrics(self.snn)),
        })
        self.agent.events.append(event)
        self._persist_new_events()
        return {"kind": "snn_batch", "delivered": len(delivered),
                "emitted": len(emitted), "metrics": asdict(metrics(self.snn))}

    def snapshot(self) -> dict[str, object]:
        """Return a JSON-compatible state summary without mutating runtime state."""
        result = {"facts": [[fact.predicate, fact.value] for fact in sorted(
                    self.agent.facts, key=lambda item: (item.predicate, item.value))],
                "goal": self.agent.goal.name if self.agent.goal else None,
                "episodes": len(self.agent.episodes),
                "cognitive_events": len(self.agent.events),
                "memory_records": len(self.store.load()) if self.store else 0,
                "snn_metrics": asdict(metrics(self.snn))}
        if self.body is not None:
            result["body"] = self.body.snapshot()
        return result

    def sense_body(self, *, timestamp: int | None = None, salience: float = 1.0):
        """Sense the simulated body and feed the result through cognition."""
        if self.body is None:
            raise RuntimeError("runtime has no body")
        observation = self.body.sense(timestamp=timestamp, salience=salience)
        result = self.agent.observe(observation)
        self._persist_new_events()
        action, plan = result
        return {"action": action.name if action else None,
                "plan": [item.name for item in plan] if plan is not None else None}

    def actuate_body(self, command: str, dx: float, dy: float, *, tick: int | None = None):
        """Apply a bounded simulated actuator command and persist its result."""
        if self.body is None:
            raise RuntimeError("runtime has no body")
        event = self.body.actuate(command, dx, dy, tick=tick)
        self.agent.events.append(CognitiveEvent(event.tick, "actuator", asdict(event)))
        self._persist_new_events()
        return asdict(event)
