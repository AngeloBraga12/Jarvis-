"""Small deterministic command router used by the local UI foundation."""

from __future__ import annotations

from app.core.agent import Agent


STATUS_TERMS = ("status", "sistema", "computador", "pc", "recursos")


def handle_command(command: str, agent: Agent) -> dict[str, object]:
    """Route only safe, explicitly supported commands in the foundation UI."""
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

    return {
        "ok": True,
        "message": "Recebi o comando. O núcleo de linguagem ainda será conectado nesta etapa.",
        "supported": False,
    }
