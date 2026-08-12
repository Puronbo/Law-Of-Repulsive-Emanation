"""packaging - autonomous case-packaging line control code.

Python mirror of the IEC 61131-3:2025 ST source in `packaging/plc_61131_3.py`,
implementing the fold servo (PID + restoring-torque feedforward), the
majority-honesty quorum, and the ERECT step machine from
`docs/AUTO_PACKAGING_SYSTEM.md`.
"""

from packaging.servo import ErectorFlow, FoldAxis, PidController, QuorumVote

__all__ = ["ErectorFlow", "FoldAxis", "PidController", "QuorumVote"]
