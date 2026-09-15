"""Read-only system diagnostics."""

from __future__ import annotations

import os
import platform
import shutil
import time


def _gb(value: int) -> float:
    return round(value / 1024**3, 2)


def system_status() -> dict[str, object]:
    """Return non-sensitive local runtime diagnostics."""
    disk = shutil.disk_usage(os.getcwd())
    return {
        "os": platform.platform(),
        "hostname": platform.node(),
        "cpu_count": os.cpu_count(),
        "disk_free_gb": _gb(disk.free),
        "disk_total_gb": _gb(disk.total),
    }


def system_health() -> dict[str, object]:
    """Return read-only health metrics without collecting user content."""
    disk = shutil.disk_usage(os.getcwd())
    load_average: tuple[float, float, float] | None = None
    try:
        load_average = tuple(round(value, 2) for value in os.getloadavg())
    except (AttributeError, OSError):
        pass

    return {
        "os": platform.system(),
        "release": platform.release(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "disk_free_gb": _gb(disk.free),
        "disk_total_gb": _gb(disk.total),
        "uptime_seconds": round(time.monotonic()),
        "load_average": load_average,
    }
