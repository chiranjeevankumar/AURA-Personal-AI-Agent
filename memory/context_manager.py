
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
        max_items: int = 20
    ):

        if max_items < 1:
            raise ValueError(
                "max_items must be at least 1"
            )

        self.max_items = max_items
        self._items: List[ContextItem] = []

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
