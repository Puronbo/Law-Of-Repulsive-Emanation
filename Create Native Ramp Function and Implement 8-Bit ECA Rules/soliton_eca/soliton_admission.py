"""Ingress admission policy for the soliton AER SNN endpoint."""
from __future__ import annotations

from dataclasses import dataclass
from collections import Counter
from typing import Iterable

from .soliton_snn import AERSpike


@dataclass(frozen=True, slots=True)
class AdmissionPolicy:
    """Bounds applied before events enter the scheduler."""
    allowed_channels: frozenset[str] = frozenset({"spike", "signed"})
    max_payload: float = 1.0
    max_future_ticks: int = 10_000
    max_events: int = 100_000
    max_events_per_timestamp: int = 10_000
    max_pending_events: int = 100_000

    def __post_init__(self) -> None:
        if not self.allowed_channels:
            raise ValueError("at least one channel must be allowed")
        if self.max_payload <= 0 or self.max_future_ticks < 0:
            raise ValueError("payload and future horizon bounds must be positive/non-negative")
        if self.max_events < 1 or self.max_events_per_timestamp < 1:
            raise ValueError("event limits must be positive")
        if self.max_pending_events < 1:
            raise ValueError("max_pending_events must be positive")


def admit_spikes(spikes: Iterable[AERSpike], *, current_time: int = 0,
                 policy: AdmissionPolicy = AdmissionPolicy(),
                 pending_events: int = 0) -> tuple[AERSpike, ...]:
    """Validate a finite batch before scheduler admission.

    Admission is atomic: no caller-visible partial result is returned when any
    event violates policy. Input order is preserved for deterministic replay.
    """
    if current_time < 0:
        raise ValueError("current_time must be non-negative")
    if pending_events < 0:
        raise ValueError("pending_events must be non-negative")
    batch = tuple(spikes)
    if len(batch) > policy.max_events:
        raise ValueError("event batch exceeds admission limit")
    if pending_events + len(batch) > policy.max_pending_events:
        raise ValueError("pending event capacity exceeded")
    counts = Counter(spike.timestamp for spike in batch)
    if max(counts.values(), default=0) > policy.max_events_per_timestamp:
        raise ValueError("timestamp burst exceeds admission limit")
    previous = current_time
    for spike in batch:
        if spike.channel not in policy.allowed_channels:
            raise ValueError(f"channel {spike.channel!r} is not admitted")
        if spike.timestamp < current_time:
            raise ValueError("event timestamp precedes admission time")
        if spike.timestamp > current_time + policy.max_future_ticks:
            raise ValueError("event exceeds admission time horizon")
        if spike.payload > policy.max_payload:
            raise ValueError("event payload exceeds admission limit")
        if spike.timestamp < previous:
            raise ValueError("admission batch must be timestamp ordered")
        previous = spike.timestamp
    return batch
