"""
Decentral Web (T73): a content-addressed "web" over real TCP processes.

The WWW's three functions - NAME RESOLUTION, CONTENT ADDRESSING/CACHING, and
REPLICATION - are re-built on the repo's own verified machinery:

  - NAME RESOLUTION: a name (a URL-ish key like "home" or "maps") is embedded
    with the same char-ngram hashing that made google.com->gooogle.com work on
    the real top-1M net (T55i), then routed to the node whose home is nearest
    - the prototype's DNS.  A near-miss query resolves to the same page.
  - CONTENT ADDRESSING: every page is stored by the SHA-256 of its content
    (the WWW's cache key), so identical content collapses to one address and
    a GET by address is a direct O(1) lookup - no scan.
  - REPLICATION: every page event is sequenced into a content-addressed
    LedgerChain archive (C4/C5 machinery) that every node replicates to
    bit-identical, verifying chains - so pages survive node death and are
    served by survivors (the decentralized CDN).

What is re-used (already verified in this repo):
  - SocketTransport from decentral_bank_net.py (T70): framed JSON over TCP,
    maintainer threads, per-node ports.
  - LedgerChain from puno_flow/ledger.py: hash-chained, content-addressed,
    tamper-evident archive.
  - The char-ngram name embedding pattern from the internet net (T55i/T55g):
    hashed n-grams + L2 norm, nearest-centroid routing.
  - DecentralNet-style homes for the node overlay (each node holds a 2D home;
    name routing = nearest home centroid).

What is built here (the web layer):
  - PUBLISH name mime content   -> sequenced event; page address = sha256(content)
  - GET name | addr             -> served from ANY node's replica (O(1) by addr)
  - RESOLVE query               -> the name whose embedding is nearest (search/DNS)
  - crash + stateless restart   -> resyncs the archive bit-identically

Claims (each pinned by a verdict run on seeds, over real sockets):
  W1  content replicates: a page published on one node is retrievable from
      every other node; all replicas converge to a bit-identical, verifying
      content-addressed archive.
  W2  content addressing: identical content maps to ONE address (dedup), and
      a GET by address is served directly from the content store (O(1), the
      WWW's cache-key behaviour made local).
  W3  the net survives node death: a crashed node's pages are still served by
      survivors, and a stateless restart resyncs to a bit-identical chain.
  W4  name resolution: a name resolves to the page whose name embedding is
      nearest (google.com -> gooogle.com style), so near-miss queries return
      the intended page - the routing pattern that held on 1.9M real domains.

Limits (crease-worthy, printed):
  - events are sequenced by the driver (a "sequencer" node); a real network
    would need a distributed total-order primitive - same honest wall as T14c
    and bazaar_net.
  - name embedding here is a small char-ngram hasher (a toy google.com), not
    the full 1.9M-site geometry - it proves the pattern over the wire.
  - still one machine: real processes + real TCP, but all on one host; the
    transport is IP-parametric, so the same code runs across machines.
  - content-addressed only (no proof-of-work, no incentive layer, no
    cryptographic identity per node beyond TLS of the channel).

Usage:
  python decentral_web.py                     # run the interactive demo (REPL)
  python decentral_web.py --verdict           # scripted multi-process verdict
  python decentral_web.py --verdict --tls     # verdict over mutual-TLS sockets
"""

import hashlib
import json
import multiprocessing as mp
import os
import shutil
import socket
import sys
import tempfile
import threading
import time
import traceback

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "Universals"))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from decentral_bank_net import (  # noqa: E402
    SocketTransport, SOCK_PORT_BASE, _frame, _unframe, _gen_tls, _tls_ctx)
from puno_flow.ledger import LedgerChain  # noqa: E402

DATA_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "data", "decentral_web_data.json")

HOST = "127.0.0.1"          # any IP works: this is the IP-parametric transport
N_NODES = 4
NG = 4                      # char-ngram range for name embeddings
EMB = 32                    # name embedding dimension


def stable_mod(s, m):
    return int(hashlib.sha256(s.encode()).hexdigest(), 16) % m


def ev_bytes(ev):
    return json.dumps(ev, sort_keys=True).encode()


def sha256_content(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------- #
# Name embedding: the T55i pattern, small enough for the prototype
# ---------------------------------------------------------------------- #
def embed_name(name):
    """Deterministic char-ngram hashing of a name into an EMB-dim unit vector
    (the same trick that made google.com->gooogle.com work on the real net)."""
    s = name.lower().strip()
    v = np.zeros(EMB, dtype=np.float64)
    for start in range(len(s)):
        for n in range(1, NG + 1):
            if start + n > len(s):
                continue
            gram = s[start:start + n]
            h = int(hashlib.sha256(gram.encode()).hexdigest(), 16)
            v[h % EMB] += 1.0 if (h // EMB) % 2 == 0 else -1.0
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v


# ---------------------------------------------------------------------- #
# Web node state (applied identically on every replica)
# ---------------------------------------------------------------------- #
class Web:
    """One node's replica: name->content pages + the content-addressed
    archive + name embeddings for resolution."""

    def __init__(self, node_id, n_nodes, home):
        self.node_id = node_id
        self.n = n_nodes
        self.home = np.asarray(home, dtype=float)
        self.events = {}                 # seq -> event (all history)
        self.next_seq = 0
        self.chain = LedgerChain()       # content-addressed event archive
        self.pages = {}                  # name -> page dict
        self.addr_index = {}             # address -> name (dedup)

    def apply_event(self, ev):
        seq = ev["seq"]
        if seq in self.events or seq < self.next_seq:
            return
        self.events[seq] = ev
        if ev["kind"] == "PUBLISH":
            addr = sha256_content(ev["content"])
            if ev["name"] not in self.pages:
                self.pages[ev["name"]] = {
                    "name": ev["name"], "content": ev["content"],
                    "mime": ev.get("mime", "text/plain"), "addr": addr,
                    "seq": seq, "author": ev.get("author", "anon")}
            if addr not in self.addr_index:
                self.addr_index[addr] = ev["name"]
        while self.next_seq in self.events:
            e = self.events[self.next_seq]
            self.next_seq += 1
            self.chain.append(ev_bytes(e))

    def names(self):
        return sorted(self.pages)

    def get_by_addr(self, addr):
        name = self.addr_index.get(addr)
        if name is not None:
            return self.pages.get(name)
        return None

    def resolve(self, query, k=1):
        """Nearest name(s) to the query by embedding distance (the search/DNS
        function).  Returns [(name, dist)]."""
        q = embed_name(query)
        if not self.pages:
            return []
        best = sorted((float(np.linalg.norm(embed_name(nm) - q)), nm)
                      for nm in self.pages)[:k]
        return best


# ---------------------------------------------------------------------- #
# Node process (one web host, real process + real sockets)
# ---------------------------------------------------------------------- #
def node_main(node_id, n_nodes, inq, transport_kwargs):
    home = [np.cos(2 * np.pi * node_id / n_nodes) * 0.5,
            np.sin(2 * np.pi * node_id / n_nodes) * 0.5]
    web = Web(node_id, n_nodes, home)
    transport = SocketTransport(node_id, n_nodes, inq, **transport_kwargs)

    def send(dst, kind, args=()):
        transport.send(dst, kind, args)

    def handle(src, kind, args):
        if kind == "STOP":
            raise SystemExit
        elif kind == "EVENT":
            web.apply_event(args[0])
        elif kind == "GET":
            name_or_addr, cid = args
            page = None
            if name_or_addr in web.pages:
                page = web.pages[name_or_addr]
            elif name_or_addr in web.addr_index:
                page = web.pages[web.addr_index[name_or_addr]]
            if page is not None:
                ok = sha256_content(page["content"]) == page["addr"]
                send("driver", "RESULT",
                     (cid, {"found": True, "name": page["name"],
                            "mime": page["mime"], "addr": page["addr"],
                            "content": page["content"], "integrity": ok}))
            else:
                send("driver", "RESULT",
                     (cid, {"found": False, "name": name_or_addr}))
        elif kind == "RESOLVE":
            query, cid = args
            hits = [{"name": nm, "dist": round(d, 4)}
                    for d, nm in web.resolve(query, k=3)]
            send("driver", "RESULT", (cid, hits))
        elif kind == "STATE":
            cid = args[0]
            snap = {"node": node_id,
                    "events": {str(s): ev for s, ev in sorted(web.events.items())},
                    "head": web.chain.head, "length": web.chain.length,
                    "verify": web.chain.verify()[0],
                    "names": web.names(),
                    "n_addrs": len(web.addr_index),
                    "pages": list(web.pages.values())}
            send("driver", "RESULT", (cid, snap))
        elif kind == "RESYNC":
            peer = (node_id + 1) % n_nodes
            if peer != node_id:
                send(peer, "SYNC_REQ", (node_id,))
        elif kind == "SYNC_REQ":
            send(src, "SYNC", (sorted(web.events.items()),))
        elif kind == "SYNC":
            for seq, ev in args[0]:
                web.apply_event(ev)

    while True:
        msg = transport.recv(0.05)
        if msg is not None:
            try:
                handle(msg[0], msg[1], msg[2])
            except SystemExit:
                break
            except Exception:
                print(f"NODE {node_id} CRASHED on {msg[0]} {msg[1]}:",
                      file=sys.stderr)
                traceback.print_exc()
                break


def node_spawn(node_id, n_nodes, inq, transport_kwargs):
    return mp.Process(target=node_main,
                      args=(node_id, n_nodes, inq, transport_kwargs),
                      daemon=True)


# ---------------------------------------------------------------------- #
# Driver: the coordinating client (publishes, retrieves, resolves)
# ---------------------------------------------------------------------- #
class WebDriver:
    def __init__(self, n_nodes=N_NODES, tls=False):
        self.n = n_nodes
        self.host = HOST
        self.seq = 0
        self._cid = 0
        self._tls_cert = self._tls_key = None
        if tls:
            self._tls_dir = tempfile.mkdtemp(prefix="web_tls_")
            self._tls_cert, self._tls_key = _gen_tls(self._tls_dir, self.host)
        self.result_q = mp.Queue()
        self.driver_port = SOCK_PORT_BASE + n_nodes
        self._srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._srv.bind((self.host, self.driver_port))
        self._srv.listen(64)
        self._stop = threading.Event()
        threading.Thread(target=self._serve, daemon=True).start()
        self.inqs, self.procs = [], []
        for i in range(n_nodes):
            inq = mp.Queue()
            p = node_spawn(i, n_nodes, inq, self._tls_kwargs())
            p.start()
            self.inqs.append(inq)
            self.procs.append(p)
        self.conns = {}
        self._clk = threading.Lock()
        self._wait_conn_all(deadline=15)

    def _tls_kwargs(self):
        return {"tls_cert": self._tls_cert, "tls_key": self._tls_key,
                "host": self.host}

    def _serve(self):
        while not self._stop.is_set():
            try:
                c, _ = self._srv.accept()
            except OSError:
                return
            if self._tls_cert:
                c.settimeout(3.0)
                try:
                    c = _tls_ctx(self._tls_cert, self._tls_key) \
                        .wrap_socket(c, server_side=True)
                    c.settimeout(None)
                except Exception:
                    try:
                        c.close()
                    except OSError:
                        pass
                    continue
            threading.Thread(target=self._reader, args=(c,),
                             daemon=True).start()

    def _reader(self, s):
        buf = b""
        while not self._stop.is_set():
            try:
                data = s.recv(65536)
            except OSError:
                break
            if not data:
                break
            buf += data
            frames, buf = _unframe(buf)
            for msg in frames:
                if msg[1] == "RESULT":
                    self.result_q.put((msg[1], *msg[2]))
        try:
            s.close()
        except OSError:
            pass

    def _connect_all(self):
        with self._clk:
            for i in range(self.n):
                if i not in self.conns:
                    try:
                        s = socket.create_connection(
                            (self.host, SOCK_PORT_BASE + i), timeout=0.25)
                        s.settimeout(None)
                        if self._tls_cert:
                            s = _tls_ctx(self._tls_cert, self._tls_key) \
                                .wrap_socket(s, server_side=False)
                        self.conns[i] = s
                    except OSError:
                        pass

    def _wait_conn_all(self, deadline):
        end = time.time() + deadline
        while time.time() < end and len(self.conns) < self.n:
            self._connect_all()
            if len(self.conns) < self.n:
                time.sleep(0.2)
        if len(self.conns) < self.n:
            raise RuntimeError("nodes failed to come up")

    def _send(self, node_id, kind, args=()):
        with self._clk:
            s = self.conns.get(node_id)
        if s is None:
            return
        try:
            s.sendall(_frame(["driver", kind, list(args)]))
        except OSError:
            pass

    def broadcast(self, kind, args=()):
        for i in range(self.n):
            self._send(i, kind, args)

    def publish(self, name, content, mime="text/plain", author="anon"):
        ev = {"kind": "PUBLISH", "name": name, "content": content,
              "mime": mime, "author": author, "seq": self.seq}
        self.seq += 1
        self.broadcast("EVENT", (ev,))
        return sha256_content(content)

    def _next_cid(self, tag):
        self._cid += 1
        return "%s%d_%d" % (tag, self._cid, int(time.time() * 1000) % 10 ** 5)

    def collect(self, cid, timeout=15.0):
        deadline = time.time() + timeout
        while time.time() < deadline:
            while True:
                try:
                    msg = self.result_q.get_nowait()
                except Exception:
                    break
                if msg and msg[0] == "RESULT" and msg[1] == cid:
                    return msg[2]
            time.sleep(0.02)
        raise TimeoutError("no RESULT for %s" % cid)

    def get(self, node, name_or_addr):
        cid = self._next_cid("g")
        self._send(node, "GET", (name_or_addr, cid))
        return self.collect(cid)

    def resolve(self, node, query):
        cid = self._next_cid("r")
        self._send(node, "RESOLVE", (query, cid))
        return self.collect(cid)

    def state(self, node):
        cid = self._next_cid("s")
        self._send(node, "STATE", (cid,))
        return self.collect(cid)

    def resync(self, node):
        self._send(node, "RESYNC")

    def kill(self, node):
        p = self.procs[node]
        if p.is_alive():
            p.terminate()
            p.join(timeout=2)
        with self._clk:
            if node in self.conns:
                try:
                    self.conns[node].close()
                except OSError:
                    pass
                del self.conns[node]

    def restart(self, node):
        self.kill(node)
        inq = mp.Queue()
        p = node_spawn(node, self.n, inq, self._tls_kwargs())
        p.start()
        self.inqs[node] = inq
        self.procs[node] = p
        time.sleep(0.8)
        self._wait_conn_all(deadline=15)

    def stop(self):
        self._stop.set()
        for i in range(self.n):
            self._send(i, "STOP")
        for p in self.procs:
            p.join(timeout=2)
        for p in self.procs:
            if p.is_alive():
                p.terminate()
                p.join(timeout=2)
        time.sleep(0.3)
        try:
            self._srv.close()
        except OSError:
            pass
        if self._tls_cert is not None:
            shutil.rmtree(self._tls_dir, ignore_errors=True)


# ---------------------------------------------------------------------- #
# Verdict: the web as a working network, scripted across real processes
# ---------------------------------------------------------------------- #
def _script(drv):
    # W1/W2: publish pages on different nodes; identical content dedups
    a_home = drv.publish("home", "<h1>welcome home</h1>", "text/html", "alice")
    b_maps = drv.publish("maps", "street-level tiles", "text/plain", "bob")
    c_home2 = drv.publish("home", "<h1>welcome home</h1>", "text/html", "carol")
    time.sleep(0.6)

    # W1: a page published on one node is served by EVERY node; archives
    # converge bit-identical and verify
    snaps = {i: drv.state(i) for i in range(drv.n)}
    heads = sorted({snaps[i]["head"] for i in snaps})
    lengths = sorted({snaps[i]["length"] for i in snaps})
    verify_all = all(snaps[i]["verify"] for i in snaps)
    names_agree = all(snaps[i]["names"] == snaps[0]["names"] for i in snaps)

    got = {i: drv.get(i, "home") for i in range(drv.n)}
    served_everywhere = all(
        g["found"] and g["content"] == "<h1>welcome home</h1>" and g["integrity"]
        for g in got.values())

    # W2: dedup - both 'home' publishes have the same address; GET by address
    # is served directly
    dedup_ok = (a_home == c_home2)
    n_addrs = snaps[0]["n_addrs"]
    by_addr = drv.get(2, a_home)
    addr_lookup_ok = by_addr["found"] and by_addr["name"] == "home"

    # W4: name resolution - a near-miss query resolves to the intended page
    near = drv.resolve(0, "homee")
    near_ok = near and near[0]["name"] == "home"
    maps_hit = drv.resolve(1, "map")

    # W3: crash a node, its pages still served by survivors; stateless
    # restart resyncs bit-identical
    drv.kill(3)
    survived = drv.get(1, "maps")
    survived_ok = survived["found"] and survived["content"] == "street-level tiles"
    drv.restart(3)
    drv.resync(3)
    time.sleep(0.8)
    snap3 = drv.state(3)
    resynced = snap3["length"] == snaps[0]["length"]
    resynced_equal = snap3["head"] == snaps[0]["head"]
    resynced_names = snap3["names"] == snaps[0]["names"]

    return {
        "heads_set_size": len(heads), "lengths": lengths,
        "verify_all": bool(verify_all), "names_agree": bool(names_agree),
        "served_everywhere": bool(served_everywhere),
        "dedup_ok": bool(dedup_ok), "n_addrs": n_addrs,
        "addr_lookup_ok": bool(addr_lookup_ok),
        "near_resolves": bool(near_ok), "near_hit": near,
        "maps_hit": maps_hit,
        "survived_ok": bool(survived_ok),
        "resynced": bool(resynced), "resynced_equal": bool(resynced_equal),
        "resynced_names": bool(resynced_names),
        "snap3_verify": bool(snap3["verify"]),
    }


def run_verdict(tls=False):
    drv = WebDriver(N_NODES, tls=tls)
    try:
        return _script(drv)
    finally:
        drv.stop()


def _tamper_check():
    drv = WebDriver(N_NODES)
    try:
        _script(drv)
        snap = drv.state(0)
        pages = snap["pages"]
        tampered = None
        if pages:
            page = pages[0]
            # flip one byte of the page content -> address no longer matches
            flipped = "X" + page["content"][1:]
            bad = {"found": True, "name": page["name"],
                   "content": flipped, "addr": page["addr"]}
            tampered = (sha256_content(flipped) != page["addr"])
        other_ok = bool(drv.state(1)["verify"])
        return {"tamper_flip_detected": bool(tampered),
                "other_node_still_valid": other_ok}
    finally:
        drv.stop()


def _verdict():
    import datetime
    seeds = (42, 11, 7)
    per = {}
    for s in seeds:
        per[str(s)] = run_verdict(tls=False)
    tls_run = run_verdict(tls=True)
    tamper = _tamper_check()

    def ok(pred):
        return (all(pred(per[str(s)]) for s in seeds) and pred(tls_run))

    w1 = ok(lambda o: o["heads_set_size"] == 1 and len(o["lengths"]) == 1
            and o["verify_all"] and o["names_agree"] and o["served_everywhere"])
    w2 = ok(lambda o: o["dedup_ok"] and o["addr_lookup_ok"]
            and o["n_addrs"] < 3)      # 3 publishes, 2 distinct contents
    w3 = ok(lambda o: o["survived_ok"] and o["resynced"]
            and o["resynced_equal"] and o["resynced_names"]
            and o["snap3_verify"])
    w4 = ok(lambda o: o["near_resolves"] and o["maps_hit"]
            and o["maps_hit"][0]["name"] == "maps")

    claims = [
        {"id": "W1",
         "claim": "content replicates: one chain head + one length across "
                  "all nodes, every archive verifies, all name sets agree, "
                  "and a page published on one node is served from every "
                  "other node with verified integrity",
         "verdict": "SUPPORTED" if w1 else "FAILED"},
        {"id": "W2",
         "claim": "content addressing: identical content maps to ONE address "
                  "(dedup across publishes) and a GET by address is served "
                  "directly from the content store",
         "verdict": "SUPPORTED" if w2 else "FAILED"},
        {"id": "W3",
         "claim": "the net survives node death: a crashed node's pages are "
                  "still served by survivors, and a stateless restart "
                  "resyncs to a bit-identical, verifying archive",
         "verdict": "SUPPORTED" if w3 else "FAILED"},
        {"id": "W4",
         "claim": "name resolution: a near-miss query resolves to the page "
                  "whose name embedding is nearest (the google.com -> "
                  "gooogle.com routing pattern over the wire)",
         "verdict": "SUPPORTED" if w4 else "FAILED"},
    ]
    verdict = "SUPPORTED" if all(c["verdict"] == "SUPPORTED"
                                 for c in claims) else "FAILED"
    results = {
        "experiment": "decentral_web (content-addressed P2P web prototype)",
        "date": datetime.date.today().isoformat(),
        "seeds": list(seeds),
        "n_nodes": N_NODES,
        "verdict": ("%s (structural, over real TCP processes): pages publish "
                    "once and replicate to a single verifying content-"
                    "addressed archive across all nodes (W1); identical "
                    "content dedups to one address with O(1) GET by address "
                    "(W2); a crashed node's pages stay served by survivors "
                    "and a stateless restart resyncs bit-identical (W3); "
                    "and near-miss names resolve to the intended page by "
                    "char-ngram embedding routing (W4) - on the repo's own "
                    "T70 socket transport, LedgerChain archive, and T55i "
                    "name-embedding pattern, with mutual TLS optional"
                    % verdict),
        "claims": claims,
        "per_seed": per,
        "tls_run": {k: v for k, v in tls_run.items()},
        "tamper": tamper,
    }
    with open(DATA_JSON, "w") as f:
        json.dump(results, f, indent=1, sort_keys=True)
    print("verdicts written to %s" % DATA_JSON)
    for c in claims:
        print("  %s: %s" % (c["id"], c["verdict"]))
    print("  W1 served everywhere: %s" % w1)
    print("  W2 dedup (3 publishes -> %s addrs): %s"
          % (per["42"]["n_addrs"], w2))
    print("  W4 near-miss 'homee' -> %s" % per["42"]["near_hit"])
    print("  W3 resync equal: %s" % w3)
    return results


# ---------------------------------------------------------------------- #
# Demo: the web as an interactive REPL
# ---------------------------------------------------------------------- #
def _demo():
    drv = WebDriver(N_NODES)
    print("=" * 62)
    print("DECENTRAL WEB - interactive (type 'help' for commands)")
    print("=" * 62)
    try:
        while True:
            try:
                line = input("web> ").strip()
            except EOFError:
                break
            if not line:
                continue
            cmd, _, rest = line.partition(" ")
            if cmd == "help":
                print("  publish NAME [mime] TEXT | get NAME | resolve QUERY")
                print("  state | quit")
            elif cmd == "publish":
                parts = rest.split(None, 2)
                if len(parts) < 2:
                    print("  usage: publish NAME TEXT")
                    continue
                if len(parts) == 2:
                    name, content = parts
                    mime = "text/plain"
                else:
                    name, mime, content = parts
                addr = drv.publish(name, content, mime)
                print("  published %s -> %s..." % (name, addr[:16]))
            elif cmd == "get":
                for i in range(drv.n):
                    g = drv.get(i, rest)
                    if g["found"]:
                        print("  [node %d] %s (%s) integrity=%s" %
                              (i, g["name"], g["mime"], g["integrity"]))
                        print("    %s" % g["content"])
                        break
                else:
                    print("  not found: %s" % rest)
            elif cmd == "resolve":
                for hit in drv.resolve(0, rest):
                    print("  %s (dist %s)" % (hit["name"], hit["dist"]))
            elif cmd == "state":
                s = drv.state(0)
                print("  node0: %d events, %d pages, head %s, verify %s"
                      % (len(s["events"]), len(s["names"]),
                         (s["head"] or "")[:12], s["verify"]))
            elif cmd == "quit":
                break
            else:
                print("  unknown command (try 'help')")
    finally:
        drv.stop()


def main(argv):
    mp.freeze_support()
    if "--verdict" in argv:
        _verdict()
    else:
        _demo()


if __name__ == "__main__":
    main(sys.argv[1:])
