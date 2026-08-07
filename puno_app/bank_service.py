"""BankService: headless driver around the Decentral Bank socket network.

This is the application layer the dashboard drives (mirrors how ``NetworkApp``
sits under ``canned_ui`` for the toy lab).  It owns one ``SocketNetwork`` (the
T70/T71 driver), a set of accounts with keys + balances, and a single pump
loop that continuously drains the driver's result queue so transactions
commit asynchronously while a live state snapshot is refreshed for the UI.

The service is the only transaction source, so it can track balances and
nonces deterministically: every committed CLIENT_RESULT debits the sender
and credits the recipient, matching the ledger replay exactly.

Run the HTTP layer with ``python -m puno_app.bank_server``.
"""

import os
import sys
import threading
import time
from collections import defaultdict, deque

_EXP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "experiments")
_UNI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Universals")
for _p in (_EXP, _UNI):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from decentral_bank_net import (  # noqa: E402
    SOCK_HOST, SocketNetwork, make_accounts, make_tx, replay_from,
    consensus_heads)

EVENT_LOG_MAX = 200
SNAP_INTERVAL = 1.0          # seconds between live state snapshots
SNAP_TIMEOUT = 2.5           # per-snapshot wait for node STATE replies


class BankService:
    """One live Decentral Bank network + accounts + a background pump loop.

    Construction is intentionally NOT at module import time: starting a
    ``SocketNetwork`` spawns child processes, and a Windows ``spawn`` child
    re-imports ``__main__``.  Always build inside ``main()``.
    """

    def __init__(self, n_frag=6, k=3, vote_timeout=0.8, n_accounts=24,
                 min_balance=100, wal_dir=None, tls=False, host=SOCK_HOST):
        self.lock = threading.RLock()
        self.n_frag = n_frag
        self.k = k
        self.vote_timeout = vote_timeout
        self.n_accounts = n_accounts
        self.min_balance = min_balance
        self.host = host
        self._wal_dir = wal_dir
        self._tls = tls

        self.net = SocketNetwork(n_frag, k, vote_timeout=vote_timeout,
                                 wal_dir=wal_dir, tls=tls, host=host)
        self.witnesses = self.net.witnesses
        self._frag_for, self._keys, self.addrs = make_accounts(
            self.net.net, n_accounts)
        self._balances = {a: min_balance for a in self.addrs}
        self._nonces = defaultdict(int)
        self._pending = {}            # cid -> tx
        self._cid = 0
        self._event_log = deque(maxlen=EVENT_LOG_MAX)
        self._snapshot = None         # ordered list of per-node views or None
        self._committed = 0
        self._denied = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._pump, daemon=True)
        self._thread.start()
        self._log("network up: n=%d k=%d accounts=%d balance=%d"
                  % (n_frag, k, n_accounts, min_balance))

    # ------------------------------------------------------------------ #
    # pump loop
    # ------------------------------------------------------------------ #
    def _pump(self):
        next_snap = time.time() + SNAP_INTERVAL
        while not self._stop.is_set():
            try:
                self._drain()
                now = time.time()
                if now >= next_snap:
                    self._snapshot_once()
                    next_snap = now + SNAP_INTERVAL
            except Exception:
                # never let the pump die: a broken snapshot/relay must not
                # take down the live status feed
                import traceback
                traceback.print_exc()
            time.sleep(0.03)

    def _drain(self):
        """Read every queued result without blocking."""
        net = self.net
        while True:
            try:
                msg = net.result_q.get_nowait()
            except Exception:
                break
            kind = msg[0]
            if kind == "CLIENT_RESULT":
                self._on_client_result(msg[1], msg[2], msg[3])
            elif kind == "STATE":
                cid, snap = msg[1], msg[2]
                self._snap_replies[cid] = {int(k): v for k, v in snap.items()}

    def _on_client_result(self, cid, ok, why):
        tx = self._pending.pop(cid, None)
        if tx is None:
            return
        if ok:
            self._balances[tx["from"]] -= tx["amount"]
            self._balances[tx["to"]] += tx["amount"]
            self._committed += 1
            self._log("commit  %s -> %s  %d"
                      % (tx["from"][:8], tx["to"][:8], tx["amount"]))
        else:
            self._denied += 1
            self._log("denied  %s  (%s)" % (tx["from"][:8], why))

    def _snapshot_once(self):
        """Query every node's full view; a dead node simply doesn't reply."""
        net = self.net
        cids = ["live%d" % i for i in range(self.n_frag)]
        self._snap_replies = {}
        for i in range(self.n_frag):
            net._send(i, "QUERY_STATE", (cids[i],))
        deadline = time.time() + SNAP_TIMEOUT
        while time.time() < deadline and len(self._snap_replies) < self.n_frag:
            self._drain()
            time.sleep(0.02)
        with self.lock:
            self._snapshot = [self._snap_replies.get(c) for c in cids]

    # ------------------------------------------------------------------ #
    # operations
    # ------------------------------------------------------------------ #
    def submit(self, from_idx, to_idx, amount):
        """Submit a signed transfer; returns (cid, tx) or raises ValueError."""
        amount = int(amount)
        if amount <= 0:
            raise ValueError("amount must be positive")
        if from_idx == to_idx:
            raise ValueError("sender and recipient must differ")
        with self.lock:
            if not (0 <= from_idx < len(self.addrs)
                    and 0 <= to_idx < len(self.addrs)):
                raise ValueError("account index out of range")
            sender = self.addrs[from_idx]
            if self._balances[sender] < amount:
                raise ValueError("insufficient balance (%d < %d)"
                                 % (self._balances[sender], amount))
            nonce = self._nonces[sender] + 1
            self._nonces[sender] = nonce
            tx = make_tx(self._keys, sender, self.addrs[to_idx], amount,
                         nonce=nonce)
            cid = "t%d" % self._cid
            self._cid += 1
            self._pending[cid] = tx
            self.net.submit(tx, cid)
            return cid, tx

    def kill(self, node_id):
        self.net.kill(node_id)
        self._log("kill   node %d" % node_id)

    def restart(self, node_id):
        self.net.restart(node_id)
        self._log("restart node %d (stateless, recovers from peers)" % node_id)

    def kill_all(self):
        self.net.kill_all()
        self._log("kill-all: total simultaneous crash (WAL is the only state)")

    def restart_all(self):
        self.net.restart_all()
        self._log("restart-all: WAL reload + RESYNC rebuild of the fabric")

    def partition(self, groups):
        groups = [list(map(int, g)) for g in groups]
        self.net.set_partition(groups)
        self._log("partition %s" % [sorted(g) for g in groups])

    def full_network(self):
        self.net.full_network()
        self._log("full network restored")

    def resync(self, node_id=None):
        if node_id is None:
            self.net.resync_all()
            self._log("resync-all")
        else:
            self.net.resync(node_id)
            self._log("resync node %d" % node_id)

    def rebuild(self, n_frag=None, k=None, vote_timeout=None, n_accounts=None,
                min_balance=None, tls=None):
        """Tear down and build a fresh network with the given parameters."""
        with self.lock:
            old = self.net
            old.stop()
            self.n_frag = int(n_frag) if n_frag else self.n_frag
            self.k = int(k) if k else self.k
            self.vote_timeout = (float(vote_timeout) if vote_timeout
                                 else self.vote_timeout)
            self.n_accounts = int(n_accounts) if n_accounts else self.n_accounts
            self.min_balance = (int(min_balance) if min_balance
                                else self.min_balance)
            self._tls = bool(tls) if tls is not None else self._tls
            self.net = SocketNetwork(self.n_frag, self.k,
                                     vote_timeout=self.vote_timeout,
                                     wal_dir=self._wal_dir,
                                     tls=self._tls, host=self.host)
            self.witnesses = self.net.witnesses
            self._frag_for, self._keys, self.addrs = make_accounts(
                self.net.net, self.n_accounts)
            self._balances = {a: self.min_balance for a in self.addrs}
            self._nonces = defaultdict(int)
            self._pending = {}
            self._committed = 0
            self._denied = 0
            self._snapshot = None
            self._log("rebuild: n=%d k=%d vote_timeout=%.2f accounts=%d tls=%s"
                      % (self.n_frag, self.k, self.vote_timeout,
                         self.n_accounts, self._tls))

    # ------------------------------------------------------------------ #
    # views
    # ------------------------------------------------------------------ #
    def _live_nodes(self):
        return [self.net.procs[i].is_alive() for i in range(self.n_frag)]

    def status(self):
        with self.lock:
            snap = self._snapshot
            alive = self._live_nodes()
            consensus, frag_blocks = None, None
            if snap:
                frag_heads = {f: set() for f in range(self.n_frag)}
                frag_blocks = {}
                for view in snap:
                    if not view:
                        continue
                    for f in range(self.n_frag):
                        if f in view:
                            frag_heads[f].add(view[f]["head"])
                            frag_blocks[f] = len(view[f]["blocks"])
                consensus = {f: len(h) == 1 for f, h in frag_heads.items()}
                consensus = {f: (c if f in frag_heads else None)
                             for f, c in consensus.items()}
            n_blocks = (sum(frag_blocks.values()) if frag_blocks else 0)
            return {
                "ok": True,
                "n_frag": self.n_frag,
                "k": self.k,
                "vote_timeout": self.vote_timeout,
                "n_accounts": self.n_accounts,
                "min_balance": self.min_balance,
                "tls": self._tls,
                "host": self.host,
                "nodes_alive": alive,
                "alive_count": sum(alive),
                "witnesses": self.witnesses,
                "snapshot_ready": snap is not None,
                "consensus": consensus,
                "frag_blocks": frag_blocks,
                "total_blocks": n_blocks,
                "committed": self._committed,
                "denied": self._denied,
                "pending": len(self._pending),
                "balance_total": sum(self._balances.values()),
                "balance_expected": len(self.addrs) * self.min_balance,
                "conserved": abs(sum(self._balances.values())
                                 - len(self.addrs) * self.min_balance) < 1e-9,
                "event_log": list(self._event_log),
            }

    def accounts(self):
        with self.lock:
            return [{
                "idx": i,
                "addr": a,
                "short": a[:10],
                "owner": int(self._frag_for[a]),
                "balance": self._balances[a],
            } for i, a in enumerate(self.addrs)]

    def ledgers(self, node_id=0):
        """Full chain view for every fragment as seen by one node."""
        with self.lock:
            snap = self._snapshot
            if not snap or node_id >= len(snap) or not snap[node_id]:
                return None
            return snap[node_id]

    def validate_all(self):
        """Replay the union of ledgers from the first responding node and
        report chain validity + conservation (the harness's T12 check)."""
        with self.lock:
            snap = self._snapshot
            if not snap:
                return None
            view = next((v for v in snap if v), None)
            if view is None:
                return None
            valid, conserved = replay_from(
                {"ref": view}, self.n_frag, self.addrs,
                min_balance=self.min_balance)
            return {"chains_valid": valid, "conserved": conserved,
                    "n_frag": self.n_frag,
                    "accounts": len(self.addrs)}

    # ------------------------------------------------------------------ #
    def _log(self, text):
        self._event_log.append("[%s] %s"
                               % (time.strftime("%H:%M:%S"), text))

    def stop(self):
        self._stop.set()
        self._thread.join(timeout=2)
        self.net.stop()
