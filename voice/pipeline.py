"""
AURA Voice Pipeline.

Flow:

audio/text
    ↓
STT
    ↓
wake-word handling
    ↓
AURAAgent
    ↓
TTS
    ↓
spoken response

The pipeline is runtime-independent and can therefore be tested
in Google Colab before Android microphone/speaker integration.
"""

from dataclasses import dataclass
from typing import Any, Optional

from .stt.base import (
    SpeechToText,
    STTResult,
)

from .tts.base import (
    TextToSpeech,
    TTSResult,
)

from .wakeword.detector import (
    WakeWordDetector,
)


@dataclass
class VoicePipelineResult:
    success: bool
    input_text: str = ""
    response_text: str = ""
    message: str = ""
    stt: Optional[STTResult] = None
    tts: Optional[TTSResult] = None
    agent_response: Any = None


class VoicePipeline:
    """
    Connects STT, AURAAgent and TTS.
    """

    def __init__(
        self,
        agent,
        stt: SpeechToText,
        tts: TextToSpeech,
        wakeword: Optional[
            WakeWordDetector
        ] = None,
        require_wake_word: bool = False,
    ):

        self.agent = agent
        self.stt = stt
        self.tts = tts
        self.wakeword = (
            wakeword
            if wakeword is not None
            else WakeWordDetector()
        )
        self.require_wake_word = (
            require_wake_word
        )

    def process(
        self,
        audio: Any,
        confirmed: bool = False,
    ) -> VoicePipelineResult:

        stt_result = self.stt.transcribe(
            audio
        )

        if not stt_result.success:

            return VoicePipelineResult(
                success=False,
                message=stt_result.message,
                stt=stt_result,
            )

        text = stt_result.text.strip()

        if self.require_wake_word:

            if not self.wakeword.detect(text):

                return VoicePipelineResult(
                    success=False,
                    input_text=text,
                    message="Wake word not detected.",
                    stt=stt_result,
                )

            text = self.wakeword.strip_wake_word(
                text
            )

            if not text:

                return VoicePipelineResult(
                    success=False,
                    input_text=stt_result.text,
                    message="Wake word detected but no command followed.",
                    stt=stt_result,
                )

        agent_response = self.agent.run(
            text,
            confirmed=confirmed,
        )

        response_text = (
            agent_response.message
            if agent_response is not None
            else ""
        )

        if not response_text:

            return VoicePipelineResult(
                success=False,
                input_text=text,
                message="AURA returned an empty response.",
                stt=stt_result,
                agent_response=agent_response,
            )

        tts_result = self.tts.speak(
            response_text
        )

        if not tts_result.success:

            return VoicePipelineResult(
                success=False,
                input_text=text,
                response_text=response_text,
                message=tts_result.message,
                stt=stt_result,
                tts=tts_result,
                agent_response=agent_response,
            )

        return VoicePipelineResult(
            success=bool(
                agent_response.success
            ),
            input_text=text,
            response_text=response_text,
            message="Voice pipeline completed.",
            stt=stt_result,
            tts=tts_result,
            agent_response=agent_response,
        )
