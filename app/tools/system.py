"""Read-only system diagnostics."""

from __future__ import annotations

import os
import platform
import shutil


def system_status() -> dict[str, object]:
    """Return non-sensitive local runtime diagnostics."""
    disk = shutil.disk_usage(os.getcwd())
    return {
        "os": platform.platform(),
        "hostname": platform.node(),
        "cpu_count": os.cpu_count(),
        "disk_free_gb": round(disk.free / 1024**3, 2),
        "disk_total_gb": round(disk.total / 1024**3, 2),
    }
