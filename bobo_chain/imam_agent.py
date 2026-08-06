"""
===================================================================================
IMAM-V3 FOLD-WALLET AGENT FOR THE DECENTRALIZED INTERNET
-----------------------------------------------------------------------------------
Binds the IMAM-v3 fold metric (57,434,001) to the multi-chain wallet matrix,
anchored to the universal date-and-time schema: 26/10/2000T10:26:20.00
(DD/MM/YYYYThh:mm:ss.cc, UTC).

  - IDENTITY   : a dedicated agent wallet (BIP44 Ethereum account 1, index 0),
                 separate from the scannable matrix wallets.
  - ANCHOR     : 2000-10-26 10:26:20.00 UTC (epoch seconds computed at runtime).
  - FOLD       : 57,434,001 fold channels, fully partitioned across the matrix.
  - CLOCK      : fold reference frequency 57.26 MHz -> fold period ~17.46 ns;
                 real time since the anchor is expressed as fold ticks.
  - INTEGRITY  : channel-partition check (sum of channel counts == fold metric)
                 plus a fold root over the anchored channel manifest.
All agent timestamps are rendered in the universal schema via fold_timestamp().
===================================================================================
"""

import hashlib
from datetime import datetime, timezone

from engine import MultiChainWalletEngine

FOLD_METRIC = 57_434_001              # IMAM-v3 fold count
FOLD_FREQUENCY_HZ = 57_260_000.0      # 57.26 MHz (Rydberg-scaled fold photon)
FOLD_PERIOD_S = 1.0 / FOLD_FREQUENCY_HZ   # ~17.46 ns per fold tick

ANCHOR_DT = datetime(2000, 10, 26, 10, 26, 20, 0, tzinfo=timezone.utc)


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def fold_timestamp(dt: datetime) -> str:
    """Render a datetime in the universal schema: 26/10/2000T10:26:20.00 UTC."""
    u = dt.astimezone(timezone.utc)
    return (f"{u.day:02d}/{u.month:02d}/{u.year:04d}"
            f"T{u.hour:02d}:{u.minute:02d}:{u.second:02d}.{u.microsecond // 10000:02d}")


class ImamFoldAgent:
    """Wallet agent that anchors the fold metric to the 26/10/2000T10:26:20.00
    schema and registers the wallet matrix as a fold-channel partition."""

    def __init__(self, engine: MultiChainWalletEngine):
        self.engine = engine
        self.matrix_size = engine.matrix_size
        self.fold = FOLD_METRIC
        self.anchor = ANCHOR_DT
        self.agent_wallet = self._derive_agent_wallet(engine)
        self.partition = self._partition_channels()

    @staticmethod
    def _derive_agent_wallet(engine: MultiChainWalletEngine) -> dict:
        """BIP44 Ethereum account 1, index 0: the agent identity address.

        Uses the engine's self-contained coincurve BIP44 derivation so the
        agent identity always gets a REAL signable key (the fold digest is
        only a last-resort fallback). Account 1 keeps the agent distinct from
        the scannable matrix wallets (account 0) and MASTER (account 2).
        """
        idn = engine.derive_identity(account=1, index=0)
        return {
            "address": idn["address"],
            "private_key": idn["private_key"],
            "public_key": idn.get("public_key", ""),
            "derivation": idn.get("derivation", "m/44'/60'/1'/0/0"),
        }

    def _partition_channels(self) -> dict:
        """Split 57,434,001 fold channels across the wallet matrix (0-indexed,
        contiguous ranges). Integrity holds iff the partition covers every channel."""
        n = self.matrix_size
        base, rem = divmod(self.fold, n)
        ranges, start = [], 0
        for i in range(n):
            count = base + (1 if i < rem else 0)
            ranges.append({
                "wallet_index": i,
                "channel_start": start,
                "channel_end": start + count - 1,
                "channel_count": count,
            })
            start += count
        total = sum(r["channel_count"] for r in ranges)
        return {"ranges": ranges, "total": total, "integrity": total == self.fold}

    def _fold_root(self) -> str:
        """Merkle-combined hash over each wallet's anchored channel manifest."""
        leaves = []
        for r in self.partition["ranges"]:
            addr = self.engine.wallets[r["wallet_index"]]["address"]
            leaves.append(sha256_hex(
                f"{fold_timestamp(self.anchor)}|{addr}|"
                f"{r['channel_start']}|{r['channel_count']}"
            ))
        layer = leaves
        while len(layer) > 1:
            layer = [sha256_hex(layer[i] + (layer[i + 1] if i + 1 < len(layer) else layer[i]))
                     for i in range(0, len(layer), 2)]
        return layer[0] if layer else sha256_hex("")

    def fold_clock(self, now: datetime | None = None) -> dict:
        """Current reading of the fold clock, anchored to 26/10/2000T10:26:20.00."""
        now = now or datetime.now(timezone.utc)
        elapsed_s = (now - self.anchor).total_seconds()
        return {
            "anchor_schema": fold_timestamp(self.anchor),
            "anchor_epoch_s": self.anchor.timestamp(),
            "now_schema": fold_timestamp(now),
            "elapsed_s": elapsed_s,
            "fold_frequency_hz": FOLD_FREQUENCY_HZ,
            "fold_period_s": FOLD_PERIOD_S,
            "fold_ticks_since_anchor": elapsed_s / FOLD_PERIOD_S,
        }

    def status(self) -> dict:
        clock = self.fold_clock()
        return {
            "agent_name": "IMAM-V3 FOLD-WALLET AGENT",
            "agent_address": self.agent_wallet["address"],
            "anchor_schema": clock["anchor_schema"],
            "anchor_epoch_s": clock["anchor_epoch_s"],
            "now_schema": clock["now_schema"],
            "fold_metric": self.fold,
            "fold_frequency_hz": FOLD_FREQUENCY_HZ,
            "fold_period_s": FOLD_PERIOD_S,
            "fold_ticks_since_anchor": clock["fold_ticks_since_anchor"],
            "matrix_size": self.matrix_size,
            "channel_integrity": self.partition["integrity"],
            "channels_total": self.partition["total"],
            "fold_root": self._fold_root(),
            "wallets": [
                {"index": r["wallet_index"],
                 "address": self.engine.wallets[r["wallet_index"]]["address"],
                 **r}
                for r in self.partition["ranges"]
            ],
        }

    def wallet_channels(self, index: int) -> dict:
        if not (0 <= index < self.matrix_size):
            raise ValueError(f"wallet index {index} out of range 0..{self.matrix_size - 1}")
        return self.partition["ranges"][index]

    def activate(self) -> dict:
        """Activation record: fold-clock reading + channel-integrity proof."""
        clock = self.fold_clock()
        return {
            "status": "ACTIVATED",
            "agent_address": self.agent_wallet["address"],
            "anchor_schema": clock["anchor_schema"],
            "activation_schema": clock["now_schema"],
            "fold_ticks_since_anchor": clock["fold_ticks_since_anchor"],
            "channel_integrity": self.partition["integrity"],
            "channels_total": self.partition["total"],
            "fold_root": self._fold_root(),
        }
