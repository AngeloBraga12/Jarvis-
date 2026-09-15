"""Model-visible tool definitions kept separate from execution policy."""

from __future__ import annotations

CURRENT_TIME_TOOL = {
    "type": "function",
    "name": "current_time",
    "description": "Obtém a data e hora da máquina local, sem alterar o sistema.",
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    },
    "strict": True,
}

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

SYSTEM_HEALTH_TOOL = {
    "type": "function",
    "name": "system_health",
    "description": "Obtém métricas técnicas somente leitura do computador, sem alterar o sistema.",
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    },
    "strict": True,
}

OPEN_APPLICATION_TOOL = {
    "type": "function",
    "name": "open_application",
    "description": "Solicita a abertura de um aplicativo previamente permitido. Exige aprovação explícita do usuário.",
    "parameters": {
        "type": "object",
        "properties": {
            "application": {
                "type": "string",
                "enum": ["notepad", "calculator", "explorer"],
                "description": "Aplicativo permitido que será aberto.",
            },
        },
        "required": ["application"],
        "additionalProperties": False,
    },
    "strict": True,
}


def model_tools() -> list[dict[str, object]]:
    """Return only explicitly approved model-visible tools."""
    return [
        CURRENT_TIME_TOOL.copy(),
        SYSTEM_STATUS_TOOL.copy(),
        SYSTEM_HEALTH_TOOL.copy(),
        OPEN_APPLICATION_TOOL.copy(),
    ]
