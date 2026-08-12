"""Air-system and general design-calculation helpers for the packaging line.

Pure functions used by `experiments/air_sizing.py` and
`experiments/rainwater_sizing.py`, pinned by
`tests/test_packaging_utilities.py`. Units: scfm (free air at 14.7 psi),
kW, gallons, m3. All sizing is schematic-level; the "excess air" question is
answered explicitly: headroom belongs in the receiver tank and a VFD
compressor, not in an oversized fixed-speed machine.
"""


def fad_scfm(peak_scfm, margin_frac=0.30):
    """Compressor free-air delivery sized for peak demand + margin."""
    return peak_scfm * (1.0 + margin_frac)


def avg_real_scfm(avg_scfm, leak_frac=0.25):
    """Average demand including the typical compressed-air leak allowance.

    Plant surveys routinely find 20-30% of compressed air lost to leaks;
    the allowance sizes the running cost, the tank handles the peaks.
    """
    return avg_scfm * (1.0 + leak_frac)


def avg_power_kw(avg_real_scfm, specific_power=0.22):
    """Average compressor draw in kW. VFD compressors follow average flow;
    specific power ~0.16-0.25 kW per scfm is typical for screw compressors."""
    return specific_power * avg_real_scfm


def receiver_volume_gal(fad_scfm, rule_gal_per_scfm=1.0):
    """Receiver tank volume. Rule of thumb: ~1 gal/scfm FAD for a VFD/trim
    system (2-3 min buffer), ~6 gal/scfm for fixed-speed stop/start."""
    return fad_scfm * rule_gal_per_scfm


def vacuum_venturi_demand(n_pads, scfm_per_pad):
    """Continuous free-air demand of Bernoulli/venturi vacuum pads."""
    return n_pads * scfm_per_pad


def annual_energy_kwh(avg_power_kw, hours_per_year):
    """Energy draw at the given average power."""
    return avg_power_kw * hours_per_year


def runoff_m3(area_m2, rainfall_mm, runoff_coeff=0.85, collection_eff=0.9):
    """Harvested volume (m3) from a catchment in one period.

    rainfall_mm / 1000 -> metres of rain; runoff_coeff is roof-material loss
    (~0.85 metal standing seam, ~0.7-0.8 asphalt, ~0.6 gravel/vegetated);
    collection_eff covers first-flush diversion, leaf screens and filter
    losses.
    """
    return area_m2 * (rainfall_mm / 1000.0) * runoff_coeff * collection_eff


def rainwater_balance_series(tank_m3, inflows_m3, demands_m3):
    """Month-by-month tank simulation.

    For each period: add inflow (capped at tank capacity), record the peak
    fill, then serve demand or record the shortfall. Returns final level,
    total deficit and peak fill reached. inflow/demand lists must have equal
    length.
    """
    level = 0.0
    deficit = 0.0
    peak = 0.0
    for inflow, demand in zip(inflows_m3, demands_m3):
        level = min(tank_m3, level + inflow)
        peak = max(peak, level)
        if level >= demand:
            level -= demand
        else:
            deficit += demand - level
            level = 0.0
    return {"final_level_m3": level, "total_deficit_m3": deficit,
            "peak_level_m3": peak}


def tank_size_for_zero_deficit(inflows_m3, demands_m3,
                               cap_max_m3=10.0, step_m3=0.5):
    """Smallest tank capacity (m3) with zero total deficit over the series.

    Returns None if cap_max_m3 is insufficient.
    """
    cap = step_m3
    while cap <= cap_max_m3 + 1e-9:
        if rainwater_balance_series(cap, inflows_m3, demands_m3)["total_deficit_m3"] <= 1e-9:
            return cap
        cap += step_m3
    return None


def water_cost_per_yr(demand_m3, price_per_m3):
    """Municipal water cost for the non-potable demand being offset."""
    return demand_m3 * price_per_m3
