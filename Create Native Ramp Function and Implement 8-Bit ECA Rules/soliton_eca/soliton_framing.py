"""Integrity framing for the soliton AER spike protocol."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Iterable

from .soliton_snn import AERSpike, decode_spike, encode_spike


@dataclass(frozen=True, slots=True)
class AERFrame:
    sequence: int
    spike: AERSpike
    checksum: str

    @staticmethod
    def checksum_for(sequence: int, spike: AERSpike) -> str:
        payload = json.dumps({"sequence": sequence, "spike": spike.to_dict()},
                             sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    @classmethod
    def create(cls, sequence: int, spike: AERSpike) -> "AERFrame":
        if sequence < 0:
            raise ValueError("sequence must be non-negative")
        return cls(sequence, spike, cls.checksum_for(sequence, spike))

    def encode(self) -> str:
        return json.dumps({"checksum": self.checksum, "sequence": self.sequence,
                           "spike": self.spike.to_dict()},
                          sort_keys=True, separators=(",", ":"))

    @classmethod
    def decode(cls, line: str) -> "AERFrame":
        value = json.loads(line)
        if not isinstance(value, dict) or not isinstance(value.get("spike"), dict):
            raise ValueError("invalid AER frame object")
        try:
            sequence = int(value["sequence"])
            checksum = str(value["checksum"])
            spike = AERSpike.from_dict(value["spike"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("invalid AER frame fields") from exc
        expected = cls.checksum_for(sequence, spike)
        if sequence < 0 or checksum != expected:
            raise ValueError("AER frame checksum or sequence is invalid")
        return cls(sequence, spike, checksum)


def encode_frames(spikes: Iterable[AERSpike], *, start_sequence: int = 0) -> str:
    """Encode an ordered capture with contiguous sequence numbers."""
    if start_sequence < 0:
        raise ValueError("start_sequence must be non-negative")
    return "\n".join(AERFrame.create(start_sequence + i, spike).encode()
                     for i, spike in enumerate(spikes))


def decode_frames(text: str, *, start_sequence: int = 0,
                  require_contiguous: bool = True) -> list[AERSpike]:
    """Verify checksums and optionally enforce contiguous frame sequence."""
    if start_sequence < 0:
        raise ValueError("start_sequence must be non-negative")
    frames = [AERFrame.decode(line) for line in text.splitlines() if line.strip()]
    spikes: list[AERSpike] = []
    expected = start_sequence
    for frame in frames:
        if require_contiguous and frame.sequence != expected:
            raise ValueError(f"AER sequence gap or duplicate at {frame.sequence}; expected {expected}")
        expected = frame.sequence + 1
        spikes.append(frame.spike)
    return spikes
