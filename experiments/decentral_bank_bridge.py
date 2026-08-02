"""
DECENTRAL BANK BRIDGE (T-series T69) - on/off-ramp to a centralized bank.

The honest fact that shapes a bridge: a decentralized ledger CANNOT self-settle
fiat.  Money crosses into bank money only through a licensed gateway holding
custody.  This file builds the thinnest honest version of that boundary:

  MockBank  - a stand-in for the centralized bank: one custody account plus
              per-customer fiat ledger, idempotent by reference id (ref).
  Gateway   - a DCN account that holds the mint reserve (the backing).  It
              mints on-ramp (fiat in -> DCN credit) and burns off-ramp
              (DCN burn -> fiat paid out).  Every op is idempotent by ref,
              so a retried wire cannot double-settle.

The measured security invariant (the null the bridge must not beat):
    custody_fiat + gateway_DCN_balance == initial_reserve
i.e. the gateway can never pay out more than its backing.  Reconcile() is
that check, and every test reports it.

Tests (each with a null):
  T9  round trip:  on-ramp credits DCN 1:1, off-ramp pays fiat 1:1, user's
      DCN and fiat statements move by exactly the amounts.
  T10 idempotency: replaying a ref (on-ramp or off-ramp) settles NOTHING
      twice - no double mint, no double payout (null: a bank without refs
      would double-pay).
  T11 backing:     after a randomized batch (some replayed refs, a forged
      over-withdraw attempt), reconcile() holds EXACTLY and the forged
      off-ramp is rejected (null: paying out more than backing is the
      bridge's cardinal sin).

Limits (crease-worthy, printed):
  - Custody is a single simulated account; a real gateway needs m-of-n
    threshold multisig and an HSM, not one key.
  - The bank is a mock; no network, no TLS, no KYC/AML/sanctions, no
    regulator reporting - the parts a real bank actually demands.
  - Idempotency is by caller-supplied ref; a real bridge must derive refs
    from bank-side transaction IDs, never trust the customer's ref.
  - The burn-before-payout order uses a custody peek so payout "can't fail"
    after burn; a real bridge needs a reversal (compensation) path.
"""

import json
import os
from collections import defaultdict

import numpy as np

from cryptography.hazmat.primitives.asymmetric.ed25519 import (  # noqa: E402
    Ed25519PrivateKey)
from cryptography.hazmat.primitives.serialization import (  # noqa: E402
    Encoding, NoEncryption, PrivateFormat, PublicFormat)

from decentral_bank import FragmentBank, address_of  # noqa: E402

RNG = np.random.RandomState(20260802)


# ---------------------------------------------------------------------- #
# The centralized bank (mock)
# ---------------------------------------------------------------------- #
class MockBank:
    """One custody account + per-customer fiat ledger.  All ops idempotent
    by reference id - replaying a ref settles nothing twice."""

    def __init__(self):
        self.custody = 0.0
        self.ledger = defaultdict(float)   # customer_id -> cumulative fiat
        self.refs = set()

    def deposit(self, ref, amount, customer_id):
        """Customer wires fiat into gateway custody."""
        if ref in self.refs:
            return False, "already-settled"
        self.refs.add(ref)
        self.custody += amount
        self.ledger[customer_id] += amount
        return True, "ok"

    def withdraw(self, ref, amount, customer_id):
        """Gateway pays fiat out of custody to the customer."""
        if ref in self.refs:
            return False, "already-settled"
        if self.custody < amount - 1e-9:
            return False, "insufficient-custody"
        self.refs.add(ref)
        self.custody -= amount
        self.ledger[customer_id] += amount
        return True, "ok"


# ---------------------------------------------------------------------- #
# The gateway (custody holder + DCN mint/burn)
# ---------------------------------------------------------------------- #
class Gateway:
    def __init__(self, bank, reserve=1_000_000):
        priv = Ed25519PrivateKey.generate()
        pub = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        self.addr = address_of(pub)
        self.bank = bank
        self.reserve = reserve
        self.refs = set()                      # gateway-side idempotency
        self.owner = bank.route(self.addr)
        bank.balances[self.owner][self.addr] = reserve
        bank.frag_for[self.addr] = self.owner
        bank.keys[self.addr] = (pub, priv)
        bank.accounts.append((self.addr, self.owner))
        self.mock = MockBank()

    # ---- the two directions ------------------------------------------ #
    def onramp(self, ref, amount, customer_id, user_addr):
        """fiat in -> DCN credit.  Replayed ref = no second mint."""
        if ref in self.refs:
            return False, "ref-replay"
        ok, why = self.mock.deposit(ref, amount, customer_id)
        if not ok:
            return False, why
        self.refs.add(ref)
        return self.bank.transfer(self.addr, user_addr, int(amount))

    def offramp(self, ref, amount, customer_id, user_addr):
        """DCN burn -> fiat out.  Peek custody BEFORE burning so a payout
        cannot fail after the burn (toy: no compensation path)."""
        if ref in self.refs:
            return False, "ref-replay"
        if self.mock.custody < amount - 1e-9:
            return False, "insufficient-custody"
        ok, why = self.bank.transfer(user_addr, self.addr, int(amount))
        if not ok:
            return False, why
        self.refs.add(ref)
        return self.mock.withdraw(ref, amount, customer_id)

    # ---- the measured invariant -------------------------------------- #
    def reconcile(self):
        """The bridge's null: custody + gateway DCN == reserve.  Anything
        else means the gateway minted or paid more than it holds."""
        gw_bal = self.bank.balances[self.owner][self.addr]
        diff = (self.mock.custody + gw_bal) - self.reserve
        return (abs(diff) < 1e-9), round(float(diff), 6)

    def gw_balance(self):
        return self.bank.balances[self.owner][self.addr]


# ---------------------------------------------------------------------- #
# Tests
# ---------------------------------------------------------------------- #
def _fresh():
    bank = FragmentBank(10, accounts_per_frag=15)
    gw = Gateway(bank, reserve=1_000_000)
    return bank, gw


def _users(bank, gw):
    """User addresses EXCLUDING the gateway (the gateway is registered in
    bank.accounts; a bridge must never let the reserve pay itself)."""
    return [a for a, _ in bank.accounts if a != gw.addr]


def test_t9_round_trip():
    bank, gw = _fresh()
    user = _users(bank, gw)[0]
    before = bank.balances[bank.frag_for[user]][user]
    ok1, why1 = gw.onramp("w1", 1000, "cust-a", user)
    mid = bank.balances[bank.frag_for[user]][user]
    ok2, why2 = gw.offramp("w2", 400, "cust-a", user)
    after = bank.balances[bank.frag_for[user]][user]
    cust_fiat = gw.mock.ledger["cust-a"]
    okr, dif = gw.reconcile()
    return {"test": "T9 round trip",
            "onramp_ok": ok1, "offramp_ok": ok2,
            "dcn_credit": mid - before, "dcn_burn": mid - after,
            "customer_fiat": cust_fiat,
            "reconcile": okr, "diff": dif,
            "verdict": "PASS" if (ok1 and ok2 and okr
                                  and mid - before == 1000
                                  and mid - after == 400
                                  and cust_fiat == 1400) else "FAIL"}


def test_t10_idempotency():
    bank, gw = _fresh()
    user = _users(bank, gw)[0]
    gw.onramp("w1", 1000, "cust-a", user)
    gw.offramp("w2", 300, "cust-a", user)
    cust_before = gw.mock.custody
    dcn_before = bank.balances[bank.frag_for[user]][user]
    # replay both refs - the null: a naive bank would settle again
    ok1, _ = gw.onramp("w1", 1000, "cust-a", user)
    ok2, _ = gw.offramp("w2", 300, "cust-a", user)
    cust_after = gw.mock.custody
    dcn_after = bank.balances[bank.frag_for[user]][user]
    okr, dif = gw.reconcile()
    double = (not ok1 and not ok2 and cust_before == cust_after
              and dcn_before == dcn_after)
    return {"test": "T10 idempotency",
            "replayed_onramp_rejected": not ok1,
            "replayed_offramp_rejected": not ok2,
            "custody_unchanged": cust_before == cust_after,
            "dcn_unchanged": dcn_before == dcn_after,
            "reconcile": okr, "diff": dif,
            "verdict": "PASS" if (double and okr) else "FAIL"}


def test_t11_backing():
    bank, gw = _fresh()
    rng = np.random.RandomState(11)
    users = _users(bank, gw)
    ref_pool = ["w%04d" % i for i in range(150)]   # 300 ops, 150 refs -> replays
    refs_seen = set()
    n_ok = n_replay = 0
    forged_attempted = forged_ok = False
    for i in range(300):
        user = users[rng.randint(0, len(users))]
        amount = int(rng.randint(1, 300))
        ref = ref_pool[rng.randint(0, len(ref_pool))]
        if ref in refs_seen:
            n_replay += 1
        if rng.rand() < 0.5:
            ok, why = gw.onramp(ref, amount, "cust-b", user)
        else:
            # 10% of withdraws are forged: more than the user holds
            bal = bank.balances[bank.frag_for[user]][user]
            amt = amount * 10 if rng.rand() < 0.1 else amount
            ok, why = gw.offramp(ref, amt, "cust-b", user)
            if amt > bal + 1:
                forged_attempted = True
                forged_ok = ok
        refs_seen.add(ref)
        n_ok += bool(ok)
    okr, dif = gw.reconcile()
    forged_rejected = forged_attempted and not forged_ok
    return {"test": "T11 backing", "ops_ok": n_ok,
            "replays_seen": n_replay,
            "forged_overwithdraw_rejected": forged_rejected,
            "reconcile": okr, "diff": dif,
            "verdict": "PASS" if (okr and forged_rejected) else "FAIL"}


# ---------------------------------------------------------------------- #
def main():
    print("=" * 66)
    print("DECENTRAL BANK BRIDGE (T69) - mock centralized bank on/off-ramp")
    print("=" * 66)
    results = {}
    for fn in [test_t9_round_trip, test_t10_idempotency, test_t11_backing]:
        r = fn()
        results[r["test"]] = r
        print(f"  [{r['verdict']:8s}] {r['test']}")
        for k, v in r.items():
            if k not in ("test", "verdict"):
                print(f"        {k} = {v}")

    limits = {
        "single_key_custody": "one gateway key, no m-of-n threshold, no HSM",
        "mock_bank": "no network, no TLS, no KYC/AML/sanctions, no regulator reporting",
        "trusted_refs": "idempotency by caller-supplied ref; a real bridge must derive refs from bank-side txn IDs",
        "no_compensation": "burn-before-payout uses a custody peek so payout cannot fail after burn; no reversal path",
    }
    print("\nLIMITS (crease-worthy):")
    for k, v in limits.items():
        print(f"  {k}: {v}")

    out = {"results": results, "limits": limits}
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "data", "decentral_bank_bridge_data.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote data/decentral_bank_bridge_data.json")


if __name__ == "__main__":
    main()
