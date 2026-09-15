"""Short-lived approval requests for confirm-risk tools."""

from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from time import monotonic
from uuid import uuid4

DEFAULT_TTL_SECONDS = 300.0


@dataclass(frozen=True)
class ApprovalRequest:
    request_id: str
    tool: str
    arguments: dict[str, object]
    description: str
    expires_at: float


class ApprovalStore:
    """In-memory approval queue with single-use, time-limited requests."""

    def __init__(self, ttl_seconds: float = DEFAULT_TTL_SECONDS) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be greater than zero")
        self._ttl_seconds = ttl_seconds
        self._requests: dict[str, ApprovalRequest] = {}
        self._lock = Lock()

    def _purge_expired(self, now: float) -> None:
        expired = [request_id for request_id, request in self._requests.items() if request.expires_at <= now]
        for request_id in expired:
            self._requests.pop(request_id, None)

    def create(self, tool: str, arguments: dict[str, object], description: str) -> ApprovalRequest:
        now = monotonic()
        request = ApprovalRequest(
            uuid4().hex,
            tool,
            dict(arguments),
            description,
            now + self._ttl_seconds,
        )
        with self._lock:
            self._purge_expired(now)
            self._requests[request.request_id] = request
        return request

    def pop(self, request_id: str) -> ApprovalRequest | None:
        now = monotonic()
        with self._lock:
            self._purge_expired(now)
            return self._requests.pop(request_id, None)
