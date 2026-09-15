"""Command router for deterministic commands and permissioned language-model tools."""

import json
from typing import TYPE_CHECKING

from app.core.conversation import Conversation
from app.core.tool_registry import model_tools
from app.providers.base import LLMProviderError

if TYPE_CHECKING:
    from app.core.agent import Agent
    from app.providers.base import LLMProvider


STATUS_TERMS = ("status", "sistema", "computador", "pc", "recursos")


def _run_model_tools(
    response: object,
    calls: list[dict[str, object]],
    agent: "Agent",
) -> tuple[list[dict[str, str]], list[dict[str, object]]]:
    """Execute safe calls and collect confirmation requests without bypassing policy."""
    outputs: list[dict[str, str]] = []
    approvals: list[dict[str, object]] = []
    for call in calls:
        name = call.get("name")
        call_id = call.get("call_id")
        arguments = call.get("arguments")
        if not isinstance(name, str) or not isinstance(call_id, str):
            continue
        if not isinstance(arguments, dict):
            arguments = {}
        agent.audit.record("model_tool_request", tool=name)
        result = agent.run(name, **arguments)
        if isinstance(result, dict) and result.get("requires_approval"):
            approval = result.get("approval")
            if isinstance(approval, dict):
                approvals.append(approval)
        outputs.append(
            {
                "type": "function_call_output",
                "call_id": call_id,
                "output": json.dumps(result, ensure_ascii=False, default=str),
            }
        )
        agent.audit.record(
            "model_tool_result",
            tool=name,
            ok=bool(result.get("ok")) if isinstance(result, dict) else False,
        )
    return outputs, approvals


def handle_command(
    command: str,
    agent: "Agent",
    provider: "LLMProvider | None" = None,
    conversation: Conversation | None = None,
) -> dict[str, object]:
    """Route deterministic commands, then allow the model to request approved tools."""
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
        request_with_tools = getattr(provider, "request_with_tools", None)
        approvals: list[dict[str, object]] = []
        if callable(request_with_tools):
            response, calls = request_with_tools(messages, model_tools())
            if calls:
                tool_outputs, approvals = _run_model_tools(response, calls, agent)
                response_text = provider.respond_to_tool_results(response, tool_outputs)
            else:
                response_text = response.output_text.strip()
        else:
            response_text = provider.respond(messages)
        if not response_text:
            raise LLMProviderError("The language model returned an empty response")
        session.append_turn(command, response_text)
    except LLMProviderError as exc:
        agent.audit.record("llm_error", error=type(exc).__name__)
        return {
            "ok": False,
            "message": "Não consegui consultar o núcleo de linguagem agora.",
            "error": "llm_request_failed",
        }

    agent.audit.record("llm_response", model=getattr(provider, "model", "unknown"))
    result: dict[str, object] = {"ok": True, "message": response_text, "source": "llm"}
    if approvals:
        result["approval_required"] = approvals
    return result
