"""repo_audit: the supervisor's interface to REAL repo subsystems.

The first audited system is credit_commons.web.ledger.Ledger -- the
persistent bigsqlite implementation of the trust-backed mutual-credit
ledger, which asserts spec gate 6 (conservation) on every action.

    L14 gate6 conservation: trade/grant move value between accounts
        (credit) and the commons reserve; the invariant
        conserved_total = sum(account.credit) + reserve must be exactly
        unchanged by every approved or rejected action.  Statement
        certificates re-derive it as an independent measurement over
        controlled random sequences of real trades/grants (floats,
        checked to 1e-6, the ledger's own bar), each action sequence on
        a fresh :memory: ledger, deterministic rng.

    L14_bad: the candidate invariant "sum(account.credit) alone is
        conserved" must FAIL wherever fee residue reaches the reserve or
        a grant draws it back down -- honest negative for the supervisor
        to reject concretely.

NOTED FINDING (recorded, not used): credit_commons.sim.Commons.grant
credits `amount` to the recipient and grows total_credit WITHOUT
debiting or tracking reserve -- so it mints and violates gate 6, unlike
the ledger.  The audited conservation law belongs to the ledger; the sim
grants are a known divergence (cf tests/test_credit_commons.py).

Also provides fresh-table drift detection: the persisted
law_certificates.json must reproduce exactly from current code, or
`--gate` supervision fails (audit-the-audit).
"""
import json
import os
import random
import tempfile

from credit_commons.web.ledger import Ledger

_LAB = os.path.dirname(os.path.abspath(__file__))
_CERTS = os.path.join(_LAB, "data", "law_certificates.json")
_TOL = 1e-6


def _run_sequence(seed):
    """Controlled deterministic action sequence on a fresh :memory: ledger;
    returns (conserved_before_each, credit_sum_before_each,
    n_actions_executed)."""
    rng = random.Random(seed)
    led = Ledger(":memory:")
    buyers = []
    for h in ("a", "b", "c"):
        buyers.append(led.create_account(h, "pin")[0])
    conserved = []
    credit_sum = []
    n_actions = 0
    for _ in range(24):
        conserved.append(led.conserved_total())
        credit_sum.append(led.accounts_sum())
        buyer = rng.choice(buyers)
        seller = rng.choice([i for i in buyers if i != buyer])
        X = rng.randint(1, 9)
        if rng.random() < 0.15:
            ok, _ = led.grant(buyer, X, sponsor_id=seller)
        else:
            ok, _ = led.trade(
                buyer, seller, X,
                necessity=(False if rng.random() < 0.6 else True),
                committed_harm=(1.0 if rng.random() < 0.15 else 0.0))
        if ok:
            n_actions += 1
    led.close()
    return conserved, credit_sum, n_actions


def system_certificates():
    """L14 / L14_bad measured on the real ledger + calendar exactness
    invariants (both from real subsystems in this repository)."""
    from experiments.emanation.calendars_audit import calendar_certificates
    from experiments.emanation import law_checker as lc
    seeds = list(range(30))

    def invariant_holds(seed, metric):
        rng = random.Random(seed)
        led = Ledger(":memory:")
        buyers = [led.create_account(h, "pin")[0] for h in ("a", "b", "c")]
        ok_count = 0
        for _ in range(24):
            before = metric(led)
            buyer = rng.choice(buyers)
            seller = rng.choice([i for i in buyers if i != buyer])
            X = rng.randint(1, 9)
            if rng.random() < 0.15:
                ok, _ = led.grant(buyer, X, sponsor_id=seller)
            else:
                ok, _ = led.trade(
                    buyer, seller, X,
                    necessity=(False if rng.random() < 0.6 else True),
                    committed_harm=(1.0 if rng.random() < 0.15 else 0.0))
            if abs(metric(led) - before) > _TOL:
                led.close()
                return False
            if ok:
                ok_count += 1
        led.close()
        return ok_count > 0

    conserved_metric = lambda led: led.conserved_total()
    credit_metric = lambda led: led.accounts_sum()

    return [
        lc.certify_statement(
            "L14_gate6_conservation",
            {"domain": "30 seeded action-sequences on 3 real accounts of "
                       "the SQLite ledger (24 actions each: trades with "
                       "necessity/harm draws plus grants; gate-rejections "
                       "count too)",
             "law": "conserved_total = sum(account.credit) + reserve is "
                    "invariant under every approved or rejected action "
                    "(spec gate 6)",
             "measured_on": "credit_commons.web.ledger.Ledger (sqlite), "
                            "deterministic rng per sequence",
             "tolerance": 1e-6,
             "note": "credit_commons.sim.Commons.grant mints credit without "
                     "debiting reserve and so is NOT covered by this law"},
            lambda s: invariant_holds(s, conserved_metric), seeds),
        lc.certify_statement(
            "L14_bad_credit_sum_invariant",
            {"domain": "same 30 seeded action-sequences on the same ledger",
             "law": "FLAWED CANDIDATE: sum(account.credit) alone (no "
                    "reserve) is invariant -- reserve absorbs fee residue "
                    "and pays out grants",
             "honest_check": "must fail on sequences where fee residue "
                             "reached the reserve or a grant was issued"},
            lambda s: invariant_holds(s, credit_metric), seeds),
    ] + calendar_certificates()


def full_table():
    """Lab certificates + real-subsystem statements + T2 proposer
    certificates + the discovery agent's collected laws (the complete,
    self-reproducing gate table)."""
    from experiments.emanation import law_checker as lc
    from experiments.emanation import law_proposer as lp
    from experiments.emanation import law_discovery as ldd
    return (lc.all_certificates() + system_certificates()
            + lp.proposer_certificates() + ldd.discovery_certificates())


def fresh_table_matches(path=_CERTS):
    """Audit-the-audit: does the persisted table equal a fresh recompute?
    Returns (ok, drift_labels)."""
    with open(path, encoding="utf-8") as fh:
        persisted = json.load(fh)
    by_label = {c["label"]: c for c in persisted}
    fresh = full_table()
    drift = []
    for c in fresh:
        p = by_label.get(c["label"])
        if p is None:
            drift.append("missing: " + c["label"])
        elif (p.get("status") != c["status"]
              or p.get("first_mismatch") != c.get("first_mismatch")
              or p.get("first_failure") != c.get("first_failure")
              or p.get("n_fail") != c.get("n_fail")
              or p.get("n_ok") != c.get("n_ok")):
            drift.append("drifted: " + c["label"])
    fresh_labels = {c["label"] for c in fresh}
    for lbl in by_label:
        if lbl not in fresh_labels:
            drift.append("stale: " + lbl)
    return len(drift) == 0, drift


def write_full_table(path=_CERTS):
    table = full_table()
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(table, fh, indent=1, sort_keys=True)
    return path


if __name__ == "__main__":
    import sys
    ok, drift = fresh_table_matches()
    if not ok:
        print("certificate table drift detected:")
        for d in drift:
            print("  - " + d)
        sys.exit(1)
    print("certificate table fresh: %d certificates, no drift"
          % len(full_table()))