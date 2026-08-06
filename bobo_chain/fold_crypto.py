"""
===================================================================================
FOLD CRYPTO -- ACTUAL-SECURITY SIGNING LAYER FOR THE DECENTRALIZED INTERNET
-----------------------------------------------------------------------------------
Replaces the fold-digest (sha256 of a seed string) with REAL secp256k1 ECDSA over
the available identities derived from the anchor mnemonic:

  ACCOUNT 0  -> scannable wallet matrix   (MATRIX-0..N, each signs its own records)
  ACCOUNT 1  -> fold agent identity       (AGENT, signs every internet block header)
  ACCOUNT 2  -> MASTER fold-collector     (MASTER, signs parked / trash-collection)

  - SIGN      : deterministic (RFC6979) recoverable ECDSA over the canonical
                record message; the 65-byte signature embeds the recovery id so
                any verifier can RECOVER the signer's public key from the record
                alone, no key lookup required.
  - VERIFY    : recover pubkey -> derive Ethereum address -> compare to the
                recorded signer identity (self-describing, no shared state).
  - SEAL      : at-rest integrity for state files (HMAC-SHA256 keyed by a device
                key derived from the mnemonic in memory; the key is never written
                to disk).

KEY CUSTODY: private keys live only in memory, are derived on demand, are never
persisted, never logged, and never broadcast. The mnemonic is the only secret and
it comes exclusively from the IMAM_MNEMONIC environment variable.
===================================================================================
"""

import hashlib
import hmac
import json
from hashlib import sha256

import coincurve

from imam_agent import ImamFoldAgent, FOLD_METRIC, ANCHOR_DT


def _address_from_public_key(pub_hex: str) -> str:
    """Ethereum address (lowercase) from an uncompressed 0x-prefixed pubkey."""
    pub_bytes = bytes.fromhex(pub_hex[2:] if pub_hex.startswith("0x") else pub_hex)
    from web3 import AsyncWeb3
    return "0x" + AsyncWeb3().keccak(pub_bytes[1:])[-20:].hex().lower()


def record_message(record: dict) -> str:
    """Canonical signed message for an activity record. The verifier rebuilds
    exactly this string from the stored fields, so every field it covers is
    cryptographically authenticated (tamper with any of them and the signature
    no longer recovers to the signer's key)."""
    return (f"{record['timestamp_schema']}|{record['address']}|"
            f"{record['wallet_index']}:{record['channel']}|{record['type']}|"
            f"{record['seq']}|{record.get('seed', '')}")


def device_seal_key(mnemonic: str) -> bytes:
    """In-memory device key for at-rest state sealing. Derived from the mnemonic
    with PBKDF2; never persisted, so only this machine/process lineage can re-seal."""
    return hashlib.pbkdf2_hmac(
        "sha256", mnemonic.encode("utf-8"),
        b"IMAM-decentralized-internet-seal-v1", 100_000, 32)


def message_digest(message: str) -> bytes:
    """The exact 32-byte sha256 digest over the canonical UTF-8 message that is
    signed / verified by the secp256k1 layer."""
    return sha256(message.encode("utf-8")).digest()


def hmac_seal(key: bytes, payload: str) -> str:
    return hmac.new(key, payload.encode("utf-8"), hashlib.sha256).hexdigest()


class SigningAuthority:
    """Real ECDSA sign/verify over the available identities (accounts 0/1/2)."""

    def __init__(self, agent: ImamFoldAgent):
        self.agent = agent
        self.engine = agent.engine
        self.matrix_size = agent.matrix_size
        self._identities = {}
        self._build_identities()

    # ------------------------------------------------------------------ #
    def _build_identities(self) -> None:
        """Identity map: role -> {address, public_key, private_key}."""
        for i, w in enumerate(self.engine.wallets):
            self._identities[f"MATRIX-{i}"] = {
                "address": w["address"], "public_key": w["public_key"],
                "private_key": w["private_key"], "account": 0, "index": i,
            }
        self._identities["AGENT"] = {
            "address": self.agent.agent_wallet["address"],
            "public_key": self.agent.agent_wallet.get("public_key", ""),
            "private_key": self.agent.agent_wallet["private_key"],
            "account": 1, "index": 0,
        }
        master = self.engine.derive_identity(account=2, index=0)
        self._identities["MASTER"] = {
            "address": master["address"], "public_key": master["public_key"],
            "private_key": master["private_key"], "account": 2, "index": 0,
        }

    def roles(self) -> dict:
        return {role: {"address": idn["address"], "public_key": idn["public_key"]}
                for role, idn in self._identities.items()}

    def identity_map(self) -> dict:
        """address(lower) -> public_key, for independent verification."""
        return {idn["address"].lower(): idn["public_key"]
                for idn in self._identities.values()}

    def resolve_role(self, record: dict) -> str:
        if record.get("signer_role"):
            return record["signer_role"]
        if record.get("dead_wallet_play"):
            return "MASTER"
        if record["wallet_index"] >= self.matrix_size:
            return "MASTER"
        return f"MATRIX-{record['wallet_index']}"

    # ------------------------------------------------------------------ #
    def sign_message(self, message: str, role: str) -> str:
        """Recoverable ECDSA (RFC6979 deterministic) signature, 130 hex chars:
        r(64) + s(64) + recovery_id(2)."""
        idn = self._identities[role]
        priv_hex = idn["private_key"]
        if not priv_hex:
            raise RuntimeError(f"no private key for role {role} (fold fallback)")
        sk = coincurve.PrivateKey(bytes.fromhex(priv_hex[2:]))
        sig65 = sk.sign_recoverable(message_digest(message), hasher=None)
        return sig65[:64].hex() + format(sig65[64], "02x")

    def sign_record(self, record: dict) -> dict:
        """Sign an activity record in place: adds seed, fold_digest, real
        signature, signer role/address, and the signing timestamp."""
        record.setdefault("seed", hashlib.sha256(
            f"{record['timestamp_schema']}|{record['address']}|"
            f"{record['wallet_index']}:{record['channel']}|{record['type']}|"
            f"{record['seq']}".encode()).hexdigest()[:16])
        record["fold_digest"] = sha256(
            record_message(record).encode("utf-8")).hexdigest()
        role = self.resolve_role(record)
        record["signer_role"] = role
        record["signer_address"] = self._identities[role]["address"]
        record["signature"] = self.sign_message(record_message(record), role)
        record["auth"] = "ECDSA-SECP256K1"
        return record

    # ------------------------------------------------------------------ #
    def verify_record(self, record: dict) -> tuple:
        """Cryptographically verify one record. Returns (ok, reason)."""
        if record.get("auth") != "ECDSA-SECP256K1" or not record.get("signature"):
            return False, "NOT_ECDSA_SIGNED"
        try:
            role = record.get("signer_role") or self.resolve_role(record)
            idn = self._identities.get(role)
            if idn is None:
                return False, f"UNKNOWN_SIGNER_ROLE:{role}"
            sig = record["signature"]
            sig65 = bytes.fromhex(sig)
            pk = coincurve.PublicKey.from_signature_and_message(
                sig65, message_digest(record_message(record)), hasher=None)
            recovered_pub = "0x" + pk.format(compressed=False).hex()
            recovered_addr = _address_from_public_key(recovered_pub)
            if recovered_pub.lower() != idn["public_key"].lower():
                return False, "RECOVERED_PUBKEY_MISMATCH"
            if recovered_addr != idn["address"].lower():
                return False, "RECOVERED_ADDRESS_MISMATCH"
            if role.startswith("MATRIX-"):
                if record["address"].lower() != idn["address"].lower():
                    return False, "RECORD_ADDRESS_NOT_OWNER"
            return True, "OK"
        except Exception as e:
            return False, f"VERIFY_ERROR:{type(e).__name__}:{e}"

    def verify_block(self, block: dict, payload: dict) -> tuple:
        """Verify a block header signature. The payload is the re-derived block
        header (index/prev_hash/merkle/...), canonicalized exactly as at signing
        time; the signature must recover to the AGENT identity."""
        role = block.get("signer_role", "AGENT")
        idn = self._identities.get(role)
        if idn is None:
            return False, f"UNKNOWN_BLOCK_SIGNER:{role}"
        canonical = json.dumps(payload, sort_keys=True)
        try:
            sig = block["signature"]
            pk = coincurve.PublicKey.from_signature_and_message(
                bytes.fromhex(sig), message_digest(canonical), hasher=None)
            recovered_pub = "0x" + pk.format(compressed=False).hex()
            if recovered_pub.lower() != idn["public_key"].lower():
                return False, "BLOCK_SIGNER_PUBKEY_MISMATCH"
            return True, "OK"
        except Exception as e:
            return False, f"BLOCK_VERIFY_ERROR:{type(e).__name__}:{e}"

    def verify_records(self, records: list) -> dict:
        """Battery over a list; returns summary + per-record verdicts."""
        results = []
        ok = 0
        for r in records:
            valid, reason = self.verify_record(r)
            results.append({"seq": r.get("seq"), "role": r.get("signer_role"),
                            "ok": valid, "reason": reason})
            ok += 1 if valid else 0
        return {"total": len(records), "valid": ok,
                "invalid": len(records) - ok,
                "records": results}

    def wipe(self) -> None:
        """Drop private key material from memory (identities stay public)."""
        for idn in self._identities.values():
            idn["private_key"] = ""
