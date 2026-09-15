"""Security tests for the explicit approval boundary."""

from app.core.agent import Agent
from app.core.permissions import Risk


def test_confirm_tool_never_executes_without_approval(tmp_path) -> None:
    agent = Agent()
    agent.audit.path = tmp_path / "audit.jsonl"

    decision = agent.authorize("open_application")
    assert decision.allowed is False
    assert decision.requires_approval is True
    assert decision.risk is Risk.CONFIRM

    result = agent.run("open_application", application="notepad")
    assert result["ok"] is False
    assert result["error"] == "approval_required"
    assert result["approval"]["tool"] == "open_application"


def test_dangerous_tool_cannot_be_approved(tmp_path) -> None:
    agent = Agent()
    agent.audit.path = tmp_path / "audit.jsonl"

    result = agent.run("execute_command", command="echo blocked", approved=True)
    assert result["ok"] is False
    assert result["risk"] == "dangerous"
    assert result["requires_approval"] is False


def test_approval_is_single_use(tmp_path) -> None:
    agent = Agent()
    agent.audit.path = tmp_path / "audit.jsonl"

    pending = agent.run("open_application", application="notepad")
    request_id = pending["approval"]["request_id"]

    denied = agent.deny(request_id)
    assert denied["ok"] is True
    assert agent.deny(request_id)["error"] == "approval_not_found"
