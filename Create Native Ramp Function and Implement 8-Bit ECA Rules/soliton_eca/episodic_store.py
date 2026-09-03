"""Checksummed append-only episodic storage for cognitive traces."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Iterable

from .cognitive_agent import CognitiveEvent


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    sequence: int
    event: CognitiveEvent
    checksum: str

    @staticmethod
    def checksum_for(sequence: int, event: CognitiveEvent) -> str:
        payload = json.dumps({"sequence": sequence, "event": {
            "timestamp": event.timestamp, "kind": event.kind, "payload": event.payload}},
            sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    @classmethod
    def create(cls, sequence: int, event: CognitiveEvent) -> "MemoryRecord":
        if sequence < 0:
            raise ValueError("sequence must be non-negative")
        return cls(sequence, event, cls.checksum_for(sequence, event))

    def encode(self) -> str:
        return json.dumps({"checksum": self.checksum, "sequence": self.sequence,
                           "event": {"timestamp": self.event.timestamp,
                                      "kind": self.event.kind,
                                      "payload": self.event.payload}},
                          sort_keys=True, separators=(",", ":"))

    @classmethod
    def decode(cls, line: str) -> "MemoryRecord":
        value = json.loads(line)
        if not isinstance(value, dict) or not isinstance(value.get("event"), dict):
            raise ValueError("invalid memory record")
        event_value = value["event"]
        try:
            event = CognitiveEvent(int(event_value["timestamp"]), str(event_value["kind"]),
                                   dict(event_value["payload"]))
            record = cls(int(value["sequence"]), event, str(value["checksum"]))
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("invalid memory record fields") from exc
        if record.sequence < 0 or record.checksum != cls.checksum_for(record.sequence, record.event):
            raise ValueError("memory checksum or sequence is invalid")
        return record


class EpisodicStore:
    """Append-only JSONL store with strict contiguous sequence verification."""
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def append(self, events: Iterable[CognitiveEvent]) -> int:
        existing = self.load()
        sequence = existing[-1].sequence + 1 if existing else 0
        records = [MemoryRecord.create(sequence + i, event)
                   for i, event in enumerate(events)]
        if records:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as handle:
                for record in records:
                    handle.write(record.encode() + "\n")
        return len(records)

    def load(self) -> list[MemoryRecord]:
        if not self.path.exists():
            return []
        records: list[MemoryRecord] = []
        with self.path.open(encoding="utf-8") as handle:
            for expected, line in enumerate(handle):
                if not line.strip():
                    continue
                record = MemoryRecord.decode(line)
                if record.sequence != len(records):
                    raise ValueError(f"memory sequence gap or duplicate at {record.sequence}")
                records.append(record)
        return records

    def events(self) -> list[CognitiveEvent]:
        return [record.event for record in self.load()]
