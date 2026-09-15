"""Permission policy for JARVIS tools."""

from enum import Enum


class Risk(str, Enum):
    SAFE = "safe"
    CONFIRM = "confirm"
    DANGEROUS = "dangerous"


TOOL_RISK: dict[str, Risk] = {
    "system_status": Risk.SAFE,
    "current_time": Risk.SAFE,
    "open_application": Risk.CONFIRM,
    "read_file": Risk.CONFIRM,
    "write_file": Risk.CONFIRM,
    "execute_command": Risk.DANGEROUS,
    "delete_file": Risk.DANGEROUS,
}


def risk_for(tool_name: str) -> Risk:
    """Return the risk class for a tool; unknown tools fail closed."""
    return TOOL_RISK.get(tool_name, Risk.CONFIRM)
