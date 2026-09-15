"""Tests for the provider-neutral voice foundation."""

import platform

import pytest

from app.voice_base import SpeechToTextProvider, TextToSpeechProvider
from app.voice_capabilities import detect_capabilities


class DummySTT(SpeechToTextProvider):
    def transcribe(self, audio: bytes) -> str:
        return "teste"


class DummyTTS(TextToSpeechProvider):
    def speak(self, text: str) -> None:
        return None


def test_voice_interfaces_are_implementable() -> None:
    assert DummySTT().transcribe(b"audio") == "teste"
    assert DummyTTS().speak("resposta") is None


def test_capability_detection_does_not_activate_devices() -> None:
    capabilities = detect_capabilities()
    assert capabilities["platform"] == platform.system()
    assert capabilities["microphone_active_by_default"] is False
    assert capabilities["push_to_talk"] is True
    assert capabilities["wake_word"] is False


def test_native_adapters_are_not_claimed_until_installed() -> None:
    capabilities = detect_capabilities()
    assert capabilities["native_stt"] is False
    assert capabilities["native_tts"] is False


def test_abstract_voice_provider_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        SpeechToTextProvider()  # type: ignore[abstract]
    with pytest.raises(TypeError):
        TextToSpeechProvider()  # type: ignore[abstract]
