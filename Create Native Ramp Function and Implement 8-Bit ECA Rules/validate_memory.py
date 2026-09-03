import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import (
    Action, CognitiveAgent, EpisodicStore, Fact, Goal, Observation,
    apply_command, parse_command,
)

obs = parse_command('observe location=A state=ready salience=0.75', timestamp=3)
assert isinstance(obs, Observation)
assert obs.timestamp == 3 and obs.salience == 0.75
assert Fact('location', 'A') in obs.facts
goal = parse_command('goal location=B state=ready')
assert isinstance(goal, Goal) and len(goal.desired) == 2
for command in ('', 'think location=A', 'observe bad-token', 'goal x=bad=value', 'observe location=A salience=nan'):
    try:
        parse_command(command)
    except (TypeError, ValueError):
        pass
    else:
        raise AssertionError(f'unsupported command accepted: {command!r}')

root = Path('/tmp/soliton_memory_test.jsonl')
root.unlink(missing_ok=True)
store = EpisodicStore(root)
events = []
a = CognitiveAgent((Action('noop', frozenset(), frozenset({Fact('state', 'ready')})),))
a.set_goal(Goal('ready', frozenset({Fact('state', 'ready')})))
apply_command(a, 'observe location=A', timestamp=0)
events.extend(a.events)
assert store.append(events) == len(events)
loaded = store.load()
assert [record.event.encode() for record in loaded] == [event.encode() for event in events]
assert [event.encode() for event in store.events()] == [event.encode() for event in events]
# Tamper detection and sequence checks are mandatory.
original = root.read_text()
root.write_text(original.replace('goal_set', 'goal_tampered', 1))
try:
    store.load()
except ValueError as exc:
    assert 'checksum' in str(exc)
else:
    raise AssertionError('tampered memory record accepted')
root.write_text(original)
print('memory validation passed')
print('records:', len(loaded))
