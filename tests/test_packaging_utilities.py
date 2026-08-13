"""Tests for the air-system / design-calculation helpers in packaging.utilities."""

import pytest

from packaging.utilities import (
    annual_cost_usd,
    annual_energy_kwh,
    avg_power_kw,
    avg_real_scfm,
    fad_scfm,
    rainwater_balance_series,
    receiver_volume_gal,
    runoff_m3,
    scfm_saved_power_kw,
    standby_savings_kwh_yr,
    tank_size_for_zero_deficit,
    vacuum_venturi_demand,
    water_cost_per_yr,
)


def test_fad_includes_margin():
    assert fad_scfm(20.0, margin_frac=0.30) == pytest.approx(26.0)


def test_fad_default_margin():
    assert fad_scfm(20.0) == pytest.approx(26.0)


def test_avg_real_includes_leak_allowance():
    assert avg_real_scfm(6.0, leak_frac=0.25) == pytest.approx(7.5)


def test_avg_real_default_leak_allowance():
    assert avg_real_scfm(6.0) == pytest.approx(7.5)


def test_avg_power_scales_with_flow():
    assert avg_power_kw(7.5, specific_power=0.22) == pytest.approx(1.65)
    assert avg_power_kw(15.0, specific_power=0.22) == pytest.approx(3.3)


def test_receiver_scales_with_fad_and_rule():
    assert receiver_volume_gal(27.3, rule_gal_per_scfm=1.0) == pytest.approx(27.3)
    assert receiver_volume_gal(27.3, rule_gal_per_scfm=6.0) == pytest.approx(163.8)


def test_receiver_default_vfd_rule():
    assert receiver_volume_gal(27.3) == pytest.approx(27.3)


def test_venturi_demand_linear_in_pads():
    assert vacuum_venturi_demand(4, 0.5) == pytest.approx(2.0)
    assert vacuum_venturi_demand(8, 0.5) == pytest.approx(4.0)


def test_annual_energy_linear():
    assert annual_energy_kwh(1.65, 8760.0) == pytest.approx(14454.0)
    assert annual_energy_kwh(1.65, 2080.0) == pytest.approx(3432.0)


def test_runoff_m3_math():
    # 300 m2, 800 mm, metal roof 0.85, 0.9 collection -> 183.6 m3
    assert runoff_m3(300.0, 800.0) == pytest.approx(183.6)
    assert runoff_m3(300.0, 800.0, runoff_coeff=0.6) == pytest.approx(129.6)


def test_runoff_scales_linear_with_area_and_rain():
    assert runoff_m3(100.0, 100.0) == pytest.approx(7.65)
    assert runoff_m3(200.0, 100.0) == pytest.approx(15.3)


def test_rainwater_balance_series_full_supply():
    r = rainwater_balance_series(tank_m3=10.0, inflows_m3=[5.0, 5.0],
                                 demands_m3=[3.0, 3.0])
    assert r["total_deficit_m3"] == pytest.approx(0.0)
    assert r["final_level_m3"] == pytest.approx(4.0)


def test_rainwater_balance_series_deficit_accumulates():
    r = rainwater_balance_series(tank_m3=2.0, inflows_m3=[0.0, 0.0],
                                 demands_m3=[1.0, 1.0])
    assert r["total_deficit_m3"] == pytest.approx(2.0)
    assert r["final_level_m3"] == pytest.approx(0.0)


def test_rainwater_balance_tank_caps_level():
    r = rainwater_balance_series(tank_m3=1.0, inflows_m3=[5.0],
                                 demands_m3=[0.0])
    assert r["peak_level_m3"] == pytest.approx(1.0)
    assert r["final_level_m3"] == pytest.approx(1.0)


def test_rainwater_peak_tracks_max_fill_not_post_serve():
    r = rainwater_balance_series(tank_m3=3.0, inflows_m3=[5.0],
                                 demands_m3=[1.0])
    assert r["peak_level_m3"] == pytest.approx(3.0)
    assert r["final_level_m3"] == pytest.approx(2.0)


def test_tank_size_for_zero_deficit_finds_minimum():
    inflows = [5.0, 0.0, 0.0]
    demands = [1.0, 1.0, 1.0]
    # refill arrives in month 1; the tank must carry 3.0 m3 to serve months 2-3
    assert tank_size_for_zero_deficit(inflows, demands,
                                      cap_max_m3=10.0, step_m3=0.5) == pytest.approx(3.0)


def test_tank_size_returns_none_when_insufficient():
    inflows = [0.0, 0.0]
    demands = [1.0, 1.0]
    assert tank_size_for_zero_deficit(inflows, demands,
                                      cap_max_m3=1.0, step_m3=0.5) is None


def test_water_cost_linear():
    assert water_cost_per_yr(39.6, 4.0) == pytest.approx(158.4)
    assert water_cost_per_yr(0.0, 4.0) == pytest.approx(0.0)


def test_standby_savings_math():
    # 8 h/day at 1.4 kW dropped load, 260 days -> 2912 kWh/yr
    assert standby_savings_kwh_yr(8.0, 2.3, 0.9, 260.0) == pytest.approx(2912.0)


def test_standby_savings_zero_when_no_idle():
    assert standby_savings_kwh_yr(0.0, 2.3, 0.9, 260.0) == pytest.approx(0.0)


def test_standby_savings_scales_with_days():
    assert standby_savings_kwh_yr(8.0, 2.3, 0.9, 130.0) == pytest.approx(1456.0)


def test_scfm_saved_power_math():
    assert scfm_saved_power_kw(1.5, specific_power=0.22) == pytest.approx(0.33)


def test_scfm_saved_power_default_specific_power():
    assert scfm_saved_power_kw(2.0) == pytest.approx(0.44)


def test_annual_cost_linear():
    assert annual_cost_usd(2912.0, 0.12) == pytest.approx(349.44)
    assert annual_cost_usd(0.0, 0.12) == pytest.approx(0.0)
