"""
Speech-to-Text interfaces for AURA.

The Android layer will eventually provide real microphone/audio
input. This module deliberately keeps the core independent from
Android-specific APIs.
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class STTResult:
    """
    Result returned by a speech-to-text engine.
    """

    success: bool
    text: str = ""
    confidence: float = 0.0
    message: str = ""
    data: Optional[dict[str, Any]] = None


class SpeechToText:
    """
    Abstract STT interface.
    """

    name = "speech_to_text"

    def transcribe(
        self,
        audio: Any
    ) -> STTResult:
        raise NotImplementedError(
            "A concrete STT engine must implement transcribe()."
        )
