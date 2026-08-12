"""Tests for the air-system / design-calculation helpers in packaging.utilities."""

import pytest

from packaging.utilities import (
    annual_energy_kwh,
    avg_power_kw,
    avg_real_scfm,
    fad_scfm,
    receiver_volume_gal,
    vacuum_venturi_demand,
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
