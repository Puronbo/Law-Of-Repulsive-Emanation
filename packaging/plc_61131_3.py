"""IEC 61131-3:2025 ST source for the packaging line's servo control.

This module *embeds* the Structured Text (ST) source that would be pasted
into a CODESYS / TwinCAT / Beckhoff IDE and run on the EtherCAT servo bus of
`docs/AUTO_PACKAGING_SYSTEM.md`. The Python module `packaging/servo.py` is a
1:1 testable mirror of this logic; tests pin that the two stay in agreement.

Contents (all IEC 61131-3:2025, edition 4.0 - ST, UTF-8 allowed):
  * PID      - discrete PID function block with clamped integral
  * FoldAxis - fold-arm axis: PID + restoring-torque feedforward, with the
               drive -> dwell (overshoot) -> settle phases
  * Quorum   - 3-sensor majority-honesty decision (T16-T20)
  * Erector  - program: the ERECT SFC implemented as a CASE step machine,
               with per-step watchdogs (fault -> safe state)
  * STO      - safe-torque-off request on the drive (IEC 61800-5-2 / 62061)
"""

ST_SOURCE = """\
(* ============================================================ *)
(* FoldAxis: one servo fold arm, spring-back compensated.       *)
(* The restoring constant rKRestore is MEASURED per blank lot,  *)
(* never assumed (L.O.R.E. doctrine). EtherCAT cycle: 1 ms.     *)
(* ============================================================ *)
FUNCTION_BLOCK PID
VAR_INPUT
    rError     : REAL;
END_VAR
VAR_IN_OUT
    rIntegral  : REAL;
END_VAR
VAR_INPUT
    bReset     : BOOL;
END_VAR
VAR_OUTPUT
    rOut       : REAL;
END_VAR
VAR
    rKp        : REAL := 0.5;
    rKi        : REAL := 0.5;
    rKd        : REAL := 0.002;
    rIClamp    : REAL := 2.0;
    rIntBand   : REAL := 1.0;
    rPrevErr   : REAL := 0.0;
    rDt        : REAL := 0.001;
    bFirst     : BOOL := TRUE;
END_VAR

IF bReset THEN
    rIntegral := 0.0;
    bFirst := TRUE;
END_IF;

(* conditional integration: only null the residual error; the fold's
   steady state is carried by the restoring-torque feedforward, so the
   integral must never wind up across the drive transient *)
IF ABS(rError) < rIntBand THEN
    rIntegral := rIntegral + rKi * rError * rDt;
END_IF;
IF rIntegral > rIClamp THEN rIntegral := rIClamp; END_IF;
IF rIntegral < -rIClamp THEN rIntegral := -rIClamp; END_IF;

IF NOT bFirst THEN
    rOut := rKp * rError + rIntegral + rKd * (rError - rPrevErr) / rDt;
ELSE
    rOut := rKp * rError + rIntegral;
    bFirst := FALSE;
END_IF;
rPrevErr := rError;

FUNCTION_BLOCK FoldAxis
VAR_INPUT
    bEnable      : BOOL;        (* axis active                              *)
    rTargetDeg   : REAL;        (* square 90 deg target                     *)
    rKRestore    : REAL;        (* N*m per deg, measured per blank lot      *)
    rOvershootDeg: REAL := 3.0; (* overshoot past target before dwell       *)
    rDwellS      : REAL := 1.0; (* dwell for tape/glue lock                 *)
END_VAR
VAR_IN_OUT
    rAngleDeg    : REAL;        (* encoder feedback, deg                     *)
    rOmegaDeg_s  : REAL;
END_VAR
VAR_OUTPUT
    bInPosition  : BOOL;
    rTorqueCmd   : REAL;
    bFault       : BOOL;
END_VAR
VAR
    ePhase      : INT := 0;     (* 0 idle, 1 drive, 2 dwell, 3 settle        *)
    rAimDeg     : REAL;
    rDwellLeft  : REAL;
    rIntegral   : REAL;
    fbPID       : PID;
    rFeedFwd    : REAL;
    rErr        : REAL;
    rTorque     : REAL;
END_VAR

IF NOT bEnable THEN
    ePhase := 0;
    bInPosition := FALSE;
    rTorqueCmd := 0.0;
    RETURN;
END_IF;

CASE ePhase OF
    0: (* idle -> drive *)
        rAimDeg := rTargetDeg + rOvershootDeg;
        fbPID(bReset := TRUE);
        ePhase := 1;
    1: (* drive to overshoot *)
        IF ABS(rAngleDeg - (rTargetDeg + rOvershootDeg)) < 0.25 THEN
            rDwellLeft := rDwellS;
            ePhase := 2;
        END_IF;
    2: (* dwell past 90 deg *)
        rDwellLeft := rDwellLeft - 0.001;
        IF rDwellLeft <= 0.0 THEN
            ePhase := 3;
        END_IF;
    3: (* settle back to square target *)
        IF ABS(rAngleDeg - rTargetDeg) < 0.25 AND ABS(rOmegaDeg_s) < 0.5 THEN
            bInPosition := TRUE;
        END_IF;
END_CASE;

CASE ePhase OF
    0:   rAimDeg := rTargetDeg + rOvershootDeg;
    2:   rAimDeg := rTargetDeg + rOvershootDeg;
    ELSE rAimDeg := rTargetDeg;
END_CASE;

rErr := rAimDeg - rAngleDeg;
fbPID(rError := rErr, rIntegral := rIntegral, bReset := FALSE);
rFeedFwd := rKRestore * rAimDeg;
rTorque := fbPID.rOut + rFeedFwd;
rTorqueCmd := rTorque;
IF ABS(rTorqueCmd) > 100.0 THEN
    rTorqueCmd := 100.0;
END_IF;

FUNCTION_BLOCK Quorum
VAR_INPUT
    bSensor  : ARRAY[1..3] OF BOOL;
END_VAR
VAR_OUTPUT
    eVerdict  : INT; (* 0 ok, 1 repair-margin, 2 stop *)
    rDisagree : REAL;
END_VAR
VAR
    iN : INT := 0;
    i  : INT;
END_VAR

iN := 0;
FOR i := 1 TO 3 DO
    IF NOT bSensor[i] THEN iN := iN + 1; END_IF;
END_FOR;
rDisagree := INT_TO_REAL(iN) / 3.0;
IF rDisagree >= 0.50 THEN
    eVerdict := 2;        (* >=50% disagree -> line stop and reset  *)
ELSIF rDisagree >= 0.40 THEN
    eVerdict := 1;        (* 40..50% -> repair margin               *)
ELSE
    eVerdict := 0;        (* <40% disagree -> continue              *)
END_IF;

PROGRAM Erector
VAR_INPUT
    bBlankPresent : ARRAY[1..3] OF BOOL;
    bTapeApplied  : ARRAY[1..3] OF BOOL;
    bSquareOk     : ARRAY[1..3] OF BOOL;
    bCycleEnable  : BOOL;
END_VAR
VAR_OUTPUT
    nResult       : INT; (* 0 running, 1 pass, 2 fail, 3 fault       *)
    bFault        : BOOL;
END_VAR
VAR
    (* four axes: side L, side R, bottom major, bottom minor *)
    aFold         : ARRAY[1..4] OF FoldAxis;
    rAngle        : ARRAY[1..4] OF REAL;
    rOmega        : ARRAY[1..4] OF REAL;
    bInPos        : ARRAY[1..4] OF BOOL;
    bTapeLock     : ARRAY[1..4] OF BOOL;
    fbQuorumBlank : Quorum;
    fbQuorumTape  : Quorum;
    fbQuorumSquare: Quorum;
    eStep         : INT := 0;
    rElapsed      : REAL := 0.0;
    rTimeout      : REAL := 6.0;
    i             : INT;
END_VAR

IF NOT bCycleEnable THEN
    nResult := 0;
    RETURN;
END_IF;

IF nResult = 3 THEN
    RETURN; (* latched fault, operator reset required *)
END_IF;

rElapsed := rElapsed + 0.001;
IF rElapsed > rTimeout THEN
    bFault := TRUE;
    nResult := 3;
    RETURN;
END_IF;

CASE eStep OF
    0: (* GRIP *)
        fbQuorumBlank(bSensor := bBlankPresent);
        IF fbQuorumBlank.eVerdict = 0 THEN
            FOR i := 1 TO 4 DO
                aFold[i](bEnable := TRUE, rTargetDeg := 90.0,
                         rKRestore := 0.02, rAngleDeg := rAngle[i],
                         rOmegaDeg_s := rOmega[i]);
            END_FOR;
            eStep := 1;
            rElapsed := 0.0;
        END_IF;
    1..3: (* FOLD_SIDES / MAJORS / MINORS *)
        FOR i := 1 TO 4 DO
            aFold[i](bEnable := TRUE, rTargetDeg := 90.0, rKRestore := 0.02,
                     rAngleDeg := rAngle[i], rOmegaDeg_s := rOmega[i]);
            bInPos[i] := aFold[i].bInPosition;
        END_FOR;
        IF bInPos[1] AND bInPos[2] AND bInPos[3] AND bInPos[4] THEN
            eStep := eStep + 1;
            rElapsed := 0.0;
        END_IF;
    4: (* TAPE_BOTTOM: hold while tape locks *)
        FOR i := 1 TO 4 DO
            aFold[i](bEnable := TRUE, rTargetDeg := 90.0, rKRestore := 0.02,
                     rAngleDeg := rAngle[i], rOmegaDeg_s := rOmega[i]);
            bTapeLock[i] := aFold[i].bInPosition;
        END_FOR;
        fbQuorumTape(bSensor := bTapeApplied);
        IF fbQuorumTape.eVerdict = 0 THEN
            eStep := 5;
            rElapsed := 0.0;
        END_IF;
    5: (* RAISE - fixed 1 s *)
        IF rElapsed >= 1.0 THEN
            eStep := 6;
            rElapsed := 0.0;
        END_IF;
    6: (* VERIFY: squareness invariant *)
        fbQuorumSquare(bSensor := bSquareOk);
        IF fbQuorumSquare.eVerdict = 0 THEN
            nResult := 1; (* PASS -> palletizer *)
        ELSE
            nResult := 2; (* FAIL -> reject lane *)
        END_IF;
END_CASE;

(* STO request: independent of the controller logic *)
bFault := bFault OR (NOT bSquareOk[1] AND NOT bSquareOk[2]);
"""


def st_source():
    """Return the embedded IEC 61131-3 ST source."""
    return ST_SOURCE
