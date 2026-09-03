"""Tests for the soliton wire protocol (framed TCP transport).

These exercise the real loopback path (an ephemeral bound port, a
background accept thread, an actual socket round-trip) plus the pure
framing layer, asserting the protocol's measured guarantees:
    * order + integrity: N contiguous frames arrive intact, in order;
    * corruption: a tampered/forged frame is always rejected;
    * version gate: a mismatched protocol version is a clean WireError;
    * admission: a policy-violating request is rejected with a structured
      error envelope, never an ambiguous truncation.
"""
import json
import threading

import pytest

from soliton_eca.soliton_framing import decode_frames, encode_frames
from soliton_eca.soliton_snn import AERSpike
from soliton_eca.soliton_wire import (
    VERSION, SolitonWireClient, SolitonWireServer, WireError,
    WireRequest, WireResponse, decode_response, encode_envelope, handshake_probe,
    request_from_spikes, _decode_envelope, wire_frame,
)


def _serve_in_thread(server, errs, results):
    try:
        req = server.serve_one()
        if req is None:
            results["n"] = None
        else:
            results["n"] = len(req.spikes())
    except WireError as exc:
        errs.append(str(exc))
    except Exception as exc:  # noqa: BLE001
        errs.append("unexpected: %r" % exc)


def _run(handler, request):
    with SolitonWireServer(handler) as srv:
        errs, results = [], {}
        t = threading.Thread(target=_serve_in_thread, args=(srv, errs, results))
        t.start()
        client = SolitonWireClient()
        resp = client.roundtrip(request, host="127.0.0.1", port=srv.bound_port)
        t.join()
        assert not errs, errs
        return resp, results


def test_round_trip_preserves_order_and_count():
    spikes = [AERSpike(i, i % 3, (i + 1) % 3) for i in range(50)]
    handler = lambda req: {"delivered": len(req.spikes())}  # noqa: E731
    resp, results = _run(handler, request_from_spikes(spikes))
    assert resp.result == {"delivered": 50}
    assert results["n"] == 50


def test_envelope_round_trip_is_lossless():
    env = encode_envelope("request", 7, "hello")
    framed = wire_frame(env)
    assert isinstance(framed, bytes)
    # framing is byte-exact: the length prefix must match the payload
    length = int.from_bytes(framed[:4], "big")
    assert length == len(framed) - 4
    assert _decode_envelope(__import__("json").loads(framed[4:].decode()))["sequence"] == 7


def test_tampered_inner_frame_rejected():
    spikes = [AERSpike(0, 0, 2)]
    req = request_from_spikes(spikes)
    frames = req.frames.splitlines()
    frames[0] = frames[0].replace('"checksum":"', '"checksum":"00')
    corrupt = WireRequest(0, "\n".join(frames))

    def handler(req):
        return {"delivered": 99}

    with SolitonWireServer(handler) as srv:
        errs = []
        t = threading.Thread(target=_serve_in_thread, args=(srv, errs, {}))
        t.start()
        with pytest.raises(WireError) as excinfo:
            SolitonWireClient().roundtrip(corrupt, host="127.0.0.1",
                                          port=srv.bound_port)
        t.join()
        # the handler must never have run; the rejection names the reason
        assert "verification failed" in str(excinfo.value)


def test_tampered_envelope_checksum_rejected():
    env = encode_envelope("request", 0, "x")
    env["checksum"] = "0" * 64
    with pytest.raises(WireError):
        _decode_envelope(env)


def test_bad_version_rejected():
    env = encode_envelope("response", 0, "{}")
    env["version"] = VERSION + 1
    with pytest.raises(WireError):
        _decode_envelope(env)


def test_out_of_order_frames_rejected_by_SNN_path():
    # non-contiguous sequence inside a request is a protocol / verify error
    spikes = decode_frames("", require_contiguous=True)  # sanity
    assert spikes == []
    text = encode_frames((AERSpike(0, 0, 2),)) + "\n" + encode_frames(
        (AERSpike(0, 0, 2),), start_sequence=5)
    with pytest.raises(ValueError):
        decode_frames(text, require_contiguous=True)


def test_response_decode_round_trip():
    resp = WireResponse(3, {"delivered": 2})
    decoded = decode_response(resp.envelope())
    assert decoded.sequence == 3
    assert decoded.result == {"delivered": 2}


def test_version_probe_const():
    assert handshake_probe() == VERSION


def test_policy_violation_rejected_with_structured_error():
    # a channel outside the admission set must be rejected up front and the
    # client must observe WHY (a structured error envelope, not a truncation)
    bad = request_from_spikes([AERSpike(0, 1, 2, 1, 0.5, "nope")])

    def handler(req):  # pragma: no cover - must never run for a rejecting req
        return {"delivered": 99}

    with SolitonWireServer(handler) as srv:
        t = threading.Thread(target=lambda: srv.serve_one())
        t.start()
        with pytest.raises(WireError) as excinfo:
            SolitonWireClient().roundtrip(bad, host="127.0.0.1",
                                          port=srv.bound_port)
        t.join()
    assert "admission policy" in str(excinfo.value)


def test_out_of_bounds_payload_rejected():
    bad = request_from_spikes([AERSpike(0, 1, 2, 1, 9.9, "spike")])

    def handler(req):  # pragma: no cover
        return {"delivered": 99}

    with SolitonWireServer(handler) as srv:
        t = threading.Thread(target=lambda: srv.serve_one())
        t.start()
        with pytest.raises(WireError) as excinfo:
            SolitonWireClient().roundtrip(bad, host="127.0.0.1",
                                          port=srv.bound_port)
        t.join()
    assert "admission policy" in str(excinfo.value)


def test_checksum_is_stable_across_reencode():
    # the optimized checksum must be a pure function of the envelope's
    # meaningful fields, so re-encoding and re-parsing yields the same tag
    env = encode_envelope("request", 9, "abc")
    reparsed = json.loads(wire_frame(env)[4:].decode())
    assert reparsed["checksum"] == env["checksum"]


def test_verified_spikes_are_cached():
    req = request_from_spikes([AERSpike(0, 1, 2)])
    first = req.spikes()
    assert req.spikes() is first
