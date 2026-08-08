
"""
AURA Memory Manager

High-level memory interface for the AURA agent.

The agent should interact with this class instead of directly
reading or writing memory files.
"""

from typing import Optional, List, Dict, Any

from memory.local_store import LocalMemoryStore
from memory.models import MemoryItem, ShortTermItem


class MemoryManager:

    def __init__(
        self,
        store: Optional[LocalMemoryStore] = None
    ):

        self.store = store or LocalMemoryStore()

    # ========================================================
    # REMEMBER
    # ========================================================

    def remember(
        self,
        content: str,
        memory_type: str = "fact",
        importance: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> MemoryItem:

        return self.store.save_memory(
            content=content,
            memory_type=memory_type,
            importance=importance,
            metadata=metadata
        )

    # ========================================================
    # RECALL
    # ========================================================

    def recall(
        self,
        query: str,
        limit: int = 5
    ) -> List[MemoryItem]:

        return self.store.search_memories(
            query=query,
            limit=limit
        )

    # ========================================================
    # ALL MEMORIES
    # ========================================================

    def memories(
        self,
        limit: Optional[int] = None
    ) -> List[MemoryItem]:

        return self.store.list_memories(
            limit=limit
        )

    # ========================================================
    # FORGET
    # ========================================================

    def forget(
        self,
        memory_id: str
    ) -> bool:

        return self.store.delete_memory(
            memory_id
        )

    # ========================================================
    # SHORT-TERM CONTEXT
    # ========================================================

    def remember_recent(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ShortTermItem:

        return self.store.add_short_term(
            content=content,
            metadata=metadata
        )

    def recent(
        self,
        limit: int = 20
    ) -> List[ShortTermItem]:

        return self.store.get_short_term(
            limit=limit
        )

    def clear_recent(self):

        self.store.clear_short_term()
