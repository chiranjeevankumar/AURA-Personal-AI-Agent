"""
AURA Speech-to-Text foundation.
"""

from .base import (
    STTResult,
    SpeechToText,
)

from .offline import (
    OfflineSpeechToText,
)

__all__ = [
    "STTResult",
    "SpeechToText",
    "OfflineSpeechToText",
]
