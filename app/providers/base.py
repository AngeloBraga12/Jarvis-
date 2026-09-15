"""Provider contract for JARVIS language models."""

from __future__ import annotations

from abc import ABC, abstractmethod


class LLMProviderError(RuntimeError):
    """Expected provider failure that can be safely surfaced to the orchestrator."""


class LLMProvider(ABC):
    """Small provider interface so the agent is not coupled to one vendor."""

    @abstractmethod
    def respond(self, conversation: list[dict[str, str]]) -> str:
        """Generate one assistant response from the supplied conversation."""
        raise NotImplementedError
