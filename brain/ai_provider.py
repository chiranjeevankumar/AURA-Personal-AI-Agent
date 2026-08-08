
"""
AURA AI Provider Interface

This module defines a common interface for AI understanding.

AURA itself does not depend on one specific AI provider.

Possible future providers:

    Local model
    Free API
    Rule-based fallback
    Other compatible providers

Every provider should return a structured result.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class AIUnderstandingResult:
    """
    Standard result returned by an AI provider.
    """

    success: bool

    intent: str = "unknown"

    parameters: Dict[str, Any] = field(
        default_factory=dict
    )

    confidence: float = 0.0

    explanation: str = ""

    raw_response: Optional[Any] = None

    provider: str = "unknown"


class AIProvider(ABC):
    """
    Base interface for every AURA AI provider.
    """

    name: str = "unknown"

    @abstractmethod
    def understand(
        self,
        text: str
    ) -> AIUnderstandingResult:
        """
        Convert natural language into structured intent.
        """
        raise NotImplementedError

    def is_available(self) -> bool:
        """
        Check whether the provider is currently usable.
        """
        return True

    def describe(self) -> str:
        """
        Human-readable provider description.
        """
        return self.name


class FallbackProvider(AIProvider):
    """
    Minimal provider used when no external/local AI is available.

    It intentionally does not pretend to be a real AI model.
    It provides a safe fallback result.
    """

    name = "fallback"

    def understand(
        self,
        text: str
    ) -> AIUnderstandingResult:

        return AIUnderstandingResult(
            success=False,
            intent="unknown",
            parameters={
                "original_text": text
            },
            confidence=0.0,
            explanation=(
                "No AI provider is currently available."
            ),
            provider=self.name
        )
