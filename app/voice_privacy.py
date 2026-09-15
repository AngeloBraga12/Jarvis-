"""Explicit voice privacy policy used by future native adapters."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VoicePrivacy:
    """Safe defaults for microphone and speech processing."""

    microphone_opt_in: bool = True
    continuous_capture: bool = False
    store_audio: bool = False
    wake_word_enabled: bool = False

    def allows_capture(self, *, explicit_interaction: bool) -> bool:
        """Allow audio capture only for an explicit interaction."""
        return self.microphone_opt_in and explicit_interaction and not self.continuous_capture

    def allows_wake_word(self) -> bool:
        """Wake-word processing remains disabled until explicitly enabled."""
        return self.wake_word_enabled and not self.store_audio
