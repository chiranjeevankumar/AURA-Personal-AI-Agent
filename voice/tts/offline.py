"""
Offline/dry-run TTS implementation.

No external service and no paid API are required.
"""

from .base import (
    TTSResult,
    TextToSpeech,
)


class OfflineTextToSpeech(
    TextToSpeech
):
    """
    Dependency-free TTS test adapter.

    It returns the text that a real Android TTS engine
    will eventually speak.
    """

    name = "offline_tts"

    def synthesize(
        self,
        text: str
    ) -> TTSResult:

        if text is None:

            return TTSResult(
                success=False,
                message="No text supplied.",
            )

        text = str(text).strip()

        if not text:

            return TTSResult(
                success=False,
                message="Text-to-speech input was empty.",
            )

        return TTSResult(
            success=True,
            text=text,
            message="Offline TTS synthesis prepared.",
            audio=None,
            data={
                "engine": self.name,
                "mode": "dry_run",
                "requires_android_output": True,
            },
        )
