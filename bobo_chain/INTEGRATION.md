# IMAM-V3 Fold-Metric → Multi-Chain → Decentralized Internet Integration

**Anchor schema:** `26/10/2000T10:26:20.00` (UTC, `DD/MM/YYYYThh:mm:ss.cc`)
**Fold metric:** `57,434,001` | **Fold clock:** 57.26 MHz → 17.46 ns/tick

## 1. The Data Path (fold metric → internet record)

```
fold metric 57,434,001
      │  (imam_agent)  partitioned across the wallet matrix, integrity-checked
      ▼
fold channels  (each wallet owns a contiguous channel range)
      │  (agent_toy)   token walks channels; neighbor-jumps at wallet boundaries
      ▼
wallet address (COLD)  + activity record (SIGN/SWEEP/ROTATE/JUMP/TRASH)
      │  (fold_crypto) ECDSA-secp256k1 (RFC6979) signed by the wallet that owns
      │                the channel; MASTER signs parked / trash records
      ▼
time-anchored internet block
      │  (internet_registry)  merkle root over ECDSA signatures + prev_hash chain,
      │                       block header signed by the AGENT identity
      ▼
independent verifiers  (Node 0D + MATRIX-0..N + AGENT + MASTER; public keys only)
      │   each recomputes the chain, verifies every record + block signature,
      ▼   checks the at-rest HMAC seal, then votes VALID/INVALID
```

## 2. Modules

| Module | Role | API |
| ------ | ---- | --- |
| `engine.py` | HD wallet matrix (BIP44, fold-identity fallback), `derive_identity()` | `/api/scan`, `/api/report`, `/api/configure` |
| `imam_agent.py` | Fold agent: channel partition, fold clock, fold root; real AGENT identity key (account 1) | `/api/agent`, `/api/agent/activate`, `/api/agent/foldclock`, `/api/agent/wallets/{i}` |
| `fold_crypto.py` | Actual-security layer: ECDSA sign/verify/recover, identity map, canonical record messages, HMAC at-rest seal | (used by toy + registry) |
| `agent_toy.py` | Cold-wallet activity + neighbor jumping, append-only ECDSA-signed ledger | `/api/toy`, `/api/toy/coldwallets`, `/api/toy/step`, `/api/toy/reset`, `/api/toy/activity`, `/api/toy/verify`, `/api/toy/migrate` |
| `internet_registry.py` | Time-anchored registry, signed blocks, chain of custody, independent verifiers, Merkle proofs, at-rest seal | `/api/internet/registry`, `/api/internet/ingest`, `/api/internet/consensus`, `/api/internet/verify`, `/api/internet/proof`, `/api/internet/nodes`, `/api/internet/identities`, `/api/internet/reseal` |
| `cold_crawler.py` | Crawls cold matrix on real chain data (actual mode only), routes inactive reserves to MASTER | `/api/crawler`, `/api/crawler/table`, `/api/crawler/run`, `/api/crawler/reset`, `/api/crawler/ledger`, `/api/crawler/actual` |
| `wallet_connect.py` | External-wallet bridge: Base58Check/CashAddr → pubkey hash → EVM address; connected-wallet battery; multi-network genesis registry | `/api/connected`, `/api/genesis` |

## 3. Invariants (checked end-to-end)

1. **Fold integrity:** `sum(channel_count) == 57,434,001`.
2. **Neighbor jumping:** every step moves +1 channel; at a wallet boundary the
   token ring-hops to the neighbor wallet's first channel.
3. **Record authenticity:** every record is ECDSA-signed by the wallet that owns
   its channel (MASTER for parked/trash); the signature covers
   `schema|address|wallet:channel|type|seq|seed`, so editing any of those fields
   breaks signature recovery → INVALID.
4. **Block authenticity:** each block header is signed by the AGENT identity;
   re-minting or reordering blocks fails verification.
5. **Chain of custody:** every block's hash covers `prev_hash + merkle_root +
   records`, so rewriting one record invalidates the recomputed hash.
6. **Consensus:** the verifiers are the available identities (Node **0D**,
   `MATRIX-0..N`, `AGENT`, `MASTER`), each holding public keys only and
   independently recomputing the whole chain. One altered record or signature
   flips every vote to INVALID (tamper detected).
7. **At-rest integrity:** the persisted registry carries an HMAC-SHA256 seal
   (in-memory key); editing the file is detected on load, flags `TAMPERED`, and
   blocks ingest until the operator calls `POST /api/internet/reseal`.
8. **Merkle proofs:** `GET /api/internet/proof?seq=N` returns an O(log n)
   sibling path proving a record's inclusion in its block.

## 4. External wallet bridge → genesis wallets

Any external UTXO address can anchor the stack: `wallet_connect.py` decodes the
address (Base58Check or BCH CashAddr) into its 20-byte pubkey hash, exposes it
as an EVM bridge address (`0x` + hash), and derives the wallet matrix via
`0x + sha256(anchor|idx)` — the same derivation `engine.py` uses in
connected-wallet mode.

`GET /api/genesis` runs the connected-wallet battery against every registered
chain's hard-coded genesis wallet:

| Network | Version | Genesis wallet | EVM bridge (pubkey hash) |
| --- | --- | --- | --- |
| Bitcoin | `0x00` | `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` | `0x62e907b15cbf27d5425399ebf6f0fb50ebb88f18` |
| Bitcoin Cash | `0x00` (legacy) / CashAddr | `bitcoincash:qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy` | `0x62e907b15cbf27d5425399ebf6f0fb50ebb88f18` |
| Litecoin | `0x30` | `Ler4HNAEfwYhBmGXcFP2Po1NpRUEiK8km2` | `0xd73e63c04a6cbad8d5dc94fdbef5175d2364e32f` |
| Dogecoin | `0x1e` | `DQmCZQo3thCvTxkyAhPHfY7DVLqFtJ2ji6` | `0xd73e63c04a6cbad8d5dc94fdbef5175d2364e32f` |

Litecoin and Dogecoin share the genesis P2PK key (DOGE forked from LTC), so
both bridge to the same EVM address. The `network` param on `/api/connected`
enforces the version byte — a cross-chain address is rejected with HTTP 400.
The BCH CashAddr encoder was verified against the reference-implementation
test vectors, so the genesis CashAddr matches the official BCH documentation.

## 5. Master dashboard (Node 0D)

`GET /api/master` returns the whole stack restructured as consumers of the
universal date protocol: protocol clock (anchor/now/fold ticks), the five
layers (wallet matrix, fold agent, cold toy, internet registry, crawler +
master), and the live consensus including Node 0D's vote. The dashboard header
shows the live clock and the **Node 0D** badge; `window.onload` calls
`masterLoad()` so the master view syncs automatically.

## 6. Run

```
$env:IMAM_MNEMONIC = "your-12-word-anchor-mnemonic"   # the ONLY secret (kept out of the repo)
python run_server.py                            # 127.0.0.1:8000 by default
# optional hardening: HOST, PORT, API_TOKEN, TLS_CERT, TLS_KEY env vars
```

Dashboard sequence: **Query Fold Agent** → toy **Step 100** → toy **Refresh** →
**Ingest Ledger** → **Verify Consensus** (VALID) → **Tamper Test** (INVALID) →
**Internet Verify** (crypto battery) → **Merkle Proof**.

Actual-security verification (in-process):

```python
from fold_crypto import SigningAuthority
from internet_registry import InternetRegistry
# ...
reg.verify()            # chain + record + block + at-rest + per-node votes
reg.consensus(tamper_seq=5)   # tamper detection demo (INVALID)
reg.proof(seq=3)        # Merkle inclusion proof
```

## 7. Actual security (M14)

See `SECURITY.md` for the full threat model. In short:

- **ECDSA (secp256k1, RFC6979) records and blocks** — the wallet that owns a
  channel signs every record; the AGENT identity signs every block header.
- **Available identities as verifiers** — Node 0D, MATRIX-0..N, AGENT, MASTER;
  each holds public keys only and independently recomputes the chain.
- **Key custody** — mnemonic env-only, keys in memory only, `data/` excluded by
  `.gitignore`; no private key is ever written to disk or broadcast.
- **At-rest HMAC seal** — disk edits are detected and block ingest until reseal.
- **Transport** — loopback bind by default; optional bearer token + TLS.
- Posture overview: `GET /api/security`.

## 8. Honest limits

- Toy only: no real transactions; wallet keys never leave the machine.
- `bip-utils` requires a `coincurve` wheel (py3.11/3.12); on interpreters
  without it the engine/agent use the deterministic fold-identity fallback
  (which yields digest signatures, not ECDSA).
- 57,434,001 simultaneous channels is an idealized metric (see master
  documentation, limitations section).
