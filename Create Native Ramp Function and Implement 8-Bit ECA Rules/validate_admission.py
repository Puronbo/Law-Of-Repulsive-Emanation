import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import (
    AERSpike, AdmissionPolicy, Connection, LIFNeuron, SolitonSNN,
    admit_spikes, encode_frames,
)

policy = AdmissionPolicy(max_payload=1.0, max_future_ticks=5,
                         max_events=3, max_events_per_timestamp=2)
valid = (AERSpike(0, 0, 1), AERSpike(1, 0, 1, -1, 0.5))
assert admit_spikes(valid, policy=policy) == valid

cases = [
    (lambda: AERSpike(0, 0, 1, payload=float('nan')), 'payload'),
    (lambda: AERSpike(0, 0, 1, payload=-0.1), 'payload'),
    (lambda: admit_spikes((AERSpike(0, 0, 1, channel='unknown'),), policy=policy), 'channel'),
    (lambda: admit_spikes((AERSpike(6, 0, 1),), policy=policy), 'horizon'),
    (lambda: admit_spikes((AERSpike(2, 0, 1), AERSpike(1, 0, 1)), policy=policy), 'ordered'),
    (lambda: admit_spikes(tuple(AERSpike(0, i, 1) for i in range(3)), policy=policy), 'burst'),
]
for action, label in cases:
    try:
        action()
    except (TypeError, ValueError) as exc:
        assert label in str(exc) or label == 'payload'
    else:
        raise AssertionError(f'{label} violation was accepted')

# Framing is verified before admission and then routed atomically.
net = SolitonSNN([LIFNeuron(0), LIFNeuron(1)], (Connection(0, 1, 1.0),))
net.ingest_framed(encode_frames((AERSpike(0, 0, 1),)))
assert len(net.run()) == 1

# Repeated valid batches are bounded by cumulative pending capacity, and a
# rejected batch leaves the queue unchanged so the caller can apply backpressure.
bounded = AdmissionPolicy(max_pending_events=2, max_future_ticks=100)
backlog = SolitonSNN([LIFNeuron(1, threshold=10.0)], ())
backlog.ingest((AERSpike(5, 0, 1), AERSpike(6, 0, 1)), policy=bounded)
before = len(backlog._queue)
try:
    backlog.ingest((AERSpike(7, 0, 1),), policy=bounded)
except ValueError as exc:
    assert 'capacity' in str(exc)
else:
    raise AssertionError('pending capacity violation was accepted')
assert len(backlog._queue) == before == 2
backlog.run(until=5)
backlog.ingest((AERSpike(7, 0, 1),), policy=bounded)
assert len(backlog._queue) == 2
print('admission validation passed')
