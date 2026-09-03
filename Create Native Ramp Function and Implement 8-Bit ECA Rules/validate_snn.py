import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from soliton_eca import (
    AERSpike, Action, Connection, LIFNeuron, SolitonSNN, decode_spike,
    decode_spike_stream, encode_spike, encode_spike_stream, trace_digest,
)

for constructor in (
    lambda: AERSpike(0, 0, 1, payload=float('inf')),
    lambda: Connection(0, 1, float('nan')),
    lambda: LIFNeuron(0, tau=float('nan')),
    lambda: Action('bad', cost=float('inf')),
):
    try:
        constructor()
    except (TypeError, ValueError):
        pass
    else:
        raise AssertionError('non-finite parameter accepted')

spikes = [AERSpike(0, 10, 20, -1, 0.75, 'signed'), AERSpike(4, 11, 20)]
wire = encode_spike_stream(spikes)
assert decode_spike(encode_spike(spikes[0])) == spikes[0]
assert decode_spike_stream(wire) == spikes

# Coincident inputs fire neuron 2; its output is delayed to neuron 3.
neurons = [LIFNeuron(i, tau=10.0, threshold=1.0, refractory=2) for i in range(4)]
network = SolitonSNN(neurons, (Connection(2, 3, 1.0, delay=2),))
network.inject((AERSpike(0, 0, 2, 1, 0.6), AERSpike(0, 1, 2, 1, 0.6)))
emitted = network.run()
assert [(s.timestamp, s.source, s.target) for s in emitted] == [(0, 2, -1), (2, 3, -1)]
assert [(s.timestamp, s.source, s.target) for s in network.delivered] == [(0, 0, 2), (0, 1, 2), (2, 2, 3)]
assert network.neurons[3].voltage == 0.0

# Refractory behavior suppresses a second event during the refractory window.
neuron = LIFNeuron(5, threshold=1.0, refractory=3)
assert neuron.receive(AERSpike(0, 0, 5, payload=1.0), 1.0) is not None
assert neuron.receive(AERSpike(1, 0, 5, payload=1.0), 1.0) is None

# STDP potentiates a causal pre-before-post pair.
stdp = SolitonSNN([LIFNeuron(0), LIFNeuron(1)],
                  (Connection(0, 1, 1.0),), stdp=True)
stdp.inject((AERSpike(0, 0, 1),))
stdp.run()
assert stdp.weights()[(0, 1)] > 1.0

# A source-global trace must not potentiate an unrelated target synapse.
isolated = SolitonSNN([LIFNeuron(0), LIFNeuron(1), LIFNeuron(2)],
                      (Connection(0, 1, 1.0), Connection(0, 2, 1.0)), stdp=True)
isolated.inject((AERSpike(0, 0, 1),))
isolated.run()
assert isolated.weights()[(0, 1)] > 1.0
assert isolated.weights()[(0, 2)] == 1.0

# Post-before-pre activity depresses a connection when the later pre-event
# does not itself reach threshold.
anti = SolitonSNN([LIFNeuron(0), LIFNeuron(1)],
                  (Connection(0, 1, 0.5),), stdp=True)
anti.inject((AERSpike(0, 9, 1, payload=1.0), AERSpike(1, 0, 1, payload=1.0)))
anti.run()
assert anti.weights()[(0, 1)] < 0.5

# Same-timestamp events retain deterministic injection order.
ordered = SolitonSNN([LIFNeuron(1, threshold=10.0)], ())
ordered.inject((AERSpike(0, 7, 1), AERSpike(0, 8, 1)))
ordered.run()
assert [event.source for event in ordered.delivered] == [7, 8]

# Recurrent excitation must terminate with an explicit event budget.
loop = SolitonSNN([LIFNeuron(0), LIFNeuron(1)],
                  (Connection(0, 1, 2.0), Connection(1, 0, 2.0)))
loop.inject((AERSpike(0, 99, 0),))
try:
    loop.run(max_events=10)
except RuntimeError as exc:
    assert 'event budget' in str(exc)
else:
    raise AssertionError('recurrent loop exceeded budget without failure')

# Inhibitory polarity cancels excitation without firing.
inhibitory = LIFNeuron(6, threshold=1.0)
assert inhibitory.receive(AERSpike(0, 0, 6, 1, 0.6), 1.0) is None
assert inhibitory.receive(AERSpike(0, 0, 6, -1, 0.6), 1.0) is None
assert inhibitory.voltage == 0.0

# Reset makes an identical capture replay bit-for-bit and can restore weights.
replay = SolitonSNN([LIFNeuron(0), LIFNeuron(1)], (Connection(0, 1, 1.0),), stdp=True)
capture = (AERSpike(0, 0, 1),)
replay.inject(capture)
first = replay.run()
first_digest = trace_digest(first)
replay.connections[(0, 1)] = Connection(0, 1, 0.25)
replay.reset(reset_weights=True)
replay.inject(capture)
second = replay.run()
assert trace_digest(second) == first_digest
assert replay.weights()[(0, 1)] > 1.0
assert replay.delivered == list(capture)

# Past events and malformed timing must be rejected.
try:
    network.inject((AERSpike(0, 9, 2),))
except ValueError:
    pass
else:
    raise AssertionError('unknown target accepted')
try:
    network.run(until=-1)
except ValueError:
    pass
else:
    raise AssertionError('invalid until accepted')
print('SNN validation passed')
print('wire:', wire)
print('weights:', stdp.weights())
