"""Unit tests for the language-model boundary without network access."""

from app.core.agent import Agent
from app.core.commands import handle_command
from app.core.conversation import Conversation
from app.providers.base import LLMProvider


class FakeProvider(LLMProvider):
    model = "test-model"

    def __init__(self) -> None:
        self.calls: list[list[dict[str, str]]] = []

    def respond(self, conversation: list[dict[str, str]]) -> str:
        self.calls.append(conversation)
        return "Resposta de teste do JARVIS."


def test_natural_language_uses_provider_and_preserves_context(tmp_path) -> None:
    provider = FakeProvider()
    conversation = Conversation(max_messages=4)
    agent = Agent()
    agent.audit.path = tmp_path / "audit.jsonl"

    first = handle_command("Olá, JARVIS", agent, provider, conversation)
    second = handle_command("Você lembra do que eu disse?", agent, provider, conversation)

    assert first == {"ok": True, "message": "Resposta de teste do JARVIS.", "source": "llm"}
    assert second["ok"] is True
    assert len(provider.calls) == 2
    assert provider.calls[1][0] == {"role": "user", "content": "Olá, JARVIS"}
    assert provider.calls[1][-1] == {
        "role": "user",
        "content": "Você lembra do que eu disse?",
    }


def test_missing_provider_fails_closed(tmp_path) -> None:
    agent = Agent()
    agent.audit.path = tmp_path / "audit.jsonl"

    result = handle_command("Conte uma piada", agent)

    assert result["ok"] is False
    assert result["error"] == "llm_not_configured"
