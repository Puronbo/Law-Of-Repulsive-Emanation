"""Standalone validator for SNN observability metrics + the runtime
over-the-wire adapter.

Checks `soliton_metrics.py` over a real SNN run, all measured:
    1. SNAPSHOT   : metrics() reports the scheduler truth exactly
                   (delivered == len(delivered), queue depth, firing
                   rate, synapse weight bounds) and is non-mutating.
    2. TRACE      : validate_spike_trace returns the event count for a
                   valid ordered trace and rejects an unordered trace
                   or a non-finite payload.
    3. WIRE       : the runtime-over-wire adapter (SolitonCognitiveRun-
                   time.wire_handler) serves TWO framed batches over ONE
                   keep-alive session on a real loopback socket, each
                   answered with live delivered/emitted/metrics counts.

Exit 0 iff all checks pass; prints each measured outcome.
"""
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from soliton_eca import (  # noqa: E402
    AERSpike, Connection, LIFNeuron, SolitonSNN, metrics,
    validate_spike_trace,
)


def _build_snn() -> SolitonSNN:
    return SolitonSNN(
        [LIFNeuron(0), LIFNeuron(1), LIFNeuron(2)],
        (Connection(0, 2, 1.0), Connection(1, 2, 1.0)))


def _check_snapshot():
    net = _build_snn()
    net.ingest([AERSpike(0, 0, 2), AERSpike(3, 1, 2)])
    net.run()
    time_before = net.time
    payload_before = (net.time, len(net.delivered), len(net.emitted))
    m1 = metrics(net)
    m2 = metrics(net)
    assert m1 == m2, "metrics() snapshot must be stable/repeatable"
    assert (net.time, len(net.delivered), len(net.emitted)) \
        == payload_before, "metrics() must not mutate scheduler state"
    assert time_before == 3, "two delivered events -> time == 3"
    assert m1.delivered_events == len(net.delivered) == 2
    assert m1.emitted_spikes == len(net.emitted)
    assert m1.firing_rate_per_tick \
        == len(net.emitted) / max(net.time + 1, 1)
    assert (m1.min_weight, m1.max_weight) == (1.0, 1.0)
    assert m1.max_queue_depth == 2, "both spikes queued before run"
    assert m1.current_time == net.time
    print("  snapshot: delivered=%d emitted=%d rate=%.3f/tick "
          "weights [1.0, 1.0], queue 2, repeatable + non-mutating"
          % (m1.delivered_events, m1.emitted_spikes,
             m1.firing_rate_per_tick))
    return True


def _check_trace():
    net = _build_snn()
    net.ingest([AERSpike(0, 0, 2), AERSpike(3, 1, 2)])
    net.run()
    assert validate_spike_trace(net.delivered) == 2
    # an out-of-order trace is rejected
    try:
        validate_spike_trace([AERSpike(5, 0, 2), AERSpike(1, 1, 2)])
    except ValueError:
        pass
    else:
        raise AssertionError("unordered trace accepted")
    # a non-finite payload is rejected
    try:
        validate_spike_trace([AERSpike(0, 0, 2, 1, float("nan"))])
    except ValueError:
        pass
    else:
        raise AssertionError("non-finite payload accepted")
    print("  trace: ordered finite trace counts 2; unordered/non-finite "
          "rejected")
    return True


def _check_runtime_over_wire():
    import socket as _socket

    from soliton_eca import (  # noqa: E402
        Action, SolitonCognitiveRuntime, SolitonWireServer,
        WireRequest, encode_frames, request_from_spikes,
    )
    from soliton_eca.soliton_wire import decode_response, recv_frame, \
        wire_frame

    runtime = SolitonCognitiveRuntime(
        (Action("noop", frozenset(), frozenset(), frozenset()),),
        neurons=(LIFNeuron(0), LIFNeuron(1)),
        connections=(Connection(0, 1, 1.0),))
    handler = runtime.wire_handler()
    with SolitonWireServer(handler) as srv:
        served = {}
        errs = []

        def accept_loop():
            try:
                served["n"] = srv.serve()
            except BaseException as exc:  # noqa: BLE001
                errs.append(repr(exc))

        t = threading.Thread(target=accept_loop)
        t.start()
        conn = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        conn.settimeout(3.0)
        conn.connect(("127.0.0.1", srv.bound_port))
        for i in (1, 2):  # two framed batches over ONE connection
            batch = (AERSpike(i, 0, 1),)
            conn.sendall(wire_frame(
                WireRequest(i, encode_frames(batch)).envelope()))
            resp = decode_response(recv_frame(conn))
            assert resp.result["delivered"] == 1
            assert resp.result["emitted"] == 1
            assert resp.result["metrics"]["delivered_events"] == i
            assert resp.result["metrics"]["current_time"] == i
        conn.close()
        t.join()
        assert not errs, errs
        assert served.get("n") == 2, (
            "keep-alive session served %r, expected 2" % served)
        print("  wire: runtime adapter served 2 framed batches over 1 "
              "keep-alive session, metrics live")
        # and SolitonWireClient still round-trips through the adapter
        from soliton_eca import SolitonWireClient
        second = {}
        with SolitonWireServer(handler) as srv:
            t2 = threading.Thread(target=lambda: second.update(
                n=srv.serve()))
            t2.start()
            client = SolitonWireClient()
            resp = client.roundtrip(
                request_from_spikes([AERSpike(9, 0, 1)]),
                host="127.0.0.1", port=srv.bound_port)
            t2.join(timeout=5.0)
            assert second.get("n") == 1, second
            assert resp.result["delivered"] == 1
        print("  wire: SolitonWireClient round-trip through the adapter "
              "delivered 1")
    return True


def main():
    print("soliton metrics + runtime-over-wire validator")
    ok = _check_snapshot() and _check_trace() and _check_runtime_over_wire()
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())