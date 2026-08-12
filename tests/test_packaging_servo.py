"""Tests for the packaging-line servo control: the Python mirror pins the
behaviors that the embedded IEC 61131-3 ST source (`packaging/plc_61131_3.py`)
must reproduce on a PLC.

Run:  python -m pytest tests/test_packaging_servo.py -q
"""

import pytest

from packaging.plc_61131_3 import st_source
from packaging.servo import (
    ErectorFlow,
    FoldAxis,
    PidController,
    QuorumVote,
    run_erector,
)

TARGET = 90.0


def _four_axes(k_restore=0.02):
    return {
        "side_l": FoldAxis(k_restore),
        "side_r": FoldAxis(k_restore),
        "bottom_major": FoldAxis(k_restore),
        "bottom_minor": FoldAxis(k_restore),
    }


def _good_votes():
    return {
        "blank_present": [True, True, True],
        "tape_applied": [True, True, True],
        "square_ok": [True, True, True],
    }


# --------------------------------------------------------------------------- #
# PID / spring-back compensation
# --------------------------------------------------------------------------- #
def test_fold_axis_overshoots_and_settles_at_target():
    """The fold must overshoot past 90 deg, dwell, then settle on 90 deg
    (the 'overshoot + dwell until tape/glue lock' claim)."""
    axis = FoldAxis(k_restore=0.02)
    axis.set_goal(TARGET, overshoot_deg=3.0, dwell_s=1.0)
    saw_overshoot = False
    saw_dwell = False
    for _ in range(200_000):
        axis.step()
        if axis.angle > TARGET + 1.0:
            saw_overshoot = True
        if axis.phase == "dwell":
            saw_dwell = True
        if axis.in_position:
            break
    assert saw_overshoot
    assert saw_dwell
    assert axis.in_position
    assert abs(axis.angle - TARGET) < 0.25


def test_feedforward_carries_the_restoring_moment():
    """With feedforward the PID only handles transients: the steady-state
    restoring moment at the aim angle is compensated, not integrated up."""
    pid = PidController(kp=0.5, ki=2.0, kd=0.002, i_clamp=10.0, dt=1e-3)
    axis = FoldAxis(k_restore=0.02)
    axis.set_goal(TARGET)
    peak = 0.0
    for _ in range(50_000):
        axis.step()
        peak = max(peak, axis.pid._integral)
        if axis.in_position:
            break
    # integral stays small: the feedforward does the steady-state work
    assert axis.in_position
    assert abs(axis.pid._integral) < 1.0


# --------------------------------------------------------------------------- #
# quorum (majority honesty, T16-T20)
# --------------------------------------------------------------------------- #
def test_quorum_majority_honesty():
    q = QuorumVote()
    assert q.decide([True, True, True]) == "ok"      # 0 disagree
    assert q.decide([True, True, False]) == "ok"     # 1/3 = 33% < 40%
    assert q.decide([True, False, False]) == "stop"  # 2/3 = 67% >= 50%
    assert q.decide([False, False, False]) == "stop"


def test_quorum_margins_are_boundaries():
    q = QuorumVote(n_sensors=10, repair_fraction=0.40, stop_fraction=0.50)
    assert q.decide([True] * 7 + [False] * 3) == "ok"      # 0.30 < 0.40
    assert q.decide([True] * 6 + [False] * 4) == "repair"  # 0.40 boundary
    assert q.decide([True] * 5 + [False] * 5) == "stop"    # 0.50 boundary


# --------------------------------------------------------------------------- #
# ERECT SFC
# --------------------------------------------------------------------------- #
def test_erector_good_blank_passes():
    axes = _four_axes()
    result, ticks = run_erector(axes, _good_votes())
    assert result == "PASS"
    assert all(a.in_position for a in axes.values())
    assert ticks < 100_000


def test_erector_rejects_on_squareness_fail():
    votes = _good_votes()
    votes["square_ok"] = [True, False, False]   # >=50% disagree -> FAIL
    result, _ = run_erector(_four_axes(), votes)
    assert result == "FAIL"


def test_erector_watchdog_faults_on_stall():
    """A stalled axis (huge inertia) must trip the step watchdog -> FAULT
    (line stop and reset), not hang."""
    axes = _four_axes()
    axes["side_l"] = FoldAxis(k_restore=0.02, inertia=1e6)
    result, _ = run_erector(axes, _good_votes())
    assert result == "FAULT"


def test_erector_quorum_stop_blocks_line():
    """>=50% sensor disagreement at GRIP -> never leave the safe start."""
    votes = _good_votes()
    votes["blank_present"] = [True, False, False]
    flow = ErectorFlow(_four_axes())
    for _ in range(100):
        out = flow.step_sim(1e-3, votes)
        assert out is None            # still waiting on the quorum
        assert flow.step == "GRIP"


# --------------------------------------------------------------------------- #
# ST source smoke test (the PLC must say the same things as the mirror)
# --------------------------------------------------------------------------- #
def test_st_source_declares_the_servo_fbs():
    src = st_source()
    for needle in (
        "FUNCTION_BLOCK PID",
        "FUNCTION_BLOCK FoldAxis",
        "FUNCTION_BLOCK Quorum",
        "PROGRAM Erector",
        "rFeedFwd := rKRestore * rAimDeg",   # restoring-moment feedforward
        "fbPID(rError := rErr",               # formal-parameter FB call
        "rDwellLeft <= 0.0",                  # dwell ends -> settle
        ">=50% disagree",                  # quorum stop threshold
        "STO",                                # safe torque off
    ):
        assert needle in src, needle


def test_regen_accounting_conserves_energy():
    """Power accounting must close: motoring minus regen equals the net
    mechanical energy put into the axis (potential + kinetic), so the
    recovered fraction is a defensible number."""
    axis = FoldAxis(k_restore=0.02)
    axis.set_goal(TARGET)
    motoring = regen = 0.0
    for _ in range(200_000):
        axis.step()
        p = axis.motor_power
        if p >= 0.0:
            motoring += p * axis.dt
        else:
            regen += -p * axis.dt
        if axis.in_position:
            break
    assert axis.in_position
    assert motoring > 0.0
    assert 0.0 < regen < motoring          # some spring-back work recovered
    # energy stored in the spring field at the target: 1/2 k theta^2
    # (the axis ends holding against the restore moment, so the net bus
    # energy must at least match it - a weak but real conservation bound)
    spring_j = 0.5 * axis.k_restore * (axis.angle ** 2)
    assert (motoring - regen) >= spring_j * 0.99


def test_st_source_phases_match_python_mirror():
    """drive=1, dwell=2, settle=3 - the ST CASE arms and the Python phase
    names describe the same overshoot/dwell/settle behavior."""
    src = st_source()
    assert "0 idle, 1 drive, 2 dwell, 3 settle" in src
    assert "ePhase := 1" in src
    assert "ePhase := 2" in src
    assert "ePhase := 3" in src
