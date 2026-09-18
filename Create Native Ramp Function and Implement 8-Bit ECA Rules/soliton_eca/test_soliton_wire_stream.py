"""Tests for the soliton wire STREAMING path.

The streaming path delivers each verified spike at its OWN first tick --
O(1) in the batch size -- then seals the whole exchange with a band-level
``stream_checksum`` checked in the background.  These tests drive the
real loopback path (ephemeral port, background accept thread, actual
socket round-trip) and assert:
    * first-tick delivery: the handler sees spike 0 BEFORE the tail of the
      batch is even sent (deterministic thread events, no sleeps);
    * order + integrity: N contiguous frames arrive intact, in order;
    * corruption: a tampered inner frame is rejected at its tick;
    * band-level rewrite: a rewrite that passes every per-frame check but
      distorts the whole-batch checksum is caught in the background and
      the stream is rejected as a unit;
    * version gate: a mismatched stream protocol version is a clean
      WireError;
    * admission: a policy-violating spike is rejected at its tick and the
      stream is rejected as a whole.
"""
import hashlib
import json
import socket
import threading

import pytest

from soliton_eca.soliton_snn import AERSpike
from soliton_eca.soliton_wire import (
    StreamRequest, SolitonWireServer, SolitonWireStreamClient, WireError,
    recv_stream_header, stream_frame, wire_frame,
    _stream_canonical_bytes,
)


def _recv_all(sock, n):
    b = bytearray()
    while len(b) < n:
        chunk = sock.recv(n - len(b))
        if not chunk:
            raise WireError("closed mid-frame")
        b.extend(chunk)
    return bytes(b)


def _read_response(sock):
    head = _recv_all(sock, 4)
    length = int.from_bytes(head, "big")
    payload = _recv_all(sock, length)
    return json.loads(payload.decode("utf-8"))


def test_stream_first_tick_before_tail():
    # The handler's first next(spikes()) must complete having only seen
    # the header + first inner chunk; the tail is withheld until the
    # handler reports the first tick.  If the server waited for the whole
    # batch, the event never fires -> deterministically FAIL, no sleeps.
    spikes = [AERSpike(i, i % 5, (i + 2) % 5) for i in range(8)]
    header, chunks = stream_frame(spikes)
    got_first_tick = threading.Event()
    first_tick = {}

    def handler(request: StreamRequest):
        it = iter(request.spikes())
        s0 = next(it)
        first_tick["first"] = (s0.timestamp, s0.source, s0.target)
        got_first_tick.set()
        return {"first": first_tick["first"]}

    with SolitonWireServer(handler) as srv:
        t = threading.Thread(target=lambda: srv.serve_one_stream())
        t.start()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", srv.bound_port))
        sock.sendall(wire_frame(header))
        sock.sendall(chunks[0])
        assert got_first_tick.wait(5.0), "first tick never fired => O(N)"
        sock.sendall(b"".join(chunks[1:]))
        resp = _read_response(sock)
        sock.close()
        t.join()
    assert resp["kind"] == "response"
    assert first_tick["first"] == (0, 0, 2)


def test_stream_round_trip_preserves_order_and_count():
    spikes = [AERSpike(i, i % 3, (i + 1) % 3) for i in range(50)]
    handler = lambda req: {"delivered": len(list(req.spikes()))}  # noqa: E731
    with SolitonWireServer(handler) as srv:
        t = threading.Thread(target=lambda: srv.serve_one_stream())
        t.start()
        resp = SolitonWireStreamClient().roundtrip(
            spikes, host="127.0.0.1", port=srv.bound_port)
        t.join()
    assert resp.result == {"delivered": 50}


def test_stream_tampered_inner_frame_rejected():
    spikes = [AERSpike(0, 0, 2), AERSpike(1, 1, 3), AERSpike(2, 2, 4)]
    header, chunks = stream_frame(spikes)
    payload = chunks[1][4:].decode("utf-8")
    payload = payload.replace('"checksum":"', '"checksum":"00', 1)
    chunks[1] = len(payload.encode("utf-8")).to_bytes(4, "big") \
        + payload.encode("utf-8")

    def handler(req):
        return {"delivered": 99}

    with SolitonWireServer(handler) as srv:
        t = threading.Thread(target=lambda: srv.serve_one_stream())
        t.start()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", srv.bound_port))
        sock.sendall(wire_frame(header))
        for chunk in chunks:
            sock.sendall(chunk)
        resp = _read_response(sock)
        sock.close()
        t.join()
    # rejected at the frame's tick: structured error, never a success
    assert resp["kind"] == "error"


def test_stream_band_level_rewrite_rejected():
    # every per-frame checksum stays VALID; only the whole-batch
    # stream_checksum (the band-level seal) is forged.  Per-frame checks
    # cannot catch it; the background band check must reject the stream.
    spikes = [AERSpike(0, 0, 2), AERSpike(1, 1, 3), AERSpike(2, 2, 4)]
    header, chunks = stream_frame(spikes)
    header["stream_checksum"] = hashlib.sha256(b"forged-body").hexdigest()
    header["checksum"] = hashlib.sha256(
        _stream_canonical_bytes(header)).hexdigest()

    def handler(req):
        return {"delivered": 99}

    with SolitonWireServer(handler) as srv:
        t = threading.Thread(target=lambda: srv.serve_one_stream())
        t.start()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", srv.bound_port))
        sock.sendall(wire_frame(header))
        for chunk in chunks:
            sock.sendall(chunk)
        resp = _read_response(sock)
        sock.close()
        t.join()
    assert resp["kind"] == "error"


def test_stream_bad_version_rejected():
    header, _ = stream_frame([AERSpike(0, 0, 2)])
    header["version"] = 999
    header["checksum"] = hashlib.sha256(
        _stream_canonical_bytes(header)).hexdigest()
    with pytest.raises(WireError):
        recv_stream_header(_FakeStream(wire_frame(header)))


def test_stream_policy_violation_rejected():
    spikes = [AERSpike(0, 0, 2), AERSpike(1, 1, 3),
              AERSpike(2, 2, 4), AERSpike(3, 3, 5, 1, 0.5, "nope")]
    header, chunks = stream_frame(spikes)

    def handler(req):
        return {"delivered": 99}

    with SolitonWireServer(handler) as srv:
        t = threading.Thread(target=lambda: srv.serve_one_stream())
        t.start()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", srv.bound_port))
        sock.sendall(wire_frame(header))
        for chunk in chunks:
            sock.sendall(chunk)
        resp = _read_response(sock)
        sock.close()
        t.join()
    assert resp["kind"] == "error"


def test_stream_unconsumed_frames_still_verified():
    # a handler that never iterates spikes() must still have the full
    # exchange verified in the background: finish() drains + band-checks.
    spikes = [AERSpike(i, i % 3, (i + 1) % 3) for i in range(20)]
    handler = lambda req: {"count": req.count}  # noqa: E731
    with SolitonWireServer(handler) as srv:
        t = threading.Thread(target=lambda: srv.serve_one_stream())
        t.start()
        resp = SolitonWireStreamClient().roundtrip(
            spikes, host="127.0.0.1", port=srv.bound_port)
        t.join()
    assert resp.result == {"count": 20}


class _FakeStream:
    def __init__(self, data: bytes):
        self._data = bytes(data)

    def recv(self, n: int) -> bytes:
        if not self._data:
            return b""
        out, self._data = self._data[:n], self._data[n:]
        return out