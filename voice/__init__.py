"""
AURA Voice subsystem.

Day 3 provides runtime-independent STT/TTS/wake-word
interfaces and the voice-to-agent pipeline.
"""

from .pipeline import (
    VoicePipeline,
    VoicePipelineResult,
)

from .stt import (
    STTResult,
    SpeechToText,
    OfflineSpeechToText,
)

from .tts import (
    TTSResult,
    TextToSpeech,
    OfflineTextToSpeech,
)

from .wakeword import (
    WakeWordDetector,
)

__all__ = [
    "VoicePipeline",
    "VoicePipelineResult",
    "STTResult",
    "SpeechToText",
    "OfflineSpeechToText",
    "TTSResult",
    "TextToSpeech",
    "OfflineTextToSpeech",
    "WakeWordDetector",
]
