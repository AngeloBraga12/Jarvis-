"""Minimal permission-aware orchestration core."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.core.audit import AuditLog
from app.core.permissions import Risk, risk_for
from app.tools.system import system_status


@dataclass(frozen=True)
class ToolDecision:
    allowed: bool
    requires_approval: bool
    risk: Risk
    reason: str


class Agent:
    def __init__(self, audit: AuditLog | None = None) -> None:
        self.audit = audit or AuditLog()

    def authorize(self, tool_name: str, approved: bool = False) -> ToolDecision:
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
            return {
                "ok": False,
                "error": decision.reason,
                "requires_approval": decision.requires_approval,
                "risk": decision.risk.value,
            }

        if tool_name == "system_status":
            result = system_status()
        else:
            raise NotImplementedError(f"Tool not implemented: {tool_name}")

        self.audit.record("tool_execution", tool=tool_name, success=True)
        return {"ok": True, "result": result}
