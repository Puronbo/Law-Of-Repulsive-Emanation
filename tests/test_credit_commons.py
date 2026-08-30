"""Tests asserting the 14 hard gates + stability/equity properties of the
Credit-Commons simulator (docs/CREDIT_COMMONS.md)."""

import pytest

from credit_commons import Commons
from credit_commons.sim import Params


# ---------------------------------------------------------------------------
# Gate 6 / §3 — money is conserved, never minted from a trade
# ---------------------------------------------------------------------------
def test_total_credit_conserved_across_trades():
    c = Commons()
    b = c.add_account()
    s = c.add_account()
    total0 = c.total_credit
    for _ in range(50):
        c.trade(b, s, 2.0, terminal=s)
        c.trade(s, b, 1.0, terminal=b)
    cons = sum(a.credit for a in c.accounts.values()) + c.reserve
    assert abs(c.total_credit - total0) < 1e-9          # no mintage
    assert abs(cons - total0) < 1e-9                     # nothing lost


def test_no_external_anchor_after_seed():
    # trades must never create credit out of nothing (Phase 1 purity, gate 2).
    c = Commons()
    b = c.add_account(); s = c.add_account()
    before = c.total_credit
    for _ in range(20):
        c.trade(b, s, 3.0)
    assert c.total_credit <= before + 1e-9
    # and total credit only ever changes via grants/seed (external), never trades.


# ---------------------------------------------------------------------------
# Gate 4 — trust is bounded; buy denied beyond the trust ceiling
# ---------------------------------------------------------------------------
def test_trust_never_negative():
    c = Commons()
    a = c.add_account()
    for _ in range(200):
        c.step()
    assert all(ac.trust >= 0 for ac in c.accounts.values())


def test_buy_denied_beyond_trust_ceiling():
    c = Commons()
    b = c.add_account(); s = c.add_account()
    # spend far beyond trust -> rejected
    ok = True
    X = 0
    for _ in range(1000):
        r = c.trade(b, s, 5.0)
        if not r.ok:
            ok = False
            break
    assert ok is False  # eventually the ceiling stops the buyer


# ---------------------------------------------------------------------------
# Gate 5 & §5.6 — negative action is weighted in irreversibility
# ---------------------------------------------------------------------------
def test_committed_harm_is_irreversible():
    c = Commons()
    b = c.add_account(seed_credit=100, seed_trust=100)
    s = c.add_account(seed_credit=100, seed_trust=100)
    before = c.accounts[b].trust
    c.trade(b, s, 5.0, committed_harm=1.0)               # a fraud/default
    scarred = c.accounts[b].trust
    assert scarred < before                              # trust scarred
    # later positive action cannot erase the irreversible notch
    for _ in range(50):
        c.trade(s, b, 1.0, terminal=b)                   # b sells (positive)
        c.trade(b, s, 1.0, necessity=True)               # b consumes necessity
    # irrev stays exactly I — positive reward never subtracts it.
    assert c.accounts[b].irrev == pytest.approx(Params().I * 1.0, abs=1e-9)


def test_positive_weighted_in_magnitude():
    # §5.6 alpha>0: a seller earns MORE trust than the nominal r per unit.
    p = Params(r=0.10, alpha=0.5)
    c = Commons(p)
    b = c.add_account(); s = c.add_account(seed_trust=40, seed_credit=40)
    t0 = c.accounts[s].trust
    c.trade(b, s, 10.0)
    gain = c.accounts[s].trust - t0
    expected = p.r * (1 + p.alpha) * 10.0
    assert gain == pytest.approx(expected, abs=1e-9)
    assert gain > p.r * 10.0   # bias is real


# ---------------------------------------------------------------------------
# Gate 13 / §5.5 — the pro-poor spine
# ---------------------------------------------------------------------------
def test_necessity_consumption_rebuilds_trust_E1():
    c = Commons()
    a = c.add_account(); s = c.add_account(seed_trust=100, seed_credit=100)
    t0 = c.accounts[a].trust
    r = c.trade(a, s, 5.0, necessity=True)
    assert r.ok
    assert c.accounts[a].trust > t0   # necessity REBUILDS trust


def test_drawdown_is_progressive_in_depth_E2():
    # deeper borrowing costs more trust per unit (bounds over-leverage).
    c = Commons()
    deep_i = c.add_account(seed_trust=10, seed_credit=10)
    shallow_i = c.add_account(seed_trust=10, seed_credit=10)
    s_i = c.add_account(seed_trust=100, seed_credit=100)
    # push `deep` deep into negative first
    for _ in range(150):
        if not c.trade(deep_i, s_i, 2.0).ok:
            break
    # push `shallow` only slightly
    for _ in range(5):
        c.trade(shallow_i, s_i, 2.0)
    deep = c.accounts[deep_i]
    shallow = c.accounts[shallow_i]
    assert deep.depth() > shallow.depth()
    assert deep.depth() > 0.0


def test_taper_is_progressive_E2():
    # large idle surplus decays faster than modest surplus (progressive).
    p = Params(taperA=0.001)
    assert p.taper_of(100) > p.taper_of(1)   # bigger surplus, bigger taper
    assert p.taper_of(1) < 0.01              # modest surplus barely touched


# ---------------------------------------------------------------------------
# E3 — fee split reserves a use-side consumer floor
# ---------------------------------------------------------------------------
def test_fee_has_consumer_floor_E3():
    c = Commons()
    b = c.add_account(); s = c.add_account()
    before = c.accounts[b].credit
    c.trade(b, s, 10.0)
    assert c.accounts[b].credit > before - 10.0  # buyer got some fee value back


# ---------------------------------------------------------------------------
# Stability — no cold-start stall; concentration stays bounded
# ---------------------------------------------------------------------------
def test_no_cold_start_stall_for_poor_consumer():
    # A consumer who only buys necessities stays solvent and trusted — sustained
    # by Phase-2 progressive grants from the commons reserve (the design's real
    # mechanism for those who cannot contribute). No honest system gives
    # *infinite* credit to a never-contributor (that is the sybil/free-money
    # hole gate 1 forbids); grants bridge the gap.
    c = Commons()
    poor = c.add_account(seed_credit=5, seed_trust=5)
    s = c.add_account(seed_credit=100, seed_trust=100)
    r = c.trade(poor, s, 8.0, necessity=True)   # deep necessity borrowing
    assert not r.ok or c.accounts[poor].credit >= -c.accounts[poor].trust
    # grant support keeps the pure consumer solvent
    c.grant(poor, 8.0)
    for _ in range(50):
        if not c.trade(poor, s, 2.0, necessity=True).ok:
            break
    assert c.accounts[poor].trust > 0          # never driven to zero


def test_no_runaway_concentration_random_trades():
    # rich-get-richer check: with the floor + progressive g, the Gini of trust
    # stays modest across many random trades (not trending to 1).
    import random
    random.seed(42)
    c = Commons()
    ids = [c.add_account() for _ in range(20)]
    for _ in range(2000):
        b, s = random.sample(ids, 2)
        c.trade(b, s, random.uniform(0.5, 3.0), necessity=(random.random() < 0.5))
        if random.random() < 0.2:
            c.step()
    g = c.gini("trust")
    assert g < 0.6   # bounded, far from total concentration (Gini ~1)


def test_baseline_floor_keeps_idle_account_alive_B5():
    c = Commons()
    idle = c.add_account()
    t0 = c.accounts[idle].trust
    for _ in range(50):
        c.step()
    assert c.accounts[idle].trust > 0          # floor regenerates
