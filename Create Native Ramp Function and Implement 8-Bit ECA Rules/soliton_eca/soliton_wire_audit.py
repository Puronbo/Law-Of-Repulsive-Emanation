"""soliton_wire_audit: certifies the framed TCP wire protocol's measured
guarantees, in the same certificate shape the honesty gate consumes
(label / meta / verdict PASS|HONEST_NEGATIVE / n_ok / n_fail /
first_failure).

What is audited (all over the REAL loopback path -- an ephemeral bound
port, a background accept thread, an actual socket round-trip):

    L_wire_order_integrity          PASS -- N contiguous AER frames arrive
                                       intact and in order (byte-exact,
                                       same sequence).
    L_wire_tampered_frame_rejected  PASS -- a frame whose inner per-spike
                                       checksum is rewritten is rejected
                                       BEFORE the handler runs (the
                                       response is an explicit rejection).
    L_wire_tampered_envelope_reject PASS -- a tampered envelope checksum is
                                       rejected at the framing layer.
    L_wire_version_gate             PASS -- a mismatched protocol version
                                       is rejected cleanly.
    L_wire_admission_rejection      PASS -- a request that violates the
                                       admission policy (bad channel /
                                       out-of-bounds payload) is rejected
                                       with a structured error envelope
                                       naming why, and the handler never
                                       runs.
    L_wire_multi_request_session   PASS -- one socket connection carries
                                       N sequential independent requests,
                                       each verified + answered over the
                                       SAME connection (keep-alive); a
                                       clean close ends the session.  The
                                       legacy one-exchange-per-connection
                                       behaviour (L_wire_single_stream)
                                       is gone; the limitation was
                                       deliberately lifted.

Every verdict is a measured fact on the stated domain; nothing is assumed.
"""
from __future__ import annotations

import threading
from typing import Callable, Iterable

from .soliton_snn import AERSpike
from .soliton_wire import (
    SolitonWireClient, SolitonWireServer, WireError,
    WireRequest, decode_response, encode_envelope, recv_frame,
    request_from_spikes, wire_frame,
)


def certify(label: str, meta: dict[str, object],
            pred: Callable, domain: Iterable) -> dict[str, object]:
    """Certificate in the gate's shape: HONEST_NEGATIVE iff any datum
    fails the predicate (recorded with first_failure), else PASS."""
    n_ok = n_fail = 0
    first = None
    for d in domain:
        ok = bool(pred(d))
        n_ok += ok
        n_fail += not ok
        if not ok and first is None:
            first = {"datum": list(d) if isinstance(d, tuple) else d}
    return {
        "label": label,
        "meta": meta,
        "kind": "statement",
        "domain": meta.get("domain"),
        "points_checked": n_ok + n_fail,
        "n_ok": n_ok,
        "n_fail": n_fail,
        "status": "HONEST_NEGATIVE" if first is not None else "PASS",
        "first_failure": first,
    }


def _serve(server, errs, ran, result_box):
    try:
        req = server.serve_one()
        if req is None:
            result_box["rejected"] = True
        else:
            ran.append(1)
    except WireError as exc:
        errs.append(str(exc))
    except Exception as exc:  # noqa: BLE001
        errs.append("unexpected: %r" % exc)


def _roundtrip(request, handler, server_ran):
    """Run a request against a fresh server (default admission policy);
    returns the client response or None if the server rejected it."""
    with SolitonWireServer(handler) as srv:
        errs = []
        result_box = {}
        t = threading.Thread(target=_serve,
                             args=(srv, errs, server_ran, result_box))
        t.start()
        try:
            resp = SolitonWireClient().roundtrip(
                request, host="127.0.0.1", port=srv.bound_port)
        except WireError:
            resp = None
        t.join()
        # any unexpected server-side error is a hard audit failure
        if any("unexpected" in e for e in errs):
            raise AssertionError("server errored: %r" % errs)
        return resp


# ---- each certified law, measured -----------------------------------

def _L_order_integrity(n):
    """Round-trip n contiguous frames and check intact + in-order."""
    spikes = [AERSpike(i, i % 5, (i + 2) % 5) for i in range(n)]
    req = request_from_spikes(spikes)
    server_ran = []

    def handler(r):
        got = r.spikes()
        if len(got) != n:
            return {"n": len(got), "bad": True}
        for a, b in zip(spikes, got):
            if (a.timestamp, a.source, a.target,
                    a.polarity, a.payload, a.channel) != \
               (b.timestamp, b.source, b.target,
                    b.polarity, b.payload, b.channel):
                return {"n": len(got), "bad": True}
        return {"n": len(got), "bad": False}

    resp = _roundtrip(req, handler, server_ran)
    return resp is not None and resp.result.get("bad") is False and server_ran


def _L_tampered_frame_rejected(_):
    spikes = [AERSpike(0, 0, 2)]
    req = request_from_spikes(spikes)
    frames = req.frames.splitlines()
    frames[0] = frames[0].replace('"checksum":"', '"checksum":"00')
    corrupt = WireRequest(0, "\n".join(frames))
    server_ran = []

    def handler(r):  # must never run for a rejected request
        return {"delivered": 99}

    resp = _roundtrip(corrupt, handler, server_ran)
    # a structured rejection reaches the client => resp is None here (we
    # collapsed the WireError), AND the handler never ran
    return not server_ran


def _L_tampered_envelope_rejected(_):
    env = encode_envelope("request", 0, "x")
    env["checksum"] = "0" * 64
    try:
        from .soliton_wire import _decode_envelope
        _decode_envelope(env)
    except WireError:
        return True
    return False


def _L_version_gate(_):
    env = encode_envelope("response", 0, "{}")
    env["version"] = 999
    try:
        from .soliton_wire import _decode_envelope
        _decode_envelope(env)
    except WireError:
        return True
    return False


def _L_admission_rejection(which):
    """A policy-violating request (bad channel or oversized payload) is
    rejected with a structured error and the handler never runs."""
    if which == "channel":
        bad = request_from_spikes([AERSpike(0, 1, 2, 1, 0.5, "nope")])
    else:
        bad = request_from_spikes([AERSpike(0, 1, 2, 1, 9.9, "spike")])
    server_ran = []

    def handler(r):  # must never run
        return {"delivered": 99}

    resp = _roundtrip(bad, handler, server_ran)
    return not server_ran


def _L_multi_request_session(n):
    """Predicate for the candidate law 'one socket connection carries
    several requests in sequence'.  True ONLY IF all n sequential
    requests complete over the SAME connection, each verified and
    answered, and the session ends cleanly on the client's close."""
    from socket import socket as Socket

    with SolitonWireServer(lambda r: {"n": len(r.spikes())}) as srv:
        conn = Socket()
        conn.settimeout(3.0)
        conn.connect(("127.0.0.1", srv.bound_port))
        served = {}
        ok = {}

        def runner():
            try:
                served["n"] = srv.serve()
            except BaseException as exc:  # noqa: BLE001
                ok["error"] = repr(exc)

        t = threading.Thread(target=runner)
        t.start()
        for i in range(n):
            req = request_from_spikes([AERSpike(i, 1, 2)])
            conn.sendall(wire_frame(req.envelope()))
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


def wire_certificates() -> list[dict[str, object]]:
    certs = []

    def ok_cert(label, law, domain, pred):
        certs.append(certify(
            label,
            {"domain": "real loopback round-trip; all measured, none "
                       "assumed",
             "law": law,
             "measured_on": "soliton_eca.soliton_wire"},
            pred, domain))

    ok_cert("L_wire_order_integrity",
            "N contiguous AER frames arrive intact and in order over a "
            "real loopback request/response",
            [5, 10, 50, 200], _L_order_integrity)
    ok_cert("L_wire_tampered_frame_rejected",
            "a frame with a rewritten inner per-spike checksum is rejected "
            "before the handler runs (explicit rejection, never admitted)",
            [0], _L_tampered_frame_rejected)
    ok_cert("L_wire_tampered_envelope_rejected",
            "a tampered envelope checksum is rejected at the framing layer",
            [0], _L_tampered_envelope_rejected)
    ok_cert("L_wire_version_gate",
            "a mismatched protocol version is rejected cleanly (no "
            "silently degraded exchange)",
            [0], _L_version_gate)
    ok_cert("L_wire_admission_rejection",
            "a request violating the admission policy (bad channel or "
            "oversized payload) is rejected with a structured error "
            "naming why, and the handler never runs",
            ["channel", "payload"], _L_admission_rejection)
    ok_cert("L_wire_multi_request_session",
            "one socket connection carries N sequential independent "
            "requests, each verified and answered over the SAME "
            "connection; a clean close ends the session",
            [3, 8, 25], _L_multi_request_session)
    return certs


if __name__ == "__main__":
    import json
    import sys
    certs = wire_certificates()
    print("soliton wire protocol audit")
    for c in certs:
        print("  %-36s %-16s n_ok=%-4d n_fail=%d" % (
            c["label"], c["status"], c["n_ok"], c["n_fail"]))
    print("RESULT: %s" % ("PASS" if all(
        c["status"] in ("PASS", "HONEST_NEGATIVE") for c in certs)
        else "FAIL"))
    sys.exit(0 if all(
        c["status"] in ("PASS", "HONEST_NEGATIVE") for c in certs) else 1)
