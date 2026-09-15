"""Permission-aware orchestration core."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.core.approvals import ApprovalStore
from app.core.audit import AuditLog
from app.core.permissions import TOOL_RISK, Risk, risk_for
from app.tools.apps import open_application
from app.tools.safe import current_time
from app.tools.system import system_status


@dataclass(frozen=True)
class ToolDecision:
    allowed: bool
    requires_approval: bool
    risk: Risk
    reason: str


class Agent:
    def __init__(
        self,
        audit: AuditLog | None = None,
        approvals: ApprovalStore | None = None,
    ) -> None:
        self.audit = audit or AuditLog()
        self.approvals = approvals or ApprovalStore()

    def authorize(self, tool_name: str, approved: bool = False) -> ToolDecision:
        if tool_name not in TOOL_RISK:
            decision = ToolDecision(False, False, Risk.DANGEROUS, "unknown tool blocked")
        else:
            risk = risk_for(tool_name)
            if risk is Risk.SAFE:
                decision = ToolDecision(True, False, risk, "safe tool")
            elif risk is Risk.CONFIRM:
                decision = ToolDecision(approved, not approved, risk, "explicit approval required")
            else:
                decision = ToolDecision(False, False, risk, "dangerous tool blocked by default")
        self.audit.record("authorization", tool=tool_name, **decision.__dict__)
        return decision

    def run(self, tool_name: str, *, approved: bool = False, **kwargs: Any) -> Any:
        decision = self.authorize(tool_name, approved)
        if not decision.allowed:
            if decision.requires_approval:
                request = self.approvals.create(
                    tool_name,
                    kwargs,
                    f"Autorizar {tool_name} com os argumentos fornecidos?",
                )
                self.audit.record("approval_requested", tool=tool_name, request_id=request.request_id)
                return {
                    "ok": False,
                    "error": "approval_required",
                    "requires_approval": True,
                    "risk": decision.risk.value,
                    "approval": {
                        "request_id": request.request_id,
                        "tool": request.tool,
                        "description": request.description,
                        "arguments": request.arguments,
                    },
                }
            return {
                "ok": False,
                "error": decision.reason,
                "requires_approval": decision.requires_approval,
                "risk": decision.risk.value,
            }

        if tool_name == "system_status":
            result = system_status()
        elif tool_name == "current_time":
            result = current_time()
        elif tool_name == "open_application":
            result = open_application(**kwargs)
        else:
            raise RuntimeError("registered tool has no execution handler")

        self.audit.record("tool_execution", tool=tool_name, success=True)
        return {"ok": True, "result": result}

    def approve(self, request_id: str) -> Any:
        """Consume one pending request and execute it exactly once."""
        request = self.approvals.pop(request_id)
        if request is None:
            return {"ok": False, "error": "approval_not_found"}
        self.audit.record("approval_granted", tool=request.tool, request_id=request.request_id)
        return self.run(request.tool, approved=True, **request.arguments)

    def deny(self, request_id: str) -> dict[str, object]:
        """Consume one pending request without executing it."""
        request = self.approvals.pop(request_id)
        if request is None:
            return {"ok": False, "error": "approval_not_found"}
        self.audit.record("approval_denied", tool=request.tool, request_id=request.request_id)
        return {"ok": True, "status": "denied", "tool": request.tool}
