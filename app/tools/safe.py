"""Small read-only tools that do not modify the user's machine."""

from __future__ import annotations

from datetime import UTC, datetime


def current_time() -> dict[str, str]:
    """Return the local machine time and UTC time without exposing other data."""
    now = datetime.now().astimezone()
    return {
        "local": now.isoformat(timespec="seconds"),
        "utc": datetime.now(UTC).isoformat(timespec="seconds"),
    }
