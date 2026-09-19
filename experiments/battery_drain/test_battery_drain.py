"""battery_drain_model tests: exact math, no fake telemetry."""
import pytest

from battery_drain_model import (NodeProfile, compensation_pacing,
                                 days_to_empty, energy_per_cycle,
                                 mesh_balance)


def test_energy_per_cycle_exact():
    p = NodeProfile("n1", sleep_seconds=95.0, awake_seconds=5.0,
                    transceiver_mw=20.0, compute_mw=100.0)
    # 5 s awake at 120 mW = 0.6 J; 95 s listening at 20 mW = 1.9 J.
    assert energy_per_cycle(p) == pytest.approx(2.5)


def test_days_to_empty_exact():
    p = NodeProfile("n1", sleep_seconds=95.0, awake_seconds=5.0,
                    transceiver_mw=20.0, compute_mw=100.0)
    # 2.5 J per 100 s cycle -> 2160 J/day. A 2160 J battery lasts 1 day.
    assert days_to_empty(p, capacity_j=2160.0) == pytest.approx(1.0)


def test_compensation_pacing_tariff():
    p = NodeProfile("n1", sleep_seconds=95.0, awake_seconds=5.0,
                    transceiver_mw=20.0, compute_mw=100.0)
    # natural drain 2160 J/day; tariff capacity/30d = 72 J/day ->
    # must net ~2088 J/day to hold a 30-day horizon.
    assert compensation_pacing(p, capacity_j=2160.0, target_days=30.0) \
        == pytest.approx(2088.0)


def test_validation():
    p = NodeProfile("n1", sleep_seconds=-1.0, awake_seconds=5.0,
                    transceiver_mw=20.0, compute_mw=100.0)
    with pytest.raises(ValueError):
        energy_per_cycle(p)
    with pytest.raises(ValueError):
        days_to_empty(p, capacity_j=0.0)
    with pytest.raises(ValueError):
        compensation_pacing(p, capacity_j=2160.0, target_days=0.0)


def test_mesh_balance_shape():
    ps = [NodeProfile("a", 95.0, 5.0, 20.0, 100.0),
          NodeProfile("b", 99.0, 1.0, 10.0, 50.0)]
    rows = mesh_balance(ps, capacity_j=2160.0, target_days=30.0)
    assert set(rows) == {"a", "b", "__mesh_total_daily_drain_J/day",
                         "__mesh_capacity_J", "__target_days"}
    assert rows["a"]["days_to_empty"] == pytest.approx(1.0)