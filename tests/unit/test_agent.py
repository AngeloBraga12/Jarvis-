from app.core.agent import Agent
from app.core.permissions import Risk


def test_safe_tool_runs() -> None:
    result = Agent().run("system_status")
    assert result["ok"] is True


def test_confirm_tool_is_blocked_without_approval() -> None:
    result = Agent().run("read_file")
    assert result["ok"] is False
    assert result["requires_approval"] is True
    assert result["risk"] == Risk.CONFIRM.value


def test_dangerous_tool_is_blocked() -> None:
    result = Agent().run("execute_command", approved=True)
    assert result["ok"] is False
    assert result["risk"] == Risk.DANGEROUS.value
