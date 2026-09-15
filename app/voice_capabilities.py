"""Voice capability detection."""

from __future__ import annotations

import platform


def detect_capabilities() -> dict[str, object]:
    """Report voice targets without opening audio devices."""
    return {
        "platform": platform.system(),
        "native_stt": False,
        "native_tts": False,
        "browser_stt_fallback": True,
        "browser_tts_fallback": True,
        "push_to_talk": True,
        "wake_word": False,
        "microphone_active_by_default": False,
    }
