"""Air-system and general design-calculation helpers for the packaging line.

Pure functions used by `experiments/air_sizing.py` and pinned by
`tests/test_packaging_utilities.py`. Units: scfm (free air at 14.7 psi),
kW, gallons. All sizing is schematic-level; the "excess air" question is
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
