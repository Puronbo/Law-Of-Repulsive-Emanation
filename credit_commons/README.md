# Credit-Commons Pilot — how to run

This is a *working web pilot* of the design in `docs/CREDIT_COMMONS.md`, built
on the validated simulator (`credit_commons/sim.py`). It is a browser PWA
(installable to a phone home screen) backed by a persistent SQLite ledger that
enforces the same rules — conservation (gate 6), trust ceiling, necessity
ceiling, fee split, action asymmetry — and never runs offline cash (§6).

## Requirements

- Python 3.10+
- `flask` (everything else, including `sqlite3`, is in the standard library)

```powershell
pip install -r credit_commons/requirements-web.txt
```

## Run it

```powershell
# from the repo root
$env:PYTHONPATH="C:\Users\Me\Downloads\Puno_Calculus"
python credit_commons/web/app.py
```

Then open **http://127.0.0.1:5000** in a browser.

- To use a different database file: `$env:CC_DB="C:\path\to\pilot.db"`
- To use a different port: `$env:PORT=8080`

## Using it in the browser

1. **Join** — pick a handle + a memorized PIN (4–8), choose a tier
   (individual / business / producer). This is the one-shot seed (Phase 0).
2. **Sign in** — PIN-verified, live session, rate-limited (§6). Credentials are
   never stored; only a salted hash.
3. **Trade** — enter the seller's handle, an amount, mark *necessity* for
   protected necessities (food, medicine, transport — §5.5 E1). Terminal =
   the merchant providing the terminal (gets part of the fee).
4. **Network** button — live status: members, circulation, reserve, Gini(trust)
   (low = equitable), and the conserved total.
5. **Ledger** — the living audit of every trade and grant.

## Installing on a phone (PWA)

Open the URL in a mobile browser (Chrome/Edge/Safari), then use
*Add to Home Screen* / *Install app*. The shell is cached for instant launch,
but **trades and sign-in are always live calls** (§6 — never offline cash).

## API (what the front end calls)

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/accounts` | create account (handle, pin, tier) |
| POST | `/api/session` | sign in → short-lived revocable session |
| GET  | `/api/me` | your credit/trust/irrev/necessity |
| POST | `/api/trade` | atomic, conserved trade (seller, x, necessity, terminal) |
| POST | `/api/grant` | progressive grant funded from the reserve (Phase 2) |
| GET  | `/api/status` | members, circulation, reserve, Gini(trust), conserved total |
| GET  | `/api/ledger` | audit trail |
| POST | `/api/logout` | end session |

## Tests

```powershell
$env:PYTHONPATH="C:\Users\Me\Downloads\Puno_Calculus"
python -m pytest tests\test_credit_commons.py tests\test_credit_commons_web.py -q
```

- `test_credit_commons.py` — the 14 hard gates / stability / equity in the sim.
- `test_credit_commons_web.py` — end-to-end over Flask's test client
  (conservation holds across the wire, bad PIN rejected, unauth blocked, PWA
  routes serve).

## What this pilot is and is not

- **Is:** a real, persistent, browser/mobile-usable pilot that proves the rules
  and lets a small community trade in-network.
- **Is not (yet):** the §7.5 multi-node replicated/fork-free survival layer, or
  the full governance/dispute machinery. It models *one* honest ledger — which
  is the correct first pilot. The metrics it reports (`Gini(trust)`,
  `poor_ok%`, reserve, grant frequency) are exactly the ones the field pilot
  needs to tune the free parameters (§2.6, §6 of the pilot doc).
