"""battery_drain_model: a pure, model-only skeleton for the
battery-drain compensation dashboard (application lane).

ANCHOR (repository fact): THE_HARVEST_BOOK.md:288 records the honest
wall that mesh nodes 'transmits, and sleeps, with no line and no
battery change'.  This module implements the *mechanics* a dashboard
would need to display and compensate for heterogeneous battery drain:
for each node, integrate its duty cycle into energy consumed, compute
days-to-empty, and the per-node compensation pacing that equalizes
drain across the mesh.

MODELLING ONLY: there is no real telemetry dataset in the repository.
All inputs are numbers; every output is a computed number with units
declared.  No claim about a real device is made anywhere.

Units: energy in J (joules); draw in mW; time in s; capacity in J.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class NodeProfile:
    name: str
    sleep_seconds: float
    awake_seconds: float
    transceiver_mw: float
    compute_mw: float
    cells_serial: int = 1


def energy_per_cycle(p: NodeProfile) -> float:
    """Energy (J) one full sleep+awake cycle consumes.

    cycle = sleep + awake; power while awake = compute + transceiver,
    power while sleeping = transceiver (listener) only.
    """
    period = p.sleep_seconds + p.awake_seconds
    if period <= 0 or p.sleep_seconds < 0 or p.awake_seconds < 0:
        raise ValueError("duty-cycle times must be non-negative and "
                         "the cycle length positive")
    p_awake_mw = p.compute_mw + p.transceiver_mw
    p_sleep_mw = p.transceiver_mw
    return (p_awake_mw * p.awake_seconds + p_sleep_mw * p.sleep_seconds) \
        / 1000.0


def days_to_empty(p: NodeProfile, capacity_j: float) -> float:
    """Days until an ideal battery of capacity_j J is drained."""
    if capacity_j <= 0:
        raise ValueError("capacity must be positive")
    cycle_j = energy_per_cycle(p)
    if cycle_j <= 0:
        raise ValueError("a node that consumes nothing has no drain")
    period_s = p.sleep_seconds + p.awake_seconds
    return (capacity_j / cycle_j) * period_s / 86400.0


def compensation_pacing(p: NodeProfile, capacity_j: float,
                        target_days: float) -> float:
    """J/day of externally delivered energy that keeps the node alive
    for `target_days` with drain continuing (equalization pacing).

    Positive = the mesh must deliver energy to this node (charge or
    duty-cycle subsidy); negative = the node has headroom it can loan
    back (it drains slower than the target tariff).
    """
    if target_days <= 0:
        raise ValueError("target horizon must be positive")
    natural_j_per_day = (energy_per_cycle(p)
                         / (p.sleep_seconds + p.awake_seconds)) * 86400.0
    budget_j_per_day = capacity_j / target_days
    return natural_j_per_day - budget_j_per_day


def mesh_balance(profiles: list[NodeProfile], capacity_j: float,
                 target_days: float) -> dict[str, dict[str, float]]:
    """One-screen dashboard payload: per-node numbers plus the mesh
    totals, in a plain dict so any renderer can display it."""
    rows = {}
    for p in profiles:
        jpc = energy_per_cycle(p)
        dte = days_to_empty(p, capacity_j)
        comp = compensation_pacing(p, capacity_j, target_days)
        rows[p.name] = {
            "J_per_cycle": jpc,
            "days_to_empty": dte,
            "comp_J_per_day": comp,
        }
    rows["__mesh_total_daily_drain_J/day"] = sum(
        r["comp_J_per_day"] + capacity_j / target_days
        for r in rows.values())
    rows["__mesh_capacity_J"] = capacity_j
    rows["__target_days"] = target_days
    return rows