"""Short-lived approval requests for confirm-risk tools."""

from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from uuid import uuid4


@dataclass(frozen=True)
class ApprovalRequest:
    request_id: str
    tool: str
    arguments: dict[str, object]
    description: str


class ApprovalStore:
    """In-memory, single-process approval queue. Requests never persist to disk."""

    def __init__(self) -> None:
        self._requests: dict[str, ApprovalRequest] = {}
        self._lock = Lock()

    def create(self, tool: str, arguments: dict[str, object], description: str) -> ApprovalRequest:
        request = ApprovalRequest(uuid4().hex, tool, dict(arguments), description)
        with self._lock:
            self._requests[request.request_id] = request
        return request

    def pop(self, request_id: str) -> ApprovalRequest | None:
        with self._lock:
            return self._requests.pop(request_id, None)
