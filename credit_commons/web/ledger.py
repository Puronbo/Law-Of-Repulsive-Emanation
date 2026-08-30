"""Persistent SQLite ledger for the Credit-Commons pilot.

Encodes the *same* validated rules as `credit_commons.sim` but persists state
(accounts, credits, trust, ledger, reserve) to SQLite and enforces each trade
atomically inside a transaction, so a real browser/mobile pilot can run against
it. Conservation (sum(credit)+reserve == total_credit) is enforced on every
trade — a live assertion of spec gate 6.
"""

from __future__ import annotations

import hashlib
import os
import secrets
import sqlite3
import time

from credit_commons.sim import Params


class Ledger:
    def __init__(self, path: str, params: Params | None = None):
        self.path = path
        self.p = params or Params()
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()
        self._seed_epoch()

    # -- schema ------------------------------------------------------------
    def _init_schema(self):
        c = self.conn
        c.executescript(
            """
            CREATE TABLE IF NOT EXISTS accounts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                handle TEXT UNIQUE NOT NULL,
                pin_hash TEXT NOT NULL,
                tier TEXT NOT NULL DEFAULT 'individual',
                credit REAL NOT NULL DEFAULT 0,
                trust REAL NOT NULL DEFAULT 0,
                irrev REAL NOT NULL DEFAULT 0,
                necess REAL NOT NULL DEFAULT 0,
                created REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS ledger(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts REAL NOT NULL,
                kind TEXT NOT NULL,
                buyer INTEGER,
                seller INTEGER,
                x REAL,
                fee REAL,
                necessity INTEGER,
                note TEXT
            );
            CREATE TABLE IF NOT EXISTS meta(
                k TEXT PRIMARY KEY, v TEXT
            );
            """
        )
        c.commit()

    def _seed_epoch(self):
        """Spec §7: a single documented genesis timestamp anchors time-slots."""
        cur = self.conn.execute("SELECT v FROM meta WHERE k='genesis'")
        if cur.fetchone() is None:
            epoch = time.time()
            self.conn.execute("INSERT INTO meta(k,v) VALUES('genesis', ?)",
                              (str(epoch),))
            self.conn.commit()
        row = self.conn.execute("SELECT v FROM meta WHERE k='genesis'").fetchone()
        self.genesis = float(row["v"])

    # -- meta / totals -----------------------------------------------------
    def account_credit(self, acc_id):
        row = self.conn.execute(
            "SELECT credit, trust, irrev, necess FROM accounts WHERE id=?",
            (acc_id,)).fetchone()
        return row

    def accounts_sum(self):
        row = self.conn.execute("SELECT COALESCE(SUM(credit),0) FROM accounts").fetchone()
        return row[0]

    @property
    def total_credit(self):
        # circulation = credit in accounts (the "money")
        return self.accounts_sum()

    @property
    def reserve(self):
        # reserve = seed-created surplus not yet granted; maintained explicitly
        row = self.conn.execute("SELECT v FROM meta WHERE k='reserve'").fetchone()
        return float(row["v"]) if row else 0.0

    def conserved_total(self):
        """The invariant: accounts' credit + reserve. A trade or grant must
        leave this unchanged (gate 6); only a seed (external Phase-0 inflow)
        may grow it."""
        return self.accounts_sum() + self.reserve

    # -- accounts ----------------------------------------------------------
    def create_account(self, handle, pin, tier="individual",
                       seed_credit=None, seed_trust=None):
        """Phase 0 seed (capped). Returns (id, ok, message)."""
        if self.conn.execute("SELECT 1 FROM accounts WHERE handle=?",
                             (handle,)).fetchone():
            return None, False, "handle already exists"
        if seed_credit is None:
            seed_credit = self.p.seed_credit
        if seed_trust is None:
            seed_trust = self.p.seed_trust
        pin_hash = self._hash(pin, handle)
        cur = self.conn.execute(
            "INSERT INTO accounts(handle,pin_hash,tier,credit,trust,created) "
            "VALUES(?,?,?,?,?,?)",
            (handle, pin_hash, tier, seed_credit, seed_trust, time.time()))
        self.conn.commit()
        return cur.lastrowid, True, "created"

    def verify_pin(self, handle, pin):
        row = self.conn.execute(
            "SELECT id, pin_hash FROM accounts WHERE handle=?", (handle,)).fetchone()
        if row is None:
            return None
        if self._hash(pin, handle) != row["pin_hash"]:
            return None
        return row["id"]

    @staticmethod
    def _hash(pin, handle):
        return hashlib.sha256(f"{handle}:{pin}".encode()).hexdigest()

    # -- the atomic trade ---------------------------------------------------
    def trade(self, buyer_id, seller_id, x, necessity=False, terminal=None,
              committed_harm=0.0):
        """Atomic, conserved trade. Returns (ok, dict)."""
        p = self.p
        if x <= 0:
            return False, {"reason": "non-positive quantity"}
        with self.conn:
            b = self.conn.execute("SELECT * FROM accounts WHERE id=?",
                                  (buyer_id,)).fetchone()
            s = self.conn.execute("SELECT * FROM accounts WHERE id=?",
                                  (seller_id,)).fetchone()
            if b is None or s is None:
                return False, {"reason": "unknown account"}

            bcredit = b["credit"]; btrust = b["trust"]
            scredit = s["credit"]

            # gate (§5): necessity draws against a protected ceiling, otherwise
            # against full trust ceiling.
            if necessity:
                ceiling = btrust * p.necessity_ceiling
                if bcredit - x < -ceiling:
                    return False, {"reason": "beyond necessity-protection ceiling"}
            else:
                if bcredit - x < -btrust * p.max_leverage:
                    return False, {"reason": "credit would exceed trust ceiling"}

            fee = p.f * x

            before = self.conserved_total()

            # committed harm (§5.6): irreversible scar (I), never erasable.
            if committed_harm > 0:
                harm = p.I * committed_harm
                self.conn.execute("UPDATE accounts SET irrev=irrev+?, trust=trust-? "
                                  "WHERE id=?", (harm, harm, buyer_id))
                btrust -= harm

            # debit/credit (conserved)
            new_bcredit = bcredit - x
            # necessity E1: rebuild trust; discretionary: progressive draw-down
            if necessity:
                self.conn.execute("UPDATE accounts SET necess=necess+? WHERE id=?",
                                  (x, buyer_id))
                new_btrust = btrust + p.n * x
            else:
                depth = max(0.0, -bcredit) / max(btrust, 1e-9) if btrust > 0 else 1.0
                new_btrust = btrust - p.g_at(depth) * x

            new_scredit = scredit + x - fee
            seller_trust = s["trust"] + p.reward() * x

            self.conn.execute(
                "UPDATE accounts SET credit=?, trust=? WHERE id=?",
                (new_bcredit, max(0.0, new_btrust), buyer_id))
            self.conn.execute(
                "UPDATE accounts SET credit=?, trust=? WHERE id=?",
                (new_scredit, seller_trust, seller_id))

            # reserve keeps the unallocated fee (conservation), not minted.
            self._credit_reserve(fee - self._distribute_fee(
                fee, buyer_id, terminal))

            self.conn.execute(
                "INSERT INTO ledger(ts,kind,buyer,seller,x,fee,necessity,note) "
                "VALUES(?,?,?,?,?,?,?,?)",
                (time.time(), "trade", buyer_id, seller_id, x, fee,
                 1 if necessity else 0,
                 f"harm={committed_harm}" if committed_harm else ""))

            # post-trade conservation assertion (gate 6)
            after = self.conserved_total()
            if abs(after - before) > 1e-6:
                self.conn.rollback()
                return False, {"reason": "conservation violated"}
        return True, {"fee": fee, "x": x}

    def _distribute_fee(self, fee, buyer_id, terminal):
        """E3: use-side consumer floor; remainder elsewhere(token) or reserve."""
        p = self.p
        floor_val = fee * p.consumer_floor
        self.conn.execute("UPDATE accounts SET credit=credit+? WHERE id=?",
                          (floor_val, buyer_id))
        allocated = floor_val
        if terminal is not None:
            rem = fee - floor_val
            t_amt = rem * p.terminal_share
            self.conn.execute("UPDATE accounts SET credit=credit+? WHERE id=?",
                              (t_amt, terminal))
            allocated += t_amt
        return allocated

    def _credit_reserve(self, amount):
        self.conn.execute(
            "INSERT INTO meta(k,v) VALUES('reserve', ?) "
            "ON CONFLICT(k) DO UPDATE SET v=CAST(v AS REAL)+?",
            (str(amount), amount))

    def grant(self, recipient_id, amount, sponsor_id=None):
        """Phase 2 progressive grant funded from the reserve. The full granted
        amount (after progressive scaling) is debited from reserve, so credit is
        conserved (the progressive bonus is funded, not minted)."""
        with self.conn:
            row = self.conn.execute("SELECT credit,trust FROM accounts WHERE id=?",
                                    (recipient_id,)).fetchone()
            if row is None:
                return False, "unknown recipient"
            scale = 1.0 + self.p.grant_bias / max(1e-9, 1.0 + row["trust"])
            amt = amount * scale
            if self.reserve < amt:
                return False, "insufficient reserve"
            before = self.conserved_total()
            self.conn.execute("UPDATE accounts SET credit=credit+?, trust=trust+? "
                              "WHERE id=?", (amt, 0.05 * amt, recipient_id))
            # reserve funds the full granted amount (conservation)
            self.conn.execute(
                "INSERT INTO meta(k,v) VALUES('reserve', ?) "
                "ON CONFLICT(k) DO UPDATE SET v=CAST(v AS REAL)-?",
                (str(amt), amt))
            self.conn.execute(
                "INSERT INTO ledger(ts,kind,buyer,seller,x,fee,necessity,note) "
                "VALUES(?,?,?,?,?,?,?,?)",
                (time.time(), "grant", sponsor_id, recipient_id, amt, 0, 0, ""))
            after = self.conserved_total()
            if abs(after - before) > 1e-6:
                self.conn.rollback()
                return False, "conservation violated"
        return True, amt

    # -- audit --------------------------------------------------------------
    def ledger_rows(self, limit=100):
        cur = self.conn.execute(
            "SELECT * FROM ledger ORDER BY id DESC LIMIT ?", (limit,))
        return cur.fetchall()

    def all_accounts(self):
        cur = self.conn.execute(
            "SELECT id, handle, tier, credit, trust, irrev, necess FROM accounts "
            "ORDER BY id")
        return cur.fetchall()

    def close(self):
        self.conn.close()
