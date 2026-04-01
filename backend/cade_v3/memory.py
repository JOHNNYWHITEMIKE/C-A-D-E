from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass(slots=True)
class MemoryEntry:
    topic: str
    content: str
    confidence: float
    created_at: datetime = field(default_factory=datetime.utcnow)


class SharedMemory:
    """Simple append-only shared memory for cross-agent learning."""

    def __init__(self) -> None:
        self._entries: List[MemoryEntry] = []

    def add(self, topic: str, content: str, confidence: float = 0.8) -> None:
        self._entries.append(MemoryEntry(topic=topic, content=content, confidence=confidence))

    def query(self, topic: str, limit: int = 5) -> List[MemoryEntry]:
        matches = [entry for entry in reversed(self._entries) if topic.lower() in entry.topic.lower()]
        return matches[:limit]

    def snapshot(self) -> Dict[str, int]:
        topics: Dict[str, int] = {}
        for entry in self._entries:
            topics[entry.topic] = topics.get(entry.topic, 0) + 1
        return topics
