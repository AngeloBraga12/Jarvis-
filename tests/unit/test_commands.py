from app.core.agent import Agent
from app.core.commands import handle_command


def test_status_command_uses_safe_tool() -> None:
    result = handle_command("mostre o status do sistema", Agent())
    assert result["ok"] is True
    assert "Sistema operacional" in result["message"]
    assert result["result"]["ok"] is True


def test_unknown_command_does_not_execute_a_tool() -> None:
    result = handle_command("apague meus arquivos", Agent())
    assert result["ok"] is True
    assert result["supported"] is False
    assert "ainda será conectado" in result["message"]
