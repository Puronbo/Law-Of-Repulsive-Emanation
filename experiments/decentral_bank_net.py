"""
DECENTRAL BANK NETWORK (T70) - fragments as real processes.

Phase 1 (T68) proved signatures + WAL in ONE process; its own limit said the
quorum was "an in-process simulation."  This file removes that: every fragment
runs as its OWN OS process (multiprocessing), and ALL inter-fragment messages
travel through a driver-owned relay that can partition or drop them.  The
consensus path is real message exchange: PROPOSE -> VOTE -> COMMIT -> NOTIFY,
with replicas synced via SYNC_REQ/SYNC when gaps appear.

This is still NOT BFT (crease #16); Phase 2 measures how the honest-majority
quorum behaves when it cannot peek at another process's memory.

  Node      - one fragment process: authoritative ledger for its fragment,
              full replicas of every other fragment, witness-vote logic.
  Network   - the harness in the driver: starts the node processes, relays
              node->node messages only along a controllable reachability
              graph (partitions = cut edges); node->driver and driver->node
              are always open.  The relay is pumped by the driver (Windows
              spawn cannot pickle bound-method process targets).

Tests (each with a null):
  T12 network commit + consistency: txs submitted over real messages commit
      via a real witness quorum; afterwards every node's replica of every
      ledger is bit-identical and a replay conserves total balance.
  T13 partition + rejoin: cut the network in two; measure commit availability
      on each side (quorums straddling the cut degrade); rejoin; wait for
      sync; verify all nodes converge to identical ledgers, chains re-validate
      (no double-spend, nonces monotone), and conservation still holds.
  T14 Byzantine across processes:
      (a) fabrication - a corrupt fragment broadcasts a forged block; honest
          nodes must reject it (signatures/hash) at rate 1.0.
      (b) availability wall - corrupt witnesses (vote-invert + refuse) vs f%;
          honest commit success drops as corruption crosses ~50%, reproducing
          crease #16 over real messages.
      (c) partition equivocation - two conflicting blocks for the same account
          and nonce committed to opposite halves; each half accepts its own
          during the partition (double-spend window), and the fork is
          DETECTED after rejoin (not prevented) - the honest wall.
  T15 crash + stateless restart (T71): terminate one node process mid-flight,
      confirm its accounts cannot transact while it is down but everyone
      else's commits survive (k-1 honest witnesses still exceed half), then
      restart it with EMPTY ledgers and let it recover EVERY fragment - its
      OWN included - from peers' replicas.  A stateless node is rebuilt
      entirely from the local-witness ring; recovery is proven by
      re-convergence, chain validity, conservation, and a fresh commit.

Limits (crease-worthy, printed):
  - Still majority-honesty, not BFT: a >50%-corrupt neighbourhood, or a
    partition the proposer can exploit, wins until detection.
  - Single machine, deterministic topology (no real sockets/TLS).
  - Crash recovery is from PEERS' replicas: if every node loses state at
    once, only the per-fragment WAL (T8) can rebuild - not tested here.
"""

import json
import multiprocessing as mp
import os
import socket
import struct
import sys
import threading
import time
import traceback
from collections import defaultdict, deque

import numpy as np

from cryptography.hazmat.primitives.asymmetric.ed25519 import (  # noqa: E402
    Ed25519PrivateKey)
from cryptography.hazmat.primitives.serialization import (  # noqa: E402
    Encoding, PublicFormat)

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "Universals"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from decentral_bank import (  # noqa: E402
    Ledger, verify_tx, sign_tx, address_of, embed, to_disk)
from manifold.decentral_net import DecentralNet  # noqa: E402


# ---------------------------------------------------------------------- #
# Transports (the SAME protocol runs over either)
# ---------------------------------------------------------------------- #
SOCK_PORT_BASE = 60100


def _frame(msg):
    data = json.dumps(msg).encode()
    return struct.pack(">I", len(data)) + data


def _unframe(buf):
    """Pull complete frames from a byte buffer; returns (frames, rest)."""
    frames = []
    while len(buf) >= 4:
        (ln,) = struct.unpack(">I", buf[:4])
        if len(buf) < 4 + ln:
            break
        frames.append(json.loads(buf[4:4 + ln].decode()))
        buf = buf[4 + ln:]
    return frames, buf


class QueueTransport:
    """Driver-relayed transport (mp.Queue).  Messages move as Python tuples
    through the controllable relay; used by the deterministic T12-T15 suite."""
    def __init__(self, inq, outq):
        self.inq = inq
        self.outq = outq

    def recv(self, timeout):
        try:
            msg = self.inq.get(timeout=timeout)
        except Exception:
            return None
        return (msg[0], msg[1], msg[2:])

    def is_ready(self, peers):
        return True

    def send(self, dst, kind, args=()):
        self.outq.put((dst, (kind, *args)))


class SocketTransport:
    """Real TCP loopback transport with the SAME message schema.  Each node
    listens on its own port and keeps outbound connections to every peer and
    to the driver; inbound messages land in a shared queue.  Reachability
    (partitions) is enforced by the driver sending REACH - a node drops
    inbound traffic from peers outside its allowed set.  A maintainer thread
    re-establishes any connection that dies (crash/restart)."""
    def __init__(self, node_id, n_frag, inq):
        self.node_id = node_id
        self.inq = inq
        self.port = SOCK_PORT_BASE + node_id
        self.n = n_frag
        self.allowed = None
        self._conns = {}
        self._pending = defaultdict(list)       # dst -> buffered frames
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        deadline = time.time() + 6        # retry bind: a killed process from a
        while True:                       # previous test can still hold the port
            try:
                self._srv.bind(("127.0.0.1", self.port))
                break
            except OSError as e:
                if time.time() > deadline:
                    raise
                time.sleep(0.1)
        self._srv.listen(64)
        threading.Thread(target=self._serve, daemon=True).start()
        ports = {j: SOCK_PORT_BASE + j for j in range(n_frag) if j != node_id}
        ports["driver"] = SOCK_PORT_BASE + n_frag
        threading.Thread(target=self._maintain, args=(ports,),
                         daemon=True).start()

    def recv(self, timeout):
        try:
            msg = self.inq.get(timeout=timeout)
        except Exception:
            return None
        return (msg[0], msg[1], msg[2])

    def set_reachability(self, allowed):
        self.allowed = set(allowed) if allowed is not None else None

    def is_ready(self, peers):
        """True while a quorum is still ATTAINABLE: more than half of the
        given witnesses are connected.  A dead witness leaves k-1 > half live
        ones, so its owner keeps committing (it just waits out the deadline);
        if every witness is gone no commit is possible and blocks wait."""
        with self._lock:
            live = sum(1 for p in peers if p in self._conns)
            return live > len(peers) / 2

    def _serve(self):
        while not self._stop.is_set():
            try:
                c, _ = self._srv.accept()
            except OSError:
                return
            threading.Thread(target=self._reader, args=(c,),
                             daemon=True).start()

    def _maintain(self, ports):
        while not self._stop.is_set():
            for pid, port in ports.items():
                with self._lock:
                    have = pid in self._conns
                if not have:
                    self._connect(pid, port)
            time.sleep(0.2)

    def _connect(self, peer_id, port):
        try:
            s = socket.create_connection(("127.0.0.1", port), timeout=0.25)
        except OSError:
            return
        s.settimeout(None)              # blocking: idle conns must NOT look EOF
        with self._lock:
            self._conns[peer_id] = s
        threading.Thread(target=self._reader, args=(s, peer_id),
                         daemon=True).start()
        self._flush(peer_id, s)

    def _flush(self, dst, s):
        """Deliver everything buffered for 'dst' once the connection exists.
        Frames that cannot be sent stay buffered for the next reconnect."""
        with self._lock:
            pending = self._pending.get(dst, [])
            self._pending[dst] = []
        i = 0
        while i < len(pending):
            try:
                s.sendall(pending[i])
                i += 1
            except OSError:
                with self._lock:
                    self._pending[dst] = pending[i:] + self._pending[dst]
                    if self._conns.get(dst) is s:
                        del self._conns[dst]
                try:
                    s.close()
                except OSError:
                    pass
                return

    def _reader(self, s, outbound_for=None):
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
                src, kind, args = msg[0], msg[1], msg[2]
                if (self.allowed is not None and src != "driver"
                        and src not in self.allowed):
                    continue
                self.inq.put((src, kind, tuple(args)))
        if outbound_for is not None:
            with self._lock:
                if self._conns.get(outbound_for) is s:
                    del self._conns[outbound_for]
        try:
            s.close()
        except OSError:
            pass

    def send(self, dst, kind, args=()):
        frame = _frame([self.node_id, kind, list(args)])
        with self._lock:
            s = self._conns.get(dst)
            if s is None:
                self._pending[dst].append(frame)
                return
            self._pending[dst].append(frame)
        self._flush(dst, s)


# ---------------------------------------------------------------------- #
# Node (a fragment, running in its own process)
# ---------------------------------------------------------------------- #
def node_main_loop(node_id, witnesses, faulty, refusing, n_frag, vote_timeout,
                   transport):
    """Event loop for one fragment process.  'faulty'/'refusing' simulate a
    corrupt fragment: vote-inverting and vote-silencing respectively.
    'transport' abstracts delivery; the SAME loop runs over the queue relay
    and over real TCP sockets."""
    ledger = Ledger(node_id)
    replicas = {f: Ledger(f) for f in range(n_frag)}
    pending = defaultdict(list)       # frag -> out-of-order buffered blocks
    sync_inflight = defaultdict(int)  # frag -> consecutive SYNC re-requests
    quorums = []                      # in-flight commit proposals
    submit_buffer = deque()   # serialized pending client txs

    def send(dst, kind, args=()):
        transport.send(dst, kind, args)

    def drain(frag):
        while pending.get(frag):
            ok, _ = rep_for(frag).replica_append(pending[frag][0])
            if ok:
                pending[frag].pop(0)
            else:
                break

    def rep_for(frag):
        return ledger if frag == node_id else replicas[frag]

    def handle(src, kind, args):
        if kind == "STOP":
            pass
        elif kind == "REACH":
            transport.set_reachability(args[0])
        elif kind == "QUERY_STATE":
            cid = args[0]
            snap = {}
            for f in range(n_frag):
                rep = rep_for(f)
                snap[f] = {"head": rep.head, "blocks": rep.blocks}
            send("driver", "STATE", (cid, snap))
        elif kind == "NOTIFY":
            frag, block = args
            ok, _ = rep_for(frag).replica_append(block)
            if not ok:
                pending[frag].append(block)
                if sync_inflight[frag] < 3:
                    sync_inflight[frag] += 1
                    send(frag, "SYNC_REQ", (frag, len(rep_for(frag).blocks)))
            else:
                drain(frag)
                sync_inflight[frag] = 0
        elif kind == "SYNC_REQ":
            frag, from_idx = args
            send(src, "SYNC", (frag, rep_for(frag).blocks[from_idx:]))
        elif kind == "SYNC":
            frag, blocks = args
            for b in blocks:
                ok, _ = rep_for(frag).replica_append(b)
                if ok:
                    drain(frag)
                    sync_inflight[frag] = 0
                elif sync_inflight[frag] < 3:
                    sync_inflight[frag] += 1
                    send(frag, "SYNC_REQ", (frag, len(rep_for(frag).blocks)))
        elif kind == "RESYNC":
            # Full catch-up (used on rejoin AND on stateless restart): pull
            # every OTHER fragment from its owner, and our OWN fragment from
            # every peer - a peer's replica of us is authoritative until we
            # catch up, and we cannot serve ourselves (the relay drops
            # self-messages).  For a synced owner this is a no-op (peers can
            # never be ahead of the authority), so the extra traffic is safe.
            for f in range(n_frag):
                sync_inflight[f] = 0
                if f == node_id:
                    for j in range(n_frag):
                        if j != node_id:
                            send(j, "SYNC_REQ", (f, len(rep_for(f).blocks)))
                else:
                    send(f, "SYNC_REQ", (f, len(rep_for(f).blocks)))
        elif kind == "PROPOSE":
            proposer, frag, block = args
            rep = rep_for(frag)
            if refusing:
                return                          # silence (no vote)
            ok, _ = validate_proposal(rep, block)
            if faulty:
                ok = not ok
            send(proposer, "VOTE", (frag, block["index"], ok))
        elif kind == "VOTE":
            frag, idx, approved = args
            for q in quorums:
                if q["frag"] == frag and q["idx"] == idx:
                    q["replies"][src] = approved
                    break
        elif kind == "SUBMIT":
            submit_buffer.append((args[0], args[1]))

    def start_block(tx, cid):
        """Append a client tx as a new block and begin its quorum.  Called
        only when no quorum for this fragment is in flight (serialized)."""
        ok, why = ledger.try_append([tx])
        if not ok:
            send("driver", "CLIENT_RESULT", (cid, False, why))
            return
        block = ledger.blocks[-1]
        for w in witnesses:
            send(w, "PROPOSE", (node_id, node_id, block))
        quorums.append({"frag": node_id, "idx": block["index"], "cid": cid,
                        "replies": {}, "deadline": time.time() + vote_timeout})

    while True:
        msg = transport.recv(0.05)
        if msg is not None:
            if msg[1] == "STOP":
                break
            try:
                handle(msg[0], msg[1], msg[2])
            except Exception:
                print(f"NODE {node_id} CRASHED on {msg[0]} {msg[1]}:",
                      file=sys.stderr)
                traceback.print_exc()
                break
        now = time.time()
        for q in list(quorums):
            if len(q["replies"]) >= len(witnesses) or now > q["deadline"]:
                approved = sum(1 for v in q["replies"].values() if v)
                if approved > len(witnesses) / 2:
                    block = ledger.blocks[q["idx"]]
                    for j in range(n_frag):
                        if j != node_id:
                            send(j, "NOTIFY", (node_id, block))
                    send("driver", "CLIENT_RESULT", (q["cid"], True, "ok"))
                else:
                    ledger.rollback()
                    send("driver", "CLIENT_RESULT", (q["cid"], False,
                                                     "quorum-denied"))
                quorums.remove(q)
        if not any(q["frag"] == node_id for q in quorums) and submit_buffer:
            if transport.is_ready(witnesses):
                try:
                    start_block(*submit_buffer.popleft())
                except Exception:
                    print(f"NODE {node_id} CRASHED in start_block:", file=sys.stderr)
                    traceback.print_exc()
                    break


def node_main_socket(node_id, witnesses, faulty, refusing, n_frag,
                     vote_timeout, inq):
    """Spawn entry for the socket mode: the SocketTransport (sockets, locks,
    threads) is created HERE in the child process - it cannot be pickled
    through Windows spawn."""
    node_main_loop(node_id, witnesses, faulty, refusing, n_frag, vote_timeout,
                   SocketTransport(node_id, n_frag, inq))


def validate_proposal(rep, block):
    """Witness-side check of a proposed block against its replica."""
    if block["index"] != len(rep.blocks):
        return False, "gap-index"
    if block["prev"] != rep.head:
        return False, "gap-prev"
    if block["hash"] != rep.block_hash(block["index"], block["prev"],
                                       block["txs"]):
        return False, "hash-mismatch"
    for t in block["txs"]:
        ok, why = verify_tx(t)
        if not ok:
            return False, why
        if t["nonce"] <= rep.nonces[t["from"]]:
            return False, "nonce-replay"
    return True, "ok"


# ---------------------------------------------------------------------- #
# Topology + accounts (driver side)
# ---------------------------------------------------------------------- #
def build_topology(n_frag, k):
    net = DecentralNet(dim=2, k=k, mu0=0.12)
    th = np.linspace(0, 2 * np.pi, n_frag, endpoint=False)
    homes = np.column_stack([0.55 * np.cos(th), 0.55 * np.sin(th)])
    for h in homes:
        net.add(h)
    net.settle(800)
    net.absorb(400)
    witnesses = [list(map(int, w)) for w in net._knn()]
    return net, witnesses


def route(net, addr):
    v = to_disk(embed(addr) * 0.6, 0.9)
    return int(net.predict(v.reshape(1, -1))[0])


def make_accounts(net, n_accounts):
    frag_for, keys, addrs = {}, {}, []
    for _ in range(n_accounts):
        priv = Ed25519PrivateKey.generate()
        pub = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        addr = address_of(pub)
        frag_for[addr] = route(net, addr)
        keys[addr] = (pub, priv)
        addrs.append(addr)
    return frag_for, keys, addrs


def make_tx(keys, sender, recipient, amount, nonce=1):
    pub, priv = keys[sender]
    tx = {"from": sender, "to": recipient, "amount": amount,
          "nonce": nonce, "pub": pub.hex()}
    tx["sig"] = sign_tx(priv, tx).hex()
    return tx


def next_tx(keys, nonces, sender, recipient, amount):
    nonces[sender] += 1
    return make_tx(keys, sender, recipient, amount, nonce=nonces[sender])


# ---------------------------------------------------------------------- #
# Harness
# ---------------------------------------------------------------------- #
class Network:
    """Driver-side network: starts node processes and relays their messages
    along a controllable reachability graph (partitions = cut edges).
    The relay is pumped by the driver itself."""

    def __init__(self, n_frag, k, vote_timeout=0.8, faulty=set(),
                 refusing=set()):
        self.n = n_frag
        self.k = k
        self.vote_timeout = vote_timeout
        self.faulty = set(faulty)
        self.refusing = set(refusing)
        self.net, self.witnesses = build_topology(n_frag, k)
        self.inqs, self.outqs, self.procs = [], [], []
        for i in range(n_frag):
            inq = mp.Queue()
            outq = mp.Queue()
            p = mp.Process(target=node_main_loop, args=(
                i, self.witnesses[i], i in faulty, i in refusing,
                n_frag, vote_timeout, QueueTransport(inq, outq)))
            p.daemon = True
            p.start()
            self.inqs.append(inq)
            self.outqs.append(outq)
            self.procs.append(p)
        self.result_q = mp.Queue()
        self.edges = {i: {j for j in range(n_frag) if j != i}
                      for i in range(n_frag)}
        self.pump()
        time.sleep(0.8)                          # let nodes spin up

    def pump(self):
        """Relay: move every queued node->node message that the current
        reachability graph allows, and every node->driver result."""
        for i, q in enumerate(self.outqs):
            while True:
                try:
                    dst, payload = q.get_nowait()
                except Exception:
                    break
                if dst == "driver":
                    self.result_q.put(payload)
                elif dst in self.edges.get(i, set()):
                    self.inqs[dst].put((i, *payload))

    def set_partition(self, groups):
        self.edges = {}
        for g in groups:
            for i in g:
                self.edges[i] = {j for j in g if j != i}

    def full_network(self):
        self.edges = {i: {j for j in range(self.n) if j != i}
                      for i in range(self.n)}

    def resync_all(self):
        """Reconnect catch-up: ask every node to pull any missing blocks from
        every owner (the on-connect reconcile routine)."""
        for i in range(self.n):
            self.inqs[i].put(("driver", "RESYNC"))
        self.pump()

    def resync(self, node_id):
        self.inqs[node_id].put(("driver", "RESYNC"))
        self.pump()

    def kill(self, node_id):
        """Simulate a process crash: terminate the node abruptly (no
        shutdown, no state flush).  Its queues stay behind but go silent."""
        p = self.procs[node_id]
        if p.is_alive():
            p.terminate()
            p.join(timeout=2)

    def restart(self, node_id):
        """Stateless restart: a fresh process with EMPTY ledgers and new
        queues.  It recovers purely by pulling from peers (RESYNC), including
        its own fragment's chain from their replicas."""
        self.kill(node_id)
        inq = mp.Queue()
        outq = mp.Queue()
        p = mp.Process(target=node_main_loop, args=(
            node_id, self.witnesses[node_id], node_id in self.faulty,
            node_id in self.refusing, self.n, self.vote_timeout,
            QueueTransport(inq, outq)))
        p.daemon = True
        p.start()
        self.inqs[node_id] = inq
        self.outqs[node_id] = outq
        self.procs[node_id] = p
        time.sleep(0.8)                          # let the fresh node spin up

    def submit(self, tx, cid):
        owner = self._owner_of(tx["from"])
        self.inqs[int(owner)].put(("driver", "SUBMIT", tx, cid))
        self.pump()

    def _owner_of(self, addr):
        return route(self.net, addr)

    def query_states(self, timeout=5.0):
        cids = [f"q{i}" for i in range(self.n)]
        for i in range(self.n):
            self.inqs[i].put(("driver", "QUERY_STATE", cids[i]))
        got, deadline = {}, time.time() + timeout
        while len(got) < self.n and time.time() < deadline:
            self.pump()
            while True:
                try:
                    msg = self.result_q.get_nowait()
                except Exception:
                    break
                if msg and msg[0] == "STATE" and msg[1] in cids:
                    # JSON round-trip (sockets) stringifies integer fragment
                    # keys; normalize so both transports hand back int keys.
                    got[msg[1]] = {int(k): v for k, v in msg[2].items()}
            time.sleep(0.02)
        if len(got) < self.n:
            raise RuntimeError("state query timeout")
        return got

    def collect_results(self, cids, timeout=25.0):
        cids = set(cids)
        got, deadline = {}, time.time() + timeout
        while time.time() < deadline and len(got) < len(cids):
            self.pump()
            while True:
                try:
                    msg = self.result_q.get_nowait()
                except Exception:
                    break
                if msg and msg[0] == "CLIENT_RESULT" and msg[1] in cids:
                    got[msg[1]] = (msg[2], msg[3])
            time.sleep(0.02)
        return got

    def inject_notify(self, frag, block, targets):
        """Driver-side injection of a block into specific nodes' replicas
        (used to simulate a compromised proposer)."""
        for t in targets:
            self.inqs[t].put(("driver", "NOTIFY", frag, block))
        self.pump()

    def wait(self, seconds):
        deadline = time.time() + seconds
        while time.time() < deadline:
            self.pump()
            time.sleep(0.05)

    def stop(self):
        for q in self.inqs:
            try:
                q.put(("driver", "STOP"))
            except Exception:
                pass
        for p in self.procs:
            p.join(timeout=2)
        for p in self.procs:
            if p.is_alive():
                p.terminate()


# ---------------------------------------------------------------------- #
# SocketNetwork: the SAME protocol over a real TCP loopback transport
# ---------------------------------------------------------------------- #
class SocketNetwork:
    """Driver side for real sockets.  The driver binds a listener (every
    node connects out to it) and also connects out to every node, so
    driver->node and node->driver traffic both flow over TCP.  Reachability
    (partitions) is enforced by REACH: the driver tells each node which peers
    it may receive from, and the node drops the rest - the same cut semantics
    as the relay's edge set, but over real TCP/IP packets."""

    def __init__(self, n_frag, k, vote_timeout=0.8, faulty=set(),
                 refusing=set()):
        self.n = n_frag
        self.k = k
        self.vote_timeout = vote_timeout
        self.faulty = set(faulty)
        self.refusing = set(refusing)
        self.net, self.witnesses = build_topology(n_frag, k)
        self.result_q = mp.Queue()
        self.driver_port = SOCK_PORT_BASE + n_frag
        self._srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._srv.bind(("127.0.0.1", self.driver_port))
        self._srv.listen(64)
        self._stop = threading.Event()
        threading.Thread(target=self._serve, daemon=True).start()
        self.inqs, self.procs = [], []
        for i in range(n_frag):
            inq = mp.Queue()
            p = mp.Process(target=node_main_socket, args=(
                i, self.witnesses[i], i in faulty, i in refusing,
                n_frag, vote_timeout, inq))
            p.daemon = True
            p.start()
            self.inqs.append(inq)
            self.procs.append(p)
        self.conns = {}                       # node id -> driver outbound sock
        self._clk = threading.Lock()
        self._wait_conn_all(deadline=12)

    def _serve(self):
        while not self._stop.is_set():
            try:
                c, _ = self._srv.accept()
            except OSError:
                return
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
                src, kind, args = msg[0], msg[1], msg[2]
                self.result_q.put((kind, *args))
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
                            ("127.0.0.1", SOCK_PORT_BASE + i), timeout=0.25)
                        s.settimeout(None)
                        self.conns[i] = s
                    except OSError:
                        pass

    def _wait_conn_all(self, deadline):
        """Retry driver->node connections until every node answers (nodes boot
        asynchronously; refused loopback conns cost ~0.25s each)."""
        end = time.time() + deadline
        while time.time() < end and len(self.conns) < self.n:
            self._connect_all()
            if len(self.conns) < self.n:
                time.sleep(0.2)

    def _send(self, node_id, kind, args=()):
        with self._clk:
            s = self.conns.get(node_id)
        if s is None:
            return
        try:
            s.sendall(_frame(["driver", kind, list(args)]))
        except OSError:
            pass

    def set_partition(self, groups):
        allowed = {}
        for g in groups:
            for i in g:
                allowed[i] = [j for j in g if j != i] + ["driver"]
        for i in range(self.n):
            self._send(i, "REACH", (allowed.get(i, ["driver"]),))

    def full_network(self):
        for i in range(self.n):
            self._send(i, "REACH", ([j for j in range(self.n) if j != i]
                                    + ["driver"],))

    def resync_all(self):
        for i in range(self.n):
            self._send(i, "RESYNC")

    def resync(self, node_id):
        self._send(node_id, "RESYNC")

    def submit(self, tx, cid):
        self._send(self._owner_of(tx["from"]), "SUBMIT", (tx, cid))

    def _owner_of(self, addr):
        return int(route(self.net, addr))

    def query_states(self, timeout=5.0):
        cids = [f"q{i}" for i in range(self.n)]
        for i in range(self.n):
            self._send(i, "QUERY_STATE", (cids[i],))
        got, deadline = {}, time.time() + timeout
        while len(got) < self.n and time.time() < deadline:
            while True:
                try:
                    msg = self.result_q.get_nowait()
                except Exception:
                    break
                if msg and msg[0] == "STATE" and msg[1] in cids:
                    # JSON round-trip (sockets) stringifies integer fragment
                    # keys; normalize so both transports hand back int keys.
                    got[msg[1]] = {int(k): v for k, v in msg[2].items()}
            time.sleep(0.02)
        if len(got) < self.n:
            raise RuntimeError("socket state query timeout")
        return got

    def collect_results(self, cids, timeout=25.0):
        cids = set(cids)
        got, deadline = {}, time.time() + timeout
        while time.time() < deadline and len(got) < len(cids):
            while True:
                try:
                    msg = self.result_q.get_nowait()
                except Exception:
                    break
                if msg and msg[0] == "CLIENT_RESULT" and msg[1] in cids:
                    got[msg[1]] = (msg[2], msg[3])
            time.sleep(0.02)
        return got

    def wait(self, seconds):
        deadline = time.time() + seconds
        while time.time() < deadline:
            time.sleep(0.05)

    def kill(self, node_id):
        p = self.procs[node_id]
        if p.is_alive():
            p.terminate()
            p.join(timeout=2)
        with self._clk:
            if node_id in self.conns:
                try:
                    self.conns[node_id].close()
                except OSError:
                    pass
                del self.conns[node_id]

    def restart(self, node_id):
        """Stateless restart over sockets: a fresh process rebinds the node's
        port and the maintainer threads on both sides re-establish the dead
        connections automatically."""
        self.kill(node_id)
        inq = mp.Queue()
        p = mp.Process(target=node_main_socket, args=(
            node_id, self.witnesses[node_id], node_id in self.faulty,
            node_id in self.refusing, self.n, self.vote_timeout, inq))
        p.daemon = True
        p.start()
        self.inqs[node_id] = inq
        self.procs[node_id] = p
        self._wait_conn_all(deadline=10)

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
        time.sleep(0.3)      # let OS release the node ports before a new test
        try:
            self._srv.close()
        except OSError:
            pass


# ---------------------------------------------------------------------- #
# Shared assertions
# ---------------------------------------------------------------------- #
def consensus_heads(snaps, n):
    """Per-fragment agreement: all nodes' replica head for each ledger."""
    frag_heads = {f: set() for f in range(n)}
    for snap in snaps.values():
        for f in range(n):
            frag_heads[f].add(snap[f]["head"])
    return {f: (len(h) == 1, h) for f, h in frag_heads.items()}


def replay_from(snaps, n, addrs, min_balance=100):
    """Replay the union of ledgers from one node's full view."""
    ref = list(snaps.values())[0]
    bal = {a: min_balance for a in addrs}
    valid = True
    for f in range(n):
        ld = Ledger(f)
        for b in ref[f]["blocks"]:
            ok, _ = ld.replica_append(b)
            valid = valid and ok
            for t in b["txs"]:
                bal[t["from"]] -= t["amount"]
                bal[t["to"]] += t["amount"]
    conserved = abs(sum(bal.values()) - len(addrs) * min_balance) < 1e-9
    return valid, conserved


# ---------------------------------------------------------------------- #
# Tests
# ---------------------------------------------------------------------- #
def test_t12_network_commit():
    n, k = 8, 3
    netw = Network(n, k)
    frag_for, keys, addrs = make_accounts(netw.net, 30)
    rng = np.random.RandomState(12)
    nonces = defaultdict(int)
    cids = []
    for i in range(24):
        s, r = rng.randint(0, len(addrs), size=2)
        if s == r:
            continue
        tx = next_tx(keys, nonces, addrs[s], addrs[r], int(rng.randint(1, 30)))
        cids.append(f"t{i}")
        netw.submit(tx, cids[-1])
    results = netw.collect_results(cids, timeout=40)
    missing = [c for c in cids if c not in results]
    ok_all = all(v[0] for v in results.values())
    snaps = netw.query_states()
    heads = consensus_heads(snaps, n)
    consistent = all(h[0] for h in heads.values())
    valid, conserved = replay_from(snaps, n, addrs)
    netw.stop()
    return {"test": "T12 network commit",
            "commits": len(results), "missing": missing, "all_ok": ok_all,
            "consistent": consistent, "conserved": conserved,
            "chains_valid": valid,
            "verdict": "PASS" if (ok_all and consistent and conserved and valid)
            else "FAIL"}


def test_t13_partition_rejoin():
    n, k = 8, 3
    netw = Network(n, k)
    frag_for, keys, addrs = make_accounts(netw.net, 32)
    group_a = {0, 1, 2, 3}
    group_b = {4, 5, 6, 7}
    netw.set_partition([list(group_a), list(group_b)])
    netw.wait(0.3)
    rng = np.random.RandomState(13)
    nonces = defaultdict(int)
    submitted = {}
    while len(submitted) < 16:
        s, r = rng.randint(0, len(addrs), size=2)
        if s == r:
            continue
        tx = next_tx(keys, nonces, addrs[s], addrs[r], int(rng.randint(1, 30)))
        cid = f"p{len(submitted)}"
        submitted[cid] = tx
        netw.submit(tx, cid)
    results = netw.collect_results(list(submitted.keys()))
    ok_during = sum(1 for v in results.values() if v[0])
    in_a = sum(1 for c, tx in submitted.items()
               if results.get(c, (False, ""))[0]
               and frag_for[tx["from"]] in group_a)
    in_b = sum(1 for c, tx in submitted.items()
               if results.get(c, (False, ""))[0]
               and frag_for[tx["from"]] in group_b)
    netw.full_network()
    netw.resync_all()
    netw.wait(2.5)
    snaps = netw.query_states()
    heads = consensus_heads(snaps, n)
    consistent = all(h[0] for h in heads.values())
    valid, conserved = replay_from(snaps, n, addrs)
    netw.stop()
    return {"test": "T13 partition + rejoin",
            "commits_during_partition": ok_during,
            "attempted": len(submitted),
            "commits_side_a": in_a, "commits_side_b": in_b,
            "converged": consistent, "conserved": conserved,
            "chains_valid": valid,
            "verdict": "PASS" if (consistent and conserved and valid) else "FAIL"}


def test_t14_fabrication():
    """A forged block (bad signature) broadcast by a corrupt fragment must be
    rejected by every honest node's replica (null: rate == 1.0)."""
    n, k = 6, 3
    netw = Network(n, k)
    frag_for, keys, addrs = make_accounts(netw.net, 12)
    victim = addrs[0]
    pub, _ = keys[victim]
    forged_tx = {"from": victim, "to": addrs[1], "amount": 5000,
                 "nonce": 1, "pub": pub.hex()}
    forged_tx["sig"] = "00" * 64          # garbage signature
    forged_block = {"index": 0, "prev": "genesis", "txs": [forged_tx]}
    forged_block["hash"] = Ledger(0).block_hash(0, "genesis", [forged_tx])
    victims_owner = frag_for[victim]
    targets = [j for j in range(n) if j != victims_owner]
    netw.inject_notify(victims_owner, forged_block, targets)
    netw.wait(0.8)
    snaps = netw.query_states()
    accepted = 0
    for snap in snaps.values():
        if len(snap[victims_owner]["blocks"]) == 1:
            accepted += 1
    netw.stop()
    return {"test": "T14a fabrication",
            "nodes_rejecting_forgery": n - accepted, "total": n,
            "forgery_accept_rate": round(accepted / n, 3),
            "verdict": "PASS" if accepted == 0 else "FAIL"}


def test_t14_availability_wall():
    """Honest commit success vs fraction of corrupt (vote-inverting +
    vote-silencing) witnesses.  Theory (k=4, need >half): a commit succeeds
    iff the owner has at most 1 corrupt witness, so P = (1-f)^4 + 4f(1-f)^3
    ~= {1.0, 0.65, 0.48, 0.31, 0.18} at f = {0, 0.3, 0.4, 0.5, 0.6} for
    SCATTERED corruption.  CONTIGUOUS corruption (a corrupt block) leaves an
    honest cluster whose witnesses are mostly honest -> availability holds
    higher - a real structural property of the local-witness ring, not a
    bug.  Both are measured."""
    def run(f_frac, scattered):
        n, k = 16, 4
        n_corrupt = int(round(n * f_frac))
        if scattered:
            rng = np.random.RandomState(1000 + int(f_frac * 100))
            corrupt = set(rng.choice(n, n_corrupt, replace=False).tolist())
        else:
            corrupt = set(range(n_corrupt))
        netw = Network(n, k, faulty=corrupt, refusing=corrupt,
                       vote_timeout=0.6)
        frag_for, keys, addrs = make_accounts(netw.net, 24)
        rng2 = np.random.RandomState(7)
        nonces = defaultdict(int)
        cids = []
        owners = sorted({frag_for[a] for a in addrs
                         if frag_for[a] not in corrupt})
        for owner in owners:
            accts = [a for a in addrs if frag_for[a] == owner]
            for _ in range(2):
                s = accts[rng2.randint(len(accts))]
                r = addrs[rng2.randint(len(addrs))]
                tx = next_tx(keys, nonces, s, r, int(rng2.randint(1, 20)))
                cids.append(f"w{len(cids)}")
                netw.submit(tx, cids[-1])
        results = netw.collect_results(cids, timeout=40)
        ok = sum(1 for v in results.values() if v[0]) / max(len(cids), 1)
        netw.stop()
        return round(float(ok), 3)

    scattered = []
    for f in [0.0, 0.3, 0.5, 0.7]:
        scattered.append({"faulty_frac": f, "honest_commit_frac": run(f, True)})
    contiguous = {"faulty_frac": 0.7, "honest_commit_frac": run(0.7, False)}
    return {"test": "T14b availability wall",
            "scattered_corruption_curve": scattered,
            "contiguous_corruption_at_0.7": contiguous,
            "verdict": "MEASURED"}


def test_t14_equivocation():
    """Partition equivocation: two conflicting blocks (same account, same
    nonce) injected to opposite halves during a partition.  Both halves
    accept their own (double-spend window); the fork is DETECTED after
    rejoin because one side cannot append the other's conflicting block."""
    n, k = 6, 3
    netw = Network(n, k)
    frag_for, keys, addrs = make_accounts(netw.net, 12)
    victim = addrs[0]
    owner = frag_for[victim]
    others = [j for j in range(n) if j != owner]
    half_a = others[: len(others) // 2]
    half_b = others[len(others) // 2:]
    tx1 = make_tx(keys, victim, addrs[1], 40, nonce=1)
    tx2 = make_tx(keys, victim, addrs[2], 40, nonce=1)
    b1 = {"index": 0, "prev": "genesis", "txs": [tx1]}
    b1["hash"] = Ledger(0).block_hash(0, "genesis", [tx1])
    b2 = {"index": 0, "prev": "genesis", "txs": [tx2]}
    b2["hash"] = Ledger(0).block_hash(0, "genesis", [tx2])
    netw.set_partition([list(half_a + [owner]), list(half_b)])
    netw.wait(0.3)
    netw.inject_notify(owner, b1, [owner] + half_a)
    netw.inject_notify(owner, b2, half_b)
    netw.wait(1.0)
    snaps_before = netw.query_states()
    heads_before = consensus_heads(snaps_before, n)[owner][1]
    divergent = len(heads_before) > 1
    netw.full_network()
    netw.resync_all()
    netw.wait(2.5)
    snaps_after = netw.query_states()
    detected = 0
    for snap in snaps_after.values():
        blocks = snap[owner]["blocks"]
        if len(blocks) == 1:
            detected += 1
    netw.stop()
    return {"test": "T14c partition equivocation",
            "divergent_heads_during_partition": divergent,
            "nodes_holding_single_version": detected, "total": n,
            "verdict": "PASS" if (divergent and detected > 0) else "FAIL"}


def test_t15_crash_restart():
    """Node crash + stateless restart.  A fragment's authority lives in its
    OWN process: while that process is dead its accounts cannot transact,
    while every other owner's commit still succeeds (the dead node's missing
    vote leaves k-1 honest witnesses, still > half).  A restarted node starts
    with EMPTY ledgers and must recover every fragment from peers' replicas -
    including its OWN fragment's chain.  Recovery is proven by re-convergence,
    chain validity, conservation, and a fresh commit (nonce continuity means
    the node truly rebuilt its own authority)."""
    n, k = 6, 3
    netw = Network(n, k)
    frag_for, keys, addrs = make_accounts(netw.net, 24)
    owners = sorted({frag_for[a] for a in addrs})
    rng = np.random.RandomState(15)
    nonces = defaultdict(int)

    # phase 1: healthy batch - at least one committed block in EVERY fragment
    cids = []
    for owner in owners:
        accts = [a for a in addrs if frag_for[a] == owner]
        for _ in range(2):
            s = accts[rng.randint(len(accts))]
            r = addrs[rng.randint(len(addrs))]
            if s == r:
                continue
            tx = next_tx(keys, nonces, s, r, int(rng.randint(1, 30)))
            cids.append(f"a{len(cids)}")
            netw.submit(tx, cids[-1])
    before = netw.collect_results(cids, timeout=40)
    before_ok = all(v[0] for v in before.values()) and len(before) == len(cids)

    # crash one node
    target = 2
    netw.kill(target)

    # phase 2a: txs OWNED by the dead fragment must NOT commit
    dead_accts = [a for a in addrs if frag_for[a] == target]
    dead_cids = []
    for _ in range(3):
        s = dead_accts[rng.randint(len(dead_accts))]
        r = addrs[rng.randint(len(addrs))]
        if s == r:
            continue
        tx = next_tx(keys, nonces, s, r, int(rng.randint(1, 20)))
        dead_cids.append(f"d{len(dead_cids)}")
        netw.submit(tx, dead_cids[-1])

    # phase 2b: txs owned by LIVE fragments must still commit
    live_owners = [o for o in owners if o != target]
    live_cids = []
    while len(live_cids) < 8:
        owner = live_owners[rng.randint(len(live_owners))]
        accts = [a for a in addrs if frag_for[a] == owner]
        s = accts[rng.randint(len(accts))]
        r = addrs[rng.randint(len(addrs))]
        if s == r:
            continue
        tx = next_tx(keys, nonces, s, r, int(rng.randint(1, 20)))
        live_cids.append(f"l{len(live_cids)}")
        netw.submit(tx, live_cids[-1])
    live = netw.collect_results(live_cids, timeout=40)
    live_ok = all(v[0] for v in live.values()) and len(live) == len(live_cids)

    # the dead node's submissions must NOT resolve (its process is gone)
    dead = netw.collect_results(dead_cids, timeout=6)
    dead_committed = len(dead)

    # phase 3: stateless restart + full catch-up from peers
    netw.restart(target)
    netw.resync(target)
    deadline = time.time() + 12
    converged = False
    snaps = None
    while time.time() < deadline and not converged:
        netw.wait(0.5)
        snaps = netw.query_states(timeout=8)
        heads = consensus_heads(snaps, n)
        converged = all(h[0] for h in heads.values())
        if not converged:
            netw.resync(target)
    recovered_own_matches_peers = (snaps is not None and
                                   snaps[f"q{target}"][target]["head"] ==
                                   snaps["q0"][target]["head"])

    # phase 4: recovered node must propose + commit a NEW tx
    s = dead_accts[rng.randint(len(dead_accts))]
    others = [a for a in addrs if a != s]
    r = others[rng.randint(len(others))]
    tx = next_tx(keys, nonces, s, r, int(rng.randint(1, 20)))
    netw.submit(tx, "recovered")
    post = netw.collect_results(["recovered"], timeout=40)
    recovered_commits = post.get("recovered", (False, ""))[0]

    valid, conserved = replay_from(snaps, n, addrs)
    netw.stop()
    return {"test": "T15 crash + stateless restart",
            "committed_before_crash": len(before), "before_all_ok": before_ok,
            "crashed_owner_txs_committed": dead_committed,
            "live_owner_commits_during_crash": len(live),
            "live_all_ok": live_ok,
            "recovered_own_chain_matches_peers": recovered_own_matches_peers,
            "converged": converged, "chains_valid": valid,
            "conserved": conserved,
            "recovered_node_commits_after": recovered_commits,
            "verdict": "PASS" if (
                before_ok and dead_committed == 0 and live_ok
                and recovered_own_matches_peers and converged and valid
                and conserved and recovered_commits) else "FAIL"}


def test_t16_socket_commit():
    """T16a: the SAME consensus over a real TCP loopback transport.  The
    protocol is transport-agnostic - node_main runs identically over the
    queue relay and over sockets.  Verifies commit, cross-node consistency,
    and conservation over real TCP/IP packets."""
    n, k = 6, 3
    sn = SocketNetwork(n, k)
    frag_for, keys, addrs = make_accounts(sn.net, 24)
    rng = np.random.RandomState(16)
    nonces = defaultdict(int)
    cids = []
    while len(cids) < 14:
        s, r = rng.randint(0, len(addrs), size=2)
        if s == r:
            continue
        tx = next_tx(keys, nonces, addrs[s], addrs[r], int(rng.randint(1, 30)))
        cids.append(f"s{len(cids)}")
        sn.submit(tx, cids[-1])
    results = sn.collect_results(cids, timeout=40)
    missing = [c for c in cids if c not in results]
    ok_all = all(v[0] for v in results.values())
    snaps = sn.query_states()
    heads = consensus_heads(snaps, n)
    consistent = all(h[0] for h in heads.values())
    valid, conserved = replay_from(snaps, n, addrs)
    sn.stop()
    return {"test": "T16a socket commit",
            "commits": len(results), "missing": missing, "all_ok": ok_all,
            "consistent": consistent, "conserved": conserved,
            "chains_valid": valid,
            "verdict": "PASS" if (ok_all and consistent and conserved and valid)
            else "FAIL"}


def test_t16_socket_partition():
    """T16b: partition + rejoin over real sockets.  The driver cuts the ring
    with REACH (nodes drop inbound traffic from the other half), measures
    degraded commit availability, then rejoins and verifies convergence over
    the same TCP transport."""
    n, k = 8, 3
    sn = SocketNetwork(n, k)
    frag_for, keys, addrs = make_accounts(sn.net, 32)
    group_a = {0, 1, 2, 3}
    group_b = {4, 5, 6, 7}
    sn.set_partition([list(group_a), list(group_b)])
    sn.wait(0.3)
    rng = np.random.RandomState(17)
    nonces = defaultdict(int)
    submitted = {}
    while len(submitted) < 16:
        s, r = rng.randint(0, len(addrs), size=2)
        if s == r:
            continue
        tx = next_tx(keys, nonces, addrs[s], addrs[r], int(rng.randint(1, 30)))
        cid = f"sp{len(submitted)}"
        submitted[cid] = tx
        sn.submit(tx, cid)
    results = sn.collect_results(list(submitted.keys()), timeout=40)
    ok_during = sum(1 for v in results.values() if v[0])
    sn.full_network()
    sn.resync_all()
    sn.wait(3.0)
    snaps = sn.query_states()
    heads = consensus_heads(snaps, n)
    consistent = all(h[0] for h in heads.values())
    valid, conserved = replay_from(snaps, n, addrs)
    sn.stop()
    return {"test": "T16b socket partition + rejoin",
            "commits_during_partition": ok_during,
            "attempted": len(submitted),
            "converged": consistent, "conserved": conserved,
            "chains_valid": valid,
            "verdict": "PASS" if (consistent and conserved and valid) else "FAIL"}


def test_t17_socket_crash_restart():
    """T17: the T15 crash + stateless-restart guarantee over REAL TCP sockets
    instead of the controllable relay.  Kill a node (its listener and every
    conn die; peers' maintainers keep failing to reconnect).  While it is
    dead: its OWN accounts cannot commit (no process to submit to), but live
    owners with k-1 > half witnesses still commit.  Restarting is truly
    stateless: a fresh process rebinds the port, re-establishes the fabric,
    and must rebuild every fragment - including its own chain - from peers'
    replicas, then propose a fresh tx."""
    n, k = 6, 3
    sn = SocketNetwork(n, k)
    frag_for, keys, addrs = make_accounts(sn.net, 24)
    owners = sorted({frag_for[a] for a in addrs})
    rng = np.random.RandomState(21)
    nonces = defaultdict(int)

    cids = []
    for owner in owners:
        accts = [a for a in addrs if frag_for[a] == owner]
        for _ in range(2):
            s = accts[rng.randint(len(accts))]
            r = addrs[rng.randint(len(addrs))]
            if s == r:
                continue
            tx = next_tx(keys, nonces, s, r, int(rng.randint(1, 30)))
            cids.append(f"a{len(cids)}")
            sn.submit(tx, cids[-1])
    before = sn.collect_results(cids, timeout=60)
    before_ok = all(v[0] for v in before.values()) and len(before) == len(cids)

    target = 2
    sn.kill(target)

    dead_accts = [a for a in addrs if frag_for[a] == target]
    dead_cids = []
    for _ in range(3):
        s = dead_accts[rng.randint(len(dead_accts))]
        r = addrs[rng.randint(len(addrs))]
        if s == r:
            continue
        tx = next_tx(keys, nonces, s, r, int(rng.randint(1, 20)))
        dead_cids.append(f"d{len(dead_cids)}")
        sn.submit(tx, dead_cids[-1])

    live_owners = [o for o in owners if o != target]
    live_cids = []
    while len(live_cids) < 8:
        owner = live_owners[rng.randint(len(live_owners))]
        accts = [a for a in addrs if frag_for[a] == owner]
        s = accts[rng.randint(len(accts))]
        r = addrs[rng.randint(len(addrs))]
        if s == r:
            continue
        tx = next_tx(keys, nonces, s, r, int(rng.randint(1, 20)))
        live_cids.append(f"l{len(live_cids)}")
        sn.submit(tx, live_cids[-1])
    live = sn.collect_results(live_cids, timeout=60)
    live_ok = all(v[0] for v in live.values()) and len(live) == len(live_cids)

    dead = sn.collect_results(dead_cids, timeout=8)
    dead_committed = len(dead)

    sn.restart(target)
    sn.resync(target)
    deadline = time.time() + 15
    converged = False
    snaps = None
    while time.time() < deadline and not converged:
        sn.wait(0.5)
        snaps = sn.query_states(timeout=8)
        heads = consensus_heads(snaps, n)
        converged = all(h[0] for h in heads.values())
        if not converged:
            sn.resync(target)
    recovered_own_matches_peers = (snaps is not None and
                                   snaps[f"q{target}"][target]["head"] ==
                                   snaps["q0"][target]["head"])

    s = dead_accts[rng.randint(len(dead_accts))]
    others = [a for a in addrs if a != s]
    r = others[rng.randint(len(others))]
    tx = next_tx(keys, nonces, s, r, int(rng.randint(1, 20)))
    sn.submit(tx, "recovered")
    post = sn.collect_results(["recovered"], timeout=60)
    recovered_commits = post.get("recovered", (False, ""))[0]

    valid, conserved = replay_from(snaps, n, addrs)
    sn.stop()
    return {"test": "T17 socket crash + stateless restart",
            "committed_before_crash": len(before), "before_all_ok": before_ok,
            "crashed_owner_txs_committed": dead_committed,
            "live_owner_commits_during_crash": len(live),
            "live_all_ok": live_ok,
            "recovered_own_chain_matches_peers": recovered_own_matches_peers,
            "converged": converged, "chains_valid": valid,
            "conserved": conserved,
            "recovered_node_commits_after": recovered_commits,
            "verdict": "PASS" if (
                before_ok and dead_committed == 0 and live_ok
                and recovered_own_matches_peers and converged and valid
                and conserved and recovered_commits) else "FAIL"}


# ---------------------------------------------------------------------- #
def main():
    print("=" * 66)
    print("DECENTRAL BANK NETWORK (T70/T71) - fragments as real processes")
    print("with the crash/restart guarantees repeated over real TCP sockets")
    print("=" * 66)
    results = {}
    for fn in [test_t12_network_commit, test_t13_partition_rejoin,
               test_t14_fabrication, test_t14_availability_wall,
               test_t14_equivocation, test_t15_crash_restart,
               test_t16_socket_commit, test_t16_socket_partition,
               test_t17_socket_crash_restart]:
        r = fn()
        results[r["test"]] = r
        print(f"  [{r['verdict']:8s}] {r['test']}")
        for kk, v in r.items():
            if kk not in ("test", "verdict"):
                print(f"        {kk} = {v}")

    limits = {
        "not_bft": "majority-honesty quorum; >50% corrupt neighbourhood or an exploitable partition wins until detected",
        "single_machine": "real loopback TCP sockets but still one machine and no TLS; transport-specific faults (partitions, machine death) are only modelled at the fragment level",
        "no_total_state_loss": "a crash recovers from PEERS' replicas (stateless restart); if every node loses state at once only the per-fragment WAL (T8) can rebuild - not tested here",
        "equivocation_needs_collusion": "a double-signed tx needs the account holder's key; the network only detects the fork afterwards",
    }
    print("\nLIMITS (crease-worthy):")
    for kk, v in limits.items():
        print(f"  {kk}: {v}")

    out = {"results": results, "limits": limits}
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "data", "decentral_bank_net_data.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote data/decentral_bank_net_data.json")


if __name__ == "__main__":
    main()
