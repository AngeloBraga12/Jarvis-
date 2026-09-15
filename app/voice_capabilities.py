"""Voice capability detection."""

from __future__ import annotations

import importlib.util
import platform


def _module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def detect_capabilities() -> dict[str, object]:
    """Report voice targets without opening audio devices."""
    windows = platform.system() == "Windows"
    native_tts = windows and _module_available("pyttsx3")
    native_stt = windows and _module_available("winrt")
    return {
        "platform": platform.system(),
        "native_stt": native_stt,
        "native_tts": native_tts,
        "browser_stt_fallback": True,
        "browser_tts_fallback": True,
        "push_to_talk": True,
        "wake_word": False,
        "microphone_active_by_default": False,
        "audio_storage": False,
    }
