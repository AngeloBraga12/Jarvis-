"""Provider-neutral voice interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod


class SpeechToTextProvider(ABC):
    """Convert explicit user speech input into text."""

    name = "abstract-stt"

    @abstractmethod
    def transcribe(self, audio: bytes) -> str:
        """Transcribe one bounded audio segment."""
        raise NotImplementedError


class TextToSpeechProvider(ABC):
    """Convert text into spoken output."""

    name = "abstract-tts"

    @abstractmethod
    def speak(self, text: str) -> None:
        """Speak one bounded response."""
        raise NotImplementedError
