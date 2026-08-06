"""
===================================================================================
COLD-WALLET ACTIVITY + NEIGHBOR-JUMP AGENT TOY
-----------------------------------------------------------------------------------
A toy agent that treats the fold-wallet matrix as COLD wallets (signing keys held
offline; nothing is ever broadcast) and runs them for "activity": the agent token
walks the 57,434,001 fold channels by NEIGHBOR JUMPING -- moving one channel at a
time, and hopping to the neighbor wallet's edge channel when it crosses a wallet
boundary. Every landing produces a deterministic activity record (SIGN / SWEEP /
ROTATE / JUMP) timestamped in the universal schema 26/10/2000T10:26:20.00.

All state is persisted to data/agent_toy_activity.json (append-only activity log).
No real transactions, no private keys leave the machine -- purely educational.
===================================================================================
"""

import hashlib
import json
import os
from datetime import datetime, timezone

from imam_agent import ImamFoldAgent, fold_timestamp, FOLD_PERIOD_S, ANCHOR_DT

ACTIVITY_TYPES = ["SIGN", "SWEEP", "ROTATE", "JUMP"]
STATE_PATH = os.path.join("data", "agent_toy_activity.json")


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


class ColdWalletToy:
    """Cold-wallet activity simulator with fold-channel neighbor jumping."""

    def __init__(self, agent: ImamFoldAgent, state_path: str = STATE_PATH,
                 master_wallet: dict | None = None,
                 signing=None):
        self.agent = agent
        self.matrix_size = agent.matrix_size
        self.ranges = agent.partition["ranges"]
        self.anchor = ANCHOR_DT
        self.state_path = state_path
        self.master = master_wallet
        self.signing = signing
        self.state = self._load_state()

    # ------------------------------------------------------------------ #
    def set_master(self, address: str) -> None:
        """Point the toy at the MASTER account (the 'unused' wallet) that the
        token parks on when every matrix wallet is turned off."""
        self.master = {"address": address, "index": self.matrix_size}

    def _on_wallets(self, state: dict | None = None) -> list:
        state = state if state is not None else self.state
        return [i for i in range(self.matrix_size)
                if i not in state.get("off", [])]

    def _first_on_wallet(self, state: dict | None = None):
        on = self._on_wallets(state)
        return on[0] if on else None

    def _wallet_address(self, idx: int) -> str:
        if idx >= self.matrix_size:
            return self.master["address"] if self.master else "0xMASTER"
        return self.agent.engine.wallets[idx]["address"]

    # ------------------------------------------------------------------ #
    def _load_state(self) -> dict:
        default = {
            "token_wallet": 0,
            "token_channel": self.ranges[0]["channel_start"],
            "jumps": 0,
            "off": [],
            "activity": [],
        }
        if os.path.exists(self.state_path):
            try:
                with open(self.state_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                default.update({k: v for k, v in loaded.items()
                                if k in default})
            except Exception:
                pass
        return self._validate_state(default)

    def _validate_state(self, state: dict) -> dict:
        """Repair state after a matrix resizing: keep the token in range and
        never seated on a turned-off wallet (park on MASTER when all are off)."""
        state["off"] = sorted({int(i) for i in state.get("off", [])
                               if 0 <= int(i) < self.matrix_size})
        w = state["token_wallet"]
        if not (0 <= w < self.matrix_size):
            w, state["token_channel"] = 0, self.ranges[0]["channel_start"]
        if w in state["off"]:
            nxt = self._first_on_wallet(state)
            if nxt is None:
                w, state["token_channel"] = self.matrix_size, 0
            else:
                w, state["token_channel"] = nxt, self.ranges[nxt]["channel_start"]
        if w < self.matrix_size:
            r = self.ranges[w]
            if not (r["channel_start"] <= state["token_channel"] <= r["channel_end"]):
                state["token_channel"] = r["channel_start"]
        state["token_wallet"] = w
        return state

    def _save_state(self) -> None:
        os.makedirs(os.path.dirname(self.state_path) or ".", exist_ok=True)
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    # ------------------------------------------------------------------ #
    def set_power(self, off: list, relocate: bool = True) -> dict:
        """Turn matrix wallets OFF (the token skips them) or ON. If the token
        sits on a wallet that just turned off it relocates to the next ON
        wallet, or parks on MASTER when every matrix wallet is off."""
        self.state["off"] = sorted({int(i) for i in off
                                    if 0 <= int(i) < self.matrix_size})
        w = self.state["token_wallet"]
        if relocate and w < self.matrix_size and w in self.state["off"]:
            nxt = self._first_on_wallet()
            if nxt is None:
                self.state["token_wallet"] = self.matrix_size
                self.state["token_channel"] = 0
            else:
                self.state["token_wallet"] = nxt
                self.state["token_channel"] = self.ranges[nxt]["channel_start"]
        self._save_state()
        return self.summary()

    def _neighbor(self, wallet_index: int, channel: int,
                  on_wallets: list):
        """Next channel in fold order; across a wallet boundary the token
        NEIGHBOR-JUMPS to the next ON wallet's first channel (ring order,
        skipping turned-off wallets)."""
        r = self.ranges[wallet_index]
        if channel < r["channel_end"]:
            return wallet_index, channel + 1
        nxt = (wallet_index + 1) % self.matrix_size
        while nxt not in on_wallets:
            nxt = (nxt + 1) % self.matrix_size
        return nxt, self.ranges[nxt]["channel_start"]

    def _seed(self) -> int:
        """Deterministic per-step seed from the fold clock + jump count."""
        now = datetime.now(timezone.utc)
        ticks = int((now - self.anchor).total_seconds() / FOLD_PERIOD_S)
        return ticks ^ self.state["jumps"]

    # ------------------------------------------------------------------ #
    def cold_wallets(self) -> list:
        """The matrix wallets, labeled COLD (keys offline) with channel ranges."""
        out = []
        for i, w in enumerate(self.agent.engine.wallets):
            r = self.ranges[i]
            out.append({
                "wallet_index": i,
                "address": w["address"],
                "status": "COLD",
                "channel_start": r["channel_start"],
                "channel_end": r["channel_end"],
                "channel_count": r["channel_count"],
            })
        return out

    def step(self, activity_type: str | None = None) -> dict:
        """Run one activity + one neighbor jump; append to the ledger. When
        every matrix wallet is turned off the token plays on the unused
        MASTER wallet (parked, no channel movement). Records are ECDSA-signed
        by the wallet that owns the channel (MASTER for parked / trash play)
        when a SigningAuthority is attached."""
        now = datetime.now(timezone.utc)
        seed = self._seed()
        atype = activity_type or ACTIVITY_TYPES[self.state["jumps"] % len(ACTIVITY_TYPES)]
        w, c = self.state["token_wallet"], self.state["token_channel"]
        addr = self._wallet_address(w)
        on = self._on_wallets()
        parked = w >= self.matrix_size or not on
        if parked:
            nw, nc = w, c
        else:
            nw, nc = self._neighbor(w, c, on)
        record = {
            "seq": self.state["jumps"],
            "type": atype,
            "wallet_index": w,
            "address": addr,
            "channel": c,
            "timestamp_schema": fold_timestamp(now),
            "neighbor_jump": nw != w,
            "parked_on_master": parked and w >= self.matrix_size,
            "next_wallet_index": nw,
            "next_channel": nc,
        }
        if self.signing is not None:
            record["seed"] = seed
            self.signing.sign_record(record)
        else:
            record["seed"] = seed
            record["signature"] = sha256_hex(
                f"{fold_timestamp(now)}|{addr}|{w}:{c}|{atype}|{self.state['jumps']}|{seed}"
            )[:64]
        self.state["activity"].append(record)
        self.state["jumps"] += 1
        self.state["token_wallet"] = nw
        self.state["token_channel"] = nc
        self._save_state()
        return record

    def play_trash(self, dead_wallets: list, steps: int = 1) -> dict:
        """Play on the dead-wallet collection (the crawler's trash ledger):
        each step consumes one dead wallet in order and appends a TRASH record
        carrying its public key + cleaned schema + reason. Falls back to a
        regular SIGN step when the collection is empty."""
        records = []
        for _ in range(max(1, min(steps, 10_000))):
            if not dead_wallets:
                records.append(self.step("SIGN"))
                continue
            dead = dead_wallets[self.state["jumps"] % len(dead_wallets)]
            now = datetime.now(timezone.utc)
            seed = self._seed()
            w = dead.get("wallet_index", self.matrix_size)
            addr = dead.get("address") or self._wallet_address(w)
            c = self.state["token_channel"]
            atype = "TRASH"
            record = {
                "seq": self.state["jumps"],
                "type": atype,
                "wallet_index": w,
                "address": addr,
                "public_key": dead.get("public_key", ""),
                "channel": c,
                "timestamp_schema": fold_timestamp(now),
                "cleaned_schema": dead.get("cleaned_schema"),
                "fold_ticks_since_anchor": dead.get("fold_ticks_since_anchor"),
                "reason": dead.get("reason"),
                "neighbor_jump": False,
                "parked_on_master": False,
                "dead_wallet_play": True,
            }
            if self.signing is not None:
                record["seed"] = seed
                self.signing.sign_record(record)
            else:
                record["seed"] = seed
                record["signature"] = sha256_hex(
                    f"{fold_timestamp(now)}|{addr}|{w}:{c}|{atype}|{self.state['jumps']}|{seed}"
                )[:64]
            self.state["activity"].append(record)
            self.state["jumps"] += 1
            records.append(record)
        self._save_state()
        return {"steps": len(records), "records": records, "summary": self.summary()}

    def run(self, steps: int = 1, activity_type: str | None = None) -> dict:
        """Run N steps; returns the summary + the new records."""
        records = []
        for _ in range(steps):
            records.append(self.step(activity_type))
        return {"steps": steps, "records": records, "summary": self.summary()}

    def power_table(self) -> list:
        """Per-wallet power state: matrix wallets plus the unused MASTER."""
        off = set(self.state.get("off", []))
        out = []
        for i in range(self.matrix_size):
            w = self.agent.engine.wallets[i]
            out.append({
                "wallet_index": i,
                "address": w["address"],
                "power": "OFF" if i in off else "ON",
                "status": "COLD",
                "channel_count": self.ranges[i]["channel_count"],
            })
        out.append({
            "wallet_index": self.matrix_size,
            "address": self.master["address"] if self.master else "0xMASTER",
            "power": "ON",
            "status": "UNUSED-MASTER",
            "channel_count": 0,
        })
        return out

    def summary(self) -> dict:
        activity = self.state["activity"]
        by_type = {}
        for a in activity:
            by_type[a["type"]] = by_type.get(a["type"], 0) + 1
        cold_crossed = sum(1 for a in activity if a["neighbor_jump"])
        signed = sum(1 for a in activity if a.get("auth") == "ECDSA-SECP256K1")
        w, c = self.state["token_wallet"], self.state["token_channel"]
        return {
            "token_wallet": w,
            "token_channel": c,
            "token_address": self._wallet_address(w),
            "parked_on_master": w >= self.matrix_size,
            "jumps": self.state["jumps"],
            "activity_count": len(activity),
            "activity_by_type": by_type,
            "cold_wallet_crossings": cold_crossed,
            "auth_mode": "ECDSA-SECP256K1" if self.signing is not None
                          else "FOLD-DIGEST",
            "signed_records": signed,
            "cold_wallets_total": self.matrix_size,
            "off_wallets": sorted(self.state.get("off", [])),
            "on_wallets": self._on_wallets(),
            "master_address": self.master["address"] if self.master else None,
            "channel_integrity": self.agent.partition["integrity"],
        }

    def activity(self, limit: int = 20) -> list:
        return list(reversed(self.state["activity"][-limit:]))

    def reset(self) -> dict:
        self.state = {
            "token_wallet": 0,
            "token_channel": self.ranges[0]["channel_start"],
            "jumps": 0,
            "off": [],
            "activity": [],
        }
        self._save_state()
        return self.summary()

    # ------------------------------------------------------------------ #
    def migrate_signatures(self) -> dict:
        """Upgrade legacy records (fold-digest signatures, no auth) to real
        ECDSA signatures. The registry has no blocks over the old ledger yet,
        so re-signing in place is safe; every record becomes cryptographically
        authenticated by the wallet that owns its channel."""
        if self.signing is None:
            return {"migrated": 0, "message": "no SigningAuthority attached"}
        migrated = 0
        for r in self.state["activity"]:
            if r.get("auth") != "ECDSA-SECP256K1":
                r.setdefault("seed", hashlib.sha256(
                    f"{r['timestamp_schema']}|{r['address']}|"
                    f"{r['wallet_index']}:{r['channel']}|{r['type']}|"
                    f"{r['seq']}".encode()).hexdigest()[:16])
                r["migrated_to_ecdsa"] = True
                self.signing.sign_record(r)
                migrated += 1
        self._save_state()
        return {"migrated": migrated,
                "verified": self.verify_activity()}

    def verify_activity(self) -> dict:
        """Cryptographic verification of every activity record in the ledger."""
        if self.signing is None:
            return {"supported": False,
                    "message": "no SigningAuthority attached"}
        return self.signing.verify_records(self.state["activity"])
