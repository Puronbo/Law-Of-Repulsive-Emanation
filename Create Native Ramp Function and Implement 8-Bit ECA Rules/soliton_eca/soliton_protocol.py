"""Discrete soliton packet protocol and verified routing primitives.

This module is the executable reference for the proposed bus architecture:
packets are localized, timestamped, signed scalar events and routing is a pure
state transition that can later be mapped to optical or neuromorphic hardware.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True, order=True)
class Packet:
    """A localized soliton-like packet on a 1-D discrete bus."""
    tick: int
    position: int
    velocity: int
    amplitude: float
    channel: str = "data"
    phase: int = 0

    def advance(self, *, length: int, boundary: str = "reflect") -> "Packet | None":
        """Advance one tick with explicit boundary behavior."""
        if self.velocity not in (-1, 1):
            raise ValueError("velocity must be -1 or +1")
        position = self.position + self.velocity
        velocity = self.velocity
        if 0 <= position < length:
            return Packet(self.tick + 1, position, velocity, self.amplitude,
                          self.channel, self.phase)
        if boundary == "annihilate":
            return None
        if boundary != "reflect":
            raise ValueError("boundary must be 'reflect' or 'annihilate'")
        position = 0 if position < 0 else length - 1
        return Packet(self.tick + 1, position, -velocity, self.amplitude,
                      self.channel, self.phase)


def collision(a: Packet, b: Packet, *, mode: str = "xor") -> Packet | None:
    """Resolve a same-site/same-tick collision.

    ``xor`` is a reversible bit-level annihilation rule for unit amplitudes;
    ``sum`` conserves signed amplitude; ``cancel`` models destructive
    interference. Different channels are rejected to avoid silent mixing.
    """
    if (a.tick, a.position) != (b.tick, b.position):
        raise ValueError("packets must collide at the same tick and position")
    if a.channel != b.channel:
        raise ValueError("cross-channel collision requires an explicit coupler")
    if mode == "xor":
        value = float((int(bool(a.amplitude)) ^ int(bool(b.amplitude))))
    elif mode == "sum":
        value = a.amplitude + b.amplitude
    elif mode == "cancel":
        value = a.amplitude - b.amplitude
    else:
        raise ValueError("mode must be 'xor', 'sum', or 'cancel'")
    if value == 0:
        return None
    return Packet(a.tick, a.position, a.velocity, value, a.channel,
                  (a.phase + b.phase) % 2)


class SolitonLattice:
    """Synchronous packet bus with collision detection and event logging."""
    def __init__(self, length: int, *, boundary: str = "reflect"):
        if length < 2:
            raise ValueError("length must be at least 2")
        if boundary not in ("reflect", "annihilate"):
            raise ValueError("boundary must be 'reflect' or 'annihilate'")
        self.length = length
        self.boundary = boundary
        self.tick = 0
        self.packets: tuple[Packet, ...] = ()
        self.log: list[tuple[int, str, int]] = []

    def inject(self, packets: Iterable[Packet]) -> None:
        incoming = tuple(packets)
        if any(p.tick != self.tick for p in incoming):
            raise ValueError("injected packet tick must equal lattice tick")
        if any(not 0 <= p.position < self.length for p in incoming):
            raise ValueError("packet position outside lattice")
        self.packets = self.packets + incoming

    def step(self, *, collision_mode: str = "xor") -> tuple[Packet, ...]:
        """Advance all packets, then resolve same-position collisions."""
        if collision_mode not in ("xor", "sum", "cancel"):
            raise ValueError("mode must be 'xor', 'sum', or 'cancel'")
        advanced = [p.advance(length=self.length, boundary=self.boundary)
                    for p in self.packets]
        grouped: dict[tuple[int, int, str], list[Packet]] = {}
        for packet in advanced:
            if packet is not None:
                grouped.setdefault((packet.tick, packet.position, packet.channel), []).append(packet)
        next_packets: list[Packet] = []
        for key, group in sorted(grouped.items()):
            result = group[0]
            for other in group[1:]:
                result = None if result is None else collision(result, other, mode=collision_mode)
            if result is not None:
                next_packets.append(result)
            self.log.append((key[0], key[1], len(group)))
        self.tick += 1
        self.packets = tuple(next_packets)
        return self.packets

    def run(self, ticks: int, *, collision_mode: str = "xor") -> list[tuple[Packet, ...]]:
        if ticks < 0:
            raise ValueError("ticks must be non-negative")
        return [self.step(collision_mode=collision_mode) for _ in range(ticks)]


def reversible_pair(length: int, position: int, amplitude: float = 1.0) -> tuple[Packet, Packet]:
    """Create equal/opposite packets useful for collision and boundary tests."""
    if not 0 < position < length - 1:
        raise ValueError("position must leave room on both sides")
    return (Packet(0, position, -1, amplitude),
            Packet(0, position, 1, amplitude))
