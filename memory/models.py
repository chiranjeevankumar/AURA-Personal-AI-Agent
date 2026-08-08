
"""
AURA Memory Models

Defines the basic structures used by AURA memory.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class MemoryItem:

    id: str

    content: str

    memory_type: str

    created_at: str

    updated_at: str

    importance: float = 0.5

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class ShortTermItem:

    id: str

    content: str

    created_at: str

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )
