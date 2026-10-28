"""A run as one timeline: its events and its model calls in time order, read from the run folder.
Only complete lines are read, so the same reader follows a run that is still being written."""

from __future__ import annotations

import datetime
import json
from dataclasses import dataclass
from pathlib import Path


def stamp(text: str) -> float:
    return datetime.datetime.fromisoformat(text).timestamp()


@dataclass
class Tail:
    """The complete JSON lines appended to a file since the last read."""
    path: Path
    offset: int = 0

    def read(self) -> list[dict]:
        if not self.path.exists():
            return []
        with self.path.open("rb") as stream:
            stream.seek(self.offset)
            data = stream.read()
        end = data.rfind(b"\n") + 1
        self.offset += end
        return [json.loads(line) for line in data[:end].splitlines() if line.strip()]


def merge(events: list[dict], calls: list[dict]) -> list[dict]:
    """Events and calls in time order; each item gets t (epoch seconds) and kind ("event" or "call")."""
    items = [{**e, "kind": "event", "t": stamp(e["ts"])} for e in events]
    items += [{**c, "kind": "call", "t": stamp(c["ts"])} for c in calls]
    return sorted(items, key=lambda item: item["t"])


def load(folder: Path) -> list[dict]:
    return merge(Tail(folder / "events.jsonl").read(), Tail(folder / "calls.jsonl").read())
