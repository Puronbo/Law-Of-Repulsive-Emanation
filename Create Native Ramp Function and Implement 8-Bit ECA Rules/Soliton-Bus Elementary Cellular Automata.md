# Soliton-Bus Elementary Cellular Automata

This package implements the requested 8-bit elementary cellular automata (ECA) rules:

`4, 12, 36, 44, 68, 76, 100, 108, 132, 140, 164, 172, 196, 204, 228, 236`.

## Native ramp primitives

`ramp(x)` is the positive native ramp expressed as a sign gate:

```python
x * (x > 0)
```

`negative_ramp(x)` provides the complementary negative branch:

```python
x * (x < 0)
```

The comparison is kept explicit so the primitives can map directly to a branchless dataflow or hardware implementation.

## Soliton-bus architecture

A **soliton** is a localized immutable message carrying a bus name, spatial position, binary value, and generation number. A `SolitonBus` is a FIFO transport. Every `EcaCell` receives three neighborhood solitons, forms the 3-bit neighborhood index, looks up the corresponding rule bit, and emits exactly one output soliton.

`SolitonECA.step()` injects all neighborhood frames before consuming outputs. This barrier makes the update synchronous, as required by ECA semantics, while keeping all computation and state transfer on soliton buses. Finite-grid boundaries are zero-valued ghost solitons.

## Usage

```python
from soliton_eca import SolitonECA, evolve

machine = SolitonECA(204, width=31, initial=[0] * 15 + [1] + [0] * 15)
for state in machine.run(10):
    print("".join("#" if bit else "." for bit in state))

# Or collect all emitted generations.
rows = evolve(4, [0, 0, 0, 1, 0, 0, 0], generations=8)
```

Run the regression suite from this directory with:

```bash
cd .. && python3 -m pytest -q soliton_eca/test_soliton_eca.py
```

## Soliton neural network

`SolitonNeuralNetwork` is a dense, synchronous feed-forward network. Each
weighted connection is a `WeightedSolitonBus`; each neuron waits for all
incoming synaptic solitons, adds a bias, applies the native positive ramp, and
emits one activation soliton. Training uses online squared-error
backpropagation and the piecewise derivative of the ramp.

```python
from soliton_eca import SolitonNeuralNetwork

net = SolitonNeuralNetwork((2, 4, 1), seed=11)
losses = net.train(
    [((0.0, 0.0), (0.0,)), ((0.0, 1.0), (1.0,)),
     ((1.0, 0.0), (1.0,)), ((1.0, 1.0), (0.0,))],
    epochs=200,
    learning_rate=0.03,
)
prediction = net.forward((1.0, 0.0))
```

The neural architecture is dependency-free and uses a deterministic internal
pseudo-random initializer. The physics digital twin additionally uses NumPy.

## Rigorous soliton prototype

`soliton_protocol.py` defines an explicit packet contract:

```text
(tick, position, velocity, amplitude, channel, phase)
```

`SolitonLattice` implements synchronous transport, reflective or annihilating
boundaries, event logging, and collision modes for XOR, signed summation, and
destructive cancellation. This makes routing testable before mapping it to
optical or neuromorphic hardware.

`soliton_physics.py` provides a generalized nonlinear Schrödinger digital twin
using a symmetric split-step Fourier method. The normalized fundamental pulse
`sech(t)` is used as the first invariance benchmark. `soliton_validation()`
returns relative power-envelope error and relative energy drift.

Run the expanded checks from the project root:

```bash
python3 soliton_eca/validate.py
python3 soliton_eca/validate_rigorous.py
```

The intended development order is: validate propagation, validate packet
routing primitives, add signed weighted mixing, measure a real activation
transfer function, then introduce learning and hardware-in-the-loop
calibration. Accuracy alone is insufficient; report timing error, packet loss,
crosstalk, drift, BER/SER, energy per event, and end-to-end latency.

## Signed differential mixing

`DifferentialEncoder` represents a signed scalar as two explicitly routed
channels: positive and negative. This avoids the invalid assumption that
optical intensity can directly represent a negative weight. `CalibratedMixer`
performs weighted signed accumulation and applies measured gain, offset,
saturation, and deterministic noise parameters.

```python
from soliton_eca import CalibratedMixer, DifferentialEncoder

encoder = DifferentialEncoder()
signals = (
    encoder.encode(+0.75, tick=0, position=8),
    encoder.encode(-0.25, tick=0, position=8),
)
mixer = CalibratedMixer((2.0, 3.0), bias=0.1)
output = mixer.mix(signals, tick=0, position=8)
assert output.value == 0.85
```

`ramp_activation` and `sigmoid_activation` are available as reference
transfer functions. Use `transfer_curve` to sample a device’s measured
input/output behavior. Acceptance tests should verify the signed round trip,
weight error, saturation ceiling, noise sensitivity, and activation monotonicity
before connecting the mixer to a trainable network.

## Hardware-in-the-loop perturbation harness

`CalibratedSolitonLayer` maps a dense layer onto calibrated soliton mixers.
`Perturbation` makes four hardware risks explicit: gain error, arrival-time
jitter, packet loss, and channel crosstalk. Misaligned packets are rejected
with a measured total-error result rather than silently entering the wrong
synchronous frame.

```python
from soliton_eca import CalibratedSolitonLayer, Perturbation, perturbation_report

layer = CalibratedSolitonLayer(((1.0, -0.5), (0.25, 2.0)), (0.1, -0.2))
report = perturbation_report(
    layer,
    (0.8, -0.4),
    (Perturbation(), Perturbation(gain_error=0.1),
     Perturbation(timing_jitter=1), Perturbation(crosstalk=0.2)),
)
```

The report uses normalized Euclidean output error. Ideal transport must have
zero modeled error, timing misalignment must be detected, and every nonzero
impairment must be visible in the measured error. This is a simulation
harness, not a claim of physical-device validation. Run it with:

```bash
python3 soliton_eca/validate_hardware.py
```

## Closed-loop calibration and robust training

`fit_affine_calibration` estimates gain and offset from measured transfer
pairs using ordinary least squares and reports root-mean-square residual. The
resulting `ActivationCalibration` can be applied to every mixer in a layer.
`robust_train` then uses finite-difference optimization against the same fixed
impairment profile used for evaluation. Finite differences are deliberate:
they remain valid across clipping, packet loss, and other non-smooth modeled
effects where an ideal analytical gradient would be misleading.

```python
from soliton_eca import (
    CalibratedSolitonLayer, Perturbation, fit_affine_calibration, robust_train,
)

calibration = fit_affine_calibration(
    [(0.0, 0.1), (1.0, 0.6), (2.0, 1.0)], saturation=2.0,
)
layer = CalibratedSolitonLayer(((0.2, -0.1),), calibration=calibration.calibration)
losses = robust_train(
    layer,
    [((1.0, 0.0), (1.0,)), ((0.0, 1.0), (0.0,))],
    epochs=20,
    impairment=Perturbation(gain_error=0.1),
)
```

Acceptance requires a nonzero measured transfer residual to be reported, a
monotonic calibrated response over the operating range, and lower robust loss
after training. Calibration does not remove physical noise or timing errors;
it only identifies the model used to compensate and retrain the layer.

## End-to-end calibrated network

`CalibratedSolitonNetwork` chains calibrated differential-soliton layers and
applies the native ramp after each layer. Its `train_robust` method evaluates
the complete multilayer impaired path while perturbing each weight, so it does
not optimize one layer against an ideal downstream system. This is currently
a finite-difference optimizer intended for small research prototypes; larger
networks should replace it with analytic or automatic differentiation after
the measured device transfer functions are stable.

```python
from soliton_eca import CalibratedSolitonNetwork, Perturbation

network = CalibratedSolitonNetwork(
    weights=(((0.5, 0.25), (0.25, 0.5)), ((0.5, 0.5),)),
    biases=((0.1, 0.1), (0.0,)),
)
losses = network.train_robust(
    [((1.0, 0.0), (0.75,)), ((0.0, 1.0), (0.75,)),
     ((1.0, 1.0), (1.0,)), ((0.0, 0.0), (0.0,))],
    epochs=8,
    impairment=Perturbation(gain_error=0.05),
)
```

The end-to-end acceptance test requires deterministic inference, dimensionally
valid layer chaining, and decreasing loss under a nonzero gain impairment.
Run it with `python3 soliton_eca/validate_end_to_end.py`.

## Adversarial validation

The implementation includes an adversarial validation pass covering empty-bus
inspection, reflective boundary invariants, invalid collision modes,
degenerate calibration data, malformed layer dimensions, and floating-point
identity behavior at zero propagation distance. The audit also removed private
queue reads from neural computation, rebuilt active mixers during numerical
weight trials, rejected malformed target shapes, and enforced exact bias-layer
counts.

Run the full suite from `/home/ubuntu`:

```bash
python3 soliton_eca/validate.py
python3 soliton_eca/validate_rigorous.py
python3 soliton_eca/validate_mixing.py
python3 soliton_eca/validate_hardware.py
python3 soliton_eca/validate_calibration.py
python3 soliton_eca/validate_end_to_end.py
python3 soliton_eca/validate_adversarial.py
```

The tests are reference-model checks. They do not establish performance or
reliability of a physical optical device; those require measured transfer
curves, timing distributions, packet-loss statistics, crosstalk spectra, and
wall-plug energy measurements.

## Measured-curve benchmark

`load_transfer_csv` accepts explicit `input,output` measurements and rejects
missing columns, malformed numeric rows, and underspecified curves.
`calibrate_csv` fits the affine device model and reports monotonicity, dynamic
range, residual error, and saturation fraction. `impairment_sweep` evaluates a
deterministic Cartesian grid of gain, timing, crosstalk, and packet-loss cases.

The included `sample_transfer.csv` fixture produces a monotonic five-point
curve with fitted RMSE `0.110516967` and a 24-case sweep. The generated
`benchmark_report.md` is an example of the machine-readable acceptance summary.
These values are fixtures, not physical-device claims.

## Measurement-quality gate

`QualityGate` is the promotion barrier before device data can drive robust
training. The default gate requires at least five samples, nonzero input and
output span, a monotonic response, and relative affine-fit RMSE no greater than
25% of the measured output span. `evaluate_quality` also reports leave-one-out
gain and offset standard deviations, which expose calibration sensitivity to
individual measurements. `require_quality` raises instead of silently
proceeding when the gate fails.

This threshold is a starting engineering policy, not a universal physical
standard. Tighten it as measurement noise and device requirements become
known. The benchmark validator now requires the default gate to pass before
running its impairment sweep.

## Replicate-aware calibration

`aggregate_replicates` groups repeated observations at the same input and
reports mean output, population standard deviation, and count. This matters
because a monotonic mean curve can still be physically unstable. `calibrate_replicates`
fits the mean response, applies the ordinary quality gate, and adds a maximum
relative replicate-standard-deviation gate. The default workflow should use
multiple captures per input, randomize capture order where possible, and retain
the raw observations alongside the aggregated curve.

The stable fixture has two observations per input and relative replicate
standard deviation `0.00185185`; the unstable fixture has `0.185185` and is
rejected at a `0.02` threshold. Run:

```bash
python3 soliton_eca/validate_replicates.py
```

## Acquisition-order drift gate

Replicate variance does not detect a slow change that is monotonic across the
whole capture. `estimate_drift` fits calibration residual versus actual
acquisition order, and `calibrate_replicates` rejects the dataset when the
normalized residual slope exceeds its configured threshold. Measurement order
must therefore be recorded; randomized or interleaved input schedules are
preferred so transfer-curve shape is not mistaken for temporal drift.

The default normalized drift limit is `0.01` output-span units per capture
step. This is a policy threshold that must be tightened or relaxed from actual
instrument repeatability data. A drift rejection is a reason to recapture or
segment the run, not a reason to silently discard the time variable.

## Event-driven soliton SNN

`AERSpike` is the wire-level packet: timestamp, source address, target
address, polarity, payload, and channel. `encode_spike` and
`decode_spike_stream` provide canonical JSON-lines serialization suitable for
logging or a transport adapter. `SolitonSNN` schedules events by timestamp,
routes them through integer-tick delayed `Connection` buses, and updates
`LIFNeuron` state only when an event arrives. Refractory suppression, causal
ordering, event budgets, and unknown-address rejection are explicit.

Optional local STDP applies causal potentiation and anti-causal depression to
the same connection table used for routing. This is a reference event-driven
SNN, not a claim that JSON is the final physical-link encoding; a hardware
adapter can map the same fields onto an optical or neuromorphic packet bus.

`SolitonSNN.reset()` clears queued events, membrane state, traces, and prior
event logs; `reset_weights=True` also restores the initial connection table.
`trace_digest` hashes the canonical ordered JSON representation of an event
trace, enabling capture replay checks and fault-recovery audits. Inhibitory
polarity is tested as signed payload cancellation rather than an ad hoc
negative weight convention.

For transport integrity, `AERFrame` wraps each spike with a contiguous
sequence number and SHA-256 checksum over the sequence plus canonical spike
payload. `encode_frames` and `decode_frames` detect payload corruption,
reordering, duplicates, and gaps. Non-contiguous inspection is available only
through an explicit `require_contiguous=False` choice; deployment ingestion
should keep the strict default.

`AdmissionPolicy` is the SNN ingress boundary. `admit_spikes` enforces allowed
channels, finite non-negative payloads, future-time horizon, total batch size,
per-timestamp burst size, and timestamp ordering before queueing. The
`SolitonSNN.ingest_framed` path verifies frame checksums and contiguous sequence
numbers first, then applies admission atomically. This separates wire
integrity, endpoint policy, and neuron execution, making rejected traffic
observable without partially mutating scheduler state.

`max_pending_events` adds cumulative backpressure beyond per-batch limits.
Admission counts the scheduler backlog before queueing; if capacity would be
exceeded, the whole batch is rejected and the existing queue is unchanged.
After events are consumed, capacity becomes available again. A transport
adapter should translate this rejection into flow control or retry behavior,
not drop the batch silently.

STDP traces are connection-local: a pre-event on `(source, target_a)` cannot
potentiate `(source, target_b)` merely because the source address is shared.
This fan-out isolation is explicitly tested in `validate_snn.py`.

The SNN scheduler preserves insertion order for events sharing a timestamp,
applies anti-causal STDP depression only when post activity precedes a later
pre-event, and enforces a configurable `max_events` budget. The budget is a
safety boundary for recurrent networks: exceeding it raises rather than
silently hanging or producing an unbounded packet stream.

```python
from soliton_eca import AERSpike, Connection, LIFNeuron, SolitonSNN

net = SolitonSNN(
    [LIFNeuron(0), LIFNeuron(1)],
    [Connection(0, 1, weight=1.0, delay=1)],
    stdp=True,
)
net.inject([AERSpike(0, source=0, target=1)])
emitted = net.run()
```

Run the protocol and dynamics checks with:

```bash
python3 soliton_eca/validate_snn.py
```

## Parameter uncertainty gate

`estimate_uncertainty` computes normal-approximation confidence intervals for
the fitted gain and offset, residual standard deviation, degrees of freedom,
and prediction half-width at any input. `require_uncertainty` evaluates both
ends of the intended operating range and blocks promotion when predicted
measurement uncertainty exceeds the error budget. With only two points the
residual degrees of freedom are zero, so uncertainty is treated as unbounded
rather than manufactured from insufficient data.

The benchmark applies this gate over `[-2, 2]` before running its impairment
sweep. This is a model-based statistical screen; it does not replace
confidence intervals from repeated physical captures or independent validation
data.

## Operating-domain coverage gate

`evaluate_coverage` verifies that the intended input range lies inside the
measured domain and can also reject large internal gaps between measured input
levels. `require_coverage` blocks promotion by default when extrapolation or
undersampled gaps are present. Extrapolation can be enabled only through an
explicit `allow_extrapolation=True` decision, and the resulting report records
that authorization. Confidence intervals do not make extrapolation equivalent
to measurement.

The benchmark requires complete coverage of `[-2, 2]` with no internal input
gap greater than `1.0` before it runs holdout, uncertainty, or impairment
checks.

## Independent holdout gate

In-sample residuals and confidence intervals can look acceptable when the
affine model is misspecified. `leave_one_input_out` therefore removes each
input level, fits the remaining levels, and predicts the held-out mean.
`require_holdout` blocks promotion when the worst held-out error exceeds the
configured fraction of output span. The benchmark applies a `0.35` normalized
maximum-error threshold before impairment evaluation. For production data,
use repeated captures and reserve an entirely independent validation run in
addition to this leave-one-input-out screen.

## Bounded AGI-like cognitive prototype

`CognitiveAgent` composes the validated substrate into an auditable cognitive
loop: observations become facts and episodic records, a goal defines desired
facts, bounded breadth-first planning selects an applicable action, salience is
processed through an event-driven LIF neuron, and the decision is emitted as a
canonical cognitive trace. Trace hashing makes identical runs replayable.

This is **AGI-like in architecture, not in capability**. It has explicit
symbolic facts, a finite action vocabulary, bounded search, in-process memory,
and no open-ended language grounding, world model, autonomous persistence, or
general transfer claim. Those limits are deliberate: every action is auditable,
every state transition is testable, and no action is invented when the goal is
unreachable.

```python
from soliton_eca import Action, CognitiveAgent, Fact, Goal, Observation

at_a, at_b = Fact('location', 'A'), Fact('location', 'B')
move = Action('move', frozenset({at_a}), frozenset({at_b}), frozenset({at_a}))
agent = CognitiveAgent((move,), plan_horizon=2)
agent.remember((at_a,))
agent.set_goal(Goal('at-B', frozenset({at_b})))
action, plan = agent.observe(Observation(0, frozenset({at_a}), salience=1.0))
```

Run the cognitive validation with:

```bash
python3 soliton_eca/validate_cognitive.py
```

## Bounded language grounding and episodic storage

`parse_command` accepts only a small explicit grammar: `observe` followed by
`predicate=value` facts and optional numeric salience, or `goal` followed by
`predicate=value` desired facts. Unsupported verbs, malformed tokens, and
non-finite salience are rejected; this is intentional grounding, not unrestricted
natural-language understanding.

`EpisodicStore` persists canonical cognitive events as append-only JSONL records
with contiguous sequence numbers and SHA-256 checksums. Loading verifies every
record before returning it. A corrupted record cannot be silently replayed or
extended. JSON normalization means consumers should compare canonical event
encodings rather than relying on Python tuple/list identity.

```python
from soliton_eca import EpisodicStore, apply_command

apply_command(agent, 'observe location=A salience=0.8', timestamp=0)
store = EpisodicStore('/tmp/episodes.jsonl')
store.append(agent.events)
recovered = store.events()
```

Run the grounding and persistence checks with:

```bash
python3 soliton_eca/validate_memory.py
```

## Cost-aware cognitive planning

The planner uses bounded Dijkstra-style search over symbolic fact states. Action
`cost` is now part of the objective, so a longer plan can be preferred when its
accumulated cost is lower than a short expensive alternative. Positive-cost
plans are terminated only when the lowest-cost goal state is removed from the
priority queue; equal-cost alternatives resolve in declared action order. The
finite `plan_horizon` remains a hard safety bound, and unreachable goals still
produce an auditable no-op.

## Numeric trust boundaries

All externally meaningful numeric constructors now reject non-finite values.
This includes AER payloads, synaptic weights, LIF parameters, cognitive action
costs, activation calibration, impairment parameters, and sigmoid parameters.
The rule is deliberate: NaN and infinity can evade ordinary positivity checks,
poison comparisons, and create non-reproducible planner or neuron behavior.
Ingress limits remain necessary even for finite values.

## Packaging, observability, and stress validation

The repository includes `/home/ubuntu/pyproject.toml` for reproducible Python
installation. Use `python3 -m pip install -e .` from that directory. The package
has no hidden runtime service and keeps the physical-device model explicitly
simulated.

`SNNMetrics` reports delivered events, emitted spikes, maximum queue depth,
current simulation time, firing rate, and synaptic weight range. The fixed-seed
stress validator exercises one hundred timestamped signed events and verifies
bounded execution, ordered traces, queue metrics, and exact replay equivalence.

```bash
cd /home/ubuntu
python3 -m pip install -e .
python3 soliton_eca/validate_stress.py
```

## Unified runtime and CLI

`SolitonCognitiveRuntime` is the integrated facade. It accepts bounded grounded
commands, executes cognitive planning, ingests checksummed AER frames through
admission and backpressure, runs the event-driven SNN, records runtime metrics,
and appends cognitive/SNN events to the checksummed episodic store. Its
`snapshot()` result is directly JSON-compatible for monitoring or test output.

The installed `soliton-cognitive` command runs a deterministic demonstration:

```bash
cd /home/ubuntu
python3 -m pip install -e .
soliton-cognitive --store /tmp/soliton_memory.jsonl
```

The complete integrated path is tested by `validate_runtime.py`. A CLI adapter
is intentionally only a local reference endpoint; production transport,
authentication, authorization, and external action side effects still require
separate design and explicit policy.

## Safe simulated body

`SimulatedBody` provides embodiment without real-world side effects. It stores a
2-D position, battery, tick, workspace bounds, and actuator limits. `actuate`
rejects non-finite, over-speed, boundary-colliding, or energy-insufficient
commands without changing position, and records every result. `sense` grounds
position and battery into symbolic cognitive facts. `SolitonCognitiveRuntime`
exposes `sense_body` and `actuate_body`, persisting both sensor and actuator
events in the same checksummed episodic store.

This body is deliberately a simulator. It does not access motors, devices,
networks, or external systems. A physical adapter would require separate
hardware authorization, watchdogs, emergency stop behavior, calibration, and
human-reviewed safety policy.

```python
from soliton_eca import SimulatedBody, SolitonCognitiveRuntime

body = SimulatedBody(bounds=(-1, 1, -1, 1), max_speed=0.5)
runtime = SolitonCognitiveRuntime((), body=body)
runtime.actuate_body('step', 0.2, 0.1, tick=1)
sensor_result = runtime.sense_body(timestamp=1)
```

Run the embodiment checks with:

```bash
python3 soliton_eca/validate_body.py
```

## Reproducible closed-loop simulation

`simulate.py` runs the complete safe-body scenario without real hardware. It
feeds sensor observations through cognition, applies one accepted actuator
movement, attempts speed and boundary violations, injects checksummed AER
traffic, runs the SNN, and persists the resulting audit records.

Run it with:

```bash
cd /home/ubuntu
python3 -m soliton_eca.simulate
```

The report is written to `/tmp/soliton_simulation/simulation_report.json` and
memory to `/tmp/soliton_simulation/episodes.jsonl`. In the reference run, the
body ends at `(x=0.5, y=0.0)` with battery `0.9`; actuator outcomes are
`accepted, rejected, rejected`; two SNN events are delivered and one spike is
emitted; and seven memory records are persisted. These are deterministic
simulator results, not measurements of physical hardware.
