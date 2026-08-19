"""
Dependency-free wake-word detector foundation.

This is intentionally a deterministic text detector for Colab.
Real continuous microphone wake-word detection belongs to the
Android runtime layer.
"""


class WakeWordDetector:
    """
    Detect an AURA wake word in supplied text.
    """

    def __init__(
        self,
        wake_words=None
    ):

        if wake_words is None:
            wake_words = [
                "aura",
                "hey aura",
                "ok aura",
            ]

        self.wake_words = tuple(
            word.lower().strip()
            for word in wake_words
            if word and word.strip()
        )

    def detect(
        self,
        text: str
    ) -> bool:

        if not text:
            return False

        normalized = (
            str(text)
            .lower()
            .strip()
        )

        return any(
            word in normalized
            for word in self.wake_words
        )

    def strip_wake_word(
        self,
        text: str
    ) -> str:

        if not text:
            return ""

        result = str(text).strip()

        lowered = result.lower()

        for word in sorted(
            self.wake_words,
            key=len,
            reverse=True
        ):

            if lowered.startswith(word):

                result = result[
                    len(word):
                ].strip()

                break

        return result
