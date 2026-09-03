"""Safe simulated embodiment for the soliton cognitive runtime."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from math import hypot, isfinite

from .cognitive_agent import Fact, Observation


@dataclass(frozen=True, slots=True)
class BodyState:
    x: float = 0.0
    y: float = 0.0
    battery: float = 1.0
    tick: int = 0


@dataclass(frozen=True, slots=True)
class ActuatorEvent:
    tick: int
    command: str
    dx: float
    dy: float
    accepted: bool
    reason: str
    state: BodyState


class SimulatedBody:
    """2-D bounded body; it has no real hardware or external side effects."""
    def __init__(self, *, bounds: tuple[float, float, float, float] = (-10.0, 10.0, -10.0, 10.0),
                 max_speed: float = 1.0, energy_per_unit: float = 0.05,
                 initial: BodyState = BodyState()):
        if len(bounds) != 4 or bounds[0] >= bounds[1] or bounds[2] >= bounds[3]:
            raise ValueError("bounds must be (xmin, xmax, ymin, ymax)")
        if not isfinite(max_speed) or max_speed <= 0 or not isfinite(energy_per_unit) or energy_per_unit < 0:
            raise ValueError("max_speed positive and energy_per_unit non-negative")
        if not all(isfinite(v) for v in (initial.x, initial.y, initial.battery)) or initial.battery < 0:
            raise ValueError("initial body state must be finite with non-negative battery")
        if not (bounds[0] <= initial.x <= bounds[1] and bounds[2] <= initial.y <= bounds[3]):
            raise ValueError("initial position outside bounds")
        self.bounds = tuple(float(v) for v in bounds)
        self.max_speed, self.energy_per_unit = float(max_speed), float(energy_per_unit)
        self.state = initial
        self.events: list[ActuatorEvent] = []

    def actuate(self, command: str, dx: float, dy: float, *, tick: int | None = None) -> ActuatorEvent:
        """Apply one bounded movement command; rejected commands do not mutate state."""
        if not command:
            raise ValueError("command must be non-empty")
        if not all(isfinite(v) for v in (dx, dy)):
            raise ValueError("actuator deltas must be finite")
        tick = self.state.tick if tick is None else tick
        if tick < self.state.tick:
            raise ValueError("body tick cannot move backwards")
        distance = hypot(dx, dy)
        reason = "accepted"
        accepted = True
        if distance > self.max_speed:
            accepted, reason = False, "speed limit exceeded"
        nx, ny = self.state.x + dx, self.state.y + dy
        if accepted and not (self.bounds[0] <= nx <= self.bounds[1] and self.bounds[2] <= ny <= self.bounds[3]):
            accepted, reason = False, "boundary collision"
        cost = distance * self.energy_per_unit
        if accepted and cost > self.state.battery:
            accepted, reason = False, "insufficient battery"
        if accepted:
            self.state = BodyState(nx, ny, self.state.battery - cost, tick)
        else:
            self.state = BodyState(self.state.x, self.state.y, self.state.battery, tick)
        event = ActuatorEvent(tick, command, float(dx), float(dy), accepted, reason, self.state)
        self.events.append(event)
        return event

    def sense(self, *, timestamp: int | None = None, salience: float = 1.0) -> Observation:
        """Ground body state into explicit symbolic sensor facts."""
        timestamp = self.state.tick if timestamp is None else timestamp
        if timestamp < self.state.tick:
            raise ValueError("sensor timestamp cannot precede body tick")
        x, y, battery = self.state.x, self.state.y, self.state.battery
        horizontal = "right" if x > 0 else "left" if x < 0 else "center"
        vertical = "up" if y > 0 else "down" if y < 0 else "center"
        level = "empty" if battery <= 0 else "low" if battery < 0.2 else "charged"
        return Observation(timestamp, frozenset({
            Fact("body_x", f"{x:.6g}"), Fact("body_y", f"{y:.6g}"),
            Fact("horizontal", horizontal), Fact("vertical", vertical),
            Fact("battery", level),
        }), salience)

    def snapshot(self) -> dict[str, object]:
        return {"state": asdict(self.state), "events": len(self.events),
                "bounds": list(self.bounds), "max_speed": self.max_speed,
                "energy_per_unit": self.energy_per_unit}
