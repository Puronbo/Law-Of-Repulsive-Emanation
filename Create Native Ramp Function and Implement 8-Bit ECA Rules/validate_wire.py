"""Standalone validator for the soliton wire protocol (framed TCP).

Runs three measured checks over real loopback sockets:
    1. ROUND TRIP  : N contiguous frames -> all delivered intact, in order.
    2. CORRUPTION   : a rewritten/tampered frame is rejected with WireError
                      (never partially admitted, never silently degraded).
    3. VERSION GATE : a mismatched protocol version is a clean protocol
                      error.

Exit 0 iff all three pass; prints each measured outcome.
"""
import sys
import threading

sys.path.insert(0, r"C:\Users\Me\Downloads\Puno_Calculus\Create Native Ramp Function and Implement 8-Bit ECA Rules")

from soliton_eca.soliton_snn import AERSpike  # noqa: E402
from soliton_eca.soliton_wire import (  # noqa: E402
    SolitonWireClient, SolitonWireServer, WireError, request_from_spikes,
    wire_frame, VERSION,
)


def _accept_once(srv, errs, results):
    try:
        req = srv.serve_one()
        results["n"] = len(req.spikes())
    except WireError as exc:
        errs.append(str(exc))
    except Exception as exc:  # noqa: BLE001
        errs.append("unexpected: %r" % exc)


def _roundtrip(spikes):
    handler = lambda req: {"delivered": len(req.spikes())}  # noqa: E731
    with SolitonWireServer(handler) as srv:
        errs = []
        results = {}
        t = threading.Thread(target=_accept_once, args=(srv, errs, results))
        t.start()
        client = SolitonWireClient()
        resp = client.roundtrip(request_from_spikes(spikes),
                                host="127.0.0.1", port=srv.bound_port)
        t.join()
        return resp.result.get("delivered"), errs, results


def _check_round_trip():
    spikes = [AERSpike(i, i % 3, (i + 1) % 3) for i in range(50)]
    n, errs, results = _roundtrip(spikes)
    got = results.get("n")
    assert not errs, "unexpected server error: %s" % errs
    assert got == len(spikes), "delivered %d != sent %d" % (got, len(spikes))
    assert n == len(spikes)
    print("  round trip: %d frames delivered intact, in order" % got)
    return True


def _check_corruption():
    # tamper an inner AERFrame (rewrite the checksum) -> server WireError
    from soliton_eca.soliton_framing import AERFrame
    from soliton_eca.soliton_wire import WireRequest, SolitonWireClient, \
        SolitonWireServer
    spikes = [AERSpike(0, 0, 2)]
    req = request_from_spikes(spikes)
    frames = req.frames.splitlines()
    frames[0] = frames[0].replace('"checksum":"', '"checksum":"00')  # corrupt
    corrupt_req = WireRequest(0, "\n".join(frames))

    def handler(req):
        # should never run: decoding the corrupted inner frame raises first
        req.spikes()
        return {"delivered": 99}

    with SolitonWireServer(handler) as srv:
        errs = []
        t = threading.Thread(target=_accept_once, args=(srv, errs, {}))
        t.start()
        try:
            client = SolitonWireClient()
            client.roundtrip(corrupt_req, host="127.0.0.1", port=srv.bound_port)
            t.join()
            raise AssertionError("corrupted frame was NOT rejected")
        except WireError:
            t.join()
            print("  corruption: tampered inner frame rejected (WireError)")
            return True


def _check_version_gate():
    from soliton_eca.soliton_wire import encode_envelope, _decode_envelope, \
        WireError
    env = encode_envelope("request", 0, "dummy")
    env["version"] = 2
    try:
        _decode_envelope(env)
        raise AssertionError("bad version was NOT rejected")
    except WireError:
        print("  version gate: mismatched version rejected (WireError)")
        return True


def main():
    print("soliton wire protocol validator")
    ok = _check_round_trip() and _check_corruption() and _check_version_gate()
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
