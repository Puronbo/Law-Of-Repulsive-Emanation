"""
===================================================================================
FULL-STACK INTEGRABLE MULTI-CHAIN MATRIX ENGINE
-----------------------------------------------------------------------------------
Asynchronous Web3 engine handling HD wallet derivation, multi-chain scanning,
ERC-20 token tracking, rank leaderboards, and automated rebalancing.
===================================================================================
"""

import asyncio
import json
import logging
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.eth import AsyncEth
import hashlib
import hmac

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

DEMO_MNEMONIC = "vessel march fossil explicit basic radar pulse trim standard logic echo grain"

def _load_networks() -> Dict[str, Dict[str, Any]]:
    """Load chain config from networks.json so RPC endpoints are config-driven."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "networks.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.warning("networks.json not loaded (%s); using embedded fallback.", e)
        return _embedded_networks()

def _embedded_networks() -> Dict[str, Dict[str, Any]]:
    return {
        "Ethereum Sepolia": {
            "rpc": "https://ethereum-sepolia-rpc.publicnode.com",
            "symbol": "ETH",
            "chain_id": 11155111,
            "tokens": {
                "USDT": "0xaA8E23Fb1079EA71e0a56F48a2aA51851D8433D0",
                "USDC": "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238"
            }
        },
        "Ethereum Mainnet": {
            "rpc": "https://ethereum-rpc.publicnode.com",
            "symbol": "ETH",
            "chain_id": 1,
            "tokens": {
                "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
            }
        },
        "BNB Smart Chain": {
            "rpc": "https://bsc-rpc.publicnode.com",
            "symbol": "BNB",
            "chain_id": 56,
            "tokens": {
                "USDT": "0x55d398326f99059fF775485246999027B3197955",
                "USDC": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"
            }
        },
        "Polygon POS": {
            "rpc": "https://polygon-bor-rpc.publicnode.com",
            "symbol": "POL",
            "chain_id": 137,
            "tokens": {
                "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
                "USDC": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359"
            }
        },
        "Arbitrum One": {
            "rpc": "https://arbitrum-one-rpc.publicnode.com",
            "symbol": "ETH",
            "chain_id": 42161,
            "tokens": {
                "USDT": "0xFd086bC7cd5C481DCC9C85ebE478A1C0b69FCbb9",
                "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
            }
        }
    }

NETWORKS = _load_networks()

def _resolve_mnemonic() -> str:
    """Mnemonic comes from the IMAM_MNEMONIC env var; the built-in value is a
    clearly-labeled DEMO phrase and must never be used for real funds."""
    mnemonic = os.environ.get("IMAM_MNEMONIC", "").strip()
    if mnemonic:
        return mnemonic
    logging.warning("IMAM_MNEMONIC env var not set; using DEMO mnemonic (not for real funds).")
    return DEMO_MNEMONIC

ERC20_ABI = [
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"}
]

def _fold_public_key(seed: str, idx: int) -> str:
    """Deterministic fold-identity public key (65-byte uncompressed hex) for
    wallets without a real HD key. Purely for identity/listing; no real key
    material exists for fold-identity wallets."""
    x = hashlib.sha256(f"{seed}|PUBKEY-X|{idx}".encode()).hexdigest()
    y = hashlib.sha256(f"{seed}|PUBKEY-Y|{idx}".encode()).hexdigest()
    return "04" + x + y


# Self-contained BIP39 -> BIP32 -> BIP44 (Ethereum) derivation. Used instead of
# bip_utils, which needs native wheels (coincurve/cbor2/etc.) that are not
# published for this interpreter. Verified against the BIP39 test vector and
# the well-known abandon.../test...junk m/44'/60'/0'/0/0 addresses.
_SECP256K1_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
_BIP44_HARDENED = 0x80000000


def _bip39_seed(mnemonic: str, passphrase: str = "") -> bytes:
    return hashlib.pbkdf2_hmac("sha512", mnemonic.encode("utf-8"),
                               ("mnemonic" + passphrase).encode("utf-8"),
                               2048, 64)


def _bip32_master(seed: bytes) -> tuple:
    i = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    return int.from_bytes(i[:32], "big"), i[32:]


def _bip32_ckd_priv(k: int, c: bytes, index: int) -> tuple:
    if index >= _BIP44_HARDENED:
        data = b"\x00" + k.to_bytes(32, "big") + index.to_bytes(4, "big")
    else:
        import coincurve
        pub = coincurve.PublicKey.from_valid_secret(
            k.to_bytes(32, "big")).format(compressed=True)
        data = pub + index.to_bytes(4, "big")
    i = hmac.new(c, data, hashlib.sha512).digest()
    return ((int.from_bytes(i[:32], "big") + k) % _SECP256K1_N), i[32:]


def _bip44_eth_private_key(mnemonic: str, index: int,
                           account: int = 0) -> int:
    """m/44'/60'/{account}'/0/index private key scalar from a BIP39 mnemonic."""
    k, c = _bip32_master(_bip39_seed(mnemonic))
    for el in (44 + _BIP44_HARDENED, 60 + _BIP44_HARDENED,
               account + _BIP44_HARDENED, 0, index):
        k, c = _bip32_ckd_priv(k, c, el)
    return k


class MultiChainWalletEngine:
    def __init__(self, mnemonic: Optional[str] = None, matrix_size: int = 5,
                 wallet: Optional[str] = None):
        self.mnemonic = mnemonic or _resolve_mnemonic()
        self.matrix_size = matrix_size
        self.anchor_wallet = wallet
        self.wallets = self._derive_hd_wallets()
        self._scanned_sessions = []

    def derive_identity(self, account: int = 0, index: int = 0) -> Dict[str, Any]:
        """Derive one BIP44 Ethereum identity (address + signable private key +
        public key) from this engine's mnemonic. Accounts used by the stack:
        account 0 = scannable wallet matrix, account 1 = fold agent identity,
        account 2 = MASTER (fold-collector). The private key is returned in
        memory only and must never be persisted or broadcast."""
        try:
            import coincurve
            priv = _bip44_eth_private_key(self.mnemonic, index, account=account)
            priv_hex = f"0x{priv:064x}"
            account_obj = AsyncWeb3().eth.account.from_key(priv_hex)
            pub = coincurve.PublicKey.from_valid_secret(
                priv.to_bytes(32, "big")).format(compressed=False)
            return {"address": account_obj.address, "private_key": priv_hex,
                    "public_key": "0x" + pub.hex(),
                    "derivation": f"m/44'/60'/{account}'/0/{index}"}
        except Exception:
            digest = hashlib.sha256(
                f"{self.mnemonic}|ACCOUNT{account}|{index}".encode()).hexdigest()
            return {"address": "0x" + digest[:40], "private_key": "",
                    "public_key": _fold_public_key(f"{self.mnemonic}|ACCOUNT{account}",
                                                   index),
                    "derivation": f"FOLD-DERIVED-FALLBACK (account {account}, index {index})"}

    def _derive_hd_wallets(self) -> List[Dict[str, Any]]:
        """BIP44 HD derivation when bip-utils is available; otherwise a
        deterministic mnemonic+index fold-identity fallback so the engine
        stays importable on interpreters without a coincurve wheel.

        When an external anchor wallet is supplied, the matrix wallets are
        derived deterministically FROM that wallet (connected-wallet mode):
        address = 0x + sha256(anchor|idx)."""
        if self.anchor_wallet:
            wallets = []
            for idx in range(self.matrix_size):
                digest = hashlib.sha256(
                    f"{self.anchor_wallet}|{idx}".encode()).hexdigest()
                wallets.append({
                    "index": idx,
                    "address": "0x" + digest[:40],
                    "private_key": "",
                    "derivation": f"CONNECTED-via-external-wallet {self.anchor_wallet}",
                    "public_key": _fold_public_key(self.anchor_wallet, idx),
                })
            return wallets
        try:
            import coincurve
            w3_sync = AsyncWeb3()
            wallets = []
            for idx in range(self.matrix_size):
                priv = _bip44_eth_private_key(self.mnemonic, idx)
                priv_hex = f"0x{priv:064x}"
                account = w3_sync.eth.account.from_key(priv_hex)
                pub = coincurve.PublicKey.from_valid_secret(
                    priv.to_bytes(32, "big")).format(compressed=False)
                wallets.append({
                    "index": idx,
                    "address": account.address,
                    "private_key": priv_hex,
                    "public_key": "0x" + pub.hex(),
                })
            return wallets
        except Exception:
            wallets = []
            for idx in range(self.matrix_size):
                digest = hashlib.sha256(
                    f"{self.mnemonic}|{idx}".encode()
                ).hexdigest()
                wallets.append({
                    "index": idx,
                    "address": "0x" + digest[:40],
                    "private_key": "",
                    "derivation": "FOLD-IDENTITY-FALLBACK (bip-utils unavailable)",
                    "public_key": _fold_public_key(self.mnemonic, idx),
                })
            return wallets

    async def _scan_single(self, wallet: Dict[str, Any], net_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        result = {
            "network": net_name,
            "chain_id": config["chain_id"],
            "wallet_index": wallet["index"],
            "address": wallet["address"],
            "native_balance": 0.0,
            "native_symbol": config["symbol"],
            "nonce": 0,
            "tokens": {},
            "status": "VALIDATED"
        }

        try:
            w3 = AsyncWeb3(AsyncHTTPProvider(config["rpc"], request_kwargs={'timeout': 5}), modules={'eth': (AsyncEth,)})
            self._scanned_sessions.append(w3)
            if not await w3.is_connected():
                result["status"] = "RPC_OFFLINE"
                return result

            bal_wei = await w3.eth.get_balance(wallet["address"])
            result["native_balance"] = float(w3.from_wei(bal_wei, 'ether'))
            result["nonce"] = await w3.eth.get_transaction_count(wallet["address"])

            for symbol, contract_addr in config.get("tokens", {}).items():
                try:
                    contract = w3.eth.contract(address=w3.to_checksum_address(contract_addr), abi=ERC20_ABI)
                    raw_bal = await contract.functions.balanceOf(wallet["address"]).call()
                    decimals = await contract.functions.decimals().call()
                    result["tokens"][symbol] = raw_bal / (10 ** decimals)
                except Exception:
                    result["tokens"][symbol] = 0.0

        except Exception as e:
            result["status"] = f"ERROR: {type(e).__name__}"

        return result

    async def _close_scanned_sessions(self) -> None:
        """web3 v7 AsyncHTTPProvider caches aiohttp sessions internally; close
        them so repeated scans don't leak file descriptors/sockets."""
        for w3 in self._scanned_sessions:
            try:
                rsm = w3.provider._request_session_manager
                cache = rsm.session_cache
                for s in list(cache._data.values()):
                    if hasattr(s, "close"):
                        try:
                            await s.close()
                        except Exception:
                            pass
                cache._data.clear()
            except Exception:
                pass
        self._scanned_sessions = []

    async def scan_address(self, address: str, index: int) -> Dict[str, Any]:
        """Scan a single address (e.g. the MASTER account) across every
        network and aggregate it into the same shape as a run_full_scan
        leaderboard item, so it can be tracked as a hot wallet."""
        tasks = []
        wallet = {"index": index, "address": address}
        for net_name, config in NETWORKS.items():
            tasks.append(self._scan_single(wallet, net_name, config))
        try:
            raw_results = await asyncio.gather(*tasks)
        finally:
            await self._close_scanned_sessions()

        total_native = sum(r["native_balance"] for r in raw_results)
        total_tx = sum(r["nonce"] for r in raw_results)
        tokens = {}
        for r in raw_results:
            for sym, bal in r["tokens"].items():
                tokens[sym] = tokens.get(sym, 0.0) + bal
        return {
            "index": index,
            "address": address,
            "total_native_balance": total_native,
            "total_nonces": total_tx,
            "tokens": tokens,
            "networks": raw_results,
        }

    async def run_full_scan(self) -> Dict[str, Any]:
        tasks = []
        for wallet in self.wallets:
            for net_name, config in NETWORKS.items():
                tasks.append(self._scan_single(wallet, net_name, config))

        try:
            raw_results = await asyncio.gather(*tasks)
        finally:
            await self._close_scanned_sessions()

        aggregated = []
        for wallet in self.wallets:
            w_res = [r for r in raw_results if r["wallet_index"] == wallet["index"]]
            total_native = sum(r["native_balance"] for r in w_res)
            total_tx = sum(r["nonce"] for r in w_res)

            tokens = {}
            for r in w_res:
                for sym, bal in r["tokens"].items():
                    tokens[sym] = tokens.get(sym, 0.0) + bal

            aggregated.append({
                "index": wallet["index"],
                "address": wallet["address"],
                "total_native_balance": total_native,
                "total_nonces": total_tx,
                "tokens": tokens,
                "networks": w_res
            })

        # Order-Statistic Tree simulation: Rank descending by native balance
        ranked = sorted(aggregated, key=lambda x: x["total_native_balance"], reverse=True)
        for idx, item in enumerate(ranked, start=1):
            item["rank"] = idx

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "matrix_size": self.matrix_size,
            "leaderboard": ranked
        }