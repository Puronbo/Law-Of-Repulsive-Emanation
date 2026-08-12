"""packaging - autonomous case-packaging line control code.

Python mirror of the IEC 61131-3:2025 ST source in `packaging/plc_61131_3.py`,
implementing the fold servo (PID + restoring-torque feedforward), the
majority-honesty quorum, and the ERECT step machine from
`docs/AUTO_PACKAGING_SYSTEM.md`.
"""

from packaging.servo import ErectorFlow, FoldAxis, PidController, QuorumVote
from packaging.utilities import (
    annual_energy_kwh,
    avg_power_kw,
    avg_real_scfm,
    fad_scfm,
    rainwater_balance_series,
    receiver_volume_gal,
    runoff_m3,
    tank_size_for_zero_deficit,
    vacuum_venturi_demand,
    water_cost_per_yr,
)

__all__ = [
    "ErectorFlow",
    "FoldAxis",
    "PidController",
    "QuorumVote",
    "annual_energy_kwh",
    "avg_power_kw",
    "avg_real_scfm",
    "fad_scfm",
    "rainwater_balance_series",
    "receiver_volume_gal",
    "runoff_m3",
    "tank_size_for_zero_deficit",
    "vacuum_venturi_demand",
    "water_cost_per_yr",
]
