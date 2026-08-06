"""
===================================================================================
COLD-WALLET CRAWLER (ACTUAL / REAL CHAIN DATA ONLY)
-----------------------------------------------------------------------------------
A toy layer on top of the fold-wallet stack, running exclusively on real
on-chain data:

  - SCAN   : a real wallet-matrix scan (engine.run_full_scan) replaces every
             cold wallet's reserve with its REAL on-chain balance (native +
             ERC-20 across all networks in networks.json) and records the real
             transaction counts for dormancy detection.
  - CRAWLER: scans the cold-wallet matrix and flags INACTIVE / DORMANT wallets
             (real nonce == 0, or not active for a window of crawls). Each
             inactive wallet's reserve is ROUTED into the MASTER wallet
             (SWEEP record).

There is no simulated reserve regeneration and no master payoff toy: balances
come from the last applied scan and sweeps only move tokens into MASTER.

Every SWEEP record is stamped in the universal schema 26/10/2000T10:26:20.00
plus fold ticks since the anchor, and signed with a deterministic sha256
digest -- consistent with agent_toy / internet_registry.

All state persists to data/cold_crawler.json. No real transactions; nothing is
broadcast. Purely educational.
===================================================================================
"""

import json
import os
from datetime import datetime, timezone

from imam_agent import (ImamFoldAgent, fold_timestamp, FOLD_PERIOD_S,
                        ANCHOR_DT, FOLD_METRIC)
from agent_toy import sha256_hex, ColdWalletToy

STATE_PATH = os.path.join("data", "cold_crawler.json")

SWEEP_MIN = 0.5                  # reserve must clear this to be swept
INACTIVITY_WINDOW_CRAWLS = 2     # crawls since last active before INACTIVE


def _ticks(now: datetime | None = None) -> int:
    now = now or datetime.now(timezone.utc)
    return int((now - ANCHOR_DT).total_seconds() / FOLD_PERIOD_S)


class ColdWalletCrawler:
    """Cold-wallet crawler on real data: dormancy detection from the applied
    scan, sweep-to-master routing. No payoff, no simulation."""

    def __init__(self, agent: ImamFoldAgent, toy: ColdWalletToy,
                 state_path: str = STATE_PATH):
        self.agent = agent
        self.engine = agent.engine
        self.toy = toy
        self.matrix_size = agent.matrix_size
        self.state_path = state_path
        self.master = self._derive_account(self.engine, 0)
        self.state = self._load_state()

    # ------------------------------------------------------------------ #
    @staticmethod
    def _derive_account(engine, index: int) -> dict:
        """Master toy account: BIP44 Ethereum account 2, index `index`,
        derived from the engine's real coincurve BIP44 path (signable key).
        Falls back to bip_utils, then to a fold-derived digest."""
        try:
            from engine import _bip44_eth_private_key
            from web3 import AsyncWeb3
            priv = _bip44_eth_private_key(engine.mnemonic, index, account=2)
            priv_hex = f"0x{priv:064x}"
            account = AsyncWeb3().eth.account.from_key(priv_hex)
            import coincurve
            pub = coincurve.PublicKey.from_valid_secret(
                priv.to_bytes(32, "big")).format(compressed=False)
            return {"address": account.address, "private_key": priv_hex,
                    "public_key": "0x" + pub.hex()}
        except Exception:
            try:
                from bip_utils import (Bip39SeedGenerator, Bip44, Bip44Coins,
                                       Bip44Changes)
                seed = Bip39SeedGenerator(engine.mnemonic).Generate()
                ctx = (Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
                       .Purpose().Coin().Account(2).Change(Bip44Changes.CHAIN_EXT)
                       .AddressIndex(index))
                return {"address": ctx.PublicKey().ToAddress(),
                        "private_key": f"0x{ctx.PrivateKey().Raw().ToHex()}"}
            except Exception:
                digest = sha256_hex(f"{fold_timestamp(ANCHOR_DT)}|{FOLD_METRIC}|"
                                    f"ACCOUNT2|{index}")
                return {"address": "0x" + digest[:40], "private_key": "",
                        "derivation": "FOLD-DERIVED-FALLBACK (no bip44 available)"}

    # ------------------------------------------------------------------ #
    def _default_state(self) -> dict:
        hot = [{
            "wallet_index": i,
            "tier": "matrix",
            "address": self.engine.wallets[i]["address"],
            "reserve": 0.0,
            "actual_nonce": -1,
            "last_active_crawl": -1,
            "last_seen_jump": -1,
        } for i in range(self.matrix_size)]
        hot.append({
            "wallet_index": self.matrix_size,
            "tier": "master",
            "address": self.master["address"],
            "reserve": 0.0,
            "actual_nonce": -1,
            "last_active_crawl": -1,
            "last_seen_jump": -1,
        })
        return {
            "mode": "actual",
            "actual_scan_schema": None,
            "actual_scan_ticks": 0,
            "crawl_count": 0,
            "master_balance": 0.0,
            "swept_total": 0.0,
            "cold": [{
                "wallet_index": i,
                "address": self.engine.wallets[i]["address"],
                "reserve": 0.0,
                "last_seen_jump": -1,
                "last_active_crawl": -1,
                "actual_nonce": -1,
            } for i in range(self.matrix_size)],
            "hot": hot,
            "sweeps": [],
            "trash": [],
        }

    def _load_state(self) -> dict:
        default = self._default_state()
        if os.path.exists(self.state_path):
            try:
                with open(self.state_path, "r", encoding="utf-8") as f:
                    default.update(json.load(f))
            except Exception:
                pass
        return self._validate_state(default)

    def _validate_state(self, state: dict) -> dict:
        """Repair state after a matrix resize OR a mnemonic/engine change:
        cold-wallet addresses are rebound to the engine's current derivation
        and stale reserves from the old addresses are dropped. The hot tier
        (all matrix wallets + MASTER) is rebound the same way."""
        fresh = self._default_state()["cold"]
        engine_addrs = [c["address"] for c in fresh]
        if len(state["cold"]) != self.matrix_size or \
                [c["address"] for c in state["cold"]] != engine_addrs:
            state["cold"] = fresh
        fresh_hot = self._default_state()["hot"]
        hot_addrs = [h["address"] for h in fresh_hot]
        if len(state.get("hot", [])) != len(fresh_hot) or \
                [h["address"] for h in state.get("hot", [])] != hot_addrs:
            state["hot"] = fresh_hot
        return state

    def _save_state(self) -> None:
        os.makedirs(os.path.dirname(self.state_path) or ".", exist_ok=True)
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    # ------------------------------------------------------------------ #
    def _refresh_last_seen(self) -> None:
        """Sync each cold wallet's last-seen jump from the toy ledger."""
        seen = {}
        for a in self.toy.state["activity"]:
            seen[a["wallet_index"]] = max(seen.get(a["wallet_index"], -1),
                                          a["seq"])
        for c in self.state["cold"]:
            c["last_seen_jump"] = max(c["last_seen_jump"],
                                      seen.get(c["wallet_index"], -1))
        for h in self.state["hot"]:
            h["last_seen_jump"] = max(h["last_seen_jump"],
                                      seen.get(h["wallet_index"], -1))

    def _is_inactive(self, cold: dict) -> bool:
        """Inactivity is measured in crawl time. Wallets scanned with a real
        zero transaction count (actual_nonce == 0) are DORMANT and sweepable;
        otherwise a wallet is INACTIVE once it has not been active for a
        window of crawls."""
        if cold.get("actual_nonce", 0) == 0:
            return True
        if cold["last_active_crawl"] < 0:
            return True
        return (self.state["crawl_count"] - cold["last_active_crawl"]) > \
            INACTIVITY_WINDOW_CRAWLS

    # ------------------------------------------------------------------ #
    def _sweep(self, cold: dict, now: datetime) -> dict:
        """Route one inactive wallet's full reserve into the master wallet."""
        amount = round(cold["reserve"], 6)
        cold["reserve"] = 0.0
        cold["last_active_crawl"] = self.state["crawl_count"]
        cold["last_seen_jump"] = self.toy.state["jumps"]
        self.state["master_balance"] = round(self.state["master_balance"] + amount, 6)
        self.state["swept_total"] = round(self.state["swept_total"] + amount, 6)
        ticks = _ticks(now)
        record = {
            "seq": len(self.state["sweeps"]),
            "kind": "SWEEP",
            "crawl": self.state["crawl_count"],
            "wallet_index": cold["wallet_index"],
            "address": cold["address"],
            "amount": amount,
            "to": "MASTER",
            "master_address": self.master["address"],
            "balance_after": self.state["master_balance"],
            "timestamp_schema": fold_timestamp(now),
            "fold_ticks_since_anchor": ticks,
            "signature": sha256_hex(
                f"{fold_timestamp(now)}|{cold['address']}|SWEEP|{amount}|"
                f"{self.state['crawl_count']}|{ticks}")[:64],
        }
        self.state["sweeps"].append(record)
        return record

    # ------------------------------------------------------------------ #
    def run(self) -> dict:
        """One crawl cycle over the applied real balances: sweep every inactive
        reserve into the master wallet. Returns the fresh records plus a
        summary."""
        now = datetime.now(timezone.utc)
        self._refresh_last_seen()
        self.state["crawl_count"] += 1
        new_sweeps = []
        for c in self.state["cold"]:
            if self._is_inactive(c) and c["reserve"] >= SWEEP_MIN:
                new_sweeps.append(self._sweep(c, now))
        self._save_state()
        return {"run": self.state["crawl_count"], "sweeps": new_sweeps,
                "summary": self.summary()}

    # ------------------------------------------------------------------ #
    def apply_actual_scan(self, scan_result: dict) -> dict:
        """Replace every cold wallet's reserve with its REAL on-chain balance
        from the wallet-matrix scan (native + ERC-20 across all networks), and
        record the real transaction counts for dormancy detection.

        The sweep mechanics stay as toy accounting (no keys leave the machine,
        nothing is broadcast) but every decision now runs on real on-chain data.
        """
        now = datetime.now(timezone.utc)
        leaderboard = {item["index"]: item for item in scan_result["leaderboard"]}
        applied = 0
        for c in self.state["cold"]:
            item = leaderboard.get(c["wallet_index"])
            if item is None:
                continue
            bal = round(item["total_native_balance"] +
                        sum(item["tokens"].values()), 6)
            c["reserve"] = bal
            c["actual_nonce"] = item["total_nonces"]
            applied += 1
        for h in self.state["hot"]:
            item = leaderboard.get(h["wallet_index"])
            if item is None:
                continue
            bal = round(item["total_native_balance"] +
                        sum(item["tokens"].values()), 6)
            h["reserve"] = bal
            h["actual_nonce"] = item["total_nonces"]
        self.state["actual_scan_schema"] = fold_timestamp(now)
        self.state["actual_scan_ticks"] = _ticks(now)
        self._save_state()
        return {"applied": applied, "mode": "actual",
                "scan_schema": self.state["actual_scan_schema"],
                "matrix_size": self.matrix_size}

    def inactive_indices(self) -> list:
        """Matrix wallets the crawler currently deems inactive (dormant per
        real nonce, or past the inactivity window)."""
        return [c["wallet_index"] for c in self.state["cold"]
                if self._is_inactive(c)]

    def hot_table(self) -> list:
        out = []
        for h in self.state["hot"]:
            nonce = h.get("actual_nonce", -1)
            out.append({
                "wallet_index": h["wallet_index"],
                "tier": h.get("tier", "matrix"),
                "address": h["address"],
                "reserve": h["reserve"],
                "actual_nonce": nonce,
                "last_active_crawl": h["last_active_crawl"],
                "status": "ACTIVE" if nonce > 0 else ("IDLE" if nonce == 0 else "UNSCANNED"),
            })
        return out

    def cold_table(self) -> list:
        out = []
        for c in self.state["cold"]:
            inactive = self._is_inactive(c)
            out.append({
                "wallet_index": c["wallet_index"],
                "address": c["address"],
                "public_key": self._public_key(c["wallet_index"]),
                "reserve": c["reserve"],
                "last_seen_jump": c["last_seen_jump"],
                "actual_nonce": c.get("actual_nonce", -1),
                "status": "TRASH" if c.get("cleaned") else
                          ("INACTIVE" if inactive and c["reserve"] > 0 else
                           ("DORMANT" if inactive else "ACTIVE")),
            })
        return out

    def _public_key(self, wallet_index: int) -> str:
        try:
            return self.engine.wallets[wallet_index].get("public_key", "")
        except (IndexError, KeyError):
            return ""

    def clean_trash(self, threshold: float = SWEEP_MIN) -> dict:
        """Clean TRASH wallets: zero/dust-reserve cold wallets are zeroed,
        flagged as cleaned, and logged with their public key in the trash
        ledger. Returns the cleaned entries plus the full listing."""
        now = datetime.now(timezone.utc)
        ticks = _ticks(now)
        removed = []
        for c in self.state["cold"]:
            if c.get("cleaned") or c["reserve"] >= threshold:
                continue
            removed.append({
                "wallet_index": c["wallet_index"],
                "address": c["address"],
                "public_key": self._public_key(c["wallet_index"]),
                "reserve": c["reserve"],
                "actual_nonce": c.get("actual_nonce", -1),
                "cleaned_schema": fold_timestamp(now),
                "fold_ticks_since_anchor": ticks,
                "reason": "DUST/EMPTY (below sweep minimum)" if c["reserve"] > 0
                          else "EMPTY (zero reserve)",
            })
            c["reserve"] = 0.0
            c["cleaned"] = True
        self.state["trash"].extend(removed)
        self._save_state()
        return {"cleaned": removed, "trash_count": len(removed),
                "listing": self.cold_table()}

    def listing(self) -> list:
        """Full cold-wallet listing with public keys."""
        return self.cold_table()

    def ledger(self, limit: int = 20) -> list:
        return list(reversed(self.state["sweeps"][-limit:]))

    def summary(self) -> dict:
        cold = self.state["cold"]
        hot = self.state["hot"]
        return {
            "crawler": "COLD-WALLET CRAWLER (ACTUAL)",
            "mode": "actual",
            "reserve_source": "REAL CHAIN SCAN",
            "actual_scan_schema": self.state["actual_scan_schema"],
            "anchor_schema": fold_timestamp(ANCHOR_DT),
            "fold_metric": FOLD_METRIC,
            "master_address": self.master["address"],
            "master_balance": self.state["master_balance"],
            "swept_total": self.state["swept_total"],
            "crawl_count": self.state["crawl_count"],
            "sweep_min": SWEEP_MIN,
            "inactivity_window_crawls": INACTIVITY_WINDOW_CRAWLS,
            "reserve_total": round(sum(c["reserve"] for c in cold), 6),
            "inactive_wallets": [c["wallet_index"] for c in cold
                                 if self._is_inactive(c) and c["reserve"] > 0],
            "actual_dormant": [c["wallet_index"] for c in cold
                               if c.get("actual_nonce", 0) == 0
                               and c["reserve"] > 0],
            "hot_count": len(hot),
            "hot_total": round(sum(h["reserve"] for h in hot), 6),
            "hot_active": [h["wallet_index"] for h in hot
                           if h.get("actual_nonce", 0) > 0],
            "hot_idle": [h["wallet_index"] for h in hot
                         if h.get("actual_nonce", 0) == 0],
        }

    def reset(self) -> dict:
        self.state = self._default_state()
        self._save_state()
        return self.summary()
