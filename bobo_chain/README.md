# Puno_Calculus — bobo Chain Stack (IMAM-V3)

Multi-chain HD wallet matrix + fold-metric agent + cold-wallet neighbor-jump
toy + time-anchored decentralized-internet registry with multi-node consensus.

Everything is structured as a **master dashboard (Node 0D)** over the universal
date protocol `26/10/2000T10:26:20.00`: every layer consumes the same fold
clock, and Node 0D aggregates and votes on the whole stack.

## Quick start

```
pip install -r requirements.txt
uvicorn server:app --port 8000
```

Open http://localhost:8000 — the dashboard auto-syncs via `/api/master`
(anchor clock, Node 0D badge, per-layer status) and covers the full data path:
Query Fold Agent -> toy Step -> Ingest Ledger -> Verify Consensus -> Tamper Test
-> Crawler sweep -> MASTER.

## Configuration

- **Mnemonic:** set `IMAM_MNEMONIC` env var. The built-in value is a labeled
  DEMO phrase only; never use it for real funds.
  ```powershell
  $env:IMAM_MNEMONIC = "your twelve words here"
  uvicorn server:app --port 8000
  ```
- **Networks/RPCs:** edit `networks.json` (loaded at import; falls back to an
  embedded copy if missing).

## Modules

| Module | Role | Endpoints |
| ------ | ---- | --------- |
| `engine.py` | HD wallet matrix scan (BIP44 or fold-identity fallback), `derive_identity()` | `/api/scan`, `/api/report`, `/api/configure` |
| `imam_agent.py` | Fold agent: 57,434,001-channel partition, fold clock, fold root; real AGENT identity key (account 1) | `/api/agent`, `/api/agent/activate`, `/api/agent/foldclock`, `/api/agent/wallets/{i}` |
| `fold_crypto.py` | Actual-security layer: ECDSA sign/verify/recover, identity map, HMAC at-rest seal | (used by toy + registry) |
| `agent_toy.py` | Cold-wallet activity + neighbor jumping (append-only ECDSA-signed ledger) | `/api/toy`, `/api/toy/coldwallets`, `/api/toy/step`, `/api/toy/reset`, `/api/toy/activity`, `/api/toy/verify`, `/api/toy/migrate` |
| `internet_registry.py` | Time-anchored registry, AGENT-signed blocks, merkle roots, chain of custody, independent verifiers, Merkle proofs, at-rest seal | `/api/internet/registry`, `/api/internet/ingest`, `/api/internet/consensus`, `/api/internet/verify`, `/api/internet/proof`, `/api/internet/nodes`, `/api/internet/identities`, `/api/internet/reseal` |
| `cold_crawler.py` | Cold-wallet crawler (actual only): applies the real chain scan, routes inactive reserves to MASTER | `/api/crawler`, `/api/crawler/table`, `/api/crawler/run`, `/api/crawler/reset`, `/api/crawler/ledger`, `/api/crawler/actual` |
| `wallet_connect.py` | External-wallet bridge (Base58Check/CashAddr -> pubkey hash -> EVM address) + connected-wallet battery + multi-network genesis-wallet registry | `/api/connected`, `/api/genesis` |
| `server.py` | Node 0D master view: aggregates every layer under the date protocol; optional bearer-token auth | `/api/master`, `/api/configure`, `/api/security` |

## External wallet / connected wallets

Use any external address (e.g. the Bitcoin genesis wallet
`1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa`) as the stack's anchor:

```
curl http://localhost:8000/api/connected
# -> Base58Check decode, pubkey hash 62e907b1...f18, EVM bridge
#    0x62e907b15cbf27d5425399ebf6f0fb50ebb88f18, 5 connected wallets, 6/6 tests
curl -X POST http://localhost:8000/api/configure \
     -H "Content-Type: application/json" \
     -d '{"wallet":"1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"}'
# -> whole stack (matrix/agent/toy/registry/crawler) derives from that wallet
```

Connected-wallet battery: checksum, 20-byte pubkey hash, EVM bridge,
derivation link to the anchor, fold-channel neighbor ring, single Merkle fold root.

## Genesis wallets (other blockchain networks)

`GET /api/genesis` runs the same connected-wallet battery against every
registered network's hard-coded genesis wallet, deriving the wallet matrix
from each anchor:

| Network | Symbol | Genesis wallet | EVM bridge (pubkey hash) |
| --- | --- | --- | --- |
| Bitcoin | BTC | `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` | `0x62e907b15cbf27d5425399ebf6f0fb50ebb88f18` |
| Bitcoin Cash | BCH | `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` (legacy) / `bitcoincash:qp3wjpa3tjlj042z2wv7hahsldgwhwy0rq9sywjpyy` | `0x62e907b15cbf27d5425399ebf6f0fb50ebb88f18` |
| Litecoin | LTC | `Ler4HNAEfwYhBmGXcFP2Po1NpRUEiK8km2` | `0xd73e63c04a6cbad8d5dc94fdbef5175d2364e32f` |
| Dogecoin | DOGE | `DQmCZQo3thCvTxkyAhPHfY7DVLqFtJ2ji6` | `0xd73e63c04a6cbad8d5dc94fdbef5175d2364e32f` |

The `network` query param on `/api/connected` enforces the version byte
(e.g. `0x30` Litecoin, `0x1e` Dogecoin, `0x00` BTC/BCH legacy); a mismatched
chain is rejected with HTTP 400. BCH genesis also decodes from its CashAddr
form. Litecoin/Dogecoin share their genesis P2PK key (Dogecoin forked from
Litecoin), so they bridge to the same EVM address.

```
curl http://localhost:8000/api/genesis
# -> 4/4 genesis networks CONNECTED, each 7/7 tests
curl "http://localhost:8000/api/connected?wallet=Ler4HNAEfwYhBmGXcFP2Po1NpRUEiK8km2&network=litecoin"
# -> CONNECTED 7/7 (LTC genesis anchor)
```

## Crawler: real chain data only (actual mode)

The crawler runs exclusively on real on-chain data. `POST /api/crawler/actual`
runs the real wallet-matrix scan over the RPCs in `networks.json` and replaces
each cold wallet's reserve with its REAL on-chain balance (native + ERC-20
across all networks), and uses the real transaction count for dormancy
detection (nonce == 0 -> dormant). Sweeps route inactive reserves into the
MASTER wallet.

There is no simulated mode and no master payoff: balances come from the last
applied scan, and sweeps only move tokens into MASTER. The routing mechanics
remain toy accounting — **nothing is broadcast**; this is read-only integration
of real data. Re-running the scan refreshes reserves; `POST /api/crawler/reset`
clears the crawler back to an unscanned state.

## Anchor schema

`26/10/2000T10:26:20.00` UTC = `datetime(2000,10,26,10,26,20,0,utc)`.
Timestamps render as `DD/MM/YYYYThh:mm:ss.cc` (centiseconds).
Fold clock: 57.26 MHz -> 17.46 ns/tick; ~4.657e16 ticks since anchor.

## Verifying consensus (actual security)

Records are ECDSA-signed by their owning wallet, block headers are signed by the
AGENT identity, verifiers (Node 0D + MATRIX-0..N + AGENT + MASTER) hold public
keys only, and the persisted registry is HMAC-sealed at rest. See `SECURITY.md`.

```powershell
$env:IMAM_MNEMONIC = "your-12-word-anchor-mnemonic"   # the ONLY secret (kept out of the repo)
python run_server.py                            # binds 127.0.0.1:8000
# then in another shell:
curl -X POST http://localhost:8000/api/toy/step          # ECDSA-signed record
curl -X POST http://localhost:8000/api/internet/ingest   # AGENT-signed block
curl http://localhost:8000/api/internet/verify           # full crypto battery
curl http://localhost:8000/api/internet/consensus        # VALID (8/8 nodes)
curl "http://localhost:8000/api/internet/consensus?tamper_seq=0"   # INVALID
curl "http://localhost:8000/api/internet/proof?seq=0"    # Merkle inclusion proof
curl -X POST http://localhost:8000/api/crawler/actual    # apply real scan + sweep
curl http://localhost:8000/api/security                  # posture overview
```

Hardening: `HOST` (default `127.0.0.1`), `PORT`, `API_TOKEN` (requires
`Authorization: Bearer <token>` on `/api/*`), `TLS_CERT`/`TLS_KEY` (HTTPS).

## Notes

- Toy only: wallet keys never leave the machine and nothing is broadcast.
- Keys are memory-only; the mnemonic is env-only; `data/` is `.gitignore`d.
- `bip-utils` needs a `coincurve` wheel for your interpreter; on interpreters
  without it the engine/agent use the deterministic fold-identity fallback
  (digest signatures, not ECDSA).
- Full integration write-up: `INTEGRATION.md`. Threat model: `SECURITY.md`.
  Milestone checklist: `ROADMAP.txt`.
