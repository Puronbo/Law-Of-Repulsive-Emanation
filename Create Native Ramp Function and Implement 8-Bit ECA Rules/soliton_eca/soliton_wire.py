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
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from socket import socket as Socket, SO_REUSEADDR, SOL_SOCKET
from typing import Callable, Iterable

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


class SolitonWireClient:
    """A framed client that sends one request and reads the response."""
    def roundtrip(self, request: WireRequest, *, host: str, port: int,
                  ) -> WireResponse:
        with _new_socket() as sock:
            sock.connect((host, port))
            sock.sendall(wire_frame(request.envelope()))
            response = decode_response(recv_frame(sock))
        return response


def _new_socket() -> Socket:
    import socket
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def handshake_probe() -> int:
    """Echo the protocol version (a trivial connectivity probe, exported
    for tests/validators to confirm both ends share the wire)."""
    return VERSION
