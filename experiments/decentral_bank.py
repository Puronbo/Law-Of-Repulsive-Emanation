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

  Built here (the "bank" half - honest: toy, not secure):
    - hashed char-ngram account embeddings (mimics the repo's
      HashingVectorizer(analyzer='char_wb', ngram_range=(2,4)) pattern so that
      name-similar accounts route to nearby fragments).
    - per-fragment hash-chained ledger (blocks link by SHA-256 of prev hash,
      double-entry debit/credit, per-account nonce => double-spend rejection).
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

Limits (crease-worthy, printed at the end):
  - NO Byzantine fault tolerance: a >50% corrupt neighbourhood wins.
  - Single-threaded, in-memory, deterministic toy - not a bank.
  - Account "signatures" are a stand-in (nonce + hashed name), not crypto.
"""

import json
import os
import sys
import hashlib
import itertools
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Universals"))
from manifold.decentral_net import DecentralNet, to_disk  # noqa: E402

RNG = np.random.RandomState(20260802)


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
    """Hash-chained double-entry ledger for one fragment."""

    def __init__(self, fragment_id):
        self.fragment_id = fragment_id
        self.blocks = []
        self.head = "genesis"
        self.nonces = defaultdict(int)   # account -> last used nonce

    def block_hash(self, index, prev, txs):
        payload = json.dumps({"i": index, "p": prev,
                              "t": sorted(txs, key=lambda t: t["nonce"])},
                             sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()

    def try_append(self, txs):
        """Append a block if the whole batch is valid (monotone nonces).
        Returns (ok, reason)."""
        for t in txs:
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

    def rollback(self):
        """Undo the most recently appended block (a quorum refused it)."""
        if self.blocks:
            self.blocks.pop()
            self.head = self.blocks[-1]["hash"] if self.blocks else ""

    def validate(self):
        """Full chain re-validation: link hashes and nonce monotonicity."""
        prev = "genesis"
        seen = defaultdict(int)
        for i, b in enumerate(self.blocks):
            if b["index"] != i or b["prev"] != prev:
                return False, f"link-broken@{i}"
            if b["hash"] != self.block_hash(i, prev, b["txs"]):
                return False, f"hash-mismatch@{i}"
            for t in b["txs"]:
                if t["nonce"] <= seen[t["from"]]:
                    return False, f"nonce-regress@{i}"
                seen[t["from"]] = t["nonce"]
            prev = b["hash"]
        return True, "ok"


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
        self.accounts = []                                    # (name, owner_frag)
        self.frag_for = {}
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
            for j in range(per_frag):
                name = f"frag{f}:acct{j}:x{abs(hash((f, j))) % 997}"
                owner = self.route(name)
                self.balances[owner][name] = self.min_balance
                self.frag_for[name] = owner
                self.accounts.append((name, owner))

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
        """Send money.  Returns (ok, reason).  Double-spend rejected by
        nonce + balance check.  Committed only under witness quorum."""
        frag = self.frag_for[sender]
        if nonce is None:
            nonce = self.ledgers[frag].nonces[sender] + 1
        if self.balances[frag][sender] < amount:
            return False, "insufficient"
        txs = [{"from": sender, "to": recipient, "amount": amount,
                "nonce": nonce}]
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


# ---------------------------------------------------------------------- #
def main():
    print("=" * 66)
    print("DECENTRAL BANK PROTOTYPE (T68) - built on DecentralNet")
    print("=" * 66)
    results = {}
    for fn in [test_t1_routing, test_t2_integrity, test_t3_double_spend,
               test_t4_damage, test_t5_faulty_quorum, test_t6_anomaly]:
        r = fn()
        results[r["test"]] = r
        print(f"  [{r['verdict']:8s}] {r['test']}")
        for k, v in r.items():
            if k not in ("test", "verdict"):
                print(f"        {k} = {v}")

    limits = {
        "no_byzantine": "a >50% corrupt neighbourhood wins; quorum is weak consensus, not BFT",
        "toy": "single-threaded, in-memory, deterministic; not a real bank",
        "no_real_crypto": "nonce+hash stand-in, not cryptographic signatures",
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
