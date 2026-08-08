
"""
AURA Local Memory Store

A simple local JSON-backed memory database.

No cloud service.
No API.
No subscription.

Designed as the first memory backend.

Later we can replace the storage engine without changing
the rest of AURA's memory interface.
"""

import json
import uuid

from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from memory.models import (
    MemoryItem,
    ShortTermItem
)


class LocalMemoryStore:

    def __init__(
        self,
        storage_directory: str = "/content/AURA/memory/data"
    ):

        self.storage_directory = Path(
            storage_directory
        )

        self.storage_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.long_term_file = (
            self.storage_directory
            / "long_term.json"
        )

        self.short_term_file = (
            self.storage_directory
            / "short_term.json"
        )

        self._initialize_files()

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def _initialize_files(self):

        if not self.long_term_file.exists():

            self._write_json(
                self.long_term_file,
                []
            )

        if not self.short_term_file.exists():

            self._write_json(
                self.short_term_file,
                []
            )

    # ========================================================
    # TIME
    # ========================================================

    def _now(self):

        return datetime.now(
            timezone.utc
        ).isoformat()

    # ========================================================
    # JSON
    # ========================================================

    def _read_json(
        self,
        file_path: Path
    ):

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):

            return []

    def _write_json(
        self,
        file_path: Path,
        data
    ):

        temporary = file_path.with_suffix(
            file_path.suffix + ".tmp"
        )

        with open(
            temporary,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False
            )

        temporary.replace(
            file_path
        )

    # ========================================================
    # LONG-TERM MEMORY
    # ========================================================

    def save_memory(
        self,
        content: str,
        memory_type: str = "fact",
        importance: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> MemoryItem:

        if not content or not content.strip():

            raise ValueError(
                "Memory content cannot be empty."
            )

        importance = max(
            0.0,
            min(1.0, float(importance))
        )

        now = self._now()

        item = MemoryItem(
            id=str(uuid.uuid4()),
            content=content.strip(),
            memory_type=memory_type,
            created_at=now,
            updated_at=now,
            importance=importance,
            metadata=metadata or {}
        )

        memories = self._read_json(
            self.long_term_file
        )

        memories.append(
            item.__dict__
        )

        self._write_json(
            self.long_term_file,
            memories
        )

        return item

    def get_memory(
        self,
        memory_id: str
    ) -> Optional[MemoryItem]:

        memories = self._read_json(
            self.long_term_file
        )

        for item in memories:

            if item.get("id") == memory_id:

                return MemoryItem(
                    **item
                )

        return None

    def search_memories(
        self,
        query: str,
        limit: int = 10
    ) -> List[MemoryItem]:

        if not query or not query.strip():

            return []

        query_words = set(
            query.lower().split()
        )

        memories = self._read_json(
            self.long_term_file
        )

        scored = []

        for item in memories:

            content = item.get(
                "content",
                ""
            ).lower()

            words = set(
                content.split()
            )

            overlap = len(
                query_words.intersection(words)
            )

            if overlap > 0:

                scored.append(
                    (
                        overlap,
                        float(
                            item.get(
                                "importance",
                                0.5
                            )
                        ),
                        item
                    )
                )

        scored.sort(
            key=lambda x: (
                x[0],
                x[1]
            ),
            reverse=True
        )

        return [
            MemoryItem(**item)
            for _, _, item in scored[:limit]
        ]

    def list_memories(
        self,
        limit: Optional[int] = None
    ) -> List[MemoryItem]:

        memories = self._read_json(
            self.long_term_file
        )

        memories = [
            MemoryItem(**item)
            for item in memories
        ]

        memories.reverse()

        if limit is not None:

            memories = memories[:limit]

        return memories

    def delete_memory(
        self,
        memory_id: str
    ) -> bool:

        memories = self._read_json(
            self.long_term_file
        )

        original_count = len(
            memories
        )

        memories = [
            item
            for item in memories
            if item.get("id") != memory_id
        ]

        self._write_json(
            self.long_term_file,
            memories
        )

        return len(memories) != original_count

    # ========================================================
    # SHORT-TERM MEMORY
    # ========================================================

    def add_short_term(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ShortTermItem:

        if not content or not content.strip():

            raise ValueError(
                "Short-term memory cannot be empty."
            )

        item = ShortTermItem(
            id=str(uuid.uuid4()),
            content=content.strip(),
            created_at=self._now(),
            metadata=metadata or {}
        )

        memories = self._read_json(
            self.short_term_file
        )

        memories.append(
            item.__dict__
        )

        self._write_json(
            self.short_term_file,
            memories
        )

        return item

    def get_short_term(
        self,
        limit: int = 20
    ) -> List[ShortTermItem]:

        memories = self._read_json(
            self.short_term_file
        )

        memories.reverse()

        memories = memories[:limit]

        return [
            ShortTermItem(**item)
            for item in memories
        ]

    def clear_short_term(self):

        self._write_json(
            self.short_term_file,
            []
        )
