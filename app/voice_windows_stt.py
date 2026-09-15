"""Optional Windows native speech-recognition adapter."""

from __future__ import annotations

import asyncio
import platform

from app.voice_base import SpeechToTextProvider


class WindowsSpeechRecognizer(SpeechToTextProvider):
    """Recognize one explicit, bounded microphone utterance with Windows Speech APIs.

    The Windows Runtime recognizer owns the microphone session. The adapter never
    starts listening during construction and performs exactly one recognition per
    explicit ``recognize_once`` call.
    """

    name = "windows-speech"

    def __init__(self) -> None:
        if platform.system() != "Windows":
            raise RuntimeError("Windows Speech Recognition is available only on Windows")
        try:
            from winrt.windows.media.speechrecognition import SpeechRecognizer
        except ImportError as exc:
            raise RuntimeError(
                "Install the Windows speech extra to enable native speech recognition"
            ) from exc
        self._recognizer_type = SpeechRecognizer

    async def _recognize(self) -> str:
        recognizer = self._recognizer_type()
        await recognizer.CompileConstraintsAsync()
        result = await recognizer.RecognizeAsync()
        status = str(result.Status)
        if not status.endswith("Success"):
            raise RuntimeError(f"Windows speech recognition failed: {status}")
        text = str(result.Text).strip()
        if not text:
            raise RuntimeError("Windows speech recognition returned no text")
        if len(text) > 1000:
            raise RuntimeError("recognized speech exceeds the command limit")
        return text

    def recognize_once(self) -> str:
        """Capture exactly one explicit utterance from the default microphone."""
        return asyncio.run(self._recognize())

    def transcribe(self, audio: bytes) -> str:
        """Reject raw audio because this native provider captures its own session."""
        if not isinstance(audio, bytes):
            raise TypeError("audio must be bytes")
        raise NotImplementedError(
            "Windows native speech recognition captures an explicit microphone session; "
            "use recognize_once() instead of passing raw audio"
        )
