"""
Text-to-Speech interfaces for AURA.
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class TTSResult:
    """
    Result returned by a TTS engine.
    """

    success: bool
    text: str = ""
    message: str = ""
    audio: Any = None
    data: Optional[dict[str, Any]] = None


class TextToSpeech:
    """
    Abstract TTS interface.
    """

    name = "text_to_speech"

    def synthesize(
        self,
        text: str
    ) -> TTSResult:

        raise NotImplementedError(
            "A concrete TTS engine must implement synthesize()."
        )

    def speak(
        self,
        text: str
    ) -> TTSResult:

        return self.synthesize(
            text
        )
