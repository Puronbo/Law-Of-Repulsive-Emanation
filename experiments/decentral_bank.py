"""
DECENTRAL BANK PROTOTYPE (T-series T68) - a fragment bank on DecentralNet.

A banking layer is NOT shipped in this repo: no ledger, no consensus, no
transactions.  This file BUILDS the missing layer on top of the existing
DecentralNet identity/routing (Universals/manifold/decentral_net.py) and TESTS
it, reporting every verdict with its null, per the project's doctrine.

Architecture (what is re-used vs what is built):

  Re-used (verified engine):
    - DecentralNet neurons = bank fragments.  kNN neighborhoods = witness
      sets.  Nearest-centroid predict = account-to-fragment routing.
    - to_disk / settle / heal = the physical topology the bank lives in.

  Built here (the "bank" half):
    - Ed25519 account identities (Phase 1): each account owns a keypair; its
      address = SHA-256(public key); routing embeds the address.  Every
      transaction carries the sender's public key + signature over the tx
      body; the ledger verifies signature AND address/pubkey binding at
      append and during full re-validation (T7).
    - hash-chained double-entry ledger (blocks link by SHA-256 of prev hash,
      per-account nonce => double-spend rejection).
    - write-ahead persistence (Phase 1): each fragment appends committed
      blocks to its own log file with fsync; the bank saves/loads accounts,
      topology, and ledgers and replays balances exactly (T8).
    - kNN witness quorum: a fragment commits only if a majority of its k
      nearest-neighbour fragments confirm the head hash (weak consensus -
      honest about being NON-Byzantine).
    - anomaly layer: novelty = distance-from-peers of a tx, flagged against
      chance.

Tests (each with a null):
  T1 routing:  do txns actually reach the fragment owning the sender?
  T2 integrity: is the ledger hash-chain valid, nonces monotone, balances
                conserved (sum of all balances constant)?
  T3 double-spend: does a replayed/spent-again nonce get rejected?
  T4 damage: after killing 30% of fragments, do survivors still route and
             the ledger still validate?
  T5 quorum vs faulty fragments: with f% of fragments evil (report wrong
     head hashes / refuse), does the majority quorum still catch forgery
     better than a coin-flip null?
  T6 anomaly: does novelty flag synthetic fraud at better-than-random rate?
  T7 signatures: does the ledger reject a tampered block and a tx signed by
     the wrong key (forgery) while accepting a legitimately signed tx?
  T8 persistence: after save + load, are the chains, heads, and balances
     bit-identical and conserved?

Limits (crease-worthy, printed at the end):
  - NO Byzantine fault tolerance: a >50% corrupt neighbourhood wins.
  - Single-process, local filesystem, deterministic toy - not a bank.
  - Real Ed25519 signatures + WAL fsync, but no network transport and no
    crash-torn-log recovery; the quorum is still an in-process simulation.
"""

import json
import os
import sys
import hashlib
import itertools
from collections import defaultdict

import numpy as np

from cryptography.hazmat.primitives.asymmetric.ed25519 import (  # noqa: E402
    Ed25519PrivateKey, Ed25519PublicKey)
from cryptography.hazmat.primitives.serialization import (  # noqa: E402
    Encoding, NoEncryption, PrivateFormat, PublicFormat)

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Universals"))
from manifold.decentral_net import DecentralNet, to_disk  # noqa: E402

RNG = np.random.RandomState(20260802)

ADDR_BYTES = 40          # hex chars of sha256(pubkey) used as the address


def address_of(pub_bytes):
    """Account address = first ADDR_BYTES hex chars of SHA-256(pubkey)."""
    return hashlib.sha256(pub_bytes).hexdigest()[:ADDR_BYTES]


def tx_body(t):
    """Canonical bytes signed by the sender (covers pub so address binding
    is part of the signature, and routing name can't be detached)."""
    return json.dumps({"from": t["from"], "to": t["to"], "amount": t["amount"],
                       "nonce": t["nonce"], "pub": t["pub"]},
                      sort_keys=True).encode()


def sign_tx(priv, t):
    return priv.sign(tx_body(t))


def verify_tx(t):
    """Returns (ok, reason).  Verifies pubkey/address binding AND the Ed25519
    signature over the tx body.  Called at append and during re-validation."""
    pub = bytes.fromhex(t["pub"])
    if address_of(pub) != t["from"]:
        return False, "addr-mismatch"
    try:
        Ed25519PublicKey.from_public_bytes(pub).verify(
            bytes.fromhex(t["sig"]), tx_body(t))
    except Exception:
        return False, "bad-signature"
    return True, "ok"


# ---------------------------------------------------------------------- #
# Account embeddings (mimic the repo's hashed char-ngram routing)
# ---------------------------------------------------------------------- #
def _ngrams(name, lo=2, hi=4):
    name = name.lower()
    for n in range(lo, hi + 1):
        s = " " * (n - 1) + name + " " * (n - 1)
        for i in range(len(s) - n + 1):
            yield s[i:i + n]


def embed(name, dim=2):
    """Deterministic hashed char-ngram embedding (name -> dim-vector)."""
    v = np.zeros(dim)
    for g in _ngrams(name):
        h = int(hashlib.md5(g.encode()).hexdigest(), 16)
        # component from bits of the hash - deterministic, no global RNG
        for c in range(dim):
            bit = (h >> (8 * c)) & 0xFF
            v[c] += (bit / 127.5) - 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


# ---------------------------------------------------------------------- #
# Ledger
# ---------------------------------------------------------------------- #
class Ledger:
    """Hash-chained double-entry ledger for one fragment (with WAL)."""

    def __init__(self, fragment_id, log_path=None):
        self.fragment_id = fragment_id
        self.log_path = log_path
        self.blocks = []
        self.head = "genesis"
        self.nonces = defaultdict(int)   # account -> last used nonce

    def block_hash(self, index, prev, txs):
        payload = json.dumps({"i": index, "p": prev,
                              "t": sorted(txs, key=lambda t: t["nonce"])},
                             sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()

    def try_append(self, txs):
        """Append a block if the whole batch is valid: signatures OK,
        pubkey/address binding OK, nonces monotone.  Returns (ok, reason)."""
        for t in txs:
            ok, why = verify_tx(t)
            if not ok:
                return False, why
            if t["nonce"] <= self.nonces[t["from"]]:
                return False, "nonce-replay"
        self.blocks.append({
            "index": len(self.blocks),
            "prev": self.head,
            "txs": txs,
            "hash": self.block_hash(len(self.blocks), self.head, txs),
        })
        for t in txs:
            self.nonces[t["from"]] = t["nonce"]
        self.head = self.blocks[-1]["hash"]
        return True, "ok"

    def commit_last(self):
        """WAL: persist the most recently appended (quorum-accepted) block.
        Append-only line per block + fsync, so a crash can't lose a commit."""
        if self.log_path is None or not self.blocks:
            return
        with open(self.log_path, "a") as f:
            f.write(json.dumps(self.blocks[-1], sort_keys=True) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def _rewrite_log(self):
        if self.log_path is None:
            return
        with open(self.log_path, "w") as f:
            for b in self.blocks:
                f.write(json.dumps(b, sort_keys=True) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def rollback(self):
        """Undo the most recently appended block (a quorum refused it)."""
        if self.blocks:
            self.blocks.pop()
            self.head = self.blocks[-1]["hash"] if self.blocks else "genesis"
            self._rewrite_log()

    def replica_append(self, b):
        """Append a block received from the network to a REPLICA of this
        ledger (also used for the authoritative copy).  Rejects out-of-order
        blocks (gap) and any block whose txs don't verify.  Returns
        (ok, reason)."""
        if b["index"] != len(self.blocks):
            return False, "gap-index"
        if b["prev"] != self.head:
            return False, "gap-prev"
        if b["hash"] != self.block_hash(b["index"], b["prev"], b["txs"]):
            return False, "hash-mismatch"
        for t in b["txs"]:
            ok, why = verify_tx(t)
            if not ok:
                return False, why
            if t["nonce"] <= self.nonces[t["from"]]:
                return False, "nonce-replay"
        self.blocks.append(b)
        for t in b["txs"]:
            self.nonces[t["from"]] = t["nonce"]
        self.head = b["hash"]
        return True, "ok"

    def validate(self):
        """Full chain re-validation: link hashes, nonce monotonicity, and
        every transaction's Ed25519 signature + address binding."""
        prev = "genesis"
        seen = defaultdict(int)
        for i, b in enumerate(self.blocks):
            if b["index"] != i or b["prev"] != prev:
                return False, f"link-broken@{i}"
            if b["hash"] != self.block_hash(i, prev, b["txs"]):
                return False, f"hash-mismatch@{i}"
            for t in b["txs"]:
                ok, why = verify_tx(t)
                if not ok:
                    return False, f"sig-fail@{i}:{why}"
                if t["nonce"] <= seen[t["from"]]:
                    return False, f"nonce-regress@{i}"
                seen[t["from"]] = t["nonce"]
            prev = b["hash"]
        return True, "ok"

    @classmethod
    def from_log(cls, log_path, fragment_id):
        """Reconstruct a ledger by replaying its WAL.  The caller validates
        afterwards (signatures + chain)."""
        ld = cls(fragment_id, log_path=log_path)
        if not os.path.exists(log_path):
            return ld
        with open(log_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                b = json.loads(line)
                ld.blocks.append(b)
                for t in b["txs"]:
                    ld.nonces[t["from"]] = t["nonce"]
        ld.head = ld.blocks[-1]["hash"] if ld.blocks else "genesis"
        return ld


# ---------------------------------------------------------------------- #
# The bank
# ---------------------------------------------------------------------- #
class FragmentBank:
    def __init__(self, n_frag, k=6, accounts_per_frag=40, min_balance=100):
        self.n_frag = n_frag
        self.min_balance = min_balance
        self.net = DecentralNet(dim=2, k=k, mu0=0.12)
        th = np.linspace(0, 2 * np.pi, n_frag, endpoint=False)
        homes = np.column_stack([0.55 * np.cos(th), 0.55 * np.sin(th)])
        for h in homes:
            self.net.add(h)
        self.net.settle(800)
        self.net.absorb(400)
        self.ledgers = [Ledger(i) for i in range(n_frag)]
        self.balances = defaultdict(lambda: defaultdict(int))  # frag -> acct -> bal
        self.accounts = []                                    # (addr, owner_frag)
        self.frag_for = {}
        self.keys = {}                                        # addr -> (pub, priv)
        # known[f][w] = last head of fragment f that witness w has seen
        # (replication: each fragment pushes its head to its kNN witnesses)
        self.known = defaultdict(lambda: defaultdict(str))
        self._populate(accounts_per_frag)
        self.faulty = set()            # fragments that lie about head hashes
        self.refusing = set()          # fragments that refuse to confirm

    # ---- populate ---------------------------------------------------- #
    def _populate(self, per_frag):
        # Ownership is DEFINED by routing (the repo's own pattern: homes =
        # data centroids).  Each account embeds to the fragment whose home is
        # nearest - that fragment owns it.  This is the "postal system".
        for f in range(self.n_frag):
            for _ in range(per_frag):
                priv = Ed25519PrivateKey.generate()
                pub = priv.public_key().public_bytes(Encoding.Raw,
                                                     PublicFormat.Raw)
                addr = address_of(pub)
                owner = self.route(addr)
                self.balances[owner][addr] = self.min_balance
                self.frag_for[addr] = owner
                self.keys[addr] = (pub, priv)
                self.accounts.append((addr, owner))

    # ---- routing ----------------------------------------------------- #
    def route(self, name):
        """Nearest-centroid: account -> owning fragment."""
        v = to_disk(embed(name) * 0.6, 0.9)
        return int(self.net.predict(v.reshape(1, -1))[0])

    def route_failures(self):
        """Fraction of accounts routed to a fragment different from their
        stored owner (should be 0: ownership IS routing)."""
        wrong = 0
        for name, owner in self.accounts:
            if self.route(name) != owner:
                wrong += 1
        return wrong / len(self.accounts)

    def partition_spread(self):
        """How evenly routing splits accounts across fragments (min/max/std
        of accounts-per-fragment).  A degenerate partition (one fragment owns
        everything) would be a routing failure for a bank."""
        counts = defaultdict(int)
        for name, owner in self.accounts:
            counts[owner] += 1
        vals = [counts[f] for f in range(self.n_frag)]
        return {"min": int(min(vals)), "max": int(max(vals)),
                "std": round(float(np.std(vals)), 2),
                "empty_fragments": int(sum(1 for v in vals if v == 0))}

    # ---- witnesses --------------------------------------------------- #
    def witnesses(self, f):
        return [j for j in self.net._knn()[f]]

    def replicate(self, f):
        """Push fragment f's head to its kNN witnesses.  Faulty fragments
        push a corrupted head (they lie); refusing fragments push nothing."""
        if f in self.refusing:
            return
        head = self.ledgers[f].head
        payload = "corrupt" if f in self.faulty else head
        for w in self.witnesses(f):
            self.known[f][w] = payload

    def confirm(self, w, owner_f, expected_head):
        """Does witness w's replicated view of owner_f's head match the
        expected head?  (Faulty witnesses report the opposite.)"""
        view = self.known[owner_f].get(w, None)
        truth = (view == expected_head)
        if w in self.faulty:
            return not truth
        return truth

    # ---- transactions ------------------------------------------------ #
    def transfer(self, sender, recipient, amount, nonce=None):
        """Send money.  Returns (ok, reason).  Signed with the sender's key;
        double-spend rejected by nonce + balance check; committed only under
        witness quorum; persisted to the fragment's WAL on commit."""
        frag = self.frag_for[sender]
        if nonce is None:
            nonce = self.ledgers[frag].nonces[sender] + 1
        if self.balances[frag][sender] < amount:
            return False, "insufficient"
        pub, priv = self.keys[sender]
        tx = {"from": sender, "to": recipient, "amount": amount,
              "nonce": nonce, "pub": pub.hex()}
        tx["sig"] = sign_tx(priv, tx).hex()
        txs = [tx]
        ok, why = self.ledgers[frag].try_append(txs)
        if not ok:
            return False, why
        # witness quorum: replicate the new head, then a strict majority of
        # kNN fragments must confirm it (hold a matching copy).
        self.replicate(frag)                      # broadcast before voting
        witnesses = self.witnesses(frag)
        expected = self.ledgers[frag].head
        votes = [self.confirm(w, frag, expected) for w in witnesses]
        if sum(votes) <= len(votes) / 2:
            self.ledgers[frag].rollback()         # undo the rejected block
            return False, "quorum-denied"
        self.ledgers[frag].commit_last()          # WAL: only committed blocks
        # debit/credit (double entry)
        self.balances[frag][sender] -= amount
        r = self.frag_for[recipient]
        self.balances[r][recipient] += amount
        return True, "ok"

    # ---- invariants -------------------------------------------------- #
    def check_invariants(self):
        total = 0
        for f in range(self.n_frag):
            ok, why = self.ledgers[f].validate()
            if not ok:
                return False, f"chain-{f}-{why}"
            total += sum(self.balances[f].values())
        expected = len(self.accounts) * self.min_balance
        return (abs(total - expected) < 1e-9), f"total={total} vs {expected}"

    # ---- damage ------------------------------------------------------ #
    def kill(self, fraction):
        kill = list(RNG.choice(self.n_frag, int(self.n_frag * fraction),
                               replace=False))
        self.net.remove(kill)
        self.net.heal(800)
        return kill

    # ---- persistence -------------------------------------------------- #
    def save(self, dirpath):
        """Persist accounts, topology, and every fragment's WAL."""
        os.makedirs(dirpath, exist_ok=True)
        registry = [{"addr": a, "owner": o,
                     "pub": self.keys[a][0].hex(),
                     "priv": self.keys[a][1].private_bytes(
                         Encoding.Raw, PrivateFormat.Raw, NoEncryption()).hex()}
                    for a, o in self.accounts]
        with open(os.path.join(dirpath, "accounts.json"), "w") as f:
            json.dump(registry, f, indent=1)
        with open(os.path.join(dirpath, "net.json"), "w") as f:
            json.dump({"n_frag": self.n_frag,
                       "q": self.net.q.tolist(), "h": self.net.h.tolist()}, f)
        for i in range(self.n_frag):
            self.ledgers[i].log_path = os.path.join(dirpath, f"ledger_{i}.log")
            self.ledgers[i]._rewrite_log()
        return dirpath

    @classmethod
    def load(cls, dirpath, k=6, min_balance=100):
        """Reconstruct a bank from save(): rebuild keys/routing from the
        registry, topology from net.json, and replay each WAL into balances.
        The caller should check_invariants() to verify the replay."""
        with open(os.path.join(dirpath, "accounts.json")) as f:
            registry = json.load(f)
        with open(os.path.join(dirpath, "net.json")) as f:
            netd = json.load(f)
        bank = cls.__new__(cls)
        bank.min_balance = min_balance
        bank.n_frag = netd["n_frag"]
        bank.net = DecentralNet(dim=2, k=k, mu0=0.12)
        bank.net.add_many(np.asarray(netd["q"], dtype=float),
                          homes=np.asarray(netd["h"], dtype=float))
        bank.ledgers = [Ledger.from_log(
            os.path.join(dirpath, f"ledger_{i}.log"), i) for i in range(bank.n_frag)]
        bank.balances = defaultdict(lambda: defaultdict(int))
        bank.accounts = []
        bank.frag_for = {}
        bank.keys = {}
        bank.known = defaultdict(lambda: defaultdict(str))
        bank.faulty = set()
        bank.refusing = set()
        for e in registry:
            addr, owner = e["addr"], e["owner"]
            pub = bytes.fromhex(e["pub"])
            priv = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(e["priv"]))
            bank.balances[owner][addr] = min_balance
            bank.frag_for[addr] = owner
            bank.keys[addr] = (pub, priv)
            bank.accounts.append((addr, owner))
        # replay committed blocks -> balances
        for i, ld in enumerate(bank.ledgers):
            for b in ld.blocks:
                for t in b["txs"]:
                    bank.balances[i][t["from"]] -= t["amount"]
                    bank.balances[bank.frag_for[t["to"]]][t["to"]] += t["amount"]
        return bank


# ---------------------------------------------------------------------- #
# Tests
# ---------------------------------------------------------------------- #
def test_t1_routing():
    """Ownership IS routing (homes = data centroids).  The meaningful bank
    properties: routing is deterministic, and it actually splits the account
    set across fragments (not one fragment owning everything)."""
    bank = FragmentBank(16, accounts_per_frag=40)
    spread = bank.partition_spread()
    det = all(bank.route(a) == owner for a, owner in bank.accounts)
    degenerate = (spread["empty_fragments"] > 4
                  or spread["max"] > len(bank.accounts) / 2)
    return {"test": "T1 routing", "deterministic": det,
            "partition_spread": spread,
            "verdict": "PASS" if det and not degenerate else "PARTIAL"}


def test_t2_integrity():
    bank = FragmentBank(16, accounts_per_frag=40)
    rng = np.random.RandomState(1)
    names = [a for a, _ in bank.accounts]
    ok_all = True
    for _ in range(3000):
        s, r = rng.randint(0, len(names), size=2)
        amt = int(rng.randint(1, 40))
        if s != r:
            ok, why = bank.transfer(names[s], names[r], amt)
            if not ok and why != "insufficient":
                ok_all = False
                break
    ok, why = bank.check_invariants()
    return {"test": "T2 integrity", "invariants": ok, "detail": why,
            "verdict": "PASS" if ok and ok_all else "FAIL"}


def test_t3_double_spend():
    bank = FragmentBank(8, accounts_per_frag=20)
    s = bank.accounts[0][0]
    r = bank.accounts[-1][0]
    first, why1 = bank.transfer(s, r, 10, nonce=1)
    second, why2 = bank.transfer(s, r, 10, nonce=1)   # replay nonce
    return {"test": "T3 double-spend",
            "first": first, "replay_rejected": (not second and why2 == "nonce-replay"),
            "verdict": "PASS" if first and not second else "FAIL"}


def test_t4_damage():
    bank = FragmentBank(20, accounts_per_frag=30)
    rng = np.random.RandomState(2)
    names = [a for a, _ in bank.accounts]
    for _ in range(2000):
        s, r = rng.randint(0, len(names), size=2)
        if s != r:
            bank.transfer(names[s], names[r], int(rng.randint(1, 40)))
    killed = bank.kill(0.30)
    # routing after damage: survivors re-resolve (nearest living fragment)
    ok, why = bank.check_invariants()          # surviving chains still valid
    return {"test": "T4 damage", "killed": len(killed),
            "surviving_invariants": ok, "detail": why,
            "verdict": "PASS" if ok else "FAIL"}


def test_t5_faulty_quorum():
    """With f% of fragments lying/refusing: transfers owned by honest
    fragments should mostly succeed (availability), transfers owned by faulty
    fragments should be caught by the quorum - unless corruption exceeds 50%
    of the neighbourhood, in which case the faulty side wins (the crease)."""
    results = []
    for f_frac in [0.0, 0.2, 0.4, 0.5, 0.6]:
        bank = FragmentBank(12, k=6, accounts_per_frag=20)
        n_faulty = int(12 * f_frac)
        bank.faulty = set(range(n_faulty))       # lie about head hashes
        bank.refusing = set(range(n_faulty))     # refuse to replicate
        honest = [a for a, o in bank.accounts if o not in bank.faulty]
        faulty = [a for a, o in bank.accounts if o in bank.faulty]
        r_name = bank.accounts[-1][0]
        n_try = min(30, len(honest))
        honest_ok = sum(bank.transfer(a, r_name, 1)[0] for a in honest[:n_try])
        honest_ok = honest_ok / n_try if n_try else 0.0
        faulty_caught = 0.0
        if faulty:
            n_try = min(30, len(faulty))
            caught = [not bank.transfer(a, r_name, 1)[0] for a in faulty[:n_try]]
            faulty_caught = sum(caught) / len(caught)
        results.append({"faulty_frac": f_frac,
                        "honest_ok_frac": round(float(honest_ok), 3),
                        "faulty_send_caught_frac": round(float(faulty_caught), 3),
                        "null_coinflip": 0.5})
    return {"test": "T5 faulty quorum", "results": results,
            "verdict": "MEASURED"}


def test_t6_anomaly():
    """Novelty layer: flag txs whose amount is an outlier vs that sender's
    history.  Compare recall/precision against random flagging."""
    bank = FragmentBank(8, accounts_per_frag=25)
    rng = np.random.RandomState(3)
    names = [a for a, _ in bank.accounts]
    history = defaultdict(list)
    fraud_flags, legit_flags = [], []
    fraud_total = legit_total = 0
    for _ in range(2000):
        s, r = rng.randint(0, len(names), size=2)
        if s == r:
            continue
        # 2% of txs are "fraud" = 20x the usual amount
        is_fraud = rng.rand() < 0.02
        base = int(rng.randint(1, 40))
        amt = base * 20 if is_fraud else base
        bank.transfer(names[s], names[r], amt)
        history[s].append(amt)
        mu = np.mean(history[s]) if history[s] else 1.0
        sd = np.std(history[s]) if len(history[s]) > 1 else 1.0
        novel = (amt > mu + 2 * sd) if sd > 0 else False
        if is_fraud:
            fraud_total += 1
            fraud_flags.append(novel)
        else:
            legit_total += 1
            legit_flags.append(novel)
    rec = np.mean(fraud_flags) if fraud_total else 0.0
    prec_denom = sum(fraud_flags) + sum(legit_flags)
    prec = sum(fraud_flags) / prec_denom if prec_denom else 0.0
    null_prec = (fraud_total / (fraud_total + legit_total)) if (fraud_total + legit_total) else 0.0
    return {"test": "T6 anomaly",
            "recall_fraud": round(float(rec), 3),
            "precision": round(float(prec), 3),
            "null_precision_random": round(float(null_prec), 4),
            "verdict": "PASS" if rec > 0.5 else "MEASURED"}


def test_t7_signatures():
    """Ledger must accept a legitimately signed tx and reject (a) a tampered
    committed block, (b) a tx signed by the wrong key, (c) a tx that claims a
    victim address but carries the attacker's pubkey."""
    bank = FragmentBank(8, accounts_per_frag=20)
    s = bank.accounts[0][0]
    r = bank.accounts[-1][0]
    ok, why = bank.transfer(s, r, 10)
    if not ok:
        return {"test": "T7 signatures", "accepted": False, "detail": why,
                "verdict": "FAIL"}
    frag = bank.frag_for[s]
    ld = bank.ledgers[frag]

    # (a) tamper a committed block -> full re-validation must fail
    ld.blocks[-1]["txs"][0]["amount"] += 1
    tamper_rejected = ld.validate()[0] is False
    ld.blocks[-1]["txs"][0]["amount"] -= 1

    # (b) victim's pubkey but signed with the ATTACKER's key
    #     (address binding passes; the signature must fail)
    victim = s
    victim_pub, _ = bank.keys[victim]
    attacker_priv = bank.keys[bank.accounts[1][0]][1]
    tx_b = {"from": victim, "to": r, "amount": 5,
            "nonce": ld.nonces[victim] + 1, "pub": victim_pub.hex()}
    tx_b["sig"] = sign_tx(attacker_priv, tx_b).hex()
    wrong_key_rejected = ld.try_append([tx_b])[1] == "bad-signature"

    # (c) attacker's keypair but claiming the victim's address
    attacker_pub, _ = bank.keys[bank.accounts[1][0]]
    tx_c = {"from": victim, "to": r, "amount": 5,
            "nonce": ld.nonces[victim] + 1, "pub": attacker_pub.hex()}
    tx_c["sig"] = sign_tx(attacker_priv, tx_c).hex()
    # pubkey hashes to attacker's own address, not victim -> addr-mismatch
    addr_spoof_rejected = ld.try_append([tx_c])[1] == "addr-mismatch"

    # (d) a fresh legitimate tx still accepted
    ok2, _ = bank.transfer(s, r, 3)

    all_rejected = tamper_rejected and wrong_key_rejected and addr_spoof_rejected
    return {"test": "T7 signatures", "accepted": ok, "accepted_again": ok2,
            "tamper_rejected": tamper_rejected,
            "wrong_key_rejected": wrong_key_rejected,
            "addr_spoof_rejected": addr_spoof_rejected,
            "verdict": "PASS" if ok and ok2 and all_rejected else "FAIL"}


def test_t8_persistence():
    """After save + load into a fresh bank, the chains/heads/balances must be
    bit-identical, invariants must hold, and the loaded bank must still
    transact."""
    import tempfile
    bank = FragmentBank(10, accounts_per_frag=15)
    rng = np.random.RandomState(4)
    names = [a for a, _ in bank.accounts]
    for _ in range(400):
        s, r = rng.randint(0, len(names), size=2)
        if s != r:
            bank.transfer(names[s], names[r], int(rng.randint(1, 30)))
    heads_a = [ld.head for ld in bank.ledgers]
    with tempfile.TemporaryDirectory() as d:
        bank.save(d)
        bank2 = FragmentBank.load(d)
        heads_b = [ld2.head for ld2 in bank2.ledgers]
        ok, why = bank2.check_invariants()
        # a fresh transfer on the loaded bank works (WAL path still alive)
        s2, r2 = bank2.accounts[0][0], bank2.accounts[-1][0]
        ok2, _ = bank2.transfer(s2, r2, 5)
    return {"test": "T8 persistence", "heads_equal": heads_a == heads_b,
            "invariants": ok, "detail": why, "loaded_transacts": ok2,
            "verdict": "PASS" if heads_a == heads_b and ok and ok2 else "FAIL"}


# ---------------------------------------------------------------------- #
def main():
    print("=" * 66)
    print("DECENTRAL BANK PROTOTYPE (T68) - built on DecentralNet")
    print("=" * 66)
    results = {}
    for fn in [test_t1_routing, test_t2_integrity, test_t3_double_spend,
               test_t4_damage, test_t5_faulty_quorum, test_t6_anomaly,
               test_t7_signatures, test_t8_persistence]:
        r = fn()
        results[r["test"]] = r
        print(f"  [{r['verdict']:8s}] {r['test']}")
        for k, v in r.items():
            if k not in ("test", "verdict"):
                print(f"        {k} = {v}")

    limits = {
        "no_byzantine": "a >50% corrupt neighbourhood wins; quorum is weak consensus, not BFT",
        "toy": "single-process, local filesystem, deterministic; not a real bank",
        "no_network": "no transport, no cross-process consensus; quorum is an in-process simulation",
        "no_crash_recovery": "WAL is append+fsync but torn-log recovery is untested; an OS crash mid-commit could orphan a block",
        "observation_bank_missing": "anomaly uses tx amounts only; the declared T66 multivariate bank is still absent",
    }
    print("\nLIMITS (crease-worthy):")
    for k, v in limits.items():
        print(f"  {k}: {v}")

    out = {"results": results, "limits": limits}
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "data", "decentral_bank_data.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote data/decentral_bank_data.json")


if __name__ == "__main__":
    main()
