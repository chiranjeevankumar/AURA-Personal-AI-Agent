
"""
AURA Memory Tools

Tools exposed to the Agent Executor.

The actual storage is handled by MemoryManager.
"""

from memory.manager import MemoryManager


class MemoryTools:

    def __init__(
        self,
        memory_manager: MemoryManager
    ):

        self.memory = memory_manager

    # ========================================================
    # REMEMBER
    # ========================================================

    def remember(
        self,
        memory: str
    ):

        saved = self.memory.remember(
            content=memory,
            memory_type="user_memory",
            importance=0.8
        )

        return {
            "success": True,
            "message": (
                f"Memory saved: {saved.content}"
            ),
            "memory_id": saved.id
        }

    # ========================================================
    # RECALL
    # ========================================================

    def recall(
        self,
        query: str
    ):

        results = self.memory.recall(
            query=query,
            limit=5
        )

        memories = [
            item.content
            for item in results
        ]

        return {
            "success": True,
            "message": (
                " | ".join(memories)
                if memories
                else "No matching memories found."
            ),
            "memories": memories
        }
