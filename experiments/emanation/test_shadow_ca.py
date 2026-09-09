"""Tests for the shadow (de Bruijn / second-order) CA construction.

The shadow construction PRESERVES additivity: additive bases (rules 90, 150)
have additive shadows (0/1000 superposition failures); non-additive bases
(12/44/68/100, proven non-linear in test_shift_bus) have NON-additive
shadows (~100% failures).  So applying a shadow to the shift-bus rules does
NOT make them additive, linear, or any closer to a computing or network
substrate -- the transform preserves a property it cannot create.

Capacity: the shadow macro-cell holds (top,bottom) = 2 bits, so on a fixed
physical width it doubles the cell count; any capacity in bits per cell
shrinks accordingly.  No free lunch: shadows change the algebra, not the
information budget.
"""

import pytest

from shadow_ca import ShadowCA


@pytest.mark.parametrize("base_rule", [12, 44, 68, 100])
def test_shadow_of_nonadditive_rule_stays_nonadditive(base_rule):
    s = ShadowCA(base_rule)
    failures, trials = s.additivity_failures(trials=300, seed=base_rule)
    assert failures == trials, (
        'expected non-additive shadow for rule %d, got %d/%d'
        % (base_rule, failures, trials))


@pytest.mark.parametrize("additive_rule", [90, 150])
def test_shadow_of_additive_rule_stays_additive(additive_rule):
    """Sanity: the construction itself preserves additivity, so the
    non-additivity seen for 12/44/68/100 is inherited from the base, not an
    artifact of the shadow transform."""
    s = ShadowCA(additive_rule)
    failures, trials = s.additivity_failures(trials=600, seed=additive_rule)
    assert failures == 0, (
        'additive base rule %d must keep additive shadow, got %d/%d'
        % (additive_rule, failures, trials))


def test_shadow_material_cost_is_two_bits_per_cell():
    """Every original lattice cell becomes a top+bottom macro-cell: the
    shadow needs >= 2x cells for the same physical extent.  A 'fix' that
    worked would still pay this -- shadows change the algebra, not the
    information budget."""
    assert ShadowCA.MACRO_BITS == 2
    # concrete: a width-100 base row needs 200 macro cells at equal extent
    assert ShadowCA.macro_width(100) == 200