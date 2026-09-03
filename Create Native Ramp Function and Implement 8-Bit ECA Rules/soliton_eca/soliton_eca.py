"""Elementary cellular automata implemented as a soliton-bus network.

A soliton is a localized, immutable message.  Buses carry solitons between
cells; cells consume the three-neighbor frame and emit the next-cell state.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Iterable, Iterator, Sequence


def ramp(x: int | float) -> int | float:
    """Positive native ramp: x for x > 0, otherwise 0.

    The comparison is deliberately part of the primitive rather than using a
    max/min helper, which makes the intended hardware/dataflow form explicit:
    ``x * (x > 0)``.
    """
    return x * (x > 0)


def negative_ramp(x: int | float) -> int | float:
    """Negative native ramp: x for x < 0, otherwise 0: ``x * (x < 0)``."""
    return x * (x < 0)


# The requested rule family.  Values are keyed by the 3-bit neighborhood
# encoded as (left << 2) | (center << 1) | right, i.e. 111 ... 000.
RULES = (4, 12, 36, 44, 68, 76, 100, 108,
         132, 140, 164, 172, 196, 204, 228, 236)


@dataclass(frozen=True, slots=True)
class Soliton:
    """A localized value travelling on a named bus."""
    bus: str
    position: int
    value: int
    generation: int


class SolitonBus:
    """FIFO transport for localized messages."""
    def __init__(self) -> None:
        self._queue: Deque[Soliton] = deque()

    def send(self, soliton: Soliton) -> None:
        self._queue.append(soliton)

    def receive(self) -> Soliton:
        return self._queue.popleft()

    def peek(self) -> Soliton:
        """Inspect the next soliton without consuming it."""
        if not self._queue:
            raise IndexError("cannot peek an empty soliton bus")
        return self._queue[0]

    def __len__(self) -> int:
        return len(self._queue)


class EcaCell:
    """One cell node. It computes only after a complete neighborhood arrives."""
    def __init__(self, index: int, rule: int, output: SolitonBus) -> None:
        self.index = index
        self.rule = rule
        self.output = output
        self._frame: dict[int, int] = {}

    def accept(self, soliton: Soliton) -> None:
        self._frame[soliton.position] = 1 if soliton.value else 0
        if len(self._frame) == 3:
            left = self._frame[self.index - 1]
            center = self._frame[self.index]
            right = self._frame[self.index + 1]
            neighborhood = (left << 2) | (center << 1) | right
            value = (self.rule >> neighborhood) & 1
            self.output.send(Soliton("state", self.index, value,
                                     soliton.generation))
            self._frame.clear()


class SolitonECA:
    """Finite, synchronous ECA whose transport and computation use solitons.

    Boundary cells use zero-valued ghost solitons. ``step`` is synchronous:
    all input state solitons are injected first, then every cell emits one
    output soliton, preserving the cellular-automaton update semantics.
    """
    def __init__(self, rule: int, width: int, initial: Iterable[int] | None = None):
        if rule not in RULES:
            raise ValueError(f"rule must be one of {RULES}, got {rule}")
        if width < 1:
            raise ValueError("width must be positive")
        self.rule, self.width, self.generation = rule, width, 0
        bits = list(initial) if initial is not None else [0] * width
        if len(bits) != width or any(bit not in (0, 1) for bit in bits):
            raise ValueError("initial must contain exactly width binary values")
        self.state = bits
        self._cells = [EcaCell(i, rule, SolitonBus()) for i in range(width)]

    @staticmethod
    def apply_rule(rule: int, left: int, center: int, right: int) -> int:
        if rule not in RULES:
            raise ValueError(f"rule must be one of {RULES}, got {rule}")
        neighborhood = (left << 2) | (center << 1) | right
        return (rule >> neighborhood) & 1

    def step(self) -> tuple[int, ...]:
        generation = self.generation + 1
        buses = [SolitonBus() for _ in range(self.width)]
        # Each cell has its own local input bus. A neighborhood frame is
        # fanned out as three solitons; this is the bus-level synchronizer.
        for i, cell in enumerate(self._cells):
            cell.output = buses[i]
        for i, cell in enumerate(self._cells):
            for position in (i - 1, i, i + 1):
                value = self.state[position] if 0 <= position < self.width else 0
                cell.accept(Soliton("neighborhood", position, value, generation))
        self.state = [buses[i].receive().value for i in range(self.width)]
        self.generation = generation
        return tuple(self.state)

    def run(self, generations: int) -> Iterator[tuple[int, ...]]:
        if generations < 0:
            raise ValueError("generations must be non-negative")
        for _ in range(generations):
            yield self.step()

    def diagram(self, generations: int) -> str:
        """Render the initial state and subsequent bus generations."""
        rows = ["".join("█" if x else "·" for x in self.state)]
        rows.extend("".join("█" if x else "·" for x in state)
                    for state in self.run(generations))
        return "\n".join(rows)


def evolve(rule: int, initial: Sequence[int], generations: int) -> list[tuple[int, ...]]:
    """Convenience API returning each emitted soliton-bus state."""
    return list(SolitonECA(rule, len(initial), initial).run(generations))
