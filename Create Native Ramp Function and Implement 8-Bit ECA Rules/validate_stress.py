import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import (
    AERSpike, LIFNeuron, SolitonSNN, metrics, validate_spike_trace,
)

# Fixed-seed randomized input preserves reproducibility while exercising
# duplicate timestamps, polarity, leakage, and bounded queue behavior.
rng = random.Random(20260903)
spikes = [AERSpike(rng.randrange(0, 20), rng.randrange(-5, 5), 0,
                  -1 if rng.randrange(2) else 1, rng.random()) for _ in range(100)]
spikes.sort(key=lambda spike: spike.timestamp)
net = SolitonSNN([LIFNeuron(0, threshold=2.0)], ())
net.ingest(spikes)
outputs = net.run(max_events=200)
assert validate_spike_trace(net.delivered) == 100
assert all(event.timestamp >= 0 for event in outputs)
report = metrics(net)
assert report.delivered_events == 100
assert report.max_queue_depth == 100
assert report.current_time <= 19
assert report.firing_rate_per_tick >= 0.0
# Deterministic replay of the same seed and inputs.
net.reset()
net.ingest(spikes)
outputs_again = net.run(max_events=200)
assert outputs_again == outputs
assert metrics(net) == report
print('stress validation passed')
print(report)
