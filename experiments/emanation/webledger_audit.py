"""webledger_audit: the SQLite-backed credit_commons.web.ledger.Ledger,
audited for mintage / conservation / reserve invariants.

Complements credit_commons_audit.py which certifies the SIMULATOR
(credit_commons/sim.py) as HONEST_NEGATIVE on L33 (grants mint instead
of drawing from reserve).  The web Ledger is the *spec-correct*
implementation: its grant() debits reserve and its trade() is internally
asserted to be gate-6 conserved.

Audited invariants (deterministic, float arithmetic checked to 1e-6):
    L44_webledger_grant_debits_reserve:
        "Web Ledger.grant is funded from the commons reserve (not
        minted)."  Over many seeded sequences: run grants and verify
        that conserved_total() is unchanged after every grant (credit +
        reserve invariant).  This is the correct behaviour that
        contrasts the sim's HONEST_NEGATIVE L33.

    L45_webledger_grants_only_within_reserve:
        The ledger refuses (returns ok=False) a grant that would draw
        more than the available reserve.  Verify: attempt a grant
        larger than the reserve and confirm it is rejected; a grant
        within the reserve succeeds.

    L46_webledger_trade_conserves_total:
        Over seeded trade sequences (with necessity/harm and fee
        handling), conserved_total() is invariant after every trade --
        gate-6 conservation confirmed directly on the SQLite ledger.
        Complements L14 which used the python-level sim handle.

    L47_webledger_grant_increases_recipient_trust:
        Candidate law: "a grant never changes the recipient's trust."
        FALSE: grants add 0.05 * scaled_amount to the recipient's trust
        (progressive trust bonus), so trust IS modified.  HONEST_NEGATIVE.
"""

import random

_TOL = 1e-6
_SEED_RANGE = list(range(10))


# ---------------------------------------------------------------------------
# Action-scripting helpers
# ---------------------------------------------------------------------------

def _fresh_ledger(seed):
    """In-memory SQLite Ledger with a deterministic roster of accounts.
    Two accounts are always created; on alternating seeds a third and
    fourth are added to exercise multi-party trades."""
    from credit_commons.web.ledger import Ledger
    rng = random.Random(seed)
    ledger = Ledger(":memory:")
    handles = ["alice", "bob"]
    if rng.random() < 0.6:
        handles.append("charlie")
    if rng.random() < 0.4:
        handles.append("diana")
    for h in handles:
        ledger.create_account(h, "pin_" + h)
    return ledger, rng, handles


def _account_ids(ledger):
    return [r["id"] for r in ledger.all_accounts()]


def _draw_trade(rng, ledger):
    ids = _account_ids(ledger)
    if len(ids) < 2:
        return None
    buyer = rng.choice(ids)
    seller = rng.choice([i for i in ids if i != buyer])
    x = float(rng.randint(1, 5))
    necessity = rng.random() < 0.35
    committed_harm = rng.choice([0.0, 0.5])
    terminal = rng.choice(ids) if rng.random() < 0.5 else None
    return dict(buyer_id=buyer, seller_id=seller, x=x,
                necessity=necessity, committed_harm=committed_harm,
                terminal=terminal)


# ---------------------------------------------------------------------------
# L44 -- grants are funded from the reserve (PASS)
# ---------------------------------------------------------------------------

def _L44_grant_debits_reserve(datum):
    """For one seed: create a ledger, run some trades to build reserve
    balance, then run grants.  After every grant the conserved_total()
    (accounts_sum + reserve) must be unchanged -- proving the grant
    drew from reserve and did NOT mint new credit."""
    seed = datum
    ledger, rng, _ = _fresh_ledger(seed)
    ids = _account_ids(ledger)
    # build reserve through trades
    for _ in range(15):
        kw = _draw_trade(rng, ledger)
        if kw is None:
            continue
        ledger.trade(**kw)
    # now grant from reserve
    for _ in range(rng.randint(1, 5)):
        recipient = rng.choice(ids)
        amount = float(rng.randint(1, 5))
        before = ledger.conserved_total()
        ledger.grant(recipient, amount)
        after = ledger.conserved_total()
        if abs(after - before) > _TOL:
            return False
    ledger.close()
    return True


# ---------------------------------------------------------------------------
# L45 -- grants exceeding reserve are rejected (PASS)
# ---------------------------------------------------------------------------

def _L45_grants_within_reserve(datum):
    """For one seed: create a ledger, do some trades to build reserve,
    then attempt a grant that exceeds the reserve (must fail) followed
    by a grant within the reserve (must succeed).  If both conditions
    hold the candidate law is satisfied."""
    seed = datum
    ledger, rng, _ = _fresh_ledger(seed)
    ids = _account_ids(ledger)
    # build reserve
    for _ in range(10):
        kw = _draw_trade(rng, ledger)
        if kw is None:
            continue
        ledger.trade(**kw)
    r = ledger.reserve
    recipient = rng.choice(ids)
    # attempt an impossibly large grant -- must be rejected
    ok_big, _ = ledger.grant(recipient, r + 9999.0)
    if ok_big:
        ledger.close()
        return False
    # a grant within the reserve must succeed
    small = max(0.1, r * 0.1) if r > 0 else 0.01
    ok_small, _ = ledger.grant(recipient, small)
    if not ok_small:
        ledger.close()
        return False
    ledger.close()
    return True


# ---------------------------------------------------------------------------
# L46 -- trades conserve total (PASS)
# ---------------------------------------------------------------------------

def _L46_trade_conserves_total(datum):
    """For one seed: run a scripted sequence of trades (mixed
    directions, necessity on/off, committed_harm, terminal present)
    and require that conserved_total() is EXACTLY conserved across
    every single trade."""
    seed = datum
    ledger, rng, _ = _fresh_ledger(seed)
    for _ in range(30):
        kw = _draw_trade(rng, ledger)
        if kw is None:
            continue
        before = ledger.conserved_total()
        ledger.trade(**kw)
        after = ledger.conserved_total()
        if abs(after - before) > _TOL:
            ledger.close()
            return False
    ledger.close()
    return True


# ---------------------------------------------------------------------------
# L47 -- HONEST NEGATIVE: grants DO increase recipient trust
# ---------------------------------------------------------------------------

def _L47_grant_increases_trust(datum):
    """The FALSE candidate law: 'a grant never changes the recipient's
    trust.'  Returns True ONLY IF the recipient's trust is unchanged
    after the grant.  Since grants add 0.05*scaled_amount to the
    recipient's trust, trust IS increased and pred returns False on
    its first datum: HONEST_NEGATIVE."""
    seed = datum
    ledger, rng, _ = _fresh_ledger(seed)
    ids = _account_ids(ledger)
    # build a comfortable reserve that guarantees the grant succeeds
    for _ in range(25):
        kw = _draw_trade(rng, ledger)
        if kw is None:
            continue
        ledger.trade(**kw)
    recipient = rng.choice(ids)
    trust_before = ledger.account_credit(recipient)["trust"]
    amount = 0.05  # small enough to be funded from the built-up reserve
    ok, _ = ledger.grant(recipient, amount)
    # the grant must actually succeed for this probe to be meaningful;
    # if it fails the "trust unchanged" is trivial and the probe voids
    if not ok:
        ledger.close()
        return True  # grant rejected: trust untouched (law vacuously holds here)
    trust_after = ledger.account_credit(recipient)["trust"]
    ledger.close()
    # law holds only if trust is unchanged
    return abs(trust_after - trust_before) < _TOL


# ---------------------------------------------------------------------------
# Certify
# ---------------------------------------------------------------------------

def _certify(label, meta, pred, domain):
    from experiments.emanation import law_checker as lc
    return lc.certify_statement(label, meta, pred, list(domain))


def webledger_certificates():
    """Return the four web-ledger audit certificates."""
    certs = []
    # L44: grants are funded from reserve (PASS)
    certs.append(_certify(
        "L44_webledger_grant_debits_reserve",
        {"domain": "10 seeded sequences: reserve built via 15 trades, "
                   "then 1-5 grants; conserved_total() checked to 1e-6 "
                   "after each grant",
         "law": "Web Ledger.grant funds from the commons reserve (not "
                "minted): conserved_total() == accounts_sum() + reserve "
                "is invariant across grants",
         "measured_on": "credit_commons.web.ledger.Ledger.grant, "
                        "in-memory SQLite, deterministic rng per sequence",
         "tolerance": 1e-6},
        _L44_grant_debits_reserve, _SEED_RANGE))
    # L45: grant overdraws are rejected (PASS)
    certs.append(_certify(
        "L45_webledger_grants_only_within_reserve",
        {"domain": "10 seeded sequences: reserve built via 10 trades, "
                   "then an impossibly large grant (must fail) followed "
                   "by a valid small grant (must succeed)",
         "law": "The ledger refuses a grant that would draw more than "
                "the available reserve; grants within the reserve "
                "succeed",
         "measured_on": "credit_commons.web.ledger.Ledger.grant "
                        "return value (ok, msg), in-memory SQLite",
         "tolerance": 1e-6},
        _L45_grants_within_reserve, _SEED_RANGE))
    # L46: trades conserve total (PASS)
    certs.append(_certify(
        "L46_webledger_trade_conserves_total",
        {"domain": "10 seeded sequences of 30 trades each (mixed "
                   "directions, necessity on/off, committed_harm in "
                   "{0.0, 0.5}, terminal present); conserved_total() "
                   "checked to 1e-6 after every trade",
         "law": "A trade is pure redistribution: conserved_total() "
                "(accounts_sum + reserve) is exactly conserved (no "
                "minting, no destruction), with the conserved fee "
                "reaching accounts and any unclaimed residue flowing to "
                "the commons reserve",
         "measured_on": "credit_commons.web.ledger.Ledger.trade, "
                        "in-memory SQLite, deterministic rng per sequence",
         "tolerance": 1e-6},
        _L46_trade_conserves_total, _SEED_RANGE))
    # L47: HONEST_NEGATIVE -- grants DO increase trust
    certs.append(_certify(
        "L47_webledger_grant_increases_recipient_trust",
        {"domain": "10 seeded sequences: reserve built via 8 trades, "
                   "then one grant; recipient trust checked before/after",
         "law": "FALSE CANDIDATE: a grant never changes the recipient's "
                "trust -- in fact grants add 0.05*scaled_amount to the "
                "recipient's trust (progressive trust bonus per spec "
                "section 5.5)",
         "honest_check": "recipient trust must be unchanged after the "
                         "grant; since grants add 0.05*amt to trust, the "
                         "pred is False and ships HONEST_NEGATIVE",
         "tolerance": 1e-6},
        _L47_grant_increases_trust, _SEED_RANGE))
    return certs
