"""soliton_wire_stream_audit: certifies the STREAMING wire path's measured
guarantees, in the same certificate shape the honesty gate consumes.

The streaming path (``stream_frame`` / ``recv_stream_header`` /
``StreamRequest`` / ``serve_one_stream`` / ``SolitonWireStreamClient``)
delivers each verified spike at its OWN first tick -- O(1) in the batch
size -- while a layer of integrity checks runs incrementally and a
whole-batch ``stream_checksum`` seals the exchange at the end:

    L_stream_first_tick_delivery   PASS -- the handler receives the first
                                       verified spike BEFORE the tail of
                                       the batch has even been sent
                                       (measured deterministically with
                                       thread events, no sleeps).
    L_stream_order_integrity       PASS -- N contiguous AER frames arrive
                                       intact and in order over the
                                       streaming path.
    L_stream_tampered_frame_reject PASS -- an inner frame with a rewritten
                                       per-spike checksum is rejected at
                                       its tick; the stream is rejected
                                       (no success response).
    L_stream_band_level_rewrite    PASS -- a rewrite that preserves every
                                       per-frame checksum but distorts the
                                       whole-batch stream_checksum is
                                       caught by the background band check
                                       and rejected as a unit.
    L_stream_version_gate          PASS -- a mismatched stream protocol
                                       version is rejected cleanly.
    L_stream_admission_rejected    PASS -- a policy-violating spike
                                       (bad channel / oversized payload)
                                       is rejected at its own tick and the
                                       stream is rejected as a whole.
    L_stream_multi_stream_session PASS -- one socket connection carries
                                       N sequential stream requests, each
                                       fully handled + answered over the
                                       SAME connection (keep-alive); a
                                       clean close ends the session.  The
                                       legacy one-stream-per-connection
                                       behaviour (L_stream_single_stream)
                                       is gone; the limitation was
                                       deliberately lifted.

Every verdict is a measured fact on the real loopback path (ephemeral
port, background accept thread, actual socket round-trip, deterministic
thread events).  Nothing is assumed.
"""
from __future__ import annotations

import threading
from typing import Callable, Iterable, Iterator

from .soliton_snn import AERSpike
from .soliton_wire import (
    SolitonWireStreamClient, SolitonWireServer, StreamRequest, WireError,
    decode_response, recv_frame, stream_frame, wire_frame,
)
from .soliton_wire_audit import certify


def _serve_stream(server, errs, ran, result_box):
    try:
        req = server.serve_one_stream()
        if req is None:
            result_box["rejected"] = True
        else:
            ran.append(1)
    except WireError as exc:
        errs.append(str(exc))
    except Exception as exc:  # noqa: BLE001
        errs.append("unexpected: %r" % exc)


class _FakeStream:
    """A minimal ``recv(n)``-capable stream over fixed bytes (for header
    level unit checks, mirroring the batch path's direct envelope tests)."""
    def __init__(self, data: bytes):
        self._data = bytes(data)

    def recv(self, n: int) -> bytes:
        if not self._data:
            return b""
        out, self._data = self._data[:n], self._data[n:]
        return out


def _L_first_tick_delivery(_):
    """The handler must receive the first verified spike before the tail
    of the batch has been sent at all.  Deterministic: the client sends
    the header + first chunk, then waits for the handler's
    ``got_first_tick`` event.  If the server waited for the whole batch
    before delivering, the event never fires and the test deadlocks into
    a timeout -- a measured FAIL, not an assumption."""
    spikes = [AERSpike(i, i % 5, (i + 2) % 5) for i in range(8)]
    header, chunks = stream_frame(spikes)
    got_first_tick = threading.Event()
    first_tick = {}
    errs = []

    def handler(request: StreamRequest):
        try:
            it = iter(request.spikes())
            s0 = next(it)  # first tick: must not wait for the tail
            first_tick["first"] = (s0.timestamp, s0.source, s0.target)
            got_first_tick.set()
            return {"first": first_tick["first"]}
        except Exception as exc:  # noqa: BLE001
            errs.append("handler: %r" % exc)
            raise

    with SolitonWireServer(handler) as srv:
        t = threading.Thread(target=_serve_stream,
                             args=(srv, errs, [], {}))
        t.start()
        import socket as _socket
        sock = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", srv.bound_port))
        sock.sendall(wire_frame(header))
        sock.sendall(chunks[0])          # ONLY the first inner chunk
        fired = got_first_tick.wait(5.0)
        if not fired:
            sock.close()
            t.join()
            return False                  # first tick stalled on the tail
        sock.sendall(b"".join(chunks[1:]))  # release the tail now
        # read the response frame (reuse wire framing via a socket recv)
        import json
        head = _recv_all(sock, 4)
        length = int.from_bytes(head, "big")
        payload = _recv_all(sock, length)
        sock.close()
        t.join()
        if errs:
            return False
        resp = json.loads(payload.decode("utf-8"))
        return (resp.get("kind") == "response"
                and first_tick.get("first") == (0, 0, 2))


def _recv_all(sock, n: int) -> bytes:
    b = bytearray()
    while len(b) < n:
        chunk = sock.recv(n - len(b))
        if not chunk:
            raise WireError("closed mid-frame")
        b.extend(chunk)
    return bytes(b)


def _L_order_integrity(n):
    spikes = [AERSpike(i, i % 5, (i + 2) % 5) for i in range(n)]
    ran = []
    errs = []

    def handler(request: StreamRequest):
        got = list(request.spikes())
        if len(got) != n:
            return {"n": len(got), "bad": True}
        for a, b in zip(spikes, got):
            if (a.timestamp, a.source, a.target,
                    a.polarity, a.payload, a.channel) != \
               (b.timestamp, b.source, b.target,
                    b.polarity, b.payload, b.channel):
                return {"n": len(got), "bad": True}
        return {"n": len(got), "bad": False}

    with SolitonWireServer(handler) as srv:
        t = threading.Thread(target=_serve_stream,
                             args=(srv, errs, ran, {}))
        t.start()
        try:
            resp = SolitonWireStreamClient().roundtrip(
                spikes, host="127.0.0.1", port=srv.bound_port)
        except WireError:
            resp = None
        t.join()
        if any("unexpected" in e for e in errs):
            return False
        return (resp is not None and resp.result.get("bad") is False
                and ran == [1])


def _L_tampered_frame_rejected(_):
    spikes = [AERSpike(0, 0, 2), AERSpike(1, 1, 3), AERSpike(2, 2, 4)]
    header, chunks = stream_frame(spikes)
    # rewrite the inner per-spike checksum of the MIDDLE frame only
    payload = chunks[1][4:].decode("utf-8")
    payload = payload.replace('"checksum":"', '"checksum":"00', 1)
    chunks[1] = len(payload.encode("utf-8")).to_bytes(4, "big") \
        + payload.encode("utf-8")
    errs = []

    def handler(request: StreamRequest):
        try:
            list(request.spikes())
        except WireError as exc:
            return {"rejected": str(exc)}
        return {"delivered": 99}

    import socket as _socket
    with SolitonWireServer(handler) as srv:
        t = threading.Thread(target=_serve_stream,
                             args=(srv, errs, [], {}))
        t.start()
        sock = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", srv.bound_port))
        sock.sendall(wire_frame(header))
        for chunk in chunks:
            sock.sendall(chunk)
        try:
            head = _recv_all(sock, 4)
            length = int.from_bytes(head, "big")
            payload = _recv_all(sock, length)
        except WireError:
            sock.close()
            t.join()
            return False
        sock.close()
        t.join()
        import json
        if errs:
            return False
        resp = json.loads(payload.decode("utf-8"))
        # the stream must be REJECTED: no success response, ever
        return resp.get("kind") == "error"


def _L_band_level_rewrite(_):
    """A consistent rewrite: every inner AER frame keeps a valid per-frame
    checksum, but the whole-batch stream_checksum in the header reflects a
    DIFFERENT body.  Per-frame checks cannot catch this; the background
    band-level check must, and the stream must be rejected as a unit."""
    spikes = [AERSpike(0, 0, 2), AERSpike(1, 1, 3), AERSpike(2, 2, 4)]
    header, chunks = stream_frame(spikes)
    import hashlib
    import json as _json
    from .soliton_wire import _stream_canonical_bytes
    header["stream_checksum"] = hashlib.sha256(b"forged-body").hexdigest()
    header["checksum"] = hashlib.sha256(
        _stream_canonical_bytes(header)).hexdigest()
    errs = []

    def handler(request: StreamRequest):
        try:
            list(request.spikes())  # per-frame checks all pass
        except WireError:
            return {"rejected": "per-frame"}
        return {"delivered": 99}

    import socket as _socket
    with SolitonWireServer(handler) as srv:
        t = threading.Thread(target=_serve_stream,
                             args=(srv, errs, [], {}))
        t.start()
        sock = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", srv.bound_port))
        sock.sendall(wire_frame(header))
        for chunk in chunks:
            sock.sendall(chunk)
        try:
            head = _recv_all(sock, 4)
            length = int.from_bytes(head, "big")
            payload = _recv_all(sock, length)
        except WireError:
            sock.close()
            t.join()
            return False
        sock.close()
        t.join()
        if errs:
            return False
        resp = _json.loads(payload.decode("utf-8"))
        return resp.get("kind") == "error"


def _L_version_gate(_):
    from .soliton_wire import recv_stream_header
    header, _ = stream_frame([AERSpike(0, 0, 2)])
    header["version"] = 999
    header["checksum"] = None
    import hashlib
    from .soliton_wire import _stream_canonical_bytes
    header["checksum"] = hashlib.sha256(
        _stream_canonical_bytes(header)).hexdigest()
    try:
        recv_stream_header(_FakeStream(wire_frame(header)))
    except WireError:
        return True
    return False


def _L_admission_rejected(which):
    """A policy-violating spike (bad channel or oversized payload) is
    rejected at its own tick; the stream is rejected as a whole (no
    success response, and the violating spike is never delivered)."""
    good = [AERSpike(0, 0, 2), AERSpike(1, 1, 3), AERSpike(2, 2, 4)]
    if which == "channel":
        bad = AERSpike(3, 3, 5, 1, 0.5, "nope")
    else:
        bad = AERSpike(3, 3, 5, 1, 9.9, "spike")
    spikes = good + [bad]
    header, chunks = stream_frame(spikes)
    errs = []

    def handler(request: StreamRequest):
        try:
            list(request.spikes())
        except WireError as exc:
            return {"rejected": str(exc)}
        return {"delivered": 99}

    import socket as _socket
    with SolitonWireServer(handler) as srv:
        t = threading.Thread(target=_serve_stream,
                             args=(srv, errs, [], {}))
        t.start()
        sock = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", srv.bound_port))
        sock.sendall(wire_frame(header))
        for chunk in chunks:
            sock.sendall(chunk)
        try:
            head = _recv_all(sock, 4)
            length = int.from_bytes(head, "big")
            payload = _recv_all(sock, length)
        except WireError:
            sock.close()
            t.join()
            return False
        sock.close()
        t.join()
        import json
        if errs:
            return False
        resp = json.loads(payload.decode("utf-8"))
        return resp.get("kind") == "error"


def _L_multi_stream_session(n):
    """Predicate for 'one socket connection carries several streams in
    sequence' -- True ONLY IF all n sequential stream requests complete
    over the SAME connection, each fully handled and answered, and the
    session ends cleanly on the client's close."""
    from socket import socket as Socket

    spikes = [AERSpike(0, 1, 2)]
    header, chunks = stream_frame(spikes)
    with SolitonWireServer(lambda r: {"n": len(list(r.spikes()))}) as srv:
        conn = Socket()
        conn.settimeout(3.0)
        conn.connect(("127.0.0.1", srv.bound_port))
        served = {}
        ok = {}

        def runner():
            try:
                served["n"] = srv.serve_streams()
            except BaseException as exc:  # noqa: BLE001
                ok["error"] = repr(exc)

        t = threading.Thread(target=runner)
        t.start()
        for _ in range(n):
            conn.sendall(wire_frame(header))
            for chunk in chunks:
                conn.sendall(chunk)
            resp = decode_response(recv_frame(conn))
            if resp.result.get("n") != 1:
                conn.close()
                t.join()
                return False
        conn.close()
        t.join()
        if "error" in ok:
            return False
        return served.get("n") == n


def wire_stream_certificates() -> list[dict[str, object]]:
    certs = []

    def ok_cert(label, law, domain, pred):
        certs.append(certify(
            label,
            {"domain": "real streaming loopback (header + inner chunks "
                       "over one socket); measured, none assumed",
             "law": law,
             "measured_on": "soliton_eca.soliton_wire streaming path"},
            pred, domain))

    ok_cert("L_stream_first_tick_delivery",
            "the handler receives the first verified spike at the first "
            "tick, O(1) in the batch: BEFORE the tail of the batch is even "
            "sent (measured with deterministic thread events, no sleeps)",
            [0], _L_first_tick_delivery)
    ok_cert("L_stream_order_integrity",
            "N contiguous AER frames arrive intact and in order over the "
            "streaming wire path",
            [5, 10, 50, 200], _L_order_integrity)
    ok_cert("L_stream_tampered_frame_rejected",
            "an inner frame with a rewritten per-spike checksum is "
            "rejected at its tick and the stream is rejected as a unit",
            [0], _L_tampered_frame_rejected)
    ok_cert("L_stream_band_level_rewrite",
            "a consistent rewrite that preserves every per-frame checksum "
            "but distorts the whole-batch stream_checksum is caught by "
            "the background band check and rejected; no success response",
            [0], _L_band_level_rewrite)
    ok_cert("L_stream_version_gate",
            "a mismatched stream protocol version is rejected cleanly "
            "(no silently degraded exchange)",
            [0], _L_version_gate)
    ok_cert("L_stream_admission_rejected",
            "a policy-violating spike (bad channel or oversized payload) "
            "is rejected at its own tick and the stream is rejected as a "
            "whole (no success response)",
            ["channel", "payload"], _L_admission_rejected)
    ok_cert("L_stream_multi_stream_session",
            "one socket connection carries N sequential stream requests, "
            "each fully handled and answered over the SAME connection; a "
            "clean close ends the session",
            [3, 8, 25], _L_multi_stream_session)
    return certs


if __name__ == "__main__":
    import json
    import sys
    certs = wire_stream_certificates()
    print("soliton wire STREAMING audit")
    for c in certs:
        print("  %-38s %-16s n_ok=%-4d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("RESULT: %s" % ("PASS" if all(
        c["status"] in ("PASS", "HONEST_NEGATIVE") for c in certs)
        else "FAIL"))
    sys.exit(0 if all(
        c["status"] in ("PASS", "HONEST_NEGATIVE") for c in certs) else 1)