"""Fold servo control for the autonomous packaging line (Python mirror).

This module is the *testable* mirror of `packaging/plc_61131_3.py`, which
carries the IEC 61131-3:2025 ST source that would run in a real PLC. The
physics is deliberately classical and schematic-level:

  J*theta'' + b*theta'  =  tau_motor - tau_restore(theta)

with tau_restore = k_restore*theta the spring-back restoring moment of the
folded panel (measured per blank lot, never assumed - the L.O.R.E. doctrine).
The servo drives the arm past 90 deg, dwells while the tape/glue lock sets,
then settles back to the square 90 deg target.

Supporting logic mirrors the design doc `docs/AUTO_PACKAGING_SYSTEM.md`:
  * QuorumVote  - 3-sensor majority honesty (T16-T20): <40% disagreement
                  continues, >=50% stops the line.
  * ErectorFlow - the ERECT SFC: grip -> fold sides -> majors -> minors ->
                  tape bottom -> raise -> verify square, with per-step
                  watchdogs that fault the line on stall.
"""

from __future__ import annotations

import math

# --------------------------------------------------------------------------- #
# servo loop
# --------------------------------------------------------------------------- #
class PidController:
    """Discrete PID with clamped integral (anti-windup).

    Conditional integration: the integral integrates only while the error is
    inside `integrate_band`. The fold's steady state is carried by the
    restoring-torque *feedforward*; the integral's only job is to null the
    residual error, so it must never wind up across the large drive transient.
    """

    def __init__(self, kp, ki, kd, i_clamp, dt, integrate_band=1.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.i_clamp = i_clamp
        self.integrate_band = integrate_band
        self.dt = dt
        self._integral = 0.0
        self._prev_error = 0.0
        self._first = True

    def step(self, error):
        if abs(error) < self.integrate_band:
            self._integral += self.ki * error * self.dt
            self._integral = max(-self.i_clamp, min(self.i_clamp, self._integral))
        deriv = 0.0 if self._first else (error - self._prev_error) / self.dt
        self._first = False
        self._prev_error = error
        return self.kp * error + self._integral + self.kd * deriv

    def reset(self):
        self._integral = 0.0
        self._first = True


class FoldAxis:
    """One fold arm: PID + restoring-torque feedforward + 2nd-order plant.

    Phases per fold:
      drive  -> accelerate to target+overshoot
      dwell  -> hold past 90 deg for the tape/glue lock (fixed duration)
      settle -> relax back to the square 90 deg target
    Feedforward always compensates the restoring moment at the *current aim*
    angle, so the PID only handles the transient error.
    """

    def __init__(self, k_restore, inertia=0.01, damping=0.05, dt=1e-3,
                 kp=0.5, ki=0.5, kd=0.002, i_clamp=2.0):
        self.k_restore = k_restore          # N*m per degree of fold (per-lot, measured)
        self.inertia = inertia              # J, kg*m^2
        self.damping = damping              # b, N*m*s/deg
        self.dt = dt
        self.angle = 0.0                    # deg
        self.omega = 0.0                    # deg/s
        self.pid = PidController(kp, ki, kd, i_clamp, dt)
        self._phase = "idle"
        self._aim = 0.0
        self._target = 0.0
        self._dwell_left = 0.0
        self.in_position = False

    def set_goal(self, target_deg, overshoot_deg=3.0, dwell_s=1.0):
        self._target = target_deg
        self._overshoot = overshoot_deg
        self._dwell = dwell_s
        self._phase = "drive"
        self._dwell_left = 0.0
        self.in_position = False
        self.pid.reset()

    @property
    def phase(self):
        return self._phase

    def step(self):
        if self._phase == "idle":
            return
        tol = 0.25
        if self._phase == "drive":
            self._aim = self._target + self._overshoot
            if abs(self.angle - self._aim) < tol:
                self._phase = "dwell"
                self._dwell_left = self._dwell
        elif self._phase == "dwell":
            self._aim = self._target + self._overshoot
            self._dwell_left -= self.dt
            if self._dwell_left <= 0.0:
                self._phase = "settle"
                self._aim = self._target
        elif self._phase == "settle":
            self._aim = self._target
            if (abs(self.angle - self._target) < tol
                    and abs(self.omega) < 0.5):
                self.in_position = True

        error = self._aim - self.angle
        feedforward = self.k_restore * self._aim
        torque = self.pid.step(error) + feedforward
        self._integrate(torque)

    def _integrate(self, torque):
        acc = (torque - self.k_restore * self.angle
               - self.damping * self.omega) / self.inertia
        self.omega += acc * self.dt
        self.angle += self.omega * self.dt


# --------------------------------------------------------------------------- #
# quorum (fragment-bank majority honesty, T16-T20)
# --------------------------------------------------------------------------- #
class QuorumVote:
    """Three independent sensors on one check.

    disagree/n >= stop_fraction -> 'stop' (line stop and reset)
    otherwise                   -> 'ok'  (continue; margin < 40%)
    """

    def __init__(self, n_sensors=3, repair_fraction=0.40, stop_fraction=0.50):
        self.n = n_sensors
        self.repair_fraction = repair_fraction
        self.stop_fraction = stop_fraction

    def decide(self, votes):
        disagree = self.n - sum(1 for v in votes if v)
        frac = disagree / float(self.n)
        if frac >= self.stop_fraction:
            return "stop"
        if frac >= self.repair_fraction:
            return "repair"
        return "ok"


# --------------------------------------------------------------------------- #
# ERECT SFC (mirrors the ST CASE machine in plc_61131_3.py)
# --------------------------------------------------------------------------- #
STEPS = [
    "GRIP",
    "FOLD_SIDES",
    "FOLD_MAJORS",
    "FOLD_MINORS",
    "TAPE_BOTTOM",
    "RAISE",
    "VERIFY",
]

TARGET = 90.0


class ErectorFlow:
    """The station-2 erector step machine with per-step watchdogs.

    Returns one of: 'PASS', 'FAIL' (reject lane), 'FAULT' (line stop/reset).
    """

    def __init__(self, axes, step_timeout=8.0, quorum=QuorumVote()):
        self.axes = axes              # dict name -> FoldAxis
        self.quorum = quorum
        self.step_timeout = step_timeout
        self.step_index = 0
        self.elapsed = 0.0
        self.result = None

    @property
    def step(self):
        return STEPS[self.step_index]

    def verify(self, blank):
        """blank: dict of sensor names -> list of 3 sensor votes."""
        return blank

    def step_sim(self, dt, sensor_votes):
        """Advance the machine one control tick.

        sensor_votes: {'blank_present': [b,b,b], 'tape_applied': [..],
                       'square_ok': [..]} - lists of len quorum.n.
        """
        if self.result is not None:
            return self.result
        self.elapsed += dt
        name = STEPS[self.step_index]

        if self.elapsed > self.step_timeout:
            self.result = "FAULT"
            return self.result

        if name == "GRIP":
            if self.quorum.decide(sensor_votes["blank_present"]) == "ok":
                for axis in self.axes.values():
                    axis.set_goal(TARGET)
                self._advance()
        elif name in ("FOLD_SIDES", "FOLD_MAJORS", "FOLD_MINORS"):
            for axis in self.axes.values():
                axis.step()
            folded = [a.in_position for a in self.axes.values()]
            if all(folded):
                self._advance()
        elif name == "TAPE_BOTTOM":
            for axis in self.axes.values():
                axis.step()
            if self.quorum.decide(sensor_votes["tape_applied"]) == "ok":
                self._advance()
        elif name == "RAISE":
            if self.elapsed >= 1.0:
                self._advance()
        elif name == "VERIFY":
            if self.quorum.decide(sensor_votes["square_ok"]) != "ok":
                self.result = "FAIL"
            else:
                self.result = "PASS"
        return self.result

    def _advance(self):
        self.step_index += 1
        self.elapsed = 0.0
        if self.step_index >= len(STEPS):
            self.result = "FAULT"


def run_erector(axes, sensor_votes, dt=1e-3):
    """Run a full erector cycle to completion. Returns (result, ticks)."""
    flow = ErectorFlow(axes)
    ticks = 0
    while flow.result is None:
        flow.step_sim(dt, sensor_votes)
        ticks += 1
        if ticks > 100_000:
            flow.result = "FAULT"
            break
    return flow.result, ticks
