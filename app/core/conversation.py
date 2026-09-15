"""Bounded in-memory conversation state for the local JARVIS session."""

from __future__ import annotations

from threading import Lock

MAX_MESSAGES = 20


class Conversation:
    """Keep a short local session without persisting user prompts to disk."""

    def __init__(self, max_messages: int = MAX_MESSAGES) -> None:
        self._messages: list[dict[str, str]] = []
        self._max_messages = max(2, max_messages)
        self._lock = Lock()

    def snapshot_with_user(self, text: str) -> list[dict[str, str]]:
        with self._lock:
            return [*self._messages, {"role": "user", "content": text}]

    def append_turn(self, user: str, assistant: str) -> None:
        with self._lock:
            self._messages.extend(
                [
                    {"role": "user", "content": user},
                    {"role": "assistant", "content": assistant},
                ]
            )
            if len(self._messages) > self._max_messages:
                self._messages = self._messages[-self._max_messages :]

    def clear(self) -> None:
        with self._lock:
            self._messages.clear()
