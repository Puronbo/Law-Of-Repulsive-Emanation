import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import (
    Action, AERSpike, Connection, Fact, Goal, LIFNeuron,
    SolitonCognitiveRuntime, encode_frames,
)

root = Path('/tmp/soliton_runtime_memory.jsonl')
root.unlink(missing_ok=True)
at_a, at_b = Fact('location', 'A'), Fact('location', 'B')
move = Action('move-A-B', frozenset({at_a}), frozenset({at_b}), frozenset({at_a}))
runtime = SolitonCognitiveRuntime(
    (move,), neurons=(LIFNeuron(0), LIFNeuron(1)),
    connections=(Connection(0, 1, 1.0),), store_path=root,
)
runtime.agent.remember((at_a,))
assert runtime.command('goal location=B')['kind'] == 'goal'
decision = runtime.command('observe location=A salience=1.0', timestamp=0)
assert decision['action'] == 'move-A-B'
batch = runtime.framed_events(encode_frames((AERSpike(1, 0, 1),)))
assert batch['delivered'] == 1 and batch['emitted'] == 1
snapshot = runtime.snapshot()
assert snapshot['episodes'] == 1
assert snapshot['memory_records'] == 3
assert snapshot['snn_metrics']['delivered_events'] == 1
assert json.loads(json.dumps(snapshot)) == snapshot
assert len(runtime.store.load()) == 3
print('runtime validation passed')
print(json.dumps(snapshot, sort_keys=True))
