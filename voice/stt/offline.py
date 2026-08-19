"""
Offline/dry-run STT implementation.

This implementation does not access a microphone.
It accepts text supplied by the caller and represents the
result as if STT had produced it.

This is useful for:
- Colab development
- unit testing
- Android integration testing
- zero-cost development
"""

from typing import Any

from .base import (
    STTResult,
    SpeechToText,
)


class OfflineSpeechToText(
    SpeechToText
):
    """
    Dependency-free STT test adapter.
    """

    name = "offline_stt"

    def transcribe(
        self,
        audio: Any
    ) -> STTResult:

        if audio is None:

            return STTResult(
                success=False,
                message="No audio input supplied.",
            )

        if isinstance(
            audio,
            str
        ):

            text = audio.strip()

            if not text:

                return STTResult(
                    success=False,
                    message="Speech input was empty.",
                )

            return STTResult(
                success=True,
                text=text,
                confidence=1.0,
                message="Offline STT text input accepted.",
                data={
                    "engine": self.name,
                    "mode": "dry_run",
                },
            )

        return STTResult(
            success=False,
            message=(
                "Offline STT expects text input during "
                "Colab development."
            ),
        )
