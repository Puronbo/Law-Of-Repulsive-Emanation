"""Command-line demo for the integrated soliton cognitive runtime."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .cognitive_agent import Action, Fact, Goal
from .runtime import SolitonCognitiveRuntime
from .soliton_snn import AERSpike, Connection, LIFNeuron
from .soliton_framing import encode_frames


def demo(store: str | None) -> dict[str, object]:
    at_a, at_b = Fact("location", "A"), Fact("location", "B")
    move = Action("move-A-B", frozenset({at_a}), frozenset({at_b}), frozenset({at_a}))
    runtime = SolitonCognitiveRuntime(
        (move,), neurons=(LIFNeuron(0), LIFNeuron(1)),
        connections=(Connection(0, 1, 1.0),),
        store_path=store,
    )
    runtime.agent.remember((at_a,))
    runtime.agent.set_goal(Goal("at-B", frozenset({at_b})))
    decision = runtime.command("observe location=A salience=1.0", timestamp=0)
    batch = runtime.framed_events(encode_frames((AERSpike(1, 0, 1),)))
    return {"decision": decision, "snn": batch, "snapshot": runtime.snapshot()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Integrated soliton cognitive runtime")
    parser.add_argument("--store", default=None, help="append-only episodic JSONL path")
    args = parser.parse_args()
    print(json.dumps(demo(args.store), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
