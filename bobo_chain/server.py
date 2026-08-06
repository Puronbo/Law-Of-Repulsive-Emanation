"""
===================================================================================
FASTAPI REST GATEWAY FOR MULTI-CHAIN WALLET MATRIX
-----------------------------------------------------------------------------------
Provides OpenAPI endpoints for state querying, rank ordering, and rebalancing tests.
Run with: uvicorn server:app --reload --port 8000
===================================================================================
"""

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import os
import json

from engine import MultiChainWalletEngine
from imam_agent import ImamFoldAgent
from agent_toy import ColdWalletToy
from internet_registry import InternetRegistry
from internet_registry import SEAL_ALG
from cold_crawler import ColdWalletCrawler
from fold_crypto import SigningAuthority
import hashlib

app = FastAPI(title="Multi-Chain Wallet Matrix API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = MultiChainWalletEngine()
agent = ImamFoldAgent(engine)
signing = SigningAuthority(agent)
toy = ColdWalletToy(agent, signing=signing)
crawler = ColdWalletCrawler(agent, toy)
toy.set_master(crawler.master["address"])
registry = InternetRegistry(toy, signing)
LATEST_CACHE = {}


# ---------------- Optional bearer-token auth (API_TOKEN env) --------------- #
from fastapi import Request
from fastapi.responses import JSONResponse

_API_TOKEN = os.environ.get("API_TOKEN", "").strip()


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """When API_TOKEN is set, every /api/* route requires
    'Authorization: Bearer <token>'. The dashboard HTML stays open on the
    local bind."""
    if _API_TOKEN and request.url.path.startswith("/api/"):
        auth = request.headers.get("authorization", "")
        if auth != f"Bearer {_API_TOKEN}":
            return JSONResponse(status_code=401,
                                content={"detail": "UNAUTHORIZED"})
    return await call_next(request)

class ConfigurePayload(BaseModel):
    mnemonic: str | None = None
    matrix_size: int = 5
    wallet: str | None = None

class WalletIndexPayload(BaseModel):
    index: int

class ToyStepPayload(BaseModel):
    type: str | None = None
    steps: int = 1

class CrawlerRunPayload(BaseModel):
    run_cycles: int = 1

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Multi-Chain Engine Active</h1><p>Dashboard file index.html not found.</p>"

@app.post("/api/configure")
async def configure_engine(payload: ConfigurePayload):
    global engine, agent, toy, registry, crawler, signing
    try:
        if payload.wallet:
            engine = MultiChainWalletEngine(matrix_size=payload.matrix_size,
                                            wallet=payload.wallet)
        else:
            engine = MultiChainWalletEngine(mnemonic=payload.mnemonic,
                                            matrix_size=payload.matrix_size)
        agent = ImamFoldAgent(engine)
        signing = SigningAuthority(agent)
        toy = ColdWalletToy(agent, signing=signing)
        crawler = ColdWalletCrawler(agent, toy)
        toy.set_master(crawler.master["address"])
        registry = InternetRegistry(toy, signing)
        mode = f"connected to external wallet {payload.wallet}" if payload.wallet \
            else f"mnemonic {engine.mnemonic[:10]}..."
        return {"status": "SUCCESS", "mode": mode,
                "message": f"Engine initialized with {payload.matrix_size} wallets ({mode})."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/scan")
async def execute_scan():
    global LATEST_CACHE
    LATEST_CACHE = await engine.run_full_scan()
    return LATEST_CACHE

@app.get("/api/report")
async def get_report():
    if not LATEST_CACHE:
        return await execute_scan()
    return LATEST_CACHE

# ---------------- IMAM-V3 fold-wallet agent endpoints ---------------- #
@app.get("/api/agent")
async def agent_status():
    return agent.status()

@app.post("/api/agent/activate")
async def agent_activate():
    return agent.activate()

@app.get("/api/agent/foldclock")
async def agent_foldclock():
    return agent.fold_clock()

@app.get("/api/agent/wallets/{index}")
async def agent_wallet_channels(index: int):
    try:
        return agent.wallet_channels(index)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ---------------- Cold-wallet activity + neighbor-jump agent toy -------- #
@app.get("/api/toy")
async def toy_status():
    return toy.summary()

@app.get("/api/toy/coldwallets")
async def toy_cold_wallets():
    return {"cold_wallets": toy.cold_wallets(), "power": toy.power_table()}

@app.post("/api/toy/powerdown")
async def toy_powerdown(steps: int = 1):
    """Scan crawler inactivity, turn the inactive matrix wallets OFF in the
    toy, then let the toy play on the remaining unused wallet (MASTER when
    every matrix wallet is off)."""
    inactive = crawler.inactive_indices()
    power = toy.set_power(off=inactive)
    play = toy.run(steps=max(1, min(steps, 10_000)))
    return {
        "scan_source": "crawler actual scan",
        "inactive_wallets": inactive,
        "power": power,
        "play": play,
    }

@app.post("/api/toy/trashplay")
async def toy_trashplay(steps: int = 1):
    """Let the toy play on the dead-wallet collection: the crawler's trash
    ledger. Each step emits one TRASH activity record over the dead wallets
    (public key + cleaned schema + reason). Persisted to the toy ledger."""
    dead = crawler.state["trash"]
    return {
        "dead_wallet_collection": len(dead),
        "trash_ledger": dead,
        "play": toy.play_trash(dead, steps=steps),
    }

@app.post("/api/toy/step")
async def toy_step(payload: ToyStepPayload):
    steps = max(1, min(payload.steps, 10_000))
    result = toy.run(steps=steps, activity_type=payload.type)
    return {"step": result["records"][-1], "summary": result["summary"]}

@app.post("/api/toy/reset")
async def toy_reset():
    summary = toy.reset()
    # the registry's chain is anchored to toy record seqs; a toy reset must
    # clear it too or new records (seq restarting at 0) would never ingest.
    registry.state = {"blocks": [], "last_ingested_seq": -1}
    registry._save_state()
    return {"reset": True, "summary": summary}

@app.get("/api/toy/activity")
async def toy_activity(limit: int = 20):
    return {"activity": toy.activity(limit=max(1, min(limit, 1000)))}

@app.post("/api/toy/migrate")
async def toy_migrate():
    """Upgrade legacy fold-digest records to real ECDSA signatures."""
    return toy.migrate_signatures()

@app.get("/api/toy/verify")
async def toy_verify():
    """Cryptographic verification of every activity record in the ledger."""
    return {"verify": toy.verify_activity()}

# ---------------- Decentralized internet registry + consensus ---------- #
@app.get("/api/internet/registry")
async def internet_registry_view():
    return registry.registry()

@app.post("/api/internet/ingest")
async def internet_ingest():
    return registry.ingest()

@app.get("/api/internet/consensus")
async def internet_consensus(tamper_seq: int | None = None):
    return registry.consensus(tamper_seq=tamper_seq)

@app.get("/api/internet/verify")
async def internet_verify(tamper_seq: int | None = None):
    """Full actual-security battery: chain integrity, record + block ECDSA
    authentication, at-rest integrity, and per-identity consensus votes."""
    return registry.verify(tamper_seq=tamper_seq)

@app.get("/api/internet/nodes")
async def internet_nodes():
    """The consensus verifiers = the available identities (Node 0D, matrix
    wallets, AGENT, MASTER), each verifying with public keys only."""
    return {"nodes": registry.node_identities(),
            "roles": signing.roles()}

@app.get("/api/internet/proof")
async def internet_proof(seq: int):
    """Merkle inclusion proof for a record sequence number."""
    if seq < 0:
        raise HTTPException(status_code=400, detail="seq must be >= 0")
    return registry.proof(seq)

@app.post("/api/internet/reseal")
async def internet_reseal():
    """Operator action: re-seal the persisted registry after a legitimate edit
    or an at-rest tamper alert."""
    return registry.reseal()

@app.get("/api/internet/identities")
async def internet_identities():
    """Public identity map (address -> public key) for external verifiers."""
    return {"identities": signing.identity_map(),
            "roles": signing.roles()}

@app.get("/api/security")
async def security_overview():
    """Actual-security posture of the stack."""
    t = toy.summary()
    r = registry.registry()
    return {
        "auth_mode": t["auth_mode"],
        "signing_curve": "secp256k1 (ECDSA, RFC6979 deterministic)",
        "key_custody": {
            "private_keys": "memory-only, derived from IMAM_MNEMONIC on demand",
            "persisted": "no private key or mnemonic is ever written to disk",
            "node_verifiers": "public keys only (independent recomputation)",
        },
        "internet_registry": {
            "auth": r["auth"],
            "integrity_at_rest": r["integrity_at_rest"],
            "seal_algorithm": SEAL_ALG,
            "block_count": r["block_count"],
            "signed_records": t["signed_records"],
            "records_total": t["activity_count"],
        },
        "transport": {
            "bearer_token": "ENABLED" if _API_TOKEN else "disabled (set API_TOKEN)",
            "tls": "ENABLED" if (os.environ.get("TLS_CERT") and os.environ.get("TLS_KEY"))
                else "disabled (set TLS_CERT + TLS_KEY)",
        },
    }

# ---------------- Cold-wallet crawler (actual mode) ------------------- #
@app.get("/api/crawler")
async def crawler_status():
    return crawler.summary()

@app.get("/api/crawler/table")
async def crawler_table():
    return {"cold": crawler.cold_table(), "hot": crawler.hot_table()}

@app.post("/api/crawler/run")
async def crawler_run(payload: CrawlerRunPayload):
    cycles = max(1, min(payload.run_cycles, 10_000))
    result = None
    for _ in range(cycles):
        result = crawler.run()
    return result

@app.post("/api/crawler/reset")
async def crawler_reset():
    return {"reset": True, "summary": crawler.reset()}

@app.get("/api/crawler/ledger")
async def crawler_ledger(limit: int = 20):
    return {"records": crawler.ledger(limit=max(1, min(limit, 1000)))}

@app.post("/api/crawler/clean")
async def crawler_clean():
    """Clean TRASH wallets (zero/dust reserves): zero them, flag as cleaned,
    log address + public key in the trash ledger. Returns cleaned + listing."""
    return crawler.clean_trash()

@app.post("/api/crawler/actual")
async def crawler_actual():
    """Apply the real on-chain scan to the crawler: reserves become actual
    balances, dormancy uses real tx counts. The hot tier covers every wallet
    (matrix + MASTER). Mechanics stay toy (no broadcast)."""
    scan = await engine.run_full_scan()
    try:
        master_scan = await engine.scan_address(crawler.master["address"],
                                                crawler.matrix_size)
        scan["leaderboard"].append(master_scan)
    except Exception:
        pass
    applied = crawler.apply_actual_scan(scan)
    result = crawler.run()
    return {
        "scan": {"timestamp": scan["timestamp"], "matrix_size": scan["matrix_size"]},
        "applied": applied,
        "run": result["run"],
        "sweeps": result["sweeps"],
        "summary": crawler.summary(),
        "table": crawler.cold_table(),
        "hot": crawler.hot_table(),
    }

# ---------------- External wallet bridge + connected-wallet test --------- #
@app.get("/api/connected")
async def connected_wallets(wallet: str | None = None, count: int = 5,
                            network: str | None = None):
    from wallet_connect import connected_report, DEFAULT_WALLET
    w = wallet or getattr(engine, "anchor_wallet", None) or DEFAULT_WALLET
    try:
        return connected_report(w, max(1, min(count, 50)), network=network)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/genesis")
async def genesis_wallets(count: int = 5):
    """Every registered blockchain's genesis wallet decoded and tested:
    BTC, BCH, LTC, DOGE (version-byte + connected-wallet battery)."""
    from wallet_connect import genesis_report
    return genesis_report(max(1, min(count, 50)))

# ---------------- Node 0D master dashboard (date protocol) ------------- #
@app.get("/api/master")
async def master_dashboard():
    """Master view: every layer restructured as a consumer of the universal
    date protocol (26/10/2000T10:26:20.00) aggregated by Node 0D."""
    from wallet_connect import genesis_report
    clock = agent.fold_clock()
    a = agent.status()
    t = toy.summary()
    reg = registry.registry()
    cons = registry.consensus()
    cr = crawler.summary()
    return {
        "node": "0D",
        "node_role": "MASTER DASHBOARD NODE (date-protocol aggregator)",
        "protocol": {
            "name": "UNIVERSAL DATE PROTOCOL",
            "anchor_schema": clock["anchor_schema"],
            "now_schema": clock["now_schema"],
            "anchor_epoch_s": clock["anchor_epoch_s"],
            "fold_metric": agent.fold,
            "fold_frequency_hz": clock["fold_frequency_hz"],
            "fold_period_s": clock["fold_period_s"],
            "fold_ticks_since_anchor": clock["fold_ticks_since_anchor"],
        },
        "layers": {
            "wallet_matrix": {
                "matrix_size": engine.matrix_size,
                "addresses": [w["address"] for w in engine.wallets],
            },
            "fold_agent": {k: a[k] for k in
                           ("agent_address", "channel_integrity",
                            "channels_total", "fold_root")},
            "cold_toy": {k: t[k] for k in
                         ("token_wallet", "token_channel", "jumps",
                          "activity_count", "cold_wallet_crossings",
                          "channel_integrity")},
            "internet": {
                "block_count": reg["block_count"],
                "record_count": reg["record_count"],
                "last_block_hash": reg["last_block_hash"],
                "nodes": reg["nodes"],
                "auth": reg["auth"],
                "integrity_at_rest": reg["integrity_at_rest"],
                "consensus": cons,
            },
            "crawler": {k: cr[k] for k in
                        ("mode", "reserve_source", "master_balance",
                         "swept_total", "crawl_count", "reserve_total",
                         "inactive_wallets")},
            "connected": {
                "anchor_wallet": getattr(engine, "anchor_wallet", None),
                "matrix": [w["address"] for w in engine.wallets],
                "derivation": engine.wallets[0].get("derivation", "HD") if engine.wallets else None,
                "genesis": genesis_report(3),
            },
        },
        "status": "OK",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)