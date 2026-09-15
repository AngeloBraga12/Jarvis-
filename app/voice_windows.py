"""Optional Windows voice adapters."""

from __future__ import annotations

import platform

from app.voice_base import TextToSpeechProvider


class WindowsSapiTTS(TextToSpeechProvider):
    """Offline Windows SAPI5 text-to-speech through pyttsx3."""

    name = "windows-sapi5"

    def __init__(self) -> None:
        if platform.system() != "Windows":
            raise RuntimeError("Windows SAPI5 is available only on Windows")
        try:
            import pyttsx3
        except ImportError as exc:
            raise RuntimeError("Install the Windows voice extra to enable SAPI5") from exc
        self._engine = pyttsx3.init("sapi5")

    def speak(self, text: str) -> None:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text must be a non-empty string")
        if len(text) > 2000:
            raise ValueError("text exceeds the voice output limit")
        self._engine.say(text)
        self._engine.runAndWait()

    def stop(self) -> None:
        """Stop the current utterance and clear the local speech queue."""
        self._engine.stop()
