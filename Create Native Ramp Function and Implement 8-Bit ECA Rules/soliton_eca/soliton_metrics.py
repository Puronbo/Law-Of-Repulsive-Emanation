"""Observability and deterministic stress utilities for the soliton SNN."""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable

from .soliton_snn import AERSpike, SolitonSNN


@dataclass(frozen=True, slots=True)
class SNNMetrics:
    delivered_events: int
    emitted_spikes: int
    max_queue_depth: int
    current_time: int
    firing_rate_per_tick: float
    min_weight: float | None
    max_weight: float | None


def metrics(network: SolitonSNN) -> SNNMetrics:
    """Snapshot scheduler and synapse metrics without mutating state."""
    weights = list(network.weights().values())
    rate = len(network.emitted) / max(network.time + 1, 1)
    return SNNMetrics(len(network.delivered), len(network.emitted),
                      network.max_queue_depth, network.time, rate,
                      min(weights) if weights else None,
                      max(weights) if weights else None)


def validate_spike_trace(spikes: Iterable[AERSpike]) -> int:
    """Validate basic trace invariants and return its event count."""
    count = 0
    previous = -1
    for spike in spikes:
        if spike.timestamp < previous or not isfinite(spike.payload):
            raise ValueError("trace is unordered or contains a non-finite payload")
        previous = spike.timestamp
        count += 1
    return count
