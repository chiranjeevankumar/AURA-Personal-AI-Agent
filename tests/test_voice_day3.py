"""
AURA Day-3 Voice Foundation Tests.
"""

from brain.agent import AURAAgent
from tools.registry import ToolRegistry

from voice.stt import (
    OfflineSpeechToText,
)

from voice.tts import (
    OfflineTextToSpeech,
)

from voice.wakeword import (
    WakeWordDetector,
)

from voice.pipeline import (
    VoicePipeline,
)


def make_agent():

    registry = ToolRegistry()

    return AURAAgent(
        registry=registry
    )


def test_stt():

    stt = OfflineSpeechToText()

    result = stt.transcribe(
        "hello aura"
    )

    assert result.success
    assert result.text == "hello aura"
    assert result.confidence == 1.0


def test_stt_empty():

    stt = OfflineSpeechToText()

    result = stt.transcribe(
        ""
    )

    assert not result.success


def test_tts():

    tts = OfflineTextToSpeech()

    result = tts.speak(
        "Hello from AURA"
    )

    assert result.success
    assert result.text == "Hello from AURA"


def test_tts_empty():

    tts = OfflineTextToSpeech()

    result = tts.speak(
        ""
    )

    assert not result.success


def test_wake_word():

    detector = WakeWordDetector()

    assert detector.detect(
        "Hey AURA what time is it"
    )

    assert detector.detect(
        "aura open youtube"
    )

    assert not detector.detect(
        "open youtube"
    )


def test_wake_word_strip():

    detector = WakeWordDetector()

    result = detector.strip_wake_word(
        "Hey AURA open youtube"
    )

    assert result == "open youtube"


def test_voice_pipeline_memory():

    agent = make_agent()

    pipeline = VoicePipeline(
        agent=agent,
        stt=OfflineSpeechToText(),
        tts=OfflineTextToSpeech(),
        require_wake_word=True,
    )

    result = pipeline.process(
        "Hey AURA remember that my project is called AURA"
    )

    assert result.stt is not None
    assert result.tts is not None
    assert result.input_text.startswith(
        "remember"
    )
    assert result.agent_response is not None
    assert result.agent_response.success


def test_voice_pipeline_recall():

    agent = make_agent()

    first = VoicePipeline(
        agent=agent,
        stt=OfflineSpeechToText(),
        tts=OfflineTextToSpeech(),
        require_wake_word=True,
    )

    save_result = first.process(
        "Hey AURA remember that voice testing works"
    )

    assert save_result.agent_response.success

    recall_result = first.process(
        "Hey AURA what do you remember about voice testing"
    )

    assert recall_result.agent_response.success
    assert "voice testing works" in (
        recall_result.response_text.lower()
    )


def test_pipeline_rejects_missing_wake_word():

    agent = make_agent()

    pipeline = VoicePipeline(
        agent=agent,
        stt=OfflineSpeechToText(),
        tts=OfflineTextToSpeech(),
        require_wake_word=True,
    )

    result = pipeline.process(
        "open youtube"
    )

    assert not result.success
    assert result.message == "Wake word not detected."
