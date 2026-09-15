"""OpenAI Responses API provider used by the local JARVIS service."""

from __future__ import annotations

import os

from openai import OpenAI, OpenAIError

from app.providers.base import LLMProvider, LLMProviderError

DEFAULT_MODEL = "gpt-5.6-luna"
DEFAULT_INSTRUCTIONS = (
    "Você é JARVIS, um assistente pessoal local. Responda em português do Brasil, "
    "de forma clara, direta e natural. Não invente ações executadas no computador. "
    "Nesta fase você conversa e interpreta comandos; ferramentas do sistema só devem "
    "ser usadas quando o núcleo de permissões as autorizar explicitamente."
)


class OpenAIProvider(LLMProvider):
    """Minimal, server-side OpenAI provider with no client-side secret exposure."""

    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        instructions: str = DEFAULT_INSTRUCTIONS,
    ) -> None:
        if not api_key.strip():
            raise ValueError("OPENAI_API_KEY is empty")
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.instructions = instructions

    @classmethod
    def from_env(cls) -> OpenAIProvider | None:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            return None
        return cls(
            api_key=api_key,
            model=os.getenv("JARVIS_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL,
        )

    def respond(self, conversation: list[dict[str, str]]) -> str:
        try:
            response = self.client.responses.create(
                model=self.model,
                instructions=self.instructions,
                input=conversation,
                store=False,
            )
        except OpenAIError as exc:
            raise LLMProviderError("OpenAI request failed") from exc

        text = response.output_text.strip()
        if not text:
            raise LLMProviderError("The language model returned an empty response")
        return text
