---
title: "Provisional Patent Application"
subtitle: "System and Method for a Decentralized Fragment Bank with Routing-Defined Ownership"
docket: "PUNO-PPA-003"
inventor: "Michael Grafiel Sayson Puno"
date: "2026-08-04"
---

# PROVISIONAL PATENT APPLICATION

## System and Method for a Decentralized Fragment Bank with Routing-Defined Ownership, Majority-Honesty Witness Quorums, and an Integrity-Anomaly Layer

**Docket:** PUNO-PPA-003
**Inventor:** Michael Grafiel Sayson Puno
**Filed (priority date basis):** 2026-08-04
**Corpus reference:** Puno Calculus T1–T20 / T68–T71 (`experiments/decentral_bank.py`, `experiments/decentral_bank_bridge.py`, `experiments/decentral_bank_net.py`, `Universals/manifold/decentral_net.py`, `data/decentral_bank_data.json`, `data/decentral_bank_bridge_data.json`, `data/decentral_bank_net_data.json`)

---

## 1. TITLE OF THE INVENTION

System and Method for a Decentralized Fragment Bank in which Account Ownership Is Defined by Deterministic Spatial Routing, Transactions Commit Through Majority-Honesty Nearest-Neighbor Witness Quorums, and an Integrity-Anomaly Layer Detects Fraudulent Flow.

## 2. FIELD OF THE INVENTION

The invention relates to decentralized financial ledgers, distributed account custody, and anomaly detection over transaction streams. In particular it relates to a bank whose units are spatial "fragments" of a population-flow network; each account belongs to exactly one fragment by a deterministic embedding rule (ownership IS routing), transfers are signed with a public-key scheme and committed by a quorum of the k nearest-neighbor fragments, and a statistical anomaly layer flags flows inconsistent with honest behavior.

## 3. BACKGROUND OF THE INVENTION

### 3.1 The problem of many accounts, one place

Centralized banks concentrate all account state in one store: a single failure or compromise risks everything, and the operator must be trusted for bookkeeping. Distributed ledgers solve custody by consensus among peers, but full replicated consensus (e.g., BFT variants) is expensive and has an adversarial threshold at one-third faulty nodes.

### 3.2 Prior approaches and their limitations

1. **Centralized ledger:** single point of failure, trust in the operator.
2. **Replicated BFT consensus:** requires ≥ 2/3 honest replicas for liveness and safety; heavy message complexity; no spatial locality; every node holds all state.
3. **Sharded ledgers:** sharding reduces per-node storage but shard assignment is typically decoupled from account identity and often re-balanced by a central coordinator or complex protocol, so "who owns which account" is not derivable from the account identifier alone.
4. **Heuristic fraud/anomaly detection:** rule- and model-based, often with unmeasured or poor precision on unbalanced streams; rarely benchmarked against a random baseline.

None of these provides: (a) account ownership that is a pure function of the account key and a fixed spatial embedding — so a fragment failure is self-healing by re-resolution to the nearest living fragment; (b) a weak consensus whose liveness degrades *gracefully and measurably* with the fraction of faulty witnesses and collapses only beyond 50% neighborhood corruption; and (c) an anomaly detector benchmarked (recall 0.514, precision 0.633) against a random null (0.0186).

## 4. SUMMARY OF THE INVENTION

The invention provides a computer-implemented decentralized fragment bank comprising:

- **A) Deterministic account identity and routing-defined ownership.** Each account address is a deterministic truncation of a hash of the account holder's public key (measured: first 40 hex characters of SHA-256 of an Ed25519 public key). A deterministic embedding maps each account to a vector; the account is owned by the fragment whose home vector is nearest (measured: 100% routing determinism, 0% route mismatch over 640 accounts across 16 fragments; partition spread min 8 / max 74 accounts per fragment, std 20.6, zero empty fragments). Ownership is therefore derivable from the key alone and needs no registry: **ownership IS routing**.
- **B) Double-entry hash-chained ledger with replay rejection.** Each fragment keeps a double-entry ledger whose blocks chain on SHA-256 of the prior head. Each account carries a monotonically increasing nonce; a signed transaction is rejected if its nonce has already been applied (measured: first spend accepted, replay rejected; on-ramp/off-ramp replay rejected with custody and supply unchanged).
- **C) Witness quorum commitment.** A fragment commits a transfer only if a majority of its k nearest-neighbor fragments confirm the head hash — a weak, majority-honesty consensus, deliberately not BFT. Measured liveness under scattered corruption (honest-commit success): 1.0 at 0% faulty, 0.6 at 30%, 0.286 at 50%, 0.0 at 70%; under *contiguous* corruption at 70% it stays 1.0. Transfers owned by a fragment whose witnesses are all dead cannot commit (availability wall), as designed.
- **D) Stateless crash recovery.** A crashed fragment restarts with no private state and recovers its chain from its peers' replicas (measured: zero crashed-owner transactions committed during the crash; all live-owner commits succeed; recovered chain matches peers). In the case where every node dies at once, each node's own write-ahead log (WAL) rebuilds the pre-crash committed state bit-identically (measured: rebuilt heads match pre-crash, block counts match, invariants conserved, a fresh commit succeeds after rebuild).
- **E) End-to-end integrity-anomaly layer.** A statistical layer scores transaction flows for consistency with honest behavior; measured recall 0.514, precision 0.633, against a random null precision of 0.0186 — roughly 34× the random baseline.

The invention further covers a bridge embodiment for fiat entry/exit and a networked embodiment with mutual-TLS message transport.

## 5. DETAILED DESCRIPTION

### 5.1 Account identity and routing

Addresses: `address = SHA-256(public_key_bytes).hexdigest()[:40]`. Signatures are Ed25519 over a canonical transaction body; verification uses the public key and re-derives the address (measured: genuine signature accepted and re-accepted; tampered body rejected; wrong-key signature rejected; address spoof — a signature from a different key presented under a victim's address — rejected).

Routing: an account is embedded deterministically by a hashed character-ngram embedding into a dim-dimensional vector, scaled and clamped to the disk; ownership = the fragment whose home (centroid) is nearest by Euclidean distance. Because routing is a pure function of the key, a killed fragment's accounts re-resolve to the nearest *living* fragment (measured: after killing 6 of 16 fragments, survivors keep routing and total balance conserved at 60000 vs 60000).

### 5.2 Ledger and consensus

Each fragment's ledger is a hash-chained sequence of blocks; a block holds a set of double-entry transfers (debit/credit pairs), the prior-head hash, and the proposer. Persistence is append+fsync WAL written *before* a commit is announced.

Network consensus is real message exchange in four phases: **PROPOSE → VOTE → COMMIT → NOTIFY**. A proposer sends a block to its k witnesses; each witness checks the proposed block against its replica of the owner's chain and votes; the proposer commits when a strict majority of witnesses approve (writing the WAL before announcing); COMMIT is broadcast to all peers; NOTIFY propagates the committed block. Measured on sockets with 16 fragments: 14/14 transactions commit with no missing blocks, all chains consistent and valid, balance conserved.

### 5.3 Fault and availability behavior (measured)

- **T13 partition + rejoin:** during a network partition 12/16 attempted transactions commit (10 on side A, 2 on side B); after rejoin all nodes converge to a single consistent history, chains valid, balance conserved.
- **T14a fabrication:** a forged block injected to an owner and its witnesses is rejected by all 6 nodes (accept rate 0.0).
- **T14b availability wall:** see Summary C curve. The system is availability-tradeable: corruption that is scattered degrades liveness monotonically past 30–50%, while contiguous corruption is survivable because honest witnesses remain in the majority neighborhood.
- **T14c partition equivocation:** a double-signed transaction during a partition produces divergent heads that only converge after rejoin; the network detects the fork afterwards. (Requires the account holder's own key.)
- **T15 / T17 crash + stateless restart:** see Summary D. During a dead node's downtime its own accounts commit 0 transactions, all live owners commit 8/8, and the restarted node's recovered chain matches its peers exactly, after which it can commit new transactions with correct nonce continuity.
- **T18 total state loss + WAL rebuild:** every node loses all state; each node rebuilds its own committed chain from its own WAL; rebuilt heads and block counts match the pre-crash state; invariants hold; a fresh commit follows.
- **T19 mutual TLS:** nodes authenticate with TLS certificates; a client presenting no identity is rejected; after a TLS restart the network reconverges and commits 14/14.
- **T20 LAN:** the same system runs over real mutual-TLS sockets bound to a LAN NIC at 192.168.100.241; 14/14 commits, reconvergence after NIC restart.

### 5.4 Integrity-anomaly layer

The anomaly detector scores sequences of transactions by their deviation from honest flow (measured features: per-account amounts and rates) and flags outliers. Measured on an attack injection: recall (fraction of injected frauds caught) 0.514; precision (fraction of flags that are true frauds) 0.633; a random baseline classifier yields precision 0.0186. The null baseline quantifies how much signal the layer contributes: ~34× above chance.

### 5.5 Bridge embodiment (fiat on/off ramp)

An on-ramp converts fiat deposits into network credit (DCN) at a gateway; an off-ramp burns DCN for fiat payout; both sides reconcile to 0.0 difference; both directions are idempotent by caller-supplied reference and reject replays; a forged over-withdrawal is rejected. Measured round trip: 1000 DCN in, 400 DCN burned, 1400.0 fiat out, reconcile diff 0.0.

### 5.6 Honest limits

- The quorum is weak consensus, not BFT: a >50% corrupt neighborhood, or an exploitable partition, wins until detected. There is no BFT guarantee under arbitrary adversaries.
- Measured deployments are single-machine (T20 binds real sockets to the LAN NIC but still one host); two-host transport-specific faults are only modeled at the fragment level.
- An OS-level crash mid-commit could still tear the WAL; torn-log recovery is untested.
- Anomaly features are transaction amounts only (the declared multivariate observation bank was not yet exercised); single gateway key, no m-of-n threshold, no HSM, no KYC/AML/sanctions/regulator reporting.

## 6. CLAIMS (provisional)

1. A computer-implemented method for operating a decentralized bank over a plurality of bank fragments in a metric space, comprising: deriving an account address for a holder from a hash of the holder's public key; deterministically embedding the account address into the metric space; assigning ownership of the account to the fragment whose assigned home is nearest to the embedding, whereby ownership is a pure function of the public key and requires no registry; and, upon unavailability of the owning fragment, reassigning the account to the nearest available fragment by the same rule.

2. The method of claim 1, further comprising verifying that a transaction directed to the account carries a signature from the public key matching the account address, and rejecting the transaction when the signature does not verify or when the signature is presented under a different address.

3. The method of claim 1, further comprising committing a transaction to the account's ledger only when a strict majority of the k nearest-neighbor witness fragments of the owning fragment confirm the resulting head hash, whereby liveness degrades as the fraction of faulty witnesses increases and ceases at approximately 50% scattered corruption.

4. The method of claim 3, further comprising rejecting a transaction whose nonce has already been applied to the account, whereby replayed and double-spent transactions are rejected.

5. The method of claim 3, wherein each fragment persists committed blocks in a write-ahead log before announcing a commit, and a fragment that loses all state rebuilds its chain from its own write-ahead log or from peer replicas, returning to a state identical to the pre-failure state.

6. A computer-implemented method for detecting fraudulent transactions in a decentralized bank, comprising: scoring transaction flows by their deviation from honest behavior; and flagging outliers, wherein the flagged set exhibits a precision at least an order of magnitude above a random baseline on the same stream.

7. A system comprising one or more processors and memory configured to perform the method of any of claims 1–6.

## 7. ABSTRACT

A decentralized fragment bank in which account ownership is defined by deterministic spatial routing: each account address is a truncation of the SHA-256 hash of the holder's Ed25519 public key, embedded to the nearest of a set of fragment homes, so ownership is a pure function of the key (0% route mismatch measured). Transfers are Ed25519-signed, replay-rejected by per-account nonces, and committed by a majority-honesty quorum of the k nearest-neighbor fragments (PROPOSE→VOTE→COMMIT→NOTIFY; liveness 1.0 → 0.6 → 0.286 → 0.0 as scattered corruption rises 0%→30%→50%→70%). Crashed fragments recover statelessly from peer replicas or their own write-ahead logs, bit-identically. An integrity-anomaly layer flags fraudulent flow with recall 0.514 / precision 0.633 versus 0.0186 random. Measured end-to-end over real mutual-TLS sockets on a LAN NIC: 14/14 commits, partition re-convergence, and crash recovery.

---

*This document is a provisional disclosure establishing a priority date for the subject matter described. All measured values are reproduced from the inventor's verified corpus (2026-08-04); no assertion is made regarding patentability beyond enablement and written description.*
