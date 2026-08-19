"""
AURA Text-to-Speech foundation.
"""

from .base import (
    TTSResult,
    TextToSpeech,
)

from .offline import (
    OfflineTextToSpeech,
)

__all__ = [
    "TTSResult",
    "TextToSpeech",
    "OfflineTextToSpeech",
]
