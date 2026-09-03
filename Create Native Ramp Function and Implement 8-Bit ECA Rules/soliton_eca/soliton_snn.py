"""Working event-driven soliton spiking neural network.

The network uses timestamped address-event spikes. No global clock step is
required: the scheduler consumes the next causal event, updates one LIF neuron,
and routes any emitted spike over delayed soliton buses.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import heapq
import json
from math import exp, isfinite
from typing import Iterable, Iterator, Sequence


@dataclass(frozen=True, slots=True, order=True)
class AERSpike:
    """Address-event soliton packet on the SNN wire protocol."""
    timestamp: int
    source: int
    target: int
    polarity: int = 1
    payload: float = 1.0
    channel: str = "spike"

    def __post_init__(self) -> None:
        if self.timestamp < 0 or self.polarity not in (-1, 1):
            raise ValueError("timestamp must be non-negative and polarity ±1")
        if not isfinite(self.payload) or self.payload < 0:
            raise ValueError("payload must be finite and non-negative")
        if not self.channel:
            raise ValueError("channel must not be empty")
        if not all(isinstance(x, int) for x in (self.source, self.target)):
            raise TypeError("source and target must be integer addresses")

    def to_dict(self) -> dict[str, int | float | str]:
        return {"timestamp": self.timestamp, "source": self.source,
                "target": self.target, "polarity": self.polarity,
                "payload": self.payload, "channel": self.channel}

    @classmethod
    def from_dict(cls, value: dict[str, object]) -> "AERSpike":
        required = ("timestamp", "source", "target", "polarity", "payload", "channel")
        if any(key not in value for key in required):
            raise ValueError("AER spike is missing a required field")
        return cls(int(value["timestamp"]), int(value["source"]), int(value["target"]),
                   int(value["polarity"]), float(value["payload"]), str(value["channel"]))


def encode_spike(spike: AERSpike) -> str:
    """Serialize one spike as canonical JSON."""
    return json.dumps(spike.to_dict(), sort_keys=True, separators=(",", ":"))


def decode_spike(line: str) -> AERSpike:
    """Deserialize one JSON-line spike and reject trailing records."""
    value = json.loads(line)
    if not isinstance(value, dict):
        raise ValueError("one JSON object is required")
    return AERSpike.from_dict(value)


def encode_spike_stream(spikes: Iterable[AERSpike]) -> str:
    return "\n".join(encode_spike(spike) for spike in spikes)


def decode_spike_stream(text: str) -> list[AERSpike]:
    return [decode_spike(line) for line in text.splitlines() if line.strip()]


@dataclass(frozen=True, slots=True)
class Connection:
    source: int
    target: int
    weight: float
    delay: int = 1

    def __post_init__(self) -> None:
        if not isfinite(self.weight) or self.delay < 1:
            raise ValueError("connection delay must be at least one tick")


class LIFNeuron:
    """Continuous-time leaky integrate-and-fire neuron sampled at events."""
    def __init__(self, address: int, *, tau: float = 10.0,
                 threshold: float = 1.0, reset: float = 0.0,
                 refractory: int = 1):
        if (not all(isfinite(x) for x in (tau, threshold, reset))
                or tau <= 0 or threshold <= 0 or refractory < 0):
            raise ValueError("tau/threshold must be positive and refractory non-negative")
        self.address, self.tau = address, float(tau)
        self.threshold, self.reset = float(threshold), float(reset)
        self.refractory = refractory
        self.voltage = float(reset)
        self.last_timestamp = 0
        self.refractory_until = 0

    def reset_state(self) -> None:
        """Reset membrane and timing state without changing neuron parameters."""
        self.voltage = self.reset
        self.last_timestamp = 0
        self.refractory_until = 0

    def receive(self, spike: AERSpike, weight: float) -> AERSpike | None:
        """Consume one event, decay voltage, integrate, and optionally fire."""
        if spike.target != self.address:
            raise ValueError("spike target does not match neuron address")
        if spike.timestamp < self.last_timestamp:
            raise ValueError("events must arrive in nondecreasing timestamp order")
        dt = spike.timestamp - self.last_timestamp
        self.voltage *= exp(-dt / self.tau)
        self.last_timestamp = spike.timestamp
        if spike.timestamp < self.refractory_until:
            return None
        self.voltage += weight * spike.polarity * spike.payload
        if self.voltage < self.threshold:
            return None
        self.voltage = self.reset
        self.refractory_until = spike.timestamp + self.refractory
        return AERSpike(spike.timestamp, self.address, -1, 1, 1.0, "spike")


class SolitonSNN:
    """Event scheduler, delayed soliton buses, LIF neurons, and local STDP."""
    def __init__(self, neurons: Iterable[LIFNeuron], connections: Iterable[Connection],
                 *, stdp: bool = False, a_plus: float = 0.01,
                 a_minus: float = 0.012, stdp_tau: float = 20.0):
        self.neurons = {neuron.address: neuron for neuron in neurons}
        self.connections = {(c.source, c.target): c for c in connections}
        self._initial_connections = dict(self.connections)
        if not self.neurons:
            raise ValueError("at least one neuron is required")
        if any(c.source not in self.neurons or c.target not in self.neurons for c in self.connections.values()):
            raise ValueError("every connection endpoint must reference a neuron")
        if stdp and (a_plus < 0 or a_minus < 0 or stdp_tau <= 0):
            raise ValueError("STDP rates non-negative and tau positive")
        self.stdp, self.a_plus, self.a_minus, self.stdp_tau = stdp, a_plus, a_minus, stdp_tau
        self._queue: list[tuple[int, int, AERSpike]] = []
        self._sequence = 0
        self.max_queue_depth = 0
        self.time = 0
        self.emitted: list[AERSpike] = []
        self.delivered: list[AERSpike] = []
        self._last_pre: dict[tuple[int, int], int] = {}
        self._last_post: dict[int, int] = {}

    def reset(self, *, reset_weights: bool = False) -> None:
        """Clear queued events and neuron state; optionally restore synapses."""
        for neuron in self.neurons.values():
            neuron.reset_state()
        if reset_weights:
            self.connections = dict(self._initial_connections)
        self._queue.clear()
        self._sequence = 0
        self.max_queue_depth = 0
        self.time = 0
        self.emitted.clear()
        self.delivered.clear()
        self._last_pre.clear()
        self._last_post.clear()

    def inject(self, spikes: Iterable[AERSpike]) -> None:
        """Queue external input events without advancing the scheduler."""
        for spike in spikes:
            if spike.target not in self.neurons:
                raise ValueError(f"unknown spike target {spike.target}")
            if spike.timestamp < self.time:
                raise ValueError("cannot inject an event in the past")
            self._push(spike)

    def ingest(self, spikes: Iterable[AERSpike], *, policy=None) -> None:
        """Admit and queue a raw spike batch under an ingress policy."""
        from .soliton_admission import AdmissionPolicy, admit_spikes
        admitted = admit_spikes(spikes, current_time=self.time,
                                policy=policy or AdmissionPolicy(),
                                pending_events=len(self._queue))
        self.inject(admitted)

    def ingest_framed(self, text: str, *, start_sequence: int = 0,
                      policy=None) -> None:
        """Verify checksummed frames, then admit the decoded spike batch."""
        from .soliton_framing import decode_frames
        self.ingest(decode_frames(text, start_sequence=start_sequence), policy=policy)

    def _push(self, spike: AERSpike) -> None:
        self._sequence += 1
        heapq.heappush(self._queue, (spike.timestamp, self._sequence, spike))
        self.max_queue_depth = max(self.max_queue_depth, len(self._queue))

    def _update_stdp_pre(self, spike: AERSpike) -> None:
        if not self.stdp:
            return
        key = (spike.source, spike.target)
        self._last_pre[key] = spike.timestamp
        connection = self.connections.get(key)
        last_post = self._last_post.get(spike.target)
        if connection and last_post is not None and last_post < spike.timestamp:
            delta = -self.a_minus * exp(-(spike.timestamp - last_post) / self.stdp_tau)
            self.connections[key] = replace(connection, weight=connection.weight + delta)

    def _update_stdp_post(self, neuron: int, timestamp: int) -> None:
        if not self.stdp:
            return
        self._last_post[neuron] = timestamp
        for key, connection in tuple(self.connections.items()):
            if connection.target != neuron:
                continue
            last_pre = self._last_pre.get(key)
            if last_pre is not None and last_pre <= timestamp:
                delta = self.a_plus * exp(-(timestamp - last_pre) / self.stdp_tau)
                self.connections[key] = replace(connection, weight=connection.weight + delta)

    def run(self, *, until: int | None = None, max_events: int = 100_000) -> list[AERSpike]:
        """Consume events in timestamp/arrival order and route emitted spikes."""
        if until is not None and until < self.time:
            raise ValueError("until cannot precede current time")
        if max_events < 1:
            raise ValueError("max_events must be positive")
        processed = 0
        while self._queue:
            timestamp, _, spike = self._queue[0]
            if until is not None and timestamp > until:
                break
            heapq.heappop(self._queue)
            self.time = timestamp
            processed += 1
            if processed > max_events:
                raise RuntimeError("event budget exceeded; possible runaway recurrent activity")
            self.delivered.append(spike)
            self._update_stdp_pre(spike)
            neuron = self.neurons[spike.target]
            connection = self.connections.get((spike.source, spike.target))
            # External AER payload is the event amplitude; an unconnected
            # injection therefore has unit synaptic gain and must not multiply
            # the payload a second time.
            weight = connection.weight if connection else 1.0
            emitted = neuron.receive(spike, weight)
            if emitted is None:
                continue
            self.emitted.append(emitted)
            self._update_stdp_post(neuron.address, timestamp)
            for outgoing in self.connections.values():
                if outgoing.source == neuron.address:
                    self._push(AERSpike(timestamp + outgoing.delay, neuron.address,
                                        outgoing.target, emitted.polarity,
                                        emitted.payload, emitted.channel))
        return list(self.emitted)

    def weights(self) -> dict[tuple[int, int], float]:
        return {key: connection.weight for key, connection in self.connections.items()}


def temporal_xor_spikes() -> tuple[list[AERSpike], list[AERSpike]]:
    """Small causal fixture: two input spikes drive a downstream neuron."""
    return ([AERSpike(0, 0, 2), AERSpike(3, 1, 2)],
            [AERSpike(1, 2, 3), AERSpike(4, 2, 3)])


def trace_digest(spikes: Iterable[AERSpike]) -> str:
    """Return a stable SHA-256 digest of a canonical ordered spike trace."""
    payload = encode_spike_stream(spikes).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
