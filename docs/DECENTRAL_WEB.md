# Decentral Web — the WWW's three functions, rebuilt on verified machinery

A working mini-"web" over real TCP processes: pages publish once and replicate
to a single content-addressed archive shared by every node; a node can die and
its pages are still served by survivors; a stateless restart resyncs
bit-identical; and a near-miss name ("homee") resolves to the intended page
("home") the same way google.com resolved to gooogle.com on the real top-1M
net.  The design doc maps each function of the World Wide Web to machinery this
repo has already verified, so the prototype is assembly, not invention.

## The mapping (WWW function -> repo machinery)

| WWW function | Prototype mechanism | Verified machinery re-used |
|---|---|---|
| DNS / search | nearest-centroid routing on char-ngram name embeddings | T55i pattern: `google.com -> gooogle.com` on 1.9M real domains |
| Content addressing / cache key | every page addressed by SHA-256 of its content; identical content dedups to one address; GET by address is an O(1) store lookup | `LedgerChain` (puno_flow/ledger.py): hash-chained, content-addressed |
| Replication / CDN | every publish is an event appended to a shared, verifying archive; each node serves from its own replica | T70 `SocketTransport` (experiments/decentral_bank_net.py) |
| Survives node death | kill a node -> survivors serve its pages; stateless restart -> resync to the same chain | T15/T17 crash-restart machinery |

The node overlay itself is DecentralNet-style: each node holds a 2D home on a
circle and name routing picks the node (or page) whose embedding is nearest.

## Where things live

| Piece | Location |
|---|---|
| Prototype + verdict | `experiments/decentral_web.py` |
| Verdict artifact | `data/decentral_web_data.json` (gitignored, `git add -f`) |
| Design doc (this file) | `docs/DECENTRAL_WEB.md` |
| Plug-and-play UI (the web client for it) | `puno_app/plugin_ui.py` + `plugin_ui.html` |

```python
import sys; sys.path.insert(0, 'experiments')
from decentral_web import WebDriver
d = WebDriver(4)                    # 4 real processes, real TCP, optional TLS
d.publish("home", "<h1>hi</h1>")    # publish once...
print(d.get(3, "home"))             # ...served from EVERY node
print(d.resolve(0, "homee"))        # -> home (nearest-embedding DNS)
d.kill(3); d.restart(3); d.resync(3)
```

## Claims (each a verdict run over real sockets, 3 seeds + TLS)

- **W1 content replicates** — one chain head, one length, every archive
  verifies, all name sets agree; a page published on one node is served (with
  verified content-address integrity) from every other node.
- **W2 content addressing** — 3 publishes of 2 distinct contents collapse to 2
  addresses (dedup), and a GET by address is served directly (the WWW's cache
  key made local).
- **W3 the net survives node death** — a crashed node's pages stay served by
  survivors; a stateless restart resyncs to a bit-identical, verifying archive.
- **W4 name resolution** — a near-miss query resolves to the page whose
  name-embedding is nearest, the routing pattern that held on 1.9M real domains.

All four SUPPORTED on 2026-08-11 (seeds 42/11/7, plain + mutual-TLS sockets).

## Honest walls (crease-worthy)

- **Sequencer is centralized.**  Events are sequenced by the driver node.  A
  real distributed web needs a distributed total order — the same honest wall
  as T14c and bazaar_net's relay.  Content addressing removes the *mutation*
  attack (a flipped byte is caught) but not the *ordering* problem.
- **Toy embedding.**  The name hasher is a small char-ngram hash over a few
  pages, not the 1.9M-site geometry.  It proves the routing *pattern* over the
  wire; scaling it is the T55g/T55i problem, already solved in the parent net.
- **One machine.**  Real processes + real TCP, but one host.  The transport is
  IP-parametric (`HOST`), so the same code runs across machines — the 
  LAN-interface proof already exists (T20).
- **No incentives.**  No proof-of-work, no payments, no per-node cryptographic
  identity beyond TLS of the channel.  Replication is an honest-design choice
  here, not an economic one.

## Interactive demo

    python experiments/decentral_web.py

A REPL: `publish NAME TEXT`, `get NAME`, `resolve QUERY`, `state`, `quit`.
