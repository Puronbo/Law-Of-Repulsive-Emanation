# SECURITY — Decentralized Internet (Actual Security Model)

This document states the threat model and controls for the decentralized
internet registry (chain of custody + consensus) over the IMAM-V3 fold-wallet
stack. The stack is **accounting software**: it reads real chain data, signs
local records, and verifies them. It never broadcasts transactions.

## Identities (available assets)

All identity keys are derived from the anchor mnemonic (BIP44, secp256k1) via
`engine.derive_identity()`:

| Account | Role            | Signs |
|---|---|---|
| 0       | MATRIX-0..N      | activity records on its own channels |
| 1       | AGENT (fold agent) | every internet block header |
| 2       | MASTER           | parked / trash-collection records |

These are the only "assets" the decentralized internet uses: wallet identities,
not external balances.

## Cryptographic controls

1. **Record authentication — ECDSA (secp256k1).** Each activity record is signed
   with deterministic RFC6979 recoverable signatures (`fold_crypto.py`). The
   canonical message covers `schema|address|wallet:channel|type|seq|seed`, so
   every covered field is authenticated. Any verifier recovers the signer's
   public key from the signature alone.
2. **Block authentication.** Each block header is ECDSA-signed by the AGENT
   identity. Blocks cannot be re-minted or re-ordered without the agent key.
3. **Chain of custody.** `prev_hash` chaining + a Merkle root over the per-record
   signatures make every block tamper-evident.
4. **Independent verifiers.** Consensus nodes are the available identities
   (Node 0D, MATRIX-0..N, AGENT, MASTER). Verifiers hold **public keys only**
   and independently recompute the entire chain, verifying every record and
   block signature before voting. A single altered record/field flips consensus
   to INVALID. (`/api/internet/consensus?tamper_seq=N` demonstrates detection.)
5. **Merkle inclusion proofs.** Any record's membership in its block is provable
   with an O(log n) sibling path (`/api/internet/proof?seq=N`).
6. **At-rest integrity.** The persisted registry is sealed with HMAC-SHA256 keyed
   by an in-memory device key (PBKDF2 from the mnemonic; never written to disk).
   Any edit to the state file is flagged `TAMPERED` on load and blocks ingest
   until the operator explicitly re-seals (`POST /api/internet/reseal`).

## Key custody

- The mnemonic is the only secret; it comes **exclusively** from the
  `IMAM_MNEMONIC` environment variable (`run_server.py` refuses to boot without
  it).
- Private keys are derived in memory on demand and are **never persisted,
  logged, or broadcast**.
- State files (`data/*.json`) contain addresses, public keys, records, and
  seals — never private keys. The `.gitignore` excludes the `data/` tree.

## Transport

- The API binds `127.0.0.1` by default (`run_server.py`). Only set `HOST`
  explicitly if you need remote access.
- Set `API_TOKEN` to require `Authorization: Bearer <token>` on every `/api/*`
  route.
- Set `TLS_CERT` + `TLS_KEY` to serve HTTPS. Remote access without TLS and a
  token is strongly discouraged.
- Posture overview: `GET /api/security`.

## Threat model (what this does and does not protect)

| Threat | Control |
|---|---|
| Forged activity record | ECDSA signature fails verification → consensus INVALID |
| Record field edited after signing | Signature no longer recovers to signer → INVALID |
| Block re-mint / reorder | AGENT block signature + prev_hash chain → INVALID |
| State file edited on disk | At-rest HMAC seal → TAMPERED, ingest blocked |
| Compromised private keys | Out of scope here: keys never leave memory and the mnemonic is env-only |
| Remote attacker probing the API | Loopback bind + optional bearer token + optional TLS |
| On-chain rebalancing of real balances | Out of scope by design: nothing is ever broadcast |
