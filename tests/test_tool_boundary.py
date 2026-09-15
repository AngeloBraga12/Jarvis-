"""Security tests for the model-to-tool permission boundary."""

from app.core.agent import Agent
from app.core.commands import handle_command
from app.core.conversation import Conversation
from app.core.tool_registry import model_tools
from app.providers.base import LLMProvider


class ToolCallingProvider(LLMProvider):
    model = "test-model"

    def __init__(self, calls: list[dict[str, object]]) -> None:
        self.calls = calls
        self.tool_requests: list[list[dict[str, object]]] = []

    def respond(self, conversation: list[dict[str, str]]) -> str:
        return "fallback"

    def request_with_tools(self, conversation, tools):
        self.tool_requests.append(tools)
        return type("Response", (), {"output_text": "", "output": []})(), self.calls

    def respond_to_tool_results(self, response, tool_outputs):
        return "Ferramenta executada com segurança."


def test_model_sees_only_registered_tools() -> None:
    tools = model_tools()
    names = {tool["name"] for tool in tools}
    assert names == {"system_status", "current_time", "open_application"}
    assert all(tool["name"] not in {"execute_command", "delete_file"} for tool in tools)


def test_unknown_tool_is_blocked_without_approval(tmp_path) -> None:
    agent = Agent()
    agent.audit.path = tmp_path / "audit.jsonl"

    result = agent.run("unknown_tool", value="blocked")

    assert result["ok"] is False
    assert result["requires_approval"] is False
    assert result["error"] == "unknown tool blocked"


def test_dangerous_tool_is_blocked_even_if_model_requests_it(tmp_path) -> None:
    agent = Agent()
    agent.audit.path = tmp_path / "audit.jsonl"
    result = agent.run("execute_command", command="whoami")

    assert result["ok"] is False
    assert result["risk"] == "dangerous"
    assert result["requires_approval"] is False


def test_model_tool_request_cannot_bypass_permission_boundary(tmp_path) -> None:
    agent = Agent()
    agent.audit.path = tmp_path / "audit.jsonl"
    provider = ToolCallingProvider(
        [
            {
                "name": "execute_command",
                "call_id": "call-dangerous",
                "arguments": {"command": "whoami"},
            }
        ]
    )

    result = handle_command("execute uma tarefa", agent, provider, Conversation())

    assert result["ok"] is True
    assert result["message"] == "Ferramenta executada com segurança."
    audit = (tmp_path / "audit.jsonl").read_text(encoding="utf-8")
    assert "whoami" not in audit
