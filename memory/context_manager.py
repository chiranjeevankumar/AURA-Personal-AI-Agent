
"""
AURA Conversation Context Manager.

Stores recent conversational context locally in memory.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


@dataclass
class ContextItem:

    role: str
    content: str
    data: Dict[str, Any] = field(default_factory=dict)

    timestamp: str = field(
        default_factory=lambda:
        datetime.now(timezone.utc).isoformat()
    )


class ConversationContext:

    def __init__(
        self,
        max_items: int = 20,
        memory_manager=None
    ):

        if max_items < 1:
            raise ValueError(
                "max_items must be at least 1"
            )

        self.max_items = max_items
        self.memory_manager = memory_manager
        self._items: List[ContextItem] = []

        # ----------------------------------------------------
        # Restore persisted conversational context.
        # ----------------------------------------------------

        if self.memory_manager is not None:

            persisted = self.memory_manager.recent(
                limit=max_items
            )

            for stored in reversed(persisted):

                metadata = stored.metadata or {}

                # Only restore records explicitly written by
                # ConversationContext itself.
                if not metadata.get(
                    "conversation_context",
                    False
                ):
                    continue

                self._items.append(
                    ContextItem(
                        role=metadata.get(
                            "role",
                            "assistant"
                        ),
                        content=stored.content,
                        data=metadata.get(
                            "data",
                            {}
                        ),
                        timestamp=metadata.get(
                            "timestamp",
                            stored.created_at
                        )
                    )
                )

    def add(
        self,
        role: str,
        content: str,
        data: Optional[Dict[str, Any]] = None
    ) -> ContextItem:

        item = ContextItem(
            role=role,
            content=content,
            data=data or {}
        )

        self._items.append(item)

        # ----------------------------------------------------
        # Persist context when a memory manager is available.
        # ----------------------------------------------------

        if self.memory_manager is not None:

            self.memory_manager.remember_recent(
                content=item.content,
                metadata={
                    "conversation_context": True,
                    "role": item.role,
                    "data": item.data,
                    "timestamp": item.timestamp,
                }
            )

        if len(self._items) > self.max_items:

            self._items = self._items[
                -self.max_items:
            ]

        return item

    def add_user(
        self,
        content: str,
        data: Optional[Dict[str, Any]] = None
    ):

        return self.add(
            "user",
            content,
            data
        )

    def add_assistant(
        self,
        content: str,
        data: Optional[Dict[str, Any]] = None
    ):

        return self.add(
            "assistant",
            content,
            data
        )

    def add_system(
        self,
        content: str,
        data: Optional[Dict[str, Any]] = None
    ):

        return self.add(
            "system",
            content,
            data
        )

    def recent(
        self,
        limit: Optional[int] = None
    ):

        if limit is None:
            return list(self._items)

        if limit < 0:
            raise ValueError(
                "limit cannot be negative"
            )

        return self._items[-limit:]

    def last_user(self):

        for item in reversed(self._items):

            if item.role == "user":
                return item

        return None

    def last_assistant(self):

        for item in reversed(self._items):

            if item.role == "assistant":
                return item

        return None

    def last_action(self):

        for item in reversed(self._items):

            if (
                item.data.get("type")
                == "action_result"
            ):

                return item

        return None

    def clear(self):

        self._items.clear()

    def __len__(self):

        return len(self._items)
