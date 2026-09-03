"""Run a reproducible safe simulated-body cognitive/SNN scenario."""
from __future__ import annotations

import json
from pathlib import Path

from .cognitive_agent import Action, Fact, Goal
from .episodic_store import EpisodicStore
from .runtime import SolitonCognitiveRuntime
from .simulated_body import BodyState, SimulatedBody
from .soliton_framing import encode_frames
from .soliton_snn import AERSpike, Connection, LIFNeuron


def run(output_dir: str | Path = "/tmp/soliton_simulation") -> dict[str, object]:
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    memory_path = root / "episodes.jsonl"
    memory_path.unlink(missing_ok=True)

    body = SimulatedBody(
        bounds=(-2.0, 2.0, -2.0, 2.0), max_speed=0.75,
        energy_per_unit=0.2, initial=BodyState(0.0, 0.0, 1.0, 0),
    )
    at_origin = Fact("location", "origin")
    at_east = Fact("location", "east")
    move_east = Action("move-east", frozenset({at_origin}),
                       frozenset({at_east}), frozenset({at_origin}), cost=1.0)
    runtime = SolitonCognitiveRuntime(
        (move_east,), neurons=(LIFNeuron(0, threshold=1.0), LIFNeuron(1, threshold=1.0)),
        connections=(Connection(0, 1, weight=1.0, delay=1),),
        store_path=memory_path, body=body,
    )
    runtime.agent.remember((at_origin,))
    runtime.agent.set_goal(Goal("reach-east", frozenset({at_east})))

    records: list[dict[str, object]] = []
    records.append({"step": 0, "sensor": runtime.sense_body(timestamp=0, salience=1.0)})
    records.append({"step": 1, "actuator": runtime.actuate_body("east", 0.5, 0.0, tick=1)})
    records.append({"step": 2, "sensor": runtime.sense_body(timestamp=1, salience=0.5)})
    records.append({"step": 3, "actuator": runtime.actuate_body("unsafe-fast", 1.0, 0.0, tick=2)})
    records.append({"step": 4, "actuator": runtime.actuate_body("unsafe-boundary", 2.0, 0.0, tick=3)})
    framed = encode_frames((AERSpike(4, 0, 1, payload=1.0), AERSpike(5, 0, 1, polarity=-1, payload=0.25)))
    records.append({"step": 5, "snn": runtime.framed_events(framed)})

    report = {
        "simulation": "safe-soliton-body-v1",
        "real_hardware": False,
        "steps": records,
        "final_snapshot": runtime.snapshot(),
        "memory_records": len(EpisodicStore(memory_path).load()),
    }
    (root / "simulation_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
