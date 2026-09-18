"""Soliton wire protocol: a framed, checksummed, versioned transport for
the soliton-cognitive runtime over real TCP loopback.

The in-process stack already has an *integrity* layer -- `AERFrame`
(per-spike SHA-256 + contiguous sequence) and `AdmissionPolicy` -- but no
*network* boundary: every exchange is an in-process JSON string.  This
module adds the missing transport while preserving the stack's ethos
(deterministic, lossless, measured):

    * length-prefixed frames (4-byte big-endian length, then UTF-8 JSON)
      so the byte stream is unambiguous and binary-safe;
    * a versioned request/response envelope
        {"version":1,"kind":...,"sequence":N,"frames":...,
         "checksum":sha256}
      whose checksum covers the whole envelope, so a corrupted, truncated,
      or rewritten frame fails BEFORE any spike is admitted;
    * the server re-verifies every inner `AERFrame` (its own per-spike
      SHA-256 + sequence), admits under the policy, runs the SNN/runtime,
      and replies with a response envelope carrying the measured outcome.

Failure is explicit: a bad envelope checksum, an invalid version, an
out-of-order frame, or a non-contiguous sequence yields a clean protocol
error -- not a silently degraded belief.  Every such rejection is a
measured fact the honesty gate can certify.

There is also a STREAMING path (`kind` "stream": `StreamRequest`,
``serve_one_stream``, ``SolitonWireStreamClient``) whose first verified
spike is delivered at the FIRST TICK -- O(1) in the batch size, before
the remainder of the batch has even arrived.  Each spike is verified by
its own per-frame SHA-256 + contiguous sequence as it arrives, and the
whole-batch ``stream_checksum`` (a band-level check) completes in the
background after the last frame; a band mismatch or any inner failure
surfaces as an explicit rejection envelope, so no successful belief is
ever produced for a rewritten stream.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass, field
from socket import socket as Socket, SO_REUSEADDR, SOL_SOCKET
from typing import Callable, Iterable, Iterator

from .soliton_admission import AdmissionPolicy, admit_spikes
from .soliton_framing import AERFrame, decode_frames, encode_frames
from .soliton_snn import AERSpike

VERSION = 1
_LEN_BYTES = 4


class WireError(ValueError):
    """A malformed, corrupted, or out-of-protocol exchange."""


def _canonical_bytes(envelope: dict[str, object]) -> bytes:
    """Deterministic byte layout over the envelope's meaningful fields.

    `frames` is already canonical compact JSON (produced by
    ``encode_frames``/``AERFrame.encode``), so it is hashed VERBATIM --
    we never re-escape the (potentially large) frame text just to hash
    it.  The small header is serialized once into a fixed JSON shape and
    a ``|`` delimiter (which cannot occur in JSON text) separates the two
    regions, making the layout unambiguous.
    """
    head = json.dumps({"kind": envelope["kind"],
                       "sequence": envelope["sequence"],
                       "version": envelope.get("version", VERSION)},
                      sort_keys=True, separators=(",", ":"))
    return head.encode("utf-8") + b"|" + str(envelope["frames"]).encode("utf-8")


def _checksum(envelope: dict[str, object]) -> str:
    return hashlib.sha256(_canonical_bytes(envelope)).hexdigest()


def encode_envelope(kind: str, sequence: int, frames_text: str) -> dict[str, object]:
    """Build a versioned, checksummed envelope dict."""
    env = {"version": VERSION, "kind": kind, "sequence": sequence,
           "frames": frames_text}
    env["checksum"] = _checksum(env)
    return env


def _decode_envelope(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise WireError("envelope must be a JSON object")
    if value.get("version") != VERSION:
        raise WireError("invalid protocol version: %r" % value.get("version"))
    kind = value.get("kind")
    if kind not in ("request", "response", "error"):
        raise WireError("invalid envelope kind: %r" % kind)
    if not isinstance(value.get("sequence"), int) or value["sequence"] < 0:
        raise WireError("invalid envelope sequence")
    if not isinstance(value.get("frames"), str):
        raise WireError("invalid envelope frames")
    expected = _checksum(value)
    if value.get("checksum") != expected:
        raise WireError("envelope checksum mismatch (corrupted or rewritten frame)")
    return value


def wire_frame(envelope: dict[str, object]) -> bytes:
    """Serialize an envelope as a length-prefixed, binary-safe frame.

    Serializes the envelope exactly once (JSON-escapes `frames` a single
    time for transport); the integrity checksum is computed by
    ``_canonical_bytes`` -- which never re-escapes the frame text -- so a
    large frame is only escaped once in total across checksum+transport.
    """
    payload = json.dumps(envelope, sort_keys=True, separators=(",", ":")).encode("utf-8")
    if len(payload) > (1 << (_LEN_BYTES * 8)) - 1:
        raise WireError("envelope too large to frame")
    return len(payload).to_bytes(_LEN_BYTES, "big") + payload


def recv_frame(stream) -> dict[str, object]:
    """Read exactly one length-prefixed frame from a socket/stream and
    verify its envelope.  Raises WireError on truncation or corruption."""
    head = _recv_exact(stream, _LEN_BYTES)
    length = int.from_bytes(head, "big")
    payload = _recv_exact(stream, length)
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WireError("frame is not valid UTF-8 JSON") from exc
    return _decode_envelope(value)


def _recv_exact(stream, n: int) -> bytes:
    chunks = bytearray()
    while len(chunks) < n:
        chunk = stream.recv(n - len(chunks))
        if not chunk:
            raise WireError("connection closed mid-frame (truncated)")
        chunks.extend(chunk)
    return bytes(chunks)


@dataclass(slots=True)
class WireRequest:
    """A client->server batch: the framed spike text plus its sequence.

    ``spikes()`` decodes and verifies the inner AER frames exactly ONCE,
    caching the result -- the server's verification pass and the handler
    both read the same decoded batch.
    """
    sequence: int
    frames: str
    _spikes: object = field(default=None, init=False, repr=False)

    def spikes(self) -> list[AERSpike]:
        if self._spikes is None:
            self._spikes = decode_frames(self.frames, start_sequence=0)
        return self._spikes

    def envelope(self) -> dict[str, object]:
        return encode_envelope("request", self.sequence, self.frames)


@dataclass(frozen=True, slots=True)
class WireResponse:
    """A server->client outcome envelope."""
    sequence: int
    result: dict[str, object]

    def envelope(self) -> dict[str, object]:
        return encode_envelope("response", self.sequence,
                               json.dumps(self.result, sort_keys=True))


def request_from_spikes(spikes: Iterable[AERSpike]) -> WireRequest:
    """Frame a spike batch into a single request at sequence 0."""
    return WireRequest(0, encode_frames(spikes, start_sequence=0))


def decode_response(envelope: dict[str, object]) -> WireResponse:
    env = _decode_envelope(envelope)
    if env["kind"] == "error":
        try:
            message = json.loads(env["frames"])["message"]
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise WireError("malformed error envelope") from exc
        raise WireError("server rejected request: %s" % message)
    if env["kind"] != "response":
        raise WireError("expected a response envelope, got %r" % env["kind"])
    result = json.loads(env["frames"])
    if not isinstance(result, dict):
        raise WireError("response payload must be a JSON object")
    return WireResponse(env["sequence"], result)


# ---- STREAMING path: first-tick O(1) delivery -------------------------
#
# A stream is a SINGLE exchange with the same header/lying-on-the-wire as
# a batch, except the inner AER frames are NOT bundled into one envelope:
# the client sends a small header envelope first, then each inner frame
# as a separate length-prefixed chunk.  The server may therefore deliver
# the FIRST verified spike at the first tick -- O(1) in the batch size,
# before the remainder of the batch has even arrived.
#
# Integrity is layered, exactly like the batch path:
#     * the stream header carries count + ``stream_checksum`` (a SHA-256
#       over the whole-batch payload bytes) and is itself protected by the
#       regular envelope checksum;
#     * every inner frame keeps its own per-spike AERFrame checksum and a
#       contiguous sequence, and is verified at its OWN tick;
#     * ``StreamRequest.spikes()`` yields each spike only AFTER that frame
#       verified; a tampered, reordered, or truncated frame raises before
#       the offending spike is delivered;
#     * the whole-batch ``stream_checksum`` is the band-level seal: it can
#       only complete after the last frame, so the server verifies it in
#       the background (``StreamRequest.finish()``) and REJECTS the stream
#       -- producing no success response, hence no belief -- if a
#       consistent rewrite slipped past every per-frame check.
#
# Admission is incremental to preserve first-tick: the header's exact
# count is checked at the header first tick (capacity), and each spike is
# admitted at its own tick with the same channel / horizon / order /
# burst / payload predicates as ``admit_spikes``.  A violation anywhere
# poisons the whole stream: the request is rejected, so no success
# response is ever issued for a faulty stream (individual delivered
# spikes remain independently verified -- the stream as a whole yields
# no belief).


def _stream_canonical_bytes(envelope: dict[str, object]) -> bytes:
    head = json.dumps({"count": envelope["count"], "kind": envelope["kind"],
                       "sequence": envelope["sequence"],
                       "stream_checksum": envelope["stream_checksum"],
                       "version": envelope.get("version", VERSION)},
                      sort_keys=True, separators=(",", ":"))
    return head.encode("utf-8")


def _stream_checksum(envelope: dict[str, object]) -> str:
    return hashlib.sha256(_stream_canonical_bytes(envelope)).hexdigest()


def _stream_body_bytes(sequence: int, count: int,
                       payloads: list[bytes]) -> bytes:
    acc = bytearray(("%d:%d:" % (sequence, count)).encode("utf-8"))
    for p in payloads:
        acc.extend(p)
    return bytes(acc)


def stream_frame(spikes: Iterable[AERSpike], *, sequence: int = 0,
                 ) -> tuple[dict[str, object], list[bytes]]:
    """Frame a spike batch into (stream header envelope, [inner chunk]).

    The header carries ``count`` and the whole-batch ``stream_checksum``.
    Each inner chunk is a length-prefixed AERFrame payload (the same
    bytes that would live inside a batch envelope, but framed as ONE
    per-spike wire message so the server can deliver the first tick
    without the tail).
    """
    payloads = []
    chunks = []
    for i, spike in enumerate(spikes):
        payload = AERFrame.create(i, spike).encode().encode("utf-8")
        if len(payload) > (1 << (_LEN_BYTES * 8)) - 1:
            raise WireError("stream frame too large to frame")
        payloads.append(payload)
        chunks.append(len(payload).to_bytes(_LEN_BYTES, "big") + payload)
    header = {"version": VERSION, "kind": "stream", "sequence": sequence,
              "count": len(payloads),
              "stream_checksum": hashlib.sha256(
                  _stream_body_bytes(sequence, len(payloads), payloads)
              ).hexdigest()}
    header["checksum"] = _stream_checksum(header)
    return header, chunks


def recv_stream_header(stream) -> dict[str, object]:
    """Read exactly one length-prefixed frame and require it to be a
    valid stream header (version, kind, sequence, count, stream_checksum,
    and the header's own checksum).  Raises WireError on any violation."""
    head = _recv_exact(stream, _LEN_BYTES)
    length = int.from_bytes(head, "big")
    payload = _recv_exact(stream, length)
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WireError("stream header is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise WireError("stream header must be a JSON object")
    if value.get("version") != VERSION:
        raise WireError("invalid stream protocol version: %r" % value.get("version"))
    if value.get("kind") != "stream":
        raise WireError("invalid stream header kind: %r" % value.get("kind"))
    if not isinstance(value.get("sequence"), int) or value["sequence"] < 0:
        raise WireError("invalid stream sequence")
    if not isinstance(value.get("count"), int) or value["count"] < 0:
        raise WireError("invalid stream count")
    if not isinstance(value.get("stream_checksum"), str):
        raise WireError("invalid stream checksum")
    expected = _stream_checksum(value)
    if value.get("checksum") != expected:
        raise WireError("stream header checksum mismatch (corrupted or rewritten header)")
    return value


@dataclass(slots=True)
class StreamRequest:
    """A client->server streaming request.

    ``spikes()`` is a lazy, one-shot generator that reads ONE inner frame
    per step (an O(1) first tick), verifies the AERFrame checksum and the
    contiguous sequence, updates the running whole-batch accumulator, and
    admits the spike (same predicates as ``admit_spikes``) BEFORE yielding
    it.  Wrapping the whole stream: ``finish()`` drains any frames a
    handler did not consume, completes the band-level ``stream_checksum``
    comparison, and reports whether the exchange was verified end to end.
    """
    sequence: int
    count: int
    stream_checksum: str
    _stream: object = field(repr=False)
    _policy: AdmissionPolicy = field(default=None, repr=False)
    _frames_read: int = field(default=0, init=False, repr=False)
    _acc: object = field(default=None, init=False, repr=False)
    _verified: bool = field(default=False, init=False, repr=False)
    _poisoned: bool = field(default=False, init=False, repr=False)
    _touched: bool = field(default=False, init=False, repr=False)
    _previous_ts: int = field(default=0, init=False, repr=False)
    _burst: object = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        self._acc = hashlib.sha256(
            ("%d:%d:" % (self.sequence, self.count)).encode("utf-8"))
        self._burst: Counter[int] = Counter()

    def spikes(self) -> Iterator[AERSpike]:
        if self._touched:
            raise WireError("stream spikes() may be consumed exactly once")
        self._touched = True
        while self._frames_read < self.count:
            yield self._read_one()
        self._verify_batch()

    def finish(self) -> bool:
        """Background envelope check: drain any frames the handler did not
        consume (verifying + admitting each), then check the whole-batch
        stream_checksum.  Returns True only if the full exchange verified
        end to end (every frame verified, every spike admitted, and the
        band-level checksum matched)."""
        if self._verified:
            return True
        try:
            while self._frames_read < self.count:
                self._read_one()
            self._verify_batch()
        except WireError:
            return False
        return self._verified and not self._poisoned

    def _read_one(self) -> AERSpike:
        expected = self._frames_read
        head = _recv_exact(self._stream, _LEN_BYTES)
        length = int.from_bytes(head, "big")
        payload = _recv_exact(self._stream, length)
        try:
            frame = AERFrame.decode(payload.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            self._poisoned = True
            raise WireError(
                "stream frame verification failed at %d: %s" % (expected, exc)
            ) from exc
        if frame.sequence != expected:
            self._poisoned = True
            raise WireError(
                "stream frame sequence gap at %d; expected %d"
                % (frame.sequence, expected))
        self._acc.update(payload)
        self._frames_read = expected + 1
        spike = frame.spike
        try:
            self._admit(spike)
        except WireError:
            self._poisoned = True
            raise
        return spike

    def _admit(self, spike: AERSpike) -> None:
        p = self._policy
        if p is None:
            return
        if spike.channel not in p.allowed_channels:
            raise WireError("channel %r is not admitted" % spike.channel)
        if spike.timestamp < 0 or spike.timestamp > p.max_future_ticks:
            raise WireError("event exceeds admission time horizon")
        if spike.timestamp < self._previous_ts:
            raise WireError("stream must be timestamp ordered")
        self._previous_ts = spike.timestamp
        if spike.payload > p.max_payload:
            raise WireError("event payload exceeds admission limit")
        n = self._burst[spike.timestamp] + 1
        if n > p.max_events_per_timestamp:
            raise WireError("timestamp burst exceeds admission limit")
        self._burst[spike.timestamp] = n

    def _verify_batch(self) -> None:
        if self._frames_read != self.count:
            raise WireError("stream truncated at %d of %d frames"
                            % (self._frames_read, self.count))
        if self._acc.hexdigest() != self.stream_checksum:
            raise WireError(
                "stream whole-batch checksum mismatch "
                "(consistent rewrite or missing frames)")
        self._verified = True


class SolitonWireServer:
    """A bounded, single-connection framed server for the runtime.

    Handles one request per connection by default (insertion-corruption
    on a shared connection is out of scope; each request is a fresh,
    checked exchange).  Spawns a short-lived child thread so the
    accept/serve loop is non-blocking and deterministic.
    """
    def __init__(self, handler: Callable[[WireRequest], dict[str, object]],
                 *, host: str = "127.0.0.1", port: int = 0,
                 policy: AdmissionPolicy = AdmissionPolicy()):
        self._handler = handler
        self._policy = policy
        self._host = host
        self._port = port
        self._listen: Socket | None = None
        self.bound_port: int | None = None

    def __enter__(self) -> "SolitonWireServer":
        self._listen = _new_socket()
        self._listen.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._listen.bind((self._host, self._port))
        self._listen.listen(1)
        self.bound_port = self._listen.getsockname()[1]
        return self

    def __exit__(self, *exc) -> None:
        if self._listen is not None:
            self._listen.close()
            self._listen = None

    def serve_one(self):
        """Accept one connection, handle one framed request, reply."""
        if self._listen is None:
            raise RuntimeError("server not bound (use as a context manager)")
        conn, _ = self._listen.accept()
        try:
            with conn:
                req_env = recv_frame(conn)
                if req_env["kind"] != "request":
                    self._reject(conn, "server expects a request envelope")
                    return None
                request = WireRequest(req_env["sequence"], req_env["frames"])
                # Verify the inner AER frames BEFORE any handler runs: a
                # corrupted/forged/out-of-order frame is a first-class
                # protocol error, never a silently degraded belief.  A
                # rejection is answered with a structured error envelope so
                # the client observes WHY, not an ambiguous truncation.
                try:
                    spikes = request.spikes()
                except ValueError as exc:
                    self._reject(conn, "request frame verification failed: %s" % exc)
                    return None
                # Admit under the policy (channel/payload/horizon/capacity
                # bounds) -- a request that violates policy is rejected up
                # front, atomically, and is reported as a protocol error.
                try:
                    admit_spikes(spikes, current_time=0, policy=self._policy)
                except ValueError as exc:
                    self._reject(conn, "request failed admission policy: %s" % exc)
                    return None
                result = self._handler(request)
                response = WireResponse(request.sequence, result)
                conn.sendall(wire_frame(response.envelope()))
        except WireError:
            raise
        return request

    @staticmethod
    def _reject(conn, message: str) -> None:
        """Answer a client with an explicit rejection envelope."""
        env = encode_envelope("error", 0,
                              json.dumps({"message": message}, sort_keys=True))
        conn.sendall(wire_frame(env))

    def serve_one_stream(self):
        """Accept one connection, handle one STREAMING request, reply.

        The header arrives first (with count + whole-batch
        ``stream_checksum``); capacity admission runs at the header's
        first tick, BEFORE any inner frame is read.  The handler consumes
        ``StreamRequest.spikes()`` lazily -- each spike delivered at its
        own first tick, verified + admitted first.  After the handler
        returns, the band-level whole-batch checksum is verified in the
        background (``finish()``) and only a fully verified exchange gets
        a success response; anything less is an explicit rejection.
        """
        if self._listen is None:
            raise RuntimeError("server not bound (use as a context manager)")
        conn, _ = self._listen.accept()
        try:
            with conn:
                header = recv_stream_header(conn)
                # capacity admission is knowable at the header first tick
                if header["count"] > self._policy.max_events:
                    self._reject(conn, "stream exceeds admission capacity")
                    return None
                if header["count"] > self._policy.max_pending_events:
                    self._reject(conn, "stream exceeds pending capacity")
                    return None
                request = StreamRequest(
                    header["sequence"], header["count"],
                    header["stream_checksum"], conn, self._policy)
                try:
                    result = self._handler(request)
                    if not request.finish():
                        self._reject(
                            conn, "stream whole-batch checksum did not verify")
                        return None
                except WireError as exc:
                    self._reject(conn, "stream rejected: %s" % exc)
                    return None
                response = WireResponse(request.sequence, result)
                conn.sendall(wire_frame(response.envelope()))
        except WireError:
            raise
        return request


class SolitonWireClient:
    """A framed client that sends one request and reads the response."""
    def roundtrip(self, request: WireRequest, *, host: str, port: int,
                  ) -> WireResponse:
        with _new_socket() as sock:
            sock.connect((host, port))
            sock.sendall(wire_frame(request.envelope()))
            response = decode_response(recv_frame(sock))
        return response


class SolitonWireStreamClient:
    """A streaming client: sends the stream header, then each inner
    length-prefixed AER frame chunk one at a time, then reads the single
    response.  Sending chunk-by-chunk is what lets the server deliver the
    first verified tick before the batch's tail has even left this client.
    """
    def roundtrip(self, spikes: Iterable[AERSpike], *, host: str, port: int,
                  ) -> WireResponse:
        header, chunks = stream_frame(spikes)
        with _new_socket() as sock:
            sock.connect((host, port))
            sock.sendall(wire_frame(header))
            for chunk in chunks:
                sock.sendall(chunk)
            response = decode_response(recv_frame(sock))
        return response


def _new_socket() -> Socket:
    import socket
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def handshake_probe() -> int:
    """Echo the protocol version (a trivial connectivity probe, exported
    for tests/validators to confirm both ends share the wire)."""
    return VERSION
