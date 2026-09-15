"""Model-visible tool definitions kept separate from execution policy."""

from __future__ import annotations

SYSTEM_STATUS_TOOL = {
    "type": "function",
    "name": "system_status",
    "description": "Obtém informações básicas do computador local, sem alterar o sistema.",
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    },
    "strict": True,
}


def model_tools() -> list[dict[str, object]]:
    """Return only tools that the orchestrator currently exposes to the model."""
    return [SYSTEM_STATUS_TOOL.copy()]
