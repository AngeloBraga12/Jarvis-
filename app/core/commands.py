"""Command router for deterministic tools and the language-model conversation."""

from typing import TYPE_CHECKING

from app.core.conversation import Conversation
from app.providers.base import LLMProviderError

if TYPE_CHECKING:
    from app.core.agent import Agent
    from app.providers.base import LLMProvider


STATUS_TERMS = ("status", "sistema", "computador", "pc", "recursos")


def handle_command(
    command: str,
    agent: "Agent",
    provider: "LLMProvider | None" = None,
    conversation: Conversation | None = None,
) -> dict[str, object]:
    """Route safe commands first, then delegate natural language to the LLM."""
    normalized = " ".join(command.casefold().split())
    if not normalized:
        return {"ok": False, "message": "Não recebi nenhum comando."}

    if any(term in normalized for term in STATUS_TERMS):
        result = agent.run("system_status")
        if result.get("ok"):
            system = result["result"]
            return {
                "ok": True,
                "message": (
                    f"Sistema operacional {system['os']}. "
                    f"Host {system['hostname']}. "
                    f"{system['cpu_count']} núcleos de CPU disponíveis."
                ),
                "result": result,
            }

    if provider is None:
        return {
            "ok": False,
            "message": "O núcleo de linguagem não está configurado. Defina OPENAI_API_KEY no ambiente do JARVIS.",
            "error": "llm_not_configured",
        }

    session = conversation or Conversation()
    try:
        messages = session.snapshot_with_user(command)
        response = provider.respond(messages)
        session.append_turn(command, response)
    except LLMProviderError as exc:
        agent.audit.record("llm_error", error=type(exc).__name__)
        return {
            "ok": False,
            "message": "Não consegui consultar o núcleo de linguagem agora.",
            "error": "llm_request_failed",
        }

    agent.audit.record("llm_response", model=getattr(provider, "model", "unknown"))
    return {"ok": True, "message": response, "source": "llm"}
