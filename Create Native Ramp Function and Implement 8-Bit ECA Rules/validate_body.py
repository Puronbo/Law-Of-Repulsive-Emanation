import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import (
    Action, BodyState, EpisodicStore, Fact, Goal, SimulatedBody,
    SolitonCognitiveRuntime,
)

body = SimulatedBody(bounds=(-1, 1, -1, 1), max_speed=0.5, energy_per_unit=0.5,
                     initial=BodyState(0, 0, 1.0, 0))
event = body.actuate('step', 0.3, 0.4, tick=1)
assert event.accepted and body.state.x == 0.3 and body.state.y == 0.4
before = body.state
assert not body.actuate('too-fast', 0.5, 0.5, tick=2).accepted
assert body.state.x == before.x and body.state.y == before.y
assert not body.actuate('collision', 1.0, 0.0, tick=3).accepted
assert body.state.x == before.x and body.state.y == before.y
observation = body.sense(timestamp=3)
assert Fact('horizontal', 'right') in observation.facts
assert Fact('vertical', 'up') in observation.facts
assert Fact('battery', 'charged') in observation.facts

# Integrated runtime persists actuator and sensor events and exposes body state.
root = Path('/tmp/soliton_body_memory.jsonl')
root.unlink(missing_ok=True)
rt = SolitonCognitiveRuntime((), store_path=root, body=body)
rt.actuate_body('settle', 0.0, 0.0, tick=4)
rt.sense_body(timestamp=4)
snapshot = rt.snapshot()
assert snapshot['body']['state']['tick'] == 4
assert snapshot['memory_records'] == 2
assert json.loads(json.dumps(snapshot)) == snapshot
assert len(EpisodicStore(root).load()) == 2
print('body validation passed')
